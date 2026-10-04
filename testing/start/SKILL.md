---
name: start
description: Use this skill when the user runs /start, says "start", "enable the SDLC workflow", "I want to build", "I want to fix", "set up", "get started", or otherwise signals they want to activate or re-enable the SDLC workflow. Handles three distinct paths based on marker state — fresh install (opt-in activation), re-enable after suspension (reconciliation), and already-enabled (hand off to /plan). Power users who already have an active plan can skip directly to /plan.
next_suggestions:
  - when: fresh_install_complete
    suggest: "review the draft plan below, then run /plan to sign it and unlock /analyze"
  - when: reenable_complete
    suggest: "run /plan to draft and sign the superseding REQ before editing"
  - when: already_enabled
    suggest: "run /plan to start a new task"
---

# Start — Opt-in Activation, Re-enable, and Task Intake

Read the marker state first. The path taken depends entirely on which marker files exist.

## Marker state dispatch

| State | Condition | Path |
|---|---|---|
| Fresh install | `.claude/sdlc/.enabled` absent AND `.claude/sdlc/.suspended` absent | Activate → Steps 0–4 |
| Suspended | `.claude/sdlc/.suspended` present | Re-enable → Steps R1–R5 |
| Already enabled | `.claude/sdlc/.enabled` present | Hand off to `/plan` |

Check `.claude/sdlc/.suspended` first. If present, go to the re-enable path even if `.enabled` also somehow exists — `.suspended` wins.

---

## PATH A — Fresh Install (Steps 0–4)

### Step 0 — Config check and auto-detection

Skip this step entirely if `config/tools.json` already exists.

Run the following detections silently — no prompts, just observe:

| Signal | Detected value |
|---|---|
| `.git` directory | `vcs: "git"` |
| `git remote get-url origin` | repo slug (`owner/repo`) |
| `.github/workflows` present | `ci: "github-actions"` |
| `.gitlab-ci.yml` present | `ci: "gitlab-ci"` |
| `.circleci/config.yml` present | `ci: "circleci"` |
| `Jenkinsfile` present | `ci: "jenkins"` |
| `package.json` present | `language: "node"` |
| `pyproject.toml` or `requirements.txt` | `language: "python"` |
| `go.mod` present | `language: "go"` |
| `Cargo.toml` present | `language: "rust"` |
| `pom.xml` or `build.gradle` | `language: "java"` |
| `jest` or `vitest` in devDependencies | `test.command` |
| `pytest` in pyproject.toml | `test.command` |
| `eslint` in devDependencies | `lint.command` |
| `ruff` in pyproject.toml | `lint.command` |
| Remote URL contains `github.com` | `tracker: "github"` |
| Remote URL contains `gitlab` | `tracker: "gitlab"` |
| Remote URL contains `bitbucket` | `tracker: "bitbucket"` |

Show detected values as facts, not questions. Then ask up to three prompts:

**Prompt 1 — Tracker confirm (always shown, pre-selected if detected):**
```
Issue tracker (inferred: GitHub Issues) — correct? [Y/n/override]
```
If remote is absent or ambiguous:
```
Which issue tracker does this project use?
A) GitHub Issues  B) GitLab  C) Jira  D) Linear  E) None
(detected: none) _
```

**Prompt 2 — Auth token (only if tracker ≠ None):**
```
Paste your <tracker> token (stored in config/tools.local.json, never committed).
Skip with Enter to omit: _
```

**Prompt 3 — Project slug (only if tracker detected but slug not parseable from remote):**
```
Project key or repo slug: _
```

Best case (GitHub/GitLab remote present): 1 prompt (token only).
Typical case (no remote): 3 prompts maximum.
Multi-team sign-off configuration: not surfaced here — deferred to `/configure`.

After prompts, show a diff of the proposed `config/tools.json` and `config/tools.local.json`. Write only on explicit confirmation. If the user declines, proceed to Step 1 without writing config — they can run `/configure` later.

### Step 1 — Create `.enabled` marker

```bash
mkdir -p .claude/sdlc
touch .claude/sdlc/.enabled
```

Hooks are now armed. This runs immediately after config is confirmed (or skipped).

### Step 2 — Task intake

Single prompt:
```
What are you building or fixing — one sentence.
> _
```

Auto-classify task type from keywords in the response:

| Keywords | Classification |
|---|---|
| add / build / create / implement / new | `new-build` |
| fix / bug / broken / patch / correct | `fix` |
| change / update / migrate / refactor / modify | `change-request` |
| ambiguous | Ask: "Is this a new feature, a bug fix, or a change to existing behavior? (feature/fix/change)" |

**Fix-fast eligibility check** — offer routing to `/fix-fast` only when all five hold:
- Classification is `fix`
- Description implies no UI/UX changes
- Description implies no API or schema changes
- File count implied: ≤ 2
- Size implied: tiny (≤ 50 lines)

If eligible, ask:
```
This looks like it may qualify for /fix-fast — a compressed path that skips Analyze and Design.
Eligibility: fix only, ≤ 2 files, ≤ 50 LOC, no API/schema changes, no UI changes.
Route to /fix-fast? [Y/n — if unsure, choose n and use the full flow]
```
If yes: tell the user to run `/fix-fast` with their description. Stop. Do not invoke fix-fast yourself.

### Step 3 — Auto-generate artifacts

**scope.md** — if `.claude/sdlc/scope.md` does not exist, create it from the description:
```
# Scope: <repo-slug or "this project">

## Summary
<one-sentence description from Step 2>

## In scope
- <heuristic: primary files or directories implied by description>

## Out of scope
- Anything not mentioned above
- Test infrastructure changes beyond what the task requires
- Documentation unless explicitly part of the task

**Status:** draft — review and confirm in /plan before treating as authoritative
```

**Plan artifact** — create `.claude/sdlc/plans/<slug>.md` using `templates/plan.md` with these fields pre-filled:

| Field | Source |
|---|---|
| `REQ-ID` | `REQ-001` (or next available `REQ-N` by scanning existing plan files) |
| `Classification` | auto-classified from Step 2 |
| `Stack` | detected in Step 0 |
| `In-scope files` | heuristic from description keywords — mark as `[suggested]` |
| `In-scope functions` | `TBD — refine in /plan` |
| `Out-of-scope` | standard safety list |
| `Estimate` | keyword-based: "add/build/create" → medium; "fix" → small; "change" → medium |
| `Status` | `draft` |

All auto-generated fields are marked `[suggested]` or `[draft]` — they require human confirmation in `/plan` before they are authoritative.

### Step 4 — "What this armed" summary

Print the activation summary, then display the plan inline:

```
[SDLC] Workflow enabled.

  Repo:    github.com/owner/my-app     (or: no remote detected)
  CI:      github-actions              (or: none detected)
  Stack:   python / pytest / ruff      (or: not detected)
  Tracker: GitHub Issues → owner/my-app

  config/tools.json              → written           (or: skipped — run /configure to set up)
  .claude/sdlc/scope.md          → created  [draft — review in /plan]
  .claude/sdlc/plans/<slug>.md   → REQ-001  [draft — review in /plan]
    classification: <type>                   [suggested]
    estimate:       <size>                   [suggested]
    in-scope files: <n> heuristic matches    [suggested — confirm in /plan]

Hooks now active:
  ✓ plan-gate        — blocks edits without a signed plan
  ✓ secret-scan      — catches credentials before they're written (always-on)
  ✓ diff-scope-check — warns if edits drift outside scope
  ✓ bash-safety      — flags destructive shell commands

Next: review the plan below, then run /plan to sign it.
All [draft] and [suggested] fields require your confirmation in /plan before they are authoritative.
```

Display the plan artifact inline. Hand off to `/plan` for review and sign-off. Do not invoke `/plan` yourself — print the hand-off message and stop.

---

## PATH B — Re-enable After Suspension (Steps R1–R5)

This path runs when `.claude/sdlc/.suspended` exists. Skip the config wizard entirely — config already exists.

### Step R1 — Run snapshot verification

Call `hooks/suspend-snapshot.sh verify`. The script outputs plan-keyed JSON to stdout.

If the script outputs `{"error": "no_snapshot", ...}`: inform the user:
```
[SDLC] Snapshot file not found. Cannot verify governance integrity.
Re-enabling without tamper detection. Enforcement will be active but no reconciliation is possible.
Continue? [Y/n]
```
If yes: skip to Step R5 (re-enable directly). If no: stop.

If the script outputs `{"error": "decryption_failed_refused"}` or `{"error": "key_expired_refused"}` or `{"error": "key_missing_refused"}`: the user already declined degraded mode inside the script. Print:
```
[SDLC] Re-enable cancelled. Workflow remains suspended.
```
Stop.

### Step R2 — Parse verify output

The JSON has this shape (from `suspend-snapshot.sh verify`):
```json
{
  "plans": {
    "REQ-001": {
      "changed_files": [...],
      "severity": "HIGH",
      "revert_candidates": [...]
    }
  },
  "clean_plan_count": 2,
  "degraded": false,
  "cap_warning": null
}
```

**Scope overflow cap warning:** if `cap_warning` is non-null, display it before showing any plan output:
```
[SDLC] WARNING: <cap_warning text>
Active plans exceeding the cap are not marked safe — they are deferred. Run /status after re-enable to review them.
```

Count changed plans (K = keys in `plans` where `changed_files` is non-empty).

- K = 0 → no governance changes → skip to Step R4 (clean path)
- K ≥ 1 → changed plans present → Step R3

### Step R3 — Per-plan reconciliation prompts

For each changed plan in `plans` (ordered by severity: HIGH first, then LOW), show:

```
━━ REQ-001  <slug>  [HIGH] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Files modified during suspension:
    .claude/sdlc/gates/build-<slug>.md
    .claude/sdlc/sign-offs/REQ-001-qa.md
    src/auth/login.py

  Re-examining requirements...
```

Load the changed files for this plan (from `changed_files`), plus their one-hop artifact neighbors per RFC §7.3 rules, restricted to this plan's active artifacts. Produce a plain-language summary — no gate-file notation, no jargon.

Then show:
```
  Changes summary:
    • Build gate: QA sign-off was removed
    • src/auth/login.py: expanded from 120 → 190 lines
      (outside original REQ-001 scope of 3 files)
    • No schema or API changes detected

  Accept changes to REQ-001? [Y/n]
```

For plans with severity LOW (source drift only, no governance artifacts changed):
```
━━ REQ-003  <slug>  [LOW] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Files modified during suspension (source drift only):
    src/ui/search.py

  Changes summary:
    • src/ui/search.py: 8-line addition within REQ-003 scope

  Accept changes to REQ-003? [Y/n]
```

If the user enters `n` on **any** plan: collect all rejected REQ-IDs. After all prompts complete, print:
```
  <REQ-ID> rejected. Workflow stays suspended.

  Revert these files and run /start to try again:
    <revert_candidates for each rejected plan>
```
`.suspended` marker remains. Snapshot is preserved. Stop.

If the clean plan count is non-zero, append after all per-plan prompts:
```
<N> plan(s) verified clean: <REQ-IDs>
```

**For accepted HIGH-severity plans** — propose REQ supersession (do not write the new plan file yet):

```
  Proposed: supersede REQ-001 → REQ-002.

  REQ-001 remains active. REQ-002 has not been written.

  To confirm:
    1. Run /plan — Claude will draft REQ-002 for your review.
    2. Sign REQ-002 in /plan as you would any new plan.
    3. REQ-001 is marked superseded only after REQ-002 is signed.
```

For accepted LOW-severity plans: no supersession proposed. Drift is surfaced in `/status`.

### Step R4 — Clean path (K = 0)

```
[SDLC] Resuming after suspension — no governance changes detected.

  Source files modified during suspension: <N>  [below escalation threshold]
  ⚠ Suspension drift pending review — run /status to see affected files.

  Workflow re-enabled.
```

(Omit the drift line if source changes are also zero.)

Snapshot is deleted: `rm .claude/sdlc/.suspension-snapshot.enc`

### Step R5 — Re-enable

```bash
mv .claude/sdlc/.suspended .claude/sdlc/.enabled
```

If snapshot still exists (governance changes accepted, supersession pending): leave it until REQ supersession is signed. Do not delete it here.

Print:
```
[SDLC] Workflow re-enabled. Enforcement is active.
plan-gate will require a signed plan before editing — sign the superseding REQ in /plan.
```

---

## PATH C — Already Enabled

If `.claude/sdlc/.enabled` exists and `.claude/sdlc/.suspended` is absent:

```
[SDLC] Workflow is already enabled.
Run /plan to start a new task or continue an existing one.
```

Hand off to `/plan` if the user also provided a task description. Otherwise stop.

---

## What this skill must NOT do

- Do not write plan artifacts in re-enable path — only propose supersession. `/plan` owns the plan file.
- Do not auto-run `/plan` after activation — print the hand-off message and let the user run it.
- Do not mark REQ-001 as superseded before the human signs REQ-002 in `/plan`.
- Do not delete the snapshot until: (a) clean path (K=0), or (b) all supersession sign-offs are confirmed.
- Do not skip the re-enable path even if the config wizard hasn't been run.

## Graceful degradation

- `hooks/suspend-snapshot.sh` not found → surface the error; offer to re-enable without integrity verification (Step R1 no-snapshot path).
- `config/tools.json` absent on fresh install → proceed without config; show "not configured" in the armed summary; prompt to run `/configure` to finish setup.
- `.claude/sdlc/plans/` absent → treat as no active plans; skip plan artifact creation in Step 3 for re-enable; still create scope.md and plan in fresh install.

## References

- `hooks/suspend-snapshot.sh` — verify mode called in Step R1
- `skills/plan/SKILL.md` — receives pre-fill context after Step 4 or after REQ supersession proposal
- `commands/fix-fast.md` — fix-fast eligibility rules
- `docs/rfcs/opt-in-activation-suspend-resume.md` §5 (fresh install) and §7 (re-enable)
