---
name: ato-mission
version: 1.0.0
description: |
  Before any multi-step work with a stated goal — a feature, a bugfix
  spanning multiple files, a QA sweep, a doc draft + iterations, a
  multi-day investigation — create an ATO Mission instead of doing it
  via bare `ato dispatch` calls. A Mission persists the goal + the
  verifiable success criteria, lets the coordinator tick drive the work
  across days, captures every event in a structured audit trail
  (SQLite + markdown narrative), and integrates parallel agents' work
  via merge strategies. Complement to `ato-warroom` (the cross-family
  decision before you start) and `ato-review` (the post-code-diff
  review). Missions is where multi-step work LIVES; war-rooms are where
  decisions ABOUT it get made; reviews are where the resulting commits
  get vetted.

  Fires when: the work has more than one decision point, a verifiable
  end state, or runs across more than one session. Use it for any
  ATO development that doesn't fit in a single dispatch.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Skill
---

## What this skill is

The Missions skill teaches the **goal-driven coordinator** pattern
shipped in ATO v2.16. The pattern: human writes a goal + programmatic
success criteria, ATO coordinates LLMs as a writing+reviewing team
(each in its own git worktree if needed), success is verified by
running check_commands, the human reviews the merged result.

Three things make a Mission different from a bare dispatch:

1. **Persistence.** State lives in SQLite (`missions` + `mission_events`
   tables) plus a markdown sidecar at `~/.ato/missions/<slug>.md`. You
   can close your laptop and come back tomorrow — the coordinator tick
   picks up where it left off.
2. **Verifiability.** Each `success_criterion` has a programmatic
   `check_command` (any shell expression — runs via `sh -c` in the
   workspace_root, exit-0 = met). The mission can't be marked complete
   without all criteria passing.
3. **Multi-agent orchestration.** With `workspace_strategy=per_agent_worktree`,
   each LLM worker gets its own git worktree on its own branch from a
   recorded base SHA. Merge strategies (`human_approves_each`,
   `coordinator_merges_all`, future picks_winner/ranked) integrate the
   parallel work. The coordinator runs check_commands after every
   accepted merge and rolls back regressors via `git reset --hard HEAD~1`.

## When to use it

Use a Mission when ANY of:

- The work has a clear end state you can write as `test -f X && ...`
- You'll need to delegate parts to peer LLMs (codex, gemini) and merge their work
- The work spans days, sessions, or interruptions
- You want the audit trail later — what was tried, what worked, what got rolled back

Use a war-room (`ato-warroom`) when:

- A single design decision needs cross-family second opinions
- You're choosing between A and B before any code gets written

Use a bare `ato dispatch` when:

- One-shot question with a single answer (no iteration, no goal state)
- The receipt is the deliverable (e.g. a summary, a translation)

## Minimal lifecycle (single_cwd)

```bash
# 1. Create the mission with a verifiable criterion.
cat > /tmp/crit.json <<'EOF'
[{"description": "tests pass", "check_command": "cargo test --quiet"}]
EOF

ato missions create \
  --name "Fix the keychain race" \
  --goal "Resolve task #31 — cross-process master_key_v2 ACL mismatch." \
  --success-criteria /tmp/crit.json

# 2. Configure the coordinator worker — which LLM, what tools.
ato missions set-worker keychain-fix \
  --runtime google \
  --require-tools read_file,grep,edit_file,write_file,bash

# 3. (Optional) install a scheduled tick. Until you do, run it by hand:
ato missions tick keychain-fix      # one action per wake
ato missions tick keychain-fix      # next action
# ...the tick fires the worker, checks success_criteria, escalates if needed
```

## Multi-agent lifecycle (per_agent_worktree)

When you need codex AND gemini AND maybe minimax to work on the same
goal in parallel:

```bash
BASE=$(git rev-parse HEAD)

ato missions create \
  --name "Refactor the dispatch path" \
  --goal "Split api_dispatch.rs into per-provider modules" \
  --success-criteria /tmp/refactor_crit.json \
  --workspace-strategy per_agent_worktree \
  --base-sha "$BASE" \
  --merge-strategy human_approves_each

# Each agent gets its own ato/mission/<slug>/<agent_key> branch and worktree.
# Drive them however you like — `ato missions dispatch <slug> --runtime codex --agent codex-refactorer ...`
# Or let the coordinator tick do it once worker_config supports multi-runtime fan-out.

# Review and integrate:
ato missions merge refactor-the-dispatch-path --status     # see pending agents
ato missions merge refactor-the-dispatch-path --approve codex-refactorer
ato missions merge refactor-the-dispatch-path --approve gemini-refactorer
ato missions merge refactor-the-dispatch-path --finish     # success_criteria re-run
```

## Reading the audit trail

Every Mission writes to two places:

```bash
ato missions events keychain-fix --human    # structured event log
ato missions narrative keychain-fix --human # cat-friendly markdown
ato missions briefs keychain-fix            # pending decision briefs
```

The narrative file at `~/.ato/missions/<slug>.md` auto-populates as
events land (PR-8). Open it in any markdown viewer to see the
play-by-play without booting the desktop.

## When the coordinator escalates

If the worker fails 3 times in a row, or the success criteria are unmet
at `--finish`, or base_sha goes missing — the tick writes an `escalated`
event with a structured decision brief (PR-6): `reason`, `summary`,
exact `options` to choose from. Surface it with:

```bash
ato missions briefs <slug>          # pending only
ato missions briefs <slug> --all    # full history
```

The brief tells you exactly what choices you have. Pick one, act on it
(usually `set-state` or `set-category` plus the recommended fix), and
the next tick continues from there.

## The pattern at the team level

When the work involves Claude (you, coordinating) + codex + gemini:

1. Convene an `ato-warroom` on the design first — cross-family verdict
   locks the approach.
2. Create the Mission with the war-room's verdict embedded in the goal.
3. Each LLM peer fires its work via the PR-1.5 tool surface
   (`--require-tools edit_file,write_file,bash`). They DON'T just
   describe — they actually edit code.
4. Reviews happen as additional dispatches into the SAME war-room
   (`--war-room-id`, incremented `--war-room-round`).
5. Merge via the strategies above. Mission completes when criteria pass.

The whole loop is itself the dogfood of v2.16. If we're not using
Missions for our own non-trivial work, the feature isn't real.
