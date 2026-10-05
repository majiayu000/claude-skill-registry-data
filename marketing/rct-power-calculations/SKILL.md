---
name: rct-power-calculations
description: "Calculate statistical power and sample sizes for RCTs. Use when user mentions: power analysis, sample size calculation, minimum detectable effect, MDE, statistical power, effect size, clustering effects, design effect, ICC, intra-cluster correlation."
---

<skill_content>

<overview>
Power analysis determines the sample size required to detect treatment effects of a given magnitude with specified probability. Adequate power prevents Type II errors (failing to detect real effects). Power calculations must account for clustering (design effects), non-compliance (reduces effective sample), attrition (reduces final sample), and multiple testing (inflates α). Underpowered studies waste resources and risk being misinterpreted as evidence of no effect.

Power = 80% is conventional. Higher power (90%) is better when study is expensive or one-shot.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Conduct Power Analysis Before Data Collection</name>
  <description>Calculate required sample size BEFORE starting enrollment or randomization</description>
  <rationale>Post-hoc power calculations are meaningless. Power must guide design, not rationalize results (Hoenig & Heisey 2001)</rationale>
  <consequence>Underpowered studies waste resources, fail to detect real effects, mislead policy with false nulls</consequence>
</requirement>

<requirement priority="critical">
  <name>Account for Clustering Design Effects</name>
  <description>When using cluster randomization, multiply base sample size by design effect: DE = 1 + (m-1) × ICC</description>
  <rationale>Clustering reduces effective sample size due to within-cluster correlation. Ignoring this causes severe underpowering (Donner & Klar 2000)</rationale>
  <consequence>Studies underpowered by 2-4x, inability to detect real effects despite large nominal sample</consequence>
</requirement>

<requirement priority="critical">
  <name>Inflate for Attrition and Non-Compliance</name>
  <description>Adjust sample size for expected attrition and imperfect compliance before finalizing design</description>
  <rationale>Attrition reduces final sample. Non-compliance attenuates ITT effects. Both reduce power substantially</rationale>
  <consequence>Final analysis underpowered even if initial enrollment meets naive power target</consequence>
</requirement>

<requirement priority="high">
  <name>Use Realistic Effect Sizes</name>
  <description>Base MDE on pilot data, similar interventions, or smallest policy-relevant effect, not on wishful thinking</description>
  <rationale>Overoptimistic effect size assumptions guarantee underpowered study. True effects in social science typically 0.1-0.3 SD (Vivalt 2020)</rationale>
  <consequence>Study designed to detect implausibly large effects, fails to detect realistic effects, wasted resources</consequence>
</requirement>

<requirement priority="high">
  <name>Adjust for Multiple Comparisons</name>
  <description>When testing multiple outcomes, increase sample size or reduce α to maintain family-wise error rate</description>
  <rationale>Multiple testing inflates Type I error. With 5 tests at α=0.05, false positive rate is 26% not 5%</rationale>
  <consequence>Study powered for single test but not for actual analysis plan, false discoveries</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="Effect Size Estimate">
  <description>Assumed MDE or effect size is realistic based on prior evidence or theory</description>
  <how_to_check>Review similar interventions, conduct pilot, consult domain experts, use smallest policy-relevant effect</how_to_check>
  <if_violated>Study either grossly overpowered (wasteful) or underpowered (fails to detect real effects)</if_violated>
</assumption>

<assumption name="ICC Estimate for Cluster Designs">
  <description>Assumed intra-cluster correlation reflects true within-cluster similarity</description>
  <how_to_check>Use baseline data from same clusters, similar studies, or conservative upper bound (ICC=0.10-0.20)</how_to_check>
  <if_violated>Design effect wrong → sample size wrong → power incorrect</if_violated>
</assumption>

<assumption name="Attrition and Compliance Rates">
  <description>Expected attrition and take-up rates match what actually occurs</description>
  <how_to_check>Base on pilot data, similar studies in same context, plan retention strategies</how_to_check>
  <if_violated>Actual power lower than designed power, inability to detect effects</if_violated>
</assumption>

</assumptions>

<thinking_process>
When conducting power analysis:
1. Specify primary outcome and effect size (MDE or expected effect)
2. Choose significance level (α=0.05 typical) and desired power (0.80-0.90)
3. Calculate base sample size for simple design
4. Apply design effect if cluster randomization (multiply by 1+(m-1)×ICC)
5. Inflate for expected non-compliance (divide by compliance²)
6. Inflate for expected attrition (divide by (1-attrition_rate))
7. Adjust for multiple testing if applicable
8. Check feasibility; if infeasible, reduce scope or accept larger MDE
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def comprehensive_power_calculation():
    # Full power calculation with all real-world adjustments
    # Demonstrates compounding inflation factors for RCT sample size

    import numpy as np
    from scipy.stats import norm

    # Parameters
    alpha = 0.05
    power = 0.80
    mde = 0.25  # Effect size in SD units (realistic for social programs)
    p = 0.50  # Treatment allocation

    # Base calculation
    z_alpha = norm.ppf(1 - alpha/2)
    z_power = norm.ppf(power)
    n_base = ((z_alpha + z_power)**2) / (p * (1-p) * mde**2)

    print(f"COMPREHENSIVE POWER ANALYSIS")
    print(f"=" * 60)
    print(f"Parameters: α={alpha}, power={power}, MDE={mde} SD")
    print(f"\n1. Base sample size: {int(np.ceil(n_base))}")

    # Adjustment 1: Clustering
    icc = 0.05
    cluster_size = 30
    design_effect = 1 + (cluster_size - 1) * icc
    n_after_clustering = n_base * design_effect

    print(f"\n2. Clustering adjustment:")
    print(f"   ICC={icc}, avg cluster size={cluster_size}")
    print(f"   Design effect: {design_effect:.2f}")
    print(f"   After clustering: {int(np.ceil(n_after_clustering))}")

    # Adjustment 2: Non-compliance
    compliance_rate = 0.70
    n_after_compliance = n_after_clustering / (compliance_rate**2)

    print(f"\n3. Non-compliance adjustment:")
    print(f"   Expected compliance: {compliance_rate:.0%}")
    print(f"   Inflation factor: {1/compliance_rate**2:.2f}")
    print(f"   After compliance: {int(np.ceil(n_after_compliance))}")

    # Adjustment 3: Attrition
    attrition_rate = 0.20
    n_final = n_after_compliance / (1 - attrition_rate)

    print(f"\n4. Attrition adjustment:")
    print(f"   Expected attrition: {attrition_rate:.0%}")
    print(f"   Inflation factor: {1/(1-attrition_rate):.2f}")
    print(f"   FINAL REQUIRED N: {int(np.ceil(n_final))}")

    print(f"\n" + "=" * 60)
    print(f"Total inflation: {n_final/n_base:.2f}x base sample size")
    print(f"Baseline N needed: {int(np.ceil(n_final))}")
    print(f"Endline N expected: {int(np.ceil(n_final * (1-attrition_rate)))}")

    return int(np.ceil(n_final)),
```
</code_template>

</implementation_pattern>

<examples>

<example context="cluster_rct_power" difficulty="intermediate">
<description>Calculate power for cluster-randomized trial with design effect</description>
<code>
```python
@app.cell
def cluster_rct_power():
    # Cluster RCT power accounting for design effect
    # Shows how clustering can reduce power by 2-4x

    import numpy as np
    from scipy.stats import norm

    alpha = 0.05
    power = 0.80
    mde = 0.30

    # Individual randomization (baseline)
    z_a = norm.ppf(1 - alpha/2)
    z_p = norm.ppf(power)
    n_individual = ((z_a + z_p)**2) / (0.25 * mde**2)

    print(f"CLUSTER vs. INDIVIDUAL RANDOMIZATION")
    print(f"=" * 60)
    print(f"Individual randomization: {int(np.ceil(n_individual))} participants")

    # Cluster randomization scenarios
    scenarios = [
        {"icc": 0.05, "cluster_size": 20},
        {"icc": 0.05, "cluster_size": 50},
        {"icc": 0.10, "cluster_size": 30},
        {"icc": 0.20, "cluster_size": 30},
    ]

    for scenario in scenarios:
        icc = scenario["icc"]
        m = scenario["cluster_size"]
        de = 1 + (m - 1) * icc
        n_cluster = n_individual * de
        n_clusters_needed = int(np.ceil(n_cluster / m))

        print(f"\nICC={icc}, cluster size={m}:")
        print(f"  Design effect: {de:.2f}")
        print(f"  Total N needed: {int(np.ceil(n_cluster))}")
        print(f"  Clusters needed: {n_clusters_needed}")
        print(f"  Inflation: {de:.2f}x individual design")

    print("\nKey lesson: Higher ICC or larger clusters → much larger N needed")

    return ()
```
</code>
<lesson>
Design effect = 1 + (m-1) × ICC. With ICC=0.10 and m=30, DE=3.9, meaning you need 4x the individual-randomized sample size. Cluster randomization trades power for validity when spillovers are a concern.
</lesson>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Conducting power analysis after data collection (post-hoc power)</what>
  <consequence>Meaningless exercise, doesn't inform anything, misinterpreted as evidence quality</consequence>
  <prevention>Power analysis is for design phase only. Never calculate "observed power" after study</prevention>
</mistake>

<mistake severity="critical">
  <what>Ignoring clustering design effect in sample size calculation</what>
  <consequence>Study underpowered by 2-4x, fails to detect real effects despite large nominal sample</consequence>
  <prevention>ALWAYS multiply by design effect DE = 1+(m-1)×ICC for cluster randomization</prevention>
</mistake>

<mistake severity="high">
  <what>Using overoptimistic effect size assumptions</what>
  <consequence>Study designed to detect implausibly large effects, fails for realistic effects</consequence>
  <prevention>Use conservative estimates from pilots, literature, or smallest policy-relevant effect</prevention>
</mistake>

<mistake severity="high">
  <what>Not inflating for attrition and non-compliance</what>
  <consequence>Final analysis underpowered even if enrollment meets naive target</consequence>
  <prevention>Always inflate for expected attrition (÷ (1-attrition_rate)) and compliance (÷ compliance²)</prevention>
</mistake>

<mistake severity="medium">
  <what>Treating power as binary threshold (80% good, 79% bad)</what>
  <consequence>Arbitrary decisions, missing that power is continuous and context-dependent</consequence>
  <prevention>Power is a continuum. Consider costs, effect importance, and Type I vs. II error tradeoffs</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<sample_size_rules_of_thumb>
For 80% power, α=0.05, 50/50 allocation:
- MDE = 0.10 SD: ~3,140 total
- MDE = 0.20 SD: ~786 total
- MDE = 0.30 SD: ~350 total
- MDE = 0.40 SD: ~198 total
- MDE = 0.50 SD: ~128 total

Then multiply by:
- Design effect if clustering: 1+(m-1)×ICC
- 1/compliance² for non-compliance
- 1/(1-attrition_rate) for attrition
</sample_size_rules_of_thumb>

<when_study_is_underpowered>
If power calculation shows infeasible N:
- Increase MDE (accept detecting only larger effects)
- Reduce scope (fewer outcomes, simpler design)
- Improve efficiency (stratification, ANCOVA with baseline)
- Pool with other studies (consortium approach)
- Use alternative design (regression discontinuity, DID)
- Accept higher Type II error risk (document explicitly)

Do NOT: proceed with underpowered study and hope for best.
</when_study_is_underpowered>

</interpretation_guide>

<references>
<paper>Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences. 2nd ed. Erlbaum.</paper>
<paper>Duflo, E., Glennerster, R., & Kremer, M. (2007). Using randomization in development economics research. Handbook of Development Economics, 4, 3895-3962.</paper>
<paper>Donner, A., & Klar, N. (2000). Design and Analysis of Cluster Randomization Trials in Health Research. Arnold Publishers.</paper>
<paper>Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power: The pervasive fallacy of power calculations for data analysis. American Statistician, 55(1), 19-24.</paper>
<paper>Vivalt, E. (2020). How much can we generalize from impact evaluations? Journal of the European Economic Association, 18(6), 3045-3089.</paper>
</references>

</skill_content>
