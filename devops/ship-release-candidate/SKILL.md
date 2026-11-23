---
name: ship-release-candidate
description: >
  Produce a thorough release candidate PR to main. Validates state, checks
  merge conflicts, infers the version bump from commit history, and drafts a
  release-focused PR body. Trigger on requests like "cut a release", "cut an
  RC", "prep the release candidate", or "what version should this be". This
  fires only when a branch bundles multiple changes into a versioned release
  — for an ordinary single-change PR, use create-pr instead.
---

# ship-release-candidate

You are a release manager. Follow these steps **in order** to produce a thorough, reviewable release candidate PR to `main`.

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Step 1 — Fetch, orient, and validate branch state

Run the basic repository checks first:

```bash
git fetch origin --tags
git branch --show-current
git status --short
git diff
git diff --staged
git status -sb
git log --oneline --decorate -10
git log origin/main..HEAD --oneline
git diff --stat origin/main...HEAD
```

Record:

- `CURRENT_BRANCH`
- whether there are uncommitted changes
- whether the branch tracks a remote and is up to date with it
- how many commits are ahead of `origin/main`
- whether there is meaningful diff versus `origin/main`

Stop and ask the user if:

- `CURRENT_BRANCH` is `main`
- there are local changes that may not belong in the release candidate
- the branch is behind its upstream and needs a sync decision
- there are no commits or no meaningful diff versus `origin/main`

---

## Step 2 — Check release blockers before drafting anything

Run these checks and stop if any fail:

```bash
git ls-remote --heads origin main
git merge-base HEAD origin/main
git merge-tree $(git merge-base HEAD origin/main) origin/main HEAD
gh pr list --head <CURRENT_BRANCH> --base main --state open
```

Rules:

- If `origin/main` cannot be resolved, stop and report it
- If merge simulation shows conflicts, stop and report that the branch is not merge-ready
- If an open PR already exists from `CURRENT_BRANCH` to `main`, do not create a duplicate; return that PR instead

---

## Step 3 — Review the complete release candidate scope

Analyze the full branch contents, not just the latest commit:

```bash
git diff origin/main...HEAD
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
git log origin/main..HEAD --oneline
```

Categorize the included work into release-friendly buckets:

| Category                       | Indicators                                                                   |
| ------------------------------ | ---------------------------------------------------------------------------- |
| New Features                   | new controllers, services, endpoints, modules                                |
| Bug Fixes                      | commits or diffs addressing defects                                          |
| Refactoring                    | internal restructuring with no intended behavior change                      |
| Documentation                  | `*.md`, docs, comments intended for readers                                  |
| Tests                          | `*.spec.ts`, `test/`, test config                                            |
| Configuration / Infrastructure | workflows, Docker, environment docs, runtime config                          |
| Database                       | `prisma/schema.prisma`, `prisma/migrations/`                                 |
| Dependencies                   | manifest or lockfile dependency updates                                      |
| Breaking Changes               | commits with `!` or `BREAKING CHANGE:` or behavior requiring consumer action |

Call out explicitly:

- migrations or schema changes
- new environment variables
- behavior changes that need rollout coordination
- mixed concerns that may make the release candidate too broad

If the branch includes unrelated work, stop and ask the user before proceeding.

---

## Step 4 — Determine the expected version bump carefully

Use tags and commit history to infer the bump:

```bash
git describe --tags --abbrev=0
git log <last-tag>..HEAD --oneline
```

Rules:

- Any `BREAKING CHANGE:` footer or `!` in a relevant commit -> `major`
- Otherwise any `feat` -> `minor`
- Otherwise `fix`, `perf`, `refactor`, or `revert` -> `patch`
- If the branch only contains `docs`, `test`, `chore`, `ci`, `build`, or `style`, flag that this may not justify a release

If no tag exists, state that clearly and infer the bump from the available commit history only.

---

## Step 5 — Use the repository PR template as a base

Before drafting the PR body, check `.github/` for a pull request template and use it if present.

Common locations:

```text
.github/pull_request_template.md
.github/PULL_REQUEST_TEMPLATE.md
.github/PULL_REQUEST_TEMPLATE/*.md
```

If a template exists:

- preserve its sections
- adapt the release-candidate narrative to fit that structure
- add release-specific detail in the sections where it naturally fits
- do not invent issue numbers, test results, screenshots, deployment steps, or JIRA tickets

For this repository, align the release candidate body with the detected template sections, especially:

- `Summary`
- `Changes Made`
- `Type of Change`
- `Testing`
- `Database Changes`
- `Deployment Notes`
- `Checklist`
- `Additional Notes`

---

## Step 6 — Draft the release candidate PR body

Create a release-oriented PR title and body.

### Title

Use:

```text
Release Candidate: <expected-version-bump> — <one-line summary>
```

The summary should describe the overall branch, not just the latest commit.

### Body

Use the repository PR template if present, but make sure the final body still includes release-specific information such as:

- branch name and base branch
- expected version bump
- number of commits included
- grouped release highlights
- testing status and any gaps
- database and migration impact
- deployment considerations
- rollback considerations

If you need a release-specific supplement, add it in `Additional Notes` rather than replacing the repository template entirely.

Rules:

- Only mark checkboxes that are supported by evidence
- Clearly label unknowns, risks, and unverified areas
- Mention breaking changes together with migration or rollout guidance when applicable

---

## Step 7 — Push branch if needed

If the branch is not yet pushed or is missing local commits remotely, push it safely:

```bash
git push -u origin <CURRENT_BRANCH>
```

If upstream already exists and only a normal push is needed:

```bash
git push origin <CURRENT_BRANCH>
```

Rules:

- never force push unless the user explicitly requests it
- if the push is rejected, stop and report the reason

---

## Step 8 — Create the release candidate PR safely

Use `gh pr create` with a HEREDOC body:

```bash
gh pr create \
  --base main \
  --head <CURRENT_BRANCH> \
  --title "Release Candidate: <expected-version-bump> — <summary>" \
  --body "$(cat <<'EOF'
<release candidate body aligned with the repository PR template>
EOF
)"
```

Before running it:

- ensure the branch is pushed
- ensure there is no existing open PR for the same head/base pair
- ensure the body reflects the repository template if one exists

Capture the PR URL.

---

## Step 9 — Report back with release-focused context

Show the user:

- the PR URL
- the expected version bump and how it was inferred
- stats from `git diff --stat origin/main...HEAD`
- the top 3–5 release highlights
- database/migration impact
- deployment or rollback concerns
- missing verification, CI uncertainty, or other release risks

If anything looks risky, call it out explicitly. Do not silently omit:

- large migrations
- breaking changes without rollout notes
- missing tests
- broad config or workflow changes
- unresolved push or merge issues
