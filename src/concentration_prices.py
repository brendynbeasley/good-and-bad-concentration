"""Good or bad concentration: the regressions, tables and figures.

Reads the panels written by build_panel.py and runs:

    1. The paper's Table 3 on public data: five-year changes in prices and markups on
       five-year changes in log CR4, with a post-2002 interaction, sector-by-year fixed
       effects, sales weights and industry-clustered standard errors (windows 1997-2017).
    2. The paper's Table 2 split for manufacturing: TFP, prices and markups on log CR4,
       estimated separately on the 1997-2002 window and on later windows.
    3. Robustness: unweighted, without petroleum refining, and leave-one-industry-out.
    4. The extension: the same price regression on the BEA panel window by window,
       including 2017-2022, which the paper could not see.
    5. A table of named industries.

Run from the repository root, after build_panel.py:
    python src/concentration_prices.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"

PAPER_BREAK = 2002  # the paper's interaction is 1{t > 2002}: windows ending 2007 or later
REFINING_NAICS = "324110"  # petroleum refineries, the largest and most oil-driven industry
COMPUTERS_NAICS = "334111"  # electronic computers, the paper's leading case of good concentration

# The paper's Table 3, columns 1-6 (NBER Working Paper 25983, p. 22): coefficient and SE.
PAPER_T3 = {
    ("dlog_p", "All"): (-0.01, 0.03, 0.17, 0.04, 2083),
    ("dlog_p", "Manufacturing"): (0.05, 0.02, 0.20, 0.06, 1682),
    ("dlog_p", "Non-manufacturing"): (-0.03, 0.04, 0.17, 0.05, 401),
    ("dlog_mu", "All"): (0.02, 0.04, 0.23, 0.06, 2083),
    ("dlog_mu", "Manufacturing"): (0.10, 0.03, 0.13, 0.07, 1682),
    ("dlog_mu", "Non-manufacturing"): (-0.00, 0.05, 0.26, 0.07, 401),
}
# The paper's Table 2 (p. 20), BLS industries, Compustat CR4: pre-2000 and post-2000 slopes.
PAPER_T2 = {"dlog_tfp": (0.186, 0.070, -0.044, 0.051), "dlog_p": (-0.093, 0.069, 0.077, 0.088),
            "dlog_mu": (-0.102, 0.047, 0.116, 0.064)}

# Named industries for the table of real names: (BEA industry, window end, leaders).
# Leaders are each market's well-known firms; the Census does not name companies.
NAMED = [
    ("Electronic computer manufacturing", 2002, "Dell, HP, Compaq, Apple"),
    ("Wireless telecommunications carriers (except satellite)", 2012, "Verizon, AT&T, Sprint, T-Mobile"),
    ("Data processing, hosting, and related services", 2022, "Amazon Web Services, Microsoft, Google"),
    ("Software publishers", 2022, "Microsoft, Oracle, Adobe"),
    ("Air transportation", 2012, "American, Delta, United, Southwest"),
    ("Health and personal care stores", 2007, "CVS, Walgreens, Rite Aid"),
    ("Pharmaceutical preparation manufacturing", 2017, "Pfizer, Merck, Johnson & Johnson, AbbVie"),
    ("Petroleum refineries", 2022, "Marathon, Valero, ExxonMobil, Phillips 66"),
    ("Cement manufacturing", 2022, "Holcim, CEMEX, Heidelberg Materials"),
    ("Veterinary services", 2022, "Mars (Banfield, VCA)"),
    ("Breakfast cereal manufacturing", 2022, "General Mills, Kellogg's, Post, Quaker"),
]


def stars(p):
    return "**" if p < 0.01 else "*" if p < 0.05 else "+" if p < 0.10 else ""


def fit(d, y, rhs, fe, weighted=True, cluster=True):
    """WLS of y on rhs with fixed effects; SEs clustered by industry (or HC1)."""
    cols = [y, "dlog_cr4", "weight", "industry_id"] + [c for c in ["dlog_lp", "dlog_w"] if c in rhs]
    d = d.dropna(subset=cols).copy()
    formula = f"{y} ~ {rhs}" + (f" + C({fe})" if fe and d[fe].nunique() > 1 else "")
    w = d.weight if weighted else np.ones(len(d))
    if cluster and d.industry_id.nunique() < len(d):
        groups = pd.factorize(d.industry_id)[0]
        return smf.wls(formula, d, weights=w).fit(cov_type="cluster", cov_kwds={"groups": groups})
    return smf.wls(formula, d, weights=w).fit(cov_type="HC1")


def coef_row(res, term, **labels):
    lo, hi = res.conf_int().loc[term]
    return dict(labels, term=term, coef=res.params[term], se=res.bse[term], p=res.pvalues[term],
                ci_low=lo, ci_high=hi, n=int(res.nobs), r2=res.rsquared)


def contrast(res, expr):
    """Estimate, SE, p-value and 95% CI of a linear combination of coefficients."""
    g = res.t_test(expr)
    lo, hi = np.ravel(g.conf_int())[:2]
    return dict(coef=float(np.ravel(g.effect)[0]), se=float(np.ravel(g.sd)[0]),
                p=float(np.ravel(g.pvalue)[0]), ci_low=float(lo), ci_high=float(hi), n=int(res.nobs))


def prepare(d):
    d = d.copy()
    d["post"] = (d.t1 > PAPER_BREAK).astype(int)
    d["secyr"] = d.sector.astype(str) + "_" + d.t1.astype(str)
    return d


def load():
    mfg = pd.read_csv(OUT / "panel_mfg.csv", dtype={"naics12": str, "industry_id": str, "sector": str})
    bea = pd.read_csv(OUT / "panel_bea.csv", dtype={"sector": str})
    n6 = pd.read_csv(OUT / "panel_naics6.csv", dtype={"naics0": str, "naics1": str, "sector": str})
    print(f"Loaded panel_mfg ({len(mfg)} rows), panel_bea ({len(bea)} rows), panel_naics6 ({len(n6)} rows)")
    return prepare(mfg), prepare(bea), n6


def replication(mfg, bea):
    """The paper's Table 3: manufacturing at 6-digit NAICS, the rest at BEA detail."""
    non = bea[~bea.mfg & (bea.t1 <= 2017)]
    pooled = pd.concat([mfg, non], ignore_index=True)
    print(f"Replication sample: {len(mfg)} manufacturing + {len(non)} non-manufacturing industry-windows")
    samples = {"All": pooled, "Manufacturing": mfg, "Non-manufacturing": non}
    rows = []
    for y, ctrl in [("dlog_p", " + dlog_lp + dlog_w"), ("dlog_p", ""), ("dlog_mu", "")]:
        for name, d in samples.items():
            res = fit(d, y, "dlog_cr4 + dlog_cr4:post" + ctrl, "secyr")
            spec = "with LP and wage controls" if ctrl else "no controls"
            b, bse, i, ise, n = PAPER_T3[(y, name)]
            for term in ["dlog_cr4", "dlog_cr4:post"]:
                r = coef_row(res, term, outcome=y, sample=name, spec=spec)
                r["paper_coef"] = b if term == "dlog_cr4" else i
                r["paper_se"] = bse if term == "dlog_cr4" else ise
                r["paper_n"] = n
                rows.append(r)
            # Implied post-2002 slope and its SE
            rows.append(dict(outcome=y, sample=name, spec=spec, term="post-2002 slope (sum)",
                             r2=res.rsquared, **contrast(res, "dlog_cr4 + dlog_cr4:post = 0")))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "replication_table3.csv", index=False)
    print("\nTable 3 on public data (coef, SE, stars; paper in brackets):")
    for _, r in t.iterrows():
        paper = f"  [paper {r.paper_coef:+.2f} ({r.paper_se:.2f})]" if pd.notna(r.get("paper_coef")) else ""
        print(f"  {r.outcome:8s} {r['sample']:18s} {r.spec:26s} {r.term:22s} "
              f"{r.coef:+.3f} ({r.se:.3f}){stars(r.p):2s} N={r.n}{paper}")
    return pooled


def split_table(mfg):
    """The paper's Table 2 layout for manufacturing: separate pre and post regressions."""
    rows = []
    for y in ["dlog_tfp", "dlog_p", "dlog_mu"]:
        for period, d in [("1997-2002", mfg[mfg.post == 0]), ("2002-2017", mfg[mfg.post == 1])]:
            for weighted in [True, False]:
                res = fit(d, y, "dlog_cr4", "secyr", weighted=weighted)
                r = coef_row(res, "dlog_cr4", outcome=y, period=period,
                             weights="sales" if weighted else "none")
                pb, pse, qb, qse = PAPER_T2[y]
                r["paper_coef"], r["paper_se"] = (pb, pse) if period == "1997-2002" else (qb, qse)
                rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "mfg_split_table2.csv", index=False)
    print("\nManufacturing, separate regressions (paper's Table 2 layout):")
    for _, r in t.iterrows():
        print(f"  {r.outcome:9s} {r.period}  weights={r.weights:5s} {r.coef:+.3f} ({r.se:.3f}){stars(r.p)} "
              f"N={r.n}  [paper {r.paper_coef:+.3f}]")


def robustness(mfg, pooled):
    rows = []
    rhs = "dlog_cr4 + dlog_cr4:post"
    cases = [
        ("Manufacturing, sales-weighted (baseline)", mfg, True, ""),
        ("Manufacturing, unweighted", mfg, False, ""),
        ("Manufacturing, without petroleum refining", mfg[mfg.naics12 != REFINING_NAICS], True, ""),
        ("Manufacturing, with LP and wage controls", mfg, True, " + dlog_lp + dlog_w"),
        ("Manufacturing, controls, without refining", mfg[mfg.naics12 != REFINING_NAICS], True,
         " + dlog_lp + dlog_w"),
        ("All industries, unweighted", pooled, False, ""),
        ("All industries, without petroleum refining", pooled[pooled.industry_id != REFINING_NAICS], True, ""),
    ]
    for label, d, weighted, ctrl in cases:
        res = fit(d, "dlog_p", rhs + ctrl, "secyr", weighted=weighted)
        rows.append(coef_row(res, "dlog_cr4:post", case=label))
    # The 1997-2002 slope with and without electronic computers
    pre = mfg[mfg.post == 0]
    for label, d in [("Manufacturing 1997-2002 slope, all industries", pre),
                     ("Manufacturing 1997-2002 slope, without electronic computers",
                      pre[pre.naics12 != COMPUTERS_NAICS])]:
        res = fit(d, "dlog_p", "dlog_cr4", "secyr")
        rows.append(coef_row(res, "dlog_cr4", case=label))
    # Leave one manufacturing industry out at a time
    loo = []
    for ind in mfg.industry_id.unique():
        res = fit(mfg[mfg.industry_id != ind], "dlog_p", rhs, "secyr")
        loo.append((ind, res.params["dlog_cr4:post"], res.bse["dlog_cr4:post"],
                    res.pvalues["dlog_cr4:post"], int(res.nobs)))
    loo = pd.DataFrame(loo, columns=["dropped", "coef", "se", "p", "n"])
    for label, i in [("min", loo.coef.idxmin()), ("max", loo.coef.idxmax())]:
        r = loo.loc[i]
        rows.append(dict(case=f"Manufacturing, leave-one-industry-out ({label}), dropping {r.dropped}",
                         term="dlog_cr4:post", coef=r.coef, se=r.se, p=r.p, n=int(r.n)))
    rows.append(dict(case="Manufacturing, leave-one-industry-out, largest p-value", term="dlog_cr4:post",
                     coef=loo.loc[loo.p.idxmax(), "coef"], se=loo.loc[loo.p.idxmax(), "se"],
                     p=loo.p.max(), n=int(loo.loc[loo.p.idxmax(), "n"])))
    # Petroleum refining's share of the manufacturing sample's start-of-window shipments
    share = (mfg[mfg.naics12 == REFINING_NAICS].groupby("t1").weight.sum()
             / mfg.groupby("t1").weight.sum()).rename("refining_share").reset_index()
    share.to_csv(OUT / "refining_share.csv", index=False)
    print("\nPetroleum refining's share of manufacturing shipments by window end:")
    print(share.round(3).to_string(index=False))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "robustness.csv", index=False)
    print("\nRobustness, post-2002 interaction in the price regression:")
    for _, r in t.iterrows():
        se = f"({r.se:.3f})" if pd.notna(r.get("se")) else ""
        print(f"  {r.case:70s} {r.coef:+.3f} {se} p={r.p:.3f}")


def window_slopes(bea, mfg):
    """The extension: one price slope per five-year window, 1997-2002 through 2017-2022."""
    rows = []
    for (t0, t1), d in bea.groupby(["t0", "t1"]):
        for name, dd in [("All", d), ("Manufacturing", d[d.mfg]), ("Non-manufacturing", d[~d.mfg]),
                         ("All, without refining", d[d.bea_title != "Petroleum refineries"]),
                         ("Manufacturing, without refining", d[d.mfg & (d.bea_title != "Petroleum refineries")])]:
            for y in ["dlog_p", "dlog_q"]:
                res = fit(dd, y, "dlog_cr4", "sector", cluster=False)
                r = coef_row(res, "dlog_cr4", panel="BEA detail", window=f"{t0}-{t1}", t1=t1,
                             sample=name, outcome=y)
                r["mean_dlog_cr4"] = np.average(dd.dlog_cr4, weights=dd.weight)
                r["share_rising"] = (dd.dlog_cr4 > 0).mean()
                rows.append(r)
    for (t0, t1), d in mfg.groupby(["t0", "t1"]):
        res = fit(d, "dlog_p", "dlog_cr4", "sector", cluster=False)
        r = coef_row(res, "dlog_cr4", panel="NBER-CES 6-digit", window=f"{t0}-{t1}", t1=t1,
                     sample="Manufacturing", outcome="dlog_p")
        r["mean_dlog_cr4"] = np.average(d.dlog_cr4, weights=d.weight)
        r["share_rising"] = (d.dlog_cr4 > 0).mean()
        rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "window_slopes.csv", index=False)
    print("\nPrice slope by window (sector FE, sales-weighted, HC1):")
    p = t[t.outcome == "dlog_p"].pivot_table(index="window", columns=["panel", "sample"], values="coef")
    print(p.round(3).to_string())

    # Pooled BEA regression with separate interactions for 2002-2017 and 2017-2022
    b = bea.copy()
    b["mid"] = ((b.t1 > PAPER_BREAK) & (b.t1 <= 2017)).astype(int)
    b["late"] = (b.t1 == 2022).astype(int)
    rows = []
    for name, d in [("All", b), ("Manufacturing", b[b.mfg]), ("Non-manufacturing", b[~b.mfg])]:
        res = fit(d, "dlog_p", "dlog_cr4 + dlog_cr4:mid + dlog_cr4:late", "secyr")
        for term in ["dlog_cr4", "dlog_cr4:mid", "dlog_cr4:late"]:
            rows.append(coef_row(res, term, sample=name))
        rows.append(dict(sample=name, term="late minus mid",
                         **contrast(res, "dlog_cr4:late - dlog_cr4:mid = 0")))
    e = pd.DataFrame(rows)
    e.to_csv(OUT / "extension_pooled.csv", index=False)
    print("\nBEA panel pooled, interactions for 2002-2017 (mid) and 2017-2022 (late):")
    for _, r in e.iterrows():
        print(f"  {r['sample']:18s} {r.term:16s} {r.coef:+.3f} ({r.se:.3f}){stars(r.p)} N={r.n}")
    return t


def markups_by_window(n6, mfg):
    """Markup over unit labor cost, sales / payroll, from Census where payroll is published."""
    d = n6.dropna(subset=["payroll0", "payroll1"]).copy()
    d = d[(d.payroll0 > 0) & (d.payroll1 > 0)]
    d["dlog_mu"] = np.log((d.sales1 / d.payroll1) / (d.sales0 / d.payroll0))
    d["weight"], d["industry_id"] = d.sales0, d.naics1
    rows = []
    for (t0, t1), g in d.groupby(["t0", "t1"]):
        for name, gg in [("Manufacturing", g[g.mfg]), ("Non-manufacturing", g[~g.mfg])]:
            if len(gg) < 30:
                continue
            res = fit(gg, "dlog_mu", "dlog_cr4", "sector", cluster=False)
            rows.append(coef_row(res, "dlog_cr4", source="Census 6-digit", window=f"{t0}-{t1}",
                                 sample=name))
    for (t0, t1), g in mfg.groupby(["t0", "t1"]):
        res = fit(g, "dlog_mu", "dlog_cr4", "sector", cluster=False)
        rows.append(coef_row(res, "dlog_cr4", source="NBER-CES 6-digit", window=f"{t0}-{t1}",
                             sample="Manufacturing"))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "markup_windows.csv", index=False)
    print("\nMarkup (sales/payroll) slope by window:")
    print(t[["source", "sample", "window", "coef", "se", "n"]].round(3).to_string(index=False))


def named_table(bea):
    med = bea.groupby("t1").apply(lambda g: np.average(g.dlog_p, weights=g.weight)).rename("avg_dlog_p")
    rows = []
    for title, t1, leaders in NAMED:
        r = bea[(bea.bea_title == title) & (bea.t1 == t1)]
        if r.empty:
            print(f"  (named industry not in panel: {title} {t1})")
            continue
        r = r.iloc[0]
        rows.append(dict(industry=title, leaders=leaders, window=f"{r.t0}-{r.t1}", cr4_start=r.cr4_0,
                         cr4_end=r.cr4_1, dlog_cr4=r.dlog_cr4, price_change_pct=100 * np.expm1(r.dlog_p),
                         all_industry_price_change_pct=100 * np.expm1(med[t1]),
                         output_change_pct=100 * np.expm1(r.dlog_q), gross_output_start_bn=r.go0 / 1000))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "named_industries.csv", index=False)
    print("\nNamed industries:")
    print(t[["industry", "window", "cr4_start", "cr4_end", "price_change_pct",
             "all_industry_price_change_pct"]].round(1).to_string(index=False))


def worked_examples(bea, mfg):
    """Numbers for the README's worked examples and its three-row CR4 table."""
    rows = []
    for title in ["Breakfast cereal manufacturing", "Cement manufacturing", "Offices of physicians"]:
        r = bea[(bea.bea_title == title) & (bea.t1 == 2022)].iloc[0]
        rows.append(dict(example="CR4 in 2022", item=title, value=r.cr4_1))
    r = bea[(bea.bea_title == "Cement manufacturing") & (bea.t1 == 2022)].iloc[0]
    rows += [dict(example="Cement 2017-2022", item=k, value=v) for k, v in
             [("cr4_2017", r.cr4_0), ("cr4_2022", r.cr4_1), ("dlog_cr4", r.dlog_cr4),
              ("dlog_price", r.dlog_p), ("price_change_pct", 100 * np.expm1(r.dlog_p))]]
    r = mfg[(mfg.naics12 == "325412") & (mfg.t1 == 2017)].iloc[0]
    rows += [dict(example="Pharmaceutical preparations 2012-2017 (NBER-CES)", item=k, value=v) for k, v in
             [("shipments_2012_musd", r.vship_0), ("payroll_2012_musd", r.pay_0),
              ("shipments_2017_musd", r.vship_1), ("payroll_2017_musd", r.pay_1),
              ("markup_2012", r.vship_0 / r.pay_0), ("markup_2017", r.vship_1 / r.pay_1),
              ("dlog_markup", r.dlog_mu), ("dlog_price", r.dlog_p), ("dlog_cr4", r.dlog_cr4)]]
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "worked_examples.csv", index=False)
    print("\nWorked examples:")
    print(t.round(4).to_string(index=False))


def figures(slopes, mfg):
    s = slopes[(slopes.outcome == "dlog_p") & (slopes.panel == "BEA detail")]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    styles = {"Manufacturing": ("#1f5f99", -0.12), "Non-manufacturing": ("#c4652a", 0.12)}
    for name, (color, dx) in styles.items():
        g = s[s["sample"] == name].sort_values("t1")
        x = np.arange(len(g)) + dx
        ax.errorbar(x, g.coef, yerr=[g.coef - g.ci_low, g.ci_high - g.coef], fmt="o", color=color,
                    capsize=4, label=name, lw=1.5)
    ax.axhline(0, color="#555555", lw=0.8)
    ax.axvline(0.5, color="#999999", lw=0.8, ls="--")
    ax.axvline(3.5, color="#999999", lw=0.8, ls=":")
    ax.set_xticks(range(5))
    ax.set_xticklabels(sorted(s.window.unique()))
    ax.text(0.55, ax.get_ylim()[1] * 0.92, "paper's post-2002 period", fontsize=8, color="#555555")
    ax.text(3.55, ax.get_ylim()[1] * 0.92, "new data", fontsize=8, color="#555555")
    ax.set_ylabel("Price change per unit change in log CR4")
    ax.set_title("How much prices rose with concentration, by five-year window (95% CI)")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "slopes_by_window.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True)
    periods = [("the 1997-2002 window", mfg[mfg.post == 0]), ("the three windows, 2002-2017", mfg[mfg.post == 1])]
    for ax, (label, d) in zip(axes, periods):
        size = 400 * d.weight / mfg.weight.max()
        ax.scatter(d.dlog_cr4, d.dlog_p, s=size.clip(lower=3), alpha=0.45, color="#1f5f99", lw=0)
        res = fit(d, "dlog_p", "dlog_cr4", "secyr")  # same slope as results/mfg_split_table2.csv
        slope = res.params["dlog_cr4"]
        xbar, ybar = np.average(d.dlog_cr4, weights=d.weight), np.average(d.dlog_p, weights=d.weight)
        xs = np.linspace(-0.6, 0.6, 50)
        ax.plot(xs, ybar + slope * (xs - xbar), color="#c4652a", lw=2)
        hidden = int(((d.dlog_p.abs() > 1) | (d.dlog_cr4.abs() > 0.7)).sum())
        ax.set_xlim(-0.7, 0.7)
        ax.set_ylim(-1.0, 1.0)
        ax.axhline(0, color="#999999", lw=0.6)
        ax.axvline(0, color="#999999", lw=0.6)
        ax.set_title(f"Manufacturing, {label}\nweighted slope {slope:+.2f} ({hidden} points off the chart)")
        ax.set_xlabel("Five-year change in log CR4")
    axes[0].set_ylabel("Five-year change in log price")
    fig.tight_layout()
    fig.savefig(OUT / "mfg_scatter.png", dpi=150)
    plt.close(fig)
    print("\nWrote results/slopes_by_window.png and results/mfg_scatter.png")


def main():
    mfg, bea, n6 = load()
    pooled = replication(mfg, bea)
    split_table(mfg)
    robustness(mfg, pooled)
    slopes = window_slopes(bea, mfg)
    markups_by_window(n6, mfg)
    named_table(bea)
    worked_examples(bea, mfg)
    figures(slopes, mfg)


if __name__ == "__main__":
    main()
