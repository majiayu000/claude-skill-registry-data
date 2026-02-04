---
name: torch-shape-validator
description: Add tensor shape validation and documentation to PyTorch code. This skill should be used when working with PyTorch models to ensure tensor shapes are correct and well-documented with inline comments.
---

# PyTorch Shape Validator

Add comprehensive tensor shape documentation and runtime validation to PyTorch code.

## Purpose

Tensor shape mismatches are a common source of bugs in deep learning code. This skill adds inline shape comments and runtime assertions to catch shape errors early and make code self-documenting.

## When to Use

Use this skill when:
- Working with PyTorch models and tensor operations
- Debugging shape mismatches
- Adding documentation to tensor-heavy code
- Want runtime validation during development

## Shape Documentation Pattern

### Inline Shape Comments

```python
def forward(self, x: Tensor) -> Tensor:  # [B, C, H, W] -> [B, C', H', W']
    """Forward pass through network.

    Args:
        x: Input tensor [B, C, H, W]

    Returns:
        Output tensor [B, C', H', W']
    """
    # x: [B, C, H, W]
    x = self.conv1(x)  # [B, C, H, W] -> [B, 64, H, W]

    x = F.relu(x)  # [B, 64, H, W]

    x = self.conv2(x)  # [B, 64, H, W] -> [B, 128, H/2, W/2]

    return x  # [B, 128, H/2, W/2]
```

### Shape Notation

- `B`: Batch size
- `C`: Channels
- `H`, `W`: Height, Width
- `D`: Depth (3D)
- `L`: Sequence length
- `N`: Number of elements
- `*`: Variable size

Examples:
```python
image: Tensor  # [B, 3, 256, 256]
mask: Tensor  # [B, 1, H, W]
sequence: Tensor  # [B, L, D]
points: Tensor  # [N, 2]
variable: Tensor  # [*, H, W] - variable batch size
```

## Runtime Assertions

### Basic Shape Checks

```python
def process_image(image: Tensor) -> Tensor:
    """Process a batch of images."""
    # Validate input shape
    assert image.ndim == 4, f"Expected 4D tensor [B, C, H, W], got {image.ndim}D"
    assert image.shape[1] == 3, f"Expected 3 channels, got {image.shape[1]}"

    B, C, H, W = image.shape

    # Process...
    result = transform(image)

    # Validate output shape
    assert result.shape == (B, C, H, W), \
        f"Shape mismatch: expected {(B, C, H, W)}, got {result.shape}"

    return result
```

### Detailed Validation

```python
def validate_tensor_shape(
    tensor: Tensor,
    expected_ndim: int,
    expected_shape: tuple[int | None, ...],
    name: str = "tensor"
) -> None:
    """Validate tensor has expected shape.

    Args:
        tensor: Tensor to validate
        expected_ndim: Expected number of dimensions
        expected_shape: Expected shape (None for any size)
        name: Tensor name for error messages

    Raises:
        AssertionError: If shape doesn't match

    Example:
        >>> validate_tensor_shape(image, 4, (None, 3, 256, 256), "image")
    """
    assert tensor.ndim == expected_ndim, \
        f"{name}: expected {expected_ndim}D tensor, got {tensor.ndim}D"

    for i, (actual, expected) in enumerate(zip(tensor.shape, expected_shape)):
        if expected is not None:
            assert actual == expected, \
                f"{name}: dimension {i} expected {expected}, got {actual}"
```

### Conditional Validation

Use assertions only in development:

```python
def forward(self, x: Tensor) -> Tensor:
    if __debug__:  # Only in development mode
        assert x.ndim == 4, f"Expected 4D, got {x.ndim}D"
        assert x.shape[1] == self.in_channels

    # Production code
    return self.layer(x)
```

Run with `-O` flag to disable assertions in production:
```bash
python -O script.py  # Assertions disabled
```

## Shape Comments for Complex Operations

### FFT Operations

```python
def fft2(image: Tensor) -> Tensor:
    """2D Fourier transform.

    Args:
        image: Spatial domain image [B, C, H, W]

    Returns:
        Frequency domain tensor [B, C, H, W] (complex)
    """
    # image: [B, C, H, W] (real)
    freq = torch.fft.fft2(image, norm='ortho')  # [B, C, H, W] (complex)

    # Shift zero frequency to center
    freq = torch.fft.fftshift(freq, dim=(-2, -1))  # [B, C, H, W] (complex)

    return freq  # [B, C, H, W] (complex)
```

### Reshaping Operations

```python
def flatten_spatial(x: Tensor) -> Tensor:
    """Flatten spatial dimensions.

    Args:
        x: Input tensor [B, C, H, W]

    Returns:
        Flattened tensor [B, C*H*W]
    """
    B, C, H, W = x.shape  # [B, C, H, W]

    # Reshape to merge spatial dims
    x = x.reshape(B, C * H * W)  # [B, C, H, W] -> [B, C*H*W]

    return x  # [B, C*H*W]
```

### Broadcasting

```python
def apply_mask(image: Tensor, mask: Tensor) -> Tensor:
    """Apply mask to image.

    Args:
        image: Image tensor [B, C, H, W]
        mask: Binary mask [B, 1, H, W] or [H, W]

    Returns:
        Masked image [B, C, H, W]
    """
    # image: [B, C, H, W]
    # mask: [B, 1, H, W] or [H, W]

    if mask.ndim == 2:
        # Broadcast [H, W] to [1, 1, H, W]
        mask = mask[None, None, :, :]  # [H, W] -> [1, 1, H, W]

    # Element-wise multiplication with broadcasting
    # [B, C, H, W] * [B, 1, H, W] -> [B, C, H, W]
    masked = image * mask

    return masked  # [B, C, H, W]
```

## Type Aliases for Complex Shapes

```python
# prism/types.py
from typing import TypeAlias
from torch import Tensor

# Image types with documented shapes
ImageBatch: TypeAlias = Tensor  # [B, C, H, W]
ImageSingle: TypeAlias = Tensor  # [1, 1, H, W]
ComplexImage: TypeAlias = Tensor  # [B, C, H, W] complex-valued

# Mask types
BinaryMask: TypeAlias = Tensor  # [H, W], values in {0, 1}
BatchMask: TypeAlias = Tensor  # [B, 1, H, W], values in {0, 1}

# Coordinate types
Points2D: TypeAlias = Tensor  # [N, 2], (y, x) coordinates
Grid2D: TypeAlias = Tensor  # [H, W, 2], (y, x) at each pixel

# Use in code
def process(image: ImageBatch, mask: BinaryMask) -> ImageBatch:
    pass
```

## Validation Helpers

Create reusable validation functions:

```python
# prism/utils/validation.py
"""Tensor shape validation utilities."""

from torch import Tensor

def assert_image_batch(tensor: Tensor, channels: int | None = None) -> None:
    """Assert tensor is valid image batch [B, C, H, W]."""
    assert tensor.ndim == 4, f"Expected 4D [B, C, H, W], got {tensor.ndim}D"

    if channels is not None:
        actual_channels = tensor.shape[1]
        assert actual_channels == channels, \
            f"Expected {channels} channels, got {actual_channels}"


def assert_same_spatial_size(t1: Tensor, t2: Tensor) -> None:
    """Assert tensors have same spatial dimensions."""
    assert t1.shape[-2:] == t2.shape[-2:], \
        f"Spatial size mismatch: {t1.shape[-2:]} vs {t2.shape[-2:]}"


def get_spatial_shape(tensor: Tensor) -> tuple[int, int]:
    """Extract (H, W) from tensor."""
    assert tensor.ndim >= 2, "Tensor must have at least 2 dimensions"
    return tensor.shape[-2], tensor.shape[-1]
```

Usage:

```python
def forward(self, image: Tensor, mask: Tensor) -> Tensor:
    assert_image_batch(image, channels=3)
    assert_same_spatial_size(image, mask)

    H, W = get_spatial_shape(image)
    # ...
```

## Shape Tracking in Complex Models

```python
class ProgressiveDecoder(nn.Module):
    def __init__(self, size: int = 256):
        super().__init__()
        # Track shapes through network
        self.size = size  # Output spatial size

        # Document expected shapes at each layer
        self.conv1 = nn.Conv2d(1, 64, 3, padding=1)  # [B, 1, H, W] -> [B, 64, H, W]
        self.conv2 = nn.Conv2d(64, 128, 3, stride=2, padding=1)  # [B, 64, H, W] -> [B, 128, H/2, W/2]
        self.up1 = nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1)  # [B, 128, H/2, W/2] -> [B, 64, H, W]

    def forward(self, x: Tensor | None = None) -> Tensor:
        """Generate output image.

        Args:
            x: Optional input [B, 1, H, W]. If None, generates from latent.

        Returns:
            Output image [B, 1, size, size]
        """
        if x is None:
            # Generate from latent
            B = 1
            x = self.latent.expand(B, -1, 1, 1)  # [1, C] -> [B, C, 1, 1]

        # Track shapes through network
        if __debug__:
            shapes = {}
            shapes['input'] = x.shape

        x = self.conv1(x)  # [B, C_in, H, W] -> [B, 64, H, W]
        if __debug__:
            shapes['conv1'] = x.shape

        x = F.relu(x)  # [B, 64, H, W]

        x = self.conv2(x)  # [B, 64, H, W] -> [B, 128, H/2, W/2]
        if __debug__:
            shapes['conv2'] = x.shape

        x = self.up1(x)  # [B, 128, H/2, W/2] -> [B, 64, H, W]
        if __debug__:
            shapes['up1'] = x.shape
            print(f"Shape progression: {shapes}")

        return x  # [B, 1, H, W]
```

## Checklist

For tensor-heavy code:
- [ ] All tensors have shape comments on first use
- [ ] Function signatures document input/output shapes
- [ ] Critical operations have shape assertions
- [ ] Reshape/view operations clearly documented
- [ ] Broadcasting behavior documented
- [ ] Complex shapes use type aliases
- [ ] Validation helpers used where appropriate
