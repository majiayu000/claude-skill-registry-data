---
name: nma-methodology
description: Deep methodology knowledge for network meta-analysis including transitivity, consistency assessment, treatment rankings, and model selection. Use when conducting or reviewing NMA.
---

# Network Meta-Analysis Methodology

Comprehensive methodological guidance for conducting rigorous network meta-analysis following NICE DSU and PRISMA-NMA guidelines.

## When to Use This Skill

- Planning a network meta-analysis
- Assessing transitivity and consistency
- Interpreting treatment rankings
- Choosing between frequentist and Bayesian NMA
- Designing NMA sensitivity analyses
- Reviewing NMA code or results

## Fundamental Assumptions

### 1. Transitivity Assumption

**Definition**: If we can estimate A vs B directly and B vs C directly, we can estimate A vs C indirectly, provided the studies are sufficiently similar.

**Requirements**:
- Studies comparing different treatments should be similar enough to have been included in the same RCT
- Effect modifiers should be balanced across comparisons
- No important differences in study-level characteristics

**Assessment**:
```
For each comparison in network, check:
├── Population similarity
│   - Age, sex, disease severity
│   - Biomarker status, prior treatments
├── Outcome definitions
│   - Same definition of response/event
│   - Same time point of assessment
├── Treatment definitions
│   - Dose, duration, route
│   - Concomitant medications
└── Study design
    - Randomization, blinding
    - Follow-up duration
```

**Presenting Transitivity Assessment**:
- Create table of study characteristics by comparison
- Highlight any systematic differences
- Use forest plots stratified by comparison

### 2. Consistency Assumption

**Definition**: Direct and indirect evidence for the same comparison should agree (within random variability).

**Relation to Transitivity**:
- Transitivity is untestable (conceptual)
- Consistency is testable (statistical)
- Consistency violations suggest transitivity violations

## Consistency Assessment

### Global Consistency Tests

#### Design-by-Treatment Interaction
```r
# netmeta
decomp.design(nma_result)
# Tests overall consistency across network
# Q statistic partitioned into within-design and between-design
```

#### Q Statistic Decomposition
- Q_total = Q_heterogeneity + Q_inconsistency
- Test Q_inconsistency against chi-square distribution

### Local Consistency: Node-Splitting

```r
# netmeta
netsplit(nma_result)

# gemtc
nodesplit_model <- mtc.nodesplit(network)
```

**Interpretation**:
| Direct vs Indirect | Conclusion |
|-------------------|------------|
| Similar (p > 0.05) | No evidence of inconsistency |
| Different (p < 0.05) | Possible inconsistency - investigate |

**Caution**: Multiple testing - expect some false positives.

### Net Heat Plot
```r
netheat(nma_result)
# Visual display of inconsistency
# Red: high inconsistency contribution
# Blue: low inconsistency
```

### What to Do with Inconsistency

1. **Check data** - errors in data entry
2. **Investigate sources** - which comparisons differ
3. **Explore heterogeneity** - meta-regression on potential modifiers
4. **Consider splitting network** - if clinical rationale exists
5. **Report transparently** - don't hide inconsistency
6. **Use inconsistency model** - as sensitivity analysis

## Treatment Rankings

### Frequentist (netmeta)

#### P-scores
```r
netrank(nma_result, small.values = "bad")
# P-score: probability of being better than average treatment
# Ranges 0-1
# NOT probability of being best
```

### Bayesian (gemtc)

#### SUCRA (Surface Under Cumulative Ranking Curve)
```r
sucra(mtc_result)
# Similar interpretation to P-score
# Based on cumulative ranking probabilities
```

#### Probability of Being Best
```r
rank.probability(mtc_result)
# Full ranking probability matrix
# Prob_best = P(rank = 1)
```

### Interpretation Cautions

**Critical**: Rankings are uncertain - always present with uncertainty measures.

```
Problems with rankings:
├── Small differences → different rankings
├── Wide credible intervals often ignored
├── Multiple treatments may be effectively tied
├── Rankings don't consider clinical relevance
└── "Best" might have limited evidence
```

**Best Practice**:
- Report ranking probabilities, not just point ranks
- Show cumulative ranking plots
- Consider clustering treatments by effect
- Discuss clinical significance alongside statistical

## Model Selection

### Fixed vs Random Effects

| Factor | Fixed-Effect | Random-Effects |
|--------|-------------|----------------|
| Studies similar | ✓ | ✓ |
| Studies different | ✗ | ✓ |
| Few studies per comparison | Consider | Default |
| Inference goal | Included studies | Broader population |

### Bayesian Prior Selection

#### Treatment Effects
```r
prior_trt = prior_normal(0, sd)
# sd should be large enough to be weakly informative
# Consider scale of effect measure (log OR ~2-3 is large)
```

#### Heterogeneity (τ)
```r
prior_het = prior_half_normal(scale)
# Scale depends on expected heterogeneity
# Turner et al. informative priors available
```

### Model Comparison

#### DIC (Deviance Information Criterion)
```r
# Lower is better
# Difference of ~3-5 is meaningful
dic(model1)
dic(model2)
```

#### Residual Deviance
- Compare to number of data points
- Should be close if model fits well

## Network Geometry

### Key Considerations

```
Network Structure Assessment:
├── Connectivity
│   - All treatments connected (directly or indirectly)?
│   - Star network? (single common comparator)
│   - Well-connected?
├── Evidence Distribution
│   - Some comparisons well-informed, others sparse?
│   - Imbalanced networks problematic
├── Multi-arm Trials
│   - Must account for correlations
│   - Contribution to network
└── Placebo/Active Control
    - Consider clinical relevance of network anchor
```

### Contribution Matrix
```r
# netmeta
netcontrib(nma_result)
# Shows % contribution of each direct comparison to each estimate
```

### Network Graph
```r
netgraph(nma_result,
         plastic = FALSE,
         thickness = "number.of.studies",
         multiarm = TRUE,
         points = TRUE)
```

## Reporting Checklist (PRISMA-NMA)

### Methods
- [ ] Network geometry description
- [ ] Transitivity assessment approach
- [ ] Effect measure and rationale
- [ ] Model choice (fixed/random, frequentist/Bayesian)
- [ ] Prior specifications (if Bayesian)
- [ ] Consistency assessment methods
- [ ] Ranking methods and interpretation
- [ ] Sensitivity analyses planned

### Results
- [ ] Network diagram
- [ ] Study characteristics table by comparison
- [ ] Pairwise MA results (for direct evidence)
- [ ] NMA results for all comparisons
- [ ] League table
- [ ] Consistency assessment results
- [ ] Treatment rankings with uncertainty
- [ ] Sensitivity analysis results

## Common Pitfalls

### 1. Ignoring Transitivity
- Must assess before running NMA
- Not just a formality - fundamental requirement

### 2. Over-interpreting Rankings
- "Treatment A ranked #1" without uncertainty
- Small differences may give different rankings
- Clinical relevance matters more than rank

### 3. Selective Consistency Reporting
- Report all node-split results
- Don't dismiss inconsistency findings

### 4. Multi-arm Trial Handling
- Must account for correlations
- Software handles this, but check it's done correctly

### 5. Sparse Networks
- Very uncertain indirect comparisons
- Consider if NMA is appropriate

## Quick Reference Code

### Frequentist (netmeta)
```r
library(netmeta)

# Fit NMA
nma <- netmeta(TE, seTE, treat1, treat2, studlab,
               data = pairwise_data,
               sm = "OR",
               reference.group = "Placebo",
               random = TRUE)

# Network graph
netgraph(nma, plastic = FALSE, multiarm = TRUE)

# Forest vs reference
forest(nma, reference.group = "Placebo")

# League table
netleague(nma)

# Consistency
netsplit(nma)
netheat(nma)

# Rankings
netrank(nma, small.values = "bad")
```

### Bayesian (gemtc)
```r
library(gemtc)
library(rjags)

# Create network
network <- mtc.network(data.ab = arm_data)

# Fit model
model <- mtc.model(network,
                   likelihood = "binom",
                   link = "logit",
                   linearModel = "random")
result <- mtc.run(model, n.adapt = 5000, n.iter = 50000)

# Check convergence
gelman.diag(result)

# Summary
summary(result)

# Rankings
rank.probability(result)
sucra(result)

# Node-splitting
nodesplit <- mtc.nodesplit(network)
ns_result <- mtc.run(nodesplit)
summary(ns_result)
```

## Resources

- NICE DSU TSD 2: https://www.sheffield.ac.uk/nice-dsu/tsds
- PRISMA-NMA: Hutton et al. 2015
- Dias et al. (2018): Network Meta-Analysis for Decision Making
- Salanti (2012): Ann Intern Med - Intro to NMA
