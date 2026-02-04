---
name: Implement Increment Controls Question
description: Create D3 questions with +/- button controls and emoji/visual displays. Common for ratio, mixture, and recipe problems where students adjust quantities.
---

# Implement Increment Controls Question

Use this skill when creating questions where students:
- Adjust quantities using increment/decrement buttons
- See visual feedback (emoji displays, diagrams)
- Explain their reasoning about ratios, mixtures, or recipes

## When to Use This Pattern

**Perfect for:**
- Drink mix ratio problems (🧂 salt, 🥛 water, 🍫 chocolate)
- Recipe scaling questions (🌾 flour, 🥚 eggs, 🧈 butter)
- Part-to-whole ratio explorations
- Comparing quantities/concentrations

**Not suitable for:**
- Questions requiring free-form numeric input → use [implement-table-question](../implement-table-question/SKILL.md)
- Questions with complex graphs → use [implement-graph-question](../implement-graph-question/SKILL.md)
- Drag-and-drop categorization → use [implement-drag-match-question](../implement-drag-match-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Cards (Required)
- `cards/standard-card.js` → `createStandardCard()`

### Cards (Optional)
- `cards/explanation-card.js` → `createExplanationCard()` - For student explanations
- `cards/video-accordion.js` → `createVideoAccordion()` - For help videos

### Form Inputs (Required)
- `form-inputs.js` → Increment/decrement button pattern

## Quick Start

1. **Study the working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/01/attachments/chart.js
   ```

2. **Customize the scenario data** (emojis, names, colors, ranges)
3. **Adjust the visualization** (emoji grid or SVG)
4. **Test locally** with `chart.html`

## Working Example

**Reference this codebase file:**
```bash
courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/01/attachments/chart.js
```

This example includes:
- ✅ Scenario constants setup (🥤 drink, 💧 water)
- ✅ State management with default values
- ✅ Increment/decrement controls for 2 items
- ✅ Emoji grid visualization
- ✅ Explanation card
- ✅ Full message protocol
- ✅ Interactivity locking

## Customization Points

### 1. Scenario Data
```javascript
const SCENARIO = {
  item1: { emoji: "🧂", name: "Salt", color: "#FFD700" },
  item2: { emoji: "🥛", name: "Water", color: "#87CEEB" },
  minValue: 0,
  maxValue: 20,
  initialValue1: 2,
  initialValue2: 5
};
```

### 2. State Shape
```javascript
function createDefaultState() {
  return {
    item1Count: SCENARIO.initialValue1,
    item2Count: SCENARIO.initialValue2,
    explanation: ""
  };
}
```

### 3. Visualization Style
- **Emoji grid** (simple, performant) - Most common
- **SVG diagram** (custom shapes) - For more complex visualizations

## Common Variations

### Two-Column Comparison
Display two mixtures side-by-side:
```javascript
const layout = container.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "1fr 1fr")
  .style("gap", "20px");
```

### Fraction/Ratio Display
Show the relationship as a fraction:
```javascript
fractionDiv.append("div").text(numerator);
fractionDiv.append("hr").style("width", "50px");
fractionDiv.append("div").text(denominator);
```

### Range Validation
Disable buttons at limits:
```javascript
.property("disabled", interactivityLocked || count <= MIN)
.style("opacity", count <= MIN ? 0.3 : 1);
```

## Implementation Checklist

- [ ] Copied template to question directory
- [ ] Updated scenario constants (emojis, names, colors, ranges)
- [ ] Customized visualization (emoji grid or SVG)
- [ ] Added explanation card (if needed)
- [ ] Tested increment/decrement at min/max boundaries
- [ ] Verified state restoration with `setInitialState`
- [ ] Tested interactivity locking
- [ ] Checked message payload structure
- [ ] Tested locally with chart.html

## Tips

1. **Keep it simple** - Emoji displays are faster and more accessible than complex SVG
2. **Label clearly** - Tell students what each button controls
3. **Show the ratio** - Display fractions, ratios, or percentages prominently
4. **Add context** - Use intro cards to set up the scenario
5. **Validate ranges** - Always check min/max before updating state

## Related Skills

- [implement-table-question](../implement-table-question/SKILL.md) - For ratio tables
- [implement-slider-question](../implement-slider-question/SKILL.md) - Alternative control style
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill
