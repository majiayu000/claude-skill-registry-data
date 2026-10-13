---
name: fix-ci
description: Find and fix why a CI run failed on a pull request or on master - lint, types, tests, codegen drift, the PR title, images, charts. Use when checks are red, a workflow run failed, or the user pastes a CI error.
argument-hint: <pr number, run id or branch>
---

# Fix CI

The `ci-triager` agent finds the cause without changing anything; start with it when
the failure isn't obvious.

1. **Find the failure.** `gh pr checks <number>`, or `gh run list --branch <branch>
   --limit 5`. Then `gh run view <id>` for the failing jobs and
   `gh run view <id> --log-failed` for their output. Read from the top of the failing
   step: the first real error, not the cascade after it.
2. **Reproduce it locally** with the command the job runs
   (`.github/workflows/ci.yml`):

   | Job | Locally |
   |---|---|
   | Lint and boundaries | `bun run lint` |
   | Type-check | `bun run check-types` |
   | Unit tests | `bun run test`, `bun test ./scripts/ ./.claude/hooks/` |
   | Components | `bun run --cwd packages/ui test:stories` (`test:visual` needs Docker) |
   | Integration tests | `bun run test:integration`, then `bun run test:coverage` |
   | End-to-end tests | `bun run test:e2e` (stop `bun dev` first) |
   | Python service | `bun run --filter @repo/ai lint`, `check-types`, `test`, `coverage` |
   | Generated code is committed | `bun run gen`, then `git status`: commit what changed |
   | API compatibility | a removed or narrowed field in `apps/api/openapi.json`: make it additive, or mark the title `!` |
   | Pull request title | Conventional Commits with a scope from `commitlint.config.ts`: `printf '%s\n' "<title>" \| bunx commitlint` checks it locally |
   | Migration safety | `bun run db:lint` |
   | Helm charts and GitOps | `bun run charts:check` |
   | OpenTofu | `bun run infra:check` |
   | Container images | `docker buildx bake <image>`; a Trivy finding needs the fixed version, or a reviewed entry in `.trivyignore.yaml` with a reason and expiry |
   | Code generators | `bun scripts/generators.ts` |

   Long ones (`test:integration`, `test:coverage`, `test:e2e`, the generators) run in
   the background.
3. **Passes locally, fails in CI?** CI runs with `.env.example`'s values and its own
   services; a test that depends on your `.env`, on timing, or on test order is the
   usual cause. Check whether `master` fails the same way
   (`gh run list --branch master --workflow ci.yml --limit 3`): then it isn't this change.
4. **Fix the cause** (CLAUDE.md principle 1). Never skip or loosen the check, retry until
   green, or add a suppression. A flaky test is a bug: fix the race or the wait.
5. Push only with the user's approval; CI runs again on the new commit.

## Done when

The command that failed passes locally, and the next CI run on the pull request is
green (`gh pr checks <number>`).
