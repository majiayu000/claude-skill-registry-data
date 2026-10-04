---
name: pr-authoring
description: >
  Use when writing or opening a PR. Opening it is not the end; CI, the merge,
  and the report stay in session-unit. The body still meets the narrative bar:
  Problem, What changed, Out of scope, evidence, Testing, AI review, Security,
  Notes.
---

# PR authoring (DeepSeek Build harness)

This skill is the **agent harness** for change delivery. It is not CI.

## Load these docs (in order)

1. `docs/product/ULTRAGOAL_PR_PLANNING.md` — **if ultragoal/overnight:** PR units, sequential/parallel, atomic commits, stacking (**before code**)
2. `docs/contributing/pr-body-standard.md` — narrative bar (Orca-aligned)
3. `docs/contributing/examples.md` — filled bodies by kind
4. `docs/contributing/pull-requests.md` — unit of work, title, labels, merge
5. `docs/contributing/review-checklist.md` — self-merge gate

## Hard rules

1. **Never push product work straight to `main`.** Branch → PR → **merge commit**
   (AGENTS.md **Merge on GitHub**; squash and rebase are disabled on this repo).
2. **One meaningful unit** per PR (one review lens). Prefer split over mega-PR.
2b. **Ultragoal:** plan **all** PR units + sequential/parallel DAG **before** implementing; stack sequential PRs; atomic commits on the branch.
3. **Title:** Conventional Commits  
   `feat|fix|docs|spec|chore|refactor|test|ci|perf|build(scope)?: summary`
4. **Exactly one kind label** matching the title type (`gh pr create --label …`).
5. **Body is the review artifact** (Orca density):
   - Summary: **Problem** + **What changed** + **Out of scope**
   - Screenshots / evidence (or “No visual change” + paths to read)
   - Testing: real commands or honest N/A + reason
   - AI review report (focus areas, flags, fixes)
   - Security audit (or justified “no sensitive surface”)
   - Notes (limits, follow-ups)
   - Kind / Related / Cache-impact / Checklist
6. **Do not** treat empty template checkboxes as done.
7. **Do not** invent “process CI” (title linters, path inventories) as a substitute for product tests.
8. Spec-before-large-feat for agent behavior; cite `docs/specs/…`.
9. Cache-impact honest for prompts / tools / skills / memory / routing.
10. After `gh pr create`, verify labels: `gh pr view --json title,labels,url`.
11. **SemVer only:** version mentions must be full `MAJOR.MINOR.PATCH` (e.g. `1.0.0`), never bare `1.0`. See `docs/contributing/versioning.md`.
12. **CLI names:** public docs prefer `deepseek-build`; `dsb` is the supported alias (ADR 0006).
13. **Opening the PR is not the end of the unit.** CI, the merge commit, and
    the report stay in `skills/session-unit`. This skill stops at the body and
    `gh pr view --json title,labels,url`.
14. **A publication-route denial is a missing registration.** If `gh pr create`
    is denied before GitHub runs because the branch is not a registered unit,
    register it in the same turn and call `gh pr create` again as one command:
    `GH_TOKEN="$(gh auth token --user innocarpe)"`, `--repo innocarpe/deepseek-build`,
    `--base main`, `--head` the branch, `--title` exactly the registered title,
    `--body-file` a `.md` file under `/tmp`, and only the registered labels.
    No pipe, no redirection, and no second command on the same line. Do not
    disable the hook, and do not end the unit by quoting the denial.

## Optional local helper (not required)

```bash
./scripts/check-pr-title.sh "spec(cache): define stable prefix rules"
```

Title/label discipline is **process**, not a GitHub Actions gate.

## Workflow sketch

Run this in a linked worktree. The primary checkout stays on `main`.
`git checkout -b` there is how that tree left `main` on 2026-09-26
(`chore/release-6.0.2`). See `skills/worktree-dispatch`.

```bash
# inside the linked worktree, already branched off origin/main
git fetch origin && git pull --ff-only
# … work …
git push -u origin HEAD
gh pr create --base main \
  --title "<type>(scope): <summary>" \
  --label <kind> \
  --body-file <path-to-full-narrative-body>
gh pr view --json title,labels,url
```

**Control-tower mode** (AGENTS.md §Control-tower checkout): the linked
worktree already has its branch (`skills/worktree-dispatch`). Do not create
that branch in the primary checkout; that checkout stays on `main`. Push with
`git -C "$WT" push -u origin HEAD`, and add `--repo innocarpe/deepseek-build
--head <branch>` to the `gh` calls when not running from inside the tree.

## Anti-patterns

| Bad | Why |
|-----|-----|
| Summary = file list | Not reviewable |
| Testing all unchecked, no reasons | Unverifiable |
| “AI Review: LGTM” | Theater |
| Mixing M1 provider + M4 subagents | Wrong unit |
| Adding CI that only checks markdown paths / PR titles | Not product CI; rejects user intent for harness |

## Done means

- [ ] Narrative body meets `pr-body-standard.md`
- [ ] Kind label present and matches title
- [ ] Unit of work is coherent and revertable
- [ ] You would accept this PR from a stranger

The unit is not done when this skill is done. CI, the merge commit, and the
report stay in `skills/session-unit`.
