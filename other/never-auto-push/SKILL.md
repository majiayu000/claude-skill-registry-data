---
name: never-auto-push
description: >
  Load-bearing Nimbus rule — never `git push` without explicit user authorization
  in the current turn. Commits are local. Pushes fire preprod deploys, prod
  releases (on tags), and are visible to the team.

  Trigger this skill when:
  - You're about to run any `git push` variant.
  - User asks about pushing state.
  - Session start (silently enforce).
---

## The rule

**Commit when the user says "commit" (or equivalent like "go ahead" after you've
staged work). Never run `git push` unless the user has explicitly said "push"
in the current turn.** If unsure whether the user authorized a push, ask first;
never assume.

- "commit and push the X changes" authorizes the push only for that change. The
  next change needs its own explicit authorization.
- This rule overrides any pattern where you previously pushed within the
  session. **Authorization does not carry forward.**

## What counts as authorization

Explicit permission words in the **current user turn** (not a prior one):

- `push`
- `push it`
- `git push`
- `send to remote`
- `deploy` (only if context clearly means git push, not app-level deploy)

What does NOT authorize:
- `commit` alone
- `create a PR` — creates the PR remote-side but I still need push first, which needs its own auth
- "we should push after review" — future tense, not now
- Prior turns in the session, no matter how many pushes were done earlier

## Why so strict

- Pushing `dev` fires path-filtered preprod deploys on cidca-platform + cidca-services.
- Pushing tags (`v<X.Y.Z>` or `<service>/v<X.Y.Z>`) fires **prod deploys**.
- Pushing to a PR branch adds commits visible to reviewers; force-push loses reviewer state.
- Pushing to `main` on zotea auto-deploys via Vercel to prod.

Unauthorized push = unauthorized deploy = incident risk.

## Behavior

Before any `git push` call:

1. Scan the current user turn for authorization tokens.
2. If found → proceed. Log to user: `Pushing per current-turn auth: "<quoted word>"`.
3. If NOT found → STOP. Ask: `Ready to push? (say "push" to authorize)`.
4. Never run `git push` from a hook, cron, background task, or auto-retry.
5. Never `git push --force` unless user says "force push" verbatim in the current turn AND you've warned about the consequences.

## Force push additional guards

- Never force-push `main` / `master` / `dev` — even with authorization, block and warn: `Force push to shared branch <name>? Confirm again with "yes force push <name>".`
- Force push to PR branch: allowed with explicit "force push" in the turn, no double confirm needed.

## `--no-verify` guards

- Never use `--no-verify` (skips hooks) unless user says "skip hooks" or "no verify" in the current turn.
- Never use `--no-gpg-sign` or `-c commit.gpgsign=false` unless user says so.

## Recovery

If you accidentally pushed unauthorized:
1. Immediately report it to the user.
2. Do not `git push --force` to "undo" without user confirmation.
3. If it's a `dev` push that triggered preprod deploy, the deploy is already
   running — offer to revert with a follow-up commit rather than force-push
   revision.
