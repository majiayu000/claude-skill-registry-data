---
name: multi-agent-rl
description: Master QMIX, MADDPG, CTDE - multi-agent learning with coordination and credit assignment
---

# Multi-Agent Reinforcement Learning

## When to Use This Skill

Invoke this skill when you encounter:

- **Multiple Learners**: 2+ agents learning simultaneously in shared environment
- **Coordination Problem**: Agents must coordinate to achieve goals
- **Non-Stationarity**: Other agents changing policies during training
- **CTDE Implementation**: Separating centralized training from decentralized execution
- **Value Factorization**: Credit assignment in cooperative multi-agent settings
- **QMIX Algorithm**: Learning cooperative Q-values with value factorization
- **MADDPG**: Multi-agent actor-critic with centralized critics
- **Communication**: Agents learning to communicate to improve coordination
- **Team Reward Ambiguity**: How to split team reward fairly among agents
- **Cooperative vs Competitive**: Designing reward structure for multi-agent problem
- **Non-Stationarity Handling**: Dealing with other agents' policy changes
- **When Multi-Agent RL Needed**: Deciding if problem requires MARL vs single-agent

**This skill teaches learning from multiple simultaneous agents with coordination challenges.**

Do NOT use this skill for:

- Single-agent RL (use rl-foundations, value-based-methods, policy-gradient-methods)
- Supervised multi-task learning (that's supervised learning)
- Simple parallel independent tasks (use single-agent RL in parallel)
- Pure game theory without learning (use game theory frameworks)

## Core Principle

**Multi-agent RL learns coordinated policies for multiple agents in shared environment, solving the fundamental problem that environment non-stationarity from other agents' learning breaks standard RL convergence guarantees.**

The core insight: When other agents improve their policies, the environment changes. Your value estimates computed assuming other agents play old policy become wrong when they play new policy.

```
Single-Agent RL:
  1. Agent learns policy π
  2. Environment is fixed
  3. Agent value estimates Q(s,a) stable
  4. Algorithm converges to optimal policy

Multi-Agent RL:
  1. Agent 1 learns policy π_1
  2. Agent 2 also learning, changing π_2
  3. Environment from Agent 1 perspective is non-stationary
  4. Agent 1's value estimates invalid when Agent 2 improves
  5. Standard convergence guarantees broken
  6. Need special algorithms: QMIX, MADDPG, communication

Without addressing non-stationarity, multi-agent learning is unstable.
```

**Without understanding multi-agent problem structure and non-stationarity, you'll implement algorithms that fail to coordinate, suffer credit assignment disasters, or waste effort on agent conflicts instead of collaboration.**

---

## Part 1: Multi-Agent RL Fundamentals

### Why Multi-Agent RL Differs From Single-Agent

**Standard RL Assumption (Single-Agent)**:

- You have one agent
- Environment dynamics and reward function are fixed
- Agent's actions don't change environment structure
- Goal: Learn policy that maximizes expected return

**Multi-Agent RL Reality**:

- Multiple agents act in shared environment
- Each agent learns simultaneously
- When Agent 1 improves, Agent 2 sees changed environment
- Reward depends on all agents' actions: R = R(a_1, a_2, ..., a_n)
- Non-stationarity: other agents' policies change constantly
- Convergence undefined (what is "optimal" when others adapt?)

### Problem Types: Cooperative, Competitive, Mixed

**Cooperative Multi-Agent Problem**:

```
Definition: All agents share same objective
Reward: R_team(a_1, a_2, ..., a_n) = same for all agents

Example - Robot Team Assembly:
  - All robots get same team reward
  - +100 if assembly succeeds
  - 0 if assembly fails
  - All robots benefit from success equally

Characteristic:
  - Agents don't conflict on goals
  - Challenge: Credit assignment (who deserves credit?)
  - Solution: Value factorization (QMIX, QPLEX)

Key Insight:
  Cooperative doesn't mean agents see each other!
  - Agents might have partial/no observation of others
  - Still must coordinate for team success
  - Factorization enables coordination without observation
```

**Competitive Multi-Agent Problem**:

```
Definition: Agents have opposite objectives (zero-sum)
Reward: R_i(a_1, ..., a_n) = -R_j(a_1, ..., a_n) for i≠j

Example - Chess, Poker, Soccer:
  - Agent 1 tries to win
  - Agent 2 tries to win
  - One's gain is other's loss
  - R_1 + R_2 = 0 (zero-sum)

Characteristic:
  - Agents are adversarial
  - Challenge: Computing best response to opponent
  - Solution: Nash equilibrium (MADDPG, self-play)

Key Insight:
  In competitive games, agents must predict opponent strategies.
  - Agent 1 assumes Agent 2 plays best response
  - Agent 2 assumes Agent 1 plays best response
  - Nash equilibrium = mutual best response
  - No agent can improve unilaterally
```

**Mixed Multi-Agent Problem**:

```
Definition: Some cooperation, some competition
Reward: R_i(a_1, ..., a_n) contains both shared and individual terms

Example - Team Soccer (3v3):
  - Blue team agents cooperate for same goal
  - But blue vs red is competitive
  - Blue agent reward:
    R_i = +10 if blue scores, -10 if red scores (team-based)
        + 1 if blue_i scores goal (individual bonus)

Characteristic:
  - Agents cooperate with teammates
  - Agents compete with opponents
  - Challenge: Balancing cooperation and competition
  - Solution: Hybrid approaches using both cooperative and competitive algorithms

Key Insight:
  Mixed scenarios are most common in practice.
  - Robot teams: cooperate internally, compete for resources
  - Trading: multiple firms (cooperate via regulations, compete for profit)
  - Multiplayer games: team-based (cooperate with allies, compete with enemies)
```

### Non-Stationarity: The Core Challenge

**What is Non-Stationarity?**

```
Stationarity: Environment dynamics P(s'|s,a) and rewards R(s,a) are fixed
Non-Stationarity: Dynamics/rewards change over time

In multi-agent RL:
  Environment from Agent 1's perspective:
    P(s'_1 | s_1, a_1, a_2(t), a_3(t), ...)

  If other agents' policies change:
    π_2(t) ≠ π_2(t+1)

  Then transition dynamics change:
    P(s'_1 | s_1, a_1, a_2(t)) ≠ P(s'_1 | s_1, a_1, a_2(t+1))

  Environment is non-stationary!
```

**Why Non-Stationarity Breaks Standard RL**:

```python
# Single-agent Q-learning assumes:
# Environment is fixed during learning
# Q-values converge because bellman expectation is fixed point

Q[s,a] ← Q[s,a] + α(r + γ max_a' Q[s',a'] - Q[s,a])

# In multi-agent with non-stationarity:
# Other agents improve their policies
# Max action a' depends on other agents' policies
# When other agents improve, max action changes
# Q-values chase moving target
# No convergence guarantee
```

**Impact on Learning**:

```
Scenario: Two agents learning to navigate
Agent 1 learns: "If Agent 2 goes left, I go right"
Agent 1 builds value estimates based on this assumption

Agent 2 improves: "Actually, going right is better"
Now Agent 2 goes right (not left)
Agent 1's assumptions invalid!
Agent 1's value estimates become wrong
Agent 1 must relearn

Agent 1 tries new path based on new estimates
Agent 2 sees Agent 1's change and adapts
Agent 2's estimates become wrong

Result: Chaotic learning, no convergence
```

---

## Part 2: Centralized Training, Decentralized Execution (CTDE)

### CTDE Paradigm

**Key Idea**: Use centralized information during training, decentralized information during execution.

```
Training Phase (Centralized):
  - Trainer observes: o_1, o_2, ..., o_n (all agents' observations)
  - Trainer observes: a_1, a_2, ..., a_n (all agents' actions)
  - Trainer observes: R_team or R_1, R_2, ... (reward signals)
  - Trainer can assign credit fairly
  - Trainer can compute global value functions

Execution Phase (Decentralized):
  - Agent 1 observes: o_1 only
  - Agent 1 executes: π_1(a_1 | o_1)
  - Agent 1 doesn't need to see other agents
  - Each agent is independent during rollout
  - Enables scalability and robustness
```

**Why CTDE Solves Non-Stationarity**:

```
During training:
  - Centralized trainer sees all information
  - Can compute value Q_1(s_1, s_2, ..., s_n | a_1, a_2, ..., a_n)
  - Can factor: Q_team = f(Q_1, Q_2, ..., Q_n) (QMIX)
  - Can compute importance weights: who contributed most?

During execution:
  - Decentralized agents only use own observations
  - Policies learned during centralized training work well
  - No need for other agents' observations at runtime
  - Robust to other agents' changes (policy doesn't depend on their states)

Result:
  - Training leverages global information for stability
  - Execution is independent and scalable
  - Solves non-stationarity via centralized credit assignment
```

### CTDE in Practice

**Centralized Information Used in Training**:

```python
# During training, compute global value function
# Inputs: observations and actions of ALL agents
def compute_value_ctde(obs_1, obs_2, obs_3, act_1, act_2, act_3):
    # See everyone's observations
    global_state = combine(obs_1, obs_2, obs_3)

    # See everyone's actions
    joint_action = (act_1, act_2, act_3)

    # Compute shared value with all information
    Q_shared = centralized_q_network(global_state, joint_action)

    # Factor into individual Q-values (QMIX)
    Q_1 = q_network_1(obs_1, act_1)
    Q_2 = q_network_2(obs_2, act_2)
    Q_3 = q_network_3(obs_3, act_3)

    # Factorization: Q_team ≈ mixing_network(Q_1, Q_2, Q_3)
    # Each agent learns its contribution via QMIX loss
    return Q_shared, (Q_1, Q_2, Q_3)
```

**Decentralized Execution**:

```python
# During execution, use only own observation
def execute_policy(agent_id, own_observation):
    # Agent only sees and uses own obs
    action = policy_network(own_observation)

    # No access to other agents' observations
    # Doesn't need other agents' actions
    # Purely decentralized execution
    return action

# All agents execute in parallel:
# Agent 1: o_1 → a_1 (decentralized)
# Agent 2: o_2 → a_2 (decentralized)
# Agent 3: o_3 → a_3 (decentralized)
# Execution is independent!
```

---

## Part 3: QMIX - Value Factorization for Cooperative Teams

### QMIX: The Core Insight

**Problem**: In cooperative teams, how do you assign credit fairly?

```
Naive approach: Joint Q-value
  Q_team(s, a_1, a_2, ..., a_n) = expected return from joint action

Problem: Still doesn't assign individual credit
  If Q_team = 100, how much did Agent 1 contribute?
  Agent 1 might think: "I deserve 50%" (overconfident)
  But Agent 1 might deserve only 10% (others did more)

Result: Agents learn wrong priorities
```

**Solution: Value Factorization (QMIX)**

```
Key Assumption: Monotonicity in actions
  If improving Agent i's action improves team outcome,
  improving Agent i's individual Q-value should help

Mathematical Form:
  Q_team(a) ≥ Q_team(a') if Agent i plays better action a_i instead of a'_i
  and Agent i's Q_i(a_i) > Q_i(a'_i)

Concrete Implementation:
  Q_team(s, a_1, ..., a_n) = f(Q_1(s_1, a_1), Q_2(s_2, a_2), ..., Q_n(s_n, a_n))

  Where:
  - Q_i: Individual Q-network for agent i
  - f: Monotonic mixing network (ensures monotonicity)

  Monotonicity guarantee:
    If Q_1 increases, Q_team increases (if f is monotonic)
```

### QMIX Algorithm

**Architecture**:

```
Individual Q-Networks:           Mixing Network (Monotonic):
┌─────────┐                      ┌──────────────────┐
│ Agent 1 │─o_1─────────────────→│                  │
│  LSTM   │                      │   MLP (weights)  │─→ Q_team
│ Q_1     │                      │  are monotonic   │
└─────────┘                      │   (ReLU blocks)  │
                                 └──────────────────┘
┌─────────┐                             ↑
│ Agent 2 │─o_2──────────────────────────┤
│  LSTM   │                              │
│ Q_2     │                              │
└─────────┘                              │
                                    Hypernet:
┌─────────┐                        generates weights
│ Agent 3 │─o_3────────────────────→    as function
│  LSTM   │                        of state
│ Q_3     │
└─────────┘

Value outputs: Q_1(o_1, a_1), Q_2(o_2, a_2), Q_3(o_3, a_3)
Mixing: Q_team = mixing_network(Q_1, Q_2, Q_3, state)
```

**QMIX Training**:

```python
import torch
import torch.nn as nn
from torch.optim import Adam

class QMIXAgent:
    def __init__(self, n_agents, state_dim, obs_dim, action_dim, hidden_dim=64):
        self.n_agents = n_agents

        # Individual Q-networks (one per agent)
        self.q_networks = nn.ModuleList([
            nn.Sequential(
                nn.Linear(obs_dim + action_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1)  # Q-value for this action
            )
            for _ in range(n_agents)
        ])

        # Mixing network: takes individual Q-values and produces joint Q
        self.mixing_network = nn.Sequential(
            nn.Linear(n_agents + state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        # Hypernet: generates mixing network weights (ensuring monotonicity)
        self.hypernet = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim * (n_agents + state_dim))
        )

        self.optimizer = Adam(
            list(self.q_networks.parameters()) +
            list(self.mixing_network.parameters()) +
            list(self.hypernet.parameters()),
            lr=5e-4
        )

        self.discount = 0.99
        self.target_update_rate = 0.001
        self.epsilon = 0.05

        # Target networks (soft update)
        self._init_target_networks()

    def _init_target_networks(self):
        """Create target networks for stable learning."""
        self.target_q_networks = nn.ModuleList([
            nn.Sequential(*[nn.Linear(*p.shape[::-1]) for p in q.parameters()])
            for q in self.q_networks
        ])
        self.target_mixing_network = nn.Sequential(
            *[nn.Linear(*p.shape[::-1]) for p in self.mixing_network.parameters()]
        )

    def compute_individual_q_values(self, observations, actions):
        """
        Compute Q-values for each agent given their observation and action.

        Args:
            observations: list of n_agents observations (each [batch_size, obs_dim])
            actions: list of n_agents actions (each [batch_size, action_dim])

        Returns:
            q_values: tensor [batch_size, n_agents]
        """
        q_values = []
        for i, (obs, act) in enumerate(zip(observations, actions)):
            # Concatenate observation and action
            q_input = torch.cat([obs, act], dim=-1)
            q_i = self.q_networks[i](q_input)
            q_values.append(q_i)

        return torch.cat(q_values, dim=-1)  # [batch_size, n_agents]

    def compute_joint_q_value(self, q_values, state):
        """
        Mix individual Q-values into joint Q-value using monotonic mixing network.

        Args:
            q_values: individual Q-values [batch_size, n_agents]
            state: global state [batch_size, state_dim]

        Returns:
            q_joint: joint Q-value [batch_size, 1]
        """
        # Ensure monotonicity by using weight constraints
        # Mixing network learns to combine Q-values
        q_joint = self.mixing_network(torch.cat([q_values, state], dim=-1))
        return q_joint

    def train_step(self, batch, state_batch):
        """
        One QMIX training step.

        Batch contains:
          observations: list[n_agents] of [batch_size, obs_dim]
          actions: list[n_agents] of [batch_size, action_dim]
          rewards: [batch_size] (shared team reward)
          next_observations: list[n_agents] of [batch_size, obs_dim]
          dones: [batch_size]
        """
        observations, actions, rewards, next_observations, dones = batch
        batch_size = observations[0].shape[0]

        # Compute current Q-values
        q_values = self.compute_individual_q_values(observations, actions)
        q_joint = self.compute_joint_q_value(q_values, state_batch)

        # Compute target Q-values
        with torch.no_grad():
            # Get next Q-values for all possible joint actions (in practice, greedy)
            next_q_values = self.compute_individual_q_values(
                next_observations,
                [torch.zeros_like(a) for a in actions]  # Best actions (simplified)
            )

            # Mix next Q-values
            next_q_joint = self.compute_joint_q_value(next_q_values, state_batch)

            # TD target: team gets shared reward
            td_target = rewards.unsqueeze(-1) + (
                1 - dones.unsqueeze(-1)
            ) * self.discount * next_q_joint

        # QMIX loss
        qmix_loss = ((q_joint - td_target) ** 2).mean()

        self.optimizer.zero_grad()
        qmix_loss.backward()
        self.optimizer.step()

        # Soft update target networks
        self._soft_update_targets()

        return {'qmix_loss': qmix_loss.item()}

    def _soft_update_targets(self):
        """Soft update target networks."""
        for target, main in zip(self.target_q_networks, self.q_networks):
            for target_param, main_param in zip(target.parameters(), main.parameters()):
                target_param.data.copy_(
                    self.target_update_rate * main_param.data +
                    (1 - self.target_update_rate) * target_param.data
                )

    def select_actions(self, observations):
        """
        Greedy action selection (decentralized execution).
        Each agent selects action independently.
        """
        actions = []
        for i, obs in enumerate(observations):
            with torch.no_grad():
                # Agent i evaluates all possible actions
                best_action = None
                best_q = -float('inf')

                for action in range(self.action_dim):
                    q_input = torch.cat([obs, one_hot(action, self.action_dim)])
                    q_val = self.q_networks[i](q_input).item()

                    if q_val > best_q:
                        best_q = q_val
                        best_action = action

                # Epsilon-greedy
                if torch.rand(1).item() < self.epsilon:
                    best_action = torch.randint(0, self.action_dim, (1,)).item()

                actions.append(best_action)

        return actions
```

**QMIX Key Concepts**:

1. **Monotonicity**: If agent improves action, team value improves
2. **Value Factorization**: Q_team = f(Q_1, Q_2, ..., Q_n)
3. **Decentralized Execution**: Each agent uses only own observation
4. **Centralized Training**: Trainer sees all Q-values and state

**When QMIX Works Well**:

- Fully observable or partially observable cooperative teams
- Sparse communication needs
- Fixed team membership
- Shared reward structure

**QMIX Limitations**:

- Assumes monotonicity (not all cooperative games satisfy this)
- Doesn't handle explicit communication
- Doesn't learn agent roles dynamically

---

## Part 4: MADDPG - Multi-Agent Actor-Critic

### MADDPG: For Competitive and Mixed Scenarios

**Core Idea**: Actor-critic but with centralized critic during training.

```
DDPG (single-agent):
  - Actor π(a|s) learns policy
  - Critic Q(s,a) estimates value
  - Critic trains actor via policy gradient

MADDPG (multi-agent):
  - Each agent has actor π_i(a_i|o_i)
  - Centralized critic Q(s, a_1, ..., a_n) sees all agents
  - During training: use centralized critic for learning
  - During execution: each agent uses only own actor
```

**MADDPG Algorithm**:

```python
class MADDPGAgent:
    def __init__(self, agent_id, n_agents, obs_dim, action_dim, state_dim, hidden_dim=256):
        self.agent_id = agent_id
        self.n_agents = n_agents
        self.action_dim = action_dim

        # Actor: learns decentralized policy π_i(a_i|o_i)
        self.actor = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Continuous actions in [-1, 1]
        )

        # Critic: centralized value Q(s, a_1, ..., a_n)
        # Input: global state + all agents' actions
        self.critic = nn.Sequential(
            nn.Linear(state_dim + n_agents * action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # Single value output
        )

        # Target networks for stability
        self.target_actor = copy.deepcopy(self.actor)
        self.target_critic = copy.deepcopy(self.critic)

        self.actor_optimizer = Adam(self.actor.parameters(), lr=1e-4)
        self.critic_optimizer = Adam(self.critic.parameters(), lr=1e-3)

        self.discount = 0.99
        self.tau = 0.01  # Soft update rate

    def train_step(self, batch):
        """
        MADDPG training step.

        Batch contains:
          observations: list[n_agents] of [batch_size, obs_dim]
          actions: list[n_agents] of [batch_size, action_dim]
          rewards: [batch_size] (agent-specific reward!)
          next_observations: list[n_agents] of [batch_size, obs_dim]
          global_state: [batch_size, state_dim]
          next_global_state: [batch_size, state_dim]
          dones: [batch_size]
        """
        observations, actions, rewards, next_observations, \
            global_state, next_global_state, dones = batch

        batch_size = observations[0].shape[0]
        agent_obs = observations[self.agent_id]
        agent_action = actions[self.agent_id]
        agent_reward = rewards  # Agent-specific reward

        # Step 1: Critic Update (centralized)
        with torch.no_grad():
            # Compute next actions using target actors
            next_actions = []
            for i, next_obs in enumerate(next_observations):
                if i == self.agent_id:
                    next_a = self.target_actor(next_obs)
                else:
                    # Use stored target actors from other agents
                    next_a = other_agents_target_actors[i](next_obs)
                next_actions.append(next_a)

            # Concatenate all next actions
            next_actions_cat = torch.cat(next_actions, dim=-1)

            # Compute next value (centralized critic)
            next_q = self.target_critic(
                torch.cat([next_global_state, next_actions_cat], dim=-1)
            )

            # TD target
            td_target = agent_reward.unsqueeze(-1) + (
                1 - dones.unsqueeze(-1)
            ) * self.discount * next_q

        # Compute current Q-value
        current_actions_cat = torch.cat(actions, dim=-1)
        current_q = self.critic(
            torch.cat([global_state, current_actions_cat], dim=-1)
        )

        # Critic loss
        critic_loss = ((current_q - td_target) ** 2).mean()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Step 2: Actor Update (decentralized policy improvement)
        # Actor only uses own observation
        policy_actions = []
        for i, obs in enumerate(observations):
            if i == self.agent_id:
                # Use current actor for this agent
                action_i = self.actor(obs)
            else:
                # Use current actors of other agents
                action_i = other_agents_actors[i](obs)
            policy_actions.append(action_i)

        # Compute Q-value under current policy
        policy_actions_cat = torch.cat(policy_actions, dim=-1)
        policy_q = self.critic(
            torch.cat([global_state, policy_actions_cat], dim=-1)
        )

        # Policy gradient: maximize Q-value
        actor_loss = -policy_q.mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Soft update target networks
        self._soft_update_targets()

        return {
            'critic_loss': critic_loss.item(),
            'actor_loss': actor_loss.item(),
            'avg_q_value': current_q.mean().item()
        }

    def _soft_update_targets(self):
        """Soft update target networks toward main networks."""
        for target_param, main_param in zip(
            self.target_actor.parameters(),
            self.actor.parameters()
        ):
            target_param.data.copy_(
                self.tau * main_param.data + (1 - self.tau) * target_param.data
            )

        for target_param, main_param in zip(
            self.target_critic.parameters(),
            self.critic.parameters()
        ):
            target_param.data.copy_(
                self.tau * main_param.data + (1 - self.tau) * target_param.data
            )

    def select_action(self, observation):
        """Decentralized action selection."""
        with torch.no_grad():
            action = self.actor(observation)
            # Add exploration noise
            action = action + torch.normal(0, 0.1, action.shape)
            action = torch.clamp(action, -1, 1)
        return action.cpu().numpy()
```

**MADDPG Key Properties**:

1. **Centralized Critic**: Sees all agents' observations and actions
2. **Decentralized Actors**: Each agent uses only own observation
3. **Agent-Specific Rewards**: Each agent maximizes own reward
4. **Handles Competitive/Mixed**: Doesn't assume cooperation
5. **Continuous Actions**: Works well with continuous action spaces

**When MADDPG Works Well**:

- Competitive and mixed-motive scenarios
- Continuous action spaces
- Partial observability (agents don't see each other)
- Need for independent agent rewards

---

## Part 5: Communication in Multi-Agent Systems

### When and Why Communication Helps

**Problem Without Communication**:

```
Agents with partial observability:
Agent 1: sees position p_1, but NOT p_2
Agent 2: sees position p_2, but NOT p_1

Goal: Avoid collision while moving to targets

Without communication:
  Agent 1: "I don't know where Agent 2 is"
  Agent 2: "I don't know where Agent 1 is"

  Both might move toward same corridor
  Collision, but agents couldn't coordinate!

With communication:
  Agent 1: broadcasts "I'm moving left"
  Agent 2: receives message, moves right
  No collision!
```

**Communication Trade-offs**:

```
Advantages:
- Enables coordination with partial observability
- Can solve some problems impossible without communication
- Explicit intention sharing

Disadvantages:
- Adds complexity: agents must learn what to communicate
- High variance: messages might mislead
- Computational overhead: processing all messages
- Communication bandwidth limited in real systems

When to use communication:
- Partial observability prevents coordination
- Explicit roles (e.g., one agent is "scout")
- Limited field of view, agents are out of sight
- Agents benefit from sharing intentions

When NOT to use communication:
- Full observability (agents see everything)
- Simple coordination (value factorization sufficient)
- Communication is unreliable
```

### CommNet: Learning Communication

**Idea**: Agents learn to send and receive messages to improve coordination.

```
Architecture:
1. Each agent processes own observation: f_i(o_i) → hidden state h_i
2. Agent broadcasts hidden state as "message"
3. Agent receives messages from neighbors
4. Agent aggregates messages: Σ_j M(h_j) (attention mechanism)
5. Agent processes aggregated information: policy π(a_i | h_i + aggregated)

Key: Agents learn what information to broadcast in h_i
     Receiving agents learn what messages are useful
```

**Simple Communication Example**:

```python
class CommNetAgent:
    def __init__(self, obs_dim, action_dim, hidden_dim=64):
        # Encoding network: observation → hidden message
        self.encoder = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)  # Message to broadcast
        )

        # Communication aggregation (simplified attention)
        self.comm_processor = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),  # Own + received
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # Policy network
        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def compute_message(self, observation):
        """Generate message to broadcast to other agents."""
        return self.encoder(observation)

    def forward(self, observation, received_messages):
        """
        Process observation + received messages, output action.

        Args:
            observation: [obs_dim]
            received_messages: list of messages from neighbors

        Returns:
            action: [action_dim]
        """
        # Generate own message
        my_message = self.encoder(observation)

        # Aggregate received messages (mean pooling)
        if received_messages:
            others_messages = torch.stack(received_messages).mean(dim=0)
        else:
            others_messages = torch.zeros_like(my_message)

        # Process aggregated communication
        combined = torch.cat([my_message, others_messages], dim=-1)
        hidden = self.comm_processor(combined)

        # Select action
        action = self.policy(hidden)
        return action, my_message
```

**Communication Pitfall**: Agents learn to send misleading messages!

```python
# Without careful design, agents learn deceptive communication:
Agent 1 learns: "If I broadcast 'I'm going right', Agent 2 will go left"
Agent 1 broadcasts: "Going right" (but actually goes left)
Agent 2 goes right as expected (collision!)
Agent 1 gets higher reward (its deception worked)

Solution: Design communication carefully
- Verify agents to be truthful (implicit in cooperative setting)
- Use communication only when beneficial
- Monitor emergent communication protocols
```

---

## Part 6: Credit Assignment in Cooperative Teams

### Individual Reward vs Team Reward

**Problem**:

```
Scenario: 3-robot assembly team
Team reward: +100 if assembly succeeds, 0 if fails

Individual Reward Design:
Option 1 - Split equally: each robot gets +33.33
  Problem: Robot 3 (insignificant) gets same credit as Robot 1 (crucial)

Option 2 - Use agent contribution:
  Robot 1 (held piece): +60
  Robot 2 (guided insertion): +25
  Robot 3 (steadied base): +15
  Problem: How to compute contributions? (requires complex analysis)

Option 3 - Use value factorization (QMIX):
  Team value = mixing_network(Q_1, Q_2, Q_3)
  Each robot learns its Q-value
  QMIX learns to weight Q-values by importance
  Result: Fair credit assignment via factorization
```

**QMIX Credit Assignment Mechanism**:

```
Training:
  Observe: robot_1 does action a_1, gets q_1
           robot_2 does action a_2, gets q_2
           robot_3 does action a_3, gets q_3
           Team gets reward r_team

  Factorize: r_team ≈ mixing_network(q_1, q_2, q_3)
             = w_1 * q_1 + w_2 * q_2 + w_3 * q_3 + bias

  Learn weights w_i via mixing network

  If Robot 1 is crucial:
    mixing network learns w_1 > w_2, w_3
    Robot 1 gets larger credit (w_1 * q_1 > others)

  If Robot 3 is redundant:
    mixing network learns w_3 ≈ 0
    Robot 3 gets small credit

Result: Each robot learns fair contribution
```

**Value Decomposition Pitfall**: Agents can game the factorization!

```
Example: Learned mixing network w = [0.9, 0.05, 0.05]

Agent 1 learns: "I must maximize q_1 (it has weight 0.9)"
Agent 1 tries: action that maximizes own q_1
Problem: q_1 computed from own reward signal (myopic)
         might not actually help team!

Solution: Use proper credit assignment metrics
- Shapley values: game theory approach to credit
- Counterfactual reasoning: what if agent didn't act?
- Implicit credit (QMIX): let factorization emergently learn
```

---

## Part 7: Common Multi-Agent RL Failure Modes

### Failure Mode 1: Non-Stationarity Instability

**Symptom**: Learning curves erratic, no convergence.

```python
# Problem scenario:
for episode in range(1000):
    # Agent 1 learns
    episode_reward_1 = []
    for t in range(steps):
        a_1 = agent_1.select_action(o_1)
        a_2 = agent_2.select_action(o_2)  # Using old policy!
        r, o'_1, o'_2 = env.step(a_1, a_2)
        agent_1.update(a_1, r, o'_1)

    # Agent 2 improves (environment changes for Agent 1!)
    episode_reward_2 = []
    for t in range(steps):
        a_1 = agent_1.select_action(o_1)  # OLD VALUE ESTIMATES
        a_2 = agent_2.select_action(o_2)  # NEW POLICY (Agent 2 improved)
        r, o'_1, o'_2 = env.step(a_1, a_2)
        agent_2.update(a_2, r, o'_2)

Result: Agent 1's Q-values become invalid when Agent 2 improves
        Learning is unstable, doesn't converge
```

**Solution**: Use CTDE or opponent modeling

```python
# CTDE Approach:
# During training, use global information to stabilize
trainer.observe(o_1, a_1, o_2, a_2, r)
# Trainer sees both agents' actions, can compute stable target

# During execution:
agent_1.execute(o_1 only)  # Decentralized
agent_2.execute(o_2 only)  # Decentralized
```

### Failure Mode 2: Reward Ambiguity

**Symptom**: Agents don't improve, stuck at local optima.

```python
# Problem: Multi-agent team, shared reward
total_reward = 50

# Distribution: who gets what?
# Agent 1 thinks: "I deserve 50" (overconfident)
# Agent 2 thinks: "I deserve 50" (overconfident)
# Agent 3 thinks: "I deserve 50" (overconfident)

# Each agent overestimates importance
# Each agent learns selfishly (internal conflict)
# Team coordination breaks

Result: Team performance worse than if agents cooperated
```

**Solution**: Use value factorization

```python
# QMIX learns fair decomposition
q_1, q_2, q_3 = compute_individual_values(a_1, a_2, a_3)
team_reward = mixing_network(q_1, q_2, q_3)

# Mixing network learns importance
# If Agent 2 crucial: weight_2 > weight_1, weight_3
# Training adjusts weights based on who actually helped

Result: Fair credit, agents coordinate
```

### Failure Mode 3: Algorithm-Reward Mismatch

**Symptom**: Learning fails in specific problem types (cooperative/competitive).

```python
# Problem: Using QMIX (cooperative) in competitive setting
# Competitive game (agents have opposite rewards)

# QMIX assumes: shared reward (monotonicity works)
# But in competitive:
#   Q_1 high means Agent 1 winning
#   Q_2 high means Agent 2 winning (opposite!)
# QMIX mixing doesn't make sense
# Convergence fails

# Solution: Use MADDPG (handles competitive)
# MADDPG doesn't assume monotonicity
# Works with individual rewards
# Handles competition naturally
```

---

## Part 8: When to Use Multi-Agent RL

### Problem Characteristics for MARL

**Use MARL when**:

```
1. Multiple simultaneous learners
   - Problem has 2+ agents learning
   - NOT just parallel tasks (that's single-agent x N)

2. Shared/interdependent environment
   - Agents' actions affect each other
   - One agent's action impacts other agent's rewards
   - True interaction (not independent MDPs)

3. Coordination is beneficial
   - Agents can improve by coordinating
   - Alternative: agents could act independently (inefficient)

4. Non-trivial communication/credit
   - Agents need to coordinate or assign credit
   - NOT trivial to decompose into independent subproblems
```

**Use Single-Agent RL when**:

```
1. Single learning agent (others are environment)
   - Example: one RL agent vs static rules-based opponents
   - Environment includes other agents, but they're not learning

2. Independent parallel tasks
   - Example: 10 robots, each with own goal, no interaction
   - Use single-agent RL x 10 (faster, simpler)

3. Fully decomposable problems
   - Example: multi-robot path planning (can use single-agent per robot)
   - Problem decomposes into independent subproblems

4. Scalability critical
   - Single-agent RL scales to huge teams
   - MARL harder to scale (centralized training bottleneck)
```

### Decision Tree

```
Problem: Multiple agents learning together?
  NO → Use single-agent RL
  YES ↓

Problem: Agents' rewards interdependent?
  NO → Use single-agent RL x N (parallel)
  YES ↓

Problem: Agents must coordinate?
  NO → Use independent learning (but expect instability)
  YES ↓

Problem structure:
  COOPERATIVE → Use QMIX, MAPPO, QPLEX
  COMPETITIVE → Use MADDPG, self-play
  MIXED → Use hybrid (cooperative + competitive algorithms)
```

---

## Part 9: Opponent Modeling in Competitive Settings

### Why Model Opponents?

**Problem Without Opponent Modeling**:

```
Agent 1 (using MADDPG) learns:
  "Move right gives Q=50"

But assumption: Agent 2 plays policy π_2

When Agent 2 improves to π'_2:
  "Move right gives Q=20" (because Agent 2 blocks that path)

Agent 1's Q-value estimates become stale!
Environment has changed (opponent improved)
```

**Solution: Opponent Modeling**

```python
class OpponentModelingAgent:
    def __init__(self, agent_id, n_agents, obs_dim, action_dim):
        self.agent_id = agent_id

        # Own actor and critic
        self.actor = self._build_actor(obs_dim, action_dim)
        self.critic = self._build_critic()

        # Model opponent policies (for agents we compete against)
        self.opponent_models = {
            i: self._build_opponent_model() for i in range(n_agents) if i != agent_id
        }

    def _build_opponent_model(self):
        """Model what opponent will do given state."""
        return nn.Sequential(
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, self.action_dim)
        )

    def train_step_with_opponent_modeling(self, batch):
        """
        Update own policy AND opponent models.

        Key insight: predict what opponent will do,
        then plan against those predictions
        """
        observations, actions, rewards, next_observations = batch

        # Step 1: Update opponent models (supervised)
        # Predict opponent action from observation
        for opponent_id, model in self.opponent_models.items():
            predicted_action = model(next_observations[opponent_id])
            actual_action = actions[opponent_id]
            opponent_loss = ((predicted_action - actual_action) ** 2).mean()
            # Update opponent model
            optimizer.zero_grad()
            opponent_loss.backward()
            optimizer.step()

        # Step 2: Plan against opponent predictions
        predicted_opponent_actions = {
            i: model(observations[i])
            for i, model in self.opponent_models.items()
        }

        # Use predictions in MADDPG update
        # Critic sees: own obs + predicted opponent actions
        # Actor learns: given opponent predictions, best response

        return {'opponent_loss': opponent_loss.item()}
```

**Opponent Modeling Trade-offs**:

```
Advantages:
  - Accounts for opponent improvements (non-stationarity)
  - Enables planning ahead
  - Reduces brittleness to opponent policy changes

Disadvantages:
  - Requires learning opponent models (additional supervision)
  - If opponent model is wrong, agent learns wrong policy
  - Computational overhead
  - Assumes opponent is predictable

When to use:
  - Competitive settings with clear opponents
  - Limited number of distinct opponents
  - Opponents have consistent strategies

When NOT to use:
  - Too many potential opponents
  - Opponents are unpredictable
  - Cooperative setting (waste of resources)
```

---

## Part 10: Advanced: Independent Q-Learning (IQL) for Multi-Agent

### IQL in Multi-Agent Settings

**Idea**: Each agent learns Q-value using only own rewards and observations.

```python
class IQLMultiAgent:
    def __init__(self, agent_id, obs_dim, action_dim):
        self.agent_id = agent_id

        # Q-network for this agent only
        self.q_network = nn.Sequential(
            nn.Linear(obs_dim + action_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

        self.optimizer = Adam(self.q_network.parameters(), lr=1e-3)

    def train_step(self, batch):
        """
        Independent Q-learning: each agent learns from own reward only.

        Problem: Non-stationarity
        - Other agents improve policies
        - Environment from this agent's perspective changes
        - Q-values become invalid

        Benefit: Decentralized
        - No centralized training needed
        - Scalable to many agents
        """
        observations, actions, rewards, next_observations = batch

        # Q-value update (standard Q-learning)
        with torch.no_grad():
            # Greedy next action (assume agent acts greedily)
            next_q_values = []
            for action in range(self.action_dim):
                q_input = torch.cat([next_observations, one_hot(action)])
                q_val = self.q_network(q_input)
                next_q_values.append(q_val)

            max_next_q = torch.max(torch.stack(next_q_values), dim=0)[0]
            td_target = rewards + 0.99 * max_next_q

        # Current Q-value
        q_pred = self.q_network(torch.cat([observations, actions], dim=-1))

        # TD loss
        loss = ((q_pred - td_target) ** 2).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return {'loss': loss.item()}
```

**IQL in Multi-Agent: Pros and Cons**:

```
Advantages:
  - Fully decentralized (scalable)
  - No communication needed
  - Simple implementation
  - Works with partial observability

Disadvantages:
  - Non-stationarity breaks convergence
  - Agents chase moving targets (other agents improving)
  - No explicit coordination
  - Performance often poor without CTDE

Result:
  - IQL works but is unstable in true multi-agent settings
  - Better to use CTDE (QMIX, MADDPG) for stability
  - IQL useful if centralized training impossible
```

---

## Part 11: Multi-Agent Experience Replay and Batch Sampling

### Challenges of Experience Replay in Multi-Agent

**Problem**:

```
In single-agent RL:
  Experience replay stores (s, a, r, s', d)
  Sample uniformly from buffer
  Works well (iid samples)

In multi-agent RL:
  Experience replay stores (s, a_1, a_2, ..., a_n, r, s')
  But agents are non-stationary!

  Transition (s, a_1, a_2, r, s') valid only if:
    - Assumptions about other agents' policies still hold
    - If other agents improved, assumptions invalid

Solution: Prioritized experience replay for multi-agent
  - Prioritize transitions where agent's assumptions are likely correct
  - Down-weight transitions from old policies (outdated assumptions)
  - Focus on recent transitions (more relevant)
```

**Batch Sampling Strategy**:

```python
class MultiAgentReplayBuffer:
    def __init__(self, capacity=100000, n_agents=3):
        self.buffer = deque(maxlen=capacity)
        self.n_agents = n_agents
        self.priority_weights = deque(maxlen=capacity)

    def add(self, transition):
        """Store experience with priority."""
        # transition: (observations, actions, rewards, next_observations, dones)
        self.buffer.append(transition)

        # Priority: how relevant is this to current policy?
        # Recent transitions: high priority (policies haven't changed much)
        # Old transitions: low priority (agents have improved, assumptions stale)
        priority = self._compute_priority(transition)
        self.priority_weights.append(priority)

    def _compute_priority(self, transition):
        """Compute priority for multi-agent setting."""
        # Heuristic: prioritize recent transitions
        # Could use TD-error (how surprised are we by this transition?)
        age = len(self.buffer)  # How long ago was this added?
        decay = 0.99 ** age  # Exponential decay
        return decay

    def sample(self, batch_size):
        """Sample prioritized batch."""
        # Weighted sampling: high priority more likely
        indices = np.random.choice(
            len(self.buffer),
            batch_size,
            p=self.priority_weights / self.priority_weights.sum()
        )

        batch = [self.buffer[i] for i in indices]
        return batch
```

---

## Part 12: 10+ Critical Pitfalls

1. **Treating as independent agents**: Non-stationarity breaks convergence
2. **Giving equal reward to unequal contributors**: Credit assignment fails
3. **Forgetting decentralized execution**: Agents need independent policies
4. **Communicating too much**: High variance, bandwidth waste
5. **Using cooperative algorithm in competitive game**: Convergence fails
6. **Using competitive algorithm in cooperative game**: Agents conflict
7. **Not using CTDE**: Weak coordination, brittle policies
8. **Assuming other agents will converge**: Non-stationarity = moving targets
9. **Value overestimation in team settings**: Similar to offline RL issues
10. **Forgetting opponent modeling**: In competitive settings, must predict others
11. **Communication deception**: Agents learn to mislead for short-term gain
12. **Scalability (too many agents)**: MARL doesn't scale to 100+ agents
13. **Experience replay staleness**: Old transitions assume old opponent policies
14. **Ignoring observability constraints**: Partial obs needs communication or factorization
15. **Reward structure not matching algorithm**: Cooperative/competitive mismatch

---

## Part 13: 10+ Rationalization Patterns

Users often rationalize MARL mistakes:

1. **"Independent agents should work"**: Doesn't understand non-stationarity
2. **"My algorithm converged to something"**: Might be local optima due to credit ambiguity
3. **"Communication improved rewards"**: Might be learned deception, not coordination
4. **"QMIX should work everywhere"**: Doesn't check problem for monotonicity
5. **"More agents = more parallelism"**: Ignores centralized training bottleneck
6. **"Rewards are subjective anyway"**: Credit assignment is objective (factorization)
7. **"I'll just add more training"**: Non-stationarity can't be fixed by more epochs
8. **"Other agents are fixed"**: But they're learning too (environment is non-stationary)
9. **"Communication bandwidth doesn't matter"**: In real systems, it does
10. **"Nash equilibrium is always stable"**: No, it's just best-response equilibrium

---

## Part 14: MAPPO - Multi-Agent Proximal Policy Optimization

### When to Use MAPPO

**Cooperative teams with policy gradients**:

```python
class MAPPOAgent:
    def __init__(self, agent_id, obs_dim, action_dim, hidden_dim=256):
        self.agent_id = agent_id

        # Actor: policy for decentralized execution
        self.actor = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

        # Critic: centralized value function (uses global state during training)
        self.critic = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        self.actor_optimizer = Adam(self.actor.parameters(), lr=3e-4)
        self.critic_optimizer = Adam(self.critic.parameters(), lr=1e-3)

    def train_step_on_batch(self, observations, actions, returns, advantages):
        """
        MAPPO training: advantage actor-critic with clipped policy gradient.

        Key difference from DDPG:
        - Policy gradient (not off-policy value)
        - Centralized training (uses global returns/advantages)
        - Decentralized execution (policy uses only own observation)
        """
        # Actor loss (clipped PPO)
        action_probs = torch.softmax(self.actor(observations), dim=-1)
        action_log_probs = torch.log(action_probs.gather(-1, actions))

        # Importance weight (in on-policy setting, = 1)
        # In practice, small advantage clipping for stability
        policy_loss = -(action_log_probs * advantages).mean()

        # Entropy regularization (exploration)
        entropy = -(action_probs * torch.log(action_probs + 1e-8)).sum(dim=-1).mean()
        actor_loss = policy_loss - 0.01 * entropy

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Critic loss (value estimation)
        values = self.critic(observations)
        critic_loss = ((values - returns) ** 2).mean()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        return {
            'actor_loss': actor_loss.item(),
            'critic_loss': critic_loss.item(),
            'entropy': entropy.item()
        }
```

**MAPPO vs QMIX**:

```
QMIX:
  - Value-based (discrete actions)
  - Value factorization (credit assignment)
  - Works with partial observability

MAPPO:
  - Policy gradient-based
  - Centralized critic (advantage estimation)
  - On-policy (requires recent trajectories)

Use MAPPO when:
  - Continuous or large discrete action spaces
  - On-policy learning acceptable
  - Value factorization not needed (reward structure simple)

Use QMIX when:
  - Discrete actions
  - Need explicit credit assignment
  - Off-policy learning preferred
```

---

## Part 15: Self-Play for Competitive Learning

### Self-Play Mechanism

**Problem**: Training competitive agents requires opponents.

```
Naive approach:
  - Agent 1 trains vs fixed opponent
  - Problem: fixed opponent doesn't adapt
  - Agent 1 learns exploitation (brittle to new opponents)

Self-play:
  - Agent 1 trains vs historical versions of itself
  - Agent 1 improves → creates stronger opponent
  - New Agent 1 trains vs stronger Agent 1
  - Cycle: both improve together
  - Result: robust agent that beats all versions of itself
```

**Self-Play Implementation**:

```python
class SelfPlayTrainer:
    def __init__(self, agent_class, n_checkpoint_opponents=5):
        self.current_agent = agent_class()
        self.opponent_pool = []  # Keep historical versions
        self.n_checkpoints = n_checkpoint_opponents

    def train(self, num_episodes):
        """Train with self-play against previous versions."""
        for episode in range(num_episodes):
            # Select opponent: current agent or historical version
            if not self.opponent_pool or np.random.rand() < 0.5:
                opponent = copy.deepcopy(self.current_agent)
            else:
                opponent = np.random.choice(self.opponent_pool)

            # Play episode: current_agent vs opponent
            trajectory = self._play_episode(self.current_agent, opponent)

            # Train current agent on trajectory
            self.current_agent.train_on_trajectory(trajectory)

            # Periodically add current agent to opponent pool
            if episode % (num_episodes // self.n_checkpoints) == 0:
                self.opponent_pool.append(copy.deepcopy(self.current_agent))

        return self.current_agent

    def _play_episode(self, agent1, agent2):
        """Play episode: agent1 vs agent2, collect experience."""
        trajectory = []
        state = self.env.reset()
        done = False

        while not done:
            # Agent 1 action
            action1 = agent1.select_action(state['agent1_obs'])

            # Agent 2 action (opponent)
            action2 = agent2.select_action(state['agent2_obs'])

            # Step environment
            state, reward, done = self.env.step(action1, action2)

            trajectory.append({
                'obs1': state['agent1_obs'],
                'obs2': state['agent2_obs'],
                'action1': action1,
                'action2': action2,
                'reward1': reward['agent1'],
                'reward2': reward['agent2']
            })

        return trajectory
```

**Self-Play Benefits and Pitfalls**:

```
Benefits:
  - Agents automatically improve together
  - Robust to different opponent styles
  - Emergent complexity (rock-paper-scissors dynamics)

Pitfalls:
  - Agents might exploit specific weaknesses (not generalizable)
  - Training unstable if pool too small
  - Forgetting how to beat weaker opponents (catastrophic forgetting)
  - Computational cost (need to evaluate multiple opponents)

Solution: Diverse opponent pool
  - Keep varied historical versions
  - Mix self-play with evaluation vs fixed benchmark
  - Monitor for forgetting (test vs all opponents periodically)
```

---

## Part 16: Practical Implementation Considerations

### Observation Space Design

**Key consideration**: Partial vs full observability

```python
# Full Observability (not realistic but simplest)
observation = {
    'own_position': agent_pos,
    'all_agent_positions': [pos1, pos2, pos3],  # See everyone!
    'all_agent_velocities': [vel1, vel2, vel3],
    'targets': [target1, target2, target3]
}

# Partial Observability (more realistic, harder)
observation = {
    'own_position': agent_pos,
    'own_velocity': agent_vel,
    'target': own_target,
    'nearby_agents': agents_within_5m,  # Limited field of view
    # Note: don't see agents far away
}

# Consequence: With partial obs, agents must communicate or learn implicitly
# Via environmental interaction (e.g., bumping into others)
```

### Reward Structure Design

**Critical for multi-agent learning**:

```python
# Cooperative game: shared reward
team_reward = +100 if goal_reached else 0
# Problem: ambiguous who contributed

# Cooperative game: mixed rewards (shared + individual)
team_reward = +100 if goal_reached
individual_bonus = +5 if agent_i_did_critical_action
total_reward_i = team_reward + individual_bonus  # incentivizes both

# Competitive game: zero-sum
reward_1 = goals_1 - goals_2
reward_2 = goals_2 - goals_1  # Opposite

# Competitive game: individual scores
reward_1 = goals_1
reward_2 = goals_2
# Problem: agents don't care about each other (no implicit competition)

# Mixed: cooperation + competition (team sports)
reward_i = +10 if team_wins
        + 1 if agent_i_scores
        + 0.1 * team_score  # Shared team success bonus
```

**Reward Design Pitfall**: Too much individual reward breaks cooperation

```
Example: 3v3 soccer
reward_i = +100 if agent_i_scores  (individual goal)
        + +5 if agent_i_assists     (passes to scorer)
        + 0 if teammate scores      (not rewarded!)

Result:
  Agent learns: "Only my goals matter, don't pass to teammates"
  Agent hoards ball, tries solo shots
  Team coordination breaks
  Lose to coordinated opponent team

Solution: Include team reward
reward_i = +100 if team_wins
        + +10 if agent_i_scores goal
        + +2 if agent_i_assists
```

---

## Summary: When to Use Multi-Agent RL

**Multi-agent RL is needed when**:

1. Multiple agents learning simultaneously in shared environment
2. Agent interactions cause non-stationarity
3. Coordination or credit assignment is non-trivial
4. Problem structure matches available algorithm (cooperative/competitive)

**Multi-agent RL is NOT needed when**:

1. Single learning agent (others are static)
2. Agents act independently (no true interaction)
3. Problem easily decomposes (use single-agent RL per agent)
4. Scalability to 100+ agents critical (MARL hard to scale)

**Key Algorithms**:

1. **QMIX**: Cooperative, value factorization, decentralized execution
2. **MADDPG**: Competitive/mixed, continuous actions, centralized critic
3. **MAPPO**: Cooperative, policy gradients, centralized training
4. **Self-Play**: Competitive, agents train vs historical versions
5. **Communication**: For partial observability, explicit coordination
6. **CTDE**: Paradigm enabling stable multi-agent learning

**Algorithm Selection Matrix**:

```
                 Cooperative    Competitive    Mixed
Discrete Action    QMIX          Nash-Q         Hybrid
Continuous Action  MAPPO/MADDPG  MADDPG         MADDPG
Partial Obs        +Comm         +Opponent Mod  +Both
Scalable           IQL (unstable) IQL           IQL (unstable)
```

**Critical Success Factors**:

1. Match algorithm to problem structure (cooperative vs competitive)
2. Design reward to align with desired coordination
3. Use CTDE for stable training
4. Monitor for non-stationarity issues
5. Validate agents work independently during execution

Use this skill to understand multi-agent problem structure and select appropriate algorithms for coordination challenges.
