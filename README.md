### Monetary Tightening and Opioid-Related Harms in Canada: A Province-Quarter Analysis of Deaths and Hospitalizations (2016–2025)

# Project Overview

MARCH 17 UPDATE: MASTER PANEL ADDED WAITING VISUALIZATIONS AND ANALYSIS 

This project investigates whether rapid Bank of Canada interest rate hikes (“monetary tightening shocks”) are associated with subsequent increases in opioid-related harms across Canadian provinces. Using a province-by-quarter dataset from 2016Q1 to 2025Q2, we will analyze opioid toxicity deaths and opioid-related hospitalizations and test whether these outcomes tend to rise in the 1–2 quarters following major rate increases. Our current focus is building a clean, analysis-ready panel dataset by standardizing quarterly opioid outcomes by province, constructing quarterly interest-rate shock variables (including lagged versions), and preparing the merged dataset for statistical analysis and visualizations.

This project is currently a work in progress and is done under Youreka Canada.

- Research Lead: Zan Tian
- Investigator: Ehab Gheriani
- Investigator: Alex Zhu
- Investigator: Mohammad Fatemi Tabar

PROJECT DEADLINE APRIL 1 


# Regression Results: Key Takeaways

1. Direction: Both lag1 and lag2 coefficients are positive across all models, suggesting 50bp rate hike shocks are associated with increases in opioid deaths in subsequent quarters.

2. Timing: The lag2 coefficient is consistently larger than lag1 (7.6 vs 23.1 in m1_deaths), suggesting effects take roughly 2 quarters to materialize.

3. Significance: No individual shock coefficient reaches significance at a = 0.05 in any model. The closest is lag2 in m2_deaths (p = 0.075).

4. Joint F-test: Shocks are jointly significant only in m2_deaths (chi2 = 7.41, p = 0.025, Reject H0). All other models retain H0.

5. Deaths vs hosp: Shock coefficients are larger and closer to significance for deaths than hosp. Hospitalisations show near-zero coefficients across all models.

Limitation: Shock variables are national-level so quarter FE were dropped in favour of a linear time trend. Quarter-clustered SEs are recommended for robustness.

## Sensitivity Check: Continuous Shock Variable (shock_bp_q)

6. The continuous shock variable (shock_bp_q) shows stronger and clearer results than the binary 50bp indicator. It is statistically significant for deaths in both models (p = 0.003 without unemp, p < 0.001 with unemp) and for hosp in both models (p = 0.034 without unemp, p = 0.009 with unemp).

7. Coefficient size: A 1bp increase in the quarterly rate shock is associated with roughly 24-35 additional deaths and 10-14 additional hospitalizations per quarter, after controlling for province FE and time trend.

8. The sensitivity check supports the main finding that monetary tightening shocks are positively associated with opioid deaths. The continuous measure captures dose-response more precisely than the binary 50bp threshold.
results_takeaways.md
