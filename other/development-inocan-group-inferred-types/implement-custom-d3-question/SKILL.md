---
name: Implement Custom D3 Question
description: Create D3 questions with unique, non-standard interactions. Fallback skill for questions not fitting standard patterns.
---

# Implement Custom D3 Question

Use this skill when creating questions that don't fit standard patterns. For unique visualizations or complex custom interactions.

## When to Use This Pattern

**Use when:**
- Question requires truly unique interactions
- None of the standard patterns fit
- Complex custom visualization needed
- Multiple interaction types combined in novel ways

**Try standard patterns first:**
- [implement-increment-controls-question](../implement-increment-controls-question/SKILL.md)
- [implement-table-question](../implement-table-question/SKILL.md)
- [implement-drag-match-question](../implement-drag-match-question/SKILL.md)
- [implement-slider-question](../implement-slider-question/SKILL.md)
- [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md)
- [implement-text-response-question](../implement-text-response-question/SKILL.md)
- [implement-graph-question](../implement-graph-question/SKILL.md)

## Components Available

All components in `.claude/skills/question-types/snippets/` can be mixed and matched:

- `cards/` - Standard cards, video players, explanation cards
- `form-inputs.js` - Buttons, inputs, textareas
- `tables.js` - D3 tables
- `drag-match.js` - Drag-and-drop system
- `svg-basics.js` - SVG shapes and diagrams

## Core Architecture Requirements

All D3 questions MUST implement these patterns:

### 1. State Management
```javascript
function createDefaultState() {
  return {
    // All student response data
  };
}

let chartState = createDefaultState();
```

### 2. Message Protocol
```javascript
function sendChartState() {
  sendMessage("response_updated", {
    // Send complete state
  });
}

// Call after EVERY state change
```

### 3. Interactivity Locking
```javascript
let interactivityLocked = false;

function setInteractivity(enabled) {
  interactivityLocked = !enabled;
  // Update all interactive elements
}
```

### 4. State Restoration
```javascript
function applyInitialState(payload) {
  if (!payload) return;
  // Restore state from payload
  chartState = { ...createDefaultState(), ...payload };
}
```

### 5. Message Handlers
```javascript
window.addEventListener("message", (event) => {
  const { data } = event;
  if (!data || typeof data !== "object") return;

  if (data.type === "setInitialState") {
    applyInitialState(data.payload);
    renderFromState(d3);
  }

  if (data.type === "set_lock") {
    setInteractivity(data.payload === false);
  }

  if (data.type === "check_answer") {
    sendChartState();
  }
});
```

## Implementation Guide

See [PATTERN.md](PATTERN.md) for detailed custom implementation guide.

## Reference Example

Study existing questions for patterns:
```bash
# Find all D3 questions
find courses/ -name "chart.js" -type f

# Look for unique patterns
grep -r "createChart" courses/ | head -5
```

## Checklist

- [ ] Defined `createDefaultState()`
- [ ] Implemented `sendChartState()` with complete payload
- [ ] Called `sendChartState()` after every state change
- [ ] Implemented `setInteractivity(enabled)`
- [ ] Implemented `applyInitialState(payload)`
- [ ] Set up message event listeners
- [ ] Implemented `window.clearChart()`
- [ ] Implemented `window.getSvg()` (if using SVG)
- [ ] Tested state restoration
- [ ] Tested interactivity locking
- [ ] Verified message protocol

## Tips

1. **Start simple** - Build incrementally
2. **Borrow liberally** - Copy patterns from existing questions
3. **Test frequently** - Use chart.html for local testing
4. **Document state** - Comment what each state field represents
5. **Inline components** - All components must be inlined in chart.js

## Related Skills

- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill
- All other question-type skills for standard patterns

## Additional Resources

- [PATTERN.md](PATTERN.md) - Custom visualization pattern guide
- [../snippets/](../snippets/) - All reusable components
- [../../implement-d3-conversion/](../../implement-d3-conversion/) - Original conversion skill
