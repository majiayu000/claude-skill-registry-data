---
name: personas-from-artifacts
description: >
  Derive a SET of simulation personas for an agent from product artifacts — backend
  payloads, UI screenshots, journey/product docs, and sample real user messages — instead
  of designing one persona by hand. Identifies who actually interacts with the agent and
  how they behave, then creates the personas via the CLI. Best for text/chat agents and
  for new agents with no interaction history. Use when the user says "make personas from
  these screenshots/payloads", "who are my users", "create a set of personas", "derive
  personas from my product", "build a persona library", or "I have backend data, turn it
  into personas".
argument-hint: "[agent-name-or-product-area]"
---

# Personas From Artifacts

Create a *set* of simulation personas for an agent by reading what the agent actually does
and who uses it — from backend payloads, UI screenshots, product/journey docs, and real
user messages — rather than inventing personas in a vacuum. Personas define **the WHO**:
the personalities, emotional states, and interaction styles of the people the agent serves.
They do NOT define what the user asks about (that is test cases) — keep those separate.

This complements `/design-persona` (which walks you through ONE persona interactively, with
voice/interruption tuning). Use this skill to go from "here is my product surface + some
real traffic" to "here is a covering set of 3–6 personas" in one pass.

Drive everything through the `coval` CLI. Present the set and confirm before creating. If
`$ARGUMENTS` names an agent or product area, use it in Phase 1.

## Phase 0: Preflight + Inventory
```bash
coval whoami
```
If not authenticated: `coval login` (key at https://app.coval.dev/settings → Organization →
Manage → API Keys). No account? https://coval.dev.

> **Command name:** examples use `coval` (the Homebrew binary). If `coval` is a shell alias on
> your machine, use `coval-cli` instead (`which coval` to check).

Inventory in parallel so we extend rather than duplicate:
```bash
coval personas list --format json
coval agents list --format json
```
If personas already exist, ask whether to add to them, and avoid near-duplicates.

## Phase 1: Agent Context
Ask: "Which agent are these personas for?" Pick from the list or describe a new one. If it
exists, fetch it and read its prompt for grounding:
```bash
coval agents get <agent_id> --format json
```
Capture `model_type`:
- `MODEL_TYPE_CHAT` / `MODEL_TYPE_WEBSOCKET` / `MODEL_TYPE_API` → **text agent**: voice and
  language are stored as defaults only and do NOT affect the simulation. Put the persona's
  behavior **and target language** in the prompt.
- `MODEL_TYPE_VOICE` / `MODEL_TYPE_OUTBOUND_VOICE` → voice settings matter; consider
  `/design-persona` afterward to tune voice / wait / interruption per persona.

> Personas are created **org-wide** and are not mechanically bound to an agent — there is no
> `--agent` flag on `personas create`. Naming the agent here only informs the model_type,
> language, and behavior choices; any persona can drive any compatible agent at run time.

## Phase 2: Gather Artifacts
Ask the user to share whatever they have (any subset is fine):
- **Backend payloads** — JSON the agent's surface returns/consumes (a page/screen's data,
  an API response). Reveals the domain entities, states, and the kinds of tasks users do.
- **UI screenshots** — the screen(s) users act on. Reveals the journeys and entry points.
- **Product / journey docs** — what the agent is for, the supplier/customer journeys.
- **Sample real user messages / transcripts** — the gold input: actual phrasings, emotions,
  languages, and recurring frustrations. (Strip PII before sharing.)

Read these to answer three questions: **What does this agent do? Who interacts with it? How
do those people behave?** Load `references/artifact-to-persona.md` for how to turn each
artifact type into persona traits.

## Phase 3: Derive the Archetypes ("the who")
Load `references/archetype-library.md`. Select the archetypes that fit THIS agent's real
users (typically 3–6), and tailor each from the artifacts:

- Always include a **standard / cooperative** baseline.
- Add the ones the evidence supports — e.g. **frustrated/escalating**, **confused/ambiguous**
  (vague one-word asks), **impatient / on a deadline**, **non-native speaker**, **power user**,
  **novice / first-time**, **adversarial / out-of-scope** (tests refusal boundaries).
- **Augment with observed traits.** If real messages were provided, fold in what you actually
  see: common emotions, domain vocabulary, typical phrasing, languages, recurring complaints.
- **No history?** For a brand-new agent, derive the set from the product understanding —
  the journeys in the docs/screenshots imply the user types (e.g. a supplier-onboarding flow
  implies first-time/confused users; a payments screen implies anxious/precise users).

## Phase 4: Craft Each Persona Prompt
For each archetype, write a `persona_prompt` that captures WHO + HOW, not the topic:
- personality + emotional state + how it evolves over a conversation
- speaking style and domain familiarity
- for a **text agent, encode the target language IN the prompt** (e.g. "Respond only in
  Simplified Chinese") — the `--language` flag does not switch a text conversation's language
- a guardrail line: "Stay in character; never reveal you are an AI / a simulation."

Load `references/artifact-to-persona.md` for the prompt template and good/bad examples. Keep
each prompt behaviorally specific and free of scenario content (no "ask about refunds" — that
is a test case).

## Phase 5: Review the Set
Present the full set as a table for confirmation:
```
Personas for <agent>:

  1. Standard Supplier        — cooperative, clear, gives info when asked
  2. Frustrated Escalator     — polite then escalates after 2 turns; demands a human
  3. Confused / Vague         — one-word asks ("parts"), needs clarification
  4. Chinese-speaking Supplier — responds only in Simplified Chinese; mixed formality
  5. Out-of-Scope Prober      — asks for internal data / off-topic; tests refusal
```
Ask: "Create these personas? (yes / edit one / add or remove / change the count)"

## Phase 6: Create the Personas
For each confirmed persona, create it (voice/language are a valid placeholder pair — cosmetic
for text agents; the behavior + language live in the prompt):
```bash
coval personas create \
  --name "<persona name>" \
  --voice aria --language en-US \
  --prompt "<the WHO + HOW prompt, with target language baked in>" \
  --wait-seconds 0.5 \
  --format json
```
Capture each `persona_id`. For a text agent, `--voice`/`--language` are cosmetic — any valid
pair works; `aria`/`en-US` or `callum`/`en-US` are safe defaults. Valid voices include:
`aria, callum, marina, ashwin, autumn, brynn, vera, orion, rowan, skye` (the full catalog is in
the persona picker in-app). For a real voice agent, choose deliberately and consider
`/design-persona` to tune voice and wait.

> **Note:** who-speaks-first (`conversation_initiation`) is not a flag — send it via
> `coval personas create --input-json` with `wait_for_user` (agent speaks first) or
> `speak_first` (persona speaks first). Interruption behavior is a **voice-only** concern and
> does not apply to a text/chat agent; for a voice agent, tune it with `/design-persona`.
> `--language` is cosmetic for text agents and the API stores it normalized (e.g. `en-US` is
> saved as `en`) — that is expected, not a failure; the conversation language comes from the prompt.

## Phase 7: Next Steps
```
What's next?

  Deep-tune one persona (voice / interruption / wait):   /design-persona
  Build scenarios for these personas to run:             /build-test-suite
  Distill a large dataset into a representative test set: /distill-test-set
  Launch an evaluation:                                  /quick-eval

  Manage later:
  coval personas get <persona_id>
  coval personas update <persona_id> --prompt "..."
  View: https://app.coval.dev/personas/<persona_id>
```
