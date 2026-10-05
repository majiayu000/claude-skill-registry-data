---
name: smart-image-slicer
description: This skill should be used when users need to automatically detect, separate, and extract multiple objects from a single image, particularly for game sprite sheets, character animations, UI elements, or any image containing multiple distinct objects that need to be isolated with transparent backgrounds.
---

# Smart Image Slicer

Automatically detect and separate multiple objects from images using computer vision techniques, with intelligent background removal and transparent PNG output.

## When to Use This Skill

Use this skill when users request:
- Separating sprite sheets into individual sprites
- Extracting character animation frames from sequence images
- Isolating UI elements from design mockups
- Converting hand-drawn sketches into individual digital assets
- Batch processing images with multiple objects
- Any task involving "cutting out", "separating", or "extracting" objects from images

## Key Capabilities

### Intelligent Object Detection
- Uses OpenCV contour detection to identify separate objects
- Filters out noise and small artifacts automatically
- Handles complex shapes and irregular boundaries

### Smart Background Removal
- Analyzes local background colors for each object
- Supports gradient and non-uniform backgrounds
- Generates transparent PNG outputs
- Preserves object details while removing backgrounds

### Configurable Processing
- Adjustable area thresholds to filter noise
- Tolerance settings for background removal precision
- Customizable detection sensitivity
- Preset configurations for common use cases

## How to Use This Skill

### 1. Execute the Smart Slice Script

The core functionality is provided by `scripts/smart_slice.py`. Use it directly:

```bash
python3 scripts/smart_slice.py input_image.png
```

### 2. Parameter Optimization

For best results, adjust parameters based on image characteristics:

**Basic Usage:**
```bash
python3 scripts/smart_slice.py input.png -o output_folder
```

**With Custom Parameters:**
```bash
python3 scripts/smart_slice.py input.png -m 800 -t 45 -b 235
```

**Parameter Guidelines:**
- `-m, --min-area`: Minimum object size (default: 500)
  - Increase for images with many small noise elements
  - Decrease to capture smaller objects
- `-t, --tolerance`: Background removal sensitivity (default: 40)
  - Increase for gradient/uneven backgrounds
  - Decrease for high-contrast, uniform backgrounds
- `-b, --bg-threshold`: Background detection threshold (default: 240)
  - Decrease for darker backgrounds
  - Increase for pure white backgrounds

### 3. Use Configuration Presets

Reference `assets/config_presets.json` for optimized settings:

- **game_sprites**: For game character sprites and icons
- **character_animations**: For animation frame sequences
- **ui_elements**: For interface components and buttons
- **hand_drawn**: For scanned sketches and artwork
- **high_precision**: For detailed, precision-required images

### 4. Troubleshooting Common Issues

Consult `references/usage_guide.md` for detailed troubleshooting:

- **Too many fragments**: Increase min_area parameter
- **Missing objects**: Decrease bg_threshold and min_area
- **Poor background removal**: Adjust tolerance parameter
- **Over-removal of object parts**: Decrease tolerance parameter

## Workflow Integration

### For Game Development
1. Process sprite sheets to extract individual character frames
2. Use extracted sprites directly in game engines
3. Maintain transparent backgrounds for proper layering

### For UI Design
1. Extract individual elements from design mockups
2. Create reusable component libraries
3. Generate assets for different screen densities

### For Digital Art
1. Convert hand-drawn sketches to digital assets
2. Separate complex illustrations into layers
3. Create animation-ready sprite sequences

## Technical Requirements

Ensure the following dependencies are installed:
```bash
pip install opencv-python pillow numpy
```

The skill works with:
- Python 3.6+
- Common image formats (PNG, JPG, BMP)
- Images of any resolution (1000x1000+ recommended)

## Output Format

- Files saved as `sprite_000.png`, `sprite_001.png`, etc.
- Transparent PNG format preserving alpha channel
- Original object dimensions maintained
- Organized in specified output directory

## Best Practices

### Input Image Preparation
- Use solid, preferably white backgrounds for best results
- Ensure good contrast between objects and background
- Higher resolution images generally produce better results

### Parameter Tuning Strategy
1. Start with default parameters
2. Analyze initial results
3. Adjust parameters based on specific image characteristics
4. Use preset configurations for similar image types

### Quality Assurance
- Review extracted objects for completeness
- Check transparency edges for artifacts
- Verify all intended objects were detected
- Manually adjust parameters if needed for optimal results