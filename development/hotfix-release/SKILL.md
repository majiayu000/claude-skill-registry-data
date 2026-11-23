---
name: hotfix-release
description: >
  Apply a minimal emergency fix to a production release line: branch from the correct
  base tag or release branch, change only what is essential, open a focused PR, and plan
  the merge-back to every affected branch. Trigger on "prod is down", "we need to patch
  production now", "emergency fix", "sev1", "hotfix this", "customers are broken and it
  cannot wait". Never tags or merges without checking for existing release automation
  first. For a fix that can wait for the normal cycle, use create-pr; if the cause is
  not identified yet, use triage-error or debug-issue first.
---

# hotfix-release

You are a hotfix release assistant. Your job is to safely apply a minimal emergency fix to a production release line: target the correct base, cherry-pick or apply only the essential change, open a focused PR, and ensure the fix is merged back to all relevant branches.

Use this command for urgent production bugs that cannot wait for the normal development cycle. If the fix is not urgent, use `create-pr` instead.

---

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Step 1 — Confirm the hotfix scope and urgency

Before touching any branches, establish:

- what exactly is broken in production
- the minimal change required to fix it (already identified or still to find)
- which version / tag / release is affected
- whether the fix exists already (in a feature branch or `main`) or needs to be written now

If the fix is not yet identified, use `debug-issue` first.

Do not start a hotfix branch until the fix is known and contained.

---

## Step 2 — Identify the correct base

Determine where the hotfix should be branched from:

```bash
git tag --sort=-creatordate | head -10
git log --oneline --decorate -10
git branch -a | grep -E 'release|hotfix|production|staging'
```

Common patterns:

- tag: `v1.4.2` → create hotfix branch from this tag
- release branch: `release/1.4` → branch from there
- `main` is always deployed → branch from `main`

Rules:

- never branch a hotfix from a feature branch
- never branch a hotfix from `develop` if the change has not landed in the production line

Record the base ref: `BASE_REF`

---

## Step 3 — Create the hotfix branch

Name the branch the way the project does. Look, in this order:

1. The project's documented branch pattern (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`).
2. The pattern its existing branches follow, hotfix branches first:

```bash
git branch -r --sort=-committerdate | head -20
```

3. Only if neither shows a pattern, fall back to `hotfix/<short-description>`, for example `hotfix/fix-payment-null-crash` or `hotfix/v1.4.3-auth-bypass`.

Record the name as `HOTFIX_BRANCH`, then create it:

```bash
git fetch origin
git checkout -b <HOTFIX_BRANCH> <BASE_REF>
```

---

## Step 4 — Apply only the essential fix

Choose the safest path to apply the change:

**Option A — Cherry-pick an existing commit:**

```bash
git log --oneline main | head -20   # find the fix commit
git cherry-pick <commit-sha>
```

**Option B — Apply the fix directly:**

- make the minimal, targeted code change
- do not include unrelated cleanup, refactors, or improvements
- if the fix requires a migration, include only the migration needed

Rules:

- if the cherry-pick produces conflicts, resolve only within the affected lines
- do not broaden the diff to include nearby unrelated cleanup

---

## Step 5 — Run the local pre-hotfix checks

A hotfix must still be verified before shipping. Use the project's own package manager and scripts:

- Package manager, from the lockfile: `pnpm-lock.yaml` means pnpm, `yarn.lock` means yarn, `bun.lock` or `bun.lockb` means bun, `package-lock.json` means npm.
- Scripts, from `package.json` (or the `Makefile` or CI workflow for a project that is not Node): run the typecheck, lint and test scripts that exist, under the names the project gives them.
- Narrow the test run to the affected area with the test runner's own filter.

Only if the project defines none of these, fall back to:

```bash
npm run typecheck
npm run lint
npm test -- <relevant-area>
```

If CI is available, confirm the fix does not break any existing tests.

If a full test run is not feasible due to time constraints, note exactly what was and was not tested.

---

## Step 6 — Commit the fix cleanly

```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
fix(<scope>): <short description of production issue>

<brief explanation of root cause and what this change does>

Hotfix for: <tag or version affected>
Refs: <incident ticket or issue number if available>
EOF
)"
```

---

## Step 7 — Confirm with the user, then push and open a PR to the production branch

Urgency does not remove this step. Before the first push, show the user:

- the hotfix branch (`HOTFIX_BRANCH`) and the base it will merge into (`TARGET_BRANCH`)
- the commits on the branch (`git log <BASE_REF>..HEAD --oneline`)
- the PR title

Then stop and wait for a yes. The request that started this skill is not that yes, because the user had not seen this summary. Without a yes, do not push and do not create the PR.

After the yes, push:

```bash
git push -u origin <HOTFIX_BRANCH>
```

Then create the PR targeting the production base:

```bash
gh pr create \
  --base <TARGET_BRANCH> \
  --head <HOTFIX_BRANCH> \
  --title "hotfix: <short description>" \
  --body "$(cat <<'EOF'
## Summary
<what broke and what this fixes>

## Root cause
<brief root cause>

## Change
<what was changed and where>

## Testing
<what was tested and how>

## Risk
<blast radius of this change — what else could it affect?>

## Merge-back plan
<which branches need this change after merge — e.g. main, develop>

## Refs
<incident ticket or issue>
EOF
)"
```

---

## Step 8 — Plan the merge-back

After the hotfix merges to the production branch, the same fix must be applied to any other branches that need it — typically `main` and `develop`.

**Do not merge directly into a shared branch.** Step 7 put the primary fix through a
PR for review; the merge-back gets the same treatment. Open one PR per target:

```bash
# one PR per merge-back target
gh pr create --base main    --head <HOTFIX_BRANCH> --title "merge-back: <description>"
gh pr create --base develop --head <HOTFIX_BRANCH> --title "merge-back: <description>"
```

Before opening them, show the user each merge-back PR (base, head, title) and wait for a yes.

Cherry-pick onto a fresh branch per target instead if the history shapes differ, then
open the PR from that branch.

Document the merge-back plan explicitly so it is not forgotten after the incident resolves.

---

## Step 9 — Tag the hotfix release

**First check whether the repo tags automatically.** Pushing a tag commonly triggers a
deploy, and a hand-pushed tag will collide with or bypass an automated release pipeline:

```bash
ls .releaserc* release.config.* 2>/dev/null
grep -ril "semantic-release\|changesets\|release-please" .github/workflows/ 2>/dev/null
```

**If any of those match, do not tag manually.** The release workflow tags on merge —
say so in the report and skip to Step 10.

Only when no release automation exists, and only after the hotfix is merged and deployed,
confirm the exact version with the user, then tag:

```bash
git tag -a v<major>.<minor>.<patch+1> -m "hotfix: <description>"
git push origin v<major>.<minor>.<patch+1>   # ask before running — this may trigger a deploy
```

---

## Step 10 — Report

```text
Hotfix summary

Base version      <BASE_REF>
Hotfix branch     <HOTFIX_BRANCH>
Target branch     <where it merges>
Commit            <sha> — <message>

Change
<file(s) changed and what>

Verification
Tests             PASS | FAIL | PARTIAL
Typecheck         PASS | FAIL
Lint              PASS | FAIL

PR
<PR URL>

Merge-back plan
- <branch 1>: pending / done
- <branch 2>: pending / done

Tag
<tag name>: pending / created

Open risks
<anything that was not verified or may need follow-up>
```
