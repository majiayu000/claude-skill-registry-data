---
name: system-one
description: Reference for System One decision models — Ollama's local POST /v1/systemone endpoint (nimble, clef, clef-flash) and TypeSafe's hosted Jev API (jev-latest / jev-1.13.0), plus the typesafe-sdk Python and @typesafe-ai/sdk JS clients. Covers the three question types (choice, score, noul), state shaping, structured instructions/criteria, confidence math, request limits and errors, the Ollama-vs-TypeSafe differences, Jev's known failure modes, and worked patterns from the official cookbooks (fan-out, confidence gating, composite scoring, intent routing, guardrails, RAG gating, extraction, re-ranking, hierarchical beam search). Use whenever the work mentions System One, systemone, Ollama decision models, nimble, clef, TypeSafe, Jev, noul, or classifying/scoring/yes-no judgments that code consumes instead of generated text.
---

# System One — typed decisions, not text

A System One model takes one `state` + named typed `questions`, evaluates every question **independently and in parallel** against the state, returns typed answers + probabilities. It does **not** generate text, write code, reason step by step, or call tools. Code owns control flow; the model makes narrow judgments.

Two providers, same wire shape:

| | Ollama (local) | TypeSafe (hosted) |
|---|---|---|
| Endpoint | `POST http://localhost:11434/v1/systemone` | `POST https://api.typesafe.ai/v1/systemone` |
| Auth | none | `Authorization: Bearer $TYPESAFE_API_KEY` |
| Models | `nimble`, `clef`, `clef-flash`, Tev1 (Together AI) | `jev-latest` → `jev-1.13.0`, `jev-preview` |
| Min version | Ollama v0.35.0 (images v0.35.1) | — |
| Images | `images: [base64…]`, Clef models only | not supported (text only) |
| Score levels | 2–26 | 2–10 |
| Choice options | 2–26 per model pages (API schema says 255) | up to 255 |
| Questions/request | 1–64 | not stated |
| Size limit | 64 KiB body (32 MiB with images); must fit loaded context | 64k tokens total; 32k for state + longest question |
| Extra field | `keep_alive` (`"5m"`, seconds, `0` unload, negative = keep) | — |
| Cost | free | $0.042 / M input tokens, output free |

**PHP / Symfony:** use Symfony AI 0.15+ (`symfony/ai-decision-platform` + the Ollama or TypeSafe bridge), not raw HTTP; classes, wiring and tests are in the `symfony-ai-platform` skill → Decision models, routing between agents in `symfony-ai-agent` → MultiAgent. This skill stays the source for question design and measured limits.

Details: [references/api.md](references/api.md) (both HTTP APIs + Python/JS SDKs). Worked examples: [references/examples.md](references/examples.md).
Real nimble runs on invented products (exact request + response, timings, ground truth): [examples/ollama/](examples/ollama/) — 10 object criteria → 400 · 11 structured e-commerce 11/11 · 12 weak spots (dates/math/negation/quantifiers) 7/10 · 13 support ticket routing + guardrail 6/7.

## Request

```json
{
  "model": "nimble",
  "state": {"ticket": "I was charged twice. Please refund the extra payment."},
  "questions": {
    "refund":   {"type": "noul",   "instructions": "Is the customer requesting a refund?"},
    "team":     {"type": "choice", "instructions": "Which team should handle this?",
                 "criteria": {"billing": "Payments and refunds", "bug": "Software errors", "account": null}},
    "urgency":  {"type": "score",  "instructions": "How urgently does this need a response?",
                 "criteria": ["Routine: no time pressure", "Soon: a customer is inconvenienced",
                              "Immediate: a critical service is unavailable"]}
  }
}
```

- `state`: non-empty string, JSON object, or array. Prefer an object with named parts.
- Question **ids are never sent to the model** — put the full question in `instructions`.
- `choice.criteria`: object `{option: description | null}`. `null` = bare label.
- `score.criteria`: array, index 0 = lowest. Scale is `0 … len-1`.
- `noul.criteria`: optional `{"true": …, "false": …}`; Ollama defaults `Yes`/`No`.
- `instructions` and every criteria entry may be string, object, or array on TypeSafe. **Ollama: only `instructions` may be structured; criteria must be strings (400 otherwise).**
- Answers are not passed between questions. Dependent question → second request.

## Response

```json
{
  "model": "nimble",
  "answers": {
    "refund":  {"type": "noul", "noul": 0.9989},
    "team":    {"type": "choice", "choice": "billing",
                "probabilities": {"billing": 0.97, "bug": 0.02, "account": 0.01}, "confidence": 0.95},
    "urgency": {"type": "score", "score": 0.83, "legend": {"0": "Routine…", "1": "Soon…", "2": "Immediate…"},
                "probabilities": {"0": 0.25, "1": 0.67, "2": 0.08}, "confidence": 0.4}
  },
  "usage": {"input_tokens": 174, "output_tokens": 1}
}
```

- `noul` = P(yes), a number, not a boolean. No `confidence`.
- `score` = Σ level × P(level); can land between levels; **not** normalized to 0–1.
- `probabilities`/`legend` keys for score are level indices as strings (Python SDK: ints).
- TypeSafe's `model` returns the resolved version (e.g. `jev-1.13.0`) — log it.
- Ties in choice follow option order.

## Confidence (Choice/Score only)

- Ollama spec: `1 − H(p)/ln(N)` (entropy). 0 = uniform, ~1 = one candidate dominates.
- TypeSafe docs: Choice `(p_max − 1/n)/(1 − 1/n)`; Score `max(0, 1 − Σ p_i|i−m| / MAD_unif)` with `MAD_unif = (1/n)Σ|i−(n−1)/2|`; noul-equivalent `|2p−1|`.
- The two providers document different formulas — don't port thresholds between them blindly.
- Confidence = peakedness, **not** correctness. Calibrate thresholds on your own data.
- Alternatives: top probability `p_max`, or top/second ratio.

## Design rules (from the docs, in priority order)

1. **Code first.** Anything deterministic (dates, arithmetic, regex, status checks) stays in code.
2. **Atomic questions.** One snap judgment each. "Is this spam?" → six nouls (credentials request, unexpected reward, time pressure, sender/domain mismatch, link mismatch, disguised link) combined in code.
3. **Batch everything in one request**, including speculative questions only some code paths read. Parallel → near-zero latency cost. Batching 13 questions: ~12× cheaper, ~10× faster, identical answers.
4. **Send only relevant state.** Irrelevant content lowers accuracy (context rot).
5. **Point at state parts with backtick paths**: ``"Does `ticket.messages[0].text` request a refund?"``.
6. **Pick the type by what code does next**: Choice → switch, Score → threshold/sort, Noul → `if`.
7. **Route on uncertainty**: high → act, middle → confirm/review, low → human or bigger model. Threshold scales with action risk.
8. **Composite scores**: normalize each Score by `len(criteria)-1`, weight in code; tune weights, not prompts.

## Writing good questions

- Noul: one condition; high value = yes ("contains personal data", not "is free of…"); statement or question both work; add `criteria` only when the boundary is subtle.
- Noul ≠ degree. "Strong in Python?" at 0.5 means *unsure*, not *medium*. Use a Score for degree.
- Score levels describe **situations**, not degrees. `["0","1","2"]` fails. Each level is judged alone — "worse than previous" means nothing. One dimension per Score. Give rare extremes their own top level.
- Choice: give the full option list; add `other`/`none` escape hatch; describe options so they separate. Confusable options → objects `{what, not_for, examples}`.
- Structure (any field): put the question in one key and data in others, reference by backtick name. Field names are free and seen by the model:
  ```json
  "instructions": {
    "potential_duplicate": {"name": "Jon Smith", "location": "Oakland, CA"},
    "question": "Is the resume for the same person as `potential_duplicate`?"
  }
  ```

## Known failure modes (Jev 1.13; assume similar for local models until tested)

| Failure | Do instead |
|---|---|
| Literal reading | State exact condition; boundary cases in criteria |
| Counting, math, hex/RGB, interpolating scores | Do it in code; ask one noul per item and sum |
| Date comparison/arithmetic | Extract parts via Choices, compute in code |
| Indirection / double negatives | Direct wording; name the state field |
| Large irrelevant state | Filter first |
| Adversarial/injected state | Precise criteria; test edge cases |
| instructions vs criteria contradict | Align them; never map `true` to "no" |
| First-option bias in Choice | Reorder options, check consistency |
| Generation | Use an LLM; let System One pick among candidates |

English is strongest; other languages work with lower accuracy.

## Ollama errors

`400` invalid request / unsupported model or runner / prompt exceeds context / cloud model · `404` model not pulled (`ollama pull nimble`) · `413` body over 64 KiB (32 MiB with images) · `500` load/render/scoring failed. Body: `{"error": "…"}`. No streaming, tools, video, or generation options. Input never truncated. Requires GGUF weights; MLX/Safetensors and cloud models unsupported. Not on Ollama Cloud.

## Ollama models (from ollama.com/library, read 2026-10-10)

| Model | Maker | Size | Input | Effective prompt limit | Notes |
|---|---|---|---|---|---|
| `nimble` (9b) | Bespoke Labs, from Qwen3.5-9B | 9.3–9.5 GB | text | **8,192 tokens** (full state + all questions per question) | <100 ms on M5 Max; contrastive-pair training |
| `clef-flash` (9b) | Cloudflare, from Qwen3.5-9B | 11–12 GB | text + image | 64K | 38.8 ms median, lowest latency in Cloudflare's runs |
| `clef` (27b) | Cloudflare, from Qwen3.8-27B | 18 GB | text + image | 64K | ~5× slower than clef-flash, "more accurate" |
| Tev1 (4B, 0.8B) | Together AI | — | text | — | 73.3% / 63.5% on Bespoke's suite |

Model pages say Choice/Score take **2–26 options** (API schema says 255 — trust the model page). Ties follow option order: put the preferred option first.

Vendor benchmarks (no shared head-to-head between nimble and clef-flash; each only vs Jev, different suites):
- Nimble vs Jev 1.13 (Bespoke, 13 public sets, 3,880 decisions): macro 74.8 vs 76.0; Choice 81.6 vs 82.9; Boolean 80.2 vs 84.6; **Score 54.6 vs 50.1**.
- Clef-flash / Clef / Jev (Cloudflare): BFCL 98.8/98.5/95.8; API-Bank 93.1/91.9/88.2; BANKING77 90.9/94.2/79.7; CLINC150+OOS 66.8/97.4/89.3; Home appliance 97.7/83.0/52.3; ANLI 59.1/69.8/74.8; RouterBench 79.9/79.7/79.9; When2Call 65.6/72.4/81.0; latency median 38.8/209.3/524.1 ms.

## Measured (2026-10-10, nimble q8_0, Ollama 0.40.2, CPU-only laptop: `size_vram 0`)

- 36 KB document as state → `400 {"error":"prompt 0 has 11282 tokens; expected 1–8194 (input is never truncated)"}`. Limit is per question prompt (state + questions).
- 17 KB (~5k-token) state + 5 questions → OK, but `usage.input_tokens` 26,657 (state re-scored per question) and **327 s** wall time on CPU.
- Real CPU throughput ≈ **18–20 uncached input tokens/s** (604-token section + 1 noul: 32 s warm; 698 tokens: 40 s incl. load). A 5-question run on a ~5k-token document fits this too (~6k unique tokens / 327 s): `usage.input_tokens` multiplies the state per question, but the shared state prefix seems to be computed once (prompt cache). Cost ≈ state once + each question, not state × questions.
- ~400-word state + 10 easy factual questions (warm): 10/10, **103 s**, `usage.input_tokens` 13,647 (≈ state × 10). ~8–10 s per extra question on CPU: cheaper than re-sending the state, not free.
- Same state, 10 hard questions: **7/10**, 70.7 s (state prefix cached). Failed exactly the documented weak spots: date math ("published more than one year ago?" → 0.41, wrong), double negative ("is it false that X never uses Y?" → 0.10, wrong), arithmetic (monthly price × 12 > threshold? → 0.32, wrong). Passed: counting 3 named items (0.99), multi-hop match, "not stated" trap, close options (0.89, conf 0.67), counting 4 items (> 3? → 0.61, right but unsure). Wrong answers sat at 0.1–0.4, not near 0: middling noul = warning sign. Keep math, dates, and negation in code.
- Harder non-math set (injection, misbinding, tense, NOT-choice, quantifier): 9/10. Miss: "does the state say **every** project uses language X?" → 0.96 yes (one project's language unstated; overgeneralized). Quantifiers ("every", "all") are a weak spot.
- **Ollama rejects object criteria**: `400 {"error":"question \"x\": choice criteria must map option keys to descriptions or null"}`. Flatten `{what, not_for, examples}` into one string (`"what. Not for: … Examples: a; b"`). **Structured `instructions` objects work** (`{"claim": …, "question": "Is `claim` supported by `product`?"}`).
- E-commerce product state (nested JSON, ~1k tokens) + 11 structured questions: **11/11**, 119.5 s. Passed: care-label misuse vs defect, sarcasm → angry, injection in `seller_notes` ignored, marketing "pure merino" vs 87% materials, variant pick (size + dark + in stock), health claim, EU→Germany, Kids listing ≠ adult listing.
- Product weak-spot run (12): date and sum-over-variants math wrong (0.28, 0.43); percent-off and double negative right only at ~0.55. Confidence on a wrong Choice can be 0.99 when the question word is ambiguous ("offered" vs "in stock").
- Support-ticket run (13): the one wrong route came back at confidence 0.32; all correct answers ≥ 0.76. Confidence gating works here — gate Choices below ~0.6.
- An identical repeat request returned in 0.48 s (prompt cache) — never benchmark with a repeated request.
- Tiny request: 10.5 s cold, 0.48 s warm. The "<100 ms" claim assumes a GPU (M5 Max). Check `GET /api/ps` → `size_vram` before blaming the model.
- Literal reading confirmed: the document said readers "already know the basics", the choice option said "new to the topic" → nimble picked `advanced` (0.98). Write options that match the text's own wording.

## TypeSafe SDK against Ollama (officially documented on ollama.com)

```bash
pip install typesafe-sdk
export TYPESAFE_BASE_URL=http://localhost:11434
export TYPESAFE_API_KEY=ollama          # required by SDK, ignored by Ollama
export TYPESAFE_DEFAULT_MODEL=nimble
```
Use `TypeSafeClient(timeout=120)` — local first load is slow. Decision models are not in the Ollama CLI or the `ollama` Python/JS libraries yet (model pages show `ollama.systemone(...)` snippets but say to use the API or TypeSafe SDK for now).

## Unverified

- Whether Jev itself runs on Ollama (not listed).
