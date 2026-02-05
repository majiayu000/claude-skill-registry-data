---
name: lightsheet-psf-deconvolution
description: "KINTSUGI deconvolution: True lightsheet PSF calculation to fix horizontal banding artifacts. Trigger: deconvolution artifacts, horizontal banding, PSF issues, fcyl, slitwidth, lightsheet, LsDeconv."
author: KINTSUGI Team
date: 2025-12-27
---

# Lightsheet PSF for Deconvolution - Fixing Horizontal Banding Artifacts

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-27 |
| **Goal** | Fix horizontal banding artifacts in Python deconvolution by implementing true lightsheet PSF |
| **Environment** | KINTSUGI KDecon module, HiPerGator, CuPy GPU |
| **Status** | RESOLVED |

## Context

The Python KDecon module was producing horizontal banding artifacts after deconvolution. The original MATLAB LsDeconv.m worked correctly. Investigation revealed that Python was using a widefield PSF that ignored the lightsheet parameters (`fcyl` and `slitwidth`), while MATLAB used a true lightsheet PSF.

## Root Cause

The lightsheet PSF is fundamentally different from a widefield PSF:

### Widefield PSF (WRONG for lightsheet data)
```python
# Both excitation and emission use same NA and coordinate system
psf_ex = PSF(x, y, z, NA, n, lambda_ex)
psf_em = PSF(x, y, z, NA, n, lambda_em)
psf = psf_ex * psf_em
```

### Lightsheet PSF (CORRECT - from MATLAB LsDeconv.m)
```python
# Excitation uses lightsheet NA and SWAPPED coordinates (z, 0, x)
# Emission uses objective NA and standard coordinates (x, y, z)
NA_ls = np.sin(np.arctan(slitwidth / (2 * fcyl)))  # ~0.956 for fcyl=1, slitwidth=6.5
psf_ex = PSF(z, 0, x, NA_ls, n, lambda_ex)   # Note: z->x, y->0, x->z
psf_em = PSF(x, y, z, NA_obj, n, lambda_em)  # Standard coordinates
psf = psf_ex * psf_em
```

The coordinate swap `(z, 0, x)` instead of `(x, y, z)` models the lightsheet illuminating perpendicular to the detection axis.

## Solution

### 1. Added `_psf_light_sheet_full()` function to `psf.py`

```python
def _psf_light_sheet_full(x, y, z, NA_obj, n, lambda_ex, lambda_em, NA_ls):
    """
    True lightsheet PSF matching MATLAB LsDeconv implementation.
    """
    # Lightsheet excitation PSF - coordinate swap (z, 0, x)
    psf_ex = _psf_single_wavelength(z, 0, x, NA_ls, n, lambda_ex)
    # Objective emission PSF - standard (x, y, z)
    psf_em = _psf_single_wavelength(x, y, z, NA_obj, n, lambda_em)
    return psf_ex * psf_em
```

### 2. Updated `generate_psf()` to use lightsheet mode when parameters provided

```python
def generate_psf(dxy, dz, NA, n, lambda_ex, lambda_em,
                 fcyl=None, slitwidth=None, ...):
    use_lightsheet = fcyl is not None and slitwidth is not None
    if use_lightsheet:
        NA_ls = np.sin(np.arctan(slitwidth / (2 * fcyl)))
        # Use _psf_light_sheet_full instead of _psf_light_sheet
```

### 3. Updated `main.py` to pass parameters through

```python
def _compute_psf(self):
    self._psf, self._psf_info = generate_psf(
        self.dxy, self.dz, self.NA, self.rf,
        self.lambda_ex, self.lambda_em,
        fcyl=self.fcyl,        # ADD
        slitwidth=self.slitwidth,  # ADD
        verbose=self.verbose
    )
```

### 4. Updated notebook DECON_PARAMS

```python
DECON_PARAMS = {
    'xy_vox': 377,
    'z_vox': 1500,
    'iterations': 25,
    'mic_NA': 0.75,
    'tissue_RI': 1.44,
    'damping': 0,
    'stop_criterion': 5.0,
    'device': 'auto',
    'hist_clip': 0.01,      # ADD - histogram clipping percentage
    'slit_aper': 6.5,       # ADD - slit aperture width (mm)
    'f_cyl': 1,             # ADD - cylinder lens focal length (mm)
}
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Ignoring fcyl/slitwidth as "metadata only" | These aren't metadata - they define the PSF shape | Check MATLAB reference code before dismissing parameters |
| Using same NA for both excitation and emission | Lightsheet has separate illumination NA | Lightsheet optics are fundamentally different from widefield |
| Using same coordinate system for both PSFs | Lightsheet illuminates perpendicular to detection | The coordinate swap (z,0,x) is essential |

## Key Parameters

| Parameter | Typical Value | Description |
|-----------|---------------|-------------|
| `fcyl` | 1 mm | Cylinder lens focal length |
| `slitwidth` | 6.5 mm | Slit aperture width |
| `NA_ls` | ~0.956 | Calculated: `sin(atan(slitwidth / (2 * fcyl)))` |
| `hist_clip` | 0.01% | Histogram clipping for output normalization |

## Diagnostic Signs

**Symptom: Horizontal banding artifacts after deconvolution**

1. Check if `fcyl` and `slitwidth` are being passed to PSF generation
2. Check if PSF uses coordinate swap for excitation component
3. Compare PSF shape - lightsheet PSF should be anisotropic (narrower in lightsheet direction)

## Key Insights

- **MATLAB is the reference** - When Python produces artifacts MATLAB doesn't, compare implementations line-by-line
- **"Metadata" parameters may be functional** - Just because a parameter isn't in the main algorithm doesn't mean it's unused
- **PSF shape determines deconvolution quality** - Wrong PSF = wrong deconvolution = artifacts
- **Coordinate swaps are not typos** - In optics code, coordinate manipulations usually have physical meaning

## References

- MATLAB LsDeconv.m (lines 560, 652-654): Original lightsheet deconvolution implementation
- `notebooks/Kdecon/psf.py`: Python PSF calculation
- `notebooks/Kdecon/main.py`: Python deconvolution interface
- Commit `37d1693`: fix(decon): implement true lightsheet PSF matching MATLAB LsDeconv
