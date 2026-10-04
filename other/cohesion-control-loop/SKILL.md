---
name: cohesion-control-loop
description: Continuously map built ChefFlow surfaces, classify wiring/access/completion/proof state, document every pass, route through Omninet and the default ChefFlow skill roster, and produce queue-ready mandatory gaps until the current product graph has no mystery surfaces. Use when the user says continue cohesion loop, blueprint completion, zero out the codebase, run the cohesion daemon, map all wired surfaces, or asks whether ChefFlow is fully cohesive.
---

# Cohesion Control Loop

Canonical Codex source: `.agents/skills/cohesion-control-loop/`.

Use the Codex-visible skill body and scripts there. The required deterministic commands are:

```powershell
node .agents/skills/cohesion-control-loop/scripts/cohesion-control-loop.mjs init
node .agents/skills/cohesion-control-loop/scripts/cohesion-control-loop.mjs run --focus routes
node .agents/skills/cohesion-control-loop/scripts/cohesion-control-loop.mjs status
node .agents/skills/cohesion-control-loop/scripts/cohesion-control-loop.mjs next
```

Hard rule: every run must update `.agents/cohesion/state.json`, `.agents/cohesion/blueprint.json`, `.agents/cohesion/ledger.md`, `.agents/cohesion/handoff.md`, a gap file, or a proof pack. A spoken summary alone is a failed run.

Completion rule: every built surface must be evaluated against the default ChefFlow wiring matrix in `.agents/skills/cohesion-control-loop/references/DEFAULT-WIRING-MATRIX.md`. A surface does not need every domain wired, but every relevant domain must be `wired`, `not-applicable`, `queued-gap`, `blocked`, `deprecated`, or `intentionally-local`; lingering `unknown` domains prevent completion.
