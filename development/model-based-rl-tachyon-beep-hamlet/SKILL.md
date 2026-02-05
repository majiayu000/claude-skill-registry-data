---
name: model-based-rl
description: Master Dyna-Q, MBPO, Dreamer - model-based RL with world models and planning
---

# Model-Based Reinforcement Learning

## When to Use This Skill

Invoke this skill when you encounter:

- **Learning World Models**: User wants to predict future states from current state + action
- **Planning with Models**: How to use learned models for planning (MPC, shooting)
- **Dyna-Q Questions**: How to combine model-free (Q-learning) with model-based (planning)
- **MBPO Implementation**: Short rollouts, model ensemble, policy optimization
- **Dreamer Architecture**: Latent world models, imagination in latent space
- **Model Error Handling**: Why long rollouts diverge, how to keep rollouts short
- **Sim-to-Real**: Using simulators, domain randomization, reality gap
- **Sample Efficiency Claims**: When model-based actually saves samples vs compute cost
- **Distribution Shift**: Policy improves → states leave training distribution → model fails

**This skill bridges model learning and policy improvement.**

Do NOT use this skill for:

- Pure dynamics learning (use supervised learning, not RL)
- Perfect simulators (those are Dreamers, not world models)
- Model-free policy optimization (use policy-gradient-methods, actor-critic-methods)
- Debugging specific algorithm (use rl-debugging)

## Core Principle

**Model-based RL trades sample complexity for model error.**

The fundamental tradeoff:

- **Sample Complexity**: Learning from real world requires few samples (model helps)
- **Model Error**: Learned models diverge from reality, planning on wrong models hurts
- **Solution**: Keep rollouts short (k=5-10), bootstrap with value function, handle distribution shift

**Without understanding error mechanics, you'll implement algorithms that learn model errors instead of policies.**

---

## Part 1: World Models (Dynamics Learning)

### What is a World Model?

A world model (dynamics model) learns to predict the next state from current state and action:

```
Deterministic: s_{t+1} = f(s_t, a_t)
Stochastic:    p(s_{t+1} | s_t, a_t)  = N(μ_θ(s_t, a_t), σ_θ(s_t, a_t))
```

**Key Components**:

1. **State Representation**: What info captures current situation? (pixels, features, latent)
2. **Dynamics Function**: Neural network mapping (s, a) → s'
3. **Loss Function**: How to train? (MSE, cross-entropy, contrastive)
4. **Uncertainty**: Estimate model confidence (ensemble, aleatoric, epistemic)

### Example 1: Pixel-Based Dynamics

**Environment**: Cart-pole

```
Input: Current image (84×84×4 pixels)
Output: Next image (84×84×4 pixels)
Model: CNN that predicts image differences

Loss = MSE(predicted_frame, true_frame) + regularization
```

**Architecture**:

```python
class PixelDynamicsModel(nn.Module):
    def __init__(self):
        self.encoder = CNN(input_channels=4, output_dim=256)
        self.dynamics_net = MLP(256 + action_dim, 256)
        self.decoder = TransposeCNN(256, output_channels=4)

    def forward(self, s, a):
        # Encode image
        z = self.encoder(s)

        # Predict latent next state
        z_next = self.dynamics_net(torch.cat([z, a], dim=1))

        # Decode to image
        s_next = self.decoder(z_next)
        return s_next
```

**Training**:

```
For each real transition (s, a, s_next):
    pred_s_next = model(s, a)
    loss = MSE(pred_s_next, s_next)
    loss.backward()
```

**Problem**: Pixel-space errors compound (blurry 50-step predictions).

---

### Example 2: Latent-Space Dynamics

**Better for high-dim observations** (learn representation + dynamics separately).

**Architecture**:

```
1. Encoder: s → z (256-dim latent)
2. Dynamics: z_t, a_t → z_{t+1}
3. Decoder: z → s (reconstruction)
4. Reward Predictor: z, a → r
```

**Training**:

```
Reconstruction loss: ||s - decode(encode(s))||²
Dynamics loss: ||z_{t+1} - f(z_t, a_t)||²
Reward loss: ||r - reward_net(z_t, a_t)||²
```

**Advantage**: Learns compact representation, faster rollouts, better generalization.

---

### Example 3: Stochastic Dynamics

**Handle environment stochasticity** (multiple outcomes from (s, a)):

```python
class StochasticDynamicsModel(nn.Module):
    def forward(self, s, a):
        # Predict mean and std of next state distribution
        z = self.encoder(s)
        mu, log_sigma = self.dynamics_net(torch.cat([z, a], dim=1))

        # Sample next state
        z_next = mu + torch.exp(log_sigma) * torch.randn_like(mu)
        return z_next, mu, log_sigma
```

**Training**:

```
NLL loss = -log p(s_{t+1} | s_t, a_t)
         = ||s_{t+1} - μ||² / (2σ²) + log σ
```

**Key**: Captures uncertainty (aleatoric: environment noise, epistemic: model uncertainty).

---

### World Model Pitfall #1: Compounding Errors

**Bad Understanding**: "If model is 95% accurate, 50-step rollout is (0.95)^50 = 5% accurate."

**Reality**: Error compounds worse.

**Mechanics**:

```
Step 1: s1_pred = s1_true + ε1
Step 2: s2_pred = f(s1_pred, a1) = f(s1_true + ε1, a1) = f(s1_true, a1) + ∇f ε1 + ε2
       Error grows: ε_cumulative ≈ ||∇f|| * ε_prev + ε2
Step 3: Error keeps magnifying (if ||∇f|| > 1)
```

**Example**: Cart-pole position error 0.1 pixel

```
After 1 step: 0.10
After 5 steps: ~0.15 (small growth)
After 10 steps: ~0.25 (noticeable)
After 50 steps: ~2.0 (completely wrong)
```

**Solution**: Use short rollouts (k=5-10), trust value function beyond.

---

### World Model Pitfall #2: Distribution Shift

**Scenario**: Train model on policy π_0 data, policy improves to π_1.

**What Happens**:

```
π_0 data distribution: {s1, s2, s3, ...}
Model trained on: P_0(s)

π_1 visits new states: {s4, s5, s6, ...}
Model has no training data for {s4, s5, s6}
Model predictions on new states: WRONG (distribution shift)

Planning uses wrong model → Policy learns model errors
```

**Example**: Cartpole

- Initial: pole barely moving
- After learning: pole swinging wildly
- Model trained on small-angle dynamics
- New states (large angle) outside training distribution
- Model breaks

**Solution**:

1. Retrain model frequently (as policy improves)
2. Use ensemble (detect epistemic uncertainty in new states)
3. Keep policy close to training distribution (regularization)

---

## Part 2: Planning with Learned Models

### What is Planning?

Planning = using model to simulate trajectories and find good actions.

**General Form**:

```
Given:
- Current state s_t
- Dynamics model f(·)
- Reward function r(·) (known or learned)
- Value function V(·) (for horizon beyond imagination)

Find action a_t that maximizes:
  Q(s_t, a_t) = E[Σ_{τ=0}^{k} γ^τ r(s_τ, a_τ) + γ^k V(s_{t+k})]
```

**Two Approaches**:

1. **Model Predictive Control (MPC)**: Solve optimization at each step
2. **Shooting Methods**: Sample trajectories, pick best

---

### Model Predictive Control (MPC)

**Algorithm**:

```
1. At each step:
   - Initialize candidate actions a₀, a₁, ..., a_{k-1}

2. Compute k-step imagined rollout:
   s₁ = f(s_t, a₀)
   s₂ = f(s₁, a₁)
   ...
   s_k = f(s_{k-1}, a_{k-1})

3. Evaluate trajectory:
   Q = Σ τ=0 to k-1 [γ^τ r(s_τ, a_τ)] + γ^k V(s_k)

4. Optimize actions to maximize Q
5. Execute first action a₀, discard rest
6. Replan at next step
```

**Optimization Methods**:

- **Cross-Entropy Method (CEM)**: Sample actions, keep best, resample
- **Shooting**: Random shooting, iLQR, etc.

**Example**: Cart-pole with learned model

```python
def mpc_planning(s_current, model, reward_fn, value_fn, k=5, horizon=100):
    best_action = None
    best_return = -float('inf')

    # Sample candidate action sequences
    for _ in range(100):  # CEM: sample trajectories
        actions = np.random.randn(k, action_dim)

        # Simulate trajectory
        s = s_current
        trajectory_return = 0

        for t in range(k):
            s_next = model(s, actions[t])
            r = reward_fn(s, actions[t])
            trajectory_return += gamma**t * r
            s = s_next

        # Bootstrap with value
        trajectory_return += gamma**k * value_fn(s)

        # Track best
        if trajectory_return > best_return:
            best_return = trajectory_return
            best_action = actions[0]

    return best_action
```

**Key Points**:

- Replan at every step (expensive, but avoids compounding errors)
- Use short horizons (k=5-10)
- Bootstrap with value function

---

### Shooting Methods

**Random Shooting** (simplest):

```python
def random_shooting(s, model, reward_fn, value_fn, k=5, num_samples=1000):
    best_action = None
    best_return = -float('inf')

    # Sample random action sequences
    for _ in range(num_samples):
        actions = np.random.uniform(action_min, action_max, size=(k, action_dim))

        # Rollout
        s_current = s
        returns = 0
        for t in range(k):
            s_next = model(s_current, actions[t])
            r = reward_fn(s_current, actions[t])
            returns += gamma**t * r
            s_current = s_next

        # Bootstrap
        returns += gamma**k * value_fn(s_current)

        if returns > best_return:
            best_return = returns
            best_action = actions[0]

    return best_action
```

**Trade-offs**:

- Pros: Simple, parallelizable, no gradient computation
- Cons: Slow (needs many samples), doesn't refine actions

**iLQR/LQR**: Assumes quadratic reward, can optimize actions.

---

### Planning Pitfall #1: Long Horizons

**User Belief**: "k=50 is better than k=5 (more planning)."

**Reality**:

```
k=5: Q = r₀ + γr₁ + ... + γ⁴r₄ + γ⁵V(s₅)
     Errors from 5 steps of model error
     But V(s₅) more reliable (only 5 steps out)

k=50: Q = r₀ + γr₁ + ... + γ⁴⁹r₄₉ + γ⁵⁰V(s₅₀)
      Errors from 50 steps compound!
      s₅₀ prediction probably wrong
      V(s₅₀) estimated on out-of-distribution state
```

**Result**: k=50 rollouts learn model errors, policy worse than k=5.

---

## Part 3: Dyna-Q (Model + Model-Free Hybrid)

### The Idea

**Dyna = Dynamics + Q-Learning**

Combine:

1. **Real Transitions**: Learn Q from real environment data (model-free)
2. **Imagined Transitions**: Learn Q from model-generated data (model-based)

**Why?** Leverage both:

- Real data: Updates are correct, but expensive
- Imagined data: Updates are cheap, but noisy

---

### Dyna-Q Algorithm

```
Initialize:
  Q(s, a) = 0 for all (s, a)
  M = {} (dynamics model, initially empty)

Repeat:
  1. Sample real transition: (s, a) → (r, s_next)

  2. Update Q from real transition (Q-learning):
     Q[s, a] += α(r + γ max_a' Q[s_next, a'] - Q[s, a])

  3. Update model M with real transition:
     M[s, a] = (r, s_next)  [deterministic, or learn distribution]

  4. Imagine k steps:
     For n = 1 to k:
       s_r = random state from visited states
       a_r = random action
       (r, s_next) = M[s_r, a_r]

       # Update Q from imagined transition
       Q[s_r, a_r] += α(r + γ max_a' Q[s_next, a'] - Q[s_r, a_r])
```

**Key Insight**: Use model to generate additional training data (imagined transitions).

---

### Example: Dyna-Q on Cartpole

```python
class DynaQ:
    def __init__(self, alpha=0.1, gamma=0.9, k_planning=10):
        self.Q = defaultdict(lambda: defaultdict(float))
        self.M = {}  # state, action → (reward, next_state)
        self.alpha = alpha
        self.gamma = gamma
        self.k = k_planning
        self.visited_states = set()
        self.visited_actions = {}

    def learn_real_transition(self, s, a, r, s_next):
        """Learn from real transition (step 1-3)"""
        # Q-learning update
        max_q_next = max(self.Q[s_next].values()) if s_next in self.Q else 0
        self.Q[s][a] += self.alpha * (r + self.gamma * max_q_next - self.Q[s][a])

        # Model update
        self.M[(s, a)] = (r, s_next)

        # Track visited states/actions
        self.visited_states.add(s)
        if s not in self.visited_actions:
            self.visited_actions[s] = set()
        self.visited_actions[s].add(a)

    def planning_steps(self):
        """Imagine k steps (step 4)"""
        for _ in range(self.k):
            # Random state-action from memory
            s_r = random.choice(list(self.visited_states))
            a_r = random.choice(list(self.visited_actions[s_r]))

            # Imagine transition
            if (s_r, a_r) in self.M:
                r, s_next = self.M[(s_r, a_r)]

                # Q-learning update on imagined transition
                max_q_next = max(self.Q[s_next].values()) if s_next in self.Q else 0
                self.Q[s_r][a_r] += self.alpha * (
                    r + self.gamma * max_q_next - self.Q[s_r][a_r]
                )

    def choose_action(self, s, epsilon=0.1):
        """ε-greedy policy"""
        if random.random() < epsilon:
            return random.choice(actions)
        return max(self.Q[s].items(), key=lambda x: x[1])[0]

    def train_episode(self, env):
        s = env.reset()
        done = False

        while not done:
            a = self.choose_action(s)
            s_next, r, done, _ = env.step(a)

            # Learn from real transition
            self.learn_real_transition(s, a, r, s_next)

            # Planning steps
            self.planning_steps()

            s = s_next
```

**Benefits**:

- Real transitions: Accurate but expensive
- Imagined transitions: Cheap, accelerates learning

**Sample Efficiency**: Dyna-Q learns faster than Q-learning alone (imagined transitions provide extra updates).

---

### Dyna-Q Pitfall #1: Model Overfitting

**Problem**: Model learned on limited data, doesn't generalize.

**Example**: Model memorizes transitions, imagined transitions all identical.

**Solution**:

1. Use ensemble (multiple models, average predictions)
2. Track model uncertainty
3. Weight imagined updates by confidence
4. Limit planning in uncertain regions

---

## Part 4: MBPO (Model-Based Policy Optimization)

### The Idea

**MBPO = Short rollouts + Policy optimization (SAC)**

Key Insight: Don't use model for full-episode rollouts. Use model for short rollouts (k=5), bootstrap with learned value function.

**Architecture**:

```
1. Train ensemble of dynamics models (4-7 models)
2. For each real transition (s, a) → (r, s_next):
   - Roll out k=5 steps with model
   - Collect imagined transitions (s, a, r, s', s'', ...)
3. Combine real + imagined data
4. Update Q-function and policy (SAC)
5. Repeat
```

---

### MBPO Algorithm

```
Initialize:
  Models = [M1, M2, ..., M_n]  (ensemble)
  Q-function, policy, target network

Repeat for N environment steps:
  1. Collect real transition: (s, a) → (r, s_next)

  2. Roll out k steps using ensemble:
     s = s_current
     For t = 1 to k:
       # Use ensemble mean (or sample one model)
       s_next = mean([M_i(s, a) for M_i in Models])
       r = reward_fn(s, a)  [learned reward model]

       Store imagined transition: (s, a, r, s_next)
       s = s_next

  3. Mix real + imagined:
     - Real buffer: 10% real transitions
     - Imagined buffer: 90% imagined transitions (from rollouts)

  4. Update Q-function (n_gradient_steps):
     Sample batch from mixed buffer
     Compute TD error: (r + γ V(s_next) - Q(s, a))²
     Optimize Q

  5. Update policy (n_policy_steps):
     Use SAC: maximize E[Q(s, a) - α log π(a|s)]

  6. Decay rollout ratio:
     As model improves, increase imagined % (k stays fixed)
```

---

### Key MBPO Design Choices

**1. Rollout Length k**:

```
k=5-10 recommended (not k=50)

Why short?
- Error compounding (k=5 gives manageable error)
- Value bootstrapping works (V is learned from real data)
- MPC-style replanning (discard imagined trajectory)
```

**2. Ensemble Disagreement**:

```
High disagreement = model uncertainty in new state region

Use disagreement as:
- Early stopping (stop imagining if uncertainty high)
- Weighting (less trust in uncertain predictions)
- Exploration bonus (similar to curiosity)

disagreement = max_i ||M_i(s, a) - M_j(s, a)||
```

**3. Model Retraining Schedule**:

```
Too frequent: Overfitting to latest data
Too infrequent: Model becomes stale

MBPO: Retrain every N environment steps
     Typical: N = every 1000 real transitions
```

**4. Real vs Imagined Ratio**:

```
High real ratio: Few imagined transitions, limited speedup
High imagined ratio: Many imagined transitions, faster, higher model error

MBPO: Start high real % (100%), gradually increase imagined % to 90%

Why gradually?
- Early: Model untrained, use real data
- Later: Model accurate, benefit from imagined data
```

---

### MBPO Example (Pseudocode)

```python
class MBPO:
    def __init__(self, env, k=5, num_models=7):
        self.models = [DynamicsModel() for _ in range(num_models)]
        self.q_net = QNetwork()
        self.policy = SACPolicy()
        self.target_q_net = deepcopy(self.q_net)

        self.k = k  # Rollout length
        self.real_ratio = 0.05
        self.real_buffer = ReplayBuffer()
        self.imagined_buffer = ReplayBuffer()

    def collect_real_transitions(self, num_steps=1000):
        """Collect from real environment"""
        for _ in range(num_steps):
            s = self.env.state
            a = self.policy(s)
            r, s_next = self.env.step(a)

            self.real_buffer.add((s, a, r, s_next))

            # Retrain models
            if len(self.real_buffer) % 1000 == 0:
                self.train_models()
                self.generate_imagined_transitions()

    def train_models(self):
        """Train ensemble on real data"""
        for model in self.models:
            dataset = self.real_buffer.sample_batch(batch_size=256)
            for _ in range(model_epochs):
                loss = model.train_on_batch(dataset)

    def generate_imagined_transitions(self):
        """Roll out k steps with each real transition"""
        for (s, a, r_real, s_next_real) in self.real_buffer.sample_batch(256):
            # Discard, use to seed rollouts

            # Rollout k steps
            s = s_next_real  # Start from real next state
            for t in range(self.k):
                # Ensemble prediction (mean)
                s_pred = torch.stack([m(s, None) for m in self.models]).mean(dim=0)
                r_pred = self.reward_model(s, None)  # Learned reward

                # Check ensemble disagreement
                disagreement = torch.std(
                    torch.stack([m(s, None) for m in self.models]), dim=0
                ).mean()

                # Early stopping if uncertain
                if disagreement > uncertainty_threshold:
                    break

                # Store imagined transition
                self.imagined_buffer.add((s, a_random, r_pred, s_pred))

                s = s_pred

    def train_policy(self, num_steps=10000):
        """Train Q-function and policy with mixed data"""
        for step in range(num_steps):
            # Sample from mixed buffer (5% real, 95% imagined)
            if random.random() < self.real_ratio:
                batch = self.real_buffer.sample_batch(128)
            else:
                batch = self.imagined_buffer.sample_batch(128)

            # Q-learning update (SAC)
            td_target = batch['r'] + gamma * self.target_q_net(batch['s_next'])
            q_loss = MSE(self.q_net(batch['s'], batch['a']), td_target)
            q_loss.backward()

            # Policy update (SAC)
            a_new = self.policy(batch['s'])
            policy_loss = -self.q_net(batch['s'], a_new) + alpha * entropy(a_new)
            policy_loss.backward()
```

---

### MBPO Pitfalls

**Pitfall 1: k too large**

```
k=50 → Model errors compound, policy learns errors
k=5 → Manageable error, good bootstrap
```

**Pitfall 2: No ensemble**

```
Single model → Overconfident, plans in wrong regions
Ensemble → Uncertainty estimated, early stopping works
```

**Pitfall 3: Model never retrained**

```
Policy improves → States change → Model becomes stale
Solution: Retrain every N steps (or when performance plateaus)
```

**Pitfall 4: High imagined ratio early**

```
Model untrained, 90% imagined data → Learning garbage
Solution: Start low (5% imagined), gradually increase
```

---

## Part 5: Dreamer (Latent World Models)

### The Idea

**Dreamer = Imagination in latent space**

Problem: Pixel-space world models hard to train (blurry reconstructions, high-dim).
Solution: Learn latent representation, do imagination there.

**Architecture**:

```
1. Encoder: Image → Latent (z)
2. VAE: Latent space with KL regularization
3. Dynamics in latent: z_t, a_t → z_{t+1}
4. Policy: z_t → a_t (learns to dream)
5. Value: z_t → V(z_t)
6. Decoder: z_t → Image (reconstruction)
7. Reward: z_t, a_t → r (predict reward in latent space)
```

**Key Difference from MBPO**:

- MBPO: Short rollouts in state space, then Q-learning
- Dreamer: Imagine trajectories in latent space, then train policy + value in imagination

---

### Dreamer Algorithm

```
Phase 1: World Model Learning (offline)
  Given: Real replay buffer with (image, action, reward)

  1. Encode: z_t = encoder(image_t)
  2. Learn VAE loss: KL(z || N(0, I)) + ||decode(z) - image||²
  3. Learn dynamics: ||z_{t+1} - dynamics(z_t, a_t)||²
  4. Learn reward: ||r_t - reward_net(z_t, a_t)||²
  5. Learn value: ||V(z_t) - discounted_return_t||²

Phase 2: Imagination (online, during learning)
  Given: Trained world model

  1. Sample state from replay buffer: z₀ = encoder(image₀)
  2. Imagine trajectory (15-50 steps):
     a_t ~ π(a_t | z_t)  [policy samples actions]
     r_t = reward_net(z_t, a_t)  [predict reward]
     z_{t+1} ~ dynamics(z_t, a_t)  [sample next latent]
  3. Compute imagined returns:
     G_t = r_t + γ r_{t+1} + ... + γ^{k-1} r_{t+k} + γ^k V(z_{t+k})
  4. Train policy to maximize: E[G_t]
  5. Train value to match: E[(V(z_t) - G_t)²]
```

---

### Dreamer Details

**1. Latent Dynamics Learning**:

```
In pixel space: Errors accumulate visibly (blurry)
In latent space: Errors more abstract, easier to learn dynamics

Model: z_{t+1} = μ_θ(z_t, a_t) + σ_θ(z_t, a_t) * ε
       ε ~ N(0, I)

Loss: NLL(z_{t+1} | z_t, a_t)
```

**2. Policy Learning via Imagination**:

```
Standard RL in imagined trajectories (not real)

π(a_t | z_t) learns to select actions that:
- Maximize predicted reward
- Maximize value (long-term)
- Be uncertain in model predictions (curious)
```

**3. Value Learning via Imagination**:

```
V(z_t) learns to estimate imagined returns

Using stop-gradient (or separate network):
V(z_t) ≈ E[G_t]  over imagined trajectories

This enables bootstrapping in imagination
```

---

### Dreamer Example (Pseudocode)

```python
class Dreamer:
    def __init__(self):
        self.encoder = Encoder()  # image → z
        self.decoder = Decoder()  # z → image
        self.dynamics = Dynamics()  # (z, a) → z
        self.reward_net = RewardNet()  # (z, a) → r
        self.policy = Policy()  # z → a
        self.value_net = ValueNet()  # z → V(z)

    def world_model_loss(self, batch_images, batch_actions, batch_rewards):
        """Phase 1: Learn world model (supervised)"""
        # Encode
        z = self.encoder(batch_images)
        z_next = self.encoder(batch_images_next)

        # VAE loss (regularize latent)
        kl_loss = kl_divergence(z, N(0, I))
        recon_loss = MSE(self.decoder(z), batch_images)

        # Dynamics loss
        z_next_pred = self.dynamics(z, batch_actions)
        dynamics_loss = MSE(z_next_pred, z_next)

        # Reward loss
        r_pred = self.reward_net(z, batch_actions)
        reward_loss = MSE(r_pred, batch_rewards)

        total_loss = kl_loss + recon_loss + dynamics_loss + reward_loss
        return total_loss

    def imagine_trajectory(self, z_start, horizon=50):
        """Phase 2: Imagine trajectory"""
        z = z_start
        trajectory = []

        for t in range(horizon):
            # Sample action
            a = self.policy(z)

            # Predict reward
            r = self.reward_net(z, a)

            # Imagine next state
            mu, sigma = self.dynamics(z, a)
            z_next = mu + sigma * torch.randn_like(mu)

            trajectory.append((z, a, r, z_next))
            z = z_next

        return trajectory

    def compute_imagined_returns(self, trajectory):
        """Compute G_t = r_t + γ r_{t+1} + ... + γ^k V(z_k)"""
        returns = []
        G = 0

        # Backward pass
        for z, a, r, z_next in reversed(trajectory):
            G = r + gamma * G

        # Add value bootstrap
        z_final = trajectory[-1][3]
        G += gamma ** len(trajectory) * self.value_net(z_final)

        return G

    def train_policy_and_value(self, z_start_batch, horizon=15):
        """Phase 2: Train policy and value in imagination"""
        z = z_start_batch
        returns_list = []

        # Rollout imagination
        for t in range(horizon):
            a = self.policy(z)
            r = self.reward_net(z, a)

            mu, sigma = self.dynamics(z, a)
            z_next = mu + sigma * torch.randn_like(mu)

            # Compute return-to-go
            G = r + gamma * self.value_net(z_next)
            returns_list.append(G)

            z = z_next

        # Train value
        value_loss = MSE(self.value_net(z_start_batch), returns_list[0])
        value_loss.backward()

        # Train policy (maximize imagined return)
        policy_loss = -returns_list[0].mean()  # Maximize return
        policy_loss.backward()
```

---

### Dreamer Pitfalls

**Pitfall 1: Too-long imagination**

```
h=50: Latent dynamics errors compound
h=15: Better (manageable error)
```

**Pitfall 2: No KL regularization**

```
VAE collapses → z same for all states → dynamics useless
Solution: KL term forces diverse latent space
```

**Pitfall 3: Policy overfits to value estimates**

```
Early imagination: V(z_t) estimates wrong
Policy follows wrong value

Solution:
- Uncertainty estimation in imagination
- Separate value network
- Stop-gradient on value target
```

---

## Part 6: When Model-Based Helps

### Sample Efficiency

**Claim**: "Model-based RL is 10-100x more sample efficient."

**Reality**: Depends on compute budget.

**Example**: Cartpole

```
Model-free (DQN): 100k samples, instant policy
Model-based (MBPO):
  - 10k samples to train model: 2 minutes
  - 1 million imagined rollouts: 30 minutes
  - Total: 32 minutes for 10k real samples

Model-free wins on compute
```

**When Model-Based Helps**:

1. **Real samples expensive**: Robotics (100s per hour)
2. **Sim available**: Use for pre-training, transfer to real
3. **Multi-task**: Reuse model for multiple tasks
4. **Offline RL**: No online interaction, must plan from fixed data

---

### Sim-to-Real Transfer

**Setup**:

1. Train model + policy in simulator (cheap samples)
2. Test on real robot (expensive, dangerous)
3. Reality gap: Simulator ≠ Real world

**Approaches**:

1. **Domain Randomization**: Vary simulator dynamics, color, physics
2. **System Identification**: Fit simulator to real robot
3. **Robust Policy**: Train policy robust to model errors

**MBPO in Sim-to-Real**:

```
1. Train in simulator (unlimited samples)
2. Collect real data (expensive)
3. Finetune model + policy on real data
4. Continue imagining with real-trained model
```

---

### Multi-Task Learning

**Setup**: Train model once, use for multiple tasks.

**Example**:

```
Model learns: p(s_{t+1} | s_t, a_t)  [task-independent]
Task 1 reward: r₁(s, a)
Task 2 reward: r₂(s, a)

Plan with model + reward₁
Plan with model + reward₂
```

**Advantage**: Model amortizes over tasks.

---

## Part 7: Model Error Handling

### Error Sources

**1. Aleatoric (Environment Noise)**:

```
Same (s, a) can lead to multiple s'
Example: Pushing object, slight randomness in friction

Solution: Stochastic model p(s' | s, a)
```

**2. Epistemic (Model Uncertainty)**:

```
Limited training data, model hasn't seen this state
Example: Policy explores new region, model untrained

Solution: Ensemble, Bayesian network, uncertainty quantification
```

**3. Distribution Shift**:

```
Policy improves, visits new states
Model trained on old policy data
New states: Out of training distribution

Solution: Retraining, regularization, uncertainty detection
```

---

### Handling Uncertainty

**Approach 1: Ensemble**:

```python
# Train multiple models on same data
models = [DynamicsModel() for _ in range(7)]
for model in models:
    train_model(model, data)

# Uncertainty = disagreement
predictions = [m(s, a) for m in models]
mean_pred = torch.stack(predictions).mean(dim=0)
std_pred = torch.stack(predictions).std(dim=0)

# Use for early stopping
if std_pred.mean() > threshold:
    stop_rollout()
```

**Approach 2: Uncertainty Weighting**:

```
High uncertainty → Less trust → Lower imagined data weight

Weight for imagined transition = 1 / (1 + ensemble_disagreement)
```

**Approach 3: Conservative Planning**:

```
Roll out only when ensemble agrees

disagreement = max_disagreement between models
if disagreement < threshold:
    roll_out()
else:
    use_only_real_data()
```

---

## Part 8: Implementation Patterns

### Pseudocode: Learning Dynamics Model

```python
class DynamicsModel:
    def __init__(self, state_dim, action_dim):
        self.net = MLP(state_dim + action_dim, state_dim)
        self.optimizer = Adam(self.net.parameters())

    def predict(self, s, a):
        """Predict next state"""
        sa = torch.cat([s, a], dim=-1)
        s_next = self.net(sa)
        return s_next

    def train(self, dataset):
        """Supervised learning on real transitions"""
        s, a, s_next = dataset

        # Forward pass
        s_next_pred = self.predict(s, a)

        # Loss
        loss = MSE(s_next_pred, s_next)

        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
```

### Pseudocode: MPC Planning

```python
def mpc_plan(s_current, model, reward_fn, value_fn, k=5, num_samples=100):
    """Model Predictive Control"""
    best_action = None
    best_return = -float('inf')

    for _ in range(num_samples):
        # Sample action sequence
        actions = np.random.uniform(-1, 1, size=(k, action_dim))

        # Rollout k steps
        s = s_current
        trajectory_return = 0

        for t in range(k):
            s_next = model.predict(s, actions[t])
            r = reward_fn(s, actions[t])
            trajectory_return += (gamma ** t) * r
            s = s_next

        # Bootstrap with value
        trajectory_return += (gamma ** k) * value_fn(s)

        # Track best
        if trajectory_return > best_return:
            best_return = trajectory_return
            best_action = actions[0]

    return best_action
```

---

## Part 9: Common Pitfalls Summary

### Pitfall 1: Long Rollouts

```
k=50 → Model errors compound
k=5 → Manageable error, good bootstrap
FIX: Keep k small, use value function
```

### Pitfall 2: Distribution Shift

```
Policy changes → New states outside training distribution → Model wrong
FIX: Retrain model frequently, use ensemble for uncertainty
```

### Pitfall 3: Model Overfitting

```
Few transitions → Model memorizes
FIX: Ensemble, regularization, hold-out validation set
```

### Pitfall 4: No Value Bootstrapping

```
Pure imagined returns → All error in rollout
FIX: Bootstrap with learned value at horizon k
```

### Pitfall 5: Using Model-Based When Model-Free Better

```
Simple task, perfect simulator → Model-based wastes compute
FIX: Use model-free (DQN, PPO) unless samples expensive
```

### Pitfall 6: Model Never Updated

```
Policy improves, model stays frozen → Model stale
FIX: Retrain every N steps or monitor validation performance
```

### Pitfall 7: High Imagined Data Ratio Early

```
Untrained model, 90% imagined → Learning garbage
FIX: Start with low imagined ratio, gradually increase
```

### Pitfall 8: No Ensemble

```
Single model → Overconfident in uncertain regions
FIX: Use 4-7 models, aggregate predictions
```

### Pitfall 9: Ignoring Reward Function

```
Use true reward with imperfect state model
FIX: Also learn reward model (or use true rewards if available)
```

### Pitfall 10: Planning Too Long

```
Expensive planning, model errors → Not worth compute
FIX: Short horizons (k=5), real-time constraints
```

---

## Part 10: Red Flags in Model-Based RL

- [ ] **Long rollouts (k > 20)**: Model errors compound, use short rollouts
- [ ] **No value function**: Pure imagined returns, no bootstrap
- [ ] **Single model**: Overconfident, use ensemble
- [ ] **Model never retrained**: Policy changes, model becomes stale
- [ ] **High imagined ratio early**: Learning from bad model, start with 100% real
- [ ] **No distribution shift handling**: New states outside training distribution
- [ ] **Comparing to wrong baseline**: MBPO vs model-free, not MBPO vs DQN with same compute
- [ ] **Believing sample efficiency claims**: Model helps sample complexity, not compute time
- [ ] **Treating dynamics as perfect**: Model is learned, has errors
- [ ] **No uncertainty estimates**: Can't detect when to stop rolling out

---

## Part 11: Rationalization Resistance

| Rationalization | Reality | Counter | Red Flag |
|---|---|---|---|
| "k=50 is better planning" | Errors compound, k=5 better | Use short rollouts, bootstrap value | Long horizons |
| "I trained a model, done" | Missing planning algorithm | Use model for MPC/shooting/Dyna | No planning step |
| "100% imagined data" | Model untrained, garbage quality | Start 100% real, gradually increase | No real data ratio |
| "Single model fine" | Overconfident, plans in wrong regions | Ensemble provides uncertainty | Single model |
| "Model-based always better" | Model errors + compute vs sample efficiency | Only help when real samples expensive | Unconditional belief |
| "One model for life" | Policy improves, model becomes stale | Retrain every N steps | Static model |
| "Dreamer works on pixels" | Needs good latent learning, complex tuning | MBPO simpler on state space | Wrong problem |
| "Value function optional" | Pure rollout return = all model error | Bootstrap with learned value | No bootstrapping |

---

## Summary

**You now understand**:

1. **World Models**: Learning p(s_{t+1} | s_t, a_t), error mechanics
2. **Planning**: MPC, shooting, Dyna-Q, short horizons, value bootstrapping
3. **Dyna-Q**: Combining real + imagined transitions
4. **MBPO**: Short rollouts (k=5), ensemble, value bootstrapping
5. **Dreamer**: Latent imagination, imagination in latent space
6. **Model Error**: Compounding, distribution shift, uncertainty estimation
7. **When to Use**: Real samples expensive, sim-to-real, multi-task
8. **Pitfalls**: Long rollouts, no bootstrapping, overconfidence, staleness

**Key Insights**:

- **Error compounding**: Keep k small (5-10), trust value function beyond
- **Distribution shift**: Retrain model as policy improves, use ensemble
- **Value bootstrapping**: Horizon k, then V(s_k), not pure imagined return
- **Sample vs Compute**: Model helps sample complexity, not compute time
- **When it helps**: Real samples expensive (robotics), sim-to-real, multi-task

**Route to implementation**: Use MBPO for continuous control, Dyna-Q for discrete, Dreamer for visual tasks.

**This foundation enables debugging model-based algorithms and knowing when they're appropriate.**

---

## Part 12: Advanced Model Learning Techniques

### Latent Ensemble Models

**Why Latent?** State/pixel space models struggle with high-dimensional data.

**Architecture**:

```
Encoder: s (pixels) → z (latent, 256-dim)
Ensemble models: z_t, a_t → z_{t+1}
Decoder: z → s (reconstruction)

7 ensemble models in latent space (not pixel space)
```

**Benefits**:

1. **Smaller models**: Latent 256-dim vs pixel 84×84×3
2. **Better dynamics**: Learned in abstract space
3. **Faster training**: 10x faster than pixel models
4. **Better planning**: Latent trajectories more stable

**Implementation Pattern**:

```python
class LatentEnsembleDynamics:
    def __init__(self):
        self.encoder = PixelEncoder()  # image → z
        self.decoder = PixelDecoder()  # z → image
        self.models = [LatentDynamics() for _ in range(7)]

    def encode_batch(self, images):
        return self.encoder(images)

    def predict_latent_ensemble(self, z, a):
        """Predict next latent, with uncertainty"""
        predictions = [m(z, a) for m in self.models]
        z_next_mean = torch.stack(predictions).mean(dim=0)
        z_next_std = torch.stack(predictions).std(dim=0)
        return z_next_mean, z_next_std

    def decode_batch(self, z):
        return self.decoder(z)
```

---

### Reward Model Learning

**When needed**: Visual RL (don't have privileged reward)

**Structure**:

```
Reward predictor: (s or z, a) → r
Trained via supervised learning on real transitions
```

**Training**:

```python
class RewardModel(nn.Module):
    def __init__(self, latent_dim, action_dim):
        self.net = MLP(latent_dim + action_dim, 1)

    def forward(self, z, a):
        za = torch.cat([z, a], dim=-1)
        r = self.net(za)
        return r

    def train_step(self, batch):
        z, a, r_true = batch
        r_pred = self.forward(z, a)
        loss = MSE(r_pred, r_true)
        loss.backward()
        return loss.item()
```

**Key**: Train on ground truth rewards from environment.

**Integration with MBPO**:

- Use learned reward when true reward unavailable
- Use true reward when available (more accurate)

---

### Model Selection and Scheduling

**Problem**: Which model to use for which task?

**Solution: Modular Approach**

```python
class ModelScheduler:
    def __init__(self):
        self.deterministic = DeterministicModel()  # For planning
        self.stochastic = StochasticModel()  # For uncertainty
        self.ensemble = [DynamicsModel() for _ in range(7)]

    def select_for_planning(self, num_rollouts):
        """Choose model based on phase"""
        if num_rollouts < 100:
            return self.stochastic  # Learn uncertainty
        else:
            return self.ensemble  # Use for planning

    def select_for_training(self):
        return self.deterministic  # Simple, stable
```

**Use Cases**:

- Deterministic: Fast training, baseline
- Stochastic: Uncertainty quantification
- Ensemble: Planning with disagreement detection

---

## Part 13: Multi-Step Planning Algorithms

### Cross-Entropy Method (CEM) for Planning

**Idea**: Iteratively refine action sequence.

```
1. Sample N random action sequences
2. Evaluate all (rollout with model)
3. Keep top 10% (elite)
4. Fit Gaussian to elite
5. Sample from Gaussian
6. Repeat 5 times
```

**Implementation**:

```python
def cem_plan(s, model, reward_fn, value_fn, k=5, num_samples=100, num_iters=5):
    """Cross-Entropy Method for planning"""
    action_dim = 2  # Example: 2D action
    a_min, a_max = -1.0, 1.0

    # Initialize distribution
    mu = torch.zeros(k, action_dim)
    sigma = torch.ones(k, action_dim)

    for iteration in range(num_iters):
        # Sample candidates
        samples = []
        for _ in range(num_samples):
            actions = (mu + sigma * torch.randn_like(mu)).clamp(a_min, a_max)
            samples.append(actions)

        # Evaluate (rollout)
        returns = []
        for actions in samples:
            s_temp = s
            ret = 0
            for t, a in enumerate(actions):
                s_temp = model(s_temp, a)
                r = reward_fn(s_temp, a)
                ret += (0.99 ** t) * r
            ret += (0.99 ** k) * value_fn(s_temp)
            returns.append(ret)

        # Keep elite (top 10%)
        returns = torch.tensor(returns)
        elite_idx = torch.topk(returns, int(num_samples * 0.1))[1]
        elite_actions = [samples[i] for i in elite_idx]

        # Update distribution
        elite = torch.stack(elite_actions)  # (elite_size, k, action_dim)
        mu = elite.mean(dim=0)
        sigma = elite.std(dim=0) + 0.01  # Add small constant for stability

    return mu[0]  # Return first action of best sequence
```

**Comparison to Random Shooting**:

- Random: Simple, parallelizable, needs many samples
- CEM: Iterative refinement, fewer samples, more compute per sample

---

### Shooting Methods: iLQR-Like Planning

**Idea**: Linearize dynamics, solve quadratic problem.

```
For simple quadratic cost, can find optimal action analytically
Uses: Dynamics Jacobian, Reward Hessian
```

**Simplified Version** (iterative refinement):

```python
def ilqr_like_plan(s, model, reward_fn, value_fn, k=5):
    """Iterative refinement of action sequence"""
    actions = torch.randn(k, action_dim)  # Initialize

    for iteration in range(10):
        # Forward pass: evaluate trajectory
        s_traj = [s]
        for t, a in enumerate(actions):
            s_next = model(s_traj[-1], a)
            s_traj.append(s_next)

        # Backward pass: compute gradients
        returns = 0
        for t in range(k - 1, -1, -1):
            r = reward_fn(s_traj[t], actions[t])
            returns = r + 0.99 * returns

            # Gradient w.r.t. action
            grad = torch.autograd.grad(returns, actions[t], retain_graph=True)[0]

            # Update action (gradient ascent)
            actions[t] += 0.01 * grad

        # Clip actions
        actions = actions.clamp(a_min, a_max)

    return actions[0]
```

**When to Use**:

- Continuous action space (not discrete)
- Differentiable model (neural network)
- Need fast planning (compute-constrained)

---

## Part 14: When NOT to Use Model-Based RL

### Red Flags for Model-Based (Use Model-Free Instead)

**Flag 1: Perfect Simulator Available**

```
Example: Mujoco, Unity, Atari emulator
Benefit: Unlimited free samples
Model-based cost: Training model + planning
Model-free benefit: Just train policy (simpler)
```

**Flag 2: Task Very Simple**

```
Cartpole, MountainCar (horizon < 50)
Benefit of planning: Minimal (too short)
Cost: Model training
Model-free wins
```

**Flag 3: Compute Limited, Samples Abundant**

```
Example: Atari (free samples from emulator)
Model-based: 30 hours train + plan
Model-free: 5 hours train
Model-free wins on compute
```

**Flag 4: Stochastic Environment (High Noise)**

```
Example: Dice rolling, random collisions
Model must predict distribution (hard)
Model-free: Just stores Q-values (simpler)
```

**Flag 5: Evaluation Metric is Compute Time**

```
Model-based sample efficient but compute-expensive
Model-free faster on wall-clock time
Choose based on metric
```

---

## Part 15: Model-Based + Model-Free Hybrid Approaches

### When Both Complement Each Other

**Idea**: Use model-based for data augmentation, model-free for policy.

**Architecture**:

```
Phase 1: Collect real data (model-free exploration)
Phase 2: Train model
Phase 3: Augment data (model-based imagined rollouts)
Phase 4: Train policy on mixed data (model-free algorithm)
```

**MBPO Example**:

- Model-free: SAC (learns Q and policy)
- Model-based: Short rollouts for data augmentation
- Hybrid: Best of both

**Other Hybrids**:

1. **Model for Initialization**:

   ```
   Train model-based policy → Initialize model-free policy
   Fine-tune with model-free (if needed)
   ```

2. **Model for Curriculum**:

   ```
   Model predicts difficulty → Curriculum learning
   Easy → Hard task progression
   ```

3. **Model for Exploration Bonus**:

   ```
   Model uncertainty → Exploration bonus
   Curious about uncertain states
   Combines model-based discovery + policy learning
   ```

---

## Part 16: Common Questions and Answers

### Q1: Should I train one model or ensemble?

**A**: Ensemble (4-7 models) provides uncertainty estimates.

- Single model: Fast training, overconfident
- Ensemble: Disagreement detects out-of-distribution states

For production: Ensemble recommended.

---

### Q2: How long should rollouts be?

**A**: k=5-10 for most tasks.

- Shorter (k=1-3): Very safe, but minimal planning
- Medium (k=5-10): MBPO default, good tradeoff
- Longer (k=20+): Error compounds, avoid

Rule of thumb: k = task_horizon / 10

---

### Q3: When should I retrain the model?

**A**: Every N environment steps or when validation loss increases.

- MBPO: Every 1000 steps
- Dreamer: Every episode
- Dyna-Q: Every 10-100 steps

Monitor validation performance.

---

### Q4: Model-based or model-free for my problem?

**A**: Decision tree:

1. Are real samples expensive? → Model-based
2. Do I have perfect simulator? → Model-free
3. Is task very complex (high-dim)? → Model-based (Dreamer)
4. Is compute limited? → Model-free
5. Default → Model-free (simpler, proven)

---

### Q5: How do I know if model is good?

**A**: Metrics:

1. **Validation MSE**: Low on hold-out test set
2. **Rollout Accuracy**: Predict 10-step trajectory, compare to real
3. **Policy Performance**: Does planning with model improve policy?
4. **Ensemble Disagreement**: Should be low in training dist, high outside

---

## Part 17: Conclusion and Recommendations

### Summary of Key Concepts

**1. World Models**:

- Learn p(s_{t+1} | s_t, a_t) from data
- Pixel vs latent space (latent better for high-dim)
- Deterministic vs stochastic

**2. Planning**:

- MPC: Optimize actions at each step
- Shooting: Sample trajectories
- CEM: Iterative refinement
- Short rollouts (k=5-10) + value bootstrap

**3. Algorithms**:

- **Dyna-Q**: Real + imagined transitions
- **MBPO**: Short rollouts + policy optimization
- **Dreamer**: Latent imagination + policy learning

**4. Error Handling**:

- Ensemble for uncertainty
- Early stopping on disagreement
- Distribution shift via retraining
- Value bootstrapping for tail uncertainty

**5. When to Use**:

- Real samples expensive → Model-based
- Compute cheap → Model-free
- Multi-task → Model-based (reuse)
- Offline RL → Model-based (planning from fixed data)

### Best Practices

1. **Start simple**: Model-free first, model-based only if justified
2. **Use ensemble**: 4-7 models, not single
3. **Keep rollouts short**: k=5-10, not 50
4. **Retrain frequently**: Monitor performance
5. **Validate carefully**: Hold-out test set, policy performance
6. **Understand your domain**: Real samples expensive? Complex? Sparse reward?

### Next Steps

After this skill:

- **Implementation**: value-based-methods, policy-gradient-methods, actor-critic-methods
- **Advanced**: offline-RL (planning from fixed data), curiosity-driven (exploration via model), sim-to-real (domain randomization)
- **Evaluation**: rl-evaluation (proper benchmarking, statistics)

---

**Congratulations!** You now understand model-based RL from foundations through implementation.

You can:

- Implement Dyna-Q for discrete control
- Implement MBPO for continuous control
- Handle model errors appropriately
- Choose the right algorithm for your problem
- Debug model-based learning issues
- Design robust world models

**Key insight**: Model-based RL trades sample complexity for model error. Success requires short rollouts, value bootstrapping, proper error handling, and appropriate algorithm selection.

Go build something amazing!
