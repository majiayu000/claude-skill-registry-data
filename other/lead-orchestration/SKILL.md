---
name: lead-orchestration
description: "Use when you are the LEAD (main session) and an owner request arrives that needs agents -- intake, routing, briefs, follow-up, blocks, verification, learning, report. Canonical procedure from request to verified report; not for sub-agents executing a brief."
references: references/brief-template.md, references/worked-examples.md
related-skills: apex-methodology, verification, challenge, sniper-check
---

<objective>
One procedure for the lead, from an owner request to a verified report. It sequences rules that live elsewhere -- it does not restate them. Each step names its source of truth and ends with a **Check**: the step is not done until the check holds.

It exists because the owner kept doing the lead's job: asking "is it moving?", re-stating parts the lead dropped, finding visual defects the lead reported as done, typing steps the lead could run. Every step below targets one of those failures (see `references/worked-examples.md`).
</objective>

# Lead Orchestration

## Sources of truth (link, never copy)

| Topic | Canonical file |
|-------|----------------|
| HARD STOPS, RECURRING TRAPS, AUTONOMY | `plugins/claude-rules/templates/CLAUDE.md.template` |
| Lead = coordinator, scope ladder, two-speed communication, ownership, follow-up, idle != done, re-dispatch clause | `plugins/claude-rules/rules/03-agent-teams.md` |
| Hook compliance, mandate quality, exit contract, no hand-back | `plugins/claude-rules/rules/08-subagent-conduct.md` |
| Done = sniper + verification, response language | `plugins/claude-rules/rules/00-critical-rules.md` |
| Release flow, external executors never release | `plugins/claude-rules/rules/06-tooling-rules.md`, agent `fuse-ai-pilot:commit` |
| Phases Analyze -> eXamine | skill `apex-methodology` |
| Functional proof / adversarial check | skills `verification`, `challenge` (agent `challenger`) |

---

## Procedure

### 1. Intake -- the request as a checklist
Restate the request as numbered named parts, including negative constraints ("don't touch X") and any reference the owner sent (mockup, file, style). An owner message mid-task amends the list: add the part, tell the running agents, keep going -- only an explicit stop halts.
**Check:** every sentence of the owner maps to a part; nothing in the list was invented by you.

### 2. Route -- one agent per task
Split the checklist into tasks and route by TASK: one agent per task, and the task owns every file it needs. Two tasks that must edit the same file are merged into one task or sequenced (the second starts after the first is verified on disk). Use the scope ladder (rule 03) to size the work.
Pick the domain agent from Project Detection AND the skills it must load: the stack's SOLID skill via `fuse-solid:solid-detection`, the domain skills (e.g. `design-method` -> `design-web`/`design-ios`, `motion-method` -> `motion-*`, `swiftui-core`...), plus `verification`. The lead loads only `lead-orchestration` (and `apex-methodology` to plan); it never applies domain skills itself.
Before sending anyone into a folder: `ls -lT <folder>` + `date` -- mtime under ~5 min = busy, send no one there. Announce the budget (agents, expected duration) in one line.
**Check:** each task has exactly one agent; no file is owned by two concurrent tasks (merged or sequenced instead); no task targets a busy folder.

### 3. Brief -- self-contained mandate
Fill `references/brief-template.md`: context, exact files, the owner's words quoted verbatim, guardrails, proof required, report format. A protected path (HARD STOP 3: `~/.claude`, `~/.codex`, deployed marketplace, install scripts) goes into a brief only when the owner named it -- quote his exact sentence; the agent writes that target and nothing else.
**Check:** an agent with zero conversation context could execute it; every checklist part from step 1 appears as an acceptance criterion; the brief contains no "ask the owner if…" escape hatch.

### 4. Delegate everything
The lead never edits project files -- only its own memory and scratchpad. Every edit, even one line in a skill or rule, goes to an agent -- the only exception: after 2 failed delegations on a localised, already-measured defect, the lead reads and fixes it itself (the only case where the lead edits). External executors (Kimi / Codex / Cursor) write code only: never push, PR, merge, tag or publish -- releases go through the `fuse-ai-pilot:commit` agent.
**Check:** your own tool calls since intake contain no Write/Edit on project files (except the 2-failed-delegations case); no external executor brief mentions git release steps.

### 5. Follow -- the owner never asks "is it moving?"
Poll every running executor (output file, mtimes, transcript) at a fixed cadence; give the owner a one-line status (done / blocked / next) without being asked. Stall = no new output on disk since the last poll -> push it via `SendMessage` with the precise next step. Resume the same agent with `SendMessage`; never spawn a duplicate on the same mandate. Relaunch cap: after 2 failed delegations on a localised, already-measured defect, the lead reads and fixes it itself (the only case where the lead edits); any other blocked mandate past the rule-08 cap (3 cycles) -> escalate to the owner with a root-cause note. No relaunch loop. A message does not stop an agent: use TaskStop, then confirm mtimes froze.
**Check:** you can answer "where is it?" with the last measurement (time, files changed, tests), never "I don't know".

### 6. Blocks -- find the legitimate route
Before handing anything back, try every authorized path: trash instead of delete (`mv <f> ~/.Trash/`), a scriptable source instead of a blocked site, the page's own file/CDN link or an API instead of a bot-walled page, a real browser session instead of a plain fetch. A hook or gate refuses: read its source and do exactly what the message says before calling it a bug (rule 08 Hook Compliance). Only a CAPTCHA, a password, or an approval the hook requires the owner to type goes back -- one line, exact text to type.
**Check:** the hand-back names the routes already tried; the gate source was read when a gate is blamed.

### 7. Verify -- open the real output
Open the actual deliverable: screenshot / extracted frames / runtime against the real target (dev server, DB, installed version -- not the manifest or an isolated fixture). Tick each checklist part by name. Then: `sniper` after any code change (once, after all agents finish); `challenger` before any root-cause, done/verified claim, irreversible action or 2nd-time fix. Unproven part = write "not verified". Proven = state it as guaranteed with its proof; never open with "I can't guarantee".
**Check:** each part has a proof artifact path or is marked "not verified"; sniper and challenger verdicts are in hand; the report lists the skills consulted -- a missing one = not verified.

### 8. Learn -- each correction becomes a rule
Each owner correction -> one line in the skill/agent that failed, in the source repo, the same turn (rule 03 #11). Sync to the marketplace only when the owner asked for it (HARD STOP 3). Record durable owner preferences in memory.
**Check:** the correction is grep-able in the failing skill/agent before the turn ends.

### 9. Report -- answer first
Owner reply, in the owner's language (rule 00): first line = the answer (done / not done / blocked), then <= 10 lines total, one recommendation + the next step, no option menu when one choice is clearly better. Deliverables at a path the owner sees (visible folder, sent file, link) -- never only a hidden directory.
**Check:** line 1 answers the question asked; every deliverable path is outside a dot-folder.

---

## Critical rules (pointers)

1. A mandate is the go -- reversible steps inside it need no question (template AUTONOMY).
2. Never invent a cap, path or constraint the owner did not state (template RECURRING TRAPS).
3. A short positive verdict from an agent is not global -- re-check it covers the NAMED defect.
4. An owner verdict that contradicts your measurement wins -- propagate it to every brief already dispatched.

## Reference Guide

| Need | Reference |
|------|-----------|
| Writing a brief (step 3) | [brief-template.md](references/brief-template.md) |
| Bad vs good lead behaviour from real sessions | [worked-examples.md](references/worked-examples.md) |
