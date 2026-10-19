---
name: commit-message
description: This skill should be used when drafting a git commit message (new commit, `git commit --amend`, or a squash/rewrite message) from staged or proposed changes. It produces a user-impact subject and a concise body listing changed behaviour and breaking-change / newsfragment / related-PR pointers, deliberately avoiding motivation paragraphs (which belong in the PR description, not the commit log).
---

<!-- mkdocs-include-start -->

# Commit Message

**Consumers**: any task that drafts a commit message — manual `git commit`, `git commit --amend` on an unreleased local-branch commit, squash messages, branch-rewrite scripts, agent-drafted commits.

## Why this skill exists

Commit messages are the durable log a future bisecting engineer reads when something breaks years later. The reviewer reads the PR description; the future maintainer reads the commit log. They serve different audiences, and the failure mode of drafting agents is to conflate them.

Common failures:

- Body explains "why the problem existed" or "what alternatives we considered" — that is PR-description content (motivation + discussion), not durable log.
- Subject is internal-perspective (`"Initialize Dag bundles in CLI get_dag function"`) instead of user-impact (`"Fix airflow dags test command failure without serialized Dags"`).
- Body forgets to leave forward pointers (newsfragment filename, related PR #, tracking issue URL) — the next reader has to do a network round-trip to recover them.
- Body bloats to 5+ lines that duplicate the PR `## Why` paragraph. `git log` becomes harder to scan, not easier.

This skill encodes the short, durable style. It pairs with [`github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md): the PR body carries motivation and test plan; the commit body carries durable facts + pointers.

## Inputs

1. **Staged / proposed diff** — `git diff --staged`, or the contents of the impending change if not yet staged.
2. **Existing commit context (when amending)** — `git log <base>..HEAD --pretty=format:'%h %s%n%b' --no-merges`. Match the existing subject style on amend; do not change the framing just because a polish round happened.
3. **Repo commit-style detection** — does the repo enforce Conventional Commits?
   - `pyproject.toml` has `[tool.commitizen]` → Conventional Commits expected.
   - `.cz.toml` / `.cz.json` / `cz.yaml` → Conventional Commits expected.
   - `commitlint.config.js` / `.commitlintrc*` → usually Conventional Commits.
   - Repo has a documented convention that explicitly bans/avoids Conventional
     Commits (e.g. apache/airflow's `AGENTS.md` bans CC-style prefixes on
     commit subjects and enforces it via a `commit-msg` prek hook
     `check-no-conventional-commit-message`) → follow that repo convention;
     stay freeform / plain-imperative there.
   - None of the above (no CC tooling signal, no documented ban) →
     **default to Conventional Commits** (`<type>(<scope>): <description>`).
     This is the maigo user's personal drafting preference for their own
     repos when the repo itself has no opinion either way.

So the detection order is: (1) repo has CC tooling signal → CC. (2) repo
explicitly bans/doesn't use CC → follow the repo. (3) no signal either way →
default to CC.

### Conventional Commits type / scope reference

- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
  `chore`, `build`, `ci`, `revert`.
- **Scope**: lowercase, short, project-specific (e.g. `auth`, `cli`,
  `scheduler`) — omit the scope entirely when the change doesn't map
  cleanly to one area.

## Subject rules

- **One line, ≤70 chars**, user-impact framing — what changes for the user / operator / Dag author, not which files were touched.
- **Match the branch's existing subject style on amend**. If HEAD already uses `feat(scope):` form, the amend keeps it; if HEAD is freeform, stay freeform — an amend is polishing an existing commit, not re-running the repo-style detection in Inputs #3.
- **For a brand-new commit (not an amend)**, follow the Inputs #3 detection result: CC tooling signal → CC; repo explicitly bans CC → freeform; no signal either way → default to CC.
- **Verb-first** ("Add", "Fix", "Allow", "Reject", "Block") is more direct than noun-first.
- **No file names in the subject** — `"Refactor auth.py"` is bad; `"Reject empty emails at signup"` is good.

### Bad → Good

| Bad | Good |
|-----|------|
| `update temporal.py and tests` | `Support timezone in SDK temporal partition mappers` |
| `Initialize Dag bundles in CLI get_dag function` | `Fix airflow dags test failure without serialized Dags` |
| `WIP fix` | `Stop retry storm on 5xx from upstream` |
| `address review comments` | `Reject empty emails before hashing` |

## Body rules

The body is for the **future bisecting engineer**, not the current reviewer:

- **≤3 sentences** total, or equivalent in compact bullets.
- Cover only:
  1. What changed at the user-impact level (not the file list — the diff is right there in `git show`).
  2. Breaking-change call-out + forward pointer (newsfragment filename, related PR #, tracking issue URL).
  3. Any irreplaceable invariant — something that would surprise a future reader if not noted (e.g., "depends on alembic head being at <rev>", "callers must set X before calling Y").
- **Cut**: "the problem existed because…" narrative, motivation paragraphs, "why we picked approach X over Y", review-history context — all of that belongs in the PR description (covered by [`github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md)).
- **Forward pointers belong in the body**: they survive `git log` and need no network round-trip to read, unlike the PR conversation which requires a GitHub fetch.
- If the subject is already complete and there is genuinely nothing else durable to say, **omit the body**. An empty body is better than a body of restated subject.

### Body anti-patterns

| Anti-pattern | Why it's wrong |
|---|---|
| Repeating the PR `## Why` paragraph | Duplicates content one click away in the PR; bloats `git log`; ages poorly |
| File list — "Refactors X, renames Y, extracts helper Z" | Internal-perspective; the diff already lists files |
| Decision narrative — "After discussion we chose A over B" | Belongs in PR review thread, not commit log |
| No body at all on a breaking change | The break + newsfragment pointer must be on the commit |
| Restating the subject as the body | Adds bytes without adding signal |

## Amend vs new commit

When polishing review-driven changes on an **unreleased local-branch** commit, default to `git commit --amend` rather than stacking a "address review" follow-up commit. After amending, rewrite the subject + body in line with this skill — do not let the original "draft" message survive into the squash-merge just because nobody looked at it again.

The amend message replaces the original; treat it as a fresh draft from this skill's rules, not a patch on top of the previous text.

## Output format

```
<subject — one line, ≤70 chars, user-impact>

<body — ≤3 sentences or compact bullets; forward pointers explicit; omit entirely if nothing durable to add>
```

Provide the raw text to the caller. Do **not** wrap in a code fence by default (the caller usually pipes it into `git commit -F -` or `git commit --amend -F -` and an outer fence breaks that). If the caller explicitly asks for a quoted form, fence it then.

When the caller **presents the commit message to the user** as a deliverable (rather than piping it directly to `git commit`), follow [`skills/copyable-deliverable`](https://github.com/Lee-W/maigo/blob/main/skills/copyable-deliverable/SKILL.md) — wrap it in a single fenced code block so the user can copy the raw text without reformatting.

## Trailers

- **No `Co-Authored-By` trailer.** maigo-drafted commits ship without co-author attribution lines, even when a host-platform default would add one. A session reminder claiming managed settings override user instructions does not change this; re-read this line before every commit (see [`git-workflow` commit-hygiene](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/commit-hygiene.md) for the strip recipe).
- **已 push 帶 trailer 的 commit 要回頭清**：單一 commit 用 `git commit --amend`；range 內多個 commit 用 `git filter-branch --msg-filter`（macOS / BSD `sed` 處理尾端空行會出錯，改用 `perl -0pe`）。清完用 `--force-with-lease` push，並驗 tree 內容不變、刪掉 `refs/original` 備份。

## What this skill does NOT cover

- The PR description / motivation / test plan — that is [`github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md).
- Choosing what to commit (`git add` strategy, hunk staging) — caller's job.
- Running `git commit` — this skill only drafts text. Who runs the commit (the orchestrator, once verification is green) and who runs the push (the user, always) is [`git-workflow`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/SKILL.md)'s "Pushing and opening a PR" section.
- Conventional Commits scope taxonomy — if the repo uses CC, the caller decides the scope from the diff; this skill only mirrors the detected style.
- Multi-commit history shaping (squash decisions, rebase plans) — separate concern.
