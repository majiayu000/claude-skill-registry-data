---
name: planning-pr
description: "Advisory checkpoint for deciding whether planning-document edits should be split into a separate planning branch/PR. Use only when the user explicitly asks where to commit `memory/SPEC.md` or `memory/PLAN.md` changes, mentions planning-doc merge conflicts, asks for a planning PR, or instructs you to prepare/submit one. Do not trigger for ordinary ln-* planning edits, one-line status updates, or routine canonical reconciliation."
---

# Planning PR

This is a **commit-placement advisor**, not part of the normal `ln-*` execution path.

Most `memory/SPEC.md` and `memory/PLAN.md` edits stay on the active feature branch. A separate planning PR is useful only when planning docs become a shared serialization point for multiple branches.

## Default stance

Stay on the current feature branch for:

- one-line status ticks or typo fixes
- marking the active frontier item done
- routine `ln-build` / `ln-scope` canonical reconciliation
- small SPEC/PLAN edits needed to explain the current code change
- local planning edits that do not affect other active branches

Do not invoke Linear, Graphite, or branch creation just because a planning file is touched.

## When to recommend a planning PR

Recommend, but do not create, a separate planning PR when one or more is true:

- the user explicitly asks for a planning PR or asks where planning edits should land
- active branches are already conflicting on `memory/SPEC.md` or `memory/PLAN.md`
- an `ln-sync` or planning pass rewrites shared narrative sections, reorders frontier items, or rotates substantial history
- edits to SPEC tracked rows (`A##`, `D###`, `Requirement N`, `I###`) are likely to collide with other active branches adding adjacent IDs
- the edit establishes a planning baseline that several implementation branches should rebase onto before continuing

Phrase it as a recommendation:

```md
This looks like a planning-PR candidate because [reason].
Do you want me to split it onto a separate planning branch off main, or keep it on the current feature branch?
```

Ask before creating issues, branches, commits, or PRs.

## Decision table

| Change | Default placement |
| --- | --- |
| One-line status tick / typo | Current feature branch |
| Mark current frontier item done | Current feature branch |
| Small canonical reconciliation for current slice | Current feature branch |
| Paragraph rewrite that affects only current work | Current feature branch, unless user wants separation |
| Large PLAN rewrite / Sequencing reshuffle / Frontier Definitions migration | Recommend planning PR |
| Substantive `ln-sync` across SPEC + PLAN | Recommend planning PR |
| SPEC tracked-ID changes with parallel branch risk | Recommend planning PR |
| Known merge conflicts in planning docs | Recommend planning PR |

When uncertain, ask. Do not silently escalate to process work.

## Planning PR workflow

Only after user approval:

1. Create a Linear issue in the **Frontend (FE)** team and **brunch** project via `/cli-linear`. Title frames the planning intent, not a feature. No parent unless explicitly named.
2. Create a Graphite branch off `main` via `/cli-graphite` after reading `docs/praxis/graphite-workflow.md`. Name it using the project branch convention.
3. Move only planning files onto the branch: normally `memory/PLAN.md`, `memory/SPEC.md`, and related archive/history files. No code, tests, config, or unrelated docs.
4. Run `npm run verify` before submission unless the user explicitly accepts a lighter check.
5. Submit a PR titled `FE-XXX: <Sentence-case planning frame>`.
6. State in the PR body that this is a planning baseline / serialization point for downstream branches.
7. After merge, restack downstream feature branches onto the new main baseline.

## Anti-patterns

- Treating this skill as a mandatory gate for every `memory/*` edit.
- Creating Linear issues or branches without explicit user approval.
- Bundling code changes into a planning PR.
- Splitting tiny status updates away from the feature branch that produced them.
- Stacking a planning PR on top of an implementation branch when the goal is a shared baseline.

## Relationship to other skills

- `ln-spec`, `ln-plan`, `ln-sync`, `ln-scope`, and `ln-build` decide what the planning docs should say.
- `planning-pr` only advises where substantive planning edits should be committed.
- `/cli-linear` and `/cli-graphite` perform the tracker/branch work after the user approves the split.
