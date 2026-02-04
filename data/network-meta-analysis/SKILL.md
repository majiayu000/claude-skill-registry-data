---
name: network-meta-analysis
version: 1.0.0
description: Network meta-analysis for comparing multiple treatments
author: NeuroResearch Agent
license: MIT

triggers:
  - pattern: "network meta-analysis"
  - pattern: "NMA"
  - pattern: "compare.*treatments"
  - pattern: "multiple interventions"
  - pattern: "indirect comparison"
  - pattern: "mixed treatment comparison"

requires:
  - r-execute
  - filesystem

tools:
  - name: run_nma
    description: Run network meta-analysis
    script: scripts/nma.R
    
  - name: generate_network_plot
    description: Generate network geometry plot
    script: scripts/network_plot.R
    
  - name: generate_league_table
    description: Generate league table of all comparisons
    script: scripts/league_table.R
    
  - name: rank_treatments
    description: Calculate treatment rankings (SUCRA, P-scores)
    script: scripts/ranking.R
    
  - name: assess_consistency
    description: Assess local and global consistency
    script: scripts/consistency.R

schemas:
  nma_input:
    required:
      - study: string
      - treat1: string
      - treat2: string
    for_binary:
      - events1: integer
      - n1: integer
      - events2: integer
      - n2: integer
    for_continuous:
      - mean1: number
      - sd1: number
      - n1: integer
      - mean2: number
      - sd2: number
      - n2: integer
---

# Network Meta-Analysis Skill

## Overview

Network meta-analysis (NMA) extends traditional pairwise meta-analysis to compare multiple treatments simultaneously, even when some treatments have never been directly compared in head-to-head trials.

## When to Use

- Comparing 3+ treatment options
- Combining direct and indirect evidence
- Determining treatment rankings
- Creating treatment recommendations

## Key Concepts

### Network Geometry
- **Nodes**: Treatments being compared
- **Edges**: Direct comparisons from studies
- **Thickness**: Number of studies/participants

### Consistency
- **Direct evidence**: From head-to-head trials
- **Indirect evidence**: Derived through common comparators
- **Consistency assumption**: Direct ≈ Indirect

### Transitivity
For valid indirect comparisons, studies comparing A vs B must be similar to those comparing B vs C (effect modifiers must be balanced).

## R Code Templates

### Basic NMA Setup

```r
library(netmeta)
library(meta)

# Load pairwise data
# Format: study, treat1, treat2, TE, seTE (or raw data)
data <- read.csv("{{INPUT}}")

# For binary outcomes - calculate OR
data$TE <- log((data$events1 / (data$n1 - data$events1)) / 
               (data$events2 / (data$n2 - data$events2)))
data$seTE <- sqrt(1/data$events1 + 1/(data$n1-data$events1) + 
                   1/data$events2 + 1/(data$n2-data$events2))

# Run NMA
nma <- netmeta(
  TE = TE,
  seTE = seTE,
  treat1 = treat1,
  treat2 = treat2,
  studlab = study,
  data = data,
  sm = "OR",
  reference.group = "{{REFERENCE}}",
  random = TRUE,
  details.chkmultiarm = TRUE
)

summary(nma)
```

### Network Plot

```r
# Network geometry
png("{{OUTPUT}}/network_plot.png", width = 800, height = 800, res = 150)
netgraph(nma,
         plastic = TRUE,
         thickness = "number.of.studies",
         number.of.studies = TRUE,
         points = TRUE,
         cex.points = 3,
         col = "blue",
         multiarm = TRUE)
dev.off()

# Alternative with ggplot
library(ggplot2)
library(ggraph)

# Create edge list
edges <- data.frame(
  from = data$treat1,
  to = data$treat2,
  weight = 1
) %>%
  group_by(from, to) %>%
  summarise(n = n(), .groups = 'drop')

# Network visualization
graph <- igraph::graph_from_data_frame(edges)
ggraph(graph, layout = 'stress') +
  geom_edge_link(aes(width = n), alpha = 0.5) +
  geom_node_point(size = 8, color = 'steelblue') +
  geom_node_text(aes(label = name), repel = TRUE) +
  theme_void() +
  labs(title = "Network of Treatment Comparisons")

ggsave("{{OUTPUT}}/network_ggplot.png", width = 10, height = 8)
```

### Forest Plot vs Reference

```r
# Forest plot comparing all treatments to reference
png("{{OUTPUT}}/forest_nma.png", width = 1000, height = 800, res = 150)
forest(nma, 
       reference.group = "{{REFERENCE}}",
       sortvar = -TE,
       smlab = "Odds Ratio vs {{REFERENCE}}",
       drop.reference.group = TRUE)
dev.off()
```

### League Table

```r
# Generate league table
league <- netleague(nma, 
                    digits = 2,
                    bracket = "(",
                    separator = " to ")

# Upper triangle: random effects estimates
# Lower triangle: direct evidence only

# Save as CSV
league_df <- as.data.frame(league$random)
write.csv(league_df, "{{OUTPUT}}/league_table.csv")

# Pretty print
print(league, digits = 2)
```

### Treatment Rankings

```r
# Calculate rankings
rank <- netrank(nma, small.values = "{{DIRECTION}}")  # "good" or "bad"

# SUCRA/P-scores
print(rank)

# Rankogram
png("{{OUTPUT}}/rankogram.png", width = 1000, height = 600, res = 150)
plot(rank, cumulative = FALSE)
dev.off()

# Cumulative ranking
png("{{OUTPUT}}/sucra_plot.png", width = 1000, height = 600, res = 150)
plot(rank, cumulative = TRUE)
dev.off()

# P-scores (frequentist analog of SUCRA)
cat("\nP-scores (probability of being best):\n")
print(sort(rank$Pscore, decreasing = TRUE))
```

### Consistency Assessment

```r
# Check network connectivity
netconnection(data$treat1, data$treat2)

# Global inconsistency (design-by-treatment interaction)
decomp <- decomp.design(nma)
print(decomp)

# Q statistics
cat("\nInconsistency Q-statistic:\n")
cat(sprintf("Q = %.2f, df = %d, p = %.4f\n", 
            decomp$Q.inc.random, decomp$df.Q.inc, decomp$pval.Q.inc))

# Local inconsistency (node-splitting)
split <- netsplit(nma)

png("{{OUTPUT}}/nodesplit.png", width = 1200, height = 800, res = 150)
forest(split, show = "all")
dev.off()

# Summary
cat("\nNode-splitting results:\n")
print(split)
```

### Comparison-Adjusted Funnel Plot

```r
# Publication bias assessment
png("{{OUTPUT}}/funnel_nma.png", width = 800, height = 600, res = 150)
funnel(nma, 
       order = netrank(nma)$ranking,
       pch = data$treat1)
dev.off()
```

### Heat Plot

```r
# Contribution matrix visualization
library(NMAoutlier)  # or custom implementation

# Shows which studies contribute to each comparison
png("{{OUTPUT}}/heatplot.png", width = 1000, height = 800, res = 150)
netheat(nma, random = TRUE)
dev.off()
```

## Data Preparation

### From Arm-Level Data

```r
# Convert arm-level to contrast-level
library(netmeta)

# Arm-level format
arm_data <- data.frame(
  study = c("A", "A", "A", "B", "B"),
  treatment = c("Drug1", "Drug2", "Placebo", "Drug1", "Drug3"),
  events = c(10, 15, 20, 8, 5),
  n = c(50, 50, 50, 40, 40)
)

# Convert to pairwise
pw <- pairwise(
  treat = treatment,
  event = events,
  n = n,
  studlab = study,
  data = arm_data,
  sm = "OR"
)
```

### Handling Multi-Arm Studies

```r
# Multi-arm studies require correlation adjustment
# netmeta handles this automatically if studlab properly identifies studies

# For gemtc (Bayesian NMA), use arm-level data directly
library(gemtc)

network <- mtc.network(
  data.ab = arm_data  # arm-based data
)

model <- mtc.model(network, 
                   likelihood = "binom", 
                   link = "logit")

results <- mtc.run(model, n.adapt = 5000, n.iter = 20000)
```

## Interpretation Guidelines

### Effect Estimates
- League table shows all pairwise comparisons
- Row treatment vs column treatment
- Values < 1 favor row treatment (for OR/RR)

### Rankings
- SUCRA/P-score: Probability of being among the best
- 100% = always best, 0% = always worst
- Consider uncertainty in rankings

### Consistency
- If p < 0.05 for inconsistency tests, interpret with caution
- May indicate effect modification or bias
- Consider splitting network or investigating sources

## Common Issues

### Disconnected Network
- Some treatments not connected to others
- Cannot make all comparisons
- May need to exclude some treatments

### Sparse Network
- Few studies per comparison
- Wide confidence intervals
- Rankings unreliable

### Inconsistency
- Direct ≠ indirect estimates
- Investigate effect modifiers
- Consider separate analyses

## GRADE for NMA

Rate confidence for each comparison:
1. Within-study bias (RoB of contributing studies)
2. Publication bias (comparison-adjusted funnel)
3. Indirectness (transitivity violations)
4. Imprecision (CI width, ranking uncertainty)
5. Heterogeneity (I² for direct comparisons)
6. Incoherence (inconsistency tests)

Use CINeMA tool for systematic assessment.
