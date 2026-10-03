---
name: open-router
description: >-
  Resolve a colloquial OpenRouter model name (e.g. "GLM 5.2", "Nemotron Ultra 3")
  to its canonical `provider/slug[:variant]` id BEFORE setting `AIDER_MODEL` for
  `aider-turn.sh`, `consult.sh --models aider`, or `DEEP_RESEARCH_OPENROUTER_MODEL`
  for `deep-research.mjs --provider openrouter`. Checks the local alias table
  (`relay-automation/openrouter-model-aliases.yml` via `resolve-model-alias.sh`,
  GH-120) first — zero network calls — and only falls back to the live
  `openrouter.ai/api/v1/models` catalog on a miss, then writes the new alias back
  so the next lookup is instant. Use whenever the operator names a model
  informally for an OpenRouter-routed lane and asks to configure it, or when you
  are about to run `aider --list-models` / curl the OpenRouter API to find a slug
  — check the alias table first instead. NOT for choosing between models or
  picking a model for a task; only for resolving a name you already have to its
  canonical id.
---

# open-router — fast OpenRouter model-name resolve

Turns a colloquial model name into the canonical slug an OpenRouter-routed lane
needs (`AIDER_MODEL=openrouter/<slug>`), without probing.

## Step 1 — check the local alias table first (always)

```bash
relay-automation/resolve-model-alias.sh "<name>"
```

- Exit 0: canonical slug printed on stdout (e.g. `z-ai/glm-5.2`). Use it directly:
  `AIDER_MODEL="openrouter/$(relay-automation/resolve-model-alias.sh "<name>")"`.
- Exit 1: no match — go to Step 2. Do **not** reach for `aider --list-models` or a
  live `curl` first; that's the slow path this skill exists to skip.

Matching is fuzzy (case/punctuation/hyphen/whitespace-insensitive, token-order
insensitive, substring fallback) — try the name as given before assuming a miss.

## Step 2 — only on a miss: query the live catalog

```bash
curl -s https://openrouter.ai/api/v1/models | grep -i '"id":"<partial-name>'
```

Find the exact `provider/slug[:variant]` id. Confirm it's the model the operator
meant (check context length / pricing / provider if there's ambiguity).

## Step 3 — write the alias back (always, once resolved via Step 2) — the two-PR flow (GH-450)

**Do not append to `relay-automation/openrouter-model-aliases.yml`.** It is a
generated file (rendered from the vendored HiQS-Labs/Model-catalog copy), and a
hand-added line turns `python3 utils/py/model_catalog.py check` and
`test/gh450-model-catalog-pin.sh` red. Instead:

1. PR the row to [Model-catalog](https://github.com/HiQS-Labs/Model-catalog)
   `data/catalog.json` (`target: "openrouter"`, `source` = first-party URL, bump
   `version` + `updated`); the maintainer tags it.
2. Sync PR here once the tag exists — exact recipe in `relay-automation/README.md`
   → "Adding a new model alias" (`model_catalog.py pin` / `render` / `check`), plus
   a hand-written assertion for the new row in `test/model-alias.sh`.

This is still the whole point of the skill: every miss should shrink the miss set
for next time, not repeat the probe — it just lands upstream first.

Note: this skill calls `resolve-model-alias.sh` directly with the operator's raw
input. An **exact `provider/slug` id never needs resolving** — use it as is. Feeding
one to the raw resolver can hit its tier-4 substring fallback (the GH-450 seam guard
in `utils/py/model_alias.py` protects the shims, not this manual path).

## Known adjacent issue — edit-format quirk (GH-118)

Many OpenRouter-proxied models aren't in Aider's `model-settings.yml` and default
to the `whole` edit format, which some models don't reliably produce (confirmed:
GLM-5.2, Nemotron Ultra 3, **stealth/ox-alpha** — GH-161 QA relay,
2026-08-22: the model returned a full, well-formed review in diff-style `+`
lines under `whole` format, which aider's whole-format parser cannot apply as
a file replacement; no error, no reflection, the turn just sat idle until the
900s wall-clock kill with the response already sitting unused in the log).
If a driven turn reports "no tracked changes" despite a seemingly valid model
response — or times out with zero applied edit despite a normal-looking
`Tokens: X sent, Y received` line in the turn's log — set
`AIDER_FLAGS=--edit-format diff` — see `relay-automation/README.md`'s "Known
OpenRouter edit-format quirks" section. Any new/unlisted model not yet in
Aider's `model-settings.yml` (e.g. an anonymized "stealth" preview model) should
be assumed to need this flag proactively, not discovered reactively after a
wasted turn.

## What this skill does NOT do

- Does not pick which model to use for a task — that's the operator's call.
- Does not touch `AIDER_FLAGS`, edit-format, or any other Aider config beyond the
  model id itself.
- Does not run the turn — it only resolves the id you'll pass into
  `AIDER_MODEL` / `DEEP_RESEARCH_OPENROUTER_MODEL`.
