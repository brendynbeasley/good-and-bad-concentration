# Covarrubias, Gutiérrez & Philippon (2020) on public data: findings

## In plain English

The paper argued that, after 2002, American industries that became more concentrated also raised their prices,
while in the 1990s concentration had come with falling prices and rising productivity. This rerun uses the Economic
Census, NBER-CES and BEA price data for 1997 to 2022.

- **In factories, the paper holds up.** After 2002, manufacturing industries whose top four firms gained share also
  raised prices faster than others in their sector, by about 0.3 to 0.46 log points per unit of log CR4. Before
  2002 the link was negative, carried by computer makers such as Dell, HP and Compaq, whose market share rose as their
  prices collapsed.
- **In services, it does not.** Taken together, industries outside manufacturing, from pharmacies such as CVS and
  Walgreens to airlines such as Delta and United, show no change in the price link after 2002 in this data.
- **The newest data look the same.** In 2017 to 2022, the window the paper could not see, the manufacturing price
  link was 0.40, about what it had been from 2002 to 2017. Cement (Holcim, CEMEX) and veterinary care (Mars's Banfield
  and VCA) concentrated sharply in those years, while cloud hosting (Amazon Web Services, Microsoft, Google) concentrated
  and got cheaper.
- **The result depends on the big industries.** With every manufacturing industry weighted equally, prices and
  concentration still move together after 2002 (0.075) and not before (0.005), but the difference, 0.070 (0.063), is
  too imprecise to call a break. Dropping electronic computers alone halves the weighted interaction, to 0.318.

A friendlier tour is in the [README](../README.md); methods are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels.** *dlog_cr4* = five-year change in the log four-firm concentration ratio. *dlog_p* = five-year
change in the log price index (NBER-CES `piship` for 6-digit manufacturing, BEA UGO304 otherwise). *dlog_mu* =
five-year change in log sales over payroll, the markup over unit labor cost. *dlog_tfp* = five-year change in log
NBER-CES five-factor TFP (through 2016, so the 2002–2017 TFP rows cover the 2002–2007 and 2007–2012 windows only).
*dlog_q* = five-year change in the log BEA real output index. *post* = window ends after 2002. *Mid* = windows ending
2007–2017; *late* = 2017–2022. *coef (se)* are WLS coefficients with industry-clustered SEs in pooled regressions and
HC1 SEs in single windows; p-values of 0.000 are below 0.0005. *paper_coef* and *paper_se* are the paper's Table 3
(replication) or Table 2 (split samples). *mean_dlog_cr4* is the sales-weighted mean change in log CR4 and
*share_rising* the share of industries whose CR4 rose. In the robustness table, the leave-one-industry-out rows give
the smallest and largest interaction across the 363 regressions that each drop one manufacturing industry (named by
its 2012 NAICS code), and the regression with the largest p-value; the two 1997–2002 rows are the slope term, not the
interaction. *All industries* price change in the named table is the
sales-weighted average across the BEA panel in the same window.

## Table 3 on public data (results/replication_table3.csv)

Manufacturing at 6-digit NAICS with NBER-CES outcomes, other industries at BEA detail, windows 1997–2017,
sector-by-window fixed effects, start-of-window sales weights.

| outcome | sample | spec | term | coef | se | p | ci_low | ci_high | n | paper_coef | paper_se |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dlog_p | All | with LP and wage controls | dlog_cr4 | 0.040 | 0.043 | 0.355 | −0.045 | 0.124 | 1772 | −0.010 | 0.030 |
| dlog_p | All | with LP and wage controls | dlog_cr4:post | 0.129 | 0.075 | 0.085 | −0.018 | 0.276 | 1772 | 0.170 | 0.040 |
| dlog_p | All | with LP and wage controls | post-2002 slope (sum) | 0.169 | 0.053 | 0.002 | 0.065 | 0.273 | 1772 |  |  |
| dlog_p | Manufacturing | with LP and wage controls | dlog_cr4 | 0.065 | 0.069 | 0.348 | −0.071 | 0.201 | 1360 | 0.050 | 0.020 |
| dlog_p | Manufacturing | with LP and wage controls | dlog_cr4:post | 0.392 | 0.103 | 0.000 | 0.190 | 0.593 | 1360 | 0.200 | 0.060 |
| dlog_p | Manufacturing | with LP and wage controls | post-2002 slope (sum) | 0.457 | 0.100 | 0.000 | 0.260 | 0.654 | 1360 |  |  |
| dlog_p | Non-manufacturing | with LP and wage controls | dlog_cr4 | 0.046 | 0.030 | 0.129 | −0.013 | 0.105 | 412 | −0.030 | 0.040 |
| dlog_p | Non-manufacturing | with LP and wage controls | dlog_cr4:post | −0.030 | 0.047 | 0.519 | −0.123 | 0.062 | 412 | 0.170 | 0.050 |
| dlog_p | Non-manufacturing | with LP and wage controls | post-2002 slope (sum) | 0.015 | 0.030 | 0.609 | −0.044 | 0.075 | 412 |  |  |
| dlog_p | All | no controls | dlog_cr4 | −0.076 | 0.095 | 0.425 | −0.261 | 0.110 | 1772 | −0.010 | 0.030 |
| dlog_p | All | no controls | dlog_cr4:post | 0.179 | 0.113 | 0.113 | −0.043 | 0.401 | 1772 | 0.170 | 0.040 |
| dlog_p | All | no controls | post-2002 slope (sum) | 0.104 | 0.049 | 0.034 | 0.008 | 0.199 | 1772 |  |  |
| dlog_p | Manufacturing | no controls | dlog_cr4 | −0.310 | 0.263 | 0.237 | −0.825 | 0.204 | 1360 | 0.050 | 0.020 |
| dlog_p | Manufacturing | no controls | dlog_cr4:post | 0.621 | 0.295 | 0.035 | 0.042 | 1.200 | 1360 | 0.200 | 0.060 |
| dlog_p | Manufacturing | no controls | post-2002 slope (sum) | 0.311 | 0.120 | 0.010 | 0.075 | 0.547 | 1360 |  |  |
| dlog_p | Non-manufacturing | no controls | dlog_cr4 | 0.033 | 0.031 | 0.293 | −0.028 | 0.094 | 412 | −0.030 | 0.040 |
| dlog_p | Non-manufacturing | no controls | dlog_cr4:post | −0.032 | 0.047 | 0.498 | −0.124 | 0.060 | 412 | 0.170 | 0.050 |
| dlog_p | Non-manufacturing | no controls | post-2002 slope (sum) | 0.001 | 0.034 | 0.975 | −0.066 | 0.069 | 412 |  |  |
| dlog_mu | All | no controls | dlog_cr4 | 0.073 | 0.054 | 0.173 | −0.032 | 0.178 | 1772 | 0.020 | 0.040 |
| dlog_mu | All | no controls | dlog_cr4:post | 0.112 | 0.088 | 0.203 | −0.060 | 0.284 | 1772 | 0.230 | 0.060 |
| dlog_mu | All | no controls | post-2002 slope (sum) | 0.185 | 0.050 | 0.000 | 0.088 | 0.282 | 1772 |  |  |
| dlog_mu | Manufacturing | no controls | dlog_cr4 | 0.053 | 0.050 | 0.285 | −0.044 | 0.151 | 1360 | 0.100 | 0.030 |
| dlog_mu | Manufacturing | no controls | dlog_cr4:post | 0.392 | 0.113 | 0.001 | 0.171 | 0.614 | 1360 | 0.130 | 0.070 |
| dlog_mu | Manufacturing | no controls | post-2002 slope (sum) | 0.446 | 0.098 | 0.000 | 0.254 | 0.638 | 1360 |  |  |
| dlog_mu | Non-manufacturing | no controls | dlog_cr4 | 0.082 | 0.079 | 0.301 | −0.074 | 0.238 | 412 | −0.000 | 0.050 |
| dlog_mu | Non-manufacturing | no controls | dlog_cr4:post | −0.026 | 0.109 | 0.810 | −0.239 | 0.187 | 412 | 0.260 | 0.070 |
| dlog_mu | Non-manufacturing | no controls | post-2002 slope (sum) | 0.056 | 0.039 | 0.154 | −0.021 | 0.133 | 412 |  |  |

## Manufacturing, separate pre and post regressions (results/mfg_split_table2.csv)

| outcome | period | weights | coef | se | p | n | paper_coef | paper_se |
|---|---|---|---|---|---|---|---|---|
| dlog_tfp | 1997-2002 | sales | 0.304 | 0.199 | 0.127 | 360 | 0.186 | 0.070 |
| dlog_tfp | 1997-2002 | none | 0.109 | 0.054 | 0.043 | 360 | 0.186 | 0.070 |
| dlog_tfp | 2002-2017 | sales | 0.082 | 0.049 | 0.095 | 643 | −0.044 | 0.051 |
| dlog_tfp | 2002-2017 | none | 0.059 | 0.031 | 0.062 | 643 | −0.044 | 0.051 |
| dlog_p | 1997-2002 | sales | −0.310 | 0.263 | 0.237 | 360 | −0.093 | 0.069 |
| dlog_p | 1997-2002 | none | 0.005 | 0.052 | 0.920 | 360 | −0.093 | 0.069 |
| dlog_p | 2002-2017 | sales | 0.311 | 0.120 | 0.010 | 1000 | 0.077 | 0.088 |
| dlog_p | 2002-2017 | none | 0.075 | 0.025 | 0.003 | 1000 | 0.077 | 0.088 |
| dlog_mu | 1997-2002 | sales | 0.053 | 0.050 | 0.284 | 360 | −0.102 | 0.047 |
| dlog_mu | 1997-2002 | none | 0.097 | 0.038 | 0.011 | 360 | −0.102 | 0.047 |
| dlog_mu | 2002-2017 | sales | 0.446 | 0.098 | 0.000 | 1000 | 0.116 | 0.064 |
| dlog_mu | 2002-2017 | none | 0.310 | 0.043 | 0.000 | 1000 | 0.116 | 0.064 |

## Robustness of the manufacturing post-2002 price interaction (results/robustness.csv)

| case | coef | se | p | n |
|---|---|---|---|---|
| Manufacturing, sales-weighted (baseline) | 0.621 | 0.295 | 0.035 | 1360 |
| Manufacturing, unweighted | 0.070 | 0.063 | 0.265 | 1360 |
| Manufacturing, without petroleum refining | 0.518 | 0.301 | 0.086 | 1356 |
| Manufacturing, with LP and wage controls | 0.392 | 0.103 | 0.000 | 1360 |
| Manufacturing, controls, without refining | 0.382 | 0.123 | 0.002 | 1356 |
| All industries, unweighted | 0.048 | 0.047 | 0.313 | 1772 |
| All industries, without petroleum refining | 0.138 | 0.109 | 0.203 | 1768 |
| Manufacturing 1997-2002 slope, all industries | −0.310 | 0.263 | 0.237 | 360 |
| Manufacturing 1997-2002 slope, without electronic computers | −0.021 | 0.047 | 0.653 | 359 |
| Manufacturing, leave-one-industry-out (min), dropping 334111 | 0.318 | 0.137 | 0.020 | 1356 |
| Manufacturing, leave-one-industry-out (max), dropping 311511 | 0.647 | 0.307 | 0.035 | 1356 |
| Manufacturing, leave-one-industry-out, largest p-value | 0.518 | 0.301 | 0.086 | 1356 |

## Petroleum refining's share of manufacturing start-of-window shipments (results/refining_share.csv)

| window end | refining_share |
|---|---|
| 2002 | 0.042 |
| 2007 | 0.052 |
| 2012 | 0.131 |
| 2017 | 0.142 |

## Price slope by five-year window, the extension (results/window_slopes.csv)

| panel | window | sample | coef | se | p | n | mean_dlog_cr4 | share_rising |
|---|---|---|---|---|---|---|---|---|
| BEA detail | 1997-2002 | All | −0.070 | 0.086 | 0.419 | 320 | 0.116 | 0.684 |
| BEA detail | 1997-2002 | Manufacturing | −0.336 | 0.262 | 0.200 | 229 | 0.087 | 0.668 |
| BEA detail | 1997-2002 | Non-manufacturing | 0.033 | 0.032 | 0.298 | 91 | 0.138 | 0.725 |
| BEA detail | 1997-2002 | All, without refining | −0.079 | 0.088 | 0.368 | 319 | 0.112 | 0.683 |
| BEA detail | 1997-2002 | Manufacturing, without refining | −0.395 | 0.274 | 0.149 | 228 | 0.075 | 0.667 |
| BEA detail | 2002-2007 | All | 0.035 | 0.088 | 0.693 | 327 | 0.026 | 0.526 |
| BEA detail | 2002-2007 | Manufacturing | 0.228 | 0.177 | 0.197 | 222 | 0.006 | 0.518 |
| BEA detail | 2002-2007 | Non-manufacturing | −0.115 | 0.063 | 0.067 | 105 | 0.037 | 0.543 |
| BEA detail | 2002-2007 | All, without refining | −0.031 | 0.066 | 0.632 | 326 | 0.024 | 0.525 |
| BEA detail | 2002-2007 | Manufacturing, without refining | 0.079 | 0.121 | 0.515 | 221 | −0.002 | 0.516 |
| BEA detail | 2007-2012 | All | 0.055 | 0.064 | 0.394 | 306 | 0.018 | 0.549 |
| BEA detail | 2007-2012 | Manufacturing | 0.381 | 0.138 | 0.006 | 198 | −0.002 | 0.530 |
| BEA detail | 2007-2012 | Non-manufacturing | −0.073 | 0.036 | 0.042 | 108 | 0.027 | 0.583 |
| BEA detail | 2007-2012 | All, without refining | 0.061 | 0.064 | 0.338 | 305 | 0.019 | 0.551 |
| BEA detail | 2007-2012 | Manufacturing, without refining | 0.407 | 0.134 | 0.002 | 197 | −0.001 | 0.533 |
| BEA detail | 2012-2017 | All | 0.190 | 0.064 | 0.003 | 336 | −0.005 | 0.503 |
| BEA detail | 2012-2017 | Manufacturing | 0.437 | 0.226 | 0.053 | 228 | −0.009 | 0.474 |
| BEA detail | 2012-2017 | Non-manufacturing | 0.125 | 0.052 | 0.017 | 108 | −0.002 | 0.565 |
| BEA detail | 2012-2017 | All, without refining | 0.140 | 0.044 | 0.002 | 335 | −0.003 | 0.504 |
| BEA detail | 2012-2017 | Manufacturing, without refining | 0.200 | 0.094 | 0.034 | 227 | −0.003 | 0.476 |
| BEA detail | 2017-2022 | All | 0.097 | 0.068 | 0.154 | 312 | 0.041 | 0.542 |
| BEA detail | 2017-2022 | Manufacturing | 0.404 | 0.186 | 0.030 | 219 | 0.015 | 0.539 |
| BEA detail | 2017-2022 | Non-manufacturing | 0.047 | 0.067 | 0.479 | 93 | 0.051 | 0.548 |
| BEA detail | 2017-2022 | All, without refining | 0.064 | 0.059 | 0.274 | 311 | 0.038 | 0.540 |
| BEA detail | 2017-2022 | Manufacturing, without refining | 0.180 | 0.099 | 0.070 | 218 | 0.001 | 0.537 |
| NBER-CES 6-digit | 1997-2002 | Manufacturing | −0.310 | 0.263 | 0.237 | 360 | 0.088 | 0.650 |
| NBER-CES 6-digit | 2002-2007 | Manufacturing | 0.126 | 0.120 | 0.294 | 349 | 0.010 | 0.544 |
| NBER-CES 6-digit | 2007-2012 | Manufacturing | 0.390 | 0.157 | 0.013 | 294 | 0.000 | 0.548 |
| NBER-CES 6-digit | 2012-2017 | Manufacturing | 0.470 | 0.299 | 0.115 | 357 | −0.012 | 0.515 |

## Real-output slope by five-year window (results/window_slopes.csv, outcome dlog_q)

| panel | window | sample | coef | se | p | n | mean_dlog_cr4 | share_rising |
|---|---|---|---|---|---|---|---|---|
| BEA detail | 1997-2002 | All | 0.122 | 0.089 | 0.167 | 320 | 0.116 | 0.684 |
| BEA detail | 1997-2002 | Manufacturing | 0.383 | 0.226 | 0.090 | 229 | 0.087 | 0.668 |
| BEA detail | 1997-2002 | Non-manufacturing | 0.022 | 0.068 | 0.748 | 91 | 0.138 | 0.725 |
| BEA detail | 1997-2002 | All, without refining | 0.122 | 0.090 | 0.177 | 319 | 0.112 | 0.683 |
| BEA detail | 1997-2002 | Manufacturing, without refining | 0.404 | 0.242 | 0.095 | 228 | 0.075 | 0.667 |
| BEA detail | 2002-2007 | All | 0.035 | 0.079 | 0.659 | 327 | 0.026 | 0.526 |
| BEA detail | 2002-2007 | Manufacturing | 0.103 | 0.130 | 0.429 | 222 | 0.006 | 0.518 |
| BEA detail | 2002-2007 | Non-manufacturing | −0.017 | 0.101 | 0.864 | 105 | 0.037 | 0.543 |
| BEA detail | 2002-2007 | All, without refining | 0.032 | 0.080 | 0.691 | 326 | 0.024 | 0.525 |
| BEA detail | 2002-2007 | Manufacturing, without refining | 0.097 | 0.133 | 0.464 | 221 | −0.002 | 0.516 |
| BEA detail | 2007-2012 | All | 0.112 | 0.101 | 0.269 | 306 | 0.018 | 0.549 |
| BEA detail | 2007-2012 | Manufacturing | 0.288 | 0.175 | 0.100 | 198 | −0.002 | 0.530 |
| BEA detail | 2007-2012 | Non-manufacturing | 0.043 | 0.124 | 0.730 | 108 | 0.027 | 0.583 |
| BEA detail | 2007-2012 | All, without refining | 0.118 | 0.101 | 0.242 | 305 | 0.019 | 0.551 |
| BEA detail | 2007-2012 | Manufacturing, without refining | 0.311 | 0.171 | 0.070 | 197 | −0.001 | 0.533 |
| BEA detail | 2012-2017 | All | 0.022 | 0.093 | 0.813 | 336 | −0.005 | 0.503 |
| BEA detail | 2012-2017 | Manufacturing | 0.214 | 0.105 | 0.042 | 228 | −0.009 | 0.474 |
| BEA detail | 2012-2017 | Non-manufacturing | −0.028 | 0.116 | 0.807 | 108 | −0.002 | 0.565 |
| BEA detail | 2012-2017 | All, without refining | 0.029 | 0.093 | 0.755 | 335 | −0.003 | 0.504 |
| BEA detail | 2012-2017 | Manufacturing, without refining | 0.254 | 0.098 | 0.010 | 227 | −0.003 | 0.476 |
| BEA detail | 2017-2022 | All | 0.018 | 0.121 | 0.884 | 312 | 0.041 | 0.542 |
| BEA detail | 2017-2022 | Manufacturing | 0.123 | 0.127 | 0.332 | 219 | 0.015 | 0.539 |
| BEA detail | 2017-2022 | Non-manufacturing | 0.001 | 0.149 | 0.997 | 93 | 0.051 | 0.548 |
| BEA detail | 2017-2022 | All, without refining | 0.028 | 0.121 | 0.818 | 311 | 0.038 | 0.540 |
| BEA detail | 2017-2022 | Manufacturing, without refining | 0.215 | 0.119 | 0.071 | 218 | 0.001 | 0.537 |

## Pooled BEA panel with separate 2002–2017 and 2017–2022 interactions (results/extension_pooled.csv)

| sample | term | coef | se | p | ci_low | ci_high | n |
|---|---|---|---|---|---|---|---|
| All | dlog_cr4 | −0.070 | 0.086 | 0.419 | −0.239 | 0.099 | 1601 |
| All | dlog_cr4:mid | 0.170 | 0.100 | 0.090 | −0.026 | 0.366 | 1601 |
| All | dlog_cr4:late | 0.167 | 0.103 | 0.104 | −0.034 | 0.368 | 1601 |
| All | late minus mid | −0.003 | 0.067 | 0.964 | −0.135 | 0.129 | 1601 |
| Manufacturing | dlog_cr4 | −0.336 | 0.262 | 0.200 | −0.850 | 0.178 | 1096 |
| Manufacturing | dlog_cr4:mid | 0.676 | 0.276 | 0.014 | 0.136 | 1.216 | 1096 |
| Manufacturing | dlog_cr4:late | 0.740 | 0.301 | 0.014 | 0.150 | 1.330 | 1096 |
| Manufacturing | late minus mid | 0.064 | 0.123 | 0.602 | −0.177 | 0.306 | 1096 |
| Non-manufacturing | dlog_cr4 | 0.033 | 0.031 | 0.294 | −0.029 | 0.094 | 505 |
| Non-manufacturing | dlog_cr4:mid | −0.032 | 0.047 | 0.499 | −0.124 | 0.060 | 505 |
| Non-manufacturing | dlog_cr4:late | 0.014 | 0.068 | 0.832 | −0.119 | 0.148 | 505 |
| Non-manufacturing | late minus mid | 0.046 | 0.075 | 0.538 | −0.101 | 0.194 | 505 |

## Markup slope by window (results/markup_windows.csv)

| source | sample | window | coef | se | p | n |
|---|---|---|---|---|---|---|
| Census 6-digit | Non-manufacturing | 1997-2002 | 0.043 | 0.034 | 0.206 | 372 |
| Census 6-digit | Non-manufacturing | 2002-2007 | 0.111 | 0.077 | 0.148 | 454 |
| Census 6-digit | Non-manufacturing | 2007-2012 | 0.187 | 0.059 | 0.001 | 447 |
| Census 6-digit | Non-manufacturing | 2012-2017 | 0.129 | 0.087 | 0.139 | 445 |
| Census 6-digit | Manufacturing | 2017-2022 | 0.596 | 0.168 | 0.000 | 330 |
| Census 6-digit | Non-manufacturing | 2017-2022 | 0.094 | 0.050 | 0.061 | 384 |
| NBER-CES 6-digit | Manufacturing | 1997-2002 | 0.053 | 0.050 | 0.284 | 360 |
| NBER-CES 6-digit | Manufacturing | 2002-2007 | 0.301 | 0.094 | 0.001 | 349 |
| NBER-CES 6-digit | Manufacturing | 2007-2012 | 0.455 | 0.219 | 0.038 | 294 |
| NBER-CES 6-digit | Manufacturing | 2012-2017 | 0.631 | 0.150 | 0.000 | 357 |

## Named industries (results/named_industries.csv)

Leaders are each market's well-known firms; the Census does not name companies. Gross output is in billions of
dollars at the start of the window.

| industry | leaders | window | cr4_start | cr4_end | dlog_cr4 | price_change_pct | all_industry_price_change_pct | output_change_pct | gross_output_start_bn |
|---|---|---|---|---|---|---|---|---|---|
| Electronic computer manufacturing | Dell, HP, Compaq, Apple | 1997-2002 | 45.400 | 75.500 | 0.509 | −74.524 | 3.678 | 222.3 | 63.801 |
| Wireless telecommunications carriers (except satellite) | Verizon, AT&T, Sprint, T-Mobile | 2007-2012 | 80.200 | 89.100 | 0.105 | −16.568 | 10.844 | 61.294 | 171.3 |
| Data processing, hosting, and related services | Amazon Web Services, Microsoft, Google | 2017-2022 | 17.200 | 37.200 | 0.771 | −6.183 | 21.007 | 114.0 | 176.2 |
| Software publishers | Microsoft, Oracle, Adobe | 2017-2022 | 32.400 | 24.300 | −0.288 | −6.335 | 21.007 | 71.629 | 282.1 |
| Air transportation | American, Delta, United, Southwest | 2007-2012 | 51.197 | 63.404 | 0.203 | 20.632 | 10.844 | 0.820 | 160.7 |
| Health and personal care stores | CVS, Walgreens, Rite Aid | 2002-2007 | 50.510 | 59.767 | 0.164 | 21.528 | 15.399 | 10.007 | 56.096 |
| Pharmaceutical preparation manufacturing | Pfizer, Merck, Johnson & Johnson, AbbVie | 2012-2017 | 37.200 | 43.900 | 0.166 | 31.089 | 1.432 | −4.872 | 149.5 |
| Petroleum refineries | Marathon, Valero, ExxonMobil, Phillips 66 | 2017-2022 | 44.900 | 52.200 | 0.151 | 94.434 | 21.007 | −14.484 | 494.7 |
| Cement manufacturing | Holcim, CEMEX, Heidelberg Materials | 2017-2022 | 40.100 | 51.700 | 0.254 | 21.069 | 21.007 | 17.268 | 8.362 |
| Veterinary services | Mars (Banfield, VCA) | 2017-2022 | 13.300 | 22.400 | 0.521 | 22.627 | 21.007 | 20.600 | 42.612 |
| Breakfast cereal manufacturing | General Mills, Kellogg's, Post, Quaker | 2017-2022 | 81.800 | 86.600 | 0.057 | 15.643 | 21.007 | −9.237 | 10.141 |

## Worked examples used in the README (results/worked_examples.csv)

| example | item | value |
|---|---|---|
| CR4 in 2022 | Breakfast cereal manufacturing | 86.600 |
| CR4 in 2022 | Cement manufacturing | 51.700 |
| CR4 in 2022 | Offices of physicians | 6.195 |
| Cement 2017-2022 | cr4_2017 | 40.100 |
| Cement 2017-2022 | cr4_2022 | 51.700 |
| Cement 2017-2022 | dlog_cr4 | 0.254 |
| Cement 2017-2022 | dlog_price | 0.191 |
| Cement 2017-2022 | price_change_pct | 21.069 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | shipments_2012_musd | 136,453.0 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | payroll_2012_musd | 12,516.5 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | shipments_2017_musd | 153,923.1 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | payroll_2017_musd | 12,209.8 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | markup_2012 | 10.902 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | markup_2017 | 12.607 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | dlog_markup | 0.145 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | dlog_price | 0.304 |
| Pharmaceutical preparations 2012-2017 (NBER-CES) | dlog_cr4 | 0.166 |

## Panels

`results/panel_naics6.csv` holds every 6-digit industry-window that passed the one-to-one concordance rule (4,002 rows).
`results/panel_mfg.csv` is the manufacturing replication panel on 2012 NBER-CES codes (1,360 rows, 363 industries).
`results/panel_bea.csv` is the BEA detail panel used for non-manufacturing and the extension (1,601 rows, 338
industries). Figures: `results/mfg_scatter.png` and `results/slopes_by_window.png`.
