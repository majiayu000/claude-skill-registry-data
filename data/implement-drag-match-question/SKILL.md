---
name: Implement Drag Match Question
description: Create D3 questions with drag-and-drop matching interactions. Students drag items (tables, graphs, equations) to categories.
---

# Implement Drag Match Question

Use this skill when creating questions where students:
- Drag items to match them with categories or labels
- Categorize or sort visual elements
- Match representations (tables, graphs, equations)

## When to Use This Pattern

**Perfect for:**
- "Match each table to the equation it represents"
- "Drag graphs to the descriptions that match"
- "Match scenarios to proportional relationships"
- Any "match X with Y" interaction
- Categorization tasks with 2+ categories

**Not suitable for:**
- Simple selection from options → use [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md)
- Fill-in-the-blank tables → use [implement-table-question](../implement-table-question/SKILL.md)
- Ordering/sequencing (use ordered list pattern instead)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Required
- `drag-match.js` → Full `createDragMatcher()` system (sophisticated!)
- `cards/standard-card.js` → `createStandardCard()`

### Optional
- `cards/explanation-card.js` → `createExplanationCard()` - For student explanations
- `cards/video-accordion.js` → `createVideoAccordion()` - For help videos
- `tables.js` → If rendering tables inside draggable items

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md)
2. **Study the working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/510-Proportion-Equations/questions/06/attachments/chart.js
   ```

## Key Implementation Decisions

1. **Define items** - What can be dragged? (tables, graphs, equations, text)
2. **Define categories** - Where can items be dropped? (2+ categories)
3. **Render function** - How to display each item (table, graph, simple text)
4. **State structure** - One array per category storing matched item IDs

## Data Structure

```javascript
const ITEMS = [
  { id: "item1", /* your item data */ },
  { id: "item2", /* your item data */ },
  { id: "item3", /* your item data */ },
];

const CATEGORIES = [
  { id: "cat1", text: "Category 1 description" },
  { id: "cat2", text: "Category 2 description" },
];
```

## State Shape

```javascript
function createDefaultState() {
  return {
    cat1Matches: [],  // Array of matched item IDs
    cat2Matches: [],
    explanation: ""
  };
}
```

## Core Pattern

```javascript
dragMatcher = createDragMatcher(d3, content, {
  items: ITEMS.map(item => ({
    id: item.id,
    content: (container) => renderItem(container, item),  // Custom render function
  })),
  categories: CATEGORIES.map(cat => ({
    id: cat.id,
    label: cat.text,
  })),
  state: {
    cat1: chartState.cat1Matches,
    cat2: chartState.cat2Matches,
  },
  onStateChange: (newState) => {
    chartState.cat1Matches = newState.cat1 || [];
    chartState.cat2Matches = newState.cat2 || [];
    sendChartState();
  },
  locked: interactivityLocked,
});
```

## Working Examples

**In codebase:**
- [IM-8th-Grade Ramp-Up-01 Q03](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/03/attachments/chart.js) - Match tables to movie download plans

**In this skill:**

## Common Variations

### Simple Text Items
For text-only items (not tables/graphs):
```javascript
items: ITEMS.map(item => ({
  id: item.id,
  content: item.text,  // String instead of render function
}))
```

### 3+ Categories
```javascript
function createDefaultState() {
  return {
    cat1Matches: [],
    cat2Matches: [],
    cat3Matches: [],
    explanation: ""
  };
}

dragMatcher = createDragMatcher(d3, content, {
  // ...
  state: {
    cat1: chartState.cat1Matches,
    cat2: chartState.cat2Matches,
    cat3: chartState.cat3Matches,
  },
});
```

### Custom Item Rendering (Tables, Graphs, Images)
```javascript
function renderTableItem(container, tableData) {
  // Use D3 to render a table
  const table = container.append("table")
    .style("width", "100%")
    .style("border-collapse", "collapse");

  // Add headers, rows, etc.
  // See working example for full implementation
}

items: ITEMS.map(item => ({
  id: item.id,
  content: (container) => renderTableItem(container, item.data),
}))
```

## Implementation Checklist

- [ ] Defined ITEMS array with unique IDs
- [ ] Defined CATEGORIES array
- [ ] Created render function for items (if complex)
- [ ] Created `createDefaultState()` with one array per category
- [ ] Implemented `createDragMatcher()` with `onStateChange` callback
- [ ] Added explanation card (if needed)
- [ ] Implemented `setInteractivity()` to call `dragMatcher.setLocked()`
- [ ] Implemented `applyInitialState()` to restore matches
- [ ] Tested dragging items between categories
- [ ] Tested removing items from categories
- [ ] Tested locking/unlocking
- [ ] Verified state restoration

## Tips

1. **Keep item rendering simple** - Complex DOM structures can slow down dragging
2. **Use clear category labels** - Students should know where to drag items
3. **Provide context** - Use intro cards to explain the matching task
4. **Test on mobile** - Drag-and-drop works on touch devices but test carefully
5. **Add visual feedback** - The component provides this, but ensure it's visible

## The createDragMatcher API

The `createDragMatcher` component is a complete drag-and-drop system. Key features:

- **Automatic drag handling** - No manual event listeners needed
- **Touch support** - Works on mobile devices
- **Visual feedback** - Highlights drop zones, shows drag state
- **Remove buttons** - Students can unmatch items
- **Lock support** - Disable dragging after submission via `.setLocked(true)`

**Important methods:**
- `dragMatcher.setLocked(boolean)` - Enable/disable dragging
- `dragMatcher.getState()` - Get current match state
- `dragMatcher.setState(newState)` - Update matches programmatically

## Related Skills

- [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md) - For simple selection
- [implement-table-question](../implement-table-question/SKILL.md) - For table completion
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [PATTERN.md](PATTERN.md) - Detailed pattern guide
- [snippets/drag-match.js](../snippets/drag-match.js) - Component source code
