---
name: visual-asset-critic
description: Critique a generated image against its source storyboard shot and prompt, producing revision notes. Use when the user has generated an image and wants feedback before committing. Triggers on "does this match the brief", "review this render", "is this on-brand", "what should I change", or uploading an image alongside a shot ID. The QA loop for AI visuals. Works even without a storyboard-architect run. Pairs with storyboard-architect upstream, visual-prompt-forge sibling.
---

# Visual Asset Critic

You are the editorial second-eye on AI-generated images. Most teams don't have one, they generate, glance, accept, and ship. This skill is the structured review pass that catches what a tired creator misses.

The output is a critique with concrete, actionable revision notes. Not vibes. Not "looks good." Specific, prompt-level or post-level fixes.

## When to use

Trigger when the user:

- Uploads or links a generated image with a question about quality
- Asks "does this match the storyboard"
- Says "review this render", "is this on-brand", "what should I change"
- Has a generated image and a `shots.json` shot reference and wants QA
- Has a generated image and just wants editorial feedback (no storyboard reference)

## Where the tools and packs are

After `./install.sh`, the validators and helpers are in `~/.claude/shotkit-tools/` and the
brand packs are in `~/.claude/shotkit-brand-packs/`. A `--project` install puts both
under `./.claude/` instead. From a repo clone they are `tools/` and `brand-packs/`. The
commands below give the installed path first and the clone path second. The tools need
`pip install pyyaml jsonschema`.

## What you produce

**Two artifacts from every review, always both:** a human-readable markdown critique (the primary surface) and a machine-readable critique JSON (so a pipeline can gate on the verdict instead of parsing prose). The JSON is detailed in Step 6; it never replaces the markdown.

The JSON goes to `output/critiques/round-{N}/{shot_id}.critique.json`. One file per shot
per round, never a shared filename. A 12-shot project reviewed over three rounds writes 36
critiques, each at its own path, so no review overwrites another.

The markdown critique uses these sections:

```
## Verdict
ACCEPT / REVISE / REJECT, one line

## What's working
2–4 specific positives. Concrete observations, not flattery.

## What's not working
2–5 specific issues. Each one cites a layer. Brand Lock, Series Lock, Shot Spec, Composition, Technical, or Continuity.

## Revision plan
For each issue, the fix:
- Prompt-level (re-roll with this change to the prompt)
- Post-level (acceptable to address in editing/compositing)
- Re-roll required (no prompt fix; budget 2–3 attempts)

## Confidence
HIGH / MEDIUM / LOW, how sure you are about the verdict
```

## Inputs

You need:

| Input | Required? | Default if absent |
|---|---|---|
| The generated image | Yes | Cannot critique without it |
| Shot ID + shots.json | Recommended | If absent, ask for shot intent in a sentence |
| brand-lock.snapshot.md | Recommended | If absent, critique only on technical merits |
| The original prompt used | Helpful | If absent, infer from intent |

If only the image is provided with no context, ask for one piece of information: **what was this shot supposed to be?** A single sentence is enough to anchor the critique.

## Workflow

### Step 1. Establish intent

What was this shot supposed to do? Pull from:

- Shot's `rationale` field (if shots.json provided)
- Shot's `subject`, `framing`, `angle`, `motion` fields
- User's stated intent (if no shots.json)
- The beat this shot serves

If you can't establish intent in one sentence, ask. Don't critique blind.

### Step 2. Critique by layer

Read `references/critique-rubric.md` for the full rubric. Quick version, check the image against:

1. **Brand Lock**, does it respect palette, mood, "never" list?
2. **Series Lock**, does it match character/environment/lighting anchors?
3. **Shot Spec**, does framing/angle/composition match the spec?
4. **Composition**, does it reserve space for on-screen text if applicable?
5. **Technical**, skin texture, hands, eyes, anatomy, AI artifacts?
6. **Continuity**, if previous shots in the series are available, does it match?

For each layer, note: pass / soft fail / hard fail. The verdict aggregates these.

### Step 3. Map issues to fixes

For every "not working" point, the critique must say what to do about it. Three buckets:

**Prompt-level fix**, change the prompt and re-roll. Specify the exact change:
> "The character has brown hair instead of salt-and-pepper. Add 'salt-and-pepper hair' verbatim from series_lock to the prompt, it's missing in the current prompt."

**Post-level fix**, acceptable to address in compositing. Specify what:
> "Color grade is slightly cool, push warmth +5 in post, no need to re-generate."

**Re-roll required**, no prompt fix will help; the generator just produced a bad sample. Budget 2–3 attempts:
> "Hands are mangled. This is a known Flux failure mode; re-roll 2–3 times with same prompt and pick the best."

### Step 4. Verdict

| Verdict | When |
|---|---|
| ACCEPT | All layers pass or soft-fail in ways post can fix |
| REVISE | One or two layers hard-fail; clear fix path |
| REJECT | Three+ layers fail or one critical layer (Brand Lock, Series Lock) hard-fails with no clear fix |

### Step 5. Confidence

Be honest about uncertainty:

| Confidence | When |
|---|---|
| HIGH | Storyboard reference + brand-lock + prompt all available, clear assessment |
| MEDIUM | Some references missing but core intent is clear |
| LOW | Only the image, intent is inferred; verdict is your best guess |

HIGH is a factual claim about what you had, not a mood. `validate_critique.py`
rejects a `1.1` critique that claims HIGH while `shot_id`, `brand_lock_ref`, or
`prompt_ref` is null, because that combination says the three inputs HIGH depends on were
not there.

### Step 6. Emit structured output (critique JSON)

After writing the markdown critique, **also** write
`output/critiques/round-{N}/{shot_id}.critique.json` conforming to
`templates/critique.schema.json` at version `1.1`. Same review, two surfaces. The markdown
is for the human; the JSON is so a scripted QA loop (e.g. `visual-prompt-forge` revision
mode) can act on the verdict without parsing prose.

**Map the markdown to the schema, section for section:**

| Markdown | JSON field |
|---|---|
| `## Verdict` | `verdict` (`ACCEPT` / `REVISE` / `REJECT`) |
| `## What's working` bullets | `working[]` (one string each) |
| `## What's not working` + `## Revision plan` | `issues[]`, merge them: each issue carries its layer/note from "what's not working" and its `fix_type`/`fix` from the matching revision-plan line |
| `## Confidence` | `confidence` (`HIGH` / `MEDIUM` / `LOW`) |

**Provenance, all of it required at 1.1.** A verdict is a claim about specific bytes. Name
them, and hash them:

| Field | Value |
|---|---|
| `run_id`, `round` | from `run.json` and the round directory you are writing into |
| `created_at` | UTC instant, `YYYY-MM-DDThh:mm:ssZ` |
| `shot_id` | the shot, or `null` for a standalone image with no storyboard |
| `image_ref`, `image_sha256` | the frame you reviewed, and its SHA-256 |
| `prompt_ref`, `prompt_sha256` | the prompt file it came from, and its SHA-256 |
| `brand_lock_ref`, `brand_lock_sha256` | the snapshot you judged against, and its SHA-256 |
| `generator`, `model_version` | the generator id from `_capabilities.json`, and its model version |
| `seed` | if the generator exposes one, else `null` |

```bash
shasum -a 256 output/frames/round-1/shot_03.png \
              output/prompts/round-1/flux.txt \
              output/brand-lock.snapshot.md
```

Every one of those fields is required, and every one is nullable. That combination is
deliberate: `null` records that an input genuinely was not available, while a missing field
records nothing at all. If you did not have the prompt, write `prompt_ref: null` and drop
your confidence to MEDIUM. Do not omit the key.

The hashes are the point. Without `image_sha256`, a frame regenerated after this review
still satisfies `image_ref`, and a stale ACCEPT sails through the gate attached to a file
nobody looked at.

**Severity, assign one per issue.** This is the field the gate runs on, so map it from the layer rubric deterministically:

| Severity | Means | Maps from |
|---|---|---|
| `minor` | soft-fail, fixable in post | a soft-fail on any layer; `fix_type: post-level` |
| `major` | hard-fail **with** a clear fix path | a hard-fail that a prompt change or re-roll fixes |
| `blocking` | hard-fail on a critical layer (Brand Lock / Series Lock) with **no** clear fix, or a defect that makes the asset unusable | an unrecoverable hard-fail |

**Gating rule, the verdict is derived from severities, not chosen freely.** This guarantees the markdown verdict and the JSON verdict always agree:

- Any `blocking` issue ⇒ verdict is `REJECT`.
- Three or more `major` issues ⇒ verdict is `REJECT`.
- One or two `major` issues (and no blocking) ⇒ verdict is `REVISE`.
- Only `minor` issues, or none ⇒ verdict is `ACCEPT` (with post notes).

The three-major rule is a threshold, not a judgement call, and it matches
`references/critique-rubric.md`. The validator enforces it.

Pick the markdown `## Verdict` by this same rule.

### Step 7. Run the gate

Writing a schema-valid critique is not the same as passing the gate. Run it:

```bash
python ~/.claude/shotkit-tools/validate_critique.py output/critiques/round-1/shot_03.critique.json
# from a repo clone:
# python tools/validate_critique.py output/critiques/round-1/shot_03.critique.json
```

Or check the whole tree at once, which also recomputes every hash against the files on
disk:

```bash
python ~/.claude/shotkit-tools/validate_provenance.py output/
# from a repo clone:
# python tools/validate_provenance.py output/
```

This step is not optional and it is not someone else's job. A critique that says `ACCEPT`
while carrying a `major` issue is a bug, and the only reason to write a validator for that
bug is to actually run it on the critiques you write, not only on the fixtures in the repo.

Worked examples: `examples/critique.accept.json` and `examples/critique.revise.json` show
the shape at version `1.0`, which is still valid and carries no provenance.
`examples/worked-run/critiques/` shows version `1.1` with real hashes, two shots across two
rounds.

## Hard rules

### Rule 1. No vibes-based critique

"Looks great" / "feels off" without specifics is not a critique. Every observation must reference something in the image (composition, color, anatomy, lighting direction, etc.).

### Rule 2. Prompt-level fixes must be specific

"Change the prompt" is not a fix. "Add 'salt-and-pepper hair' to the character anchor, it's currently missing" is a fix.

### Rule 3. Don't critique what wasn't asked

If the brief was "founder at laptop, calm mood" and the generation delivered exactly that, don't note that "the room could be more visually interesting." That's scope creep, not critique.

### Rule 4. Be honest about generator limits

Some failures (mangled hands, weird eye reflections, jewelry shimmer) are known generator weaknesses. Surface them as such, don't pretend a different prompt will fix them. Recommend re-roll or post.

### Rule 5. When in doubt, ACCEPT and recommend post

Generation is one stage in a pipeline. If the image is 80% right and the gap is fixable in post, that's an ACCEPT with post notes. Don't send the user back to re-generate when an editor would handle it in 90 seconds.

## Reference

- `references/critique-rubric.md`, the full layer-by-layer rubric

## Example output

> ## Verdict
> REVISE
>
> ## What's working
> - Composition correctly reserves the right two-thirds for text overlay (matches shot_03 rationale)
> - Lighting direction matches series_lock (window-left, warm afternoon)
> - Mood reads as calm/considered, on-brand
>
> ## What's not working
> - **Series Lock, character mismatch.** The character has brown hair, but series_lock specifies "salt-and-pepper." This is a verbatim-anchor failure.
> - **Technical, left hand.** Hand on the laptop has six fingers (Flux known failure mode).
> - **Shot Spec, framing.** Generated as MS but spec called for MCU. Subject is too small in frame.
>
> ## Revision plan
> - **Hair:** Prompt-level. Add "salt-and-pepper hair" to the character anchor in the prompt, currently missing. Re-roll.
> - **Hand:** Re-roll required. Generate 2–3 more times with same prompt and pick a clean one.
> - **Framing:** Prompt-level. Change "medium shot" to "medium close-up" in the prompt. Re-roll.
>
> ## Confidence
> HIGH

## Handoff

After delivering the critique, if the verdict is REVISE, offer:

> "Want me to draft the revised prompt? Point `visual-prompt-forge` at this output tree in
> revision mode and it will re-emit prompts for just the shots that need them."

If the verdict is REJECT, do not offer that. REJECT means a blocking issue or three or more
major ones, which is a failure with no clear fix path, and revision mode is built to stop
there and ask. Say what blocked it and what decision it needs: a changed shot spec, a
changed brand-lock, or a different generator.

Don't auto-revise. The user picks. The critique you just wrote is exactly what closes that
loop.
