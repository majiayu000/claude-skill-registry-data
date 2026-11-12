---
name: maintain-contract
description: >
  The workflow contract for any agent that ingests, retrieves from, or maintains
  a claude-wiki-pages vault. Documents the safe ordering — ground → judge →
  verify — checkpoint discipline, retrieval grounding, and the immutability
  rules, so an external agent can drive the wiki correctly without re-reading
  the whole spec. Trigger when an agent or user asks "how should I maintain the
  wiki", "what is the safe ingest/retrieve order", "how do other agents use
  this", or invokes /claude-wiki-pages:maintain-contract. Reference, not action.
allowed-tools: Read
---

# Maintain contract — how to drive the wiki safely

This is the procedure any agent (this plugin's or a third party's) follows to
operate on a vault without corrupting it. It pairs with
`/claude-wiki-pages:engine-api`, which documents the tool surface this contract sequences.

## The three invariants

1. **Ground, then judge, then verify.** Compute facts with the engine (verify, fix, and the planned link-suggest/search) before reasoning. The LLM makes only judgment calls — topic placement, prose, what to synthesize — over engine-computed facts, never from memory. Close every write with `verify`/`heal`.
2. **`raw/` is immutable.** Never write, move, or delete anything under `vault/raw/`. Sources are the provenance anchor. The `protect-raw` hook enforces this; do not fight it.
3. **Git is the safety net, not approval.** Self-heal is automatic. Before structural changes, a checkpoint commit is written; rollback is `git revert <healCommit>`. Do not prompt the user for permission to fix structure. Write phases that happen outside the engine (ingest writes, judgment fixes, polish) are bounded the same way: `snapshot.sh pre` before the phase, `snapshot.sh post` after it, and the `SubagentStop` commit backstop sweeps up anything left dirty — no LLM write escapes git coverage.

## Ingest (add knowledge)

1. `snapshot.sh pre` — checkpoint the pre-write state. 2. Read each source in `raw/` completely. 3. Write cited wiki pages (`sources:` as `[[wikilinks]]` to `_sources/` summaries), then `snapshot.sh post --label "ingest …"`. 4. Run `engine.sh heal` — it checkpoints, then verify→fix→re-verify, then commits. 5. Surface only what needs editorial intent (ambiguous merges, deletions).

## Retrieve (answer questions)

1. Use grounded retrieval (engine `search`, or `grep` over `wiki/` until `search` ships) to fetch candidate pages. 2. Answer **only** from those pages. 3. Cite every claim with the `[[Page Title]]` it came from. 4. Never invent a citation; if the wiki cannot answer, say so.

## Maintain (keep it healthy)

1. `engine.sh verify --json` to diagnose. 2. `engine.sh heal --json` to repair the structural-error subset under a checkpoint. 3. Apply judgment fixes (restructures, merges) automatically under the same checkpoint. 4. Re-verify; iterate within the engine's cap; surface residual editorial items.

## Hard rules (never violate)

- Never create a `[[wikilink]]` to a non-existent page, and never create a stub just to satisfy a broken link.
- Never forge provenance — do not edit `sources:` to manufacture a citation.
- Never delete page content; connect orphans instead.
- Always read `vault/CLAUDE.md` first — it is the authoritative schema and wins any conflict.

## Multi-vault operating rules

When more than one vault is registered, every engine call must be explicitly scoped. These rules
are derived from [ADR-0009](../../docs/adr/ADR-0009-multi-vault-confinement.md) and
[ADR-0016](../../docs/adr/ADR-0016-simultaneous-multi-vault-management.md); the enforcement
mechanism is the firewall twins (`scripts/firewall.sh` + `src/core/firewall.ts`) and the registry
reader (`scripts/resolve-vault.sh`).

**Rule 1 — Always target the active vault.**
Pass `--target <active-vault-path>` to every engine call. Never omit `--target` when a registry is
configured; the engine resolves the vault independently and may not agree with the hook's resolved
path if the registry has changed between calls.

**Rule 2 — Pass `--other-vaults` from the registry for confinement.**
`scripts/resolve-vault.sh` exports `registry_other_vaults` — the registered vault roots minus the
active one. Pass that set as `--other-vaults` to the engine's `firewall` command so both the bash
twin and the TS twin enforce the `cross-vault` deny rule with the same root set. Do not hard-code
vault paths; derive them from the registry at call time.

**Rule 3 — Reads from a non-active registered vault are permitted.**
An agent may read files (via `Read` tool or `grep`/`Glob` over a non-active vault path) when a
cross-vault comparison is needed. Read operations are not governed by the firewall write-confinement
boundary. No engine flag is required for reads.

**Rule 4 — Writes to any non-active vault are firewall-BLOCKED regardless of `--other-vaults`.**
The `cross-vault` deny rule fires before the `allowPaths` check (ADR-0009 precedence:
deny → cross-vault → vault → allowPaths → outside-vault). Passing `--other-vaults` does not
grant write access — it provides the root set the firewall uses to *identify and block* cross-vault
writes. No `firewall.allowPaths` entry can override a `cross-vault` block. To write to a
different vault, first switch the active vault via `scripts/set-vault.sh switch <path>`.

**Rule 5 — A malformed or inconsistent registry resolves FAIL-CLOSED (zero writable roots).**
If `registry_other_vaults` (`scripts/resolve-vault.sh`) exits non-zero — because the registry JSON
is malformed or `current_vault_path ∉ vaults[]` — the firewall maps this to zero writable roots:
neither the active vault nor any other vault is writable until the registry is repaired. This is
not an error to work around; it is the security posture mandated by ADR-0016 (PM.2/N4). The
fail-closed signal is an exit code, not a stdout sentinel; the `__FAIL_CLOSED__` token lives only
inside `scripts/firewall.sh`. Run `bash scripts/set-vault.sh list` to diagnose the inconsistency.

## Specification anchor

Contracts: [`docs/architecture.md`](../../docs/architecture.md) (command & agent contracts), [`SECURITY.md`](../../SECURITY.md) (security model).
