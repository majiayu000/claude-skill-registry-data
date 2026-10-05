---
name: comfyui-prompt-engineering
description: Diagnose and improve ComfyUI text conditioning with architecture-aware prompts, encoder and node compatibility checks, controlled experiments, and.
---

# ComfyUI Prompt Engineering

Prompt behavior belongs to the loaded workflow, text encoder, checkpoint architecture, and node implementation. Never apply one universal token limit, weight syntax, negative-prompt recipe, or keyword style to every ComfyUI model.

## Start With the Workflow, Not a Prompt Myth

Inspect the workflow JSON or live graph and record:

- checkpoint/model architecture and exact loader nodes;
- positive and negative conditioning paths;
- text encoders loaded and how many are active;
- built-in versus custom prompt/conditioning nodes and their versions;
- LoRAs, textual inversions, style models, ControlNet/adapters, and guidance nodes;
- sampler, scheduler, steps, CFG/guidance, denoise, resolution, seed;
- relevant console warnings and model/node compatibility errors.

If the architecture cannot be identified, say so and use a minimal empirical test. Do not guess from the filename alone.

## Architecture-Aware Routing

| Family or workflow | Prompt implication to verify |
|---|---|
| SD 1.x/2.x-style CLIP | concise tag/phrase prompts and CLIP weighting often work well |
| SDXL | dual-CLIP conditioning and pooled output matter; use SDXL-compatible embeddings/LoRAs |
| FLUX-style native workflows | commonly combine CLIP-L and T5; natural descriptions may matter more than legacy quality-tag piles |
| SD3-style workflows | may use multiple text encoders; follow the official template and loader contract |
| model-specific/custom nodes | syntax, token handling, negative conditioning, and weights may differ |

These are routing hints, not universal laws. Prefer the model card, official ComfyUI example/template, and the actual node source for the installed version.

## Supported Built-In Syntax

For the built-in `CLIPTextEncode` path, current official ComfyUI documentation describes:

- `(phrase:1.2)` to increase weight;
- `(phrase:0.8)` to decrease weight;
- `(phrase)` as the default emphasis step;
- `\(` and `\)` for literal parentheses;
- `embedding:file_name` for textual inversions;
- dynamic prompt and comment syntax supported by the current built-in node/UI.

Before using any syntax, verify that the active node is the built-in encoder. Custom nodes may parse prompts differently.

Do not state that all prompts are truncated after 77 tokens. A CLIP encoder has a limited native context window, but ComfyUI and custom nodes can tokenize, chunk, pad, combine, or route long input differently. Inspect the active tokenizer/node implementation or test with controlled prompts. Likewise, do not claim `BREAK` has identical behavior across all nodes and architectures.

## Weighting Rules

- Start at `1.0` and change one concept at a time.
- Use small changes first; large weights can distort composition or create artifacts.
- Weight phrases, not long paragraphs.
- If weighting appears ineffective, confirm node syntax and encoder compatibility before increasing it.
- Nested-parenthesis math and accepted ranges are implementation details; do not present them as universal unless verified from the active parser.
- Record the exact prompt and workflow seed for every comparison.

## Embeddings and LoRAs

- Verify architecture compatibility before loading. An SD 1.5 embedding is not automatically valid for SDXL or another encoder family.
- Confirm the file resolved and check console output for missing/unloaded keys.
- Use the trigger words and recommended strengths from the artifact's trusted documentation, then test locally.
- Separate model strength from text-encoder strength when the loader exposes both.
- Add one adapter at a time during diagnosis; stacked adapters can mask prompt effects.
- Treat downloaded model files as untrusted. Preserve hashes and source provenance; do not run bundled executables/scripts blindly.

## Prompt Construction

Build from intent to detail:

1. subject and action;
2. composition and camera/viewpoint;
3. environment and relationships;
4. lighting, material, and color;
5. style/medium when desired;
6. model-specific quality or trigger tokens only when evidence supports them.

Put important concepts clearly and early, but do not assume simple word order alone determines attention. Avoid contradictory adjectives, duplicated quality tags, incompatible styles, and excessive micro-detail.

### Negative conditioning

Use negatives only when the workflow/model supports them meaningfully. Start empty or minimal, observe a repeatable failure, then add the smallest exclusion that improves it. Huge generic negative lists can remove desired features or interact unpredictably with CFG/guidance.

Some architectures or distilled workflows use different guidance/negative-conditioning designs. Follow the official template rather than forcing an SD 1.5 pattern.

## Controlled Improvement Loop

Freeze every non-prompt variable:

- seed;
- checkpoint and encoders;
- LoRA/embedding versions and strengths;
- sampler, scheduler, steps, guidance/CFG, denoise;
- resolution and latent/image inputs.

Then run:

1. **baseline** — shortest prompt that states the goal;
2. **single-factor variant** — add or alter one prompt concept;
3. **repeat** — use several fixed seeds if the result may be seed-specific;
4. **compare** — composition, subject accuracy, artifacts, style, and unwanted changes;
5. **keep/revert** — retain only measured improvements;
6. **save** — workflow JSON, prompts, seeds, output paths, and notes.

Do not compare two prompts while also changing checkpoint, sampler, resolution, and LoRA stack.

## Symptom Triage

| Symptom | Check before rewriting the whole prompt |
|---|---|
| details ignored | encoder/node path, tokenizer behavior, prompt conflicts, concept load |
| image does not match prompt | wrong text encoder/checkpoint pairing, bypassed conditioning, adapter dominance |
| weights do nothing | custom-node syntax, parser version, phrase boundaries |
| style overwhelms subject | style/LoRA strength, repeated trigger terms, CFG/guidance |
| distorted output | excessive weights, incompatible embeddings/LoRAs, resolution, sampler/guidance |
| negative prompt harms image | architecture support, overly broad negatives, high CFG |
| different behavior after update | node/ComfyUI/model version drift; diff workflow and logs |

## Evidence Sources

Use this order:

1. actual workflow JSON and console output;
2. installed node source/version;
3. official ComfyUI workflow template and built-in-node documentation;
4. model card and trusted artifact documentation;
5. controlled local A/B results.

Community prompt recipes are hypotheses, not facts.

## Completion Report

Report the architecture, encoder/node path, prompt changes, frozen parameters, seeds, outputs compared, result, and remaining uncertainty. If a live render was not run, state that the recommendation is unverified.

## Quality Gate

- [ ] Architecture and encoder path were identified or uncertainty was stated.
- [ ] Syntax was verified for the active node.
- [ ] No universal 77-token, `BREAK`, negative-prompt, or weight claim was made.
- [ ] Embeddings/LoRAs were checked for compatibility and provenance.
- [ ] A/B tests changed one factor at a time and preserved seeds.
- [ ] Workflow and output evidence were saved for reproduction.
