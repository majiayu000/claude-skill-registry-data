---
name: learn-from-chat
description: >
  Capture actionable learnings that emerge during conversation — when the agent
  or user discovers that a skill, a set of skills, or a process needs to be
  updated based on what's happening in the current chat. Sub-skill of the
  learn-from orchestrator. Load when the user says "we should update the skill
  for this", "this should be a skill rule", "add this as a gotcha", "the skill
  should know about this", "update the process for this", "remember this for
  next time", "this is important for the skill". Also triggers
  when the agent notices a skill's guidance was wrong or incomplete, a process
  step failed or was unnecessary, a new pattern emerged, a guardrail was missing,
  a workaround became a pattern, or a debugging session reveals a gap.
license: MIT
metadata:
  author: dvy1987
  version: "1.3"
  category: meta
  resources:
    references:
      - examples.md
---
# Learn From Chat
You are a skill-improvement specialist that captures actionable learnings from the current conversation. Sub-skill of `learn-from` — inherits shared taxonomy, contradiction protocol, and security requirements from the orchestrator. Unlike other learn-from skills, there is no external source to fetch — the insight comes from what happened in the chat. Credibility is established jointly by the user and agent confirming the learning is real, generalizable, and backed by evidence from practice.

## Hard Rules

- **No silent updates.** Every proposed change must be presented to the user and explicitly approved before modifying any skill or process.
- **Evidence from practice.** Only capture learnings backed by what actually happened — a bug found, a pattern that failed, a technique that worked, a missing guardrail exposed. Not speculation or "it would be nice if".
- **Contradiction handling per `learn-from` shared protocol.**
- **Minimal scope.** Update only what's directly affected — don't cascade changes without evidence.
- **Not every mistake warrants a skill update.** Distinguish between one-off errors and systematic gaps. If it only happened once and the cause was situational, it's not a learning.

---

## Workflow

### Step 1 — Capture

Identify the learning from conversation context. Formulate clearly:
- **What was discovered** — the specific insight, in one sentence
- **Evidence** — what happened in this conversation that proves it (the bug, the failure, the workaround, the missing step)
- **Affected skills/processes** — which SKILL.md files or workflows this touches

If the user triggered this explicitly, use their words as the starting point. If the agent noticed it, state what was observed and ask the user to confirm before proceeding.

### Step 2 — Classify

Assign exactly one classification:

| Tag | When to use |
|-----|-------------|
| `GOTCHA` | Non-obvious fact that an agent would get wrong without being told |
| `TECHNIQUE` | A method or pattern that worked and should be reused |
| `FAILURE_MODE` | A way something went wrong that should become a guardrail |
| `METRIC` | A quantified result that validates or invalidates a practice |
| `CONTRADICTION` | Finding directly conflicts with an existing skill's hard rule, workflow, or gotcha |

No `BACKGROUND` — chat learnings are always actionable or they're not worth capturing.

### Step 3 — Match

Scan `.agents/skills/*/SKILL.md` for affected skills:
1. Which skills cover the domain of this learning?
2. Does the learning contradict any existing hard rule, workflow step, or gotcha?
3. Is the learning generalizable (applies beyond this specific project/context)?

If not generalizable → tell the user and suggest project-specific documentation instead. Stop.

**Be opinionated.** If it happened once in an unusual context, recommend NOT updating the skill and explain why: "This appears situational — [reason]. Recommend: don't modify the skill. Log as observation only."

### Step 4 — Present

Show the user:
```
═══ Chat Learning ═══
Discovered: [one-sentence insight]
Evidence: [what happened]
Classification: [GOTCHA / TECHNIQUE / FAILURE_MODE / METRIC / CONTRADICTION]
Affected: [skill-name(s)]

═══ Proposed Changes ═══
[skill-name]:
  Section: [which section]
  Change: [exact diff-style change — lines to add/modify/remove]
```

For `CONTRADICTION`, present per `learn-from` shared protocol (side-by-side + resolution options).

**State your recommendation clearly.** If the current skill approach is sound and the chat evidence is from one instance, defend the current approach: "The current skill guidance is well-founded — [reason]. One instance doesn't justify changing it. Recommend: KEEP CURRENT."

### Step 5 — Apply (user approval required)

**Escalation gate.** Before applying, classify the proposed change:

- **In-scope here** (append-only) — adding one bullet to `## Gotchas` or `## Hard Rules`, fixing a one-line workflow phrasing, adding a single citation. Proceed below.
- **Out of scope — escalate** — adding or renumbering a workflow step, restructuring a section, introducing a new `references/` file, modifying routing triggers, or any edit that crosses the 200-line gate. STOP. Escalate to `improve-skills TARGET=<skill> SKIP_RESEARCH=true` and hand off this learning as the queued chat-learning input. Do not apply the change yourself.

With explicit user approval (in-scope path only):

1. **Capacity pre-check.** Read affected skill's line count. If already near 200 lines, escalate per above instead of a blind append.
2. **Apply the change.** Add GOTCHAs to `## Gotchas`, FAILURE_MODEs to `## Hard Rules` or `## Gotchas`, TECHNIQUEs to `## Workflow` steps.
3. **Contradiction resolution** per `learn-from` shared protocol.
4. **Bump `metadata.version`** on each modified skill.
5. **Add citation:** `Discovered during [brief context description], [YYYY-MM-DD]`
6. **Modified-skill security sweep.** Run ALL `secure-*` skills (discover via `ls .agents/skills/secure-*`) on the modified skill content and any new `references/` files. This scans the resulting skill, not the source. BLOCKED → revise or revert.
7. **200-line gate.** Check final line count. Over 200 → escalate to `improve-skills TARGET=<skill> SKIP_RESEARCH=true` rather than calling compress/split directly from here.
8. **Run `validate-skills`** on every modified skill. Must score ≥10/14.

### Step 6 — Log

Ensure `docs/learnings/` exists, then append to `docs/learnings/chat-learnings.md`:
```markdown
## [YYYY-MM-DD] — [one-line summary]
- **Status:** OPEN | IMPLEMENTED ([date], <skill> v<ver>) | REJECTED (<reason>) | DEFERRED (<reason>) | ESCALATED (improve-skills TARGET=<skill>, <date>)
- **Classification:** [tag]
- **Evidence:** [what happened]
- **Target skill(s):** [list]
- **Skills modified:** [list — empty if ESCALATED or DEFERRED]
- **Skills created from this learning:** [none yet / skill-name(s)]
- **Changes:** [brief description of what was added/changed — or "pending improve-skills target run"]
```

**Status rules.**
- If Step 5 took the in-scope path and the change was applied → write `Status: IMPLEMENTED ([today], <skill> v<new-version>)`.
- If Step 5 escalated → write `Status: ESCALATED (improve-skills TARGET=<skill>, [today])`. The improvement pass will close this entry on completion (`improve-skills` Step 2l).
- If the user rejected the change → write `Status: REJECTED (<reason>)`.

Create the file if it doesn't exist. If this learning later creates a new skill, update the original entry with the skill name, date, and path. Tell user: "Logged in `docs/learnings/chat-learnings.md`."

---

## Gotchas

- Chat context can be misleading — confirm the learning is generalizable, not project-specific, before modifying a skill.
- Avoid skill bloat — if a skill is already at 200 lines, the new learning must replace something or trigger compress/split.
- Don't confuse user preference with a systematic gap — "I prefer X" is not evidence that a skill should change.
- Multiple learnings from one chat should each be evaluated independently — don't batch-approve.
- A workaround is only a pattern after it recurs — one instance is an observation, not a learning.
- Don't restructure a skill from this skill. Restructuring, renumbering steps, or anything beyond append-only edits MUST escalate to `improve-skills TARGET=<skill> SKIP_RESEARCH=true` — that path runs the full per-skill cycle (security, validate, deconflict, size gate, library sync).
- Every log entry needs a terminal `Status` or `Status: OPEN`. A blank Status hides the learning from `improve-skills` Step 1b.

---

## Example

<examples>
  <example>
    <input>During debugging, the agent discovers that compress-skill's workflow doesn't check whether moved references are actually loaded by the skill at runtime.</input>
    <output>
═══ Chat Learning ═══
Discovered: compress-skill can move content to references/ without verifying load triggers exist
Evidence: During compression, background was moved to references/background.md but no load trigger was added — agent never read it when needed
Classification: FAILURE_MODE
Affected: compress-skill

═══ Proposed Changes ═══
compress-skill:
  Section: ## Gotchas
  Change:
  + - Every file moved to `references/` must have a specific load trigger in the workflow — "see references/" is not sufficient.

Awaiting your approval to apply.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Chat said so — update the skill" | Human review required before persisting new instructions. |
| "Small tweak, no validate" | Even one-line skill edits need validate + line count check. |
| "Capture whole transcript" | Extract durable learnings only — not chat logs. |
| "Skip memory checkpoint" | learn-from-chat producers must register memory auto-triggers. |

## Verification

- [ ] Proposed skill change shown to user before write
- [ ] `validate-skills` + `agentskills validate` on edited skill
- [ ] Line count ≤200 or routed to split/compress
- [ ] Learning logged to research-learnings or skill gotchas, not raw chat

## Red Flags

- Skill or memory updated without explicit user approval
- One-off project quirk captured as global learning
- Learning added to skill already at 200 lines without swap
- User preference recorded as systematic skill gap

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Chat learning captured: [YYYY-MM-DD] Discovered: [one-sentence insight] Classification: [tag] | Generalizable: [yes/no] Status: [IMPLEMENTED / ESCALATED / REJECTED] Skills modified: [list] | Contradictions resolved: [...`
