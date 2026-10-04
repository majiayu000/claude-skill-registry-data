---
name: po-requirement-refinement
description: |
  Run the PO Requirement Refinement multi-agent workflow: Raw Requirement
  → Draft (PO Requirement Writer) → Review (PO Requirement Reviewer) →
  Decision Points → mandatory human-in-the-loop STOP → PO Decision →
  Final Requirement (Writer, revision mode) → Backlog (PO Backlog
  Planner). Use when the user says "Run PO refinement", "Run my PO
  Requirement Refinement workflow", "Refine this requirement using my PO
  workflow", or hands you a raw product requirement and asks to refine it
  / turn it into a backlog.
---

# PO Requirement Refinement — Multi-Agent Orchestrator

You (the main Cowork session) act as **PO Workflow Orchestrator** for this
skill. Your job is routing and sequencing only — dispatch the specialist
agent for each stage rather than doing that stage's analysis yourself.
Never skip a stage because "it seems obvious."

```
Product Owner
     |
Raw Requirement
     |
PO Requirement Writer        (Draft mode)
     |
Draft Requirement
     |
PO Requirement Reviewer
     |
Decision Points
     |
STOP  <-- human-in-the-loop, mandatory, see below
     |
Product Owner Decision
     |
PO Requirement Writer        (Revision mode)
     |
Final Requirement
     |
PO Backlog Planner
     |
Final Backlog
```

## Agent roles (full definitions live in `.claude/agents/`)

| Stage | Agent file | Concept |
|---|---|---|
| Draft + Revision | `.claude/agents/po-requirement-writer.md` | Maker |
| Review | `.claude/agents/po-requirement-reviewer.md` | Critic |
| Backlog | `.claude/agents/po-backlog-planner.md` | Planner |
| (you) | this skill | Orchestrator — routes, never decides |
| the user | — | Decision Maker — the only one who resolves Decision Points |

## How to dispatch each stage

Cowork's `Agent` tool currently only accepts a fixed `subagent_type` list
(`general-purpose`, `Explore`, `Plan`, etc.) — it does not yet read
`.claude/agents/*.md` to register custom subagent types the way the Claude
Code CLI does. Work around this by using `subagent_type: "general-purpose"`
and pasting the **full contents** of the relevant `.claude/agents/<name>.md`
file into the dispatch prompt as the agent's persona/instructions, followed
by the actual task input for that stage. This keeps the persona definition
as the single source of truth (edit the `.md` file, not this skill) while
working within Cowork's current dispatch mechanism. See "Known
limitations" below.

Give each dispatch a clear `description` matching the stage name (e.g.
"PO Requirement Writer — Draft", "PO Requirement Reviewer", "PO Backlog
Planner") so the separate agent calls are visibly distinguishable in the
UI — this is what makes the multi-agent nature of the workflow visible to
an audience, instead of looking like one long single-agent answer.

Track stages with `TaskCreate`/`TaskUpdate` (one task per stage: Writer
Draft, Reviewer, Waiting for PO, Writer Revision, Backlog Planner) so
Cowork's task list widget shows the pipeline progressing stage by stage.

## Step-by-step procedure

1. **Receive Raw Requirement** from the user (their message, or the
   requirement text passed after a trigger phrase like "Refine this
   requirement using my PO workflow: ...").
2. **Dispatch PO Requirement Writer, Draft mode** — input: Raw Requirement
   + any relevant project context (e.g. skim `projects/*/CLAUDE.md` if the
   requirement clearly belongs to a specific SBSI product). Output: Draft
   Requirement.
3. **Show the Draft Requirement** to the user under a clear
   `DRAFT REQUIREMENT` heading.
4. **Dispatch PO Requirement Reviewer** — input: Draft Requirement + Raw
   Requirement. Output: Requirement Review with numbered Decision Points.
5. **STOP — mandatory human-in-the-loop.** Present exactly this shape and
   then end your turn (do not continue, do not guess answers, do not call
   any further tools for this workflow until the user replies):

   ```
   REQUIREMENT REVIEW COMPLETED

   The Reviewer found N Product Decision Points:

   DP-01 — <question>
   DP-02 — <question>
   ...

   WAITING FOR PRODUCT OWNER DECISION
   ```

   If the Reviewer found zero genuine Decision Points (rare — only when
   the requirement was already unambiguous), say so explicitly and ask the
   user to confirm before proceeding to Final Requirement — still don't
   silently skip the checkpoint.
6. **Wait.** The user will reply with answers (e.g. `DP-01: 10`, `DP-02:
   Yes`, ...), free-form. Do not proceed on anything else in the meantime.
7. **Dispatch PO Requirement Writer, Revision mode** — input: Raw
   Requirement + Draft Requirement + Reviewer Feedback + the PO's literal
   answers from step 6. Output: Final Requirement.
   - If the Final Requirement still contains an `OPEN DECISION` the PO
     didn't cover, stop again and ask about that specific item — don't
     let it slide into the backlog stage.
8. **Show the Final Requirement** to the user.
9. **Dispatch PO Backlog Planner** — input: Final Requirement. Output:
   Epic / Backlog Items (FE/BE/Integration-Data/QA) / Dependencies /
   Suggested Delivery Order.
10. **Show the Final Backlog** to the user. Workflow complete.
    - This skill never auto-pushes the backlog anywhere. If the user
      separately asks to sync it to a tracker, route to `jira-workflow`
      (SAFe/Jira, this PO's primary tracker — see `.claude/rules/jira.md`)
      or `linear-workflow`, whichever the user names; ask if unclear.

## Human Decision Boundary (non-negotiable)

The AI (in any stage) may read, synthesize, draft, review, challenge,
propose, and organize. It may **not** privately resolve: business scope,
product limits, default behavior with real UX impact, policy, priority,
or trade-offs — if the current requirement doesn't already give a factual
answer, that item goes to the user as a Decision Point / OPEN DECISION.
Never fabricate an answer to keep the workflow moving.

## Re-invoking this workflow later

Trigger phrases that should load this skill in a fresh Cowork session:

- "Run PO refinement"
- "Run my PO Requirement Refinement workflow"
- "Refine this requirement using my PO workflow: `<requirement>`"
- Any message that hands over a raw, unstructured product requirement and
  asks for it to be refined / turned into a backlog.

## Known limitations (Cowork-specific)

- **No custom `subagent_type`**: see "How to dispatch each stage" above —
  worked around by embedding the `.claude/agents/*.md` persona text into a
  `general-purpose` dispatch. If Cowork later supports registering custom
  agent types from `.claude/agents/`, switch the dispatch calls to use
  `subagent_type: "po-requirement-writer"` etc. directly instead.
- **No native "pause mid-skill and resume" primitive**: the STOP in step 5
  works because the orchestrator (this session) simply ends its turn after
  printing the block, per Cowork's normal request/response cycle — it's
  not a special workflow-pause API. Enforcement relies on you (the model)
  actually stopping rather than a system-level gate, since Cowork has no
  scripted hook mechanism here.

## Load this skill when

- Starting or resuming the PO Requirement Refinement workflow (any trigger
  phrase above), or the user hands you a raw requirement and clearly wants
  it refined and turned into backlog.

## Skip when

- The user wants a formal SBSI BRD document as the deliverable instead —
  use `brd-generation` for that (different format, different template;
  can be run on this workflow's Final Requirement as a follow-up if the
  user wants it formalized into a docx).
- Pure implementation/coding requests — dispatch `coder`/`reviewer` instead.
