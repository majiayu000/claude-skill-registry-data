---
name: pd-spawn
description: >
  Spawn another Project Director to do work on your behalf. The caller PD
  creates a briefing, tags the spawned PD in both projects' memory, then waits
  for a report. Use when the operator says "spawn {other-pd} to do X". The spawned PD
  works in its own project, reads only its identity + your briefing, and reports
  back when done.
triggerPatterns:
  - "work with {slug}-pd to"
  - "have {slug}-pd do"
  - "{slug}-pd, work on"
  - "{slug}-pd, can you"
---

# PD Spawn Protocol

Spawns another PD on the operator's command. Caller PD creates the briefing, spawns
the other PD, tracks the delegation in its own memory, and waits.

## Activation Triggers

This skill activates in two ways:

1. **Slash command:** `/pd-spawn`
2. **Natural language:** Any phrase matching one of these patterns:
   - `"work with {slug}-pd to do {task}"`
   - `"have {slug}-pd do {task}"`
   - `"{slug}-pd, work on {task}"`
   - `"{slug}-pd, can you {task}"`

When you hear a phrase matching any pattern above, invoke this skill immediately
— do not attempt to do the work yourself.

## SSOT: medium-term.md

The list of active PDs and their project paths is in `~/.claude/memory/medium-term.md`.

## Step 1 — Identify the Target PD

From medium-term.md, find:
- `{target-slug}` — the project slug
- `{target-pd-name}` — the PD's agent name (e.g. `example-pd`)
- `{target-memory-path}` — the project's memory directory

## Step 2 — Create the Task ID

Generate: `{YYYYMMDD}-{slug}-{n}` e.g. `20260416-website-pitch-1`

## Step 3 — Create Incoming Briefing

`{caller-name}` used below resolves per Step 3.5/5's rule (`{caller-pd-name}` if
the caller is a PD, else `parent-ai (operator direct)`) — resolve `caller_type` now,
even though Step 3.5 documents the rule in full.

Write to the **target PD's** inter-spawn-tasks folder:
`{target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}.md`

```markdown
# Inter-Spawn Task — {task-id}

**Created by:** {caller-name} (on behalf of the operator)
**Created at:** {ISO timestamp} UTC
**From PD:** {caller-name}
**To PD:** {target-pd-name}
**Status:** INCOMING

## End Goal
[Taken verbatim from the operator's instruction — state the outcome, not the method]

## Available Assets & Context
- Branding: [paths from the operator's instruction or project memory]
- Content: [paths or "none specified — use best judgment"]
- Stack: [from target project's CLAUDE.md if known]
- Other: [any other context the operator provided]

## Constraints
- [Any constraints the operator named]
- Default: work in spawned PD's own project directory
```

## Step 3.5 — Resolve Caller Type

Determine the caller before Step 4:

- **Caller = PD** (default): caller is `{caller-pd-name}`, owns `{caller-project}/memory/tasks/`. Use canonical paths in Steps 4 + 5b.
- **Caller = parent-ai** (operator direct): parent-ai has no `{caller-project}` of its own — it has no durable memory folder at all. This does NOT mean the task is ownerless. `/pd-spawn` always names a `{target-slug}` in Step 1, and that target project IS the task's owner (task ownership follows the project the work is ABOUT, not the session that initiated it — see `core/memory/lessons/agent-workflows.md`, "pd-spawn caller_type branch — inbox misfiling correction" entry). File the delegation-tracking file inside the **target** project instead:
  - Caller's delegation file → `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md`
  - Completion target in Step 5b → same file
  - Spawn prompt's `{caller-completion-path}` resolves to this same in-target-project path — no external write outside `{target-project-root}/` is ever needed for a parent-ai caller
  - The delegation file MUST state `**Delegated by:** parent-ai (operator direct)` for traceability
  - **The global inbox (`{agency-root}/tasks/inbox/`) is NEVER used by `/pd-spawn`.** Inbox is reserved exclusively for tasks with no existing owning project at all — `/pd-spawn` by construction always has one (the target project named in Step 1).

Record `caller_type = pd | parent_ai` for use in Steps 4 + 5 + 5b.

## Step 4 — Create Caller's Delegation Task

Write the canonical delegation file to:
- `caller_type = pd` → `{caller-project}/memory/tasks/ongoing/delegated-{task-id}.md`
- `caller_type = parent_ai` → `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md` (inside the **target** project — see Step 3.5 rationale)

Canonical delegation file format (both caller types — `{caller-name}` resolves per Step 5's substitution rule: `{caller-pd-name}` for `pd`, `parent-ai (operator direct)` for `parent_ai`):

```markdown
# Delegated Task — {task-id}

**Delegated by:** {caller-name}
**Delegated to:** {target-pd-name}
**Status:** DELEGATED — awaiting report

## What Was Delegated
[End goal from Step 3]

## Briefing File
{target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}.md

## Callback Required
Mark this task DONE only after {target-pd-name} sends completion message.

## Revision History
(none yet)
```

## Step 4.5 — Check Showcase Mode

Showcase is **off by default**. Do NOT probe `~/.claude/state/pd-showcase.flag`
on every spawn — only check it when explicitly activated.

**Determine showcase_on:**
- If the operator passed `--showcase` as an argument to the current `/pd-spawn` call → `showcase_on = true`.
- If `/pd-showcase on` was explicitly invoked in this session → check `~/.claude/state/pd-showcase.flag` as confirmation.
- Otherwise → `showcase_on = false`. Do NOT read the flag file.

**If showcase_on = false (default):** standard background spawn, no narration injection.
**If showcase_on = true:** spawn in foreground and inject the Showcase Narration Directive into the briefing.

Record this as `showcase_on = true | false` for use in Step 5.

## Step 5 — Spawn the Target PD

Use the Agent tool to spawn the target PD.

**Caller-type substitution rules (apply BEFORE rendering the prompt):**
- `{caller-name}` = `{caller-pd-name}` if `caller_type = pd`, else `parent-ai (operator direct)`
- `{caller-completion-path}` = `{caller-project}/memory/tasks/ongoing/delegated-{task-id}.md` if `caller_type = pd`, else `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md`
- The "Do NOT read/write {caller-project}" block applies only when `caller_type = pd`. For `caller_type = parent_ai`, there is no external-write exception needed — `{caller-completion-path}` already lives inside `{target-project-root}/`.

```
prompt: |
  You are {target-pd-name}, resuming work as Project Director for {target-slug}.
  You have been spawned by {caller-name} to complete an inter-spawn task.

  YOUR IDENTITY FILE (read first):
  {target-memory-path}/{target-slug}-pd.md

  YOUR BRIEFING (read second — this is your task):
  {target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}.md

  PROTOCOL — read and follow:

  1. Read your identity file: {target-memory-path}/{target-slug}-pd.md
  2. Read the briefing: {target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}.md
     (confirm it exists, update status to IN_PROGRESS)
  3. Do the work in {target-project-root}/ only
  4. When done: append completion record to {caller-completion-path} (format in Step 5b)
  5. Move briefing from inter-spawn-tasks/incoming/ to inter-spawn-tasks/completed/
  6. Run /save-state [{target-slug}]
  7. Stop.

  Do NOT use SendMessage to notify the caller — background headless agents
  do not have active sessions and cannot receive direct messages. The message
  would land in the parent session instead of the caller's context, and
  neither would act on it. Always use the filesystem completion protocol below.

  {IF caller_type = pd:}
  Do NOT read any files in {caller-project}/.
  Do NOT write any files to {caller-project}/.

  {IF caller_type = parent_ai:}
  Do NOT read or write any files outside {target-project-root}/.
  (No exception needed — the completion record at {caller-completion-path} is
  already inside {target-project-root}/memory/tasks/ongoing/.)

  Start now. Read your identity file first.

{IF showcase_on, append:}

  --- SHOWCASE MODE ---
  A live audience is watching this session. Optimize for comprehension over speed:

  1. Before each tool call, write ONE short sentence explaining what you're
     about to do and why.
  2. After each tool result, write ONE short sentence summarizing what you
     learned before choosing the next step.
  3. When deciding between approaches, narrate the trade-off out loud
     ("I could either X or Y — going with X because...").
  4. When you finish a phase (research, planning, implementation, verification),
     call it out explicitly so the audience knows where you are.

  Keep narration tight — one sentence each, no lectures. The audience reads
  your tool calls; you just connect the dots.
  --- END SHOWCASE MODE ---
```

Spawn config:
- `subagent_type`: general-purpose
- `model`: opus
- `run_in_background`: `false` if `showcase_on`, else `true`
- `team_name`: {target-slug}

## Step 5b — Filesystem Completion Protocol (MANDATORY)

When the spawned PD completes, it writes a completion record directly to the
caller's filesystem — NOT via SendMessage. Background headless agents cannot
receive direct messages; the caller's session is already closed by the time
completion happens.

**The spawned PD (target) writes the completion record to one of two paths
based on `caller_type` (set in Step 3.5):**

**IF `caller_type = pd`:** append to `{caller-project}/memory/tasks/ongoing/delegated-{task-id}.md`:

```markdown
## Completion — {ISO timestamp} UTC
**Status:** DONE — [1-sentence summary of what was delivered]
```

**IF `caller_type = parent_ai`:** append to `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md` (inside the target project — see Step 3.5):

```markdown
## Completion — {ISO timestamp} UTC
**Status:** DONE — [1-sentence summary of what was delivered]
**Output:** [path to deliverable, e.g. plans/2026-06-04-foo.html]
```

The `**Output:**` line is REQUIRED for parent-ai callers — the operator uses it to find the deliverable without re-reading the spawn briefing. The operator (or parent-ai on a later session) learns of completion via `/pd-resume [{target-slug}]`, which surfaces the target project's own `memory/tasks/ongoing/` — NOT via the global inbox.

Then in BOTH cases, append the same Completion block to the briefing file:
`{target-memory-path}/inter-spawn-tasks/completed/inter-spawn-{task-id}.md`

**This is the ONLY way the caller learns the task is done.** The caller (PD or parent-ai)
must read the delegation file (in the caller's own project for `pd`, in the target
project for `parent_ai` — never the global inbox) to know when the task completed —
it cannot wait for a SendMessage that will never arrive.

## Inter-Spawn Notify Protocol

**File-only. SendMessage is forbidden for inter-spawn completion notification.**

Background headless PDs do not have active sessions. Any SendMessage from a spawned
PD to its caller PD will land in the parent session (the operator's main window) or be
lost — the caller's session is already closed. Only filesystem writes survive the
session boundary.

Full protocol, flow diagram, and smoke test:
`~/.claude/runbooks/inter-spawn-notify-protocol.md`

This rule applies to all PD identity files. If a Spawner Protocol section in any
`agents/specialized/*-pd.md` says "SendMessage to caller" for inter-spawn
completion, that instruction is wrong and must be replaced with the filesystem
protocol above.

## Step 6 — Confirm

Output:
```
PD SPAWN: {task-id}
  Caller: {caller-pd-name}
  Spawned: {target-pd-name}
  Project: {target-slug}
  Briefing: {target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}.md
  Delegation task: {caller-project}/memory/tasks/ongoing/delegated-{task-id}.md   [caller_type=pd]
                or {target-memory-path}/tasks/ongoing/delegated-{task-id}.md      [caller_type=parent_ai]

Spawned PD running. Completion record written to `delegated-{task-id}.md` on finish — caller learns via /pd-resume [{caller-slug}] (pd), or /pd-resume [{target-slug}] (parent-ai — the record lives in the target project it's about).
```

## Handling the Completion — Filesystem Protocol

The caller does NOT wait for a SendMessage (it will never arrive).
Instead it polls the delegation file written in Step 4 — location depends on `caller_type`:
- `caller_type = pd` → caller PD polls its own `{caller-project}/memory/tasks/ongoing/delegated-{task-id}.md`
- `caller_type = parent_ai` → there is no caller project to poll. The record lives in `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md`, which surfaces automatically the next time anyone runs `/pd-resume [{target-slug}]` (Startup Priority reads `memory/tasks/ongoing/` for every PD) — the operator never needs to check the global inbox for this.

**Trigger:** When `/pd-resume [{slug}]` is run and a delegation task
is found with a "Completion" section, the PD:
1. Reads the completion record from `delegated-{task-id}.md`
2. Moves `memory/tasks/ongoing/delegated-{task-id}.md` → `memory/tasks/completed/`
3. Logs the completion to the operator: "✅ {task-id} complete — [summary from completion record]"
4. Runs /save-state [{slug}]

**How completion is discovered between sessions:**
`/pd-resume [{slug}]` reads `memory/tasks/ongoing/delegated-*.md` files for that project.
Any with a "Completion" section are marked done, others remain "DELEGATED — awaiting report."

## Handling Failure / Blocker — Filesystem Protocol

If the spawned PD encounters a blocker, it writes to the caller's delegation task —
same location rule as Step 5b: `{caller-project}/memory/tasks/ongoing/delegated-{task-id}.md`
for `caller_type = pd`, or `{target-memory-path}/tasks/ongoing/delegated-{task-id}.md`
for `caller_type = parent_ai`.

Append:
```markdown
## Blocker — {ISO timestamp} UTC
**Reason:** [what is blocking progress]
**Suggested path forward:** [workaround or escalation]
```

Caller reads this on next `/pd-resume`. Do NOT use SendMessage for blockers either.

## Revision Protocol — "Not Satisfied, Adjust and Continue"

When the operator or the caller PD is unsatisfied with the result:

**Trigger:** "revision needed on {task-id}" or "website-pitch PD, revise the landing page"

**Step 1 — The requesting PD (caller):**
1. Move `{caller}/memory/tasks/completed/delegated-{task-id}.md` → `memory/tasks/revisions/delegated-{task-id}.md`
2. Append revision note to the revision copy:

```markdown
## Revision — {YYYY-MM-DD HH:MM UTC}
**Requested by:** {caller-pd-name or "the operator"}
**Reason:** [what is wrong or needs changing]
**Instructions:** [specific adjustments required]
```

3. Create new briefing `{target-memory-path}/inter-spawn-tasks/incoming/inter-spawn-{task-id}-r{n}.md`:

```markdown
# Inter-Spawn Task — {task-id}-r{n}

**Revision of:** {task-id}
**Created by:** {caller-pd-name}
**Status:** INCOMING — REVISION {n}

## Prior Work
Task {task-id} delivered: [1-sentence summary of what was done]
Prior task file: {target-memory-path}/inter-spawn-tasks/completed/inter-spawn-{task-id}.md

## Revision Request
**What to change:** [specific changes required]
**What to keep:** [aspects to preserve]

## Available Context
- Prior task: {target-memory-path}/inter-spawn-tasks/completed/inter-spawn-{task-id}.md
- Delegation: {caller-project}/memory/tasks/revisions/delegated-{task-id}.md
- Branding: [same paths as original]
```

4. Create new delegation task: `memory/tasks/ongoing/delegated-{task-id}-r{n}.md`
5. Spawn the same PD with the revision briefing

**The spawned PD on revision:**
1. Reads its identity + revision briefing
2. Reads prior task: `{target-memory-path}/inter-spawn-tasks/completed/inter-spawn-{task-id}.md`
3. Applies only the requested adjustments — does NOT discard prior work
4. Writes completion record to caller's `delegated-{task-id}-r{n}.md` (same as Step 5b above)
5. Moves briefing to inter-spawn-tasks/completed/
6. /save-state → stops

**Revision counter:** r1, r2, r3... originating task ID preserved for traceability.

**Escalation:** If a revision is rejected twice, caller PD escalates to the operator: "⚠️ {task-id} rejected twice — needs your call."
