---
name: difference-in-differences
description: "Causal inference with treatment/control groups over time. Use when user mentions: treatment effects, policy evaluation, pre/post comparison, parallel trends, DID, DiD, difference in differences, natural experiment, quasi-experimental."

---

<skill_content>

<overview>
Difference-in-Differences (DID) is a causal inference method that estimates treatment effects by comparing changes over time between treated and control groups. It leverages both cross-sectional and temporal variation to identify causal effects when randomization is infeasible.

DID is the workhorse of policy evaluation in economics and social sciences.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Parallel Trends Testing</name>
  <description>MUST test the parallel trends assumption using pre-treatment data</description>
  <rationale>Parallel trends is THE identifying assumption. Without it, DID estimates are biased. Violations have invalidated numerous published studies (Roth, 2022)</rationale>
  <consequence>Biased treatment effect estimates that could be entirely spurious</consequence>
</requirement>

<requirement priority="critical">
  <name>Cluster-Robust Standard Errors</name>
  <description>MUST cluster standard errors at the treatment level</description>
  <rationale>Serial correlation within units severely underestimates standard errors. Bertrand, Duflo & Mullainathan (2004) show 45% false positive rate with unclustered SE</rationale>
  <consequence>Type I error rates can exceed 45% instead of 5%</consequence>
</requirement>

<requirement priority="critical">
  <name>Event Study Specification</name>
  <description>MUST run event study with leads and lags when multiple pre-periods exist</description>
  <rationale>Event studies reveal dynamics, test pre-trends, and detect anticipation effects simultaneously (Sun & Abraham, 2021)</rationale>
  <consequence>Missing pre-trends violations, anticipation effects, or dynamic treatment effects</consequence>
</requirement>

<requirement priority="high">
  <name>Clear Treatment Timing</name>
  <description>Document exactly when treatment starts and who is treated</description>
  <rationale>Ambiguous treatment timing or definition makes results unreplicable and potentially wrong</rationale>
  <consequence>Wrong attribution of effects to treatment</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="Parallel Trends">
  <description>Treatment and control groups would follow parallel trajectories absent treatment</description>
  <how_to_check>Visual inspection of pre-trends, event study coefficients on leads, formal pre-trends test</how_to_check>
  <if_violated>Consider synthetic control, changes-in-changes, or interactive fixed effects</if_violated>
</assumption>

<assumption name="No Anticipation">
  <description>Units don't change behavior before treatment actually occurs</description>
  <how_to_check>Check event study leads immediately before treatment</how_to_check>
  <if_violated>Redefine treatment timing to when announcement occurred</if_violated>
</assumption>

<assumption name="SUTVA">
  <description>No spillovers between treated and control units</description>
  <how_to_check>Test for spatial correlation, check economic linkages</how_to_check>
  <if_violated>Exclude contaminated controls or use spatial methods</if_violated>
</assumption>

<assumption name="Common Support">
  <description>Treatment and control groups are comparable</description>
  <how_to_check>Compare covariate distributions and pre-treatment outcomes</how_to_check>
  <if_violated>Consider matching or weighting before DID</if_violated>
</assumption>

</assumptions>

<thinking_process>
When implementing DID:
1. Verify panel structure and treatment timing
2. Check pre-treatment balance between groups
3. Test parallel trends assumption (CRITICAL)
4. Implement main DID specification
5. Run event study for dynamics
6. Conduct robustness checks
7. Interpret magnitude and significance carefully
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def did_with_diagnostics(df):
    # Implementing DID with all required diagnostics to ensure valid causal
    # inference. Following Angrist & Pischke (2009) and recent best practices
    # from Roth et al. (2023) on credible DID designs.

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt
    import os

    # MANDATORY: Validate panel structure
    required = {"outcome", "treat", "post", "unit_id", "time", "cluster_id"}
    assert required.issubset(df.columns), f"Missing columns: {required - set(df.columns)}"

    # Verify treatment is binary
    assert df["treat"].isin([0, 1]).all(), "Treatment must be binary (0/1)"

    # Check panel balance
    panel_check = df.groupby("unit_id")["time"].nunique()
    is_balanced = (panel_check == panel_check.iloc[0]).all()
    print(f"Panel structure: {'Balanced' if is_balanced else 'Unbalanced'}")

    # MANDATORY: Test parallel trends visually
    pre_data = df[df["post"] == 0].copy()
    trends = pre_data.groupby(["time", "treat"])["outcome"].mean().unstack()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Pre-trends plot
    axes[0].plot(trends.index, trends[0], marker='o', label='Control', linewidth=2)
    axes[0].plot(trends.index, trends[1], marker='s', label='Treatment', linewidth=2)
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Outcome (mean)")
    axes[0].set_title("Pre-Treatment Trends (Parallel Trends Check)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # MANDATORY: Statistical test for parallel trends
    if len(pre_data["time"].unique()) >= 3:
        # Test for differential trends in pre-period
        pre_data["time_trend"] = pre_data.groupby("unit_id")["time"].transform(lambda x: x - x.min())
        pre_data["treat_trend"] = pre_data["treat"] * pre_data["time_trend"]

        trend_test = smf.ols(
            "outcome ~ treat + time_trend + treat_trend + C(unit_id) + C(time)",
            data=pre_data
        ).fit(cov_type="cluster", cov_kwds={"groups": pre_data["cluster_id"]})

        trend_coef = trend_test.params.get("treat_trend", 0)
        trend_pval = trend_test.pvalues.get("treat_trend", 1)

        print("\n" + "=" * 60)
        print("PARALLEL TRENDS TEST")
        print("=" * 60)
        print(f"Differential trend coefficient: {trend_coef:.4f}")
        print(f"P-value: {trend_pval:.4f}")
        if trend_pval < 0.05:
            print("WARNING: Parallel trends assumption may be violated!")
        else:
            print("SUCCESS: No significant differential pre-trends detected")

    # MANDATORY: Main DID estimation with cluster-robust SE
    df_did = df.copy()
    df_did["did"] = df_did["treat"] * df_did["post"]

    # Two-way fixed effects specification
    did_model = smf.ols(
        "outcome ~ did + C(unit_id) + C(time)",
        data=df_did
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": df_did["cluster_id"]}
    )

    # Extract key results
    did_coef = did_model.params["did"]
    did_se = did_model.bse["did"]
    did_pval = did_model.pvalues["did"]
    ci_lower = did_coef - 1.96 * did_se
    ci_upper = did_coef + 1.96 * did_se

    print("\n" + "=" * 60)
    print("DIFFERENCE-IN-DIFFERENCES RESULTS")
    print("=" * 60)
    print(f"Treatment Effect: {did_coef:.4f}")
    print(f"Clustered SE: {did_se:.4f}")
    print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"P-value: {did_pval:.4f}")
    print(f"\nClustering: {df_did['cluster_id'].nunique()} clusters")
    print(f"N observations: {len(df_did):,}")

    # MANDATORY: Event study for dynamics and further pre-trends check
    # Create relative time variable if not exists
    if "rel_time" not in df.columns:
        treatment_time = df[df["post"] == 1].groupby("unit_id")["time"].min()
        df["treatment_time"] = df["unit_id"].map(treatment_time)
        df["rel_time"] = df["time"] - df["treatment_time"]
        df.loc[df["treat"] == 0, "rel_time"] = -999  # Never treated

    # Event study with reasonable window
    event_window = range(-4, 5)  # 4 pre, 4 post periods
    df_event = df[(df["rel_time"].isin(event_window)) | (df["rel_time"] == -999)].copy()

    # Create event time dummies (omit -1 as reference)
    for k in event_window:
        if k == -1:
            continue
        df_event[f"event_{k}"] = ((df_event["rel_time"] == k) & (df_event["treat"] == 1)).astype(int)

    # Build formula
    event_vars = [f"event_{k}" for k in event_window if k != -1]
    event_formula = "outcome ~ " + " + ".join(event_vars) + " + C(unit_id) + C(time)"

    event_model = smf.ols(event_formula, data=df_event).fit(
        cov_type="cluster",
        cov_kwds={"groups": df_event["cluster_id"]}
    )

    # Plot event study
    periods = [k for k in event_window if k != -1]
    coefs = [event_model.params.get(f"event_{k}", 0) for k in periods]
    ses = [event_model.bse.get(f"event_{k}", 0) for k in periods]

    axes[1].axhline(0, color='gray', linestyle='--', alpha=0.5)
    axes[1].axvline(-0.5, color='red', linestyle='--', alpha=0.5, label='Treatment')
    axes[1].errorbar(periods, coefs, yerr=[1.96*s for s in ses],
                     marker='o', capsize=5, linewidth=2)
    axes[1].set_xlabel("Relative Time to Treatment")
    axes[1].set_ylabel("Effect Estimate")
    axes[1].set_title("Event Study (Pre-trends & Dynamics)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # MANDATORY: Save diagnostic plots
    plt.tight_layout()
    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/did_diagnostics.png", dpi=144, bbox_inches="tight")

    print(f"\nSUCCESS: Diagnostic plots saved to ./images/did_diagnostics.png")

    # Get figure for inline display
    fig = plt.gcf()
    return did_model, event_model, fig,
```
</code_template>

</implementation_pattern>

<examples>

<example context="clean_2x2" difficulty="basic">
<description>Classic 2×2 DID with one treatment group and two periods</description>
<code>
```python
@app.cell
def did_2x2_simple(df):
    # Implementing the canonical 2×2 DID where we have one treatment group,
    # one control group, and two time periods. This is the simplest and most
    # transparent DID design (Card & Krueger, 1994).

    import statsmodels.formula.api as smf
    import pandas as pd

    # Verify 2×2 structure
    assert df["treat"].nunique() == 2, "Need exactly 2 groups"
    assert df["time"].nunique() == 2, "Need exactly 2 time periods"
    assert df["post"].nunique() == 2, "Need pre and post indicators"

    # Calculate means for 2×2 table
    means = df.groupby(["treat", "post"])["outcome"].mean().unstack()

    print("2×2 DID Table")
    print("=" * 50)
    print(means)

    # Manual DID calculation for transparency
    diff_treat = means.loc[1, 1] - means.loc[1, 0]  # Treatment group change
    diff_control = means.loc[0, 1] - means.loc[0, 0]  # Control group change
    did_manual = diff_treat - diff_control

    print(f"\nManual DID Calculation:")
    print(f"  Treatment group change: {diff_treat:.4f}")
    print(f"  Control group change: {diff_control:.4f}")
    print(f"  DID estimate: {did_manual:.4f}")

    # Regression approach (should match manual calculation)
    df["did"] = df["treat"] * df["post"]
    model = smf.ols("outcome ~ treat + post + did", data=df).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["cluster_id"]}
    )

    print(f"\nRegression DID estimate: {model.params['did']:.4f}")
    print(f"Clustered SE: {model.bse['did']:.4f}")
    print(f"P-value: {model.pvalues['did']:.4f}")

    # Interpretation
    baseline_mean = means.loc[1, 0]  # Pre-treatment mean for treated group
    pct_effect = (model.params['did'] / baseline_mean) * 100

    print(f"\nEffect size: {pct_effect:.1f}% relative to baseline")

    return model,
```
</code>
<output_interpretation>
In 2×2 DID:
- The coefficient represents the average treatment effect on the treated (ATT)
- Compare manual and regression estimates to verify implementation
- Report both absolute and relative (%) effects for context
</output_interpretation>
</example>

<example context="staggered_adoption" difficulty="intermediate">
<description>Staggered treatment adoption with heterogeneous effects</description>
<code>
```python
@app.cell
def did_staggered_robust(df):
    # Standard TWFE DID is biased with staggered adoption and heterogeneous
    # effects (Goodman-Bacon, 2021). We implement both standard TWFE and
    # robust alternatives (Callaway & Sant'Anna, 2021).

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf

    # Check for staggered adoption
    treatment_times = df[df["treat"] == 1].groupby("unit_id")["time"].min()
    n_cohorts = treatment_times.nunique()

    print("Staggered Adoption Structure")
    print("=" * 50)
    print(f"Number of treatment cohorts: {n_cohorts}")
    print("\nTreatment timing distribution:")
    print(treatment_times.value_counts().sort_index())

    if n_cohorts > 1:
        print("\nWARNING: Staggered adoption detected!")
        print("Standard TWFE may be biased. Showing both approaches:")

    # 1. Standard TWFE (potentially biased)
    print("\n1. STANDARD TWFE APPROACH")
    print("-" * 40)

    df["treated_post"] = (df["treat"] == 1) & (df["post"] == 1)
    twfe = smf.ols(
        "outcome ~ treated_post + C(unit_id) + C(time)",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["cluster_id"]})

    print(f"TWFE estimate: {twfe.params['treated_post[T.True]']:.4f}")
    print(f"SE: {twfe.bse['treated_post[T.True]']:.4f}")

    # 2. Cohort-specific effects (diagnostic)
    print("\n2. COHORT-SPECIFIC EFFECTS")
    print("-" * 40)

    cohort_effects = {}
    for cohort_time in treatment_times.unique():
        cohort_units = treatment_times[treatment_times == cohort_time].index

        # Get cohort data plus never-treated controls
        cohort_data = df[
            (df["unit_id"].isin(cohort_units)) |
            (df["treat"] == 0)
        ].copy()

        cohort_data["post_cohort"] = cohort_data["time"] >= cohort_time
        cohort_data["did_cohort"] = (
            cohort_data["unit_id"].isin(cohort_units) &
            cohort_data["post_cohort"]
        )

        cohort_model = smf.ols(
            "outcome ~ did_cohort + C(unit_id) + C(time)",
            data=cohort_data
        ).fit(cov_type="cluster", cov_kwds={"groups": cohort_data["cluster_id"]})

        effect = cohort_model.params.get("did_cohort[T.True]", np.nan)
        cohort_effects[cohort_time] = effect
        print(f"Cohort {cohort_time}: {effect:.4f}")

    # Check for heterogeneity
    effects_array = np.array(list(cohort_effects.values()))
    heterogeneity = effects_array.std()

    print(f"\nHeterogeneity check:")
    print(f"  SD of cohort effects: {heterogeneity:.4f}")
    if heterogeneity > abs(effects_array.mean()) * 0.5:
        print("  WARNING: Substantial heterogeneity detected!")
        print("  Consider using robust DID methods (CS, SA, or Sun-Abraham)")

    # 3. Simple aggregation (equally weighted)
    print("\n3. SIMPLE AVERAGE OF COHORT EFFECTS")
    print("-" * 40)
    simple_avg = effects_array.mean()
    print(f"Average effect: {simple_avg:.4f}")
    print(f"Difference from TWFE: {simple_avg - twfe.params['treated_post[T.True]']:.4f}")

    return twfe, cohort_effects,
```
</code>
<lesson>
With staggered adoption:
1. TWFE can be biased due to "bad comparisons"
2. Check cohort-specific effects for heterogeneity
3. Consider modern robust estimators (Callaway-Sant'Anna, Sun-Abraham)
4. Report both standard and robust estimates for transparency
</lesson>
</example>

<example context="failed_pretrends" difficulty="advanced">
<description>Handling DID when parallel trends fails</description>
<code>
```python
@app.cell
def did_with_failed_pretrends(df):
    # When parallel trends fails, standard DID is biased. We demonstrate the
    # failure, then show alternative approaches: controlling for differential
    # trends, matching before DID, or synthetic control methods.

    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt
    import os
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighbors

    # First, demonstrate the pre-trends failure
    pre_data = df[df["post"] == 0].copy()
    pre_data["time_numeric"] = pre_data.groupby("unit_id")["time"].transform(
        lambda x: x - x.min()
    )

    # Test for differential trends
    pre_data["treat_x_time"] = pre_data["treat"] * pre_data["time_numeric"]
    trend_test = smf.ols(
        "outcome ~ treat + time_numeric + treat_x_time + C(unit_id)",
        data=pre_data
    ).fit(cov_type="cluster", cov_kwds={"groups": pre_data["cluster_id"]})

    diff_trend = trend_test.params["treat_x_time"]
    p_value = trend_test.pvalues["treat_x_time"]

    print("PRE-TRENDS DIAGNOSTIC")
    print("=" * 60)
    print(f"Differential trend: {diff_trend:.4f} (p={p_value:.4f})")

    if p_value < 0.05:
        print("WARNING: PARALLEL TRENDS VIOLATED - Standard DID is biased!")
        print("\nImplementing alternative approaches:")

        # Approach 1: Control for differential trends
        print("\n1. DID WITH DIFFERENTIAL TRENDS")
        print("-" * 40)

        df_trends = df.copy()
        df_trends["time_numeric"] = df_trends.groupby("unit_id")["time"].transform(
            lambda x: x - x.min()
        )
        df_trends["treat_x_time"] = df_trends["treat"] * df_trends["time_numeric"]
        df_trends["did"] = df_trends["treat"] * df_trends["post"]

        trends_model = smf.ols(
            "outcome ~ did + treat_x_time + C(unit_id) + C(time)",
            data=df_trends
        ).fit(cov_type="cluster", cov_kwds={"groups": df_trends["cluster_id"]})

        print(f"Effect (controlling for trends): {trends_model.params['did']:.4f}")
        print(f"SE: {trends_model.bse['did']:.4f}")
        print("Note: Assumes linear differential trends continue post-treatment")

        # Approach 2: Propensity score matching + DID
        print("\n2. MATCHED DID")
        print("-" * 40)

        # Match on pre-treatment characteristics
        pre_chars = pre_data.groupby("unit_id").agg({
            "outcome": ["mean", "std", lambda x: x.iloc[-1] - x.iloc[0]],  # level, volatility, trend
            "treat": "first"
        }).reset_index()

        pre_chars.columns = ["unit_id", "pre_mean", "pre_std", "pre_trend", "treat"]

        # Estimate propensity scores
        X = pre_chars[["pre_mean", "pre_std", "pre_trend"]].values
        y = pre_chars["treat"].values

        ps_model = LogisticRegression(random_state=42)
        ps_model.fit(X, y)
        pre_chars["pscore"] = ps_model.predict_proba(X)[:, 1]

        # Match treated to control units
        treated_units = pre_chars[pre_chars["treat"] == 1]
        control_units = pre_chars[pre_chars["treat"] == 0]

        # 1:1 nearest neighbor matching on propensity score
        nn = NearestNeighbors(n_neighbors=1)
        nn.fit(control_units[["pscore"]].values)

        distances, indices = nn.kneighbors(treated_units[["pscore"]].values)

        matched_controls = control_units.iloc[indices.flatten()]["unit_id"].values
        treated_ids = treated_units["unit_id"].values

        # Create matched sample
        matched_df = df[
            df["unit_id"].isin(treated_ids) |
            df["unit_id"].isin(matched_controls)
        ].copy()

        print(f"Matched sample: {len(matched_df['unit_id'].unique())} units")
        print(f"  ({len(treated_ids)} treated, {len(matched_controls)} control)")

        # Run DID on matched sample
        matched_df["did"] = matched_df["treat"] * matched_df["post"]
        matched_model = smf.ols(
            "outcome ~ did + C(unit_id) + C(time)",
            data=matched_df
        ).fit(cov_type="cluster", cov_kwds={"groups": matched_df["cluster_id"]})

        print(f"Effect (matched DID): {matched_model.params['did']:.4f}")
        print(f"SE: {matched_model.bse['did']:.4f}")

        # Approach 3: Recommend alternatives
        print("\n3. RECOMMENDED ALTERNATIVES")
        print("-" * 40)
        print("Consider these methods when parallel trends fails:")
        print("• Synthetic Control Method (if few treated units)")
        print("• Changes-in-Changes (Athey & Imbens, 2006)")
        print("• Interactive Fixed Effects (Bai, 2009)")
        print("• Instrumental Variables (if available)")

        # Visualize the pre-trends failure and solutions
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Original pre-trends (failing)
        pre_means = pre_data.groupby(["time", "treat"])["outcome"].mean().unstack()
        axes[0].plot(pre_means.index, pre_means[0], 'o-', label='Control')
        axes[0].plot(pre_means.index, pre_means[1], 's-', label='Treatment')
        axes[0].set_title("Original: Parallel Trends FAILED")
        axes[0].set_xlabel("Time")
        axes[0].set_ylabel("Outcome")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # After matching
        matched_pre = matched_df[matched_df["post"] == 0]
        matched_means = matched_pre.groupby(["time", "treat"])["outcome"].mean().unstack()
        axes[1].plot(matched_means.index, matched_means[0], 'o-', label='Matched Control')
        axes[1].plot(matched_means.index, matched_means[1], 's-', label='Treatment')
        axes[1].set_title("After Matching: Improved Balance")
        axes[1].set_xlabel("Time")
        axes[1].set_ylabel("Outcome")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Comparison of estimates
        methods = ["Standard\nDID", "Trend-\nAdjusted", "Matched\nDID"]
        estimates = [
            df[df["treat"] == 1]["outcome"].mean() - df[df["treat"] == 0]["outcome"].mean(),
            trends_model.params["did"],
            matched_model.params["did"]
        ]
        axes[2].bar(methods, estimates)
        axes[2].set_title("Comparison of Estimates")
        axes[2].set_ylabel("Effect Estimate")
        axes[2].axhline(0, color='gray', linestyle='--', alpha=0.5)
        axes[2].grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        os.makedirs("./images", exist_ok=True)
        plt.savefig("./images/did_pretrends_failure.png", dpi=144, bbox_inches="tight")

        print("\nSUCCESS: Diagnostic plots saved to ./images/did_pretrends_failure.png")

        # Get figure for inline display
        fig = plt.gcf()
        return trends_model, matched_model, fig,

    else:
        print("SUCCESS: Parallel trends holds - proceed with standard DID")
        return None, None, None,
```
</code>
<best_practice>
When parallel trends fails:
1. NEVER ignore it - standard DID will be biased
2. Try multiple approaches and check sensitivity
3. Be transparent about the failure in reporting
4. Consider that treatment might truly be endogenous
5. Sometimes the honest answer is "we cannot identify the causal effect"
</best_practice>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Not clustering standard errors</what>
  <consequence>Type I error rates can be 45% instead of 5% (Bertrand et al., 2004)</consequence>
  <prevention>ALWAYS cluster at treatment assignment level (usually unit level)</prevention>
</mistake>

<mistake severity="critical">
  <what>Ignoring pre-trends test</what>
  <consequence>Entire estimate may be spurious if trends differ</consequence>
  <prevention>Always test and visualize pre-trends, report even if fails</prevention>
</mistake>

<mistake severity="high">
  <what>Using TWFE with heterogeneous effects and staggered adoption</what>
  <consequence>Estimate is weighted average including "bad comparisons" (negative weights)</consequence>
  <prevention>Use Callaway-Sant'Anna, Sun-Abraham, or other robust estimators</prevention>
</mistake>

<mistake severity="high">
  <what>Including bad controls (post-treatment variables)</what>
  <consequence>Bias from controlling for mechanisms</consequence>
  <prevention>Only control for pre-treatment characteristics</prevention>
</mistake>

<mistake severity="medium">
  <what>Not checking for anticipation effects</what>
  <consequence>Underestimate true effect if behavior changes before official treatment</consequence>
  <prevention>Check event study leads just before treatment</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<interpreting_results>
- DID coefficient = Average Treatment Effect on the Treated (ATT)
- Units are same as outcome variable (be specific!)
- Relative effect = (coefficient / pre-treatment mean) × 100%
- Check both statistical and economic significance
</interpreting_results>

<red_flags>
- Pre-trend coefficients significantly different from zero
- Event study shows effects before treatment (anticipation)
- Very different estimates with different specifications
- Implausibly large effects (>50% changes are rare)
</red_flags>

<next_steps>
- All checks pass → Report main estimate with confidence
- Pre-trends fail → Try alternative methods or acknowledge limitation
- Heterogeneous effects → Report by subgroup
- Dynamic effects → Focus on event study rather than single coefficient
</next_steps>

</interpretation_guide>

<references>
<paper>Angrist, J.D. & Pischke, J.S. (2009). "Mostly Harmless Econometrics." Princeton University Press. Canonical DID exposition.</paper>
<paper>Bertrand, M., Duflo, E. & Mullainathan, S. (2004). "How Much Should We Trust DID Estimates?" QJE. Serial correlation and clustering.</paper>
<paper>Roth, J. et al. (2023). "What's Trending in DID?" AER Insights. Modern best practices and pre-testing.</paper>
<paper>Goodman-Bacon, A. (2021). "DID with Variation in Treatment Timing." Journal of Econometrics. TWFE bias.</paper>
<paper>Callaway, B. & Sant'Anna, P.H.C. (2021). "DID with Multiple Time Periods." Journal of Econometrics. Robust estimation.</paper>
<paper>Sun, L. & Abraham, S. (2021). "Estimating Dynamic Treatment Effects." Journal of Econometrics. Event study bias correction.</paper>
</references>

</skill_content>