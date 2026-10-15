---
name: tokenlab-decisions
description: "Get typed answers (yes/no probability, one choice from a list, or a score on a scale) about a piece of text or JSON with TokenLab System One decision models, for routing, gating, scoring, and triage inside an app or agent. Use when the user says \"classify these tickets\", \"route each request to the right team\", \"is this a refund request?\", \"score how urgent this is\", \"should the agent take this branch?\", \"gate this action\", or \"give me a probability, not a paragraph\". Writes the questions, calls /v1/systemone or the MCP evaluate_decisions tool, and keeps thresholds in your code. For free-form text, summaries, or tool-calling, use a chat model through tokenlab-api-integration. For native route details, use tokenlab-native-endpoints."
license: MIT
metadata:
  category: decision
---

# Decisions

Ask a decision model named, typed questions about a state, and get structured answers back: a probability for yes/no, a choice from your options, or a score on your scale. The call is synchronous. There is no text to parse.

## Inputs to collect

- **State:** the thing to judge. A string, a JSON object, or a JSON array (a ticket, a message plus account facts, an agent's current step).
- **Questions:** for each, a short name, a type (`noul`, `choice`, or `score`), instructions, and criteria.
- **Actions:** what the app does with each answer, and the threshold for each action. These stay in your code.
- **Labeled examples,** if the user has them, to check the answers before they drive real actions.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `systemone` | `jev-1.13` | default | Typed decisions on text or JSON |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **Typed decisions on text or JSON:** Jev. It prices per input token.

Exact fields come from the model contract.

Discover decision models with `GET /v1/models?category=decision`. `recommended_for=decision` is also meant to work; if the API rejects it with `invalid_recommended_for`, use `category=decision`.

## Decisions vs chat

| Use a decision model when | Use a chat model when |
| --- | --- |
| You need a branch, a route, a gate, or a score | You need prose, a summary, or a rewrite |
| The answer is one of your options or a number | The answer is open-ended |
| Code acts on the answer with a threshold | A person reads the answer |
| You want probabilities and confidence as data | You need tools, streaming, or a long conversation |

The decision endpoint takes only `model`, `state`, and `questions`. It has no messages, system prompt, tools, streaming, or batch.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Discover and read the contract: `GET /v1/models?category=decision`, then `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL_ID --operation systemone`. Take `MODEL_ID` from the Models list above or from that discovery call. The contract lists `state` and `questions`.
2. Write the questions (see Technique and `references/question-design.md`). Give each a stable name; the response uses the same names.
3. Estimate with `GET /v1/models/{model}/pricing`. Jev prices per input token. Example: 469 input tokens × (input price per 1M tokens) / 1,000,000. Estimate a batch from one real call's `usage.input_tokens`.
4. Call `POST /v1/systemone`: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/systemone --json @body.json`. Keep the `x-request-id`. There is no task to poll.
5. Read `answers.<name>` and `usage`. Keep `noul`, `probabilities`, `confidence`, and `usage` exactly as returned. Do not round a probability into a Boolean in storage.
6. Apply your thresholds in code (see below). Log the request ID, the answers, and the action taken.
7. Before the answers drive real actions, run them on the user's labeled cases and tune the thresholds.

HTTP (take `MODEL_ID` from the Models list above):

```bash
curl https://api.tokenlab.sh/v1/systemone \
  -H "Authorization: Bearer $TOKENLAB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "state": {"ticket": "I was charged twice for my October invoice. Please refund the duplicate payment today.", "plan": "pro"},
    "questions": {
      "refund_requested": {"type": "noul", "instructions": "Does the customer explicitly ask for a refund?",
        "criteria": {"true": "The message asks for money back.", "false": "The message only reports a problem or asks a question."}},
      "team": {"type": "choice", "instructions": "Which team should handle this ticket?",
        "criteria": {"billing": "Charges, invoices, refunds", "technical": "Bugs, errors, API problems", "sales": "Plans, quotes, upgrades"}},
      "urgency": {"type": "score", "instructions": "How urgent is this ticket?",
        "criteria": ["Routine question", "Money or access affected", "Outage or safety issue"]}
    }
  }'
```

Response (live, 2026-10-12, trimmed):

```json
{"model": "MODEL_ID",
 "answers": {
   "refund_requested": {"type": "noul", "noul": 0.99},
   "team": {"type": "choice", "choice": "billing", "probabilities": {"billing": 1, "technical": 0, "sales": 0}, "confidence": 1},
   "urgency": {"type": "score", "score": 1, "legend": {"0": "Routine question", "1": "Money or access affected", "2": "Outage or safety issue"}, "probabilities": {"0": 0, "1": 1, "2": 0}, "confidence": 1}},
 "usage": {"input_tokens": 469, "output_tokens": 70}}
```

MCP (`core` or `full` profile), same fields:

```json
{"name": "evaluate_decisions",
 "arguments": {"model": "MODEL_ID",
   "state": {"ticket": "Please refund the duplicate payment."},
   "questions": {"refund_requested": {"type": "noul", "instructions": "Does the customer explicitly ask for a refund?"}}}}
```

Check `isError`, then read `structuredContent.answers` and `structuredContent.usage`. The tool is synchronous; do not use `get_task_status`. Allow a client timeout of at least 150 s.

Act in code, not in the prompt:

```python
a = resp["answers"]
if a["refund_requested"]["noul"] >= 0.8 and a["team"]["choice"] == "billing":
    queue = "billing-refunds"
elif a["urgency"]["score"] >= 2:
    queue = "on-call"
else:
    queue = a["team"]["choice"]
```

## Technique

- **`noul`:** one yes/no fact per question. Optional `criteria` must have both `true` and `false` guidance. The answer is a probability from 0 to 1, not a Boolean.
- **`choice`:** `criteria` maps 1–255 option names to guidance (or `null`). Use short, stable option names your code can switch on. The answer is always one of your names.
- **`score`:** `criteria` is an ordered list of 2–10 level descriptions, low to high. The `score` runs from 0 to the last index and can be a fraction.
- **Put facts in `state`, not in the question.** Questions say what to judge; `state` holds the case. JSON state with clear keys works well.
- **One decision per question.** Split "is it urgent and about billing?" into a `score` and a `choice`. Several questions on one state go in one call.
- **Thresholds and actions stay in your code.** Do not put "if over 0.8 then..." in instructions. Tune thresholds on labeled cases.
- **Keep the raw answers.** Store `noul`, `probabilities`, `confidence`, and `usage` as returned for audit and tuning.
- A request with any other field (`messages`, `stream`, `tools`) fails validation. A question with a wrong shape (for example a `score` with one level) fails too.

## Quality bar

- Each question has one clear decision, a stable name, and valid criteria for its type.
- Answers are stored as returned; thresholds live in code and were checked on labeled cases.
- The app has a safe default when a call fails or an answer is near the threshold.
- The final answer names the model, request ID, answers, and token usage.

## Related skills

- `tokenlab-run`: the call and error mechanics.
- `tokenlab-native-endpoints`: System One next to Responses, Messages, and Gemini routes.
- `tokenlab-api-integration`: put the decision call into application code.
- `tokenlab-cost-routing`: route between decision and chat models by cost.
