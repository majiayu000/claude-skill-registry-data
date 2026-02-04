---
name: Implement Dynamic Graph Question
description: Create interactive coordinate plane questions using p5.js where students draw linear lines with snap-to-grid.
---

# Implement Dynamic Graph Question

Use this skill when creating questions where students:
- Draw lines on an interactive coordinate plane
- Explore linear relationships by drawing from points
- Create proportional relationships from the origin
- Compare multiple linear scenarios

## When to Use This Pattern

**Perfect for:**
- "Draw a line showing a proportional relationship"
- "Draw a line from (0,0) through (5, 10)"
- "Draw lines to match the given equations"
- Interactive slope/linear function exploration
- Comparing rates by drawing multiple lines

**Not suitable for:**
- Static graph reading → use [implement-static-graph-question](../implement-static-graph-question/SKILL.md)
- Simple table completion → use [implement-table-question](../implement-table-question/SKILL.md)
- Pre-defined graph manipulation (use slider pattern)

## Technology Stack

**Uses p5.js (NOT D3)** for the coordinate plane because:
- Better for real-time interactive drawing
- Simpler mouse/touch event handling
- Built-in animation and rendering loop
- Easier geometric operations

**Integrates with D3** for:
- Layout and cards (intro, explanation, etc.)
- State management
- Message protocol

## Components Required

**Copy these:**

### P5.js Coordinate Plane (Required)
- `snippets/coordinate-plane-p5.js` → Full p5 sketch in instance mode

### D3 Cards (Optional)
- `.claude/skills/question-types/snippets/cards/standard-card.js` → `createStandardCard()`
- `.claude/skills/question-types/snippets/cards/explanation-card.js` → `createExplanationCard()`

### P5.js Library (Required)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js"></script>
```

## Quick Start

1. **Study the base implementation**:
   ```bash
   cat alex/coordinatePlane/linear-graph-drawing.ts
   cat .claude/skills/question-types/implement-dynamic-graph-question/snippets/coordinate-plane-p5.js
   ```

2. **Copy the p5 coordinate plane snippet** into your chart.js IIFE

3. **Follow the integration pattern below**

## State Shape

```javascript
function createDefaultState() {
  return {
    drawnLines: [],  // [{ start: {x, y}, end: {x, y} }, ...]
    explanation: ""
  };
}
```

## Core Integration Pattern

### 1. Load P5.js (in chart.html for testing)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
</head>
<body>
  <div id="chart-root"></div>
  <script src="chart.js"></script>
  <script>createChart("#chart-root");</script>
</body>
</html>
```

### 2. Chart.js Structure (IIFE with p5 + D3)

```javascript
(function () {
  "use strict";

  // ============================================================
  // INLINE P5 COORDINATE PLANE COMPONENT HERE
  // ============================================================

  // [Paste full content of coordinate-plane-p5.js here]

  // ============================================================
  // INLINE D3 CARD COMPONENTS (if needed)
  // ============================================================

  // [Paste createStandardCard, createExplanationCard, etc.]

  // ============================================================
  // QUESTION STATE & SETUP
  // ============================================================

  function createDefaultState() {
    return {
      drawnLines: [],
      explanation: ""
    };
  }

  let chartState = createDefaultState();
  let interactivityLocked = false;
  let d3Promise = null;
  let messageHandlerRegistered = false;
  let containerSelectorRef = "#chart-root";
  let currentD3 = null;
  let coordinatePlane = null;

  // D3 loading...
  function ensureD3() { /* ... standard D3 loading ... */ }

  // Message protocol
  function sendMessage(type, payload) { /* ... standard ... */ }

  function sendChartState() {
    sendMessage("response_updated", {
      lines: chartState.drawnLines.map(line => ({
        start: { x: line.start.x, y: line.start.y },
        end: { x: line.end.x, y: line.end.y },
        slope: calculateSlope(line),
        intercept: calculateIntercept(line)
      })),
      explanation: {
        text: chartState.explanation
      }
    });
  }

  function calculateSlope(line) {
    const dx = line.end.x - line.start.x;
    const dy = line.end.y - line.start.y;
    return dx === 0 ? Infinity : dy / dx;
  }

  function calculateIntercept(line) {
    const slope = calculateSlope(line);
    if (slope === Infinity) return null;
    return line.start.y - slope * line.start.x;
  }

  function setInteractivity(enabled) {
    interactivityLocked = !enabled;
    if (coordinatePlane) {
      coordinatePlane.setLocked(!enabled);
    }
  }

  function buildLayout(d3, containerSelector) {
    const container = d3.select(containerSelector);
    container.html("");
    container
      .style("font-family", "'Inter', system-ui, -apple-system")
      .style("padding", "20px")
      .style("overflow", "auto");

    // Intro card (using D3)
    const introCard = createStandardCard(d3, container, {
      size: "large",
      title: "Draw Linear Relationships"
    });
    introCard.append("p")
      .text("Click to start drawing a line, then click again to finish. Lines snap to grid intersections.");

    // P5 coordinate plane container
    const planeContainer = container.append("div")
      .attr("id", "coordinate-plane-container")
      .style("margin", "20px 0")
      .node();

    // Create p5 coordinate plane
    coordinatePlane = createCoordinatePlane("coordinate-plane-container", {
      xMin: 0,
      xMax: 10,
      yMin: 0,
      yMax: 100,
      xLabel: "Time (hours)",
      yLabel: "Distance (miles)",
      gridScaleX: 1,
      gridScaleY: 10,
      // Optional: initialPoints, initialEquations, predrawnStartPoint
    }, {
      onLineDrawn: (line) => {
        console.log("Line drawn:", line);
      },
      onLinesChanged: (lines) => {
        chartState.drawnLines = lines;
        sendChartState();
      }
    });

    // Explanation card (using D3)
    createExplanationCard(d3, container, {
      prompt: "Explain your thinking:",
      value: chartState.explanation,
      onInput: (value) => {
        chartState.explanation = value;
        sendChartState();
      },
      locked: interactivityLocked
    });
  }

  function applyInitialState(payload) {
    if (!payload) return;

    if (payload.lines && Array.isArray(payload.lines)) {
      chartState.drawnLines = payload.lines;
      // Restore lines in p5 coordinate plane
      // Note: Need to expose setLines method from p5 sketch
    }

    chartState.explanation = payload.explanation?.text || "";
  }

  function setupMessageHandlers(d3) {
    if (messageHandlerRegistered) return;
    messageHandlerRegistered = true;

    window.addEventListener("message", (event) => {
      const { data } = event;
      if (!data || typeof data !== "object") return;

      if (data.type === "setInitialState") {
        applyInitialState(data.payload);
      }

      if (data.type === "set_lock") {
        setInteractivity(data.payload === false);
      }

      if (data.type === "check_answer") {
        sendChartState();
      }
    });
  }

  function createChart(containerSelector) {
    containerSelectorRef = containerSelector || "#chart-root";

    ensureD3()
      .then((d3) => {
        currentD3 = d3;
        buildLayout(d3, containerSelectorRef);

        window.clearChart = function () {
          chartState = createDefaultState();
          if (coordinatePlane && coordinatePlane.reset) {
            coordinatePlane.reset();
          }
          sendMessage("selection_cleared", null);
          sendChartState();
        };

        window.setInteractivity = setInteractivity;
        setupMessageHandlers(d3);
      })
      .catch((error) => {
        console.error(error);
        const fallback = document.querySelector(containerSelectorRef) || document.body;
        fallback.innerHTML = "<p style='color:#b91c1c'>Failed to load visualization.</p>";
      });
  }

  window.createChart = createChart;
  window.createArtifact = createChart;
})();
```

## Configuration Options

### Basic Configuration

```javascript
{
  // Axis ranges
  xMin: 0,
  xMax: 10,
  yMin: 0,
  yMax: 100,

  // Grid spacing
  gridScaleX: 1,      // X-axis grid step
  gridScaleY: 10,     // Y-axis grid step

  // Labels
  xLabel: "Time (hours)",
  yLabel: "Distance (miles)",
  xVariable: "t",     // Optional italic variable (e.g., "t" for time)
  yVariable: "d",     // Optional italic variable (e.g., "d" for distance)

  // Display options
  showCoordinatesOnHover: true,  // Show (x, y) on hover (default: true)

  // Snap configuration (for fractional values)
  snapSubdivisions: 1,      // 1=grid only, 2=halves, 3=thirds, 5=fifths, etc.
  snapSubdivisionsX: 1,     // Per-axis: snap X to subdivisions
  snapSubdivisionsY: 2,     // Per-axis: snap Y to halves
}
```

### With Initial Data

```javascript
{
  xMin: 0, xMax: 10,
  yMin: 0, yMax: 100,
  gridScaleX: 1, gridScaleY: 10,
  xLabel: "X", yLabel: "Y",

  // Show reference equations (green lines)
  initialEquations: [
    { slope: 5, intercept: 0, color: [34, 197, 94] },  // y = 5x
    { slope: 8, intercept: 10, color: [59, 130, 246] } // y = 8x + 10
  ],

  // Show specific points
  initialPoints: [
    { x: 2, y: 10 },
    { x: 5, y: 25 },
    { x: 8, y: 40 }
  ],
}
```

### Force Drawing from Origin

```javascript
{
  xMin: 0, xMax: 10,
  yMin: 0, yMax: 50,
  gridScaleX: 1, gridScaleY: 5,
  xLabel: "X", yLabel: "Y",

  // Force first line to start from (0, 0)
  predrawnStartPoint: { x: 0, y: 0 },
}
```

## Common Patterns

### Pattern 1: Proportional Relationships (from origin)

```javascript
const plane = createCoordinatePlane("container", {
  xMin: 0, xMax: 10,
  yMin: 0, yMax: 50,
  xLabel: "X", yLabel: "Y",
  predrawnStartPoint: { x: 0, y: 0 },
}, {
  onLineDrawn: (line) => {
    const slope = (line.end.y - line.start.y) / (line.end.x - line.start.x);
    console.log(`Constant of proportionality: ${slope}`);
  }
});
```

### Pattern 2: Compare to Reference Line

```javascript
const plane = createCoordinatePlane("container", {
  xMin: 0, xMax: 10,
  yMin: 0, yMax: 100,
  xLabel: "Time", yLabel: "Distance",
  initialEquations: [
    { slope: 5, intercept: 0, color: [34, 197, 94] } // Reference: 5 mph
  ]
}, {
  onLinesChanged: (lines) => {
    // Students draw their own speed, compare to reference
  }
});
```

### Pattern 3: Connect the Dots

```javascript
const plane = createCoordinatePlane("container", {
  xMin: 0, xMax: 5,
  yMin: 0, yMax: 4000,
  xLabel: "Days", yLabel: "Steps",
  initialPoints: [
    { x: 1, y: 800 },
    { x: 3, y: 2400 },
    { x: 5, y: 4000 }
  ]
});
```

### Pattern 4: Fractional Snapping

Use when slopes require fractional coordinates (e.g., slope = 2/3 needs thirds):

```javascript
const plane = createCoordinatePlane("container", {
  xMin: 0, xMax: 12,
  yMin: 0, yMax: 8,
  xLabel: "X", yLabel: "Y",
  gridScaleX: 1, gridScaleY: 1,

  // Allow snapping to thirds (for slope = 2/3)
  snapSubdivisions: 3,  // Both axes snap to 0, 1/3, 2/3, 1, 4/3, ...

  // Or different subdivisions per axis:
  // snapSubdivisionsX: 3,  // X snaps to thirds
  // snapSubdivisionsY: 2,  // Y snaps to halves

  predrawnStartPoint: { x: 0, y: 0 },
});
```

## Implementation Checklist

- [ ] Loaded p5.js library in chart.html
- [ ] Inlined `coordinate-plane-p5.js` into chart.js IIFE
- [ ] Inlined D3 card components (if needed)
- [ ] Created `createDefaultState()` with `drawnLines` array
- [ ] Created p5 container div with unique ID
- [ ] Called `createCoordinatePlane()` with configuration
- [ ] Implemented `onLinesChanged` callback to update chartState
- [ ] Implemented `sendChartState()` with line data
- [ ] Calculated slope/intercept for each line (if needed)
- [ ] Implemented `setInteractivity()` to lock/unlock drawing
- [ ] Implemented `applyInitialState()` (if state restoration needed)
- [ ] Tested locally with chart.html
- [ ] Tested drawing lines
- [ ] Tested keyboard controls (R to reset, ESC to cancel)
- [ ] Tested state updates trigger `response_updated` messages

## Tips

1. **p5 + D3 coexistence** - p5 handles the graph, D3 handles everything else
2. **Use instance mode** - Never use global p5 mode when embedding
3. **Unique container IDs** - Each p5 sketch needs its own container
4. **State extraction** - Pull line data from p5 into chartState via callbacks
5. **Clear instructions** - Tell students the interaction model (click-click-click)
6. **Snap-to-grid** - Already built-in, makes drawing easier
7. **Preview line** - Extends to infinity, helps visualize slope
8. **Initial equations** - Great for "match this slope" exercises

## Limitations & Notes

- **One p5 instance per question** - Don't create multiple coordinate planes
- **State restoration** - Need to explicitly restore lines to p5 from `setInitialState`
- **Mobile support** - p5 handles touch events automatically
- **Performance** - p5 is fast, but keep canvas size reasonable (600x600 default)

## Related Skills

- [implement-static-graph-question](../implement-static-graph-question/SKILL.md) - For non-interactive graphs
- [implement-slider-question](../implement-slider-question/SKILL.md) - For parameter adjustment
- [create-p5-animation](../../create-p5-animation/SKILL.md) - For animated explanations
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [snippets/coordinate-plane-p5.js](snippets/coordinate-plane-p5.js) - Full p5 component
- [alex/coordinatePlane/](../../../../../alex/coordinatePlane/) - Original p5 implementation
- [p5.js Reference](https://p5js.org/reference/) - p5.js documentation
