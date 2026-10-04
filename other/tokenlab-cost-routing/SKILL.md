---
name: tokenlab-cost-routing
description: Choose TokenLab models and fallback chains using public pricing, task fit, latency expectations, and native endpoint needs before writing production routing code.
license: MIT
metadata:
  category: coding
---

# TokenLab Cost Routing

Use this skill when a user asks how to reduce TokenLab cost, compare model prices, pick fallbacks, or route requests by quality, latency, and budget.

## What this skill should deliver

- A compact routing recommendation with exact public TokenLab model IDs.
- A cost-aware fallback chain for the user's workload.
- A catalog/pricing lookup path that can be rerun.
- A note on which endpoint family each model should use.
- Guardrails for when not to switch models because doing so would change output, safety, or request semantics.

## Preferred approach

1. Identify the workload and constraints:
   - chat, coding, agent loop, image, video, audio, embedding, rerank, translation, decisions, or multimodal
   - quality floor
   - latency target
   - budget or cost ceiling
   - native endpoint requirement
2. Read live public catalog signals before recommending:
   - `GET https://api.tokenlab.sh/v1/models`
   - `GET https://api.tokenlab.sh/v1/models?recommended_for=<scene>`
   - `GET https://api.tokenlab.sh/v1/models/:model`
   - `GET https://api.tokenlab.sh/v1/models/:model/pricing`
3. Build a chain with roles:
   - primary quality model
   - balanced default
   - fast fallback
   - budget fallback
4. If the user asks for exact cost, compute from live pricing and their estimated token/media volume. State units and assumptions.
5. For non-chat requests, inspect model details before changing parameters or endpoint family.
6. For bounded semantic decisions, discover `category=decision` and the System One operation. Compare live pricing and measured task errors; a zero output price does not imply zero output tokens. Never insert a decision model into a chat fallback chain or replace typed answers with free text silently. Escalation and action authorization remain application decisions.

## Output format

- One sentence stating workload and assumptions.
- A table with `Route role`, `Model ID`, `Endpoint`, `Why`, and `When to fall back`.
- One catalog command and one pricing command.
- A short implementation note for retries, rate limits, and user approval when quality would drop.

## Avoid

- Do not invent prices, discounts, or model counts.
- Do not choose a cheaper model if that would silently remove required native behavior, tools, media support, safety constraints, or structured output guarantees.
- Do not expose TokenLab internal channel, physical provider, or routing details.
- Do not turn a user-provided model into a different model without saying why.
- Do not hardcode a fallback list without saying when it was checked or how to refresh it.

## Edge Cases

- If catalog or pricing endpoints are unavailable, say that routing cannot be price-verified and provide only an example pattern.
- If the user asks for "cheapest", include capability and reliability tradeoffs.
- If billing risk is high, require explicit user approval before adding automatic fallback to paid media/video generation.
