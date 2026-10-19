---
name: paas-cli
description: Command-line workflows for PaaS platforms — project management, deploys, logs, and automation — vendor-neutral patterns.
category: railway
---

## Overview

Every PaaS ships a CLI for what the dashboard does slowly: deploying,
tailing logs, managing env vars, running one-off commands, and scripting it
all in CI. CLI fluency turns platform operations from clicking into
repeatable, automatable workflows. This skill covers the universal CLI
patterns across providers.

## When to use

- Deploying, rolling back, or promoting releases from the terminal
- Tailing and searching logs without the dashboard
- Managing environment variables and secrets via CLI
- Running one-off commands (migrations, consoles, data fixes) in production
- Scripting platform operations in CI/CD pipelines

## Core concepts

**The CLI mirrors the platform model.** Projects → environments → services
is the common shape; learn your provider's nouns once (`apps`, `services`,
`deployments`) and every command follows. `--help` at each level is the real
documentation — CLIs are self-describing if you ask.

**Authenticate safely in automation.** Interactive login for humans; API
tokens for CI (scoped minimally, stored as CI secrets, rotated periodically).
Never paste tokens into chat logs or commit them; prefer the CLI's
non-interactive auth flags in scripts.

**Logs are a stream, not a file.** `logs --tail` follows live output;
filters by service and time range narrow it down. For anything beyond
eyeballing, drain logs to an aggregator — CLIs show recent history, not
durable searchable archives.

**One-off commands run in the deployed environment.** The equivalent of
"SSH in and run a command": migrations, Rails/Django consoles, data
backfills. They run against production config and data — which is the point
and the danger. Prefer non-interactive, logged, reviewable commands over
interactive shells for anything consequential.

**Script the repetitive.** Env var syncing across environments, deploy +
migrate sequences, backup triggers — if you type it twice, script it. CLI
commands compose in shell scripts and CI jobs; the dashboard doesn't.

## Practical workflow

1. **Install and authenticate** per provider docs; verify with a read-only
   command (list projects) before doing anything mutating.
2. **Learn the core verbs:** deploy, logs (tail/follow), env (list/set/
   unset), run (one-off command), status/ps (what's running), rollback/
   redeploy, domains, and backups — in that order of daily usefulness.
3. **Set up shell conveniences:** project/env context switching, aliases for
   common log tails, and completion.
4. **Wire CI:** token auth, deploy on merge to main, run migrations as a
   distinct step with failure handling, post deploy URLs/status to the PR.
5. **Document team runbooks** as CLI command sequences (copy-paste ready)
   rather than dashboard click-paths — they survive UI redesigns and work
   identically for everyone.
6. **Audit periodically:** who has tokens, what automation exists, and
   whether scripts still match current CLI versions (CLIs evolve; pin or
   test in CI).

## Common pitfalls

- **Running one-off commands against the wrong environment** — prod vs
  staging mix-ups are the classic CLI disaster; make the current context
  visible (prompt integration, explicit `--env` flags, confirmation for
  prod).
- **Tokens with excessive scope** committed to CI — least privilege, and
  rotate on personnel changes.
- **Interactive commands in CI** — hanging pipelines waiting for a prompt
  that never comes; use `--yes`/non-interactive flags everywhere in
  automation.
- **Assuming CLI output is stable** for scripting — human-readable output
  changes; prefer `--json`/`--format json` and parse that.
- **No local parity** — debugging "works on my machine" without reproducing
  the platform environment; use the CLI's local/dev emulation where offered.
- **Forgetting the CLI in incident response** — dashboard is slow under
  pressure; the fastest rollback path should be a practiced CLI command.
