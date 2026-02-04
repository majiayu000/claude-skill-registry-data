---
name: tsa-integration
version: 1.0.0
description: Trial Sequential Analysis for meta-analyses with information size calculations
author: NeuroResearch Agent
license: MIT

triggers:
  - pattern: "trial sequential analysis"
  - pattern: "TSA"
  - pattern: "information size"
  - pattern: "required information size"
  - pattern: "cumulative z-score"
  - pattern: "monitoring boundaries"
  - pattern: "futility"
  - pattern: "O'Brien-Fleming"

requires:
  - r-execute
  - filesystem
  - tsa-mcp  # Optional: MCP server for TSA software

tools:
  - name: calculate_ris
    description: Calculate Required Information Size
    
  - name: generate_tsa_plot
    description: Generate TSA plot with boundaries
    
  - name: prepare_tsa_input
    description: Prepare data for TSA software
    
  - name: interpret_tsa
    description: Interpret TSA results
---

# Trial Sequential Analysis Skill

## Overview

Trial Sequential Analysis (TSA) applies sequential monitoring boundaries to cumulative meta-analysis to control for random errors due to repeated analyses. It helps determine if the current evidence is conclusive or if more trials are needed.

## When to Use

- Evaluating if meta-analysis has sufficient statistical power
- Determining if positive/negative results are conclusive
- Planning future trials based on current evidence
- Updating living systematic reviews

## Key Concepts

### Required Information Size (RIS)
The total sample size needed to reliably detect or refute the intervention effect:
- Type I error (α): Usually 5%
- Type II error (β): Usually 10-20% (power 80-90%)
- Anticipated effect: From pilot studies or clinical relevance
- Variance: Heterogeneity-adjusted

### Monitoring Boundaries
- **Conventional boundary**: α = 0.05 (Z = 1.96)
- **TSA boundary**: Adjusted for sequential looks (stricter)
- **Futility boundary**: When harm or no effect is likely

### Boundary Types
- **O'Brien-Fleming (α-spending)**: Conservative early, relaxed late
- **Lan-DeMets**: Flexible timing
- **Haybittle-Peto**: Very conservative early stopping

## R Implementation

### Basic TSA in R

While the official TSA software is Java-based, R can perform equivalent analyses:

```r
library(meta)
library(metafor)

# Cumulative meta-analysis
data <- read.csv("{{INPUT}}")
data <- data[order(data$year), ]  # Sort by year

# Run cumulative meta-analysis
if ("events_int" %in% names(data)) {
  ma <- metabin(event.e = events_int, n.e = n_int,
                event.c = events_ctrl, n.c = n_ctrl,
                studlab = study, data = data, 
                sm = "{{MEASURE}}", random = TRUE)
} else {
  ma <- metacont(n.e = n_int, mean.e = mean_int, sd.e = sd_int,
                 n.c = n_ctrl, mean.c = mean_ctrl, sd.c = sd_ctrl,
                 studlab = study, data = data,
                 sm = "MD", random = TRUE)
}

cum <- metacum(ma, sortvar = data$year)
```

### Required Information Size Calculation

```r
# For binary outcomes
calculate_ris_binary <- function(
  p_control,        # Control event rate
  rrr,              # Relative risk reduction
  alpha = 0.05,
  beta = 0.20,      # Power = 1 - beta
  two_sided = TRUE,
  heterogeneity = 0 # Diversity (D²)
) {
  p_intervention <- p_control * (1 - rrr)
  
  # Sample size for single trial
  za <- qnorm(1 - alpha / ifelse(two_sided, 2, 1))
  zb <- qnorm(1 - beta)
  
  # Per-group sample size (Friedman formula for RR)
  n_per_group <- ((za + zb)^2 * (p_control * (1 - p_control) + 
                                  p_intervention * (1 - p_intervention))) /
                  (p_control - p_intervention)^2
  
  # Adjust for heterogeneity
  ris <- 2 * n_per_group * (1 / (1 - heterogeneity))
  
  return(ceiling(ris))
}

# For continuous outcomes
calculate_ris_continuous <- function(
  effect_size,      # Expected mean difference
  sd_pooled,        # Pooled standard deviation
  alpha = 0.05,
  beta = 0.20,
  two_sided = TRUE,
  heterogeneity = 0
) {
  za <- qnorm(1 - alpha / ifelse(two_sided, 2, 1))
  zb <- qnorm(1 - beta)
  
  n_per_group <- 2 * ((za + zb)^2 * sd_pooled^2) / effect_size^2
  
  ris <- 2 * n_per_group * (1 / (1 - heterogeneity))
  
  return(ceiling(ris))
}

# Example
ris <- calculate_ris_binary(
  p_control = 0.20,
  rrr = 0.25,
  alpha = 0.05,
  beta = 0.10,
  heterogeneity = ma$I2
)

cat(sprintf("Required Information Size: %d participants\n", ris))
cat(sprintf("Current sample size: %d\n", sum(data$n_int) + sum(data$n_ctrl)))
cat(sprintf("Information fraction: %.1f%%\n", 
            100 * (sum(data$n_int) + sum(data$n_ctrl)) / ris))
```

### O'Brien-Fleming Boundaries

```r
# Calculate spending function boundaries
obf_boundary <- function(information_fraction, alpha = 0.05, two_sided = TRUE) {
  # O'Brien-Fleming alpha-spending function
  if (two_sided) {
    a <- 2 * (1 - pnorm(qnorm(1 - alpha/2) / sqrt(information_fraction)))
    z <- qnorm(1 - a/2)
  } else {
    a <- 1 - pnorm(qnorm(1 - alpha) / sqrt(information_fraction))
    z <- qnorm(1 - a)
  }
  return(z)
}

# Calculate boundaries at each analysis
calculate_tsa_boundaries <- function(cum_n, ris, alpha = 0.05) {
  if_fractions <- cum_n / ris
  boundaries <- sapply(if_fractions, obf_boundary, alpha = alpha)
  return(data.frame(
    n = cum_n,
    if_fraction = if_fractions,
    z_boundary = boundaries
  ))
}
```

### TSA Plot Generation

```r
generate_tsa_plot <- function(cum_ma, ris, alpha = 0.05, beta = 0.20) {
  # Extract cumulative results
  cum_data <- data.frame(
    study = cum_ma$studlab,
    n = cumsum(cum_ma$n.e + cum_ma$n.c),
    z = cum_ma$TE.random / cum_ma$seTE.random,
    te = cum_ma$TE.random,
    lower = cum_ma$lower.random,
    upper = cum_ma$upper.random
  )
  
  # Calculate boundaries
  boundaries <- calculate_tsa_boundaries(cum_data$n, ris, alpha)
  
  # Plot
  library(ggplot2)
  
  # Information fraction on x-axis
  cum_data$if_frac <- cum_data$n / ris * 100
  boundaries$if_frac <- boundaries$n / ris * 100
  
  # Extend boundaries to 100%
  max_if <- max(100, max(cum_data$if_frac) + 10)
  extra_points <- seq(max(boundaries$if_frac) + 5, max_if, by = 5)
  extra_boundaries <- sapply(extra_points / 100, obf_boundary, alpha = alpha)
  
  boundaries <- rbind(boundaries,
                      data.frame(n = extra_points * ris / 100,
                                 if_fraction = extra_points / 100,
                                 z_boundary = extra_boundaries,
                                 if_frac = extra_points))
  
  p <- ggplot() +
    # Monitoring boundaries
    geom_line(data = boundaries, 
              aes(x = if_frac, y = z_boundary),
              color = "red", linewidth = 1) +
    geom_line(data = boundaries,
              aes(x = if_frac, y = -z_boundary),
              color = "red", linewidth = 1) +
    
    # Conventional boundaries
    geom_hline(yintercept = c(-1.96, 1.96), 
               linetype = "dashed", color = "gray50") +
    
    # Futility boundaries (inner)
    geom_line(data = boundaries,
              aes(x = if_frac, y = z_boundary * 0.5),
              color = "blue", linetype = "dashed") +
    geom_line(data = boundaries,
              aes(x = if_frac, y = -z_boundary * 0.5),
              color = "blue", linetype = "dashed") +
    
    # Z-curve
    geom_line(data = cum_data, 
              aes(x = if_frac, y = z),
              color = "black", linewidth = 1.2) +
    geom_point(data = cum_data,
               aes(x = if_frac, y = z),
               size = 3, color = "black") +
    
    # RIS line
    geom_vline(xintercept = 100, linetype = "solid", color = "darkgreen") +
    
    # Labels
    labs(x = "Information Fraction (%)",
         y = "Cumulative Z-score",
         title = "Trial Sequential Analysis",
         subtitle = sprintf("RIS = %d | Current = %d (%.1f%%)", 
                            ris, max(cum_data$n), max(cum_data$if_frac))) +
    
    # Annotations
    annotate("text", x = 105, y = 0, label = "RIS", 
             color = "darkgreen", angle = 90, vjust = -0.5) +
    annotate("text", x = max_if - 5, y = 2.5, label = "Benefit", color = "red") +
    annotate("text", x = max_if - 5, y = -2.5, label = "Harm", color = "red") +
    annotate("text", x = max_if - 5, y = 0, label = "Futility", color = "blue") +
    
    theme_minimal() +
    theme(legend.position = "none") +
    scale_y_continuous(limits = c(-4, 4))
  
  return(p)
}

# Generate and save
p <- generate_tsa_plot(cum, ris)
ggsave("{{OUTPUT}}/tsa_plot.png", p, width = 12, height = 8, dpi = 300)
```

## Preparing Data for TSA Software

The official TSA software (Java) requires specific input format:

```r
prepare_tsa_input <- function(data, outcome = "{{OUTCOME}}") {
  # For binary outcomes
  if ("events_int" %in% names(data)) {
    tsa_data <- data.frame(
      Study = data$study,
      Year = data$year,
      Ei = data$events_int,      # Events intervention
      Ni = data$n_int,           # Total intervention
      Ec = data$events_ctrl,     # Events control
      Nc = data$n_ctrl           # Total control
    )
  } else {
    # For continuous outcomes
    tsa_data <- data.frame(
      Study = data$study,
      Year = data$year,
      Ni = data$n_int,
      Mi = data$mean_int,
      SDi = data$sd_int,
      Nc = data$n_ctrl,
      Mc = data$mean_ctrl,
      SDc = data$sd_ctrl
    )
  }
  
  # Sort by year
  tsa_data <- tsa_data[order(tsa_data$Year), ]
  
  # Write for TSA software
  write.csv(tsa_data, sprintf("{{OUTPUT}}/tsa_input_%s.csv", outcome), 
            row.names = FALSE)
  
  cat("TSA input file created. Use in TSA software with:\n")
  cat("1. Open TSA software\n")
  cat("2. File > Import > CSV\n")
  cat("3. Select outcome type (binary/continuous)\n")
  cat("4. Set alpha, beta, and anticipated effect\n")
  cat("5. Run analysis\n")
  
  return(tsa_data)
}
```

## Interpretation Guidelines

### Crosses Benefit Boundary
- Strong evidence of benefit
- Unlikely to change with more trials
- Consider stopping accrual

### Crosses Harm Boundary
- Strong evidence of harm
- Intervention may be harmful
- Ethically consider stopping

### Within Boundaries, < RIS
- Insufficient evidence
- More trials needed
- Effect size uncertain

### Within Boundaries, > RIS
- No significant effect detected
- Adequate power achieved
- May conclude no difference

### Crosses Futility Boundary
- Unlikely to ever show benefit
- Consider stopping futile trials
- But doesn't prove harm

## Example Workflow

```r
# 1. Load data
data <- read.csv("extractions/pooled_data.csv")
data <- data[order(data$year), ]

# 2. Run cumulative meta-analysis
ma <- metabin(events_int, n_int, events_ctrl, n_ctrl,
              studlab = study, data = data, sm = "OR", random = TRUE)
cum <- metacum(ma, sortvar = data$year)

# 3. Calculate RIS
ris <- calculate_ris_binary(
  p_control = sum(data$events_ctrl) / sum(data$n_ctrl),
  rrr = 0.20,  # Anticipated 20% relative risk reduction
  alpha = 0.05,
  beta = 0.10,  # 90% power
  heterogeneity = ma$I2
)

# 4. Generate TSA plot
p <- generate_tsa_plot(cum, ris)
ggsave("figures/tsa_mortality.png", p, width = 12, height = 8, dpi = 300)

# 5. Interpret
current_n <- sum(data$n_int) + sum(data$n_ctrl)
if_fraction <- current_n / ris

cat(sprintf("\n=== TSA Summary ===\n"))
cat(sprintf("Required Information Size: %d\n", ris))
cat(sprintf("Current sample size: %d\n", current_n))
cat(sprintf("Information fraction: %.1f%%\n", if_fraction * 100))

current_z <- cum$TE.random[length(cum$TE.random)] / 
             cum$seTE.random[length(cum$seTE.random)]
tsa_boundary <- obf_boundary(if_fraction)

cat(sprintf("Current Z-score: %.2f\n", current_z))
cat(sprintf("TSA boundary: %.2f\n", tsa_boundary))

if (abs(current_z) > tsa_boundary) {
  cat("CONCLUSION: Evidence is conclusive\n")
} else if (if_fraction >= 1) {
  cat("CONCLUSION: RIS reached, effect not significant\n")
} else {
  cat("CONCLUSION: More evidence needed\n")
}
```

## Advanced: RTSA Package

```r
# If available, use RTSA package
# install.packages("RTSA")
library(RTSA)

# Run TSA
tsa_result <- rtsa(
  type = "binary",
  data = data,
  alpha = 0.05,
  beta = 0.10,
  RRR = 0.20,  # Relative risk reduction
  boundary = "OBF"  # O'Brien-Fleming
)

# Plot
plot(tsa_result)
summary(tsa_result)
```
