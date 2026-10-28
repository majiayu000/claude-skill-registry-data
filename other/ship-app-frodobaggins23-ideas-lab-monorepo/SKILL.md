---
name: ship-app
description: Ship an app in this lab repo - branch, commit, push, draft pull request, Vercel project and preview URL. Use after verify-app passes, or to push follow-up changes to an existing app PR.
---

# ship-app

Input: `appName`. Rules for what the agent may do on its own are in the root `CLAUDE.md`
("Git and pull requests"). Never commit to `main`, force-push, skip hooks, merge or delete branches.

1. **Branch:** `feat/<appName>` for a new app, `fix/<appName>-<topic>` for later changes. Reuse the
   existing branch if it already exists.
2. **Commit:** one logical change per commit, Conventional Commits, English. Let the hooks run; if
   one fails, fix the cause.
3. **Vercel project** (first ship only, before the first push: Vercel deploys only pushes made
   after the project exists): `npm run lab:vercel-project -- <appName>`. It is idempotent. Any
   other Vercel operation is the user's to run outside the sandbox: tell them the command.
4. **Push** with `npm run lab:push`, never `git push`, which cannot authenticate from the sandbox
   (see "Pushing from the sandbox" in `docs/agentSetup/claude/README.md`). It runs the pre-push
   tests, then pushes the current branch. If it refuses (not a fast-forward, missing `main`
   head, signed commit), report its message to the user; do not try another way to push.
   Then open a **draft** PR with `gh pr create --draft` (or update the existing PR).
   Body: the idea, preview URL (fill in below), checks run with results, Assumptions, new
   dependencies added through `lab:add` (and any package the user installed themselves after a
   failed check, with the failed check), open questions.
5. **Preview URL:** `npm run lab:deployment -- <appName>` (run it in the background; it waits up
   to 15 minutes) waits for the deployment of the pushed commit and prints `READY <url>`. On
   `ERROR` it prints the build log: fix the cause and push again. `CANCELED` means Vercel skipped
   the build because nothing in the app changed. `NO_DEPLOYMENT` means the branch has no
   deployment at all, usually because the push came before the project existed: run step 3 and
   push again. Add the URL to the PR.
   To see what Vercel did (any state, any commit), run `npm run lab:vercel-status -- <appName>`.
   Do not query the Vercel API by hand.
6. Run `inspect-app` against the preview URL. Report the PR link, the preview URL and what was not
   verified.
