---
name: srpo-vla-policy
title: "SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2511.15605"
keywords: [Embodied AI, Vision-Language-Action Models, Policy Optimization, Reward Sparsity, Self-Supervision]
description: "Train VLA models for robotic manipulation by using the model's own successful trajectories as self-reference for reward—enable progress-based feedback for failed attempts without external rewards or demonstrations."
---

# Train VLA Models with Self-Referential Rewards for Robotic Manipulation

Vision-Language-Action (VLA) models for robotics face extreme reward sparsity: tasks succeed or fail, with little feedback for in-between attempts. SRPO (Self-Referential Policy Optimization) breaks this bottleneck by using the model's own successful trajectories as self-reference. Failed attempts are measured against the model's successful ones from the same training batch, enabling dense progress-based rewards without external reward models or demonstrations.

This achieves 99.2% success on LIBERO (103% relative improvement from supervised baseline) by leveraging the model's latent world representation to assess behavioral progress robustly.

## Core Concept

Standard VLA training for manipulation suffers from:

1. **Reward Sparsity**: Most trajectories fail; binary success/failure provides no gradient signal for intermediate progress
2. **Sparse Demonstrations**: Expert trajectories are expensive; RL without them requires dense rewards
3. **Domain Shift**: Reward models trained on one set of tasks fail on new objects/scenes

SRPO addresses all three by enabling self-comparison: rather than comparing failed trajectories to fixed rewards or external demonstrations, the model compares its current attempt to its own successful trajectories (from the same batch). A latent world model captures progress via compressed state representations, enabling robust progress estimation without task-specific fine-tuning.

## Architecture Overview

- **Vision-Language-Action Model**: Encoder (vision + language) → action decoder; generates manipulation actions
- **Latent World Model**: Encodes trajectories into latent state representations capturing progress
- **Self-Referential Comparison**: Compare failed trajectory's latent progression to successful trajectories' latent states
- **Progress-Based Rewards**: Measure behavioral advancement using latent space distances, not task-specific metrics
- **Batch-Based Training**: Successful and failed trajectories in same batch enable direct comparison

## Implementation Steps

**Step 1: World Model for State Representation.** Encode trajectories into latent progress space.

```python
import torch
import torch.nn as nn

class LatentWorldModel(nn.Module):
    """
    Encodes manipulation trajectories into latent state representations.
    Captures progress toward goals without task-specific knowledge.
    """
    def __init__(self, observation_dim=512, action_dim=7, latent_dim=128):
        super().__init__()

        # Encoder: vision + action → latent state
        self.encoder = nn.Sequential(
            nn.Linear(observation_dim + action_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)
        )

        # Predictor: predict next latent state from current + action
        self.predictor = nn.Sequential(
            nn.Linear(latent_dim + action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)
        )

        self.latent_dim = latent_dim

    def encode_trajectory(self, observations, actions):
        """
        Encode trajectory into sequence of latent states.
        observations: (traj_len, obs_dim)
        actions: (traj_len, action_dim)
        """
        latent_states = []

        for t in range(len(observations)):
            obs_action = torch.cat([observations[t], actions[t]], dim=0)
            latent = self.encoder(obs_action)
            latent_states.append(latent)

        return torch.stack(latent_states)  # (traj_len, latent_dim)

    def predict_next_state(self, latent_state, action):
        """Predict next latent state (for training/debugging)."""
        input_combined = torch.cat([latent_state, action], dim=-1)
        next_latent = self.predictor(input_combined)
        return next_latent

    def compute_progress(self, failed_latent_traj, success_latent_traj):
        """
        Measure progress of failed trajectory toward success.
        Compares each step of failed trajectory to success trajectory.
        """
        # Align trajectories (handle length mismatch)
        min_len = min(len(failed_latent_traj), len(success_latent_traj))

        distances = []
        for t in range(min_len):
            # L2 distance in latent space
            dist = torch.norm(
                failed_latent_traj[t] - success_latent_traj[t],
                p=2
            )
            distances.append(dist)

        # Average distance to success trajectory
        avg_distance = torch.stack(distances).mean()

        # Progress reward: negative distance (closer = better)
        progress = -avg_distance
        return progress
```

**Step 2: Implement Self-Referential Comparison.**

```python
class SelfReferentialComparison:
    """
    Compare failed trajectories to successful ones in the batch.
    """
    def __init__(self, world_model):
        self.world_model = world_model

    def compute_self_referential_reward(self, failed_traj, success_trajs):
        """
        Compute reward for failed trajectory based on self-comparison.
        failed_traj: dict with 'observations' and 'actions'
        success_trajs: list of successful trajectory dicts
        """
        # Encode failed trajectory
        failed_latent = self.world_model.encode_trajectory(
            failed_traj['observations'],
            failed_traj['actions']
        )

        # Encode successful trajectories
        success_latents = []
        for traj in success_trajs:
            latent = self.world_model.encode_trajectory(
                traj['observations'],
                traj['actions']
            )
            success_latents.append(latent)

        # Compare to each successful trajectory
        progress_scores = []
        for success_latent in success_latents:
            progress = self.world_model.compute_progress(failed_latent, success_latent)
            progress_scores.append(progress)

        # Average progress across all successful trajectories
        avg_progress = torch.stack(progress_scores).mean()

        return avg_progress.item()

    def compute_batch_rewards(self, trajectories):
        """
        Process batch of trajectories, extracting successful and failed.
        Compute self-referential rewards for each failed trajectory.
        """
        successful = [t for t in trajectories if t['success']]
        failed = [t for t in trajectories if not t['success']]

        rewards = {}

        for i, traj in enumerate(trajectories):
            if traj['success']:
                # Successful trajectories get positive baseline reward
                rewards[i] = 1.0
            else:
                # Failed trajectories get self-referential progress reward
                if successful:
                    progress_reward = self.compute_self_referential_reward(
                        traj,
                        successful
                    )
                    rewards[i] = progress_reward  # Typically in [-1, 0] range
                else:
                    # No successful trajectories in batch; use zero reward
                    rewards[i] = 0.0

        return rewards
```

**Step 3: VLA Model with SRPO Training.**

```python
class VisionLanguageActionModel(nn.Module):
    """
    VLA model for manipulation: encodes vision + language → actions.
    """
    def __init__(self, vision_encoder_dim=512, language_encoder_dim=256, action_dim=7):
        super().__init__()

        # Vision encoder (e.g., ViT or CNN)
        self.vision_encoder = load_vision_encoder()

        # Language encoder (e.g., BERT)
        self.language_encoder = load_language_encoder()

        # Action decoder
        self.action_decoder = nn.Sequential(
            nn.Linear(vision_encoder_dim + language_encoder_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim)
        )

    def forward(self, observations, language_input):
        """
        observations: (batch, seq_len, 3, H, W) or (batch, obs_features)
        language_input: (batch, seq_len) tokenized language
        Returns: actions (batch, seq_len, action_dim)
        """
        # Encode observations
        if len(observations.shape) == 5:  # Image observations
            batch, seq_len, _, _, _ = observations.shape
            obs_flat = observations.reshape(batch * seq_len, 3, -1, -1)
            vision_features = self.vision_encoder(obs_flat)
            vision_features = vision_features.reshape(batch, seq_len, -1)
        else:
            vision_features = self.vision_encoder(observations)

        # Encode language
        lang_features = self.language_encoder(language_input)  # (batch, lang_dim)
        lang_features = lang_features.unsqueeze(1).expand_as(vision_features[:, :, :lang_features.shape[-1]])

        # Combine and decode actions
        combined = torch.cat([vision_features, lang_features], dim=-1)
        actions = self.action_decoder(combined)

        return actions
```

**Step 4: SRPO Training Loop.**

```python
def train_vla_with_srpo(
    vla_model, world_model, environment, num_episodes=10000,
    vla_lr=1e-4, world_model_lr=1e-4
):
    """
    Train VLA model with self-referential policy optimization.
    """
    vla_optimizer = torch.optim.AdamW(vla_model.parameters(), lr=vla_lr)
    world_optimizer = torch.optim.AdamW(world_model.parameters(), lr=world_model_lr)
    comparator = SelfReferentialComparison(world_model)

    for episode in range(num_episodes):
        # Collect batch of trajectories
        batch_trajs = []

        for rollout in range(8):  # 8 rollouts per batch
            obs_list = []
            action_list = []
            reward = None

            # Reset environment and get initial observation
            obs, lang = environment.reset()

            trajectory_success = False

            # Rollout episode
            for step in range(100):
                obs_list.append(obs)

                # VLA generates action
                with torch.no_grad():
                    obs_tensor = torch.tensor(obs).unsqueeze(0)
                    lang_tensor = torch.tensor(lang).unsqueeze(0)
                    action = vla_model(obs_tensor, lang_tensor)[0].detach().numpy()

                # Environment step
                obs, done, task_success = environment.step(action)

                action_list.append(action)

                if task_success or done:
                    trajectory_success = task_success
                    break

            batch_trajs.append({
                'observations': obs_list,
                'actions': action_list,
                'success': trajectory_success
            })

        # ===== Compute SRPO Rewards =====
        rewards = comparator.compute_batch_rewards(batch_trajs)

        # ===== Update VLA Policy =====
        vla_loss = 0

        for i, traj in enumerate(batch_trajs):
            # Reconstruct actions from VLA
            obs_tensor = torch.tensor(traj['observations']).float()
            lang_tensor = torch.tensor([lang] * len(traj['observations'])).unsqueeze(1)

            with torch.enable_grad():
                vla_actions = vla_model(obs_tensor, lang_tensor)

            # Target actions (actual executed)
            target_actions = torch.tensor(traj['actions']).float()

            # MSE loss weighted by reward
            action_loss = torch.nn.functional.mse_loss(vla_actions, target_actions)
            weighted_loss = action_loss * rewards[i]  # Reward weighting

            vla_loss += weighted_loss

        avg_vla_loss = vla_loss / len(batch_trajs)

        vla_optimizer.zero_grad()
        avg_vla_loss.backward()
        torch.nn.utils.clip_grad_norm_(vla_model.parameters(), 1.0)
        vla_optimizer.step()

        # ===== Update World Model =====
        # Train world model to improve trajectory encoding
        world_loss = 0

        for traj in batch_trajs:
            obs_tensor = torch.tensor(traj['observations']).float()
            action_tensor = torch.tensor(traj['actions']).float()

            # Encode trajectory
            latents = world_model.encode_trajectory(obs_tensor, action_tensor)

            # Predict next states (reconstruction loss)
            for t in range(len(latents) - 1):
                pred_next = world_model.predict_next_state(latents[t], action_tensor[t])
                reconstruction_loss = torch.nn.functional.mse_loss(pred_next, latents[t + 1])
                world_loss += reconstruction_loss

        avg_world_loss = world_loss / max(len(batch_trajs), 1)

        world_optimizer.zero_grad()
        avg_world_loss.backward()
        torch.nn.utils.clip_grad_norm_(world_model.parameters(), 1.0)
        world_optimizer.step()

        if episode % 100 == 0:
            success_rate = sum(1 for t in batch_trajs if t['success']) / len(batch_trajs)
            print(f"Episode {episode}: success_rate={success_rate:.2%}, "
                  f"vla_loss={avg_vla_loss.item():.4f}, "
                  f"world_loss={avg_world_loss.item():.4f}")
```

## Practical Guidance

**When to Use:** Robotic manipulation tasks with sparse rewards (pick-and-place, assembly); scenarios with few expert demonstrations.

**Hyperparameters:**
- Latent dimension: 128–256 depending on task complexity
- Batch size: ≥ 8 to ensure successful trajectories in batch for comparison
- Progress normalization: scale latent distances to [0, 1] range for stable training

**Pitfalls:**
- **Successful trajectory requirements**: If all trajectories fail, no self-reference possible; initialize with BC or weak RL first
- **Latent space collapse**: World model may learn trivial encodings; use reconstruction losses to maintain expressiveness
- **Task-specific adaptation**: Model may overfit to initial task distribution; use diverse task set
- **Trajectory length mismatch**: Align trajectories by timestep or use dynamic time-warping

**When NOT to Use:** Tasks with very sparse successes (< 10% baseline); single-task learning where diversity is low.

**Integration**: Works with any VLA backbone (OpenVLA, RT-2, etc.); requires environment interface for data collection.

---
Reference: https://arxiv.org/abs/2511.15605
