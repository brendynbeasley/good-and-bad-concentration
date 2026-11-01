"""Build the industry panels for the Covarrubias, Gutierrez & Philippon (2020) rerun.

The paper relates five-year changes in an industry's four-firm concentration ratio (CR4)
to five-year changes in its prices, productivity and markups, before and after 2002.
This script assembles the same ingredients from public files:

    Concentration  Economic Census CR4 for 6-digit NAICS industries, 1997-2022
    Manufacturing  NBER-CES Manufacturing Industry Database (prices, TFP, payroll), to 2018
    All industries BEA underlying-detail gross output price and quantity indexes, 1997-2025

Each five-year window pairs two adjacent Censuses. An industry enters a window only if
its NAICS code maps one-to-one across that Census pair in the official concordance, so
every change compares the same industry with itself.

Outputs (results/):
    panel_naics6.csv  one row per 6-digit industry and window (CR4, sales, payroll)
    panel_mfg.csv     manufacturing rows merged with NBER-CES outcomes (windows to 2017)
    panel_bea.csv     one row per BEA detail industry and window, with BEA prices

Run from the repository root:
    python src/build_panel.py
"""

import re
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# pandas notes that its default Excel readers will change; the files read the same either way.
warnings.filterwarnings("ignore", message=".*engine.*")
# Markups use np.where on industries without payroll; the unused branch may divide by zero.
np.seterr(divide="ignore", invalid="ignore")

CENSUS_YEARS = [1997, 2002, 2007, 2012, 2017, 2022]
WINDOWS = list(zip(CENSUS_YEARS[:-1], CENSUS_YEARS[1:]))

# Sectors left out: no Census concentration before 2017 (agriculture, mining, utilities,
# construction), imputed BEA prices (finance and insurance), or no meaningful CR4
# (management of companies). Real estate lessors (531) are dropped because BEA prices
# them as housing rents. The paper's non-manufacturing sample has the same coverage.
EXCLUDE_SECTORS = {"11", "21", "22", "23", "52", "55"}
EXCLUDE_PREFIXES = ("531",)

# BEA detail rows whose names are newer than the 2017 input-output concordance;
# their 2017 NAICS codes are taken from the 2017 NAICS manual.
BEA_EXTRA = {
    "Furniture and home furnishings stores": "442",
    "Electronics and appliance stores": "443",
    "Sporting goods, hobby, book, and music stores": "451",
    "Miscellaneous store retailers": "453",
    "Scenic and sightseeing transportation and support activities for transportation": "487, 488",
    "Periodical Publishers": "51112",
    "Community food, housing, and other relief services, including rehabilitation services": "6242, 6243",
    "Automotive repair and maintenance": "8111",
}


def read_dat(zip_path):
    """Read the pipe-delimited .dat table inside a Census zip."""
    with zipfile.ZipFile(zip_path) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".dat")][0]
        df = pd.read_csv(z.open(name), sep="|", dtype=str, encoding="latin-1")
    df.columns = [c.strip().lstrip("#") for c in df.columns]
    return df


def first_col(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None


def num(s):
    return pd.to_numeric(s, errors="coerce")


def tidy_census(df, year):
    """Turn one Census concentration table into rows of (naics, group, sales, cr4, ...)."""
    code = first_col(df, ["NAICS", "NAICS2002", "NAICS2007", "NAICS2012", "NAICS2017", "NAICS2022"])
    if "VSTOP4" in df.columns:  # 1997 manufacturing table is wide, one row per industry
        out = pd.DataFrame({"naics": df[code], "group": "ALL", "sales": num(df["ECVALUE"]),
                            "cr4": num(df["VSTOP4"]), "payroll": np.nan, "emp": np.nan})
    else:
        grp_col = first_col(df, ["OPTAX", "TAXIND", "OPTYPE", "TYPOP"])
        grp = df[grp_col] if grp_col else pd.Series("ALL", index=df.index)
        # The paper keeps taxable firms where a tax split exists, and the wholesale total.
        grp = grp.map({"T": "T", "A": "ALL", "00": "ALL", "ALL": "ALL"})
        cf = df["CONCENFI"].str.strip()
        sales = first_col(df, ["RCPTOT", "ECVALUE"])
        share = first_col(df, ["VAL_PCT", "VALPCT", "CCORCPPCT"])
        pay = first_col(df, ["PAYANN", "PAYANT", "PAY"])
        base = pd.DataFrame({"naics": df[code], "group": grp, "cf": cf,
                             "sales": num(df[sales]), "share": num(df[share]),
                             "payroll": num(df[pay]) if pay else np.nan,
                             "emp": num(df["EMP"]) if "EMP" in df.columns else np.nan})
        allf = base[base.cf.isin(["001", "003", "004"])].drop(columns=["cf", "share"])
        top4 = base[base.cf.isin(["804", "856", "604"])][["naics", "group", "share"]]
        out = allf.merge(top4.rename(columns={"share": "cr4"}), on=["naics", "group"])
    out["naics"] = out["naics"].str.strip()
    out = out[out["naics"].str.fullmatch(r"\d{6}") & out["group"].notna()]
    out = out[(out["cr4"] > 0) & (out["sales"] > 0)].copy()
    out["year"] = year
    return out


def load_census():
    rows = []
    for f in sorted((RAW / "census").glob("*.zip")):
        yy = int(re.match(r"(?:EC|e)(\d{2})", f.name).group(1))
        year = 1900 + yy if yy > 50 else 2000 + yy
        t = tidy_census(read_dat(f), year)
        rows.append(t)
    c = pd.concat(rows, ignore_index=True)
    c = c.drop_duplicates(["year", "naics", "group"])
    before = len(c)
    c = c[~c.naics.str[:2].isin(EXCLUDE_SECTORS) & ~c.naics.str.startswith(EXCLUDE_PREFIXES)]
    print(f"Census: {before} industry-year-group cells with CR4 > 0; "
          f"dropped {before - len(c)} in excluded sectors; kept {len(c)}")
    print(c.groupby("year").naics.nunique().rename("6-digit industries").to_string())
    return c


def load_concordances():
    """Return {(old_year, new_year): DataFrame(old, new)} for each Census pair."""
    files = {(1997, 2002): "1997_NAICS_to_2002_NAICS.xls", (2002, 2007): "2002_to_2007_NAICS.xls",
             (2007, 2012): "2007_to_2012_NAICS.xls", (2012, 2017): "2012_to_2017_NAICS.xlsx",
             (2017, 2022): "2017_to_2022_NAICS.xlsx"}
    conc = {}
    for key, fn in files.items():
        path = RAW / "naics" / fn
        if key == (1997, 2002):
            # A pivot table: 2002 code in column 0 (blank under its first row), 1997 code in column 1
            d = pd.read_excel(path, sheet_name="Sheet1", header=None, skiprows=2).iloc[:, :2]
            d.columns = ["new", "old"]
            d = d[~d.new.astype(str).str.contains("Total")]
            d["new"] = d.new.ffill()
        else:
            d = pd.read_excel(path, header=None, skiprows=3).iloc[:, [0, 2]]
            d.columns = ["old", "new"]
        d = d.dropna().astype({"old": str, "new": str})
        d["old"] = d["old"].str.replace(r"\.0$", "", regex=True).str.strip()
        d["new"] = d["new"].str.replace(r"\.0$", "", regex=True).str.strip()
        d = d[d.old.str.fullmatch(r"\d{6}") & d.new.str.fullmatch(r"\d{6}")].drop_duplicates()
        n_old = d.groupby("old").new.transform("count")
        n_new = d.groupby("new").old.transform("count")
        d["one_to_one"] = (n_old == 1) & (n_new == 1)
        conc[key] = d
        print(f"Concordance {key[0]}->{key[1]}: {len(d)} links, {int(d.one_to_one.sum())} one-to-one")
    return conc


def chain(codes, conc, start, end, strict):
    """Map codes of vintage `start` forward to vintage `end`. Strict keeps 1:1 links only."""
    cur = {c: {c} for c in codes}
    for (a, b), d in conc.items():
        if a < start or b > end:
            continue
        links = d[d.one_to_one] if strict else d
        fwd = links.groupby("old").new.apply(set).to_dict()
        cur = {c: set().union(*[fwd.get(x, set()) for x in s]) if s else set() for c, s in cur.items()}
    return cur


def build_pairs(census, conc):
    """One row per 6-digit industry and window, comparing the industry with itself."""
    out = []
    for t0, t1 in WINDOWS:
        links = conc[(t0, t1)]
        links = links[links.one_to_one][["old", "new"]]
        a = census[census.year == t0].add_suffix("0")
        b = census[census.year == t1].add_suffix("1")
        m = links.merge(a, left_on="old", right_on="naics0").merge(b, left_on="new", right_on="naics1")
        m = m[m.group0 == m.group1]
        # Prefer the taxable-firm series when both Censuses report it (the paper's rule).
        m["pref"] = (m.group0 == "T").astype(int)
        m = m.sort_values("pref", ascending=False).drop_duplicates(["old", "new"])
        n_all = len(links.merge(a, left_on="old", right_on="naics0"))
        m["t0"], m["t1"] = t0, t1
        m["dlog_cr4"] = np.log(m.cr41 / m.cr40)
        m["sector"] = m.new.str[:2]
        m["mfg"] = m.sector.isin(["31", "32", "33"])
        out.append(m)
        print(f"Window {t0}-{t1}: {n_all} industries in {t0} with a 1:1 code; "
              f"{len(m)} matched in {t1} with the same tax group")
    p = pd.concat(out, ignore_index=True)
    keep = ["t0", "t1", "old", "new", "group0", "sector", "mfg", "cr40", "cr41", "dlog_cr4",
            "sales0", "sales1", "payroll0", "payroll1", "emp0", "emp1"]
    return p[keep].rename(columns={"old": "naics0", "new": "naics1", "group0": "group"})


def load_nberces():
    n = pd.read_csv(RAW / "nber" / "nberces5818v1_n2012.csv", dtype={"naics": str})
    n = n[["naics", "year", "vship", "pay", "emp", "piship", "tfp5", "tfp4"]]
    print(f"NBER-CES: {len(n)} industry-years, {n.naics.nunique()} industries, "
          f"{n.year.min()}-{n.year.max()}")
    return n


def build_mfg(pairs, conc, nber):
    """Merge manufacturing pairs with NBER-CES outcomes (windows ending 2017 or earlier).

    NBER-CES is published on 2012 NAICS codes. A Census industry whose code later merged
    into a broader 2012 code is folded into that code, with CR4 changes averaged using
    start-of-window sales as weights (the same rule used for BEA industries below).
    """
    m = pairs[pairs.mfg & (pairs.t1 <= 2017)].copy()
    ids = []
    for _, r in m.iterrows():
        if r.t0 >= 2012:
            ids.append(r.naics0)  # already a 2012 code
        else:
            s = chain([r.naics1], conc, r.t1, 2012, strict=False)[r.naics1]
            ids.append(next(iter(s)) if len(s) == 1 else None)
    m["naics12"] = ids
    before = len(m)
    m = m.dropna(subset=["naics12"])
    m["wcr"] = m.sales0 * m.dlog_cr4
    m["c0"], m["c1"] = m.sales0 * m.cr40, m.sales1 * m.cr41
    m = m.groupby(["naics12", "t0", "t1", "sector"]).agg(
        n_codes=("naics1", "size"), w=("sales0", "sum"), s1=("sales1", "sum"), wcr=("wcr", "sum"),
        c0=("c0", "sum"), c1=("c1", "sum")).reset_index()
    m["dlog_cr4"] = m.wcr / m.w
    m["cr4_0"], m["cr4_1"] = m.c0 / m.w, m.c1 / m.s1
    x0 = nber.add_suffix("_0").rename(columns={"naics_0": "naics12", "year_0": "t0"})
    x1 = nber.add_suffix("_1").rename(columns={"naics_1": "naics12", "year_1": "t1"})
    m = m.merge(x0, on=["naics12", "t0"]).merge(x1, on=["naics12", "t1"])
    m["dlog_p"] = np.log(m.piship_1 / m.piship_0)
    m["dlog_tfp"] = np.log(m.tfp5_1 / m.tfp5_0)
    m["dlog_w"] = np.log((m.pay_1 / m.emp_1) / (m.pay_0 / m.emp_0))
    m["dlog_lp"] = np.log((m.vship_1 / m.piship_1 / m.emp_1) / (m.vship_0 / m.piship_0 / m.emp_0))
    m["dlog_mu"] = np.log((m.vship_1 / m.pay_1) / (m.vship_0 / m.pay_0))
    m["dlog_q"] = np.log((m.vship_1 / m.piship_1) / (m.vship_0 / m.piship_0))
    m["weight"] = m.vship_0  # $ millions, start-of-window shipments
    m["unit"] = "naics6"
    m["industry_id"] = m.naics12
    m["mfg"] = True
    # NBER-CES TFP stops in 2016, so the 2012-2017 window has prices and markups but no TFP.
    good = np.isfinite(m[["dlog_p", "dlog_mu", "dlog_lp", "dlog_cr4"]]).all(axis=1)
    m = m[good].drop(columns=["wcr", "c0", "c1"])
    print(f"Manufacturing panel: {before} Census pairs; {len(m)} industry-windows on 2012 codes "
          f"after merging NBER-CES ({m.naics12.nunique()} industries)")
    print(m.groupby(["t0", "t1"]).size().rename("industries").to_string())
    return m


def load_bea():
    """BEA detail industries with their 2017 NAICS prefixes and annual price/quantity indexes."""
    io = pd.read_excel(RAW / "bea" / "IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx",
                       sheet_name="NAICS Codes", header=None)
    io = io.iloc[5:, [3, 4, 6]].dropna(subset=[3, 4])
    io.columns = ["bea", "title", "naics"]
    io["title"] = io.title.astype(str).str.strip()
    io = io.drop_duplicates("title")
    with zipfile.ZipFile(RAW / "bea" / "UGdpByInd.zip") as z:
        sheets = {s: pd.read_excel(z.open("GrossOutput.xlsx"), sheet_name=s, header=None)
                  for s in ["UGO303-A", "UGO304-A", "UGO305-A"]}
    frames = {}
    for s, g in sheets.items():
        years = g.iloc[7, 3:].astype(int).tolist()
        body = g.iloc[8:, 1:].copy()
        body.columns = ["title", "blank"] + years
        body["title"] = body.title.astype(str).str.strip()
        frames[s] = body.drop(columns="blank").drop_duplicates("title").set_index("title")
    titles = frames["UGO304-A"].index
    lookup = dict(zip(io.title, io.naics.astype(str)))
    codes = dict(zip(io.title, io.bea.astype(str)))
    rows = []
    for t in titles:
        spec = BEA_EXTRA.get(t, lookup.get(t, ""))
        prefixes = []
        for part in re.split(r",\s*", spec):
            mm = re.fullmatch(r"(\d+)-(\d)", part)
            if mm:
                stem, last = mm.group(1)[:-1], int(mm.group(1)[-1])
                prefixes += [stem + str(k) for k in range(last, int(mm.group(2)) + 1)]
            elif re.fullmatch(r"\d+", part):
                prefixes.append(part)
        rows.append({"bea_title": t, "bea_code": codes.get(t, t[:20]), "prefixes": prefixes})
    bea = pd.DataFrame(rows)
    print(f"BEA detail: {len(bea)} industries, {int((bea.prefixes.str.len() > 0).sum())} with NAICS codes")
    return bea, frames


def assign_bea(code2017, bea):
    """Longest-prefix match of a 2017 NAICS code to a BEA detail industry."""
    best, blen = None, 0
    for _, r in bea.iterrows():
        for p in r.prefixes:
            if code2017.startswith(p) and len(p) > blen:
                best, blen = r.bea_title, len(p)
    return best


def build_bea_panel(pairs, conc, bea, frames):
    p = pairs.copy()
    cache = {}
    titles = []
    for _, r in p.iterrows():
        if r.t1 == 2022:
            desc = {r.naics0}
        else:
            desc = chain([r.naics1], conc, r.t1, 2017, strict=False)[r.naics1]
        found = {cache.setdefault(c, assign_bea(c, bea)) for c in desc}
        titles.append(found.pop() if len(found) == 1 else None)
    p["bea_title"] = titles
    print(f"BEA mapping: {p.bea_title.notna().sum()} of {len(p)} industry-windows assigned to one "
          f"BEA industry; {p.bea_title.isna().sum()} dropped (split across BEA industries)")
    p = p.dropna(subset=["bea_title"])
    p["w"] = p.sales0
    p["wcr"] = p.w * p.dlog_cr4
    agg = p.groupby(["bea_title", "t0", "t1"]).agg(
        n_codes=("naics1", "size"), w=("w", "sum"), wcr=("wcr", "sum"),
        sales0=("sales0", "sum"), sales1=("sales1", "sum"), pay0=("payroll0", "sum"),
        pay1=("payroll1", "sum"), emp0=("emp0", "sum"), emp1=("emp1", "sum"),
        mfg=("mfg", "max"), sector=("sector", "first")).reset_index()
    agg["dlog_cr4"] = agg.wcr / agg.w
    lev = p.assign(c0=p.w * p.cr40, c1=p.sales1 * p.cr41).groupby(["bea_title", "t0", "t1"]).agg(
        c0=("c0", "sum"), c1=("c1", "sum"))
    agg = agg.merge(lev.reset_index(), on=["bea_title", "t0", "t1"])
    agg["cr4_0"] = agg.c0 / agg.w
    agg["cr4_1"] = agg.c1 / agg.sales1
    price, qty, go = frames["UGO304-A"], frames["UGO303-A"], frames["UGO305-A"]
    agg["p0"] = [price.loc[t, y] for t, y in zip(agg.bea_title, agg.t0)]
    agg["p1"] = [price.loc[t, y] for t, y in zip(agg.bea_title, agg.t1)]
    agg["q0"] = [qty.loc[t, y] for t, y in zip(agg.bea_title, agg.t0)]
    agg["q1"] = [qty.loc[t, y] for t, y in zip(agg.bea_title, agg.t1)]
    agg["go0"] = [go.loc[t, y] for t, y in zip(agg.bea_title, agg.t0)]
    for c in ["p0", "p1", "q0", "q1", "go0"]:
        agg[c] = pd.to_numeric(agg[c], errors="coerce")
    agg["dlog_p"] = np.log(agg.p1 / agg.p0)
    agg["dlog_q"] = np.log(agg.q1 / agg.q0)
    # Census sales, payroll and employment give the markup over unit labor cost and labor
    # productivity where payroll is published (all non-manufacturing years; 2017 and 2022 in
    # manufacturing).
    has_pay = (agg.pay0 > 0) & (agg.pay1 > 0) & (agg.emp0 > 0) & (agg.emp1 > 0)
    agg["dlog_mu"] = np.where(has_pay, np.log((agg.sales1 / agg.pay1) / (agg.sales0 / agg.pay0)), np.nan)
    agg["dlog_w"] = np.where(has_pay, np.log((agg.pay1 / agg.emp1) / (agg.pay0 / agg.emp0)), np.nan)
    agg["dlog_lp"] = np.where(has_pay, np.log((agg.sales1 / agg.p1 / agg.emp1) /
                                              (agg.sales0 / agg.p0 / agg.emp0)), np.nan)
    agg["weight"] = agg.go0  # BEA gross output, $ millions, start of window
    agg["unit"] = "bea"
    agg["industry_id"] = agg.bea_title
    before = len(agg)
    agg = agg[np.isfinite(agg.dlog_p) & np.isfinite(agg.dlog_cr4) & (agg.weight > 0)]
    print(f"BEA panel: {before} industry-windows; {len(agg)} with prices; "
          f"{agg.bea_title.nunique()} BEA industries")
    print(agg.groupby(["t0", "t1", "mfg"]).size().unstack().to_string())
    return agg.drop(columns=["wcr", "c0", "c1"])


def main():
    OUT.mkdir(exist_ok=True)
    census = load_census()
    conc = load_concordances()
    pairs = build_pairs(census, conc)
    pairs.to_csv(OUT / "panel_naics6.csv", index=False)
    nber = load_nberces()
    mfg = build_mfg(pairs, conc, nber)
    mfg.to_csv(OUT / "panel_mfg.csv", index=False)
    bea, frames = load_bea()
    panel = build_bea_panel(pairs, conc, bea, frames)
    panel.to_csv(OUT / "panel_bea.csv", index=False)
    print("Wrote results/panel_naics6.csv, results/panel_mfg.csv, results/panel_bea.csv")


if __name__ == "__main__":
    main()
