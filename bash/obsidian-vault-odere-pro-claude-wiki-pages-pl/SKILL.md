---
name: obsidian-vault
description: >
  Guard contract for driving the Obsidian CLI safely — always scope every
  invocation to the resolved vault, never operate on arbitrary vaults or paths.
  Trigger when an agent is about to run `obsidian` commands, or asks "how do I
  call the Obsidian CLI", "which vault am I writing to", or invokes
  /claude-wiki-pages:obsidian-vault. Reference material that complements the
  enforced firewall hook (`scripts/firewall.sh`).
allowed-tools: Read Bash
---

# Obsidian Vault — safe CLI scoping

The Obsidian CLI (`obsidian`, used by `obsidian-cli`, `obsidian-graph-colors`)
can act on any vault registered on the machine. This skill is the convention
that keeps an agent inside the **one** vault it was asked to work on — the
behavioural twin of the firewall hook, which enforces the same boundary on the
write path.

## The rule

1. **Resolve the vault first.** `VAULT=$(bash scripts/resolve-vault.sh && …)` —
   use the four-tier resolution, never a hard-coded path. The resolved path is
   the only vault you may touch.
2. **Always pass the vault explicitly.** Every Obsidian CLI call carries
   `--vault "$VAULT"` (or the CLI's equivalent). Never rely on the CLI's
   "current"/"default" vault — that is whatever the user last opened.
3. **Never operate on a different vault name.** If a task names another vault,
   stop and surface it; do not switch vaults to satisfy it.
4. **File operations stay inside the vault.** Reads/writes you issue alongside
   the CLI must resolve under `$VAULT`. Writes outside it are rejected by the
   firewall hook anyway — treat that block as a contract, not an obstacle to
   work around.

## Why both a skill and a hook

- The **hook** (`scripts/firewall.sh`, `firewall` engine command) is the
  enforcement: it blocks an out-of-vault Write/Edit regardless of intent.
- This **skill** is the intent: it teaches an agent to scope correctly in the
  first place, so the hook rarely has to fire. Defence in depth — a confused
  agent is stopped by the hook; a careful agent never reaches it.

## Configuration

Vault isolation is configured under `firewall` in `claude-wiki-pages.json`
(`enabled`, `mode` = `enforce`/`warn`/`off`, `allowPaths`, `denyPaths`). To let
an agent write to an extra root (e.g. a shared notes directory), add it to
`firewall.allowPaths` — do not disable the firewall.
