---
name: killer-ui
version: "1.0.0"
description: >
  Killer UI — a Claude Code skill set that turns vibe-coded UIs into
  production-grade, Apple-quality design systems. Covers design systems,
  brand identity, screen design, accessibility, dark mode, Figma specs,
  design-to-code translation, and design critique. Built for developers
  who ship fast but want their apps to actually look good.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Killer UI

**Your AI's design degree.** Killer UI is a Claude Code skill set that gives
your coding agent the eye of an Apple Principal Designer, the rigor of a
Pentagram Creative Director, and the pragmatism of a Vercel Design Engineer.

Most vibe-coded apps work fine but look like nobody cared. Random spacing,
clashing colors, broken dark mode, no visual hierarchy. Killer UI fixes that
by encoding real design expertise into repeatable, auditable workflows.

## Getting Started

```
/KUI:review          ← Critique your current UI — find every design sin
/KUI:system          ← Generate a full design system from scratch
/KUI:screen          ← Design a screen with proper patterns
/KUI:code            ← Translate any design into production code
```

## Full Command Reference

| Command | What It Does |
|---------|-------------|
| `/KUI:system` | Create a comprehensive design system (palette, typography, spacing, components, tokens) |
| `/KUI:brand` | Develop a complete brand identity (strategy, visual system, applications, guidelines) |
| `/KUI:screen` | Design screens following platform-native patterns (hierarchy, states, interactions) |
| `/KUI:review` | Full design critique — heuristic evaluation, visual hierarchy, typography, color, usability |
| `/KUI:a11y` | WCAG 2.2 AA accessibility audit with remediation plan |
| `/KUI:code` | Convert designs into production-ready, accessible frontend code |
| `/KUI:figma` | Generate Figma-ready specs (auto-layout, components, variants, tokens) |
| `/KUI:trends` | Research and synthesize current design trends for any industry |
| `/KUI:darkmode` | Audit and fix dark mode issues — contrast, inverted colors, hardcoded values |

## Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  REVIEW  │──▶│  SYSTEM  │──▶│  SCREEN  │──▶│   CODE   │
│ critique │   │  design  │   │  design  │   │  build   │
│ what's   │   │  system  │   │  screens │   │  ship it │
│ broken   │   │  first   │   │  right   │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
   │ A11Y   │   │ BRAND  │   │ FIGMA  │   │ DARK   │
   │ audit  │   │ identity│   │ specs  │   │ MODE   │
   └────────┘   └────────┘   └────────┘   └────────┘
```

## Design Philosophy

1. **Systems over opinions.** Every color, size, and spacing value exists in a
   scale. No magic numbers. No "that looks about right."

2. **Dark mode is not an afterthought.** If it breaks in dark mode, it was never
   designed — it was just themed. Design for both from day one.

3. **Accessibility is not a feature.** It's a baseline. WCAG AA minimum.
   44px touch targets. 4.5:1 contrast ratios. No exceptions.

## Artifacts

Killer UI writes to `.design/` in your project root:

```
.design/
├── STATE.json              ← Progress tracking
├── system/                 ← Design system artifacts
│   ├── tokens.json         ← Design tokens (colors, type, spacing)
│   ├── palette.md          ← Color palette documentation
│   ├── typography.md       ← Type scale documentation
│   └── components.md       ← Component specifications
├── brand/                  ← Brand identity artifacts
├── screens/                ← Screen design specs
├── audit/                  ← Review and audit reports
│   ├── review-report.md    ← Design critique report
│   ├── a11y-report.md      ← Accessibility audit
│   └── darkmode-report.md  ← Dark mode issues
└── code/                   ← Generated code artifacts
```
