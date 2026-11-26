---
name: ci-conventions
description: "Rules for an agent running inside CI with no human in the loop, and for naming and shaping workflow files, including OpenTofu plan and apply pipelines across several modules. Use when the session runs non interactively in a workflow, or when naming, reviewing or setting up a workflow file."
disallowed-tools: AskUserQuestion
---

# CI conventions

Behaviour when nobody is there to answer a question, and how workflow files are named and
shaped.

## When to use

- The session runs in a GitHub Actions workflow or any other non interactive runner.
- A workflow asks for a review, a fix or an implementation.

## Rules

- `CI=true` means unattended. Never ask an interactive question. Record the question on
  the issue or in the output and stop that task instead.
- Use the CI settings profile: read only shell plus `gh pr view`, `gh pr diff`,
  `gh pr checks`, `gh pr review`, `gh pr comment`, `gh issue comment`.
- Stay inside the triggering context: the pull request, the issue, the branch. Do not
  touch unrelated files.
- Never push to any branch, never force push, never rewrite history, never delete a
  branch, never merge a pull request.
- Never create or change a release, a tag or a deployment, and never run `tofu apply`,
  `helm upgrade`, `kubectl apply` or anything touching live infrastructure.
- Secrets stay in the runner environment, provided by the workflow. Never echo them,
  never write them into a comment, a file or a log.
- Do not install tooling the workflow did not provide. Report the missing tool instead.
- Bound the run: a fixed step budget and a timeout from the workflow, not an open loop.
- Stop and report instead of guessing when the task is underspecified.
- Output is structured and short: what was done, what was found, what is open, what a
  human must decide. State what was not verified or could not be executed.
- Post findings as a review comment or an issue comment, matching what the workflow
  triggered. Never as a commit message or a file in the repository.

## Workflow files

- Name the file after what it does: `lint.yaml`, `test.yaml`, `release.yaml`, `plan.yaml`,
  `apply.yaml`. Never `ci.yaml` or `main.yaml`.
- One concern per file. A workflow that lints stays separate from one that deploys.
- One job per check: `fmt`, `lint`, `test` and `validate` run as separate jobs, never bundled
  into a single job that calls an umbrella task. A failing job names the check that failed.
  Everything that can run in CI runs in CI.
- A matrix runs the same check over several targets, for example several chart or Kubernetes
  versions, instead of a repeated job for each one.
- Every workflow sets its own `permissions` block, scoped to what its jobs need. None relies on
  the repository default.
- Every action is pinned to a commit digest: `uses: owner/action@<commit sha> # v<tag>`. The
  digest is what runs, the tag comment is for readers, and Renovate keeps both updated.
- Workflow files end in `.yaml`.

## OpenTofu

- A detect job checks out with history (`fetch-depth: 0`), diffs the pull request against
  the merge base of the base branch, or the push against the commit before the push
  (`github.event.before`), and lists every root module whose files changed. A changed
  shared module, or a file every root module reads, maps to every root module that
  references it. Every later job reads that list, none recomputes it.
- The plan and apply jobs run only when the detect job's module list is not empty, guarded
  by an `if` on that output. Neither runs with an empty matrix: a pull request or push
  that touches no module stays green.
- A matrix plan job runs one `tofu plan` per changed module on a pull request from a
  branch of the repository. A fork pull request gets a read only token and no secrets, so
  its plan job does not run. Each matrix cell posts or updates one sticky comment for its
  own module, the marker carries the module path so cells never overwrite each other's
  comment, with the plan grouped by create, update, replace, destroy and import.
- No plan artifact. A plan file holds every value in clear, secrets included, so it is
  never uploaded anywhere. The pull request plan is review input only.
- On merge to the default branch a matrix apply job runs one `tofu plan` followed by
  `tofu apply` of that plan, in the same job, per module that was touched, same module
  list, same grouping in the job summary.
- One job per check: `fmt`, `validate`, `tflint`, `trivy config`, `test`, `plan`, `apply`.
  `tflint` and `trivy config` both check the same written code but run as separate jobs,
  one scanner per job. The apply job is the one exception that runs two commands: its
  plan is the input of its apply, not a check of its own.
- `tofu test` is its own job, on the pull request and on the push to the default branch.
  Mock providers on a pull request by default. A real provider test runs only in a
  dedicated test workspace the repository names in its `AGENTS.md`, never against
  resources that exist for another purpose.
- `validate` and a mock provider `test` need no backend: `tofu init -backend=false`.
  `tflint` needs `tflint --init`, `fmt` and `trivy config` need no init at all. `plan`,
  `apply` and a real provider `test` need the backend and its credentials.
- Concurrency is set at workflow level, not per job. One group per pull request for the
  plan workflow, `cancel-in-progress` true. One group per default branch for the apply
  workflow, `cancel-in-progress` false: an apply never gets cancelled halfway through.
- No allowlist of modules or directories. Every root module the diff touches is in scope.
- No manual trigger. `pull_request` and `push` to the default branch are the only events.
- The Rules above bind an agent running inside CI, not the workflow's own jobs. The apply
  job is the pipeline's gate: the merge is the approval, so it runs `tofu apply` where no
  agent session may.

## Guardrails

- No interactive prompts used anywhere in the run.
- Scope limited to the triggering pull request, issue or branch.
- No push, merge, release, tag, deploy or infrastructure change.
- Secrets never echoed, logged or persisted.
- Output structured, open questions listed, limits of the run stated.

## References

- `ci-review` for the review output format, including how to read a sticky plan comment.
- `tofu-plan` and `opentofu-conventions` for the plan and apply rules this pipeline enforces.
- `repo-conventions` for where a workflow file sits among a repository's required files.
- `release-conventions` for the Renovate rules that keep a pinned action current.
