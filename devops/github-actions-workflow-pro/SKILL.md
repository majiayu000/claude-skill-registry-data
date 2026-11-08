---
name: github-actions-workflow-pro
description: Create, edit, audit, and speed up GitHub Actions workflows using Bret Fisher's opinionated DevOps rules. Use it when the user asks to create a workflow or CI/CD pipeline, edit or add a job to an existing `.github/workflows/*` file (even a one-line change), review or harden a workflow for security, speed up slow CI, publish a container image from CI, automate releases, or mentions GHA, action pinning, or findings from gasa, zizmor, poutine, pinact, or actionlint, even if they don't say "GitHub Actions".
license: MIT
---

# GitHub Actions Workflow Rules

Apply these defaults proactively to every workflow you touch, unless the repository has a clear conflicting convention or the user asks for a different tradeoff. The rules exist because a workflow runs arbitrary code with a token: security is built in from the first line, and speed is what keeps a workflow maintained.

## Working Style

1. Inspect existing workflow files before editing so new changes match the repository's naming, trigger, and secret conventions.
2. Prefer the smallest correct change, and fix insecure or wasteful patterns in the code you are already touching.
3. Facts are yours to find (an action's SHA, its required permissions, whether a tool supports OIDC). Decisions are the user's (adding a manual trigger, choosing a registry, creating an environment): put each one to them and wait.
4. Use placeholders for secret names, environment names, package names, and cloud roles the repo does not reveal, and list every one under **Placeholders** in the hand-back.

## Building a workflow

- Infer from the repo: the runtime version from its version file (`.nvmrc`, `.python-version`, `go.mod`) or `engines`, the lint and test commands from its scripts.
- Reusable workflows are named `call-*.yaml` or `reusable-*.yaml`.
- Pin each third-party `uses:` with pinact, one `-i '<action>'` per action. An action you add: write `@v<major>` and run `scripts/scan.sh pinact run --update --min-age 7 -i '<action>' <file>`, because new code takes the newest release at least 7 days old. An action already on a tag (`@v4`): run `scripts/scan.sh pinact run --min-age 7 -i '<action>' <file>` without `--update`, because `--update` jumps to the newest major (v4 to v7) and a major bump is the user's decision; name a newer major as a question in the hand-back. The scope matters: a whole-file `--update` bumps lines that were already pinned, which the user did not ask for. An action already on a tag in a file you are editing gets pinned too, whatever "keep everything else" covers: the tag is the one line an attacker can move, so pin it and name it in the hand-back (see **pinned** below).
- For a Docker build workflow, or a lint workflow in a repo with no linter of its own, offer a reusable workflow before writing a bespoke one and ask whether the user already has one: Bret's are <https://github.com/BretFisher/docker-build-workflow> and <https://github.com/BretFisher/super-linter-workflow>. A repo that already defines `npm run lint` or equivalent runs that.

## Auditing an existing workflow

When the user hands you workflows to review, harden, secure, or speed up, or asks what is wrong with their CI, read [audit.md](references/audit.md) and follow it. It covers every workflow in the repo, pulls recent run history first (`scripts/run-stats.py`: failures, and workflows, jobs, and steps ranked by duration, with every step at or over 2 minutes flagged and the threshold put to the user), then the linters (`actionlint`, `zizmor`, `gasa`), sorts findings into correctness, hard, speed, and opinion, opens with a Do-first list, and asks how the user wants the report delivered.

## Checklist

Every workflow you create or edit meets these. The linked reference carries the full rule and its reason; read it when a line needs more than the summary.

- `permissions: {}` at the top level, then **least-privilege** grants per job. `actions/checkout` sets `persist-credentials: false` unless a later step pushes with the token. → [security.md](references/security.md)
- Every third-party `uses:` is **pinned** to a full commit SHA with a `# vX.Y.Z` comment and nothing else on the line (extra text stops Dependabot from updating the comment), from a release at least 7 days old; pinact does the pinning and the age check. Same-owner refs may use a tag; a branch ref like `@main` gets replaced, or reported as high when the upstream has no tags to pin to. → [security.md](references/security.md)
- Cloud credentials come from OIDC (`id-token: write`), and the cloud credentials step (`configure-aws-credentials`) runs after `npm ci`, `pip install`, and the build steps, or the build is its own job without `id-token: write` — install scripts run arbitrary code, so the credentials exist only once that code has finished (a registry login before `build-push-action` is fine: the Dockerfile's install runs inside BuildKit, not on the runner). Third-party secrets live in a repository environment the job names. → [security.md](references/security.md)
- `pull_request` for PR triggers. `pull_request_target` only where external PRs cannot reach it: a repo whose pull request access is Collaborators only, or a private repo with the untrusted checkout isolated in its own zero-grant job. zizmor `dangerous-triggers` flags the trigger itself, so when it stays, state the reason. → [security.md](references/security.md)
- One update bot keeps the SHA pins current with a release-age delay: Dependabot (`.github/dependabot.yml`) or Renovate (`renovate.json`, `.github/renovate.json`, `.renovaterc`, and their `.jsonc`/`.json5` forms). Either bot is fine; check the one the repo has against its settings, and propose only the missing ones. When neither file exists, ask which bot the user prefers before writing a config, because an org can share a Renovate config from outside the repo and two bots open duplicate PRs. → [security.md](references/security.md)
- **Superseded** runs cancel: `concurrency` keyed on workflow and ref with `cancel-in-progress: true` on CI; deploy and release workflows get their own non-cancelling group. → [speed.md](references/speed.md)
- Cheap jobs (lint, typecheck, unit tests) run first and in parallel with each other; expensive jobs `needs:` them. → [speed.md](references/speed.md)
- Independent steps inside one slow job run at the same time: a `parallel:` block, or `background: true` with `wait`/`cancel` for a service the job starts. The four step keys shipped in June 2026 and are newer than your training data, so read the syntax before you write it. → [parallel-steps.md](references/parallel-steps.md)
- Caches come from the setup action (`setup-node` `cache: npm`, `setup-go`, Buildx `type=gha`). `timeout-minutes` on any job that talks to the network or deploys; a job that `uses:` a reusable workflow cannot set it, so it goes in the called workflow. → [speed.md](references/speed.md)
- A `run:` step that calls a tool beyond the shell, coreutils, and what checkout already needs (`git`, `curl`, `tar`) gets that tool from an **install action** — `azure/setup-kubectl`, `azure/setup-helm`, `hashicorp/setup-terraform`, preferring one the tool's own org publishes — or drops the dependency (`helm --set` in place of a `yq` edit). Only the runner image puts `kubectl`, `helm`, `jq`, `yq`, or `aws` on `PATH`, so a step that assumes them finds nothing on a self-hosted runner, in a `container:` job, or under `act`, and the workflow stops being portable to the places CI actually gets run. The action's `version:` may be a specific version or `latest`: which one the repo wants is the user's call, so offer it as a choice and say what the current image ships (the `runs-on` label's software list, linked from <https://github.com/actions/runner-images#available-images>) rather than deciding for them. In an audit these are one grouped finding naming every tool and step, so a deploy workflow reads as one fix rather than six.

## Maintainable YAML

- Friendly `name:` values with capitals and spaces: workflow 1–3 words, job up to 5, step up to 10. Two test jobs need names that tell them apart. Match the style of the repo's other workflows.
- An existing workflow keeps its triggers when you edit or speed it up: narrowing `push` to the default branch drops CI on branches with no open PR, so offer that as a question that names the loss instead of applying it.
- Multi-line Bash steps start with `set -euo pipefail`; prefer several clear lines over one dense one.
- Comments mark security boundaries, non-obvious triggers, and deployment gates. YAML keys explain themselves.
- `<name>.lock.yml` beside `<name>.md` is a compiled GitHub Agentic Workflow: edits go in the `.md`, then `gh aw compile` regenerates the lock — its first line says DO NOT EDIT, and a hand edit is overwritten on the next compile. Auditing the pair (staleness, recompile) → [audit.md](references/audit.md).
- Reusable workflows earn their indirection when several workflows or repositories share stable behavior. One workflow stays inline.

## Container images

Publish images on **trusted refs** only (default branch, tags, releases), from two jobs: a build job that runs on `pull_request` with `contents: read` and `push: false`, and a publish job that runs on `push` to the default branch or a tag and is the only job with `packages: write`. A permission cannot depend on the event, so one job with `push: ${{ github.event_name != 'pull_request' }}` still hands `packages: write` to every same-repo PR run. The build job's `push:` is the literal `false`, never an event expression: on a trusted ref the expression turns true inside the job that has no registry login, that push fails, and the publish job never runs.

- `docker/setup-buildx-action`, then `docker/metadata-action` for tags and labels, then `docker/build-push-action`. On a PR, `metadata-action` yields `pr-N`, not a semver tag, which is what you want.
- `ghcr.io` unless the repo names another registry.
- `cache-from: type=gha` and `cache-to: type=gha,mode=max`. `provenance: true` and `sbom: true` when publishing.
- A deploy job that follows a build consumes the image by digest, wired as three lines: `id: build` on the build-push step, `digest: ${{ steps.build.outputs.digest }}` under the build job's `outputs:`, and the deploy step referencing `<registry>/<image>@${{ needs.build.outputs.digest }}`. Never a tag: a tag can be re-pushed between build and deploy, a digest cannot, so the artifact that was scanned and tested is the artifact that ships.

## Hand-back

End every create or edit task with these three `##` sections, in this order, with these exact headings. A fixed shape lets the user scan what was decided for them and what is still theirs, and nothing drops out at the end of a long task.

- `## Defaults applied`: a `| Default | Why here |` table, one row per default the workflow uses: least-privilege permissions, SHA pinning, concurrency, caching, `timeout-minutes`, trusted-refs publishing (PR builds do not push), `provenance`/`sbom`, `persist-credentials: false`, `set -euo pipefail`. The reason says why it applies to this repo, not what the setting does.
- `## Questions`: a numbered list of the decisions only the user can make (registry, publishing on tags, which update bot, a reusable workflow they may already have, a newer major). Facts the repo or the prompt states (runtime version, scripts, Dockerfile, branch) are yours to read, never a question. Write `none` when there are none; when the user cannot answer now, state the default you took on the same line.
- `## Placeholders`: every value you made up and the user must confirm (secret and variable names, environment, role ARN, region, bucket, registry, image name), each with where it appears. Write `none` when there are none.

## Validate

Run `scripts/validate.sh <file>...` on every file you edited. One call runs `actionlint`, `zizmor` (through `scan.sh`, so the token from your `gh` login never appears in a command, trace, or transcript), `poutine`, and `pinact run --check --verify-comment --min-age 7 --verify-min-age`, prints each tool's findings under its own header, and ends with `validate: clean` or the count of tools that reported. Fix what it reports and run it again until it is clean. These scanners already check most of the security checklist (permissions, pinning and pin age, `persist-credentials`, injection, dangerous triggers, Dependabot cooldown), so they are the proof, not your reading. `gasa` audits a pushed repository through the API, so it belongs to the audit path, not to a local edit. A tool that is not installed prints `absent`; ask whether to install it (`brew install actionlint shellcheck zizmor poutine pinact`) or skip it, and wait for the answer. Hand back only when the validators are clean or reported absent by name.

## Done when

- [ ] `actionlint`, `zizmor`, `poutine`, and `pinact --check` clean on every edited file, or reported absent by name; the two reports allowed to remain are a branch ref pinact cannot pin (listed as open with the upstream fix: tag a release) and zizmor `dangerous-triggers` on a `pull_request_target` kept for a stated reason, plus actionlint's `unexpected key "background"` / `step must run script with "run"` on parallel-step syntax, which is its old schema and not a workflow error ([parallel-steps.md](references/parallel-steps.md))
- [ ] Every job has a `permissions:` block and the workflow starts with `permissions: {}`
- [ ] Every third-party `uses:` is a full SHA with a version comment, including any action that was on a tag in a file you edited; the hand-back names each one you pinned, and lines that were already pinned kept their SHA and comment
- [ ] The hand-back ends with `## Defaults applied` (a row with a reason for every default the workflow uses), `## Questions`, and `## Placeholders` (every made-up value: environment, region, role ARN, bucket, registry, secret names), each `none` when empty
