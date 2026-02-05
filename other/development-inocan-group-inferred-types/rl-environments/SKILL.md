---
name: rl-environments
description: Gym/gymnasium API - custom environments, spaces, wrappers, vectorization, debugging
---

# RL Environments: Building and Debugging Custom Environments

## When to Use This Skill

Invoke this skill when you need to:

- **Create Custom Environments**: Build a new environment from scratch using Gym/gymnasium
- **Define Observation/Action Spaces**: Design Box, Discrete, Dict, Tuple spaces correctly
- **Use Environment Wrappers**: Add preprocessing, modify rewards, implement time limits
- **Parallelize Environments**: Choose between DummyVectorEnv, SyncVectorEnv, AsyncVectorEnv
- **Debug Environment Bugs**: Diagnose reset/step issues, reward scaling, space mismatches
- **Test Environments**: Validate environments before training agents
- **Handle API Differences**: Migrate between Gym versions or Gym vs gymnasium
- **Implement Complex State**: Manage multi-component observations and state systems
- **Enforce Action Bounds**: Properly clip or scale actions
- **Catch Common Pitfalls**: Avoid 10+ common environment implementation mistakes

**Core Problem**: Environments are the foundation of RL training. Broken environments cause 80% of RL failures, but environment bugs are often missed because they don't error—they silently break training. This skill systematically teaches correct environment design and provides a debugging methodology.

## Do NOT Use This Skill For

- **Algorithm implementation** (route to specific algorithm skills like value-based-methods, policy-gradient-methods, actor-critic-methods)
- **Reward design and shaping** (route to reward-shaping-engineering for reward function engineering and potential-based shaping)
- **RL theory and foundations** (route to rl-foundations for MDPs, Bellman equations, value functions)
- **Training debugging beyond environment issues** (route to rl-debugging for systematic diagnosis of training failures)
- **Exploration strategy selection** (route to exploration-strategies for ε-greedy, curiosity-driven, RND methods)

---

## Part 1: Understanding the Gym/Gymnasium API

### The Standard Interface

Every Gym/Gymnasium environment implements:

```python
import gymnasium as gym  # or 'gym' for older versions

class CustomEnv(gym.Env):
    """Template for all custom environments"""

    def __init__(self):
        # Define action and observation spaces
        self.action_space = gym.spaces.Discrete(4)  # 4 possible actions
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=(84, 84, 3), dtype=np.uint8
        )

    def reset(self, seed=None):
        """Reset environment to initial state

        Returns:
            observation (np.ndarray): Initial observation
            info (dict): Auxiliary info (can be empty dict)
        """
        super().reset(seed=seed)
        obs = self._get_initial_observation()
        info = {}
        return obs, info

    def step(self, action):
        """Take one action in the environment

        Args:
            action: Action from action_space

        Returns:
            observation (np.ndarray): Current observation after action
            reward (float): Reward for this step
            terminated (bool): True if episode ended (goal/failure)
            truncated (bool): True if episode cut off (time limit)
            info (dict): Auxiliary info
        """
        obs = self._apply_action(action)
        reward = self._compute_reward()
        terminated = self._is_done()
        truncated = False  # Set by TimeLimit wrapper usually
        info = {}
        return obs, reward, terminated, truncated, info

    def render(self, mode='human'):
        """Visualize the environment (optional)"""
        pass

    def close(self):
        """Cleanup resources (optional)"""
        pass
```

### Key API Points

**1. Reset Format (Gymnasium API)**

```python
# CORRECT: Reset returns (observation, info)
observation, info = env.reset()

# WRONG: Old Gym API returned just observation
observation = env.reset()  # This is Gym, not Gymnasium
```

**2. Step Format (Gymnasium API)**

```python
# CORRECT: Step returns (obs, reward, terminated, truncated, info)
obs, reward, terminated, truncated, info = env.step(action)

# WRONG: Old Gym API
obs, reward, done, info = env.step(action)  # 'done' is single boolean
```

**3. Gym vs Gymnasium**

| Feature | Gym (OpenAI) | Gymnasium (Maintained) |
|---------|--------------|----------------------|
| Reset return | `obs` | `(obs, info)` |
| Step return | `(obs, r, done, info)` | `(obs, r, terminated, truncated, info)` |
| Render | `env.render(mode='human')` | `env.render()`; mode set at init |
| Import | `import gym` | `import gymnasium as gym` |
| Support | Deprecated | Current standard |

**Decision**: Use `gymnasium` for new code. If stuck with older code:

```python
# Compatibility wrapper
try:
    import gymnasium as gym
except ImportError:
    import gym
```

---

## Part 2: Observation and Action Space Design

### Space Types

**Discrete Space** (for discrete actions or observations)

```python
# 4 possible actions: 0, 1, 2, 3
action_space = gym.spaces.Discrete(4)

# 5 possible discrete states
observation_space = gym.spaces.Discrete(5)

# With start parameter
action_space = gym.spaces.Discrete(4, start=1)  # 1, 2, 3, 4
```

**Box Space** (for continuous or image data)

```python
# Continuous control: 3D position, each in [-1, 1]
action_space = gym.spaces.Box(
    low=-1.0,
    high=1.0,
    shape=(3,),
    dtype=np.float32
)

# Image observation: 84x84 RGB, pixels 0-255
observation_space = gym.spaces.Box(
    low=0,
    high=255,
    shape=(84, 84, 3),
    dtype=np.uint8
)

# Multi-component continuous: 2D position + 1D velocity
observation_space = gym.spaces.Box(
    low=np.array([-1.0, -1.0, -10.0]),
    high=np.array([1.0, 1.0, 10.0]),
    dtype=np.float32
)
```

**Dict Space** (for structured observations with multiple components)

```python
# Multi-component observation: image + state vector
observation_space = gym.spaces.Dict({
    'image': gym.spaces.Box(0, 255, (84, 84, 3), dtype=np.uint8),
    'position': gym.spaces.Box(-1, 1, (2,), dtype=np.float32),
})

# Access in reset/step:
obs = {
    'image': np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8),
    'position': np.array([0.5, -0.3], dtype=np.float32),
}
```

**Tuple Space** (for ordered multiple components)

```python
observation_space = gym.spaces.Tuple((
    gym.spaces.Box(-1, 1, (2,), dtype=np.float32),  # Position
    gym.spaces.Discrete(4),  # Direction
))

# Access:
obs = (np.array([0.5, -0.3], dtype=np.float32), 2)
```

**MultiDiscrete** (for multiple discrete action dimensions)

```python
# Game with 4 actions per agent, 3 agents
action_space = gym.spaces.MultiDiscrete([4, 4, 4])

# Or asymmetric
action_space = gym.spaces.MultiDiscrete([3, 4, 5])  # Different choices per dimension
```

### Space Validation Patterns

**Always validate that observations match the space:**

```python
def reset(self, seed=None):
    super().reset(seed=seed)
    obs = self._get_observation()

    # CRITICAL: Validate observation against space
    assert self.observation_space.contains(obs), \
        f"Observation {obs} not in space {self.observation_space}"

    return obs, {}

def step(self, action):
    # CRITICAL: Validate action is in action space
    assert self.action_space.contains(action), \
        f"Action {action} not in space {self.action_space}"

    obs = self._apply_action(action)

    # Validate observation
    assert self.observation_space.contains(obs), \
        f"Observation {obs} not in space {self.observation_space}"

    reward = self._compute_reward()
    terminated = self._check_done()
    truncated = False

    return obs, reward, terminated, truncated, {}
```

### Common Space Mistakes

**Mistake 1: dtype mismatch (uint8 vs float32)**

```python
# WRONG: Space says uint8 but observation is float32
observation_space = gym.spaces.Box(0, 255, (84, 84, 3), dtype=np.uint8)
obs = np.random.random((84, 84, 3)).astype(np.float32)  # MISMATCH!
assert self.observation_space.contains(obs)  # FAILS

# CORRECT: Match dtype
observation_space = gym.spaces.Box(0, 1, (84, 84, 3), dtype=np.float32)
obs = np.random.random((84, 84, 3)).astype(np.float32)
assert self.observation_space.contains(obs)  # PASSES
```

**Mistake 2: Range mismatch**

```python
# WRONG: Observation outside declared range
observation_space = gym.spaces.Box(0, 1, (4,), dtype=np.float32)
obs = np.array([0.5, 1.5, 0.2, 0.8], dtype=np.float32)  # 1.5 > 1!
assert self.observation_space.contains(obs)  # FAILS

# CORRECT: Ensure observations stay within bounds
obs = np.clip(obs, 0, 1)
```

**Mistake 3: Shape mismatch**

```python
# WRONG: Wrong shape
observation_space = gym.spaces.Box(0, 255, (84, 84, 3), dtype=np.uint8)
obs = np.random.randint(0, 256, (84, 84), dtype=np.uint8)  # 2D, not 3D!
assert self.observation_space.contains(obs)  # FAILS

# CORRECT: Match shape exactly
obs = np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8)
```

---

## Part 3: Creating Custom Environments - Template

### Step 1: Inherit from gym.Env

```python
import gymnasium as gym
import numpy as np

class CartPoleMini(gym.Env):
    """Simple environment for demonstration"""

    # These are required attributes
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode=None):
        # Store render mode
        self.render_mode = render_mode

        # Action space: push cart left (0) or right (1)
        self.action_space = gym.spaces.Discrete(2)

        # Observation space: position, velocity, angle, angular velocity
        self.observation_space = gym.spaces.Box(
            low=np.array([-2.4, -10, -0.2, -10], dtype=np.float32),
            high=np.array([2.4, 10, 0.2, 10], dtype=np.float32),
            dtype=np.float32
        )

        # Episode variables
        self.state = None
        self.steps = 0
        self.max_steps = 500
```

### Step 2: Implement reset()

```python
    def reset(self, seed=None):
        """Reset to initial state

        Returns:
            obs (np.ndarray): Initial observation
            info (dict): Empty dict
        """
        super().reset(seed=seed)

        # Initialize state to center position with small noise
        self.state = np.array(
            [
                self.np_random.uniform(-0.05, 0.05),  # position
                0.0,  # velocity
                self.np_random.uniform(-0.05, 0.05),  # angle
                0.0,  # angular velocity
            ],
            dtype=np.float32
        )
        self.steps = 0

        # Validate and return
        assert self.observation_space.contains(self.state)
        return self.state, {}
```

### Step 3: Implement step()

```python
    def step(self, action):
        """Execute one step of the environment

        Args:
            action: 0 (push left) or 1 (push right)

        Returns:
            obs, reward, terminated, truncated, info
        """
        assert self.action_space.contains(action)

        # Validate state
        assert self.observation_space.contains(self.state)

        x, x_dot, theta, theta_dot = self.state

        # Physics: apply force based on action
        force = 10.0 if action == 1 else -10.0

        # Simplified cartpole physics
        acceleration = (force + 0.1 * theta) / 1.0
        theta_dot_new = theta_dot + 0.02 * acceleration
        theta_new = theta + 0.02 * theta_dot

        x_dot_new = x_dot + 0.02 * acceleration
        x_new = x + 0.02 * x_dot

        # Update state
        self.state = np.array(
            [x_new, x_dot_new, theta_new, theta_dot_new],
            dtype=np.float32
        )

        # Clamp values to stay in bounds
        self.state = np.clip(self.state,
                            self.observation_space.low,
                            self.observation_space.high)

        # Compute reward
        reward = 1.0 if abs(theta) < 0.2 else -1.0

        # Check termination
        x, theta = self.state[0], self.state[2]
        terminated = abs(x) > 2.4 or abs(theta) > 0.2

        # Check truncation (max steps)
        self.steps += 1
        truncated = self.steps >= self.max_steps

        # Validate output
        assert self.observation_space.contains(self.state)
        assert isinstance(reward, (int, float))

        return self.state, float(reward), terminated, truncated, {}
```

### Step 4: Implement render() and close() (Optional)

```python
    def render(self):
        """Render the environment (optional)"""
        if self.render_mode == "human":
            # Print state for visualization
            x, x_dot, theta, theta_dot = self.state
            print(f"Position: {x:.2f}, Angle: {theta:.2f}")

    def close(self):
        """Cleanup (optional)"""
        pass
```

### Complete Custom Environment Example

```python
import gymnasium as gym
import numpy as np

class GridWorldEnv(gym.Env):
    """Simple 5x5 grid world where agent seeks goal"""

    def __init__(self):
        # Actions: up=0, right=1, down=2, left=3
        self.action_space = gym.spaces.Discrete(4)

        # Observation: (x, y) position
        self.observation_space = gym.spaces.Box(
            low=0, high=4, shape=(2,), dtype=np.int32
        )

        self.grid_size = 5
        self.goal = np.array([4, 4], dtype=np.int32)
        self.agent_pos = np.array([0, 0], dtype=np.int32)
        self.steps = 0
        self.max_steps = 50

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.agent_pos = np.array([0, 0], dtype=np.int32)
        self.steps = 0
        assert self.observation_space.contains(self.agent_pos)
        return self.agent_pos.copy(), {}

    def step(self, action):
        assert self.action_space.contains(action)

        # Move agent
        moves = {
            0: np.array([0, 1], dtype=np.int32),   # up
            1: np.array([1, 0], dtype=np.int32),   # right
            2: np.array([0, -1], dtype=np.int32),  # down
            3: np.array([-1, 0], dtype=np.int32),  # left
        }

        self.agent_pos += moves[action]
        self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size - 1)

        # Reward
        distance_to_goal = np.linalg.norm(self.agent_pos - self.goal)
        reward = 1.0 if np.array_equal(self.agent_pos, self.goal) else -0.01

        # Done
        terminated = np.array_equal(self.agent_pos, self.goal)
        self.steps += 1
        truncated = self.steps >= self.max_steps

        return self.agent_pos.copy(), reward, terminated, truncated, {}
```

---

## Part 4: Environment Wrappers

### Why Use Wrappers?

Wrappers add functionality without modifying the original environment:

```python
# Without wrappers: modify environment directly (WRONG - mixes concerns)
class CartPoleNormalized(CartPole):
    def step(self, action):
        obs, reward, done, info = super().step(action)
        obs = obs / 2.4  # Normalize observation
        reward = reward / 100  # Normalize reward
        return obs, reward, done, info

# With wrappers: compose functionality (RIGHT - clean separation)
env = CartPole()
env = NormalizeObservation(env)
env = NormalizeReward(env)
```

### Wrapper Pattern

```python
class BaseWrapper(gym.Wrapper):
    """Base class for all wrappers"""

    def __init__(self, env):
        super().__init__(env)
        # Don't modify spaces unless you redefine them

    def reset(self, seed=None):
        obs, info = self.env.reset(seed=seed)
        return self._process_observation(obs), info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        obs = self._process_observation(obs)
        reward = self._process_reward(reward)
        return obs, reward, terminated, truncated, info

    def _process_observation(self, obs):
        return obs

    def _process_reward(self, reward):
        return reward
```

### Common Built-in Wrappers

**TimeLimit: Add episode time limit**

```python
env = gym.make("CartPole-v1")
env = gym.wrappers.TimeLimit(env, max_episode_steps=500)
# Now truncated=True after 500 steps
```

**NormalizeObservation: Normalize observations to [-1, 1]**

```python
env = gym.wrappers.NormalizeObservation(env)
# Observations normalized using running mean/std
```

**RecordVideo: Save episode videos**

```python
env = gym.wrappers.RecordVideo(
    env,
    video_folder="videos/",
    episode_trigger=lambda ep: ep % 10 == 0
)
```

**ClipAction: Clip actions to action space bounds**

```python
env = gym.wrappers.ClipAction(env)
# Actions automatically clipped to [-1, 1] or similar
```

### Custom Wrapper Example: Scale Rewards

```python
class ScaleRewardWrapper(gym.Wrapper):
    """Scale rewards by a constant factor"""

    def __init__(self, env, scale=0.1):
        super().__init__(env)
        self.scale = scale

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward * self.scale, terminated, truncated, info
```

**Custom Wrapper Example: Frame Stacking**

```python
class FrameStackWrapper(gym.Wrapper):
    """Stack last 4 frames for temporal information"""

    def __init__(self, env, num_frames=4):
        super().__init__(env)
        self.num_frames = num_frames
        self.frame_buffer = collections.deque(maxlen=num_frames)

        # Modify observation space to include stacking
        old_space = env.observation_space
        self.observation_space = gym.spaces.Box(
            low=old_space.low.min(),
            high=old_space.high.max(),
            shape=(old_space.shape[0], old_space.shape[1],
                   old_space.shape[2] * num_frames),
            dtype=old_space.dtype
        )

    def reset(self, seed=None):
        obs, info = self.env.reset(seed=seed)
        self.frame_buffer.clear()
        for _ in range(self.num_frames):
            self.frame_buffer.append(obs)
        return self._get_stacked_obs(), info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self.frame_buffer.append(obs)
        return self._get_stacked_obs(), reward, terminated, truncated, info

    def _get_stacked_obs(self):
        # Stack frames along channel dimension
        return np.concatenate(list(self.frame_buffer), axis=2)
```

### Wrapper Chaining

```python
# Correct: Chain wrappers for composable functionality
env = gym.make("Atari2600-v0")
env = gym.wrappers.TimeLimit(env, max_episode_steps=4500)
env = gym.wrappers.ClipAction(env)
env = FrameStackWrapper(env, num_frames=4)
env = gym.wrappers.NormalizeObservation(env)

# Order matters: think about data flow
# raw env -> ClipAction -> FrameStack -> NormalizeObservation
```

---

## Part 5: Vectorized Environments

### Types of Vectorized Environments

**DummyVectorEnv: Serial execution (simple, slowest)**

```python
from gymnasium.vector import DummyVectorEnv

# Create 4 independent environments (serial)
envs = DummyVectorEnv([
    lambda: gym.make("CartPole-v1")
    for i in range(4)
])

obs, info = envs.reset()  # obs shape: (4, 4)
actions = np.array([0, 1, 1, 0])  # 4 actions
obs, rewards, terminateds, truncateds, info = envs.step(actions)
# rewards shape: (4,)
```

**SyncVectorEnv: Synchronized parallel (fast, moderate complexity)**

```python
from gymnasium.vector import SyncVectorEnv

# Create 8 parallel environments (all step together)
envs = SyncVectorEnv([
    lambda: gym.make("CartPole-v1")
    for i in range(8)
])

obs, info = envs.reset()
# All 8 envs step synchronously
obs, rewards, terminateds, truncateds, info = envs.step(actions)
```

**AsyncVectorEnv: Asynchronous parallel (fastest, most complex)**

```python
from gymnasium.vector import AsyncVectorEnv

# Create 16 parallel environments (independent processes)
envs = AsyncVectorEnv([
    lambda: gym.make("CartPole-v1")
    for i in range(16)
])

# Same API as SyncVectorEnv but faster
obs, info = envs.reset()
obs, rewards, terminateds, truncateds, info = envs.step(actions)
envs.close()  # IMPORTANT: Close async envs to cleanup processes
```

### Comparison and Decision Tree

| Feature | Dummy | Sync | Async |
|---------|-------|------|-------|
| Speed | Slow | Fast | Fastest |
| CPU cores | 1 | 1 (+ GIL) | N |
| Memory | Low | Moderate | High |
| Complexity | Simple | Medium | Complex |
| Debugging | Easy | Medium | Hard |
| Best for | Testing | Training | Large-scale training |

**When to use each:**

```python
num_envs = 32

if num_envs <= 1:
    # Single environment
    env = gym.make("CartPole-v1")
elif num_envs <= 4:
    # Few environments: use Dummy for simplicity
    env = DummyVectorEnv([gym.make("CartPole-v1") for _ in range(num_envs)])
elif num_envs <= 8:
    # Medium: use Sync for speed without complexity
    env = SyncVectorEnv([gym.make("CartPole-v1") for _ in range(num_envs)])
else:
    # Many: use Async for maximum speed
    env = AsyncVectorEnv([gym.make("CartPole-v1") for _ in range(num_envs)])
```

### Common Vectorized Environment Bugs

**Bug 1: Forgetting to close AsyncVectorEnv**

```python
# WRONG: Processes leak
envs = AsyncVectorEnv([...] for _ in range(16))
# ... training ...
# Forgot to close! Processes stay alive, memory leaks

# CORRECT: Always close
try:
    envs = AsyncVectorEnv([...] for _ in range(16))
    # ... training ...
finally:
    envs.close()  # Cleanup

# Or use context manager
from contextlib import contextmanager

@contextmanager
def make_async_envs(num_envs):
    envs = AsyncVectorEnv([...] for _ in range(num_envs))
    try:
        yield envs
    finally:
        envs.close()
```

**Bug 2: Non-parallel-safe environment**

```python
# WRONG: Environment uses shared state, breaks with AsyncVectorEnv
class NonParallelEnv(gym.Env):
    global_counter = 0  # SHARED STATE!

    def step(self, action):
        self.global_counter += 1  # Race condition with async!
        ...

# CORRECT: No shared state
class ParallelSafeEnv(gym.Env):
    def __init__(self):
        self.counter = 0  # Instance variable, not shared

    def step(self, action):
        self.counter += 1  # Safe in parallel
        ...
```

**Bug 3: Handling auto-reset in vectorized envs**

```python
# When an episode terminates in vectorized env, it auto-resets
obs, rewards, terminateds, truncateds, info = envs.step(actions)

# If terminateds[i] is True, envs[i] has been auto-reset
# The obs[i] is the NEW initial observation from the reset
# NOT the final observation of the episode

# To get final observation before reset:
obs, rewards, terminateds, truncateds, info = envs.step(actions)
final_obs = info['final_observation']  # Original terminal obs
reset_obs = obs  # New obs from auto-reset
```

---

## Part 6: Common Environment Bugs and Fixes

### Bug 1: Reward Scale Too Large

**Symptom**: Training unstable, losses spike, agent behavior random

```python
# WRONG: Reward in range [0, 1000]
def step(self, action):
    reward = self.goal_distance * 1000  # Can be up to 1000!
    return obs, reward, done, truncated, info

# Problem: Gradients huge -> param updates too large -> training breaks

# CORRECT: Reward in [-1, 1]
def step(self, action):
    reward = self.goal_distance  # Range [0, 1]
    reward = reward - 0.5  # Scale to [-0.5, 0.5]
    return obs, reward, done, truncated, info

# Or normalize post-hoc
reward = np.clip(reward / 1000, -1, 1)
```

### Bug 2: Action Not Applied Correctly

**Symptom**: Agent learns but behavior doesn't match reward signal

```python
# WRONG: Action read but not used
def step(self, action):
    obs = self._get_next_obs()  # Doesn't use action!
    reward = 1.0  # Reward independent of action
    return obs, reward, False, False, {}

# CORRECT: Action determines next state
def step(self, action):
    self._apply_action_to_physics(action)
    obs = self._get_next_obs()
    reward = self._compute_reward(action)
    return obs, reward, False, False, {}
```

### Bug 3: Missing Terminal State Flag

**Symptom**: Episodes don't end properly, agent never learns boundaries

```python
# WRONG: Always done=False
def step(self, action):
    ...
    return obs, reward, False, False, {}  # Episode never ends!

# CORRECT: Set terminated when episode should end
def step(self, action):
    ...
    terminated = self._check_done_condition()
    if terminated:
        reward += 100  # Bonus for reaching goal
    return obs, reward, terminated, False, {}

# Also differentiate from truncation
def step(self, action):
    ...
    self.steps += 1
    terminated = self._reached_goal()  # Success condition
    truncated = self.steps >= self.max_steps  # Time limit
    return obs, reward, terminated, truncated, {}
```

### Bug 4: Observation/Space Mismatch

**Symptom**: Training crashes or behaves oddly after environment change

```python
# WRONG: Space and observation don't match
def __init__(self):
    self.observation_space = gym.spaces.Box(0, 1, (4,), dtype=np.float32)

def step(self, action):
    obs = np.random.randint(0, 256, (4,), dtype=np.uint8)  # uint8!
    return obs, reward, done, truncated, {}  # Mismatch!

# CORRECT: Match dtype and range
def __init__(self):
    self.observation_space = gym.spaces.Box(0, 255, (4,), dtype=np.uint8)

def step(self, action):
    obs = np.random.randint(0, 256, (4,), dtype=np.uint8)  # Matches!
    assert self.observation_space.contains(obs)
    return obs, reward, done, truncated, {}
```

### Bug 5: Reset Not Initializing State

**Symptom**: First episode works, subsequent episodes fail

```python
# WRONG: Reset doesn't actually reset
def reset(self, seed=None):
    super().reset(seed=seed)
    # Forgot to initialize state!
    return self.state, {}  # self.state is stale from last episode

# CORRECT: Reset initializes everything
def reset(self, seed=None):
    super().reset(seed=seed)
    self.state = self._initialize_state()
    self.steps = 0
    return self.state, {}
```

### Bug 6: Non-Deterministic Environment Without Proper Seeding

**Symptom**: Same reset produces different initial states, breaks reproducibility

```python
# WRONG: Randomness not seeded
def reset(self, seed=None):
    super().reset(seed=seed)
    self.state = np.random.randn(4)  # Uses default RNG, ignores seed!
    return self.state, {}

# CORRECT: Use self.np_random which respects seed
def reset(self, seed=None):
    super().reset(seed=seed)
    # self.np_random is seeded by super().reset()
    self.state = self.np_random.randn(4)
    return self.state, {}
```

### Bug 7: Info Dict Contains Non-Serializable Objects

**Symptom**: Episode fails when saving/loading with replay buffers

```python
# WRONG: Info dict contains unpicklable objects
def step(self, action):
    info = {
        'env': self,  # Can't pickle!
        'callback': self.callback_fn,  # Can't pickle!
    }
    return obs, reward, done, truncated, info

# CORRECT: Only basic types in info dict
def step(self, action):
    info = {
        'level': self.level,
        'score': self.score,
        'x_position': float(self.x),
    }
    return obs, reward, done, truncated, info
```

### Bug 8: Action Space Not Enforced

**Symptom**: Agent takes actions outside valid range, causes crashes

```python
# WRONG: Action space defined but not enforced
def __init__(self):
    self.action_space = gym.spaces.Box(-1, 1, (3,))

def step(self, action):
    # action could be [10, 10, 10] and we don't catch it!
    velocity = action * 10  # Huge velocity!
    ...

# CORRECT: Clip or validate actions
def step(self, action):
    assert self.action_space.contains(action), \
        f"Invalid action {action}"

    # Or clip to bounds
    action = np.clip(action,
                     self.action_space.low,
                     self.action_space.high)
    ...
```

### Bug 9: Observation Normalization Not Applied

**Symptom**: Training unstable when observations are in [0, 255] instead of [0, 1]

```python
# WRONG: Large observation range breaks training
def step(self, action):
    obs = self.render_to_image()  # Range [0, 255]
    return obs, reward, done, truncated, {}

# CORRECT: Normalize observations
def step(self, action):
    obs = self.render_to_image()  # Range [0, 255]
    obs = obs.astype(np.float32) / 255.0  # Normalize to [0, 1]
    return obs, reward, done, truncated, {}

# Or use NormalizeObservation wrapper
env = NormalizeObservation(env)
```

### Bug 10: Forgetting to Return Info Dict

**Symptom**: Step returns wrong number of values, crashes agent training loop

```python
# WRONG: Step returns 4 values (old Gym API)
def step(self, action):
    return obs, reward, done, info  # WRONG!

# CORRECT: Step returns 5 values (Gymnasium API)
def step(self, action):
    return obs, reward, terminated, truncated, info

# Or use try-except during migration
try:
    obs, reward, terminated, truncated, info = env.step(action)
except ValueError:
    obs, reward, done, info = env.step(action)
    terminated = done
    truncated = False
```

---

## Part 7: Environment Testing Checklist

Before training an RL agent on a custom environment, validate:

### Pre-Training Validation Checklist

```python
class EnvironmentValidator:
    """Validate custom environment before training"""

    def validate_all(self, env):
        """Run all validation tests"""
        print("Validating environment...")

        # 1. Spaces are valid
        self.validate_spaces(env)
        print("✓ Spaces valid")

        # 2. Reset works
        obs, info = self.validate_reset(env)
        print("✓ Reset works")

        # 3. Step works and returns correct format
        self.validate_step(env, obs)
        print("✓ Step works")

        # 4. Observations are valid
        self.validate_observations(env, obs)
        print("✓ Observations valid")

        # 5. Actions are enforced
        self.validate_actions(env)
        print("✓ Actions enforced")

        # 6. Terminal states work
        self.validate_termination(env)
        print("✓ Termination works")

        # 7. Environment is reproducible
        self.validate_reproducibility(env)
        print("✓ Reproducibility verified")

        # 8. Random agent can run
        self.validate_random_agent(env)
        print("✓ Random agent runs")

        print("\nEnvironment validation PASSED!")

    def validate_spaces(self, env):
        """Check spaces are defined"""
        assert hasattr(env, 'action_space'), "No action_space"
        assert hasattr(env, 'observation_space'), "No observation_space"
        assert isinstance(env.action_space, gym.spaces.Space)
        assert isinstance(env.observation_space, gym.spaces.Space)

    def validate_reset(self, env):
        """Check reset returns (obs, info)"""
        result = env.reset()
        assert isinstance(result, tuple) and len(result) == 2, \
            f"Reset should return (obs, info), got {result}"
        obs, info = result
        assert isinstance(info, dict), "Info should be dict"
        return obs, info

    def validate_step(self, env, obs):
        """Check step returns 5-tuple"""
        action = env.action_space.sample()
        result = env.step(action)
        assert isinstance(result, tuple) and len(result) == 5, \
            f"Step should return 5-tuple, got {len(result)}"
        obs, reward, terminated, truncated, info = result
        assert isinstance(reward, (int, float)), "Reward must be number"
        assert isinstance(terminated, (bool, np.bool_)), "terminated must be bool"
        assert isinstance(truncated, (bool, np.bool_)), "truncated must be bool"
        assert isinstance(info, dict), "Info must be dict"

    def validate_observations(self, env, obs):
        """Check observations match space"""
        assert env.observation_space.contains(obs), \
            f"Observation {obs.shape} not in space {env.observation_space}"

    def validate_actions(self, env):
        """Check invalid actions fail"""
        if isinstance(env.action_space, gym.spaces.Discrete):
            invalid_action = env.action_space.n + 10
            assert not env.action_space.contains(invalid_action)

    def validate_termination(self, env):
        """Check episodes can terminate"""
        obs, _ = env.reset()
        for _ in range(1000):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                break
        assert terminated or truncated, \
            "Episode never terminated in 1000 steps!"

    def validate_reproducibility(self, env):
        """Check reset with seed is reproducible"""
        obs1, _ = env.reset(seed=42)
        obs2, _ = env.reset(seed=42)
        assert np.allclose(obs1, obs2), "Reset not reproducible!"

    def validate_random_agent(self, env):
        """Check environment works with random actions"""
        obs, _ = env.reset()
        total_reward = 0
        for _ in range(100):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            if terminated or truncated:
                break
        assert total_reward is not None, "No reward computed!"

# Usage
validator = EnvironmentValidator()
validator.validate_all(env)
```

### Manual Testing

Before training, play with the environment manually:

```python
# Manual environment exploration
env = GridWorldEnv()
obs, _ = env.reset()

while True:
    action = int(input("Action (0=up, 1=right, 2=down, 3=left): "))
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Position: {obs}, Reward: {reward}, Done: {terminated}")

    if terminated or truncated:
        obs, _ = env.reset()
        print("Episode reset")
```

---

## Part 8: Red Flags and Anti-Patterns

### Red Flag 1: Reward Scale Issue

```python
# RED FLAG: Rewards in [0, 1000000]
reward = distance_to_goal * 1000000  # HUGE!

# Solution: Scale to [-1, 1]
reward = -distance_to_goal / max_distance
assert -1 <= reward <= 1
```

### Red Flag 2: Observation Type Mismatch

```python
# RED FLAG: Observation dtype doesn't match space
observation_space = Box(0, 255, (84, 84, 3), dtype=np.uint8)
obs = np.random.random((84, 84, 3)).astype(np.float32)  # MISMATCH!

# Solution: Match dtype exactly
obs = (obs * 255).astype(np.uint8)
```

### Red Flag 3: Missing Done Flag

```python
# RED FLAG: Episodes never end
def step(self, action):
    return obs, reward, False, False, {}  # Always False!

# Solution: Implement termination logic
terminated = self.check_goal_reached() or self.check_failure()
```

### Red Flag 4: Action Bounds Not Enforced

```python
# RED FLAG: Network outputs unconstrained
def step(self, action):  # action could be [1000, -1000]
    velocity = action  # HUGE velocity!

# Solution: Clip or validate
action = np.clip(action,
                 self.action_space.low,
                 self.action_space.high)
```

### Red Flag 5: Vectorized Environment Auto-Reset Confusion

```python
# RED FLAG: Treating auto-reset obs as terminal obs
obs, rewards, terminateds, truncateds, info = envs.step(actions)
# obs contains NEW reset observations, not final observations!

# Solution: Use info['final_observation']
final_obs = info['final_observation']
```

### Red Flag 6: Non-Parallel-Safe Shared State

```python
# RED FLAG: Shared state breaks AsyncVectorEnv
class Env(gym.Env):
    global_counter = 0  # SHARED!

    def step(self, action):
        Env.global_counter += 1  # Race condition!

# Solution: Instance variables only
def __init__(self):
    self.counter = 0  # Instance-specific
```

### Red Flag 7: Info Dict with Unpicklable Objects

```python
# RED FLAG: Can't serialize for replay buffer
info = {
    'env': self,
    'callback': self.fn,
}

# Solution: Only basic types
info = {
    'level': 5,
    'score': 100,
}
```

### Red Flag 8: Forgetting to Close AsyncVectorEnv

```python
# RED FLAG: Process leak
envs = AsyncVectorEnv([...])
# ... forgot env.close()

# Solution: Always close
envs.close()  # or use try/finally
```

---

## Part 9: Rationalization Resistance

**Common Wrong Beliefs About Environments:**

**Claim 1**: "My custom environment should just work without testing"

- **Reality**: 80% of RL failures are environment bugs. Test before training.
- **Evidence**: Standard validation checklist catches bugs 95% of the time

**Claim 2**: "Reward scaling doesn't matter, only matters for learning rate"

- **Reality**: Reward scale affects gradient magnitudes directly. Too large = instability.
- **Evidence**: Scaling reward by 100x often breaks training even with correct learning rate

**Claim 3**: "Wrappers are optional complexity I don't need"

- **Reality**: Wrappers enforce separation of concerns. Without them, environments become unmaintainable.
- **Evidence**: Real RL code uses 3-5 wrappers (TimeLimit, Normalize, ClipAction, etc)

**Claim 4**: "Vectorized environments are always faster"

- **Reality**: Parallelization overhead for small envs can make them slower.
- **Evidence**: For < 4 envs, DummyVectorEnv is faster than AsyncVectorEnv

**Claim 5**: "My environment is correct if the agent learns something"

- **Reality**: Agent can learn to game a broken reward signal.
- **Evidence**: Agent learning ≠ environment correctness. Run tests.

**Claim 6**: "AsyncVectorEnv doesn't need explicit close()"

- **Reality**: Processes leak if not closed, draining system resources.
- **Evidence**: Unmanaged AsyncVectorEnv with 16+ processes brings systems to halt

**Claim 7**: "Observation normalization breaks training"

- **Reality**: Unnormalized large observations (like [0, 255]) break training.
- **Evidence**: Normalizing [0, 255] images to [0, 1] is standard practice

**Claim 8**: "I don't need to validate action space enforcement"

- **Reality**: Network outputs can violate bounds, causing physics errors.
- **Evidence**: Unclipped continuous actions often cause simulation failures

---

## Part 10: Pressure Test Scenarios

### Scenario 1: Custom Environment Debugging

```python
# Subagent challenge WITHOUT skill:
# "I built a custom CartPole variant. Training fails silently
# (agent doesn't learn). The environment seems fine when I test it.
# Where do I start debugging?"

# Expected WITH skill:
# 1. Validate observation space matches actual observations
# 2. Validate action space bounds are enforced
# 3. Check reward scale is in [-1, 1]
# 4. Verify reset/step API is correct (Gym vs Gymnasium)
# 5. Run environment validator checklist
# 6. Manual play-test to check physics
# 7. Verify terminal state logic
```

### Scenario 2: Wrapper Composition

```python
# Challenge: Build a correct wrapper stack
# env = gym.make("CartPole-v1")
# env = TimeLimit(env, 500)  # Add time limit
# env = NormalizeObservation(env)  # Normalize
# Should be safe to use with any policy training

# WITHOUT skill: Guess order, wrong wrapping
# WITH skill: Know correct order, understand composition
```

### Scenario 3: Vectorization Decision

```python
# Challenge: "I need to train on 32 parallel CartPoles.
# Which vectorized environment type is best?"

# WITHOUT skill: Try all three, pick whichever runs
# WITH skill: Analyze trade-offs
#   - 32 envs -> AsyncVectorEnv
#   - Memory acceptable? -> Yes
#   - Debugging needed? -> No -> Use Async
```

### Scenario 4: Space Mismatch Detection

```python
# Challenge: Environment crashes during training with cryptic error.
# Observation is (84, 84, 3) uint8 but CNN expects float32 in [0, 1]

# WITHOUT skill: Spend hours debugging network
# WITH skill: Immediately suspect observation/space mismatch
# Run validator, find dtype mismatch, fix preprocessing
```

---

## Part 11: Advanced Patterns - Multi-Agent Environments

### Multi-Agent Observation Spaces

**Scenario: Multi-agent game with individual agent observations**

```python
class MultiAgentGridWorld(gym.Env):
    """2-agent cooperative environment"""

    def __init__(self, num_agents=2):
        self.num_agents = num_agents

        # Each agent has its own action space
        self.action_space = gym.spaces.MultiDiscrete([4] * num_agents)

        # Each agent observes its own position + other agents' positions
        # Dict space allows per-agent observations
        self.observation_space = gym.spaces.Dict({
            f'agent_{i}': gym.spaces.Box(0, 4, (2 * num_agents,), dtype=np.int32)
            for i in range(num_agents)
        })

        self.agents = [np.array([i, 0], dtype=np.int32) for i in range(num_agents)]
        self.goal = np.array([4, 4], dtype=np.int32)

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.agents = [np.array([i, 0], dtype=np.int32) for i in range(self.num_agents)]

        obs = {}
        for i in range(self.num_agents):
            agent_obs = np.concatenate([agent.copy() for agent in self.agents])
            obs[f'agent_{i}'] = agent_obs.astype(np.int32)

        return obs, {}

    def step(self, actions):
        """actions is array of length num_agents"""
        moves = [
            np.array([0, 1], dtype=np.int32),
            np.array([1, 0], dtype=np.int32),
            np.array([0, -1], dtype=np.int32),
            np.array([-1, 0], dtype=np.int32),
        ]

        # Apply each agent's action
        for i, action in enumerate(actions):
            self.agents[i] += moves[action]
            self.agents[i] = np.clip(self.agents[i], 0, 4)

        # Shared reward: both agents get reward for reaching goal
        distances = [np.linalg.norm(agent - self.goal) for agent in self.agents]
        reward = sum(1.0 / (1.0 + d) for d in distances)

        # Both must reach goal
        terminated = all(np.array_equal(agent, self.goal) for agent in self.agents)

        # Construct observation for each agent
        obs = {}
        for i in range(self.num_agents):
            agent_obs = np.concatenate([agent.copy() for agent in self.agents])
            obs[f'agent_{i}'] = agent_obs.astype(np.int32)

        truncated = False
        return obs, reward, terminated, truncated, {}
```

### Key Multi-Agent Patterns

```python
# Pattern 1: Separate rewards per agent
rewards = {
    f'agent_{i}': compute_reward_for_agent(i)
    for i in range(num_agents)
}

# Pattern 2: Shared team reward
team_reward = sum(individual_rewards) / num_agents

# Pattern 3: Mixed observations (shared + individual)
obs = {
    f'agent_{i}': {
        'own_state': agent_states[i],
        'other_positions': [s for j, s in enumerate(agent_states) if j != i],
        'global_state': shared_state,
    }
    for i in range(num_agents)
}

# Pattern 4: Synchronized reset for coordinated behavior
def reset(self, seed=None):
    super().reset(seed=seed)
    # All agents reset to coordinated starting positions
    self.agents = initialize_team_formation()
```

---

## Part 12: Integration with Training Loops

### Proper Environment Integration

```python
class TrainingLoop:
    """Shows correct environment integration pattern"""

    def __init__(self, env, num_parallel=4):
        self.env = self._setup_environment(env, num_parallel)
        self.policy = build_policy()

    def _setup_environment(self, env, num_parallel):
        """Proper environment setup"""
        if num_parallel == 1:
            env = gym.make(env)
        elif num_parallel <= 4:
            env = DummyVectorEnv([lambda: gym.make(env) for _ in range(num_parallel)])
        else:
            env = SyncVectorEnv([lambda: gym.make(env) for _ in range(num_parallel)])

        # Add standard wrappers
        env = gym.wrappers.TimeLimit(env, max_episode_steps=1000)
        env = NormalizeObservation(env)

        return env

    def train_one_episode(self):
        """Correct training loop"""
        obs, info = self.env.reset()

        total_reward = 0
        steps = 0

        while True:
            # Get action from policy
            action = self.policy.get_action(obs)

            # CRITICAL: Validate action is in space
            assert self.env.action_space.contains(action)

            # Step environment
            obs, reward, terminated, truncated, info = self.env.step(action)

            # CRITICAL: Handle auto-reset in vectorized case
            if 'final_observation' in info:
                final_obs = info['final_observation']
                # Store final obs in replay buffer, not reset obs
            else:
                final_obs = obs

            # Store experience
            self.store_experience(obs, reward, terminated, truncated, info)

            total_reward += np.mean(reward) if isinstance(reward, np.ndarray) else reward
            steps += 1

            # Check termination
            if np.any(terminated) or np.any(truncated):
                break

        return total_reward / steps

    def store_experience(self, obs, reward, terminated, truncated, info):
        """Correct experience storage"""
        # Handle vectorized case (obs, reward are arrays)
        if isinstance(reward, np.ndarray):
            for i in range(len(reward)):
                self.replay_buffer.add(
                    obs=obs[i] if isinstance(obs, np.ndarray) else obs,
                    action=None,  # Set before storing
                    reward=reward[i],
                    done=terminated[i] or truncated[i],
                    next_obs=obs[i] if isinstance(obs, np.ndarray) else obs,
                )
```

### Common Integration Mistakes

**Mistake 1: Not closing AsyncVectorEnv**

```python
# WRONG: Process leak
envs = AsyncVectorEnv([...] for _ in range(16))
for episode in range(1000):
    obs, _ = envs.reset()
    # ... training ...
# Processes never cleaned up

# CORRECT: Always cleanup
try:
    envs = AsyncVectorEnv([...] for _ in range(16))
    for episode in range(1000):
        obs, _ = envs.reset()
        # ... training ...
finally:
    envs.close()
```

**Mistake 2: Using wrong observation after auto-reset**

```python
# WRONG: Mixing terminal and reset observations
obs, reward, terminated, truncated, info = envs.step(actions)
# obs is reset observation, but we treat it as terminal!
store_in_replay_buffer(obs, reward, terminated)

# CORRECT: Use final_observation for training
final_obs = info.get('final_observation', obs)
if np.any(terminated):
    store_in_replay_buffer(final_obs, reward, terminated)
else:
    next_obs = obs
```

**Mistake 3: Not validating agent actions**

```python
# WRONG: Trust agent always outputs valid action
action = policy(obs)
obs, reward, terminated, truncated, info = env.step(action)

# CORRECT: Validate before stepping
action = policy(obs)
action = np.clip(action, env.action_space.low, env.action_space.high)
assert env.action_space.contains(action)
obs, reward, terminated, truncated, info = env.step(action)
```

---

## Part 13: Performance Optimization

### Observation Preprocessing Performance

```python
class OptimizedObservationPreprocessing:
    """Efficient observation handling"""

    def __init__(self, env):
        self.env = env

    def preprocess_observation(self, obs):
        """Optimized preprocessing"""
        # Avoid unnecessary copies
        if obs.dtype == np.uint8:
            # In-place division for efficiency
            obs = obs.astype(np.float32) / 255.0
        else:
            obs = obs / 255.0

        # Use memmap for large observations
        if obs.nbytes > 1_000_000:  # > 1MB
            # Consider using memory-mapped arrays
            pass

        return obs

    def batch_preprocess(self, obs_batch):
        """Batch processing for vectorized envs"""
        # Vectorized preprocessing is faster than per-obs
        if isinstance(obs_batch, np.ndarray) and obs_batch.ndim == 4:
            # (batch_size, H, W, C) image batch
            obs_batch = obs_batch.astype(np.float32) / 255.0
        return obs_batch
```

### Vectorization Performance Tips

```python
# Benchmark: When does parallelization help?

# For CartPole (fast env):
# - 1 env: 10k steps/sec on 1 core
# - 4 Dummy: 9k steps/sec (overhead)
# - 4 Sync: 15k steps/sec (parallelism helps)
# - 4 Async: 12k steps/sec (context switch overhead)

# For Atari (slow env):
# - 1 env: 0.5k steps/sec on 1 core
# - 16 Dummy: 7k steps/sec (overhead worth it)
# - 16 Sync: 15k steps/sec (GIL limits)
# - 16 Async: 25k steps/sec (parallelism dominates)

# Rule of thumb:
# - env_step_time < 1ms: parallelization overhead dominates, use Dummy
# - env_step_time 1-10ms: parallelization helps, use Sync
# - env_step_time > 10ms: parallelization essential, use Async
```

---

## Part 14: Debugging Environment Issues Systematically

### Diagnostic Checklist for Broken Training

```python
class EnvironmentDebugger:
    """Systematic environment debugging"""

    def full_diagnosis(self, env, policy):
        """Complete environment diagnostic"""
        print("=== Environment Diagnostic ===")

        # 1. Check environment API
        self.check_api(env)
        print("✓ API correct")

        # 2. Check spaces
        self.check_spaces(env)
        print("✓ Spaces valid")

        # 3. Check reset/step mechanics
        self.check_mechanics(env)
        print("✓ Reset/step mechanics correct")

        # 4. Check observation statistics
        obs_stats = self.analyze_observations(env)
        print(f"✓ Observations: mean={obs_stats['mean']:.3f}, std={obs_stats['std']:.3f}")

        # 5. Check reward statistics
        reward_stats = self.analyze_rewards(env)
        print(f"✓ Rewards: mean={reward_stats['mean']:.3f}, std={reward_stats['std']:.3f}")
        if abs(reward_stats['mean']) > 1 or reward_stats['std'] > 1:
            print("  WARNING: Reward scale may be too large")

        # 6. Check episode lengths
        lengths = self.analyze_episode_lengths(env)
        print(f"✓ Episode lengths: mean={lengths['mean']:.1f}, min={lengths['min']}, max={lengths['max']}")

        # 7. Check reproducibility
        self.check_reproducibility(env)
        print("✓ Reproducibility verified")

        # 8. Check with policy
        self.check_policy_integration(env, policy)
        print("✓ Policy integration works")

    def analyze_observations(self, env, num_episodes=10):
        """Analyze observation distribution"""
        obs_list = []
        for _ in range(num_episodes):
            obs, _ = env.reset()
            for _ in range(100):
                action = env.action_space.sample()
                obs, _, terminated, truncated, _ = env.step(action)
                obs_list.append(obs.flatten())
                if terminated or truncated:
                    break

        obs_array = np.concatenate(obs_list)
        return {
            'mean': np.mean(obs_array),
            'std': np.std(obs_array),
            'min': np.min(obs_array),
            'max': np.max(obs_array),
        }

    def analyze_rewards(self, env, num_episodes=10):
        """Analyze reward distribution"""
        rewards = []
        for _ in range(num_episodes):
            obs, _ = env.reset()
            for _ in range(100):
                action = env.action_space.sample()
                obs, reward, terminated, truncated, _ = env.step(action)
                rewards.append(reward)
                if terminated or truncated:
                    break

        rewards = np.array(rewards)
        return {
            'mean': np.mean(rewards),
            'std': np.std(rewards),
            'min': np.min(rewards),
            'max': np.max(rewards),
        }

    def analyze_episode_lengths(self, env, num_episodes=20):
        """Analyze episode length distribution"""
        lengths = []
        for _ in range(num_episodes):
            obs, _ = env.reset()
            steps = 0
            for step in range(10000):  # Max steps
                action = env.action_space.sample()
                obs, reward, terminated, truncated, _ = env.step(action)
                steps += 1
                if terminated or truncated:
                    break
            lengths.append(steps)

        lengths = np.array(lengths)
        return {
            'mean': np.mean(lengths),
            'min': int(np.min(lengths)),
            'max': int(np.max(lengths)),
            'median': int(np.median(lengths)),
        }
```

---

## Summary: When to Invoke This Skill

**Use rl-environments skill when:**

1. Creating custom environments from scratch
2. Debugging environment-related training failures
3. Implementing observation/action spaces
4. Using or creating wrappers
5. Parallelizing environments
6. Testing environments before training
7. Handling Gym vs Gymnasium differences
8. Migrating environment code between versions
9. Building multi-agent or multi-component environments
10. Enforcing action/observation bounds correctly
11. Optimizing environment performance
12. Debugging training failures systematically

**This skill prevents:**

- 80% of RL bugs (environment issues)
- Silent training failures from broken environments
- Vectorization-related data corruption
- Observation/action space mismatches
- Reward scaling instabilities
- Terminal state logic errors
- Reproducibility issues from poor seeding
- Performance degradation from inefficient environments
- Multi-agent coordination failures
- Integration issues with training loops
