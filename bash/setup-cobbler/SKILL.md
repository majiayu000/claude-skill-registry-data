---
name: setup-cobbler
description: Configure Cobbler model routes and external-agent preferences for this checkout. Use when the user types /setup-cobbler, asks to set up Cobbler model routes, onboard models, or update which tools handle planning/implement/review in Claude Code.
disable-model-invocation: true
---

<!-- elves-managed-alias: claude-skill-alias v1 -->

# Setup Cobbler / Model Onboarding

This is an Elves-managed Claude Code alias for `/setup-cobbler`.

Run the **model onboarding** contract from the main `elves` skill and
`references/model-onboarding.md`. Operator CLI:

```bash
python3 scripts/cobbler_agents.py onboard plan|show|apply|probe [--json]
python3 scripts/cobbler_agents.py setup …   # apply-only / inventory
```

Setup must not require OpenRouter or any external provider key. Native-only Elves remains fully
usable without running setup.

## Default behavior (both Claude Code and Codex)

1. **Plan:** `onboard plan --json` — inventory tools, detect env **names** present (never values),
   emit purpose→route questions.
2. **Interview the user** for each purpose (planning, implement, review, scout, validate, synthesize,
   optional math evolutionary search). Offer **host-native first**. Respect available CLIs/keys.
3. **Apply:** `onboard apply` writes ignored `.elves/models.toml` only. Never stage it. Never paste
   API keys into TOML, chat, or the Survival Guide.
4. **Probe:** `onboard probe` runs structural checks (PATH, `--help`, env names). Optional
   `--smoke` only if the user wants a paid live check — host runs a real tiny completion; fake
   smoke does not count.
5. **Update later:** same flow (`show` → re-interview → `apply --force` → `probe`).
6. Recommend routes by capability, not prestige model names. Keep host-native fallbacks.
7. Snapshot effective routes into the Survival Guide during Elves staging for reviewable provenance.

Codex equivalent (not a top-level slash command): `$elves setup-cobbler` or natural language such as
"Set up Cobbler external-agent preferences" / "onboard my models."

Compatibility: `/setup-council` is the same setup contract with a Council-era name.
