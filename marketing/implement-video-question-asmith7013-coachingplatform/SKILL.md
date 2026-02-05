---
name: Implement Video Question
description: Create D3 questions where students watch a video and provide written responses. The video is the primary instructional content.
---

# Implement Video Question

Use this skill when creating questions where students:
- Watch a video as the primary instructional content
- Provide written reflections based on the video
- Answer questions about what they observed in the video

## When to Use This Pattern

**Perfect for:**
- "Watch this video and explain the main concept"
- Video-based instruction followed by reflection questions
- Visual demonstrations requiring written analysis
- Questions where the video IS the lesson content

**Not suitable for:**
- Text-only reflections without video → use [implement-text-response-question](../implement-text-response-question/SKILL.md)
- Video as optional help/hint → use `createVideoAccordion()` from shared snippets
- Interactive controls + optional video help → use other question types with video accordion

## Distinction from Text Response Questions

| Feature | Video Question | Text Response Question |
|---------|---------------|------------------------|
| Primary content | Video is the lesson | Static text/images or no media |
| Video role | Required, main instruction | Optional or absent |
| Interaction | Watch → Respond | Read/Analyze → Respond |
| Snippet | video-response.js | No snippet (uses cards directly) |

## Components Required

**Copy these from** `.claude/skills/question-types/`:

### Required
- `implement-video-question/snippets/video-response.js` → `createVideoResponseQuestion()`
- `snippets/cards/standard-card.js` → `createStandardCard()`
- `snippets/cards/video-player.js` → `createVideoPlayer()`
- `snippets/cards/explanation-card.js` → `createExplanationCard()`

## Quick Start

1. **Review the pattern guide**: [PATTERN.md](PATTERN.md)
2. **Study the snippet**: [snippets/video-response.js](snippets/video-response.js)
3. **Copy from a working example**:
   ```bash
   cat courses/IM-8th-Grade/modules/Unit-3/assignments/161-Proportion-Graphs/questions/01/attachments/chart.js
   ```

## Working Examples

**Reference these codebase files:**
```bash
courses/IM-8th-Grade/modules/Unit-3/assignments/161-Proportion-Graphs/questions/01/attachments/chart.js
courses/IM-8th-Grade/modules/Unit-3/assignments/510-Proportion-Equations/questions/01/attachments/chart.js
courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-2/questions/01/attachments/chart.js
```

These examples include:
- ✅ Video player with embedded video
- ✅ Explanation card for written response
- ✅ State management for response field
- ✅ Full message protocol
- ✅ Interactivity locking

## State Shape

```javascript
function createDefaultState() {
  return {
    explanation: ""
  };
}
```

For multiple questions:
```javascript
function createDefaultState() {
  return {
    response1: "",
    response2: "",
    response3: ""
  };
}
```

## Implementation Pattern (Single Response)

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("").style("padding", "20px").style("overflow", "auto");

  createVideoResponseQuestion(d3, container, {
    videoUrl: "https://example.com/video.mp4",
    videoDescription: "Watch this explanation of proportional relationships",
    promptText: "What is the main concept explained in the video?",
    placeholderText: "Describe the main concept in your own words...",
    responseRows: 6,
    stateKey: "explanation",
    locked: interactivityLocked,
    introTitle: "Video Reflection",
    introContent: "Watch the video carefully and answer the question below."
  });
}
```

## Implementation Pattern (Multiple Responses)

```javascript
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("").style("padding", "20px").style("overflow", "auto");

  // Intro
  const introCard = createStandardCard(d3, container, {
    size: "large",
    title: "Video Reflection"
  });
  introCard.append("p").text("Watch the video and answer the questions below.");

  // Video
  createVideoPlayer(d3, container, "https://example.com/video.mp4", {
    description: "Proportional relationships explained"
  });

  // Multiple response cards
  const questions = [
    { prompt: "1. What is the main concept?", key: "response1" },
    { prompt: "2. How does this relate to what you know?", key: "response2" },
    { prompt: "3. Give an example from real life.", key: "response3" }
  ];

  questions.forEach(q => {
    createExplanationCard(d3, container, {
      prompt: q.prompt,
      value: chartState[q.key] || "",
      onChange: (value) => {
        chartState[q.key] = value;
        sendChartState();
      },
      locked: interactivityLocked,
      rows: 4
    });
  });
}
```

## Configuration Options

### Video Player Options
```javascript
{
  videoUrl: "https://example.com/video.mp4",  // Required
  videoDescription: "Watch this...",           // Shown above player
  autoplay: false,                             // Default: false
  controls: true                               // Default: true
}
```

### Response Card Options
```javascript
{
  promptText: "Question text",           // Required
  placeholderText: "Type here...",       // Optional
  responseRows: 6,                       // Textarea height (default: 6)
  stateKey: "explanation",               // Required - key in chartState
  locked: interactivityLocked            // Required - current lock state
}
```

### Optional Intro Card
```javascript
{
  introTitle: "Video Reflection",        // Optional
  introContent: "Instructions..."        // Optional
}
```

## Video Hosting Best Practices

1. **Supported formats**: MP4 (recommended), WebM
2. **Hosting**: Use CDN or cloud storage for best performance
3. **File size**: Keep videos under 50MB when possible
4. **Encoding**: H.264 codec for MP4, VP9 for WebM
5. **Accessibility**: Ensure videos have captions when possible

## Common Variations

### Character Count Display
```javascript
const textarea = container.append("textarea");
const counter = container.append("div")
  .style("text-align", "right")
  .style("color", "#6b7280")
  .style("font-size", "14px");

textarea.on("input", function() {
  const length = this.value.length;
  counter.text(`${length} characters`);
  chartState.explanation = this.value;
  sendChartState();
});
```

### Numbered Questions in Separate Cards
```javascript
const QUESTIONS = [
  { prompt: "What is the main concept?", placeholder: "Main concept..." },
  { prompt: "How does this relate to ratios?", placeholder: "Connection..." }
];

QUESTIONS.forEach((q, index) => {
  const qCard = createStandardCard(d3, container, {
    size: "medium",
    title: `Question ${index + 1}`
  });

  qCard.append("p").text(q.prompt);

  qCard.append("textarea")
    .attr("rows", 4)
    .style("width", "100%")
    .attr("placeholder", q.placeholder)
    .property("value", chartState[`q${index + 1}`])
    .on("input", function() {
      chartState[`q${index + 1}`] = this.value;
      sendChartState();
    });
});
```

## Implementation Checklist

- [ ] Copied `video-response.js` snippet into chart.js
- [ ] Copied required card components (standard-card, video-player, explanation-card)
- [ ] Created `createDefaultState()` with response field(s)
- [ ] Configured video URL and description
- [ ] Configured prompt text and placeholder
- [ ] Set correct stateKey for response
- [ ] Tested video playback in browser
- [ ] Tested state restoration
- [ ] Tested interactivity locking
- [ ] Verified response text is preserved
- [ ] Checked video loads and plays correctly

## Tips

1. **Clear prompts** - Tell students exactly what to observe and explain
2. **Adequate textarea height** - Use `responseRows` attribute (6+ for detailed responses)
3. **Placeholder guidance** - Show students what kind of response you expect
4. **Video length** - Keep videos under 3-5 minutes for best engagement
5. **Intro context** - Set expectations before the video plays
6. **Auto-save** - State updates automatically on every input (no submit button needed)

## State Management

### Initialization
```javascript
function createDefaultState() {
  return {
    explanation: ""
  };
}
```

### State Restoration
```javascript
function applyInitialState(state) {
  Object.assign(chartState, state);
  buildLayout(d3, containerSelector);
}
```

### Interactivity Control
```javascript
function setInteractivity(enabled) {
  interactivityLocked = !enabled;
  buildLayout(d3, containerSelector);
}
```

## Related Skills

- [implement-text-response-question](../implement-text-response-question/SKILL.md) - For text-only reflections without video
- [implement-multiple-choice-question](../implement-multiple-choice-question/SKILL.md) - For video + selection instead of text
- [create-d3-question](../../create-d3-question/SKILL.md) - Parent workflow skill

## Additional Resources

- [PATTERN.md](PATTERN.md) - Visual pattern guide
- [snippets/video-response.js](snippets/video-response.js) - Complete snippet with examples
- [../snippets/cards/video-player.js](../snippets/cards/video-player.js) - Video player component
- [../snippets/cards/explanation-card.js](../snippets/cards/explanation-card.js) - Explanation card component
