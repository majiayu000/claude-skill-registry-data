---
name: syncfusion-vue-progressbar
description: Implement Syncfusion Vue Progressbar component for displaying task progress in linear, circular, or semi-circular shapes. Use this skill to create progress indicators with customizable animations, colors, segments, and annotations. Support for determinate and indeterminate states, tooltips, events, and full accessibility compliance.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Progress Components"
---

# Implementing Syncfusion Vue Progressbar

The Syncfusion Vue Progressbar component displays the progress of a task to the user. It can be visualized in multiple shapes (linear, circular) and supports advanced features like animations, custom colors, annotations, and real-time event handling.

## When to Use This Skill

Use the Progressbar component when you need to:
- Display task progress (downloads, file uploads, form submissions)
- Show real-time progress updates
- Indicate multi-step processes with segmented progress
- Display buffering or loading states
- Combine progress with annotations (percentage text, images, buttons)
- Track progress with custom ranges and multiple progress states
- Provide accessibility-compliant progress indicators

## Component Overview

**Key Capabilities:**
- Multiple shape types: Linear, Circular
- Progress states: Determinate (known progress), Indeterminate (unknown), Buffer (dual progress)
- Customizable appearance: Colors, thickness, radius, segments
- Annotations: Add custom content to circular progress bars
- Labels: Display progress percentage or custom text
- Tooltips: Show progress information on hover
- Events: React to progress changes and completion
- Accessibility: WCAG 2.2, Section 508, Screen reader support

**Package:** `@syncfusion/ej2-vue-progressbar`

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for ProgressBarComponent
- All properties, methods, events, and enums
- Data models and configuration objects
- Component registration examples (Composition API and Options API)
- Module injection and usage patterns
- 6 comprehensive common usage patterns with examples

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Import and component registration (both Composition API and Options API)
- Basic progressbar implementation
- Module injection for annotations
- First render and initialization

### Progress Types & Shapes
📄 **Read:** [references/progress-types.md](references/progress-types.md)
- Linear progressbar implementation
- Circular progressbar implementation
- When to use each type
- Size and dimension configuration
- Type selection guidelines

### Progress States
📄 **Read:** [references/progress-states.md](references/progress-states.md)
- Determinate state (when you know the total progress)
- Indeterminate state (for unknown progress)
- Buffer/Secondary progress (dual progress display)
- Switching between states
- State selection based on use cases

### Animation Configuration
📄 **Read:** [references/animation.md](references/animation.md)
- Enabling and disabling animations
- Duration and delay configuration
- Animation performance optimization
- Animation patterns

### Customization & Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Segmentation (dividing progress into parts)
- Thickness customization (track, progress, secondary)
- Radius and corner radius configuration
- Inner radius for donut-style progressbars
- Color customization and gradients
- Advanced styling patterns

### Annotations & Labels
📄 **Read:** [references/annotations-and-labels.md](references/annotations-and-labels.md)
- Adding annotations to circular progressbars
- Custom content (text, images, buttons)
- Progress value display and formatting
- Label styling and positioning
- Text rendering customization

### Tooltips
📄 **Read:** [references/tooltips.md](references/tooltips.md)
- Tooltip configuration and display
- Show on hover behavior
- Format customization
- Styling tooltips (colors, borders, text)

### Events & Value Range
📄 **Read:** [references/events-and-ranges.md](references/events-and-ranges.md)
- valueChanged event handling
- ProgressCompleted event
- Custom range configuration (minimum, maximum)
- Event patterns and best practices

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes
- Screen reader support
- Keyboard navigation
- Right-to-left (RTL) support

## Quick Start Example

```vue
<template>
  <div id="container">
    <ejs-progressbar
      id="percentage"
      type="Circular"
      :value="value"
      :animation="animation"
    >
    </ejs-progressbar>
  </div>
</template>

<script setup>
import { ProgressBarComponent as EjsProgressbar } from "@syncfusion/ej2-vue-progressbar";

const value = 100;
const animation = {
  enable: true,
  duration: 2000,
  delay: 0
};
</script>

<style>
#container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
```

## Common Patterns

### 1. Linear Progress with Animation
- Use for sequential tasks or download progress
- Set `type="Linear"` and configure animation duration
- Display percentage label with `showProgressValue`

### 2. Circular Progress with Annotation
- Use for circular task representation
- Inject `ProgressAnnotation` service
- Add custom content (percentage, icons, buttons) in center

### 3. Buffer/Secondary Progress
- Use for buffering scenarios (video streaming)
- Set `secondaryProgress` to show buffered amount
- Combine with animation for smooth transitions

### 4. Segmented Progress
- Use for multi-step processes
- Set `segmentCount` to divide progress bar
- Each segment represents a step

### 5. Indeterminate Progress
- Use when progress amount is unknown
- Set `isIndeterminate="true"`
- Useful for loading states before actual progress data arrives

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `value` | Number | Current progress value (0-100) |
| `type` | String | Shape: 'Linear', 'Circular' |
| `animation` | Object | Animation config (enable, duration, delay) |
| `isIndeterminate` | Boolean | Enable indeterminate mode |
| `secondaryProgress` | Number | Secondary progress value (0-100) |
| `segmentCount` | Number | Number of segments to divide progress |
| `showProgressValue` | Boolean | Display progress percentage/label |
| `minimum` | Number | Minimum value of range (default: 0) |
| `maximum` | Number | Maximum value of range (default: 100) |
| `progressColor` | String | Color of progress bar |
| `trackColor` | String | Color of track/background |
| `radius` | String | Radius for circular progressbars |
| `cornerRadius` | String | Corner style: 'Auro', 'Square', 'Round', 'Round4px' |
| `tooltip` | Object | Tooltip configuration (enable, format) |

## Common Use Cases

**Use Case 1: File Upload Progress**
- Linear progressbar with animation
- Update `value` prop as file uploads
- Show percentage with `showProgressValue`

**Use Case 2: Loading Indicator**
- Circular progressbar with indeterminate state
- Use when waiting for API response
- Transition to determinate once data arrives

**Use Case 3: Multi-Step Form**
- Linear segmented progressbar
- Update `value` as steps complete
- Use `segmentCount` to show total steps

**Use Case 4: Video Streaming**
- Linear progressbar with buffer (secondary progress)
- Primary progress = video playback
- Secondary progress = downloaded portion

**Use Case 5: Task Completion Dashboard**
- Circular progressbar with annotation
- Show percentage in center
- Add completion button in annotation

## Installation & Dependencies

```bash
npm install @syncfusion/ej2-vue-progressbar --save
```

**Minimum Dependencies:**
- @syncfusion/ej2-base
- @syncfusion/ej2-data
- @syncfusion/ej2-svg-base

## Next Steps

1. Choose your progressbar type: Linear or Circular
2. Select a progress state: Determinate, Indeterminate, or Buffer
3. Configure animations and visual appearance
4. Add labels or annotations if needed
5. Implement event handlers for progress updates
6. Test with accessibility tools

For detailed implementation of each feature, refer to the appropriate reference file from the navigation guide above.
