---
name: exploration-strategies
description: Master ε-greedy, UCB, curiosity-driven, RND, intrinsic motivation exploration
---

# Exploration Strategies in Deep RL

## When to Use This Skill

Invoke this skill when you encounter:

- **Exploration-Exploitation Problem**: Agent stuck in local optimum, not finding sparse rewards
- **ε-Greedy Tuning**: Designing or debugging epsilon decay schedules
- **Sparse Reward Environments**: Montezuma's Revenge, goal-conditioned tasks, minimal feedback
- **Large State Spaces**: Too many states for random exploration to be effective
- **Curiosity-Driven Learning**: Implementing or understanding intrinsic motivation
- **RND (Random Network Distillation)**: Novelty-based exploration for sparse rewards
- **Count-Based Exploration**: Encouraging discovery in discrete/tabular domains
- **Exploration Stability**: Agent explores too much/little, inconsistent performance
- **Method Selection**: Which exploration strategy for this problem?
- **Computational Cost**: Balancing exploration sophistication vs overhead
- **Boltzmann Exploration**: Softmax-based action selection and temperature tuning

**Core Problem:** Many RL agents get stuck exploiting a local optimum, never finding sparse rewards or exploring high-dimensional state spaces effectively. Choosing the right exploration strategy is fundamental to success.

## Do NOT Use This Skill For

- **Algorithm selection** (route to rl-foundations or specific algorithm skills like value-based-methods, policy-gradient-methods)
- **Reward design issues** (route to reward-shaping-engineering)
- **Environment bugs causing poor exploration** (route to rl-debugging first to verify environment works correctly)
- **Basic RL concepts** (route to rl-foundations for MDPs, value functions, Bellman equations)
- **Training instability unrelated to exploration** (route to appropriate algorithm skill or rl-debugging)

---

## Core Principle: The Exploration-Exploitation Tradeoff

### The Fundamental Tension

In reinforcement learning, every action selection is a decision:

- **Exploit**: Take the action with highest estimated value (maximize immediate reward)
- **Explore**: Try a different action to learn about its value (find better actions)

```
Exploitation Extreme:
- Only take the best-known action
- High immediate reward (in training)
- BUT: Stuck in local optimum if initial action wasn't optimal
- Risk: Never find the actual best reward

Exploration Extreme:
- Take random actions uniformly
- Will eventually find any reward
- BUT: Wasting resources on clearly bad actions
- Risk: No learning because too much randomness

Optimal Balance:
- Explore enough to find good actions
- Exploit enough to benefit from learning
```

### Why Exploration Matters

**Scenario 1: Sparse Reward Environment**

Imagine an agent in Montezuma's Revenge (classic exploration benchmark):

- Most states give reward = 0
- First coin gives +1 (at step 500+)
- Without exploring systematically, random actions won't find that coin in millions of steps

Without exploration strategy:

```
Steps 0-1,000: Random actions, no reward signal
Steps 1,000-10,000: Learned to get to the coin, finally seeing reward
Problem: Took 1,000 steps of pure random exploration!

With smart exploration (RND):
Steps 0-100: RND detects novel states, guides toward unexplored areas
Steps 100-500: Finds coin much faster because exploring strategically
Result: Reward found in 10% of steps
```

**Scenario 2: Local Optimum Trap**

Agent finds a small reward (+1) from a simple policy:

```
Without decay:
- Agent learns exploit_policy achieves +1
- ε-greedy with ε=0.3: Still 30% random (good, explores)
- BUT: 70% exploiting suboptimal policy indefinitely

With decay:
- Step 0: ε=1.0, 100% explore
- Step 100k: ε=0.05, 5% explore
- Step 500k: ε=0.01, 1% explore
- Result: Enough exploration to find +5 reward, then exploit it
```

### Core Rule

**Exploration is an investment with declining returns.**

- Early training: Exploration critical (don't know anything yet)
- Mid training: Balanced (learning but not confident)
- Late training: Exploitation dominant (confident in good actions)

---

## Part 1: ε-Greedy Exploration

### The Baseline Method

ε-Greedy is the simplest exploration strategy: with probability ε, take a random action; otherwise, take the greedy (best-known) action.

```python
import numpy as np

def epsilon_greedy_action(q_values, epsilon):
    """
    Select action using ε-greedy.

    Args:
        q_values: Q(s, *) - values for all actions
        epsilon: exploration probability [0, 1]

    Returns:
        action: int (0 to num_actions-1)
    """
    if np.random.random() < epsilon:
        # Explore: random action
        return np.random.randint(len(q_values))
    else:
        # Exploit: best action
        return np.argmax(q_values)
```

### Why ε-Greedy Works

1. **Simple**: Easy to implement and understand
2. **Guaranteed Convergence**: Will eventually visit all states (if ε > 0)
3. **Effective Baseline**: Works surprisingly well for many tasks
4. **Interpretable**: ε has clear meaning (probability of random action)

### When ε-Greedy Fails

```
Problem Space → Exploration Effectiveness:

Small discrete spaces (< 100 actions):
- ε-greedy: Excellent ✓
- Reason: Random exploration covers space quickly

Large discrete spaces (100-10,000 actions):
- ε-greedy: Poor ✗
- Reason: Random action is almost always bad
- Example: Game with 500 actions, random 1/500 chance is right action

Continuous action spaces:
- ε-greedy: Terrible ✗
- Reason: Random action in [-∞, ∞] is meaningless noise
- Alternative: Gaussian noise on action (not true ε-greedy)

Sparse rewards, large state spaces:
- ε-greedy: Hopeless ✗
- Reason: Random exploration won't find rare reward before heat death
- Alternative: Curiosity, RND, intrinsic motivation
```

### ε-Decay Schedules

The key insight: ε should decay over time. Explore early, exploit late.

#### Linear Decay

```python
def epsilon_linear(step, total_steps, epsilon_start=1.0, epsilon_end=0.1):
    """
    Linear decay from epsilon_start to epsilon_end.

    ε(t) = ε_start - (ε_start - ε_end) * t / T
    """
    t = min(step, total_steps)
    return epsilon_start - (epsilon_start - epsilon_end) * t / total_steps
```

**Properties:**

- Simple, predictable, easy to tune
- Equal exploration reduction per step
- Good for most tasks

**Guidance:**

- Use if no special knowledge about task
- `epsilon_start = 1.0` (explore fully initially)
- `epsilon_end = 0.01` to `0.1` (small residual exploration)
- `total_steps = 1,000,000` (typical deep RL)

#### Exponential Decay

```python
def epsilon_exponential(step, decay_rate=0.9995):
    """
    Exponential decay with constant rate.

    ε(t) = ε_0 * decay_rate^t
    """
    return 1.0 * (decay_rate ** step)
```

**Properties:**

- Fast initial decay, slow tail
- Aggressive early exploration cutoff
- Exploration drops exponentially

**Guidance:**

- Use if task rewards are found quickly
- `decay_rate = 0.9995` is gentle (1% per 100 steps)
- `decay_rate = 0.999` is aggressive (1% per step)
- Watch for premature convergence to local optimum

#### Polynomial Decay

```python
def epsilon_polynomial(step, total_steps, epsilon_start=1.0,
                       epsilon_end=0.01, power=2.0):
    """
    Polynomial decay: ε(t) = ε_start * (1 - t/T)^p

    power=1: Linear
    power=2: Quadratic (faster early decay)
    power=0.5: Slower decay
    """
    t = min(step, total_steps)
    fraction = t / total_steps
    return epsilon_start * (1 - fraction) ** power
```

**Properties:**

- Smooth, tunable decay curve
- Power > 1: Fast early decay, slow tail
- Power < 1: Slow early decay, fast tail

**Guidance:**

- `power = 2.0`: Quadratic (balanced, common)
- `power = 3.0`: Cubic (aggressive early decay)
- `power = 0.5`: Slower (gentle early decay)

### Practical Guidance: Choosing Epsilon Parameters

```
Rule of Thumb:
- epsilon_start = 1.0 (explore uniformly initially)
- epsilon_end = 0.01 to 0.1 (maintain minimal exploration)
  - 0.01: For large action spaces (need some exploration)
  - 0.05: Default choice
  - 0.1: For small action spaces (can afford random actions)
- total_steps: Based on training duration
  - Usually 500k to 1M steps
  - Longer if rewards are sparse or delayed

Task-Specific Adjustments:
- Sparse rewards: Longer decay (explore for more steps)
- Dense rewards: Shorter decay (can exploit earlier)
- Large action space: Higher epsilon_end (maintain exploration)
- Small action space: Lower epsilon_end (exploitation is cheap)
```

### ε-Greedy Pitfall 1: Decay Too Fast

```python
# WRONG: Decays to 0 in just 10k steps
epsilon_final = 0.01
decay_steps = 10_000
epsilon = epsilon_final ** (step / decay_steps)  # ← BUG

# CORRECT: Decays gently over training
total_steps = 1_000_000
epsilon_linear(step, total_steps, epsilon_start=1.0, epsilon_end=0.01)
```

**Symptom:** Agent plateaus early, never improves past initial local optimum

**Fix:** Use longer decay schedule, ensure epsilon_end > 0

### ε-Greedy Pitfall 2: Never Decays (Constant ε)

```python
# WRONG: Fixed epsilon forever
epsilon = 0.3  # Constant

# CORRECT: Decay epsilon over time
epsilon = epsilon_linear(step, total_steps=1_000_000)
```

**Symptom:** Agent learns but performance noisy, can't fully exploit learned policy

**Fix:** Add epsilon decay schedule

### ε-Greedy Pitfall 3: Epsilon on Continuous Actions

```python
# WRONG: Discrete epsilon-greedy on continuous actions
action = np.random.uniform(-1, 1) if random() < epsilon else greedy_action

# CORRECT: Gaussian noise on continuous actions
def continuous_exploration(action, exploration_std=0.1):
    return action + np.random.normal(0, exploration_std, action.shape)
```

**Symptom:** Continuous action spaces don't benefit from ε-greedy (random action is meaningless)

**Fix:** Use Gaussian noise or other continuous exploration methods

---

## Part 2: Boltzmann Exploration

### Temperature-Based Action Selection

Instead of deterministic greedy action, select actions proportional to their Q-values using softmax with temperature T.

```python
def boltzmann_exploration(q_values, temperature=1.0):
    """
    Select action using Boltzmann distribution.

    P(a) = exp(Q(s,a) / T) / Σ exp(Q(s,a') / T)

    Args:
        q_values: Q(s, *) - values for all actions
        temperature: Exploration parameter
          T → 0: Becomes deterministic (greedy)
          T → ∞: Becomes uniform random

    Returns:
        action: int (sampled from distribution)
    """
    # Subtract max for numerical stability
    q_shifted = q_values - np.max(q_values)

    # Compute probabilities
    probabilities = np.exp(q_shifted / temperature)
    probabilities = probabilities / np.sum(probabilities)

    # Sample action
    return np.random.choice(len(q_values), p=probabilities)
```

### Properties vs ε-Greedy

| Feature | ε-Greedy | Boltzmann |
|---------|----------|-----------|
| Good actions | Probability: 1-ε | Probability: higher (proportional to Q) |
| Bad actions | Probability: ε/(n-1) | Probability: lower (proportional to Q) |
| Action selection | Deterministic or random | Stochastic distribution |
| Exploration | Uniform random | Biased toward better actions |
| Tuning | ε (1 parameter) | T (1 parameter) |

**Key Advantage:** Boltzmann balances better—good actions are preferred but still get chances.

```
Example: Three actions with Q=[10, 0, -10]

ε-Greedy (ε=0.2):
- Action 0: P=0.8 (exploit best)
- Action 1: P=0.1 (random)
- Action 2: P=0.1 (random)
- Problem: Good actions (Q=0, -10) barely sampled

Boltzmann (T=2):
- Action 0: P=0.88 (exp(10/2)=e^5 ≈ 148)
- Action 1: P=0.11 (exp(0/2)=1)
- Action 2: P=0.01 (exp(-10/2)≈0.007)
- Better: Action 1 still gets 11% (not negligible)
```

### Temperature Decay Schedule

Like epsilon, temperature should decay: start high (explore), end low (exploit).

```python
def temperature_decay(step, total_steps, temp_start=1.0, temp_end=0.1):
    """
    Linear temperature decay.

    T(t) = T_start - (T_start - T_end) * t / T_total
    """
    t = min(step, total_steps)
    return temp_start - (temp_start - temp_end) * t / total_steps

# Usage in training loop
for step in range(total_steps):
    T = temperature_decay(step, total_steps)
    action = boltzmann_exploration(q_values, temperature=T)
    # ...
```

### When to Use Boltzmann vs ε-Greedy

```
Choose ε-Greedy if:
- Simple implementation preferred
- Discrete action space
- Task has clear good/bad actions (wide Q-value spread)

Choose Boltzmann if:
- Actions have similar Q-values (nuanced exploration)
- Want to bias exploration toward promising actions
- Fine-grained control over exploration desired
```

---

## Part 3: UCB (Upper Confidence Bound)

### Theoretical Optimality

UCB is provably optimal for the multi-armed bandit problem:

```python
def ucb_action(q_values, action_counts, total_visits, c=1.0):
    """
    Select action using Upper Confidence Bound.

    UCB(a) = Q(a) + c * sqrt(ln(N) / N(a))

    Args:
        q_values: Current Q-value estimates
        action_counts: N(a) - times each action visited
        total_visits: N - total visits to state
        c: Exploration constant (usually 1.0 or sqrt(2))

    Returns:
        action: int (maximizing UCB)
    """
    # Avoid division by zero
    action_counts = np.maximum(action_counts, 1)

    # Compute exploration bonus
    exploration_bonus = c * np.sqrt(np.log(total_visits) / action_counts)

    # Upper confidence bound
    ucb = q_values + exploration_bonus

    return np.argmax(ucb)
```

### Why UCB Works

UCB balances exploitation and exploration via **optimism under uncertainty**:

- If Q(a) is high → exploit it
- If Q(a) is uncertain (rarely visited) → exploration bonus makes UCB high

```
Example: Bandit with 2 arms
- Arm A: Visited 100 times, estimated Q=2.0
- Arm B: Visited 10 times, estimated Q=1.5

UCB(A) = 2.0 + 1.0 * sqrt(ln(110) / 100) ≈ 2.0 + 0.26 = 2.26
UCB(B) = 1.5 + 1.0 * sqrt(ln(110) / 10) ≈ 1.5 + 0.82 = 2.32

Result: Try Arm B despite lower Q estimate (less certain)
```

### Critical Limitation: Doesn't Scale to Deep RL

UCB assumes **tabular setting** (small, discrete state space where you can count visits):

```python
# WORKS: Tabular Q-learning
state_action_counts = defaultdict(int)  # N(s, a)
state_counts = defaultdict(int)  # N(s)

# BREAKS in deep RL:
# With function approximation, states don't repeat exactly
# Can't count "how many times visited state X" in continuous/image observations
```

**Practical Issue:**

In image-based RL (Atari, vision), never see the same pixel image twice. State counting is impossible.

### When UCB Applies

```
Use UCB if:
✓ Discrete action space (< 100 actions)
✓ Discrete state space (< 10,000 states)
✓ Tabular Q-learning (no function approximation)
✓ Rewards come quickly (don't need long-term planning)

Examples: Simple bandits, small Gridworlds, discrete card games

DO NOT use UCB if:
✗ Using neural networks (state approximation)
✗ Continuous actions or large state space
✗ Image observations (pixel space too large)
✗ Sparse rewards (need different methods)
```

### Connection to Deep RL

For deep RL, need to estimate **uncertainty** without explicit counts:

```python
def deep_ucb_approximation(mean_q, uncertainty, c=1.0):
    """
    Approximate UCB using learned uncertainty (not action counts).

    Used in methods like:
    - Deep Ensembles: Use ensemble variance as uncertainty
    - Dropout: Use MC-dropout variance
    - Bootstrap DQN: Ensemble of Q-networks

    UCB ≈ Q(s,a) + c * uncertainty(s,a)
    """
    return mean_q + c * uncertainty
```

**Modern Approach:** Instead of counting visits, learn uncertainty through:

- **Ensemble Methods**: Train multiple Q-networks, use disagreement
- **Bayesian Methods**: Learn posterior over Q-values
- **Bootstrap DQN**: Separate Q-networks give uncertainty estimates

These adapt UCB principles to deep RL.

---

## Part 4: Curiosity-Driven Exploration (ICM)

### The Core Insight

**Prediction Error as Exploration Signal**

Agent is "curious" about states where it can't predict the next state well:

```
Intuition: If I can't predict what will happen, I probably
haven't learned about this state yet. Let me explore here!

Intrinsic Reward = ||next_state - predicted_next_state||^2
```

### Intrinsic Curiosity Module (ICM)

```python
import torch
import torch.nn as nn

class IntrinsicCuriosityModule(nn.Module):
    """
    ICM = Forward Model + Inverse Model

    Forward Model: Predicts next state from (state, action)
    - Input: current state + action taken
    - Output: predicted next state
    - Error: prediction error = surprise

    Inverse Model: Predicts action from (state, next_state)
    - Input: current state and next state
    - Output: predicted action taken
    - Purpose: Learn representation that distinguishes states
    """

    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()

        # Inverse model: (s, s') → a
        self.inverse = nn.Sequential(
            nn.Linear(2 * state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

        # Forward model: (s, a) → s'
        self.forward = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )

    def compute_intrinsic_reward(self, state, action, next_state):
        """
        Curiosity reward = prediction error of forward model.

        high_error → Unseen state → Reward exploration
        low_error → Seen state → Ignore (already learned)
        """
        # Predict next state
        predicted_next = self.forward(torch.cat([state, action], dim=-1))

        # Compute prediction error
        prediction_error = torch.norm(next_state - predicted_next, dim=-1)

        # Intrinsic reward is prediction error (exploration bonus)
        return prediction_error

    def loss(self, state, action, next_state, action_pred_logits):
        """
        Combine forward and inverse losses.

        Forward loss: Forward model prediction error
        Inverse loss: Inverse model action prediction error
        """
        # Forward loss
        predicted_next = self.forward(torch.cat([state, action], dim=-1))
        forward_loss = torch.mean((next_state - predicted_next) ** 2)

        # Inverse loss
        predicted_action = action_pred_logits
        inverse_loss = torch.mean((action - predicted_action) ** 2)

        return forward_loss + inverse_loss
```

### Why Both Forward and Inverse Models?

```
Forward model alone:
- Can predict next state without learning features
- Might just memorize (Q: Do pixels change when I do action X?)
- Doesn't necessarily learn task-relevant state representation

Inverse model:
- Forces feature learning that distinguishes states
- Can only predict action if states are well-represented
- Improves forward model's learned representation

Together: Forward + Inverse
- Better feature learning (inverse helps)
- Better prediction (forward is primary)
```

### Critical Pitfall: Random Environment Trap

```python
# WRONG: Using curiosity in stochastic environment
# Environment: Atari with pixel randomness/motion artifacts

# Agent gets reward for predicting pixel noise
# Prediction error = pixels changed randomly
# Intrinsic reward goes to the noisiest state!
# Result: Agent learns nothing about task, just explores random pixels

# CORRECT: Use RND instead (next section)
# RND uses FROZEN random network, doesn't get reward for actual noise
```

**Key Distinction:**

- ICM: Learns to predict environment (breaks if environment has noise/randomness)
- RND: Uses frozen random network (robust to environment randomness)

### Computational Cost

```python
# ICM adds significant overhead:
# - Forward model network (encoder + layers + output)
# - Inverse model network (encoder + layers + output)
# - Training both networks every step

# Overhead estimate:
# Base agent: 1 network (policy/value)
# With ICM: 3+ networks (policy + forward + inverse)
# Training time: ~2-3× longer
# Memory: ~3× larger

# When justified:
# - Sparse rewards (ICM critical)
# - Large state spaces (ICM helps)
#
# When NOT justified:
# - Dense rewards (environment signal sufficient)
# - Continuous control with simple rewards (ε-greedy enough)
```

---

## Part 5: RND (Random Network Distillation)

### The Elegant Solution

RND is simpler and more robust than ICM:

```python
class RandomNetworkDistillation(nn.Module):
    """
    RND: Intrinsic reward = prediction error of target network

    Key innovation: Target network is RANDOM and FROZEN
    (never updated)

    Two networks:
    1. Target (random, frozen): f_target(s) - fixed throughout training
    2. Predictor (trained): f_predict(s) - learns to predict target

    Intrinsic reward = ||f_target(s) - f_predict(s)||^2

    New state (s not seen) → high prediction error → reward exploration
    Seen state (s familiar) → low prediction error → ignore
    """

    def __init__(self, state_dim, embedding_dim=128):
        super().__init__()

        # Target network: random, never updates
        self.target = nn.Sequential(
            nn.Linear(state_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )

        # Predictor network: learns to mimic target
        self.predictor = nn.Sequential(
            nn.Linear(state_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )

        # Freeze target network
        for param in self.target.parameters():
            param.requires_grad = False

    def compute_intrinsic_reward(self, state, scale=1.0):
        """
        Intrinsic reward = prediction error of target network.

        Args:
            state: Current observation
            scale: Scale factor for reward (usually 0.1-1.0)

        Returns:
            Intrinsic reward (novelty signal)
        """
        with torch.no_grad():
            target_features = self.target(state)

        predicted_features = self.predictor(state)

        # L2 prediction error
        prediction_error = torch.norm(
            target_features - predicted_features,
            dim=-1,
            p=2
        )

        return scale * prediction_error

    def predictor_loss(self, state):
        """
        Loss for predictor: minimize prediction error.

        Only update predictor (target stays frozen).
        """
        with torch.no_grad():
            target_features = self.target(state)

        predicted_features = self.predictor(state)

        # MSE loss
        return torch.mean((target_features - predicted_features) ** 2)
```

### Why RND is Elegant

1. **No Environment Model**: Doesn't need to model dynamics (unlike ICM)
2. **Robust to Randomness**: Random network isn't trying to predict anything real, so environment noise doesn't fool it
3. **Simple**: Just predict random features
4. **Fast**: Train only predictor (target frozen)

### RND vs ICM Comparison

| Aspect | ICM | RND |
|--------|-----|-----|
| Networks | Forward + Inverse | Target (frozen) + Predictor |
| Learns | Environment dynamics | Random feature prediction |
| Robust to noise | No (breaks with stochastic envs) | Yes (random target immune) |
| Complexity | High (3+ networks, 2 losses) | Medium (2 networks, 1 loss) |
| Computation | 2-3× base agent | 1.5-2× base agent |
| When to use | Dense features, clean env | Sparse rewards, noisy env |

### RND Pitfall: Training Instability

```python
# WRONG: High learning rate, large reward scale
rnd_loss = rnd.predictor_loss(state)
optimizer.zero_grad()
rnd_loss.backward()
optimizer.step()  # ← high learning rate causes divergence

# CORRECT: Careful hyperparameter tuning
rnd_lr = 1e-4  # Much smaller than main agent
rnd_optimizer = Adam(rnd.predictor.parameters(), lr=rnd_lr)

# Scale intrinsic reward appropriately
intrinsic_reward = rnd.compute_intrinsic_reward(state, scale=0.01)
```

**Symptom:** RND rewards explode, agent overfits to novelty

**Fix:** Lower learning rate for RND, scale intrinsic rewards carefully

---

## Part 6: Count-Based Exploration

### State Visitation Counts

For **discrete/tabular** environments, track how many times each state visited:

```python
from collections import defaultdict

class CountBasedExploration:
    """
    Count-based exploration: encourage visiting rarely-seen states.

    Works for:
    ✓ Tabular (small discrete state space)
    ✓ Gridworlds, simple games

    Doesn't work for:
    ✗ Continuous spaces
    ✗ Image observations (never see same image twice)
    ✗ Large state spaces
    """

    def __init__(self):
        self.state_counts = defaultdict(int)

    def compute_intrinsic_reward(self, state, reward_scale=1.0):
        """
        Intrinsic reward inversely proportional to state visitation.

        intrinsic_reward = reward_scale / sqrt(N(s))

        Rarely visited states (small N) → high intrinsic reward
        Frequently visited states (large N) → low intrinsic reward
        """
        count = max(self.state_counts[state], 1)  # Avoid division by zero
        return reward_scale / np.sqrt(count)

    def update_counts(self, state):
        """Increment visitation count for state."""
        self.state_counts[state] += 1
```

### Example: Gridworld with Sparse Reward

```python
# Gridworld: 10×10 grid, reward at (9, 9), start at (0, 0)
# Without exploration: Random walking takes exponential time
# With count-based: Directed toward unexplored cells

# Pseudocode:
for episode in range(episodes):
    state = env.reset()
    for step in range(max_steps):
        # Compute exploration bonus
        intrinsic_reward = count_explorer.compute_intrinsic_reward(state)

        # Combine with task reward
        combined_reward = env_reward + lambda * intrinsic_reward

        # Q-learning with combined reward
        action = epsilon_greedy(q_values[state], epsilon)
        next_state, env_reward = env.step(action)

        q_values[state][action] += alpha * (
            combined_reward + gamma * max(q_values[next_state]) - q_values[state][action]
        )

        # Update counts
        count_explorer.update_counts(next_state)
        state = next_state
```

### Critical Limitation: Doesn't Scale

```python
# Works: Small state space
state_space_size = 100  # 10×10 grid
# Can track counts for all states

# Fails: Large/continuous state space
state_space_size = 10^18  # Image observations
# Can't track visitation counts for 10^18 unique states!
```

---

## Part 7: When Exploration is Critical

### Decision Framework

**Exploration matters when:**

1. **Sparse Rewards** (rewards rare, hard to find)
   - Examples: Montezuma's Revenge, goal-conditioned tasks, real robotics
   - No dense reward signal to guide learning
   - Agent must explore to find any reward
   - Solution: Intrinsic motivation (curiosity, RND)

2. **Large State Spaces** (too many possible states)
   - Examples: Image-based RL, continuous control
   - Random exploration covers infinitesimal fraction
   - Systematic exploration essential
   - Solution: Curiosity-driven or RND

3. **Long Horizons** (many steps before reward)
   - Examples: Multi-goal tasks, planning problems
   - Temporal credit assignment hard
   - Need to explore systematically to connect actions to delayed rewards
   - Solution: Sophisticated exploration strategy

4. **Deceptive Reward Landscape** (local optima common)
   - Examples: Multiple solutions, trade-offs
   - Easy to get stuck in suboptimal policy
   - Exploration helps escape local optima
   - Solution: Slow decay schedule, maintain exploration

### Decision Framework (Quick Check)

```
Do you have SPARSE rewards?
  YES → Use intrinsic motivation (curiosity, RND)
  NO → Continue

Is state space large (images, continuous)?
  YES → Use curiosity-driven or RND
  NO → Continue

Is exploration reasonably efficient with ε-greedy?
  YES → Use ε-greedy + appropriate decay schedule
  NO → Use curiosity-driven or RND
```

### Example: Reward Structure Analysis

```python
def analyze_reward_structure(rewards):
    """Determine if exploration strategy needed."""

    # Check sparsity
    nonzero_rewards = np.count_nonzero(rewards)
    sparsity = 1 - (nonzero_rewards / len(rewards))

    if sparsity > 0.95:
        print("SPARSE REWARDS detected")
        print("  → Use: Intrinsic motivation (RND or curiosity)")
        print("  → Why: Reward signal too rare to guide learning")

    # Check reward magnitude
    reward_std = np.std(rewards)
    reward_mean = np.mean(rewards)

    if reward_std < 0.1:
        print("WEAK/NOISY REWARDS detected")
        print("  → Use: Intrinsic motivation")
        print("  → Why: Reward signal insufficient to learn from")

    # Check reward coverage
    episode_length = len(rewards)
    if episode_length > 1000:
        print("LONG HORIZONS detected")
        print("  → Use: Strong exploration decay or intrinsic motivation")
        print("  → Why: Temporal credit assignment difficult")
```

---

## Part 8: Combining Exploration with Task Rewards

### Combining Intrinsic and Extrinsic Rewards

When using intrinsic motivation, balance with task reward:

```python
def combine_rewards(extrinsic_reward, intrinsic_reward,
                    intrinsic_scale=0.01):
    """
    Combine extrinsic (task) and intrinsic (curiosity) rewards.

    r_total = r_extrinsic + λ * r_intrinsic

    λ controls tradeoff:
    - λ = 0: Ignore intrinsic reward (no exploration)
    - λ = 0.01: Curiosity helps, task reward primary (typical)
    - λ = 0.1: Curiosity significant
    - λ = 1.0: Curiosity dominates (might ignore task)
    """
    return extrinsic_reward + intrinsic_scale * intrinsic_reward
```

### Challenges: Reward Hacking

```python
# PROBLEM: Intrinsic reward encourages anything novel
# Even if novel thing is useless for task

# Example: Atari with RND
# If game has pixel randomness, RND rewards exploring random pixels
# Instead of exploring to find coins/power-ups

# SOLUTION: Scale intrinsic reward carefully
# Make it significant but not dominant

# SOLUTION 2: Curriculum learning
# Start with high intrinsic reward (discover environment)
# Gradually reduce as agent finds reward signals
```

### Intrinsic Reward Scale Tuning

```python
# Quick tuning procedure:
for intrinsic_scale in [0.001, 0.01, 0.1, 1.0]:
    agent = RL_Agent(intrinsic_reward_scale=intrinsic_scale)
    for episode in episodes:
        performance = train_episode(agent)

    print(f"Scale={intrinsic_scale}: Performance={performance}")

# Find scale where agent learns task well AND explores
# Usually 0.01-0.1 is sweet spot
```

---

## Part 9: Common Pitfalls and Debugging

### Pitfall 1: Epsilon Decay Too Fast

**Symptom:** Agent plateaus at poor performance early in training

**Root Cause:** Epsilon decays to near-zero before agent finds good actions

```python
# WRONG: Decays in 10k steps
epsilon_final = 0.0
epsilon_decay = 0.9999  # Per-step decay
# After 10k steps: ε ≈ 0, almost no exploration left

# CORRECT: Decay over full training
total_training_steps = 1_000_000
epsilon_linear(step, total_training_steps,
               epsilon_start=1.0, epsilon_end=0.01)
```

**Diagnosis:**

- Plot epsilon over training: does it reach 0 too early?
- Check if performance improves after epsilon reaches low values

**Fix:**

- Use longer decay (more steps)
- Use higher epsilon_end (never go to pure exploitation)

### Pitfall 2: Intrinsic Reward Too Strong

**Symptom:** Agent explores forever, ignores task reward

**Root Cause:** Intrinsic reward scale too high

```python
# WRONG: Intrinsic reward dominates
r_total = r_task + 1.0 * r_intrinsic
# Agent optimizes novelty, ignores task

# CORRECT: Intrinsic reward is small bonus
r_total = r_task + 0.01 * r_intrinsic
# Task reward primary, intrinsic helps exploration
```

**Diagnosis:**

- Agent explores everywhere but doesn't collect task rewards
- Intrinsic reward signal going to seemingly useless states

**Fix:**

- Reduce intrinsic_reward_scale (try 0.01, 0.001)
- Verify agent eventually starts collecting task rewards

### Pitfall 3: ε-Greedy on Continuous Actions

**Symptom:** Exploration ineffective, agent doesn't learn

**Root Cause:** Random action in continuous space is meaningless

```python
# WRONG: ε-greedy on continuous actions
if random() < epsilon:
    action = np.random.uniform(-1, 1)  # Random in action space
else:
    action = network(state)  # Neural network action

# Random action is far from learned policy, completely unhelpful

# CORRECT: Gaussian noise on action
action = network(state)
noisy_action = action + np.random.normal(0, exploration_std)
noisy_action = np.clip(noisy_action, -1, 1)
```

**Diagnosis:**

- Continuous action space and using ε-greedy
- Agent not learning effectively

**Fix:**

- Use Gaussian noise: action + N(0, σ)
- Decay exploration_std over time (like epsilon decay)

### Pitfall 4: Forgetting to Decay Exploration

**Symptom:** Training loss decreases but policy doesn't improve, noisy behavior

**Root Cause:** Agent keeps exploring randomly instead of exploiting learned policy

```python
# WRONG: Constant exploration forever
epsilon = 0.3

# CORRECT: Decaying exploration
epsilon = epsilon_linear(step, total_steps)
```

**Diagnosis:**

- No epsilon decay schedule mentioned in code
- Agent behaves randomly even after many training steps

**Fix:**

- Add decay schedule (linear, exponential, polynomial)

### Pitfall 5: Using Exploration at Test Time

**Symptom:** Test performance worse than training, highly variable

**Root Cause:** Applying exploration strategy (ε > 0) at test time

```python
# WRONG: Test with exploration
for test_episode in test_episodes:
    action = epsilon_greedy(q_values, epsilon=0.05)  # Wrong!
    # Agent still explores at test time

# CORRECT: Test with greedy policy
for test_episode in test_episodes:
    action = np.argmax(q_values)  # Deterministic, no exploration
```

**Diagnosis:**

- Test performance has high variance
- Test performance < training performance (exploration hurts)

**Fix:**

- At test time, use greedy/deterministic policy
- No ε-greedy, no Boltzmann, no exploration noise

### Pitfall 6: RND Predictor Overfitting

**Symptom:** RND loss decreases but intrinsic rewards still large everywhere

**Root Cause:** Predictor overfits to training data, doesn't generalize to new states

```python
# WRONG: High learning rate, no regularization
rnd_optimizer = Adam(rnd.predictor.parameters(), lr=0.001)
rnd_loss.backward()
rnd_optimizer.step()

# Predictor fits perfectly to seen states but doesn't generalize

# CORRECT: Lower learning rate, regularization
rnd_optimizer = Adam(rnd.predictor.parameters(), lr=0.0001)
# Add weight decay for regularization
```

**Diagnosis:**

- RND training loss is low (close to 0)
- But intrinsic rewards still high for most states
- Suggests predictor fitted to training states but not generalizing

**Fix:**

- Reduce RND learning rate
- Add weight decay (L2 regularization)
- Use batch normalization in predictor

### Pitfall 7: Count-Based on Non-Tabular Problems

**Symptom:** Exploration ineffective, agent keeps revisiting similar states

**Root Cause:** State counting doesn't work for continuous/image spaces

```python
# WRONG: Counting state IDs in image-based RL
state = env.render(mode='rgb_array')  # 84x84 image
state_id = hash(state.tobytes())  # Different hash every time!
count_based_explorer.update_counts(state_id)

# Every frame is "new" because of slight pixel differences
# State counting broken

# CORRECT: Use RND or curiosity instead
rnd = RandomNetworkDistillation(state_dim)
# RND handles high-dimensional states
```

**Diagnosis:**

- Using count-based exploration with images/continuous observations
- Exploration not working effectively

**Fix:**

- Switch to RND or curiosity-driven methods
- Count-based only for small discrete state spaces

---

## Part 10: Red Flags and Pressure Tests

### Red Flags Checklist

- [ ] **Constant epsilon (no decay)**: Agent explores forever, can't exploit
- [ ] **Epsilon decays to zero (pure exploitation)**: Agent stuck in local optimum
- [ ] **ε-greedy on continuous actions**: Exploration unguided, learning slow
- [ ] **Intrinsic reward >> task reward**: Agent ignores task
- [ ] **No exploration specified**: Might be using default (often insufficient)
- [ ] **Using RND in random/stochastic environment**: Breaks because predicting noise
- [ ] **Count-based on images**: Can't count unique images, worthless
- [ ] **Exploration at test time**: Test performance degrades from exploration noise
- [ ] **ICM on pixel-randomness environment**: Forward model tries to predict noise
- [ ] **Ignoring sparse rewards**: Using ε-greedy only, no intrinsic motivation

### Pressure Test Scenario 1: "My Agent Stuck in Local Optimum"

**User Query:** "I trained my agent and it found a solution giving +10 reward. But I know the optimal solution is +100. Agent is stuck at +10. How do I fix it?"

**What Skill Must Provide:**

1. Diagnosis: Likely exploration problem (local optimum)
2. Solution: Increase exploration (slower decay, or intrinsic motivation)
3. Prevention: Design exploration strategy before training

**Skill Response:**

"Your agent found a local optimum (+10) and exploitation is too strong. This is a classic exploration-exploitation problem.

**Quick Fixes:**

1. Check epsilon decay: Is epsilon decaying too fast? Use slower decay schedule.
2. Check epsilon_end: Is epsilon_end = 0? Change to 0.01-0.05.
3. Add intrinsic motivation: Your environment might need curiosity-driven exploration.

**Systematic Approach:**

- If rewards are dense (frequent signals): ε-greedy with slow decay
- If rewards are sparse (rare signals): Add RND or curiosity
- If state space huge: Definitely use RND

**Example Fix:**

```
# Instead of epsilon decaying to 0.01 in 100k steps
# Decay over 1M steps with epsilon_end=0.05
epsilon = epsilon_linear(step, total_steps=1_000_000,
                         epsilon_start=1.0, epsilon_end=0.05)
```"

### Pressure Test Scenario 2: "Which Exploration for Montezuma's Revenge?"

**User Query:** "I'm training on Montezuma's Revenge (classic sparse reward benchmark). ε-Greedy isn't working (agent never finds first coin). What exploration strategy should I use?"

**What Skill Must Provide:**
1. Recognition: This is THE benchmark for intrinsic motivation
2. Solution: RND is standard, ICM is alternative
3. Implementation: Code/guidance for using RND

**Skill Response:**

"Montezuma's Revenge is the canonical example where ε-greedy fails. The first coin is at step 500+ with no reward signal. Random exploration won't find it.

**Recommended:** RND (Random Network Distillation)

Why RND:
- Robust to stochasticity (doesn't try to predict environment)
- Simpler than ICM (no environment model needed)
- Proven to work on Montezuma's Revenge

**Implementation:**
```python
rnd = RandomNetworkDistillation(state_dim=...)
lambda_intrinsic = 0.01  # Scale intrinsic reward

for step in training_steps:
    state = env.observation

    # Get intrinsic reward
    r_intrinsic = rnd.compute_intrinsic_reward(state)

    # Combine with task reward
    r_total = r_task + lambda_intrinsic * r_intrinsic

    # Train agent with combined reward
    action = agent.select_action(state)
    next_state, r_task = env.step(action)

    # Update RND predictor
    rnd_loss = rnd.predictor_loss(state)
    rnd_optimizer.zero_grad()
    rnd_loss.backward()
    rnd_optimizer.step()
```

**Alternative:** Curiosity-driven (ICM) also works if environment deterministic.

**What to tune:**

- lambda_intrinsic: Start 0.01, increase if agent doesn't explore enough
- RND learning rate: Usually 1e-4 (much smaller than main agent)"

### Pressure Test Scenario 3: "ε-Greedy Decay Schedule"

**User Query:** "I'm using ε-greedy but not sure about the decay schedule. I have 100k training steps. Should I decay epsilon linearly? Over how many steps? To what final value?"

**What Skill Must Provide:**

1. Formula: Linear, exponential, polynomial decay
2. Guidance: Typical values for different problem types
3. Tuning: How to adjust based on task

**Skill Response:**

"**Quick Answer:**

```python
total_steps = 100_000
epsilon = epsilon_linear(step, total_steps,
                         epsilon_start=1.0, epsilon_end=0.05)
```

**Reasoning:**

- `epsilon_start=1.0`: Explore fully initially (know nothing)
- `epsilon_end=0.05`: Keep 5% exploration always (helps with stochasticity)
- Linear decay: Simple, works well for most tasks

**Decision Tree:**

1. **How dense are rewards?**
   - Sparse: Use slower decay (maybe 0.1 epsilon_end)
   - Dense: Use faster decay (0.01 epsilon_end)

2. **How many steps?**
   - 100k steps: Decay over 50k-100k (half to full training)
   - 1M steps: Decay over 500k-1M
   - Rule: Decay over 50-100% of training time

3. **Which decay curve?**
   - Linear (ε_linear): Safe default
   - Exponential (ε_exponential): Faster early decay
   - Polynomial with power=2: Balanced

**Example Tuning:**

```python
# Sparse rewards: More exploration needed
epsilon = epsilon_linear(step, total_steps=100_000,
                        epsilon_start=1.0, epsilon_end=0.1)

# Very sparse rewards: Even more
epsilon = epsilon_linear(step, total_steps=100_000,
                        epsilon_start=1.0, epsilon_end=0.2)

# Dense rewards: Faster decay to exploitation
epsilon = epsilon_linear(step, total_steps=50_000,
                        epsilon_start=1.0, epsilon_end=0.01)
```"

### Pressure Test Scenario 4: "ICM vs RND vs ε-Greedy"

**User Query:** "I have sparse rewards and a deterministic environment. Should I use ε-greedy, ICM curiosity, or RND? How do I decide?"

**What Skill Must Provide:**
1. Comparison table: Pros/cons of each
2. Decision framework: Which for which situation
3. Implementation difficulty: Is it worth the complexity?

**Skill Response:**

"**Comparison:**

| Method | Complexity | Robustness | When to Use |
|--------|-----------|-----------|------------|
| ε-Greedy | Very Simple | Good on dense rewards | Dense rewards, simple env |
| ICM | Complex (2 models) | Poor on stochastic | Sparse, deterministic, learning important |
| RND | Medium (1 model) | Excellent | Sparse, any environment |

**Decision Framework:**

1. **Sparse rewards + Deterministic + Lots of learning:**
   → Try ICM first (forward model learns useful features)

2. **Sparse rewards + Any environment:**
   → Use RND (robust, simpler)

3. **Sparse rewards + Large pixel space:**
   → RND (better for high-dimensional observations)

4. **Dense rewards:**
   → Just use ε-greedy (intrinsic motivation not needed)

5. **Not sure, want safe choice:**
   → Use RND (works almost everywhere)

**Implementation Difficulty:**
- ε-Greedy: 5 lines of code
- ICM: 100+ lines (forward + inverse models, 2 losses)
- RND: 50 lines (target + predictor)

**My Recommendation:**
Start ε-greedy. If not working after tuning decay schedules, switch to RND. Only use ICM if environment is fully deterministic and you care about learning dynamics."

### Pressure Test Scenario 5: "Computational Cost of Curiosity"

**User Query:** "I want to add curiosity-driven exploration (ICM) to my agent. What's the computational overhead? Will it slow down training significantly?"

**What Skill Must Provide:**
1. Overhead estimate: Exact computation cost
2. Tradeoff: When overhead is justified
3. Alternatives: Lighter-weight options

**Skill Response:**

"**Computational Overhead Estimate:**

Base Agent:
- 1 policy/value network
- Training time: 1.0×

With ICM:
- Policy/value network + Forward model + Inverse model
- Forward model: Encoder + hidden layers + state-dim output
- Inverse model: Concatenate states + hidden + action-dim output
- Training time: ~2.5-3.0×

**Memory:**
- Base: X MB
- With ICM: ~3-4× X MB
- GPU memory often bottleneck

**When Overhead is Justified:**
- Sparse rewards (ICM critical to success)
- Large state space (intrinsic motivation helps)
- Willing to wait longer for better exploration

**When Overhead is NOT Justified:**
- Dense rewards (ε-greedy sufficient)
- Real-time training constraints
- Limited GPU memory

**Lighter Alternative:**
Use RND instead of ICM:
- ~1.5-2.0× overhead (vs 2.5-3.0× for ICM)
- Same exploration benefits
- Simpler to implement

**Scaling to Large Models:**
```python
# ICM with huge state encoders can be prohibitive
# Example: Vision transformer encoder → ICM
# That's very expensive

# RND scales better: predictor can be small
# Don't need sophisticated encoder
```

**Bottom Line:**
ICM costs 2-3× training time. If you can afford it and rewards are very sparse, worth it. Otherwise try RND or even ε-greedy with slower decay first."

---

## Part 11: Rationalization Resistance Table

| Rationalization | Reality | Counter-Guidance | Red Flag |
|-----------------|---------|------------------|----------|
| "ε-Greedy works everywhere" | Fails on sparse rewards, large spaces | Use ε-greedy for dense/small, intrinsic motivation for sparse/large | Applying ε-greedy to Montezuma's Revenge |
| "Higher epsilon is better" | High ε → too random, doesn't exploit | Use decay schedule (ε high early, low late) | Using constant ε=0.5 throughout training |
| "Decay epsilon to zero" | Agent needs residual exploration | Keep ε_end=0.01-0.1 always | Setting ε_final=0 (pure exploitation) |
| "Curiosity always helps" | Can break with stochasticity (model tries to predict noise) | Use RND for stochastic, ICM for deterministic | Agent learns to explore random noise instead of task |
| "RND is just ICM simplified" | RND is fundamentally different (frozen random vs learned model) | Understand frozen network prevents overfitting/noise | Not grasping why RND frozen network matters |
| "More intrinsic reward = faster exploration" | Too much intrinsic reward drowns out task signal | Balance with λ=0.01-0.1, tune on task performance | Agent explores forever, ignores task |
| "Count-based works anywhere" | Only works tabular (can't count unique images) | Use RND for continuous/high-dimensional spaces | Trying count-based on Atari images |
| "Boltzmann is always better than ε-greedy" | Boltzmann smoother but harder to tune | Use ε-greedy for simplicity (it works well) | Switching to Boltzmann without clear benefit |
| "Test with ε>0 for exploration" | Test should use learned policy, not explore | ε=0 or greedy policy at test time | Variable test performance from exploration |
| "Longer decay is always better" | Very slow decay wastes time in early training | Match decay to task difficulty (faster for easy, slower for hard) | Decaying over 10M steps when training only 1M |
| "Skip exploration, increase learning rate" | Learning rate is for optimization, exploration for coverage | Use both: exploration strategy + learning rate | Agent oscillates without exploration |
| "ICM is the SOTA exploration" | RND simpler and more robust | Use RND unless you need environment model | Implementing ICM when RND would suffice |

---

## Part 12: Summary and Decision Framework

### Quick Decision Tree

```
START: Need exploration strategy?

├─ Are rewards sparse? (rare reward signal)
│  ├─ YES → Need intrinsic motivation
│  │  ├─ Environment stochastic?
│  │  │  ├─ YES → RND
│  │  │  └─ NO → ICM (or RND for simplicity)
│  │  └─ Choose RND for safety
│  │
│  └─ NO → Dense rewards
│     └─ Use ε-greedy + decay schedule

├─ Is state space large? (images, continuous)
│  ├─ YES → Intrinsic motivation (RND/curiosity)
│  └─ NO → ε-greedy usually sufficient

└─ Choosing decay schedule:
   ├─ Sparse rewards → slower decay (ε_end=0.05-0.1)
   ├─ Dense rewards → faster decay (ε_end=0.01)
   └─ Default: Linear decay over 50% of training
```

### Implementation Checklist

- [ ] Define reward structure (dense vs sparse)
- [ ] Estimate state space size (discrete vs continuous)
- [ ] Choose exploration method (ε-greedy, curiosity, RND, UCB, count-based)
- [ ] Set epsilon/temperature parameters (start, end)
- [ ] Choose decay schedule (linear, exponential, polynomial)
- [ ] If using intrinsic motivation: set λ (usually 0.01)
- [ ] Use greedy policy at test time (ε=0)
- [ ] Monitor exploration vs exploitation (plot epsilon decay)
- [ ] Tune hyperparameters (decay schedule, λ) based on task performance

### Typical Configurations

**Dense Rewards, Small Action Space (e.g., simple game)**

```python
epsilon = epsilon_linear(step, total_steps=100_000,
                        epsilon_start=1.0, epsilon_end=0.01)
# Fast exploitation, low exploration needed
```

**Sparse Rewards, Discrete Actions (e.g., Atari)**

```python
rnd = RandomNetworkDistillation(...)
epsilon = epsilon_linear(step, total_steps=1_000_000,
                        epsilon_start=1.0, epsilon_end=0.05)
r_total = r_task + 0.01 * r_intrinsic
# Intrinsic motivation + slow decay
```

**Continuous Control, Sparse (e.g., Robotics)**

```python
rnd = RandomNetworkDistillation(...)
action = policy(state) + gaussian_noise(std=exploration_std)
exploration_std = exploration_std_linear(..., std_end=0.01)
r_total = r_task + 0.01 * r_intrinsic
# Gaussian noise + RND
```

---

## Key Takeaways

1. **Exploration is fundamental**: Don't ignore it. Design exploration strategy before training.

2. **Match method to problem**:
   - Dense rewards → ε-greedy
   - Sparse rewards → Intrinsic motivation (RND preferred)
   - Large state space → Intrinsic motivation

3. **Decay exploration over time**: Explore early, exploit late.

4. **Avoid common pitfalls**:
   - Don't decay to zero (ε_end > 0)
   - Don't use ε-greedy on continuous actions
   - Don't forget decay schedule
   - Don't use exploration at test time

5. **Balance intrinsic and extrinsic**: If using intrinsic rewards, don't let them dominate.

6. **RND is the safe choice**: Works for most exploration problems, simpler than ICM.

7. **Test exploration hypothesis**: Plot epsilon or intrinsic rewards, verify exploration strategy is active.

This skill is about **systematic exploration design**, not just tuning one hyperparameter.
