---
name: dont-break-it
description: Your agent changes code in small, additive, checked commits that never skip hooks and never block on long jobs. Use before editing code, running checks, committing or pushing in any repo, or when you say "change code safely", "commit this properly", "small commits" or "follow the engineering rules".
---

# Engineering

1. **Follow the project's contract.** Find its engineering rules first: the agent instructions at the repo root
   (`AGENTS.md`, `CLAUDE.md` or similar), a `CONTRIBUTING.md`, or an engineering contract the instructions point
   to. Changes are additive. No unrelated refactors. Ask the user before adding a new abstraction, schema or
   migration.
2. **Code first, check once.** Finish the change and review the diff. Then run typecheck, lint and the tests that
   touch the changed files once, in the background. Take the real commands from the package scripts or CI config,
   not from memory. Don't chase optional dashboard tools (code-quality bots and the like) unless the project gates
   on them.
3. **Small commits.** One change per commit. Stage named files only, never `git add -A` or `git add .`. Use the
   project's branch naming (for example git-flow `feature/...`), and the same branch name in every repo the change
   spans.
4. **Push with hooks.** Never `--no-verify`. If the repo uses submodules and you committed inside one, commit the
   new submodule pointer in the parent repo too and push both, submodule first.
5. **No worktrees unless asked.** If the user asks for one, run `lean-worktree.sh <dir>` from the
   `be-my-cto` skill folder before installing dependencies, so the worktree shares `node_modules` with the
   main checkout.
6. **Never wait.** Long jobs (builds, full test runs, installs) run in the background. Carry on and resume when
   they finish.
