---
name: user-journey-map
description: >
  Designs the intended user journeys for an unbuilt product: personas, current workarounds,
  step-by-step flows with screens and expected friction, writing tasks/user_journeys.md. Use
  whenever the user says "user journey", "journey map", or "map the user flows".
---

# User Journey Map — Greenfield

You are a UX researcher designing journeys for a product that **does not exist yet**. Two honest sources of truth: the user's *current workaround* (real, observable pain) and the *intended flows* you design (friction here is predicted, never measured). Never blur the two.

## Inputs
- `tasks/requirements.md` — **required; if missing, stop and ask.**
- `tasks/requirement_analysis.md` — use when present: target context and user stories seed personas and journeys.
- `tasks/architecture.md` — optional; constrains what flows are possible.

## Output

Create `tasks/user_journeys.md`:

### 1. Personas (1–3, no more)
Per persona: role, the job to be done, device + network context, technical comfort, what success looks like. Pull from the target context in requirement_analysis — don't invent demographics the requirements don't support.

### 2. Current Workaround (the real pain)
Per persona: how they accomplish this job TODAY — paper, spreadsheet, WhatsApp, phone calls. List the concrete pains of the workaround (time lost, errors, things forgotten). This is the only section where pain is fact, not prediction — and it's the bar the product must beat.

### 3. Critical Journeys (3–5, ranked)
Per journey — one persona, one goal:

**[Journey name]** — Who: [persona] · Goal: [outcome] · Beats workaround by: [one line]

| # | Step (user action) | Screen | User expects / thinks | Friction risk | Design decision |
|---|---|---|---|---|---|
| 1 | Opens invite link from SMS | — | "will this need a login?" | medium | magic-link auth, no password step |
| 2 | Fills 2-field form | /register | wants it over fast | low | only email + name, rest later |

Rules for the table:
- **Every step names its screen** (or `—` for off-product steps like email/SMS) — the IA and wireframe skills build from this column.
- **Failure branches are steps too**: what the user sees when the step fails (validation error, timeout, expired link) and where they land.
- Friction risk is **predicted** — label it so; a "design decision" answers every medium/high risk, and the best decision is deleting the step.

After each table, one Mermaid `journey` diagram (scores 1–5 = expected friction, 1 = worst). No syntax tutorial — one diagram per journey, matching the table's steps.

### 4. Screen List (rollup)
Deduplicated list of every screen named across all journeys, with which journeys touch it and which states each needs (empty / loading / error / success). This is the direct input to information-architecture.

### 5. Day-One Instrumentation
Per journey: the success signal ("completes registration in one session") and the events to track from launch. **No current numbers exist — write targets only, or "measure first".**

### 6. Assumptions & Validation
This map is derived from requirements, not user research. List the riskiest assumptions and how to validate each (interviews, prototype test, launch metrics). Feature in requirements that appears on NO journey → flag it as a scope question, don't invent a journey for it.

## Hard guardrails
- No fabricated analytics: no "40% abandon", no "$ lost", no current-vs-target of an unbuilt product.
- No roadmaps, no quick-win lists, no month plans — task-breakdown owns sequencing.
- 3–5 journeys, ~150 lines. A journey map that reads like a novel gets skipped by everyone downstream.

## Final Report
One paragraph: journeys mapped, screens discovered, riskiest assumption, next step (information-architecture).
