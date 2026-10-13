---
name: open-pr
description: Get a change ready for review and open its pull request, or review someone's pull request, with the repo's reviewer agents. Use when the user asks to open, prepare or review a PR.
argument-hint: <pr number to review, or nothing to open one>
disable-model-invocation: true
---

# Open or review a pull request

## Before opening one

1. **Branch.** Not `master`: `<type>/<what>` (`feat/todo-sharing`, `fix/draft-reload`).
2. **Verify.** The verify skill, with every row passing, and its report kept for the
   description.
3. **Review.** Run the agents that apply, and fix what they report:
   - always `reviewer`;
   - `security-reviewer` for auth, procedures, webhooks, uploads, secrets, anything that
     fetches a URL, or a new provider;
   - `migration-reviewer` for anything under `packages/db/prisma`;
   - `python-reviewer` for `apps/ai`;
   - `frontend-reviewer` and `i18n-checker` for `apps/web`, `apps/mobile`, `packages/ui`
     or new copy;
   - `docs-sync` when variables, ports, commands, seams or skills changed.
4. **Title.** It becomes the squashed commit and the release notes: Conventional
   Commits with a scope from `commitlint.config.ts`, in plain words, e.g.
   `feat(api): let members share a todo`. `!` before the colon for a breaking API change.
5. **Description.** What changed and why, in plain prose; how it was checked (the verify
   report); anything not tested automatically and how it was checked by hand.

## Opening it

Only with the user's go-ahead: pushing and opening a pull request act on GitHub as
them. `git push -u origin <branch>`, then `gh pr create --title "<title>" --body-file
<file>`. Then watch the checks (`gh pr checks <number>`); a red one is the fix-ci skill.

## Reviewing one

1. `gh pr view <number>`, `gh pr checks <number>`, and `gh pr view <number> --json files`
   for what it touches.
2. Check it out locally (`gh pr checkout <number>`, with the user's go-ahead) and run the
   same agents as above; the diff is against `master`.
3. Report findings in order of severity with the file and line. Post comments on GitHub
   only if the user asks.

## Done when

The verify report is all passes, every applicable agent reports nothing blocking, and the
pull request's checks are green.
