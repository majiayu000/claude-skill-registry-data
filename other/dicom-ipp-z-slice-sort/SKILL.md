---
name: cv-dicom-ipp-z-slice-sort
description: Order DICOM slices into a coherent 3D volume by sorting on ImagePositionPatient[2] (the Z coordinate in patient space), with a filename-integer fallback for series whose tag is missing — never trust filename alphabetical order, never trust InstanceNumber
---

## Overview

DICOM filenames in a CT series are not guaranteed to be in anatomical order. Different scanners, anonymizers, and export tools produce wildly inconsistent name schemes — `1.dcm` may be the topmost slice on one study and the bottommost on the next. `InstanceNumber` is also unreliable: it can be reset, missing, or assigned in scan order rather than spatial order. The single trustworthy ordering is `ImagePositionPatient[2]`, the Z coordinate of the slice in patient space — sort by it ascending and you get a consistent head→feet (or feet→head, fix later) volume regardless of vendor. Keep an integer-filename fallback for the few exports that strip the tag entirely.

## Quick Start

```python
import pydicom
from os import listdir

def load_scans(dcm_dir):
    files = listdir(dcm_dir)
    try:
        slices = [pydicom.dcmread(f'{dcm_dir}/{f}') for f in files]
        slices.sort(key=lambda s: float(s.ImagePositionPatient[2]))
    except (AttributeError, KeyError):
        # fallback: integer-filename order when IPP tag is missing
        nums = sorted(int(f.split('.')[0]) for f in files)
        slices = [pydicom.dcmread(f'{dcm_dir}/{n}.dcm') for n in nums]
    return slices
```

## Workflow

1. List every `.dcm` file in the series directory
2. Read each with `pydicom.dcmread` and key the sort on `float(ds.ImagePositionPatient[2])`
3. Wrap in `try/except (AttributeError, KeyError)` to catch the rare missing-tag series
4. In the fallback branch, sort by the integer extracted from the filename stem
5. Stack `pixel_array`s in the resulting order and apply RescaleSlope/Intercept to get HU

## Key Decisions

- **`ImagePositionPatient[2]`, not `[0]` or `[1]`**: index 2 is the through-plane axis (Z) for axial CT; the other indices are in-plane translation and are constant across slices.
- **Sort ascending, flip later**: produces deterministic ordering; canonical head→feet flip can be done as a separate step (see `cv-ct-z-stack-orientation-flip`).
- **Integer-filename fallback, not lexicographic**: `'10.dcm'` sorts before `'2.dcm'` lexicographically; integer parsing fixes it.
- **`float()` cast required**: pydicom returns the position as `DSfloat` which is a string-ish type and won't compare correctly without the cast.
- **Keep the slice objects together with the position**: don't reorder a separate position array independently of the pixel arrays — index drift bugs are silent and brutal.

## References

- [Pulmonary Dicom Preprocessing](https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection)
