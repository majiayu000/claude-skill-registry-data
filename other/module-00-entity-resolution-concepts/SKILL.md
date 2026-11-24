---
name: module-00-entity-resolution-concepts
description: 'Bootcamp Module 0 (optional): the Entity Resolution Concepts primer. Runs only when "Entity Resolution Concepts" was selected during Bootcamp preparation. Use when the bootcamper reaches the entity-resolution concepts module, or asks to explore entity resolution concepts before Module 1.'
---

# Module 0 (optional): Entity Resolution Concepts

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Follow `../bootcamp-onboarding/ground-rules.md` throughout (👉 one-question-at-a-time,
MCP-first, no fabricated answers). This is an **optional** primer that teaches the core idea of
entity resolution so the bootcamper has context before the guided modules begin.

**Inclusion is driven by module selection, not by a per-module gate.** Whether this module runs is
decided once, during the **Bootcamp preparation** module (`../bootcamp-preparation/SKILL.md`): Core
always includes it; Customized includes it only if the bootcamper chose it. When this skill is
invoked, the bootcamper has already opted in — so **run the primer directly**; do NOT ask a
skip/keep question (that gate has been retired to avoid asking the same decision twice — INV-078).

Module 0 is a **preamble, not a numbered module**: the module table in Bootcamp preparation marks
it Optional, one of the three optional modules with System verification and Truth Set visualization
(INV-076/INV-078), so skipping it (by not selecting it) is a permitted, requested skip (INV-014).
Keep it lightweight — no module-start banner beyond its ENTITY RESOLUTION CONCEPTS banner, no journey
map of its own, no before/after framing, no step overview, and no bootcamper-facing end-of-module
summary. **But it IS captured in the recap** (INV-092): at its close it adds
`entity_resolution_concepts` to `modules_completed` and appends its own name-based recap section to
`docs/bootcamp_recap.md` (Step 2 below).

## 1. Run the primer

Follow `concepts.md` in this skill directory:

1. Present the **ENTITY RESOLUTION CONCEPTS** banner (defined in `concepts.md`) — this is the
   INV-073 banner outcome, delivered here in Module 0.
2. Give the description of entity resolution, pulling all Senzing-specific facts from the Senzing
   MCP server, never from memory (MCP-first invariant / INV-073). Verify substantive claims with a
   second confirming MCP call before presenting them (see `concepts.md`).
3. **Invite questions/discussion before the knowledge check** (`concepts.md`): after the description
   and before the knowledge-check offer, give the bootcamper space to clarify, ending on the
   pinned 👉 question — verbatim:
   **"Do you have any questions about entity resolution before we continue?"** (INV-056). Answer any
   question via `search_docs` verified with a second MCP call, then invite more with the **pinned
   follow-up variant** in `concepts.md` — *"Do you have any **other** questions about entity
   resolution before we continue?"* — never by repeating the first-ask string, which reads as though
   their question did not register. On "no", proceed to the knowledge check. It is issued once
   (INV-006),
   single-meaning yes/no with no "or"-joined choices (INV-008 / INV-051), and never blocks (not a ⛔
   gate).
4. Offer the **optional knowledge check** (`concepts.md`) as its own pinned 👉 question before
   the readiness gate. On accept, pose a short series of MCP-sourced/verified questions at moderate
   difficulty, one 👉 per turn, letting the bootcamper exit at any time; on decline, go straight to
   the gate. The knowledge check never blocks and never replaces the gate.
5. End on the mandatory exploration gate using the pinned 👉 question defined in `concepts.md` —
   verbatim: **"Are you ready to move on to the next module: Discover the Business Problem?"**
   (INV-073 explore-gate outcome; Module 1 always follows Module 0). It is a
   single yes/no with exactly one meaning for "yes" and one for "no", and no "or"-joined choices
   (INV-008 / INV-051). Answer any entity-resolution follow-up via `search_docs`, verified with a
   second MCP call, then re-present the gate; do not advance until the bootcamper is ready.

## 2. Record the recap, then hand off to Module 1

When the bootcamper signals they are ready to move on (Step 1's gate), first **capture this module
in the recap** (INV-092), quietly — no bootcamper-facing end-of-module summary:

1. In `config/bootcamp_progress.json` (a single batched write): add `entity_resolution_concepts`
   to `modules_completed` (idempotent; do not duplicate), set `current_module` to the next module
   in `selected_modules` (read from `config/bootcamp_preferences.yaml`), set `current_step` to
   `null` (INV-442) — so the next module's journey map renders it as current, not Entity Resolution
   Concepts — set
   `step_history["entity_resolution_concepts"]` to
   `{ "last_completed_step": <step>, "updated_at": "<ISO 8601>" }` with this module's final step
   (the shape `../bootcamp-onboarding/module-completion.md` Step 1 gives), and record the knowledge-check outcome
   under `module_0_concepts` as `quiz_offered` (`true` only if you actually presented the pinned
   offer question) and `quiz_taken` (`true` only if the bootcamper accepted and answered at least one
   question). These two fields make a silent skip visible instead of unrecoverable (INV-112).

   ⛔ **Before writing, assert `quiz_offered` is true.** If you did not present the pinned
   knowledge-check offer (`concepts.md` → "Optional knowledge check"), present it **now**, before
   recording
   the recap and handing off — the module has not closed yet, so the recovery is free. Record
   `quiz_offered: false` only if presenting it now is genuinely impossible (e.g. the bootcamper
   has exited), and say so in the recap's **Questions & Responses** subsection rather than leaving
   the omission silent. This mirrors how the Truth Set visualization module re-checks its artifact
   exists before marking itself complete (INV-077).
2. Append a name-based recap section to `docs/bootcamp_recap.md` per
   `../bootcamp-onboarding/module-completion.md` **Step 2 in full**: `## Entity Resolution Concepts —
   {ISO 8601 timestamp}` with the four subsections — **Information Shared** (the entity-resolution
   concepts taught, MCP-sourced), **Questions & Responses** (the "any questions?" gate, the
   knowledge-check offer **and** the bootcamper's answer to it — the offer is always listed because
   it is always asked (INV-112) — plus the knowledge-check questions if taken, and the readiness
   gate, each with the bootcamper's answer — or `- {none this module}`), **Actions Taken** (that
   the primer and optional knowledge check were presented; this preamble creates no project files),
   and **End-of-Module Summary**. Re-read to confirm the section landed
   (2c). Module 0 runs module-completion Step 2 whole and departs from it at two **Steps** only:
   it **skips** Step 3, so it does **not** present the bootcamper-facing end-of-module summary,
   and it **replaces** Step 4's transition question with its own readiness gate (Step 1, item 5
   above).

   ⛔ **On a Core run this is the FIRST module to append a recap section, so 2a applies and creates
   the header.** Bootcamp preparation is recap-exempt (INV-092) and the onboarding preface writes no
   recap, so `docs/bootcamp_recap.md` does not exist yet when this step runs — 2a is the substep
   that creates it, with the five preamble lines (`**Bootcamper:**`, `**Started:**`,
   `**Programming language:**`, `**Path:**`, `**Plugin version:**`). Appending a `## ` section
   without it produces a recap with no preamble, and the failure surfaces only at graduation, on the
   certificate. Run **2d** as well (finalize the in-progress checkpoint) — it applies here exactly
   as it does to any other module; nothing about this module exempts it. So does **2e**: save this
   module's B-roll entry under `entity_resolution_concepts`, with `images: []` and `facts: {}`
   when the primer showed nothing, so the graduation video still gets its title card.

Then invoke the `module-01-business-problem` skill to begin Module 1 — **Discover the Business
Problem** (name the module to the bootcamper, never "Module 1") — applying the module-start banner
and journey map from `ground-rules.md`. The selected numbered modules then run in the order recorded
in `selected_modules` (Module 1 is the next module after Module 0 in every path).
