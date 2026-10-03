---
name: self-forcing-video
title: "Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2506.08009"
keywords: [video generation, exposure bias, autoregressive diffusion, training efficiency]
description: "Address exposure bias in video generation by training on self-generated sequences, achieving 17 FPS real-time performance while matching quality of slower baselines."
---

# Self Forcing: Bridging Train-Test Gap in Video Diffusion

## Core Concept

Autoregressive video models face an exposure bias problem: they train on ground-truth frames but generate from their own imperfect outputs at test time. Self Forcing bridges this gap by performing autoregressive rollout during training, conditioning each frame on previously self-generated outputs. This holistic video-level distribution matching eliminates frame-wise objective mismatch.

## Architecture Overview

- **Autoregressive rollout training**: Each frame conditioned on self-generated prior frames
- **Few-step diffusion**: 4-step diffusion models enable practical training speed
- **Rolling KV cache**: O(TL) complexity vs O(L²+TL) for full attention caching
- **Distribution matching loss**: Applies DMD, SiD, or GAN objectives to complete sequences
- **Real-time inference**: 17 FPS with sub-second latency on single H100

## Implementation

### Step 1: Design Few-Step Diffusion Model

Create efficient diffusion variant for video frames:

```python
class FewStepVideoDiffusion(torch.nn.Module):
    def __init__(self, num_steps: int = 4,
                 frame_shape: tuple = (64, 64, 3)):
        super().__init__()
        self.num_steps = num_steps
        self.frame_shape = frame_shape

        # Denoiser network
        self.denoiser = UNet3D(
            in_channels=3,
            out_channels=3,
            time_embedding_dim=128
        )

        # Timestep embedding
        self.time_embedder = torch.nn.Sequential(
            torch.nn.Linear(1, 128),
            torch.nn.SiLU(),
            torch.nn.Linear(128, 128)
        )

    def forward(self, x_noisy: torch.Tensor,
               t: int,
               context: torch.Tensor = None) -> torch.Tensor:
        """Predict clean frame from noisy input."""

        # Embed timestep
        t_emb = self.time_embedder(
            torch.tensor([[t / self.num_steps]],
                         dtype=torch.float32)
        )

        # Denoise with context conditioning
        if context is not None:
            x_noisy = torch.cat([x_noisy, context], dim=1)

        pred = self.denoiser(x_noisy, t_emb)

        return pred

    def reverse_diffusion_step(self, x_t: torch.Tensor,
                              t: int,
                              context: torch.Tensor = None
                              ) -> torch.Tensor:
        """Single reverse diffusion step."""

        # Predict noise
        noise_pred = self.forward(x_t, t, context)

        # Reverse step
        alpha = self._get_alpha(t)
        x_prev = (x_t - (1 - alpha) * noise_pred) / torch.sqrt(alpha)

        return x_prev

    def _get_alpha(self, t: int) -> float:
        """Get variance schedule value."""
        return 1.0 - (t / self.num_steps)
```

### Step 2: Implement Self Forcing Training Loop

Train with autoregressive rollout and gradient truncation:

```python
class SelfForcingTrainer:
    def __init__(self, diffusion_model: FewStepVideoDiffusion,
                 batch_size: int = 16):
        self.model = diffusion_model
        self.batch_size = batch_size
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=1e-4
        )

    def prepare_video_batch(self, video_frames: torch.Tensor
                           ) -> torch.Tensor:
        """Prepare video for training (add noise)."""
        # Add Gaussian noise to frames
        noise = torch.randn_like(video_frames)
        noisy_frames = torch.sqrt(torch.tensor(0.9)) * video_frames + (
            torch.sqrt(torch.tensor(0.1)) * noise
        )
        return noisy_frames

    def self_forcing_rollout(self,
                            initial_frame: torch.Tensor,
                            num_frames: int,
                            attention_window: int = 256
                            ) -> list:
        """Rollout sequence with self-generated frames."""

        frames = [initial_frame]

        for frame_idx in range(1, num_frames):
            # Get context from recent frames (limited window)
            context_start = max(0, frame_idx - attention_window)
            context_frames = torch.cat(
                frames[context_start:frame_idx],
                dim=0
            )

            # Generate next frame through diffusion steps
            current_frame = initial_frame  # Start from noise

            for step in reversed(range(self.model.num_steps)):
                current_frame = (
                    self.model.reverse_diffusion_step(
                        current_frame,
                        step,
                        context=context_frames
                    )
                )

            frames.append(current_frame)

        return frames

    def compute_distribution_matching_loss(self,
                                          generated_frames: list,
                                          loss_type: str = "dmd"
                                          ) -> torch.Tensor:
        """Compute loss on full generated sequence."""

        # Stack all generated frames
        generated = torch.stack(generated_frames, dim=0)

        if loss_type == "dmd":
            # Distribution Matching Diffusion loss
            loss = self._dmd_loss(generated)
        elif loss_type == "sid":
            # Score-based Implicit Divergence
            loss = self._sid_loss(generated)
        else:  # GAN loss
            loss = self._gan_loss(generated)

        return loss

    def _dmd_loss(self, generated: torch.Tensor) -> torch.Tensor:
        """Distribution Matching Diffusion loss."""
        # Compare real and generated distributions
        # Using optimal transport or other divergence measure
        batch_mean = generated.mean(dim=0)
        batch_std = generated.std(dim=0)

        loss = (batch_mean ** 2).mean() + (batch_std - 1.0) ** 2

        return loss

    def train_step(self, video_batch: torch.Tensor,
                  truncation_steps: int = 2) -> float:
        """Single training step with gradient truncation."""

        # Prepare noisy frames
        noisy_batch = self.prepare_video_batch(video_batch)

        # Self forcing rollout
        generated = []
        for video in noisy_batch:
            frames = self.self_forcing_rollout(
                video[0],  # Initial frame
                num_frames=video.shape[0]
            )
            generated.append(torch.stack(frames))

        generated = torch.stack(generated)

        # Truncate gradients to limit memory
        if truncation_steps > 0:
            generated = generated.detach()
            generated.requires_grad = True

        # Compute loss on full sequences
        loss = self.compute_distribution_matching_loss(generated)

        # Update
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            self.model.parameters(),
            max_norm=1.0
        )
        self.optimizer.step()

        return loss.item()
```

### Step 3: Implement Rolling KV Cache

Efficient attention caching for long sequences:

```python
class RollingKVCache:
    def __init__(self, max_cache_tokens: int = 4096,
                 hidden_dim: int = 768):
        self.max_cache = max_cache_tokens
        self.hidden_dim = hidden_dim
        self.cache = {
            "keys": torch.zeros(max_cache_tokens, hidden_dim),
            "values": torch.zeros(max_cache_tokens, hidden_dim)
        }
        self.pos = 0

    def append(self, keys: torch.Tensor,
              values: torch.Tensor):
        """Add new KV pairs, rolling out old ones."""

        new_len = keys.shape[0]

        if self.pos + new_len > self.max_cache:
            # Shift old entries out
            shift_amount = (self.pos + new_len) - self.max_cache
            self.cache["keys"] = torch.roll(
                self.cache["keys"],
                shifts=-shift_amount,
                dims=0
            )
            self.cache["values"] = torch.roll(
                self.cache["values"],
                shifts=-shift_amount,
                dims=0
            )
            self.pos = self.max_cache - new_len

        # Insert new entries
        self.cache["keys"][self.pos:self.pos + new_len] = keys
        self.cache["values"][self.pos:self.pos + new_len] = values
        self.pos += new_len

    def get(self) -> tuple:
        """Retrieve current cache."""
        return (self.cache["keys"][:self.pos],
                self.cache["values"][:self.pos])
```

### Step 4: Real-Time Inference

Generate video streams at 17 FPS:

```python
def generate_video_realtime(model: FewStepVideoDiffusion,
                           prompt: str,
                           output_fps: int = 24,
                           duration_seconds: float = 10.0
                           ) -> None:
    """Stream video generation in real-time."""

    total_frames = int(output_fps * duration_seconds)
    kv_cache = RollingKVCache()

    # Generate initial frame from prompt
    initial_frame = model.generate_from_text(prompt)

    frame_buffer = [initial_frame]
    start_time = time.time()

    for frame_idx in range(1, total_frames):
        # Get context from KV cache
        cached_keys, cached_values = kv_cache.get()

        # Generate next frame with cached context
        next_frame = model.reverse_diffusion_step(
            torch.randn(1, 3, 64, 64),
            t=0,
            context=cached_keys
        )

        # Update cache
        kv_cache.append(
            next_frame.detach(),
            next_frame.detach()
        )

        frame_buffer.append(next_frame)

        # Monitor real-time performance
        elapsed = time.time() - start_time
        expected_time = (frame_idx + 1) / output_fps

        if frame_idx % 10 == 0:
            fps = frame_idx / elapsed
            print(f"Frame {frame_idx}: {fps:.1f} FPS")

    # Save video
    save_video(frame_buffer, "output.mp4", fps=output_fps)
```

## Practical Guidance

**Few-Step Diffusion**: 4 steps balances quality and speed. Fewer steps reduce memory but hurt quality; more steps increase latency.

**Gradient Truncation**: Critical for memory efficiency in autoregressive training. Truncate after 2-3 steps to limit stored computations.

**Attention Windows**: Restrict attention during training to prevent distribution mismatch in long generation. Use 256-512 token windows.

**Real-Time Performance**: Rolling KV cache achieves O(TL) instead of O(L²+TL) by avoiding redundant recomputation. Enables single H100 streaming at 24fps.

**When to Apply**: Use Self Forcing for interactive video generation where inference speed matters, or when training video diffusion models with limited memory budgets.

## Reference

Self Forcing eliminates exposure bias by matching model behavior during training and inference. The key innovation is performing autoregressive rollout during training with distribution-matching losses over complete sequences, rather than frame-wise objectives. Combined with rolling KV cache, this enables efficient training and real-time inference.
