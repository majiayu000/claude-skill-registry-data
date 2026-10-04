---
name: paperjsx
description: Develop interactive PaperJS applications for visual drawing, animation, and vector graphics. Create canvas-based experiences with JavaScript and PaperJS framework.
compatibility:
  use-case: Vector graphics, interactive drawing, canvas animation
  frameworks: PaperJS, HTML5 Canvas, SVG
---

# PaperJS Development

## Use This Skill When

- Building interactive drawing or sketching applications
- Creating vector graphic visualizations
- Developing canvas-based animations
- Building tools for visual content creation
- Creating geometric visualization tools
- Developing interactive graphic editors

## When NOT to Use

- Simple 2D games (consider Phaser or Three.js)
- Complex 3D graphics (use Three.js)
- Non-interactive vector graphics (use SVG directly)

## Context: PaperJS Development Maturity

**Undeveloped**: Canvas basics; difficult coordinate math.

**Target**: Using PaperJS vector operations, handling paths and shapes, basic interaction.

**Optimized**: Complex interactive tools, optimized rendering, efficient event handling.

## Core Principle

**PaperJS simplifies vector graphics.** Instead of manual canvas drawing and math, PaperJS provides high-level abstractions for paths, shapes, and transformations—enabling faster interactive graphics development.

## Instructions

### Step 1: Setup and Initialization

**Install PaperJS:**

```bash
npm install paper
# or via CDN in HTML:
<script src="https://cdnjs.cloudflare.com/ajax/libs/paper.js/0.12.15/paper-full.min.js"></script>
```

**Create canvas:**

```html
<canvas id="myCanvas"></canvas>

<script>
  // Get paper ready
  paper.setup('myCanvas');
  
  // Create a simple circle
  const circle = new paper.Path.Circle({
    center: [100, 100],
    radius: 50,
    fillColor: 'blue'
  });
  
  // Render
  paper.view.draw();
</script>
```

### Step 2: Basic Shapes and Paths

**Create and manipulate shapes:**

```javascript
// Circle
const circle = new paper.Path.Circle({
  center: [100, 100],
  radius: 50,
  fillColor: 'blue'
});

// Rectangle
const rect = new paper.Path.Rectangle({
  point: [50, 50],
  size: [100, 50],
  fillColor: 'green'
});

// Custom path
const path = new paper.Path();
path.add([10, 10]);
path.add([20, 20]);
path.add([30, 10]);
path.closed = true;
path.fillColor = 'red';
```

### Step 3: Interactive Drawing

**Handle mouse events:**

```javascript
const path = new paper.Path();

paper.tool.onMouseDown = (event) => {
  path.add(event.point);
  path.strokeColor = 'black';
  path.strokeWidth = 2;
};

paper.tool.onMouseDrag = (event) => {
  path.add(event.point);
  path.smooth();  // Smooth the path
};

paper.tool.onMouseUp = () => {
  // Path is complete
  console.log('Draw complete');
};
```

### Step 4: Transformations

**Transform shapes:**

```javascript
const circle = new paper.Path.Circle({
  center: [100, 100],
  radius: 50,
  fillColor: 'blue'
});

// Rotate
circle.rotate(45);

// Scale
circle.scale(2);

// Move
circle.position.x += 50;
```

### Step 5: Animation

**Create animated effects:**

```javascript
let angle = 0;

paper.view.onFrame = (event) => {
  angle += 1;
  
  // Update position based on angle
  circle.position.x = 100 + Math.cos(angle * Math.PI / 180) * 50;
  circle.position.y = 100 + Math.sin(angle * Math.PI / 180) * 50;
};
```

### Step 6: Hit Testing and Selection

**Detect clicks on shapes:**

```javascript
paper.tool.onMouseDown = (event) => {
  // Find item at point
  const hitResult = paper.project.hitTest(event.point);
  
  if (hitResult) {
    console.log('Clicked:', hitResult.item.name);
    hitResult.item.selected = true;
  }
};
```

## Output

**Deliver:**

1. **PaperJS Setup** (HTML canvas, initialization)
2. **Basic Shapes** (circles, rectangles, paths)
3. **Interactive Drawing** (mouse event handlers)
4. **Transformations** (rotate, scale, move)
5. **Animation Loop** (frame-based updates)
6. **Hit Testing** (click detection on shapes)