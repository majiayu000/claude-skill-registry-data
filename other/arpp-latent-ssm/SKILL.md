---
name: arpp-latent-ssm---autoregressive-point-process-to-
description: Skill for AI agent capabilities
---

# arpp-latent-ssm - Autoregressive Point Process to Latent SSM

## Description

Convert Autoregressive Point Process Generalized Linear Models (PPGLM) to Latent State-Space Models (SSM) using moment-closure approach. This skill provides a mathematical framework for modeling spike train data by bridging two popular model classes in computational neuroscience.

**Source:** arXiv:1801.00475v2 (Neural Computation)
**Utility:** 0.93

## Activation Keywords

- autoregressive point process
- PPGLM to SSM
- latent state-space model
- moment closure
- spike train modeling
- neural dynamics inference
- point process GLM

## Core Concepts

### 1. Model Classes Connection

| Model | Description |
|-------|-------------|
| PPGLM | Autoregressive Point Process Generalized Linear Model |
| SSM | Latent State-Space Model with point-process observations |

### 2. Mathematical Framework

```
PPGLM → Auxiliary History Process → Infinite-dim Dynamical System → Basis Projection → SSM (via moment closure)
```

### 3. Key Innovations

- **Auxiliary History Process**: Represent history-dependent PPGLM as latent variable
- **Basis Function Projection**: Reduce infinite dimensions to finite SSM
- **Moment Closure**: Close the moment equations to tractable form

## Step-by-Step Instructions

### 1. Data Preparation

```python
import numpy as np

# Spike train data: binary spike counts per time bin
spike_train = np.array([...])  # shape: (n_trials, n_time_bins)
```

### 2. Define PPGLM Model

```python
from sklearn.linear_model import PoissonRegressor

# Autoregressive features: spike history
def create_history_features(spikes, order=10):
    features = []
    for t in range(order, len(spikes)):
        history = spikes[t-order:t].flatten()
        features.append(history)
    return np.array(features)
```

### 3. Basis Function Projection

```python
# Choose basis functions for dimension reduction
n_basis = 5  # number of basis functions
basis = np.random.randn(n_basis, order)  # example: random projection

# Project history to latent state
def project_to_latent(history_features, basis):
    latent_state = history_features @ basis.T
    return latent_state
```

### 4. Moment Closure Approximation

```python
# First-order moment closure: ignore higher-order correlations
def moment_closure_ssm(latent_state, spikes):
    # State transition: simple dynamics
    A = np.eye(n_basis) * 0.9  # decay
    
    # Observation model: Poisson likelihood
    # log λ = C * latent_state + d
    
    return A, latent_state
```

### 5. Fit SSM Model

```python
# Use variational inference or EM algorithm
def fit_ssm(latent_state, spikes):
    # Kalman filter for state estimation
    # EM for parameter learning
    pass  # implementation depends on library
```

## Tools Used

- `numpy` - Array operations for spike train data
- `scipy` - Basis function projection and optimization
- `exec` - Run Python scripts for model fitting
- `read` - Load spike train data from files

## Example Use Cases

### 1. Phasic Bursting Neuron Model

```python
# Model burst dynamics in neural recordings
burst_spikes = load_spike_data('burst_neuron.csv')
latent_state = fit_arpp_ssm(burst_spikes)
```

### 2. Neural Dynamics Inference

```python
# Infer hidden states from observed spikes
hidden_dynamics = infer_latent_dynamics(spike_train)
```

### 3. Compare PPGLM vs SSM

```python
# Compare prediction accuracy
ppglm_score = evaluate_ppglm(spikes)
ssm_score = evaluate_ssm(spikes)
print(f"PPGLM: {ppglm_score}, SSM: {ssm_score}")
```

## Instructions for Agents
Follow these steps when applying this skill:

### Step 1: Data Preparation

## Examples

### Example 1: Basic Application

**User:** I need to apply arpp-latent-ssm - Autoregressive Point Process to Latent SSM to my analysis.

**Agent:** I'll help you apply arpp-latent-ssm. First, let me understand your specific use case...

**Context:** Apply the methodology

### Example 2: Advanced Scenario

**User:** Complex analysis scenario

**Agent:** Based on the methodology, I'll guide you through the advanced application...

### Example 2: Advanced Application

**User:** What are the key considerations for arpp-latent-ssm?

**Agent:** Let me search for the latest research and best practices...

## Related Skills

- `jedi-neural-dynamics-inference` - Joint Embedded Dynamics Inference
- `neural-code-dynamics-analysis` - Neural Code Dynamics
- `kuramoto-brain-network` - Kuramoto Model for Brain Networks

## References

- Rule, M., et al. (2018). "Autoregressive Point-Processes as Latent State-Space Models" Neural Computation
- DOI: 10.1162/neco_a_01121

---

**Created:** 2026-03-29 04:10
**Author:** Aerial (from arXiv:1801.00475v2)