---
name: tokenlab-model-picker
description: Pick TokenLab models for chat, coding, image, video, audio, embeddings, reranking, decisions, and translation by reading public model catalog signals before recommending concrete model IDs.
license: MIT
metadata:
  category: coding
---

# TokenLab Model Picker

Use this skill when a user asks which TokenLab model to use, how to compare model options, or how to route a workload across model families.

## What this skill should deliver

- A short model shortlist with exact TokenLab model IDs.
- The workload assumptions used to pick the models.
- A public catalog lookup path that the user or agent can rerun.
- A fallback model when the first choice is unavailable or too expensive.
- A caveat when a recommendation depends on volatile pricing, availability, or benchmark data.

## Preferred approach

1. Identify the workload: chat, coding, agent loop, image, video, audio, embedding, rerank, translation, decisions, or multimodal.
2. Use the public model catalog before recommending hardcoded IDs:
   - General catalog: `GET https://api.tokenlab.sh/v1/models`
   - Task shortlist: `GET https://api.tokenlab.sh/v1/models?recommended_for=<scene>`
   - Model contract: `GET https://api.tokenlab.sh/v1/models/:model`
   - Pricing detail: `GET https://api.tokenlab.sh/v1/models/:model/pricing`
3. Prefer exact public model IDs over family names.
4. Separate recommendation dimensions:
   - quality or frontier capability
   - cost sensitivity
   - latency or fast iteration
   - native endpoint needs
   - multimodal input or output
5. Return a compact table, then one runnable API example if useful.

## Default shortlist patterns

- Coding and agent work: choose a strong reasoning/coding model, a cheaper fallback, and a fast iteration model.
- General chat: choose one balanced model and one lower-cost fallback.
- Image or video: use `recommended_for=image` or `recommended_for=video` instead of guessing request shapes.
- Embeddings, rerank, translation, TTS, STT, music, or 3D: use the task-specific shortlist and inspect the model contract before showing parameters.

- Bounded semantic decisions: discover `category=decision`, inspect the System One contract, and compare task error and escalation coverage on local examples. Use deterministic code for exact calculations and a generative model when the output must be free text. Do not select a decision model as the agent’s chat engine.

## Output format

- One sentence naming the workload assumptions.
- A table with `Use`, `Model ID`, `Why`, and `Fallback`.
- One catalog command the user can rerun.
- One warning line if availability, pricing, or provider-native behavior must be verified.

## Avoid

- Do not claim a single universal best model.
- Do not recommend provider-prefixed or physical route names as public model IDs.
- Do not invent prices or model counts.
- Do not silently translate a native-only need into a generic chat completion.
- Do not recommend a model that is absent from the current public catalog.

## Edge Cases

- If the user asks for the cheapest option, still include capability limits.
- If the user asks for a benchmark winner, require a cited benchmark and observed date.
- If the catalog is unavailable, say so and fall back to the last known examples only as examples, not truth.
