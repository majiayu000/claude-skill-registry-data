---
name: verify
description: Prove a change works before calling it done, by running every check that applies to what changed and reporting the real output. Use after implementing a feature or fix, before opening a PR, or when the user asks to test everything. Runs in the verifier agent.
context: fork
agent: verifier
background: false
---

# Verify a change

This is the one list of checks; the verifier agent runs it, and CI runs the same
commands. The Stop hook already runs the fast ones on changed files at the end of each
turn, with the unit coverage of the changed lines, but not the boundary checks, the full
coverage, integration or e2e tests.

## What changed

`git status --short`, `git diff master...HEAD --stat` and `git diff --stat` (uncommitted
work counts). Map each file to its package (`apps/<name>`, `packages/<name>`) and pick
the checks below.

## Always, in this order

1. `bun run lint`: Biome, the dependency and render-only boundaries, knip, the
   `ponytail:` marker check, and ruff for `apps/ai`.
2. `bun run check-types`: every package, `scripts/` and `.claude/hooks/`.
3. `bun run test`: unit tests, cached per package (Jest in `apps/mobile`, pytest in
   `apps/ai`).
4. `bun test ./scripts/ ./.claude/hooks/`: the repo scripts' and hooks' own tests, which
   turbo doesn't run.

Judge each command by its exit code, never by grepping its output: tsc and several other
tools colour their output, so a search for "error TS" can miss real errors.

## By what changed

| Changed | Also run |
|---|---|
| `packages/contracts`, `packages/jobs`, the Prisma schema, `apps/ai` routes or models | `bun run gen`, then `git status --short`: the regenerated files must be part of the change (CI's codegen job fails otherwise). It only rewrites generated files |
| `packages/db`, any service's code, queues, auth, email, webhooks, HTTP | `bun run test:integration` (starts the full Docker profile; needs about 3.9 GB free in Docker) |
| Any source file | `bun run test:coverage`: every suite, merged, with every file at 100%. It names each line, branch or function no test reaches |
| `packages/db/prisma/migrations` | `bun run db:lint` and `bun run --filter @repo/db drift` |
| `packages/ui` components | `bun run --cwd packages/ui test:stories` (and `test:visual`, which needs Docker) |
| `apps/web` or `apps/mobile` user flows | `bun run test:e2e --app web` or `--app mobile` (needs the full profile and nothing listening on the stack's ports: stop `bun dev` first, or say it wasn't run) |
| `apps/web` pages or dependencies | after e2e's build, `bun run --cwd apps/web budget` |
| `apps/ai` prompts, retrieval or models | `bun run --cwd apps/ai evals` |
| `turbo/generators` | `bun scripts/generators.ts` (runs each generator in a scratch worktree, then lint, types and tests on its output) |
| `deploy/` | `bun run charts:check` (needs helm and helm-unittest; also checks every file in the secrets directories is encrypted) |
| `infra/tofu` | `bun run infra:check` (needs tofu) |
| Anything staged for a commit | `bun scripts/secret-scan.ts` (gitleaks on the staged changes). With nothing staged, say it wasn't run: the pre-commit hook runs it |

## Long-running commands

`test:integration`, `test:coverage`, `test:e2e`, `bun scripts/generators.ts` and
`charts:check` take longer than the Bash tool's default two minutes. Start them with the
Bash tool's `run_in_background` and wait for them to finish; never cut one short, and
never report one as passed before it has exited 0. The same goes for `bun dev`, which
never exits: in the background, or not at all.

## Rules

- Never edit files, commit, push, read `.env`, or run `docker compose down`,
  `bun run db:reset` or `bun run docker:clean`. `bun run gen` is the one command allowed
  to change files, and only generated ones.
- If a command needs a tool or service that's missing, don't work around it: report it
  as not run, with the error and the fix `bun run doctor` suggests.
- Run each command once. If it fails, read the failure and say whether the change
  caused it (reason from the diff and the output; `git stash` isn't allowed).

## Report

A table, one row per command: `| command | pass / fail / not run | duration |`. Then,
for each failure, the command and the relevant part of its output, verbatim and trimmed
(the failing test names and assertions, the first type errors), and whether it looks
caused by the change or pre-existing, and why. Never write "all checks pass" unless every
row says pass.
