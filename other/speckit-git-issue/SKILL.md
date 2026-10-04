---
name: speckit-git-issue
description: Sync the linked GitHub issue's body from the current feature's spec and
  set its priority (p0..p3) and kind (bug/feature) labels (manual runs may also create
  the issue)
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.issue.md
---

# Sync Feature Issue

Create or update the GitHub issue that tracks the current feature, rendering its body from the feature's `spec.md`.

`/speckit-git-feature` opens the tracking issue with a stub body (its number drives the spec/branch numbering). This command fills that stub in — and keeps it current on every later re-spec. It runs automatically on the `after_specify` hook, and can be invoked directly as `/speckit-git-issue` at any time.

This command is idempotent: re-running it rewrites the same issue body from the current spec rather than creating duplicates or appending. It only ever touches the issue **body** on the update path — the title belongs to `/speckit-git-feature`.

## Locating the Feature

Resolve the feature directory the same way the other git commands do:

1. `$SPECIFY_FEATURE_DIRECTORY` when set.
2. Otherwise `feature_directory` from `.specify/feature.json`.

The spec is `<feature directory>/spec.md`. If neither the feature directory nor the spec file can be resolved, stop with a clear error.

## Two Invocation Modes

This one file drives two different entry points, and they behave **differently** when no issue is linked:

| Mode | Trigger | No `source_issue` in `.specify/feature.json` |
|------|---------|----------------------------------------------|
| **Automatic hook** | the `after_specify` hook | **Skip cleanly.** Print a one-line notice and exit successfully. Create nothing. |
| **Manual** | the user types `/speckit-git-issue` | May create a new issue, because the user asked for one explicitly. |

Assume you are on the **hook** path unless the user invoked `/speckit-git-issue` directly in this turn.

Why the hook must not create: `/speckit-git-feature` owns the numbering contract — it opens the tracking issue *before* numbering so the spec dir, branch, and issue share one identifier. It deliberately bypasses issue creation when the caller opted out (`--timestamp`, `--number`, `GIT_BRANCH_NAME`, `--dry-run`) or when `gh` is unavailable. In all of those cases `.specify/feature.json` has no `source_issue`, and creating an issue here would either override an explicit opt-out or hard-fail `/speckit-specify` in a repo with no `gh`.

The skip notice should read roughly:

```
[speckit-git-issue] No tracking issue linked (no source_issue in .specify/feature.json) — skipping issue sync.
  /speckit-git-feature either opted out of issue-driven numbering (--timestamp / --number / GIT_BRANCH_NAME / --dry-run) or ran without gh.
  Run /speckit-git-issue manually if you want an issue created for this feature.
```

The hook stays registered with `optional: false` in `extension.yml`: it is mandatory in the sense that the agent must always *run* it, but running it on a feature with no linked issue is a successful no-op, so it can never break `/speckit-specify` for non-GitHub users.

## GitHub Issue Integration

1. Read `.specify/feature.json`.
2. **If it has a numeric `source_issue` — update that issue's body only:**
   `gh issue edit <source_issue> --body "<body>"`
   **Do NOT pass `--title`.** `/speckit-git-feature` already set the title to `NNN: <feature description>` and owns it. The spec's H1 is the template heading (`Feature Specification: …`), not that title — writing it back would rewrite issue #N's title to something like `23: Feature Specification: …` on every re-spec.
   Then apply the triage labels (see **Priority & Kind Labels** below) — on this path only for axes the issue does not already carry.
   Here `gh` **MUST** be installed and authenticated: a linked issue that cannot be updated is a genuinely broken state. If `gh` is missing, `gh auth status` fails, or `gh issue edit` exits non-zero, stop with a clear error — never silently skip the sync.
3. **If there is no `source_issue`:**
   - On the **hook** path: print the skip notice above and exit successfully.
   - On a **manual** invocation: create one with
     `gh issue create --title "<title>" --body "<body>"`
     then parse the issue number out of the returned URL and persist it back into `.specify/feature.json` as a numeric `source_issue`, preserving every other key in the file. Subsequent runs then take the update path. Then apply the triage labels (see **Priority & Kind Labels** below). Use the spec's H1 as the title, prefixed with the feature number when the branch/spec is numbered (e.g. `008: User Auth`). This is the only path that may set a title.

## Priority & Kind Labels

Every tracking issue carries two triage labels: a priority (`p0`, `p1`, `p2`, `p3`) and a kind (`bug` or `feature`). They are not cosmetic — `/speckit-autopilot-run` orders its backlog by (priority, bug-before-feature, age), so an unlabelled issue is worked in plain filing order and a real P0 waits behind an older chore.

Apply them with the shared script — never with a hand-rolled `gh issue edit --add-label`, which would drift from the vocabulary the picker matches on and can leave an issue carrying two priorities at once:

```bash
LABEL_SCRIPT="$CLAUDE_PROJECT_DIR/.specify/extensions/git/scripts/bash/label-issue.sh"
bash "$LABEL_SCRIPT" <issue-number> --show                          # read current triage labels
bash "$LABEL_SCRIPT" <issue-number> --priority p1 --kind bug        # set them (each is exclusive)
```

Run this on **both** paths — after creating an issue, and after updating an existing one — using this policy:

1. **Read what is already there** (`--show`). A priority the human already set is authoritative: leave it alone and do not ask again. Set only the axis that is missing.
2. **The user supplied a priority or kind in their invocation** (e.g. `/speckit-git-issue p0 bug`, or said so in the turn) → use it verbatim, no question.
3. **Otherwise, when a human is in the loop, ask.** Use `AskUserQuestion` with the priority options `P0 — critical`, `P1 — high`, `P2 — normal`, `P3 — low`, and lead with the one you would have inferred, marked `(Recommended)`, so accepting the default is one keystroke. Ask for the kind in the same call **only when the spec is genuinely ambiguous** — a spec describing broken behaviour is a `bug` and one describing new capability is a `feature`, and asking about the obvious wastes the user's turn.
4. **When no human is in the loop** — the `after_specify` hook during an unattended run, or any non-interactive session — do **not** block. Infer both from the spec and apply them, then say in your output which values were inferred rather than chosen, so a human skimming the issue can correct a bad guess.

Inference heuristic, used for the recommendation in (3) and the unattended path in (4):

| Signal in the spec / issue | Label |
|---|---|
| Data loss, security hole, broken build, outage, everything blocked | `p0` |
| A user-facing feature is broken or unusable, no workaround | `p1` |
| Ordinary defect with a workaround, or ordinary new capability | `p2` |
| Polish, cleanup, nice-to-have, speculative | `p3` |
| Restores intended behaviour that is currently broken | `bug` |
| Adds or extends behaviour | `feature` |

`p2` is the deliberate default: it is also the rank the picker assumes for an unlabelled issue, so guessing it changes nothing about ordering and never fakes an urgency nobody asserted.

Label failures are **soft**: if `gh` cannot apply a label (missing repo permission, unusual label protection), print the warning the script emits and carry on — the issue body sync is the job, and an unlabelled issue is still a working issue.

## Issue Body

Derive the body from **whatever sections `spec.md` actually contains** — do not assume a fixed set. Presets may add or remove sections, so read the file and render only the headings that are present. If a section is absent, skip its heading entirely rather than emitting an empty one.

```markdown
Spec path: <feature directory>/spec.md

<one-paragraph summary of the feature>

## User Scenarios

<condensed from the spec's user scenarios section>

## Functional Requirements

<the spec's functional requirements>

## Notes

Generated/updated by /speckit-git-issue
```

**`## Success Criteria` is deliberately omitted.** Presets such as `spec-minimal` strip that section out of `spec.md`, so demanding it here would require inventing content that does not exist. The same reasoning applies to any other optional section: render it only if the spec has it.

## Failure Modes

| Situation | Behavior |
|-----------|-----------|
| No `source_issue`, hook path | **Clean skip**, exit 0 with the notice above. Nothing created. |
| No `source_issue`, manual path | Create the issue; `gh` missing/unauthenticated/failing → hard error. |
| `source_issue` present, `gh` missing or unauthenticated | **Hard error** with an install / `gh auth login` hint. |
| `source_issue` present, `gh issue edit` non-zero exit | **Hard error**, surfacing `gh`'s own message. |
| No feature directory or no `spec.md` | **Hard error** — the command was invoked with nothing to sync. |
| `label-issue.sh` fails or is missing | **Warn and continue.** Labels improve autopilot's ordering; they are not the sync. |

The rule: once an issue *is* linked, a failed sync is a real broken state worth stopping for. An absent link is not a failure — it is a supported configuration.