---
name: Implement Multiple Choice Question
description: Create D3 questions with radio button selections and optional explanations. Students select from options and explain their reasoning.
---

# Implement Multiple Choice Question

Use this skill when creating questions where students:
- Select one option from a list of choices
- Choose between equations, statements, or concepts
- Make a selection and explain their reasoning

## When to Use This Pattern

**Perfect for:**
- "Which equation represents the relationship?"
- "Select the correct statement"
- "Choose the graph that matches..."
- Any single-selection question with explanations

**Not suitable for:**
- Multiple selections (checkboxes) → use standard checkbox pattern
- Drag-and-drop matching → use [implement-drag-match-question](../implement-drag-match-question/SKILL.md)
- Value entry → use [implement-table-question](../implement-table-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Required
- `cards/standard-card.js` → `createStandardCard()`

### Optional  
- `cards/explanation-card.js` → `createExplanationCard()` - For reasoning
- `cards/video-accordion.js` → `createVideoAccordion()` - For help videos

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md) (if exists)
2. **Study working examples**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/04/attachments/chart.js
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/06/attachments/chart.js
   ```

## Key Implementation Decisions

1. **Option display** - Simple text, equations, or visual cards?
2. **Selection style** - Radio buttons or clickable cards?
3. **State structure** - Store selected option ID
4. **Explanation requirement** - Required or optional?

## State Shape

```javascript
function createDefaultState() {
  return {
    selectedOption: null,  // ID of selected option
    explanation: ""
  };
}
```

## Core Pattern (Clickable Cards)

```javascript
const OPTIONS = [
  { id: "opt1", text: "y = 2x + 3", display: "\\(y = 2x + 3\\)" },
  { id: "opt2", text: "y = 3x + 2", display: "\\(y = 3x + 2\\)" },
  { id: "opt3", text: "y = x + 5", display: "\\(y = x + 5\\)" },
];

function renderOptions(container) {
  const optionsDiv = container.append("div")
    .style("display", "flex")
    .style("flex-direction", "column")
    .style("gap", "12px");

  OPTIONS.forEach(option => {
    const isSelected = chartState.selectedOption === option.id;

    const optionCard = optionsDiv.append("div")
      .style("padding", "16px")
      .style("border", isSelected ? "2px solid #3b82f6" : "1px solid #e5e7eb")
      .style("border-radius", "12px")
      .style("background", isSelected ? "#eff6ff" : "#ffffff")
      .style("cursor", interactivityLocked ? "default" : "pointer")
      .style("transition", "all 0.2s")
      .on("click", () => {
        if (interactivityLocked) return;
        chartState.selectedOption = option.id;
        renderOptions(container);  // Re-render to show selection
        sendChartState();
      });

    optionCard.append("div")
      .style("font-size", "18px")
      .html(option.display);
  });
}
```

## Core Pattern (Radio Buttons)

```javascript
function renderOptions(container) {
  const form = container.append("form");

  OPTIONS.forEach(option => {
    const label = form.append("label")
      .style("display", "block")
      .style("margin", "12px 0")
      .style("cursor", "pointer");

    label.append("input")
      .attr("type", "radio")
      .attr("name", "choice")
      .attr("value", option.id)
      .property("checked", chartState.selectedOption === option.id)
      .property("disabled", interactivityLocked)
      .on("change", function() {
        chartState.selectedOption = this.value;
        sendChartState();
      });

    label.append("span")
      .style("margin-left", "8px")
      .html(option.display);
  });
}
```

## Working Examples

**In codebase:**
- [IM-8th-Grade Ramp-Up-01 Q04](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/04/attachments/chart.js) - Equation selection
- [IM-8th-Grade Ramp-Up-01 Q06](../../../../../courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/06/attachments/chart.js) - Multiple choice with explanation

## Common Variations

### With Explanation Card
```javascript
createExplanationCard(d3, container, {
  prompt: "Explain why you selected this option.",
  value: chartState.explanation,
  onChange: (value) => {
    chartState.explanation = value;
    sendChartState();
  },
  locked: interactivityLocked
});
```

### Visual Options (Images/Graphs)
```javascript
OPTIONS.forEach(option => {
  const optionCard = optionsDiv.append("div");
  
  // Render graph or image
  if (option.type === "graph") {
    renderGraph(optionCard, option.data);
  } else if (option.type === "image") {
    optionCard.append("img").attr("src", option.imageUrl);
  }
});
```

### Grid Layout
```javascript
const optionsGrid = container.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "repeat(2, 1fr)")
  .style("gap", "16px");
```

## Implementation Checklist

- [ ] Defined OPTIONS array with unique IDs
- [ ] Created `createDefaultState()` with `selectedOption` field
- [ ] Rendered option cards or radio buttons
- [ ] Implemented click/change handlers to update state
- [ ] Added visual feedback for selected option
- [ ] Added explanation card (if needed)
- [ ] Implemented `setInteractivity()` to disable selection when locked
- [ ] Implemented `applyInitialState()` to restore selection
- [ ] Tested selection changes
- [ ] Tested state restoration
- [ ] Tested locking/unlocking

## Tips

1. **Clear visual feedback** - Make selected option obviously different
2. **Use MathJax/KaTeX** - For mathematical expressions in options
3. **Provide context** - Use intro cards to explain what students are selecting
4. **Test on mobile** - Ensure touch targets are large enough (min 44x44px)
5. **Require explanation** - Helps prevent guessing, encourages reasoning

## Styling Tips

**Hover effects:**
```javascript
.on("mouseover", function() {
  if (!interactivityLocked) {
    d3.select(this).style("background", "#f9fafb");
  }
})
.on("mouseout", function() {
  const isSelected = /* check selection */;
  d3.select(this).style("background", isSelected ? "#eff6ff" : "#ffffff");
})
```

**Focus states for accessibility:**
```javascript
optionCard
  .attr("tabindex", "0")
  .on("keypress", (event) => {
    if (event.key === "Enter" && !interactivityLocked) {
      chartState.selectedOption = option.id;
      renderOptions(container);
      sendChartState();
    }
  });
```

## Related Skills

- [implement-text-response-question](../implement-text-response-question/SKILL.md) - For selection + explanation focus
- [implement-drag-match-question](../implement-drag-match-question/SKILL.md) - For matching multiple items
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [snippets/form-inputs.js](../snippets/form-inputs.js) - Form input patterns
- [snippets/cards/standard-card.js](../snippets/cards/standard-card.js) - Card styling
