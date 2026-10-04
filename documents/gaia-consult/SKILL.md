---
name: gaia-consult
description: >-
  Reference guide for the full manual Gaia curation pipeline. Invoke at any phase
  when unsure what command to type next: gaia-curate, L4 review, gaia push, ev-pipeline
  (Phases 0–4), gaia-ingest, or close. Trigger phrases: "/gaia-consult", "what's the
  command for", "remind me how to", "I'm lost in the pipeline", "what do I do next",
  "consult the pipeline doc", "pipeline reference".
version: 1.0.0
---

# gaia-consult

This is a **lookup skill** — it points you at the canonical pipeline reference document and tells you which section covers the phase you're in. Read the section. Type the command. Do not guess.

## Reference document

```
docs/en/manual-curation-pipeline.html
```

Open it in any browser. It is self-contained, offline-capable, and covers every phase with exact typed commands.

## Phase → section map

| You are in… | Jump to section in the doc |
|---|---|
| You want to automate everything from a URL | **[/gaia-quick-curate](../gaia-quick-curate/SKILL.md)** — not this doc |
| Discovering a skill, running prefill, writing the packet | **Phase 1 — gaia-curate** |
| Reviewing the packet, ratifying with `gaia dev ratify` | **Phase 2 — L4 Review** |
| Running `gaia push`, branching, opening the draft PR | **Phase 3 — gaia push → PR** |
| Running the evidence lake phases (0–4) | **Phase 4 — ev-pipeline** |
| Writing evidence rows, appraising TM, calibrating stars | **Phase 5 — gaia-ingest** |
| Merging the PR, posting comments, closing the issue | **Phase 6 — Close** |
| Any command failing unexpectedly | **Common errors** section at the bottom |
| Need every command in one place | **Quick-reference cheat sheet** at the bottom |

## When to invoke this skill

- You are at any phase of the pipeline and are unsure of the next command.
- A command failed and you want to check the expected invocation.
- You want to confirm a flag, a file path, or a decision-rule before proceeding.
- You are about to mutate the registry (`gaia dev evidence`, `gaia dev calibrate`, `gaia dev fuse`) and want to double-check the exact invocation.

## Suite curation detour

If the intake is for a **suite capstone** (a contributor with 3+ named skills being fused), the pipeline has an additional step between Phase 5 (ingest) and Phase 6 (close). Before closing:

1. Confirm all component named skills are already in the registry at their correct rank.
2. Run `/gaia-fuse-full-suite` — this adds the fusion node, suite manifest, `derivatives` back-links, and `fuse` timeline event.
3. Validate: `GAIA_OPERATOR_OVERRIDE=1 gaia dev validate`
4. Then proceed to Phase 6 (close) as normal.

Do not attempt to hand-write a fusion node — the CLI writes it with the correct `type: fusion` and timeline entry.

## This skill does not…

- Execute any commands itself.
- Duplicate the pipeline documentation inline.
- Replace reading the actual reference file.
