---
name: whatnext
description: Show where you are in the feature pipeline and what to do next
allowed-tools: Bash(git branch:*), Bash(git rev-parse:*), Bash(git rev-list:*), Bash(git status:*), Bash(find .specwork:*), Bash(cat .specwork/_state/*), Bash(cat .specwork/_spec/*), Bash(cat .specwork/_progress/*), Bash(grep:*), Bash(test:*), Bash(python3:*)
---

# What Next

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/whatnext/SKILL.md`

---

## Description

Inspects the current branch and `.specwork/` artifacts to determine exactly where
the developer is in the feature pipeline, then prints a focused "what to do next"
message with a one-line explanation of why.

This skill gives guidance, not a status dump. The output is always short.

---

## States

The pipeline reports one focused state at a time:

- **setup**: no SDD state detected yet
- **ready**: spec exists, Open Questions are resolved, no implementation commits yet
- **in-progress**: working tree has active implementation changes
- **review-ready**: branch is clean and has commits ahead of the feature base branch
- **blocked**: the current branch/setup is incompatible with the next pipeline step

Use Cases:

- `/sdd:whatnext` — contextual next step for the current branch (shows state + next action)
- `/sdd:whatnext overview` — full pipeline reference card, all commands explained

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Detects current branch and checks whether `.specwork/_state/*-state.json` exists |
| 2 | Reads the active state file to get the feature slug and base branch |
| 3 | Evaluates branch compatibility, spec state, open questions, worktree state, and commits ahead of base |
| 3.5 | On a branch mismatch, classifies it with `pipeline-inventory` — merged leftovers take different advice than live work elsewhere (see **Blocked States**) |
| 4 | Prints the pipeline with checkmarks showing progress (optional steps tagged `(optional)`) |
| 5 | Prints a "Next step" block with the command and a one-line explanation |

---

## Detection Logic

Handle `/sdd:whatnext overview` first: print the static reference card and stop.

For contextual mode, evaluate in this order:

| Condition | Next step if NOT met |
|-----------|---------------------|
| `.specwork/_state/<slug>-state.json` exists | `/sdd:start <ticket-or-text>` |
| Current branch matches the `branch` value in `.specwork/_state/<slug>-state.json` | Blocked — classify the mismatch first (see **Branch mismatch** below); merged leftovers → `/sdd:close`, live work elsewhere → switch back |
| `.specwork/_spec/<slug>-spec.md` exists | `/sdd:spec` (draft the spec — `/sdd:start` bootstraps state but does not write the spec) |
| Spec `## Open Questions` has no `- [ ]` items | Resolve open questions in the spec (or `/sdd:spec` with the answers as context) |
| Pending-stage file contains real paths | `/sdd:commit` |
| No uncommitted or unstaged changes (`git status` clean) | `/sdd:implement` |
| Branch has commits ahead of its recorded `base_branch` | `/sdd:mr` |

Use the state file's `base_branch` when checking whether the branch is ahead. If it
is missing, fall back to `development`, then `main`.

**Optional steps** — not part of the core detection chain. Suggest them only when
they are clearly relevant:
- `/sdd:test-design` + `/sdd:test-impl` — if you want gap-focused test coverage designed and implemented
- `/sdd:code-review` — quality + security review before MR
- `/sdd:handoff` — when another agent or model should take over execution

If the branch is clean and ahead of base, print `/sdd:mr` as the next step. Mention
`/sdd:mr-address` only as a follow-up after review comments arrive.

### Default next-step recommendation

After `/sdd:start` finishes, the spec does not exist yet — suggest `/sdd:spec` to draft it (and run triage). Once the spec is drafted, suggest `/sdd:plan` as the default checkpoint for medium-to-large features. For small/obvious changes the developer can skip planning and run `/sdd:implement` directly — the optional steps in the pipeline checklist (`/sdd:plan`, `/sdd:test-design`, `/sdd:test-impl`, `/sdd:code-review`) are always tagged `(optional)` so the developer can decide.

```
Next step:
  /sdd:mr

  Your branch is clean and contains committed work ahead of the base branch.
  Open or update the MR next. Use /sdd:mr-address after teammates leave comments.
```

---

## Output Format

When **ready** (initialized and ready to implement):

```
Pipeline: feature/PROJ-15535  [ready]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted, all questions resolved
→  /sdd:plan          (optional, recommended for medium-to-large features)
○  /sdd:implement     implement and test inline
○  /sdd:test-design   (optional)
○  /sdd:test-impl     (optional)
○  /sdd:code-review   (optional)
○  /sdd:mr
○  /sdd:mr-address

Next step:
  /sdd:plan (or /sdd:implement directly for small/obvious changes)

  Discover target files and draft an implementation plan, then implement.
```

When **blocked** (has unresolved questions):

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — 2 unresolved Open Questions

Next step:
  Resolve open questions in `/abs/path/repo/.specwork/_spec/PROJ-15535-spec.md:42`

  Unresolved:
    - [ ] #1 Should lookup use personUuid only, or personUuid + collateral?
    - [ ] #2 If multiple existing leads match, should we update latest or fail?

  Then run /sdd:implement.
```

**Path requirements:**

1. **Absolute** — relative paths are not clickable in Claude Code's CLI, VSCode/Cursor terminals, iTerm2, or Warp. Build it with `ABS="$(cd "$(dirname "$SPEC")" && pwd)/$(basename "$SPEC")"`.
2. **Wrapped in single backticks** — forces Claude Code's renderer to color the path so it stands out from the surrounding label.

The `:42` suffix is the line number of the `## Open Questions` heading: `grep -n "^## Open Questions" "$SPEC" | head -1 | cut -d: -f1`. Apply the same pattern to the second blocked output below.

Do **not** wrap the whole blocked-state block in a fenced code block when emitting it — fenced blocks suppress inline-code coloring on the path.

Legend:
- `✓` — completed
- `→` — current / in progress
- `○` — not started (may be `(optional)`)
- `✗` — blocked (unresolved Open Questions)

### Stale leftovers footnote

When the current branch **does** own its pipeline but `pipeline-inventory`
reports a non-empty `closable`, the leftovers are not this branch's problem —
they change nothing about the next step. This skill gives guidance, not a status
dump, so do not grow a section for them: append exactly one line after the
`Next step:` block, and only when there is something to report.

```
Note: 1 merged pipeline still in .specwork/ (PROJ-15500) — /sdd:close clears it.
```

Pluralize and name up to two slugs; beyond that use a count (`3 merged pipelines
still in .specwork/`). This never becomes a `✗` line, never changes `Next step:`,
and is omitted entirely when `closable` is empty — which is the normal case. For
the full list, `/sdd:state` prints its `Stale:` block.

---

## Blocked States

### Branch mismatch — classify before advising

`.specwork/` is gitignored, so it survives `git checkout` and outlives the branch
it belongs to. When the current branch does not own the pipeline on disk, there
are two very different reasons, and they take opposite advice: work still in
flight on another branch (go back to it) versus a merged feature whose
`/sdd:close` was never run (clear it). Telling someone to "resume" a pipeline
that already shipped sends them to look for work that no longer exists.

Resolve which one it is before printing anything:

```bash
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-inventory "$CURRENT_BRANCH"
```

Branch on the JSON — never on how the branch names look. `closable` holds the
orphans whose work already landed (`merge_status` of `merged` or `branch-gone`);
`orphans` holds every pipeline this branch does not own.

### Leftovers from a merged pipeline (blocked)

No entry is `is_current` and `closable` is non-empty:

```
Pipeline: feature/newwork  [blocked]
──────────────────────────────────────
✗  /sdd:start         blocked — .specwork/ still holds a finished pipeline

Next step:
  /sdd:close

  PROJ-15500 (feature/PROJ-15500) already merged into development, but its
  .specwork/ state was never cleared — so it blocks starting anything new here.
  Clear it from its own branch, or from its base, then run /sdd:start.
```

Render the reason from `merge_status`: `merged` → "already merged into
`<base_branch>`"; `branch-gone` → "its branch no longer exists locally". For a
`branch-gone` entry, add one line — a rename that skipped `/sdd:resync` is
indistinguishable from a merged-and-deleted branch, and `/sdd:close` would throw
away live work:

```
  If feature/PROJ-15500 was renamed rather than merged, run /sdd:resync instead.
```

Say "already merged" as the *reason reported by git*, never as verified fact:
`merge_status` only asks whether the branch is an ancestor of its base.
`/sdd:close` re-checks the real MR state via `glab` before deleting anything.
Never run `/sdd:close` here — this skill is read-only.

### Not on the recorded pipeline branch (blocked)

No entry is `is_current` and `closable` is **empty** — the pipeline belongs to
another branch and has not landed (`open`, or `unknown` when git could not tell).
Closing it would destroy unmerged work, so send the user back to it. Name the
branch from the first orphan's `branch` rather than pointing at the state file:

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — current branch does not match recorded pipeline branch

Next step:
  Switch back to feature/PROJ-15535

  The active .specwork state belongs to a different branch and has not been
  merged. Resume work on that branch before continuing the pipeline.
```

---

### Unresolved Open Questions in spec (blocked)

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — 2 unresolved Open Questions

Next step:
  Resolve open questions in `/abs/path/repo/.specwork/_spec/PROJ-15535-spec.md:42`

  Unresolved:
    - [ ] #1 Should lookup use personUuid only, or personUuid + collateral?
    - [ ] #2 If multiple existing leads match, should we update latest or fail?

  Mark each resolved:
    - [x] #1 Should lookup use personUuid only, or personUuid + collateral? — resolved: personUuid + collateral
    - [x] #2 If multiple existing leads match, should we update latest or fail? — resolved: fail
  
  Then run /sdd:implement.
```

---

## Overview Mode

When called as `/sdd:whatnext overview`, print the full pipeline reference regardless of
current branch state:

```
Feature Development Pipeline
═════════════════════════════════════════════════════════════════

SETUP (once per machine)
  /plugin install sdd@gatsby    installs the whole plugin: pipeline + reviewers + doc commands

─────────────────────────────────────────────────────────────────

FEATURE PIPELINE

  /sdd:auto                Non-interactive driver: runs the early flow
                         (start → spec → plan → implement → commit → mr) end-to-end
                         without pausing at each step. Use for small/obvious features;
                         drop back to the individual commands when you need control.

  /sdd:start PROJ-1234    Initialize the pipeline, create/select the working branch,
                         and write .specwork/_state metadata plus source/rules/cache files.
                         Does NOT write the spec — run /sdd:spec next.

  /sdd:spec                Draft the spec from the captured source (first run), or
                         feed extra context into an existing spec — files,
                         jira <TICKET>, pasted text, or free text. Draft mode runs
                         triage; refine mode resolves Open Questions, expands
                         Implementation Context, appends constraints, and warns
                         when plan.md becomes stale. Refine with no args is a no-op.
                         Review the spec before continuing — especially Open Questions.
                         

  /sdd:implement           Pick the next piece to implement with inline tests.
                         Repeat: code → test → /sdd:commit until feature is done.

  /sdd:commit              Stage changes, propose a semantic commit message, confirm.
                         Run after each /sdd:implement step.

  /sdd:test-design         [optional] Design missing test cases (gap analysis).
                         Works standalone on any branch with code changes.

  /sdd:test-impl           [optional] Implement missing test files from design doc.
                         Works standalone; does not depend on pipeline.

  /sdd:code-review         [optional] Quality and security review (Java or frontend).

  /sdd:mr                  Generate MR description, optionally publish spec to docs/specs/,
                          squash commits, push branch, create/update MR in GitLab.

  /sdd:mr-address      After the MR receives review comments: work through each
                          unresolved thread — fix, reply, or defer. Resolves in GitLab.

  /sdd:close               After the MR is merged: deletes .specwork/ artifacts.
                          Preserves published specs in docs/specs/.

  /sdd:handoff             Optional. Package spec + rules + context into a handoff file
                         for another agent/model to continue execution.

─────────────────────────────────────────────────────────────────

UTILITIES

  /sdd:state              Full status: commits, spec content, open questions.
  /sdd:whatnext                This. Shows your next step contextually.
  /sdd:pause               Need to switch context? Stashes everything (including
                         .specwork/) with a pipeline label and leaves branch
                         switching to you.
  /sdd:restore              Lists paused pipeline branches and restores the one you select.
  /sdd:resync              Sync .specwork/ artifacts with current branch.
                         Two modes:
                           /sdd:resync                         (after a manual git branch -m)
                           /sdd:resync --rename-branch feature/IR-70-foo  (atomic: rename + sync)
                         Renames files, updates state.json (id, branch, ticket,
                         input_type, internal paths). Use when a free-text feature
                         gets assigned a ticket, after a typo fix, or whenever the
                         pipeline state and the current branch diverge.

─────────────────────────────────────────────────────────────────

STANDALONE TOOLS  (independent — run on any branch, any time, no pipeline required)

  /sdd:code-review         Stack-aware quality and security review of staged+unstaged
                         changes. Auto-detects Java (build.gradle / pom.xml) or
                         Frontend (package.json) and runs the matching reviewer
                         agents in parallel. Inside the SDD pipeline, persists the
                         report to .specwork/_review/; outside, runs the same flow
                         without writing to disk. Use before committing — hotfixes,
                         config changes, or mid-implementation checks.

  /sdd:mr-review           Review a PEER's MR/PR or branch — resolves the input to a
                         diff and runs the same stack-aware quality+security review,
                         read-only, without ever touching your working tree. Use when
                         reviewing someone else's work (vs /sdd:code-review for your own).

  /sdd:undo                Discard uncommitted code changes — from /sdd:implement or
                         free-hand coding — reversibly (stash by default; --restore to
                         recover, --hard to discard for good). Works on any branch and
                         preserves .specwork/ when a pipeline is active.

  --- doc/adr commands below come from the `doc` bundle (ships with the pipeline,
      installed with the sdd plugin) ---

  /sdd:doc-adr               Capture an architectural decision: technology choice,
                         pattern adoption, compliance constraint, significant trade-off.
                         Stores it straight in the ADR registry at
                         $CLAUDE_DOC_HOME/adr-registry/<service>/ (no in-repo copy).
                         Modes: free text · /sdd:doc-adr PROJ-1234 · /sdd:doc-adr open-questions · /sdd:doc-adr list

  /sdd:doc-catalog           Generate or refresh the service catalog for the current
                         microservice. Scans REST endpoints, SQS/SNS integrations,
                         Feign clients, and scheduled jobs → stores it straight in the
                         service-catalog registry at $CLAUDE_DOC_HOME/service-catalog/
                         (default ~/.claude/; no in-repo copy). /sdd:doc-catalog list shows the registry.

  /sdd:doc-catalog-query     Cross-service architecture questions answered from the
                         central registry. Example:
                           /sdd:doc-catalog-query who consumes the LeadCreated SNS event?

  /sdd:doc-adr-query         Cross-service decision-history questions answered from
                         the ADR registry. Example:
                           /sdd:doc-adr-query why did consumer-portal pick PostgreSQL?

  /sdd:doc-spec              Store a hand-written / standalone spec.md in the central
                         spec registry at $CLAUDE_DOC_HOME/spec-registry/<service>/
                         (default: ~/.claude/). The pipeline's /sdd:mr stores it
                         automatically; this is the vibe-coding counterpart. /sdd:doc-spec list shows the registry.

  /sdd:doc-spec-query        Cross-service feature/spec questions answered from the
                         spec registry. Example:
                           /sdd:doc-spec-query which specs touch LeadProcessor?

  /sdd:doc-investigation     Capture the current session's investigation into a typed
                         findings doc (bug or exploration) at
                         $CLAUDE_DOC_HOME/investigation-registry/<service>/. Auto-detects
                         the type; run it in any repo after researching code.

  /sdd:doc-investigation-query  Recall/recurrence questions over captured investigations.
                         Examples:
                           /sdd:doc-investigation-query have we seen ReportToken reuse before?
                           /sdd:doc-investigation-query how does a lead reach the cache?

  /sdd:ask                   UNIFIED query across all registries (catalog/adr/spec/
                         investigation). Grounds answers in raw/ (source of truth), and
                         when a two-layer vault has a wiki/ layer, follows its backlinks
                         for cross-cutting questions; warns if the wiki is stale.
                         Optional type: filter. Subsumes the four doc-*-query commands.
                           /sdd:ask who consumes LeadCreated and why did we design it that way?

  /sdd:doc-ingest            Compile raw/ → wiki/ in a two-layer vault: extract entities +
                         concepts, write pages with [[backlinks]], update indexes + log.
                         The producer that keeps /sdd:ask sharp (no-op without a wiki/ layer).

─────────────────────────────────────────────────────────────────

CONTEXT SWITCHING

  /sdd:pause → /sdd:restore   Need to work on another branch? /sdd:pause stashes
                         everything and leaves branch switching to you.
                         /sdd:restore shows only pipeline branches, switches back
                         to the right branch, and restores the stash.

─────────────────────────────────────────────────────────────────

ARTIFACTS  (live in .specwork/, local-only/gitignored)

  _spec/<id>-spec.md        Feature spec (optionally published to docs/specs/ on /sdd:mr)
  _plan/<id>-plan.md        Implementation plan written by /sdd:plan (deleted by /sdd:close after merge)
  _progress/<id>-context.md Optional human-authored execution context (deleted by /sdd:close after merge)
  _progress/escalations.md  Append-only log of /sdd:implement escalations (deleted by /sdd:close after merge)
  _review/<id>-*.md         Code review reports (deleted by /sdd:close after merge)
```

---

## Requirements

- Run from any branch; best results when you are on the branch recorded in `.specwork/_state/*-state.json`
- Read-only — makes no changes

---

## Related Skills

- `start` — initializes the pipeline and writes `state.json` (the spec is drafted by `/sdd:spec`)
- `spec` — drafts and refines the spec
- `state` — detailed state dump (commits, plan steps, open questions counts)
- `implement` — implements the next step
- `commit` — commits and marks step complete
- `close` — clears `.specwork/`; the fix when the blocker is a merged leftover
