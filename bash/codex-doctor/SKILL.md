---
name: codex-doctor
description: Diagnose OpenAI Codex CLI, Desktop, IDE, skill, plugin, MCP, session, configuration, authentication, network, storage, and performance problems using a local-first evidence workflow. Use when Codex is failing, slow, stuck, reconnecting, losing sessions, or behaving unexpectedly; do not use it to perform unrequested repair or cleanup.
---

# Codex Doctor

Produce a diagnosis that separates evidence from inference and routes the user to the safest matching official or community Doctor.

## Define the case

State the problem before searching. Capture what is available without making the user repeat known context:

- symptom, exact error, and expected behavior;
- Codex surface: CLI, Desktop, IDE, cloud, skill, plugin, SDK, or MCP;
- operating system, shell, Codex version, and install/update channel;
- authentication or model-provider path when relevant;
- when the problem began, reproducibility, and recent changes.

Use read-only discovery to fill ordinary gaps. Ask the user only when a missing choice would materially change the diagnosis or authorize a mutation.

## Search locally first

1. Search the current workspace and relevant Codex configuration with `rg` or another read-only tool. Prefer exact error text, component names, config keys, plugin IDs, and session identifiers. Never print secrets or entire auth/config files when narrower evidence is enough.
2. Locate the `awesome-codex-doctors` repository. When this skill is installed from that repository, its root is two directories above this file. Search `CATALOG.md` and `data/github-snapshot.json` before general web search.
3. Match the case to specialties such as authentication, Windows, Desktop plugins, session repair, reconnect, MCP, hooks, providers, context, performance, storage, or logs. Shortlist only projects that address the observed symptom and platform.
4. Check whether the installed Codex provides the official command by running `codex --version` and `codex doctor --help` or equivalent read-only checks. Do not assume flags supported by a newer version.

Do not run third-party scripts, repair commands, cleanup flags, installers, or package managers during diagnosis unless the user has requested that action and the exact effect has been reviewed.

## Search outward

After the local catalog and files:

1. Search the exact error plus the Codex surface, version, operating system, and affected component.
2. Check current official OpenAI documentation and the `openai/codex` repository for intended behavior, releases, issues, and source evidence.
3. Open the shortlisted community Doctor repositories. Inspect their README, supported platforms, release/activity state, license, data touched, and safety model. Do not rely on search snippets.
4. Use broader web discussions only to find leads or corroborate; do not treat an unsourced workaround as established fact.

Prefer recent, version-matched evidence. Call out when a proposed Doctor predates the user's Codex version or depends on an undocumented local-state format.

## Rank actions by risk

Label every next step:

- **Read-only:** inspection and diagnostics that should not alter state.
- **Reversible repair:** changes with a verified backup, dry-run, or rollback path.
- **Cleanup/destructive:** removal, pruning, database rewrites, or irreversible changes.

Recommend read-only confirmation first. Before any repair or cleanup, identify exact paths and records, confirm the tool is not acting on source code or unrelated user data, explain backup/rollback, and obtain any required authorization.

Redact tokens, credentials, private repository names, usernames, and unnecessary absolute paths before sharing logs or reports online.

## Report the diagnosis

Read [references/diagnostic-report.md](references/diagnostic-report.md) before producing the final diagnostic report.

If evidence remains insufficient, say what is known, what is only suspected, and the smallest read-only observation that would discriminate between the leading causes. Never invent a matching Doctor.
