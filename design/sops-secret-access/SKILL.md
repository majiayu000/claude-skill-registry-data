---
name: sops-secret-access
description: Use when a repo stores tool config, API keys, registry URLs, environment variables, or component registry settings in SOPS-encrypted files such as components.sops.json or secrets/*.sops.json.
---

# SOPS Secret Access

Use the repo's encrypted source of truth when a task depends on secrets or private tool configuration. Do not infer from public fallback files if a matching `*.sops.*` file exists.

New SOPS payloads are JSON (`*.sops.json`). See [ADR-0011](../../docs/adr/0011-sops-files-as-json.md). Decrypt existing non-JSON files if that is what the repo already has; do not add new ones.

## When to Use

- A project has `components.sops.json`, `secrets/*.sops.json`, or another SOPS-encrypted config.
- A public config looks incomplete and a private registry, API, MCP server, deployment credential, or provider profile may be hidden behind SOPS.
- The task mentions shadcnblocks, private shadcn registries, registry auth, SOPS, secrets, env loading, or encrypted project config.
- A tool only shows public/default config but the repo has a likely encrypted companion file.

## Core Rules

- Decrypt only the file needed for the task.
- Do not paste decrypted contents into chat, logs, commits, or generated docs.
- Prefer commands that consume decrypted data directly or print only non-secret derived facts.
- If a decrypted file is written to disk temporarily, put it in a gitignored path and remove it before finishing.
- Treat plain files like `components.json` as fallbacks when a matching `components.sops.json` exists.

## Shadcn And Shadcnblocks

For Darkmatter UI projects, private shadcn registry access may live in `components.sops.json`.

Use this before querying shadcn registries when the user expects shadcnblocks/private blocks:

```bash
sops -d components.sops.json
```

Safer inspection examples:

```bash
sops -d components.sops.json | jq -r '.registries | keys[]'
sops -d components.sops.json > /tmp/components.private.json
```

If a tool needs `components.json`, do not overwrite the checked-in public file unless the user explicitly asks. Use a temp file, a subshell, or the tool's config override if available. If no override exists and a local replacement is unavoidable, back up the public file, restore it before finishing, and verify `git diff` does not include decrypted values.

## Common Mistakes

- Querying shadcn MCP before decrypting `components.sops.json`, then concluding only public registries exist.
- Printing full decrypted JSON to the user.
- Committing generated plaintext config.
- Adding secrets to `AGENTS.md`, README files, examples, or tests.
- Creating a new `*.sops.yaml`, `*.sops.yml`, or `.env.sops`. New payloads are `*.sops.json`.
