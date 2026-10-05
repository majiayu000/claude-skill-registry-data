---
name: rct-core-design
description: "Design randomized controlled trials for causal inference. Use when user mentions: randomized evaluation, RCT, field experiment, randomized experiment, treatment assignment, causal impact, experimental design, control group, intervention evaluation."
---

<skill_content>

<overview>
Randomized Controlled Trials (RCTs) are the gold standard for causal inference when randomization is feasible. Random assignment eliminates selection bias and balances observed and unobserved confounders in expectation, enabling clean identification of treatment effects. Strong RCT design requires careful attention to power, ethics, implementation fidelity, and threats to validity.

RCTs answer "does X cause Y?" with minimal assumptions.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Pre-Registration and Pre-Analysis Plan</name>
  <description>Register trial and file pre-analysis plan BEFORE data collection or analysis begins</description>
  <rationale>Pre-registration prevents p-hacking, specification searching, and publication bias. Credibility revolution in social science demands transparency (Christensen & Miguel 2018)</rationale>
  <consequence>Results perceived as data-mined, journals may reject, inability to make credible causal claims</consequence>
</requirement>

<requirement priority="critical">
  <name>Adequate Statistical Power</name>
  <description>Conduct power analysis to ensure sufficient sample size for detecting meaningful effects</description>
  <rationale>Underpowered studies waste resources and risk null findings being misinterpreted as "no effect exists" (Button et al. 2013)</rationale>
  <consequence>Failure to detect true effects (Type II error), wasted intervention resources, misleading conclusions</consequence>
</requirement>

<requirement priority="critical">
  <name>IRB Approval Before Enrollment</name>
  <description>Obtain Institutional Review Board approval before recruiting any participants</description>
  <rationale>Ethical research requires informed consent, risk minimization, and protection of human subjects (Belmont Report 1979)</rationale>
  <consequence>Research misconduct, legal liability, inability to publish, harm to participants</consequence>
</requirement>

<requirement priority="high">
  <name>Clear Theory of Change</name>
  <description>Document logical pathway from intervention inputs to expected outcomes before implementation</description>
  <rationale>Theory of change guides measurement, timing decisions, and outcome selection. Makes assumptions testable</rationale>
  <consequence>Measuring wrong outcomes at wrong times, inability to interpret null results, missing mechanisms</consequence>
</requirement>

<requirement priority="high">
  <name>Randomization at Appropriate Level</name>
  <description>Choose randomization unit (individual, cluster, geographic) to minimize spillovers while maintaining power</description>
  <rationale>Wrong randomization level causes contamination (spillovers violate SUTVA) or severe power loss from clustering</rationale>
  <consequence>Biased estimates from spillovers OR inability to detect effects due to power loss</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="SUTVA (No Spillovers)">
  <description>Treatment of one unit doesn't affect outcomes of other units</description>
  <how_to_check>Consider geographic proximity, social networks, market equilibrium effects</how_to_check>
  <if_violated>Use cluster randomization, measure spillovers explicitly, or accept partial equilibrium estimates</if_violated>
</assumption>

<assumption name="Compliance">
  <description>Units assigned to treatment actually receive it (or model non-compliance)</description>
  <how_to_check>Monitor take-up rates during implementation, plan for imperfect compliance</how_to_check>
  <if_violated>Report ITT (policy-relevant) and use IV for LATE (efficacy for compliers)</if_violated>
</assumption>

<assumption name="Stable Treatment">
  <description>Treatment delivered consistently across units and time</description>
  <how_to_check>Implementation fidelity checks, standardized protocols, training</how_to_check>
  <if_violated>Document variation, test for heterogeneous effects, consider implementation design</if_violated>
</assumption>

<assumption name="No Attrition Bias">
  <description>Loss to follow-up is unrelated to treatment or would-be outcomes</description>
  <how_to_check>Track attrition rates by treatment arm, test for differential attrition</how_to_check>
  <if_violated>Use Lee bounds, inverse probability weighting, or report bounds on treatment effects</if_violated>
</assumption>

</assumptions>

<thinking_process>
When designing an RCT:
1. Articulate research question and theory of change
2. Identify outcomes and measurement strategy (primary vs. secondary)
3. Conduct power analysis for required sample size
4. Choose randomization level (individual vs. cluster) based on spillovers
5. Design ethical treatment assignment (phase-in, lottery, encouragement)
6. Prepare IRB protocol and obtain approval
7. Register trial and file pre-analysis plan
8. Implement with fidelity monitoring
9. Plan for compliance, attrition, and threats to validity
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def power_analysis_rct():
    # Calculate required sample size for RCT design
    # Based on Duflo et al. (2007) power calculation framework

    import numpy as np
    from scipy.stats import norm

    # Parameters
    alpha = 0.05  # Significance level
    power = 0.80  # Statistical power
    mde = 0.25  # Minimum detectable effect (SD units)
    p = 0.50  # Proportion assigned to treatment

    # Calculate critical values
    z_alpha = norm.ppf(1 - alpha/2)  # Two-tailed test
    z_power = norm.ppf(power)

    # Basic sample size
    n_base = ((z_alpha + z_power)**2) / (p * (1-p) * mde**2)

    # Adjust for clustering if applicable
    icc = 0.05  # Intra-cluster correlation
    cluster_size = 30  # Average cluster size
    design_effect = 1 + (cluster_size - 1) * icc
    n_clusters = n_base * design_effect / cluster_size

    # Adjust for attrition
    attrition_rate = 0.20
    n_final = n_base * design_effect / (1 - attrition_rate)

    print(f"POWER ANALYSIS FOR RCT")
    print(f"Parameters: α={alpha}, power={power}, MDE={mde} SD")
    print(f"\nBase sample size: {int(np.ceil(n_base))}")
    print(f"Design effect: {design_effect:.2f}")
    print(f"Clusters needed: {int(np.ceil(n_clusters))}")
    print(f"Final N (with attrition): {int(np.ceil(n_final))}")

    return int(np.ceil(n_final)),
```
</code_template>

</implementation_pattern>

<examples>

<example context="ethical_design" difficulty="intermediate">
<description>Design RCT when direct denial of treatment raises ethical concerns</description>
<code>
```python
@app.cell
def ethical_rct_design():
    # Use phase-in design when denying treatment is ethically problematic
    # All units eventually receive treatment, but timing is randomized

    import pandas as pd
    import numpy as np

    # Context: Limited program slots, everyone gets treatment eventually
    # Solution: Randomize TIMING rather than ACCESS

    n_units = 300
    n_cohorts = 3  # Roll out in 3 waves

    # Assign units to cohorts randomly
    cohorts = np.random.choice(range(n_cohorts), size=n_units)

    # Cohort 1: Immediate (Year 1)
    # Cohort 2: Delayed (Year 2)
    # Cohort 3: Delayed (Year 3)

    df = pd.DataFrame({
        'unit_id': range(n_units),
        'cohort': cohorts,
        'year_treated': cohorts + 1  # Everyone gets treatment
    })

    print("PHASE-IN / STEPPED WEDGE DESIGN")
    print("=" * 50)
    print(df.groupby('cohort').size())

    print("\nEthical advantages:")
    print("- No one permanently denied treatment")
    print("- Addresses capacity constraints")
    print("- Still enables causal inference")

    print("\nAnalysis approach:")
    print("- Compare early vs. late cohorts")
    print("- Use DID or event study framework")
    print("- Longer follow-up for early cohorts")

    return df,
```
</code>
<lesson>
When direct denial is unethical: (1) Phase-in/stepped wedge (randomize timing), (2) Encouragement design (randomize encouragement, not access), (3) Lottery (when slots limited), (4) Oversubscription (randomize among eligible). Never deny established entitlements.
</lesson>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Not conducting power analysis before starting</what>
  <consequence>Underpowered study wastes resources, fails to detect real effects, misleads policy</consequence>
  <prevention>Always run power calculations with realistic effect sizes and account for clustering/attrition</prevention>
</mistake>

<mistake severity="critical">
  <what>Starting data collection before IRB approval and registration</what>
  <consequence>Research misconduct, inability to publish, ethical violations</consequence>
  <prevention>IRB approval and trial registration are prerequisites, not afterthoughts</prevention>
</mistake>

<mistake severity="high">
  <what>Individual randomization when spillovers likely</what>
  <consequence>SUTVA violation, biased estimates, contaminated control group</consequence>
  <prevention>Use cluster randomization or buffer zones when spillovers expected</prevention>
</mistake>

<mistake severity="high">
  <what>Measuring outcomes before treatment fully delivered</what>
  <consequence>Premature measurement finds null effects when treatment hasn't had time to work</consequence>
  <prevention>Theory of change specifies timing - measure outcomes after sufficient exposure period</prevention>
</mistake>

<mistake severity="medium">
  <what>Not planning for non-compliance</what>
  <consequence>Surprised by low take-up, insufficient power for actual treatment received</consequence>
  <prevention>Pilot to estimate take-up, power for ITT given expected compliance, design encouragement</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<design_checklist>
Before launching RCT:
- [ ] Research question clearly specified
- [ ] Theory of change documented
- [ ] Power analysis conducted (accounts for clustering, attrition)
- [ ] Outcomes and measurement plan specified
- [ ] Randomization method chosen (individual vs. cluster)
- [ ] Ethical design confirmed (no unjustified denial)
- [ ] IRB protocol submitted and approved
- [ ] Trial registered (AEA RCT Registry or equivalent)
- [ ] Pre-analysis plan filed
- [ ] Implementation fidelity plan created
- [ ] Compliance monitoring plan ready
- [ ] Attrition tracking procedures established
</design_checklist>

<when_not_to_use_rct>
Avoid RCTs when:
- Randomization is unethical (denying life-saving treatment)
- Spillovers are unavoidable and large (market equilibrium effects)
- Sample size insufficient for adequate power
- Treatment is national-level policy (no counterfactual)
- Cost vastly exceeds value of information gained
- Results won't inform decisions (no policy window)
</when_not_to_use_rct>

</interpretation_guide>

<references>
<paper>Duflo, E., Glennerster, R., & Kremer, M. (2007). Using randomization in development economics research: A toolkit. Handbook of Development Economics, 4, 3895-3962.</paper>
<paper>Glennerster, R., & Takavarasha, K. (2013). Running Randomized Evaluations: A Practical Guide. Princeton University Press.</paper>
<paper>Christensen, G., & Miguel, E. (2018). Transparency, reproducibility, and the credibility of economics research. Journal of Economic Literature, 56(3), 920-980.</paper>
<paper>Button, K.S., et al. (2013). Power failure: why small sample size undermines the reliability of neuroscience. Nature Reviews Neuroscience, 14(5), 365-376.</paper>
<resource>J-PAL Research Resources: https://www.povertyactionlab.org/research-resources</resource>
</references>

</skill_content>
