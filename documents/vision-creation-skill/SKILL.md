---
name: vision-creation-skill
description: >-
  Create the customer-facing Vision Document (IIBA Business Need/Solution
  Vision) from a discovery session. Triggers: create vision, vision document,
  concept brief, solution vision.
license: Apache-2.0
compatibility: opencode
category: Framework
---

## What I do

I provide the **Vision Document** template and workflow for the **customer-facing discovery** stage. The Vision captures what the client and delivery team agreed the product should be — *before* any internal requirements engineering. It is shared WITH the customer for sign-off, unlike the internal SRS.

1. **Vision Doc template** — IIBA "Business Need / Solution Vision" structure
2. **docs/vision/ naming convention** — `VISION-{slug}.md` (no draft/final rename, **no** ticket linkage)
3. **Dual-output rendering** — living interactive HTML through the session + .docx on wrap (per `interactive-document-rendering-skill`)
4. **Wireframe co-location** — wireframes live beside the Vision at `docs/vision/{slug}/wireframe-*.html`

## When to use me

Use this skill when:
- A customer discovery session is running and needs its output captured
- Someone says "create vision", "vision document", "concept brief", "solution vision", "discovery output"
- You need a **customer-facing** artifact to align stakeholders and get sign-off (NOT an internal requirements spec — that is `civiltekk-requirements-specs-skill`, route `srs`)

**Trigger phrases**: "create vision", "vision document", "concept brief", "solution vision", "discovery output", "capture the vision", "write a vision doc"

## Audience & sensitivity

The Vision is **customer-facing**. Keep tone non-technical where possible, avoid internal tradeoffs (build-vs-buy rationale, non-goals, cost baselines), and treat any client-shared material as confidential. Capture client statements **verbatim** in a notes section.

## Related

- **`discovery-specialist-subagent`** — the agent that runs the live discovery session and produces the Vision (this skill is its template)
- **`interactive-document-rendering-skill`** — the shared HTML + DOCX rendering standard (living HTML for Vision)
- **`wireframer-skill`** — generates the wireframes co-located at `docs/vision/{slug}/`
- **`pptx-specialist-subagent`** — optional customer presentation deck distilled from the Vision (routes internally to `pptx-generate-slide-skill` + `pptx-generate-template-skill`)
- **`civiltekk-requirements-specs-skill`** (route `srs`) — the DOWNSTREAM internal doc; the signed Vision feeds into the SRS (different audience, different skill)

---

## Vision Document Template

### Header

```markdown
# Vision: {Feature / Solution Name}

**Status**: Draft | In Review | Approved (client sign-off)
**Client / Sponsor**: {name}
**Author**: {name}
**Date**: {YYYY-MM-DD}
**Discovery session**: {date(s) of workshop}
```

> **No `**SRS**:` / `**PLAN**:` linkage.** The Vision is upstream of tickets. When an SRS is later authored from this Vision, the SRS links back to the Vision — not the reverse.

### Sections

#### 1. Problem / Opportunity

```markdown
## Problem / Opportunity

{What problem exists today, or what opportunity is on the table? State it in the
client's own framing. Who is affected? What is the cost of inaction?}
```

#### 2. Target Outcomes

```markdown
## Target Outcomes

What "better" looks like once this exists — expressed as outcomes, not features.
- {Outcome 1 — measurable or observable}
- {Outcome 2}
```

#### 3. Proposed Solution (Summary)

```markdown
## Proposed Solution

A plain-language summary of the agreed direction. Reference wireframes by name
(co-located at docs/vision/{slug}/). Keep this high-level — detail belongs in the SRS.

- Key capabilities
- Primary user flows (link wireframe files)
```

#### 4. Success Measures

```markdown
## Success Measures

How the client will judge success after launch.
| Measure | Today | Target | How observed |
|---|---|---|---|
| {measure} | {baseline} | {goal} | {source} |
```

#### 5. Assumptions & Constraints

```markdown
## Assumptions & Constraints

- {Assumption — something we believe to be true}
- {Constraint — budget, timeline, regulatory, integration}
```

#### 6. Scope Boundaries

```markdown
## Scope Boundaries

### In scope
- {what this initiative covers}

### Out of scope (this phase)
- {explicitly deferred — prevents scope creep in the SRS phase}
```

#### 7. Open Questions

```markdown
## Open Questions

- [ ] {question} — **Owner**: {who} — **Needed by**: {phase}
```

#### 8. Client Notes (verbatim)

```markdown
## Client Notes

Captured verbatim during the discovery session. These are the source of truth
for intent when the SRS is authored.
- "{client statement / reaction}"
- "{constraint mentioned in passing}"
```

---

## docs/vision/ Naming & Placement

```
docs/vision/
├── VISION-{slug}.md                      # source Markdown (canonical)
├── {slug}/
│   ├── VISION-{slug}.interactive.html    # living interactive HTML (regenerated through session)
│   ├── VISION-{slug}.docx                # formal deliverable (rendered on wrap)
│   └── wireframe-*.html                  # wireframer-generated wireframes
```

- `{slug}` = kebab-case from the Vision title (e.g. "Inventory Dashboard" → `inventory-dashboard`)
- **No `VISION-draft-*` → `VISION-{key}` rename** — the Vision is not ticket-keyed. It keeps its slug name for life.
- The interactive HTML is **regenerated after each wireframe/feedback round** so the client always sees the current state.

---

## Rendering

**Render dual outputs per `interactive-document-rendering-skill`:**
- **Interactive HTML** — *living*: regenerate after each discovery round (sidebar nav, dark-mode-aware, color-aware selection)
- **Word .docx** — render once on wrap for client sign-off (auto-TOC, hyperlinked headers, section page-breaks)

**Optional customer presentation deck:** after the Vision is approved, distill it into a slide deck via `pptx-specialist-subagent` (delegate via Task tool — it requires a user-supplied Slide Master template and routes to `pptx-generate-slide-skill`) for steering-committee or client meetings. This is a peer deliverable, linked from the Vision. Delegation binding (§Portability contract, applies here and to the Image-routing paragraph below): OpenCode and Claude Code — Task tool; Other/none (no subagent tool) — run the referenced skill's steps inline.

**Image routing:** if client-shared screenshots/reference images must be described, delegate to `image-analyzer-subagent` (do not interpret inline).

---

## Return Contract

```
**Status:** [success | partial | failed]
**Output:** docs/vision/VISION-{slug}.md
**Summary:** Vision drafted with N sections + M wireframes; living HTML + docx rendered to docs/vision/{slug}/
**Issues:** [blockers, warnings, or "None"]
```
