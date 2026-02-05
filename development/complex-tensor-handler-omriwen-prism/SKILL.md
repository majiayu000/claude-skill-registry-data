---
name: complex-tensor-handler
description: Handle complex-valued tensors in PyTorch for astronomical imaging applications. This skill should be used when working with Fourier transforms, phase/amplitude representations, and complex arithmetic in PRISM.
---

# Complex Tensor Handler

Work with complex-valued tensors in PyTorch for astronomical imaging, including FFT operations, phase/amplitude conversions, and complex arithmetic.

## Purpose

PRISM deals with complex-valued images (phase + amplitude or real + imaginary). This skill provides patterns for correctly handling complex tensors in PyTorch.

## When to Use

Use this skill when:
- Working with FFT/IFFT operations
- Converting between phase/amplitude and real/imaginary
- Performing complex arithmetic
- Dealing with complex-valued neural networks

## Complex Tensor Basics

### Creating Complex Tensors

```python
import torch

# From real and imaginary parts
real = torch.randn(1, 1, 256, 256)
imag = torch.randn(1, 1, 256, 256)
complex_tensor = torch.complex(real, imag)
# or: complex_tensor = real + 1j * imag

# From magnitude and phase
magnitude = torch.rand(1, 1, 256, 256)
phase = torch.rand(1, 1, 256, 256) * 2 * np.pi
complex_tensor = magnitude * torch.exp(1j * phase)

# Convert real to complex
real_tensor = torch.randn(1, 1, 256, 256)
complex_tensor = real_tensor.to(torch.complex64)
```

### Accessing Components

```python
# Real and imaginary parts
real_part = complex_tensor.real
imag_part = complex_tensor.imag

# Magnitude and phase
magnitude = complex_tensor.abs()
phase = complex_tensor.angle()

# Conjugate
conjugate = complex_tensor.conj()
```

## Common Operations

### FFT and IFFT

```python
def fft(image: Tensor, norm: str = 'ortho') -> Tensor:
    """2D FFT of image tensor.

    Parameters
    ----------
    image : Tensor
        Spatial domain image [B, C, H, W], real or complex
    norm : str
        Normalization: 'ortho', 'forward', or 'backward'

    Returns
    -------
    Tensor
        Frequency domain, complex-valued [B, C, H, W]
    """
    # PyTorch FFT handles real input automatically
    freq = torch.fft.fft2(image, norm=norm)

    # Optionally shift zero-frequency to center
    freq = torch.fft.fftshift(freq, dim=(-2, -1))

    return freq

def ifft(freq: Tensor, norm: str = 'ortho') -> Tensor:
    """Inverse 2D FFT.

    Parameters
    ----------
    freq : Tensor
        Frequency domain [B, C, H, W], complex-valued
    norm : str
        Normalization mode

    Returns
    -------
    Tensor
        Spatial domain [B, C, H, W], complex-valued
    """
    # Unshift if needed
    freq = torch.fft.ifftshift(freq, dim=(-2, -1))

    # Inverse FFT
    image = torch.fft.ifft2(freq, norm=norm)

    return image
```

### Phase and Amplitude

```python
def to_phase_amplitude(complex_tensor: Tensor) -> tuple[Tensor, Tensor]:
    """Convert complex tensor to phase and amplitude.

    Parameters
    ----------
    complex_tensor : Tensor
        Complex-valued tensor [B, C, H, W]

    Returns
    -------
    phase : Tensor
        Phase in radians [-π, π], shape [B, C, H, W]
    amplitude : Tensor
        Amplitude (magnitude), shape [B, C, H, W]
    """
    phase = complex_tensor.angle()
    amplitude = complex_tensor.abs()
    return phase, amplitude

def from_phase_amplitude(phase: Tensor, amplitude: Tensor) -> Tensor:
    """Create complex tensor from phase and amplitude.

    Parameters
    ----------
    phase : Tensor
        Phase in radians, shape [B, C, H, W]
    amplitude : Tensor
        Amplitude, shape [B, C, H, W]

    Returns
    -------
    Tensor
        Complex-valued tensor [B, C, H, W]
    """
    return amplitude * torch.exp(1j * phase)
```

### Real and Imaginary

```python
def to_real_imag(complex_tensor: Tensor) -> tuple[Tensor, Tensor]:
    """Split complex tensor into real and imaginary parts.

    Parameters
    ----------
    complex_tensor : Tensor
        Complex-valued tensor [B, C, H, W]

    Returns
    -------
    real : Tensor
        Real part, shape [B, C, H, W]
    imag : Tensor
        Imaginary part, shape [B, C, H, W]
    """
    return complex_tensor.real, complex_tensor.imag

def from_real_imag(real: Tensor, imag: Tensor) -> Tensor:
    """Create complex tensor from real and imaginary parts.

    Parameters
    ----------
    real : Tensor
        Real part, shape [B, C, H, W]
    imag : Tensor
        Imaginary part, shape [B, C, H, W]

    Returns
    -------
    Tensor
        Complex-valued tensor [B, C, H, W]
    """
    return torch.complex(real, imag)
```

## PRISM-Specific Patterns

### Generate Complex Image

```python
class ComplexImageGenerator(nn.Module):
    """Generate complex-valued images (phase + amplitude)."""

    def __init__(self, latent_dim: int = 128, output_size: int = 256):
        super().__init__()
        self.decoder = build_decoder(latent_dim, output_channels=2)
        self.output_size = output_size

    def forward(self, latent: Optional[Tensor] = None) -> Tensor:
        """Generate complex image.

        Returns
        -------
        Tensor
            Complex-valued image [1, 1, H, W]
        """
        if latent is None:
            latent = self.latent.expand(1, -1, 1, 1)

        # Generate phase and amplitude as separate channels
        output = self.decoder(latent)  # [1, 2, H, W]

        # Split into phase and amplitude
        phase = output[:, 0:1]  # [1, 1, H, W]
        amplitude = output[:, 1:2].exp()  # [1, 1, H, W], always positive

        # Create complex tensor
        complex_image = from_phase_amplitude(phase, amplitude)

        return complex_image
```

### Telescope Measurement with Complex Values

```python
class Telescope(nn.Module):
    """Telescope with complex-valued measurements."""

    def forward(
        self,
        complex_image: Tensor,
        centers: list[tuple[float, float]]
    ) -> list[Tensor]:
        """Take measurements of complex image.

        Parameters
        ----------
        complex_image : Tensor
            Complex-valued image [1, 1, H, W]
        centers : list[tuple[float, float]]
            Measurement positions

        Returns
        -------
        list[Tensor]
            Complex-valued measurements
        """
        measurements = []

        for center in centers:
            # Create aperture mask
            mask = self.create_mask(center)  # [H, W], real

            # Apply mask (broadcasts to complex)
            masked = complex_image * mask  # [1, 1, H, W], complex

            # FFT to measurement plane
            measurement = fft(masked)  # [1, 1, H, W], complex

            # Add noise (complex noise)
            if self.snr is not None:
                noise_real = torch.randn_like(measurement.real) / self.snr
                noise_imag = torch.randn_like(measurement.imag) / self.snr
                noise = torch.complex(noise_real, noise_imag)
                measurement = measurement + noise

            measurements.append(measurement)

        return measurements
```

### Complex Loss Functions

```python
def complex_mse_loss(pred: Tensor, target: Tensor) -> Tensor:
    """MSE loss for complex-valued tensors.

    Parameters
    ----------
    pred : Tensor
        Predicted complex tensor [B, C, H, W]
    target : Tensor
        Target complex tensor [B, C, H, W]

    Returns
    -------
    Tensor
        Scalar loss
    """
    # Separate real and imaginary parts
    loss_real = F.mse_loss(pred.real, target.real)
    loss_imag = F.mse_loss(pred.imag, target.imag)

    return loss_real + loss_imag

def phase_amplitude_loss(pred: Tensor, target: Tensor) -> Tensor:
    """Loss in phase-amplitude space.

    Parameters
    ----------
    pred : Tensor
        Predicted complex tensor
    target : Tensor
        Target complex tensor

    Returns
    -------
    Tensor
        Scalar loss
    """
    # Convert to phase and amplitude
    pred_phase, pred_amp = to_phase_amplitude(pred)
    target_phase, target_amp = to_phase_amplitude(target)

    # Loss on amplitude
    amp_loss = F.mse_loss(pred_amp, target_amp)

    # Loss on phase (handle wrapping)
    phase_diff = pred_phase - target_phase
    # Wrap to [-π, π]
    phase_diff = torch.atan2(torch.sin(phase_diff), torch.cos(phase_diff))
    phase_loss = (phase_diff ** 2).mean()

    return amp_loss + phase_loss
```

## Visualization

```python
def visualize_complex_image(complex_tensor: Tensor, title: str = ""):
    """Visualize complex image as phase and amplitude.

    Parameters
    ----------
    complex_tensor : Tensor
        Complex image [1, 1, H, W]
    title : str
        Plot title
    """
    # Convert to numpy [H, W]
    img = complex_tensor[0, 0].detach().cpu()

    phase = img.angle().numpy()
    amplitude = img.abs().numpy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Phase (use hsv colormap for [-π, π])
    im1 = ax1.imshow(phase, cmap='hsv', vmin=-np.pi, vmax=np.pi)
    ax1.set_title(f'{title} - Phase')
    plt.colorbar(im1, ax=ax1, label='Phase (radians)')

    # Amplitude
    im2 = ax2.imshow(amplitude, cmap='gray')
    ax2.set_title(f'{title} - Amplitude')
    plt.colorbar(im2, ax=ax2, label='Amplitude')

    plt.tight_layout()
    return fig
```

## Common Pitfalls

### Pitfall 1: Forgetting dtype

```python
# Wrong - may lose imaginary part
complex_tensor = torch.tensor([1+2j, 3+4j])  # dtype inferred incorrectly

# Correct - specify dtype
complex_tensor = torch.tensor([1+2j, 3+4j], dtype=torch.complex64)
```

### Pitfall 2: Operations Not Complex-Safe

```python
# Some operations don't support complex
complex_tensor = torch.randn(10, dtype=torch.complex64)

# Error: relu not defined for complex
# output = F.relu(complex_tensor)

# Solution: Apply to real and imag separately
output = torch.complex(
    F.relu(complex_tensor.real),
    F.relu(complex_tensor.imag)
)
```

### Pitfall 3: Phase Wrapping

```python
# Phase differences can wrap around
phase1 = torch.tensor([3.0])  # Near π
phase2 = torch.tensor([-3.0])  # Near -π

# Direct difference gives large value
diff = phase1 - phase2  # 6.0 radians

# Correct: wrap to [-π, π]
diff_wrapped = torch.atan2(torch.sin(diff), torch.cos(diff))  # Near 0
```

## Type Hints

```python
from torch import Tensor
from typing import TypeAlias

# Type aliases for clarity
ComplexTensor: TypeAlias = Tensor  # Complex-valued tensor
PhaseTensor: TypeAlias = Tensor  # Phase in radians
AmplitudeTensor: TypeAlias = Tensor  # Non-negative amplitude

def process_complex(
    image: ComplexTensor
) -> tuple[PhaseTensor, AmplitudeTensor]:
    """Process complex image."""
    phase = image.angle()
    amplitude = image.abs()
    return phase, amplitude
```

## Testing Complex Operations

```python
def test_fft_inverse():
    """Test FFT followed by IFFT returns original."""
    image = torch.randn(1, 1, 256, 256)

    freq = fft(image)
    reconstructed = ifft(freq)

    assert torch.allclose(reconstructed.real, image, rtol=1e-5)
    assert torch.allclose(reconstructed.imag, torch.zeros_like(image), atol=1e-7)

def test_phase_amplitude_roundtrip():
    """Test phase/amplitude conversion roundtrip."""
    original = torch.randn(1, 1, 256, 256, dtype=torch.complex64)

    phase, amplitude = to_phase_amplitude(original)
    reconstructed = from_phase_amplitude(phase, amplitude)

    assert torch.allclose(reconstructed, original, rtol=1e-5)
```
