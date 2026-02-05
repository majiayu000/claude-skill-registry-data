---
name: reward-shaping-engineering
description: Master reward function design - potential-based shaping, hacking patterns, validation
---

# Reward-Shaping Engineering

## When to Use This Skill

Invoke this skill when you encounter:

- **Reward Design**: "How do I design the reward function for my task?"
- **Slow Learning**: "Training is extremely slow with sparse rewards" or "Dense rewards cause weird behavior"
- **Reward Hacking**: "My agent learned a trick that works in training but fails on test", "Agent oscillating instead of balancing"
- **Potential-Based Shaping**: "How to add shaping without breaking the optimal policy?"
- **Distance-Based Rewards**: "How to reward progress toward goal without hacking?"
- **Inverse RL**: "I have expert demonstrations, can I learn reward from them?"
- **Auxiliary Rewards**: "Should I add helper rewards like action smoothness?"
- **Reward Scale Issues**: "Training feels different when rewards change magnitude"
- **Sparse vs Dense**: "When should I use sparse vs dense rewards?"
- **Reward Validation**: "How do I verify my reward function is correct?"
- **Credit Assignment**: "How to help agent understand which actions led to success?"
- **Normalization**: "Should I clip or normalize rewards?"

**This skill provides systematic frameworks and concrete patterns for reward engineering.**

Do NOT use for:

- Algorithm selection (route to rl-foundations or specific algorithm skill)
- General RL debugging (route to rl-debugging-methodology)
- Exploration strategies (route to exploration-strategies)
- Environment design (route to environment-design-patterns)

---

## Core Principle

**Reward design is often the hardest part of RL.** The reward function defines the entire objective the agent optimizes. A poorly designed reward either:

1. Learns something unintended (reward hacking)
2. Learns slowly due to sparse/noisy signal (credit assignment crisis)
3. Learns correctly but unstably due to scale/normalization issues

The key insight: **You're solving an inverse problem.** You want an agent that achieves behavior X. You need to specify function R(s,a,s') such that optimal policy under R produces behavior X. This is much harder than it sounds because:

- Agents optimize expected return, not intentions (find loopholes)
- Credit assignment requires clear reward signal (sparse rewards fail)
- Scale/normalization matters (reward magnitude affects gradients)
- Shaping can help or hurt (need to preserve optimal policy)

---

## Part 1: Reward Design Principles

### Principle 1: Reward Must Align With Task

**The Problem**: You want agent to do X, but reward incentivizes Y.

**Example (CartPole)**:

- Task: Balance pole in center for as long as possible
- Bad reward: +1 per step (true) → Agent learns to oscillate side-to-side (unintended but gets +1 every step)
- Better reward: +1 per step centered + penalty for deviation

**Example (Robotics)**:

- Task: Grasp object efficiently
- Bad reward: Just +1 when grasped → Agent grasps sloppily, jerky movements
- Better reward: +1 for grasp + small penalty per action (reward efficiency)

**Pattern**: Specify WHAT success looks like, not HOW to achieve it. Let agent find the HOW.

```python
# Anti-pattern: Specify HOW
bad_reward = -0.1 * np.sum(np.abs(action))  # Penalize movement

# Pattern: Specify WHAT
good_reward = (1.0 if grasp_success else 0.0) + (-0.01 * np.sum(action**2))
# Says: Success is good, movements have small cost
# Agent figures out efficient movements to minimize action cost
```

### Principle 2: Reward Should Enable Credit Assignment

**The Problem**: Sparse rewards mean agent can't learn which actions led to success.

**Example (Goal Navigation)**:

- Sparse: Only +1 when reaching goal (1 in 1000 episodes maybe)
- Agent can't tell: Did action 10 steps ago help or action 5 steps ago?
- Solution: Add shaping reward based on progress

**Credit Assignment Window**:

```
Short window (< 10 steps):    Need dense rewards every 1-2 steps
Medium window (10-100 steps): Reward every 5-10 steps OK
Long window (> 100 steps):    Sparse rewards very hard, need shaping
```

**When to Add Shaping**:

- Episode length > 50 steps AND sparse rewards
- Agent can't achieve >10% success after exploring

### Principle 3: Reward Should Prevent Hacking

**The Problem**: Agent finds unintended loopholes.

**Classic Hacking Patterns**:

1. **Shortcut Exploitation**: Taking unintended path to goal
   - Example: Quadruped learns to flip instead of walk
   - Solution: Specify movement requirements in reward

2. **Side-Effect Exploitation**: Achieving side-effect that gives reward
   - Example: Robotic arm oscillating (gets +1 per step for oscillation)
   - Solution: Add penalty for suspicious behavior

3. **Scale Exploitation**: Abusing unbounded reward dimension
   - Example: Agent learns to get reward signal to spike → oscillates
   - Solution: Use clipped/normalized rewards

**Prevention Framework**:

```python
def design_robust_reward(s, a, s_next):
    # Core task reward
    task_reward = compute_task_reward(s_next)

    # Anti-hacking penalties
    action_penalty = -0.01 * np.sum(a**2)  # Penalize unnecessary action
    suspension_penalty = check_suspension(s_next)  # Penalize weird postures

    return task_reward + action_penalty + suspension_penalty
```

### Principle 4: Reward Scale and Normalization Matter

**The Problem**: Reward magnitude affects gradient flow.

**Example**:

```
Task A rewards:  0 to 1000
Task B rewards:  0 to 1
Same optimizer with fixed learning rate:
  Task A: Step sizes huge, diverges
  Task B: Step sizes tiny, barely learns

Solution: Normalize both to [-1, 1]
```

**Standard Normalization Pipeline**:

```python
def normalize_reward(r):
    # 1. Clip to reasonable range (prevents scale explosions)
    r_clipped = np.clip(r, -1000, 1000)

    # 2. Normalize using running statistics
    reward_mean = running_mean(r_clipped)
    reward_std = running_std(r_clipped)
    r_normalized = (r_clipped - reward_mean) / (reward_std + 1e-8)

    # 3. Clip again to [-1, 1] for stability
    return np.clip(r_normalized, -1.0, 1.0)
```

---

## Part 2: Potential-Based Shaping (The Theorem)

### The Fundamental Problem

You want to:

- Help agent learn faster (add shaping rewards)
- Preserve the optimal policy (so shaping doesn't change what's best)

**The Solution: Potential-Based Shaping**

The theorem states: If you add shaping reward of form

```
F(s, a, s') = γ * Φ(s') - Φ(s)
```

where Φ(s) is ANY function of state, then:

1. Optimal policy remains unchanged
2. Optimal value function shifts by Φ
3. Learning accelerates due to better signal

**Why This Matters**: You can safely add rewards like distance-to-goal without worrying you're changing what the agent should do.

### Mathematical Foundation

Original MDP has Q-function: `Q^π(s,a) = E[R(s,a,s') + γV^π(s')]`

With potential-based shaping:

```
Q'^π(s,a) = Q^π(s,a) + [γΦ(s') - Φ(s)]
          = E[R(s,a,s') + γΦ(s') - Φ(s) + γV^π(s')]
          = E[R(s,a,s') + γ(Φ(s') + V^π(s')) - Φ(s)]
```

The key insight: When computing optimal policy, Φ(s) acts like state-value function offset. Different actions get different Φ values, but relative ordering (which action is best) unchanged.

**Proof Sketch**:

- Policy compares Q(s,a₁) vs Q(s,a₂) to pick action
- Both differ by same [γΦ(s') - Φ(s)] at state s
- Relative ordering preserved → same optimal action

### Practical Implementation

```python
def potential_based_shaping(s, a, s_next, gamma=0.99):
    """
    Compute shaping reward that preserves optimal policy.

    Args:
        s: current state
        a: action taken
        s_next: next state (result of action)
        gamma: discount factor

    Returns:
        Shaping reward to ADD to environment reward
    """
    # Define potential function (e.g., negative distance to goal)
    phi = compute_potential(s)
    phi_next = compute_potential(s_next)

    # Potential-based shaping formula
    shaping_reward = gamma * phi_next - phi

    return shaping_reward

def compute_potential(s):
    """
    Potential function: Usually distance to goal.

    Negative of distance works well:
    - States farther from goal have lower potential
    - Moving closer increases potential (positive shaping reward)
    - Reaching goal gives highest potential
    """
    if goal_reached(s):
        return 0.0  # Peak potential
    else:
        distance = euclidean_distance(s['position'], s['goal'])
        return -distance  # Negative distance
```

### Critical Error: NOT Using Potential-Based Shaping

**Common Mistake**:

```python
# WRONG: This changes the optimal policy!
shaping_reward = -0.1 * distance_to_goal

# WHY WRONG: This isn't potential-based. Moving from d=1 to d=0.5 gives:
#   Reward = -0.1 * 0.5 - (-0.1 * 1.0) = +0.05
# But moving from d=3 to d=2.5 gives:
#   Reward = -0.1 * 2.5 - (-0.1 * 3.0) = +0.05
# Same reward for same distance change regardless of state!
# This distorts value function and can change which action is optimal.
```

**Right Way**:

```python
# CORRECT: Potential-based shaping
def shaping(s, a, s_next):
    phi_s = -distance(s, goal)  # Potential = negative distance
    phi_s_next = -distance(s_next, goal)

    return gamma * phi_s_next - phi_s

# Moving from d=1 to d=0.5:
#   shaping = 0.99 * (-0.5) - (-1.0) = +0.495
# Moving from d=3 to d=2.5:
#   shaping = 0.99 * (-2.5) - (-3.0) = +0.475
# Slightly different, depends on state! Preserves policy.
```

### Using Potential-Based Shaping

```python
def compute_total_reward(s, a, s_next, env_reward, gamma=0.99):
    """
    Combine environment reward with potential-based shaping.

    Pattern: R_total = R_env + R_shaping
    """
    # 1. Get reward from environment
    task_reward = env_reward

    # 2. Compute potential-based shaping (safe to add)
    potential = -distance_to_goal(s_next)
    potential_prev = -distance_to_goal(s)
    shaping_reward = gamma * potential - potential_prev

    # 3. Combine
    total_reward = task_reward + shaping_reward

    return total_reward
```

---

## Part 3: Sparse vs Dense Rewards

### The Fundamental Tradeoff

| Aspect | Sparse Rewards | Dense Rewards |
|--------|---|---|
| **Credit Assignment** | Hard (credit window huge) | Easy (immediate feedback) |
| **Learning Speed** | Slow (few positive examples) | Fast (constant signal) |
| **Reward Hacking** | Less likely (fewer targets) | More likely (many targets to exploit) |
| **Convergence** | Can converge to suboptimal | May not converge if hacking |
| **Real-World** | Matches reality (goals sparse) | Artificial but helps learning |

### Decision Framework

**Use SPARSE when**:

- Task naturally has sparse rewards (goal-reaching, game win/loss)
- Episode short (< 20 steps)
- You want solution robust to reward hacking
- Final performance matters more than learning speed

**Use DENSE when**:

- Episode long (> 50 steps) and no natural sub-goals
- Learning speed critical (limited training budget)
- You can design safe auxiliary rewards
- You'll validate extensively against hacking

**Use HYBRID when**:

- Combine sparse task reward with dense shaping
- Example: +1 for reaching goal (sparse) + negative distance shaping (dense)
- This is the most practical approach for long-horizon tasks

### Design Pattern: Sparse Task + Dense Shaping

```python
def reward_function(s, a, s_next, done):
    """
    Standard pattern: sparse task reward + potential-based shaping.

    This gets the best of both worlds:
    - Sparse task reward prevents hacking on main objective
    - Dense shaping prevents credit assignment crisis
    """
    # 1. Sparse task reward (what we truly care about)
    if goal_reached(s_next):
        task_reward = 1.0
    else:
        task_reward = 0.0

    # 2. Dense potential-based shaping (helps learning)
    gamma = 0.99
    phi_s = -np.linalg.norm(s['position'] - s['goal'])
    phi_s_next = -np.linalg.norm(s_next['position'] - s_next['goal'])
    shaping_reward = gamma * phi_s_next - phi_s

    # 3. Combine: Sparse main objective + dense guidance
    total = task_reward + 0.1 * shaping_reward
    # Scale shaping (0.1) relative to task (1.0) so task dominates

    return total
```

### Validation: Confirming Sparse/Dense Choice

```python
def validate_reward_choice(sparse_reward_fn, dense_reward_fn, env, n_trials=10):
    """
    Compare sparse vs dense by checking:
    1. Learning speed (how fast does agent improve?)
    2. Final performance (does dense cause hacking?)
    3. Stability (does one diverge?)
    """
    results = {
        'sparse': train_agent(sparse_reward_fn, env, n_trials),
        'dense': train_agent(dense_reward_fn, env, n_trials)
    }

    # Check learning curves
    print("Sparse learning speed:", results['sparse']['steps_to_50pct'])
    print("Dense learning speed:", results['dense']['steps_to_50pct'])

    # Check if dense causes hacking
    print("Sparse final score:", results['sparse']['final_score'])
    print("Dense final score:", results['dense']['final_score'])

    # If dense learned faster AND achieved same/higher score: use dense + validation
    # If sparse achieved higher: reward hacking detected in dense
```

---

## Part 4: Reward Hacking - Patterns and Detection

### Common Hacking Patterns

#### Pattern 1: Shortcut Exploitation

Agent finds unintended path to success.

**Example (Quadruped)**:

- Task: Walk forward 10 meters
- Intended: Gait pattern that moves forward
- Hack: Agent learns to flip upside down (center of mass moves forward during flip!)

**Detection**:

```python
# Test on distribution shift
if test_on_different_terrain(agent) << train_performance:
    print("ALERT: Shortcut exploitation detected")
    print("Agent doesn't generalize → learned specific trick")
```

**Prevention**:

```python
def robust_reward(s, a, s_next):
    # Forward progress
    progress = s_next['x'] - s['x']

    # Requirement: Stay upright (prevents flipping hack)
    upright_penalty = -1.0 if not is_upright(s_next) else 0.0

    # Requirement: Reasonable movement (prevents wiggling)
    movement_penalty = -0.1 * np.sum(a**2)

    return progress + upright_penalty + movement_penalty
```

#### Pattern 2: Reward Signal Exploitation

Agent exploits direct reward signal rather than task.

**Example (Oscillation)**:

- Task: Balance pole in center
- Intended: Keep pole balanced
- Hack: Agent oscillates rapidly (each oscillation = +1 reward per step)

**Detection**:

```python
def detect_oscillation(trajectory):
    positions = [s['pole_angle'] for s in trajectory]
    # Count zero crossings
    crossings = sum(1 for i in range(len(positions)-1)
                    if positions[i] * positions[i+1] < 0)

    if crossings > len(trajectory) / 3:
        print("ALERT: Oscillation detected")
```

**Prevention**:

```python
def non_hackable_reward(s, a, s_next):
    # Task: Balanced pole
    balance_penalty = -(s_next['pole_angle']**2)  # Reward being centered

    # Prevent oscillation
    angle_velocity = s_next['pole_angle'] - s['pole_angle']
    oscillation_penalty = -0.1 * abs(angle_velocity)

    return balance_penalty + oscillation_penalty
```

#### Pattern 3: Unbounded Reward Exploitation

Agent maximizes dimension without bound.

**Example (Camera Hack)**:

- Task: Detect object (reward for correct detection)
- Hack: Agent learns to point camera lens at bright light source (always triggers detection)

**Detection**:

```python
def detect_unbounded_exploitation(training_history):
    rewards = training_history['episode_returns']

    # Check if rewards growing without bound
    if rewards[-100:].mean() >> rewards[100:200].mean():
        print("ALERT: Rewards diverging")
        print("Possible unbounded exploitation")
```

**Prevention**:

```python
# Use reward clipping
def clipped_reward(r):
    return np.clip(r, -1.0, 1.0)

# Or normalize
def normalized_reward(r, running_mean, running_std):
    r_norm = (r - running_mean) / (running_std + 1e-8)
    return np.clip(r_norm, -1.0, 1.0)
```

### Systematic Hacking Detection Framework

```python
def check_for_hacking(agent, train_env, test_envs, holdout_env):
    """
    Comprehensive hacking detection.
    """
    # 1. Distribution shift test
    train_perf = evaluate(agent, train_env)
    test_perf = evaluate(agent, test_envs)  # Variations of train

    if train_perf >> test_perf:
        print("HACKING: Agent doesn't generalize to distribution shift")
        return "shortcut_exploitation"

    # 2. Behavioral inspection
    trajectory = run_episode(agent, holdout_env)
    if has_suspicious_pattern(trajectory):
        print("HACKING: Suspicious behavior detected")
        return "pattern_exploitation"

    # 3. Reward curve analysis
    if rewards_diverging(agent.training_history):
        print("HACKING: Unbounded reward exploitation")
        return "reward_signal_exploitation"

    return "no_obvious_hacking"
```

---

## Part 5: Auxiliary Rewards and Shaping Examples

### Example 1: Distance-Based Shaping

**Most common shaping pattern. Safe when done with potential-based formula.**

```python
def distance_shaping(s, a, s_next, gamma=0.99):
    """
    Reward agent for getting closer to goal.

    CRITICAL: Use potential-based formula to preserve optimal policy.
    """
    goal_position = s['goal']
    curr_pos = s['position']
    next_pos = s_next['position']

    # Potential function: negative distance
    phi = -np.linalg.norm(curr_pos - goal_position)
    phi_next = -np.linalg.norm(next_pos - goal_position)

    # Potential-based shaping (preserves optimal policy)
    shaping_reward = gamma * phi_next - phi

    return shaping_reward
```

### Example 2: Auxiliary Smoothness Reward

**Help agent learn smooth actions without changing optimal behavior.**

```python
def smoothness_shaping(a, a_prev):
    """
    Penalize jittery/jerky actions.
    Helps with efficiency and generalization.
    """
    # Difference between consecutive actions
    action_jerk = np.linalg.norm(a - a_prev)

    # Penalty (small, doesn't dominate task reward)
    smoothness_penalty = -0.01 * action_jerk

    return smoothness_penalty
```

### Example 3: Energy/Control Efficiency

**Encourage efficient control.**

```python
def efficiency_reward(a):
    """
    Penalize excessive control effort.
    Makes solutions more robust.
    """
    # L2 norm of action (total control magnitude)
    effort = np.sum(a**2)

    # Small penalty
    return -0.001 * effort
```

### Example 4: Staying Safe Reward

**Prevent dangerous states (without hard constraints).**

```python
def safety_reward(s):
    """
    Soft penalty for dangerous states.
    Better than hard constraints (more learnable).
    """
    danger_score = 0.0

    # Example: Prevent collision
    min_clearance = np.min(s['collision_distances'])
    if min_clearance < 0.1:
        danger_score += 10.0 * (0.1 - min_clearance)

    # Example: Prevent extreme states
    if np.abs(s['position']).max() > 5.0:
        danger_score += 1.0

    return -danger_score
```

### When to Add Auxiliary Rewards

**Add auxiliary reward if**:

- It's potential-based (safe)
- Task reward already roughly works (agent > 10% success)
- Auxiliary targets clear sub-goals
- You validate with/without

**Don't add if**:

- Task reward doesn't work at all (fix that first)
- Creates new exploitation opportunities
- Makes reward engineering too complex

---

## Part 6: Inverse RL - Learning Rewards from Demonstrations

### The Problem

You have expert demonstrations but no explicit reward function. How to learn?

**Options**:

1. Behavioral cloning: Copy actions directly (doesn't learn why)
2. Reward learning (inverse RL): Infer reward structure from demonstrations
3. Imitation learning: Match expert behavior distribution (GAIL style)

### Inverse RL Concept

**Idea**: Expert is optimal under some reward function. Infer what reward structure makes expert optimal.

```
Expert demonstrations → Infer reward function → Train agent on learned reward
```

**Key insight**: If expert is optimal under reward R, then R(expert_actions) >> R(other_actions)

### Practical Inverse RL (Maximum Entropy IRL)

```python
class InverseRLLearner:
    """
    Learn reward function from expert demonstrations.

    Assumes expert is performing near-optimal policy under true reward.
    """

    def __init__(self, state_dim, action_dim):
        # Reward function (small neural network)
        self.reward_net = nn.Sequential(
            nn.Linear(state_dim + action_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.optimizer = torch.optim.Adam(self.reward_net.parameters())

    def compute_reward(self, s, a):
        """Learned reward function."""
        sa = torch.cat([torch.tensor(s), torch.tensor(a)])
        return self.reward_net(sa).item()

    def train_step(self, expert_trajectories, agent_trajectories):
        """
        Update reward to make expert better than agent.

        Principle: Maximize expert returns, minimize agent returns under current reward.
        """
        # Expert reward sum
        expert_returns = sum(
            sum(self.compute_reward(s, a) for s, a in traj)
            for traj in expert_trajectories
        )

        # Agent reward sum
        agent_returns = sum(
            sum(self.compute_reward(s, a) for s, a in traj)
            for traj in agent_trajectories
        )

        # Loss: Want expert >> agent
        loss = agent_returns - expert_returns

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
```

### When to Use Inverse RL

**Use when**:

- Reward is hard to specify but easy to demonstrate
- You have expert demonstrations (human, reference controller)
- Task complex enough that behavior != objective
- Training budget allows for two-stage process

**Don't use when**:

- Reward is easy to specify (just specify it!)
- No expert demonstrations available
- Demonstration quality varies
- Need fast learning (inverse RL is slow)

---

## Part 7: Reward Normalization and Clipping

### Why Normalize?

Reward scale directly affects gradient magnitude and training stability.

```python
# Without normalization
reward_taskA = 1000 * task_metric  # Large magnitude
loss = -policy_gradient * reward_taskA  # Huge gradients

# With normalization
reward_normalized = reward_taskA / reward_std  # Unit magnitude
loss = -policy_gradient * reward_normalized  # Reasonable gradients
```

### Standard Normalization Pipeline

```python
class RewardNormalizer:
    def __init__(self, epsilon=1e-8):
        self.mean = 0.0
        self.var = 1.0
        self.epsilon = epsilon

    def update_statistics(self, rewards):
        """Update running mean and variance."""
        rewards = np.array(rewards)
        # Exponential moving average (online update)
        alpha = 0.01
        self.mean = (1 - alpha) * self.mean + alpha * rewards.mean()
        self.var = (1 - alpha) * self.var + alpha * rewards.var()

    def normalize(self, reward):
        """Apply standardization then clipping."""
        # 1. Standardize (zero mean, unit variance)
        normalized = (reward - self.mean) / np.sqrt(self.var + self.epsilon)

        # 2. Clip to [-1, 1] for stability
        clipped = np.clip(normalized, -1.0, 1.0)

        return clipped
```

### Clipping Strategy

```python
def clip_reward(r, clip_range=(-1.0, 1.0)):
    """
    Clip reward to fixed range.

    Prevents large reward spikes from destabilizing training.
    """
    return np.clip(r, clip_range[0], clip_range[1])

# Usage
def total_reward(task_r, shaping_r):
    # Combine rewards
    combined = task_r + shaping_r

    # Clip combined
    clipped = clip_reward(combined)

    return clipped
```

---

## Part 8: Validating Reward Functions

### Validation Checklist

```python
def validate_reward_function(reward_fn, env, agent_class, n_trials=5):
    """
    Systematic validation of reward design.
    """
    results = {}

    # 1. Learning speed test
    agent = train_agent(agent_class, env, reward_fn, steps=100000)
    success_rate = evaluate(agent, env, n_episodes=100)
    results['learning_speed'] = success_rate

    if success_rate < 0.3:
        print("WARNING: Agent can't learn → reward signal too sparse")
        return False

    # 2. Generalization test
    test_variants = [modify_env(env) for _ in range(5)]
    test_rates = [evaluate(agent, test_env, 20) for test_env in test_variants]

    if np.mean(test_rates) < 0.7 * success_rate:
        print("WARNING: Hacking detected → Agent doesn't generalize")
        return False

    # 3. Stability test
    agents = [train_agent(...) for _ in range(n_trials)]
    variance = np.var([evaluate(a, env, 20) for a in agents])

    if variance > 0.3:
        print("WARNING: Training unstable → Reward scale issue?")
        return False

    # 4. Behavioral inspection
    trajectory = run_episode(agent, env)
    if suspicious_behavior(trajectory):
        print("WARNING: Agent exhibiting strange behavior")
        return False

    print("PASSED: Reward function validated")
    return True
```

### Red Flags During Validation

| Red Flag | Likely Cause | Fix |
|----------|---|---|
| Success rate < 10% after 50k steps | Reward too sparse | Add shaping |
| High variance across seeds | Reward scale/noise | Normalize/clip |
| Passes train but fails test | Reward hacking | Add anti-hacking penalties |
| Rewards diverging to infinity | Unbounded reward | Use clipping |
| Agent oscillates/twitches | Per-step reward exploitation | Penalize action change |
| Learning suddenly stops | Reward scale issue | Check normalization |

---

## Part 9: Common Pitfalls and Rationalizations

### Pitfall 1: "Let me just add distance reward"

**Rationalization**: "I'll add reward for getting closer to goal, it can't hurt"
**Problem**: Without potential-based formula, changes optimal policy
**Reality Check**: Measure policy difference with/without shaping

### Pitfall 2: "Sparse rewards are always better"

**Rationalization**: "Sparse rewards prevent hacking"
**Problem**: Agent can't learn in long-horizon tasks (credit assignment crisis)
**Reality Check**: 10+ steps without reward → need shaping or fail training

### Pitfall 3: "Normalize everything"

**Rationalization**: "I'll normalize all rewards to [-1, 1]"
**Problem**: Over-normalization loses task structure (goal vs near-goal now equal)
**Reality Check**: Validate that normalized reward still trains well

### Pitfall 4: "Inverse RL is the answer"

**Rationalization**: "I don't know how to specify rewards, I'll learn from demos"
**Problem**: Inverse RL is slow and requires good demonstrations
**Reality Check**: If you can specify reward clearly, just do it

### Pitfall 5: "More auxiliary rewards = faster learning"

**Rationalization**: "I'll add smoothness, energy, safety rewards"
**Problem**: Each auxiliary reward is another hacking target
**Reality Check**: Validate each auxiliary independently

### Pitfall 6: "This should work, why doesn't it?"

**Rationalization**: "The reward looks right, must be algorithm issue"
**Problem**: Reward design is usually the bottleneck, not algorithm
**Reality Check**: Systematically validate reward using test framework

### Pitfall 7: "Agent learned the task, my reward was right"

**Rationalization**: "Agent succeeded, so reward design was good"
**Problem**: Agent might succeed on hacked solution, not true task
**Reality Check**: Test on distribution shift / different environment variants

### Pitfall 8: "Dense rewards cause overfitting"

**Rationalization**: "Sparse rewards generalize better"
**Problem**: Sparse rewards just fail to learn in long episodes
**Reality Check**: Compare learning curves and final policy generalization

### Pitfall 9: "Clipping breaks the signal"

**Rationalization**: "If I clip rewards, I lose information"
**Problem**: Unbounded rewards cause training instability
**Reality Check**: Relative ordering preserved after clipping, information retained

### Pitfall 10: "Potential-based shaping doesn't matter"

**Rationalization**: "A reward penalty is a reward penalty"
**Problem**: Non-potential-based shaping CAN change optimal policy
**Reality Check**: Prove mathematically that Φ(s') - Φ(s) structure used

---

## Part 10: Reward Engineering Patterns for Common Tasks

### Pattern 1: Goal-Reaching Tasks

```python
def reaching_reward(s, a, s_next, gamma=0.99):
    """
    Task: Reach target location.
    """
    goal = s['goal']

    # Sparse task reward
    if np.linalg.norm(s_next['position'] - goal) < 0.1:
        task_reward = 1.0
    else:
        task_reward = 0.0

    # Dense potential-based shaping
    distance = np.linalg.norm(s_next['position'] - goal)
    distance_prev = np.linalg.norm(s['position'] - goal)

    phi = -distance
    phi_prev = -distance_prev
    shaping = gamma * phi - phi_prev

    # Efficiency penalty (optional)
    efficiency = -0.001 * np.sum(a**2)

    return task_reward + 0.1 * shaping + efficiency
```

### Pattern 2: Locomotion Tasks

```python
def locomotion_reward(s, a, s_next):
    """
    Task: Move forward efficiently.
    """
    # Forward progress (sparse)
    forward_reward = s_next['x_pos'] - s['x_pos']

    # Staying alive (don't fall)
    alive_bonus = 1.0 if is_alive(s_next) else 0.0

    # Energy efficiency
    action_penalty = -0.0001 * np.sum(a**2)

    return forward_reward + alive_bonus + action_penalty
```

### Pattern 3: Multi-Objective Tasks

```python
def multi_objective_reward(s, a, s_next):
    """
    Task: Multiple objectives (e.g., reach goal AND minimize energy).
    """
    goal_reward = 10.0 * (goal_progress(s, s_next))
    energy_reward = -0.01 * np.sum(a**2)
    safety_reward = -1.0 * collision_risk(s_next)

    # Weight objectives
    return 1.0 * goal_reward + 0.1 * energy_reward + 0.5 * safety_reward
```

---

## Summary: Reward Engineering Workflow

1. **Specify what success looks like** (task reward)
2. **Choose sparse or dense** based on episode length
3. **If dense, use potential-based shaping** (preserves policy)
4. **Add anti-hacking penalties** if needed
5. **Normalize and clip** for stability
6. **Validate** systematically (generalization, hacking, stability)
7. **Iterate** based on validation results

---

## Key Equations Reference

```
Potential-Based Shaping:
F(s,a,s') = γΦ(s') - Φ(s)

Value Function Shift (with shaping):
V'(s) = V(s) + Φ(s)

Optimal Policy Preservation:
argmax_a Q'(s,a) = argmax_a Q(s,a)  (same action, different Q-values)

Reward Normalization:
r_norm = (r - μ) / (σ + ε)

Clipping:
r_clipped = clip(r_norm, -1, 1)
```

---

## Testing Scenarios (13+)

The skill addresses these scenarios:

1. Detecting reward hacking from test set failure
2. Implementing potential-based shaping correctly
3. Choosing sparse vs dense based on episode length
4. Designing distance-based rewards without changing policy
5. Adding auxiliary rewards without hacking
6. Normalizing rewards across task variants
7. Validating that shaping preserves optimal policy
8. Applying inverse RL to expert demonstrations
9. Debugging when reward signal causes oscillation
10. Engineering rewards for specific task families
11. Recognizing when reward is bottleneck vs algorithm
12. Explaining reward hacking in principal-agent terms
13. Implementing end-to-end reward validation pipeline

---

## Practical Checklist

- [ ] Task reward clearly specifies success
- [ ] Reward function can't be exploited by shortcuts
- [ ] Episode length < 20 steps → sparse OK
- [ ] Episode length > 50 steps → need shaping
- [ ] Using potential-based formula F = γΦ(s') - Φ(s)
- [ ] Clipping/normalizing rewards to [-1, 1]
- [ ] Tested on distribution shift (different env variant)
- [ ] Behavioral inspection (is agent doing what you expect?)
- [ ] Training stability across seeds (variance < 0.3)
- [ ] Learning curves look reasonable (no sudden divergence)
- [ ] Final policy generalizes to test distribution
