---
name: mlx-vlm-conversion
description: >
  Convert, run, and validate vision-language, audio, video, and omni models with Apple MLX and mlx-vlm. Use this skill for image-text-to-text models, Qwen-VL and Qwen3-VL derivatives, multimodal chat, OCR, scientific-figure-to-SVG models, audio/video inputs, processor-heavy repos, and MLX-VLM servers. Do not use text-only mlx-lm conversion advice unless the user explicitly wants only the language submodule analyzed.
compatibility: Cross-platform open skill format. Intended for Apple Silicon MLX workflows using mlx-vlm, Transformers baselines, and Hugging Face multimodal repos.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

VLM behavior is not just weights. Image/audio/video preprocessing, processor files, media token placement, chat templates, and generation settings shape the result. A VLM conversion that loads but uses the wrong processor can appear successful while producing wrong outputs.

## Task

Run or convert a multimodal model with `mlx-vlm`, preserve processor behavior, and validate with real media inputs before declaring success.

Use this skill after the model repo audit identifies a VLM, audio/video model, omni model, or processor-dependent task.

## Inputs

- Model ID or local path.
- Base model ID for fine-tunes if available.
- Task and media type: image, multi-image, video, audio, OCR, diagram-to-code, etc.
- Sample input media and prompt.
- Expected output format, such as text, JSON, SVG, bounding boxes, or transcription.
- Target MLX output path and memory constraints.

## Workflow

1. **Confirm VLM scope.** If the repo has image/audio/video processor files or media tokens, use `mlx-vlm` rather than `mlx-lm`.
2. **Check existing support.** Look for an MLX Community variant and current `mlx-vlm` support for the architecture. Recent support can appear in releases, model cards, or issues before docs are updated.
3. **Build a Transformers baseline.** Use the model card’s recommended `AutoProcessor` and model class when possible. Save exact prompt, media file, generation settings, decoded output, and trimming logic.
4. **Inspect processor artifacts.** Preserve `processor_config.json`, `preprocessor_config.json`, `image_processor_config.json`, tokenizer files, chat template, generation config, and any custom code requirements.
5. **Attempt the MLX-VLM path before porting.** Convert or run using the current `mlx_vlm` CLI/API. Avoid a full architecture port until existing support fails with a concrete error.
6. **Load and generate after conversion.** A converted folder must be loaded and tested on the same sample media.
7. **Validate task-specific output.** For SVG, parse XML and open/render if possible. For OCR, compare exact text and layout-sensitive fields. For bounding boxes, verify coordinate convention.
8. **Document failures.** Record commands, package versions, model revision, error logs, and whether the failure happened at download, conversion, load, preprocessing, generation, or output validation.

## Command patterns

Verify current help first:

```bash
python -m pip install -U mlx mlx-vlm transformers accelerate pillow huggingface_hub
python -m mlx_vlm.generate --help
python -m mlx_vlm.convert --help
python -m mlx_vlm.server --help
```

Run an existing MLX-VLM model:

```bash
python -m mlx_vlm.generate \
  --model mlx-community/Qwen3-VL-4B-Instruct-4bit \
  --image ./sample.png \
  --prompt "Describe the image."
```

Conversion pattern:

```bash
python -m mlx_vlm.convert \
  --hf-path XunmeiLiu/VFIG-4B \
  --mlx-path ./models/vfig-4b-mlx \
  --dtype bfloat16
```

Quantized conversion pattern, only after a baseline plan is clear:

```bash
python -m mlx_vlm.convert \
  --hf-path XunmeiLiu/VFIG-4B \
  --mlx-path ./models/vfig-4b-mlx-4bit \
  --quantize \
  --q-bits 4 \
  --q-group-size 64 \
  --dtype bfloat16
```

Python API pattern:

```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_image

model_path = "./models/vfig-4b-mlx"
model, processor = load(model_path)
image = load_image("./figure.png")
messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "Convert this figure into valid SVG code."}]}]
prompt = apply_chat_template(processor, model.config, messages)
response = generate(model, processor, prompt, [image], max_tokens=8192, verbose=True)
print(response)
```

Treat the Python pattern as illustrative. Confirm the installed `mlx-vlm` API because model-specific prompt utilities and media arguments change faster than plain text generation APIs.

## Output validation patterns

For SVG-producing models, use the bundled parser before claiming success:

```bash
python scripts/svg_sanity_check.py ./outputs/vfig_output.txt --write-svg ./outputs/vfig_output.svg
```

A syntactically valid SVG is necessary but not sufficient. When possible, open it in a browser or Inkscape and compare visually with the input figure.

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| `mlx-lm` conversion appears to work but output ignores image | Wrong stack; only language submodule handled | Stop and reroute to `mlx-vlm` |
| Conversion reports unexpected or unused parameters | Model class mismatch, custom layers, adapter merge issue | Compare config with base; test base model in `mlx-vlm`; inspect current issues |
| Converted model fails to load | Quantization mode unsupported, missing processor/tokenizer files, bad config mapping | Retry unquantized; copy processor/tokenizer artifacts; reduce quantization complexity |
| Model loads but output differs badly from baseline | Wrong chat template, image preprocessing, special tokens, or generation config | Print rendered prompt; inspect processor fields; compare decoded baseline |
| SVG output parses but is visually wrong | Quality loss or generation settings mismatch | Compare unquantized output; increase max tokens; adjust quantization; render visually |
| OOM or extreme slowness | Model too large, media resolution too high, no cache discipline | Lower image/video resolution within model limits; use smaller quantization; benchmark |

## Done condition

Stop when the MLX-VLM model loads, processes a real media input, generates an output, and passes the task-specific sanity checks, or when a specific upstream incompatibility is documented with a minimal repro. Conversion alone is not success.
