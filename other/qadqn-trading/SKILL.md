---
name: qadqn-trading
description: "Quantum Attention Deep Q-Network (QADQN) for financial market prediction and optimal trading strategy development. Variational quantum circuit inside deep Q-learning framework, achieving superior risk-adjusted returns (Sortino ratio 1.28) with real transaction cost modeling. Use when: quantum reinforcement learning trading, quantum attention trading strategy, financial market prediction quantum, QADQN algorithm, quantum-enhanced RL for finance."
---

# QADQN Trading

## Core Methodology

Quantum Attention Deep Q-Network (QADQN) — hybrid quantum-classical reinforcement learning for financial market prediction and optimal trading strategy. Embeds variational quantum circuits within a traditional deep Q-learning framework to leverage quantum advantages in decision-making.

## Architecture

```
Market State → Feature Encoding → Quantum Attention Layer → VQC Q-Value Network → Trading Action
                     ↑                      ↑
              Historical Data         Experience Replay
              (OHLCV, indicators)    + Target Network
```

### Components

1. **State Representation**: Market features (prices, technical indicators) encoded as quantum state via amplitude or angle encoding
2. **Quantum Attention Layer**: Variational quantum circuit computes attention weights over feature dimensions, identifying market-relevant features
3. **Q-Value Network**: Hybrid quantum-classical network outputs Q-values for actions (buy/hold/sell)
4. **Experience Replay**: Standard DQN mechanism with prioritized sampling for stable training
5. **Target Network**: Stabilizes learning via periodic weight copying

## Performance Metrics (S&P 500)

- **Sortino Ratio**: 1.28 (non-overlapping test), 1.19 (overlapping test)
- **Downside Risk Management**: Superior risk-adjusted returns vs classical baselines
- **Transaction Costs**: Validated with fixed cost per trade — realistic market conditions
- **Published**: IEEE QCE 2024 (Quantum Computing and Engineering)

## Implementation Pattern

### Step 1: Data Preparation
- Collect historical market data (OHLCV, volume, technical indicators)
- Split into non-overlapping and overlapping train/test sets
- Normalize features to [-1, 1] for quantum encoding

### Step 2: Quantum Feature Encoding
- Use angle encoding: map each feature to a rotation angle on a qubit
- Number of qubits = number of features (or use amplitude encoding for compression)

### Step 3: Quantum Attention Circuit
- Design VQC with trainable rotation gates
- Compute attention scores via expectation values of Pauli-Z observables
- Softmax attention weights to weight feature contributions

### Step 4: Q-Value Computation
- Pass weighted features through classical layers
- Output Q-values for discrete action space (buy/hold/sell)
- Apply Double DQN or Dueling DQN extensions for stability

### Step 5: Training
- Loss: MSE between predicted Q-values and target Q-values
- Target: r + γ * max_a' Q_target(s', a')
- Gradient descent on both quantum and classical parameters

## When to Use

- Algorithmic trading strategy development with quantum-enhanced decision making
- Risk-aware portfolio management requiring downside protection
- Market regimes where attention over features improves prediction
- NISQ-era hybrid quantum-classical implementations

## Error Handling

- **Quantum noise**: Use noise-aware training, error mitigation (readout correction)
- **Market regime shift**: Retrain periodically with recent data, use rolling window
- **Circuit barren plateaus**: Use layer-wise training, proper initialization, shallow circuits
- **Transaction cost sensitivity**: Include costs in reward function during training

## Source

arXiv: 2408.03088 — "QADQN: Quantum Attention Deep Q-Network for Financial Market Prediction" by Siddhant Dutta, Nouhaila Innan, Alberto Marchisio, Sadok Ben Yahia, Muhammad Shafique. IEEE QCE 2024.

**Activation**: QADQN trading, quantum attention deep q network, quantum RL trading, quantum market prediction, quantum reinforcement learning finance, variational quantum circuit trading
