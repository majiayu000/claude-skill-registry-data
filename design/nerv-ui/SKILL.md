---
name: nerv-ui
description: Build original, accessible React command-center interfaces with the published @mdrbx/nerv-ui component library. Use for dashboards, monitoring terminals, operational tools, authentication screens, or sharp industrial HUD-style UI in React, Vite, or Next.js.
compatibility: React 18 or 19 project with Node.js and npm; framer-motion is required and Tailwind CSS is optional.
---

# NERV-UI

Use this skill when a React application needs an original high-contrast command-center interface with typed, reusable components. Prefer the published `@mdrbx/nerv-ui` package over recreating lookalike primitives.

Do not use it for a non-React app, a generic rounded consumer UI, or when the request is to reproduce a particular copyrighted screen. The library is inspired by command-center design language; create original labels, data, layouts, and illustrations.

## Detect and install

This package supports React 18 or 19. It is suitable for Vite, Next.js, and other React builds. `framer-motion` is required; Tailwind CSS is optional.

```bash
npm install @mdrbx/nerv-ui framer-motion
```

For a Tailwind project, optionally add the preset:

```js
// tailwind.config.js
import nervPreset from "@mdrbx/nerv-ui/tailwind.preset";

export default { presets: [nervPreset] };
```

Then import the package stylesheet once from the app entry point:

```tsx
import "@mdrbx/nerv-ui/styles.css";
```

For Next.js interactive pages, add `"use client"` before using stateful components or animation. Do not claim support for a non-React target: use a different, target-native design system there.

## Skill installation

The canonical skill source is this directory: `skills/nerv-ui/`. It contains the sole `SKILL.md`; do not create copied variants.

For Codex, install the directory in the local skills folder, then start a new task:

```bash
git clone --depth 1 https://github.com/mdrbx/nerv-ui.git /tmp/nerv-ui-skill
mkdir -p ~/.codex/skills
cp -R /tmp/nerv-ui-skill/skills/nerv-ui ~/.codex/skills/nerv-ui
```

For Claude Code, use the same directory at user or project scope:

```bash
mkdir -p ~/.claude/skills
cp -R /tmp/nerv-ui-skill/skills/nerv-ui ~/.claude/skills/nerv-ui
```

For Hermes Agent, install the same directory in its user skill tree, then verify discovery:

```bash
mkdir -p ~/.hermes/skills
cp -R /tmp/nerv-ui-skill/skills/nerv-ui ~/.hermes/skills/nerv-ui
hermes skills list
```

The repository also exposes the canonical directory through symlinks at `.agents/skills/nerv-ui` for Codex and `.claude/skills/nerv-ui` for Claude Code. Do not maintain copied project variants.

## Design rules

- Use black or near-black surfaces, squared corners, thin structural borders, compact uppercase labels, and monospace data.
- Reserve orange for primary hierarchy, cyan/green for live data, and red for exceptional states. Do not use alert colors as decoration everywhere.
- Keep a readable text contrast, visible keyboard focus, native labels for inputs, and non-color status cues.
- Respect `prefers-reduced-motion`; avoid animations that are the only way to understand state.
- Compose a complete task flow with hierarchy, empty/loading/error states, not a decorative widget pile.
- Use invented operational copy and neutral data. Never use assets, layouts, or text copied from another project or show.

## Reliable building blocks

<!-- catalog:start -->
Accordion, AccordionItem, Badge, BarChart, Breadcrumb, Button, Card, Checkbox, ClassifiedOverlay, CountdownTimer, DataGrid, Divider, Drawer, DropdownMenu, EmergencyBanner, FileUpload, Gauge, GradientStatusBar, HexGridBackground, InputField, MagiSystemPanel, MonitorOverlay, NavigationTabs, NervToastProvider, Pagination, PatternAlert, PhaseStatusStack, PieChart, PilotCard, RadioGroup, SeeleMonolith, SegmentDisplay, SelectMenu, Skeleton, StatusStamp, Stepper, SurveillanceGrid, SyncProgressBar, SyncRatioChart, SystemDialog, TargetingContainer, TargetingReticle, TerminalDisplay, Textarea, ThemeProvider, TitleScreen, ToastContainer, Toggle, Tooltip, WireframeLoader, useToast
<!-- catalog:end -->

Read [the recipes](references/recipes.md) before composing a dashboard, monitoring terminal, or authentication page. Read [the component catalogue](references/component-catalog.md) when choosing a component.

## Verification

After implementation, run the app's normal type check and build. Also confirm that `@mdrbx/nerv-ui/styles.css` is imported, every package import uses an exported name, keyboard interaction works for interactive controls, and the page remains understandable with reduced motion enabled.

## Ready-to-use prompts

- “Use `@mdrbx/nerv-ui` to build an original responsive operations dashboard with a `DataGrid`, `Gauge`, `BarChart`, loading state, and accessible filter controls. Install the package; do not recreate its components.”
- “In this Next.js client route, create a monitoring terminal using `MonitorOverlay`, `TerminalDisplay`, `StatusStamp`, and `SyncProgressBar`. Keep the copy domain-neutral and honor reduced motion.”
- “Create an accessible authentication screen with `InputField`, `Checkbox`, `Button`, and `ClassifiedOverlay` as optional feedback. Preserve native labels, errors, and keyboard flow.”
