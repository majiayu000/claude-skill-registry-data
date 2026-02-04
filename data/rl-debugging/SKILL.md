---
name: rl-debugging
description: Systematic RL debugging - diagnose learning failures, common bugs, diagnosis trees
---

# RL Debugging Methodology

## When to Use This Skill

Invoke this skill when you encounter:

- **Agent Won't Learn**: Reward stuck at baseline, not improving
- **Training Unstable**: Loss bouncing, reward highly variable
- **Suboptimal Policy**: Agent learned something but worse than expected
- **Reward Hacking**: Agent gaming the reward function
- **Exploration Issues**: Agent stuck in local optimum or exploring poorly
- **Hyperparameter Sensitivity**: Small changes break training
- **Learning Rate Tuning**: Not sure what value is right
- **Convergence Problems**: Loss doesn't decrease or decreases then stops
- **Environment vs Algorithm**: Unsure if problem is environment or RL algorithm
- **Logging Confusion**: Not sure what metrics to monitor
- **Gradual Performance Degradation**: Early training good, later poor
- **Sparse Reward Challenge**: Agent never finds reward signal

**Core Problem**: RL debugging often becomes random hyperparameter tweaking. Agents are complex systems with many failure modes. Systematic diagnosis finds root causes; random tweaking wastes time and leads to contradictory findings.

## Do NOT Use This Skill For

- **Learning RL theory** (route to rl-foundations for MDPs, Bellman equations, policy gradients)
- **Implementing new algorithms** (route to algorithm-specific skills like value-based-methods, policy-gradient-methods, actor-critic-methods)
- **Environment API questions** (route to rl-environments for Gym/Gymnasium API, custom environments, wrappers)
- **Evaluation methodology** (route to rl-evaluation for rigorous statistical testing, generalization assessment)
- **Initial algorithm selection** (route to using-deep-rl router or rl-foundations for choosing the right algorithm family)

---

## Core Principle: The 80/20 Rule

**The most important insight in RL debugging:**

```
80% of RL failures are in:
  1. Environment design (agent can't see true state)
  2. Reward function (misaligned or wrong scale)
  3. Observation/action representation (missing information)

15% are in:
  4. Hyperparameters (learning rate, batch size, etc.)
  5. Exploration strategy (too much or too little)

5% are in:
  6. Algorithm selection (wrong algorithm for problem)
```

**Consequence**: If training fails, check environment and reward FIRST. Changing the algorithm last.

### Why This Order?

**Scenario 1: Broken Environment**

```python
# BROKEN ENVIRONMENT: Agent can't win no matter what algorithm
class BrokenEnv:
    def reset(self):
        self.state = random_state()  # Agent can't control this
        return self.state

    def step(self, action):
        # Reward independent of action!
        reward = random.random()
        return self.state, reward

    # No amount of PPO, DQN, SAC can learn from random reward

# CORRECT ENVIRONMENT: Agent can win with right policy
class CorrectEnv:
    def reset(self):
        self.state = initial_state
        return self.state

    def step(self, action):
        # Reward depends on action
        reward = compute_reward(self.state, action)
        self.state = compute_next_state(self.state, action)
        return self.state, reward
```

**If environment is broken, no algorithm will learn.**

**Scenario 2: Reward Scale Issue**

```python
# WRONG SCALE: Reward in [0, 1000000]
# Algorithm gradient updates: param = param - lr * grad
# If gradient huge (due to reward scale), single step breaks everything

# CORRECT SCALE: Reward in [-1, 1]
# Gradients are reasonable, learning stable

# Fix is simple: divide reward by scale factor
# But if you don't know to check reward scale, you'll try 10 learning rates instead
```

**Consequence: Always check reward scale before tuning learning rate.**

---

## Part 1: Systematic Debugging Framework

### The Debugging Process (Not Random Tweaking)

```
START: Agent not learning (or training unstable, or suboptimal)

Step 1: ENVIRONMENT CHECK (Does agent have what it needs?)
  ├─ Can agent see the state? (Is observation sufficient?)
  ├─ Is environment deterministic or stochastic? (Affects algorithm choice)
  ├─ Can agent actually win? (Does optimal policy exist?)
  └─ Is environment reset working? (Fresh episode each reset?)

Step 2: REWARD SCALE CHECK (Is reward in reasonable range?)
  ├─ What's the range of rewards? (Min, max, typical)
  ├─ Are rewards normalized? (Should be ≈ [-1, 1])
  ├─ Is reward aligned with desired behavior? (No reward hacking)
  └─ Are rewards sparse or dense? (Affects exploration strategy)

Step 3: OBSERVATION REPRESENTATION (Is information preserved?)
  ├─ Are observations normalized? (Images: [0, 255] or [0, 1]?)
  ├─ Is temporal information included? (Frame stacking for Atari?)
  ├─ Are observations consistent? (Same format each episode?)
  └─ Is observation sufficient to solve problem? (Can human win from this info?)

Step 4: BASIC ALGORITHM CHECK (Is the RL algorithm working at all?)
  ├─ Run on simple environment (CartPole, simple task)
  ├─ Can algorithm learn on simple env? (If not: algorithm issue)
  ├─ Can algorithm beat random baseline? (If not: something is broken)
  └─ Does loss decrease? (If not: learning not happening)

Step 5: HYPERPARAMETER TUNING (Only after above passed)
  ├─ Is learning rate in reasonable range? (1e-5 to 1e-3 typical)
  ├─ Is batch size appropriate? (Power of 2: 32, 64, 128, 256)
  ├─ Is exploration sufficient? (Epsilon decaying? Entropy positive?)
  └─ Are network layers reasonable? (3 hidden layers typical)

Step 6: LOGGING ANALYSIS (What do the metrics say?)
  ├─ Policy loss: decreasing? exploding? zero?
  ├─ Value loss: decreasing? stable?
  ├─ Reward curve: trending up? flat? oscillating?
  ├─ Entropy: decreasing over time? (Exploration → exploitation)
  └─ Gradient norms: reasonable? exploding? vanishing?

Step 7: IDENTIFY ROOT CAUSE (Synthesize findings)
  └─ Where is the actual problem? (Environment, reward, algorithm, hyperparameters)
```

### Why This Order Matters

**Common mistake: Jump to Step 5 (hyperparameter tuning)**

```python
# Agent not learning. Frustration sets in.
# "I'll try learning rate 1e-4" (Step 5, skipped 1-4)
# Doesn't work.
# "I'll try batch size 64" (more Step 5 tweaking)
# Doesn't work.
# "I'll try a bigger network" (still Step 5)
# Doesn't work.
# Hours wasted.

# Correct approach: Follow Steps 1-4 first.
# Step 1: Oh! Environment reset is broken, always same initial state
# Fix environment.
# Now agent learns immediately with default hyperparameters.
```

**The order reflects probability**: It's more likely the environment is broken than the algorithm; more likely the reward scale is wrong than learning rate is wrong.

---

## Part 2: Diagnosis Trees by Symptom

### Diagnosis Tree 1: "Agent Won't Learn"

**Symptom**: Reward stuck near random baseline. Loss doesn't decrease meaningfully.

```
START: Agent Won't Learn

├─ STEP 1: Can agent beat random baseline?
│  ├─ YES → Skip to STEP 4
│  └─ NO → Environment issue likely
│     ├─ Check 1A: Is environment output sane?
│     │  ├─ Print first 5 episodes: state, action, reward, next_state
│     │  ├─ Verify types match (shapes, ranges, dtypes)
│     │  └─ Is reward always same? Always zero? (Red flag: no signal)
│     ├─ Check 1B: Can you beat it manually?
│     │  ├─ Play environment by hand (hardcode a policy)
│     │  ├─ Can you get >0 reward? (If not: environment is broken)
│     │  └─ If yes: Agent is missing something
│     └─ Check 1C: Is reset working?
│        ├─ Call reset() twice, check states differ
│        └─ If states same: reset is broken, fix it

├─ STEP 2: Is reward scale reasonable?
│  ├─ Compute: min, max, mean, std of rewards from random policy
│  ├─ If range >> 1 (e.g., [0, 10000]):
│  │  ├─ Action: Normalize rewards to [-1, 1]
│  │  ├─ Code: reward = reward / max_possible_reward
│  │  └─ Retest: Usually fixes "won't learn"
│  ├─ If range << 1 (e.g., [0, 0.001]):
│  │  ├─ Action: Scale up rewards
│  │  ├─ Code: reward = reward * 1000
│  │  └─ Or increase network capacity (more signal needed)
│  └─ If reward is [0, 1] (looks fine):
│     └─ Continue to STEP 3

├─ STEP 3: Is observation sufficient?
│  ├─ Check 3A: Are observations normalized?
│  │  ├─ If images [0, 255]: normalize to [0, 1] or [-1, 1]
│  │  ├─ Code: observation = observation / 255.0
│  │  └─ Retest
│  ├─ Check 3B: Is temporal info included? (For vision: frame stacking)
│  │  ├─ If using images: last 4 frames stacked?
│  │  ├─ If using states: includes velocity/derivatives?
│  │  └─ Missing temporal info → agent can't infer velocity
│  └─ Check 3C: Is observation Markovian?
│     ├─ Can optimal policy be derived from this observation?
│     ├─ If not: observation insufficient (red flag)
│     └─ Example: Only position, not velocity → agent can't control

├─ STEP 4: Run sanity check on simple environment
│  ├─ Switch to CartPole or equivalent simple env
│  ├─ Train with default hyperparameters
│  ├─ Does simple env learn? (Should learn in 1000-5000 steps)
│  ├─ YES → Your algorithm works, issue is your env/hyperparameters
│  └─ NO → Algorithm itself broken (rare, check algorithm implementation)

├─ STEP 5: Check exploration
│  ├─ Is agent exploring or stuck?
│  ├─ Log entropy (for stochastic policies)
│  ├─ If entropy → 0 early: agent exploiting before exploring
│  │  └─ Solution: Increase entropy regularization or ε
│  ├─ If entropy always high: too much exploration
│  │  └─ Solution: Decay entropy or ε more aggressively
│  └─ Visualize: Plot policy actions over time, should see diversity early

├─ STEP 6: Check learning rate
│  ├─ Is learning rate in [1e-5, 1e-3]? (typical range)
│  ├─ If > 1e-3: Try reducing (might be too aggressive)
│  ├─ If < 1e-5: Try increasing (might be too conservative)
│  ├─ Watch loss first step: If loss increases → LR too high
│  └─ Safe default: 3e-4

└─ STEP 7: Check network architecture
   ├─ For continuous control: small networks ok (1-2 hidden layers, 64-256 units)
   ├─ For vision: use CNN (don't use FC on pixels)
   ├─ Check if network has enough capacity
   └─ Tip: Start with simple, add complexity if needed
```

**ROOT CAUSES in order of likelihood:**

1. **Reward scale wrong** (40% of cases)
2. **Environment broken** (25% of cases)
3. **Observation insufficient** (15% of cases)
4. **Learning rate too high/low** (12% of cases)
5. **Algorithm issue** (8% of cases)

---

### Diagnosis Tree 2: "Training Unstable"

**Symptom**: Loss bounces wildly, reward spikes then crashes, training oscillates.

```
START: Training Unstable

├─ STEP 1: Characterize the instability
│  ├─ Plot loss curve: Does it bounce at same magnitude or grow?
│  ├─ Plot reward curve: Does it oscillate around mean or trend down?
│  ├─ Compute: reward variance over 100 episodes
│  └─ This tells you: Is it normal variance or pathological instability?

├─ STEP 2: Check if environment is deterministic
│  ├─ Deterministic environment + stochastic policy = normal variance
│  ├─ Stochastic environment + any policy = high variance (expected)
│  ├─ If stochastic: Can you reduce randomness? Or accept higher variance?
│  └─ Some instability is normal; distinguish from pathological

├─ STEP 3: Check reward scale
│  ├─ If rewards >> 1: Gradient updates too large
│  │  ├─ Single step might overshoot optimum
│  │  ├─ Solution: Normalize rewards to [-1, 1]
│  │  └─ This often fixes instability immediately
│  ├─ If reward has outliers: Single large reward breaks training
│  │  ├─ Solution: Reward clipping or scaling
│  │  └─ Example: r = np.clip(reward, -1, 1)
│  └─ Check: Is reward scale consistent?

├─ STEP 4: Check learning rate (LR often causes instability)
│  ├─ If loss oscillates: LR likely too high
│  │  ├─ Try reducing by 2-5× (e.g., 1e-3 → 3e-4)
│  │  ├─ Watch first 100 steps: Loss should decrease monotonically
│  │  └─ If still oscillates: try 10× reduction
│  ├─ If you have LR scheduler: Check if it's too aggressive
│  │  ├─ Scheduler reducing LR too fast can cause steps
│  │  └─ Solution: Slower schedule (more steps to final LR)
│  └─ Test: Set LR very low (1e-5), see if training is smooth
│     ├─ YES → Increase LR gradually until instability starts
│     └─ This bracketing finds safe LR range

├─ STEP 5: Check batch size
│  ├─ Small batch (< 32): High gradient variance, bouncy updates
│  │  ├─ Solution: Increase batch size (32, 64, 128)
│  │  └─ But not too large: training becomes slow
│  ├─ Large batch (> 512): Might overfit, large gradient steps
│  │  ├─ Solution: Use gradient accumulation
│  │  └─ Or reduce learning rate slightly
│  └─ Start with batch_size=64, adjust if needed

├─ STEP 6: Check gradient clipping
│  ├─ Are gradients exploding? (Check max gradient norm)
│  │  ├─ If max grad norm > 100: Likely exploding gradients
│  │  ├─ Solution: Enable gradient clipping (max_norm=1.0)
│  │  └─ Code: torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
│  ├─ If max grad norm reasonable (< 10): Skip this step
│  └─ Watch grad norm over training: Should stay roughly constant

├─ STEP 7: Check algorithm-specific parameters
│  ├─ For PPO: Is clipping epsilon reasonable? (0.2 default)
│  │  ├─ Too high: Over-clips, doesn't update
│  │  └─ Too low: Allows large updates, instability
│  ├─ For DQN: Is target network update frequency appropriate?
│  │  ├─ Update too often: Target constantly changing
│  │  └─ Update too rarely: Stale targets
│  └─ For A3C/A2C: Check entropy coefficient
│     ├─ Too high: Too much exploration, policy noisy
│     └─ Too low: Premature convergence

└─ STEP 8: Check exploration decay
   ├─ Is exploration decaying too fast? (Policy becomes deterministic)
   │  └─ If entropy→0 early: Agent exploits before exploring
   ├─ Is exploration decaying too slow? (Policy stays noisy)
   │  └─ If entropy stays high: Too much randomness in later training
   └─ Entropy should decay: high early, low late
      └─ Plot entropy over training: should show clear decay curve
```

**ROOT CAUSES in order of likelihood:**

1. **Learning rate too high** (35% of cases)
2. **Reward scale too large** (25% of cases)
3. **Batch size too small** (15% of cases)
4. **Gradient explosion** (10% of cases)
5. **Algorithm parameters** (10% of cases)
6. **Environment stochasticity** (5% of cases)

---

### Diagnosis Tree 3: "Suboptimal Policy"

**Symptom**: Agent learned something but performs worse than expected. Better than random baseline, but not good enough.

```
START: Suboptimal Policy

├─ STEP 1: How suboptimal? (Quantify the gap)
│  ├─ Compute: Agent reward vs theoretical optimal
│  ├─ If 80% of optimal: Normal (RL usually gets 80-90% optimal)
│  ├─ If 50% of optimal: Significantly suboptimal
│  ├─ If 20% of optimal: Very bad
│  └─ This tells you: Is it "good enough" or truly broken?

├─ STEP 2: Is it stuck in local optimum?
│  ├─ Run multiple seeds: Do you get similar reward each seed?
│  ├─ If rewards similar across seeds: Consistent local optimum
│  ├─ If rewards vary wildly: High variance, need more training
│  └─ Solution if local optimum: More exploration or better reward shaping

├─ STEP 3: Check reward hacking
│  ├─ Visualize agent behavior: Does it match intent?
│  ├─ Example: Cart-pole reward is [0, 1] per timestep
│  │  ├─ Agent might learn: "Stay in center, don't move"
│  │  ├─ Policy is suboptimal but still gets reward
│  │  └─ Solution: Reward engineering (bonus for progress)
│  └─ Hacking signs:
│     ├─ Agent does something weird but gets reward
│     ├─ Behavior makes no intuitive sense
│     └─ Reward increases but performance bad

├─ STEP 4: Is exploration sufficient?
│  ├─ Check entropy: Does policy explore initially?
│  ├─ Check epsilon decay (if using ε-greedy): Does it decay appropriately?
│  ├─ Is agent exploring broadly or stuck in small region?
│  ├─ Solution: Slower exploration decay or intrinsic motivation
│  └─ Use RND/curiosity if environment has sparse rewards

├─ STEP 5: Check network capacity
│  ├─ Is network too small to represent optimal policy?
│  ├─ For vision: Use standard CNN (not tiny network)
│  ├─ For continuous control: 2-3 hidden layers, 128-256 units
│  ├─ Test: Double network size, does performance improve?
│  └─ If yes: Original network was too small

├─ STEP 6: Check data efficiency
│  ├─ Is agent training long enough?
│  ├─ RL usually needs: simple tasks 100k steps, complex tasks 1M+ steps
│  ├─ If training only 10k steps: Too short, agent didn't converge
│  ├─ Solution: Train longer (but check reward curve first)
│  └─ If reward plateaus early: Extend training won't help

├─ STEP 7: Check observation and action spaces
│  ├─ Is action space continuous or discrete?
│  ├─ Is action discretization appropriate?
│  │  ├─ Too coarse: Can't express fine control
│  │  ├─ Too fine: Huge action space, hard to learn
│  │  └─ Example: 100 actions for simple control = too many
│  ├─ Is observation sufficient? (See Diagnosis Tree 1, Step 3)
│  └─ Missing information in observation = impossible to be optimal

├─ STEP 8: Check reward structure
│  ├─ Is reward dense or sparse?
│  ├─ Sparse reward + suboptimal policy: Agent might not be exploring to good region
│  │  ├─ Solution: Reward shaping (bonus for progress)
│  │  └─ Or: Intrinsic motivation (RND/curiosity)
│  ├─ Dense reward + suboptimal: Possible misalignment with intent
│  └─ Can you improve by reshaping reward?

└─ STEP 9: Compare with baseline algorithm
   ├─ Run reference implementation on same env
   ├─ Does reference get better reward?
   ├─ YES → Your implementation has a bug
   ├─ NO → Problem is inherent to algorithm or environment
   └─ This isolates: Implementation issue vs fundamental difficulty
```

**ROOT CAUSES in order of likelihood:**

1. **Exploration insufficient** (30% of cases)
2. **Training not long enough** (25% of cases)
3. **Reward hacking** (20% of cases)
4. **Network too small** (12% of cases)
5. **Observation insufficient** (8% of cases)
6. **Algorithm mismatch** (5% of cases)

---

## Part 3: What to Check First

### Critical Checks (Do These First)

#### Check 1: Reward Scale Analysis

**Why**: Reward scale is the MOST COMMON source of RL failures.

```python
# DIAGNOSTIC SCRIPT
import numpy as np

# Collect rewards from random policy
rewards = []
for episode in range(100):
    state = env.reset()
    for step in range(1000):
        action = env.action_space.sample()  # Random action
        state, reward, done, _ = env.step(action)
        rewards.append(reward)
        if done:
            break

rewards = np.array(rewards)

print(f"Reward statistics from random policy:")
print(f"  Min: {rewards.min()}")
print(f"  Max: {rewards.max()}")
print(f"  Mean: {rewards.mean()}")
print(f"  Std: {rewards.std()}")
print(f"  Range: [{rewards.min()}, {rewards.max()}]")

# RED FLAGS
if abs(rewards.max()) > 100 or abs(rewards.min()) > 100:
    print("⚠️ RED FLAG: Rewards >> 1, normalize them!")

if rewards.std() > 10:
    print("⚠️ RED FLAG: High reward variance, normalize or clip")

if rewards.mean() == rewards.max():
    print("⚠️ RED FLAG: Constant rewards, no signal to learn from!")

if (rewards > 1).any() and (rewards < -1).any():
    print("✓ Reward scale looks reasonable ([-1, 1] range)")
```

**Action if scale is wrong:**

```python
# Normalize to [-1, 1]
reward = reward / max(abs(rewards.max()), abs(rewards.min()))

# Or clip
reward = np.clip(reward, -1, 1)

# Or shift and scale
reward = 2 * (reward - rewards.min()) / (rewards.max() - rewards.min()) - 1
```

#### Check 2: Environment Sanity Check

**Why**: Broken environment → no algorithm will work.

```python
# DIAGNOSTIC SCRIPT
def sanity_check_env(env, num_episodes=5):
    """Quick check if environment is sane."""

    for episode in range(num_episodes):
        state = env.reset()
        print(f"\nEpisode {episode}:")
        print(f"  Initial state shape: {state.shape}, dtype: {state.dtype}")
        print(f"  Initial state range: [{state.min()}, {state.max()}]")

        for step in range(10):
            action = env.action_space.sample()
            next_state, reward, done, info = env.step(action)

            print(f"  Step {step}: action={action}, reward={reward}, done={done}")
            print(f"    State shape: {next_state.shape}, range: [{next_state.min()}, {next_state.max()}]")

            # Check for NaN
            if np.isnan(next_state).any() or np.isnan(reward):
                print(f"    ⚠️ NaN detected!")

            # Check for reasonable values
            if np.abs(next_state).max() > 1e6:
                print(f"    ⚠️ State explosion (values > 1e6)")

            if done:
                break

    print("\n✓ Environment check complete")

sanity_check_env(env)
```

**RED FLAGS:**

- NaN or inf in observations/rewards
- State values exploding (> 1e6)
- Reward always same (no signal)
- Done flag never true (infinite episodes)
- State never changes despite actions

#### Check 3: Can You Beat It Manually?

**Why**: If human can't solve it, agent won't either (unless reward hacking).

```python
# Manual policy: Hardcoded behavior
def manual_policy(state):
    # Example for CartPole: if pole tilting right, push right
    if state[2] > 0:  # angle > 0
        return 1  # Push right
    else:
        return 0  # Push left

# Test manual policy
total_reward = 0
for episode in range(10):
    state = env.reset()
    for step in range(500):
        action = manual_policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

avg_reward = total_reward / 10
print(f"Manual policy average reward: {avg_reward}")

# If avg_reward > 0: Environment is learnable
# If avg_reward ≤ 0: Environment is broken or impossible
```

#### Check 4: Observation Normalization

**Why**: Non-normalized observations cause learning problems.

```python
# Check if observations are normalized
for episode in range(10):
    state = env.reset()
    print(f"Episode {episode}: state range [{state.min()}, {state.max()}]")

    # For images: should be [0, 1] or [-1, 1]
    # For physical states: should be roughly [-1, 1]

    if state.min() < -10 or state.max() > 10:
        print("⚠️ Observations not normalized!")
        # Solution:
        state = state / np.abs(state).max()  # Normalize
```

---

## Part 4: Common RL Bugs Catalog

### Bug 1: Reward Scale > 1

**Symptom**: Training unstable, loss spikes, agent doesn't learn

**Root Cause**: Gradients too large due to reward scale

**Code Example**:

```python
# WRONG: Reward in [0, 1000]
reward = success_count * 1000

# CORRECT: Normalize to [-1, 1]
reward = success_count * 1000
reward = reward / max_possible_reward  # Result: [-1, 1]
```

**Fix**: Divide rewards by max possible value

**Detection**:

```python
rewards = [collect 100 episodes]
if max(abs(r) for r in rewards) > 1:
    print("⚠️ Reward scale issue detected")
```

---

### Bug 2: Environment Reset Broken

**Symptom**: Agent learns initial state but can't adapt

**Root Cause**: Reset doesn't randomize initial state or returns same state

**Code Example**:

```python
# WRONG: Reset always same state
def reset(self):
    self.state = np.array([0, 0, 0, 0])  # Always [0,0,0,0]
    return self.state

# CORRECT: Reset randomizes initial state
def reset(self):
    self.state = np.random.uniform(-0.1, 0.1, size=4)  # Random
    return self.state
```

**Fix**: Make reset() randomize initial state

**Detection**:

```python
states = [env.reset() for _ in range(10)]
if len(set(map(tuple, states))) == 1:
    print("⚠️ Reset broken, always same state")
```

---

### Bug 3: Observation Insufficient (Partial Observability)

**Symptom**: Agent can't learn because it doesn't see enough

**Root Cause**: Observation missing velocity, derivatives, or temporal info

**Code Example**:

```python
# WRONG: Only position, no velocity
state = np.array([position])  # Can't infer velocity from position alone

# CORRECT: Position + velocity
state = np.array([position, velocity])

# WRONG for images: Single frame
observation = env.render()  # Single frame, no temporal info

# CORRECT for images: Stacked frames
frames = [frame_t-3, frame_t-2, frame_t-1, frame_t]  # 4 frames
observation = np.stack(frames, axis=-1)  # Shape: (84, 84, 4)
```

**Fix**: Add missing information to observation

**Detection**:

```python
# If agent converges to bad performance despite long training
# Check: Can you compute optimal action from observation?
# If no: Observation is insufficient
```

---

### Bug 4: Reward Always Same (No Signal)

**Symptom**: Loss decreases but doesn't improve over time, reward flat

**Root Cause**: Reward is constant or nearly constant

**Code Example**:

```python
# WRONG: Constant reward
reward = 1.0  # Every step gets +1, no differentiation

# CORRECT: Differentiate good and bad outcomes
if reached_goal:
    reward = 1.0
else:
    reward = 0.0  # Or -0.1 for living cost
```

**Fix**: Ensure reward differentiates outcomes

**Detection**:

```python
rewards = [collect random policy rewards]
if rewards.std() < 0.01:
    print("⚠️ Reward has no variance, no signal to learn")
```

---

### Bug 5: Learning Rate Too High

**Symptom**: Loss oscillates or explodes, training unstable

**Root Cause**: Gradient updates too large, overshooting optimum

**Code Example**:

```python
# WRONG: Learning rate 1e-2 (too high)
optimizer = Adam(model.parameters(), lr=1e-2)

# CORRECT: Learning rate 3e-4 (safe default)
optimizer = Adam(model.parameters(), lr=3e-4)
```

**Fix**: Reduce learning rate by 2-5×

**Detection**:

```python
# Watch loss first 100 steps
# If loss increases first step: LR too high
# If loss decreases but oscillates: LR probably high
```

---

### Bug 6: Learning Rate Too Low

**Symptom**: Agent learns very slowly, training takes forever

**Root Cause**: Gradient updates too small, learning crawls

**Code Example**:

```python
# WRONG: Learning rate 1e-6 (too low)
optimizer = Adam(model.parameters(), lr=1e-6)

# CORRECT: Learning rate 3e-4
optimizer = Adam(model.parameters(), lr=3e-4)
```

**Fix**: Increase learning rate by 2-5×

**Detection**:

```python
# Training curve increases very slowly
# If training 1M steps and reward barely improved: LR too low
```

---

### Bug 7: No Exploration Decay

**Symptom**: Agent learns but remains noisy, doesn't fully exploit

**Root Cause**: Exploration (epsilon or entropy) not decaying

**Code Example**:

```python
# WRONG: Constant epsilon
epsilon = 0.3  # Forever

# CORRECT: Decay epsilon
epsilon = epsilon_linear(step, total_steps=1_000_000,
                         epsilon_start=1.0, epsilon_end=0.01)
```

**Fix**: Add exploration decay schedule

**Detection**:

```python
# Plot entropy or epsilon over training
# Should show clear decay from high to low
# If flat: not decaying
```

---

### Bug 8: Exploration Decay Too Fast

**Symptom**: Agent plateaus early, stuck in local optimum

**Root Cause**: Exploration stops before finding good policy

**Code Example**:

```python
# WRONG: Decays to zero in 10k steps (for 1M step training)
epsilon = 0.99 ** (step / 100)  # Reaches 0 too fast

# CORRECT: Decays over full training
epsilon = epsilon_linear(step, total_steps=1_000_000,
                         epsilon_start=1.0, epsilon_end=0.01)
```

**Fix**: Use longer decay schedule

**Detection**:

```python
# Plot epsilon over training
# Should reach final value at 50-80% through training
# Not at 5%
```

---

### Bug 9: Reward Hacking

**Symptom**: Agent achieves high reward but behavior is useless

**Root Cause**: Agent found way to game reward not aligned with intent

**Code Example**:

```python
# WRONG: Reward for just staying alive
reward = 1.0  # Every timestep
# Agent learns: Stay in corner, don't move, get infinite reward

# CORRECT: Reward for progress + living cost
position_before = self.state[0]
self.state = compute_next_state(...)
position_after = self.state[0]
progress = position_after - position_before

reward = progress - 0.01  # Progress bonus, living cost
```

**Fix**: Reshape reward to align with intent

**Detection**:

```python
# Visualize agent behavior
# If behavior weird but reward high: hacking
# If reward increases but task performance bad: hacking
```

---

### Bug 10: Testing with Exploration

**Symptom**: Test performance much worse than training, high variance

**Root Cause**: Using stochastic policy at test time

**Code Example**:

```python
# WRONG: Test with epsilon > 0
for test_episode in range(100):
    action = epsilon_greedy(q_values, epsilon=0.05)  # Wrong!
    # Agent still explores at test

# CORRECT: Test greedy
for test_episode in range(100):
    action = np.argmax(q_values)  # Deterministic
```

**Fix**: Use greedy/deterministic policy at test time

**Detection**:

```python
# Test reward variance high?
# Test reward < train reward?
# Check: Are you using exploration at test time?
```

---

## Part 5: Logging and Monitoring

### What Metrics to Track

```python
# Minimal set of metrics for RL debugging
class RLLogger:
    def __init__(self):
        self.episode_rewards = []
        self.policy_losses = []
        self.value_losses = []
        self.entropies = []
        self.gradient_norms = []

    def log_episode(self, episode_reward):
        self.episode_rewards.append(episode_reward)

    def log_losses(self, policy_loss, value_loss, entropy):
        self.policy_losses.append(policy_loss)
        self.value_losses.append(value_loss)
        self.entropies.append(entropy)

    def log_gradient_norm(self, norm):
        self.gradient_norms.append(norm)

    def plot_training(self):
        """Visualize training progress."""
        # Plot 1: Episode rewards over time (smoothed)
        # Plot 2: Policy and value losses
        # Plot 3: Entropy (should decay)
        # Plot 4: Gradient norms
        pass
```

### What Each Metric Means

#### Metric 1: Episode Reward

**What to look for**:

- Should trend upward over time
- Should have decreasing variance (less oscillation)
- Slight noise is normal

**Red flags**:

- Flat line: Not learning
- Downward trend: Getting worse
- Wild oscillations: Instability or unlucky randomness

**Code**:

```python
rewards = agent.get_episode_rewards()
reward_smoothed = np.convolve(rewards, np.ones(100)/100, mode='valid')
plt.plot(reward_smoothed)  # Smooth to see trend
```

#### Metric 2: Policy Loss

**What to look for**:

- Should decrease over training
- Decrease should smooth out (not oscillating)

**Red flags**:

- Loss increasing: Learning rate too high
- Loss oscillating: Learning rate too high or reward scale wrong
- Loss = 0: Policy not updating

**Code**:

```python
if policy_loss > policy_loss_prev:
    print("⚠️ Policy loss increased, LR might be too high")
```

#### Metric 3: Value Loss (for critic-based methods)

**What to look for**:

- Should decrease initially, then plateau
- Should not oscillate heavily

**Red flags**:

- Loss exploding: LR too high
- Loss not changing: Not updating

**Code**:

```python
value_loss_smoothed = np.convolve(value_losses, np.ones(100)/100)
if value_loss_smoothed[-1] > value_loss_smoothed[-100]:
    print("⚠️ Value loss increasing recently")
```

#### Metric 4: Entropy (Policy Randomness)

**What to look for**:

- Should start high (exploring)
- Should decay to low (exploiting)
- Clear downward trend

**Red flags**:

- Entropy always high: Too much exploration
- Entropy drops to zero: Over-exploiting
- No decay: Entropy not decreasing

**Code**:

```python
if entropy[-1] > entropy[-100]:
    print("⚠️ Entropy increasing, exploration not decaying")
```

#### Metric 5: Gradient Norms

**What to look for**:

- Should stay roughly constant over training
- Typical range: 0.1 to 10

**Red flags**:

- Gradient norms > 100: Exploding gradients
- Gradient norms < 0.001: Vanishing gradients
- Sudden spikes: Outlier data or numerical issue

**Code**:

```python
total_norm = 0
for p in model.parameters():
    param_norm = p.grad.norm(2)
    total_norm += param_norm ** 2
total_norm = total_norm ** 0.5

if total_norm > 100:
    print("⚠️ Gradient explosion detected")
```

### Visualization Script

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_rl_training(rewards, policy_losses, value_losses, entropies):
    """Plot training metrics for RL debugging."""

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Plot 1: Episode rewards
    ax = axes[0, 0]
    ax.plot(rewards, alpha=0.3, label='Episode reward')
    reward_smooth = np.convolve(rewards, np.ones(100)/100, mode='valid')
    ax.plot(range(100, len(rewards)), reward_smooth, label='Smoothed (100 episodes)')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reward')
    ax.set_title('Episode Rewards Over Time')
    ax.legend()
    ax.grid()

    # Plot 2: Policy loss
    ax = axes[0, 1]
    ax.plot(policy_losses, alpha=0.3)
    loss_smooth = np.convolve(policy_losses, np.ones(100)/100, mode='valid')
    ax.plot(range(100, len(policy_losses)), loss_smooth, label='Smoothed')
    ax.set_xlabel('Step')
    ax.set_ylabel('Policy Loss')
    ax.set_title('Policy Loss Over Time')
    ax.legend()
    ax.grid()

    # Plot 3: Entropy
    ax = axes[1, 0]
    ax.plot(entropies, label='Policy entropy')
    ax.set_xlabel('Step')
    ax.set_ylabel('Entropy')
    ax.set_title('Policy Entropy (Should Decrease)')
    ax.legend()
    ax.grid()

    # Plot 4: Value loss
    ax = axes[1, 1]
    ax.plot(value_losses, alpha=0.3)
    loss_smooth = np.convolve(value_losses, np.ones(100)/100, mode='valid')
    ax.plot(range(100, len(value_losses)), loss_smooth, label='Smoothed')
    ax.set_xlabel('Step')
    ax.set_ylabel('Value Loss')
    ax.set_title('Value Loss Over Time')
    ax.legend()
    ax.grid()

    plt.tight_layout()
    plt.show()
```

---

## Part 6: Common Pitfalls and Red Flags

### Pitfall 1: "Bigger Network = Better Learning"

**Wrong**: Oversized networks overfit and learn slowly

**Right**: Start with small network (2-3 hidden layers, 64-256 units)

**Red Flag**: Network has > 10M parameters for simple task

**Fix**:

```python
# Too big
model = nn.Sequential(
    nn.Linear(4, 1024),
    nn.ReLU(),
    nn.Linear(1024, 1024),
    nn.Linear(1024, 2)
)

# Right size
model = nn.Sequential(
    nn.Linear(4, 128),
    nn.ReLU(),
    nn.Linear(128, 128),
    nn.Linear(128, 2)
)
```

---

### Pitfall 2: "Random Seed Doesn't Matter"

**Wrong**: Different seeds give very different results (indicates instability)

**Right**: Results should be consistent across seeds (within reasonable variance)

**Red Flag**: Reward varies by 50%+ across 5 seeds

**Fix**:

```python
# Test across multiple seeds
rewards_by_seed = []
for seed in range(5):
    np.random.seed(seed)
    torch.manual_seed(seed)
    reward = train_agent(seed)
    rewards_by_seed.append(reward)

print(f"Mean: {np.mean(rewards_by_seed)}, Std: {np.std(rewards_by_seed)}")
if np.std(rewards_by_seed) > 0.5 * np.mean(rewards_by_seed):
    print("⚠️ High variance across seeds, training unstable")
```

---

### Pitfall 3: "Skip Observation Normalization"

**Wrong**: Non-normalized observations (scale [-1e6, 1e6])

**Right**: Normalized observations (scale [-1, 1])

**Red Flag**: State values > 100 or < -100

**Fix**:

```python
# Normalize images
observation = observation.astype(np.float32) / 255.0

# Normalize states
observation = (observation - observation_mean) / observation_std

# Or standardize on-the-fly
normalized_obs = (obs - running_mean) / (running_std + 1e-8)
```

---

### Pitfall 4: "Ignore the Reward Curve Shape"

**Wrong**: Only look at final reward, ignore curve shape

**Right**: Curve shape tells you what's wrong

**Red Flag**: Curve shapes indicate:

- Flat then sudden jump: Long exploration, then found policy
- Oscillating: Unstable learning
- Decreasing after peak: Catastrophic forgetting

**Fix**:

```python
# Look at curve shape
if reward_curve is flat:
    print("Not learning, check environment/reward")
elif reward_curve oscillates:
    print("Unstable, check LR or reward scale")
elif reward_curve peaks then drops:
    print("Overfitting or exploration decay wrong")
```

---

### Pitfall 5: "Skip the Random Baseline Check"

**Wrong**: Train agent without knowing what random baseline is

**Right**: Always compute random baseline first

**Red Flag**: Agent barely beats random (within 5% of baseline)

**Fix**:

```python
# Compute random baseline
random_rewards = []
for _ in range(100):
    state = env.reset()
    episode_reward = 0
    for step in range(1000):
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        episode_reward += reward
        if done:
            break
    random_rewards.append(episode_reward)

random_baseline = np.mean(random_rewards)
print(f"Random baseline: {random_baseline}")

# Compare agent
agent_reward = train_agent()
improvement = (agent_reward - random_baseline) / random_baseline
print(f"Agent improvement: {improvement*100}%")
```

---

### Pitfall 6: "Changing Multiple Hyperparameters at Once"

**Wrong**: Change 5 things, training breaks, don't know which caused it

**Right**: Change one thing at a time, test, measure, iterate

**Red Flag**: Code has "TUNING" comments with 10 simultaneous changes

**Fix**:

```python
# Scientific method for debugging
def debug_lr():
    for lr in [1e-5, 1e-4, 1e-3, 1e-2]:
        reward = train_with_lr(lr)
        print(f"LR={lr}: Reward={reward}")
        # Only change LR, keep everything else same

def debug_batch_size():
    for batch in [32, 64, 128, 256]:
        reward = train_with_batch(batch)
        print(f"Batch={batch}: Reward={reward}")
        # Only change batch, keep everything else same
```

---

### Pitfall 7: "Using Training Metrics to Judge Performance"

**Wrong**: Trust training reward, test once at the end

**Right**: Monitor test reward during training (with exploration off)

**Red Flag**: Training reward high, test reward low (overfitting)

**Fix**:

```python
# Evaluate with greedy policy (no exploration)
def evaluate(agent, num_episodes=10):
    episode_rewards = []
    for _ in range(num_episodes):
        state = env.reset()
        episode_reward = 0
        for step in range(1000):
            action = agent.act(state, explore=False)  # Greedy
            state, reward, done, _ = env.step(action)
            episode_reward += reward
            if done:
                break
        episode_rewards.append(episode_reward)
    return np.mean(episode_rewards)

# Monitor during training
for step in range(total_steps):
    train_agent_step()

    if step % 10000 == 0:
        test_reward = evaluate(agent)  # Evaluate periodically
        print(f"Step {step}: Test reward={test_reward}")
```

---

## Part 7: Red Flags Checklist

```
CRITICAL RED FLAGS (Stop and debug immediately):

[ ] NaN in loss or rewards
    → Check: reward scale, gradients, network outputs

[ ] Gradient norms > 100 (exploding)
    → Check: Enable gradient clipping, reduce LR

[ ] Gradient norms < 1e-4 (vanishing)
    → Check: Increase LR, check network initialization

[ ] Reward always same
    → Check: Is reward function broken? No differentiation?

[ ] Agent never improves beyond random baseline
    → Check: Reward scale, environment, observation, exploration

[ ] Loss oscillates wildly
    → Check: Learning rate (likely too high), reward scale

[ ] Episode length decreases over training
    → Check: Agent learning bad behavior, poor reward shaping

[ ] Test reward >> training reward
    → Check: Training is lucky, test is representative

[ ] Training gets worse after improving
    → Check: Catastrophic forgetting, stability issue


IMPORTANT RED FLAGS (Debug within a few training runs):

[ ] Entropy not decaying (always high)
    → Check: Entropy regularization, exploration decay

[ ] Entropy goes to zero early
    → Check: Entropy coefficient too low, exploration too aggressive

[ ] Variance across seeds > 50% of mean
    → Check: Training is unstable or lucky, try more seeds

[ ] Network weights not changing
    → Check: Gradient zero, LR zero, network not connected

[ ] Loss = 0 (perfect fit)
    → Check: Network overfitting, reward too easy


MINOR RED FLAGS (Watch for patterns):

[ ] Training slower than expected
    → Check: LR too low, batch size too small, network too small

[ ] Occasional loss spikes
    → Check: Outlier data, reward outliers, clipping needed

[ ] Reward variance high
    → Check: Normal if environment stochastic, check if aligns with intent

[ ] Agent behavior seems random even late in training
    → Check: Entropy not decaying, exploration not stopping
```

---

## Part 8: Rationalization Resistance

| Rationalization | Reality | Counter-Guidance |
|-----------------|---------|------------------|
| "Higher learning rate will speed up learning" | Can cause instability, often slows learning | Start with 3e-4, measure effect, don't assume |
| "Bigger network always learns better" | Oversized networks overfit, slow training | Start small (64-256 units), increase only if needed |
| "Random seed doesn't matter, RL is random anyway" | High variance indicates instability, not inherent randomness | Run 5+ seeds, variance should be low, not high |
| "I'll try all hyperparameters (grid search)" | Combinatorial explosion, wastes time, no diagnosis | Check environment/reward FIRST, then tune one param at a time |
| "Adding regularization helps unstable training" | Regularization is for overfitting, not instability | Instability usually LR or reward scale, not overfitting |
| "My algorithm is broken" | 80% chance environment, reward, or observation is broken | Check those FIRST before blaming algorithm |
| "More training always helps" | If reward plateaus, more training won't help | Check if training converged, if not why |
| "Skip observation normalization, network will learn to normalize" | Network should not spend capacity learning normalization | Normalize observations before network |
| "Test with epsilon > 0 to reduce variance" | Test should use learned policy, exploration harms test | Use greedy policy at test time |
| "If loss doesn't decrease, algorithm is broken" | More likely: reward scale wrong, gradient clipping needed | Check reward scale, enable gradient clipping before changing algorithm |

---

## Key Takeaways

1. **Follow the systematic process**: Don't random tweak. Check environment → reward → observation → algorithm.

2. **80/20 rule**: Most failures are in environment, reward, or observation. Check those first.

3. **Reward scale is critical**: Most common bug. Normalize to [-1, 1].

4. **Diagnosis trees**: Use them. Different symptoms have different root causes.

5. **Metrics tell you everything**: Loss, entropy, gradient norms reveal what's wrong.

6. **Rationalization is the enemy**: Don't assume, measure. Plot curves, check outputs, verify.

7. **Simple environment first**: If agent can't learn CartPole, bigger environment won't help.

8. **One seed is not enough**: Run 5+ seeds, look at variance, not just mean.

This skill is about **systematic debugging**, not random tweaking. Apply the framework, follow diagnosis trees, and you'll find the bug.
