---
name: report-uxui
description: Build a UX/UI report with ANSI box-drawing for an app/website from the given context
argument-hint: "[scope]"
related:
  - report-uxui-all-routes
  - draw-ansi
  - report
  - report-architecture-diagram
  - follow-design-system
  - review-by-all-stakeholder
  - ask-me
  - suggest-next-action
  - open-files-in-web
  - run-dev
---

## Goal

Build a UX/UI report for an app or website from the context the user gives, presenting layout, tabs, components, and user flow as ANSI box-drawing wireframes (uniform width, right borders aligned) in a ` ```text ` codeblock

## Scope

- For UX/UI sketches before implementing, or summarizing the UI of an existing project
- Supports mobile apps, web apps, desktop apps
- Shows tab/session/screen layouts, navigation, list items, buttons
- No images — ANSI/Unicode box-drawing in a ` ```text ` block only

## Execute

### 1. Gather Context

> Goal: Understand the app/website to sketch

1. Read the prompt, context, `AGENTS.md`, or related references
2. Identify the platform (iOS, Android, Web, Desktop), framework, and screen size
3. Identify the tabs, screens, main features, and target users
4. If source code exists → scan the real routes/pages/components before sketching
5. If context is insufficient → use `/ask-me`

### 2. Define Screens And Flow

> Goal: Split the app into clear screens/tabs

1. List all tab/screen names
2. Define the main flow: open app → which tab → what is pressed
3. Define the transitions between screens
4. Group screens by bottom/tab navigation

### 3. Sketch Each Screen As ANSI

> Goal: Draw each screen's wireframe as an ANSI box

1. Use box-drawing characters (`┌─┐│└─┘├┤`) inside a ` ```text ` codeblock
2. Every screen must have an outer box of equal width on every line, with the right border `│` aligned
3. Show the status bar, navigation bar, and tab bar for mobile
4. Include labels, placeholders, list items, and buttons
5. Mark working "presses" or taps: `[Tap]`, `[Press]`
6. No line wider than 80 characters
7. If a box is distorted or content needs wrapping → use the `/draw-ansi` script (`--fix`, `--width`, `--title`) to even out sizes

### 4. Add UX Annotations

> Goal: Explain each element's behavior

1. Use bullets/numbered lists to describe interactions
2. State loading, empty, and error states
3. State gestures (swipe, pull-to-refresh) if any
4. State accessibility labels

### 5. Format As ANSI Report

> Goal: Summarize the report for easy reading

1. Summarize key findings at the top
2. Use `/report` for the screen/tab summary table
3. Use `/report-architecture-diagram` for the user flow
4. Use symbols `✅` `⚠️` for status
5. Run `/suggest-next-action` at the end of the report

## Rules

### ANSI-Only Sketch

- Do not create images or binary files
- Use ANSI/Unicode box-drawing in a ` ```text ` codeblock only (no ` ```ansi ` blocks)
- Every box must be uniform width — right borders aligned, undistorted, per `/draw-ansi` rules
- One screen per sketch section
- If a route table is needed before sketching, use `/report-uxui-all-routes`

### Mobile Layout

- Show the top status bar, middle content, and bottom tab bar for mobile
- Use `Tab 1 | Tab 2 | Tab 3` for the tab bar
- State safe areas and the navigation header when needed

### Web/Desktop Layout

- Show the sidebar/top nav and main content area
- State breakpoints if there is responsive design
- Separate global nav from local nav

### Interactions

- Mark tap/click targets clearly, e.g. `[Tap]`, `[Press]`, `[Toggle]`
- Mark disabled states with `[Disabled]`
- Mark transitions, e.g. `→ Screen B`

### Formatting

- Use backticks for `tools`, `commands`, `paths`, `screen-name`
- Never use `**` bold markers
- Lines no longer than 80 characters
- Use headings to separate each screen

### Consistency

- Use the same terminology throughout the report
- Order tabs/screens by navigation sequence
- Every screen must carry its name and purpose

- Use /report-uxui-all-routes if needed
- Use /draw-ansi if needed
- Use /follow-design-system if needed
- Use /review-by-all-stakeholder if needed
- Use /open-files-in-web if needed
- Use /run-dev if needed

- Final report via `/report-review` — one chat table (No./Action/Evidence/Severity/Risk/Priority/Owner skill/Status), no report files

## Expected Outcome

- An ANSI UX/UI report covering every screen/tab with all boxes equal-sized and undistorted
- A screen summary table via `/report`
- A user flow or navigation diagram via `/report-architecture-diagram`
- Clear interactions, loading/empty/error states, and accessibility notes
- A clear next action at the end of the report
