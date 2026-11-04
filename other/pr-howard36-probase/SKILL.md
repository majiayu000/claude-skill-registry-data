---
name: pr
description: Commit the current changes on a new branch, push, and open a GitHub PR following this repo's conventions.
disable-model-invocation: true
---

Optional PR title or branch hint: $ARGUMENTS

1. Run `/verify` first. Do not open a PR with failing lint, Prettier, or build.
2. If on `main`, create a branch: descriptive kebab-case, no prefix (e.g. `one-time-use-invites`). Derive the name from the change or from the arguments.
3. Review `git status` and `git diff` before staging. Never stage `.env*` files (other than `.env.example`).
4. Commit with a Conventional Commits subject: `<type>: <short imperative description>`, lowercase description (types: `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `ci`). End the message with the Co-Authored-By and Claude-Session trailers the session provides.
5. Push with `git push -u origin <branch>`.
6. Open the PR with `gh pr create`. Title matches the commit subject. Body: what changed and why, in a few sentences. If the PR includes a Prisma migration, say so in the body and note it will apply to production on merge.
7. Reply with the PR URL.

PRs are rebased into `main`, so keep commits clean and self-contained rather than relying on squash.
