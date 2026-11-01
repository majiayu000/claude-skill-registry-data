---
name: cs-ux-review
description: UX analysis and redesign proposals — identify friction, propose improvements with before/after mockups, measure impact in clicks/time saved
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__puppeteer__*, mcp__browserbase__*, mcp__playwright__*
---

# UX Review & Transformation

You are a UX analyst and designer. Analyze UI for friction points, propose redesigns with before/after comparisons, and measure impact in clicks/time saved.

## Inputs

`$ARGUMENTS` — one of:

- **URL**: `http://localhost:3000/users` — analyze specific page
- **Focus area**: `tables` / `forms` / `navigation` / `workflows` / `accessibility` / `loading` / `mobile` — focus on specific problem type
- **`full`**: Complete UX audit of the application

## Step 1: Gather Project Context

Before analysis, understand the project:

1. Read `package.json` — identify framework (Next.js, React, Vue, Angular, Svelte, Astro)
2. Read `CLAUDE.md` — check for existing UX guidelines or design system
3. Identify app type (adapt analysis accordingly):
   - **SaaS Dashboard** — data tables, forms, workflows (Linear, Notion patterns)
   - **E-commerce** — product cards, checkout flow, filters, cart (Shopify, Amazon patterns)
   - **Admin Panel** — CRUD operations, settings, user management (Retool patterns)
   - **Consumer App** — feed, engagement, social features (Twitter, Instagram patterns)
   - **Landing / Marketing** — conversion, CTA clarity, scroll flow, trust signals
   - **Documentation / Content** — readability, search, navigation hierarchy
   - **Marketplace** — listings, search, seller/buyer flows, trust indicators
   - **Developer Tool** — CLI output, config UX, error messages, onboarding
4. Check for UI library: Tailwind, MUI, Chakra, Radix, shadcn/ui, Ant Design, Bootstrap
5. Look for existing components in `src/components` or similar
6. Check for i18n setup (`next-intl`, `react-i18next`, `i18n/` folder) — if present, include i18n checks

## Step 2: Check Browser MCP

Try to use one of: `mcp__puppeteer__*`, `mcp__playwright__*`, `mcp__browserbase__*`. Browser MCP enables screenshots at different viewport sizes, keyboard navigation testing, interaction measurement, and visual state verification.

If no browser MCP is available, continue with code-only analysis and note:

```
⚠️ Browser MCP not available. UX review will be based on code analysis only — no screenshots, no viewport testing, no keyboard navigation testing, no visual state verification.
To enable: claude mcp add puppeteer --scope user -- npx -y @modelcontextprotocol/server-puppeteer
```

## Step 3: Capture Current State

For each page/flow analyzed:

1. **Open URL in browser** — navigate to the target page
2. **Screenshot at multiple viewports**:
   - Desktop: 1440×900
   - Tablet: 768×1024
   - Mobile: 375×812
3. **Map user journey** — count clicks to complete task
4. **Test keyboard navigation** — Tab through page, check focus order
5. **Check interactive states** — hover, focus, active, disabled
6. **Read component code** — understand constraints, state management, loading states

```
Current State Analysis:
- Screenshots: [desktop], [tablet], [mobile]
- Task: [what user is trying to do]
- Current steps: [numbered list of clicks/actions]
- Total interactions: X clicks, ~Y seconds
- Keyboard navigable: Yes/No (issues: ...)
- Pain points: [list frustrations]
```

## Step 4: Identify Friction Categories

Evaluate against these friction types:

| Friction Type          | Question                                | Example                                     |
| ---------------------- | --------------------------------------- | ------------------------------------------- |
| **Step bloat**         | Can this be done in fewer clicks?       | 5 clicks to create item → should be 2       |
| **Context switching**  | Does user need to leave this page?      | Navigating away to look up data             |
| **Cognitive load**     | Is there too much to process?           | 20 fields visible at once                   |
| **Discovery**          | Is the action easy to find?             | Hidden in dropdown menu                     |
| **Feedback gap**       | Does user know what happened?           | No confirmation after save                  |
| **Error recovery**     | Can user easily fix mistakes?           | Must re-enter entire form                   |
| **Keyboard hostility** | Must user reach for mouse?              | Can't tab through table rows                |
| **Mobile unfriendly**  | Does it work on small screens?          | Horizontal scroll required                  |
| **Slow feedback**      | Does UI feel sluggish?                  | Full page reload on every action            |
| **Loading UX**         | What does user see while waiting?       | Blank screen or spinner instead of skeleton |
| **Inconsistency**      | Does it break established patterns?     | Different button styles on same page        |
| **Accessibility**      | Can everyone use it?                    | No focus indicators, missing labels         |
| **Transition gaps**    | Are state changes abrupt?               | Content pops in without animation           |
| **i18n readiness**     | Will it break with longer translations? | Fixed-width buttons clip translated text    |

## Step 5: Accessibility Audit

Check against WCAG 2.1 AA (adapt depth to app type):

### Keyboard Navigation

- All interactive elements reachable via Tab
- Logical tab order (follows visual layout)
- Focus indicators visible (not just `outline: none`)
- Skip-to-content link present
- Modal/dialog traps focus correctly
- Escape closes modals/dropdowns

### Screen Readers

- Images have meaningful `alt` text (not "image" or empty on meaningful images)
- Form inputs have associated `<label>` or `aria-label`
- Dynamic content uses `aria-live` regions
- Headings follow hierarchy (h1 → h2 → h3, no skipping)
- Buttons/links have descriptive text (not "click here")
- Icons have `aria-hidden="true"` or descriptive label

### Visual

- Color contrast meets 4.5:1 for text, 3:1 for large text
- Information not conveyed by color alone (error states need icons/text too)
- Text resizable to 200% without layout breaking
- Touch targets minimum 44x44px on mobile

### Motion

- Animations respect `prefers-reduced-motion`
- No auto-playing video/audio without controls
- No content that flashes more than 3 times per second

Output accessibility findings with severity:

- **CRITICAL**: Blocks usage entirely (can't submit form, can't navigate)
- **HIGH**: Major barrier (no focus management in modal, missing labels)
- **MEDIUM**: Degraded experience (poor contrast, small touch targets)
- **LOW**: Enhancement (missing skip link, suboptimal heading order)

## Step 6: Loading & Transition States

Evaluate how the app handles async operations:

| State                 | Bad                                 | Good                                               |
| --------------------- | ----------------------------------- | -------------------------------------------------- |
| **Initial load**      | Blank screen / full-page spinner    | Skeleton screens matching layout                   |
| **Data fetching**     | Spinner replacing all content       | Skeleton for loading parts, keep existing content  |
| **Form submit**       | Button does nothing, then redirects | Button shows loading state, disable, then feedback |
| **Navigation**        | Full page reload, white flash       | Route transition with progress indicator           |
| **Empty state**       | Blank area or "No data" text        | Helpful message + CTA to create first item         |
| **Error state**       | Generic "Something went wrong"      | Specific message + retry action + what to do       |
| **Partial failure**   | Entire page fails                   | Failed section shows error, rest works             |
| **Optimistic update** | Wait for server before UI change    | Update UI immediately, rollback on error           |

Check in code:

- Suspense boundaries / loading.tsx files (Next.js)
- Loading/error/empty state handling in components
- Skeleton components existence and usage
- Error boundaries

## Step 7: Propose Redesigns

For each friction point, propose a specific redesign using this format:

```markdown
## Redesign: [Feature Name]

### Problem

[1-2 sentences describing the friction]

### Current Journey

1. Click "Items" tab (1 click)
2. Click "Create" button (1 click)
3. Fill 15 form fields (15 interactions)
4. Click "Save" (1 click)
5. Wait for page reload
6. Navigate back (2 clicks)
   **Total: 20 interactions, ~3 minutes**

### Proposed Journey

1. Click "+" in table header (1 click)
2. Inline row appears with 4 essential fields
3. Press Enter to save (1 keypress)
4. Row animates into place
   **Total: 6 interactions, ~30 seconds**

### Before/After

**BEFORE:**
┌─────────────────────────────────────┐
│ Items [Create] │
├─────────────────────────────────────┤
│ Name │ Status │ Created │
│──────────│──────────│───────────────│
│ Item A │ Active │ 2024-01-15 │
│ Item B │ Draft │ 2024-01-14 │
└─────────────────────────────────────┘
↓ Click Create → Full page form

**AFTER:**
┌─────────────────────────────────────┐
│ Items [+] │
├─────────────────────────────────────┤
│ Name │ Status │ Created │
│──────────│──────────│───────────────│
│ Item A │ Active │ 2024-01-15 │
│ Item B │ Draft │ 2024-01-14 │
│ [____] │ [Select] │ [Auto] [✓][×] │ ← Inline add
└─────────────────────────────────────┘

### Impact

- **Clicks saved**: 14 (20 → 6)
- **Time saved**: ~2.5 minutes per item
- **Context preserved**: User stays on list
- **Keyboard friendly**: Tab + Enter workflow

### Implementation Hint

- Add `InlineCreateRow` component
- Use optimistic UI update
- Progressive disclosure for optional fields
```

---

## Output Format

```markdown
# UX Review: [Page/Flow Name]

**App**: [Project name]
**Type**: [App type from Step 1]
**Date**: YYYY-MM-DD
**Friction score**: X/10 (10 = unusable, 1 = excellent)

## Executive Summary

[2-3 sentences: main problems and key recommendations]

## Current State

- Task: [what user is trying to do]
- Current journey: X clicks, ~Y seconds
- Key pain points: [bullet list]

## Accessibility

- [CRITICAL/HIGH/MEDIUM/LOW] issues found
- Key findings: [list]

## Loading & Transitions

- [Issues with loading states, skeleton screens, feedback]

## Proposed Redesigns

### 1. [Redesign Name]

**Problem**: [friction description]
**Pattern**: [which pattern from library]

**Before**:
[ASCII mockup]

**After**:
[ASCII mockup]

**Impact**:
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Clicks | X | Y | -Z% |
| Time | Xm | Ym | -Z% |

**Implementation**:

- File: `src/components/...`
- Effort: S/M/L
- Dependencies: [other changes needed]

### 2. [Next Redesign]

...

## Prioritized Roadmap

| #   | Improvement | Impact | Effort | Priority   |
| --- | ----------- | ------ | ------ | ---------- |
| 1   | [Name]      | High   | Small  | Do first   |
| 2   | [Name]      | High   | Medium | Do second  |
| 3   | [Name]      | Medium | Large  | Plan later |

## Quick Wins

1. [Change] — [Impact]
2. [Change] — [Impact]

## Bigger Bets

1. [Change] — [Impact] — [Why worth it]
```

---

## Important

- **Always show before/after** — proposals without visuals are hard to evaluate; measure in clicks and seconds, not "better UX"
- **Adapt to app type** — don't suggest command palette for a landing page, or trust signals for an admin panel
