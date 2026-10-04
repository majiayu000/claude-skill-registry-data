---
name: rl-qec-control
description: >
  Reinforcement Learning for Quantum Error Correction control methodology. 
  Based on Google Quantum AI's Willow processor framework (arXiv:2511.08493).
  Use when: (1) designing RL-based calibration for quantum systems, 
  (2) implementing continuous error correction without halting computation,
  (3) repurposing QEC syndrome measurements as RL learning signals,
  (4) stabilizing quantum operations against environmental drift,
  (5) optimizing surface code or color code performance.
  Keywords: quantum error correction, RL calibration, QEC, surface code, 
  color code, Willow processor, syndrome decoding, environmental drift.
---

# RL-QEC Control: Reinforcement Learning for Quantum Error Correction

Based on Google Quantum AI & DeepMind paper: "Reinforcement learning control of quantum error correction" (arXiv:2511.08493, 2026).

## Core Methodology

### Problem
Quantum computers are analog machines susceptible to environmental drift. Traditional recalibration requires halting computation — unsustainable for long-running algorithms.

### Solution
Unify calibration with computation: repurpose QEC error detection events as a learning signal for an RL agent that continuously steers physical control parameters during computation.

## Framework Architecture

### Three-Layer System

1. **Physical Layer**: Analog control signals manipulate qubits
2. **QEC Layer**: Repetitive error detection digitizes errors into syndromes
3. **RL Layer**: Agent learns from syndrome patterns to adjust physical controls

### Key Innovations

- **Dual-Use Syndromes**: QEC error detection events serve both logical correction AND as RL training signal
- **Continuous Calibration**: No need to halt computation for recalibration
- **Size-Independent Optimization**: RL optimization speed independent of system size (confirmed up to distance-15 surface codes)

## Implementation Guide

### Step 1: Define State Space

```python
# State = recent syndrome measurement history
# Shape: (time_window, num_syndrome_qubits)
state = syndrome_history[-lookback:]  # e.g., lookback=10 cycles
```

### Step 2: Define Action Space

```python
# Actions = adjustments to physical control parameters
# Examples: microwave pulse amplitude, frequency, phase, duration
actions = rl_agent.act(state)
# Apply actions to pulse generator
pulse_params += actions * learning_rate
```

### Step 3: Define Reward Function

```python
# Reward = negative of logical error rate
# Computed from syndrome patterns over time window
def compute_reward(syndrome_sequence):
    error_rate = count_syndrome_violations(syndrome_sequence) / len(syndrome_sequence)
    return -error_rate  # Maximize = minimize errors

# Alternative: use decoder confidence as reward
def compute_decoder_reward(decoder_output):
    return decoder_output.confidence  # Higher confidence = better calibration
```

### Step 4: Training Loop

```python
for episode in range(num_episodes):
    # Run QEC cycles
    for cycle in range(qec_cycles):
        # Measure syndromes
        syndromes = measure_syndrome_qubits()
        
        # Update RL state
        state = update_state(syndromes)
        
        # Get action from RL agent
        action = rl_agent.get_action(state)
        
        # Apply control adjustments
        apply_control_adjustment(action)
        
        # Compute reward
        reward = compute_reward(state)
        
        # Update RL policy
        rl_agent.update(state, action, reward)
```

## Key Results (Willow Processor)

| Metric | Value |
|--------|-------|
| Logical stability improvement | 3.5x against injected drift |
| Surface code error per cycle | ε_L = 7.72(9) × 10⁻⁴ |
| Color code error per cycle | ε_L = 8.19(14) × 10⁻³ |
| Scalability | Confirmed up to distance-15 |

## Practical Tips

1. **Start with simulation**: Validate RL framework on simulated QEC before hardware deployment
2. **Use near-optimal decoders**: Combine RL control with efficient decoding algorithms
3. **Monitor drift patterns**: Different noise sources require different RL state representations
4. **Fine-tune entire system**: Joint optimization of RL + decoder + physical controls yields best results

## Related Concepts

- **Surface Code**: 2D topological QEC code with high threshold (~1%)
- **Color Code**: Alternative topological code enabling transversal gates
- **Syndrome Extraction**: Measuring stabilizer operators to detect errors
- **Environmental Drift**: Time-varying changes in qubit parameters (frequency, coupling)

## References

- arXiv:2511.08493 (2026) - Main paper
- Google Quantum AI Willow processor documentation
- QEC threshold theorems (Aharonov-Ben-Or, Knill-Laflamme)
