---
model_tier: inherit
name: song-to-script
description: "Turn an audio track into a timed `## Scene N` script: song sections → per-scene durations, auto mode adds mood + lip-sync lines. Triggers 'music video', 'from the song', 'cut to the beat'."
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

# song-to-script

> Turn a song into `<project>/script.md` — a sequence of `## Scene N`
> blocks whose `duration:` values sum to the track length and whose cut
> points land on real section boundaries. Consumed by
> [`/video:from-song`](../../commands/video/from-song.md), then handed
> to [`scene-expander`](../scene-expander/SKILL.md) and
> [`video-director`](../video-director/SKILL.md). Never invents timing —
> every boundary comes from the audio probe, and the probe's `method`
> tells this skill how musical (or not) those boundaries actually are.

## When to use

- A music-video run needs scenes cut to the song (`/video:from-song`).
- An existing script must be **re-timed** to a track after the edit
  drifted from the beat (the named second consumer — re-time without a
  full re-author).

Do NOT use when:

- The operator already supplies a `## Scene N` script with `duration:`
  values — feed it straight to `scene-expander`.
- There is no audio — use the operator brief with `scene-expander`
  directly.

## Inputs

- **Audio analysis** — adapter-first, probe as the floor:
  - **Analysis adapter** (when an `audio-analysis` provider is
    configured — see
    [`audio-adapter-contract.md`](../../scripts/ai-video/lib/audio-adapter-contract.md)):
    `{bpm, beats, downbeats, sections:[{start,end,label,energy?}]}` —
    real musical structure. Beats/downbeats become the candidate cut
    grid; section labels are musical (`verse`, `chorus`, …).
  - **Audio probe** — JSON from
    [`scripts/ai-video/lib/probe-audio.sh`](../../scripts/ai-video/lib/probe-audio.sh):
    `{duration, method, warning?, sections:[{start,end,energy,label}]}`.
    - `method: silence` — boundaries are real quiet gaps; trust them as cuts.
    - `method: rms` — boundaries are energy-delta inflections; usable but
      coarse.
    - `method: interval` — **the track is structurally flat** (brick-walled
      / sustained); sections are fixed-interval, NOT musical. When `method`
      is `interval` (or `warning` is set), the emitted script header states
      that timing is interval-based and the operator should pass
      `--scene-durations` for musical sync. Never present interval cuts as
      beat-synced.
- **Model capabilities** — the chosen video model's renderable envelope
  from the multiplexer manifest:
  `scripts/ai-video/adapters/<provider>.sh capability --model <id>` →
  `{min_duration, max_duration, audio_sync, aspect, verified}`. Scene
  durations MUST land inside `[min_duration, max_duration]`; a
  `verified: false` manifest entry is surfaced in the report, never
  trusted silently.
- **Mode** — `brief` (operator text is the creative source) or `auto`
  (infer mood + action from energy).
- **Brief** (brief mode only) — free text: story, settings, look.
- **Character lock** (optional) — `<project>/character.json` if a human
  subject was locked. **Absent is normal** — abstract / landscape /
  visualiser videos have no locked subject; see Step 2.

## Procedure

### Step 1: Map sections → scenes (capability-clamped, beat-aligned)

One `## Scene N` per analysis section. `duration:` = `end - start`
(rounded to 0.5 s). Then **clamp the plan to the chosen model's
renderable envelope** — read `min_duration` / `max_duration` from the
model-capabilities manifest (`<provider>.sh capability --model <id>`),
falling back to the provider tuning for single-model adapters:

- **Section shorter than `min_duration`** → merge into its neighbour.
  With beat data, merge toward the neighbour that keeps the joined cut
  on a **downbeat** (else any beat); without beat data, merge into the
  shorter neighbour.
- **Section longer than `max_duration`** → split into sub-scenes. With
  beat data, place every split point on the **nearest downbeat** (else
  beat) to the equal-division point — never mid-beat; without beat
  data, split equally.
- **No valid plan exists** (e.g. the whole song is shorter than
  `min_duration`, or a section cannot be split onto any beat inside the
  envelope) → **halt and surface the conflict** with the model id and
  the violated bound — an unbuildable plan never reaches the renderer.

Every emitted scene satisfies
`min_duration ≤ duration ≤ max_duration`. When the manifest entry is
`verified: false`, say so in the report — the envelope is
documented-best-effort, not a smoke-traced fact.

### Step 2: Assign mood + action

First decide the **subject mode**:

- **Character mode** — `character.json` exists: every scene's `action:`
  names the locked subject, never a fresh description.
- **Style mode** — no `character.json`: scenes describe setting, palette,
  and motion continuity (the recurring *look*), not a person. This is the
  valid abstract / landscape / visualiser path — do not invent a human
  subject to fill the slot.

Then pick the **prompt source per segment — the modality switch**:

- **Lyric segment** (the vocal map places ≥1 transcribed line inside
  it) → the scene prompt derives from the **lyric line itself**: its
  imagery, subjects, and verbs seed `mood:` + `action:` (in character
  mode, acted by the locked subject; in style mode, rendered as
  setting / weather / palette — never an invented human). The line
  lands in `dialogue:` per Step 3.
- **Instrumental segment** (no vocal-map line) → the scene prompt
  derives from the **audio features**: section `label` + `energy` via
  the intent table below. Never recycle a lyric from another segment
  into an instrumental one.

Then assign per scene:

- **Brief mode** — distribute the brief's beats across scenes in order;
  the modality switch still applies (lyric segments quote the brief's
  matching beat through the lyric's lens), and energy modulates pacing.
  Do not add story the brief did not state.
- **Auto mode** — derive mood per section from `energy` and `label`
  (probe labels and musical labels from the analysis adapter both map):

  | label / energy | default scene intent |
  |---|---|
  | intro / low | establishing wide, slow camera, calm subject/scene |
  | verse / mid | narrative motion, medium framing, follow the subject |
  | build / rising | approach, tightening framing |
  | chorus · drop / peak | dynamic motion, weather/FX, fast push |
  | bridge · breakdown / dip | close-up / detail, quiet, single light source |
  | outro / fade | pull-back, resolve, hold |

**Energy → cut frequency + motion intensity.** Section energy (0..1,
relative to the track mean) drives both how often the edit cuts and how
hard the camera moves — chorus = faster cuts / more motion:

| energy vs. track mean | cut length target | `camera:` motion intensity |
|---|---|---|
| ≥ mean + 0.10 (chorus / drop) | short — split the section toward `min_duration`, one scene per 1–2 downbeat bars | fast push / whip / handheld shake |
| within ±0.10 of mean (verse / build) | medium — one scene per section or per 4-bar phrase | steady dolly, slow tighten |
| ≤ mean − 0.10 (breakdown / outro) | long — merge toward `max_duration`, hold shots | locked-off or slow drift |

High-energy splitting and low-energy merging both stay inside the
Step 1 capability envelope and land on downbeats — the energy table
chooses *where inside the envelope* a scene length falls, never
outside it.

### Step 3: Vocal map — transcribe, never guess (vocal tracks)

```
LYRIC TIMING AND SINGER COME FROM THE TRANSCRIBED AUDIO, NEVER FROM A
BRIEF / STORY SKELETON OR A GUESSED STRETCH. NEVER PUT ONE SINGER'S
LINE ON ANOTHER SINGER'S SCENE.
```

When the track has vocals and the run intends lip-sync, build a
**vocal map** from the real audio before assigning any `dialogue:`:

1. **Transcribe** the audio to timestamped lines. Adapter-first: a
   configured `lyrics` provider (e.g.
   [`audio-adapters/whisperx.sh`](../../scripts/ai-video/audio-adapters/whisperx.sh))
   returns word-level timestamps **plus per-line diarization labels**
   (`SPEAKER_00`, …, or `"?"` when ambiguous):
   ```bash
   echo '{"audio_path":"<vocal-stem-or-song>"}' \
     | scripts/ai-video/audio-adapters/whisperx.sh analyze
   ```
   No lyrics provider configured → OpenAI `/v1/audio/transcriptions`
   (`response_format=verbose_json` → `segments[].{start,end,text}`) or
   local whisper as before (no speaker labels — every line starts as
   `"?"`). Either way the transcript is the only source of lyric timing.
2. **Label the singer** per line — map diarization labels (or unlabeled
   lines) to cast names via the operator's who-sings reference (a
   roster, a brief that names who sings which line, or a character
   cast): one diarization label ↦ one cast name, consistently. If a
   line's singer is genuinely ambiguous (label `"?"`, mixed-speaker
   line, or no roster match), keep `singer: "?"` and surface it —
   never guess a singer to fill the slot.
3. **Emit** `<project>/vocal-map.json`:
   `[{start, end, text, singer}]`, timing verbatim from the transcript.
4. **Validate** — run the ground-truth enforcer before handing the map
   to the sign-off gate:
   ```bash
   scripts/ai-video/lib/validate-vocal-map.sh <project>/vocal-map.json \
     <project>/transcript.json --roster "<cast names>"
   ```
   It rejects re-timed lines, lyrics not in the transcript, and missing
   singers (exit 7, specific line named). A red validator is a halt —
   fix the map, never bypass.
5. **Place lines into the matching scene's** `dialogue:` block using the
   transcript timing, tagged with the singer (`singer: "<line>"`). A
   scene's lip-sync subject MUST be the line's labelled singer; a
   `"?"` line gets NO lip-sync scene until the operator resolves it.

No vocals / no transcript / no lip-sync intent → leave `dialogue:` empty;
the scene is performance / B-roll. **Never fabricate lyrics**, **never
re-time a line off the brief**, and in style mode `dialogue:` stays empty
(lip-sync needs a character subject). The `/video:from-song` sign-off
gate (its Step 6) shows this map for approval before any render.

### Step 4: Emit + reconcile

Write `<project>/script.md` (and `<project>/vocal-map.json` when the
track has vocals). Report the delta, the section→scene map, **the probe
`method`** (so the operator sees whether cuts are silence-derived,
energy-derived, or interval-fallback), **and whether lyric timing is
transcript-derived** (it must be — never brief-derived). If the sum
cannot be reconciled (e.g. provider max-duration forces more time than
the song has), **halt and surface the conflict** — do not pad silently.

### Step 5: Validate before handoff

Concrete checks (all must pass before the script is handed to
`scene-expander`):

- **Assert** `Σ(duration) == probe.duration` within ±1.0 s; report the
  exact delta. A larger delta → halt, do not pad.
- **Verify** every scene boundary equals a probe section boundary (or a
  `--scene-durations` value) — no invented cut points.
- **Confirm** no scene `duration:` exceeds the model's `max_duration`
  or falls below `min_duration` (model-capabilities manifest, or the
  provider tuning for single-model adapters).
- **Verify** every lyric-segment scene derives its prompt from its own
  vocal-map line and every instrumental scene from audio features — no
  cross-segment lyric recycling (modality switch).
- **Ensure** every `## Scene N` carries all five keys (`duration` ·
  `mood` · `action` · `camera` · `dialogue`), and that `dialogue:` is
  empty in style mode.

## Output format

1. `script.md` opens with the derivation header —
   `# <project> — derived from <song-file> (<mode> mode · cuts: <method>)`
   — so the probe `method` stays visible downstream.
2. One `## Scene N` block per cut carrying exactly the keys
   `duration` · `mood` · `action` · `camera` · `dialogue` —
   `scene-expander` consumes this verbatim; keep the keys exact.
3. `dialogue:` stays empty unless operator-supplied lyrics cover the
   section — detected vocal energy alone never fills it.

```markdown
# <project> — derived from <song-file> (<mode> mode · cuts: <method>)

## Scene 1
duration: 6.0
mood: establishing, cold, pre-storm
action: <subject from character.json, OR style description in style mode>
camera: slow push-in
dialogue:

## Scene 2
duration: 4.5
mood: build, rising tension
action: close on <subject / detail>, wind picking up
camera: handheld tighten
dialogue:
  - "<subject>: \"<lyric line for this section, if any>\""
```

## Gotcha

- **`method: interval` is the brick-walled-master signal, not a bug.**
  A compressed modern master has near-constant RMS and no silence, so the
  probe degrades to fixed intervals. That is the honest floor — surface
  it and point the operator at `--scene-durations`; never dress interval
  cuts up as beat-synced.
- **A vocal section without supplied lyrics is B-roll, not lip-sync.**
  Detected vocal energy alone does not authorise `dialogue:` — only
  operator-supplied lyrics do.
- **Style mode is the default for a no-character run**, not an error
  path. Landscape / abstract / visualiser videos never get a fabricated
  human subject.

## Do NOT

- **Do NOT invent timing.** Every cut maps to a probe boundary or a
  `--scene-durations` value — never to taste.
- **Do NOT present `interval`-fallback cuts as beat-synced.** Always
  surface the probe `method`.
- **Do NOT emit a clip outside the provider's min/max duration** —
  split/merge in Step 1 instead.
- **Do NOT fabricate lyrics or story** beyond the brief / detected vocals.
- **Do NOT invent a human subject** in style mode; defer identity to
  `character.json` only when a lock exists.
- **Do NOT pad a unreconcilable timing sum** — halt and surface it.

## See also

- [`/video:from-song`](../../commands/video/from-song.md) — the command
  that drives this skill
- [`scene-expander`](../scene-expander/SKILL.md) — consumes the emitted
  script
- [`character-consistency`](../character-consistency/SKILL.md) — supplies
  the locked subject referenced in `action:` (character mode only)
