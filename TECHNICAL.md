# Technical notes

This is the technical companion to the [README](README.md). Every number below is written by the scripts in `src/`
to a CSV in `results/`; [results/FINDINGS.md](results/FINDINGS.md) reproduces every table.

## The original study

Matias Covarrubias, Germán Gutiérrez and Thomas Philippon, "From Good to Bad Concentration? US Industries over the
Past 30 Years," *NBER Macroeconomics Annual* 34 (2020), pp. 1–46; NBER Working Paper 25983 (June 2019). The paper's
Table 3 regresses five-year changes in log industry prices and markups on five-year changes in log CR4, with an
interaction for windows ending after 2002, sector-by-year fixed effects, sales weights and industry-clustered
errors. Headline: price slope −0.01 (0.03) before 2002 and interaction 0.17 (0.04), N = 2,083 (manufacturing 0.05 and
0.20, N = 1,682; non-manufacturing −0.03 and 0.17, N = 401); markup interaction 0.23 (0.06). Table 2, on BLS
industries with Compustat CR4, reports a TFP slope of 0.186 (0.070) before 2000 and −0.044 (0.051) after.

## Headline results

| Post-2002 interaction $`\hat\delta`$ | Paper | Rerun, 1997–2017 | N (rerun) |
|---|---|---|---|
| Prices, all industries, with controls | 0.17 (0.04) | 0.129 (0.075) | 1,772 |
| Prices, manufacturing, with controls | 0.20 (0.06) | 0.392 (0.103) | 1,360 |
| Prices, non-manufacturing, with controls | 0.17 (0.05) | −0.030 (0.047) | 412 |
| Markups, all industries | 0.23 (0.06) | 0.112 (0.088) | 1,772 |
| Markups, manufacturing | 0.13 (0.07) | 0.392 (0.113) | 1,360 |
| Markups, non-manufacturing | 0.26 (0.07) | −0.026 (0.109) | 412 |

Extension (BEA panel, all five windows): manufacturing interactions $`\hat\delta_1 = 0.676`$ (0.276) for 2002–2017 and
$`\hat\delta_2 = 0.740`$ (0.301) for 2017–2022, difference 0.064 (0.123), p = 0.60, N = 1,096.

## Data

All files were downloaded on 1 November 2026 and are committed under `data/raw/`.

| File | Source | Contents |
|---|---|---|
| `census/e9731r2.zip` | Census, 1997 Economic Census, sector 31 | Manufacturing CR4, 1997 NAICS |
| `census/EC0231SR12.zip`, `EC0731SR12.zip`, `EC1231SR2.zip` | Census, 2002/2007/2012 sector 31 | Manufacturing CR4 |
| `census/e97NNs6.zip`, `EC02NNSSSZ6.zip`, `EC07NNSSSZ6.zip`, `EC12NNSSSZ6.zip` | Census, sectors 42–81 | Non-manufacturing CR4, sales, payroll, employment |
| `census/EC1700SIZECONCEN.zip`, `EC2200SIZECONCEN.zip` | Census, 2017 and 2022 sector 00 | All sectors: CR4, sales, payroll, employment |
| `naics/*NAICS*.xls(x)` | census.gov/naics/concordances | 1997→2002 through 2017→2022 concordances |
| `nber/nberces5818v1_n2012.csv` | data.nber.org/nberces | NBER-CES, 2012 NAICS, 1958–2018 |
| `bea/UGdpByInd.zip` | apps.bea.gov/industry/Release/ZIP/UGdpByInd.zip (Sept. 2026 release) | Detail gross output, price and quantity indexes, 1997–2025 |
| `bea/IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx` | BEA AllTablesIO.zip | BEA detail codes and their 2017 NAICS codes |

Census flat files are under `www2.census.gov/programs-surveys/economic-census/data/<year>/sector<NN>/`.

## Method

Rules fixed before looking at results:

- Windows pair adjacent Censuses: 1997–2002 (the only pre-2002 window), 2002–2007, 2007–2012, 2012–2017, and the
  extension window 2017–2022. Following the paper, "post" means $`t > 2002`$.
- An industry enters a window only if its 6-digit code is one-to-one in that pair's concordance. Taxable-firm figures
  are used where both Censuses split them (the paper's rule); otherwise all firms. Wholesale uses the total.
- Excluded: sectors 11, 21, 22, 23 (no concentration data before 2017), 52 (imputed BEA prices), 55 (management of
  companies), and NAICS 531 (real estate lessors, priced by BEA as housing rents).
- Manufacturing (Table 3 replication): CR4 changes on Census codes, folded into 2012 NBER-CES codes by sales-weighted
  averaging when a code later merged. Outcomes from NBER-CES: `piship` for prices, `tfp5` for TFP (available
  through 2016, so the 2012–2017 window has no TFP), and shipments over payroll for markups.
- Non-manufacturing: 6-digit Census codes mapped to BEA detail industries by longest 2017-NAICS prefix (dropped if a
  code spans two BEA industries); the BEA-level change is the sales-weighted mean of code-level changes. Prices from
  BEA table UGO304; markups and labor productivity from Census sales, payroll and employment.
- The BEA panel used for the extension treats manufacturing the same way as services, so all five windows use one
  price source.
- Weights are start-of-window shipments (NBER-CES) or gross output (BEA); standard errors are clustered by industry
  in pooled regressions and HC1 in single-window regressions.

The estimating equation for the replication, with $`X_{jt} = (\Delta_5 \log LP_{jt},\ \Delta_5 \log W_{jt})`$ in the
controlled version:

```math
\begin{aligned}
\Delta_5 \log Z_{jt} ={}& \beta\, \Delta_5 \log \text{CR4}_{jt}
+ \delta\, \Delta_5 \log \text{CR4}_{jt}\, \mathbf{1}[t > 2002] \\
&+ \lambda' X_{jt} + \gamma_{s(j),t} + \varepsilon_{jt},
\qquad Z \in \{P,\ \mu\}
\end{aligned}
```

The markup is $`\mu = P/ULC = \text{sales}/\text{payroll}`$, so $`\Delta\log\mu = \Delta\log P - \Delta\log W + \Delta\log LP`$.
The extension replaces the single interaction with $`\delta_1 \mathbf{1}[2002 < t \le 2017]`$ and
$`\delta_2 \mathbf{1}[t = 2022]`$ and tests $`\delta_2 = \delta_1`$.

## Full test statistics

Replication, price regression (`results/replication_table3.csv`):

| Sample | Spec | $`\hat\beta`$ | $`\hat\delta`$ | Post-2002 slope |
|---|---|---|---|---|
| All | controls | 0.040 (0.043) | 0.129 (0.075) | 0.169 (0.053) |
| Manufacturing | controls | 0.065 (0.069) | 0.392 (0.103) | 0.457 (0.100) |
| Non-manufacturing | controls | 0.046 (0.030) | −0.030 (0.047) | 0.015 (0.030) |
| All | none | −0.076 (0.095) | 0.179 (0.113) | 0.104 (0.049) |
| Manufacturing | none | −0.310 (0.263) | 0.621 (0.295) | 0.311 (0.120) |
| Non-manufacturing | none | 0.033 (0.031) | −0.032 (0.047) | 0.001 (0.034) |
| All, markups | none | 0.073 (0.054) | 0.112 (0.088) | 0.185 (0.050) |
| Manufacturing, markups | none | 0.053 (0.050) | 0.392 (0.113) | 0.446 (0.098) |
| Non-manufacturing, markups | none | 0.082 (0.079) | −0.026 (0.109) | 0.056 (0.039) |

Manufacturing split samples (`results/mfg_split_table2.csv`), 1997–2002 then 2002–2017, weighted and unweighted:
TFP 0.304 (0.199) and 0.082 (0.049), unweighted 0.109 (0.054) and 0.059 (0.031); prices −0.310 (0.263) and 0.311
(0.120), unweighted 0.005 (0.052) and 0.075 (0.025); markups 0.053 (0.050) and 0.446 (0.098), unweighted 0.097 (0.038)
and 0.310 (0.043).

Robustness of the manufacturing price interaction (`results/robustness.csv`): unweighted 0.070 (0.063), p = 0.27;
without refining 0.518 (0.301), p = 0.086; controls without refining 0.382 (0.123); leave-one-industry-out range
0.318 (0.137) when electronic computers are dropped to 0.647 (0.307), with the largest p-value 0.086 (dropping
refining). Without computers the weighted 1997–2002 slope is −0.021 (0.047) instead of −0.310. Refining is 4.2% to
14.2% of start-of-window manufacturing shipments (`results/refining_share.csv`).

Window-by-window price slopes, BEA panel, manufacturing (`results/window_slopes.csv`): −0.336 (0.262), 0.228 (0.177),
0.381 (0.138), 0.437 (0.226), 0.404 (0.186); non-manufacturing 0.033, −0.115, −0.073, 0.125, 0.047. Census markup
slope in 2017–2022: manufacturing 0.596 (0.168), non-manufacturing 0.094 (0.050) (`results/markup_windows.csv`).

## Reproducing

```bash
pip install -r requirements.txt
python -I src/build_panel.py
python -I src/concentration_prices.py
```

The first script takes about a minute and writes the three panels; the second runs every regression, table and
figure in a few seconds. Both print what they loaded, kept and dropped.

## References

- Becker, R., Gray, W. and Marvakov, J. NBER-CES Manufacturing Industry Database, 1958–2018 release.
- Covarrubias, M., Gutiérrez, G. and Philippon, T. (2020). From good to bad concentration? US industries over the
  past 30 years. *NBER Macroeconomics Annual* 34, 1–46.
- Ganapati, S. (2021). Growing oligopolies, prices, output, and productivity. *American Economic Journal:
  Microeconomics* 13(3), 309–327.
- Philippon, T. (2019). *The Great Reversal: How America Gave Up on Free Markets*. Harvard University Press.
- US Department of Justice and Federal Trade Commission (2023). *Merger Guidelines*.
