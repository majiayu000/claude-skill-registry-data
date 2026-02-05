---
name: physics-validator
description: Validate optical physics parameters including Fresnel numbers, diffraction regimes, and resolution limits. This skill should be used when configuring Telescope, Microscope, or Camera instruments to ensure physically realistic parameters.
---

# Physics Validator

Validate optical physics parameters for PRISM instruments to ensure physically realistic configurations.

## Purpose

Optical imaging simulations require careful parameter selection to produce physically meaningful results. This skill validates that instrument configurations respect fundamental optical physics constraints.

## When to Use

Use this skill when:
- Configuring Telescope, Microscope, or Camera instruments
- Checking if parameters are physically realistic
- Validating diffraction regime (Fresnel vs Fraunhofer)
- Ensuring Nyquist sampling requirements are met
- Debugging unexpected simulation results
- Setting up new experiments or configurations

## Validation Checks

### 1. Fresnel Number Analysis

The Fresnel number determines the diffraction regime:

```python
# Fresnel number formula
F = d**2 / (wavelength * distance)

# where:
#   d = aperture diameter
#   wavelength = light wavelength
#   distance = propagation distance
```

**Interpretation:**
| Fresnel Number | Regime | Propagation Method |
|----------------|--------|-------------------|
| F << 0.1 | Fraunhofer (far-field) | FFT-based |
| F >> 10 | Fresnel (near-field) | Angular Spectrum |
| 0.1 <= F <= 10 | Transition | Angular Spectrum recommended |

**PRISM Implementation:**
```python
from prism.config.constants import is_fraunhofer, is_fresnel

# Check diffraction regime
wavelength = 500e-9  # 500 nm
aperture_diameter = 0.1  # 10 cm
distance = 1000  # 1 km

fresnel_number = aperture_diameter**2 / (wavelength * distance)

if fresnel_number < 0.1:
    print("Fraunhofer regime - use FFT propagation")
elif fresnel_number > 10:
    print("Fresnel regime - use Angular Spectrum")
else:
    print("Transition regime - Angular Spectrum recommended")
```

### 2. Resolution Limits

Each instrument type has different resolution limits:

#### Telescope (Rayleigh Criterion)
```python
# Angular resolution (radians)
theta_rayleigh = 1.22 * wavelength / diameter

# Spatial resolution at distance
resolution = 1.22 * wavelength * distance / diameter

# Example: 10cm aperture, 500nm light, 1km distance
# resolution = 1.22 * 500e-9 * 1000 / 0.1 = 6.1 mm
```

#### Microscope (Abbe Limit)
```python
# Minimum resolvable feature
d_abbe = 0.61 * wavelength / NA

# where NA = numerical aperture = n * sin(theta)
# For air (n=1) with half-angle 60deg: NA = 0.866

# Example: 500nm light, NA=0.5
# d_abbe = 0.61 * 500e-9 / 0.5 = 610 nm
```

#### Camera (Airy Disk)
```python
# Airy disk diameter
d_airy = 2.44 * wavelength * f_number

# where f_number = focal_length / aperture_diameter

# Example: 500nm light, f/2.8 lens
# d_airy = 2.44 * 500e-9 * 2.8 = 3.4 um
```

### 3. Nyquist Sampling

For proper sampling, pixel size must satisfy:

```python
# Nyquist criterion
pixel_size <= resolution_limit / 2

# Examples:
# Telescope with 6mm resolution: pixel_size <= 3mm
# Microscope with 610nm resolution: pixel_size <= 305nm
# Camera with 3.4um Airy disk: pixel_size <= 1.7um
```

**Validation Function:**
```python
def validate_nyquist(pixel_size: float, resolution_limit: float) -> bool:
    """Check if pixel size satisfies Nyquist criterion."""
    nyquist_limit = resolution_limit / 2
    is_valid = pixel_size <= nyquist_limit

    if not is_valid:
        print(f"WARNING: Pixel size {pixel_size:.2e} exceeds Nyquist limit {nyquist_limit:.2e}")
        print(f"  Aliasing may occur. Reduce pixel size or increase resolution limit.")

    return is_valid
```

### 4. Physical Parameter Ranges

Common valid ranges for optical parameters:

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Wavelength | 300nm - 1100nm | Visible + near-IR |
| Telescope aperture | 1cm - 10m | Small to large telescopes |
| Microscope NA | 0.1 - 1.4 | Air to oil immersion |
| Camera f-number | f/1.0 - f/22 | Fast to slow lenses |
| SNR | 10 - 1000 | Typical imaging conditions |

**Validation:**
```python
def validate_wavelength(wavelength: float) -> bool:
    """Validate wavelength is in reasonable range."""
    if not (100e-9 <= wavelength <= 10e-6):
        print(f"WARNING: Wavelength {wavelength:.2e} outside typical range (100nm - 10um)")
        return False
    return True

def validate_numerical_aperture(na: float) -> bool:
    """Validate NA is physically possible."""
    if not (0 < na <= 1.5):  # 1.5 for oil immersion
        print(f"WARNING: NA {na} is physically impossible (must be 0 < NA <= 1.5)")
        return False
    return True
```

### 5. Depth of Field

For 3D imaging, check depth of field:

```python
# Microscope depth of field
DOF_microscope = wavelength / NA**2

# Camera depth of field (approximate)
DOF_camera = 2 * f_number * wavelength * (magnification + 1)**2

# Example: 500nm, NA=0.5
# DOF = 500e-9 / 0.25 = 2 um
```

## Complete Validation Workflow

```python
def validate_telescope_config(config: dict) -> list[str]:
    """Validate telescope configuration."""
    issues = []

    wavelength = config['wavelength']
    diameter = config['aperture_diameter']
    distance = config['distance']
    pixel_size = config.get('pixel_size')

    # 1. Check wavelength
    if not (100e-9 <= wavelength <= 10e-6):
        issues.append(f"Wavelength {wavelength:.2e} outside typical range")

    # 2. Check Fresnel number
    F = diameter**2 / (wavelength * distance)
    if 0.1 <= F <= 10:
        issues.append(f"Fresnel number {F:.2f} in transition regime - results may be approximate")

    # 3. Check resolution
    resolution = 1.22 * wavelength * distance / diameter

    # 4. Check Nyquist (if pixel size provided)
    if pixel_size and pixel_size > resolution / 2:
        issues.append(f"Pixel size {pixel_size:.2e} violates Nyquist (limit: {resolution/2:.2e})")

    # 5. Check aperture size
    if diameter > distance / 10:
        issues.append(f"Aperture {diameter} may be too large for distance {distance}")

    return issues


def validate_microscope_config(config: dict) -> list[str]:
    """Validate microscope configuration."""
    issues = []

    wavelength = config['wavelength']
    na = config['numerical_aperture']
    pixel_size = config.get('pixel_size')

    # 1. Check NA
    if not (0 < na <= 1.5):
        issues.append(f"NA {na} is physically impossible")

    # 2. Check resolution
    resolution = 0.61 * wavelength / na

    # 3. Check Nyquist
    if pixel_size and pixel_size > resolution / 2:
        issues.append(f"Pixel size {pixel_size:.2e} violates Nyquist (limit: {resolution/2:.2e})")

    # 4. Check depth of field
    dof = wavelength / na**2
    if dof < 100e-9:
        issues.append(f"Very shallow DOF ({dof:.2e}m) - focus stability critical")

    return issues
```

## Common Issues and Solutions

### Issue 1: Aliasing Artifacts
**Symptoms**: Rings, moiré patterns, or jagged edges in reconstruction
**Cause**: Pixel size too large (Nyquist violation)
**Solution**: Reduce pixel size or use anti-aliasing

### Issue 2: Missing High Frequencies
**Symptoms**: Blurry reconstruction, loss of fine detail
**Cause**: Aperture too small, resolution limit too coarse
**Solution**: Increase aperture size or reduce wavelength

### Issue 3: Incorrect Diffraction Pattern
**Symptoms**: Wrong PSF shape, unexpected propagation behavior
**Cause**: Using wrong propagation method for Fresnel number
**Solution**: Check Fresnel number and select appropriate method

### Issue 4: Numerical Instabilities
**Symptoms**: NaN values, diverging iterations
**Cause**: Parameters outside valid range
**Solution**: Validate all parameters before simulation

## Quick Reference

### Fresnel Number
```
F = d² / (λ × z)
F < 0.1 → Far-field (Fraunhofer)
F > 10  → Near-field (Fresnel)
```

### Resolution Formulas
```
Telescope:  θ = 1.22 λ/D,  δ = 1.22 λz/D
Microscope: d = 0.61 λ/NA
Camera:     d = 2.44 λ × f/#
```

### Nyquist
```
pixel_size ≤ resolution_limit / 2
```

## Related Skills

- **torch-shape-validator**: Validate tensor dimensions in optical computations
- **complex-tensor-handler**: Handle complex-valued fields in Fourier optics
- **unit-test-generator**: Create tests for physics validation functions

## Checklist

Before running simulations:
- [ ] Wavelength in valid range (100nm - 10um)
- [ ] Fresnel number checked, appropriate propagation selected
- [ ] Resolution limit calculated for instrument type
- [ ] Nyquist sampling satisfied
- [ ] Aperture/NA in physical range
- [ ] Depth of field adequate for sample thickness
- [ ] SNR appropriate for detection conditions
