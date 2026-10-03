---
name: crun-model-router
description: Select and inspect an appropriate Crun image, video, audio, music, or media-tool model from a structured user intent. Use when the user describes the desired media result but does not provide an exact Crun model, or asks for a speed, quality, reference-media, or native-audio tradeoff.
---

# Crun Model Router

Use `../../runtime/crun_cli.py` and `../../catalog/models.json`. Treat the catalog as the source of truth for routing labels and priority, and the authenticated Models endpoint as the source of truth for the selected model's current input schema.

## Build routing intent

Normalize the request into one JSON object:

```json
{
  "modality": "image|video|audio",
  "operation": "text-to-image|image-edit|text-to-video|image-to-video|reference-to-video|text-to-speech|music-generate|...",
  "quality": "balanced|best",
  "speed": "balanced|fast",
  "native_audio": false,
  "reference_media": []
}
```

Preserve explicit constraints. Infer the operation from supplied media only when unambiguous.

## Route and inspect

Prefer a JSON file or stdin for portable invocation:

```text
python <runtime>/crun_cli.py models route --intent-file <intent.json>
python <runtime>/crun_cli.py models describe --model <selected-model>
```

Use `selected` by default. Present `alternatives` only when their tradeoffs matter or the user asks. Read `required_input_fields` and `input_schema`, then ask only for required information that cannot be derived. Never invent fields or copy a sibling model's schema.

Use `models list` when the static candidate is rejected or missing. Never infer capability or priority from a model name or schema; update `models.json` explicitly. Report a hard-constraint conflict instead of weakening it silently.

After routing, hand off affordability checks to `../crun-account-credits/SKILL.md` and all creation or monitoring work to `../crun-task-runner/SKILL.md`.
