---
name: Implement Dynamic Tape Diagram
description: Create interactive tape diagram builders using p5.js where students construct algebraic equations by dragging and resizing parts.
---

# Implement Dynamic Tape Diagram

Use this skill when creating animations where students:
- Build tape diagrams by dragging variables (x) and constants into a bar
- Resize constants before adding them to the diagram
- See proportional relationships when setting a total value
- Visualize algebraic equations as bar models

## When to Use This Pattern

**Perfect for:**
- "Build a tape diagram for x + 8 = 32"
- Interactive equation builders with visual models
- Exploring how changing parts affects the whole
- Understanding proportional relationships in algebra
- Visualizing variable vs. constant relationships

**Not suitable for:**
- Static tape diagrams (use basic p5 animation)
- Comparing multiple equations side-by-side
- Multi-step equation solving sequences (use phase-based animation)

## Technology Stack

**Uses p5.js** for the interactive tape diagram because:
- Real-time drag-and-drop interaction
- Dynamic resizing of visual elements
- Mouse and touch event handling
- Smooth proportional animations

## Configuration Options

### Basic Configuration

```javascript
// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Palette items (draggable sources)
let paletteConfig = {
  variable: {
    x: 80,
    y: 100,
    w: 60,
    h: 60,
    color: [230, 57, 70],      // Red for variables
    label: 'x'
  },
  constant: {
    x: 200,
    y: 100,
    w: 100,                    // Initial width (resizable)
    h: 60,
    minWidth: 40,              // Minimum size
    maxWidth: 300,             // Maximum size
    initialValue: 1,
    maxValue: 20,
    color: [6, 167, 125],      // Green for constants
  }
};

// Tape diagram drop zone
let tapeConfig = {
  x: 50,
  y: 320,
  w: 500,
  h: 100,
  backgroundColor: [240, 240, 240],
  borderColor: [150, 150, 150],
  label: 'Drop parts here'
};

// Total value settings
let totalConfig = {
  initial: 0,                  // Starting total value
  min: 0,
  max: 1000,
  step: 1,
  showProportions: true        // Show calculated values when total is set
};

// Visual settings
let visualConfig = {
  showEquation: true,          // Display equation text
  showInstructions: true,      // Show helper text
  animateTransitions: true,    // Smooth width changes
  highlightDropZone: true      // Highlight when dragging
};
```

## Features

### Interactive Controls

1. **Drag Variable (x)**
   - Drag from palette to drop zone
   - Each x represents 1 unit
   - Always distributes evenly in the diagram

2. **Resize and Drag Constants**
   - Drag edges to resize the constant bar
   - Shows current value as you resize
   - Drag to drop zone when ready
   - Each whole number proportionally sized

3. **Total Value Input**
   - Click +/- buttons to adjust total
   - When set, all parts resize proportionally
   - Shows calculated values for each part

4. **Part Management**
   - Click parts to select/deselect
   - Click X button to remove parts
   - Parts automatically distribute space

### Visual Elements

- **Palette area** with draggable variable and constant
- **Resize handles** on constant bar (left and right edges)
- **Drop zone** with visual feedback
- **Proportional tape bars** showing equation parts
- **Equation display** showing current expression
- **Calculated values** when total is set

## Common Patterns

### Pattern 1: Simple Equation (x + 5 = 20)
```javascript
let paletteConfig = {
  variable: {
    x: 80, y: 80, w: 60, h: 60,
    color: [230, 57, 70],
    label: 'x'
  },
  constant: {
    x: 200, y: 80, w: 100, h: 60,
    minWidth: 40, maxWidth: 200,
    initialValue: 5, maxValue: 20,
    color: [6, 167, 125]
  }
};

let totalConfig = {
  initial: 20,
  min: 0,
  max: 100,
  step: 1,
  showProportions: true
};
```

### Pattern 2: Multiple Variables (2x + 10)
```javascript
// Enable adding multiple x's
let paletteConfig = {
  variable: {
    x: 80, y: 80, w: 60, h: 60,
    color: [230, 57, 70],
    label: 'x',
    allowMultiple: true        // Can add multiple x's
  },
  constant: {
    x: 200, y: 80, w: 100, h: 60,
    minWidth: 40, maxWidth: 300,
    initialValue: 1, maxValue: 30,
    color: [6, 167, 125]
  }
};
```

### Pattern 3: Fraction Tape Diagrams
```javascript
let paletteConfig = {
  constant: {
    x: 200, y: 80, w: 100, h: 60,
    minWidth: 20, maxWidth: 400,
    initialValue: 1,
    maxValue: 12,              // For showing 1/12, 2/12, etc.
    color: [255, 153, 51],     // Orange
    showAsFraction: true       // Display as fraction of whole
  }
};

let totalConfig = {
  initial: 1,                  // Whole = 1
  min: 0,
  max: 1,
  step: 0,
  showProportions: true
};
```

## Mouse Interactions

### Dragging from Palette
- Mouse down on variable or constant → start drag
- Move mouse → item follows cursor
- Release over drop zone → add to tape
- Release elsewhere → return to palette

### Resizing Constant
- Mouse near left/right edge → show resize cursor
- Mouse down on edge → start resize
- Drag left/right → change width (snaps to whole numbers)
- Release → set new value

### Managing Tape Parts
- Click on part → select (highlight)
- Click X button → remove part
- Parts automatically redistribute space

## Drawing Logic

### Proportional Sizing
When total value is set:
1. Calculate total units: sum all part values (x=1, constant=its value)
2. Calculate unit value: totalValue / totalUnits
3. Each part width = (partValue / totalUnits) * tapeWidth
4. Show actual values: partValue * unitValue

### Drop Zone Feedback
- Hovering while dragging → highlight border
- Invalid drop → shake animation or visual feedback
- Valid drop → smooth transition into place

## Code Structure

```javascript
// State management
let tapeParts = [];           // Parts in the main diagram
let isDragging = false;       // Current drag state
let dragItem = null;          // What's being dragged
let totalValue = 0;           // Current total

function setup() {
  createCanvas(600, 600);
  textFont('Arial');
}

function draw() {
  background(255);

  drawPalette();              // Draggable sources
  drawTotalInput();           // +/- controls
  drawEquationDisplay();      // Show equation text
  drawTapeDiagram();          // Main visualization
  drawInstructions();         // Helper text

  if (isDragging) {
    drawDraggedItem();        // Follow cursor
  }
}

function mousePressed() {
  checkPaletteClick();
  checkResizeHandles();
  checkTotalButtons();
  checkPartSelection();
}

function mouseDragged() {
  updateDragPosition();
  updateResizeWidth();
}

function mouseReleased() {
  checkDropZone();
  releaseDragItem();
}
```

## Implementation Checklist

- [ ] Create palette area with variable and constant
- [ ] Implement drag from palette to drop zone
- [ ] Add resize handles to constant bar
- [ ] Show current value when resizing
- [ ] Implement drop zone with visual feedback
- [ ] Create tape parts array to store dropped items
- [ ] Calculate proportional widths based on values
- [ ] Implement total value +/- controls
- [ ] Show calculated actual values when total is set
- [ ] Add part selection (click to select)
- [ ] Add part removal (X button)
- [ ] Display equation as text
- [ ] Add helper instructions
- [ ] Test all mouse interactions
- [ ] Verify proportional sizing is correct

## Tips and Best Practices

### Proportional Calculations
- Always calculate total units first
- Handle zero cases (no total set, or totalUnits = 0)
- Use consistent rounding for display values

### Visual Feedback
- Show resize cursor when near edges
- Highlight drop zone when dragging
- Animate width changes smoothly
- Use distinct colors for variable vs constant

### User Experience
- Snap resize to whole numbers (easier to control)
- Provide clear instructions
- Show equation dynamically as parts are added
- Allow removing parts easily

## Related Patterns

- [Auto/Manual Toggle Pattern](../../AUTO-MANUAL-TOGGLE-PATTERN.md) - For multi-phase solving
- [Dynamic Graph](../implement-dynamic-graph-question/) - For coordinate plane interactions
- [Color Palette](../../primitives/colors.md) - Standard colors to use

## Examples

See `snippets/dynamic-tape-diagram.ts` for complete working code.

Common use cases in `src/app/animations/examples/tapeDiagrams/`:
- Simple equation builder (x + 5 = 20)
- Multi-variable builder (2x + 3)
- Fraction tape diagrams (showing parts of a whole)

---

**Last Updated**: November 2024
**Maintained By**: AI Coaching Platform Team
