---
name: client-translator
description: "This skill should be used when the user has architecture/engineering technical text needing client-friendly rephrasing, OR a vague client wish needing translation into actionable technical options. Trigger on 'translate this for the client', 'put this in plain language', 'client-facing version', or pasted technical specs alongside client communication context. Generates a paired client-facing or technical document in `docs/client-comms/`."
license: MIT
metadata:
  title: "Client Translator"
  summary: "Turn technical language into client-ready wording, and back"
  discipline: "practice-contracts"
  tags: "Pre-Design"
---


# Client Translator


## Overview


Translate between two registers in architectural communication: technical (architect/engineer language) and client-facing (everyday language). Both directions. Outputs a paired document the team can hand directly to a client or to a consultant.


## Scope and limits — read first


**What this does.** Moves one piece of text between two registers, technical and
client-facing, in either direction, and writes the pair to `docs/client-comms/`
so both versions stay together. Numbers, decisions, and risks survive the move
intact.

**What this does not do.**

- **It does not change the substance.** Cost, schedule, and performance figures
  cross over unchanged. A number is never softened into a phrase, and a decision
  the client has to make is never dropped to make the message read more easily.
- It does not invent the technical detail a source text is missing. A gap comes
  back as a gap, before the client version is written.
- It does not advocate for the design. Translating is the service; the argument
  is yours.
- It does not send anything. It writes files, and you transmit them.
- It does not translate between languages. Both registers are English.

**What you need before starting.** The source text, and the audience it is going
to. If the direction is ambiguous the skill asks once rather than guessing.

## When to use


Trigger on:

- Pasted technical specs (U-values, system descriptions, change-order language) needing a client-readable version.
- Vague client wishes ("we want it to feel warmer and cozier") needing decomposition into technical options.
- File path to a spec section that needs a client-facing companion.
- Explicit asks: "translate this for the client", "put this in plain language", "client-facing version".

Do NOT trigger for the team-internal documents that already speak the right register.


## Workflow


### Step 1 — Bootstrap if needed


Check `docs/client-comms/` exists. If not:


```bash
python scripts/init_comms_workspace.py
```


### Step 2 — Detect direction


Determine whether the input is **tech → client** or **client → tech**:

- Tech → client: input is precise, contains units/codes/spec sections, often imperative.
- Client → tech: input is sensory/aesthetic, contains feelings or goals, often interrogative or wishful.

If ambiguous, ask the user once.


### Step 3 — Translate


Load `references/jargon_glossary.md` for term-by-term mappings (e.g. "U-value" → "how well the wall blocks heat loss", "Passive House" → "near-zero-heating-bill standard"). Apply translation principles:


**Tech → client:**

- Keep accuracy. Do not soften specific claims into vague feelings.
- Anchor to lived experience. "R-27 wall assembly (U-0.037 Btu/h·ft²·°F)" → "interior walls stay at room temperature even on a 14°F winter day".
- Surface decision points. If the technical content implies a choice (budget, schedule, performance tradeoff), make it the headline.
- Compress. Detail belongs in the appendix; the client reads the first paragraph.

**Client → tech:**

- Extract the underlying constraint. "Cozy feel" might decompose into: warm CCT (2700-3000K), tactile materials (timber, fabric), enclosed proportions, warm finish tones.
- Offer 2-3 options at different cost/effort tiers, not a single answer.
- Flag what is actionable now vs dependent on further client input.

### Step 4 — Write the paired document


Read `assets/translation-template.md`. Fill placeholders. Filename:

- Tech → client: `docs/client-comms/<source-slug>-client.md`
- Client → tech: `docs/client-comms/<wish-slug>-options.md`

Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from the source spec section name or the client's wish keywords.


### Step 5 — Update the comms index


```bash
python scripts/append_to_index.py \
  --date 2026-05-06 \
  --slug exterior-wall-insulation-client \
  --direction tech-to-client \
  --tone warm
```


### Step 6 — Report


Tell the user:

- Path to the paired document
- Whether any open decisions need client input
- Suggested transmittal channel if `docs/project.md` mentions one

## Tone options

- `--tone=formal`: Corporate or institutional clients. Honorifics, no contractions.
- `--tone=warm` (default): Individual residential clients. Conversational, reassuring.
- `--tone=brief`: Single-paragraph summary only.

## Rules

- Sensitive numbers (cost, schedule risk) are emphasized, not buried.
- Never replace a specific number with a vague phrase. "$500,000 cost increase needed" stays as "$500,000 cost increase needed", possibly with "(about X% of the construction budget)" added.
- If the technical input contains a contradiction or assumption gap, flag it before producing the client version. Do not paper over technical issues in plain language.

## Anti-patterns

- Editorializing the architect's design choices. Translate, do not advocate.
- Omitting decision points to make the message feel pleasant. Clients need to decide; clarity is the service.
- Inventing technical details to fill gaps. If a detail is missing, say so.
- Editing `index.md` manually. Use `append_to_index.py`.

## Resources

- `scripts/init_comms_workspace.py` — bootstrap `docs/client-comms/` and the index
- `scripts/append_to_index.py` — append a row to `docs/client-comms/index.md`
- `references/jargon_glossary.md` — technical-term ↔ everyday-language mappings
- `assets/translation-template.md` — paired document template
