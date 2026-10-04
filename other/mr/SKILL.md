---
name: mr
description: Generate MR description, publish the spec to docs/specs/ and the central spec registry when a .specwork artifact exists, and create or update GitLab MR
argument-hint: "[--skip-validation]"
allowed-tools: Read, Write, Bash(find .specwork:*), Bash(cat .specwork/_spec/*), Bash(cat .specwork/_review/*), Bash(cat ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh), Bash(git rev-parse:*), Bash(git log:*), Bash(git diff:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git fetch:*), Bash(git rebase:*), Bash(mkdir:*), Bash(mv:*), Bash(cp:*), Bash(readlink:*), Bash(test:*), Bash(sed:*), Bash(glab:*), Bash(curl:*), Bash(grep:*), Bash(command -v:*), Bash(python3:*), Bash(./gradlew:*), Bash(bash ${CLAUDE_PLUGIN_ROOT}/lib/spec-publish.sh:*)
---

# MR Description

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/mr/SKILL.md`

---

## Description

Create a concise MR title and description from branch commits and available spec,
then push and provide manual or automatic GitLab creation flow.

If `.specwork` artifacts are missing, generate from git history only.

---

## Use Cases

- `/sdd:mr` — auto-detect from current branch
- `/sdd:mr PROJ-15535` — explicit ticket ID

---

## Flow

1. Detect branch and ticket; resolve this branch's pipeline slug (see [Resolve the pipeline for this branch](#resolve-the-pipeline-for-this-branch-do-this-first))
2. Target branch: `development` (default); override by passing `--target <branch>` as an argument
3. Load spec if present (`.specwork/_spec/${SLUG}-spec.md`)
4. Publish spec in-repo to `docs/specs/` (see [Publish Spec In-Repo](#publish-spec-in-repo-docsspecs)) — commits it into the feature branch so it lands in the MR diff; skipped silently when no `.specwork` spec exists
5. Read commit history vs `origin/<target_branch>`
6. Run branch sync check (behind count)
7. Generate MR title (see [MR Title Generation](#mr-title-generation)) and compact description
8. Pre-push validation — run `bash commands/check.sh` (see Pre-Push Validation)
9. Push branch (`git push -u origin HEAD`)
10. Create MR via `glab` if available, otherwise print manual GitLab URL + copy/paste text
11. Publish spec to the central registry (see [Publish Spec to Registry](#publish-spec-to-registry)) — skipped silently when no `.specwork` spec exists
12. Architectural decision hint (see [ADR Hint](#adr-hint))

---

## Resolve the pipeline for this branch (do this first)

Every `<slug>`-keyed path below — `docs/specs/`, the validation stamp, the registry
publish, the ADR hint — means **this branch's** pipeline. Resolve it once, here:

```bash
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
STATUS="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-branch-status "$BRANCH")"
```

`STATUS` is one JSON object: `has_any_pipeline`, `owns_pipeline`, `slug`,
`recorded_branch`, `recorded_base_branch`, `is_base_branch`.

- **`owns_pipeline` is `true`** → pipeline mode. `SLUG` is `slug`; substitute it for
  `<slug>` in every block below.
- **`has_any_pipeline` is `false`** (or `is_base_branch` is `true`) → standalone mode,
  `SLUG` empty. Steps 3, 4, 11 and the validation stamp are skipped silently; the MR
  is built from commits alone. A supported flow, not an error.
- **`has_any_pipeline` is `true` but `owns_pipeline` is `false`** → a *different*
  branch's pipeline is on disk. **Warn, then continue in standalone mode** (`SLUG`
  empty). Never publish that pipeline's artifacts into this MR:

  ```
  ⚠ .specwork/ belongs to '<recorded_branch>' (slug '<slug>'), not '<BRANCH>'.
    It's gitignored, so it didn't move when you switched branches.

    Opening this MR from commits only. Not publishing '<slug>'s spec: it would be
    committed into this branch, shipped in this MR's diff, and stored in the
    cross-service spec registry under this service's key.

    To clean this up:
      • /sdd:pause  — stash '<slug>' to resume it later (its MR is still open)
      • /sdd:close  — clear it (its MR merged, or the work was abandoned)
  ```

  Print it before the pre-push validation, while the MR can still be aborted.

Never take a `<slug>` from a state file that does not record `$BRANCH`. `.specwork/`
is gitignored and survives `git checkout`, so it commonly still holds a *different*
feature's pipeline. Adopting it here would commit that feature's spec into this
branch and ship it inside this MR's diff, publish it to the registry under this
service's key, and stamp this branch's HEAD onto the other pipeline's validation
marker (which then blocks that branch's own push with a sha that never matches).

Title format: `[<TICKET>] <type>: <short summary>` for ticket-bearing branches, or `<type>: <short summary>` otherwise. `<type>` (`feat`, `fix`, `chore`, …) comes from the dominant commit type and is never part of the JIRA summary. Decide `<type>` and `<short summary>` (judgment), then format with code (ticket extraction + bracketing handled there):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/titles.py mr-title "$(git rev-parse --abbrev-ref HEAD)" "<type>" "<short summary>"
```

The source of `<short summary>` depends on whether SDD pipeline state exists for the current branch.

### Step 1 — Detect mode

Reuse the `$SLUG` resolved in [Resolve the pipeline for this
branch](#resolve-the-pipeline-for-this-branch-do-this-first) — it already applies
the branch-match rule this step needs:

```bash
STATE_FILE=""
[ -n "$SLUG" ] && STATE_FILE=".specwork/_state/${SLUG}-state.json"
```

If `$STATE_FILE` is non-empty → **pipeline mode** (Step 2A). Otherwise → **standalone mode** (Step 2B).

### Step 2A — Pipeline mode

`/sdd:start` already populated `source_title` from JIRA (or from manual capture when the fetch failed). Read it directly from local state — **do not call JIRA** from inside the pipeline.

```bash
SUMMARY="$(python3 -c '
import json, sys
print((json.load(open(sys.argv[1])).get("source_title") or "").strip())
' "$STATE_FILE")"
```

- If `SUMMARY` is non-empty: use it verbatim as `<short summary>`.
- If empty: fall back to commit synthesis (Step 3). Repairing a missing `source_title` belongs upstream in `/sdd:start`, not here.

### Step 2B — Standalone mode

`/sdd:mr` runs independently of the pipeline. When the branch carries a ticket key, fetch the title directly from JIRA:

```bash
source ${CLAUDE_PLUGIN_ROOT}/lib/jira.sh

SUMMARY=""
if jira_is_ticket_key "$TICKET" && jira_is_configured; then
  SUMMARY="$(jira_fetch_summary "$TICKET" 2>/dev/null)" || SUMMARY=""
fi
```

`jira_fetch_summary` strips leading `[TAG]` prefixes and returns non-zero on any failure (not configured, fetch error, invalid key, empty summary).

- If `SUMMARY` is non-empty: use it verbatim.
- If empty: fall back to commit synthesis (Step 3).

### Step 3 — Fallback (both modes)

When `SUMMARY` is empty, synthesize `<short summary>` from commits since `origin/<target_branch>` plus the spec (original behavior). When the JIRA summary is available, use it verbatim — never paraphrase or "improve" it.

---

## Publish Spec In-Repo (docs/specs/)

Before validation and push, archive the feature spec into the project repo at
`docs/specs/<slug>-spec.md` so it is preserved as permanent, versioned
documentation and rides along in the MR diff. This is separate from — and in
addition to — the central registry publish in [Publish Spec to
Registry](#publish-spec-to-registry): `docs/specs/` is per-project and
committed; the registry is cross-service and lives outside the repo.

```bash
SPEC_FILE=""
[ -n "$SLUG" ] && SPEC_FILE=".specwork/_spec/${SLUG}-spec.md"
if [ -n "$SPEC_FILE" ] && [ -f "$SPEC_FILE" ]; then
  mkdir -p docs/specs
  DEST="docs/specs/$(basename "$SPEC_FILE")"
  cp "$SPEC_FILE" "$DEST"
  git add "$DEST"
  if ! git diff --cached --quiet -- "$DEST"; then
    SUBJECT="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/titles.py commit-subject "$(git rev-parse --abbrev-ref HEAD)" "docs" "publish spec to docs/specs/")"
    git commit -m "$SUBJECT"
  fi
fi
```

- **Standalone-safe**: when `$SLUG` is empty (no pipeline for this branch) or the
  spec file does not exist (vibe-coding flow), skip silently.
- **Idempotent**: only commits when the copy actually changed content —
  re-running `/sdd:mr` to update an existing MR does not create empty commits.
- This runs *before* Pre-Push Validation and Push, so the commit is included
  in `check.sh` and in the branch that gets pushed/MR'd.

---

## Branch Sync Check

```bash
git fetch origin "$TARGET_BRANCH" --quiet
BEHIND=$(git rev-list --count HEAD..origin/"$TARGET_BRANCH")
```

- `BEHIND=0`: continue
- `BEHIND>0`: offer `rebase / skip / cancel`

If rebase is selected:
- run `git rebase origin/"$TARGET_BRANCH"`
- if rebase conflicts, stop and ask user to resolve
- if rebase succeeds **and produced a non-empty diff**, run `bash commands/check.sh` (the same validation gate Pre-Push uses); if tests fail, stop. Do not offer scoped or fast subsets — the goal is to catch breakage introduced by what the rebase brought in (dep bumps, removed helpers, renamed fixtures), not to re-validate the feature.
- if `commands/check.sh` is missing, warn the user and require explicit confirmation before continuing.

---

## Pre-Push Validation

Before pushing, run the project's standard test command:

```bash
bash commands/check.sh
```

This script is project-provided — see SDD README §"Project validation script"
for what it should contain. A template ships at
`${CLAUDE_PLUGIN_ROOT}/templates/check.sh.example`.

- If `commands/check.sh` is missing, warn the user and ask for confirmation before pushing. Point them at the template so the next run is deterministic.
- After a non-empty rebase (`BEHIND>0` and the rebase produced a diff), this validation is required — do not offer scoped/fast subsets. The goal is to validate what the rebase brought in, not the feature itself.
- **Optional**: allow `--skip-validation` flag to bypass this step (for emergencies only)

On a **green** `check.sh` (exit 0), stamp the validated HEAD before pushing:

```bash
[ -n "$SLUG" ] && python3 ${CLAUDE_PLUGIN_ROOT}/lib/validation.py record "$SLUG"
```

Guarded on `$SLUG`: with no pipeline for this branch there is nothing to stamp, and
stamping another branch's marker would write this HEAD into *its* validation file —
blocking that branch's next push against a sha it never produced.

This writes `.specwork/_state/<slug>-validated.json` (HEAD sha + timestamp). The
`PreToolUse(git push)` quality-gate hook reads it and lets the push through only
when `HEAD` matches — so the push that follows here passes silently, while a raw
`git push` on an unvalidated HEAD is blocked. The hook is cheap (it never re-runs
`check.sh`), so it adds no latency to this flow. Skip the stamp when validation
was skipped via `--skip-validation` (the push will then be gated, by design).

---

## Publish Spec to Registry

After the MR is created, *additionally* archive the feature spec to the central
spec registry (a second, cross-service copy — this does not replace the
in-repo `docs/specs/` commit made earlier in the flow) so it is preserved by
service alongside catalogs and ADRs. The registry root is
`$CLAUDE_DOC_HOME` (defaults to `~/.claude`); the spec lands in
`$CLAUDE_DOC_HOME/spec-registry/<service>/<slug>-spec.md`, where `<service>` is
derived the same way `/sdd:doc-catalog` and `/sdd:doc-adr` derive it (so the
`spec-registry/<service>/` key matches `adr-registry/<service>/`).

```bash
[ -n "$SLUG" ] && bash ${CLAUDE_PLUGIN_ROOT}/lib/spec-publish.sh ".specwork/_spec/${SLUG}-spec.md"
```

- **Standalone-safe**: `/sdd:mr` also runs with no pipeline. With an empty `$SLUG`
  (or when `.specwork/_spec/${SLUG}-spec.md` does not exist) nothing is published —
  the script exits 0 without writing and `/sdd:mr` continues. Never block or fail on
  a missing spec, and never substitute another branch's spec to have something to
  publish: the registry is cross-service and long-lived, so a wrong entry there
  outlives the mistake and later surfaces as fact in `/sdd:ask` answers.
- It is a plain `cp` into the local-or-shared registry; it does **not** commit
  anything to the project repo.

---

## ADR Hint

After the MR is created (or the manual URL is printed), check whether the spec had any Open Questions resolved during the pipeline. Resolved OQs are the most common form of architectural decision worth preserving as an ADR.

```bash
SPEC_FILE=""
[ -n "$SLUG" ] && SPEC_FILE=".specwork/_spec/${SLUG}-spec.md"
if [ -n "$SPEC_FILE" ] && [ -f "$SPEC_FILE" ] && grep -qE '^- \[x\]' "$SPEC_FILE"; then
  echo ""
  echo "Tip: this spec had Open Questions resolved during planning."
  echo "Consider running /sdd:doc-adr open-questions to capture those decisions"
  echo "as ADRs in docs/adr/ before the MR is merged."
fi
```

- Print the hint only when at least one `- [x]` line exists in the spec.
- Do not run `/sdd:doc-adr` automatically — the user decides whether the resolutions warrant an ADR.
- Skip silently when the spec file is missing (vibe-coding flow with no `.specwork/`).

This is the only architectural-decision integration point in the pipeline. `/sdd:start`, `/sdd:plan`, and `/sdd:implement` intentionally do not nag about ADRs — by the time `/sdd:mr` runs, all resolved OQs are final, which is the right moment to retrospect.

---

## Output Format

Keep output short:

```text
Title: [PROJ-1234] feat: <short summary>

Summary:
- what changed
- why
- key risks or notes

Testing:
- <short list>
```

Avoid long narrative descriptions unless explicitly requested.

---

## Rules

- Prefer spec + commits as sources of truth
- Do not block on missing `.specwork` artifacts
- Never force-push automatically
- If push fails, surface the error and stop
- If no `glab`, always provide a pre-filled manual MR URL

---

## Requirements

- Run from the branch recorded in the active pipeline state, or from the current working branch when no `.specwork` state exists
- At least one commit must exist on branch

---

## Related Skills

- `commit` — finalize commits before MR
- `mr-address` — handle review comments after MR opens
- `close` — clean `.specwork/` after merge
