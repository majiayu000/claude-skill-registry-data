---
name: Implement Dynamic Dilation
description: Create interactive dilation animations using p5.js where students explore dilations with adjustable scale factors.
---

# Implement Dynamic Dilation

Use this skill when creating animations where students:
- Explore dilations centered at a point with interactive scale factors
- Understand how scale factors affect shape size and position
- Compare original and dilated figures
- Visualize dilation rays from center to vertices

## When to Use This Pattern

**Perfect for:**
- "Show the dilation of polygon ABCD centered at point O with scale factor 2"
- Interactive exploration of scale factors (including fractions)
- Comparing original and dilated figures
- Understanding similarity through transformations
- Showing dilation rays and transformation paths

**Not suitable for:**
- Static dilation diagrams (use basic p5 animation)
- Rotations or reflections (different transformation types)
- Non-rigid transformations

## Technology Stack

**Uses p5.js** for the interactive coordinate plane because:
- Real-time interactive slider control
- Dynamic rendering of dilated shapes
- Built-in animation and mouse/keyboard handling
- Easy geometric calculations

## Configuration Options

### Basic Configuration (from dilation.ts)

```javascript
// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Polygon vertices (any shape)
let points = [
  { x: 10, y: 10, label: 'P' },
  { x: 8, y: 8, label: 'Q' },
  { x: 12, y: 6, label: 'R' },
  { x: 14, y: 8, label: 'S' }
];

// Center of dilation
let center = { x: 10, y: 8, label: 'O' };

// Scale factors available
let scaleFactors = [
  { value: 1/3, label: '1/3' },
  { value: 1/2, label: '1/2' },
  { value: 1, label: '1' },
  { value: 2, label: '2' },
  { value: 3, label: '3' },
  { value: 4, label: '4' }
];

// Current scale factor index
let scaleIndex = 3; // Start at scale factor 2

// Toggle for showing dilation rays
let showRays = true;

// Toggle for showing grid and axes
let showGrid = true;

// Axis ranges
let xMin = 0, xMax = 20;
let yMin = 0, yMax = 15;

// Colors
let originalColor = [59, 130, 246]; // Blue
let dilatedColor = [239, 68, 68];   // Red
let gridColor = 220;
let axisColor = 100;
```

## Features

### Interactive Controls

1. **Slider Control**: Click/drag slider to change scale factor
2. **Keyboard Controls**:
   - Arrow keys (left/right) to adjust scale factor
   - **R** to reset to scale factor 1
   - **D** to toggle dilation rays on/off
   - **G** to toggle grid and axes on/off

### Visual Elements

- **Coordinate grid** with customizable axis ranges
- **Original polygon** (blue) with vertex labels
- **Dilated polygon** (red) with primed labels (e.g., P')
- **Dilation rays** (black dotted lines) extending from center through vertices
- **Center point** marked with a black dot and label
- **Interactive slider** with scale factor indicators
- **Legend** showing original, dilated, and center
- **Toggle status** showing current state of rays and grid

## Core Functions

### Coordinate Transformation

```javascript
function coordToPixel(x, y, plotWidth, plotHeight) {
  let px = padding.left + ((x - xMin) / (xMax - xMin)) * plotWidth;
  let py = padding.top + ((yMax - y) / (yMax - yMin)) * plotHeight;
  return { x: px, y: py };
}
```

### Dilation Calculation

```javascript
// Calculate dilated points
let dilatedPoints = points.map(p => ({
  x: center.x + (p.x - center.x) * scaleFactor,
  y: center.y + (p.y - center.y) * scaleFactor,
  label: p.label + "'"
}));
```

### Drawing Dilation Rays

```javascript
// Draw dilation rays (from center, extending outward)
if (showRays) {
  stroke(0);
  strokeWeight(2);
  drawingContext.setLineDash([4, 4]);
  for (let i = 0; i < points.length; i++) {
    let centerPixelPos = coordToPixel(center.x, center.y, plotWidth, plotHeight);
    let pointPixel = coordToPixel(points[i].x, points[i].y, plotWidth, plotHeight);

    // Calculate direction vector
    let dx = pointPixel.x - centerPixelPos.x;
    let dy = pointPixel.y - centerPixelPos.y;

    // Ray starts at center and extends far in the direction of the point
    let scale = 1000;
    let x2 = centerPixelPos.x + dx * scale;
    let y2 = centerPixelPos.y + dy * scale;

    line(centerPixelPos.x, centerPixelPos.y, x2, y2);
  }
  drawingContext.setLineDash([]);
}
```

## Common Patterns

### Pattern 1: Simple Quadrilateral Dilation

```javascript
let points = [
  { x: 2, y: 2, label: 'A' },
  { x: 4, y: 2, label: 'B' },
  { x: 4, y: 4, label: 'C' },
  { x: 2, y: 4, label: 'D' }
];

let center = { x: 0, y: 0, label: 'O' };

let scaleFactors = [
  { value: 1/2, label: '1/2' },
  { value: 1, label: '1' },
  { value: 2, label: '2' },
  { value: 3, label: '3' }
];
```

### Pattern 2: Triangle Dilation (Center at Vertex)

```javascript
let points = [
  { x: 2, y: 8, label: 'A' },
  { x: 2, y: 4, label: 'B' },
  { x: 6, y: 4, label: 'C' }
];

let center = { x: 6, y: 4, label: 'C' };  // Center at vertex C

let scaleFactors = [
  { value: 1/2, label: '1/2' },
  { value: 1, label: '1' },
  { value: 2, label: '2' },
  { value: 3, label: '3' }
];
```

### Pattern 3: Dilation with Negative Coordinates

```javascript
let points = [
  { x: 0, y: 0, label: 'A' },
  { x: 2, y: 2, label: 'B' },
  { x: 6, y: 1, label: 'C' },
  { x: 4, y: -1, label: 'D' }
];

let center = { x: 4, y: -1, label: 'O' };

// Adjust axis ranges to accommodate negative values
let xMin = -5, xMax = 25;
let yMin = -10, yMax = 15;
```

## Customization Points

### 1. Polygon Shape
Modify the `points` array to create any polygon. Points should be in order to form a closed shape.

### 2. Center of Dilation
Set `center` to any point. Common choices:
- Origin (0, 0)
- One of the polygon vertices
- A point inside the polygon
- A point outside the polygon

### 3. Scale Factors
Customize the `scaleFactors` array with any positive values:
- Fractions (e.g., 1/3, 1/2) for reductions
- Whole numbers (e.g., 2, 3, 4) for enlargements
- Include 1 to show the original shape

### 4. Axis Ranges
Adjust `xMin`, `xMax`, `yMin`, `yMax` to fit your shape and dilations.

### 5. Colors
Customize colors for:
- `originalColor`: Color of the original polygon
- `dilatedColor`: Color of the dilated polygon
- `gridColor`: Color of grid lines
- `axisColor`: Color of coordinate axes

### 6. Default States
- `scaleIndex`: Starting scale factor (index in scaleFactors array)
- `showRays`: Whether to show dilation rays by default
- `showGrid`: Whether to show grid by default

## Implementation Checklist

- [ ] Copied base dilation animation code
- [ ] Updated `points` array for target polygon
- [ ] Set `center` coordinates and label
- [ ] Configured `scaleFactors` array
- [ ] Adjusted axis ranges (`xMin`, `xMax`, `yMin`, `yMax`)
- [ ] Customized colors if needed
- [ ] Set appropriate default scale factor index
- [ ] Tested slider interaction
- [ ] Tested keyboard controls (arrows, R, D, G)
- [ ] Verified dilation rays extend correctly
- [ ] Verified polygon labels (original and dilated)
- [ ] Checked that dilations calculate correctly
- [ ] Tested grid toggle
- [ ] Tested rays toggle

## Tips

1. **Vertex Order**: List points in order (clockwise or counter-clockwise) for proper polygon rendering
2. **Axis Range**: Ensure axis ranges accommodate both original and largest dilated figure
3. **Center Choice**: Different centers create different visual effects - experiment!
4. **Scale Factor 1**: Always include scale factor 1 to show original/dilated overlap
5. **Labels**: Use single letters (A, B, C...) for clean vertex labels
6. **Grid Spacing**: Adjust grid scale if coordinates are very large or very small
7. **Ray Visibility**: Rays help visualize the transformation direction
8. **Color Contrast**: Use contrasting colors for original vs dilated polygons

## Limitations & Notes

- **Canvas Size**: Always use 600x600 as specified in p5-format.md
- **Positive Scale Factors Only**: No negative scale factors (would flip the figure)
- **No Animation**: Scale changes are instant, not animated
- **Simple Polygons**: Works best with convex polygons, may have visual issues with complex self-intersecting shapes

## Educational Applications

- **Understanding Scale Factors**:
  - Scale factor > 1 → enlargement
  - Scale factor < 1 → reduction
  - Scale factor = 1 → same size

- **Similarity**: Dilations preserve shape (angles) but change size (side lengths)

- **Center Effects**: Explore how center location affects the dilated figure's position

- **Coordinate Relationships**: See how each coordinate changes based on center and scale factor

## Related Animation Types

- [implement-dynamic-graph-question](../implement-dynamic-graph-question/SKILL.md) - For coordinate plane line drawing
- Other geometry animations (rotations, reflections) - To be added

## File Location

Base implementation: [src/app/animations/examples/geometry/dilation.ts](../../../../src/app/animations/examples/geometry/dilation.ts)

## Example Usage in create-p5-animation Skill

When asked to create a dilation animation:

1. Use this animation-type as the scaffold
2. Modify the configuration section for the specific problem
3. Keep all the core functionality (slider, toggles, rendering)
4. Adjust only the configurable parameters
