---
name: Implement Double Number Line Question
description: Create D3 questions with double number lines showing proportional relationships. Students complete missing values on parallel number lines.
---

# Implement Double Number Line Question

Use this skill when creating questions where students:
- Complete missing values on double number lines
- Work with proportional relationships shown on parallel number lines
- Fill in blanks on two aligned number lines showing equivalent ratios

## When to Use This Pattern

**Perfect for:**
- "Complete the double number line showing days and pies"
- "Fill in the missing values on the number lines"
- Questions with two parallel number lines showing proportional relationships
- Equivalent ratio visualization with number lines

**Not suitable for:**
- Single number lines → use custom implementation
- Graph coordinate planes → use [implement-dynamic-graph-question](../implement-dynamic-graph-question/SKILL.md)
- Simple tables → use [implement-table-question](../implement-table-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/`:

### Required
- `implement-double-number-line-question/snippets/double-number-line.js` → Complete double number line implementation
- `snippets/cards/standard-card.js` → `createStandardCard()`

### Optional
- `snippets/cards/explanation-card.js` → `createExplanationCard()` - For student explanations

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md)
2. **Study the snippet**: [snippets/double-number-line.js](snippets/double-number-line.js)
3. **Copy from the working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/02/attachments/chart.js
   ```

## Implementation Steps

### 1. Define State

```javascript
function createDefaultState() {
  return {
    dnl1: "", // First blank on top number line
    dnl2: "", // Second blank on top number line
    dnl3: "", // First blank on bottom number line
    dnl4: "", // Second blank on bottom number line
    finalAnswer: "" // Optional: answer based on the number lines
  };
}
```

### 2. Copy the Double Number Line Snippet

Inline the complete `double-number-line.js` snippet into your chart.js file.

### 3. Configure and Call

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("");

  // Create double number line
  const dnlInputs = createDoubleNumberLine(container, {
    svgWidth: 700,
    svgHeight: 200,
    topLabel: "Days",
    bottomLabel: "Pies",
    topValues: ["0", "3", "6", "9", null, null],
    bottomValues: ["0", "8", "16", "24", null, null],
    inputPositions: {
      top: [{ index: 4, key: "dnl1" }, { index: 5, key: "dnl2" }],
      bottom: [{ index: 4, key: "dnl3" }, { index: 5, key: "dnl4" }]
    }
  });

  // Store for interactivity control
  window.dnlInputs = dnlInputs;
}
```

### 4. Implement Interactivity Control

```javascript
function setInteractivity(enabled) {
  if (window.dnlInputs) {
    window.dnlInputs.setInteractivity(enabled);
  }
}
```

## Configuration Options

### Basic Configuration

```javascript
{
  svgWidth: 700,        // SVG width (default: 700)
  svgHeight: 200,       // SVG height (default: 200)
  lineY1: 60,          // Top line Y position (default: 60)
  lineY2: 140,         // Bottom line Y position (default: 140)
  lineStartX: 50,      // Line start X (default: 50)
  lineEndX: 650,       // Line end X (default: 650)
  tickLength: 10,      // Tick mark length (default: 10)
  topLabel: "Days",    // Top line label
  bottomLabel: "Pies", // Bottom line label
  numPositions: 6      // Number of tick marks (default: 6)
}
```

### Value Configuration

```javascript
{
  topValues: ["0", "3", "6", "9", null, null],    // null = input box
  bottomValues: ["0", "8", "16", "24", null, null],
  inputPositions: {
    top: [
      { index: 4, key: "dnl1" },  // Position 4, state key "dnl1"
      { index: 5, key: "dnl2" }   // Position 5, state key "dnl2"
    ],
    bottom: [
      { index: 4, key: "dnl3" },
      { index: 5, key: "dnl4" }
    ]
  }
}
```

## Critical Implementation Pattern: foreignObject

The snippet uses **SVG foreignObject** for input positioning. This is the ONLY reliable method.

### Why foreignObject?

✅ **Correct:** Uses same coordinate system as SVG text labels
✅ **Correct:** Direct SVG coordinates with centering formula
✅ **Correct:** Perfect alignment with tick marks

❌ **Wrong:** Div overlay with percentage positioning
❌ **Wrong:** Mixing coordinate systems

### Centering Formula

For an input of width `W` and height `H`, to center it on SVG coordinate `(x, y)`:

```javascript
.attr("x", x - W/2)  // Subtract half the width
.attr("y", y - H/2)  // Subtract half the height
```

Example:
- Input is 60px wide, 32px tall
- Want to center on (530, 35)
- Set x = 530 - 30 = 500
- Set y = 35 - 16 = 19

## Common Customizations

### Different Number of Ticks

```javascript
{
  numPositions: 8,  // 8 ticks instead of 6
  topValues: ["0", "2", "4", "6", null, null, "14", "16"],
  bottomValues: ["0", "5", "10", "15", null, null, "35", "40"]
}
```

### Different Input Positions

```javascript
{
  topValues: ["0", "3", null, null, "12", null],
  inputPositions: {
    top: [
      { index: 2, key: "dnl1" },
      { index: 3, key: "dnl2" },
      { index: 5, key: "dnl3" }
    ],
    bottom: [
      { index: 2, key: "dnl4" },
      { index: 3, key: "dnl5" },
      { index: 5, key: "dnl6" }
    ]
  }
}
```

### With Optional Table

Many double number line questions include a table showing the relationship first:

```javascript
// Before creating the double number line
const tableCard = createStandardCard(container, {
  title: "Ratio Table",
  content: tableHtml
});

// Then create the double number line
const dnlInputs = createDoubleNumberLine(container, config);
```

## Implementation Checklist

- [ ] State includes keys for all input boxes (dnl1, dnl2, dnl3, dnl4)
- [ ] Copied `double-number-line.js` snippet into chart.js
- [ ] Configured topLabel and bottomLabel
- [ ] Configured topValues and bottomValues (null for input positions)
- [ ] Configured inputPositions with correct indices and state keys
- [ ] Called createDoubleNumberLine() in buildLayout()
- [ ] Stored return value for interactivity control
- [ ] Implemented setInteractivity() function
- [ ] sendChartState() updates parent on input changes
- [ ] Tested in browser to verify alignment

## DO NOT

❌ Use div overlay with percentage positioning
❌ Mix coordinate systems (SVG and CSS percentages)
❌ Hardcode pixel positions without centering formula
❌ Use transform: translate() for positioning inputs
❌ Forget to subtract half width/height for centering

## DO

✅ Always use SVG foreignObject for input positioning
✅ Use same coordinate system as SVG text labels
✅ Apply centering formula: x - width/2, y - height/2
✅ Position inputs at tick mark X-coordinates
✅ Test alignment in actual browser
✅ Document Y-coordinate choices for maintainability

## Related Patterns

- [implement-table-question](../implement-table-question/SKILL.md) - For tabular data entry
- [implement-static-graph-question](../implement-static-graph-question/SKILL.md) - For coordinate graphs with tables
- [implement-custom-d3-question](../implement-custom-d3-question/SKILL.md) - For other custom SVG interactions

## Complete Working Example

```
courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/02/attachments/chart.js
```

This example includes:
- Static table showing the relationship
- Double number line with 4 input boxes
- Final answer input based on the completed number lines
- Two-part structure (Part 1: Complete number line, Part 2: Answer question)
