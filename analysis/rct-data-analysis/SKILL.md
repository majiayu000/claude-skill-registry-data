---
name: rct-data-analysis
description: "Analyze data from randomized controlled trials. Use when user mentions: treatment effects, ITT analysis, LATE, TOT, compliance analysis, attrition, balance checks, heterogeneous effects, RCT results, experimental analysis."
---

<skill_content>

<overview>
RCT analysis leverages randomization to identify causal effects with minimal assumptions. Intention-to-treat (ITT) provides policy-relevant estimates of assignment effects. Local average treatment effects (LATE/IV) recover efficacy for compliers. Balance checks verify randomization, attrition analysis guards against selection bias, and heterogeneity analysis reveals for whom treatment works.

Analysis must preserve the integrity of randomization through proper inference and transparent reporting.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Report ITT as Primary Result</name>
  <description>Intention-to-treat analysis MUST be reported as the main result, even with non-compliance</description>
  <rationale>ITT maintains randomization, provides policy-relevant parameter (effect of offering treatment), and prevents selection bias from endogenous compliance (Angrist & Pischke 2009)</rationale>
  <consequence>Selection bias, loss of causal interpretation, inability to make policy recommendations</consequence>
</requirement>

<requirement priority="critical">
  <name>Cluster-Robust Standard Errors</name>
  <description>Use cluster-robust (or HC3-robust) standard errors, never classical SEs</description>
  <rationale>Clustered/robust SEs account for within-cluster correlation and heteroskedasticity. Classical SEs severely underestimate uncertainty (Bertrand et al. 2004)</rationale>
  <consequence>Type I error rates of 45% instead of 5%, false positives, invalid inference</consequence>
</requirement>

<requirement priority="critical">
  <name>Balance Table Before Outcomes</name>
  <description>Check and report covariate balance on baseline characteristics before analyzing outcomes</description>
  <rationale>Balance checks verify randomization worked. Large imbalances suggest implementation problems or sampling variation requiring controls</rationale>
  <consequence>Hidden confounding, invalid attribution of effects, inability to diagnose randomization failures</consequence>
</requirement>

<requirement priority="high">
  <name>Address Attrition Explicitly</name>
  <description>Report attrition rates by treatment arm, test for differential attrition, bound effects if substantial</description>
  <rationale>Differential attrition creates selection bias that undermines randomization. Must be addressed or results are invalid (Lee 2009)</rationale>
  <consequence>Selection bias, invalid causal claims, inability to distinguish true effects from attrition-driven patterns</consequence>
</requirement>

<requirement priority="high">
  <name>Adjust for Multiple Testing When Examining Multiple Outcomes</name>
  <description>Use Bonferroni, Holm, or FDR adjustment when testing multiple hypotheses</description>
  <rationale>Multiple testing inflates Type I error rate. Without adjustment, 5% significance means 26% false positive rate with 5 tests</rationale>
  <consequence>False discoveries, overstated evidence, publication of spurious results</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="Random Attrition">
  <description>Loss to follow-up is unrelated to treatment assignment and potential outcomes</description>
  <how_to_check>Compare attrition rates by treatment arm, test for correlation with baseline characteristics</how_to_check>
  <if_violated>Use Lee bounds, IPW, or explicitly bound treatment effects under worst-case scenarios</if_violated>
</assumption>

<assumption name="Excludability (for IV/LATE)">
  <description>Random assignment affects outcome only through treatment receipt (not directly)</description>
  <how_to_check>Conceptual argument, check for alternative mechanisms (Hawthorne effects, etc.)</how_to_check>
  <if_violated>ITT is still valid and policy-relevant; LATE estimates are biased</if_violated>
</assumption>

<assumption name="Monotonicity (for IV/LATE)">
  <description>Assignment doesn't flip treatment direction (no defiers)</description>
  <how_to_check>Check if always-takers exist in control group and never-takers in treatment</how_to_check>
  <if_violated>LATE estimates are weighted average that may be misleading</if_violated>
</assumption>

</assumptions>

<thinking_process>
When analyzing RCT data:
1. Check data quality and completeness
2. Verify balance on baseline covariates
3. Calculate and report attrition rates (overall and differential)
4. Estimate ITT (primary analysis)
5. Estimate LATE if non-compliance exists (secondary)
6. Test for heterogeneous effects (pre-specified subgroups)
7. Conduct robustness checks (alternative specifications)
8. Report all results transparently (including null findings)
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def itt_analysis_rct(df):
    # Intention-to-treat analysis: Effect of assignment to treatment
    # This is the policy-relevant parameter even with imperfect compliance

    import statsmodels.formula.api as smf
    import pandas as pd

    # Verify data structure
    required = {'outcome', 'treatment', 'unit_id'}
    assert required.issubset(df.columns), f"Missing columns: {required - set(df.columns)}"

    # CRITICAL: Use cluster-robust or HC3-robust standard errors
    if 'cluster_id' in df.columns:
        # Cluster-robust (for cluster-randomized trials)
        model = smf.ols("outcome ~ treatment", data=df).fit(
            cov_type='cluster',
            cov_kwds={'groups': df['cluster_id']}
        )
        se_type = "Cluster-robust"
    else:
        # HC3-robust (for individual randomization)
        model = smf.ols("outcome ~ treatment", data=df).fit(cov_type='HC3')
        se_type = "HC3-robust"

    # Extract results
    itt_effect = model.params['treatment']
    itt_se = model.bse['treatment']
    itt_pval = model.pvalues['treatment']
    ci_low, ci_high = model.conf_int().loc['treatment']

    # Context for interpretation
    control_mean = df[df['treatment'] == 0]['outcome'].mean()
    control_sd = df[df['treatment'] == 0]['outcome'].std()
    effect_size = itt_effect / control_sd

    print("INTENTION-TO-TREAT (ITT) ANALYSIS")
    print("=" * 60)
    print(f"Outcome: {df.columns[df.columns.get_loc('outcome')]}")
    print(f"N: {len(df)} ({df['treatment'].sum()} treatment, {(~df['treatment'].astype(bool)).sum()} control)")
    print(f"Standard errors: {se_type}")
    print(f"\nITT Effect: {itt_effect:.4f}")
    print(f"Std. Error: {itt_se:.4f}")
    print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
    print(f"p-value: {itt_pval:.4f}")
    print(f"\nControl mean: {control_mean:.4f}")
    print(f"Effect size: {effect_size:.3f} SD")
    print(f"Relative effect: {100*itt_effect/control_mean:.1f}%")

    return model,
```
</code_template>

</implementation_pattern>

<examples>

<example context="balance_check" difficulty="basic">
<description>Verify randomization balance before analyzing outcomes</description>
<code>
```python
@app.cell
def check_balance(df):
    # Balance checks verify randomization succeeded
    # Large imbalances may require controls or suggest implementation issues

    import pandas as pd
    import numpy as np
    from scipy import stats

    # Baseline covariates (measured before randomization)
    baseline_vars = ['age', 'education', 'income', 'baseline_outcome']

    results = []
    for var in baseline_vars:
        # Means by treatment group
        control_mean = df[df['treatment'] == 0][var].mean()
        treat_mean = df[df['treatment'] == 1][var].mean()

        # Normalized difference (Imbens & Rubin 2015)
        control_var = df[df['treatment'] == 0][var].var()
        treat_var = df[df['treatment'] == 1][var].var()
        norm_diff = (treat_mean - control_mean) / np.sqrt((control_var + treat_var) / 2)

        # T-test
        t_stat, p_val = stats.ttest_ind(
            df[df['treatment'] == 0][var].dropna(),
            df[df['treatment'] == 1][var].dropna()
        )

        results.append({
            'Variable': var,
            'Control': f"{control_mean:.3f}",
            'Treatment': f"{treat_mean:.3f}",
            'Norm Diff': f"{norm_diff:.3f}",
            'p-value': f"{p_val:.3f}"
        })

    balance_table = pd.DataFrame(results)

    print("BALANCE TABLE")
    print("=" * 60)
    print(balance_table.to_string(index=False))

    # Joint F-test
    from statsmodels.formula.api import ols
    formula = "treatment ~ " + " + ".join(baseline_vars)
    joint_model = ols(formula, data=df).fit()

    print(f"\nJoint F-test: F={joint_model.fvalue:.3f}, p={joint_model.f_pvalue:.4f}")

    # Flag concerns
    large_diffs = sum(abs(float(r['Norm Diff'])) > 0.25 for r in results)
    if large_diffs > 0:
        print(f"\nNote: {large_diffs} variables have |norm diff| > 0.25")
        print("Consider including these as controls in regression")

    return balance_table,
```
</code>
<lesson>
Balance checks use baseline (pre-randomization) covariates only. Large imbalances (|norm diff| > 0.25) don't invalidate randomization but suggest including those variables as controls to improve precision. Never use post-treatment variables for balance checks.
</lesson>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Not using cluster-robust or heteroskedasticity-robust standard errors</what>
  <consequence>Type I error rates can be 45% instead of 5%, leading to massive false positive rates</consequence>
  <prevention>ALWAYS use cov_type='cluster' or cov_type='HC3'. Never use default SEs.</prevention>
</mistake>

<mistake severity="critical">
  <what>Not reporting ITT when non-compliance exists</what>
  <consequence>Selection bias from analyzing compliers only, loss of causal interpretation</consequence>
  <prevention>ALWAYS report ITT as primary result. LATE/TOT are secondary sensitivity analyses.</prevention>
</mistake>

<mistake severity="high">
  <what>Ignoring attrition or not testing for differential attrition</what>
  <consequence>Selection bias can completely invalidate results if attrition is differential</consequence>
  <prevention>Report attrition by arm, test differential attrition, use Lee bounds if substantial</prevention>
</mistake>

<mistake severity="high">
  <what>P-hacking through subgroups without adjustment</what>
  <consequence>Finding "significant" effects that are just Type I errors from multiple testing</consequence>
  <prevention>Pre-specify subgroups in PAP, use Bonferroni/Holm adjustment, report all tests</prevention>
</mistake>

<mistake severity="medium">
  <what>Using baseline covariates that were measured post-randomization</what>
  <consequence>Conditioning on post-treatment variables creates bias (bad controls)</consequence>
  <prevention>Only use covariates measured before randomization in balance checks and controls</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<reporting_standards>
Minimum reporting for RCT results:
- Sample size (by treatment arm)
- Balance table on baseline characteristics
- Attrition rates (overall and by arm)
- ITT estimates with cluster-robust/HC3 SEs
- 95% confidence intervals
- Control group mean (for context)
- Effect size in SD units
- P-values (exact, not <0.05)
- Number of clusters if cluster-randomized
</reporting_standards>

<red_flags>
Results are questionable if:
- No balance table provided
- Classical (non-robust) standard errors used
- ITT not reported for study with non-compliance
- Attrition >20% without bounding analysis
- Multiple outcomes tested without adjustment
- Post-treatment covariates included as controls
- Results only reported for "compliers" without ITT
</red_flags>

</interpretation_guide>

<references>
<paper>Angrist, J. D., & Pischke, J. S. (2009). Mostly Harmless Econometrics: An Empiricist's Companion. Princeton University Press.</paper>
<paper>Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How much should we trust differences-in-differences estimates? Quarterly Journal of Economics, 119(1), 249-275.</paper>
<paper>Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. Review of Economic Studies, 76(3), 1071-1102.</paper>
<paper>Imbens, G. W., & Rubin, D. B. (2015). Causal Inference in Statistics, Social, and Biomedical Sciences. Cambridge University Press.</paper>
</references>

</skill_content>
