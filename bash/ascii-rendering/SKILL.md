---
name: ascii-rendering
description: "ASCII Art Renderer — Convert images, videos, or canvas content into high-quality ASCII art using shape-vector matching. Unlike naive lightness-based approaches that treat characters as pixels, this renderer quantifies the geometric shape of each ASCII character via 6D shape vectors (sampling circles across 3x2 grid regions), then picks the character whose shape best matches each cell. Produces sharp edges and crisp contours. Use when the user wants to convert an image to ASCII art, render a canvas/scene as ASCII, generate ASCII art from an image file, or build an ASCII rendering pipeline. Triggers on 'ascii art', 'ascii render', 'image to ascii', 'text art', 'convert to ascii', 'ascii animation'."
---

# ASCII Art Renderer

High-quality image-to-ASCII conversion using shape-vector matching. Based on the technique described by Alex Harri: instead of treating ASCII characters as pixels (which produces blurry edges), this approach quantifies the *shape* of each character and picks the best geometric match for each grid cell.

**Source:** https://alexharri.com/blog/ascii-rendering

## Core Concept

Traditional ASCII renderers map each grid cell to a single lightness value, then pick a character by density. This is equivalent to nearest-neighbor downsampling — it produces jaggies and blurry edges.

The shape-vector approach works differently:

1. **Precompute shape vectors** for all 95 printable ASCII characters by measuring how much each character overlaps 6 sampling regions (circles arranged in a 3-row x 2-column staggered grid within each cell)
2. **For each cell** in the output grid, sample the source image at the same 6 regions to produce a 6D sampling vector
3. **Find the nearest character** whose shape vector is closest (Euclidean distance) to the sampling vector

This yields characters that follow contours and edges, not just match brightness.

## Scripts

```bash
# Convert an image to ASCII art
python3 <skill-path>/scripts/ascii_render.py <image_path> [--cols 80] [--charset full] [--contrast 0.5] [--output out.txt] [--color]

# Render a live camera feed as ASCII (requires webcam)
python3 <skill-path>/scripts/ascii_render.py --camera [--cols 120] [--fps 15]

# Convert a video to ASCII
python3 <skill-path>/scripts/ascii_render.py <video_path> [--cols 100] [--fps 10] [--output out.txt]
```

### Arguments

| Flag | Effect |
|------|--------|
| `image_path` | Path to input image, video, or `--camera` for webcam |
| `--cols N` | Number of character columns (default: 80) |
| `--charset MODE` | `full` (all 95 printable ASCII), `simple` (subset: ` .:-=+*#%@`), or `blocks` (block elements) |
| `--contrast F` | Edge contrast enhancement strength, 0.0-1.0 (default: 0.3) |
| `--invert` | Invert lightness (for light-on-dark terminals) |
| `--output PATH` | Write output to file instead of stdout |
| `--color` | Enable ANSI color output (256-color) |
| `--camera` | Use webcam as input |
| `--fps N` | Target FPS for video/camera mode (default: 15) |
| `--font-aspect F` | Character aspect ratio height/width (default: 2.0) |

## Algorithm Details

### Step 1: Precompute Character Shape Vectors

For each of the 95 printable ASCII characters:

1. Render the character into a small bitmap using a monospace font
2. Define 6 sampling circles in a 3-row x 2-column staggered layout within the cell:
   - Left circles are shifted slightly down, right circles slightly up
   - Circles overlap slightly to minimize gaps
3. For each sampling circle, compute the fraction of pixels within the circle that overlap the character glyph
4. This produces a 6D vector per character: `[top-left, top-right, mid-left, mid-right, bot-left, bot-right]`
5. Normalize all vectors: for each dimension, divide by the maximum value across all characters

```python
# Pseudocode for shape vector computation
def compute_shape_vector(char_bitmap, sampling_circles):
    vector = []
    for circle in sampling_circles:
        samples_in_circle = get_pixels_in_circle(char_bitmap, circle)
        overlap = sum(samples_in_circle) / len(samples_in_circle)
        vector.append(overlap)
    return vector

# Normalize across all characters
max_per_dim = [max(v[i] for v in all_vectors) for i in range(6)]
normalized = [[v[i] / max_per_dim[i] for i in range(6)] for v in all_vectors]
```

### Step 2: Sample the Source Image

For each cell in the ASCII grid:

1. Map the cell's position back to the source image coordinates
2. For each of the 6 sampling circles, sample multiple pixels within the circle region of the source image
3. Convert RGB samples to lightness: `L = 0.2126*R + 0.7152*G + 0.0722*B` (relative luminance)
4. Average the lightness samples within each circle to get a 6D sampling vector

### Step 3: Contrast Enhancement (Optional)

To sharpen edges between regions of different lightness (critical for 3D scenes):

1. Compute the mean lightness across all 6 components of the sampling vector
2. For each component, push it away from the mean: `enhanced[i] = mean + (v[i] - mean) * (1 + contrast_strength)`
3. Clamp values to [0, 1]

```python
def enhance_contrast(sampling_vector, strength=0.3):
    mean = sum(sampling_vector) / len(sampling_vector)
    enhanced = []
    for v in sampling_vector:
        diff = v - mean
        new_v = mean + diff * (1 + strength)
        enhanced.append(max(0.0, min(1.0, new_v)))
    return enhanced
```

This makes boundaries between differently-lit surfaces appear sharper in the ASCII output.

### Step 4: Find Best Character

For each cell's (possibly contrast-enhanced) sampling vector, find the character with the closest shape vector using squared Euclidean distance:

```python
def find_best_character(sampling_vector, characters):
    best_char = ' '
    best_dist = float('inf')
    for char, shape_vector in characters:
        dist = sum((a - b) ** 2 for a, b in zip(sampling_vector, shape_vector))
        if dist < best_dist:
            best_dist = dist
            best_char = char
    return best_char
```

### Performance: KD-Tree Acceleration

Brute-force nearest-neighbor search over 95 characters x thousands of cells is slow for real-time rendering. Use a KD-tree (from scipy or a simple implementation) to accelerate lookups from O(95) to O(log 95) per cell.

## Workflow

### Converting a single image

1. User provides an image path
2. Run `ascii_render.py <path> --cols 80`
3. Display the result or save to file
4. Adjust `--contrast` and `--cols` based on user preference

### Building ASCII rendering into a project

When the user wants to integrate ASCII rendering into their own code, guide them through the algorithm:

1. **Font rasterization**: Use Pillow (Python) or Canvas API (JS/TS) to render each ASCII character into a bitmap
2. **Sampling circle layout**: 6 circles in a 3x2 staggered grid, sized to ~60% of cell width as radius
3. **Shape vector precomputation**: Run once at startup, cache the normalized 6D vectors
4. **Per-frame rendering**: For each cell, sample source → build 6D vector → optional contrast enhance → nearest-neighbor lookup
5. **Output**: Compose the character grid into a string

### TypeScript/JavaScript implementation skeleton

```typescript
interface CharacterEntry {
  character: string;
  shapeVector: number[]; // 6D normalized
}

// Precomputed at startup
const CHARACTERS: CharacterEntry[] = precomputeShapeVectors();

function getDistance(a: number[], b: number[]): number {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    sum += (a[i] - b[i]) ** 2;
  }
  return sum; // skip sqrt — only used for comparison
}

function findBestCharacter(samplingVector: number[]): string {
  let bestChar = ' ';
  let bestDist = Infinity;
  for (const { character, shapeVector } of CHARACTERS) {
    const dist = getDistance(shapeVector, samplingVector);
    if (dist < bestDist) {
      bestDist = dist;
      bestChar = character;
    }
  }
  return bestChar;
}

function renderAscii(imageData: ImageData, cols: number, fontAspect: number): string {
  const cellW = imageData.width / cols;
  const cellH = cellW * fontAspect;
  const rows = Math.floor(imageData.height / cellH);
  
  let result = '';
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const samplingVector = sampleCell(imageData, col * cellW, row * cellH, cellW, cellH);
      const enhanced = enhanceContrast(samplingVector, 0.3);
      result += findBestCharacter(enhanced);
    }
    result += '\n';
  }
  return result;
}
```

## Key Concepts Reference

| Concept | Description |
|---------|-------------|
| **Shape vector** | 6D vector quantifying which regions of a cell a character visually occupies |
| **Sampling circles** | 6 circular regions in a 3x2 staggered grid used to measure local density |
| **Normalization** | Dividing each dimension by its max across all characters so vectors span [0,1] |
| **Contrast enhancement** | Pushing sampling vector components away from their mean to sharpen edges |
| **Nearest-neighbor search** | Finding the character whose shape vector has minimum Euclidean distance to the sampling vector |
| **Relative luminance** | `L = 0.2126R + 0.7152G + 0.0722B` — perceptually correct lightness from RGB |
| **Font aspect ratio** | Monospace characters are taller than wide (typically ~2:1), cells must reflect this |

## Prerequisites

- Python 3.9+
- Pillow (for font rasterization and image loading)
- NumPy (for vectorized operations)
- Optional: OpenCV (`opencv-python`) for video/camera input
- Optional: SciPy (for KD-tree acceleration)
