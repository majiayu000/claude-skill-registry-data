---
name: Implement Text Response Question
description: Create D3 questions focused on written explanations and reflections of static content (text, images, diagrams). For video-based questions, use implement-video-question instead.
---

# Implement Text Response Question

Use this skill when creating questions where students:
- Analyze static content (text, diagrams, images) and explain their thinking
- Provide open-ended text responses without complex interactions
- Reflect on scenarios presented via text or static visuals

**Note:** For questions where students watch a video and respond, use [implement-video-question](../implement-video-question/SKILL.md) instead.

## When to Use This Pattern

**Perfect for:**
- "Explain your thinking" questions with minimal interaction
- Analysis of static diagrams, images, or scenarios
- Open-ended written responses to text-based prompts
- Reflection questions without video content

**Not suitable for:**
- Video-based questions → use [implement-video-question](../implement-video-question/SKILL.md)
- Questions with interactive controls → use other question-type skills
- Multiple choice → use [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md)
- Table completion → use [implement-table-question](../implement-table-question/SKILL.md)

## Components Required

**Copy these from** `.claude/skills/question-types/snippets/`:

### Required
- `cards/standard-card.js` → `createStandardCard()`
- `cards/explanation-card.js` → `createExplanationCard()`

### Optional
- `cards/video-accordion.js` → `createVideoAccordion()` - For optional help videos (not primary content)
- `svg-basics.js` → For rendering static diagrams

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md)
2. **Use cards directly** - No specific snippet needed, just combine `createStandardCard()` and `createExplanationCard()`
3. **For video-based questions** - Use [implement-video-question](../implement-video-question/SKILL.md) instead

## Key Implementation Decisions

1. **Content type** - Static image, diagram, or text scenario? (Not video - use implement-video-question for that)
2. **Number of responses** - Single textarea or multiple questions?
3. **State structure** - One field per text response
4. **Required length** - Minimum characters? Word count?

## State Shape

```javascript
function createDefaultState() {
  return {
    response1: "",
    response2: "",  // If multiple questions
    explanation: ""
  };
}
```

## Core Pattern (Text/Diagram + Reflection)

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("").style("padding", "20px").style("overflow", "auto");

  // Intro card with scenario
  const introCard = createStandardCard(d3, container, {
    size: "large",
    title: "Analyze the Scenario"
  });
  introCard.append("p").text("Read the scenario below and answer the question.");

  // Add static content (text scenario, diagram, image)
  introCard.append("p")
    .style("background", "#f3f4f6")
    .style("padding", "15px")
    .style("border-radius", "8px")
    .text("Maria is planning a party. She needs to buy cups and plates...");

  // Response card
  createExplanationCard(d3, container, {
    prompt: "Explain your reasoning for Maria's best choice.",
    placeholder: "Type your answer here...",
    value: chartState.explanation,
    onChange: (value) => {
      chartState.explanation = value;
      sendChartState();
    },
    locked: interactivityLocked
  });
}
```

## Core Pattern (Static Content + Analysis)

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("").style("padding", "20px").style("overflow", "auto");

  // Display static content (diagram, scenario)
  const contentCard = createStandardCard(d3, container, {
    size: "large",
    title: "Analyze the Diagram"
  });

  // Add SVG or image
  const svg = contentCard.append("svg")
    .attr("width", 400)
    .attr("height", 300);
  // ... render diagram ...

  // Text response
  createExplanationCard(d3, container, {
    prompt: "Explain what the diagram shows about the relationship.",
    value: chartState.explanation,
    onChange: (value) => {
      chartState.explanation = value;
      sendChartState();
    },
    locked: interactivityLocked,
    rows: 6  // Larger textarea for detailed responses
  });
}
```

## Note on Video Questions

**This question type is for text/diagram-based responses only.**

If your question includes a video as the primary instructional content, use [implement-video-question](../implement-video-question/SKILL.md) instead.

| Use Text Response | Use Video Question |
|-------------------|-------------------|
| Static text scenario | Video is primary content |
| Diagram analysis | Watch and reflect |
| Image analysis | Video-based instruction |
| No video content | Video + written response |

## Common Variations

### Multiple Text Responses
```javascript
function createDefaultState() {
  return {
    answer1: "",
    answer2: "",
    answer3: ""
  };
}

// Render multiple explanation cards
questions.forEach((q, i) => {
  createExplanationCard(d3, container, {
    prompt: `${i + 1}. ${q.text}`,
    value: chartState[`answer${i + 1}`],
    onChange: (value) => {
      chartState[`answer${i + 1}`] = value;
      sendChartState();
    },
    locked: interactivityLocked
  });
});
```

### With Character/Word Count
```javascript
const textarea = container.append("textarea");
const counter = container.append("div")
  .style("text-align", "right")
  .style("color", "#6b7280")
  .style("font-size", "14px");

textarea.on("input", function() {
  const length = this.value.length;
  counter.text(`${length} characters`);
  chartState.response = this.value;
  sendChartState();
});
```

### Numbered Questions in Cards
```javascript
QUESTIONS.forEach((question, index) => {
  const qCard = createStandardCard(d3, container, {
    size: "medium",
    title: `Question ${index + 1}`
  });

  qCard.append("p").text(question.prompt);

  qCard.append("textarea")
    .attr("rows", 4)
    .style("width", "100%")
    .property("value", chartState[`q${index + 1}`])
    .on("input", function() {
      chartState[`q${index + 1}`] = this.value;
      sendChartState();
    });
});
```

## Implementation Checklist

- [ ] Created `createDefaultState()` with response fields
- [ ] Added intro content (video, image, or text scenario)
- [ ] Created explanation card(s) for text responses
- [ ] Implemented `onChange` handlers to update state
- [ ] Added clear prompts for each response
- [ ] Implemented `setInteractivity()` to disable textareas when locked
- [ ] Implemented `applyInitialState()` to restore text values
- [ ] Tested state restoration
- [ ] Tested locking/unlocking
- [ ] Verified all text is preserved

## Tips

1. **Clear prompts** - Tell students exactly what to explain
2. **Adequate space** - Use `rows` attribute to provide enough textarea height
3. **Placeholder text** - Give examples of what to write
4. **Auto-save** - State updates on every input (already handled by onChange)
5. **Scroll support** - Ensure container has `overflow: auto`

## Static Diagram Integration

Using SVG for static diagrams:
```javascript
const diagramCard = createStandardCard(d3, container, {
  size: "large",
  title: "Study the Diagram"
});

const svg = diagramCard.append("svg")
  .attr("width", 400)
  .attr("height", 300);

// Add diagram elements
svg.append("rect")
  .attr("x", 50)
  .attr("y", 50)
  .attr("width", 100)
  .attr("height", 100)
  .attr("fill", "#3b82f6");

svg.append("text")
  .attr("x", 100)
  .attr("y", 180)
  .text("Area = 100 sq units");
```

## Related Skills

- [implement-video-question](../implement-video-question/SKILL.md) - For video-based questions
- [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md) - For selection + explanation
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [PATTERN.md](PATTERN.md) - Detailed pattern guide
- [../snippets/cards/explanation-card.js](../snippets/cards/explanation-card.js) - Explanation card component
- [../snippets/cards/standard-card.js](../snippets/cards/standard-card.js) - Standard card component
- [../snippets/svg-basics.js](../snippets/svg-basics.js) - SVG diagram helpers
