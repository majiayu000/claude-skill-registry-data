---
name: github-portfolio-scan
description: >-
  v1.0.1 — Use when a directory of git checkouts needs a resume-facing GitHub
  portfolio audit: inventory every live original repository, score each one for
  release-readiness (product story, docs, tests, license, secrets, coupling,
  authorship), report positives and flaws with evidence, and rank a tier list.
  Read-only: never edit, push, or change visibility. SEO work is a later
  github-seo run after a repo is chosen for public release.
---

# GitHub portfolio scan

Scan **any directory** of git checkouts and say, with evidence, which
repositories are close to a truthful public GitHub resume piece, what is
already strong in each one, and what still blocks a release. This is a
**scored, repeatable audit**, not a cleanup and not an SEO pass.

The only context required is a path — a folder of projects, a monorepo parent,
or a single repository. No follow-up questions before the first useful action:
resolve the path, inventory, inspect one by one, score, rank, report.

## Project instructions first

Read the target directory's own `AGENTS.md` and `CLAUDE.md` when present; they
outrank this skill for ownership, routing, and local policy. The selected
`worktree`, `commits`, `testing`, `logging`, and `docs` skills own applicable
engineering and delivery policy. This skill does not restate their rules. **This run does not
edit the scanned trees**, so a worktree is not required unless some later,
explicit task starts closing gaps.

## Non-negotiables

- **Never edit, stage, commit, merge, push, or rewrite** a scanned repository.
  The audit is reported, never stored in those trees.
- **Never change GitHub visibility, the repository name, default branch, or
  archived state.** Propose those under *Pending user actions*.
- **Never publish, create remotes, or open the private repos.** Draft the
  exact `gh` command and wait.
- **Never add continuous integration**, GitHub Pages, `llms.txt`, community
  templates, or SEO extras. Those are out of scope here. After a repository is
  actually chosen for public release, run `github-seo` as a separate dispatch.
- **Never inflate a score.** Evidence or zero. "Looks fine" is zero.
- **Never present a fork as an original product.** Rank forks in a Fork tier.
- **Never skip a listed candidate.** Inspect included checkouts one by one.
- **Never print secret values.** Note that a tracked secret exists; do not echo
  keys, tokens, or `.env` contents.

## Where the score goes

**The audit is reported, never stored in a scanned repository.** It names
paths, remotes, and private repo titles — committing that into a public content
source would publish it. Hand the user the inventory, per-repo notes, tier
list, run score, and pending actions in the run report.

Use these sections:

```text
Root: <directory>
Round: <ISO date>
Run score: <n>/100 (scan completeness)
Included: <n>   Excluded: <n>

## Inventory
| Name | Verdict | Reason |
| --- | --- | --- |

## Per-repo notes
### <name>
- Purpose:
- Visibility:
- Score: <n>/100 (<earned>/<applicable> raw, <penalties> penalty)  Tier: <S|A|B|C|D|Fork>
- Very positive: (path/command evidence)
- Needs improving: (path/command evidence)

## Tier list
S / A / B / C / D / Fork — every included name exactly once

## Pending user actions
```

## Target resolution

1. If the user named a path, use it. Otherwise use the current working
   directory.
2. Resolve symlinks. The scan root is that physical directory.
3. If the root **is** a git checkout (its own `.git`, not a linked worktree)
   **and** it has no immediate child git checkouts, audit that one repository.
4. Otherwise inventory **immediate children** of the root (plus the root
   itself when it is also a live checkout). Do not recurse into nested
   clones, `.worktrees/`, or `node_modules`.
5. One run covers the directory it was given. Do not widen to sibling folders
   the user did not name.

## Inventory: include and exclude

A child is a **live checkout** when `<child>/.git` is a **directory** (or a
gitdir whose `rev-parse --git-common-dir` equals `--git-dir`). A `.git` **file**
is a linked worktree — exclude it.

**Exclude** (record a one-line reason; do not rank):

- Linked worktrees and `*-wt-*` copy directories.
- Stores named `.worktrees` or `worktrees`.
- Notes dumps (directory name is `notes` or ends in `_notes`, and there is no
  installable product surface).
- A checkout whose own README states it is a local-only policy, scorecard, or
  SEO-ops repo and must not be a public product.

**Include** every other live checkout, including private originals and forks.
Forks are ranked only as Fork / not original product.

## Per-repo inspection

For **each included checkout, one by one**, read the real files — do not skip:

- README (or record that it is missing)
- LICENSE / LICENSE.md (full text, not just the filename)
- tests (tracked test files, not `__pycache__` or prompt corpora named "test")
- installer or public entrypoint (`install.sh`, `pyproject.toml` scripts,
  `package.json` `bin`/`start`, `main.py`)
- `git remote -v`, default branch, whether origin is reachable as public
- tracked secrets and personal-path coupling (`git ls-files`, `git grep`)

Write positives **and** gaps, each with a path or a command plus the output
you actually got.

## Scoring rules (per repository)

Each criterion scores **0**, **half** (nearest 0.5), or **full**. Half credit
means the artifact exists but fails part of its full-credit clause.

- **Evidence or zero.** A file path, a command with output, or a URL fetched
  this round.
- **N/A** only when the criterion cannot apply (no registry exists, the
  project is intentionally private so clone-URL truth is N/A, a docs-only
  contest archive has no runtime tests). Record the reason. N/A points leave
  the denominator; they are never awarded.
- **Normalized total** = `round(100 × (earned − penalties) ÷ applicable_max)`,
  floored at 0. Report raw numbers alongside it.
- Penalties subtract once each; list every instance.

This rubric measures **GitHub resume / portfolio release-readiness**, not
search ranking. Do not award points for topics, social cards, awesome-lists,
or `llms.txt`.

### A. Standalone product story — 20

- **A1 (5) Definitional sentence.** Full credit requires: the README's first
  prose sentence states what the project is, what it does, and for whom,
  without leading filler ("This repository contains…") and without assuming
  the reader already lives in a sibling setup chain.
- **A2 (5) Standalone.** Full credit requires: a stranger who clones only this
  repository can understand the product. Soft optional siblings are allowed;
  a README that is only "part of the master installer" with no product of its
  own scores 0.
- **A3 (5) Honest scope.** Full credit requires: platform, status
  (experiment, thesis, production), and at least one "what this is not" or
  supported-range statement that matches the code.
- **A4 (5) Name fit.** Full credit requires: the directory/GitHub name is
  readable and matches the product or CLI a user would type. A rename is a
  pending user action — never rename.

### B. Documentation and installability — 20

- **B1 (5) README Quickstart.** Full credit requires: a real README with
  exactly one H1 and a copy-pasteable first command that is visible before
  long operator notes.
- **B2 (5) Stranger install.** Full credit requires: install or run steps a
  person without the author's machine could follow (lockfile or
  requirements, no required clone of a still-private sibling).
- **B3 (5) Usage or architecture.** Full credit requires: real entry points
  named (`main.py`, `install.sh`, `src/…`) and at least one usage example or
  architecture map that matches those files.
- **B4 (5) No operator-only lead.** Full credit requires: the first screen of
  the README does not depend on `/home/<user>/…` paths, `~/projects/…`
  operator commands, or "press → on the submenu row" as the opening
  explanation.

### C. Tests — 15

- **C1 (8) Tracked tests exist.** Full credit requires: automated tests are
  in git (`tests/`, `test_*.py`, `*_test.py`, `*.test.js`, `cargo test`
  sources, and similar), not only local `__pycache__` or untracked files.
- **C2 (7) Tests drive a real entrypoint.** Full credit requires: at least
  one test exercises a public command, installer contract, or shipped
  module. Prompt corpora, eval YAML, or files named `test_*` that are not
  runners do not count. A docs-only reference collection may score C2 as
  N/A with a reason.

### D. License — 10

- **D1 (6) Recognizable LICENSE.** Full credit requires: a LICENSE file
  GitHub would treat as a specific SPDX license, including a permission
  grant. A warranty-only "MIT" stub (disclaimer without "Permission is
  hereby granted") is half or zero, not full.
- **D2 (4) README names the license.** Full credit requires: the same license
  is named in the README.

### E. Secrets and personal-machine coupling — 20

- **E1 (7) No tracked secrets.** Full credit requires: `.env`, key files, and
  credential dumps are not in `git ls-files`. A gitignored local `.env` with
  `.env.example` is full credit.
- **E2 (7) No personal home paths in shipped source.** Full credit requires:
  production (non-test) tracked files do not hard-code `/home/<user>/…`
  paths. Tests that fixture a fake home may still mention one; record that
  as half if production code is clean.
- **E3 (6) Sample defaults, not a personal dump.** Full credit requires:
  committed default configs are examples another person could use. A keymap,
  autostart list, or prompt pack full of the author's ratings, travel, or
  `/home/<user>` bindings scores 0.

### F. Authorship and clone truth — 10

- **F1 (6) Original product.** Full credit requires: this is not a fork, or
  the README states it is a fork of `<upstream>` and does not claim
  authorship of the upstream idea. An unmarked fork scores 0 and the repo
  is ranked Fork.
- **F2 (4) Clone-URL truth.** Full credit requires: if the README tells the
  reader to `git clone https://github.com/…`, that URL is actually public.
  Private remotes with a public-looking clone snippet score 0. Intentionally
  private products with no clone snippet may score N/A.

### G. Portfolio fitness — 5

- **G1 (5) Recruiter-shaped project.** Full credit requires: a hiring
  reader would see software, research, or a documented contest archive — not
  a WordPress dump, a notes folder, or a personal GPT-project prompt stash.

## Penalties

Subtract each once, and list every instance.

| ID | Penalty | Points |
| --- | --- | --- |
| P1 | Claims the code does not support | −5 |
| P2 | Tracked secrets or credential files | −20 |
| P3 | Truncated or non-SPDX license presented as MIT | −5 |
| P4 | Fork presented as an original product | −20 |
| P5 | Personal-data dump (ratings, private photos, database dumps) | −10 |
| P6 | Audit written into a scanned repository or committed there | −20 |

## Tiers (from the per-repo normalized score)

Map each included original to exactly one tier. Forks go to Fork regardless of
score.

| Tier | Normalized score | Meaning |
| --- | --- | --- |
| S | 85–100 | Already a truthful public resume piece |
| A | 70–84 | Close; modest polish then resume-ready |
| B | 50–69 | Real software, too coupled or not a stranger-clone story |
| C | 30–49 | Early, personal, or incomplete product |
| D | 0–29 | Not a portfolio product |
| Fork | — | Not original; do not showcase as the author's work |

Order names inside a tier by score, highest first. The run may also note
which included remotes are already public versus still private (`gh repo view`
or `gh repo list`) without changing visibility.

## Run score — scan completeness

The **measurable score for this dispatch** is completeness of the scan, not
the average of repository scores. Award only from this round's evidence:

| # | Criterion | Points |
| --- | --- | --- |
| 1 | Every immediate child (and the root, when it is a live checkout) has an include/exclude reason | 25 |
| 2 | Every included checkout was inspected one by one (README, license, tests, entrypoint, coupling) | 25 |
| 3 | Every included checkout has both positives and gaps, each with path or command evidence | 20 |
| 4 | The tier list names every included checkout exactly once | 20 |
| 5 | A sample of scanned live checkouts still shows no new modifications from this run (`git status --porcelain`) | 10 |

Penalties P2 and P6 also subtract from the run score when they apply to the
run itself (the agent committed the audit, or printed a secret).

## Work loop

Repeat until the stop condition holds:

1. **Resolve the root** and write the inventory table before scoring anything.
2. **Inspect the next included checkout** that still lacks a complete note.
   Do not batch "they are all installers" from a filename.
3. **Score that checkout** against A–G with evidence. Assign a tier.
4. **After the last included checkout**, build the tier list. Confirm every
   included name appears once and no excluded name is ranked.
5. **Verify non-modification** on a sample of live checkouts (the scan root
   plus at least the already-public remotes, when those are in scope).
6. **Score the run.** If anything is missing, go back to step 2. Do not start
   editing repositories to raise their A–G scores in this skill.

### Stop condition

Stop when **all** of these hold:

- the run score is 100/100,
- every included checkout has a per-repo score with evidence from this round,
- the tier list is complete,
- no scanned tree was modified by this run,
- remaining work that needs the user (make public, rename, add a LICENSE the
  owner must choose) is listed under *Pending user actions*.

"Nothing to do" is not valid while any included checkout lacks a note.
There is no deadline: a complete evidenced scan of fewer repositories the
user named beats a guessed ranking of a wider tree.

After the report, **do not** start a `github-seo` loop, add topics, or open
the private remotes unless the user explicitly asks in this conversation.

## Measuring

Prefer real measurements. Adapt the root; do not assume a username.

```sh
ROOT="${1:-.}"

# Live checkout vs linked worktree
git -C "$child" rev-parse --git-dir --git-common-dir
test -d "$child/.git" && echo live || echo linked-or-missing

# Tracked license, tests, secrets
git -C "$child" ls-files LICENSE LICENSE.md
git -C "$child" ls-files '.env' '.env.*'
git -C "$child" ls-files | rg -n '(^|/)tests?/|(^|/)test_.*\.(py|sh|js|ts)$|_test\.py$'

# Personal-path coupling in tracked files
git -C "$child" grep -n '/home/' -- ':!*.md' ':!tests' || true

# Public vs private, when gh is available
gh repo view --json name,isPrivate,isFork,url,description
```

When `gh` is unavailable, say so in the evidence and use `git remote -v`.

Prefer `rg` over `grep` for content search. Prefer Git porcelain over
human-readable Git output that changes between versions.

## Anti-patterns

- Ranking by recency, commit count, or SEO score.
- Scoring setup-chain children as standalone products because they have
  `install.sh`.
- Treating a public README clone URL as proof the remote is public.
- Counting `finetuning/prompt_testing/prompt1.txt` as a test suite.
- Averaging per-repo scores into the run score.
- Starting to "fix" READMEs in the same run that was asked to scan.
- Hard-coding one machine's project list instead of reading the given
  directory.

## Definition of done

- [ ] The inventory covers every immediate child of the given root.
- [ ] Every included checkout was inspected one by one with evidence.
- [ ] Every included checkout has positives, gaps, a per-repo score, and a
      tier.
- [ ] The tier list names every included checkout exactly once.
- [ ] Forks are in the Fork tier, not mixed in as originals.
- [ ] The run score is stated and the stop condition holds.
- [ ] No scanned repository was modified, pushed, or published.
- [ ] SEO, CI, Pages, and `llms.txt` were not added.
- [ ] Work that needs the user is listed with the exact command or draft.
