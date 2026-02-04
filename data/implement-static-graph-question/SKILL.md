---
name: Implement Static Graph Question
description: Create D3 questions with static line graphs and coordinating table inputs. Students read graphs and fill in corresponding values.
---

# Implement Static Graph Question

Use this skill when creating questions where students:
- Read a static line graph showing a relationship
- Fill in table values based on the graph
- Explain patterns or relationships shown in the graph

## When to Use This Pattern

**Perfect for:**
- "Use the graph to complete the table"
- "Read the graph and fill in missing values"
- Proportional relationship questions with visual representation
- Rate/slope questions with coordinate visualization

**Not suitable for:**
- Interactive graph manipulation (use dynamic graph component when available)
- Simple tables without graphs → use [implement-table-question](../implement-table-question/SKILL.md)
- Drag-and-drop matching → use [implement-drag-match-question](../implement-drag-match-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Required
- `static-graph.js` → `renderStaticGraph()` - NEW! Static graph component
- `cards/standard-card.js` → `createStandardCard()`

### Optional
- `cards/explanation-card.js` → `createExplanationCard()` - For student explanations
- `cards/video-accordion.js` → `createVideoAccordion()` - For help videos
- `tables.js` → For custom table rendering (or use HTML tables)

## Quick Start

1. **Study the working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/02/attachments/chart.js
   ```

2. **Copy the static-graph component** from [snippets/static-graph.js](../snippets/static-graph.js)

3. **Use the pattern below** to render graph + table

## Key Implementation Decisions

1. **Graph configuration** - X/Y domains, labels, grid spacing
2. **Line data** - What relationship does the graph show?
3. **Table structure** - Which values are editable?
4. **State fields** - One field per editable table cell

## State Shape

```javascript
function createDefaultState() {
  return {
    // One field per editable table cell
    cell1: "",
    cell2: "",
    cell3: "",
    cell4: "",
    explanation: ""
  };
}
```

## Core Pattern

### 1. Define Graph Configuration

```javascript
// Graph data
const RATE = 20;  // $20 per day
const MAX_DAYS = 10;
const MAX_MONEY = 200;

const graphConfig = {
  width: 600,
  height: 400,
  padding: { top: 40, right: 40, bottom: 60, left: 70 },
  xDomain: [0, MAX_DAYS],
  yDomain: [0, MAX_MONEY],
  xLabel: "Days",
  yLabel: "Money Earned ($)",
  xVariable: "d",  // Variable label (optional)
  yVariable: "m",  // Variable label (optional)
  lineData: [
    { x: 0, y: 0 },
    { x: MAX_DAYS, y: MAX_DAYS * RATE }
  ],
  xGridStep: 1,
  yGridStep: 20,
  showArrow: true
};
```

### 2. Render Graph

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("").style("padding", "20px").style("overflow", "auto");

  // Intro card
  const introCard = createStandardCard(d3, container, {
    size: "large",
    title: "Read the Graph"
  });
  introCard.append("p").text("Use the graph to complete the table below.");

  // Graph card
  const graphCard = createStandardCard(d3, container, {
    size: "graph",
    title: "Sarah's Earnings"
  });

  const svg = graphCard.append("svg");
  renderStaticGraph(d3, svg, graphConfig);

  // Table and explanation below...
  renderTable(d3, container);
  renderExplanation(d3, container);
}
```

### 3. Render Table with Inputs

```javascript
function renderTable(d3, container) {
  const tableCard = createStandardCard(d3, container, {
    size: "medium",
    title: "Complete the Table"
  });

  // HTML table approach (simpler)
  const tableHtml = `
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th style="border: 1px solid #e5e7eb; padding: 12px;">Days</th>
          <th style="border: 1px solid #e5e7eb; padding: 12px;">Money ($)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="border: 1px solid #e5e7eb; padding: 12px;">1</td>
          <td style="border: 1px solid #e5e7eb; padding: 12px;">
            <input type="text" id="day1" inputmode="numeric"
                   style="width: 100%; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px;">
          </td>
        </tr>
        <tr>
          <td style="border: 1px solid #e5e7eb; padding: 12px;">3</td>
          <td style="border: 1px solid #e5e7eb; padding: 12px;">
            <input type="text" id="day3" inputmode="numeric"
                   style="width: 100%; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px;">
          </td>
        </tr>
      </tbody>
    </table>
  `;

  tableCard.html(tableCard.html() + tableHtml);

  // Bind input events
  input1 = tableCard.select("#day1")
    .property("value", chartState.day1)
    .on("input", function() {
      chartState.day1 = this.value;
      sendChartState();
    });

  input3 = tableCard.select("#day3")
    .property("value", chartState.day3)
    .on("input", function() {
      chartState.day3 = this.value;
      sendChartState();
    });
}
```

### 4. Message Protocol

```javascript
function sendChartState() {
  sendMessage("response_updated", {
    tableValues: {
      day1: chartState.day1,
      day3: chartState.day3,
      // ... other table values
    },
    explanation: {
      text: chartState.explanation
    }
  });
}
```

## Working Examples

**In codebase:**
- [IM-8th-Grade Ramp-Up-01 Q02](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/02/attachments/chart.js) - Complete example with graph + table

**Key features shown:**
- Static line graph with grid
- Arrowhead at end of line
- Variable labels (d, m)
- Table with 4 editable cells
- Explanation card
- Video accordion for help

## Common Variations

### Two-Column Layout (Graph + Table Side-by-Side)

```javascript
const layout = container.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "1fr 1fr")
  .style("gap", "20px");

const leftColumn = layout.append("div");
const rightColumn = layout.append("div");

// Graph in left column
const svg = leftColumn.append("svg");
renderStaticGraph(d3, svg, graphConfig);

// Table in right column
renderTable(d3, rightColumn);
```

### Different Graph Types

**Horizontal line (constant value):**
```javascript
lineData: [
  { x: 0, y: 50 },
  { x: 10, y: 50 }
]
```

**Non-linear relationship:**
```javascript
lineData: Array.from({length: 11}, (_, i) => ({
  x: i,
  y: i * i  // Quadratic
}))
```

### D3 Table Instead of HTML

See [snippets/tables.js](../snippets/tables.js) for D3 table patterns with custom styling.

## Static Graph Component API

The `renderStaticGraph()` function accepts these options:

```javascript
renderStaticGraph(d3, svg, {
  // Size
  width: 600,           // SVG width
  height: 400,          // SVG height
  padding: { top: 40, right: 40, bottom: 60, left: 70 },

  // Domains
  xDomain: [0, 10],     // X-axis min/max
  yDomain: [0, 200],    // Y-axis min/max

  // Labels
  xLabel: "Days",       // X-axis label
  yLabel: "Money ($)",  // Y-axis label
  xVariable: "d",       // X variable (optional, italic)
  yVariable: "m",       // Y variable (optional, italic)

  // Line data
  lineData: [           // Array of {x, y} points
    { x: 0, y: 0 },
    { x: 10, y: 200 }
  ],

  // Grid
  xGridStep: 1,         // Vertical grid line spacing
  yGridStep: 20,        // Horizontal grid line spacing

  // Axes
  xTicks: 10,           // Number of X-axis ticks (optional)
  yTicks: 10,           // Number of Y-axis ticks

  // Line styling
  showArrow: true,      // Show arrowhead at end
  lineColor: "#3b82f6", // Line color
  lineWidth: 2.5        // Line stroke width
});
```

## Implementation Checklist

- [ ] Copied `renderStaticGraph()` from snippets/static-graph.js
- [ ] Defined graph configuration (domains, labels, line data)
- [ ] Created SVG and called `renderStaticGraph()`
- [ ] Created table with editable cells (HTML or D3)
- [ ] Created `createDefaultState()` with one field per editable cell
- [ ] Bound input events to update state
- [ ] Implemented `sendChartState()` with tableValues
- [ ] Added explanation card (if needed)
- [ ] Implemented `setInteractivity()` to disable inputs when locked
- [ ] Implemented `applyInitialState()` to restore table values
- [ ] Tested state restoration
- [ ] Tested locking/unlocking
- [ ] Verified graph renders correctly at different screen sizes

## Tips

1. **Match table to graph** - Table values should correspond to visible points on the graph
2. **Use grid lines** - Help students read values accurately
3. **Label clearly** - Both axis labels and variable labels aid comprehension
4. **Provide context** - Intro card should explain the scenario
5. **Consider layout** - Side-by-side works well on desktop, stacked better on mobile
6. **Test readability** - Ensure graph is readable at different sizes (viewBox helps!)

## Graph Design Best Practices

- **Choose appropriate domains** - Don't make graph too cramped or too sparse
- **Use consistent grid spacing** - Makes values easier to read
- **Add arrowheads** - Shows the line continues beyond the visible domain
- **Include units** - Label axes with units (e.g., "Days", "Money ($)")
- **Variable labels optional** - Use when teaching function notation (e.g., m = f(d))

## Related Skills

- [implement-table-question](../implement-table-question/SKILL.md) - For tables without graphs
- [implement-slider-question](../implement-slider-question/SKILL.md) - For interactive parameter exploration
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [snippets/static-graph.js](../snippets/static-graph.js) - Static graph component
- [snippets/tables.js](../snippets/tables.js) - D3 table patterns
- [snippets/cards/](../snippets/cards/) - Card components
