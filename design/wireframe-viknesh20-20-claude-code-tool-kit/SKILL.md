---
name: wireframe
description: "Generates textual or ASCII wireframes for screens, layouts, and information architecture. Pixel-free; focused on structure, hierarchy, and component placement. Output is reviewable in a PR diff and translates directly to component code."
argument-hint: "<screen or layout to wireframe>"
---

# /wireframe

Produce wireframes that engineers can build from and reviewers can give feedback on without opening Figma. Pixel-free, structure-first, optimized for clarity over fidelity.

## When to use

- Spec'ing a new screen before any visual design work.
- Documenting an existing screen's structure for the team.
- Comparing 2–3 layout options without committing to visual design.
- Onboarding a new dev/designer to the product's IA.
- Working on a project where Figma isn't part of the workflow.

## When NOT to use

- After visual design has shipped and you need pixel-accurate review (use Figma / screenshots).
- For animations / interactions — those need a different artifact.
- For brand work — that's color, type, voice, not structure.

## Operating method

### 1. Confirm what you're wireframing

- **Single screen or whole flow?** Multi-screen flows belong to `/design-flow`; this skill is per-screen.
- **What states?** Default, loading, empty, error — pick the relevant ones. Don't wireframe states that don't matter for this screen.
- **What's the responsive context?** Desktop / tablet / mobile / all three?
- **What's the device?** Web / native iOS / native Android / TV / wearable. Conventions differ.

### 2. Pick a notation

Three notations the toolkit supports. Pick what serves the screen.

#### A. ASCII boxes — best for layouts with clear regions

```
┌─ Header ────────────────────────────────────────────┐
│ Logo  |  Search                |  ⚙   👤 Avatar    │
└─────────────────────────────────────────────────────┘
┌─ Sidebar ─┐  ┌─ Main ──────────────────────────────┐
│ Inbox  3  │  │  ┌─ Today ──────────────────────┐  │
│ Sent      │  │  │ • Sarah — Re: Q4 plan         │  │
│ Drafts    │  │  │ • System — Backup OK          │  │
│ Starred   │  │  │ • Marcus — New designs        │  │
│ + New     │  │  └───────────────────────────────┘  │
└───────────┘  │                                     │
               │  ┌─ Yesterday ───────────────────┐  │
               │  │ ...                           │  │
               │  └───────────────────────────────┘  │
               └─────────────────────────────────────┘
```

#### B. Mermaid flowchart — best for navigation / decision flows

```mermaid
flowchart TD
  Home[Home] -->|click "New"| Picker{Picker modal}
  Picker -->|"Project"| ProjectForm[Project form]
  Picker -->|"Doc"| DocEditor[Doc editor]
  Picker -->|"Cancel"| Home
  ProjectForm -->|"Save"| ProjectDetail[Project detail]
  ProjectForm -->|"Cancel"| Home
```

#### C. Outline + bullet — best for content-heavy or simple screens

```
[Page] /settings/billing

  [Section 1] Current plan
    - Plan name (e.g., "Pro")
    - Price + billing period
    - Renewal date
    - [Action] "Change plan"
    - [Action] "Cancel subscription"

  [Section 2] Payment method
    - Card brand + last 4
    - Expiration
    - [Action] "Update payment method"

  [Section 3] Billing history
    - Table: date, amount, status, [link] download invoice
    - Pagination if > 12 invoices
```

### 3. Annotate states

For each wireframed screen, list the states needed and what changes between them:

```
States:
  Default     — see above.
  Loading     — sidebar visible, main shows skeleton rows (3 sections × 5 rows of skeleton text).
  Empty       — sidebar visible, main shows centered illustration + "No messages yet" + "Connect inbox" CTA.
  Error       — banner above main: "Couldn't load messages — retry?" with retry button. Main dimmed.
  Long list   — virtualize after 50 rows; pinned date headers.
```

### 4. Annotate components

Mark each component box with:
- The component name (so engineering knows what's reusable).
- States it needs (`hover`, `pressed`, `disabled`, `focus`).
- Notable interactions (`onClick → opens modal X`).

### 5. Annotate responsiveness (when relevant)

For each breakpoint, note what changes:

```
Desktop (1024px+): sidebar 240px wide, main fluid.
Tablet (768–1023px): sidebar collapsible, hamburger toggle.
Mobile (< 768px): sidebar replaced by bottom nav (Inbox / Sent / + / Search / Profile).
```

### 6. Engineering handoff

End with:
- Routes the screen lives at.
- Components needed (new vs reused).
- Data the screen needs.
- Empty-state CTA destination.
- Loading strategy (skeleton vs spinner vs optimistic).

## Output format

```
# Wireframe: <screen>

## Purpose
<one sentence>

## Layout (default state)
[ASCII / Mermaid / outline]

## States
[per-state summary]

## Components
| Box | Component name | Reused? | Notes |
|---|---|---|---|
| Sidebar | <SideNav>  | yes | new active state needed |
| Main list | <MessageList> | new | virtualizes after 50 |

## Responsive
[per-breakpoint changes]

## Microcopy
[key strings — defer the rest to /microcopy]

## Engineering handoff
- Route: <path>
- Data: <fetched from where>
- New components: <list>
- Reused components: <list>
- Empty-state CTA destination: <route>
```

## Boundaries

- **No pixel-accurate rendering.** That's Figma's job, or `impeccable` skill on rendered HTML.
- **No color or font choice.** That's the design system + `impeccable`.
- **No motion.** That's a separate artifact (storyboard, prototype).
- **Don't wireframe past clarity.** If the layout is decided, jump to code.
- **Don't wireframe what doesn't exist yet.** If the data model isn't decided, design that first; the screen will fall out.
- Always include states (loading, empty, error) when relevant. A wireframe without them is incomplete.
