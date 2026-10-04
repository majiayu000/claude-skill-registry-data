---
name: task-level-decomposition-and-automation-fit
description: "Breaks roles and processes down to task level (People Path + Process Path) and classifies every task into an Automate/Augment/Human-Only category using SML criteria (input/output clarity, cognitive nature, error tolerance, time scale) before prioritizing AI opportunities."
---

# Task-Level Decomposition & Automation Fit

## Purpose

Prevents the most common mistake in identifying AI opportunities: assessing
an entire role or process at once ("could AI handle customer service?")
instead of breaking it down into individual tasks, each assessed
separately. AI generally doesn't replace whole job titles or entire
complex processes — it replaces or assists specific cognitive and routine
TASKS within a process. This skill is the input base for the
`ai-opportunity-portfolio` skill: it produces a prioritizable raw list of
classified tasks, from which the portfolio then selects and scores the
best ones.

## Anchored in research

- A research report supplied by the user, "Methods, Frameworks, and
  Competencies for Identifying AI Opportunities and Capacity in
  Business" (2026) — task-level atomization, the Dual Decomposition
  model, data-driven techniques for process/task analysis.
- Brynjolfsson, E. & Mitchell, T. (2017/2019) — the *Suitable for Machine
  Learning* (SML) index. The original model assesses tasks against nine
  criteria; this report explicitly names four of them (see Method
  point 2) — **the other five are not itemized in this report's
  source**, don't invent them, use only these four until the owner or
  a more precise source fills in the rest.
- Nuvepro (2026) — *The Dual Decomposition Framework: People Path +
  Process Path*.

## Method

1. **Choose the scope of the review.** One role/team (People Path) or
   one value-chain/process stage (Process Path) — don't try to do both
   at once on the first pass. If the Process Path view is missing
   entirely so far, first do a rough value-chain mapping (see
   `../../../business-design-frameworks/skills/value-chain-mapping/SKILL.md`)
   before this deeper task-level decomposition.
2. **Decomposition line for a People Path review:** Organization →
   Department → Role → Tasks. **Decomposition line for a Process Path
   review:** Value chain → Workflow → Tasks. Both lines converge at the
   task level — this is intentional: the same task often shows up from
   both perspectives and is worth cross-checking.
3. **Gather the task list in a data-driven way, not just from
   interviews.** Interviews systematically underestimate the amount of
   routine work (people forget/downplay repetitive small tasks). Use
   where applicable:
   - **Process Mining** (e.g. Celonis, UiPath Process Mining) —
     extracting the process's real-world executions from system logs
     (ERP, CRM): long lead times, rework loops, manual data-transfer
     steps between systems.
   - **Task Mining** — tracking at the level of user screens/actions:
     points where an expert copies information from one system to
     another or looks up information across multiple documents at
     once.
   - **Cognitive friction analysis** — where the employee's mental load
     is highest (e.g. analyzing a long document vs. the final decision
     based on it) — these are the points where Augment-type support is
     often more valuable than Automate.
   If none of these tools are in use, do the same analysis in a
   lighter form: have the employee keep a log for one day of every
   switch from one system to another and every point where they feel
   uncertainty or load.
4. **Classify every task against four SML criteria (1–5 or yes/no):**
   - **Input and output clarity** — does the task have a clearly
     definable digital input and output?
   - **Cognitive nature** — is the task based on pattern recognition,
     language translation, summarization, or data classification
     (natural fit for AI), or on physical presence, negotiation, or
     ethical judgment (not)?
   - **Error tolerance** — can the process tolerate a non-deterministic,
     probability-based result (e.g. a draft, a proposal), or does it
     require 100% deterministic accuracy (e.g. drug dosing, statutory
     reporting)? A quick illustrative split, useful for calibrating this
     judgment: billing logic and access/permissions decisions are
     deterministic — no error margin is acceptable, and the routing in
     `../../../human-ai-collaboration-design/skills/hitl-maturity-and-confidence-routing/SKILL.md`
     should treat them accordingly; content summarization and creative
     ideation are probabilistic — they benefit from linguistic flexibility
     and contextual synthesis, and forcing deterministic precision onto
     them wastes the model's actual strength.
   - **Time scale and response time** — does the task require a
     split-second reaction (real-time) or deep, long-term
     deliberation?
5. **Classify every task into one of three categories:**
   - **Automate** — AI/an agent performs the task independently
     without human intervention. Typically: routine, high volume,
     deterministically verifiable.
   - **Augment** — AI acts as a human assistant/co-agent
     (human-in-the-loop). Typically: complex decision-making, creative
     drafting, expert background research, context retrieval.
   - **Human-Only** — stays entirely with a human. Typically:
     strategic judgment, high-stakes negotiation, physical presence,
     ethical decision-making.
6. **Produce a structured task list** with three columns: task /
   SML assessment in brief / classification (Automate/Augment/
   Human-Only) + justification. This is the input to the
   `../ai-opportunity-portfolio/SKILL.md` skill, where Automate and
   Augment tasks are grouped into larger opportunities and scored.
7. **Watch for two systematic mistakes:** (a) don't classify an entire
   role as "Automate" at once just because some of its tasks are —
   most roles are a mix of task types; (b) don't classify a task as
   Human-Only just because it's complex — complexity by itself doesn't
   rule out Augment-level AI support, it just raises the error-tolerance
   requirement.

## What this skill does NOT do

- Doesn't assess a task's/opportunity's business value or feasibility
  more broadly — that's `../ai-opportunity-portfolio/SKILL.md`'s job.
  This skill only answers "does this task suit AI at all, and at what
  level," not "is it worth doing."
- Doesn't replace `../../../business-design-frameworks/skills/value-chain-mapping/SKILL.md`
  for function-/process-level mapping — this skill goes one level
  deeper, into individual tasks within functions.
- Doesn't do technical feasibility assessment (model choice,
  architecture) — that's `../ai-use-case-feasibility-and-poc-scoping/SKILL.md`'s
  job at a later stage.
- Doesn't include the full nine-criterion SML model — only the four
  criteria the source material itemized. Don't present the other five
  criteria as established without a more precise source.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb about which task types most often surprise
  you (assumed Human-Only but turns out Augment-eligible, or vice
  versa)
- concrete examples of using process mining / task mining tools in
  your own engagements (into `../../references/`)
- the SML model's remaining five criteria, if you find them in a more
  precise primary source (Brynjolfsson & Mitchell 2017/2019)

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this (if the value chain isn't mapped yet):
  `../../../business-design-frameworks/skills/value-chain-mapping/SKILL.md`
- Next in this pack: `../ai-opportunity-portfolio/SKILL.md` —
  groups and scores the Automate/Augment tasks this skill produces
  into opportunities.
- A parallel, top-down approach (a faster first-pass mapping before a
  detailed process description): `../ai-capability-pattern-matching/SKILL.md`
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../../human-ai-collaboration-design/references/hitl-partnership-heuristics-research.md` —
  grounding for the deterministic/probabilistic worked example added to
  the error-tolerance criterion
- `../../CLAUDE.md` — the pack's shared guardrails
