---
name: policy-gradient-methods
description: Master REINFORCE, PPO, TRPO - direct policy optimization with trust regions
---

# Policy Gradient Methods

## When to Use This Skill

Invoke this skill when you encounter:

- **Algorithm Selection**: "Should I use policy gradients or DQN for my problem?"
- **REINFORCE Issues**: User implementing REINFORCE with high variance or slow training
- **PPO Implementation**: User building PPO, debugging training, hyperparameter tuning
- **TRPO Questions**: "What's TRPO?", "Should I use TRPO vs PPO?", "How does trust region work?"
- **Continuous Actions**: User with continuous action space (robot, autonomous vehicles, trading)
- **Variance Reduction**: "How do baselines help?", "How to compute advantages?", "Advantage normalization?"
- **Policy vs Value Confusion**: User unsure whether to use policy gradients or value-based methods
- **Actor-Critic Methods**: User implementing A3C, A2C, understanding actor-critic structure
- **Discrete vs Continuous**: User confused about implementing policy gradients for discrete vs continuous actions
- **Training Instability**: "PPO learning suddenly stops", "Rewards collapse", "Loss spikes"
- **Trust Region Concepts**: Understanding how PPO's clipping enforces trust regions

**This skill provides practical implementation guidance for direct policy optimization.**

Do NOT use this skill for:

- Value-based methods like DQN (route to value-based-methods)
- Model-based RL (route to model-based-rl)
- Offline RL (route to offline-rl-methods)
- Theory foundations (route to rl-foundations)
- Advanced variants (route to advanced-rl-topics)

---

## Core Principle

**Policy gradient methods directly optimize the policy by following gradients of expected return. They're essential for continuous action spaces and excel when the policy space is simpler than the value function landscape. The fundamental tradeoff: high variance (need baselines) but can handle continuous actions naturally.**

Key insight: Unlike value-based methods that learn Q(s,a) then act greedily, policy gradients parameterize the policy directly: π(a|s,θ) and improve it via gradient ascent on expected return. This fundamental difference makes them:

- Natural for continuous actions (infinite action space, can't enumerate all actions)
- Capable of stochastic policies (useful for exploration and multi-modal solutions)
- Directly optimizing the objective you care about (expected return)
- But suffering from high variance (need variance reduction techniques)

**Use policy gradients for**:

- Continuous control (robot arms, autonomous vehicles, physics simulation)
- Stochastic policies required (exploration strategies, risk-aware policies)
- Large/continuous action spaces
- When value function is harder to learn than policy

**Do not use for** (use value-based methods instead):

- Discrete action spaces where you can enumerate all actions (use DQN)
- When off-policy efficiency is critical and state space huge (use DQN)
- Tabular/small discrete problems (Q-learning faster to converge)

---

## Part 1: Policy Gradient Theorem Foundation

### The Policy Gradient Theorem

This is the mathematical foundation. The theorem states:

```
∇_θ J(θ) = E_τ[∇_θ log π(a|s,θ) Q^π(s,a)]
```

Where:

- J(θ) = expected return (objective to maximize)
- π(a|s,θ) = policy parameterized by θ
- Q^π(s,a) = action value function under policy π
- ∇_θ log π(a|s,θ) = gradient of log-probability (score function)

**What this means**: The expected return gradient is the expectation of (policy gradient × action value). You move the policy in direction of good actions (high Q) and away from bad actions (low Q).

### Why Log-Probability (Score Function)?

The gradient ∇_θ log π(a|s,θ) is crucial. Using log-probability instead of π directly:

```
∇_θ log π(a|s,θ) = ∇_θ π(a|s,θ) / π(a|s,θ)

Key insight: This naturally rescales gradient by 1/π(a|s,θ)
- Actions with low probability get higher gradient signals (explore unusual actions)
- Actions with high probability get lower gradient signals (exploit good actions)
```

### Practical Interpretation

```python
# Pseudocode interpretation
for step in training:
    # 1. Sample trajectory under current policy
    trajectory = sample_trajectory(policy)

    # 2. For each state-action pair in trajectory
    for s, a in trajectory:
        # Compute action value (return from this step)
        q_value = compute_return(trajectory, step)

        # 3. Update policy to increase log-prob of high-value actions
        gradient = q_value * ∇ log π(a|s,θ)

        # 4. Gradient ascent on expected return
        θ ← θ + α * gradient
```

**Key insight**: If q_value > 0 (good action), increase probability. If q_value < 0 (bad action), decrease probability.

### The Baseline Problem

Raw policy gradient has huge variance because Q(s,a) values vary widely. For example:

```
Same trajectory, two baseline approaches:
WITHOUT baseline: Q values range from -1000 to +1000
  - Small differences in action quality get lost in noise
  - Gradient updates noisy and unstable

WITH baseline: Advantages A(s,a) = Q(s,a) - V(s) range from -50 to +50
  - Relative quality captured, absolute scale reduced
  - Gradient updates stable and efficient
```

---

## Part 2: REINFORCE - Vanilla Policy Gradient

### Algorithm: REINFORCE

REINFORCE is the simplest policy gradient algorithm:

```
Algorithm: REINFORCE
Input: policy π(a|s,θ), learning rate α
1. Initialize policy parameters θ

for episode in 1 to num_episodes:
    # Collect trajectory
    τ = [(s_0, a_0, r_0), (s_1, a_1, r_1), ..., (s_T, a_T, r_T)]

    # Compute returns (cumulative rewards from each step)
    for t = 0 to T:
        G_t = r_t + γ*r_{t+1} + γ²*r_{t+2} + ... + γ^{T-t}*r_T

    # Update policy (gradient ascent)
    for t = 0 to T:
        θ ← θ + α * G_t * ∇_θ log π(a_t|s_t,θ)
```

### REINFORCE Implementation Details

**Discrete Actions** (softmax policy):

```python
import torch
import torch.nn as nn
from torch.distributions import Categorical

class REINFORCEAgent:
    def __init__(self, state_dim, action_dim, hidden=128, lr=0.01):
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=lr)

    def compute_returns(self, rewards, gamma=0.99):
        """Compute cumulative returns"""
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        return torch.tensor(returns, dtype=torch.float32)

    def train_step(self, states, actions, rewards):
        """Single training step"""
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)

        # Get policy logits
        logits = self.network(states)

        # Get log probabilities (softmax + log)
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        log_prob_actions = log_probs.gather(1, actions.unsqueeze(1)).squeeze()

        # Compute returns
        returns = self.compute_returns(rewards)

        # Policy gradient loss (negative because optimizer minimizes)
        loss = -(log_prob_actions * returns).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
```

**Continuous Actions** (Gaussian policy):

```python
class REINFORCEContinuous:
    def __init__(self, state_dim, action_dim, hidden=128, lr=0.01):
        self.mean_network = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )
        self.log_std = nn.Parameter(torch.zeros(action_dim))
        self.optimizer = torch.optim.Adam(
            list(self.mean_network.parameters()) + [self.log_std],
            lr=lr
        )

    def train_step(self, states, actions, rewards):
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.float32)

        # Get policy mean
        mean = self.mean_network(states)
        std = torch.exp(self.log_std)

        # Gaussian log probability
        var = std.pow(2)
        log_prob = -0.5 * ((actions - mean) ** 2 / var).sum(dim=-1)
        log_prob -= 0.5 * torch.log(var).sum(dim=-1)

        returns = self.compute_returns(rewards)
        loss = -(log_prob * returns).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
```

### REINFORCE Pitfall #1: Ignoring High Variance

**Scenario**: User implements REINFORCE and sees training curve: extremely noisy, takes millions of samples to learn simple task.

**Problem**:

```
REINFORCE uses raw returns G_t = R_t + γR_{t+1} + ...
These have huge variance because:
- Stochastic environment: same action has different outcomes
- Credit assignment: which action caused reward 100 steps later?
- Result: gradient updates are noisy, learning inefficient
```

**Red Flag**: If you see extreme noise in training and slow convergence with REINFORCE, you're missing variance reduction.

**Solution**: Add baseline (value function estimate).

---

## Part 3: Baseline and Advantage Estimation

### Why Baselines Reduce Variance

Baseline b(s) is any function of state that doesn't change policy (0-gradient), but reduces variance:

```
Advantage: A(s,a) = Q(s,a) - b(s)

Mathematical property:
E[b(s) * ∇ log π(a|s)] = 0  (baseline cancels out in expectation)

But variance reduces:
Var[Q(s,a) * ∇ log π] >> Var[A(s,a) * ∇ log π]
```

### Value Function as Baseline

Standard baseline: learn V(s) to estimate expected return from state s.

```
Advantage estimation:
A(s,a) = r + γV(s') - V(s)  [1-step temporal difference]

or

A(s,a) = r + γV(s') - V(s) + γ² V(s'') - γV(s') + ...  [n-step]

or

A(s,a) = G_t - V(s)  [Monte Carlo, use full return]
```

### Advantage Normalization

Critical for training stability:

```python
# Compute advantages
advantages = returns - baseline_values

# Normalize (zero mean, unit variance)
advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
```

**Why normalize?**

```
Without: advantages might be [-1000, 1000] → huge gradient updates
With: advantages might be [-2, 2] → stable gradient updates
```

### Baseline Network Implementation

```python
class PolicyGradientWithBaseline:
    def __init__(self, state_dim, action_dim, hidden=128, lr=0.001):
        # Policy network (discrete actions)
        self.policy = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )

        # Value network (baseline)
        self.value = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)
        )

        self.optimizer = torch.optim.Adam(
            list(self.policy.parameters()) + list(self.value.parameters()),
            lr=lr
        )

    def train_step(self, states, actions, rewards):
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)

        # Get policy and value estimates
        logits = self.policy(states)
        values = self.value(states).squeeze()

        # Compute returns
        returns = self.compute_returns(rewards)

        # Advantages (with normalization)
        advantages = returns - values.detach()
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Policy loss: maximize expected return
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        log_prob_actions = log_probs.gather(1, actions.unsqueeze(1)).squeeze()
        policy_loss = -(log_prob_actions * advantages).mean()

        # Value loss: minimize squared error
        value_loss = ((returns - values) ** 2).mean()

        # Combined loss
        loss = policy_loss + 0.5 * value_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
```

### Pitfall #2: Unnormalized Advantages

**Scenario**: User computes advantages but doesn't normalize, gets training instability.

**Problem**:

```
Without normalization:
- Advantages might be [−500, 0, 500] (varies widely)
- Policy gradients huge: 500 * ∇log π is massive
- Learning rate must be tiny to avoid divergence
- Training unstable and slow

With normalization:
- Advantages become [−1, 0, 1] (standardized)
- Gradients stable and proportional
- Can use higher learning rate
- Training smooth and efficient
```

**Red Flag**: If training is unstable with policy gradients, first check advantage normalization.

---

## Part 4: PPO - Proximal Policy Optimization

### PPO: The Practical Standard

PPO is the most popular policy gradient method because it's simple, stable, and effective.

**Key idea**: Prevent policy from changing too much per update (trust region).

### PPO Clipped Surrogate Loss

PPO uses clipping to enforce trust region:

```
L^CLIP(θ) = E_t[min(r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t)]

Where:
r_t(θ) = π(a_t|s_t,θ) / π(a_t|s_t,θ_old)  [probability ratio]
ε = clip parameter (typically 0.2)
A_t = advantage at time t
```

**What clipping does**:

```
Advantage A > 0 (good action):
  - Without clipping: r can be arbitrarily large → huge gradient
  - With clipping: r is bounded by (1+ε) → gradient capped

Advantage A < 0 (bad action):
  - Without clipping: r can shrink to 0 → small gradient
  - With clipping: r is bounded by (1-ε) → prevents overuse

Result: Policy changes bounded per update (trust region)
```

### PPO Implementation (Discrete Actions)

```python
class PPOAgent:
    def __init__(self, state_dim, action_dim, hidden=128, lr=0.0003, clip_ratio=0.2):
        self.policy = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )

        self.value = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)
        )

        self.optimizer = torch.optim.Adam(
            list(self.policy.parameters()) + list(self.value.parameters()),
            lr=lr
        )
        self.clip_ratio = clip_ratio

    def train_step(self, states, actions, rewards, old_log_probs):
        """
        Train on collected batch using clipped surrogate loss

        Args:
            states: batch of states
            actions: batch of actions
            rewards: batch of returns
            old_log_probs: log probabilities from old policy
        """
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        returns = torch.tensor(rewards, dtype=torch.float32)
        old_log_probs = torch.tensor(old_log_probs, dtype=torch.float32)

        # Get current policy and value
        logits = self.policy(states)
        values = self.value(states).squeeze()

        # New log probabilities under current policy
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        log_prob_actions = log_probs.gather(1, actions.unsqueeze(1)).squeeze()

        # Probability ratio (new policy / old policy)
        ratio = torch.exp(log_prob_actions - old_log_probs)

        # Compute advantages with normalization
        advantages = returns - values.detach()
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Clipped surrogate loss (PPO's key contribution)
        unclipped = ratio * advantages
        clipped = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio) * advantages
        policy_loss = -torch.min(unclipped, clipped).mean()

        # Value loss
        value_loss = ((returns - values) ** 2).mean()

        # Entropy bonus (exploration)
        entropy = -(log_probs * torch.exp(log_probs)).sum(dim=-1).mean()

        # Total loss
        loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
        self.optimizer.step()

        return loss.item()
```

### PPO for Continuous Actions

```python
class PPOContinuous:
    def __init__(self, state_dim, action_dim, hidden=128, lr=0.0003):
        self.mean_network = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )
        self.log_std = nn.Parameter(torch.zeros(action_dim))

        self.value = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)
        )

        self.optimizer = torch.optim.Adam(
            list(self.mean_network.parameters()) +
            list(self.value.parameters()) +
            [self.log_std],
            lr=lr
        )
        self.clip_ratio = 0.2

    def compute_log_prob(self, states, actions):
        """Compute log probability of actions under Gaussian policy"""
        mean = self.mean_network(states)
        std = torch.exp(self.log_std)

        var = std.pow(2)
        log_prob = -0.5 * ((actions - mean) ** 2 / var).sum(dim=-1)
        log_prob -= 0.5 * torch.log(var).sum(dim=-1)

        return log_prob

    def train_step(self, states, actions, rewards, old_log_probs):
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.float32)
        returns = torch.tensor(rewards, dtype=torch.float32)
        old_log_probs = torch.tensor(old_log_probs, dtype=torch.float32)

        # Current policy
        log_probs = self.compute_log_prob(states, actions)
        values = self.value(states).squeeze()

        # Probability ratio
        ratio = torch.exp(log_probs - old_log_probs)

        # Advantages
        advantages = returns - values.detach()
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # PPO loss
        unclipped = ratio * advantages
        clipped = torch.clamp(ratio, 0.8, 1.2) * advantages
        policy_loss = -torch.min(unclipped, clipped).mean()

        value_loss = ((returns - values) ** 2).mean()

        loss = policy_loss + 0.5 * value_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
```

### PPO Pitfall #3: Wrong Clip Ratio Selection

**Scenario**: User sets clip_ratio=0.5 (too large) and agent learns very slowly.

**Problem**:

```
Clip ratio controls trust region size:
- Too small (0.05): policy restricted too much, underfits trajectories
- Too large (0.5): policy can change drastically, causes instability

Standard 0.2 works for most problems.
For sensitive environments: use 0.1
For robust environments: can use 0.3
```

**Red Flag**: If PPO isn't learning, before changing architecture check clip_ratio.

---

## Part 5: TRPO vs PPO - Trust Regions

### TRPO: Trust Region Policy Optimization

TRPO is the predecessor to PPO, using natural gradient with KL divergence constraint:

```
Maximize: E_t[r_t(θ) A_t]

Subject to: E[KL(π_old || π_new)] ≤ δ  (trust region constraint)

Implementation: natural gradient + conjugate gradient optimization
```

### TRPO vs PPO Comparison

| Aspect | TRPO | PPO |
|--------|------|-----|
| **Optimization** | Second-order (Fisher) + conjugate gradient | First-order (Adam) |
| **Constraint** | KL divergence with Lagrange multiplier | Clipping |
| **Complexity** | High (Fisher matrix computation) | Low (simple clipping) |
| **Sample Efficiency** | Slightly better | Comparable, simpler |
| **Implementation** | Complex (Fisher-vector products) | Simple (few lines) |
| **When to use** | Research/specialized | Production/practical |

**Rule of thumb**: Use PPO in 99% of cases. TRPO useful when:

- Researching trust regions
- Very high-dimensional problems where KL constraint matters
- Academic/theoretical work

### Why PPO Won

PPO's clipping approximates TRPO's KL constraint much more simply:

```
TRPO: Explicit KL divergence in optimization
PPO: Clipping implicitly prevents large policy divergence

Result: PPO achieves ~95% of TRPO's benefits with ~10% of complexity
```

---

## Part 6: When to Use Policy Gradients vs Value Methods

### Decision Framework

**Use Policy Gradients if**:

1. **Continuous action space** (position, velocity, torque)
   - Value methods need discretization (curse of dimensionality)
   - Policy gradients handle continuous naturally

2. **Stochastic policy required** (exploration, risk)
   - Policy gradients can naturally be stochastic
   - Value methods produce deterministic policies

3. **Policy space simpler than value space**
   - Sometimes policy easier to learn than Q-function
   - Especially in high-dimensional state/action spaces

**Use Value Methods (DQN) if**:

1. **Discrete action space** where you enumerate all actions
   - Sample-efficient with offline capability
   - No need for baseline variance reduction

2. **Off-policy efficiency critical** (limited data)
   - DQN naturally off-policy (experience replay)
   - Policy gradients typically on-policy

3. **Small discrete state/action spaces**
   - Simpler to implement and tune
   - Faster convergence

### Example Decision Process

```
Problem: Robot arm control (continuous 7D joint angles)
- Continuous action space → Use policy gradients
- Can't discretize (7^10 combinations way too many)
- PPO or TRPO appropriate

Problem: Video game (discrete button presses)
- Discrete actions → Value methods good option
- Can enumerate all actions (4-18 actions typical)
- DQN + variants (Double, Dueling, Rainbow) work well

Problem: Atari with continuous control modification
- Continuous output → Must use policy gradients
- DQN not applicable
- A3C, PPO, SAC appropriate
```

---

## Part 7: Common Pitfalls and Debugging

### Pitfall #4: Reward Scale Issues

**Scenario**: User trains policy gradient on custom environment, rewards in range [0, 1000], training doesn't work.

**Problem**:

```
Large reward scale affects learning:
- Reward 500 with baseline 400 → advantage 100 → huge gradient
- Same problem with different magnitude masks learning signal
- Solution: Reward clipping or normalization

Options:
1. Clip: rewards = clip(rewards, -1, 1)  [if known range]
2. Running normalization: track reward mean/std
3. Scaling: rewards = rewards / max_reward
```

**Solution**:

```python
# Running normalization
class RewardNormalizer:
    def __init__(self):
        self.mean = 0
        self.var = 1
        self.count = 0

    def normalize(self, reward):
        self.count += 1
        delta = reward - self.mean
        self.mean += delta / self.count
        self.var = self.var * (self.count - 1) / self.count + \
                   delta ** 2 / self.count
        return (reward - self.mean) / (np.sqrt(self.var) + 1e-8)
```

### Pitfall #5: Vanishing Gradients with Small Variance

**Scenario**: Policy converges to deterministic (low variance), gradients become near-zero, learning plateaus.

**Problem**:

```
In Gaussian policy: std = exp(log_std)
If log_std → -∞, then std → 0, policy deterministic
Deterministic policy: ∇log π ≈ 0 (flat log-prob landscape)
Gradient vanishes, learning stops
```

**Solution**: Entropy bonus or minimum std:

```python
# Option 1: Entropy bonus (favors exploration)
entropy = 0.5 * torch.sum(torch.log(2 * torch.pi * torch.e * std))
loss = policy_loss - 0.01 * entropy  # Encourage exploration

# Option 2: Minimum std (hard constraint)
log_std = torch.clamp(log_std, min=-20)  # Prevent std→0
```

### Pitfall #6: Credit Assignment Over Long Horizons

**Scenario**: Multi-step MDP with long trajectories, policy learns late-step actions but not early steps.

**Problem**:

```
Return G_t = r_t + γr_{t+1} + γ²r_{t+2} + ... + γ^T r_T

For early steps (t=0) with T=1000:
- Return depends on 1000 future steps
- Huge variance from far-future rewards
- Gradient signal diluted: what caused reward at t=800?

Solution: n-step advantages + GAE (Generalized Advantage Estimation)
```

**GAE Solution**:

```python
def gae(rewards, values, gamma=0.99, lambda_=0.95):
    """Generalized Advantage Estimation"""
    advantages = []
    gae_value = 0

    for t in reversed(range(len(rewards))):
        # TD residual
        if t < len(rewards) - 1:
            td_residual = rewards[t] + gamma * values[t+1] - values[t]
        else:
            td_residual = rewards[t] - values[t]

        # GAE accumulation
        gae_value = td_residual + gamma * lambda_ * gae_value
        advantages.insert(0, gae_value)

    return torch.tensor(advantages, dtype=torch.float32)
```

### Pitfall #7: Batch Size and Training Stability

**Scenario**: User trains on tiny batches (batch_size=4), gets highly unstable gradient estimates.

**Problem**:

```
Advantages have huge variance on small batches:
- Batch of 4 experiences: advantages might be [-500, -300, 200, 1500]
- Mean/std computation unstable (high variance)
- Normalized advantages: might be [-0.2, -0.1, 0.3, 0.8]
- This varies wildly per batch → training unstable

Solution: Larger batches (256-4096 depending on problem)
```

**Rule of thumb**:

```
- Simple problems: batch_size=256
- Complex continuous control: batch_size=2048-4096
- Make sure: max_episode_length << batch_size (decorrelation)
```

### Pitfall #8: Learning Rate Too High

**Scenario**: Policy gradient loss oscillates wildly, returns sometimes improve then collapse.

**Problem**:

```
Policy gradient updates are on probability distribution:
- Large learning rate → policy changes drastically per step
- KL divergence between successive policies huge
- Training unstable, collapse to local minima

PPO's clipping helps but doesn't eliminate problem
```

**Solution**: Conservative learning rates:

```
- Discrete (softmax): lr=0.001-0.0003
- Continuous (Gaussian): lr=0.0003-0.0001

Can use learning rate schedule to decay:
lr = base_lr * (1 - progress)
```

### Red Flags Summary

| Red Flag | Likely Cause | Fix |
|----------|-------------|-----|
| Training extremely noisy | Missing baseline or unnormalized advantages | Add value network + advantage normalization |
| Loss spikes, returns collapse | Learning rate too high or clip_ratio wrong | Reduce lr, check clip_ratio (0.2 standard) |
| Policy converges to deterministic | Low entropy bonus | Add entropy term: `loss - 0.01 * entropy` |
| Slow learning, high sample inefficiency | REINFORCE without advantages | Use PPO or add baselines |
| Early steps not learned | Long horizon credit assignment | Use GAE for advantage estimation |
| Gradient NaN or divergence | Reward scale or gradient explosion | Clip rewards or use gradient norm clipping |

---

## Part 8: Discrete vs Continuous Actions

### Discrete Actions (Softmax Policy)

**Network output**: logits for each action

```python
# Policy network output
logits = network(state)  # shape: [batch, num_actions]

# Convert to probabilities (softmax)
probs = torch.softmax(logits, dim=-1)  # [batch, num_actions]

# Sample action
dist = torch.distributions.Categorical(probs)
action = dist.sample()

# Log probability of specific action
log_prob = dist.log_prob(action)
```

**Key points**:

- Output dimensionality = number of discrete actions
- Softmax ensures valid probability distribution
- Log-probability: `log(π(a|s))`

### Continuous Actions (Gaussian Policy)

**Network output**: mean and std for Gaussian distribution

```python
# Policy network outputs
mean = mean_network(state)  # shape: [batch, action_dim]
log_std = log_std_param     # learnable parameter

std = torch.exp(log_std)    # ensure std > 0

# Create Gaussian distribution
dist = torch.distributions.Normal(mean, std)

# Sample action
action = dist.sample()

# Log probability
log_prob = dist.log_prob(action).sum(dim=-1)  # sum across dimensions
```

**Key points**:

- Output dimensionality = action dimensionality
- Parameterize as log_std (ensures std > 0)
- Log-probability sums across action dimensions

### Implementation Comparison

```python
class DiscretePolicy(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Linear(state_dim, action_dim)

    def forward(self, state):
        logits = self.net(state)
        return torch.softmax(logits, dim=-1)

    def log_prob(self, state, action):
        probs = self.forward(state)
        return torch.log(probs[torch.arange(len(probs)), action])


class ContinuousPolicy(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.mean_net = nn.Linear(state_dim, action_dim)
        self.log_std = nn.Parameter(torch.zeros(action_dim))

    def forward(self, state):
        mean = self.mean_net(state)
        std = torch.exp(self.log_std)
        return mean, std

    def log_prob(self, state, action):
        mean, std = self.forward(state)
        var = std ** 2
        log_prob = -0.5 * ((action - mean) ** 2 / var).sum(dim=-1)
        log_prob -= 0.5 * torch.log(var).sum(dim=-1)
        return log_prob
```

---

## Part 9: Implementation Pitfalls Table

| Pitfall | Symptom | Root Cause | Fix |
|---------|---------|-----------|-----|
| High variance learning | Noisy loss, slow convergence | REINFORCE without baseline | Add value network baseline |
| Training instability | Loss spikes, returns collapse | Unnormalized advantages | Standardize advantages: `(A - μ) / (σ + ε)` |
| Premature convergence | Policy converges to deterministic, learning stops | Low entropy | Add entropy bonus: `-β * entropy` |
| Slow learning | Excellent training behavior but very slow | Too conservative clip_ratio | Try clip_ratio=0.3 or 0.2 |
| Gradient explosion | NaN loss, divergence | Reward scale or bad gradients | Clip rewards or add grad norm clipping |
| Early steps not learned | Late steps work, early steps ignored | Long horizon variance | Use GAE for advantage estimation |
| Value function divergence | Value loss increasing | Value learning rate too high | Reduce value_loss coefficient or lr |
| Mode collapse | Policy too deterministic despite entropy | std too small or initialization | Increase entropy coefficient or initialize higher |

---

## Part 10: Testing Scenarios (13+)

1. **Basic REINFORCE** on CartPole: implement vanilla algorithm
2. **REINFORCE with Baseline** on CartPole: compare variance reduction
3. **PPO Discrete** on CartPole: verify clipping mechanism
4. **PPO Continuous** on MuJoCo: test Gaussian policy
5. **Advantage Normalization** effect: show stability improvement
6. **Batch Size Impact** on training: variance vs stability tradeoff
7. **Reward Scaling** in custom environment: demonstrate necessity
8. **Clip Ratio Sensitivity** in PPO: test different epsilon values
9. **Entropy Bonus** effect: exploration vs exploitation
10. **GAE vs Monte Carlo Returns** on long horizon task: credit assignment
11. **Learning Rate Sensitivity** across discrete and continuous
12. **Value Network Architecture** impact on baseline quality
13. **Policy vs Value Method Selection** framework validation

---

## Part 11: Rationalization Table - When Users Get It Wrong

| User Claim | Rationalization | Correct Approach |
|-----------|-----------------|------------------|
| "DQN should work for continuous actions, I'll discretize" | Can discretize but: curse of dimensionality (7D joint→7^n combos), loses continuous structure, very inefficient | Use policy gradients (PPO, SAC) naturally designed for continuous |
| "REINFORCE is too slow, must be something wrong" | REINFORCE has high variance by design. Problem: not using baseline | Add value network baseline (variance reduction) or switch to PPO |
| "PPO clip ratio 0.5 is more aggressive, should converge faster" | Larger clip ratio = larger trust region = less stability. Faster ≠ better | Use 0.2 (standard) or 0.15-0.3 range. Larger can diverge |
| "Policy gradients have huge variance, value-based better for all problems" | Confusion: policy gradients handle continuous actions, DQN doesn't | Choose based on action space: discrete→consider DQN, continuous→policy gradients |
| "I should use very small learning rate like 0.0001 to be safe" | Too conservative: policy learns very slowly, gets stuck in local minima | Use 0.001-0.0003 for discrete, 0.0003-0.0001 for continuous. Test decay. |
| "Unnormalized advantages are fine, I'll just use small learning rate" | Small LR doesn't fix variance explosion in gradients, just masks problem | Normalize advantages: `(A - mean) / (std + ε)` properly |
| "I'll use huge batch size (100k) for stability" | Diminishing returns: beyond 2048 doesn't improve stability, wastes computation | Use 256-4096 depending on problem complexity |
| "Policy should converge to deterministic (low std) for best performance" | Common misconception: deterministic policies get stuck, can't explore | Keep some exploration: entropy bonus prevents premature convergence |
| "TRPO is better than PPO because it's more sophisticated" | Confusing complexity with effectiveness: PPO achieves ~95% TRPO performance with 10% complexity | Use PPO for production unless researching KL constraints |
| "My value network loss oscillates, means gradients bad" | Value oscillation normal during learning. Only problematic if diverging | Add value loss decay, reduce coeff: `loss = policy + 0.1 * value_loss` |

---

## Summary: What You Need to Know

**Policy Gradient Foundation**:

- Policy gradients directly optimize π(a|s,θ) via ∇_θ J(θ)
- Score function ∇_θ log π (gradient of log-probability) crucial for differentiability
- High variance is the key challenge (solved by baselines)

**REINFORCE**:

- Simplest policy gradient algorithm
- Without baseline: high variance, slow learning
- Useful for understanding, not for production

**Baselines & Advantages**:

- Baseline b(s) reduces variance without changing policy
- Advantage A(s,a) = Q(s,a) - V(s) captures relative action quality
- Advantage normalization critical for training stability

**PPO**:

- Most practical policy gradient method (simple + effective)
- Clipping enforces trust region (prevents destructive updates)
- Works for discrete and continuous actions
- Use: clip_ratio=0.2, entropy_coeff=0.01, value_loss_coeff=0.5

**TRPO**:

- Natural gradient + KL constraint (trust region)
- More sophisticated but rarely necessary
- PPO achieves ~95% effectiveness with 10% complexity

**Algorithm Selection**:

- Continuous actions → Policy gradients (PPO, SAC)
- Discrete actions → Value methods (DQN) or policy gradients
- Stochastic policy needed → Policy gradients
- Maximum sample efficiency → DQN (if discrete)

**Key Implementation Details**:

- Advantage normalization: `(A - mean) / (std + ε)`
- Learning rates: 0.001-0.0003 (discrete), 0.0003-0.0001 (continuous)
- Batch size: 256-4096 (larger = more stable but slower)
- Entropy bonus: `-0.01 * entropy` (prevents mode collapse)
- Reward scaling: normalize or clip for stability
- Gradient clipping: `clip_grad_norm_(params, 0.5)` prevents explosion

**Red Flags**:

- Training noisy/slow → Missing baseline
- Loss spikes/instability → Unnormalized advantages, high LR, or clip_ratio wrong
- Deterministic policy → Insufficient entropy
- Gradient NaN → Reward scale or gradient explosion
- Early steps not learning → Need GAE for long horizon

---

## Part 12: Advanced Architecture Considerations

### Network Capacity and Policy Learning

Policy network capacity affects convergence speed and final performance:

**Under-parameterized** (network too small):

```
Problem: Network can't represent optimal policy
- Limited expressivity → stuck with poor solutions
- Example: 2-hidden unit network for complex navigation
- Result: High bias, underfitting

Solution: Increase hidden units (128, 256, 512)
Tradeoff: Slower training but better capacity
```

**Over-parameterized** (network too large):

```
Problem: Network overfits to finite trajectory samples
- Example: 4096-hidden network for simple CartPole
- Result: Fits noise in returns, poor generalization
- But: Modern networks use dropout/regularization

Solution: Standard sizes (128-512 hidden units)
Rule: Match capacity to task complexity
```

**Shared vs Separate Networks**:

```python
# Option 1: Separate policy and value networks
class SeparateNetworks:
    policy = nn.Sequential(...)  # outputs action logits
    value = nn.Sequential(...)   # outputs single value

# Option 2: Shared trunk, separate heads
class SharedTrunk:
    trunk = nn.Sequential(...)    # shared hidden layers
    policy_head = nn.Linear(...)  # policy logits
    value_head = nn.Linear(...)   # value estimate

# Option 3: Fully shared (rare, not recommended)
# Single network outputs both logits and value
```

**Recommendation**: Separate networks are cleaner, shared trunk is common in practice (efficiency), fully shared not recommended.

### Activation Functions and Training

Choice of activation function affects gradient flow:

**ReLU** (most common):

```
Advantages:
- Fast computation
- Prevents vanishing gradients
- Works well with batch normalization

Disadvantages:
- Dead ReLU problem (some units permanently inactive)
- Not smooth at zero
```

**Tanh/Sigmoid** (older, less common):

```
Advantages:
- Smooth gradient everywhere
- Bounded output [-1, 1]

Disadvantages:
- Can suffer vanishing gradients in deep networks
- Slower computation
```

**LeakyReLU** (middle ground):

```
Advantages:
- Fixes dead ReLU (small gradient when inactive)
- Still fast

Disadvantages:
- Extra hyperparameter (leak rate)
- Rarely needed for policy networks
```

**Recommendation**: Use ReLU for standard problems, LeakyReLU if debugging dead unit issues, avoid Tanh for policy networks.

### Gradient Flow and Initialization

Proper initialization prevents gradient explosion/vanishing:

```python
# Good initialization (Xavier/He)
nn.Linear(in_features, out_features)  # PyTorch default is good

# Manual Xavier initialization
nn.init.xavier_uniform_(layer.weight)

# Manual He initialization (better for ReLU)
nn.init.kaiming_uniform_(layer.weight, nonlinearity='relu')

# For output layers (policy logits)
# Often initialized smaller for stability
nn.init.uniform_(policy_output.weight, -3e-3, 3e-3)
nn.init.uniform_(policy_output.bias, -3e-3, 3e-3)
```

**Why it matters**: Poor initialization → vanishing/exploding gradients → training doesn't work.

---

## Part 13: Practical Hyperparameter Tuning

### Systematic Hyperparameter Search

Instead of random guessing, systematic approach:

**Step 1: Start with defaults**

```python
config = {
    'learning_rate': 0.0003,      # Standard
    'clip_ratio': 0.2,             # Standard
    'entropy_coeff': 0.01,         # Standard
    'value_loss_coeff': 0.5,       # Standard
    'batch_size': 64,              # Small, test first
    'num_epochs': 3,               # Updates per batch
}
```

**Step 2: Test on simple environment**

```
- Run on CartPole or simple continuous task
- If works: move to harder task
- If fails: diagnose why before tuning
```

**Step 3: Tune based on observed problem**

```
If training is noisy:
  ↓ increase batch_size (256, 512)
  ↓ increase num_epochs (5-10)
  ↓ decrease learning_rate (0.0001)

If training is slow:
  ↑ increase learning_rate (0.001)
  ↓ decrease batch_size (32)
  ↓ decrease num_epochs (1)

If policy deterministic:
  ↑ entropy_coeff (0.05, 0.1)
  ↑ minimum std (increase from 1e-6)

If value loss not decreasing:
  ↑ value_loss_coeff (1.0, 2.0)
  ↑ learning_rate for value
```

**Step 4: Grid or random search on subset**

```python
# Don't search all combinations, search subset
hyperparams = {
    'learning_rate': [0.0001, 0.0003, 0.001],
    'batch_size': [64, 256, 1024],
    'entropy_coeff': [0.0, 0.01, 0.05],
}

# Random sample 10 combinations
import random
samples = 10
configs = [
    {k: random.choice(v) for k, v in hyperparams.items()}
    for _ in range(samples)
]

# Evaluate each
for config in configs:
    train_and_evaluate(config)
```

### Environment-Specific Tuning

Different environments benefit from different settings:

**Simple Discrete** (CartPole, MountainCar):

```
batch_size: 64-256
learning_rate: 0.001
entropy_coeff: 0.01
clip_ratio: 0.2
```

**Complex Discrete** (Atari):

```
batch_size: 2048-4096
learning_rate: 0.0001-0.0003
entropy_coeff: 0.001-0.01
clip_ratio: 0.1-0.2
```

**Continuous Control** (MuJoCo):

```
batch_size: 2048-4096
learning_rate: 0.0003
entropy_coeff: 0.01
clip_ratio: 0.2
num_epochs: 10-20
```

**Custom Environments**:

```
1. Start with continuous defaults
2. Monitor advantage statistics
3. Check entropy over training
4. Adjust based on observations
```

---

## Part 14: Monitoring and Debugging Tools

### Key Metrics to Monitor

**Policy Loss Metrics**:

```python
# 1. Expected return (should increase)
expected_return = sum(episode_rewards) / num_episodes
# Should show clear upward trend

# 2. Advantage statistics (should be normalized)
mean_advantage = advantages.mean()  # Should be ~0
std_advantage = advantages.std()    # Should be ~1
# Red flag: if std too small (<0.1) or huge (>10)

# 3. Policy entropy (should not approach zero)
entropy = -(probs * log(probs)).sum()
# Red flag: if entropy → 0 (policy deterministic)

# 4. Policy ratio statistics
ratio = new_policy / old_policy
# Should be ~1.0 with small std
# Red flag: if mean >> 1.2 or << 0.8
```

**Value Function Metrics**:

```python
# 1. Value function loss (should decrease)
value_loss = (returns - value_estimates).pow(2).mean()
# Should decrease over training

# 2. Explained variance (higher better)
# How much variance in returns does value explain?
residuals = returns - value_estimates
explained_var = 1 - (residuals.var() / returns.var())
# Good: > 0.8, Bad: < 0.5

# 3. Value estimate magnitude
# Should be reasonable scale
value_mean = value_estimates.mean()
value_std = value_estimates.std()
# Sanity check with return_mean, return_std
```

**Gradient Metrics**:

```python
# 1. Gradient magnitude (should be stable)
for name, param in model.named_parameters():
    if param.grad is not None:
        grad_norm = param.grad.norm()
        # Monitor: should be in [1e-5, 1e1] typically

# 2. Gradient explosion warning
if grad_norm > 1.0:
    print("Warning: large gradients, consider clipping or smaller lr")

# 3. Gradient vanishing warning
if grad_norm < 1e-6:
    print("Warning: tiny gradients, check entropy and baseline")
```

### Debugging Checklist

When training fails:

```python
# 1. Verify data collection
# Sample random trajectory, inspect:
assert len(trajectory) > 0
assert all(not isnan(r) for r in rewards)
assert states.shape[0] == actions.shape[0] == len(rewards)

# 2. Check advantage computation
assert advantages.mean() < 0.1  # Should normalize to ~0
assert advantages.std() > 0.1   # Should have variance

# 3. Verify policy gradient
assert policy_loss > 0  # Should be positive
assert policy_loss < 1e6  # Not explosion

# 4. Check value loss
assert value_loss > 0
assert value_loss < 1e6

# 5. Monitor entropy
assert entropy > 0  # Non-zero
assert entropy < -log(1/num_actions)  # Not above maximum

# 6. Inspect learning
assert returns[-100:].mean() > returns[0:100].mean()  # Improving
```

---

## Part 15: Common Implementation Mistakes

### Mistake #1: Probability Ratio Bugs in PPO

```python
# WRONG: using raw probabilities
ratio = new_probs[action] / old_probs[action]

# CORRECT: using log-probabilities (numerically stable)
ratio = torch.exp(log_new_probs[action] - log_old_probs[action])

# Why: log is numerically stable, avoids underflow for small probs
```

### Mistake #2: Advantage Sign Errors

```python
# WRONG: computing advantage incorrectly
advantage = baseline - return  # Negative of what it should be!

# CORRECT: advantage is how much better than baseline
advantage = return - baseline

# Consequence: policy updated opposite direction
```

### Mistake #3: Log-Probability Dimension Issues

```python
# For continuous actions:

# WRONG: forgetting to sum across dimensions
log_prob = dist.log_prob(action)  # shape: [batch, action_dim]
loss = (log_prob * advantage).mean()  # broadcasting error or wrong reduction

# CORRECT: sum log-probs across action dimensions
log_prob = dist.log_prob(action).sum(dim=-1)  # shape: [batch]
loss = (log_prob * advantage).mean()

# Why: each action dimension contributes to overall probability
```

### Mistake #4: Detaching Value Estimates

```python
# WRONG: advantages affect value network gradients
advantages = returns - values
loss = -log_prob * advantages  # values included in gradient!

# CORRECT: advantages should not backprop to value during policy update
advantages = returns - values.detach()
policy_loss = -log_prob * advantages  # doesn't affect value
value_loss = (returns - values).pow(2).mean()  # separate value update

# Why: policy gradient and value loss are separate objectives
```

### Mistake #5: Entropy Computation for Discrete

```python
# WRONG: using formula for continuous
entropy = 0.5 * log(2 * pi * e * std)  # Only for Gaussian!

# CORRECT: for categorical
entropy = -(probs * log(probs + 1e-8)).sum()

# Or using distribution:
dist = Categorical(probs)
entropy = dist.entropy()
```

### Mistake #6: Old Policy Mismatch in PPO

```python
# WRONG: updating policy, then computing ratio with same policy
for epoch in range(num_epochs):
    logits = policy(states)
    log_probs_new = log_softmax(logits)
    ratio = exp(log_probs_new - old_log_probs)
    loss = clip_loss(ratio, advantages)
    update(loss)  # Modifies policy!

# CORRECT: keep old policy fixed during epochs
old_policy_state = policy.state_dict()  # Save
for epoch in range(num_epochs):
    logits = policy(states)
    log_probs_new = log_softmax(logits)
    # old_log_probs based on old policy, fixed!
    ratio = exp(log_probs_new - old_log_probs)
    loss = clip_loss(ratio, advantages)
    update(loss)
```

---

## Part 16: Performance Tips

### Computation Optimization

**Batch Processing**:

```python
# SLOW: processing one example at a time
for state in states:
    action = sample_action(state)

# FAST: batch all at once
actions = sample_actions(states)  # Vectorized

# Speedup: 10-100x on GPU
```

**In-place Operations**:

```python
# Standard (creates new tensor)
advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

# In-place (reuses memory)
advantages.sub_(advantages.mean()).div_(advantages.std() + 1e-8)

# Speedup: slight, more important for memory
```

**Mixed Precision Training**:

```python
# Use float32 for stability, computation optional
# PyTorch automatic mixed precision:
from torch.cuda.amp import autocast

with autocast():
    loss = compute_loss(...)
    loss.backward()
```

### Memory Optimization

**Trajectory Batching**:

```python
# Collect multiple trajectories before update
trajectories = []
for episode in range(num_episodes):
    traj = collect_episode()
    trajectories.append(traj)

# Stack into batch
states = torch.cat([t['states'] for t in trajectories])  # All at once
# vs creating states during collection (huge memory spike)
```

**Value Function Caching**:

```python
# For long trajectories, compute value once
values = value_network(states)  # Compute all at once
# vs computing in loop during advantage computation
```

---

## Part 17: When to Abandon Policy Gradients

### Problems Not Suited for Policy Gradients

**Sample Inefficiency Critical**:

```
Example: Robot learning from limited real-world rollouts
- Policy gradients: on-policy, need lots of data
- Better: Offline RL, DQN with replay buffer
- Switch to: offline-rl-methods skill
```

**Discrete Action Space + Limited Data**:

```
Example: 4-action game with 1M sample budget
- Policy gradients: require many trajectories
- Better: DQN (off-policy, experience replay)
- Switch to: value-based-methods skill
```

**Exploration Bonus Needed**:

```
Example: Sparse reward environment
- Policy gradients: entropy bonus minimal help
- Better: Curiosity-driven, intrinsic motivation
- Switch to: exploration-methods (if exists)
```

**Simulation Constraints**:

```
Example: Model-based planning where you have world model
- Policy gradients: ignore model information
- Better: Model-based planning (CEM, MPPI)
- Switch to: model-based-rl skill
```

### Red Flags for Switching Algorithms

| Signal | Consider Switching To |
|--------|----------------------|
| Discrete actions + huge sample budget → Can't improve | DQN or Rainbow (value-based-methods) |
| Sparse rewards, no progress → Can't reward learning | Curiosity or hindsight (exploration methods) |
| Have access to world model → Not using it | Model-based planning (model-based-rl) |
| Need off-policy data efficiency → On-policy slow | Offline RL or DQN (offline-rl-methods or value-based) |
| Multimodal solution space → Single mode explored | Evolutionary algorithms or diverse policies |
