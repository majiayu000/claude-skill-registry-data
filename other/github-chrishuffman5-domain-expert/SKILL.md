---
name: github
description: "Covers GitHub repository management and Git workflow governance: branching strategies (trunk-based, GitHub Flow, GitFlow), pull request and code review process, branch protection rulesets, CODEOWNERS, merge strategies, semantic versioning, conventional commits, Git tags, and GitHub Releases. WHEN: \"branch management\", \"branching strategy\", \"trunk-based\", \"GitHub Flow\", \"GitFlow\", \"pull request process\", \"PR review\", \"code review\", \"branch protection\", \"ruleset\", \"CODEOWNERS\", \"merge strategy\", \"squash vs rebase\", \"release management\", \"semantic versioning\", \"semver\", \"conventional commits\", \"git tag\", \"GitHub Release\", \"changelog\", \"hotfix\", \"version bump\". Do NOT use for GitHub Actions workflow YAML, runners, or CI pipeline debugging — use the `github-actions` skill."
license: MIT
---

# GitHub Repository Management Expert

This skill covers GitHub repository governance — how teams organize branches, review and merge changes, and ship versioned releases. This is the **process and policy** layer that sits above CI/CD automation: branching models, pull request workflow, branch protection, semantic versioning, and tag-based releases. For the automation that *runs* on these triggers (workflows that fire on `push`/`pull_request`/`release`), see the `github-actions` skill.

## How to Approach Tasks

1. **Classify** the request:
   - **Branching strategy** — Choosing/operating a model (trunk-based, GitHub Flow, GitFlow). Load `references/branching.md`.
   - **Pull request & review process** — PR lifecycle, required reviews, CODEOWNERS, status checks, merge strategy, protection/rulesets. Load `references/pull-requests.md`.
   - **Release management** — SemVer, conventional commits, tagging, GitHub Releases, changelogs, hotfix flow, automation. Load `references/releases.md`.

2. **Gather context** — Team size, deploy frequency, whether the product is continuously deployed (SaaS) or shipped in discrete versions (libraries, on-prem, mobile), and existing conventions. The right answer differs sharply between a 3-person SaaS team and a versioned library with many supported releases.

3. **Analyze** — Apply the principle that *the branching model, the review policy, and the release cadence must agree with each other*. A team deploying 20×/day should not run GitFlow; a quarterly-shipped on-prem product should not pretend `main` is always releasable.

4. **Recommend** — Concrete settings, commands, and file contents (rulesets, CODEOWNERS, commit conventions), not just principles. Show the `git`/`gh` commands.

## Decision: Which Branching Model?

| Model | Long-lived branches | Best for | Avoid when |
|---|---|---|---|
| **Trunk-based** | `main` only (short feature branches < 1–2 days) | High-frequency CI/CD, mature test suites, feature flags | Weak test coverage, no flag system, regulated manual QA gates |
| **GitHub Flow** | `main` + short feature branches; deploy from `main` | SaaS / continuously deployed apps, small–mid teams | You must support multiple released versions simultaneously |
| **GitFlow** | `main` + `develop` + `release/*` + `hotfix/*` | Versioned products: libraries, desktop/mobile apps, on-prem with scheduled releases | Continuous deployment — the ceremony is pure overhead |
| **Release branches** (on top of trunk/GitHub Flow) | `main` + `release/x.y` cut at release time | You ship versions but want trunk simplicity day-to-day | Single always-latest deploy target |

**Default recommendation:** GitHub Flow for deployed services, trunk-based as the maturity target; GitFlow *only* for products with discrete, supported version lines. See `references/branching.md` for full diagrams and the cherry-pick/backport mechanics.

## Branch Naming Convention

```
<type>/<short-description>        feature/user-export, fix/null-pointer-login
<type>/<issue>-<description>      feat/142-add-sso, bugfix/JIRA-88-timeout
release/<version>                 release/2.4
hotfix/<version>                  hotfix/2.3.1
```

Keep `main` (or `main` + `develop`) protected and authoritative. Everything else is disposable and deleted on merge.

## Core Concepts

### Pull Request Lifecycle

```
draft ──▶ ready for review ──▶ changes requested ──▶ approved ──▶ checks green ──▶ merged ──▶ branch deleted
```

- **Draft PRs** — open early for CI feedback and visibility without requesting review (`gh pr create --draft`).
- **Small PRs** — < ~400 lines changed review faster and more accurately. Split large work into stacked PRs.
- **Link the issue** — `Closes #142` in the body auto-closes the issue on merge.

```bash
gh pr create --base main --head feat/142-add-sso \
  --title "feat: add SAML SSO" \
  --body "Closes #142"
gh pr view --web          # open in browser
gh pr checks              # watch required checks
gh pr merge --squash --delete-branch
```

### CODEOWNERS

`.github/CODEOWNERS` auto-requests reviews and (with branch protection) *requires* owner approval for matching paths:

```
# Syntax: <path-pattern>  <owner> [<owner>...]   Last match wins.
*                       @org/maintainers
/infra/                 @org/platform-team
/services/payments/     @org/payments @alice
*.tf                    @org/cloud
/docs/                  @org/tech-writers
```

### Merge Strategies

| Strategy | Result on `main` | Use when |
|---|---|---|
| **Squash & merge** | One clean commit per PR | Default for most teams — tidy, linear history; PR title becomes the commit (pairs well with Conventional Commits) |
| **Rebase & merge** | Each commit replayed, no merge commit | You curate commits intentionally and want linear history with full granularity |
| **Merge commit** | Preserves branch + merge commit | You need the true branch topology (rare; noisy history) |

Pick **one** and enforce it (Settings → General → Pull Requests → allow only that option). Mixed strategies produce confusing history.

### Semantic Versioning + Tags + Releases

```
MAJOR.MINOR.PATCH          2.4.1
  │     │     └─ backward-compatible bug fixes
  │     └─────── backward-compatible features
  └───────────── breaking changes
pre-release / build:  2.5.0-rc.1   2.5.0+20260525
```

A **tag** marks a commit; a **GitHub Release** wraps a tag with notes and assets. Always use **annotated** tags:

```bash
git tag -a v2.4.1 -m "Release 2.4.1"     # annotated (has author/date/message) — required
git push origin v2.4.1
gh release create v2.4.1 --generate-notes # auto release notes from merged PRs
gh release create v2.4.1 --notes-file CHANGELOG-2.4.1.md ./dist/*.tar.gz  # with assets
```

Tag the **merge commit on `main`** (or on the `release/*` branch for GitFlow), never a feature branch.

### Conventional Commits → Automated Versioning

Commit messages drive the next version and the changelog when you adopt the convention:

```
<type>[optional scope][!]: <description>

feat: add CSV export            → MINOR bump
fix: handle null session token  → PATCH bump
feat!: drop Node 18 support     → MAJOR bump  (! or "BREAKING CHANGE:" footer)
docs:, chore:, refactor:, test:, ci:, perf:, build:  → no release
```

This is what tools like **release-please**, **semantic-release**, and **changesets** consume to compute versions, write `CHANGELOG.md`, tag, and create the Release — no manual version bumps. See `references/releases.md`.

## Key Patterns

### Branch Protection via Rulesets (preferred over legacy branch protection)

Rulesets are versioned, layerable, and support bypass lists. Configure in Settings → Rules → Rulesets, or as JSON via API/`gh`:

```json
{
  "name": "protect-main",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/heads/main"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    { "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "required_review_thread_resolution": true
      }
    },
    { "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [{ "context": "build" }, { "context": "test" }]
      }
    }
  ]
}
```

```bash
gh api repos/:owner/:repo/rulesets --method POST --input ruleset.json
```

Baseline for `main`: require PR + ≥1 approval, require passing status checks (`strict` = branch up to date), block force-push and deletion, require linear history, dismiss stale approvals on new commits.

### Tag-Triggered Release (handoff to CI)

The repo policy here defines *when/what* to tag; the build/publish runs in GitHub Actions. See the `github-actions` skill:

```yaml
on:
  push:
    tags: ['v*.*.*']     # release job fires only on a semver tag
```

### Hotfix Flow

- **GitHub Flow:** branch `fix/...` off `main`, PR, merge, tag `vX.Y.Z+1`, deploy.
- **GitFlow / release branches:** branch `hotfix/2.3.1` off the `v2.3.0` tag, fix, tag `v2.3.1`, then **merge/cherry-pick back into `main`/`develop`** so the fix isn't lost in the next release.

## Anti-Patterns

1. **GitFlow on a continuously deployed app** — `develop` + `release/*` ceremony with nothing to gain; you deploy `main` constantly. Use GitHub Flow.
2. **Long-lived feature branches** — Weeks-old branches cause merge hell. Integrate behind a feature flag instead.
3. **Lightweight tags for releases** — `git tag v1.0` (no `-a`) stores no author/date/message and behaves oddly with `git describe`. Always annotate.
4. **Reusing/moving a release tag** — Tags must be immutable. To fix a bad release, cut a new patch version; never re-point a published tag.
5. **Protecting `main` but allowing admin bypass silently** — If everyone is an admin, protection is theater. Use explicit, audited bypass lists in rulesets.
6. **Manual `version` bumps + hand-written changelogs** — Drifts from reality. Drive both from Conventional Commits.
7. **Mixed merge strategies** — Squash for some PRs, merge commits for others — history becomes unreadable. Standardize one.
8. **Tagging a feature branch** — A tag should point at the commit that actually landed on the release line.

## Reference Files

- `references/branching.md` — Branching models in depth (trunk-based, GitHub Flow, GitFlow, release branches), diagrams, backport/cherry-pick mechanics, monorepo vs polyrepo, feature-flag-driven integration.
- `references/pull-requests.md` — PR workflow, review etiquette, CODEOWNERS patterns, branch protection vs rulesets (full rule reference), required status checks, merge queue, stacked PRs, auto-merge.
- `references/releases.md` — Semantic versioning rules, Conventional Commits spec, annotated tags vs lightweight, GitHub Releases + assets, changelog generation, release automation (release-please, semantic-release, changesets), pre-releases and supported-version strategy.
