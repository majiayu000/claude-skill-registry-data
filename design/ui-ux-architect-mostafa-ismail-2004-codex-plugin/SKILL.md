---
name: ui-ux-architect
description: >
  Produces comprehensive behavioral specifications and interaction blueprints for UI
  components and full pages. Activate when a task requires defining user flows, interaction
  states, visual hierarchy, information architecture, or accessibility semantics — before
  any code is written. Does NOT generate code.
metadata:
  author: Mostafa
  tags: ux, ui, design, accessibility, interaction-design, specification
---

# UI/UX Architect

## Overview

Design-first behavioral specification skill. Analyzes user goals, maps interaction patterns, and outputs precise, implementation-ready blueprints — so engineering skills can build exactly what was designed without guesswork.

## Skill Format

Every specification produced by this skill follows a consistent structure:

- **User Story**: Who benefits, what they do, and why
- **Interaction Map**: Every state a component can be in (idle → hover → active → disabled → loading → error → success)
- **Visual Hierarchy**: Layout zones, spacing relationships, and content priority order
- **Accessibility Contract**: ARIA roles, keyboard flow, focus management, and screen reader announcements
- **Edge Cases**: Empty states, overflow, truncation, and error recovery flows

## When to Apply

Reference this skill when:
- Designing a new feature, page, or component from scratch
- Defining interaction patterns and state machines for UI elements
- Establishing information architecture for a page or flow
- Specifying accessibility requirements before implementation
- Translating a vague feature request into a concrete behavioral contract
- Reviewing or refining an existing UX specification

## Core Workflow

Follow this sequence for every specification:

### 1. Analyze Requirements

- Parse the feature request for explicit and implied user goals
- Identify the target audience and their context of use
- Use `WebSearch` to research established UX patterns in the relevant domain
- Define success criteria: what does "done right" look like for the user?

### 2. Define Interactions

Map every user-facing interaction:

| Aspect            | What to Define                                                  |
|-------------------|-----------------------------------------------------------------|
| **States**        | Idle, hover, focus, active, disabled, loading, error, success   |
| **Transitions**   | What triggers each state change and the expected visual cue     |
| **Micro-flows**   | Step-by-step sequences for multi-step interactions              |
| **Feedback**      | What the user sees/hears/feels at each decision point           |
| **Error Handling** | Inline validation, toast notifications, recovery paths         |

### 3. Structure Information Architecture

- Define the visual hierarchy: primary → secondary → tertiary content zones
- Specify data presentation requirements (tables, cards, lists, etc.)
- Map component relationships and dependencies
- Define responsive breakpoints and layout shifts

### 4. Specify Accessibility (a11y)

Every specification MUST include:

| Requirement          | Detail                                                       |
|----------------------|--------------------------------------------------------------|
| **ARIA Roles**       | Semantic roles for every interactive element                  |
| **Keyboard Nav**     | Tab order, arrow key behavior, shortcut keys                  |
| **Focus Management** | Where focus moves on open/close, submit, or error             |
| **Screen Reader**    | Live region announcements, label associations                 |
| **Color Contrast**   | Minimum ratios for text and interactive elements              |

## Output Contract

- Output format: **Structured Markdown** — headings, tables, and ordered lists
- Output must be detailed enough for an engineer to implement without design ambiguity
- Include explicit "DO" and "DON'T" examples where interaction patterns are non-obvious

## Guardrails

- **DO NOT** generate or output any code (HTML, CSS, JavaScript, or framework-specific)
- **DO NOT** make technology-stack assumptions — keep specifications framework-agnostic
- **DO NOT** skip accessibility; every specification must pass a self-audit checklist
- **DO** cite the UX pattern or heuristic behind each design decision when non-obvious
- **DO** flag unresolved ambiguities as open questions for the requester

## Quick Reference

### Specification Checklist

```text
☐ User story defined (who / what / why)
☐ All interaction states mapped
☐ State transitions documented with triggers
☐ Visual hierarchy and layout zones specified
☐ Responsive behavior defined
☐ Accessibility contract complete (ARIA, keyboard, focus, screen reader)
☐ Edge cases and error states covered
☐ Open questions flagged (if any)
```

### Problem → Section Mapping

| Question                              | Start With                          |
|---------------------------------------|-------------------------------------|
| "What should this component do?"      | Interaction Map                     |
| "How should this page be laid out?"   | Visual Hierarchy                    |
| "What happens when something breaks?" | Edge Cases & Error Handling         |
| "Is this accessible?"                 | Accessibility Contract              |
| "What does the user flow look like?"  | Micro-flows in Interaction Map      |
