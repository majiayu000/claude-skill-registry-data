---
name: Implement Table Question
description: Create D3 questions with fill-in-the-blank tables. Students complete missing values based on patterns, rates, or relationships.
---

# Implement Table Question

Use this skill when creating questions where students:
- Fill in missing table values
- Complete ratio or rate tables
- Enter values based on patterns or proportional relationships

## When to Use This Pattern

**Perfect for:**
- "Complete the table showing costs for different months"
- "Fill in the missing values for this proportional relationship"
- "Complete the rate table"
- Any table with editable cells for data entry

**Not suitable for:**
- Tables with interactive graphs → use [implement-graph-question](../implement-graph-question/SKILL.md)
- Drag-and-drop table matching → use [implement-drag-match-question](../implement-drag-match-question/SKILL.md)
- Simple numeric adjustments → use [implement-increment-controls-question](../implement-increment-controls-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Required
- `tables.js` → Custom D3 table patterns (most common)
- `cards/standard-card.js` → `createStandardCard()`

### Optional
- `cards/explanation-card.js` → `createExplanationCard()` - For student explanations
- `cards/video-accordion.js` → `createVideoAccordion()` - For help videos

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md)
2. **Study the working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/05/attachments/chart.js
   ```

## Key Implementation Decisions

1. **Custom D3 table vs HTML table** - D3 for complex styling, HTML for simplicity
2. **Which cells are editable** - Define which cells have inputs
3. **State structure** - One field per editable cell
4. **Input validation** - Numeric only? Allow decimals? Constraints?

## State Shape

```javascript
function createDefaultState() {
  return {
    cell1: "",  // One field per editable cell
    cell2: "",
    cell3: "",
    cell4: "",
    explanation: ""
  };
}
```

## Core Pattern (HTML Table - Simplest)

```javascript
function renderTable(container) {
  const tableHtml = `
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>Months</th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Cost ($)</td>
          <td>0</td>
          <td><input type="text" id="cell1" value="${chartState.cell1}"></td>
          <td><input type="text" id="cell2" value="${chartState.cell2}"></td>
          <td><input type="text" id="cell3" value="${chartState.cell3}"></td>
        </tr>
      </tbody>
    </table>
  `;

  container.html(tableHtml);

  // Bind input events
  container.select("#cell1").on("input", function() {
    chartState.cell1 = this.value;
    sendChartState();
  });
  // Repeat for other cells...
}
```

## Core Pattern (D3 Table - More Control)

See [snippets/tables.js](../snippets/tables.js) for full D3 table implementation with:
- Custom styling
- Conditional input rendering
- Numeric validation
- Disabled state handling

## Working Examples

**In codebase:**
- [IM-8th-Grade Ramp-Up-01 Q02](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/02/attachments/chart.js) - Table with graph
- [IM-8th-Grade Ramp-Up-01 Q05](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/05/attachments/chart.js) - Rate table completion

**Working example:**
```bash
courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/05/attachments/chart.js
```

## Common Variations

### Multiple Rows Editable
```javascript
function createDefaultState() {
  return {
    // Row 1
    row1_col1: "",
    row1_col2: "",
    // Row 2
    row2_col1: "",
    row2_col2: "",
    explanation: ""
  };
}
```

### Mixed Given/Editable Cells
```javascript
<tr>
  <td>Distance</td>
  <td>0</td>  <!-- Given -->
  <td><input id="cell1"></td>  <!-- Editable -->
  <td><input id="cell2"></td>  <!-- Editable -->
  <td>100</td>  <!-- Given -->
  <td><input id="cell3"></td>  <!-- Editable -->
</tr>
```

### Numeric Validation
```javascript
container.select("#cell1").on("input", function() {
  let value = this.value;
  // Allow only numbers and decimals
  value = value.replace(/[^0-9.]/g, '');
  this.value = value;
  chartState.cell1 = value;
  sendChartState();
});
```

### Two-Column Layout (Table + Context)
```javascript
const layout = container.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "1fr 1fr")
  .style("gap", "20px");

const leftColumn = layout.append("div");
const rightColumn = layout.append("div");

// Context/instructions in left column
// Table in right column
```

## Implementation Checklist

- [ ] Defined table headers (column labels)
- [ ] Defined row data with editable cells identified
- [ ] Created `createDefaultState()` with one field per editable cell
- [ ] Implemented input event handlers
- [ ] Mapped input values to correct state fields
- [ ] Added numeric validation (if needed)
- [ ] Added explanation card (if needed)
- [ ] Implemented `applyInitialState()` to restore cell values
- [ ] Implemented `setInteractivity()` to disable inputs when locked
- [ ] Tested state restoration
- [ ] Tested locking/unlocking

## Tips

1. **Use `inputmode="numeric"`** on mobile for better keyboard
   ```html
   <input type="text" inputmode="numeric">
   ```

2. **Provide clear labels** - Header row should explain what each column represents

3. **Show units** - Include units in headers or cell labels (e.g., "Cost ($)", "Time (hours)")

4. **Validate inputs** - Strip non-numeric characters if expecting numbers

5. **Give context** - Use intro cards or instructions to explain the table task

## When to Use HTML vs D3 Tables

**Use HTML tables when:**
- Simple, standard table layout
- Minimal styling needed
- Want less code
- Standard browser table behavior is fine

**Use D3 tables when:**
- Need custom styling (colors, borders, backgrounds)
- Complex cell interactions
- Dynamic row/column additions
- Special formatting or layouts
- See [snippets/tables.js](../snippets/tables.js) for D3 patterns

## Related Skills

- [implement-graph-question](../implement-graph-question/SKILL.md) - For tables with coordinating graphs
- [implement-increment-controls-question](../implement-increment-controls-question/SKILL.md) - For quantity adjustments
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [PATTERN.md](PATTERN.md) - Detailed pattern guide
- [snippets/tables.js](../snippets/tables.js) - D3 table component patterns
