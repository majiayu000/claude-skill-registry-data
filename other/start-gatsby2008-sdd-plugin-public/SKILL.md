---
name: start
description: Initialize SDD pipeline on current branch or create a working branch. Flexible branch handling. Fetches Jira, sets up .specwork state and source. Does not write the spec — run /sdd:spec next to draft it.
argument-hint: "<TICKET-NNNNN|description>"
allowed-tools: Write, Bash(git switch:*), Bash(git branch:*), Bash(git fetch:*), Bash(git pull:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git symbolic-ref:*), Bash(mkdir:*), Bash(grep:*), Bash(find .specwork:*), Bash(rm -rf .specwork:*), Bash(cat .specwork/_spec/*), Bash(cat ${CLAUDE_PLUGIN_ROOT}/AGENTS.md), Bash(cat .claude/service-rules.md), Bash(cat ${CLAUDE_PLUGIN_ROOT}/templates/service-rules.md), Bash(cat ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh), Bash(cat .claude/settings.local.json), Bash(cat .claude/settings.json), Bash(curl:*), Bash(test:*), Bash(python3:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/start.py:*), Bash(printenv:*)
---

# Start

Initialize the SDD pipeline on the current branch or create a new working branch.

```bash
/sdd:start PROJ-123
/sdd:start "fix duplicate leads when applicationId is null"
```

Runs `/init` to bootstrap the project's `CLAUDE.md` **only when none exists**, then pre-flight checks, fetches Jira through direct REST access when configured, creates or reuses the working branch, initializes `.specwork/`, captures the source, and writes the compact machine-readable state. It does **not** write the spec — drafting `spec.md` (and running triage on it) is `/sdd:spec`'s job. After `/sdd:start`, run `/sdd:spec`.

---

## Execution

| Step | Action |
|------|--------|
| 0 | Existing-pipeline check — classify whatever is in `.specwork/` (active here / merged leftovers / another branch's in-flight work) and stop with the matching guidance instead of re-initializing (see **Step 0** below) |
| 0.5 | Required-input guard — if no pipeline is active and no ticket/description was given, stop with no writes (see **Step 0.5** below) |
| 0.6 | If the project has no `CLAUDE.md` (repo root or `.claude/`), run `/init` to bootstrap it before branching; skip otherwise (see **Step 0.6** below) |
| 1 | Detect current branch; apply flexible pre-flight checks |
| 2 | Classify input: Jira ticket or free-text |
| 3 | If the input is a Jira key: fetch via direct REST (`curl` + `${CLAUDE_PLUGIN_ROOT}/lib/jira.sh`) — **hard-stop with no artifacts if Jira is unconfigured or unreachable** (see Step 3 below). Free-text input skips Jira entirely. |
| 4 | Suggest and confirm branch handling |
| 5 | Create a new feature branch or keep the current branch |
| 6 | Initialize `.specwork/` folders: `_spec/`, `_state/`, `_progress/` (working execution memory) |
| 7 | Load persistent rules from `${CLAUDE_PLUGIN_ROOT}/AGENTS.md` and `./.claude/service-rules.md` in the active project (if present) |
| 8 | Run `python3 ${CLAUDE_PLUGIN_ROOT}/lib/start.py` to generate rules.json, cache, state.json, and source.md in one call (it also gitignores `.specwork/`) |
| 9 | Tell the user to run `/sdd:spec` to draft `spec.md` from the captured source and run triage |

---

## Step 0 — Existing-Pipeline Check

Before initializing anything, check whether a pipeline is already active here:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

- **Non-zero** (no pipeline state on disk at all): proceed with the steps below.
- **Exit code 0** (something exists in `.specwork/`): do **not** re-initialize and
  do **not** wipe anything. Find out *what* exists before writing any message —
  `.specwork/` is gitignored, so it survives `git checkout` and can easily belong
  to a different branch, or to work that already shipped:

  ```bash
  CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-inventory "$CURRENT_BRANCH"
  ```

  This prints one JSON object with `pipelines`, `orphans` (pipelines this branch
  does not own) and `closable` (orphans whose work already landed — `merge_status`
  of `merged` or `branch-gone`). Never eyeball branch names to make this call;
  branch on the JSON. Exactly one of the three cases below applies.

Whichever case you land in, stop with no writes: `/sdd:start` never silently
reuses or deletes an existing `.specwork/`. Starting over is an explicit
`/sdd:close`.

### Case A — this branch owns an active pipeline

Some entry has `is_current: true`. The user is mid-pipeline and should continue,
park, or close it. Use that entry's `slug` as `<ACTIVE_SLUG>`:

```text
✗ There is an active pipeline for <ACTIVE_SLUG> (branch <CURRENT_BRANCH>).
  /sdd:start will not start new work on top of it.

  • Continue it:  run /sdd:spec (draft/refine) or /sdd:state (next step)
  • Park it:      run /sdd:pause to stash <ACTIVE_SLUG> and resume later
  • Close it:     run /sdd:close (then /sdd:start for the new work)
```

If `$ARGUMENTS` clearly points at **different** work (a ticket key that does not
equal `<ACTIVE_SLUG>`, or any free-text description), lead with that mismatch so
the user understands why nothing new was started. When `$ARGUMENTS` is empty or
matches, the same message applies.

### Case B — orphan leftovers whose work already landed

No entry is `is_current`, and `closable` is non-empty. This is the common
footgun: a feature was merged and `/sdd:close` was never run, so dead state sits
on disk and blocks unrelated new work. Do **not** offer `/sdd:spec` here — there
is nothing worth continuing. Name each closable entry with its reason:

```text
✗ /sdd:start did not start anything — .specwork/ still holds a finished pipeline.

    • <slug> (branch <branch>) — already merged into <base_branch>
    • <slug> (branch <branch>) — branch no longer exists locally

  That work already landed. Clear the leftovers, then start again:

    /sdd:close                 # re-checks MR state, then wipes .specwork/
    /sdd:start <your input>
```

Render one bullet per `closable` entry: `merge_status: "merged"` → "already merged
into `<base_branch>`"; `merge_status: "branch-gone"` → "branch no longer exists
locally". For a `branch-gone` entry, add this line — a branch rename that skipped
`/sdd:resync` is indistinguishable from a merged-and-deleted branch, and
`/sdd:close` would throw away live work:

```text
  If <branch> was renamed rather than merged, run /sdd:resync instead of /sdd:close.
```

`merge_status` is derived from git alone (is the branch an ancestor of its base?),
so it is a **warning, not proof** — `/sdd:close` still verifies the real MR state
via `glab` before deleting anything. Never run `/sdd:close` on the user's behalf
here; deleting a pipeline is their call.

### Case C — orphan leftovers still in flight

No entry is `is_current` and `closable` is empty: the pipelines on disk belong to
another branch and have **not** landed (`open`, or `unknown` when the merge state
could not be determined). Closing them would destroy unmerged work, so point at
the owning branch instead. Use the first orphan as `<slug>` / `<branch>`:

```text
✗ .specwork/ belongs to '<branch>' (slug '<slug>'), not '<CURRENT_BRANCH>'.
  /sdd:start will not start new work on top of another branch's pipeline.

  • Resume it:  switch to '<branch>' and run /sdd:state
  • Park it:    switch to '<branch>' and run /sdd:pause, then come back here
  • Renamed?    run /sdd:resync if '<branch>' is this branch under an old name
```

---

## Step 0.5 — Required Input Guard (HARD STOP)

`/sdd:start` needs a ticket key or a free-text description to start a pipeline.
With no input there is nothing to base a branch name, source, or spec on, so
**do not create a branch and do not initialize `.specwork/`**.

When **Step 0 found no active pipeline** *and* `$ARGUMENTS` is empty (after
trimming whitespace), stop immediately with no writes and tell the user:

```text
✗ Nothing to start. /sdd:start needs a ticket key or a description.

  /sdd:start PROJ-123
  /sdd:start "fix duplicate leads when applicationId is null"
```

This guard only applies when there is no active pipeline — if Step 0 already
found one, it stopped there and you never reach this point.

---

## Step 0.6 — Bootstrap `CLAUDE.md` with `/init` (only when missing)

`CLAUDE.md` is the project's agent-memory file — the model's persistent context
throughout the pipeline. Run `/init` to generate it **only when the project does
not already have one**. `/init` scans the whole project and can be slow, so skip
it whenever a `CLAUDE.md` is already present.

First detect it. Check the repo root **and** the project `.claude/` directory —
some projects keep `CLAUDE.md` under `.claude/` rather than at the root:

```bash
if test -f CLAUDE.md || test -f .claude/CLAUDE.md; then echo FOUND; else echo MISSING; fi
```

- **FOUND** — skip `/init` entirely; the model context is already in place.
- **MISSING** — run `/init` to generate `CLAUDE.md`.

When you do run it:

- Run `/init` **before** branch creation so the generated `CLAUDE.md` is carried
  onto the new feature branch.
- `/init` is idempotent and will not overwrite an existing agent-memory file.
- No pipeline artifact depends on the output of `/init` — it is purely for
  model-context bootstrapping.

---

## Branch Detection & Pre-flight Logic

Detect current branch and apply flexible pre-flight checks:

**On any starting branch:**
- Detect the current branch and use its current HEAD as the default base
- Offer a suggested working-branch name derived from the ticket or free-text input
- Allow creating a new branch from the current branch so the new branch inherits the parent branch's commits and changes
- Allow staying on the current branch when that is the better choice

**If on `development`, `develop`, `main`, or `master`:**
- Require a clean working tree before creating a new branch, checking with agent-memory files exempted:

  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/lib/worktree.py dirty-files --exclude-agent-files
  ```

- Abort only if that command prints anything: "Working tree has changes. Commit or stash first."
- **Agent-memory files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) dropped by `/init` or proactive models are legitimate, version-controllable context — not feature WIP — so they must **not** block `/sdd:start`. Creating the new branch carries them onto it, where they get committed with the rest of the work. They block only when other, real changes are also present.

**If staying on the current branch:**
- Reuse the current branch as the working branch
- Continue with slug extraction from the active branch name

**In all cases:**
- If **Step 0** found an active pipeline, you already stopped there — do not reach this point with an existing `.specwork/`.
- Never auto-delete an existing `.specwork/`. Starting over is an explicit `/sdd:close`, not a side effect of `/sdd:start`.

---

## Branch Confirmation Prompt

Always ask how to handle the working branch using a **single `AskUserQuestion` call** with two
explicit options plus the built-in "Other" field for custom names. Never issue a second follow-up
question.

Use this question format:

```
"Current branch: <current>  |  Suggested: <suggested>
Which branch should be used for this pipeline?"
```

Options to present:

| Label | Description |
|-------|-------------|
| `<suggested>` (Recommended) | Create `<suggested>` from `<current>` HEAD |
| Keep `<current>` | Stay on the current branch and initialize `.specwork/` here |

The tool automatically appends an **"Other"** free-text field — that is the custom-name path.
Do **not** add a third predefined option for custom names; rely on "Other" instead.

Handling each answer:

- **Suggested branch selected**: create the suggested branch from current HEAD, switch to it,
  then continue to artifact generation.
- **Keep current selected**: stay on the current branch and continue to artifact generation.
- **Other (custom text)**: treat the typed value as the branch name. Create that branch from
  current HEAD, switch to it, then continue to artifact generation. Validate the typed name is
  a valid git branch name before running `git checkout -b`; if invalid, surface the error and
  stop.

**Slug derivation (ALWAYS after branch is confirmed):** The slug passed to `start.py` must
be derived from the **final chosen branch name**, not from the original description or ticket.
Strip the leading type prefix (`feature/`, `bugfix/`, `hotfix/`, `release/`) and use the
remainder as the slug. Examples: `feature/test2` → `test2`;
`feature/fix-duplicate-leads` → `fix-duplicate-leads`; `feature/PROJ-123` → `PROJ-123`.
This guarantees that artifact file names always match the branch name.

Suggested names follow `feature/<TICKET>` or `feature/<slugified-description>`.
Example: on `feature/IR-40`, starting `/sdd:start IR-45` suggests `feature/IR-45` so the new
branch inherits the parent's commits.

---

## start.py Artifact Generator

After reading the rule sources, generate all boilerplate artifacts with a single call:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/start.py \
  --slug "<slug>" \
  --ticket "<TICKET>" \
  --input-type jira \
  --branch "<branch>" \
  --base-branch "<base>" \
  --scaffold-rules-template ${CLAUDE_PLUGIN_ROOT}/templates/service-rules.md \
  --rules \
    ${CLAUDE_PLUGIN_ROOT}/AGENTS.md \
    .claude/service-rules.md \
    .claude/rules \
  $([ "${SDD_NON_INTERACTIVE:-0}" = "1" ] && echo "--non-interactive")
```

**Free-text input — persist the description into `source.md`.** When the input
is free text (not a Jira key), do **not** let `source.md` fall back to a
placeholder: the description is the only material `/sdd:spec` has to draft from,
so it must survive on disk (this is what makes the context survive a `/sdd:auto`
run that later stops at the Open Questions gate). Pass the verbatim text via
`--source-body` — no temp file needed:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/start.py \
  --slug "<slug>" \
  --ticket "none" \
  --input-type freetext \
  --branch "<branch>" \
  --base-branch "<base>" \
  --source-body "<full free-text description verbatim>" \
  --scaffold-rules-template ${CLAUDE_PLUGIN_ROOT}/templates/service-rules.md \
  --rules \
    ${CLAUDE_PLUGIN_ROOT}/AGENTS.md \
    .claude/service-rules.md \
    .claude/rules \
  $([ "${SDD_NON_INTERACTIVE:-0}" = "1" ] && echo "--non-interactive")
```

The Jira path doesn't need this — `jira_write_issue_markdown` (see below) writes
the fetched issue straight into `source.md`.

The script creates: `state.json`, `rules.json`, `implementation-cache.json`,
`source.md` (the `--source-body` contents, or a placeholder when omitted),
and an **empty `spec.md` scaffold** — a placeholder only. `/sdd:start` never writes
spec *content*; `/sdd:spec` drafts the canonical spec downstream skills consume. It
prints a JSON summary with the paths to each artifact and `source_has_body` (true when
the body was captured).

It also ensures `.specwork/` is gitignored (transient pipeline state must never
be committed): it appends `.specwork/` to `.gitignore` if missing, creating the
file when absent. The check is idempotent. If `.specwork/` is already tracked
from a prior bad setup, the summary's `gitignore.tracked` is `true` and the
script prints a warning with the exact `git rm -r --cached .specwork/` fix — it
never untracks files automatically.

---

## Jira Access Without MCP

`/sdd:start` should use direct Jira REST access and must not depend on an MCP server.

Supported environment variables:

- `JIRA_BASE_URL` or `JIRA_URL`
- Jira Cloud: `JIRA_USER` + `JIRA_TOKEN`
- Jira Server/Data Center PAT: `JIRA_TOKEN` + `JIRA_AUTH_MODE=bearer`

Preferred fetch pattern:

```bash
source ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh

if jira_is_ticket_key "$TICKET" && jira_is_configured; then
  jira_write_issue_markdown "$TICKET" ".specwork/_spec/<slug>-source.md"
  # Preserve any supplementary free text typed alongside the ticket
  # (e.g. /sdd:start PROJ-123 "watch out: only the publisher, not the consumer").
  # That note is usually the highest-value, least-recoverable context — never drop it.
  if [ -n "$DESC" ]; then
    printf '\n## Additional context (from /sdd:start)\n\n%s\n' "$DESC" \
      >> ".specwork/_spec/<slug>-source.md"
  fi
fi
```

Here `$TICKET` is the leading ticket key and `$DESC` is any free text typed after
it. When the user passes a ticket plus a note, the note must end up in
`source.md` so `/sdd:spec` drafts from it.

**When the input is a Jira ticket key, Jira access is required — do NOT fall back silently.**

- **Jira not configured** (missing `JIRA_BASE_URL` / `JIRA_TOKEN`): stop immediately, do not create any `.specwork/` artifacts, and tell the user:
  ```
  ✗ Jira is not configured. Set the following environment variables and retry:

    export JIRA_BASE_URL=https://<your-domain>.atlassian.net
    export JIRA_USER=your@email.com
    export JIRA_TOKEN=<personal-access-token>

  Run /sdd:start again once Jira is configured.
  ```

- **Jira configured but the call fails** (curl error, HTTP error, bad credentials): stop immediately, do not create any `.specwork/` artifacts, and tell the user the specific error returned.

The fallback to free-text (using the ticket id as a title placeholder) is only acceptable when the input was free text to begin with — never when a Jira key was the input.

---

## Artifacts written by `/sdd:start`

`/sdd:start` writes three state artifacts plus a source placeholder. Their schemas and example post-run output are documented in `${CLAUDE_PLUGIN_ROOT}/skills/start/REFERENCE.md`:

- **State file schema** — `.specwork/_state/<slug>-state.json` structure and field semantics
- **Implementation cache file schema** — `.specwork/_state/<slug>-implementation-cache.json` shape
- **Rules file schema** — `.specwork/_state/<slug>-rules.json` shape (consumed by downstream skills instead of re-reading markdown rules)
- **Output examples** — canonical post-`/sdd:start` outputs (new branch from development, dependent branch, current branch kept)

The spec template (`templates/spec.md`) and spec-writing rules belong to `/sdd:spec`, which drafts `.specwork/_spec/<slug>-spec.md`. Read the relevant section before writing each artifact.

Project-level scaffolding (handled by `start.py`, not by this skill in prose):

- Service rules can live either as a single `./.claude/service-rules.md` (legacy) or as per-topic
  files under `./.claude/rules/*.md` (preferred — each file is one domain, auto-loaded by Claude
  Code). `start.py` reads both: `.claude/rules` is passed as a `--rules` source and expands to
  every `*.md` inside it.
- The "scaffold only when neither exists" decision is **enforced in code**: the
  `--scaffold-rules-template` flag (already wired into the invocation above) makes `start.py`
  create `./.claude/rules/service-rules.md` from the template **only** when there is no
  `./.claude/service-rules.md` and no `./.claude/rules/*.md`. Existing rules are never overwritten.
  The JSON summary reports the outcome under `rules_scaffold`.

---

## Next Step

`/sdd:start` only bootstraps state — the spec does not exist yet. The next step is
always `/sdd:spec`:

```bash
/sdd:spec        # draft spec.md from the captured source, then run triage
```

`/sdd:spec` owns the spec, the Open Questions summary, and triage classification
(it reads `## Summary` + `## Behavior`, which only exist once the spec is
drafted). After `/sdd:spec`, triage's recommended path leads into `/sdd:plan` /
`/sdd:implement`.

---

## Related Skills

- `spec` — drafts the spec from the source captured here; run it next
- `plan` — optional discovery + plan step (recommended for medium/large features)
- `implement` — consumes the spec + rules (and the plan if it exists)
- `close` — clears `.specwork/` artifacts including `_state/`
