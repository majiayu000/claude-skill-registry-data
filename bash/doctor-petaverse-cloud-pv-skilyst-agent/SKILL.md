---
name: doctor
description: One-shot environment self-check for the Skilyst agent — credentials present, installed skills intact, platform reachable, required nodes registered, and which scopes the restricted key actually has. Use as the FIRST command of any session or troubleshooting thread, before submitting a paid job; the output says exactly what to fix.
license: MIT
compatibility: Requires the skilyst runtime (>=0.1.0) on PATH or via SKILYST_BIN, a credential env file (default ~/.skilyst/env), and network access to the skilyst API host declared in permission.egress. Runs a POSIX shell script from scripts/.
metadata:
  skilyst.skill_id: skilyst/doctor
  skilyst.version: "1.1.0"
---

# Environment self-check (run this first)

## When to use

At the start of a session, before the first paid job, and whenever something
fails unexplained. One command answers five questions: **is the credential
there, are the installed skills intact, is the platform reachable, are the
required nodes registered, and what is this key actually allowed to do.**

## The command

```sh
sh scripts/doctor.sh            # environment + integrity + connectivity
sh scripts/doctor.sh skilyst/embed-video   # ... plus node preflight for one skill
```

The script wraps four runtime commands and prints one compact report; each
section is also available on its own:

| command | answers |
| --- | --- |
| `skilyst config` | which credential source resolved, and whether the key/secret/password are set (values are redacted) |
| `skilyst doctor` | every installed skill's integrity (`store.verify_all`) plus the resolved paths |
| `skilyst doctor <skill-id>` | node preflight for one skill: registry reachable, every declared node_id registered/enabled, fallback availability |
| `skilyst authz-probe` | what the restricted key gets — client-side gate vs server (with `--bypass-gate`) vs anonymous |

Exit codes are the runtime's contract, and the script propagates them:

| code | meaning |
| --- | --- |
| `0` | everything checked out |
| `2` | a rule said no — sandbox/scope refusal, or preflight reports a blocking problem |
| `3` | the run did not reach an answer (agent loop incomplete) |
| `4` | a platform call failed (transport/HTTP) |

## How to read the report

| field | meaning | what to do |
| --- | --- | --- |
| `beehive.access_key` / `secret_key` / `password` | `-` means *not found*, a truncated value or `set` means present | put the missing keys in the env file (or export `BEEHIVE_PLATFORM_*`); the file should be `0600` |
| `beehive.source` | which source won (process env beats the env file) | an unexpected source explains "it works in my shell but not here" |
| `llm.api_key` | `-` means the chat model cannot be reached at all | fix before blaming the skill |
| `integrity[].ok` = false | an installed skill was edited after install; `differences` names the file | re-install the package — the runtime refuses to load a mutated skill, and it says so loudly instead of running the edited copy |
| `preflight.registry_available` = false | `GET /api/v1/nodes` failed (HTTP status is in the message) | connectivity or base URL first; preflight blocks rather than guessing what the cluster can do |
| `preflight.problems[].severity` | `blocking` = cannot run, `degraded` = optional node missing or a declared fallback is in play, `info` = note | for a blocking problem where the message names an available fallback, the substitution is a different model, price and look — it needs `--allow-fallback`, never a silent swap |
| `token_scope` | `jobs:read`, `jobs:write`, `assets:read` for the platform key | anything else is refused client-side by design |

## What this check deliberately does not report

**Wallet balance and quota.** `/api/v1/billing/wallet` sits outside the restricted
key's scope: the runtime's client-side gate refuses it, while the server still
answers `200` to a `GET` with a restricted key. That asymmetry is a backend
scope-middleware gap, tracked for the M1 risk table — so doctor reports "quota:
not readable from the agent runtime" instead of inventing a number, and cost
decisions stay quote-first arithmetic from the node pricing plus an out-of-band
balance check. Run the probe with `--bypass-gate` only when auditing that gap,
never as a way to spend.

## Why this is the first command

Two of the cheap failures — a missing credential and an unregistered required
node — are detectable *before* submission, and the second one is exactly the kind
of failure that otherwise surfaces as a paid job that runs and then fails. The
runtime already refuses to run a skill whose node requirements are unmet; doctor
is how you find that out on purpose, before the run.

## Hand-off

Report the failing section verbatim (skill id, node_id, severity, HTTP status)
rather than a summary — the remedy depends on which of the five questions failed.
