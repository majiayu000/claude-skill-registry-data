---
name: gbrain
description: Use when the user asks for GBrain, personal knowledge brain setup, brain-first retrieval, local PGLite brain, hybrid RAG search, gbrain import/query/sync/embed, GBrain skills, Minions, durable agent jobs, soul-audit, brain maintenance, or integrating GBrain with gstack, Hermes, OpenClaw, Claude Code, or Codex.
---

# GBrain Universal Adapter

Canonical upstream checkout: `%USERPROFILE%\gbrain`

GBrain is a real CLI-backed personal knowledge brain. It is not just a skill
pack. The universal stack keeps the upstream checkout and local brain state in
one place, then exposes GBrain skills and commands through `skill-router`.

On Windows, the canonical GBrain binary is
`%USERPROFILE%\.bun\bin\gbrain.exe`. The compatibility shim
`%USERPROFILE%\go\bin\gbrain.cmd` delegates to it so AI hosts with an older
inherited PATH still resolve `gbrain` without duplicating the install.

## Core Commands

```bash
gbrain --version
gbrain doctor --json
gbrain stats
gbrain import <dir> --no-embed
gbrain embed --stale
gbrain search "<query>"
gbrain query "<question>"
gbrain sync --repo <brain-repo>
gbrain jobs smoke
```

Use keyword search without API keys. In the Universal AI Stack, text vector
search uses the local Qwen embedding service through
`llama-server:qwen3-embedding-0.6b` at `http://127.0.0.1:18084/v1` with 1024
dimensions, so GBrain text embeddings do not require an OpenAI key. Anthropic
query expansion and durable subagent workers require the relevant provider key
only for those optional features.

## Load GBrain Skills On Demand

The upstream GBrain skills are indexed from:

```text
%USERPROFILE%\gbrain\skills
```

Examples:

```bash
skill-router skill brain-ops
skill-router skill signal-detector
skill-router skill query
skill-router skill ingest
skill-router skill media-ingest
skill-router skill maintain
skill-router skill minion-orchestrator
skill-router skill soul-audit
skill-router skill skillify
```

Before changing a GBrain workflow, read:

```bash
skill-router skill gbrain
skill-router skill brain-ops
skill-router skill query
```

For setup or repair, read the upstream installer flow first:

```powershell
Get-Content "$env:USERPROFILE\gbrain\INSTALL_FOR_AGENTS.md"
Get-Content "$env:USERPROFILE\gbrain\AGENTS.md"
Get-Content "$env:USERPROFILE\gbrain\docs\GBRAIN_VERIFY.md"
```

## Integration Policy

- Keep `%USERPROFILE%\gbrain` as the single upstream source checkout.
- Keep `%USERPROFILE%\.gbrain` for GBrain runtime state such as PGLite data and
  user-level GBrain skills.
- Do not vendor GBrain's full skill tree into every AI root.
- Use `skill-router` for on-demand loading and `gbrain` for persistent brain
  operations.
- GStack and GBrain can cooperate: GStack supplies engineering process skills;
  GBrain supplies brain-first retrieval, memory, jobs, and durable agent context.

## Maintenance

Follow the upstream upgrade path:

```powershell
git -C "$env:USERPROFILE\gbrain" pull --ff-only
Set-Location "$env:USERPROFILE\gbrain"
bun install
gbrain init
gbrain post-upgrade
gbrain doctor --json
```

Do not run `bun install -g github:garrytan/gbrain`; upstream documents that this
skips required install behavior.
