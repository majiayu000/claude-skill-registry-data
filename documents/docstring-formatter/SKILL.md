---
name: docstring-formatter
description: Convert docstrings to NumPy/Sphinx style with proper Parameters, Returns, and Examples sections. This skill should be used when improving documentation quality across Python modules.
---

# Docstring Formatter

Convert and enhance Python docstrings to follow NumPy documentation style with complete Parameters, Returns, Examples, and Notes sections.

## Purpose

Well-formatted docstrings are essential for code documentation and API reference generation. This skill systematically converts docstrings to NumPy style and ensures completeness.

## When to Use

Use this skill when:
- Converting existing docstrings to NumPy style
- Adding missing docstring sections
- Preparing code for Sphinx documentation
- Improving API documentation quality
- Phase 3 (Code Quality) documentation tasks (~50+ docstrings)

## NumPy Docstring Style

### Complete Docstring Template

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """Brief one-line summary (under 80 chars).

    Extended description providing more context about what the function does,
    when to use it, and any important considerations. This can span multiple
    paragraphs if needed.

    Parameters
    ----------
    param1 : Type1
        Description of param1. Can span multiple lines if needed,
        but subsequent lines should be indented.
    param2 : Type2, optional
        Description of param2. Use "optional" for parameters with defaults.
        Default is <value>.

    Returns
    -------
    ReturnType
        Description of return value. For multiple return values,
        list each separately.

    Raises
    ------
    ValueError
        When param1 is negative
    TypeError
        When param2 is not the expected type

    See Also
    --------
    related_function : Brief description
    OtherClass.method : Another related function

    Notes
    -----
    Additional information about the implementation, algorithms used,
    mathematical formulas (in LaTeX), performance considerations, etc.

    .. math:: E = mc^2

    References
    ----------
    .. [1] Author Name, "Paper Title", Journal, Year.
    .. [2] https://example.com/reference

    Examples
    --------
    >>> result = function_name(10, 20)
    >>> print(result)
    30

    For more complex examples:

    >>> data = np.array([1, 2, 3])
    >>> result = function_name(data, param2=True)
    >>> assert len(result) == 3
    """
    pass
```

## Conversion Workflow

### Step 1: Read Existing Docstring

Identify current format:
- Google style: `Args:`, `Returns:`
- NumPy style: `Parameters`, `Returns` (underlined)
- Plain text: Unstructured description
- Missing: No docstring at all

### Step 2: Extract Information

From the function signature and existing docs:
- Function purpose (one-line summary)
- Each parameter: name, type, description
- Return value: type, description
- Exceptions raised
- Usage examples (if present)

### Step 3: Write NumPy Docstring

Follow the template structure:
1. One-line summary (< 80 chars)
2. Extended description (if needed)
3. Parameters section
4. Returns section
5. Raises section (if applicable)
6. Examples section

## Common Patterns

### Basic Function

```python
# Before - plain text
def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# After - NumPy style
def calculate_distance(
    p1: tuple[float, float],
    p2: tuple[float, float]
) -> float:
    """Calculate Euclidean distance between two points.

    Parameters
    ----------
    p1 : tuple[float, float]
        First point as (x, y) coordinates
    p2 : tuple[float, float]
        Second point as (x, y) coordinates

    Returns
    -------
    float
        Euclidean distance between the points

    Examples
    --------
    >>> distance = calculate_distance((0, 0), (3, 4))
    >>> print(f"{distance:.1f}")
    5.0
    """
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
```

### PyTorch nn.Module

```python
class ProgressiveDecoder(nn.Module):
    """Generative network for progressive reconstruction from sparse measurements.

    This decoder-only architecture generates phase and amplitude images
    from a learned latent vector, progressively upsampling from 1x1 to
    the target resolution.

    Parameters
    ----------
    latent_dim : int, optional
        Dimension of latent vector. Default is 128.
    hidden_channels : list[int], optional
        Number of channels in each hidden layer.
        Default is [64, 128, 256].
    output_size : int, optional
        Spatial size of output image. Default is 256.
    use_complex : bool, optional
        Whether to generate complex-valued output. Default is False.

    Attributes
    ----------
    latent : nn.Parameter
        Learnable latent vector of shape [1, latent_dim]
    decoder : nn.Sequential
        Decoder network with transposed convolutions

    Examples
    --------
    >>> model = ProgressiveDecoder(output_size=256)
    >>> output = model()  # Generate from latent
    >>> output.shape
    torch.Size([1, 2, 256, 256])

    >>> # Generate with specific latent
    >>> latent = torch.randn(1, 128, 1, 1)
    >>> output = model(latent)
    """

    def __init__(
        self,
        latent_dim: int = 128,
        hidden_channels: list[int] = [64, 128, 256],
        output_size: int = 256,
        use_complex: bool = False
    ) -> None:
        """Initialize ProgressiveDecoder."""
        super().__init__()
        # ...

    def forward(self, x: Optional[Tensor] = None) -> Tensor:
        """Generate output image.

        Parameters
        ----------
        x : Tensor, optional
            Input latent vector with shape [B, C, 1, 1].
            If None, uses the learned latent. Default is None.

        Returns
        -------
        Tensor
            Generated image with shape [B, 2, H, W] where the two channels
            represent phase and amplitude (or real and imaginary parts if
            use_complex is True).

        Examples
        --------
        >>> model = ProgressiveDecoder(output_size=256)
        >>> output = model()  # Use learned latent
        >>> output.shape
        torch.Size([1, 2, 256, 256])
        """
        # ...
```

### Function with Multiple Returns

```python
def train_step(
    model: nn.Module,
    data: Tensor,
    optimizer: torch.optim.Optimizer
) -> tuple[Tensor, dict[str, float]]:
    """Perform single training step.

    Parameters
    ----------
    model : nn.Module
        Model to train
    data : Tensor
        Input data batch with shape [B, C, H, W]
    optimizer : torch.optim.Optimizer
        Optimizer for parameter updates

    Returns
    -------
    loss : Tensor
        Scalar loss value
    metrics : dict[str, float]
        Dictionary containing training metrics:
        - 'loss': Loss value as float
        - 'grad_norm': Gradient norm
        - 'lr': Current learning rate

    Examples
    --------
    >>> model = ProgressiveDecoder()
    >>> optimizer = torch.optim.Adam(model.parameters())
    >>> data = torch.randn(8, 1, 256, 256)
    >>> loss, metrics = train_step(model, data, optimizer)
    >>> print(f"Loss: {loss.item():.4f}")
    """
    # ...
```

### Property with Setter

```python
@property
def grid(self) -> Tensor:
    """Coordinate grid for spatial operations.

    Returns
    -------
    Tensor
        Grid tensor with shape [H, W, 2] containing (y, x) coordinates
        at each pixel location, normalized to [-1, 1].

    Notes
    -----
    The grid is lazily initialized on first access and cached for
    subsequent calls.

    Examples
    --------
    >>> telescope = Telescope(n=256)
    >>> grid = telescope.grid
    >>> grid.shape
    torch.Size([256, 256, 2])
    >>> grid[128, 128]  # Center point
    tensor([0., 0.])
    """
    if self._grid is None:
        self._grid = self._create_grid()
    return self._grid

@grid.setter
def grid(self, value: Tensor) -> None:
    """Set coordinate grid.

    Parameters
    ----------
    value : Tensor
        New grid tensor with shape [H, W, 2]

    Raises
    ------
    ValueError
        If grid shape doesn't match (n, n, 2)
    """
    if value.shape != (self.n, self.n, 2):
        raise ValueError(f"Grid shape must be ({self.n}, {self.n}, 2)")
    self._grid = value
```

## PRISM-Specific Patterns

### Telescope/Optics Functions

```python
def measure(
    self,
    image: Tensor,
    centers: list[tuple[float, float]]
) -> list[Tensor]:
    """Take telescope measurements at specified aperture positions.

    Simulates realistic telescope measurements by applying circular aperture
    masks at each center position. Includes shot noise if SNR is specified.

    Parameters
    ----------
    image : Tensor
        Input image in spatial or frequency domain, shape [B, C, H, W]
    centers : list[tuple[float, float]]
        List of aperture center positions as (y, x) coordinates in pixels.
        Coordinates are relative to image center.

    Returns
    -------
    list[Tensor]
        List of measurement tensors, one per aperture position.
        Each tensor has shape [B, C, H, W] with non-zero values only
        within the aperture.

    See Also
    --------
    mask : Create aperture mask
    TelescopeAgg : Aggregate multiple measurements

    Notes
    -----
    The measurement process follows the Fraunhofer diffraction model:

    .. math:: I(u,v) = |\\mathcal{F}\\{A(x,y) \\cdot E(x,y)\\}|^2

    where :math:`A(x,y)` is the aperture function and :math:`E(x,y)`
    is the electric field.

    Examples
    --------
    >>> telescope = Telescope(n=256, r=10, snr=40)
    >>> image = torch.randn(1, 1, 256, 256)
    >>> centers = [(0, 0), (20, 0), (0, 20)]
    >>> measurements = telescope.measure(image, centers)
    >>> len(measurements)
    3
    """
    # ...
```

### FFT/Transform Functions

```python
def fft(image: Tensor, norm: str = 'ortho') -> Tensor:
    """Compute 2D Fast Fourier Transform.

    Parameters
    ----------
    image : Tensor
        Input image tensor with shape [B, C, H, W].
        Can be real or complex-valued.
    norm : str, optional
        Normalization mode: 'ortho', 'forward', or 'backward'.
        Default is 'ortho'.

    Returns
    -------
    Tensor
        Frequency domain tensor with shape [B, C, H, W].
        Always complex-valued.

    See Also
    --------
    ifft : Inverse FFT
    fftshift : Shift zero frequency to center

    Notes
    -----
    Uses PyTorch's FFT implementation which is CUDA-optimized when
    input is on GPU. For large images (>1024x1024), consider using
    real FFT (rfft2) if input is guaranteed to be real.

    The FFT is computed with periodic boundary conditions.

    Examples
    --------
    >>> image = torch.randn(1, 1, 256, 256)
    >>> freq = fft(image)
    >>> freq.dtype
    torch.complex64

    Verify Parseval's theorem (energy conservation):

    >>> spatial_energy = image.pow(2).sum()
    >>> freq_energy = freq.abs().pow(2).sum()
    >>> torch.allclose(spatial_energy, freq_energy)
    True
    """
    return torch.fft.fft2(image, norm=norm)
```

## Conversion from Other Styles

### Google Style → NumPy Style

```python
# Before - Google style
def process(data, threshold=0.5):
    """Process data with threshold.

    Args:
        data: Input data array
        threshold: Threshold value (default: 0.5)

    Returns:
        Processed data array

    Raises:
        ValueError: If threshold is negative
    """
    pass

# After - NumPy style
def process(data: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Process data with threshold.

    Parameters
    ----------
    data : np.ndarray
        Input data array
    threshold : float, optional
        Threshold value. Default is 0.5.

    Returns
    -------
    np.ndarray
        Processed data array

    Raises
    ------
    ValueError
        If threshold is negative
    """
    pass
```

## Section Guidelines

### Parameters Section
- Use `Type` not `type`
- Add "optional" for parameters with defaults
- State the default value: "Default is X"
- Indent continuation lines

### Returns Section
- For single return: Type followed by description
- For multiple returns: Name each return value
- Use descriptive names, not just types

### Examples Section
- Use `>>>` for interactive Python
- Show realistic use cases
- Include expected output when helpful
- Test that examples actually work

### Notes Section
- Implementation details
- Algorithm description
- Performance considerations
- LaTeX math using `.. math::`

## Validation Checklist

For each docstring:
- [ ] One-line summary under 80 characters
- [ ] All parameters documented with types
- [ ] Return value documented with type
- [ ] At least one example provided
- [ ] Examples are executable and correct
- [ ] Optional parameters marked as "optional"
- [ ] Default values stated
- [ ] Exceptions documented if raised
- [ ] Follows NumPy format exactly

## Tools for Validation

Check docstring quality:
```bash
# Install pydocstyle
uv add --dev pydocstyle

# Check docstrings
pydocstyle prism/

# Sphinx can build from docstrings
uv add --dev sphinx
sphinx-build -b html docs/ docs/_build
```

## Batch Conversion Strategy

For large modules:
1. Start with public API functions (most important)
2. Then convert class methods
3. Finally convert private functions
4. Test documentation generation after each module
