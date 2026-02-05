---
name: Implement Algebra Tiles
description: Create interactive algebra tiles manipulatives using p5.js where students drag tiles and see cancellations when opposites overlap.
---

# Implement Algebra Tiles

Use this skill when creating animations where students:
- Drag algebra tiles (x, -x, 1, -1) onto a workspace
- Combine tiles to model algebraic expressions
- See visual cancellation when opposite tiles are placed together
- Explore the zero principle (x + (-x) = 0)

## When to Use This Pattern

**Perfect for:**
- "Model the expression 2x - 3 using algebra tiles"
- Interactive equation solving with manipulatives
- Understanding additive inverses and the zero principle
- Simplifying algebraic expressions visually
- Combining like terms with visual models

**Not suitable for:**
- Multiplication of algebraic expressions (need x² tiles)
- Complex polynomial operations (use specialized tools)
- Static tile diagrams (use basic p5 animation)

## Technology Stack

**Uses p5.js** for the interactive tiles because:
- Real-time drag-and-drop interaction
- Dynamic collision detection for linking
- Mouse and touch event handling
- Smooth visual feedback

## Configuration Options

### Basic Configuration

```javascript
// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Tile types configuration
let tileConfig = {
  x: {
    width: 80,
    height: 60,
    color: [102, 178, 102],      // Green for positive x
    label: 'x',
    value: 'x',
    sign: 'positive'
  },
  negX: {
    width: 80,
    height: 60,
    color: [230, 57, 70],        // Red for negative x
    label: '-x',
    value: 'x',
    sign: 'negative'
  },
  one: {
    width: 50,
    height: 50,
    color: [255, 193, 94],       // Yellow/gold for positive 1
    label: '1',
    value: '1',
    sign: 'positive'
  },
  negOne: {
    width: 50,
    height: 50,
    color: [230, 57, 70],        // Red for negative 1
    label: '-1',
    value: '1',
    sign: 'negative'
  }
};

// Palette layout (where tiles can be dragged from)
let paletteConfig = {
  x: 80,
  y: 100,
  spacing: 100,
  label: 'Drag tiles onto canvas:'
};

// Canvas area (drop zone)
let canvasConfig = {
  x: 50,
  y: 250,
  w: 500,
  h: 300,
  backgroundColor: [245, 245, 245],
  borderColor: [180, 180, 180],
  label: 'Workspace'
};

// Snap & cancellation settings
let cancelConfig = {
  snapDistance: 60,              // How close tiles need to be to snap together
  cancelledColor: [200, 200, 200], // Light grey color for snapped tiles
  snapGap: 2                     // Small gap between snapped tiles
};

// Visual settings
let visualConfig = {
  showInstructions: true,
  highlightOnHover: true,
  showEquation: true
};
```

## Features

### Interactive Controls

1. **Drag Tiles from Palette**
   - Drag x, -x, 1, or -1 from top palette
   - Release on workspace to place
   - Can create unlimited copies
   - Each tile is independent

2. **Move Existing Tiles**
   - Click and drag any placed tile
   - Move to reposition
   - Drag outside workspace to remove
   - Real-time cancellation updates

3. **Automatic Snap & Cancellation**
   - When opposite tiles are dragged close, they snap together
   - x and -x snap and cancel each other
   - 1 and -1 snap and cancel each other
   - Snapped tiles physically move to align side-by-side
   - Both tiles turn light grey when snapped
   - Cancellations update as tiles move

### Visual Elements

- **Palette area** with four tile types (x, -x, 1, -1)
- **Workspace** for placing and arranging tiles
- **Snap indicators** (tiles physically align when cancelled)
- **Cancellation visuals** (light grey color for snapped pairs)
- **Equation display** showing simplified expression
- **Hover effects** for interactive feedback
- **Instructions** for user guidance

## Common Patterns

### Pattern 1: Basic Manipulative (All Four Tiles)
```javascript
let tileConfig = {
  x: {
    width: 80, height: 60,
    color: [102, 178, 102],
    label: 'x',
    value: 'x',
    sign: 'positive'
  },
  negX: {
    width: 80, height: 60,
    color: [230, 57, 70],
    label: '-x',
    value: 'x',
    sign: 'negative'
  },
  one: {
    width: 50, height: 50,
    color: [255, 193, 94],
    label: '1',
    value: '1',
    sign: 'positive'
  },
  negOne: {
    width: 50, height: 50,
    color: [230, 57, 70],
    label: '-1',
    value: '1',
    sign: 'negative'
  }
};

let cancelConfig = {
  snapDistance: 60,
  cancelledColor: [200, 200, 200],
  snapGap: 2
};
```

### Pattern 2: Variables Only (x and -x)
```javascript
let tileConfig = {
  x: {
    width: 100, height: 70,
    color: [102, 178, 102],
    label: 'x',
    value: 'x',
    sign: 'positive'
  },
  negX: {
    width: 100, height: 70,
    color: [230, 57, 70],
    label: '-x',
    value: 'x',
    sign: 'negative'
  }
  // Only include x and -x, omit 1 and -1
};

let paletteConfig = {
  x: 150,
  y: 100,
  spacing: 150,
  label: 'Drag variable tiles:'
};
```

### Pattern 3: Constants Only (1 and -1)
```javascript
let tileConfig = {
  one: {
    width: 60, height: 60,
    color: [255, 193, 94],
    label: '1',
    value: '1',
    sign: 'positive'
  },
  negOne: {
    width: 60, height: 60,
    color: [230, 57, 70],
    label: '-1',
    value: '1',
    sign: 'negative'
  }
  // Only include 1 and -1, omit x and -x
};

let paletteConfig = {
  x: 200,
  y: 100,
  spacing: 120,
  label: 'Drag constant tiles:'
};
```

### Pattern 4: Larger Snap Distance (Easier Cancellation)
```javascript
let cancelConfig = {
  snapDistance: 80,              // Larger distance for easier cancellation
  cancelledColor: [150, 150, 150],
  showCancelledLabel: true,
  showLinkLine: true             // Show dashed line between cancelled pairs
};
```

## Mouse Interactions

### Dragging from Palette
- Mouse down on tile → create new copy
- Move mouse → tile follows cursor
- Release over workspace → place tile
- Release elsewhere → discard

### Moving Placed Tiles
- Mouse down on placed tile → start drag
- Move mouse → tile follows cursor
- Release on workspace → update position
- Release outside workspace → remove tile

### Snap & Cancellation Detection
- On every mouse release → check all pairs
- Calculate distance between tile centers
- If distance < snapDistance and opposite types → snap together
- Snapped tiles physically align side-by-side
- Both tiles turn light grey to indicate cancellation

## Drawing Logic

### Snap & Cancellation Algorithm
```javascript
function updateCancellations() {
  // Reset all cancellations
  placedTiles.forEach(tile => {
    tile.isCancelled = false;
    tile.linkedTo = null;
  });

  // Check each pair of tiles
  for (let i = 0; i < placedTiles.length; i++) {
    for (let j = i + 1; j < placedTiles.length; j++) {
      let tile1 = placedTiles[i];
      let tile2 = placedTiles[j];

      // Skip if either is already cancelled
      if (tile1.isCancelled || tile2.isCancelled) continue;

      // Check if they can cancel (same value, opposite signs)
      if (tile1.config.value === tile2.config.value &&
          tile1.config.sign !== tile2.config.sign) {

        // Check if they're close enough
        let distance = dist(
          tile1.x + tile1.config.width/2,
          tile1.y + tile1.config.height/2,
          tile2.x + tile2.config.width/2,
          tile2.y + tile2.config.height/2
        );

        if (distance < cancelConfig.snapDistance) {
          // Mark as cancelled
          tile1.isCancelled = true;
          tile2.isCancelled = true;
          tile1.linkedTo = tile2;
          tile2.linkedTo = tile1;

          // SNAP: Position tiles side-by-side
          // Calculate midpoint between the two tiles
          let midX = (tile1.x + tile2.x) / 2;
          let midY = (tile1.y + tile2.y) / 2;

          // Position tiles side-by-side at the midpoint
          let gap = 2; // Small gap between snapped tiles
          tile1.x = midX - tile1.config.width / 2 - gap / 2;
          tile2.x = midX + tile2.config.width / 2 + gap / 2 - tile2.config.width;
          tile1.y = midY;
          tile2.y = midY;
        }
      }
    }
  }
}
```

### Equation Display
- Count tiles by type (exclude cancelled)
- Group like terms
- Display simplified expression
- Example: "2x - 3" or "x + (-x) + 1" → "1"

## Code Structure

```javascript
// State management
let placedTiles = [];          // Tiles on workspace
let draggedTile = null;        // Currently dragged tile
let nextTileId = 0;            // ID counter
let hoveredPaletteTile = null; // Palette hover state

function setup() {
  createCanvas(600, 600);
  textFont('Arial');
}

function draw() {
  background(255);

  drawPalette();              // Tile sources
  drawCanvasArea();           // Workspace
  drawPlacedTiles();          // All placed tiles
  drawEquation();             // Simplified expression
  drawInstructions();         // Helper text

  if (draggedTile) {
    drawDraggedTile();        // Tile following cursor
  }
}

function mousePressed() {
  checkPlacedTileClick();     // Start dragging existing tile
  checkPaletteClick();        // Create new tile from palette
}

function mouseReleased() {
  handleTileDrop();           // Place or remove tile
  draggedTile = null;
}

function mouseMoved() {
  updateHoverState();         // Visual feedback
}
```

## Implementation Checklist

- [ ] Create palette area with all four tile types
- [ ] Implement drag from palette (creates new tiles)
- [ ] Implement drag of placed tiles
- [ ] Add workspace area with visual boundaries
- [ ] Implement drop detection (in/out of workspace)
- [ ] Create snap & cancellation detection algorithm
- [ ] Calculate distance between tile centers
- [ ] Snap opposite tiles together when close enough
- [ ] Position snapped tiles side-by-side at midpoint
- [ ] Apply light grey color to snapped/cancelled tiles
- [ ] Count non-cancelled tiles by type
- [ ] Display simplified equation
- [ ] Add hover effects for palette tiles
- [ ] Add hover effects for placed tiles
- [ ] Show instructions and labels
- [ ] Test all drag and drop scenarios
- [ ] Verify snap and cancellation logic works correctly

## Tips and Best Practices

### Snap & Cancellation Logic
- Check for snap opportunities on mouse release
- Reset all cancellation states before checking
- Use center points for distance calculation
- Only pair each tile once (skip already cancelled)
- Calculate midpoint for snap positioning
- Align tiles side-by-side at the midpoint

### Visual Feedback
- Use distinct colors for positive/negative
- Make snapped tiles clearly different (light grey)
- Tiles physically move together when snapped
- Provide hover feedback on interactive elements

### User Experience
- Make snap distance reasonable (not too small/large)
- Snap provides satisfying visual feedback
- Allow removing tiles by dragging outside
- Update equation in real-time
- Provide clear instructions

### Performance
- Limit number of tiles if performance is an issue
- Use efficient distance calculations
- Only redraw when state changes

## Color Guidelines

Standard algebra tile colors:
- **Positive x**: Green [102, 178, 102]
- **Negative x**: Red [230, 57, 70]
- **Positive 1**: Yellow/Gold [255, 193, 94]
- **Negative 1**: Red [230, 57, 70]
- **Snapped/Cancelled**: Light Grey [200, 200, 200]

Alternative color schemes:
- Traditional: Yellow (positive), Red (negative)
- High contrast: Blue (positive), Orange (negative)
- Colorblind-friendly: Use patterns/textures in addition to color

## Related Patterns

- [Dynamic Tape Diagram](../implement-dynamic-tape-diagram/) - For equation building
- [Drag and Drop Pattern](../../patterns/drag-drop.md) - Core interaction
- [Color Palette](../../primitives/colors.md) - Standard colors

## Examples

See `snippets/algebra-tiles.ts` for complete working code.

Common use cases in `src/app/animations/examples/algebraTiles/`:
- Simple manipulative (all four tiles)
- Variables only (x and -x)
- Equation modeling
- Zero principle exploration

## Educational Notes

### The Zero Principle
When a positive and negative tile of the same value are paired:
- x + (-x) = 0
- 1 + (-1) = 0
This is the foundation of:
- Solving equations (adding/subtracting from both sides)
- Simplifying expressions
- Understanding additive inverses

### Modeling Expressions
- 2x + 3: Two x tiles, three 1 tiles
- x - 5: One x tile, five -1 tiles
- -3x + 2: Three -x tiles, two 1 tiles

### Solving Equations
- Model both sides with tiles
- Add opposite tiles to isolate variable
- Count remaining tiles to find solution

---

**Last Updated**: November 2024
**Maintained By**: AI Coaching Platform Team
