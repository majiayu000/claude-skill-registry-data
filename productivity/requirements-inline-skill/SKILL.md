---
name: requirements-inline-skill
description: >-
  In-session requirements delegate — runs the AC-quality detection gate,
  grills reviewer-emitted Requirements Gaps inline (Mode R, agent file as
  checklist), and drafts BRD/SRS in-session with native questioning (Mode
  A). Thin wrapper: templates stay in the specs skill; never spawns a
  subagent. Triggers: requirements detection gate, grill requirements gaps,
  inline requirements.
license: Apache-2.0
compatibility: opencode
metadata:
  mirrors: requirements-specialist-subagent
category: Planning & Alignment
---

# Requirements (inline)

You are executing the requirements specialist's workflow **in this session**.
The subagent's isolation and its headless relay dance (Modes A/B exist
precisely because a spawned session cannot ask questions) are replaced by
this session's native questioning — apply the discipline below, and never
delegate the work.

**You are a wrapper, not a copy.** Mode conduct lives in the deployed
`agents/requirements-specialist-subagent.md` (loaded as checklist); BRD/SRS
templates live in `civiltekk-requirements-specs-skill`; interrogation
methodology lives in `grilling-skill`. This file owns the detection decision
tree and the invocation loop only.

## Detection decision tree (pipeline route)

**Inputs:** the ticket's acceptance criteria, the PLAN's AC section, the Step
7 triage outcome (reviewers-selected count), and whether the ticket is new
work or a retry.

1. **Skip rule (default):** AC quality passes AND at least one reviewer was
   selected → report `skip` (one line: why), continue to reviewer triage.

   Branch hinges on judgment (thin-vs-substantive ACs, ambiguity calls)?
   Optionally consult the `laya_classify` tool with the statement — it returns
   calibrated p(yes) per question (local, offline); weigh the probabilities and
   decide. Deterministic checks (field presence, counts, template shape) stay
   in code — never classify what a rule already answers.
2. **AC-quality rule:** run the interrogation route when ANY holds —
   fewer than 3 ACs; ambiguity markers (vague quantifiers like "fast"/"most",
   "and/or" coupling, no verifiable predicate an implementation can
   pass/fail); or two ACs that conflict.
3. **Zero-reviewer rule:** triage selected no reviewers AND the ticket is new
   work → run the interrogation route regardless (there is no rider duty to
   carry requirements verification).
4. **Interrogation route:** apply `grilling-skill` methodology to the
   suspect ACs — one question at a time through the session's question
   capability, each with a recommended answer grounded in the ticket body and
   PLAN. Apply answers to the ticket body and/or PLAN ACs (edits land in the
   caller's working tree; list every file changed). Cap: 2 rounds, then
   surface the residue and proceed on documented defaults.

This gate is data-driven AC interrogation before reviewers run. It is NOT a
PLAN review by requirements-specialist (the stage-mismatch decision stands —
Mode R's designed input remains reviewer-surfaced gaps).

## Mode R route (review-gap relay)

Resolve the checklist (§Checklist resolution), load `reviewer-baseline-skill`
conduct, then per the checklist's Mode R: for each gap, sharpen
`suggested_question` into one concrete question with a recommended answer
grounded in the gap's evidence. Return `Questions for the user` — one per
gap. Max 2 relay rounds per review (caller-enforced; state the round number).

## Mode A route (in-session drafting)

Resolve the checklist, then per its workflow (Steps 0–5) with the interactive
caveat inverted: you HAVE the question channel — use it instead of relay
rounds. Doc-type routing tree, templates, and file conventions come from
`civiltekk-requirements-specs-skill` (matching `brd`/`srs` route). Drafts
land at `docs/{brd|srs}/{BRD|SRS}-draft-{slug}.md` in the caller's working
tree.

## No-subagent pin

This skill runs fully in-session. Do NOT delegate requirements work to a
subagent — no Task calls, no child sessions, no Mode A/B relay round-trips.
The isolated-child variant is a different invocation
(`requirements-specialist-subagent` via the v1 arm or direct delegation),
not an escalation path available here.

## Checklist resolution

Capability binding (per the portability contract — the agent self-selects
its row; unknown harnesses fall through to the fallback):
- OpenCode: `~/.config/opencode/agents/requirements-specialist-subagent.md`
  (deploy-mode CLI path)
- Claude Code: `~/.claude/agents/requirements-specialist-subagent.md`
- Other/none: Mode A/B → proceed checklist-less with the specs skill alone,
  noting the degraded run; Mode R → surface the gaps to the user directly
  and proceed on their answers (the pipeline's documented fallback). Never
  spawn a subagent in place of the checklist.

## Scope bounds

- No tickets, branches, PLAN files, or implementation — that is
  `ticketing-skill` / `worktree-pipeline-skill` / the executor.
- No BABOK/IEEE-830 template content in this file — the specs skill owns
  templates; the agent file owns routing conduct.
- Customer-facing discovery is `discovery-specialist-subagent`'s job — never
  yours, inline or otherwise.

## Enforcement deltas (vs requirements-specialist-subagent)

| Subagent enforcement | Inline discipline (you) |
|---|---|
| Fresh context window | State the route, inputs, and detected signal before interrogating so scope drift is visible |
| Headless relay (Modes A/B) | Question natively in-session; relay rounds are gone, not wrapped |
| `question: deny` frontmatter | You MAY question — through the session's question capability, one at a time with recommendations |
| Caller-enforced round caps | State the round counter (1/2, 2/2) in every interrogation message |

## Output contract

**Status:** [success | partial | failed] — `partial` when rounds exhausted with residue
**Output:** route taken + signal detected (skip line when skipped) + files changed + questions/answers applied (detection), `Questions for the user` list (Mode R), or draft path + parts count (Mode A)
**Summary:** ≤3 sentences, plain language
**Issues:** blockers, unresolved residue, or "None"
