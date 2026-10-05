---
name: git-collaboration-workflows
description: Run git collaboration that scales — trunk-based vs git-flow decided by deploy cadence, branch protection and required checks, PR sizing and review etiquette, monorepo vs polyrepo trade-offs, release branches and hotfixes, and history hygiene with disciplined merges.
type: skill
version: 1.0.1
updated: 2026-07-27
---
# Git Collaboration Workflows

Git workflow debates are proxy wars over one variable: **how often you ship**. Choose the
branching model from your deploy cadence, enforce it with branch protection instead of
vigilance, and keep PRs small enough to review honestly. Deep detail in `references/`;
protection settings and a PR-review playbook in `examples/`; `scripts/check-branch-hygiene.mjs`
audits a repo's local hygiene.

## Choosing the branching model

| You deploy… | Model | Shape |
|---|---|---|
| Continuously (SaaS default) | **Trunk-based** | Short-lived branches (<2 days) → main; release = deploy main; flags hide unfinished work |
| On a cadence (mobile, desktop) | Trunk + **release branches** | Cut `release/1.24` from main; only cherry-picked fixes land on it; tag ships |
| Multiple supported majors (enterprise, on-prem) | Trunk + long-lived release lines | Fix on main first, cherry-pick back (never the reverse) |

Full git-flow (develop + feature + release + hotfix branches) earns its complexity only in
the third row — adopted by SaaS teams it mostly adds merge ceremony and delays integration.
The deciding question is never taste; it's "what do we support in production simultaneously?"

```text
trunk-based:   main ──●──●──●──●──►            release = deploy latest green main
cadence:       main ──●──●──●──►               release/1.24 ──●(cp)──tag 1.24.1
hotfix:        branch from the SHIPPED TAG, fix, tag — then forward-port to main SAME DAY
```

Mechanics of each and the hotfix path: `references/branching-models.md`.

## Short-lived branches or bust

Integration pain grows superlinearly with branch age — two weeks of divergence is a merge
project. Working rules:

```text
branch age    < 2 days   (rebase on main daily if longer is unavoidable)
PR size       ≤ ~400 changed lines — review quality collapses beyond that
one PR        one logical change (refactor ≠ behavior change ≠ formatting)
big features  land dark in slices behind a flag (feature-flags-experimentation),
              never in a long-lived feature branch
```

Stacked PRs (chain of small dependent PRs) are the escape hatch when a change is genuinely
large: reviewable slices, one logical narrative — etiquette and mechanics in
`examples/pr-review-playbook.md`.

## Protection is policy-as-config

Trust the settings, not the culture doc — `examples/branch-protection.md` has the full
recommended set. The load-bearing ones: required status checks (build + tests + lint, the
same gate for everyone including admins), required review (1 for most teams, 2 for
money/security paths via CODEOWNERS), **stale-review dismissal** (a re-push invalidates old
approvals), and linear history or squash-only merges so `main` reads as a changelog.
Conventional commit messages (`conventional-commits`) make that changelog machine-readable.

## Merge strategy: pick one, encode it

- **Squash-merge** (default recommendation): PR = one commit on main; messy WIP commits
  vanish; revert = one commit. Cost: intra-PR history lost — fine when PRs are small (rule
  above).
- **Rebase-merge**: preserves commit series linearly — only worth it if authors curate
  commits (interactive rebase discipline); otherwise you're preserving noise.
- **Merge commits**: keeps true topology; `main` becomes unreadable at scale. Reserve for
  release-branch merges where the merge point *is* the information.
- Never mix by whim — one strategy per repo, enforced in settings. And **never rewrite
  pushed shared history**; `revert` forward instead (`references/history-hygiene.md` covers
  recovery, bisect, and blame-friendly practices).

## Monorepo vs polyrepo (an ownership decision)

Monorepo buys atomic cross-cutting changes, one dependency graph, and universal refactors —
at the price of tooling (selective CI via path filters/affected-graphs, CODEOWNERS, merge
queues at scale). Polyrepo buys independent pace and clear boundaries — at the price of
version-matrix coordination (`release-coordination` in `deployment-strategies`) and
cross-repo changes becoming N-PR projects. Rule of thumb: one product surface + one deploy
train → monorepo; genuinely independent products/teams → polyrepo. The failure mode is the
*unmanaged* middle: 40 repos with hand-maintained version matrices and no contract tests.

## Pitfalls

- Long-lived feature branches "to keep main stable" — main stays stable via checks and
  flags; the branch just batches risk into one giant merge.
- `main` broken and normalized ("just skip that test") — a red main blocks everyone's
  integration; fixing it outranks all feature work, and a merge queue prevents most of it.
- Force-push to shared branches — reflog archaeology for the whole team; protect against it
  in settings.
- Review theater: 2,000-line PRs approved in 4 minutes — the size rule exists because
  reviewers are human.
- Cherry-picking main→release without fixing main first — the fix vanishes in the next
  release cut.

## Verification

Run `node scripts/check-branch-hygiene.mjs` inside any repo: it reports stale branches,
oversized undelivered work, and non-linear history segments. Then diff your repo settings
against `examples/branch-protection.md`. Pairs with `conventional-commits`,
`ci-pipeline-design`, `code-review` practices in `deployment-strategies`, and
`feature-flags-experimentation`.
