---
name: exasol-setup-personal
description: "Guided setup of Exasol Personal — a free Exasol database running locally on a Mac or deployed to your own AWS, Azure, Exoscale, or STACKIT account. Covers picking the right deployment flavor, the `exasol` launcher CLI (`exasol install <preset>`, `exasol connect`, `exasol info`, `exasol deployments list`, `exasol destroy`), the `local`, `aws`, `azure`, `exoscale`, and `stackit` presets, and following the official exasol/exasol-personal instructions."
---

# Exasol Personal Setup Skill

Exasol Personal is a full Exasol analytics database, free for personal use, run
either in a VM on the user's Mac or on compute in their own cloud account. This
skill gives high-level direction — which flavor, in what order, with what
confirmations — and defers every command that installs, provisions, or destroys
to the upstream `exasol/exasol-personal` documentation.

## Routing Algorithm

1. **Any setup, install, or deployment work** — always start here
   - Trigger phrases: `set up Exasol Personal`, `install Exasol`, `deploy Exasol`, `Exasol on my Mac`, `local deployment`, `AWS`, `Azure`, `Exoscale`, `STACKIT`, `exasol install`, `preset`, `named deployment`, `sample data`
   - Load: `references/upstream-docs.md` **and** `references/setup-walkthrough.md`

2. **A deployment that already exists is failing** — diagnosis and cleanup
   - Trigger phrases: `exasol diag local`, `install failed`, `interrupted install`, `exasol destroy`, `exasol cache`, `launcher not found`, `deployment stuck`
   - Load: `references/troubleshooting.md` **and** `references/upstream-docs.md`

The two setup references are a pair: `references/upstream-docs.md` says which
upstream document to fetch and what to do when a fetch fails,
`references/setup-walkthrough.md` gives the phase order and the questions to
ask. Never run a walkthrough phase without the upstream document it names.

## Non-Negotiable Rules

- **Never reproduce install, provisioning, or account-setup commands from
  memory.** Exasol Personal changes frequently and stale commands break setups.
  Fetch the upstream document and follow it.
- **Ask at every decision point.** Never assume answers or skip confirmations.
  This applies equally to Claude Code and OpenAI Codex.
- **Use `exasol connect`, not `exapump`, for SQL during setup.** The launcher's
  client reads deployment credentials automatically; this skill never installs
  or configures exapump.
- **Never read files that may hold credentials**, including the launcher's
  deployment directory and provider credential or environment files. Use the
  launcher's own commands, such as `exasol info` and `exasol connect`, and never
  print a credential value into the conversation.
- **Warn before cloud installs.** They take 10–20 minutes, must not be
  interrupted, and incur cloud costs. An interrupted install can leave billable
  resources behind.

## After Setup

Hand off to the skill that matches the user's next task: **exasol-database**
for SQL and general exapump work, **exasol-import** or **exasol-export** for
data movement, **exasol-bucketfs** for BucketFS, and **exasol-udfs** for UDF and
Script Language Container work.
