---
name: rct-randomization
description: "Implement randomization methods for RCTs. Use when user mentions: random assignment, treatment allocation, stratification, blocking, permutation randomization, cluster randomization, randomization balance, misfit handling, re-randomization."
---

<skill_content>

<overview>
Randomization is the foundation of experimental causal inference. Proper implementation requires setting seeds once, documenting procedures, saving assignments immediately, and never re-running randomization to "improve" balance. Stratification improves precision when strata correlate with outcomes. Cluster randomization prevents spillovers but reduces power through design effects.

Randomization must be reproducible, documented, and executed exactly once per study.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Set Seed Once and Document</name>
  <description>Set random seed exactly ONCE at the beginning, document seed value, never reset seed within randomization code</description>
  <rationale>Multiple seed settings compromise randomness. Seed documentation enables replication and verification of randomization integrity</rationale>
  <consequence>Non-reproducible randomization, suspicion of manipulation, inability to verify implementation</consequence>
</requirement>

<requirement priority="critical">
  <name>Save Assignment Immediately, Never Re-Run</name>
  <description>Save randomization assignments to persistent storage immediately after generation, never re-run randomization</description>
  <rationale>Re-running randomization to "improve balance" invalidates inference and creates selection bias</rationale>
  <consequence>Invalid p-values, corrupted randomization, inability to claim true random assignment</consequence>
</requirement>

<requirement priority="critical">
  <name>Use Permutation (Not Simple) When Sample Size Known</name>
  <description>Use permutation randomization (shuffle fixed number of 1s and 0s) rather than independent Bernoulli draws when N is known</description>
  <rationale>Permutation ensures exact allocation ratios. Simple randomization creates sampling variation in treatment/control split</rationale>
  <consequence>Unbalanced groups, power loss, inability to explain allocation discrepancies</consequence>
</requirement>

<requirement priority="high">
  <name>Stratify on Strong Predictors When Available</name>
  <description>Use stratified randomization when baseline covariates strongly predict outcomes</description>
  <rationale>Stratification ensures balance on key variables, improves precision, reduces sampling variability (Bruhn & McKenzie 2009)</rationale>
  <consequence>Larger standard errors, power loss, imbalanced groups on important characteristics</consequence>
</requirement>

<requirement priority="high">
  <name>Account for Clustering in Randomization Level</name>
  <description>Randomize at cluster level when spillovers likely within clusters</description>
  <rationale>Individual randomization with spillovers violates SUTVA and biases estimates. Cluster randomization prevents contamination</rationale>
  <consequence>Biased treatment effect estimates from spillover contamination</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="No Selective Exclusion">
  <description>Sample for randomization represents full eligible population, no post-randomization exclusions</description>
  <how_to_check>Document exclusions before randomization, never drop units after seeing assignment</how_to_check>
  <if_violated>Selection bias, non-random sample, invalid causal inference</if_violated>
</assumption>

<assumption name="Implementation Fidelity">
  <description>Treatment assignment is actually implemented as randomized (no crossover without documentation)</description>
  <how_to_check>Monitor compliance, track any protocol deviations</how_to_check>
  <if_violated>Document and report deviations, analyze as encouragement design if substantial crossover</if_violated>
</assumption>

</assumptions>

<thinking_process>
When implementing randomization:
1. Define eligible sample BEFORE randomization
2. Choose randomization method (simple/permutation/stratified/cluster)
3. Set random seed ONCE, document seed value
4. Generate assignments (never re-run)
5. Save assignments to persistent storage immediately
6. Create backup of assignments
7. Check balance (but don't re-randomize if unbalanced)
8. Document any implementation deviations
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def randomize_trial():
    # Permutation randomization with stratification
    # CRITICAL: Set seed ONCE, save immediately, NEVER re-run

    import numpy as np
    import pandas as pd
    from datetime import datetime

    # Set seed ONCE at beginning (DOCUMENT THIS VALUE)
    RANDOM_SEED = 42
    np.random.seed(RANDOM_SEED)

    # Load eligible sample
    df = pd.read_csv("/mnt/data/eligible_units.csv")
    n = len(df)

    print(f"RANDOMIZATION PROTOCOL")
    print(f"Date: {datetime.now()}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Sample size: {n}")

    # Stratified permutation randomization
    treatment_prop = 0.5
    strata_var = 'baseline_risk'  # Strong outcome predictor

    df['treatment'] = 0

    for stratum in df[strata_var].unique():
        strata_mask = df[strata_var] == stratum
        n_strata = strata_mask.sum()
        n_treat = int(n_strata * treatment_prop)

        # Permutation within stratum
        assignments = np.concatenate([
            np.ones(n_treat, dtype=int),
            np.zeros(n_strata - n_treat, dtype=int)
        ])
        np.random.shuffle(assignments)

        df.loc[strata_mask, 'treatment'] = assignments

    # CRITICAL: Save immediately (NEVER re-run randomization)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"/mnt/data/randomization_assignments_{timestamp}.csv", index=False)

    # Create backup
    df.to_csv(f"/mnt/data/randomization_assignments_BACKUP.csv", index=False)

    print(f"\nAssignments saved to:")
    print(f"  /mnt/data/randomization_assignments_{timestamp}.csv")
    print(f"Treatment: {df['treatment'].sum()} ({df['treatment'].mean():.1%})")
    print(f"Control: {(~df['treatment'].astype(bool)).sum()} ({(~df['treatment'].astype(bool)).mean():.1%})")

    return df,
```
</code_template>

</implementation_pattern>

<examples>

<example context="cluster_randomization" difficulty="intermediate">
<description>Cluster randomization to prevent spillovers</description>
<code>
```python
@app.cell
def cluster_randomize(df):
    # Cluster randomization when spillovers likely within clusters
    # Reduces power due to design effect, but necessary for validity

    import numpy as np
    import pandas as pd

    # CRITICAL: Set seed once
    np.random.seed(123)

    # Identify clusters
    clusters = df['village_id'].unique()
    n_clusters = len(clusters)
    n_treat_clusters = int(n_clusters * 0.5)

    print(f"CLUSTER RANDOMIZATION")
    print(f"Total clusters: {n_clusters}")
    print(f"Treatment clusters: {n_treat_clusters}")

    # Permutation at cluster level
    cluster_assignments = np.concatenate([
        np.ones(n_treat_clusters, dtype=int),
        np.zeros(n_clusters - n_treat_clusters, dtype=int)
    ])
    np.random.shuffle(cluster_assignments)

    # Map cluster assignments to individuals
    cluster_map = dict(zip(clusters, cluster_assignments))
    df['treatment'] = df['village_id'].map(cluster_map)

    # Report
    print(f"\nIndividuals in treatment: {df['treatment'].sum()}")
    print(f"Individuals in control: {(~df['treatment'].astype(bool)).sum()}")

    # Calculate design effect
    avg_cluster_size = df.groupby('village_id').size().mean()
    icc = 0.05  # Assumed intra-cluster correlation
    design_effect = 1 + (avg_cluster_size - 1) * icc

    print(f"\nAverage cluster size: {avg_cluster_size:.1f}")
    print(f"Assumed ICC: {icc:.3f}")
    print(f"Design effect: {design_effect:.2f}")
    print(f"Effective sample size: {len(df)/design_effect:.0f}")

    return df,
```
</code>
<lesson>
Cluster randomization trades power for validity. Design effect = 1 + (m-1) × ICC where m is cluster size and ICC is intra-cluster correlation. Higher ICC or larger clusters → larger design effect → greater power loss. But necessary when spillovers would contaminate individual randomization.
</lesson>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Re-running randomization to get "better" balance</what>
  <consequence>Invalidates randomization inference, creates selection bias, corrupts p-values</consequence>
  <prevention>Run ONCE, save immediately, accept whatever balance you get. If deeply concerned about imbalance, use stratification or re-randomization with proper adjustment (difficult)</prevention>
</mistake>

<mistake severity="critical">
  <what>Setting random seed multiple times in randomization code</what>
  <consequence>Compromises randomness, makes sequence non-random, creates reproducibility issues</consequence>
  <prevention>Set seed ONCE at very beginning, never call np.random.seed() again in randomization code</prevention>
</mistake>

<mistake severity="high">
  <what>Using simple randomization when sample size is known</what>
  <consequence>Sampling variation creates unbalanced groups, power loss, difficult to explain discrepancies</consequence>
  <prevention>Use permutation randomization (shuffle fixed number of 1s and 0s) when N is known</prevention>
</mistake>

<mistake severity="high">
  <what>Not stratifying when strong predictors available</what>
  <consequence>Unnecessary power loss, imbalanced groups on important characteristics</consequence>
  <prevention>Stratify on 1-3 strong outcome predictors to improve precision</prevention>
</mistake>

<mistake severity="medium">
  <what>Not documenting randomization seed and procedure</what>
  <consequence>Non-reproducible, inability to verify implementation, suspicion of manipulation</consequence>
  <prevention>Document seed, date, time, code version, sample characteristics in protocol</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<balance_check_interpretation>
After randomization (but NOT as reason to re-randomize):
- Normalized diff |d| < 0.1: Excellent balance
- 0.1 ≤ |d| < 0.25: Acceptable balance
- |d| ≥ 0.25: Imbalanced on this variable (include as control, but don't re-randomize)
- Joint F-test p > 0.10: Overall balance adequate
- Joint F-test p < 0.05: Some imbalance (expected 5% of time by chance)

Never re-randomize based on balance. If you must, use proper re-randomization protocol with inference adjustment (complex).
</balance_check_interpretation>

<when_to_use_each_method>
- **Simple randomization**: Sequential enrollment, N unknown at randomization
- **Permutation**: N known, want exact allocation ratio
- **Stratified**: Strong baseline predictors available, want precision gains
- **Cluster**: Spillovers likely within clusters (social, geographic)
- **Re-randomization**: Advanced method requiring special inference (seek expert help)
</when_to_use_each_method>

</interpretation_guide>

<references>
<paper>Bruhn, M., & McKenzie, D. (2009). In pursuit of balance: Randomization in practice in development field experiments. American Economic Journal: Applied Economics, 1(4), 200-232.</paper>
<paper>Athey, S., & Imbens, G. W. (2017). The econometrics of randomized experiments. Handbook of Economic Field Experiments, 1, 73-140.</paper>
<paper>Duflo, E., Glennerster, R., & Kremer, M. (2007). Using randomization in development economics research. Handbook of Development Economics, 4, 3895-3962.</paper>
</references>

</skill_content>
