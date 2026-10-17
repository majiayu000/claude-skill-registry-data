---
name: forzadesigner6-vinyl-converter
description: Convert images into Forza Horizon vinyl groups and Assetto Corsa liveries using ForzaDesigner6
triggers:
  - convert image to forza vinyl
  - create forza horizon livery
  - generate vinyl group for forza
  - inject vinyl into forza horizon
  - export assetto corsa livery
  - use forzadesigner6
  - forza designer vinyl conversion
  - automate forza vinyl creation
---

# ForzaDesigner6 Vinyl Converter

> Skill by [ara.so](https://ara.so) — Design Skills collection

## Overview

ForzaDesigner6 (FD6) is a Python-based tool that converts any image (JPEG/PNG) into:
- **Vinyl groups** for Forza Horizon 3, 4, 5, and 6 via live memory injection
- **Liveries** for Assetto Corsa Competizione via file export

The tool uses geometric shape approximation algorithms to reconstruct images using in-game primitives (spheres for Forza, texture sheets for ACC), then either injects the shape data directly into the running game's memory or writes livery files to disk.

## Installation

### Pre-built Binary (Windows 10/11 x64)

```powershell
# Download FD6.exe from releases
# https://github.com/tokyubevoxelverse/ForzaDesigner6/releases

# Run directly - no installation required
.\FD6.exe
```

### From Source

```powershell
git clone https://github.com/tokyubevoxelverse/ForzaDesigner6.git
cd ForzaDesigner6

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run from source
python -m fd6

# Build executable
.\build_exe.bat  # outputs to dist/FD6.exe
```

**Requirements:**
- Python 3.10+
- Microsoft Visual C++ Redistributable (usually pre-installed)
- Windows 10/11 x64

## Core Workflow

### 1. Generate Vinyl JSON from Image

```python
# Typical programmatic usage (if building on FD6 as a library)
from fd6.generator import VinylGenerator
from fd6.profiles import Profile

# Initialize generator
generator = VinylGenerator()

# Load image and configure
image_path = "my_logo.png"
profile = Profile.BALANCED  # or FAST, QUALITY, ULTRA
max_shapes = 1500  # Must match in-game template size

# Generate vinyl JSON
vinyl_data = generator.generate(
    image_path=image_path,
    profile=profile,
    max_shapes=max_shapes,
    output_json="my_logo.json"
)
```

### 2. Prepare In-Game Template (Forza)

**Critical:** Before injection, create sphere templates in-game:

1. Open Forza Horizon (3/4/5/6)
2. Go to Vinyl Editor → Create New Group
3. Add exactly N spheres (1500 or 3000 recommended)
4. Save as template (e.g., "Template_1500_Spheres")
5. Load this template before each injection

### 3. Inject Vinyl into Forza

```python
# Memory injection workflow
from fd6.inject import ForzaInjector
from fd6.inject.game_profiles import GameTarget

# Initialize injector
injector = ForzaInjector()

# Select target game
target = GameTarget.FORZA_HORIZON_6  # or FH3, FH4, FH5

# Inject vinyl data
result = injector.inject(
    json_path="my_logo.json",
    target=target,
    validate=True  # Strict 5/5 + 95% validation
)

if result.success:
    print(f"✅ Injected {result.shapes_written} shapes")
else:
    print(f"❌ Failed: {result.error_message}")
```

**Injection Process:**
1. Locates the game process in memory
2. Finds the vinyl group via fingerprint (fresh spheres) or RTTI scan (re-injection)
3. Overwrites sphere data (position, scale, color, opacity)
4. Validates write integrity

### 4. Export Assetto Corsa Competizione Livery

```python
# ACC file-based export
from fd6.acc import ACCExporter

# Initialize exporter
exporter = ACCExporter()

# Export livery
livery = exporter.export(
    image_path="racing_stripe.png",
    car_model="porsche_991ii_gt3_r",  # Use ACC car catalog
    livery_name="MyCustomLivery",
    output_dir=None  # Auto-detects Documents/Assetto Corsa Competizione
)

print(f"Livery exported to: {livery.json_path}")
# Creates:
# - Documents/Assetto Corsa Competizione/Customs/Cars/<car>/<livery>.json
# - Documents/Assetto Corsa Competizione/Customs/Liveries/<livery>/decals.png
```

## Configuration

### Profiles

FD6 ships with pre-tuned generation profiles:

| Profile | Shapes/Iteration | Quality | Speed | Use Case |
|---------|------------------|---------|-------|----------|
| `FAST` | Low mutation rate | Low | Fast | Quick previews |
| `BALANCED` | Medium mutation | Medium | Medium | **Recommended default** |
| `QUALITY` | High mutation | High | Slow | Detailed logos |
| `ULTRA` | Maximum iterations | Very High | Very Slow | Professional work |

```python
from fd6.profiles import Profile

# Access profile settings
profile = Profile.BALANCED
print(profile.max_iterations)  # 5000
print(profile.mutation_rate)   # 0.5
print(profile.alpha_threshold) # 128
```

### Game-Specific Struct Offsets

FD6 maintains per-game memory layouts in `fd6/inject/game_profiles.py`:

```python
# Example: Forza Horizon 6 struct offsets
FH6_PROFILE = {
    "struct_size": 0x48,  # CLiveryGroup size
    "offsets": {
        "position_x": 0x00,
        "position_y": 0x04,
        "scale_x": 0x08,
        "scale_y": 0x0C,
        "rotation": 0x10,
        "color_r": 0x14,
        "color_g": 0x15,
        "color_b": 0x16,
        "opacity": 0x17,
        "shape_type": 0x18,
    },
    "rtti_class": ".?AVCLiveryGroup@@",
}
```

**When game patches break injection:** Update these offsets by reverse-engineering the new build.

## CLI Usage (GUI Wrapper)

While FD6 is primarily GUI-based, you can script the underlying modules:

```python
# Automated batch conversion script
import os
from pathlib import Path
from fd6.generator import VinylGenerator
from fd6.profiles import Profile

def batch_convert(image_dir: str, output_dir: str, max_shapes: int = 1500):
    """Convert all images in directory to vinyl JSON"""
    generator = VinylGenerator()
    
    for img_path in Path(image_dir).glob("*.png"):
        output_json = Path(output_dir) / f"{img_path.stem}.json"
        
        print(f"Converting {img_path.name}...")
        generator.generate(
            image_path=str(img_path),
            profile=Profile.BALANCED,
            max_shapes=max_shapes,
            output_json=str(output_json)
        )
        print(f"✅ Saved to {output_json}")

# Usage
batch_convert("./logos", "./vinyls", max_shapes=1500)
```

## Common Patterns

### Pattern: Progressive Shape Count Testing

Start small, scale up to avoid long re-injection scans:

```python
from fd6.generator import VinylGenerator
from fd6.inject import ForzaInjector

generator = VinylGenerator()
injector = ForzaInjector()

# Test with low shape count first
for shape_count in [500, 1000, 1500, 3000]:
    vinyl_json = f"test_{shape_count}.json"
    
    generator.generate(
        image_path="complex_logo.png",
        max_shapes=shape_count,
        output_json=vinyl_json
    )
    
    # Load matching template in-game before this step
    input(f"Load {shape_count}-sphere template, then press Enter...")
    
    result = injector.inject(vinyl_json, target="FH6")
    if result.success:
        print(f"✅ {shape_count} shapes: Success")
    else:
        print(f"❌ {shape_count} shapes: {result.error_message}")
```

### Pattern: Re-injection on Painted Template

```python
# First injection uses fingerprint (fast)
injector.inject("design_v1.json", target="FH6")  # ~10s

# Subsequent re-injections fall back to RTTI scan (slower first time)
injector.inject("design_v2.json", target="FH6")  # ~2-5 min first scan
injector.inject("design_v3.json", target="FH6")  # ~10s (cached)
```

### Pattern: ACC Multi-Car Export

```python
from fd6.acc import ACCExporter

exporter = ACCExporter()
cars = [
    "porsche_991ii_gt3_r",
    "ferrari_488_gt3",
    "lamborghini_huracan_gt3",
]

for car in cars:
    exporter.export(
        image_path="team_logo.png",
        car_model=car,
        livery_name=f"TeamLivery_{car}",
    )
```

## Troubleshooting

### Error: "No confident match found"

**Cause:** Vinyl editor not open, or template has fewer spheres than JSON requires.

```python
# Verify shape count before injection
import json

with open("design.json") as f:
    data = json.load(f)
    required_shapes = len(data["shapes"])
    print(f"This design needs {required_shapes} spheres in-game")

# Ensure in-game template matches or exceeds this count
```

### Error: "RTTI scan stalled"

**Cause:** RTTI fallback can take 2-5 minutes on large games (FH6 ~120GB).

```python
# Add timeout and progress callback
result = injector.inject(
    "design.json",
    target="FH6",
    timeout=600,  # 10-minute timeout
    progress_callback=lambda pct: print(f"Scan: {pct}%")
)
```

### Error: "Shapes offset or wrong scale"

**Cause:** Game struct offsets changed after patch.

```python
# Diagnostic: dump detected memory layout
from fd6.inject.diagnostics import dump_vinyl_group

dump_vinyl_group(
    process_name="ForzaHorizon6.exe",
    output_file="struct_dump.txt"
)

# Compare output against known-good offsets in game_profiles.py
# Update offsets if mismatched
```

### Warning: "Windows SmartScreen blocked FD6.exe"

**Solution:**
1. Click "More info"
2. Click "Run anyway"
3. Or build from source to avoid code-signing warnings

### Issue: Injection fails silently

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

from fd6.inject import ForzaInjector
injector = ForzaInjector(debug=True)
result = injector.inject("design.json", target="FH6")

# Check detailed error log
print(result.debug_log)
```

## Safety & Risk Warnings

**Memory injection modifies running game processes.** This may violate:
- Microsoft Services Agreement
- Xbox Community Standards
- Forza titles' Terms of Use

**Potential consequences:**
- Temporary or permanent account suspension
- Loss of online access, achievements, or purchased content

**ACC file export does NOT involve memory modification** and carries no ban risk.

**Mitigation:**
- Never run FD6 as administrator
- Don't click anything during injection
- Only inject into offline/non-competitive sessions
- Accept all risks before use

## Advanced: Custom Shape Algorithms

FD6's generation engine can be extended with custom shape primitives:

```python
from fd6.shapes import ShapeBase, ShapeType

class CustomTriangle(ShapeBase):
    shape_type = ShapeType.TRIANGLE
    
    def to_forza_bytes(self) -> bytes:
        """Convert to Forza CLiveryGroup struct bytes"""
        return struct.pack(
            "<ffHHHBBBB",
            self.x,          # Position X (float)
            -self.y,         # Position Y (float, negated)
            int(self.w / 63), # Scale X (uint16, div 63)
            int(self.h / 127), # Scale Y (uint16, div 127)
            self.rotation,    # Rotation (uint16)
            self.color[0],   # R (uint8)
            self.color[1],   # G (uint8)
            self.color[2],   # B (uint8)
            self.opacity,    # Alpha (uint8)
        )

# Register custom shape
from fd6.generator import VinylGenerator
generator = VinylGenerator(custom_shapes=[CustomTriangle])
```

## Testing

```powershell
# Run test suite
pytest

# Test specific module
pytest tests/test_generator.py

# Test injection (requires game running)
pytest tests/test_inject.py --game=FH6

# Benchmark generation performance
python -m fd6.benchmark --image test.png --shapes 3000
```

## Project Structure

```
ForzaDesigner6/
├── fd6/
│   ├── generator.py       # Image → vinyl JSON conversion
│   ├── inject/
│   │   ├── injector.py    # Memory injection engine
│   │   ├── game_profiles.py # Per-game struct offsets
│   │   └── rtti_locator.py  # RTTI vtable scanner
│   ├── acc/
│   │   └── exporter.py    # ACC livery file writer
│   ├── shapes.py          # Shape primitives
│   └── profiles.py        # Generation profiles
├── tools/
│   └── SplashScreen.gif
├── requirements.txt
├── build_exe.bat
└── README.md
```

## References

- **Forza vinyl-group struct layout:** Reverse-engineered from FH6 build 354.221, cross-validated with bvzrays' [forza-painter-fh6](https://github.com/bvzrays/forza-painter-fh6)
- **RTTI locator:** Searches for `.?AVCLiveryGroup@@` MSVC type descriptor
- **Shape algorithms:** Based on [geometrize-lib](https://github.com/Tw1ddle/geometrize-lib) (MIT) and [Primitive](https://github.com/fogleman/primitive) (MIT)

---

**License:** MIT  
**Repository:** https://github.com/tokyubevoxelverse/ForzaDesigner6  
**Video Tutorial:** https://youtu.be/8LGvE7O9aeg
