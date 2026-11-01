# Methods review: Covarrubias, Gutiérrez & Philippon (2020)

**Paper.** Matias Covarrubias, Germán Gutiérrez and Thomas Philippon, "From Good to Bad Concentration? US Industries
over the Past 30 Years," *NBER Macroeconomics Annual* 34 (2020), pp. 1–46 (University of Chicago Press;
DOI 10.1086/707169). Circulated as NBER Working Paper 25983 (June 2019, revised September 2019).

**Statistical focus.** The industry-level regressions of five-year changes in log prices and markups on five-year
changes in log CR4, before and after 2002 (Table 3, especially the post-2002 interaction of 0.17 in the all-industry
price regression), and the companion regressions of TFP, prices and markups on import-adjusted CR4 before and after
2000 (Table 2).

**Review standard.** The current AEA Data and Code Availability Policy, and standard reporting of estimates,
uncertainty, sample construction and robustness for observational regressions. For the model section, internal
consistency of the formal results, explicit assumptions and the testability of predictions.

**What was read.** The full text of NBER Working Paper 25983 (September 2019 revision) from nber.org, including the
data appendix and appendix tables. The published chapter in the *Macroeconomics Annual*, the replication files
listed on the NBER chapter page and the published discussions by Janice Eberly and Chad Syverson were not read. Page
numbers below refer to the working paper.

## Methods summary

**Research design.** Observational, descriptive and comparative. The paper sets out simple industry models (Section 1)
that yield sign predictions for how concentration should co-move with exit, productivity, prices, investment and
leader turnover under "good" concentration (higher substitutability, rising returns to scale) and "bad"
concentration (rising entry barriers). It then checks those signs in aggregate time series (Section 3) and in an
industry-level principal components analysis (Section 4). No causal identification strategy is claimed for the
concentration regressions; they are contemporaneous correlations within sector-by-year cells.

**Sampling strategy.** Industries, not firms, for the headline tests. Table 2 uses all industries in the BLS
multifactor productivity tables with Compustat-based, import-adjusted CR4. Table 3 combines Economic Census
concentration with NBER-CES data for manufacturing (SIC-4 before 1997, NAICS-6 after) and BEA detailed gross output
prices for non-manufacturing, restricted to industries consistently defined across each five-year period (p. 59).
The sample is the population of covered industries rather than a random draw.

**Sample size.** Table 2: 94 industry-windows before 2000 and 141 after. Table 3: 2,083 industry-windows, of which
1,682 manufacturing and 401 non-manufacturing. The split of Table 3 observations between pre- and post-2002 windows
is not reported.

**Inclusion and exclusion criteria.** Consistently defined SIC/NAICS codes over each five-year window, following
Ganapati; taxable firms where the Census splits service industries by tax status; wholesale totals only (p. 59).
The data appendix mentions manual handling of "selected data issues (e.g., outliers in sales growth)" with details
deferred to the replication code (p. 59, footnote 32).

**Independent and dependent variables.** Independent variable: the five-year change in log CR4 (import-adjusted
Compustat CR4 in Table 2; Census CR4 in Table 3), interacted with an indicator for windows ending after 2002 (Table 3)
or estimated separately before and after 2000 (Table 2). Dependent variables: five-year changes in log TFP, log price
and log markup over unit labor cost, with $`\Delta \log \mu = \Delta \log P - \Delta \log ULC`$. Table 3's price
columns also control for changes in log labor productivity and log wages.

**Statistical methods.** OLS (Table 2, weighting not stated) and sales-weighted OLS (Table 3) with year or sector-by-year fixed effects and
standard errors clustered at the industry level. Significance is marked at 10%, 5% and 1%. Section 4 uses principal
components on the correlation matrix of a wide range of industry measures (listed in its Figure 12).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Price slope on Δ log CR4, all industries | −0.01 (SE 0.03), log points per log point | Table 3, col. 1, p. 22 | Co-movement of prices and concentration in windows ending 2002 or earlier, within sector-years, with LP and wage controls | That concentration had no price effect before 2002; the estimate pools SIC and NAICS eras |
| Post-2002 interaction, all industries | 0.17 (SE 0.04), significant at 1% | Table 3, col. 1, p. 22 | The change in that co-movement for windows ending after 2002 | That rising concentration caused price increases; reverse causality and common shocks are not addressed |
| Post-2002 interaction, manufacturing | 0.20 (SE 0.06) on a base of 0.05 (0.02), N = 1,682 | Table 3, col. 2 | Same, manufacturing only | Robustness to weighting or to dominant industries is not shown |
| Post-2002 interaction, non-manufacturing | 0.17 (SE 0.05) on −0.03 (0.04), N = 401 | Table 3, col. 3 | Same, services and trade at BEA detail | Comparability of BEA prices across service industries |
| Markup interaction, all industries | 0.23 (SE 0.06) | Table 3, col. 4 | Change in co-movement of sales-to-labor-cost markups with concentration after 2002 | That markups over total marginal cost rose; materials and capital are omitted |
| Δ log CR4 × High CR, non-manufacturing | 0.41 (SE 0.14) | Table 3, col. 9 | Stronger markup link where ending concentration is high | The "High CR" threshold is not defined in the text read |
| TFP slope before / after 2000 | 0.186 (SE 0.070) / −0.044 (SE 0.051), N = 94 / 141 | Table 2, cols. 1–2, p. 20 | Correlation of TFP growth with import-adjusted concentration growth in broad BLS industries | A significant decline; the post-2000 estimate is not significant and no test of the difference is reported |
| Price slope before / after 2000 | −0.093 (0.069) / 0.077 (0.088) | Table 2, cols. 3–4 | Same for prices | Neither estimate is significant individually |
| Leader turnover | About 35% (1980s), 40% (dot-com peak), 25% (recent) chance of leaving the top 4 within five years | Section 3.1, Figure 7, p. 17 | Persistence of industry leadership in Compustat | Coverage of private firms; no uncertainty bands shown |
| Returns to scale | 0.78 before 2000, 0.80 after | Section 3.4, p. 28 | Industry-level returns to scale (Basu–Fernald–Kimball method, from a companion paper) | Standard errors are not reported in this paper |
| Import adjustment | Domestic CR8 +6.7 points vs import-adjusted +1.6 points in import-exposed manufacturing | Section 2.1, Figure 3, p. 12 | How much imports offset measured concentration | Whether Table 3 uses adjusted or unadjusted CR4 |
| PCA variance share | 34% of variance in the first two components | Section 4, p. 30 | How much of the cross-industry variation the good and bad factors summarize | That the components identify the theories; the labels are interpretive |

## Interpretation notes

- The model's central result (Proposition 1) is internally consistent. In the free-entry model with unit-elastic
  demand, the number of firms is $`N = \tfrac{\mu}{1+\mu}\,\bar{Y}/((r+\delta)\kappa+\phi)`$, so a fall in markups and a
  rise in entry costs both raise concentration, while moving prices in opposite directions. The sign of the
  price-concentration correlation is therefore a reasonable diagnostic, provided demand and productivity shocks do not
  dominate both variables.
- The headline evidence is a change in a correlation, measured as an interaction. The paper reports the interaction's
  significance but not the implied post-2002 slope with its standard error. For the all-industry price column that
  slope is about 0.16, but its uncertainty has to be inferred.
- Table 2 and Table 3 use different breaks (2000 vs 2002), different concentration sources (Compustat
  import-adjusted vs Census) and possibly different weighting (Table 2's note does not mention weights; Table 3 is
  sales-weighted). The text treats them as mutually reinforcing; it does not report how sensitive either is to the
  other's choices.
- Sales weighting gives the largest industries, including commodity-price industries such as petroleum refining, much
  of the influence. No unweighted or leave-one-out version of Table 3 is reported in the text read.
- The paper's own argument that detailed-industry productivity correlations are partly mechanical (large firm-level
  shocks raise both CR4 and measured output, p. 22) applies with similar force to the markup measure, since sales over
  payroll rises when output shifts toward large, less labor-intensive firms. This is a limitation of the measure, not
  an error.
- These are reporting gaps, not documented analytical errors. No published correction or comment identifying an
  error in the tables reviewed turned up in the sources consulted for this review.
- How the modern rerun in this repository relates: using public Census, NBER-CES and BEA data for 1997–2017, the
  manufacturing interaction comes out positive and larger (0.392 with controls), while the non-manufacturing
  interaction is near zero; the rerun differs in sample years and in its pre-2002 coverage and is not a reproduction.

## Unanswered questions

- How many Table 3 observations fall before and after 2002, and how many come from the SIC era?
- Is the CR4 in Table 3 import-adjusted, as Section 2.1 says measures are "throughout the paper"?
- Which outliers were adjusted manually (footnote 32), and do the results change without those adjustments?
- How is "High CR" defined in Table 3, columns 7–9?
- Does the post-2002 interaction survive equal weighting, the removal of energy-linked industries, or clustering at a
  broader sector level?
- Is the difference between the pre- and post-2000 TFP slopes in Table 2 statistically significant?

## Items requiring expert verification

- Whether the published chapter's tables match the working paper's Table 2 and Table 3 exactly; only the working paper
  was read here.
- Whether the NBER replication package reproduces Table 3, including the SIC-to-NAICS bridging of the pre-1997
  windows.
- Whether BEA detailed gross output price indexes for service industries, which the BEA describes as partly judgmental
  at fine levels, are reliable enough to support the non-manufacturing columns.
- Whether the returns-to-scale estimates cited from the companion paper (0.78 and 0.80) carry standard errors that
  make the reported stability meaningful.
