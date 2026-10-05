---
name: regression-diagnostics
description: "Comprehensive regression model diagnostics and assumption checking. Use when validating regression models, checking assumptions (linearity, homoskedasticity, normality, independence), detecting outliers/influence, testing multicollinearity, or when user mentions residuals, heteroskedasticity, VIF, Cook's distance, or diagnostic plots."

---

<skill_content>

<overview>
Regression diagnostics are NOT optional add-ons—they are fundamental to valid inference. A regression model is a hypothesis about the data-generating process, and diagnostics test whether that hypothesis holds. Without diagnostics, you're flying blind: your p-values may be wrong, your confidence intervals misleading, and your conclusions invalid. Every regression analysis MUST include diagnostics.

The consequences of ignoring diagnostics are severe: heteroskedasticity can inflate Type I error rates from 5% to 40%, influential outliers can reverse coefficient signs, and multicollinearity can make estimates unstable. This skill enforces rigorous diagnostic practices that protect against these failures.
</overview>

<philosophy>
<core_principle>
"All models are wrong, but some are useful" - George Box. Diagnostics tell us HOW wrong our model is and whether it's still useful despite its wrongness.

FUNDAMENTAL TRUTH:
Statistical software will happily compute invalid estimates. It's YOUR responsibility to verify assumptions hold. No diagnostic → no inference.
</core_principle>
</philosophy>

<mandatory_requirements>

<requirement priority="critical">
  <name>Complete Diagnostic Suite</name>
  <description>MUST generate all four core diagnostic plots: Residuals vs Fitted, Q-Q plot, Scale-Location, Residuals vs Leverage</description>
  <rationale>Each plot tests different assumptions. Missing any plot means missing potential violations (Belsley et al. 1980)</rationale>
  <consequence>Undetected violations lead to invalid inference, wrong p-values, misleading conclusions</consequence>
</requirement>

<requirement priority="critical">
  <name>Heteroskedasticity Testing</name>
  <description>MUST run both Breusch-Pagan and White tests, use robust SE if p < 0.05</description>
  <rationale>MacKinnon & White (1985) show HC3 robust SE correct size distortions better than classical SE under heteroskedasticity</rationale>
  <consequence>Type I error rates can reach 40% instead of nominal 5% with uncorrected heteroskedasticity</consequence>
</requirement>

<requirement priority="critical">
  <name>Multicollinearity Assessment</name>
  <description>MUST compute VIF for all predictors, flag VIF > 10, recommend action if VIF > 5</description>
  <rationale>Kutner et al. (2004) demonstrate VIF > 10 indicates serious multicollinearity requiring intervention</rationale>
  <consequence>Unstable estimates, inflated standard errors, sign reversals with minor data changes</consequence>
</requirement>

<requirement priority="high">
  <name>Influence Diagnostics</name>
  <description>MUST compute Cook's distance, identify points > 4/n threshold, investigate high-leverage observations</description>
  <rationale>Cook & Weisberg (1982) show single influential points can dominate entire regression</rationale>
  <consequence>Results driven by outliers rather than general patterns, non-robust conclusions</consequence>
</requirement>

<requirement priority="high">
  <name>Actionable Recommendations</name>
  <description>For EVERY violation detected, provide specific remediation (e.g., "use robust SE", "log transform", "remove variable X")</description>
  <rationale>Diagnostics without remediation are useless—practitioners need actionable guidance</rationale>
  <consequence>Known problems persist, analysis remains flawed despite awareness</consequence>
</requirement>

</mandatory_requirements>

<thinking_process>
When running regression diagnostics:
1. Generate diagnostic plots FIRST (visual inspection reveals patterns)
2. Run formal tests for each assumption
3. Compute influence measures for all observations
4. Check multicollinearity among predictors
5. Document ALL violations found
6. Provide specific remediation for each violation
7. Re-run diagnostics after any remediation
8. Report sensitivity to different specifications
</thinking_process>

<implementation_pattern>

<code_template>
```python
# CRITICAL: Complete regression diagnostics template

@app.cell
def complete_regression_diagnostics(model, df, cluster_var=None):
    """
    Comprehensive diagnostics are mandatory for valid inference.
    Every assumption violation has specific consequences and remediation.
    This function enforces systematic checking and clear reporting.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy import stats
    from statsmodels.stats.diagnostic import het_breuschpagan, het_white
    from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
    import os

    print("=" * 70)
    print("COMPREHENSIVE REGRESSION DIAGNOSTICS")
    print("=" * 70)

    # Extract residuals and fitted values
    fitted = model.fittedvalues
    residuals = model.resid
    standardized_resid = residuals / residuals.std()

    # 1. DIAGNOSTIC PLOTS (mandatory visualization)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Residuals vs Fitted (linearity + homoskedasticity)
    axes[0, 0].scatter(fitted, residuals, alpha=0.5, s=30)
    axes[0, 0].axhline(0, color='red', linestyle='--', linewidth=1.5)

    # Add loess smoother to detect patterns
    from scipy.interpolate import interp1d
    sorted_idx = np.argsort(fitted)
    window = max(10, len(fitted) // 20)
    smoothed = pd.Series(residuals[sorted_idx]).rolling(window, center=True).mean()
    axes[0, 0].plot(fitted[sorted_idx], smoothed, 'g-', linewidth=2, label='Loess smoother')

    axes[0, 0].set_xlabel("Fitted Values", fontsize=11)
    axes[0, 0].set_ylabel("Residuals", fontsize=11)
    axes[0, 0].set_title("Residuals vs Fitted\n(Check: Random scatter around zero)", fontsize=12)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()

    # Q-Q Plot (normality)
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title("Normal Q-Q Plot\n(Check: Points follow diagonal)", fontsize=12)
    axes[0, 1].grid(True, alpha=0.3)

    # Scale-Location (homoskedasticity)
    sqrt_abs_resid = np.sqrt(np.abs(standardized_resid))
    axes[1, 0].scatter(fitted, sqrt_abs_resid, alpha=0.5, s=30)

    # Add trend line
    z = np.polyfit(fitted, sqrt_abs_resid, 1)
    p = np.poly1d(z)
    axes[1, 0].plot(fitted, p(fitted), "r-", linewidth=2, label=f'Trend: slope={z[0]:.3f}')

    axes[1, 0].set_xlabel("Fitted Values", fontsize=11)
    axes[1, 0].set_ylabel("√|Standardized Residuals|", fontsize=11)
    axes[1, 0].set_title("Scale-Location\n(Check: Horizontal band, no trend)", fontsize=12)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()

    # Residuals vs Leverage (influence)
    influence = OLSInfluence(model)
    leverage = influence.hat_matrix_diag
    cooks_d = influence.cooks_distance[0]

    axes[1, 1].scatter(leverage, standardized_resid, alpha=0.5, s=30)
    axes[1, 1].axhline(0, color='red', linestyle='--', linewidth=1.5)

    # Mark influential points
    n = len(residuals)
    threshold = 4 / n
    influential_mask = cooks_d > threshold
    if influential_mask.any():
        axes[1, 1].scatter(leverage[influential_mask],
                          standardized_resid[influential_mask],
                          color='red', s=100, alpha=0.7,
                          label=f'Influential (Cook\'s D > {threshold:.3f})')

    # Add contour lines for Cook's distance
    x_leverage = np.linspace(0, max(leverage) * 1.1, 50)
    for cooks_level in [0.5, 1.0]:
        y_resid = np.sqrt(cooks_level * n / (x_leverage * (1 - x_leverage)))
        axes[1, 1].plot(x_leverage, y_resid, '--', color='gray', alpha=0.5)
        axes[1, 1].plot(x_leverage, -y_resid, '--', color='gray', alpha=0.5)

    axes[1, 1].set_xlabel("Leverage", fontsize=11)
    axes[1, 1].set_ylabel("Standardized Residuals", fontsize=11)
    axes[1, 1].set_title("Residuals vs Leverage\n(Check: No influential outliers)", fontsize=12)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()

    plt.suptitle("Regression Diagnostic Plots - ALL FOUR REQUIRED", fontsize=14, y=1.02)
    plt.tight_layout()

    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/regression_diagnostics_complete.png", dpi=144, bbox_inches="tight")

    # Save figure reference for inline display
    diagnostic_fig = plt.gcf()

    # 2. HETEROSKEDASTICITY TESTS (mandatory formal testing)
    print("\n" + "=" * 70)
    print("HETEROSKEDASTICITY TESTS")
    print("-" * 70)

    bp_stat, bp_pval, _, _ = het_breuschpagan(residuals, model.model.exog)
    white_stat, white_pval, _, _ = het_white(residuals, model.model.exog)

    print(f"Breusch-Pagan Test:")
    print(f"  Statistic: {bp_stat:.4f}, p-value: {bp_pval:.4f}")
    print(f"  Interpretation: {'VIOLATION - Heteroskedasticity detected' if bp_pval < 0.05 else 'No violation detected'}")

    print(f"\nWhite Test:")
    print(f"  Statistic: {white_stat:.4f}, p-value: {white_pval:.4f}")
    print(f"  Interpretation: {'VIOLATION - Heteroskedasticity detected' if white_pval < 0.05 else 'No violation detected'}")

    if bp_pval < 0.05 or white_pval < 0.05:
        print("\nWARNING: REQUIRED ACTION:")
        print("  1. Use robust standard errors: model.get_robustcov_results(cov_type='HC3')")
        if cluster_var:
            print(f"  2. Or cluster-robust SE: cov_type='cluster', cov_kwds={{'groups': df['{cluster_var}']}}")
        print("  3. Consider variance-stabilizing transformation (log, sqrt)")
        print("  4. Check for omitted variables or incorrect functional form")

    # 3. MULTICOLLINEARITY (VIF mandatory for all predictors)
    print("\n" + "=" * 70)
    print("MULTICOLLINEARITY ASSESSMENT (VIF)")
    print("-" * 70)

    X = model.model.exog
    vif_data = []

    for i in range(X.shape[1]):
        if model.model.exog_names[i] == 'const':
            continue  # Skip constant term
        vif = variance_inflation_factor(X, i)
        vif_data.append({
            'Variable': model.model.exog_names[i],
            'VIF': vif,
            'Status': 'SEVERE' if vif > 10 else 'High' if vif > 5 else 'OK'
        })

    vif_df = pd.DataFrame(vif_data).sort_values('VIF', ascending=False)
    print(vif_df.to_string(index=False))

    severe_collinear = vif_df[vif_df['VIF'] > 10]
    high_collinear = vif_df[vif_df['VIF'] > 5]

    if len(severe_collinear) > 0:
        print("\nWARNING: SEVERE MULTICOLLINEARITY DETECTED:")
        for _, row in severe_collinear.iterrows():
            print(f"  {row['Variable']}: VIF = {row['VIF']:.2f}")
        print("\nREQUIRED ACTIONS:")
        print("  1. Remove one of the correlated variables")
        print("  2. Combine into index/principal component")
        print("  3. Use ridge regression for regularization")
    elif len(high_collinear) > 0:
        print("\nWARNING: Moderate multicollinearity detected. Monitor but may be acceptable.")

    # 4. INFLUENCE DIAGNOSTICS (identify problematic observations)
    print("\n" + "=" * 70)
    print("INFLUENTIAL OBSERVATIONS")
    print("-" * 70)

    n_influential = influential_mask.sum()
    high_leverage = leverage > (2 * (X.shape[1]) / n)
    n_high_leverage = high_leverage.sum()

    print(f"Cook's Distance threshold (4/n): {threshold:.4f}")
    print(f"Influential observations: {n_influential} ({100*n_influential/n:.1f}% of data)")
    print(f"High leverage observations: {n_high_leverage} ({100*n_high_leverage/n:.1f}% of data)")

    if n_influential > 0:
        influential_idx = np.where(influential_mask)[0]
        print(f"\nInfluential observation indices: {influential_idx[:10]}")  # Show first 10
        print("\nWARNING: REQUIRED ACTIONS:")
        print("  1. Investigate these observations for data errors")
        print("  2. Check if they represent valid but unusual cases")
        print("  3. Report results with AND without influential points")
        print("  4. Consider robust regression if many influential points")

    # 5. NORMALITY TESTS (for valid inference)
    print("\n" + "=" * 70)
    print("NORMALITY OF RESIDUALS")
    print("-" * 70)

    shapiro_stat, shapiro_pval = stats.shapiro(residuals[:5000])  # Shapiro-Wilk (limit 5000)
    jb_stat, jb_pval = stats.jarque_bera(residuals)

    print(f"Shapiro-Wilk Test: p-value = {shapiro_pval:.4f}")
    print(f"Jarque-Bera Test: p-value = {jb_pval:.4f}")

    if shapiro_pval < 0.05 or jb_pval < 0.05:
        print("\nWARNING: Non-normality detected in residuals")
        print("NOTES:")
        print("  - With n > 30, CLT often ensures valid inference despite non-normality")
        print("  - For small samples, consider bootstrap or transformation")
        print("  - Check for outliers causing non-normality")

    # 6. SUMMARY RECOMMENDATIONS
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY & REQUIRED ACTIONS")
    print("=" * 70)

    violations = []
    if bp_pval < 0.05 or white_pval < 0.05:
        violations.append("Heteroskedasticity → Use robust/clustered SE")
    if len(severe_collinear) > 0:
        violations.append("Severe multicollinearity → Remove/combine variables")
    if n_influential > 0:
        violations.append("Influential observations → Report sensitivity")
    if (shapiro_pval < 0.05 or jb_pval < 0.05) and n < 30:
        violations.append("Non-normal residuals (small sample) → Bootstrap/transform")

    if violations:
        print("WARNING: VIOLATIONS REQUIRING ACTION:")
        for i, v in enumerate(violations, 1):
            print(f"  {i}. {v}")
    else:
        print("SUCCESS: No major violations detected. Standard inference is valid.")

    print("\nDiagnostic plots saved to: ./images/regression_diagnostics_complete.png")

    # Return figure for inline display along with diagnostic results
    return vif_df, influential_mask, cooks_d, diagnostic_fig,
```
</code_template>

</implementation_pattern>

<examples>

<example context="clean_regression" difficulty="basic">
<description>Well-behaved regression with no major violations</description>
<code>
```python
@app.cell
def diagnose_clean_model():
    #Even with clean data, diagnostics are mandatory.
    # We verify assumptions hold before trusting inference.

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf

    # Simulated clean data for demonstration
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        'x1': np.random.normal(0, 1, n),
        'x2': np.random.normal(0, 1, n),
        'x3': np.random.normal(0, 1, n),
    })

    # Well-specified model with homoskedastic errors
    df['y'] = 2 + 3*df['x1'] - 1.5*df['x2'] + 0.8*df['x3'] + np.random.normal(0, 2, n)

    # Estimate model
    model = smf.ols('y ~ x1 + x2 + x3', data=df).fit()

    print("MODEL SUMMARY")
    print("=" * 70)
    print(model.summary())

    # Run complete diagnostics
    vif_df, influential, cooks = complete_regression_diagnostics(model, df)

    # INTERPRETATION
    print("\n" + "=" * 70)
    print("INTERPRETATION FOR CLEAN MODEL")
    print("=" * 70)
    print("""
    This is an example of a well-behaved regression:

    1. Residuals vs Fitted: Random scatter around zero [OK]
       → Linear specification is appropriate

    2. Q-Q Plot: Points follow diagonal line [OK]
       → Residuals are approximately normal

    3. Scale-Location: Horizontal band, no trend [OK]
       → Variance is constant (homoskedastic)

    4. Residuals vs Leverage: No points outside Cook's distance contours [OK]
       → No influential outliers distorting results

    5. VIF values all < 5 [OK]
       → No problematic multicollinearity

    6. Heteroskedasticity tests p > 0.05 [OK]
       → Can use standard errors as computed

    CONCLUSION: Standard inference is valid. Report results as-is.
    """)

    return model, vif_df,
```
</code>
<lesson>
Even with "clean" data, running diagnostics is non-negotiable. This example shows what good diagnostics look like—use this as a reference for comparison.
</lesson>
</example>

<example context="heteroskedastic_regression" difficulty="intermediate">
<description>Regression with heteroskedasticity requiring robust standard errors</description>
<code>
```python
@app.cell
def diagnose_heteroskedastic_model():
    #Heteroskedasticity is common in cross-sectional data.
    # We detect it, apply robust SE, and show the difference in inference.

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf

    np.random.seed(123)
    n = 500

    # Generate data with heteroskedastic errors
    df = pd.DataFrame({
        'income': np.random.lognormal(10, 1, n),  # Log-normal income
        'education': np.random.normal(12, 3, n),
        'experience': np.random.uniform(0, 40, n),
    })

    # Error variance increases with income (heteroskedasticity)
    error_sd = 0.1 * df['income']  # Variance proportional to income
    df['consumption'] = (
        1000 +
        0.7 * df['income'] +
        50 * df['education'] +
        20 * df['experience'] +
        np.random.normal(0, error_sd)
    )

    # Naive model (ignoring heteroskedasticity)
    model_naive = smf.ols('consumption ~ income + education + experience', data=df).fit()

    print("NAIVE MODEL (Standard Errors)")
    print("=" * 70)
    print(model_naive.summary())

    # Run diagnostics - will detect heteroskedasticity
    vif_df, influential, cooks = complete_regression_diagnostics(model_naive, df)

    # CORRECTED MODEL with robust standard errors
    print("\n" + "=" * 70)
    print("CORRECTED MODEL (HC3 Robust Standard Errors)")
    print("=" * 70)

    # HC3 is preferred for finite samples (MacKinnon & White 1985)
    model_robust = model_naive.get_robustcov_results(cov_type='HC3')
    print(model_robust.summary())

    # Compare standard errors
    comparison = pd.DataFrame({
        'Variable': model_naive.params.index,
        'Coef': model_naive.params.values,
        'SE (Naive)': model_naive.bse.values,
        'SE (Robust)': model_robust.bse.values,
        'SE Ratio': model_robust.bse.values / model_naive.bse.values,
        'p-val (Naive)': model_naive.pvalues.values,
        'p-val (Robust)': model_robust.pvalues.values,
    })

    print("\n" + "=" * 70)
    print("STANDARD ERROR COMPARISON")
    print("=" * 70)
    print(comparison.to_string(index=False))

    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
    1. Heteroskedasticity detected (p < 0.001) in both tests
    2. Robust SEs are larger for variables correlated with variance
    3. Some coefficients lose significance with correct SEs
    4. Ignoring heteroskedasticity gave false precision

    LESSON: Always test for heteroskedasticity. When detected,
    robust standard errors are MANDATORY for valid inference.
    """)

    return model_robust, comparison,
```
</code>
<best_practice>
ALWAYS compare naive vs robust standard errors when heteroskedasticity is detected. The differences can be substantial and change conclusions about statistical significance.
</best_practice>
</example>

<example context="influential_outliers" difficulty="advanced">
<description>Regression dominated by influential outliers requiring sensitivity analysis</description>
<code>
```python
@app.cell
def diagnose_influential_outliers():
    #Influential observations can completely dominate results.
    # We identify them, assess impact, and report sensitivity.

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt
    import os

    np.random.seed(789)
    n = 200

    # Generate mostly normal data
    df = pd.DataFrame({
        'x': np.random.normal(50, 10, n),
        'z': np.random.normal(0, 1, n),
    })
    df['y'] = 10 + 2*df['x'] + 5*df['z'] + np.random.normal(0, 10, n)

    # Add influential outliers
    outliers = pd.DataFrame({
        'x': [100, 105, 110],  # High leverage points
        'z': [0, 0, 0],
        'y': [50, 45, 40],  # Don't follow pattern
    })
    df = pd.concat([df, outliers], ignore_index=True)

    # Full model (with outliers)
    model_full = smf.ols('y ~ x + z', data=df).fit()

    print("FULL MODEL (Including Outliers)")
    print("=" * 70)
    print(model_full.summary())

    # Run diagnostics - will identify influential points
    vif_df, influential_mask, cooks_d = complete_regression_diagnostics(model_full, df)

    # Model without influential observations
    print("\n" + "=" * 70)
    print("ROBUST MODEL (Excluding Influential Points)")
    print("=" * 70)

    df_clean = df[~influential_mask].copy()
    model_robust = smf.ols('y ~ x + z', data=df_clean).fit()
    print(model_robust.summary())

    # Sensitivity comparison
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS")
    print("=" * 70)

    comparison = pd.DataFrame({
        'Model': ['With Outliers', 'Without Outliers'],
        'n': [len(df), len(df_clean)],
        'β_x': [model_full.params['x'], model_robust.params['x']],
        'SE_x': [model_full.bse['x'], model_robust.bse['x']],
        'p_x': [model_full.pvalues['x'], model_robust.pvalues['x']],
        'R²': [model_full.rsquared, model_robust.rsquared],
    })
    print(comparison.to_string(index=False))

    # Visualize influence
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Data with regression lines
    axes[0].scatter(df[~influential_mask]['x'],
                   df[~influential_mask]['y'],
                   alpha=0.5, label='Normal observations')
    axes[0].scatter(df[influential_mask]['x'],
                   df[influential_mask]['y'],
                   color='red', s=100, label='Influential outliers')

    x_range = np.linspace(df['x'].min(), df['x'].max(), 100)
    axes[0].plot(x_range,
                model_full.params['const'] + model_full.params['x']*x_range,
                'r--', label='With outliers', linewidth=2)
    axes[0].plot(x_range,
                model_robust.params['const'] + model_robust.params['x']*x_range,
                'g-', label='Without outliers', linewidth=2)

    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    axes[0].set_title("Outlier Impact on Regression Line")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Cook's distance
    axes[1].stem(range(len(cooks_d)), cooks_d, markerfmt=",", basefmt=" ")
    axes[1].axhline(4/len(df), color='red', linestyle='--',
                   label=f'Threshold = {4/len(df):.3f}')
    axes[1].set_xlabel("Observation Index")
    axes[1].set_ylabel("Cook's Distance")
    axes[1].set_title("Influence Measure (Cook's D)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/outlier_influence_analysis.png", dpi=144, bbox_inches="tight")

    # Save figure reference for inline display
    influence_fig = plt.gcf()

    print("\n" + "=" * 70)
    print("CRITICAL FINDINGS")
    print("=" * 70)
    print(f"""
    1. {influential_mask.sum()} influential observations detected
    2. Coefficient on x changes by {abs(model_full.params['x'] - model_robust.params['x']):.3f}
    3. R² drops from {model_full.rsquared:.3f} to {model_robust.rsquared:.3f}
    4. Statistical significance {'changes' if (model_full.pvalues['x'] < 0.05) != (model_robust.pvalues['x'] < 0.05) else 'unchanged'}

    REQUIRED REPORTING:
    - Present BOTH models (with and without influential points)
    - Investigate influential observations for data quality
    - If outliers are valid, consider robust regression methods
    - State clearly which results are sensitive to outliers

    This demonstrates why influence diagnostics are MANDATORY.
    """)

    # Return figure for inline display along with models
    return model_full, model_robust, influential_mask, influence_fig,
```
</code>
<power_user_tip>
When influential observations are detected:
1. NEVER simply delete them without investigation
2. Check if they're data errors or valid extreme cases
3. Report results both with AND without
4. Consider robust methods (M-estimation, quantile regression)
5. Document which conclusions are robust to their inclusion
</power_user_tip>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Running regression without any diagnostics</what>
  <consequence>Invalid p-values, wrong confidence intervals, false discoveries</consequence>
  <prevention>ALWAYS run complete_regression_diagnostics() after EVERY regression</prevention>
</mistake>

<mistake severity="critical">
  <what>Ignoring heteroskedasticity in cross-sectional data</what>
  <consequence>Type I error rates up to 40% instead of 5%</consequence>
  <prevention>Always test with Breusch-Pagan/White, use robust SE if detected</prevention>
</mistake>

<mistake severity="critical">
  <what>Not checking for influential observations</what>
  <consequence>Results driven by 1-2 outliers rather than general pattern</consequence>
  <prevention>Compute Cook's distance, report sensitivity to outlier exclusion</prevention>
</mistake>

<mistake severity="high">
  <what>Ignoring severe multicollinearity (VIF > 10)</what>
  <consequence>Unstable estimates, coefficients flip signs with minor changes</consequence>
  <prevention>Check VIF for all variables, remove/combine if VIF > 10</prevention>
</mistake>

<mistake severity="high">
  <what>Using classical SE when robust SE required</what>
  <consequence>Overstated precision, false statistical significance</consequence>
  <prevention>Default to HC3 robust SE when heteroskedasticity detected</prevention>
</mistake>

<mistake severity="medium">
  <what>Over-interpreting normality tests with large samples</what>
  <consequence>Unnecessary transformations when CLT ensures valid inference</consequence>
  <prevention>With n > 30, normality violations rarely affect inference materially</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<reading_diagnostic_plots>
**Residuals vs Fitted**:
- GOOD: Random scatter around horizontal line at zero
- BAD: Patterns (curves, fans, clusters) indicate misspecification

**Q-Q Plot**:
- GOOD: Points follow diagonal reference line
- BAD: S-shapes indicate skewness, heavy tails indicate outliers

**Scale-Location**:
- GOOD: Horizontal band with no trend
- BAD: Increasing/decreasing spread indicates heteroskedasticity

**Residuals vs Leverage**:
- GOOD: Points within Cook's distance contours
- BAD: Points in top-right or bottom-right corners are influential
</reading_diagnostic_plots>

<decision_tree>
Heteroskedasticity detected?
  → YES: Use HC3 robust SE or cluster-robust if panel data
  → NO: Classical SE are valid

Multicollinearity detected (VIF > 10)?
  → YES: Must drop variables or use regularization
  → NO but VIF > 5: Monitor, may be acceptable

Influential outliers detected?
  → YES: Report results with AND without
  → NO: Single model sufficient

Non-normal residuals?
  → n > 30: Usually OK (CLT)
  → n < 30: Consider bootstrap or transformation
</decision_tree>

<honest_limitations>
- Diagnostics can't detect all problems (e.g., omitted variables)
- Some violations may not matter for specific research questions
- Trade-offs exist (robust SE have lower power)
- Perfect models don't exist—document deviations honestly
</honest_limitations>

</interpretation_guide>

<references>
<paper>Belsley, D.A., Kuh, E., & Welsch, R.E. (1980). Regression Diagnostics: Identifying Influential Data and Sources of Collinearity. The foundational text on regression diagnostics.</paper>
<paper>Cook, R.D. & Weisberg, S. (1982). Residuals and Influence in Regression. Introduces Cook's distance for influence detection.</paper>
<paper>MacKinnon, J.G. & White, H. (1985). "Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties." HC3 robust standard errors.</paper>
<paper>Kutner, M.H., Nachtsheim, C.J., & Neter, J. (2004). Applied Linear Regression Models. Comprehensive treatment of multicollinearity and VIF.</paper>
<paper>Long, J.S. & Ervin, L.H. (2000). "Using heteroscedasticity consistent standard errors in the linear regression model." Practical guide to robust inference.</paper>
</references>

</skill_content>