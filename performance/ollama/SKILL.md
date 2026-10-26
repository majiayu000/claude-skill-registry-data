---
name: ollama
description: Use when running local LLMs with Ollama — choosing models by measured speed and quality on CPU-only or old-GPU machines, structured JSON output, prompts that keep a small model on rails, comparing models per task, timeouts and load control on a shared PC, and using local models for extraction, classification, OCR post-processing or as teachers for distillation. Also use when a local model is too slow, returns broken JSON, invents dates, or overloads the machine.
---

# Ollama (local LLMs)

Default: Ollama as a local service, models chosen per task by measurement, JSON output enforced by schema, deterministic settings for extraction, every model answer checked by code before it is trusted.

## Setup

- Install Ollama per user if possible; confirm what it detected (`ollama ps`, server log). Old GPUs (e.g. compute capabilities the runtime no longer supports) fall back to CPU — plan for CPU speeds.
- Pull candidates: `ollama pull <model>`; models from Hugging Face in GGUF format can also be used.

## Choose models by measuring, per task

Build a tiny benchmark per task (20–50 real-looking items with known answers):

| Metric | Why |
|---|---|
| Tokens per second, median latency per item | Decides whether a batch finishes overnight or never |
| Task accuracy (exact match on dates, amounts, labels) | The only quality number that matters |
| Format failures (invalid JSON) | Each failure costs a retry |
| Language fit (e.g. share of output in the expected language) | Small models drift into English or Chinese |

Pick the smallest model that meets the accuracy target. Record results with date and hardware; re-run when models change. Different tasks often need different models.

## Structured output

```bash
curl -s localhost:11434/api/chat -d '{
  "model": "MODEL", "stream": false,
  "format": {"type":"object","properties":{"due":{"type":["string","null"]}},"required":["due"]},
  "options": {"temperature": 0, "num_ctx": 8192},
  "messages": [{"role":"user","content":"..."}]
}'
```

- Pass a JSON schema in `format`; parse and validate; retry once with the validation error appended.
- `temperature: 0` for extraction. Set `num_ctx` explicitly — the default context may silently truncate long documents.

## Keeping small models honest

- Ask for evidence: "copy the exact text that supports the date". Then check in code that the quoted text exists in the source and contains the value. Reject answers whose evidence is missing.
- Normalise before comparing (full-width vs half-width characters, era-based years to Western years, `O` vs `0`).
- Prefer "unknown" over a guess: make `null` a valid answer and say so in the prompt.
- Confidence fields from the model are weak signals; combine them with code checks.
- Two different models agreeing is a useful filter when labelling data for training a smaller model.

## Running on a shared PC

- Check system load before starting a batch; skip or delay when busy.
- Set per-item timeouts and an overall time budget; record progress so the batch resumes.
- One heavy job at a time (a lock file); unload models when done (`keep_alive: 0`).

## Verification loop

1. Run the benchmark: accuracy, failure rate, latency recorded.
2. Spot-check outputs against the source by hand.
3. For pipelines, store the model name and version with every result so reruns are comparable.

## Pitfalls

- **Large images to vision models on CPU** can take tens of minutes per page; downscale or use a dedicated OCR engine.
- **Model tags change** under the same name; pin by digest when reproducibility matters.
- **Prompt templates** differ per model family; use the chat API rather than raw prompts.
- **"Same document?" questions** get confident wrong answers; ask the model to extract identifying fields and compare them in code.
