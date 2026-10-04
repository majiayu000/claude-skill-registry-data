---
name: spec-format
description: Defines the spec document structure and conventions for feature designs and bug diagnoses in the hero workflow.
compatibility: opencode
metadata:
  audience: delivery-leads
  purpose: spec-writing
---
## What I do

Define the structure and quality bar for spec documents produced during `/design` and `/diagnose` workflows. Specs are the handoff artifact between the design phase and the delivery phase — they must be clear enough for an engineer agent to follow without getting stuck, and readable enough for a human to review before and learn from after execution.

## When to use me

Load this skill when producing a spec document for any feature, enhancement, or bug fix. The delivery lead should load this before writing a spec.

## General conventions

- One spec per work item, saved as `spec.md`
- Write in plain markdown, no special syntax or RFC keywords
- Be concrete — name files, directories, components, functions
- The Changes section is the most important section; it must be actionable
- Keep each section focused; do not repeat information across sections
- If information is unknown or requires investigation, say so explicitly
- Link to relevant issues, PRs, or external references when available

## File location

Feature specs: `{hero_folder}/planning/features/{slug}/spec.md`
Bug specs: `{hero_folder}/planning/bugs/{slug}/spec.md`

The `{hero_folder}` defaults to `.hero` and is configurable via `hero.json`.

The `{slug}` is a short, lowercase, hyphenated identifier derived from the work item title (e.g., `add-csv-export`, `login-timeout-race`).

### Folder-per-spec is the optimal layout — and why

A spec gets its **own folder** (`{slug}/spec.md`) because the folder is a
**bundle for the spec's companion artifacts**: `delivery-audit.md`, `plan.md`,
mockups under `mocks/`, `retro.md`, and any diagnosis attachments. The delivery
gates look for these *beside* `spec.md` — e.g. `hero spec verify` finds the
delivery audit at `{slug}/delivery-audit.md`. A spec without its own folder has
nowhere to put these, and the audit/coverage gates can't find them.

**Steer to folder-per-spec for any spec that will be delivered.** This is the
default; prefer it.

A **flat `<slug>.md`** file (no folder) is *tolerated by the engine* —
discovery, slug resolution, and archival all handle it — and is acceptable for a
**lightweight stub or planning-only child** that carries no companions yet (e.g.
an initiative child not yet in delivery). But **promote a flat spec to its own
folder before delivery starts**, so its delivery audit and mocks co-locate where
the gates look. Do not author a deliverable spec as a flat file.

**Stamp `slug:` in frontmatter — it is the authoritative identifier.** For a
folder spec the slug matches the folder name; for a flat file it matches the
filename. Either way, the frontmatter `slug:` is the source of truth, so never
rely on the path alone.

## Feature spec template

```markdown
# {title}

## Context
Why this work exists. What prompted it. Links to issues or tickets.
Relevant history or prior decisions that affect this work.

## Goal
What "done" looks like. One paragraph, concrete and testable.
This is the acceptance criteria in plain language.

## Approach
Architecture and design decisions. How the feature fits into the existing system.
Key technical choices already made and why.
Patterns to follow or avoid.

## Changes
Ordered list of concrete changes to make. Each item should name specific files
or components and describe what to do clearly enough that an engineer can execute
without additional context.

1. {description of first change}
   - {specific detail}
   - {specific detail}
2. {description of second change}
   - {specific detail}
3. ...

## Mockups
Optional. Visual mockups produced for this spec. Auto-populated by `/mock`
against the spec slug. Omit this section if no mockup was produced.

- [Mockup name](.hero/mocks/{slug}/index.html) — YYYY-MM-DD — what the mockup shows

## Boundaries
What is NOT in scope. Adjacent work to explicitly avoid.
Things that look related but should be separate work items.

## Risks
Known risks, edge cases, failure modes to watch for during implementation.
Dependencies on external systems or teams.

## Validation
How to verify the work is correct. Expected test coverage.
Manual verification steps if applicable.
Performance or operational checks if relevant.
```

## Bug spec template

```markdown
# {title}

## Issue
Link to the bug ticket. Reporter. When it was found. Environment details.

## Investigation
What was found during research. Evidence gathered.
Code traces — the end-to-end flow from trigger to failure.
Reproduction steps if applicable.
Key files and line numbers involved.

### Root cause
Clear explanation of why the bug occurs. Distinguish between the symptom
and the underlying cause.

### Severity
Impact, frequency, blast radius. Whether there is a workaround.
Whether this is caused by our code or an external factor.

## Goal
What the fix accomplishes. One paragraph.

## Changes
Ordered fix steps. Same format as feature changes — concrete, actionable,
naming specific files and components.

1. {description of first change}
   - {specific detail}
2. {description of second change}
   - {specific detail}
3. ...

## Mockups
Optional. Visual mockups produced for this fix, if any. Auto-populated by
`/mock` against the spec slug. Omit this section if no mockup was produced.

- [Mockup name](.hero/mocks/{slug}/index.html) — YYYY-MM-DD — what the mockup shows

## Boundaries
What this fix does NOT attempt to address.
Related issues that should be separate work items.

## Risks
Regression risks. Side effects of the fix.
Areas that need careful testing.

## Validation
How to verify the fix works. Regression test expectations.
How to confirm the original issue no longer reproduces.
```

## Mockups section

When `/mock` produces a visual prototype against a spec slug, it appends
(or updates, on `--iterate`) a `## Mockups` section in the spec body listing
each mockup. This makes the artifact discoverable to humans reading the spec
and to delivery agents reading the spec for context.

**Format.** One entry per mockup, in a top-level `## Mockups` section placed
between `## Changes` and `## Boundaries`:

```markdown
## Mockups

- [Hero landing page](.hero/mocks/hero-landing-page/index.html) — 2026-05-20 — public homepage with install CTA and feature grid
- [Hero landing page — dense variant](.hero/mocks/hero-landing-page/dense.html) — 2026-05-22 — compressed-density alternative for above-the-fold
```

**Rules:**

- The section is optional — omit it entirely if no mockup was produced.
- Path is relative to the repo root so the link works in markdown renderers.
- Date is ISO format (`YYYY-MM-DD`).
- Description is one line — what's shown, not why.
- Multiple mockups per spec are supported as additional list items.
- `/mock --iterate` updates the matching entry's date in place rather than
  appending a duplicate when the path is unchanged.
- Free-text `/mock` calls (no spec slug) do not write back — those mockups
  land under `.hero/mocks/_adhoc/` and are not linked to any spec.

`/deliver` reads `.hero/mocks/{slug}/` directly as a pre-flight step, so
mockups generated before this section was introduced (or dropped in by
hand) are still surfaced to the engineer.

## Convention spec template

```markdown
---
type: convention
status: active
scope: [glob patterns where this applies]
tags: [relevant tags]
---
# {Convention Name}

## Pattern
What this convention standardizes. One clear statement.

## When to apply
The conditions under which this convention must be followed.
File types, modules, or situations where it applies.

## How
The specific implementation pattern to follow, with concrete examples
from this codebase.

## Examples
Real examples from the codebase showing this pattern done correctly.

## Anti-patterns
Common violations of this convention and why they're problematic.

## Exceptions
When it's acceptable to deviate from this convention and why.
```

## Decision spec template (ADR)

```markdown
---
type: decision
status: accepted
tags: [relevant tags]
relates-to: [related-spec-slugs]
---
# {Decision Title}

## Context
The situation and forces that led to this decision.

## Options considered
Each option with pros, cons, and trade-offs.

## Decision
What was chosen and why.

## Consequences
What changes as a result. What becomes easier, what becomes harder.
```

## Initiative spec template

```markdown
---
type: initiative
status: planning
tags: [relevant tags]
---
# {Initiative Title}

## Vision
What this initiative achieves when all parts are complete.

## Specs
Ordered list of child specs, each a separate design/diagnose item.
Mark completion status.

## Dependencies
Cross-spec dependencies and sequencing constraints.

## Progress
Summary of what's done, what's in flight, what's next.
```

## Frontmatter conventions

All spec types use YAML frontmatter. The following fields are supported:

| Field | Required | Applies to | Description |
|-------|----------|------------|-------------|
| `title` | Yes | All | Human-readable title. |
| `slug` | Yes | All | Short kebab-case identifier and the spec's authoritative ID. Matches the folder name (folder-per-spec) or the filename (flat `<slug>.md`). Always stamp it in frontmatter — it is the source of truth for resolution and for linking the spec from another session or prompt, independent of path. |
| `type` | Yes | All | Spec type: `feature`, `bug`, `convention`, `decision`, `initiative` |
| `status` | Yes | All | Lifecycle state. Work specs: `planning`, `in-review`, `delivering`, `completed`. Conventions: `draft`, `active`. Decisions: `proposed`, `accepted`. Any type can be `superseded`. |
| `scope` | Yes (conventions) | Convention | Array of glob patterns identifying which files this convention applies to. Used by `hero relevant` to inject relevant conventions. |
| `tags` | No | All | Array of tags for search and filtering. Use lowercase, hyphenated terms. |
| `claimed_by` | No | Work specs | Who is currently working on this spec. Set via `hero spec claim`. |
| `completed_at` | No | Work specs | RFC 3339 UTC timestamp recording when `status` flipped to `completed`. Hero writes this automatically at status-transition time — agents and humans should not hand-write it. The reader also accepts `completedAt:` for tolerance, but only `completed_at:` is ever produced. Historical specs without the field can be backfilled from git history via `hero admin backfill-completed-at`. |
| `created` | No | All | ISO 8601 date when the spec was created. |
| `relates-to` | No | All | Array of spec slugs that are related but not dependent. |
| `depends-on` | No | All | Array of spec slugs that must be completed before this spec can proceed. |
| `supersedes` | No | All | Slug of the spec this one replaces. The superseded spec should have its status set to `superseded`. |
| `parent` | No | Work specs | Slug of the initiative this spec belongs to. |
| `child` | No | Initiatives | Array of spec slugs that are part of this initiative. |
| `domain` | No | All | DSKG namespace partition (`engineering`, `pm`, future packs). New specs scaffolded by `/design` and `/diagnose` emit this from the active workspace domain. Legacy specs without the field resolve to the workspace default (`engineering` if no `domain:` is set in `hero.json`). |
| `size` | No | Sized work specs (`feature`, `bug`, `enhancement`, `epic`, `initiative`) | Declared effort tier on the shared 6-tier ladder: `trivial`, `small`, `medium`, `large`, `x-large`, `giant`. Living field — set at design, updated on scope changes (authoring and mid-delivery). See the `spec-sizing` skill for the ladder, per-type bands, and the nudge protocol. |
| `size_ack` | No | Sized work specs | One-shot acknowledgement that suppresses the design-time nudge when a spec stays at a high tier deliberately. Only `giant` is consumed today. See the `spec-sizing` skill. |

### `size:` — a living field

Treat `size:` like `status:` — agents are expected to keep it accurate.
Updates happen at design time (`/design` stamps it from the design
conversation), during authoring/refinement (the spec writer bumps it
if scope grows), and mid-delivery (the delivery lead bumps it if
reality outruns the declared tier).

Brief frontmatter example:

```yaml
---
title: "Add CSV export"
type: feature
status: planning
size: medium
---
```

Don't re-explain the ladder here — the canonical reference is the
`spec-sizing` skill. It carries the 6-tier descriptions, per-type
bands, nudge schedule, and the `size_ack: giant` acknowledgement
protocol.

### Status transitions

Work specs follow a linear progression: `planning` → `in-review` → `delivering` → `completed`.

Conventions start as `draft` while being authored and reviewed. They move to `active` when the team confirms they reflect actual or intended practice.

Decisions start as `proposed` during discussion. They move to `accepted` when the decision is finalized.

Any spec can be set to `superseded` when a newer spec replaces it. Always set the `supersedes` field on the replacement spec to maintain traceability.

## Acceptance Criteria and EARS

Acceptance criteria live in a `## Acceptance Criteria` section as a bullet list.
Hero recognizes five EARS (Easy Approach to Requirements Syntax) patterns and
classifies each bullet automatically; freeform bullets remain valid for
criteria that genuinely don't fit.

| Pattern | Template | Use when |
|---|---|---|
| **Event** | `WHEN <trigger> THE SYSTEM SHALL <behavior>` | A user action or external event produces a specific outcome |
| **State** | `WHILE <state> THE SYSTEM SHALL <behavior>` | A condition holds for a span of time |
| **Unwanted** | `IF <trigger> THEN THE SYSTEM SHALL <behavior>` | An error or guard condition must be handled |
| **Optional** | `WHERE <feature> IS ENABLED THE SYSTEM SHALL <behavior>` | Behavior applies only under a feature flag or opt-in |
| **Ubiquitous** | `THE SYSTEM SHALL <behavior>` | An always-true invariant |

Example (from a real feature spec):

```markdown
## Acceptance Criteria

- WHEN a user submits invalid form data THE SYSTEM SHALL display field-level validation errors
- WHILE a sync is in flight THE SYSTEM SHALL block concurrent sync attempts
- IF the tracker token is missing THEN THE SYSTEM SHALL print a setup hint and exit non-zero
- WHERE auto_capture IS ENABLED THE SYSTEM SHALL persist learnings after /deliver
- THE SYSTEM SHALL log every failed login attempt
```

**Guidelines:**

- Keywords are case-insensitive, but uppercase reads best in review.
- A trailing period is allowed but not required.
- Don't force EARS onto criteria where it reads awkwardly — freeform is fine.
- Run `hero spec lint <slug>` to see the classification + freeform ratio.
- `hero test generate` maps the `Behavior` clause to Playwright assertions,
  so concrete identifiers (selectors, URLs, flag names) inside the behavior
  produce better autonomous tests than vague phrasing.

## Quality bar

A spec is ready for delivery when:
- The Goal section is concrete enough to verify completion
- The Changes section lists every file or component to touch
- Each change item has enough detail to implement without guessing
- Acceptance Criteria use EARS patterns where they fit; freeform ratio is
  reasonable for the spec's domain
- Boundaries are explicit — the engineer knows what NOT to do
- Risks call out anything that could cause the implementation to stall
- No section says "TBD" or "to be determined" without explanation

## Posting to trackers

When a tracker is configured in `hero.json`:
- Attach the full spec as a comment or file attachment on the issue
- Add a brief summary comment with the goal and change count
- For bugs, include the root cause summary in the comment
