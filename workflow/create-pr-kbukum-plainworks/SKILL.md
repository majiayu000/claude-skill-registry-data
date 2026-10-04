---
name: create-pr
description: >-
    Open a pull request that reads well for a reviewer — understand the change set at a high level,
    fill the repo PR template honestly, and keep the description a concise, organized,
    developer-friendly summary (no file-by-file dumps, no internal/batch/plan detail). Always open in
    draft. Bound to plainworks' engineering baseline. Use only when explicitly asked to create or
    open a PR.
---

# Opening a reviewer-friendly pull request

A PR is a reviewer's entry point, not a commit log. Create a PR **only when explicitly asked** — never as a side effect of finishing work — and always open it in **draft** so the maintainer marks it ready.

## 1. Preconditions

The branch is committed and **pushed** to `origin` (the maintainer commits and pushes, per repo workflow). Confirm before opening:

```bash
git rev-parse --abbrev-ref HEAD
git status --short                     # expect clean; uncommitted work is not in the PR
git log --oneline origin/main..HEAD    # the (single) commit this PR will contain
```

Base is `main`. If the branch isn't on the remote yet, ask the maintainer to push rather than pushing for them.

## 2. Understand the change at a high level

Read the actual diff and group it by concern — do not narrate per file:

```bash
git diff origin/main...HEAD --stat
git diff origin/main...HEAD            # skim for the shape of the change, not to transcribe it
```

Answer, in your head: what capability/fix/refactor is this, which packages and layer it touches, whether it changes a public seam (`std` contracts, event shapes, the auth-header seam, provider shapes) that other packages implement, and whether the DoD gates pass.

## 3. Write the description — high level, organized, simplified

Fill every section of [`../../PULL_REQUEST_TEMPLATE.md`](../../PULL_REQUEST_TEMPLATE.md). The guiding rule: **a reviewer should grasp the change from the description alone**, without reconstructing it from the diff.

- **Title** — Conventional Commit style naming the change: `feat(channel): SSE reconnect`, `refactor(state): per-request store factory`. No plan/batch/step numbers.
- **Description** — a few sentences of *what changed and why it's shaped this way*, at the level of capabilities and decisions.
- **Motivation** — the problem it solves. Link issues as `Fixes #123`; reference **other repos as full URLs**, never a bare `#45`.
- **Type of Change / Package(s) Affected** — mark accurately.
- **Changes Made** — a short, grouped bullet list of the *key* changes by concern, not one bullet per file and not a commit log.
- **Testing** — check only the DoD gates you actually ran, scoped to affected packages (`turbo run test --filter=@plainworks/<name>`, `bun run check-boundaries`, `bun run check-versions`). Paste real evidence if useful; don't fabricate output.
- **Breaking Changes** — alpha, so breaking changes are welcome. Say what was redesigned and what was removed, never a migration shim or deprecation path. Check **Breaking change** honestly, and use a `minor` Changeset.
- **Host-independence & seams** — if a package's server/client split or a shared seam changed, say so (e.g. "auth-header seam moved into `std`"; "`./client` entry added").
- **UI check** — for a change an app user can see, name the flows you checked and captured, and give one line per intended visual change. Attach a frame or contact sheet from `ui:capture` if it helps the reviewer (see `github-pr-media`).
- **Changeset** — confirm one is included; it is the release-note source of truth, so write it in the same plain, benefit-first voice (what a consumer gains, not the internal mechanics — see the Documentation baseline), not a commit log.
- **Checklist** — tick only what is genuinely true. An unchecked box is honest signal; a falsely checked one wastes reviewer trust.

Keep prose tight: no process narration, no "previously we…", no restating the diff.

## 4. Create it with `gh` — as a draft

Write the body to a file so formatting survives, then open a **draft** against `main`:

```bash
gh pr create --draft --base main --title "<conventional-title>" --body-file <path>
```

- Do **not** add reviewers or request Copilot review unless explicitly asked.
- Report the PR URL back. If asked to follow up on review threads, resolve them without posting replies under the maintainer's name.

## Baseline

The PR asserts the change meets plainworks' baseline ([`../../copilot-instructions.md`](../../copilot-instructions.md)); if it doesn't yet, run the [`review`](../review/SKILL.md) skill first and fix findings rather than opening a PR that fails its own checklist.
