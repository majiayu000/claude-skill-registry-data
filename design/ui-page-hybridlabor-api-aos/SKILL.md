---
name: ui-page
description: "Use when scaffolding a new mobile-first page using StyleSeed Toss layout patterns, section rhythm, and existing shell components."
category: design-ui-ux
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, page-design, mobile, layout, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI Page

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill scaffolds a complete page or screen using the Toss seed's mobile-first composition rules. It keeps page structure consistent by building on the existing shell, top bar, bottom navigation, and card rhythm instead of producing disconnected sections.

## When to Use
- Use when you need a new page in a Toss-seed app
- Use when you want a consistent page shell, spacing, and navigation structure
- Use when you are adding a new product flow and need a solid starting layout
- Use when you want to stay mobile-first even if the project later expands to larger breakpoints

## How It Works

### Step 1: Inspect the Existing Shell

Read the current page scaffolding patterns first, especially:
- page shell
- top bar
- bottom navigation
- representative pages using the same route family

### Step 2: Define the Page Purpose

Clarify:
- the page name
- the primary user question the screen answers
- the top one or two actions the user should take

Every screen should have one dominant purpose.

### Step 3: Use the Information Pyramid

Lay out the page from highest importance to lowest:
1. Hero or top summary
2. KPI or key actions
3. detail cards or supporting modules
4. lists, history, or secondary content

Avoid repeating the same section type mechanically from top to bottom.

### Step 4: Apply the Toss Layout Rules

Default layout choices:
- mobile viewport width around `max-w-[430px]`
- page background on `bg-background`
- horizontal padding around `px-6`
- section rhythm with `space-y-6`
- generous bottom padding if a bottom nav is present
- cards using semantic surface tokens, rounded corners, and light shadows

### Step 5: Compose Instead of Rebuilding

Use existing `ui/` and `patterns/` components wherever possible. New pages should primarily orchestrate existing building blocks, not recreate them.

### Step 6: Account for Real Device Constraints

- handle safe-area insets
- avoid horizontal overflow
- keep interactive clusters thumb-friendly
- ensure long content scrolls cleanly without clipping the bottom navigation

## Output

Return:
1. The page scaffold
2. The chosen section structure
3. Reused components and any newly required components
4. Empty, loading, and error states that the page will need next

## Best Practices

- Keep the first version structurally correct before adding decoration
- Use one strong hero instead of multiple competing highlights
- Preserve navigation consistency across sibling screens
- Prefer reusable section components when the page will likely repeat

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-page/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.


## Core Process
1. Scaffold the page structure using the standard StyleSeed shell component.
2. Layout the content mobile-first, ensuring proper stacking and touch ergonomics.
3. Apply consistent vertical section rhythm using design tokens.
4. Adapt the layout for desktop viewports using responsive grid patterns.

## Common Rationalizations
| Rationalization | Reality |
|---|---|
| I'll build the desktop layout first and adapt it for mobile later. | Violates the core mobile-first mandate, leading to clunky mobile experiences. |
| I don't need to use the standard shell component here. | Bypassing the shell creates inconsistent navigation and layout behavior. |
| I'll add custom margins between these sections. | Breaks the established section rhythm defined in StyleSeed. |

## Red Flags
- Page layout fails on narrow mobile screens.
- Inconsistent vertical rhythm between major page sections.
- Not utilizing standard page shell or layout wrappers.

## Verification
- [ ] Page is built mobile-first and scales up to desktop.
- [ ] Section spacing adheres to StyleSeed section rhythm tokens.
- [ ] Standard shell components are used for layout wrapping.
