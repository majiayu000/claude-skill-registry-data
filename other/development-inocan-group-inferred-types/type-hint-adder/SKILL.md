---
name: type-hint-adder
description: Add comprehensive type hints to Python functions and methods, including PyTorch tensor types. This skill should be used when improving code quality through static type checking or when preparing code for mypy validation.
---

# Type Hint Adder

Add comprehensive, accurate type hints to Python code with special support for PyTorch/scientific computing types.

## Purpose

Type hints improve code maintainability, enable static type checking with mypy, and provide better IDE support. This skill systematically adds type annotations following Python typing best practices with special attention to PyTorch tensor shapes and complex types.

## When to Use

Use this skill when:
- Adding type hints to untyped functions (100+ functions in a refactoring)
- Preparing code for mypy validation
- Improving IDE autocompletion and error detection
- Documenting expected types for complex PyTorch operations
- Working with scientific computing code requiring tensor shape documentation

## Workflow

### Step 1: Analyze Function Signature

Identify all parameters and return types:

```python
# Before
def process_image(tensor, size, normalize=True):
    result = tensor.resize(size)
    if normalize:
        result = result / result.max()
    return result
```

### Step 2: Determine Appropriate Types

For each parameter and return value:
- Check usage within function
- Identify if it's a primitive, collection, or custom type
- For PyTorch tensors, document expected shapes
- Consider Optional for parameters that can be None

### Step 3: Add Type Hints

```python
# After
from typing import Optional
import torch
from torch import Tensor

def process_image(
    tensor: Tensor,  # [B, C, H, W]
    size: tuple[int, int],
    normalize: bool = True
) -> Tensor:  # [B, C, H', W']
    result = tensor.resize(size)
    if normalize:
        result = result / result.max()
    return result
```

### Step 4: Add Required Imports

Ensure all type hint imports are present:

```python
# Standard typing imports
from typing import Optional, Union, List, Dict, Tuple, Callable, Any, TypeAlias

# For Python 3.9+ builtin generics
from collections.abc import Sequence, Mapping

# PyTorch types
import torch
from torch import Tensor, nn

# Custom type aliases
TensorImage: TypeAlias = Tensor  # [B, C, H, W]
ComplexTensor: TypeAlias = Tensor  # Complex-valued tensor
```

## Type Hint Patterns

### Basic Types

```python
def calculate(x: int, y: float, name: str) -> float:
    return x * y

def get_config(path: str) -> dict[str, Any]:
    # Use dict[str, Any] for unstructured dicts
    pass

def process_items(items: list[int]) -> list[int]:
    # Python 3.9+ allows list[] instead of List[]
    pass
```

### Optional and Union

```python
from typing import Optional, Union

def load_image(path: Optional[str] = None) -> Tensor:
    # Optional[T] is shorthand for Union[T, None]
    pass

def process(data: Union[Tensor, np.ndarray]) -> Tensor:
    # Union for multiple possible types
    pass
```

### PyTorch Tensor Types

```python
from torch import Tensor

# Basic tensor
def forward(x: Tensor) -> Tensor:
    pass

# With shape documentation in comments
def forward(x: Tensor) -> Tensor:  # [B, C, H, W] -> [B, C', H', W']
    pass

# Create type aliases for clarity
TensorImage: TypeAlias = Tensor  # [B, C, H, W]
TensorMask: TypeAlias = Tensor  # [B, 1, H, W], values in {0, 1}

def mask_image(image: TensorImage, mask: TensorMask) -> TensorImage:
    pass
```

### Complex nn.Module Classes

```python
from torch import nn, Tensor
from typing import Optional

class Telescope(nn.Module):
    def __init__(
        self,
        n: int,
        r: float,
        snr: Optional[float] = None
    ) -> None:
        super().__init__()
        self.n = n
        self.r = r
        self.snr = snr

    def forward(
        self,
        tensor: Tensor,  # [B, C, H, W]
        centers: list[list[float]]
    ) -> Tensor:  # [B, 1, H, W]
        pass
```

### Callable Types

```python
from typing import Callable

def apply_transform(
    tensor: Tensor,
    transform: Callable[[Tensor], Tensor]
) -> Tensor:
    return transform(tensor)

# With specific signature
LossFunction: TypeAlias = Callable[[Tensor, Tensor], Tensor]

def train(loss_fn: LossFunction) -> None:
    pass
```

### Generic Classes

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value
```

### TYPE_CHECKING Pattern

Avoid circular imports:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .telescope import Telescope
    from .grid import Grid

class Aggregator:
    def __init__(self, telescope: 'Telescope', grid: 'Grid') -> None:
        # String annotations avoid runtime import
        self.telescope = telescope
        self.grid = grid
```

## PRISM-Specific Type Aliases

Create these in a types.py module:

```python
# prism/types.py
"""Type definitions for PRISM project."""

from typing import TypeAlias
from torch import Tensor

# Image types
TensorImage: TypeAlias = Tensor  # [B, C, H, W] - Batch of images
ComplexImage: TypeAlias = Tensor  # Complex-valued image tensor

# Measurement types
TensorMask: TypeAlias = Tensor  # [H, W] - Binary mask, values in {0, 1}
MeasurementPoints: TypeAlias = list[tuple[float, float]]  # [(y, x), ...]

# Grid types
GridCoordinates: TypeAlias = Tensor  # [H, W, 2] - (y, x) coordinates

# Configuration types (from dataclasses)
from dataclasses import dataclass

@dataclass
class ImageConfig:
    size: int
    crop: bool
    # ...
```

## Common Patterns for PRISM

### FFT Functions

```python
def fft(tensor: Tensor, norm: str = 'ortho') -> Tensor:
    """Perform 2D FFT on image tensor.

    Args:
        tensor: Input image tensor [B, C, H, W]
        norm: Normalization mode

    Returns:
        Frequency domain tensor [B, C, H, W]
    """
    return torch.fft.fft2(tensor, norm=norm)

def ifft(tensor: Tensor, norm: str = 'ortho') -> Tensor:
    """Inverse 2D FFT.

    Args:
        tensor: Frequency domain tensor [B, C, H, W]
        norm: Normalization mode

    Returns:
        Spatial domain tensor [B, C, H, W]
    """
    return torch.fft.ifft2(tensor, norm=norm)
```

### Model Forward Methods

```python
class ProgressiveDecoder(nn.Module):
    def forward(
        self,
        obj_size: Optional[int] = None
    ) -> tuple[Tensor, Tensor]:  # (phase, amplitude)
        """Generate phase and amplitude images.

        Args:
            obj_size: Output image size in pixels

        Returns:
            Tuple of (phase, amplitude) tensors, each [1, 1, H, W]
        """
        pass
```

### Loss Functions

```python
from torch import Tensor

class LossAgg(nn.Module):
    def forward(
        self,
        prediction: Tensor,  # [B, C, H, W]
        target: Tensor,  # [B, C, H, W]
        old_mask: Tensor,  # [H, W]
        new_mask: Tensor  # [H, W]
    ) -> Tensor:  # Scalar loss
        """Compute aggregated loss over old and new measurements."""
        pass
```

## Shape Assertions

Add runtime shape validation:

```python
def process_batch(images: Tensor) -> Tensor:  # [B, C, H, W]
    """Process a batch of images."""
    assert images.ndim == 4, f"Expected 4D tensor, got {images.ndim}D"
    assert images.shape[1] == 1, f"Expected 1 channel, got {images.shape[1]}"

    B, C, H, W = images.shape
    # Process...
    return result
```

## Validation with mypy

After adding type hints, validate with mypy:

```bash
# Install mypy
uv add --dev mypy

# Run type checking
uv run mypy prism/

# Configuration in pyproject.toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
exclude = ["tests/", "scripts/"]
```

## Gradual Typing Strategy

For large codebases, add types gradually:

1. **Start with public APIs** - Functions used by other modules
2. **Add to new code** - All new functions get type hints
3. **Incrementally type existing code** - One module at a time
4. **Use `# type: ignore` sparingly** - Only for complex cases that mypy can't handle

```python
# Temporary ignore for complex cases
result = complex_function()  # type: ignore[misc]
```

## Checklist

After adding type hints:
- [ ] All function parameters have type hints
- [ ] All return types specified
- [ ] Required imports added (typing, torch, etc.)
- [ ] Complex types use type aliases
- [ ] Tensor shapes documented in comments
- [ ] mypy validation passes (or known issues documented)
- [ ] Optional used for parameters that can be None
- [ ] No use of bare `Any` (use specific types)
