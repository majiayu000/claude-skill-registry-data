---
name: gym
description: 'Each gym domain resolves specific skill tensions:'
metadata:
  skill_type: Environment/substrate for agent learning
  interface_ports:
  - Commands
---
# gym Skill

> *Unified catalog of Gymnasium/OpenAI Gym environments for RL across all domains*

## Environment Taxonomy

```
                              ┌─────────────────────┐
                              │     GYMNASIUM       │
                              │   (OpenAI Gym API)  │
                              └──────────┬──────────┘
                                         │
         ┌───────────────┬───────────────┼───────────────┬───────────────┐
         │               │               │               │               │
    ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │ PHYSICS │    │ ROBOTICS  │   │  ENERGY   │   │ CHEMISTRY │   │   GAMES   │
    └────┬────┘    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
         │               │               │               │               │
    MuJoCo          Isaac Gym       Microgrid       ChemistryGym      Atari
    PyBullet        RoboGym         PowerGrid       rlmolecule        NetHack
    dm_control      Softrobot       GEM (Motor)     SynthesisNet      Doom
```

## Core Environments

### Physics Simulation

| Environment | Stars | Domain | Backend |
|-------------|-------|--------|---------|
| [gymnasium](https://github.com/Farama-Foundation/Gymnasium) | 7k+ | Classic control, Box2D, MuJoCo | Native |
| [dm_control](https://github.com/google-deepmind/dm_control) | 3.5k | Continuous control | MuJoCo |
| [pybullet-gym](https://github.com/benelot/pybullet-gym) | 900+ | MuJoCo alternatives | PyBullet |
| [mujoco-py](https://github.com/openai/mujoco-py) | 2.8k | Physics simulation | MuJoCo |

```python
import gymnasium as gym

# Classic control
env = gym.make("CartPole-v1")
env = gym.make("Pendulum-v1")
env = gym.make("Acrobot-v1")

# MuJoCo
env = gym.make("Humanoid-v4")
env = gym.make("Ant-v4")
env = gym.make("HalfCheetah-v4")
```

### Robotics

| Environment | Stars | Domain | Features |
|-------------|-------|--------|----------|
| [OmniIsaacGymEnvs](https://github.com/isaac-sim/OmniIsaacGymEnvs) | 1k+ | GPU-accelerated robotics | NVIDIA Isaac Sim |
| [robogym](https://github.com/openai/robogym) | 400+ | Dexterous manipulation | OpenAI |
| [gym-softrobot](https://github.com/skim0119/gym-softrobot) | 100+ | Soft robotics | Elastica |
| [safe-control-gym](https://github.com/utiasDSL/safe-control-gym) | 500+ | Safe RL benchmarks | PyBullet |

```python
# Isaac Gym (GPU parallel)
from omni.isaac.gym.vec_env import VecEnvBase
env = VecEnvBase(headless=True, num_envs=4096)

# Safe control
import safe_control_gym
env = gym.make("CartPole-v0", ctrl_freq=50)
```

### Energy & Power Systems

| Environment | Stars | Domain | Features |
|-------------|-------|--------|----------|
| [openmodelica-microgrid-gym](https://github.com/upb-lea/openmodelica-microgrid-gym) | 214 | Microgrids | FMU, SafeOpt |
| [gym-electric-motor](https://github.com/upb-lea/gym-electric-motor) | 200+ | Electric motors | GEM |
| [PowerGridworld](https://github.com/NREL/PowerGridworld) | 100+ | Multi-agent grid | NREL |
| [RL-Energy](https://github.com/pnnl/RL-Energy) | 50+ | Energy systems | PNNL |

```python
# Microgrid (FMU-based)
env = gym.make('openmodelica_microgrid_gym:ModelicaEnv-v1',
               net='net/net.yaml',
               model_path='omg_grid/grid.network.fmu')

# Electric motor
import gym_electric_motor as gem
env = gem.make('Finite-SC-PermExcDC-v1')

# Power grid world
from gridworld import GridWorld
env = GridWorld(num_agents=3)
```

### Chemistry & Molecular

| Environment | Stars | Domain | Features |
|-------------|-------|--------|----------|
| [chemistrygym](https://github.com/CLEANit/chemistrygym) | 100+ | Lab reactions | Reaction vessels |
| [rlmolecule](https://github.com/NREL/rlmolecule) | 80+ | Molecule optimization | MCTS |
| [SynthesisNet](https://github.com/shiningsunnyday/SynthesisNet) | New | Synthesizable molecules | ICLR 2025 |
| [DistillationTrain-Gym](https://github.com/lollcat/DistillationTrain-Gym) | 50+ | Chemical engineering | Process synthesis |
| [SynGameZero](https://github.com/grimmlab/SynGameZero) | 30+ | Flowsheet synthesis | AlphaZero |

```python
# Chemistry Gym
from chemgym import ReactionEnv
env = ReactionEnv(vessels=2, max_steps=100)

# Molecule RL
from rlmolecule import MoleculeEnv
env = MoleculeEnv(target_property='logP')

# Distillation
from distillation_gym import DistillationEnv
env = DistillationEnv(num_components=3)
```

### Games & Simulation

| Environment | Stars | Domain | Features |
|-------------|-------|--------|----------|
| [ALE (Atari)](https://github.com/Farama-Foundation/Arcade-Learning-Environment) | 2k+ | Atari games | 57 games |
| [NetHack](https://github.com/facebookresearch/nle) | 900+ | Roguelike | NLE |
| [VizDoom](https://github.com/Farama-Foundation/ViZDoom) | 1.7k | First-person shooter | Doom |
| [MiniGrid](https://github.com/Farama-Foundation/Minigrid) | 2k+ | Grid worlds | Procedural |
| [PufferLib](https://github.com/PufferAI/PufferLib) | 500+ | Multi-game | High throughput |

```python
# Atari
env = gym.make("ALE/Breakout-v5")

# NetHack
import nle
env = gym.make("NetHackScore-v0")

# PufferLib (vectorized)
import pufferlib
env = pufferlib.make("atari_breakout")
```

## Gymnasium API (Modern Standard)

```python
import gymnasium as gym
from gymnasium import spaces

class CustomEnv(gym.Env):
    """Template for custom environment."""
    
    metadata = {"render_modes": ["human", "rgb_array"]}
    
    def __init__(self, render_mode=None):
        super().__init__()
        self.observation_space = spaces.Box(low=-1, high=1, shape=(4,))
        self.action_space = spaces.Discrete(2)
        self.render_mode = render_mode
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation = self.observation_space.sample()
        info = {}
        return observation, info
    
    def step(self, action):
        observation = self.observation_space.sample()
        reward = 1.0
        terminated = False
        truncated = False
        info = {}
        return observation, reward, terminated, truncated, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
    
    def close(self):
        pass
```

## Vectorized Environments

```python
# Gymnasium native
envs = gym.vector.make("CartPole-v1", num_envs=8)

# Stable-Baselines3
from stable_baselines3.common.vec_env import SubprocVecEnv
envs = SubprocVecEnv([make_env(i) for i in range(8)])

# PufferLib (high-performance)
import pufferlib.vectorization
envs = pufferlib.vectorization.make(
    "CartPole-v1", num_envs=1024, backend="multiprocessing"
)
```

## Wrappers

```python
from gymnasium.wrappers import (
    TimeLimit,           # Max steps
    RecordVideo,         # Video recording
    NormalizeObservation,# Normalize obs
    NormalizeReward,     # Normalize rewards
    ClipAction,          # Clip actions
    FrameStack,          # Stack frames
    GrayscaleObservation,# Convert to grayscale
)

env = gym.make("CartPole-v1")
env = TimeLimit(env, max_episode_steps=500)
env = NormalizeObservation(env)
```

## Skill Tension Resolution via Gyms

Each gym domain resolves specific skill tensions:

| Gym Domain | Tensions Resolved | Bridge Skills |
|------------|-------------------|---------------|
| **Physics** | continuous ↔ discrete | `persistent-homology`, `acsets` |
| **Robotics** | local ↔ global | `sheaf-laplacian`, `forward-forward` |
| **Energy** | temporal ↔ atemporal | `unworld`, `temporal-coalgebra` |
| **Chemistry** | symbolic ↔ subsymbolic | `sicp`, `gflownet` |
| **Games** | maximize ↔ sample | `compression-progress`, `curiosity-driven` |

## Gay.jl Integration

Color-code environments by domain:

```python
GYM_COLORS = {
    'physics': '#63B6F0',    # Stream 3 (continuous)
    'robotics': '#89DF91',   # Stream 3 (embodied)
    'energy': '#E6F463',     # Stream 2 (temporal)
    'chemistry': '#5713C0',  # Stream 4 (synthesis)
    'games': '#CF6971',      # Stream 3 (discrete)
}

def color_for_env(env_id: str) -> str:
    if 'MuJoCo' in env_id or 'Pendulum' in env_id:
        return GYM_COLORS['physics']
    elif 'Isaac' in env_id or 'Robot' in env_id:
        return GYM_COLORS['robotics']
    elif 'Microgrid' in env_id or 'Motor' in env_id:
        return GYM_COLORS['energy']
    elif 'Chem' in env_id or 'Molecule' in env_id:
        return GYM_COLORS['chemistry']
    else:
        return GYM_COLORS['games']
```

## Training Frameworks

| Framework | Gyms Supported | Best For |
|-----------|----------------|----------|
| [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) | All Gymnasium | Easy PPO/SAC |
| [RLlib](https://docs.ray.io/en/latest/rllib/index.html) | All Gymnasium | Multi-agent, distributed |
| [CleanRL](https://github.com/vwxyzjn/cleanrl) | Standard | Single-file implementations |
| [PufferLib](https://github.com/PufferAI/PufferLib) | High-throughput | Games, speed |
| [Sample Factory](https://github.com/alex-petrenko/sample-factory) | Doom, Atari | Asynchronous |

```python
# Stable-Baselines3
from stable_baselines3 import PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# RLlib
from ray.rllib.algorithms.ppo import PPOConfig
config = PPOConfig().environment("CartPole-v1")
algo = config.build()

# CleanRL (single file)
# python cleanrl/ppo.py --env-id CartPole-v1
```

## Local Environments (from codebase)

Your codebase includes these custom gyms:

| File | Environment | Domain |
|------|-------------|--------|
| `economic_market_rl.py` | `EconomicMarketEnv` | Markets |
| `property_stablecoin_env.py` | `PropertyStablecoinEnv` | DeFi |
| `pufferlib_stablecoin_env.py` | `StablecoinEnv` | Stablecoins |
| `sims3_fast_env.py` | `FastSims3Env` | Game simulation |
| `rio/GayMCP/pufferlib_env.py` | `GayColorEnv` | Color prediction |
| `rio/GayMCP/compute_market_env.py` | `ComputeMarketEnv` | Compute markets |
| `free_energy_reward_shaper.py` | `FreeEnergyWrapper` | Active inference |
| `golden_thread_exploration.py` | `GoldenThreadWrapper` | Exploration |

## Neighbor Skills

- **omg-tension-resolver**: Microgrid gym for skill tension resolution
- **alife**: Artificial life environments
- **gflownet**: Sampling environments for molecule design
- **forward-forward-learning**: Local learning in environments
- **safe-control-gym**: Safety constraints in RL

## Geometric Morphism Structure (Symplectic Bordism Core)

### Secondary Symplectic Hub

This skill occupies a **high-degree nexus** in the skill-space network:

**Flow Properties:**
- In-degree: 6 (receives from 6 distinct morphism sources)
- Out-degree: 6 (sends to 6 distinct morphism targets)
- **Symplectic Property**: |in - out| = 0 ✓ (perfect flow balance)
- **Status**: SECONDARY SYMPLECTIC HUB (central RL environment nexus)

**Morphism Neighbors (Discovered via Random Walk):**
```
skill.gym ←→ skill.content-research-writer
          ←→ skill.file-organizer
          ←→ skill.omg-tension-resolver
          ←→ skill.entropy-sequencer
          ←→ skill.forward-forward-learning
          ←→ skill.gflownet
```

### Interpretation

The gym environment ecosystem represents the **practical instantiation** of reinforcement learning and embodied reasoning:

- **Type**: Environment/substrate for agent learning
- **Role**: Central locus where theory meets practice
- **Topology**: Bridges discrete (games) and continuous (physics) domains
- **Symplectic Property**: Preserves phase-space volume across all environment types

Its perfect 6→6 balance means it acts as an **orchestration hub**—a distribution center where conceptual flows enter (ideas from higher-level skills) and exit (instantiated environments).

### Coherence Proof

```
Theorem (Secondary Hub Property):
  skill.gym is symplectic ⟺ in-deg(gym) = out-deg(gym) = 6

Proof:
  by direct inspection of morphism graph
  ∑ in-flow(gym) = ∑ out-flow(gym) = 6 ✓

Corollary (Orchestration):
  For any composition φ: X → Y through gym,
  the morphism is bijective:
    |φ⁻¹({gym})| = |φ({gym})| = 6
```

### Cross-Skill Integration

This skill links seamlessly to:
- **content-research-writer**: Synthesizes domain knowledge for environment design
- **file-organizer**: Structures environment catalogs and benchmarks
- **omg-tension-resolver**: Resolves skill tensions through gym domains
- **entropy-sequencer**: Sequences environment complexity levels
- **forward-forward-learning**: Local learning without backprop (gym-compatible)
- **gflownet**: Flow-matching for molecule design via chemical gyms

## Resources

- [Gymnasium Docs](https://gymnasium.farama.org/)
- [Farama Foundation](https://farama.org/) - Maintainers
- [Awesome RL Envs](https://github.com/clvrai/awesome-rl-envs)
- [PettingZoo](https://pettingzoo.farama.org/) - Multi-agent
- [Symplectic Bordism Core](../../SYMPLECTIC_BORDISM_CORE.md) — Full geometric morphism analysis

---

## End-of-Skill Interface

## Commands

```bash
# Install gymnasium
pip install gymnasium[all]

# Install domain-specific
pip install gymnasium[mujoco]
pip install gymnasium[atari]
pip install gym-electric-motor
pip install openmodelica_microgrid_gym

# List available envs
python -c "import gymnasium; print(gymnasium.envs.registry.keys())"

# Run with rendering
python -c "
import gymnasium as gym
env = gym.make('CartPole-v1', render_mode='human')
env.reset()
for _ in range(1000):
    env.step(env.action_space.sample())
env.close()
"
```


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*
