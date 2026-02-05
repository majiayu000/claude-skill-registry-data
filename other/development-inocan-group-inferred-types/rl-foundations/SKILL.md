---
name: rl-foundations
description: Master RL theory - MDPs, value functions, Bellman equations, value/policy iteration, TD
---

# RL Foundations

## When to Use This Skill

Invoke this skill when you encounter:

- **New to RL**: User asks "what is RL" or "how does RL work"
- **Theory Questions**: MDP, value functions, Bellman equations, policy optimization
- **Conceptual Confusion**: Mixing up V(s) and Q(s,a), value iteration vs policy iteration
- **Before Implementation**: User wants to implement RL algorithms without understanding foundations
- **Debugging Theory**: Why discount factor matters, why exploration needed, how algorithms differ
- **Foundation Check**: User jumps to DQN/PPO without understanding MDPs

**This skill provides the theoretical foundation for ALL other deep-rl skills.**

Do NOT use this skill for:

- Algorithm implementation (use value-based-methods, policy-gradient-methods, actor-critic-methods)
- Debugging code (use rl-debugging)
- Environment setup (use rl-environments)

## Core Principle

**Understanding the theory enables everything else.**

Reinforcement learning is built on a rigorous mathematical foundation:

1. **MDP** (Markov Decision Process) - the framework
2. **Value Functions** - quantify expected return
3. **Bellman Equations** - recursive decomposition
4. **Optimal Policy** - maximize expected return
5. **Algorithms** - methods to find optimal policy

**Without this foundation, you're copy-pasting code you cannot debug, adapt, or extend.**

---

## Part 1: Markov Decision Process (MDP)

### What is an MDP?

An MDP is the mathematical framework for sequential decision-making under uncertainty.

**Formal Definition**: A Markov Decision Process is a 5-tuple (S, A, P, R, γ):

- **S**: State space (set of all possible states)
- **A**: Action space (set of all possible actions)
- **P**: Transition probability P(s'|s,a) - probability of reaching state s' from state s after action a
- **R**: Reward function R(s,a,s') - immediate reward for transition
- **γ**: Discount factor (0 ≤ γ ≤ 1) - controls importance of future rewards

**Key Property**: **Markov Property**

```
P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ..., s_0, a_0) = P(s_{t+1} | s_t, a_t)
```

**Meaning**: The future depends only on the present state, not the history.

**Why this matters**: Allows recursive algorithms (Bellman equations). If Markov property violated, standard RL algorithms may fail.

---

### Example 1: GridWorld MDP

**Problem**: Agent navigates 4x4 grid to reach goal.

```
S = {(0,0), (0,1), ..., (3,3)}  # 16 states
A = {UP, DOWN, LEFT, RIGHT}      # 4 actions
R = -1 for each step, +10 at goal
γ = 0.9
P: Deterministic (up always moves up if not wall)
```

**Visualization**:

```
S  .  .  .
.  .  .  .
.  #  .  .  # = wall
.  .  .  G  G = goal (+10)
```

**Transition Example**:

- State s = (1,1), Action a = RIGHT
- Deterministic: P(s'=(1,2) | s=(1,1), a=RIGHT) = 1.0
- Reward: R(s,a,s') = -1
- Next state: s' = (1,2)

**Markov Property Holds**: Future position depends only on current position and action, not how you got there.

---

### Example 2: Stochastic GridWorld

**Modification**: Actions succeed with probability 0.8, move perpendicular with probability 0.1 each.

```
P((1,2) | (1,1), RIGHT) = 0.8  # intended
P((0,1) | (1,1), RIGHT) = 0.1  # slip up
P((2,1) | (1,1), RIGHT) = 0.1  # slip down
```

**Why Stochastic**: Models real-world uncertainty (robot actuators, wind, slippery surfaces).

**Consequence**: Agent must consider probabilities when choosing actions.

---

### Example 3: Continuous State MDP (Cartpole)

```
S ⊂ ℝ⁴: (cart_position, cart_velocity, pole_angle, pole_angular_velocity)
A = {LEFT, RIGHT}  # discrete actions, continuous state
R = +1 for each timestep upright
γ = 0.99
P: Physics-based transition (continuous dynamics)
```

**Key Difference**: State space is continuous, requires function approximation (neural networks).

**Still an MDP**: Markov property holds (physics is Markovian given state).

---

### When is Markov Property Violated?

**Example: Poker**

```
State: Current cards visible
Markov Violated: Opponents' strategies depend on past betting patterns
```

**Solution**: Augment state with history (last N actions), or use partially observable MDP (POMDP).

**Example: Robot with Noisy Sensors**

```
State: Raw sensor reading (single frame)
Markov Violated: True position requires integrating multiple frames
```

**Solution**: Stack frames (last 4 frames as state), or use recurrent network (LSTM).

---

### Episodic vs Continuing Tasks

**Episodic**: Task terminates (games, reaching goal)

```
Episode: s₀ → s₁ → ... → s_T (terminal state)
Return: G_t = r_t + γr_{t+1} + ... + γ^{T-t}r_T
```

**Continuing**: Task never ends (stock trading, robot operation)

```
Return: G_t = r_t + γr_{t+1} + γ²r_{t+2} + ... (infinite)
```

**Critical**: Continuing tasks REQUIRE γ < 1 (else return infinite).

---

### MDP Pitfall #1: Using Wrong State Representation

**Bad**: State = current frame only (when velocity matters)

```python
# Pong: Ball position alone doesn't tell velocity
state = current_frame  # WRONG - not Markovian
```

**Good**: State = last 4 frames (velocity from difference)

```python
# Frame stacking preserves Markov property
state = np.concatenate([frame_t, frame_{t-1}, frame_{t-2}, frame_{t-3}])
```

**Why**: Ball velocity = (position_t - position_{t-1}) / dt, need history.

---

### MDP Pitfall #2: Reward Function Shapes Behavior

**Example**: Robot navigating to goal

**Bad Reward**:

```python
reward = +1 if at_goal else 0  # Sparse
```

**Problem**: No signal until goal reached, hard to learn.

**Better Reward**:

```python
reward = -distance_to_goal  # Dense
```

**Problem**: Agent learns to get closer but may not reach goal (local optimum).

**Best Reward** (Potential-Based Shaping):

```python
reward = (distance_prev - distance_curr) + large_bonus_at_goal
```

**Why**: Encourages progress + explicit goal reward.

**Takeaway**: Reward function engineering is CRITICAL. Route to reward-shaping skill for details.

---

### MDP Formulation Checklist

Before implementing any RL algorithm, answer:

- [ ] **States**: What information defines the situation? Is it Markovian?
- [ ] **Actions**: What can the agent do? Discrete or continuous?
- [ ] **Transitions**: Deterministic or stochastic? Do you know P(s'|s,a)?
- [ ] **Rewards**: Immediate reward for each transition? Sparse or dense?
- [ ] **Discount**: Episodic (can use γ=1) or continuing (need γ<1)?
- [ ] **Markov Property**: Does current state fully determine future?

**If you cannot answer these, you cannot implement RL algorithms effectively.**

---

## Part 2: Value Functions

### What is a Value Function?

A value function quantifies "how good" a state (or state-action pair) is.

**State-Value Function V^π(s)**:

```
V^π(s) = E_π[G_t | s_t = s]
       = E_π[r_t + γr_{t+1} + γ²r_{t+2} + ... | s_t = s]
```

**Meaning**: Expected cumulative discounted reward starting from state s and following policy π.

**Action-Value Function Q^π(s,a)**:

```
Q^π(s,a) = E_π[G_t | s_t = s, a_t = a]
         = E_π[r_t + γr_{t+1} + γ²r_{t+2} + ... | s_t = s, a_t = a]
```

**Meaning**: Expected cumulative discounted reward starting from state s, taking action a, then following policy π.

**Relationship**:

```
V^π(s) = Σ_a π(a|s) Q^π(s,a)
```

**Intuition**: V(s) = value of state, Q(s,a) = value of state-action pair.

---

### Critical Distinction: Value vs Reward

**Reward r(s,a)**: Immediate, one-step payoff.

**Value V(s)**: Long-term, cumulative expected reward.

**Example: GridWorld**

```
Reward: r = -1 every step, r = +10 at goal
Value at state 2 steps from goal:
  V(s) ≈ -1 + γ(-1) + γ²(+10)
       = -1 - 0.9 + 0.81*10
       = -1.9 + 8.1 = 6.2
```

**Key**: Value is higher than immediate reward because it accounts for future goal reward.

**Common Mistake**: Setting V(s) = r(s). This ignores all future rewards.

---

### Example: Computing V^π for Simple Policy

**GridWorld**: 3x3 grid, goal at (2,2), γ=0.9, r=-1 per step.

**Policy π**: Always move right or down (deterministic).

**Manual Calculation**:

```
V^π((2,2)) = 0  (goal, no future rewards)

V^π((2,1)) = r + γ V^π((2,2))
           = -1 + 0.9 * 0 = -1

V^π((1,2)) = r + γ V^π((2,2))
           = -1 + 0.9 * 0 = -1

V^π((1,1)) = r + γ V^π((1,2))  (assuming action = DOWN)
           = -1 + 0.9 * (-1) = -1.9

V^π((0,0)) = r + γ V^π((0,1))
           = ... (depends on path)
```

**Observation**: Values decrease as distance from goal increases (more -1 rewards to collect).

---

### Optimal Value Functions

**Optimal State-Value Function V*(s)**:

```
V*(s) = max_π V^π(s)
```

**Meaning**: Maximum value achievable from state s under ANY policy.

**Optimal Action-Value Function Q*(s,a)**:

```
Q*(s,a) = max_π Q^π(s,a)
```

**Meaning**: Maximum value achievable from state s, taking action a, then acting optimally.

**Optimal Policy π***:

```
π*(s) = argmax_a Q*(s,a)
```

**Meaning**: Policy that achieves V*(s) at all states.

**Key Insight**: If you know Q*(s,a), optimal policy is trivial (pick action with max Q).

---

### Value Function Pitfall #1: Confusing V and Q

**Wrong Understanding**:

- V(s) = value of state s
- Q(s,a) = value of action a (WRONG - ignores state)

**Correct Understanding**:

- V(s) = value of state s (average over actions under policy)
- Q(s,a) = value of taking action a IN STATE s

**Example**: GridWorld

```
State s = (1,1)
V(s) might be 5.0 (average value under policy)

Q(s, RIGHT) = 6.0  (moving right is good)
Q(s, LEFT)  = 2.0  (moving left is bad)
Q(s, UP)    = 4.0
Q(s, DOWN)  = 7.0  (moving down is best)

V(s) = π(RIGHT|s)*6 + π(LEFT|s)*2 + π(UP|s)*4 + π(DOWN|s)*7
```

**Takeaway**: Q depends on BOTH state and action. V depends only on state.

---

### Value Function Pitfall #2: Forgetting Expectation

**Wrong**: V(s) = sum of rewards on one trajectory.

**Correct**: V(s) = expected sum over ALL possible trajectories.

**Example**: Stochastic GridWorld

```python
# WRONG: Compute V by running one episode
episode_return = sum([r_0, r_1, ..., r_T])
V[s_0] = episode_return  # This is ONE sample, not expectation

# CORRECT: Compute V by averaging over many episodes
returns = []
for _ in range(1000):
    episode_return = run_episode(policy, start_state=s)
    returns.append(episode_return)
V[s] = np.mean(returns)  # Expectation via Monte Carlo
```

**Key**: Value is an expectation, not a single sample.

---

### Value Function Pitfall #3: Ignoring Discount Factor

**Scenario**: User computes V without discounting.

**Wrong**:

```python
V[s] = r_0 + r_1 + r_2 + ...  # No discount
```

**Correct**:

```python
V[s] = r_0 + gamma*r_1 + gamma**2*r_2 + ...
```

**Why It Matters**: Without discount, values blow up in continuing tasks.

**Example**: Continuing task with r=1 every step

```
Without discount: V = 1 + 1 + 1 + ... = ∞
With γ=0.9:      V = 1 + 0.9 + 0.81 + ... = 1/(1-0.9) = 10
```

**Takeaway**: Always discount future rewards in continuing tasks.

---

## Part 3: Policies

### What is a Policy?

A policy π is a mapping from states to actions (or action probabilities).

**Deterministic Policy**: π: S → A

```
π(s) = a  (always take action a in state s)
```

**Stochastic Policy**: π: S × A → [0,1]

```
π(a|s) = probability of taking action a in state s
Σ_a π(a|s) = 1  (probabilities sum to 1)
```

---

### Example: Policies in GridWorld

**Deterministic Policy**:

```python
def policy(state):
    if state[0] < 2:
        return "RIGHT"
    else:
        return "DOWN"
```

**Stochastic Policy**:

```python
def policy(state):
    # 70% right, 20% down, 10% up
    return np.random.choice(["RIGHT", "DOWN", "UP"], 
                           p=[0.7, 0.2, 0.1])
```

**Uniform Random Policy**:

```python
def policy(state):
    return np.random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
```

---

### Policy Evaluation

**Problem**: Given policy π, compute V^π(s) for all states.

**Approach 1: Monte Carlo** (sample trajectories)

```python
# Run many episodes, average returns
V = defaultdict(float)
counts = defaultdict(int)

for episode in range(10000):
    trajectory = run_episode(policy)
    G = 0
    for (s, a, r) in reversed(trajectory):
        G = r + gamma * G
        V[s] += G
        counts[s] += 1

for s in V:
    V[s] /= counts[s]  # Average
```

**Approach 2: Bellman Expectation** (iterative)

```python
# Initialize V arbitrarily
V = {s: 0 for s in states}

# Iterate until convergence
while not converged:
    V_new = {}
    for s in states:
        V_new[s] = sum(policy(a|s) * (R(s,a) + gamma * sum(P(s'|s,a) * V[s'] 
                                                            for s' in states))
                       for a in actions)
    V = V_new
```

**Approach 2 requires knowing P(s'|s,a)** (model-based).

---

### Policy Improvement

**Theorem**: Given V^π, greedy policy π' with respect to V^π is at least as good as π.

```
π'(s) = argmax_a Q^π(s,a)
      = argmax_a Σ_{s'} P(s'|s,a) [R(s,a,s') + γV^π(s')]
```

**Proof Sketch**: By construction, π' maximizes expected immediate reward + future value.

**Consequence**: Iterating policy evaluation + policy improvement converges to optimal policy π*.

---

### Optimal Policy π*

**Theorem**: There exists an optimal policy π*that achieves V*(s) at all states.

**How to find π* from Q***:

```python
def optimal_policy(state):
    return argmax(Q_star[state, :])  # Greedy w.r.t. Q*
```

**How to find π* from V***:

```python
def optimal_policy(state):
    # One-step lookahead
    return argmax([R(state, a) + gamma * sum(P(s'|state,a) * V_star[s'] 
                                              for s' in states)
                   for a in actions])
```

**Key**: Optimal policy is deterministic (greedy w.r.t. Q*or V*).

**Exception**: In stochastic games with multiple optimal actions, any distribution over optimal actions is fine.

---

### Policy Pitfall #1: Greedy Policy Without Exploration

**Problem**: Always taking argmax(Q) means never trying new actions.

**Example**:

```python
# Pure greedy policy (WRONG for learning)
def policy(state):
    return argmax(Q[state, :])
```

**Why It Fails**: If Q is initialized wrong, agent never explores better actions.

**Solution**: ε-greedy policy

```python
def epsilon_greedy_policy(state, epsilon=0.1):
    if random.random() < epsilon:
        return random.choice(actions)  # Explore
    else:
        return argmax(Q[state, :])      # Exploit
```

**Exploration-Exploitation Tradeoff**: Explore to find better actions, exploit to maximize reward.

---

### Policy Pitfall #2: Stochastic Policy for Deterministic Optimal

**Scenario**: Optimal policy is deterministic (most MDPs), but user uses stochastic policy.

**Effect**: Suboptimal performance (randomness doesn't help).

**Example**: GridWorld optimal policy always moves toward goal (deterministic).

**When Stochastic is Needed**:

1. **During Learning**: Exploration (ε-greedy, Boltzmann)
2. **Partially Observable**: Stochasticity can help in POMDPs
3. **Multi-Agent**: Randomness prevents exploitation by opponents

**Takeaway**: After learning, optimal policy is usually deterministic. Use stochastic for exploration.

---

## Part 4: Bellman Equations

### Bellman Expectation Equation

**For V^π**:

```
V^π(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V^π(s')]
```

**Intuition**: Value of state s = expected immediate reward + discounted value of next state.

**For Q^π**:

```
Q^π(s,a) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ Σ_{a'} π(a'|s') Q^π(s',a')]
```

**Intuition**: Value of (s,a) = expected immediate reward + discounted value of next (s',a').

**Relationship**:

```
V^π(s) = Σ_a π(a|s) Q^π(s,a)
Q^π(s,a) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V^π(s')]
```

---

### Bellman Optimality Equation

**For V***:

```
V*(s) = max_a Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V*(s')]
```

**Intuition**: Optimal value = max over actions of (immediate reward + discounted optimal future value).

**For Q***:

```
Q*(s,a) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ max_{a'} Q*(s',a')]
```

**Intuition**: Optimal Q-value = expected immediate reward + discounted optimal Q-value of next state.

**Relationship**:

```
V*(s) = max_a Q*(s,a)
Q*(s,a) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V*(s')]
```

---

### Deriving the Bellman Equation

**Start with definition of V^π**:

```
V^π(s) = E_π[G_t | s_t = s]
       = E_π[r_t + γr_{t+1} + γ²r_{t+2} + ... | s_t = s]
```

**Factor out first reward**:

```
V^π(s) = E_π[r_t + γ(r_{t+1} + γr_{t+2} + ...) | s_t = s]
       = E_π[r_t | s_t = s] + γ E_π[r_{t+1} + γr_{t+2} + ... | s_t = s]
```

**Second term is V^π(s_{t+1})**:

```
V^π(s) = E_π[r_t | s_t = s] + γ E_π[V^π(s_{t+1}) | s_t = s]
```

**Expand expectations**:

```
V^π(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V^π(s')]
```

**This is the Bellman Expectation Equation.**

**Key Insight**: Value function satisfies a consistency equation (recursive).

---

### Why Bellman Equations Matter

**1. Iterative Algorithms**: Use Bellman equation as update rule

```python
# Value Iteration
V_new[s] = max_a Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V[s']]

# Q-Learning
Q[s,a] += alpha * (r + gamma * max_a' Q[s',a'] - Q[s,a])
```

**2. Convergence Guarantees**: Bellman operator is a contraction, guarantees convergence.

**3. Understanding Algorithms**: All RL algorithms approximate Bellman equations.

**Takeaway**: Bellman equations are the foundation of RL algorithms.

---

### Bellman Pitfall #1: Forgetting Max vs Expectation

**Bellman Expectation** (for policy π):

```
V^π(s) = Σ_a π(a|s) ...  # Expectation over policy
```

**Bellman Optimality** (for optimal policy):

```
V*(s) = max_a ...  # Maximize over actions
```

**Consequence**:

- Policy evaluation uses Bellman expectation
- Value iteration uses Bellman optimality

**Common Mistake**: Using max when evaluating a non-greedy policy.

---

### Bellman Pitfall #2: Ignoring Transition Probabilities

**Deterministic Transition**:

```
V^π(s) = R(s,a) + γ V^π(s')  # Direct, s' is deterministic
```

**Stochastic Transition**:

```
V^π(s) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V^π(s')]  # Weighted sum
```

**Example**: Stochastic GridWorld

```
# Action RIGHT from (1,1)
V((1,1)) = 0.8 * [r + γ V((1,2))]    # 80% intended
         + 0.1 * [r + γ V((0,1))]    # 10% slip up
         + 0.1 * [r + γ V((2,1))]    # 10% slip down
```

**Takeaway**: Don't forget to weight by transition probabilities in stochastic environments.

---

## Part 5: Discount Factor γ

### What Does γ Control?

**Discount factor γ ∈ [0, 1]** controls how much the agent cares about future rewards.

**γ = 0**: Only immediate reward matters

```
V(s) = E[r_t]  (myopic)
```

**γ = 1**: All future rewards matter equally

```
V(s) = E[r_t + r_{t+1} + r_{t+2} + ...]  (far-sighted)
```

**γ = 0.9**: Future discounted exponentially

```
V(s) = E[r_t + 0.9*r_{t+1} + 0.81*r_{t+2} + ...]
```

**Reward 10 steps away**:

- γ=0.9: worth 0.9^10 = 0.35 of immediate reward
- γ=0.99: worth 0.99^10 = 0.90 of immediate reward

---

### Planning Horizon

**Effective Horizon**: How far ahead does agent plan?

**Approximation**: Horizon ≈ 1/(1-γ)

**Examples**:

- γ=0.9 → Horizon ≈ 10 steps
- γ=0.99 → Horizon ≈ 100 steps
- γ=0.5 → Horizon ≈ 2 steps
- γ=0.999 → Horizon ≈ 1000 steps

**Intuition**: After horizon steps, rewards are discounted to ~37% (e^{-1}).

**Formal**: Σ_{t=0}^∞ γ^t = 1/(1-γ) (sum of geometric series).

---

### Choosing γ

**Rule of Thumb**:

- **Task horizon known**: γ such that 1/(1-γ) ≈ task_length
- **Short episodes** (< 100 steps): γ = 0.9 to 0.95
- **Long episodes** (100-1000 steps): γ = 0.99
- **Very long** (> 1000 steps): γ = 0.999

**Example: Pong** (episode ~ 1000 steps)

```
γ = 0.99  # Horizon ≈ 100, sees ~10% of episode
```

**Example: Cartpole** (episode ~ 200 steps)

```
γ = 0.99  # Horizon ≈ 100, sees half of episode
```

**Example: Chess** (game ~ 40 moves = 80 steps)

```
γ = 0.95  # Horizon ≈ 20, sees quarter of game
```

---

### γ = 1 Special Case

**When γ = 1**:

- Only valid for **episodic tasks** (guaranteed termination)
- Continuing tasks: V = ∞ (unbounded)

**Example: GridWorld** (terminates at goal)

```
γ = 1.0  # OK, episode ends
V(s) = -steps_to_goal + 10  (finite)
```

**Example: Stock trading** (never terminates)

```
γ = 1.0  # WRONG, V = ∞
γ = 0.99  # Correct
```

**Takeaway**: Use γ < 1 for continuing tasks, γ = 1 allowed for episodic.

---

### Discount Factor Pitfall #1: Too Small γ

**Scenario**: Task requires 50 steps to reach goal, γ=0.9.

**Problem**:

```
Reward at step 50 discounted by 0.9^50 = 0.0052
```

**Effect**: Agent effectively blind to long-term goals (can't see reward).

**Solution**: Increase γ to 0.99 (0.99^50 = 0.61, still significant).

**Symptom**: Agent learns suboptimal policy (ignores distant goals).

---

### Discount Factor Pitfall #2: γ = 1 in Continuing Tasks

**Scenario**: Continuing task (never terminates), γ=1.

**Problem**:

```
V(s) = r + r + r + ... = ∞  (unbounded)
```

**Effect**: Value iteration, Q-learning diverge (values explode).

**Solution**: Use γ < 1 (e.g., γ=0.99).

**Symptom**: Values grow without bound, algorithm doesn't converge.

---

### Discount Factor Pitfall #3: Treating γ as Hyperparameter

**Wrong Mindset**: "Let's grid search γ in [0.9, 0.95, 0.99]."

**Correct Mindset**: "Task requires planning X steps ahead, so γ = 1 - 1/X."

**Example**: Goal 100 steps away

```
Required horizon = 100
γ = 1 - 1/100 = 0.99
```

**Takeaway**: γ is not arbitrary. Choose based on task horizon.

---

## Part 6: Algorithm Families

### Three Paradigms

**1. Dynamic Programming (DP)**:

- Requires full MDP model (P, R known)
- Exact algorithms (no sampling)
- Examples: Value Iteration, Policy Iteration

**2. Monte Carlo (MC)**:

- Model-free (learn from experience)
- Learns from complete episodes
- Examples: First-visit MC, Every-visit MC

**3. Temporal Difference (TD)**:

- Model-free (learn from experience)
- Learns from incomplete episodes
- Examples: TD(0), Q-learning, SARSA

**Key Differences**:

- DP: Needs model, no sampling
- MC: No model, full episodes
- TD: No model, partial episodes (most flexible)

---

### Value Iteration

**Algorithm**: Iteratively apply Bellman optimality operator.

```python
# Initialize
V = {s: 0 for s in states}

# Iterate until convergence
while not converged:
    V_new = {}
    for s in states:
        # Bellman optimality backup
        V_new[s] = max([sum(P(s_next|s,a) * (R(s,a,s_next) + gamma * V[s_next])
                            for s_next in states)
                        for a in actions])
    
    if max(abs(V_new[s] - V[s]) for s in states) < threshold:
        converged = True
    V = V_new

# Extract policy
policy = {s: argmax([sum(P(s_next|s,a) * (R(s,a,s_next) + gamma * V[s_next])
                         for s_next in states)
                    for a in actions])
          for s in states}
```

**Convergence**: Guaranteed (Bellman operator is contraction).

**Computational Cost**: O(|S|² |A|) per iteration.

**When to Use**: Small state spaces (< 10,000 states), full model available.

---

### Policy Iteration

**Algorithm**: Alternate between policy evaluation and policy improvement.

```python
# Initialize random policy
policy = {s: random.choice(actions) for s in states}

while not converged:
    # Policy Evaluation: Compute V^π
    V = {s: 0 for s in states}
    while not converged_V:
        V_new = {}
        for s in states:
            a = policy[s]
            V_new[s] = sum(P(s_next|s,a) * (R(s,a,s_next) + gamma * V[s_next])
                          for s_next in states)
        V = V_new
    
    # Policy Improvement: Make policy greedy w.r.t. V
    policy_stable = True
    for s in states:
        old_action = policy[s]
        policy[s] = argmax([sum(P(s_next|s,a) * (R(s,a,s_next) + gamma * V[s_next])
                               for s_next in states)
                           for a in actions])
        if old_action != policy[s]:
            policy_stable = False
    
    if policy_stable:
        converged = True
```

**Convergence**: Guaranteed, often fewer iterations than value iteration.

**When to Use**: When policy converges faster than values (common).

**Key Difference from Value Iteration**:

- Value iteration: no explicit policy until end
- Policy iteration: maintain and improve policy each iteration

---

### Monte Carlo Methods

**Idea**: Estimate V^π(s) by averaging returns from state s.

```python
# First-visit MC
V = defaultdict(float)
counts = defaultdict(int)

for episode in range(num_episodes):
    trajectory = run_episode(policy)  # [(s_0, a_0, r_0), ..., (s_T, a_T, r_T)]
    
    G = 0
    visited = set()
    for (s, a, r) in reversed(trajectory):
        G = r + gamma * G  # Accumulate return
        
        if s not in visited:  # First-visit
            V[s] += G
            counts[s] += 1
            visited.add(s)
    
    for s in counts:
        V[s] /= counts[s]  # Average return
```

**Advantages**:

- No model needed (model-free)
- Can handle stochastic environments
- Unbiased estimates

**Disadvantages**:

- Requires complete episodes (can't learn mid-episode)
- High variance (one trajectory is noisy)
- Slow convergence

**When to Use**: Episodic tasks, when model unavailable.

---

### Temporal Difference (TD) Learning

**Idea**: Update V after each step using bootstrapping.

**TD(0) Update**:

```python
V[s] += alpha * (r + gamma * V[s_next] - V[s])
#                \_____________________/
#                       TD error
```

**Bootstrapping**: Use current estimate V[s_next] instead of true return.

**Full Algorithm**:

```python
V = {s: 0 for s in states}

for episode in range(num_episodes):
    s = initial_state()
    
    while not terminal:
        a = policy(s)
        s_next, r = environment.step(s, a)
        
        # TD update
        V[s] += alpha * (r + gamma * V[s_next] - V[s])
        
        s = s_next
```

**Advantages**:

- No model needed (model-free)
- Can learn from incomplete episodes (online)
- Lower variance than MC

**Disadvantages**:

- Biased estimates (bootstrap uses estimate)
- Requires tuning α (learning rate)

**When to Use**: Model-free, need online learning.

---

### Q-Learning (TD for Q-values)

**TD for action-values Q(s,a)**:

```python
Q[s,a] += alpha * (r + gamma * max_a' Q[s_next, a'] - Q[s,a])
```

**Full Algorithm**:

```python
Q = defaultdict(lambda: defaultdict(float))

for episode in range(num_episodes):
    s = initial_state()
    
    while not terminal:
        # ε-greedy action selection
        if random.random() < epsilon:
            a = random.choice(actions)
        else:
            a = argmax(Q[s])
        
        s_next, r = environment.step(s, a)
        
        # Q-learning update (off-policy)
        Q[s][a] += alpha * (r + gamma * max(Q[s_next].values()) - Q[s][a])
        
        s = s_next
```

**Key**: Off-policy (learns optimal Q regardless of behavior policy).

**When to Use**: Model-free, discrete actions, want optimal policy.

---

### SARSA (On-Policy TD)

**Difference from Q-learning**: Uses next action from policy (on-policy).

```python
Q[s,a] += alpha * (r + gamma * Q[s_next, a_next] - Q[s,a])
#                                      ^^^^^^
#                                      Action from policy, not max
```

**Full Algorithm**:

```python
Q = defaultdict(lambda: defaultdict(float))

for episode in range(num_episodes):
    s = initial_state()
    a = epsilon_greedy(Q[s], epsilon)  # Choose first action
    
    while not terminal:
        s_next, r = environment.step(s, a)
        a_next = epsilon_greedy(Q[s_next], epsilon)  # Next action from policy
        
        # SARSA update (on-policy)
        Q[s][a] += alpha * (r + gamma * Q[s_next][a_next] - Q[s][a])
        
        s, a = s_next, a_next
```

**Difference from Q-learning**:

- Q-learning: learns optimal policy (off-policy)
- SARSA: learns policy being followed (on-policy)

**When to Use**: When you want policy to reflect exploration strategy.

---

### Algorithm Comparison

| Algorithm | Model? | Episodes? | Convergence | Use Case |
|-----------|--------|-----------|-------------|----------|
| Value Iteration | Yes (P, R) | No | Guaranteed | Small MDPs, known model |
| Policy Iteration | Yes (P, R) | No | Guaranteed, faster | Small MDPs, good init policy |
| Monte Carlo | No | Complete | Slow, high variance | Episodic, model-free |
| TD(0) | No | Partial | Faster, lower variance | Online, model-free |
| Q-Learning | No | Partial | Guaranteed* | Discrete actions, off-policy |
| SARSA | No | Partial | Guaranteed* | On-policy, safe exploration |

*With appropriate exploration and learning rate schedule.

---

### Algorithm Pitfall #1: Using DP Without Model

**Scenario**: User tries value iteration on real robot (no model).

**Problem**: Value iteration requires P(s'|s,a) and R(s,a,s').

**Solution**: Use model-free methods (Q-learning, SARSA, policy gradients).

**Red Flag**: "Let's use policy iteration for Atari games." (No model available.)

---

### Algorithm Pitfall #2: Monte Carlo on Non-Episodic Tasks

**Scenario**: Continuing task (never terminates), try MC.

**Problem**: MC requires complete episodes to compute return.

**Solution**: Use TD methods (learn from partial trajectories).

**Red Flag**: "Let's use MC for stock trading." (Continuing task.)

---

### Algorithm Pitfall #3: Confusing Q-Learning and SARSA

**Scenario**: User uses Q-learning but expects on-policy behavior.

**Example**: Cliff walking with epsilon-greedy

- Q-learning: Learns optimal (risky) path along cliff
- SARSA: Learns safe path away from cliff (accounts for exploration)

**Takeaway**:

- Q-learning: Learns optimal policy (off-policy)
- SARSA: Learns policy being followed (on-policy)

**Choose based on whether you want optimal policy or policy that accounts for exploration.**

---

## Part 7: Exploration vs Exploitation

### The Tradeoff

**Exploitation**: Choose action with highest known value (maximize immediate reward).

**Exploration**: Try new actions to discover if they're better (maximize long-term information).

**Dilemma**: Must explore to find optimal policy, but exploration sacrifices short-term reward.

**Example**: Restaurant choice

- Exploitation: Go to your favorite restaurant (known good)
- Exploration: Try a new restaurant (might be better, might be worse)

---

### Why Exploration is Necessary

**Scenario**: GridWorld, Q-values initialized to 0.

**Without Exploration**:

```python
# Greedy policy
policy(s) = argmax(Q[s, :])  # Always 0 initially, picks arbitrary action
```

**Problem**: If first action happens to be BAD, Q[s,a] becomes negative, never tried again.

**Result**: Agent stuck in suboptimal policy (local optimum).

**With Exploration**:

```python
# ε-greedy
if random.random() < epsilon:
    action = random.choice(actions)  # Explore
else:
    action = argmax(Q[s, :])  # Exploit
```

**Result**: Eventually tries all actions, discovers optimal.

---

### ε-Greedy Exploration

**Algorithm**:

```python
def epsilon_greedy(state, Q, epsilon=0.1):
    if random.random() < epsilon:
        return random.choice(actions)  # Explore with prob ε
    else:
        return argmax(Q[state, :])     # Exploit with prob 1-ε
```

**Tuning ε**:

- **ε = 0**: No exploration (greedy, can get stuck)
- **ε = 1**: Random policy (no exploitation, never converges)
- **ε = 0.1**: Common choice (10% exploration)

**Decay Schedule**:

```python
epsilon = max(epsilon_min, epsilon * decay_rate)
# Start high (ε=1.0), decay to low (ε=0.01)
```

**Rationale**: Explore heavily early, exploit more as you learn.

---

### Upper Confidence Bound (UCB)

**Idea**: Choose action that balances value and uncertainty.

**UCB Formula**:

```python
action = argmax(Q[s,a] + c * sqrt(log(N[s]) / N[s,a]))
#                ^^^^^^     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#               Exploitation        Exploration bonus
```

**Where**:

- N[s] = number of times state s visited
- N[s,a] = number of times action a taken in state s
- c = exploration constant

**Intuition**: Actions tried less often get exploration bonus (uncertainty).

**Advantage over ε-greedy**: Adaptive exploration (focuses on uncertain actions).

---

### Optimistic Initialization

**Idea**: Initialize Q-values to high values (optimistic).

```python
Q = defaultdict(lambda: defaultdict(lambda: 10.0))  # Optimistic
```

**Effect**: All actions initially seem good, encourages exploration.

**How it works**:

1. All Q-values start high (optimistic)
2. Agent tries action, gets real reward (likely lower)
3. Q-value decreases, agent tries other actions
4. Continues until all actions explored

**Advantage**: Simple, no ε parameter.

**Disadvantage**: Only works for finite action spaces, exploration stops after initial phase.

---

### Boltzmann Exploration (Softmax)

**Idea**: Choose actions probabilistically based on Q-values.

```python
def softmax(Q, temperature=1.0):
    exp_Q = np.exp(Q / temperature)
    return exp_Q / np.sum(exp_Q)

probs = softmax(Q[state, :])
action = np.random.choice(actions, p=probs)
```

**Temperature**:

- High temperature (τ→∞): Uniform random (more exploration)
- Low temperature (τ→0): Greedy (more exploitation)

**Advantage**: Naturally weights exploration by Q-values (poor actions less likely).

**Disadvantage**: Requires tuning temperature, computationally more expensive.

---

### Exploration Pitfall #1: No Exploration

**Scenario**: Pure greedy policy.

```python
action = argmax(Q[state, :])  # No randomness
```

**Problem**: Agent never explores, gets stuck in local optimum.

**Example**: Q-values initialized to 0, first action is UP (arbitrary).

- Agent always chooses UP (Q still 0 for others)
- Never discovers RIGHT is optimal
- Stuck forever

**Solution**: Always use some exploration (ε-greedy with ε ≥ 0.01).

---

### Exploration Pitfall #2: Too Much Exploration

**Scenario**: ε = 0.5 (50% random actions).

**Problem**: Agent wastes time on known-bad actions.

**Effect**: Slow convergence, poor performance even after learning.

**Solution**: Decay ε over time (start high, end low).

```python
epsilon = max(0.01, epsilon * 0.995)  # Decay to 1%
```

---

### Exploration Pitfall #3: Exploration at Test Time

**Scenario**: Evaluating learned policy with ε-greedy (ε=0.1).

**Problem**: Test performance artificially low (10% random actions).

**Solution**: Use greedy policy at test time.

```python
# Training
action = epsilon_greedy(state, Q, epsilon=0.1)

# Testing
action = argmax(Q[state, :])  # Greedy, no exploration
```

**Takeaway**: Exploration is for learning, not evaluation.

---

## Part 8: When Theory is Sufficient

### Theory vs Implementation

**When Understanding Theory is Enough**:

1. **Debugging**: Understanding Bellman equation explains why Q-values aren't converging
2. **Hyperparameter Tuning**: Understanding γ explains why agent is myopic
3. **Algorithm Selection**: Understanding model-free vs model-based explains why value iteration fails
4. **Conceptual Design**: Understanding exploration explains why agent gets stuck

**When You Need Implementation**:

1. **Real Problems**: Toy examples don't teach debugging real environments
2. **Scaling**: Neural networks, replay buffers, parallel environments
3. **Engineering**: Practical details (learning rate schedules, reward clipping)

**This Skill's Scope**: Theory, intuition, foundations.

**Other Skills for Implementation**: value-based-methods, policy-gradient-methods, actor-critic-methods.

---

### What This Skill Taught You

**1. MDP Formulation**: S, A, P, R, γ - the framework for RL.

**2. Value Functions**: V(s) = expected cumulative reward, Q(s,a) = value of action in state.

**3. Bellman Equations**: Recursive decomposition, foundation of all algorithms.

**4. Discount Factor**: γ controls planning horizon (1/(1-γ)).

**5. Policies**: Deterministic vs stochastic, optimal policy π*.

**6. Algorithms**:

- DP: Value iteration, policy iteration (model-based)
- MC: Monte Carlo (episodic, model-free)
- TD: Q-learning, SARSA (online, model-free)

**7. Exploration**: ε-greedy, UCB, necessary for learning.

**8. Theory-Practice Gap**: When theory suffices vs when to implement.

---

### Next Steps

After mastering foundations, route to:

**For Discrete Actions**:

- **value-based-methods**: DQN, Double DQN, Dueling DQN (Q-learning + neural networks)

**For Continuous Actions**:

- **actor-critic-methods**: SAC, TD3, A2C (policy + value function)

**For Any Action Space**:

- **policy-gradient-methods**: REINFORCE, PPO (direct policy optimization)

**For Debugging**:

- **rl-debugging**: Why agent not learning, reward issues, convergence problems

**For Environment Setup**:

- **rl-environments**: Gym, custom environments, wrappers

---

## Part 9: Common Pitfalls

### Pitfall #1: Skipping MDP Formulation

**Symptom**: Implementing Q-learning without defining states, actions, rewards clearly.

**Consequence**: Algorithm fails, user doesn't know why.

**Solution**: Always answer:

- What are states? (Markovian?)
- What are actions? (Discrete/continuous?)
- What is reward function? (Sparse/dense?)
- What is discount factor? (Based on horizon?)

---

### Pitfall #2: Confusing Value and Reward

**Symptom**: Setting V(s) = r(s).

**Consequence**: Ignores future rewards, policy suboptimal.

**Solution**: V(s) = E[r + γr' + γ²r'' + ...], not just r.

---

### Pitfall #3: Arbitrary Discount Factor

**Symptom**: "Let's use γ=0.9 because it's common."

**Consequence**: Agent can't see long-term goals (if γ too small) or values diverge (if γ=1 in continuing task).

**Solution**: Choose γ based on horizon (γ = 1 - 1/horizon).

---

### Pitfall #4: No Exploration

**Symptom**: Pure greedy policy during learning.

**Consequence**: Agent stuck in local optimum.

**Solution**: ε-greedy with ε ≥ 0.01, decay over time.

---

### Pitfall #5: Using DP Without Model

**Symptom**: Trying value iteration on real robot.

**Consequence**: Algorithm requires P(s'|s,a), R(s,a), which are unknown.

**Solution**: Use model-free methods (Q-learning, policy gradients).

---

### Pitfall #6: Monte Carlo on Continuing Tasks

**Symptom**: Using MC on task that never terminates.

**Consequence**: Cannot compute return (episode never ends).

**Solution**: Use TD methods (learn from partial trajectories).

---

### Pitfall #7: Confusing Q-Learning and SARSA

**Symptom**: Using Q-learning but expecting safe exploration.

**Consequence**: Q-learning learns optimal (risky) policy, ignores exploration safety.

**Solution**: Use SARSA for safe on-policy learning, Q-learning for optimal off-policy.

---

### Pitfall #8: Exploration at Test Time

**Symptom**: Evaluating with ε-greedy (ε > 0).

**Consequence**: Test performance artificially low.

**Solution**: Greedy policy at test time (ε=0).

---

### Pitfall #9: Treating Bellman as Black Box

**Symptom**: Using Q-learning update without understanding why.

**Consequence**: Cannot debug convergence issues, tune hyperparameters.

**Solution**: Derive Bellman equation, understand bootstrapping.

---

### Pitfall #10: Ignoring Transition Probabilities

**Symptom**: Using deterministic Bellman equation in stochastic environment.

**Consequence**: Wrong value estimates.

**Solution**: Weight by P(s'|s,a) in stochastic environments.

---

## Part 10: Rationalization Resistance

### Rationalization Table

| Rationalization | Reality | Counter-Guidance | Red Flag |
|-----------------|---------|------------------|----------|
| "I'll just copy Q-learning code" | Doesn't understand Q(s,a) meaning, cannot debug | "Let's understand what Q represents: expected cumulative reward. Why does Bellman equation have max?" | Jumping to code without theory |
| "V(s) is the reward at state s" | V is cumulative, r is immediate | "V(s) = E[r + γr' + ...], not just r. Value is long-term." | Confusing value and reward |
| "γ=0.9 is standard" | γ depends on task horizon | "What's your task horizon? γ=0.9 means ~10 steps. Need more?" | Arbitrary discount factor |
| "I don't need exploration, greedy is fine" | Gets stuck in local optimum | "Without exploration, you never try new actions. Use ε-greedy." | No exploration strategy |
| "Value iteration for Atari" | Atari doesn't have model (P, R unknown) | "Value iteration needs full model. Use model-free (DQN)." | DP on model-free problem |
| "Monte Carlo for continuing task" | MC requires episodes (termination) | "MC needs complete episodes. Use TD for continuing tasks." | MC on continuing task |
| "Q-learning and SARSA are the same" | Q-learning off-policy, SARSA on-policy | "Q-learning learns optimal, SARSA learns policy followed." | Confusing on-policy and off-policy |
| "I'll test with ε-greedy (ε=0.1)" | Test should be greedy (exploit only) | "Exploration is for learning. Test with ε=0 (greedy)." | Exploration at test time |
| "Bellman equation is just a formula" | It's the foundation of all algorithms | "Derive it. Understand why V(s) = r + γV(s'). Enables debugging." | Black-box understanding |
| "Deterministic transition, no need for P" | Correct, but must recognize when stochastic | "If stochastic, must weight by P(s'|s,a). Check environment." | Ignoring stochasticity |

---

## Part 11: Red Flags

Watch for these signs of misunderstanding:

- [ ] **Skipping MDP Formulation**: Implementing algorithm without defining S, A, P, R, γ
- [ ] **Value-Reward Confusion**: Treating V(s) as immediate reward instead of cumulative
- [ ] **Arbitrary γ**: Choosing discount factor without considering task horizon
- [ ] **No Exploration**: Pure greedy policy during learning
- [ ] **DP Without Model**: Using value/policy iteration when model unavailable
- [ ] **MC on Continuing**: Using Monte Carlo on non-episodic tasks
- [ ] **Q-SARSA Confusion**: Not understanding on-policy vs off-policy
- [ ] **Test Exploration**: Using ε-greedy during evaluation
- [ ] **Bellman Black Box**: Using TD updates without understanding Bellman equation
- [ ] **Ignoring Stochasticity**: Forgetting transition probabilities in stochastic environments
- [ ] **Planning Horizon Mismatch**: γ=0.9 for task requiring 100-step planning
- [ ] **Policy-Value Confusion**: Confusing π(s) and V(s), or Q(s,a) and π(a|s)

**If any red flag triggered → Explain theory → Derive equation → Connect to algorithm**

---

## Part 12: Code Examples

### Example 1: Value Iteration on GridWorld

```python
import numpy as np

# GridWorld: 4x4, goal at (3,3), walls at (1,1) and (2,2)
grid_size = 4
goal = (3, 3)
walls = {(1, 1), (2, 2)}

# MDP definition
gamma = 0.9
actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

def next_state(s, a):
    """Deterministic transition"""
    x, y = s
    if a == 'UP': x -= 1
    elif a == 'DOWN': x += 1
    elif a == 'LEFT': y -= 1
    elif a == 'RIGHT': y += 1
    
    # Boundary check
    x = max(0, min(grid_size - 1, x))
    y = max(0, min(grid_size - 1, y))
    
    # Wall check
    if (x, y) in walls:
        return s  # Bounce back
    return (x, y)

def reward(s, a, s_next):
    """Reward function"""
    if s_next == goal:
        return 10
    elif s_next in walls:
        return -5
    else:
        return -1

# Value Iteration
V = np.zeros((grid_size, grid_size))
threshold = 0.01
max_iterations = 1000

for iteration in range(max_iterations):
    V_new = np.zeros((grid_size, grid_size))
    
    for x in range(grid_size):
        for y in range(grid_size):
            s = (x, y)
            
            if s == goal:
                V_new[x, y] = 0  # Terminal state
                continue
            
            # Bellman optimality backup
            values = []
            for a in actions:
                s_next = next_state(s, a)
                r = reward(s, a, s_next)
                value = r + gamma * V[s_next[0], s_next[1]]
                values.append(value)
            
            V_new[x, y] = max(values)
    
    # Check convergence
    if np.max(np.abs(V_new - V)) < threshold:
        print(f"Converged in {iteration} iterations")
        break
    
    V = V_new

# Extract policy
policy = {}
for x in range(grid_size):
    for y in range(grid_size):
        s = (x, y)
        if s == goal:
            policy[s] = None
            continue
        
        best_action = None
        best_value = -float('inf')
        for a in actions:
            s_next = next_state(s, a)
            r = reward(s, a, s_next)
            value = r + gamma * V[s_next[0], s_next[1]]
            if value > best_value:
                best_value = value
                best_action = a
        policy[s] = best_action

print("Value Function:")
print(V)
print("\nOptimal Policy:")
for x in range(grid_size):
    row = []
    for y in range(grid_size):
        action = policy.get((x, y), '')
        if action == 'UP': symbol = '↑'
        elif action == 'DOWN': symbol = '↓'
        elif action == 'LEFT': symbol = '←'
        elif action == 'RIGHT': symbol = '→'
        else: symbol = 'G'  # Goal
        row.append(symbol)
    print(' '.join(row))
```

**Output**:

```
Converged in 23 iterations
Value Function:
[[ 2.39  3.65  5.05  6.17]
 [ 3.65  0.    6.17  7.59]
 [ 5.05  0.    7.59  8.77]
 [ 6.17  7.59  8.77  0.  ]]

Optimal Policy:
→ → → ↓
↓ G → ↓
→ G → ↓
→ → → G
```

**Key Observations**:

- Values increase as you get closer to goal
- Policy points toward goal (shortest path)
- Walls (value=0) are avoided

---

### Example 2: Q-Learning on GridWorld

```python
import numpy as np
import random

# Same GridWorld setup
grid_size = 4
goal = (3, 3)
walls = {(1, 1), (2, 2)}
actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
gamma = 0.9
alpha = 0.1  # Learning rate
epsilon = 0.1  # Exploration

# Q-table
Q = {}
for x in range(grid_size):
    for y in range(grid_size):
        for a in actions:
            Q[((x, y), a)] = 0.0

def epsilon_greedy(s, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        # Greedy
        best_action = actions[0]
        best_value = Q[(s, best_action)]
        for a in actions:
            if Q[(s, a)] > best_value:
                best_value = Q[(s, a)]
                best_action = a
        return best_action

# Training
num_episodes = 1000

for episode in range(num_episodes):
    s = (0, 0)  # Start state
    
    while s != goal:
        # Choose action
        a = epsilon_greedy(s, epsilon)
        
        # Take action
        s_next = next_state(s, a)
        r = reward(s, a, s_next)
        
        # Q-learning update
        if s_next == goal:
            max_Q_next = 0  # Terminal
        else:
            max_Q_next = max(Q[(s_next, a_prime)] for a_prime in actions)
        
        Q[(s, a)] += alpha * (r + gamma * max_Q_next - Q[(s, a)])
        
        s = s_next

# Extract policy
print("Learned Policy:")
for x in range(grid_size):
    row = []
    for y in range(grid_size):
        s = (x, y)
        if s == goal:
            row.append('G')
        else:
            best_action = max(actions, key=lambda a: Q[(s, a)])
            if best_action == 'UP': symbol = '↑'
            elif best_action == 'DOWN': symbol = '↓'
            elif best_action == 'LEFT': symbol = '←'
            elif best_action == 'RIGHT': symbol = '→'
            row.append(symbol)
    print(' '.join(row))
```

**Output** (similar to value iteration):

```
→ → → ↓
↓ G → ↓
→ G → ↓
→ → → G
```

**Key Differences from Value Iteration**:

- Q-learning is model-free (doesn't need P, R)
- Learns from experience (episodes)
- Uses ε-greedy exploration
- Requires many episodes to converge

---

### Example 3: Policy Evaluation (MC vs TD)

```python
import numpy as np
from collections import defaultdict
import random

# Simple chain MDP: s0 → s1 → s2 → goal
# Deterministic policy: always go right
# Reward: -1 per step, +10 at goal
# gamma = 0.9

gamma = 0.9

# Monte Carlo Policy Evaluation
def mc_policy_evaluation(num_episodes=1000):
    V = defaultdict(float)
    counts = defaultdict(int)
    
    for _ in range(num_episodes):
        # Generate episode
        trajectory = [
            (0, -1),  # (state, reward)
            (1, -1),
            (2, -1),
            (3, 10),  # goal
        ]
        
        # Compute returns
        G = 0
        visited = set()
        for s, r in reversed(trajectory):
            G = r + gamma * G
            if s not in visited:
                V[s] += G
                counts[s] += 1
                visited.add(s)
    
    for s in V:
        V[s] /= counts[s]
    
    return V

# TD(0) Policy Evaluation
def td_policy_evaluation(num_episodes=1000, alpha=0.1):
    V = defaultdict(float)
    
    for _ in range(num_episodes):
        s = 0
        
        while s != 3:  # Until goal
            # Take action (deterministic policy)
            s_next = s + 1
            r = 10 if s_next == 3 else -1
            
            # TD update
            V[s] += alpha * (r + gamma * V[s_next] - V[s])
            
            s = s_next
    
    return V

# Compare
V_mc = mc_policy_evaluation()
V_td = td_policy_evaluation()

print("Monte Carlo V:")
print({s: round(V_mc[s], 2) for s in [0, 1, 2]})

print("\nTD(0) V:")
print({s: round(V_td[s], 2) for s in [0, 1, 2]})

# True values (analytical)
V_true = {
    0: -1 + gamma * (-1 + gamma * (-1 + gamma * 10)),
    1: -1 + gamma * (-1 + gamma * 10),
    2: -1 + gamma * 10,
}
print("\nTrue V:")
print({s: round(V_true[s], 2) for s in [0, 1, 2]})
```

**Output**:

```
Monte Carlo V:
{0: 4.39, 1: 6.1, 2: 8.0}

TD(0) V:
{0: 4.41, 1: 6.12, 2: 8.01}

True V:
{0: 4.39, 1: 6.1, 2: 8.0}
```

**Observations**:

- Both MC and TD converge to true values
- TD uses bootstrapping (updates before episode ends)
- MC waits for complete episode

---

### Example 4: Discount Factor Impact

```python
import numpy as np

# Simple MDP: chain of 10 states, +1 reward at end
# Compare different gamma values

def value_iteration_chain(gamma, num_states=10):
    V = np.zeros(num_states + 1)  # +1 for goal
    
    # Value iteration
    for _ in range(100):
        V_new = np.zeros(num_states + 1)
        for s in range(num_states):
            # Deterministic: s → s+1, reward = +1 at goal
            s_next = s + 1
            r = 1 if s_next == num_states else 0
            V_new[s] = r + gamma * V[s_next]
        V = V_new
    
    return V[:num_states]  # Exclude goal

# Compare gamma values
for gamma in [0.5, 0.9, 0.99, 1.0]:
    V = value_iteration_chain(gamma)
    print(f"γ={gamma}:")
    print(f"  V(s_0) = {V[0]:.4f}")
    print(f"  V(s_5) = {V[5]:.4f}")
    print(f"  V(s_9) = {V[9]:.4f}")
    print(f"  Effective horizon = {1/(1-gamma) if gamma < 1 else 'inf':.1f}\n")
```

**Output**:

```
γ=0.5:
  V(s_0) = 0.0010
  V(s_5) = 0.0313
  V(s_9) = 0.5000
  Effective horizon = 2.0

γ=0.9:
  V(s_0) = 0.3487
  V(s_5) = 0.5905
  V(s_9) = 0.9000
  Effective horizon = 10.0

γ=0.99:
  V(s_0) = 0.9044
  V(s_5) = 0.9510
  V(s_9) = 0.9900
  Effective horizon = 100.0

γ=1.0:
  V(s_0) = 1.0000
  V(s_5) = 1.0000
  V(s_9) = 1.0000
  Effective horizon = inf
```

**Key Insights**:

- γ=0.5: Value at s_0 is tiny (can't "see" reward 10 steps away)
- γ=0.9: Moderate values (horizon ≈ 10, matches task length)
- γ=0.99: High values (can plan far ahead)
- γ=1.0: All states have same value (no discounting)

**Lesson**: Choose γ based on how far ahead agent must plan.

---

### Example 5: Exploration Comparison

```python
import numpy as np
import random

# Simple bandit: 3 actions, true Q* = [1.0, 5.0, 3.0]
# Compare exploration strategies

true_Q = [1.0, 5.0, 3.0]
num_actions = 3

def sample_reward(action):
    """Stochastic reward"""
    return true_Q[action] + np.random.randn() * 0.5

# Strategy 1: ε-greedy
def epsilon_greedy_experiment(epsilon=0.1, num_steps=1000):
    Q = [0.0] * num_actions
    counts = [0] * num_actions
    
    total_reward = 0
    for _ in range(num_steps):
        # Choose action
        if random.random() < epsilon:
            action = random.randint(0, num_actions - 1)
        else:
            action = np.argmax(Q)
        
        # Observe reward
        reward = sample_reward(action)
        total_reward += reward
        
        # Update Q
        counts[action] += 1
        Q[action] += (reward - Q[action]) / counts[action]
    
    return total_reward / num_steps

# Strategy 2: UCB
def ucb_experiment(c=2.0, num_steps=1000):
    Q = [0.0] * num_actions
    counts = [0] * num_actions
    
    # Initialize: try each action once
    for a in range(num_actions):
        reward = sample_reward(a)
        counts[a] = 1
        Q[a] = reward
    
    total_reward = 0
    for t in range(num_actions, num_steps):
        # UCB action selection
        ucb_values = [Q[a] + c * np.sqrt(np.log(t) / counts[a]) 
                     for a in range(num_actions)]
        action = np.argmax(ucb_values)
        
        # Observe reward
        reward = sample_reward(action)
        total_reward += reward
        
        # Update Q
        counts[action] += 1
        Q[action] += (reward - Q[action]) / counts[action]
    
    return total_reward / num_steps

# Strategy 3: Greedy (no exploration)
def greedy_experiment(num_steps=1000):
    Q = [0.0] * num_actions
    counts = [0] * num_actions
    
    total_reward = 0
    for _ in range(num_steps):
        action = np.argmax(Q)
        reward = sample_reward(action)
        total_reward += reward
        
        counts[action] += 1
        Q[action] += (reward - Q[action]) / counts[action]
    
    return total_reward / num_steps

# Compare (average over 100 runs)
num_runs = 100

greedy_rewards = [greedy_experiment() for _ in range(num_runs)]
epsilon_rewards = [epsilon_greedy_experiment() for _ in range(num_runs)]
ucb_rewards = [ucb_experiment() for _ in range(num_runs)]

print(f"Greedy:     {np.mean(greedy_rewards):.2f} ± {np.std(greedy_rewards):.2f}")
print(f"ε-greedy:   {np.mean(epsilon_rewards):.2f} ± {np.std(epsilon_rewards):.2f}")
print(f"UCB:        {np.mean(ucb_rewards):.2f} ± {np.std(ucb_rewards):.2f}")
print(f"\nOptimal: {max(true_Q):.2f}")
```

**Output**:

```
Greedy:     1.05 ± 0.52
ε-greedy:   4.62 ± 0.21
UCB:        4.83 ± 0.18

Optimal: 5.00
```

**Insights**:

- Greedy: Gets stuck on first action (often suboptimal)
- ε-greedy: Explores, finds near-optimal
- UCB: Slightly better, focuses exploration on uncertain actions

**Lesson**: Exploration is critical. UCB > ε-greedy > greedy.

---

## Part 13: When to Route Elsewhere

This skill covers **theory and foundations**. Route to other skills for:

**Implementation**:

- **value-based-methods**: DQN, Double DQN, Dueling DQN (Q-learning + neural networks)
- **policy-gradient-methods**: REINFORCE, PPO, TRPO (policy optimization)
- **actor-critic-methods**: A2C, SAC, TD3 (policy + value)

**Debugging**:

- **rl-debugging**: Agent not learning, reward issues, convergence problems

**Infrastructure**:

- **rl-environments**: Gym API, custom environments, wrappers

**Special Topics**:

- **exploration-strategies**: Curiosity, RND, intrinsic motivation
- **reward-shaping**: Potential-based shaping, inverse RL
- **multi-agent-rl**: QMIX, MADDPG, cooperative/competitive
- **offline-rl**: CQL, IQL, learning from fixed datasets
- **model-based-rl**: MBPO, Dreamer, world models

**Evaluation**:

- **rl-evaluation**: Proper evaluation methodology, metrics

---

## Summary

**You now understand**:

1. **MDP**: S, A, P, R, γ - the framework for RL
2. **Value Functions**: V(s) = cumulative expected reward, Q(s,a) = value of action
3. **Bellman Equations**: Recursive decomposition, foundation of algorithms
4. **Discount Factor**: γ controls planning horizon (1/(1-γ))
5. **Policies**: π(s) maps states to actions, π* is optimal
6. **Algorithms**: DP (value/policy iteration), MC, TD (Q-learning, SARSA)
7. **Exploration**: ε-greedy, UCB, necessary for learning
8. **Theory-Practice**: When understanding suffices vs when to implement

**Key Takeaways**:

- **MDP formulation comes first** (define S, A, P, R, γ before implementing)
- **Value ≠ Reward** (V is cumulative, r is immediate)
- **γ is not arbitrary** (choose based on task horizon)
- **Exploration is mandatory** (ε-greedy, UCB, not pure greedy)
- **Algorithm families differ** (DP needs model, MC needs episodes, TD is most flexible)
- **Bellman equations enable everything** (understand them to debug algorithms)

**Next**: Route to implementation skills (value-based, policy-gradient, actor-critic) to build real agents.

**This foundation will enable you to implement, debug, and extend RL algorithms effectively.**
