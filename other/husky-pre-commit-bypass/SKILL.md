---
name: husky-pre-commit-bypass
description: >-
  Use when a Husky hook drags files the change never touched into a commit or rejects it for
  unrelated code — a `.husky/pre-commit` running the repository formatter followed by `git add -A`,
  `git status` showing modified spec, source, or config files outside the intended scope after a
  failed commit, a diff far larger than the change, or a lint / unit-test failure at commit or push
  time in code the branch does not own.
---

# Husky pre-commit hook and formatter drift

## Profile keys consumed

- `make.format`
- `make.lint`
- `make.lint_tsc`
- `make.test_unit_client`
- `make.test_unit_server`

Every command below resolves through the profile's `make` map; skip a step with a recorded note
when its key maps to `null`.

## Overview

The pre-commit hook runs the repository formatter and, in the React SPA shape, follows it with
`git add -A` — so a focused commit can swallow reformatting of files it never touched. The
compliant fix is to make the tree already formatted and already green **before** staging, so the
hook becomes a no-op. Skipping the hook is out of policy in every shape.

## When to use

- The hook rewrote spec, source, or config files that the change does not touch.
- `git status` after a failed commit shows modified files outside the intended scope.
- The commit diff is much larger than the change, obscuring review.
- The hook fails on lint or unit tests and the failure is in unrelated code.
- Not for: a deliberate repository-wide formatting pass — there the sweep is the change.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `.husky/pre-commit` runs the target mapped by `make.format`, then `git add -A`,
  then the targets mapped by `make.lint` and `make.test_unit_client` / `make.test_unit_server`;
  `git add -A` is what pulls unrelated files in.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial —
  `.husky/pre-commit` runs a staged-files-only lint runner (so no sweep) plus a host-mode type
  check via `make.lint_tsc`; the heavy format / lint / unit-test pass moved to `.husky/pre-push`.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — `.husky/`
  ships no `pre-commit` hook, and its format target is verify-only.

## Procedure

1. Run the formatter as its own step, before staging anything — the target mapped by `make.format`
   in the React SPA and Next.js shapes; the component-library shape offers only a verify-only
   format check, so there is nothing to sweep there:

   ```bash # profile-example
   make format          # React SPA and Next.js shapes
   make format-check    # component-library shape: verify only
   ```

   ```bash
   git status --porcelain
   ```

2. Decide what to do with each file the formatter touched but the change did not:
   - Pre-existing drift on the branch — land it as its own `style(#N): …` commit first, so the
     feature commit stays readable.
   - Drift that belongs to nobody — restore it with `git restore <path>` and let the branch that
     owns the file fix it.

3. Reproduce the rest of the hook locally, so nothing fails at commit time: run the targets mapped
   by `make.lint` and by `make.test_unit_client` / `make.test_unit_server`, skipping with a
   recorded note any key that maps to `null`.

   ```bash # profile-example
   make lint
   make test-unit-all
   ```

4. Stage only the intended files, confirm the set with `git diff origin/main --name-only`, and
   commit normally. The hook now finds a formatted, green tree and changes nothing.

5. Push to the feature branch explicitly — a bare `git push` follows the configured upstream, which
   is often `main`:

   ```bash
   git push origin HEAD:refs/heads/<feature-branch>
   ```

## Common mistakes

- Reaching for a hook-skipping flag instead of fixing what the hook flags — the repositories forbid
  it, and the checks it skips are the same ones CI runs.
- Formatting and committing in one motion — always inspect `git status --porcelain` in between.
- Amending the sweep away after the fact rather than splitting it into a separate commit.
- Assuming the hook is identical everywhere — in the Next.js shape the expensive gate is on
  pre-push, so a clean commit can still be rejected at push time.
- Relying on a bare `git push` — verify the target ref before pushing.
