---
name: jcamp-dx
description: Use when exchanging spectroscopic data between instruments and software, archiving spectral data, or building spectroscopy databases.
metadata:
    skill-author: MindSpore Science Team
---

## Overview

JCAMP-DX is an IUPAC standard format for exchanging chemical and spectroscopic data. It provides a universal format for IR, NMR, MS, UV-Vis, and other spectroscopic techniques.

## Format Specification

- **Encoding**: ASCII text with labeled data records
- **Structure**: Header + Data sections
- **Compression**: FIX, PAC, SQZ, DIF, DIFDUP methods
- **Line Length**: Max 80 characters per line
- **Comments**: Lines starting with `$$`

## Key LDRs (Labeled Data Records)

| LDR | Description |
|-----|-------------|
| `##TITLE` | Spectrum title |
| `##JCAMP-DX` | Version and data type |
| `##DATA TYPE` | INFRARED, NMR, MASS, etc. |
| `##XUNITS` | X-axis units |
| `##YUNITS` | Y-axis units |
| `##FIRSTX` | First X value |
| `##LASTX` | Last X value |
| `##NPOINTS` | Number of data points |
| `##XYDATA` | Start of data |
| `##END` | End of file |

## Example Snippet

```jcamp
##TITLE=Spectrum of Acetone
##JCAMP-DX=5.01
##DATA TYPE=INFRARED SPECTRUM
##ORIGIN=Lab IR Spectrometer
##XUNITS=1/CM
##YUNITS=ABSORBANCE
##FIRSTX=400.0
##LASTX=4000.0
##NPOINTS=3601
##XYDATA=(X++(Y..Y))
400.0 0.123 0.125 0.127
410.0 0.130 0.128 0.126
##END
```

## Tools

| Tool | Purpose |
|------|---------|
| jcamp (Python) | Python parser |
| JSpecView | Java viewer |
| OpenBabel | Format conversion |
| nmrglue | NMR JCAMP support |
| scipy | Can read JCAMP-DX |

## Resources

- Website: http://www.jcamp-dx.org
- Spec: IUPAC recommendations