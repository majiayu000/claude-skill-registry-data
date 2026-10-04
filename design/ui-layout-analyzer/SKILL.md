---
name: ui-layout-analyzer
description: Use when analyzing a UI screenshot to describe layout structure and interface functionality.
---

# UI Layout Analyzer

## Overview

Analyze a provided UI screenshot and output a structured layout description plus functional analysis. The skill focuses on interface screenshots, describing page structure, visual sections, hierarchy, controls, and likely user workflows without designing new UI or reviewing implementation code.

## When to Use

Use this skill when the user provides a UI image and requests analysis.

## Do not use

Do not use this skill for:
- Non-UI images (photos, diagrams, charts that are not interface screenshots)
- Requests to design or create UI (use ui-ux-pro-max instead)
- Code review of UI implementation (use code-reviewer instead)

## Instructions

Follow this format exactly:

```markdown
## UI Layout Description

### Overall Structure
Describe the overall structure type (modal dialog/full page/sidebar/drawer), background color, rounded corners, shadows, etc. End with "---".

---

### Section N: Section Name
- Specific description items
- Use bullet points for key elements

[Continue describing each section...]

---

## Function Description

| Function Module | Description |
|---|---|
| **Module Name** | Function description |
```

## Analysis Steps

### 1. Identify Overall Structure
- Page type: Modal dialog / Full page / Sidebar / Bottom drawer
- Background: White/gray/gradient/image background
- Special elements: Rounded corners, shadows, borders, dividers

### 2. Divide into Sections
Identify sections top to bottom, each containing:
- Section type: Header / Tab bar / Content area / List / Table / Input area / Action bar
- Key elements: Icons, text, buttons, input fields
- Layout: Left-aligned/centered/right-aligned, horizontal/vertical

### 3. Identify Interactive Elements
- Buttons: Primary (filled) / Secondary (text) / Icon buttons
- Inputs: Single-line/multiline text/dropdown/date picker
- Selectors: Radio/checkbox/switch/tab switch
- Lists: List items, grid layout, card layout

### 4. Describe Functions
Infer functions from visual elements:
- Form: Input, validation, submit
- Navigation: Jump, tab switch, back
- Display: List, detail, carousel
- Feedback: Toast, modal, loading state

## Notes

- Recognize and include all text visible in the image
- Mark states (disabled/selected/expanded) when visible
- Use Arabic numerals for section numbers (1, 2, 3...)
- Keep descriptions concise but complete
