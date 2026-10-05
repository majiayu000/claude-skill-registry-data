---
name: visual-prompt-forge
description: Write model-specific image and video prompts for the shots in a storyboard or shot list (shots.json). Outputs copy-paste-ready prompts for stills (Midjourney, Flux, Ideogram, GPT Image, Nano Banana, Seedream) and motion video (Kling, Veo, Seedance, Hailuo), and a revision mode that reads critiques and re-emits prompts for only the shots that failed. Use when the user asks for prompts for their shots, storyboard or shot list, hands over shots.json, or asks to apply a critique to failed shots. Naming a generator is not enough on its own; the request has to be for prompts for storyboard shots. Composes with storyboard-architect upstream and visual-asset-critic downstream.
---

# Visual Prompt Forge

You are turning structured shot data into prompts that work in production. Each image generator rewards a different prompting style, short and high-signal for Midjourney, natural-language for Flux, paragraph-form for GPT Image, text-aware for Ideogram. A prompt that crushes in one will produce slop in another.

This skill adapts. Same shot, different syntax.

## When to use

Trigger when the user:

- Hands over a `shots.json` (or any structured shot list) and asks for prompts
- Asks for "image prompts," "Midjourney prompts," "video prompts," "generation prompts" for a storyboard or its shots
- Names target generators for a storyboard's prompts (Midjourney, Flux, Ideogram, GPT Image, Nano Banana, Seedream, Kling, Veo, Seedance, Hailuo)
- Wants the same shot adapted to multiple generators

Naming a generator is not enough on its own. A request to generate an image, or to use one
of these models for something other than storyboard shots, belongs to another tool.

If the user wants to build a storyboard from scratch (no shots.json yet), use `storyboard-architect` first, then chain into this skill.

## Where the tools and packs are

After `./install.sh`, the validators and helpers are in `~/.claude/shotkit-tools/` and the
brand packs are in `~/.claude/shotkit-brand-packs/`. A `--project` install puts both
under `./.claude/` instead. From a repo clone they are `tools/` and `brand-packs/`. The
commands below give the installed path first and the clone path second. The tools need
`pip install pyyaml jsonschema`.

## What you produce

For a given `shots.json` and a list of target generators, produce one file per generator,
inside a directory named for the round:

```
output/prompts/round-1/
├── midjourney.txt          # If targeted
├── flux.txt
├── ideogram.txt
├── gpt-image.txt
├── nano-banana.txt
├── seedream.txt
├── kling.txt               # Motion-aware video, default
├── veo.txt                 # Motion, dialogue/lipsync + native audio
├── seedance.txt            # Motion, multi-shot sequences
└── hailuo.txt              # Motion, budget iteration
```

Round 1 is the first pass. Revision mode writes `output/prompts/round-2/`, and so on.
The round in the path keeps every round's prompts on disk, so the prompt that produced a
frame is always there to check against it.

Each file is plain text, one prompt per shot, separated by a blank line and a `# shot_NN` comment. Designed for copy-paste workflows, drop into the generator's UI or pipe into an API.

## The five-layer prompt anatomy

Every prompt is composed from these layers. Read `references/prompt-anatomy.md` for the full theory. Quick version:

1. **Brand Lock**, palette, type, mood, "never" list (constant across project)
2. **Series Lock**, character/environment/lighting anchors (constant across storyboard)
3. **Shot Spec**, framing, angle, motion, subject (per shot)
4. **Text Layer**, **never in the prompt**, composited separately
5. **Generator Adapter**, model-specific syntax wrapper

The first four come from `shots.json` and the brand-lock. The fifth is what this skill applies.

## Workflow

### Step 1. Read inputs

You need:

- `shots.json` (required), the structured shot list
- `brand-lock.snapshot.md` (required), referenced from shots.json
- Target generators (required), ask if not specified

Validate before composing:

```bash
python ~/.claude/shotkit-tools/validate_shots.py output/
# from a repo clone:
# python tools/validate_shots.py output/
```

If the brand-lock is missing or `shots.json` does not validate, stop and tell the user.
Don't try to forge prompts from incomplete data.

If the tools are not on hand (a Claude.ai upload, or a single-skill install), read the
schema from `../storyboard-architect/templates/shots.schema.json` and check by hand. That
relative path only resolves when the skills sit side by side; when they don't, ask the
user for the schema rather than composing from memory of it.

### Step 2. Pick the adapters

For each target generator, read the matching adapter file:

- `adapters/midjourney.md`
- `adapters/flux.md`
- `adapters/ideogram.md`
- `adapters/gpt-image.md`
- `adapters/nano-banana.md`
- `adapters/seedream.md`
- `adapters/kling.md`      (motion video, default)
- `adapters/veo.md`        (motion video, dialogue/lipsync + native audio)
- `adapters/seedance.md`   (motion video, multi-shot sequences)
- `adapters/hailuo.md`     (motion video, budget iteration)

Each adapter file documents the prompting style, parameter syntax, and known pitfalls for that generator. You **must** read the adapter before writing prompts for it. Don't guess from training data, image-gen syntax has churned multiple times.

**`adapters/_capabilities.json` is the single source of truth for per-generator limits** (`max_prompt_words`, `supports_text_render`, `supports_motion`, `aspect_param`, and so on). Read it once at the start and respect those values when composing, and do not target motion on a stills-only generator.

`max_prompt_words` is a ceiling. The range in an adapter `.md` is the recommended target
and always sits inside that ceiling, so a `.md` saying "40 to 70 words" under a ceiling of
120 is guidance, not a conflict. Where a fact in a `.md` and a fact in the JSON genuinely
disagree, **the JSON wins**.

That rule is now enforced rather than trusted. `validate_capabilities.py` fails the
build when an adapter advertises more words than its ceiling, or when an adapter never
documents the `aspect_param` the JSON tells you to send. A parameter name that differs
between the two files would otherwise send the wrong name on every prompt.

### Step 3. Compose per shot

For each shot in `shots.json`, for each target generator:

1. Pull brand-lock palette, mood, "never" list
2. Pull series_lock character/environment/lighting
3. Pull shot framing/angle/motion/subject
4. **Strip any on_screen_text reference**, text never goes in the prompt
5. Apply the generator adapter's syntax wrapper
6. Append generator-specific parameters (aspect ratio, style flags, seed if applicable)

### Step 4. Write output files

One file per generator, into `output/prompts/round-{N}/`. Format:

```
# Storyboard: {project title}
# Generator: midjourney
# Model: {model_version from _capabilities.json}
# Aspect: 9:16
# Brand-lock: brand-lock.snapshot.md
# Run: {run_id from run.json}
# Round: 1

# shot_01, hook, 0.0-2.0s, MCU eye-level static
# params: {generator parameters, from the adapter}
{the prompt}

# shot_02, pain, 2.0-6.0s, MS eye-level push
# params: {generator parameters}
{the prompt}

...
```

The `#` lines are comments; the user copies just the prompt body. `copy-prompt.py`
parses this format, treating a comment line that names a shot as a block header and any
other comment inside a block as an annotation it will not copy.

Every adapter uses this one block format. Parameters go on a `# params:` line under the
block header. Never write them as a second `# shot_NN, ...` line: every line that starts
with `# shot_NN` opens a new block, and `validate_prompts.py` fails the file for a
duplicate block. Other annotation lines are `# variant:` (a variant template, nano-banana)
and `# covers: shot_03, shot_04` (the other shots a multi-shot sequence renders, seedance).

Record the run and round in the header, not a wall-clock "Generated" line. A timestamp in
the header made every file differ between two otherwise identical runs, which is a strange
thing to put in an artifact whose selling point is determinism.

### Step 4b. Append the round to run.json

After writing the files, append an entry to `run.json`'s `rounds` array: the round number,
`started_at`, a `reason`, and for each file its generator, path, SHA-256, and the shot ids
it covers.

```bash
shasum -a 256 output/prompts/round-1/*.txt
```

`rounds` is append-only. Add the new entry at the end and never edit an earlier one.
Everything else in `run.json` was written once by the architect and is never edited.

### Step 5. Hand off

Tell the user where the files are. Offer the next step:

> "Want me to QA the generated images against the storyboard? Use `visual-asset-critic` once you have the renders."

For paste-into-generator workflows, the user can pipe individual shots to the clipboard with the bundled helper:

```bash
python ~/.claude/shotkit-tools/copy-prompt.py output/prompts/round-1/midjourney.txt
python ~/.claude/shotkit-tools/copy-prompt.py output/prompts/round-2/revised-midjourney.txt --shot shot_03
# from a repo clone:
# python tools/copy-prompt.py output/prompts/round-1/midjourney.txt
# python tools/copy-prompt.py output/prompts/round-2/revised-midjourney.txt --shot shot_03
```

This is optional. The `.txt` files are also directly readable, and the user can copy any block by hand. The helper exists for the case where the operator is bouncing between the terminal and a generator UI repeatedly.

## Revision mode (closing the QA loop)

This is what `visual-asset-critic`'s structured output is for. When the user hands you `shots.json` plus one or more `critique.json` files (the machine-readable verdict the critic writes), don't re-forge the whole storyboard, re-emit prompts for **only the shots that failed**, with the fix already applied.

### Trigger

The user says "apply the critique", "revise the failed shots", "re-roll what didn't pass", or hands over an output tree containing `critiques/`.

### Workflow

1. Read every critique under `output/critiques/round-{N}/`, where N is the highest round
   present. Each file is one shot's verdict (`shot_id`, `verdict`, `issues[]`).
2. Skip any with `verdict: ACCEPT`. Those are done.
3. **Stop on `REJECT`.** A REJECT means the critic found a blocking issue, or three or more
   major ones: a failure with no clear fix path. Re-emitting a prompt for it pretends
   otherwise. List the rejected shots, say what the critic said about them, and ask the
   user how to proceed. Common answers are a change to the shot spec, a change to the
   brand-lock, or a different generator, and all three are decisions above this skill's
   pay grade.
4. For every `REVISE` shot, walk its `issues[]` and branch on `fix_type`:
   - **`prompt-level`**, recompose that shot's prompt with the change in `fix` applied
     (e.g. add the missing series_lock anchor). Re-emit it.
   - **`re-roll`**, keep the prompt identical; the generation was just a bad sample.
     Re-emit it with a `# fix [Technical, re-roll]` annotation saying to take 2-3 samples
     and pick the cleanest.
   - **`post-level`**, do **not** re-emit. The fix happens in compositing, not a new
     generation.
5. A shot whose issues are all `post-level` needs no new prompt. Leave it out of the
   revised file and add its id to `post_only_shots` on the new round entry in `run.json`.
   Saying it in chat is not recording it: that obligation has to exist on disk or the
   compositing step is a memory.
6. Re-apply the five-layer anatomy and the same adapter as the original run.

### Output

Write `output/prompts/round-{N+1}/revised-{generator}.txt` containing only the revised
shots, then append the round to `run.json`. Annotate each shot with what changed and why,
citing the issue:

```
# shot_03, reframe, 11.0-16.0s, MCU eye-level push, revision (was REVISE)
# fix [Series Lock, major]: added 'salt-and-pepper hair' to the character anchor (was missing)
# fix [Shot Spec, minor]: medium shot -> medium close-up
{the revised prompt}
```

The block header leads with the shot id, same as a full pass. `copy-prompt.py`
identifies a block by the shot id near the start of the line, and the revision file is the
one the operator pastes from most.

Tell the user which shots were revised, which need only post work, which were rejected,
and which were already ACCEPT. Then they generate the revised shots and run
`visual-asset-critic` again.

### Determinism, and its limits

Given the same `shots.json`, the same brand-lock, and the same critique, this should
produce the same revised prompt. Nothing in the file format fights that any more: no
wall-clock stamps, no random ordering.

What the format cannot guarantee is the judgement in between. Applying a `fix` field means
reading a sentence of English and editing prose, so hold yourself to the narrowest edit
that satisfies the fix and leave every other layer byte-identical. If you find yourself
rewriting a prompt the critique did not ask you to touch, stop: that is drift, and it will
read as a mystery six shots later.

## Hard rules

These are non-negotiable. Violating them produces broken output even if the prompt looks fine.

### Rule 1. Text is never in the prompt

If the shot has `on_screen_text: "text_03"`, the prompt does NOT contain the text content. Text is composited separately. The only exception: Ideogram, where text-in-image is the reason you'd choose it, but even then, treat it as an explicit override flagged in rationale.

### Rule 2. Brand colors never in shot subject prose

Colors come from the series_lock color_grade and the brand_lock palette. They get rendered into the prompt by the adapter. Don't write "deep navy blazer" in the shot subject if "deep navy" is already in the palette, that's a duplicated description and produces oversaturation.

### Rule 3. Series_lock anchors are verbatim

The series_lock `environment`, `lighting`, and `color_grade` strings flow into every
prompt **verbatim**. This is what produces visual consistency across shots. If you
paraphrase or vary, shots stop matching each other.

Verbatim means the whole string, unedited. Not "the same idea in better prose". The
failure mode is specific and easy to walk into: you are writing fluent descriptive
English, `environment` is "minimalist home office, white walls, oak desk, single
houseplant", and it reads more naturally as "a minimal home office with white walls and
an oak desk". That is drift. The frames stop matching, and it stays invisible until you
line up six shots and see six different rooms.

Capitalising the first letter to start a sentence is fine, because the check is
case-insensitive. "Minimalist home office, white walls, oak desk, single houseplant."
satisfies the rule and reads like a sentence. Nothing else may change: no reordering, no
dropped clause, no synonym, no inserted adjective.

`character` is a warning rather than an error, because a shot with no person in it can
legitimately leave it out. When the shot has a person, it is verbatim too.

A shot may override `environment_ref` or `lighting_ref`, with its reason in the rationale.
Then that shot's prompt carries the override text verbatim in place of the series anchor.
The validator checks the override text for that shot and skips the series anchor.

This rule is enforced now, not trusted:

```bash
python ~/.claude/shotkit-tools/validate_prompts.py output/
# from a repo clone:
# python tools/validate_prompts.py output/
```

Paraphrasing an anchor reads as good writing, which is why this rule needs a check rather
than care alone.

### Rule 4. Adapters are the source of truth on syntax

If your training data says Midjourney uses `--style 4a` and the adapter file says `--style raw`, the adapter wins. Image-gen syntax changes monthly. The adapter is current; your training is not.

### Rule 5. Prompts must be reproducible

Every prompt is composed from the same inputs the same way. If two consecutive runs produce different prompts for the same shot, the skill is broken. Determinism is the whole point.

## Reference files

- `references/prompt-anatomy.md`, the five-layer model in depth
- `references/consistency-locks.md`, how series_lock prevents shot drift
- `references/failure-modes.md`, common image-gen failures and their prompt-side fixes

## Adapters

One file per generator. Read these on demand, only for the generators being targeted.

| File | Generator | Strength |
|---|---|---|
| `adapters/midjourney.md` | Midjourney v7+ | Aesthetic, cinematic |
| `adapters/flux.md` | Flux 2 / Flux 1.1 Pro | Photorealism |
| `adapters/ideogram.md` | Ideogram v3 | Text in image (override only) |
| `adapters/gpt-image.md` | GPT Image 1.5 / 2 | Prompt accuracy, spatial reasoning |
| `adapters/nano-banana.md` | Nano Banana 2 (Gemini 3.1 Flash Image) | Edit fidelity, inpainting |
| `adapters/seedream.md` | Seedream 4.5 | High-volume, cost-efficient |
| `adapters/kling.md` | Kling 3.0 | Motion video, default (best camera motion per dollar) |
| `adapters/veo.md` | Veo 3 | Motion video, dialogue/lipsync + native audio |
| `adapters/seedance.md` | Seedance 2.0 | Motion video, multi-shot sequences |
| `adapters/hailuo.md` | Hailuo 02 Pro | Motion video, budget iteration |

## Quality bar

Run the validator. Do not eyeball this list.

```bash
python ~/.claude/shotkit-tools/validate_prompts.py output/
python ~/.claude/shotkit-tools/copy-prompt.py output/prompts/round-1/flux.txt --list
# from a repo clone:
# python tools/validate_prompts.py output/
# python tools/copy-prompt.py output/prompts/round-1/flux.txt --list
```

`validate_prompts.py` checks the mechanical half:

- the header names the storyboard, generator, aspect, brand-lock, run, and round
- the generator is a real id in `_capabilities.json`
- the header aspect matches `project.aspect`
- no prompt exceeds that generator's `max_prompt_words` ceiling
- a full pass covers every shot; a revision file covers a subset of real shots
- no shot block is duplicated, and none has a header with no body
- **Rule 1**: no on-screen text copy appears in any prompt
- **Rule 3**: `environment`, `lighting`, and `color_grade` appear verbatim, with the
  character anchor as a warning

What it cannot check, and you still have to:

- [ ] One output file per requested generator
- [ ] On a revision pass, the shots you left out are accounted for as ACCEPT, post-only,
      or rejected, and you said which is which
- [ ] Generator-specific parameters are right for the surface the user will paste into
- [ ] The round is appended to `run.json` with a hash per prompt file
- [ ] The prompt actually describes the shot, which is the part no validator will ever do

## Examples

`examples/one-shot-all-adapters/` contains a single shot rendered across seven adapters
side-by-side: the six stills generators plus Kling. Use it to calibrate output quality.
The three remaining motion adapters (Veo, Seedance, Hailuo) have no worked example yet;
their `.md` files carry a worked prompt each in the meantime.

For a complete two-round output tree, prompts and frames and critiques together, see
`../visual-asset-critic/examples/worked-run/`.
