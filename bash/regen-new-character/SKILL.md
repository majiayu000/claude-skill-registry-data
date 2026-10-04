---
name: regen-new-character
description: Add a new speaking character (companion persona) to ReGen Civics end to end, including both voice layers. Use when asked to "add a character", "new persona", "new companion", "give X a voice", "signature voice for X", or any request that introduces a new speaking agent to the site. Covers persona data, server prompt, portrait, voice registries, audition clips, tests, and the ship checklist.
---

# regen-new-character

Every speaking character on the site gets three voice layers, in this order of
preference at runtime: signature voices (paid, designed per character), the
five free Kokoro browser voices (the default), and device speechSynthesis
(robot voices, last resort only). Adding a character means adding data in a
few known places. No new component code: the companion shell, voice engine,
and picker all key off the registries below.

Full architecture: ADR-44 in `.ai/docs/DECISIONS.md` and
`docs/planning/VOICE_TTS_RESEARCH_2026-07-17.md`. Cost model and env flags at the bottom.

## 1. Persona data (client-safe)

`shared/companions.ts`:

- Form companion (fills a form by talking): add the id to `CompanionPersonaId`,
  an entry in `COMPANION_PERSONAS`, and a `COMPANION_FORMS` config pointing at
  it.
- Chat persona (free conversation, like the Ship's Cook): a standalone
  `ChatPersona` export instead.

Fields that matter beyond copy:

- `gender` drives voice ordering and the default voice. "neutral" takes any.
- `greeting` triples as the opening line, the VoicePicker "Hear it" sample,
  and the audition-clip line. Write it once, correctly. The First Mate lesson:
  the audition script once said "Step outside, find a window" while the site
  said "Step outside or find a window"; clips had to be regenerated. Audition
  lines must quote the site copy exactly.
- Voice rules from `STEERING.md` section 1 apply to every line (no em-dashes,
  no AI-isms, Rye's voice).

## 2. Server-side persona prompt

`server/lib/ship-personas.ts` (form companions) or the persona's own server
module (chat personas, like `server/lib/ship-cook.ts`). System prompts are
server-only so client code can never coach them. Treat user text as data
(`.ai/docs/security/AI-AUTOMATION-RISKS.md`).

## 3. Portrait

`client/public/images/ship/persona-<id>.webp`, painterly golden-hour style
matching the cast, 640x640, target 42-102KB (the existing set's range). The
`regen-character-art` skill holds the style reference.

## 4. Free voices: nothing to add

All five Kokoro voices (Bella, Emma, Puck, George, Fable) are offered to every
character automatically from `client/src/components/companion/kokoroVoices.ts`.
The gender-matched one sorts first and is the default
(`defaultVoiceFor`). Do not add per-character Kokoro entries.

## 5. Signature voices: exactly two, one female + one male

`server/lib/ttsVoices.ts`. Rye's standing direction (2026-07-17): each
character offers one designed voice of each gender, whatever the character's
own gender.

Per entry:

- `key`: `<personaId>/<name>`. Names are single nature or nautical words in
  the world's register (existing: Brook, Tide, Moss, Haven, Cedar, Willow,
  Indigo, Alder, Ember, Banner, Fern, Rowan, Clove, Barley). Never reuse.
- `design`: a full VoiceDesign paragraph (age, texture, pace, one image from
  the character's world). This generates the audition clip and later the clone
  reference, so it IS the voice. 2-3 sentences.
- `preset` + `instruct`: the day-one fallback. Preset is one of Qwen3-TTS's
  nine timbres (English-friendly: Serena and Vivian for women, Ryan, Aiden,
  Uncle_Fu for men); instruct is the delivery direction sent with every line.
- Picker metadata: `label`, `tone` (a few words), `gender`.

## 6. Audition clips

`voice-demos/gen_signature.py` (gitignored folder). Add the persona's greeting
to `LINES` (exact site copy) and the two voices to `VOICES`, then run it from
the sandbox in batches of 2 (each clip 15-25s; bash calls cap at 45s):

```bash
pip install --break-system-packages gradio_client
SIG_OUT=.../voice-demos/signature python3 gen_signature.py <persona>_<name> ...
```

It calls the `Qwen/Qwen3-TTS` HF Space `/generate_voice_design` endpoint and
skips existing files. ZeroGPU quota: anonymous is usually zero; ask Rye for an
HF token (Read scope) and pass `token=` via the `HF_TOKEN` env var the script
reads. Never write the token to a file. Present the clips to Rye; he approves
by ear and decides whether either becomes the character's default.

## 7. Optional upgrade: clone the approved voice

Preset+instruct is consistent but shares timbre across characters. To make an
approved voice fully unique: upload its clip once to DeepInfra
(`POST /v1/voices/add`, multipart, returns `voice_id`), then map
`"<personaId>/<name>": "<voice_id>"` into the `TTS_VOICE_MAP` Railway var.
`server/lib/tts.ts` prefers the mapped id automatically.

## 8. Tests

`client/src/components/companion/kokoroVoices.test.ts` iterates
`COMPANION_PERSONAS` automatically for form companions; chat personas must be
added to its `personaIds` lists by hand (the Ship's Cook pattern). The suite
enforces exactly two signature voices per persona, one of each gender, unique
namespaced keys, and non-trivial `design`/`instruct` text. Run:

```bash
set NODE_ENV=test&& npx vitest run client/src/components/companion/
```

(NODE_ENV=test matters on Rye's machine; see `regen-windows-env`.)

## 9. Ship checklist

1. `pnpm gate` (truncation + typecheck), voice tests green.
2. Commit `type(scope):` style, push to `main`, poll `pnpm railway:deploys`
   to SUCCESS.
3. Live-verify the picker data:
   `curl 'https://regencivics.earth/api/trpc/companion.voices?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22persona%22%3A%22<personaId>%22%7D%7D%7D'`
4. If touching the speak path, one sub-cent smoke test of `companion.speak`
   proves the paid path end to end.
5. SHIPPED_LOG entry; DOMAIN-LANGUAGE entry if the character introduces a new
   load-bearing term.

## Env flags and cost (facts as of 2026-07-18)

- `TTS_API_KEY`: DeepInfra key. Account is prepaid; zero balance makes
  `companion.speak` fail gracefully (client falls back to the free voice).
- `TTS_VOICES_LIVE=1`: master switch; unset hides signature voices everywhere
  and makes the key unbillable.
- `TTS_VOICE_MAP`: JSON of cloned voice ids (step 7).
- Cost: DeepInfra Qwen3-TTS is $20 per 1M characters. A spoken reply is
  ~300 chars (~$0.006); greetings and previews are cached server-side
  (`server/lib/tts.ts`) so repeated lines cost once. Rate limit
  `companion_tts` + 600-char cap bound abuse.
- Free Kokoro voices cost nothing at any scale and stay the default unless
  Rye explicitly promotes a signature voice.
