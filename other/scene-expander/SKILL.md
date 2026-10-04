---
model_tier: inherit
name: scene-expander
description: "When expanding a one-line idea into the 12-block Cinematic Scene Blueprint — optional dialogue + ambient. Triggers 'expand this scene', 'blueprint for X'. 11-block refine → video-director."
personas:
  - hollywood-director
domain: product
workspaces:
  - small-business
packs:
  - ai-video
lifecycle: experimental
trust:
  level: experimental
install:
  default: false
  removable: true
---

# scene-expander

> Expand a one-line idea or script line into the **Cinematic Scene
> Blueprint** — 12 labeled blocks consumed by
> [`parse-blueprint.sh`](./scene-blueprint.schema.yaml). Picks
> `hollywood-director` for live-action; hands off animated beats to
> [`pixar-storyteller`](../pixar-storyteller/SKILL.md). Output is
> provider-agnostic — provider tuning is
> [`motion-choreographer`](../motion-choreographer/SKILL.md).

## When to use

- A script line, idea, or beat needs a full blueprint before any
  adapter runs.
- A `/video:from-script` run is parsing `## Scene N` headings and
  needs each scene expanded.

Do NOT use when:

- The brief is already an 11-block cinematic prompt → call
  `video-director` directly to refine it.
- The brief is a static graphic → `canvas-design`.
- Provider-specific token tuning is the next step →
  `motion-choreographer`.

## Procedure

### Step 0: Inspect

1. Read the input line. Classify as **live-action / photoreal** or
   **animated / stylized**.
2. Live-action → load `hollywood-director` voice. Animated → hand
   off to [`pixar-storyteller`](../pixar-storyteller/SKILL.md) (its
   procedure carries the acting / beat-decomposition lens). Hybrid
   (live-action with VFX) → `hollywood-director`; record VFX intent
   in ENVIRONMENT.
3. Check for an existing `character.json` lock under
   `agents/reference/ai-video/<project>/characters/`.

### Step 1: Emit the 12 blocks

One label per line. Order is mandatory.

1. **STYLE** — stylistic anchor (live-action: film stock + decade,
   e.g. "Kodak 5219, 2015"; animated: specific film + year).
2. **SUBJECT** — character read; verbatim identity tokens when a
   lock exists.
3. **ENVIRONMENT** — location, time-of-day, weather, era; what the
   world does in response to the subject.
4. **ACTION** — anticipation / action / reaction with beat counts
   (`0.5s / 1.2s / 0.8s`). No adjective paragraphs.
5. **CAMERA** — position, height, distance, move as an INTENT
   class (static hold, push-in, pull-back, lateral track, handheld
   drift, orbit). Intent vocabulary, never one provider's move
   grammar — the per-provider encoding happens in
   [`motion-choreographer`](../motion-choreographer/SKILL.md).
   Off-axis when on-axis is default.
6. **LENS** — focal length in mm and aperture intent. "Cinematic"
   alone fails. mm + aperture are cinematography units, not provider
   tokens — they stay.
7. **LIGHTING** — key / fill / back / practical named; "golden
   hour" requires a sun angle.
8. **MOOD** — one emotional read.
9. **DIALOGUE** — optional. If present: `speaker: "line"`, one per
   line. Marks `audio: native` capability requirement.
10. **AMBIENT SOUND** — optional. Layer list (wind, traffic,
    crowd, ocean). Marks `audio: native` or routes to ffmpeg mux.
11. **DURATION** — seconds (integer or one decimal). Free value;
    per-provider clip-length clamping is the encoder's concern, not
    the blueprint's.
12. **NEGATIVE** — clichés to reject, load-bearing order top-first.
    Always names: centered framing, symmetric composition, generic
    "cinematic", soap-opera contrast.

### Step 2: Self-review

1. Live-action / animated classification consistent across blocks?
2. LENS present with mm (live-action) OR stylistic anchor with
   film+year (animated)?
3. LIGHTING with a direction?
4. ACTION names beat counts, not adjectives?
5. DIALOGUE / AMBIENT SOUND present → the run requires `audio:
   native` adapter OR ffmpeg-mux fallback declared.
6. NEGATIVE ≥ 4 entries, load-bearing top?
7. SUBJECT verbatim from `character.json` when a lock exists?

Any "no" → revise that block.

### Step 3: Validate

1. Pipe output through `scripts/ai-video/lib/parse-blueprint.sh` —
   exits 0 and emits valid adapter-contract JSON.
2. No provider tokens (no aspect / model / duration flags).

## Output format

1. **`scenes/<id>/prompt.txt`** — 12 labeled blocks, ready for
   `parse-blueprint.sh`.
2. **`scenes/<id>/blueprint.json`** — parser output, adapter-stdin
   ready.
3. **`scenes/<id>/review.md`** — one-paragraph rationale per
   non-obvious choice.

## Gotcha

- The model wants to skip optional DIALOGUE / AMBIENT SOUND blocks
  silently — if they could plausibly belong, emit them; the parser
  treats missing blocks as `null`, not as an error.
- Live-action without LENS mm fails the parser's strict mode.
- Animated without a film+year anchor in STYLE drifts on every run.
- ACTION written as "the character does X dramatically" fails —
  adapters need verbs with beat counts.
- DIALOGUE forces `audio: native` requirement — flag this to the
  orchestrator so it picks an audio-native adapter
  (`capability.audio = native`).

## Do NOT

- Do NOT emit provider tokens — that is `motion-choreographer`.
- Do NOT shape any block toward one provider's prompt grammar — the
  blueprint is the decoupling layer; the anti-leak schema test scans
  it for provider tokens.
- Do NOT skip the blueprint parser validation step.
- Do NOT paraphrase identity tokens when a lock exists.
- Do NOT mix live-action LENS prescriptions with animated STYLE
  anchors in the same scene — pick one mode.

## Policies

Paths, enforcement model, and the full set: the
[media policy preamble](../../../agents/settings/policies/media/README.md).

The 12-block Cinematic Scene Blueprint is the policy choke point — every downstream skill (`motion-choreographer`, `video-director`) inherits whatever the blueprint encodes. Before emitting:

- **`likeness`** — when the SUBJECT block names or visually identifies a real person.
- **`public-figures`** — when the SUBJECT block is a recognised public figure.
- **`brand-impersonation`** — when STYLE / ENVIRONMENT references a recognised brand's visual identity.
- **`style`** — when STYLE anchors to a named living artist or studio as the primary signature.
- **`disclosure`** — every distributed blueprint output carries the AI-generation disclosure downstream.

Refuse-and-surface at the blueprint layer; do not push policy questions down to the adapter.

