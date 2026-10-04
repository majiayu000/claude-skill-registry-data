---
name: pr-authoring
description: >
  Author pull requests with intent-separated commits, blast-radius disclosure,
  and verification evidence. Load when opening a PR, writing a PR description,
  separating refactor from feature commits, or summarizing a change set for
  review. Also triggers on "write the PR", "PR body", "intent-separated
  commits", "split refactor from feature", "pr summary", or after safe-change
  cycles complete. Extends git-workflow-and-versioning — does not replace it.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: arXiv:2511.04824 Agentic Refactoring study, addyosmani/agent-skills git-workflow
  resources:
    references:
      - PR-CONVENTIONS.md
      - examples.md
---
# PR Authoring

You produce reviewable PRs: **one intent per commit**, body that states what changed, why, blast radius, and verification result. Mixed refactor+feature PRs raise review burden — separate them.

## Hard Rules

Never mix `feat`/`fix` commits with `refactor`/`chore` formatting in one PR when avoidable.
Every PR body includes blast radius (from `dependency-mapping` if available) and verification evidence (from `safe-change` or CI).
One primary intent per PR — split if the diff serves two goals.
Follow commit conventions from `git-workflow-and-versioning`.
Never omit `behaviorVerified: false` when tests were not run.

---

## Workflow

### Step 1 — Classify commits

Group staged/historical commits by intent:

| Intent | Commit types |
|--------|--------------|
| Behavior change | `feat`, `fix` |
| Structure only | `refactor` |
| Hygiene | `chore`, `docs`, `test` |

If mixed, split into separate commits/PRs before proceeding.

### Step 2 — Gather evidence

Collect: impact report (dependency-mapping), verify JSON (safe-change), or CI links.

### Step 3 — Write PR body

Use template in `references/PR-CONVENTIONS.md`. Fill every section — no placeholders.

### Step 4 — Pre-flight review

- [ ] Title matches primary intent (`feat:` / `fix:` / `refactor:`)
- [ ] Body lists blast radius
- [ ] Verification section has commands + results
- [ ] No secrets in diff or body

### Step 5 — Output for user

Emit the PR title, body (markdown), and suggested `gh pr create` command if applicable.

---

## Gotchas

- "While I'm here" refactors belong in a separate PR — reviewers cannot bisect mixed intent.
- Large PRs without blast radius get rejected — the table is mandatory.
- Squashing intent-separated commits destroys narrative — prefer merge with history.

---

## Output Format

```markdown
## PR draft — [title]

**Intent:** [feat|fix|refactor|chore] — [one line]

### Body
[paste PR-CONVENTIONS template filled]

### Commits (intent-separated)
1. `type: message`
2. ...

### Create
gh pr create --title "..." --body "$(cat <<'EOF'
...
EOF
)"
```

---

## Examples

Teaser: Two commits — `refactor: extract parser` then `feat: add validation` — PR body lists 3 affected modules and `npm test` pass.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Reviewers can figure out intent" | Mixed PRs take 2× review time (empirical). |
| "One PR is faster" | Faster to merge wrong. |
| "Blast radius is obvious" | Write it — forces you to check. |
| "CI will catch it" | CI doesn't explain *why* you changed it. |
| "Docs don't need verify section" | Docs PRs still need scope + risk statement. |

## Verification

- [ ] Intent-separated commits listed
- [ ] PR body uses PR-CONVENTIONS template
- [ ] Blast radius section present
- [ ] Verification evidence attached

## Red Flags

- feat + refactor in single commit
- PR body missing verification section
- behaviorVerified omitted when no tests ran

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 2 family)

## Impact Report

```
PR drafted: [title] | Intents: N commits | Blast radius: [low|med|high]
Verification cited: [yes|no]
```
