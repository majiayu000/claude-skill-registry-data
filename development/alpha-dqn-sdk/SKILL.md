---
name: alpha-dqn-sdk
description: Turnkey operational guide and architectural standards for integrating, deploying, and building downstream reinforcement learning applications using the Alpha-DQN core SDK without modifying internal core code.
---

# Alpha-DQN Core SDK: Turnkey Integration & Operational Guide

This skill provides comprehensive instructions for building downstream reinforcement learning (RL) projects on top of the `alpha-dqn` production engine. 

> [!IMPORTANT]
> **The Immutability Contract (Open-Closed Principle):**
> `src/core/` is **strictly immutable**. Downstream projects must **NEVER** modify or alter files in `src/core/`. 
> All custom behaviors, domain adaptation, and hyperparameter tuning must be achieved via **Configuration Objects**, **Environment Adapters**, or **Pluggable Hooks**.

---

## 1. Architectural Overview & Component Topology

Alpha-DQN is a production-grade Double-DQN framework featuring an evolved algorithmic triad:
1. **Curiosity Novelty Engine (`src/core/curiosity.py`)**: Orthogonal QR RND projections, online IDM Noisy-TV filter, and episodic Euclidean frontier expansion boost.
2. **Adaptive Loss Formulation (`src/core/loss.py`)**: $C^\infty$-smooth Pseudo-Huber loss with asymmetric expectile weighting ($\tau=0.598$), robust MAD scale estimation, and dynamic EMA $\beta$ adaptation.
3. **Novel Directed Epistemic Exploration (`src/core/exploration.py`)**: 3–5 step sticky-action momentum ($12.6\times$ diffusion speed), continuous collision sensing, 3-tier epistemic count UCB, and confident Q-margin exploitation gating.

```
Downstream Project (Your Application)
   │
   ├── 1. Environment Adapter (Transforms domain data into float vectors)
   ├── 2. Configuration (DQNConfig, CuriosityConfig, etc.)
   └── 3. Orchestrator (In-process Python import OR FastAPI HTTP REST client)
         │
         ▼
┌───────────────────────────────────────────────────────────┐
│              ALPHA-DQN CORE SDK (IMMUTABLE)               │
│                                                           │
│  src/schema/       Data contracts & Pydantic models       │
│  src/core/agent    DQNAgent (Double-DQN + Vectorized MLP) │
│  src/core/loss     AdaptiveLoss (Pseudo-Huber Expectile)  │
│  src/core/explore  ExplorationPolicy (Sticky + UCB)       │
│  src/core/curiosity CuriosityEngine (RND + IDM + Frontier)│
│  src/core/buffer   High-throughput Circular Replay Buffer │
│  src/core/persist  JSON Manifest & PyTorch Checkpoints    │
└───────────────────────────────────────────────────────────┘
```

---

## 2. Standard 5-Step Integration Workflow

Whenever you build a new application using Alpha-DQN, follow these five sequential steps:

### Step 1: Map Domain State to a Continuous Vector (`state_size`)
- Extract numeric signals from your domain (e.g. coordinates, velocities, sensor readings, technical indicators).
- Flatten and normalize observations into a 1D Python list of floats `List[float]`.
- Define `state_size = len(observation_vector)`.

### Step 2: Define Discrete Action Space (`action_size`)
- Map discrete agent decisions into contiguous integer indices: `0, 1, ..., action_size - 1`.
- Example for trading: `0: HOLD`, `1: BUY`, `2: SELL` $\to$ `action_size = 3`.
- Example for grid/navigation: `0: UP`, `1: DOWN`, `2: LEFT`, `3: RIGHT` $\to$ `action_size = 4`.

### Step 3: Instantiate Configuration
Construct a typed `DQNConfig` specifying network capacity, training hyperparameters, and desired modules:

```python
from src.schema.dqn import (
    DQNConfig,
    CuriosityConfig,
    AdaptiveLossConfig,
    ExplorationConfig,
)

config = DQNConfig(
    state_size=16,
    action_size=4,
    layers=[128, 128],                  # Configurable MLP architecture
    dueling=True,                       # Separate Value and Advantage streams
    learning_rate=0.0005,
    gamma=0.99,
    batch_size=32,
    memory_capacity=10000,
    train_interval=1,                   # Train after every N steps
    target_update_interval=100,         # Sync target model every N updates
    
    # Evolved Triad Modules (all enabled by default or configurable)
    curiosity=CuriosityConfig(enabled=True, intrinsic_reward_scale=0.1),
    adaptive_loss=AdaptiveLossConfig(enabled=True, initial_beta=0.5, tau=0.598),
    exploration=ExplorationConfig(enabled=True, sticky_min=3, sticky_max=5),
)
```

### Step 4: Initialize Agent
```python
from src.core.agent import DQNAgent

# Device is detected automatically (CUDA if available, otherwise CPU)
agent = DQNAgent(config=config)
agent.init()
```

### Step 5: Execute Standard Episode Loop
Interact with your environment using the standardized 4-call execution cycle:

```python
for episode in range(total_episodes):
    state = env.reset()
    done = False
    
    while not done:
        # 1. Action Inference
        action = agent.act(state)
        
        # 2. Environment Step
        next_state, reward, done, _ = env.step(action)
        
        # 3. Store Transition & Auto-Compute Curiosity / Exploration
        agent.remember(state, action, reward, next_state, done)
        
        # 4. Vectorized Mini-batch Gradient Descent
        agent.train_batch()
        
        state = next_state
        
    # Reset episodic buffers (directional frontier, sticky counters)
    agent.reset_episode()
```

---

## 3. Turnkey Integration Recipes

### Recipe A: Direct Python In-Process Implementation (Minimal Template)

Use this complete script pattern for standalone Python bots, simulators, and data pipelines:

```python
import random
from src.schema.dqn import DQNConfig
from src.core.agent import DQNAgent

def run_application():
    # 1. Setup Configuration
    config = DQNConfig(
        state_size=4,
        action_size=2,
        batch_size=16,
        memory_capacity=5000,
    )
    
    # 2. Instantiate Agent
    agent = DQNAgent(config=config)
    agent.init()
    
    # 3. Execution Loop
    for ep in range(10):
        state = [random.uniform(-1.0, 1.0) for _ in range(config.state_size)]
        
        for step in range(50):
            action = agent.act(state)
            next_state = [s + random.gauss(0, 0.05) for s in state]
            reward = 1.0 if abs(next_state[0]) < 0.5 else -0.5
            done = step == 49
            
            agent.remember(state, action, reward, next_state, done)
            agent.train_batch()
            state = next_state
            
        agent.reset_episode()
        print(f"Episode {ep} finished. Loss: {agent.training_loss:.4f}, Epsilon: {agent.epsilon:.3f}")

    # 4. Save Weights
    agent.save("models/project_weights.json")

if __name__ == "__main__":
    run_application()
```

---

### Recipe B: Gymnasium / OpenAI Gym Adapter

To connect any standard Gymnasium environment (e.g. `CartPole-v1`, `LunarLander-v2`):

```python
import gymnasium as gym
from src.schema.dqn import DQNConfig
from src.core.agent import DQNAgent

def train_gym(env_name: str = "CartPole-v1", episodes: int = 50):
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    
    config = DQNConfig(
        state_size=state_dim,
        action_size=action_dim,
        batch_size=64,
        learning_rate=0.001,
    )
    agent = DQNAgent(config=config)
    agent.init()
    
    for ep in range(episodes):
        obs, _ = env.reset()
        state = obs.tolist()
        total_reward = 0.0
        done = False
        
        while not done:
            action = agent.act(state)
            next_obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            agent.remember(state, action, float(reward), next_obs.tolist(), done)
            agent.train_batch()
            
            state = next_obs.tolist()
            total_reward += reward
            
        agent.reset_episode()
        print(f"Episode {ep+1}: Total Reward = {total_reward}")
        
    env.close()
```

---

### Recipe C: REST API / Microservice Integration (Decoupled Clients)

When the environment is running in a browser, separate microservice, or different programming language:

1. **Start the API Server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Client Interaction (Python `httpx` / JavaScript `fetch`)**:
   ```python
   import httpx

   API_BASE = "http://localhost:8000/api/dqn"

   # 1. Initialize custom agent session
   httpx.post(f"{API_BASE}/init", json={
       "session_id": "crypto_trader_01",
       "config": {
           "state_size": 10,
           "action_size": 3,
           "dueling": True,
           "curiosity": {"enabled": True}
       }
   })

   # 2. Get action
   act_resp = httpx.post(f"{API_BASE}/act", json={
       "session_id": "crypto_trader_01",
       "state": [0.12, 0.45, -0.3, 0.8, 1.2, -0.4, 0.0, 0.2, 0.5, 0.1]
   }).json()
   action = act_resp["action"]

   # 3. Send step transition
   step_resp = httpx.post(f"{API_BASE}/step", json={
       "session_id": "crypto_trader_01",
       "state": [0.12, 0.45, -0.3, 0.8, 1.2, -0.4, 0.0, 0.2, 0.5, 0.1],
       "action": action,
       "reward": 1.5,
       "next_state": [0.15, 0.48, -0.2, 0.9, 1.1, -0.3, 0.1, 0.3, 0.4, 0.2],
       "done": False,
       "auto_train": True
   }).json()

   # 4. Check real-time metrics
   metrics = httpx.get(f"{API_BASE}/metrics?session_id=crypto_trader_01").json()
   print("Current loss:", metrics["training_loss"], "Epsilon:", metrics["epsilon"])
   ```

---

### Recipe D: DQfD Expert Policy Blending (Guided Exploration)

To accelerate training using human rules, heuristics, or a legacy algorithmic controller:

```python
class HeuristicTradingExpert:
    """Provides estimated Q-values based on domain heuristics."""
    def get_q_values(self, state: list[float]) -> list[float]:
        # state[0] = RSI indicator
        rsi = state[0]
        if rsi < 30.0:
            return [0.1, 1.0, 0.0]  # Strong BUY preference
        elif rsi > 70.0:
            return [0.1, 0.0, 1.0]  # Strong SELL preference
        return [1.0, 0.1, 0.1]      # Strong HOLD preference

# Register expert with agent
expert = HeuristicTradingExpert()
agent.set_expert_policy(expert)
```

---

## 4. Operational Best Practices & Troubleshooting

| Topic | Best Practice | Rationale |
| :--- | :--- | :--- |
| **Path Operations** | Never use `from pathlib import Path` outside `src/config/`. Use `src.config` exports (`exists`, `read_text`, etc.). | Preserves project-wide path sandboxing and architectural compliance. |
| **Logging** | Never use raw `print()` statements in production code. Use `logger = setup_logger(Settings.LOG_DIR / "layer.log")`. | Ensures clean structured logging and zero linter violations. |
| **State Normalization** | Normalize all state variables to $[-1.0, 1.0]$ or $[0.0, 1.0]$ before passing to `act()` or `remember()`. | Prevents exploding gradients in early exploration phases. |
| **Reward Clamping** | Use `reward_scale` and `reward_clamp` inside `DQNConfig` for unstable environments. | Stabilizes Bellman target calculations. |
| **Episodic Resets** | Always call `agent.reset_episode()` when `done=True`. | Clears trajectory-specific curiosity frontiers, sticky counters, and collision buffers. |
| **Inference Mode** | Use `agent.act(state, force_pure_neural=True)` for evaluation/production benchmarks. | Completely bypasses exploration, expert blending, and randomness for 100% deterministic evaluation. |

---

## 5. Verification Checklist for New Implementations

Before deploying any new project built on Alpha-DQN, verify:
- [ ] `src/core/` files remain 100% untouched.
- [ ] `state_size` and `action_size` match the downstream environment specification.
- [ ] `agent.reset_episode()` is called at the boundary of each episode.
- [ ] Tests run and pass cleanly via `pytest tests/ -v`.
- [ ] Linter reports 0 violations via `human-skills '{"tool_name": "linter", ...}'`.
