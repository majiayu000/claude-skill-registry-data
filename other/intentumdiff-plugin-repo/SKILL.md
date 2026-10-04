---
name: intentumdiff-plugin-repo
description: >-
  The RULES a standalone IntentumDiff plugin repo must follow — every intentumdiff-<lang>-parser (and
  any third-party plugin, e.g. intentumdiff-dbt). Use this whenever you create, scaffold, review, or
  work in a plugin/parser repo: what it must contain, how it depends on the SDK, the WIT contract it
  implements, the CI it must pass, and how it earns trust via the registry. This skill is MASTERED
  in intentumdiff-plugin-sdk and COPIED (never forked) onto each plugin repo — edit the SDK master and
  re-sync, never the local copy. Read intentumdiff-parsers for parser mechanics and
  intentumdiff-repo-split for how the repos are created and how this skill is synced.
---

# IntentumDiff — Plugin repo rules

> **This skill is mastered by `intentumdiff-plugin-sdk` and copied onto each plugin repo. Do NOT edit
> the copy in a parser repo — change the SDK master and let the `sync-skills` job fan it out.**

A plugin repo is one self-contained WebAssembly component (a parser is the common case) plus its
build, tests, docs, and registry metadata. `intentumdiff-<lang>-parser` x69 are first-party;
third-party plugins (`intentumdiff-dbt`, …) follow the same rules and the same loading path — there
is **no privileged first-party route**.

## The rules (a plugin repo MUST…)

1. **Implement the WIT contract, and only the WIT contract.** `plugin.wit` (from the SDK) is the
   single source of truth for the boundary — there is no Python ABC, no host-side interface. A
   parser implements the `parser-plugin` world.
2. **Depend on `intentumdiff-plugin-sdk`; never copy-paste conversion code.** Shared behavior (CST→
   SemanticNode conversion, text/literal capture, generic labeling, position conventions, trivia,
   structural hashing) lives in the SDK's `TreeSitterConverter`. The repo supplies ONLY data
   (semantic-type lists) and genuine language overrides (`label_override` hooks). *Maintainer ruling
   (2026-07-06): do not copy the conversion template between crates — the 28 duplicated templates
   drifted and forced per-crate sweeps.* A conversion bug fix belongs in the SDK unless provably
   language-specific.
3. **Be `ParserMode::FullParse`** (first-party) — the plugin owns grammar AND CST→semantic mapping.
   Host-side `interpret-cst` is rejected on first-party paths.
4. **Export the full set:** `preprocess-source`, `process` (the full parse), `detect-language`
   (cheap, deterministic, conservative), `example`, `language-ids`/`language-info`,
   `trivia-node-types`.
5. **Emit a valid tree:** globally-unique `id`s (or the host rejects it), meaningful `node_type`
   (grammar role) + `label` (identity token), `parent_type` for methods, and privacy-safe
   `NodeFacts` on definition nodes. **0-based rows are mandatory** (issue #52). **VALUE/literal
   nodes must be semantic** or value edits vanish. Use the grammar's ACTUAL node-kind names — dump a
   parse, never guess.
6. **Meet the shipped-example contract:** every advertised language ID parses its `example` with NO
   fallback and NO parse errors, producing a structured diff. Dormant grammars stay disabled until
   they meet it.
7. **Ship + pass its Tier-B CI:** builds the `.wasm`, runs the #87 parity/fuzz suite (parses its own
   WIT example; survives truncated/binary/NUL/bracket-noise input with only valid outcomes — a tree,
   an in-band `{error}` envelope, or a typed plugin exception, never a host crash), and per-crate
   `cargo test`. The SDK provides the reusable CI workflow.
8. **Earn trust through the registry, not its repo.** "Official/safe" = **listed in
   `intentumdiff-registry` with a verified checksum, a clean capability scan, and a matching provenance
   manifest** — enforced by the registry PR gate, NOT by which org owns the repo. Ship a provenance
   manifest (SHA-256 of the staged `.wasm` + source manifest) and declare `trust_tier` / `abi_target`.
9. **Run sandboxed with zero host capabilities.** Parsers execute in wasmtime with empty WASI (no
   fs/net/env), memory-isolated and fuel-metered; the only host imports are `strip-trivia`,
   `structural-hash`, `log`. Do not assume any ambient capability.
10. **Pin the ABI/contract version.** The repo builds against a specific SDK WIT/host-utils version;
    the host enforces the version at load. Bump deliberately.

## What a plugin repo contains

```
intentumdiff-<lang>-parser/
  Cargo.toml            # standalone; depends on the intentumdiff SDK crate (not a workspace)
  src/                  # the parser crate (grammar dep + semantic-type data + overrides)
  wit/                  # the pinned plugin.wit (from the SDK)
  tests/                # per-crate cargo tests + Tier-B parity/fuzz fixtures
  .github/workflows/    # the SDK-provided reusable CI (build .wasm + parity/fuzz + register)
  provenance.json       # SHA-256 + source manifest for the built .wasm
  .claude/skills/       # this skill (SDK-mastered copy) + intentumdiff-parsers
  README.md
```

## Adding / fixing a language

Follow `intentumdiff-parsers` for the mechanics (scaffold from the SDK template, implement the
exports, map the CST, the hard-won conversion rules). The repo-level difference from the monorepo:
the five registration ledgers become **the registry entry + the ABI target** — a plugin repo does
not edit the core's `pyproject`/`registry.py`; it registers itself in `intentumdiff-registry`.

## Migration acceptance (files-only extraction)

A pure extraction leaves the corpus ratchet manifests byte-identical on regeneration
(`tests/fixtures/corpus` is the contract). No history is imported — one clean initial commit.
