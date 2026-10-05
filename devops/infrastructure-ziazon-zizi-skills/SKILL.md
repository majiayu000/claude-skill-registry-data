---
name: infrastructure
description: >
  Use when working on infrastructure or developer-workflow tooling — Nomad, Consul,
  Vault, Terraform, Docker, CI/CD (GitHub Actions), and the CLI/scripts that run a
  codebase (monorepo task runners, env management, setup/dev scripts, a project's own
  ops/deploy CLI, launchd/hooks tooling). Invoke whenever you: edit any file under
  infrastructure/ or a job-spec directory, touch a Dockerfile/workflow/Makefile, debug
  env or direnv/worktree setup, publish workspace libs, or improve the dev lifecycle.
  Do NOT use to merely LOOK UP how to run/build/test a project — that's project-config
  (this skill is for changing/building the tooling, not consulting it); do NOT use for
  third-party SaaS APIs/webhooks/MCP automations — that's integrations; do NOT use
  for app-level logging — that's monitoring.
---

# Infrastructure & Dev Workflow

Goal: handle infrastructure-as-code and the local/CI developer lifecycle the way the user
likes, and accumulate their preferred setups so future work is consistent. Infra changes
have a wide blast radius (one bad job spec takes down a service for everyone), so the
discipline is: learn the layout, mirror conventions, validate before apply.

## Workflow

1. **Read the matching reference file first** — the operating model and its gotchas are
   already recorded; rediscovering them wastes time and risks contradicting a convention.

   | Read this | When working on |
   | --- | --- |
   | [claude-code-tooling.md](claude-code-tooling.md) | Claude Code tooling: slash-command args, launchd jobs, daily-gated hooks, Markdown-embedding-Markdown, Bash-tool node version |

   Add a row per project reference file (local dev/build, the deployed-infra operating
   model, a project's own CLI and release → deploy flow) as work starts in a project.
   This install keeps those rows in `LOCAL.md` beside this skill, when your copy keeps
   one — *Project reference files*.

2. **Learn the layout before adding anything.** Identify the orchestrator (Nomad/k8s),
   service discovery (Consul), secrets (Vault/env), provisioning (Terraform), build/deploy
   (Docker, CI), and the task runner + package manager. Read 1–2 existing job/config
   files and mirror their structure — infra files are copied forward, so one
   off-convention file propagates.

3. **Respect secrets boundaries.** Use the project's mechanism (Vault refs, env, CI
   secrets); never hardcode a secret, and never print one — reference by name, source
   files to load, presence-check only (`[ -n "$VAR" ]`). A value echoed once persists in
   logs and transcripts forever.

4. **Validate before apply — this is a hard gate.** Run the dry-run the tool offers
   (`terraform plan`, `nomad job plan`, `plutil -lint`, workflow lint, `--dry=json`) and
   read its output before any apply/deploy/load. Prefer minimal, reversible changes and
   state the blast radius (which envs/services a change touches) when proposing one.

5. **Prove the change against the real lifecycle.** A tooling/dev-workflow change is
   done when the actual command succeeds from a clean state (fresh worktree, new shell)
   — not when the file looks right. For a dev-server change, restart the server from the
   worktree holding the change; a stale process on the port will happily serve the old
   code and lie to you.

## CI optimization

- **When a pipeline exceeds ~10 min, apply in order:** cache deps → parallelize
  lint/typecheck/test into separate jobs → path filters to skip unrelated jobs →
  matrix-shard the test suite → move slow tests to scheduled runs → larger runners.
  Optimize the pipeline; don't skip gates or disable flaky tests.
- **Feature-flag / kill-switch lifecycle:** create → canary → full rollout → REMOVE the
  flag and its dead code. Set a cleanup date at creation, or the flag becomes permanent
  debt. (An env kill-switch a product ships is no exception — the same lifecycle
  applies: it exists to be turned on, verified, then removed. This install's example is
  in `LOCAL.md` beside this skill, when your copy keeps one — *Kill-switch example*.)

## Merged is not deployed

- **Never infer "deployed" from "merged."** Any templating function that inlines file
  content **client-side at submit time** (Nomad's `file()`, evaluated relative to the CWD
  of whoever ran the deploy) bakes whatever *that checkout* had on disk into the submitted
  job. A merged fix can therefore sit undeployed indefinitely while git history looks
  perfectly correct — a branch cut *before* fix X, deployed, then rebased *onto* X makes X
  an ancestor of the deploy commit, so "is X merged?" answers yes while the cluster still
  runs pre-X content. **Fingerprint:** the deployed task's `Env` matches HEAD while its
  `Templates` predate it — a combination impossible from a single checkout.
- **Diff the deployed artifact rather than reasoning about it** (`nomad job inspect …`).
  Restarting does not help: a stale template means the process re-reads the same stale
  bytes. Fix the submission.
- **Fast-forward the shared checkout after every merge** — a stale `main` is a loaded gun
  for the next person who deploys from it.
- **A manifest version bump does not imply a deploy** either: tooling commonly skips a job
  whose running version already equals the manifest, so a service can be absent from the
  deploy matrix simply because it was already deployed by another route.

## Reading CI and deploy signals

- **Read the matrix, not the conclusion.** A **red** deploy run can mean a completely
  **green** deploy: one release reported `failure` while every real service deployed fine,
  because periodic/batch jobs print no `Evaluation ID` (they are *scheduled*, not
  *deployed*) and the workflow's parser fed that empty value to its wait script. Check
  per-job conclusions and the failing **step** before believing a red run broke anything.
- **A red job silently swallows everything that `needs:` it.** That same run skipped the
  release announcement — the change shipped to production and nobody was told. When a
  deploy run is red, ask what *else* didn't fire; a cosmetic CI bug can have a real
  communication blast radius.
- **When a guard fires, the bug is usually upstream of the guard.** The tempting fix was
  to let the verification script tolerate an empty id — which would have converted a
  red-but-harmless CI bug into the **silent loss of prod rollout verification**, the one
  job that script exists to do. Fix the caller that produced the bad value, never the
  assertion that caught it.
- **"Skip when the value is missing" is weaker than "skip when we know WHY it's
  missing."** Resolve the actual case and **fail loudly** for the case that should never
  be empty; otherwise the guard silently stops covering a real service the day the CLI's
  output format changes.
- **Check the real specs before trusting a category name.** Eight failing jobs were all
  described as "periodic"; two had no `periodic` stanza at all and were `type=batch`, so a
  periodic-only guard would have missed them.
- **A skipped GitHub Actions job is not recoverable by re-running.** Re-runs use the
  workflow file from the **original commit**, so a fix merged to main does not apply — and
  a fresh dispatch afterwards can yield an empty matrix, skipping the job and everything
  depending on it. Plan to redo the missed side effect by hand.
- **Say when a CI change is unverifiable at merge time.** With no rehearsal environment,
  green CI proves nothing about the fix — state that in the PR instead of implying
  otherwise. You can still test the logic: **re-implement the step's shell in a local
  harness** and drive it across every branch with synthetic inputs.

## When config is present but has no effect

- **Suspect SCHEMA or NESTING before lifecycle.** A daemon that silently ignores unknown
  keys makes a *misplaced* block indistinguishable from a *missing* one — one such block
  sat in the wrong nesting level for three years. Two confident hypotheses ("the
  provisioner never ran", "the agent needs a restart") were both wrong and both
  disprovable in minutes. Check the vendor's own example for exact nesting; don't trust
  that it looks reasonable.
- **`mtime` vs the service's `ActiveEnterTimestamp` is a ten-second test** that settles
  "was it applied?" versus "was it loaded?" — run it before theorising.
- **The driver's own error message is the best diagnostic.** A throwaway job that *tries*
  the thing ("volumes are not enabled; cannot mount host paths") beat every
  attribute-inspection attempt. Absence of a fingerprint attribute is easy to misread; the
  error is unambiguous.
- **Prove a fleet fix with a controlled comparison** — fix ONE node and show it reports
  the new attribute while the others still don't. Worth more than any argument.
- **A rolling agent restart can be non-disruptive — prove it, don't assert it.** Canary
  the lowest-alloc node, gate the roll on the agent returning, and compare alloc counts
  before and after.

## Common failure modes

- **Applying without planning** — Terraform/Nomad changes reviewed only by eye. The plan
  output IS the review; skipping it turns a typo into an outage.
- **Editing a workspace lib and expecting consumers to see it** — when a monorepo's
  consumers pin exact PUBLISHED versions of its scoped packages, a `libs/*` edit is
  invisible until published + bumped (never rsync `dist/` into node_modules). This
  install's original wording is in `LOCAL.md` beside this skill, when your copy keeps
  one — *Workspace lib publishing*.
- **Trusting a green check from the wrong environment:** a `zsh -lic` node-version probe
  doesn't reflect the Bash tool's snapshot; a server on the right port may be a stale
  process from another worktree. Verify in the environment that actually runs the thing.
- **Hardcoding what the stack derives:** ports, tokens, service addresses — Consul/Vault/
  env own these; a literal value works locally and breaks deployed.
- **Missing per-package framework deps in the monorepo:** a Nest service that doesn't
  declare `@nestjs/core` resolves a hoisted, mismatched version → runtime DI failures.
- **Breaking the host from an automation:** hooks/scheduled jobs must catch everything,
  exit 0, run detached, and log to a file — a crashing hook takes the session down with it.
- **Treating a major version bump as a tag bump.** A "v2" can be a different product with
  a different image, different config format, and no migration path — one such upgrade had
  **no default config inside the container** (silently falling back to in-memory storage,
  the exact failure being migrated away from), an `ephemeral: true` default that silently
  ignored the configured directories, and a relocated health-check endpoint that made the
  job flap forever. Read the new version's source or docs for defaults before planning the
  change, and check early whether ports/clients are unaffected — that one question turned a
  scary migration into a one-file change.
- **Promoting a high-cardinality identifier to a log/metric label.** The label an
  orchestrator gives you *for free* is often exactly the one you must never use — an
  allocation id changes every alloc and every deploy, i.e. the canonical cardinality
  explosion. Verify which labels are actually emitted by default rather than assuming the
  useful ones are.
- **Running a non-root container against a host bind mount without planning ownership** —
  you cannot `chown` a mount root, so mount the **parent** and write to a subdirectory.

## Before you call this done

- [ ] Read the relevant reference file; change mirrors existing conventions.
- [ ] No secret hardcoded, printed, or partially revealed anywhere.
- [ ] Dry-run/plan/lint executed and its output reviewed before apply.
- [ ] Blast radius stated (envs/services affected); change is minimal and reversible.
- [ ] Verified from a clean state in the environment that actually runs it.
- [ ] New setups/gotchas recorded per the protocol below.

## Related skills

- [security-and-hardening](../security-and-hardening/SKILL.md): what CI, container and secrets changes must guarantee, and where each control fires.

## Capturing learnings (session-handoff protocol)

Accumulate the user's infra preferences and dev-workflow knowledge in `LEARNINGS.md`
beside this skill, when your copy keeps one, which is a slim index over the topic
reference files above.
On handoff / "update skills" / after infra or tooling work: record the stack, conventions,
gotchas, and useful commands/scripts — append under a new `##` section in the most relevant
topic file (not the index), deduped and tagged by project. If a topic file outgrows ~250
lines, split it further (this install's split rule: `LOCAL.md` beside this skill, when
your copy keeps one — *Splitting a topic file*). Read the relevant
file(s) before infra/tooling work.
