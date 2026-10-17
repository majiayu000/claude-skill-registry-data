---
name: design-handoff-spec
category: design
description: Use when a screen design was approved (the design task is in done) - the hand-off document implementers build from - components mapped to the inventory, tokens, every state, responsive behaviour per breakpoint, accessibility notes and exact copy
---
# Design Hand-off Spec

## Overview

Every task blocked by this design task receives its documents in its run context as TEXT, under "## The approved design this task builds" — the hand-off specs first, then every mockup, the variants that were not chosen included. The markup of a mockup is dropped, so its colours, sizes and layout do not survive the trip. The hand-off spec is what they can act on. It is written after approval, from the chosen variant only, and it names things — components, tokens, copy — instead of describing pixels.

**Core principle:** An implementer reading only this spec builds the approved screen without inventing a single value, string or state.

## Shape

One markdown document per screen, attached in the `done` run with `add_task_document`, titled `handoff: <screen>` — the same `<screen>` as its `design: <screen> · <letter>` mockups. Under ~10,000 characters: a markdown document reaches a dependent's run cut at 12,000, and the end is what gets cut.

```markdown
# handoff: Invoices — list
Design task D-14 · approved: Variant A — table first, mockup `design: Invoices — list · A` (#variant-a, #states-a) — chosen by the human's "Chosen variant" comment · not chosen, never built: `design: Invoices — list · B` · design system Harbor base v3 + web layer v1

## Screen map
375: title row (Invoices · New invoice) → search → status chips (scroll sideways) → invoice rows → "Load more"
1440: sidebar 240px | content: title row → search + chips in one row → table (Customer, Number, Issued, Due, Amount, Status) → pagination

## Components
| Element | Component | Variant / props | |
|---|---|---|---|
| New invoice | atoms/Button | variant primary, size md, icon Plus | existing |
| Search | molecules/SearchField | placeholder "Customer or invoice number" | existing |
| Status | atoms/Badge | paid → success, overdue → destructive, draft → muted; always with its text | existing |
| Invoice row (375) | molecules/InvoiceRow | customer + number left; amount + status right; due date below | NEW · molecule · states: default, pressed, focus-visible |

## Tokens
colour: background, surface (table header), foreground, muted-foreground (secondary lines), border, primary/on-primary, destructive (overdue) · type: heading-2 (title), body, body-sm (secondary), tabular numbers for amounts · space: 4 (375 page padding), 6 (1440), 3 (row padding) · radius: md · shadow: none — rows are separated by border

## States
- Loading: six skeleton rows in the row's shape; title, search and New invoice stay visible.
- Empty, first use: "No invoices yet" · "Create your first invoice and send it in under a minute." · primary "New invoice".
- Empty, no match: "No invoices match "{query}"" · ghost "Clear search".
- Error: banner above the list: "Invoices couldn't load. Check your connection and try again." · "Retry"; search and chips keep their values.
- Row: hover (1440) surface background; focus-visible 2px ring inset; pressed (375) surface background.
- Dark: tokens only, no per-component overrides.

## Responsive
| Width | Behaviour |
|---|---|
| < 640 (375) | rows, chips scroll sideways, "Load more" instead of pagination |
| 768 | table: Customer (number below), Amount, Status |
| 1024 | full table; sidebar collapses to icons |
| ≥ 1280 (1440) | full table; sidebar 240px; content max 1200px |

## Accessibility
- One h1 "Invoices"; the table has a visually hidden caption and column headers.
- Status is text + colour, never colour alone. Each row is one link named "<customer>, invoice <number>".
- Focus order: search → chips → New invoice → rows → pagination. Touch targets ≥ 44px at 375.
- Checked contrast: muted-foreground/background 6.06:1 · on-primary/primary 7.52:1 (light), 7.17:1 (dark).
- The result count after a search is announced politely.

## Copy
| Where | Text |
|---|---|
| title | Invoices |
| primary action | New invoice |
| search placeholder | Customer or invoice number |
| chips | All · Draft · Sent · Overdue · Paid |

## Out of scope
Bulk actions, CSV export, the invoice detail page.
```

## Rules

- **Chosen variant only.** Each screen's chosen variant is the latest human comment `Chosen variant: <document title>` naming one of its documents, else the answered variant question, else its recommended answer. The header names its document by exact title and how it was chosen, and lists the other variant documents as not chosen — they reach the developer's run too, and this line is what tells them apart. Beyond that line the others do not appear, not even as "alternative".
- **Name, don't measure.** Tokens by role (`muted-foreground`, `space.4`), never a hex or a pixel the design system does not hold.
- **Every element maps to the inventory** — the existing component, its variant and props — or is marked NEW with its level, props and states. NEW is the exception, and it is the developer's job to add it to `INVENTORY.md`.
- **Every state the mockup drew**, in words, with its exact copy.
- **Responsive per breakpoint of the target stack** — web: the repository's breakpoints (Tailwind `sm/md/lg/xl`); mobile: compact / medium / expanded width, landscape, 200% text, safe areas and the keyboard.
- **Accessibility as it applies to this screen** — headings and landmarks, names for icon-only controls, focus order, touch targets, the contrast pairs you checked, announcements (accessibility-basics lists the rules; the spec says how each lands here).
- **Exact copy** in the product's content language, keyed by where it appears. Draft copy the human did not correct in review is now approved copy.
- **No code.** The spec says what to build; how is the developer's call.

## Common Mistakes

- Pasting the mockup's CSS — implementers need token names, not declarations.
- "Same as the mockup" for a state — the mockup does not reach them as a picture.
- Copy paraphrased instead of exact.
- Forgetting the breakpoints between the two drawn widths.

## Red Flags

- A raw value (`#1F5F4A`, `14px`) anywhere in the spec.
- A component name that is not in the inventory and not marked NEW.
- A spec longer than the 12,000-character cut — the copy table at the end is what gets lost.
