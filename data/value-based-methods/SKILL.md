---
name: value-based-methods
description: Master DQN, Double DQN, Dueling DQN, Rainbow - value-based methods for discrete actions
---

# Value-Based Methods

## When to Use This Skill

Invoke this skill when you encounter:

- **Algorithm Selection**: "Should I use DQN or policy gradient for my problem?"
- **DQN Implementation**: User implementing DQN and needs guidance on architecture
- **Training Issues**: "DQN is diverging", "Q-values too high", "slow to learn"
- **Variant Questions**: "What's Double DQN?", "Should I use Dueling?", "Is Rainbow worth it?"
- **Discrete Action RL**: User has discrete action space and implementing value method
- **Hyperparameter Tuning**: Debugging learning rates, replay buffer size, network architecture
- **Implementation Bugs**: Target network missing, frame stacking wrong, reward scaling issues
- **Custom Environments**: Designing states, rewards, action spaces for DQN

**This skill provides practical implementation guidance for discrete action RL.**

Do NOT use this skill for:

- Continuous action spaces (route to actor-critic-methods)
- Policy gradients (route to policy-gradient-methods)
- Model-based RL (route to model-based-rl)
- Offline RL (route to offline-rl-methods)
- Theory foundations (route to rl-foundations)

---

## Core Principle

**Value-based methods solve discrete action RL by learning Q(s,a) = expected return from taking action a in state s, then acting greedily. They're powerful for discrete spaces but require careful implementation to avoid instability.**

Key insight: Value methods assume you can enumerate and compare all action values. This breaks down with continuous actions (infinite actions to compare). Use them for:

- Games (Atari, Chess)
- Discrete control (robot navigation, discrete movement)
- Dialog systems (discrete utterances)
- Combinatorial optimization

**Do not use for**:

- Continuous control (robot arm angles, vehicle acceleration)
- Stochastic policies required (multi-agent, exploration in deterministic policy)
- Exploration of large action space (too slow to learn all actions)

---

## Part 1: Q-Learning Foundation

### From TD Learning to Q-Learning

You understand TD learning from rl-foundations. Q-learning extends it to **action-values**.

**TD(0) for V(s)**:

```
V[s] ← V[s] + α(r + γV[s'] - V[s])
```

**Q-Learning for Q(s,a)**:

```
Q[s,a] ← Q[s,a] + α(r + γ max_a' Q[s',a'] - Q[s,a])
```

**Key difference**: Q-learning has **max over next actions** (off-policy).

### Off-Policy Learning

Q-learning learns the **optimal policy π*(a|s) = argmax_a Q(s,a)** regardless of exploration policy.

**Example: Cliff Walking**

```
Agent follows epsilon-greedy (explores 10% random)
But Q-learning learns: "Take safe path away from cliff" (optimal)
NOT: "Walk along cliff edge" (what exploring policy does sometimes)

Q-learning separates:
- Behavior policy: ε-greedy (for exploration)
- Target policy: greedy (what we're learning toward)
```

**Why This Matters**: Off-policy learning is sample-efficient (can learn from any exploration strategy). On-policy methods like SARSA would learn the exploration noise into policy.

### Convergence Guarantee

**Theorem**: Q-learning converges to Q*(s,a) if:

1. All state-action pairs visited infinitely often
2. Learning rate α(t) → 0 (e.g., α = 1/N(s,a))
3. Sufficiently small ε (exploration not zero)

**Practical**: Use ε-decay schedule that ensures eventual convergence.

```python
epsilon = max(epsilon_min, epsilon * decay_rate)
# Start: ε=1.0, decay to ε=0.01
# Ensures: all actions eventually tried, then exploitation takes over
```

### Q-Learning Pitfall #1: Small State Spaces Only

**Scenario**: User implements tabular Q-learning for Atari.

**Problem**:

```
Atari image: 210×160 RGB = 20,160 pixels
Possible states: 256^20160 (astronomical)
Tabular Q-learning: impossible
```

**Solution**: Use function approximation (neural networks) → Deep Q-Networks

**Red Flag**: Tabular Q-learning works only for small state spaces (<10,000 unique states).

---

## Part 2: Deep Q-Networks (DQN)

### What DQN Adds to Q-Learning

DQN = Q-learning + neural network + **two critical stability mechanisms**:

1. **Experience Replay**: Break temporal correlation
2. **Target Network**: Prevent moving target problem

### Mechanism 1: Experience Replay

**Problem without replay**:

```python
# Naive approach (WRONG)
state = env.reset()
for t in range(1000):
    action = epsilon_greedy(state)
    next_state, reward = env.step(action)

    # Update Q from this single transition
    Q(state, action) += α(reward + γ max Q(next_state) - Q(state, action))
    state = next_state
```

**Why this fails**:

- Consecutive transitions are **highly correlated** (state_t and state_{t+1} very similar)
- Neural network gradient updates are unstable with correlated data
- Network overfits to recent trajectory

**Experience Replay Solution**:

```python
# Collect experiences in buffer
replay_buffer = []

for episode in range(num_episodes):
    state = env.reset()
    for t in range(max_steps):
        action = epsilon_greedy(state)
        next_state, reward = env.step(action)

        # Store experience (not learn yet)
        replay_buffer.append((state, action, reward, next_state, done))

        # Sample random batch and learn
        if len(replay_buffer) > batch_size:
            batch = random.sample(replay_buffer, batch_size)
            for (s, a, r, s_next, done) in batch:
                if done:
                    target = r
                else:
                    target = r + gamma * max(Q(s_next))
                loss = (Q(s,a) - target)^2

            # Update network weights
            optimizer.step(loss)

        state = next_state
```

**Why this works**:

1. **Breaks correlation**: Random sampling decorrelates gradient updates
2. **Sample efficiency**: Reuse old experiences (learn more from same env interactions)
3. **Stability**: Averaged gradients are smoother

### Mechanism 2: Target Network

**Problem without target network**:

```python
# Moving target problem (WRONG)
loss = (Q(s,a) - [r + γ max Q(s_next, a_next)])^2
       #     ^^^^             ^^^^
       # Same network computing both target and prediction
```

**Issue**: Network updates move both the prediction AND the target, creating instability.

**Analogy**: Trying to hit a moving target that moves whenever you aim.

**Target Network Solution**:

```python
# Separate networks
main_network = create_network()      # Learning network
target_network = create_network()    # Stable target (frozen)

# Training loop
loss = (main_network(s,a) - [r + γ max target_network(s_next)])^2
                                  ^^^^^^^^
                    Target network doesn't update every step

# Periodically synchronize
if t % update_frequency == 0:
    target_network = copy(main_network)  # Freeze for N steps
```

**Why this works**:

1. **Stability**: Target doesn't move as much (frozen for many steps)
2. **Bellman consistency**: Gives network time to learn, then adjusts target
3. **Convergence**: Bootstrapping no longer destabilized by moving target

### DQN Architecture Pattern

```python
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, input_size, num_actions):
        super().__init__()
        # For Atari: CNN backbone
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)  # Frame stack: 4 frames
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        # Flatten and FC layers
        self.fc1 = nn.Linear(64*7*7, 512)  # After convolutions
        self.fc_value = nn.Linear(512, 1)  # For dueling: value stream
        self.fc_actions = nn.Linear(512, num_actions)  # For dueling: advantage stream

    def forward(self, x):
        # x shape: (batch, 4, 84, 84) for Atari
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.flatten(start_dim=1)
        x = torch.relu(self.fc1(x))

        # For basic DQN: just action values
        q_values = self.fc_actions(x)
        return q_values
```

### Hyperparameter Guidance

| Parameter | Value Range | Effect | Guidance |
|-----------|------------|--------|----------|
| Replay buffer size | 10k-1M | Memory, sample diversity | Start 100k, increase for slow learning |
| Batch size | 32-256 | Stability vs memory | 32-64 common; larger = more stable |
| Learning rate α | 0.0001-0.001 | Convergence speed | Start 0.0001, increase if too slow |
| Target update freq | 1k-10k steps | Stability | Update every 1000-5000 steps |
| ε initial | 0.5-1.0 | Exploration | Start 1.0 (random) |
| ε final | 0.01-0.05 | Late exploitation | 0.01-0.05 typical |
| ε decay | 10k-1M steps | Exploration → Exploitation | Tune to problem (larger env → longer decay) |

### DQN Pitfall #1: Missing Target Network

**Symptom**: "DQN loss explodes immediately, Q-values diverge to ±infinity"

**Root cause**: No target network (or target updates too frequently)

```python
# WRONG - target network updates every step
loss = (Q(s,a) - [r + γ max Q(s_next)])^2  # Both from same network

# CORRECT - target network frozen for steps
loss = (Q_main(s,a) - [r + γ max Q_target(s_next)])^2
# Update target: if step % 1000 == 0: Q_target = copy(Q_main)
```

**Fix**: Verify target network update frequency (1000-5000 steps typical).

### DQN Pitfall #2: Replay Buffer Too Small

**Symptom**: "Sample efficiency very poor, agent takes millions of steps to learn"

**Root cause**: Small replay buffer = replay many recent correlated experiences

```python
# WRONG
replay_buffer_size = 10_000
# After 10k steps, only seeing recent experience (no diversity)

# CORRECT
replay_buffer_size = 100_000 or 1_000_000
# See diverse experiences from long history
```

**Rule of Thumb**: Replay buffer ≥ 10 × episode length (more is usually better)

**Memory vs Sample Efficiency Tradeoff**:

- 10k buffer: Low memory, high correlation (bad)
- 100k buffer: Moderate memory, good diversity (usually sufficient)
- 1M buffer: High memory, excellent diversity (overkill unless long episodes)

### DQN Pitfall #3: No Frame Stacking

**Symptom**: "Learning very slow or doesn't converge"

**Root cause**: Single frame doesn't show velocity (violates Markov property)

```python
# WRONG - single frame
state = current_frame  # No velocity information
# Network cannot infer: is ball moving left or right?

# CORRECT - stack frames
state = np.stack([frame_t, frame_{t-1}, frame_{t-2}, frame_{t-3}])
# Velocity: difference between consecutive frames
```

**Implementation**:

```python
from collections import deque

class FrameBuffer:
    def __init__(self, num_frames=4):
        self.buffer = deque(maxlen=num_frames)

    def add_frame(self, frame):
        self.buffer.append(frame)

    def get_state(self):
        return np.stack(list(self.buffer))  # (4, 84, 84)
```

### DQN Pitfall #4: Reward Clipping Wrong

**Symptom**: "Training unstable" or "Learned policy much worse than Q-values suggest"

**Context**: Atari papers clip rewards to {-1, 0, +1} for stability.

**Misunderstanding**: Clipping destroys reward information.

```python
# WRONG - unthinking clip
reward = np.clip(reward, -1, 1)  # All rewards become -1,0,+1
# In custom env with rewards in [-100, 1000], loses critical information

# CORRECT - Normalize instead
reward = (reward - reward_mean) / reward_std
# Preserves differences, stabilizes scale
```

**When to clip**: Only if rewards are naturally in {-1, 0, +1} (like Atari).

**When to normalize**: Custom environments with arbitrary scales.

---

## Part 3: Double DQN

### The Overestimation Bias Problem

**Max operator bias**: In stochastic environments, max over noisy estimates is biased upward.

**Example**:

```
True Q*(s,a) values: [10.0, 5.0, 8.0]

Due to noise, estimates: [11.0, 4.0, 9.0]
                            ↑
                        True Q = 10, estimate = 11

Standard DQN takes max: max(Q_estimates) = 11
But true Q*(s,best_action) = 10

Systematic overestimation! Agent thinks actions better than they are.
```

**Consequence**:

- Inflated Q-values during training
- Learned policy (greedy) performs worse than Q-values suggest
- Especially bad early in training when estimates very noisy

### Double DQN Solution

**Insight**: Use one network to **select** best action, another to **evaluate** it.

```python
# Standard DQN (overestimates)
target = r + γ max_a Q_target(s_next, a)
         #        ^^^^
         # Both selecting and evaluating with same network

# Double DQN (unbiased)
best_action = argmax_a Q_main(s_next, a)      # Select with main network
target = r + γ Q_target(s_next, best_action)  # Evaluate with target network
```

**Why it works**:

- Decouples selection and evaluation
- Removes systematic bias
- Unbiased estimator of true Q*

### Implementation

```python
class DoubleDQN(DQNAgent):
    def compute_loss(self, batch):
        states, actions, rewards, next_states, dones = batch

        # Main network Q-values for current state
        q_values = self.main_network(states)
        q_values_current = q_values.gather(1, actions)

        # Double DQN: select action with main network
        next_q_main = self.main_network(next_states)
        best_actions = next_q_main.argmax(1, keepdim=True)

        # Evaluate with target network
        next_q_target = self.target_network(next_states)
        max_next_q = next_q_target.gather(1, best_actions).detach()

        # TD target (handles done flag)
        targets = rewards + (1 - dones) * self.gamma * max_next_q

        loss = F.smooth_l1_loss(q_values_current, targets)
        return loss
```

### When to Use Double DQN

**Use Double DQN if**:

- Training a medium-complexity task (Atari)
- Suspicious that Q-values are too optimistic
- Want slightly better sample efficiency

**Standard DQN is OK if**:

- Small action space (less overestimation)
- Training is otherwise stable
- Sample efficiency not critical

**Takeaway**: Double DQN is strictly better, minimal cost, use it.

---

## Part 4: Dueling DQN

### Dueling Architecture: Separating Value and Advantage

**Insight**: Q(s,a) = V(s) + A(s,a) where:

- **V(s)**: How good is this state? (independent of action)
- **A(s,a)**: How much better is action a than average? (action-specific advantage)

**Why separate**:

1. **Better feature learning**: Network learns state features independently from action value
2. **Stabilization**: Value stream sees many states (more gradient signal)
3. **Generalization**: Advantage stream learns which actions matter

**Example**:

```
Atari Breakout:
V(s) = "Ball in good position, paddle ready" (state value)
A(s,LEFT) = -2 (moving left here hurts)
A(s,RIGHT) = +3 (moving right here helps)
A(s,NOOP) = 0 (staying still is neutral)

Q(s,LEFT) = V + A = 5 + (-2) = 3
Q(s,RIGHT) = V + A = 5 + 3 = 8  ← Best action
Q(s,NOOP) = V + A = 5 + 0 = 5
```

### Architecture

```python
class DuelingDQN(nn.Module):
    def __init__(self, input_size, num_actions):
        super().__init__()

        # Shared feature backbone
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.fc = nn.Linear(64*7*7, 512)

        # Value stream (single output)
        self.value_fc = nn.Linear(512, 256)
        self.value = nn.Linear(256, 1)

        # Advantage stream (num_actions outputs)
        self.advantage_fc = nn.Linear(512, 256)
        self.advantage = nn.Linear(256, num_actions)

    def forward(self, x):
        # Shared backbone
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.flatten(start_dim=1)
        x = torch.relu(self.fc(x))

        # Value stream
        v = torch.relu(self.value_fc(x))
        v = self.value(v)

        # Advantage stream
        a = torch.relu(self.advantage_fc(x))
        a = self.advantage(a)

        # Combine: Q = V + (A - mean(A))
        # Subtract mean(A) for normalization (prevents instability)
        q = v + (a - a.mean(dim=1, keepdim=True))
        return q
```

### Why Subtract Mean of Advantages?

```python
# Without mean subtraction
q = v + a
# Problem: V and A not separately identifiable
# V could be 100 + A = -90 or V = 50 + A = -40 (same Q)

# With mean subtraction
q = v + (a - mean(a))
# Mean advantage = 0 on average
# Forces: V learns state value, A learns relative advantage
# More stable training
```

### When to Use Dueling DQN

**Use Dueling if**:

- Training complex environments (Atari)
- Want better feature learning
- Training is unstable (helps stabilization)

**Standard DQN is OK if**:

- Simple environments
- Computational budget tight

**Takeaway**: Dueling is strictly better for neural network learning, minimal cost, use it.

---

## Part 5: Prioritized Experience Replay

### Problem with Uniform Sampling

**Issue**: All transitions equally likely to be sampled.

```python
# Uniform sampling
batch = random.sample(replay_buffer, batch_size)
# Includes: boring transitions, important transitions, rare transitions
# All mixed together with equal weight
```

**Problem**:

- Wasted learning on transitions already understood
- Rare important transitions sampled rarely
- Sample inefficiency

**Example**:

```
Atari agent learns mostly: "Move paddle left-right in routine positions"
Rarely: "What happens when ball is in corner?" (rare, important)

Uniform replay: 95% learning about paddle, 5% about corners
Should be: More focus on corners (rarer, more surprising)
```

### Prioritized Experience Replay Solution

**Insight**: Sample transitions proportional to **TD error** (surprise).

```python
# Compute TD error (surprise)
td_error = |r + γ max Q(s_next) - Q(s,a)|
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#           How wrong was our prediction?

# Probability ∝ TD error^α
# High error transitions sampled more
batch = sample_proportional_to_priority(replay_buffer, priorities)
```

### Implementation

```python
import numpy as np

class PrioritizedReplayBuffer:
    def __init__(self, size, alpha=0.6):
        self.buffer = []
        self.priorities = []
        self.size = size
        self.alpha = alpha  # How much to prioritize (0=uniform, 1=full priority)
        self.epsilon = 1e-6  # Small value to avoid zero priority

    def add(self, experience):
        # New experiences get max priority (important!)
        max_priority = np.max(self.priorities) if self.priorities else 1.0

        if len(self.buffer) < self.size:
            self.buffer.append(experience)
            self.priorities.append(max_priority)
        else:
            # Replace oldest if full
            self.buffer[len(self.buffer) % self.size] = experience
            self.priorities[len(self.priorities) % self.size] = max_priority

    def sample(self, batch_size):
        # Compute sampling probabilities
        priorities = np.array(self.priorities) ** self.alpha
        priorities = priorities / np.sum(priorities)

        # Sample indices
        indices = np.random.choice(len(self.buffer), batch_size, p=priorities)
        batch = [self.buffer[i] for i in indices]

        # Importance sampling weights (correct for bias from prioritized sampling)
        weights = (1 / (len(self.buffer) * priorities[indices])) ** (1/3)  # β=1/3
        weights = weights / np.max(weights)  # Normalize

        return batch, indices, weights

    def update_priorities(self, indices, td_errors):
        # Update priorities based on new TD errors
        for idx, td_error in zip(indices, td_errors):
            self.priorities[idx] = (np.abs(td_error) + self.epsilon) ** self.alpha
```

### Importance Sampling Weights

**Problem**: Prioritized sampling introduces bias (samples important transitions more).

**Solution**: Reweight gradients by inverse probability.

```python
# Uniform sampling: each transition contributes equally
loss = mean((r + γ max Q(s_next) - Q(s,a))^2)

# Prioritized sampling: bias toward high TD error
# Correct with importance weight (large TD error → small weight)
loss = mean(weights * (r + γ max Q(s_next) - Q(s,a))^2)
#            ^^^^^^^
#      Importance sampling correction

# weights ∝ 1/priority (inverse)
```

### When to Use Prioritized Replay

**Use if**:

- Training large environments (Atari)
- Sample efficiency critical
- Have computational budget for priority updates

**Use standard uniform if**:

- Small environments
- Computational budget tight
- Standard training is working fine

**Note**: Adds complexity (priority updates), minimal empirical gain in many cases.

---

## Part 6: Rainbow DQN

### Combining All Improvements

**Rainbow** = Double DQN + Dueling DQN + Prioritized Replay + 3 more innovations:

1. **Double DQN**: Reduce overestimation bias
2. **Dueling DQN**: Separate value and advantage
3. **Prioritized Replay**: Sample important transitions
4. **Noisy Networks**: Exploration through network parameters
5. **Distributional RL**: Learn Q distribution not just mean
6. **Multi-step Returns**: n-step TD learning instead of 1-step

### When to Use Rainbow

**Use Rainbow if**:

- Need state-of-the-art Atari performance
- Have weeks of compute for tuning
- Paper requires it

**Use Double + Dueling DQN if**:

- Standard DQN training unstable
- Want good performance with less tuning
- Typical development

**Use Basic DQN if**:

- Learning the method
- Sample efficiency not critical
- Simple environments

**Lesson**: Understand components separately before combining.

```
Learning progression:
1. Q-learning (understand basics)
2. Basic DQN (add neural networks)
3. Double DQN (fix overestimation)
4. Dueling DQN (improve architecture)
5. Add prioritized replay (sample efficiency)
6. Rainbow (combine all)
```

---

## Part 7: Common Bugs and Debugging

### Bug #1: Training Divergence (Q-values explode)

**Diagnosis Tree**:

1. **Check target network**:

   ```python
   # WRONG - updating every step
   loss = (Q_main(s,a) - [r + γ max Q_main(s_next)])^2
   # FIX - use separate target network
   loss = (Q_main(s,a) - [r + γ max Q_target(s_next)])^2
   ```

2. **Check learning rate**:

   ```python
   # WRONG - too high
   optimizer = torch.optim.Adam(network.parameters(), lr=0.1)
   # FIX - reduce learning rate
   optimizer = torch.optim.Adam(network.parameters(), lr=0.0001)
   ```

3. **Check reward scale**:

   ```python
   # WRONG - rewards too large
   reward = 1000 * indicator  # Values explode
   # FIX - normalize
   reward = 10 * indicator
   # Or: reward = (reward - reward_mean) / reward_std
   ```

4. **Check replay buffer**:

   ```python
   # WRONG - too small
   replay_buffer_size = 1000
   # FIX - increase size
   replay_buffer_size = 100_000
   ```

### Bug #2: Poor Sample Efficiency (Slow Learning)

**Diagnosis Tree**:

1. **Check replay buffer size**:

   ```python
   # Too small → high correlation
   if len(replay_buffer) < 100_000:
       print("WARNING: Replay buffer too small for Atari")
   ```

2. **Check target network update frequency**:

   ```python
   # Too frequent → moving target
   # Too infrequent → slow target adjustment
   # Good: every 1000-5000 steps
   if update_frequency > 10_000:
       print("Target updates too infrequent")
   ```

3. **Check batch size**:

   ```python
   # Too small → noisy gradients
   # Too large → slow training
   # Good: 32-64
   if batch_size < 16 or batch_size > 256:
       print("Consider adjusting batch size")
   ```

4. **Check epsilon decay**:

   ```python
   # Decaying too fast → premature exploitation
   # Decaying too slow → wastes steps exploring
   # Typical: decay over 10% of total steps
   if decay_steps < total_steps * 0.05:
       print("Epsilon decays too quickly")
   ```

### Bug #3: Q-Values Too Optimistic (Learned Policy << Training Q)

**Diagnosis**:

**Red Flag**: Policy performance much worse than max Q-value during training.

```python
# Symptom
max_q_value = 100.0
actual_episode_return = 5.0
# 20x gap suggests overestimation

# Solutions (try in order)
1. Use Double DQN (reduces overestimation)
2. Reduce learning rate (slower updates → less optimistic)
3. Increase target network update frequency (more stable target)
4. Check reward function (might be wrong)
```

### Bug #4: Frame Stacking Wrong

**Symptoms**:

- Very slow learning despite "correct" implementation
- Network can't learn velocity-dependent behaviors

**Diagnosis**:

```python
# WRONG - single frame
state_shape = (84, 84, 3)
# Network sees only position, not velocity

# CORRECT - stack 4 frames
state_shape = (84, 84, 4)
# Last 4 frames show motion

# Check frame stacking implementation
frame_stack = deque(maxlen=4)
for frame in frames:
    frame_stack.append(frame)
    state = np.stack(list(frame_stack))  # (4, 84, 84)
```

### Bug #5: Network Architecture Mismatch

**Symptoms**:

- CNN on non-image input (or vice versa)
- Output layer wrong number of actions
- Input preprocessing wrong

**Diagnosis**:

```python
# Image input → use CNN
if input_type == 'image':
    network = CNN(num_actions)

# Vector input → use FC
elif input_type == 'vector':
    network = FullyConnected(input_size, num_actions)

# Output layer MUST have num_actions outputs
assert network.output_size == num_actions
```

---

## Part 8: Hyperparameter Tuning

### Learning Rate

**Too high** (α > 0.001):

- Divergence, unstable training
- Q-values explode

**Too low** (α < 0.00001):

- Very slow learning
- May not converge in reasonable time

**Start**: α = 0.0001, adjust if needed

```python
# Adaptive strategy
if max_q_value > 1000:
    print("Reduce learning rate")
    alpha = alpha / 2
if learning_curve_flat:
    print("Increase learning rate")
    alpha = alpha * 1.1
```

### Replay Buffer Size

**Too small** (< 10k for Atari):

- High correlation in gradients
- Slow learning, poor sample efficiency

**Too large** (> 10M):

- Excessive memory
- Stale experiences dominate
- Diminishing returns

**Rule of thumb**: 10 × episode length

```python
episode_length = 1000  # typical
ideal_buffer = 100_000  # 10 × typical Atari episode

# Can increase if GPU memory available and learning slow
if learning_slow:
    buffer_size = 500_000  # More diversity
```

### Epsilon Decay

**Too fast** (decay in 10k steps):

- Agent exploits before learning
- Suboptimal policy

**Too slow** (decay in 1M steps):

- Wasted exploration time
- Slow performance improvement

**Rule**: Decay over ~10% of total training steps

```python
total_steps = 1_000_000
epsilon_decay_steps = total_steps * 0.1  # 100k steps
epsilon = max(epsilon_min, epsilon * (epsilon_decay_steps / current_step))
```

### Target Network Update Frequency

**Too frequent** (every 100 steps):

- Target still moves rapidly
- Less stabilization benefit

**Too infrequent** (every 100k steps):

- Network drifts far from target
- Large jumps in learning

**Sweet spot**: Every 1k-5k steps (1000 typical)

```python
update_frequency = 1000  # steps between target updates
if update_frequency < 500:
    print("Target updates might be too frequent")
if update_frequency > 10_000:
    print("Target updates might be too infrequent")
```

### Reward Scaling

**No scaling** (raw rewards vary wildly):

- Learning rate effects vary by task
- Convergence issues

**Clipping** (clip to {-1, 0, +1}):

- Good for Atari, loses information in custom envs

**Normalization** (zero-mean, unit variance):

- General solution
- Preserves reward differences

```python
# Track running statistics
running_mean = 0.0
running_var = 1.0

def normalize_reward(reward):
    global running_mean, running_var
    running_mean = 0.99 * running_mean + 0.01 * reward
    running_var = 0.99 * running_var + 0.01 * (reward - running_mean)**2
    return (reward - running_mean) / np.sqrt(running_var + 1e-8)
```

---

## Part 9: When to Use Each Method

### DQN Selection Matrix

| Situation | Method | Why |
|-----------|--------|-----|
| Learning method | Basic DQN | Understand target network, replay buffer |
| Medium task | Double DQN | Fix overestimation, minimal overhead |
| Complex task | Double + Dueling | Better architecture + bias reduction |
| Sample critical | Add Prioritized | Focus on important transitions |
| State-of-art | Rainbow | Best Atari performance |
| Simple Atari | DQN | Sufficient, faster to debug |
| Non-Atari discrete | DQN/Double | Adapt architecture to input type |

### Action Space Check

**Before implementing DQN, ask**:

```python
if action_space == 'continuous':
    print("ERROR: Use actor-critic or policy gradient")
    print("Value methods only for discrete actions")
    redirect_to_actor_critic_methods()

elif action_space == 'discrete' and len(actions) <= 100:
    print("✓ DQN appropriate")

elif action_space == 'discrete' and len(actions) > 1000:
    print("⚠ Large action space, consider policy gradient")
    print("Or: hierarchical RL, action abstraction")
```

---

## Part 10: Red Flags Checklist

When you see these, suspect bugs:

- [ ] **Single frame input**: No velocity info, add frame stacking
- [ ] **No target network**: Divergence expected, add it
- [ ] **Small replay buffer** (< 10k): Poor efficiency, increase
- [ ] **High learning rate** (> 0.001): Instability likely, decrease
- [ ] **No frame preprocessing**: Raw image pixels, normalize to [0,1]
- [ ] **Updating target every step**: Moving target problem, freeze it
- [ ] **No exploration decay**: Explores forever, add epsilon decay
- [ ] **Continuous actions**: Wrong method, use actor-critic
- [ ] **Very large rewards** (> 100): Scaling issues, normalize
- [ ] **Only one environment**: Bias high, use frame skipping or multiple envs
- [ ] **Immediate best performance**: Overfitting to initial conditions, likely divergence later
- [ ] **Q-values >> rewards**: Overestimation, try Double DQN
- [ ] **All Q-values zero**: Network not learning, check learning rate
- [ ] **Training loss increasing**: Learning rate too high, divergence

---

## Part 11: Pitfall Rationalization

| Rationalization | Reality | Counter-Guidance | Red Flag |
|-----------------|---------|------------------|----------|
| "I'll skip target network, save memory" | Causes instability/divergence | Target network critical, minimal memory cost | "Target network optional" |
| "DQN works for continuous actions" | Breaks fundamental assumption (enumerate all actions) | Value methods discrete-only, use SAC/TD3 for continuous | Continuous action DQN attempt |
| "Uniform replay is fine" | Wastes learning on boring transitions | Prioritized replay better, but uniform adequate for many tasks | Always recommending prioritized |
| "I'll use tiny replay buffer, it's faster" | High correlation, poor learning | 100k+ buffer typical, speed tradeoff acceptable | Buffer < 10k for Atari |
| "Frame stacking unnecessary, CNN sees motion" | Single frame Markov-violating | Frame stacking required for velocity from pixels | Single frame policy |
| "Rainbow is just DQN + tricks" | Missing that components solve specific problems | Each component fixes identified issue (overestimation, architecture, sampling) | Jumping to Rainbow without understanding |
| "Clip rewards, I saw it in a paper" | Clips away important reward information | Only clip for {-1,0,+1} Atari-style, normalize otherwise | Blind reward clipping |
| "Larger network will learn faster" | Overfitting, slower gradients, memory issues | Standard architecture (32-64-64 CNN) works, don't over-engineer | Unreasonably large networks |
| "Policy gradient would be simpler here" | Value methods discrete-only right choice | Know when each applies (discrete → value, continuous → policy) | Wrong method choice for action space |
| "Epsilon decay is a hyperparameter like any other" | decay schedule should match task complexity | Tune decay to problem (game length), not arbitrary | Epsilon decay without reasoning |

---

## Part 12: Pressure Test Scenarios

### Scenario 1: Continuous Action Space

**User**: "I have a robot with continuous action space (joint angles in ℝ^7). Can I use DQN?"

**Wrong Response**: "Sure, discretize the actions"
(Combinatorial explosion, inefficient)

**Correct Response**: "No, value methods are discrete-only. Use actor-critic (SAC) or policy gradient (PPO). They handle continuous actions naturally. Discretization would create 7-dimensional action space explosion (e.g., 10 values per joint = 10^7 actions)."

---

### Scenario 2: Training Unstable

**User**: "My DQN is diverging immediately, loss explodes. Implementation looks right. What's wrong?"

**Systematic Debug**:

```
1. Check target network
   - Print: "Is target_network separate from main_network?"
   - Likely cause: updating together

2. Check learning rate
   - Print: "Learning rate = ?"
   - If > 0.001, reduce

3. Check reward scale
   - Print: "max(rewards) = ?"
   - If > 100, normalize

4. Check initial Q-values
   - Print: "mean(Q-values) = ?"
   - Should start near zero
```

**Answer**: Target network most likely culprit. Verify separate networks with proper update frequency.

---

### Scenario 3: Rainbow vs Double DQN

**User**: "Should I implement Rainbow or just Double DQN? Is Rainbow worth the complexity?"

**Guidance**:

```
Double DQN:
+ Fixes overestimation bias
+ Simple to implement
+ 90% of Rainbow benefits in many cases
- Missing other optimizations

Rainbow:
+ Best Atari performance
+ State-of-the-art
- Complex (6 components)
- Harder to debug
- More hyperparameters

Recommendation:
Start: Double DQN
If unstable: Add Dueling
If slow: Add Prioritized
Only go to Rainbow: If need SotA and have time
```

---

### Scenario 4: Frame Stacking Issue

**User**: "My agent trains on Atari but learning is slow. How many frames should I stack?"

**Diagnosis**:

```python
# Check if frame stacking implemented
if state.shape != (4, 84, 84):
    print("ERROR: Not using frame stacking")
    print("Single frame (1, 84, 84) violates Markov property")
    print("Add frame stacking: stack last 4 frames")

# Frame count
4 frames: Standard (shows ~80ms at 50fps = ~4 frames)
3 frames: OK, slightly less velocity info
2 frames: Minimum, just barely Markovian
1 frame: WRONG, not Markovian
8+ frames: Too many, outdated states in stack
```

---

### Scenario 5: Hyperparameter Tuning

**User**: "I've tuned learning rate, buffer size, epsilon. What else affects performance?"

**Guidance**:

```
Priority 1 (Critical):
- Target network update frequency (1000-5000 steps)
- Replay buffer size (100k+ typical)
- Frame stacking (4 frames)

Priority 2 (Important):
- Learning rate (0.0001-0.0005)
- Epsilon decay schedule (over ~10% of steps)
- Batch size (32-64)

Priority 3 (Nice to have):
- Network architecture (32-64-64 CNN standard)
- Reward normalization (helps but not required)
- Double/Dueling DQN (improvements, not essentials)

Start with Priority 1, only adjust Priority 2-3 if unstable.
```

---

## Part 13: When to Route Elsewhere

### Route to rl-foundations if

- User confused about Bellman equations
- Unclear on value function definition
- Needs theory behind Q-learning convergence

### Route to actor-critic-methods if

- Continuous action space
- Need deterministic policy gradients
- Stochastic policy required

### Route to policy-gradient-methods if

- Large discrete action space (> 1000 actions)
- Need policy regularization
- Exploration by stochasticity useful

### Route to offline-rl-methods if

- No environment access (batch learning)
- Learning from logged data only

### Route to rl-debugging if

- General training issues
- Need systematic debugging methodology
- Credit assignment problems

### Route to reward-shaping if

- Sparse rewards
- Reward design affecting learning
- Potential-based shaping questions

---

## Summary

**You now understand**:

1. **Q-Learning**: TD learning for action values, off-policy convergence guarantee
2. **DQN**: Add neural networks + experience replay + target network for stability
3. **Stability Mechanisms**:
   - Replay buffer: Break correlation
   - Target network: Prevent moving target problem
4. **Common Variants**:
   - Double DQN: Fix overestimation bias
   - Dueling DQN: Separate value and advantage
   - Prioritized Replay: Focus on important transitions
   - Rainbow: Combine improvements
5. **When to Use**: Discrete action spaces only, not continuous
6. **Common Bugs**: Divergence, poor efficiency, overoptimism, frame issues
7. **Hyperparameter Tuning**: Buffer size, learning rate, epsilon decay, target frequency
8. **Debugging Strategy**: Systematic diagnosis (target network → learning rate → reward scale)

**Key Takeaways**:

- Value methods are for **discrete actions ONLY**
- DQN requires **target network and experience replay**
- **Frame stacking** needed for video inputs (Markov property)
- **Double DQN** fixes overestimation, use it
- **Start simple**, add Dueling/Prioritized only if needed
- **Systematic debugging** beats random tuning

**Next**: Implement on simple environment first (CartPole or small custom task), then scale to Atari.
