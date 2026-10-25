---
name: jev-router"
description: Uses the Jev System One model to choose which OpenCode subagent should handle an ambiguously-routed request, returning a typed choice with a calibrated confidence. Invoke when the correct subagent is not obvious from the task description, when two subagents plausibly apply, or when a previous delegation was sent to the wrong place. Skip entirely when the target is already clear.
---

# Jev Router

Picks **which subagent** handles a request. It never decides _what_ to build —
that stays with the calling agent and the approval gate.

Jev is a System One model: it evaluates a state against typed questions and
returns typed values with probabilities. It does not generate text, so there is
nothing to parse and no way for it to invent a subagent that is not in the
criteria you listed.

## When to invoke

Only when routing is genuinely ambiguous:

- Two or more subagents plausibly apply and you cannot justify picking one
- A previous delegation landed in the wrong place and you need a second opinion
- The request is cross-cutting (e.g. "fix the bug and document it")

**Skip it** when the task maps cleanly to one subagent. A confident answer to a
question you already knew the answer to costs ~0.8s and nothing else. On a
clear-cut task this skill is pure overhead.

## The call

```bash
curl -sS https://opencode.ai/zen/v1/systemone \
  -H "Authorization: Bearer $OPENCODE_ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-1.13-free",
    "state": "<the request, verbatim, plus what you already know about it>",
    "questions": {
      "subagent": {
        "type": "choice",
        "instructions": "Which subagent should handle this request?",
        "criteria": {
          "subagents/code/coder-agent": "Writing or changing source code files",
          "subagents/code/test-engineer": "Writing or fixing tests",
          "subagents/code/reviewer": "Reviewing code for correctness or security, without changing it",
          "explore": "Finding code, tracing flows, answering questions about the codebase — no changes",
          "subagents/meta/external-scout": "Upstream docs, library APIs, dependency source — outside this repo",
          "direct": "Small change you can do yourself without delegating",
          "none_of_these": "None of the listed options clearly fits"
        }
      },
      "needs_approval": {
        "type": "noul",
        "instructions": "Should a human approve the plan before any edit happens?",
        "criteria": {
          "true": "The change is risky, destructive, or hard to review",
          "false": "The change is routine and reversible"
        }
      }
    }
  }'
```

## Reading the answer

```json
{
  "answers": {
    "subagent": {
      "type": "choice",
      "choice": "subagents/code/coder-agent",
      "confidence": 0.94,
      "probabilities": {
        "subagents/code/coder-agent": 0.94,
        "subagents/core/documentation": 0.04,
        "direct": 0.02
      }
    },
    "needs_approval": { "type": "noul", "noul": 0.81 }
  },
  "usage": { "input_tokens": 340, "output_tokens": 60 },
  "cost": "0"
}
```

**`confidence` is not `probabilities[choice]`.** It is a separate number derived
from how spread out the whole distribution is. A single option at 0.4 while the
rest are at 0.3 is a confident answer in the wrong direction; 0.94 with the
rest near zero is a confident answer. `none_of_these` winning — or landing
second close behind — means the taxonomy missed; treat it as `< 0.5` below
regardless of the scalar.

Apply this policy:

| `confidence` | What to do                                                           |
| ------------ | -------------------------------------------------------------------- |
| ≥ 0.8        | Delegate to the chosen subagent                                      |
| 0.5 – 0.8    | Do not guess. Present the top two options to the user and ask.       |
| < 0.5        | Ignore the answer. Your own reading of the task was probably better. |

`needs_approval` at or above 0.8 means the approval gate applies even if the
confidence in routing is high — routing confidence and risk are separate
questions, and that is why they are asked as two.

## Constraints

- **One atomic question per judgment.** Measured on this machine: a compound
  question about a command sequence returned `noul=0.22`, while the same
  judgment asked atomically returned `noul=0.99`. If a question needs the word
  "and", it is two questions.
- **`jev-1.13-free` is temporary.** The OpenCode catalog marks it as available
  for a limited time. If the call returns 404 or an unknown-model error, fall
  back to routing by your own judgment and say so. Never block a task on this.
- **No network means no answer, and that is fine.** On a null response, route
  by hand. This skill accelerates a decision; it is not allowed to prevent one.
- **Never let Jev pick what to build or whether to build.** Scope comes from the
  user. Routing is the only thing on the table here.

## Why a separate call instead of just deciding

Because the interesting case is the one where your own first instinct and the
evidence disagree. When they agree, this skill is noise. When they do not, a
calibrated `choice` with a full probability distribution is a better basis for
asking the user a useful question than a coin flip between two plausible
options — and `confidence` tells you when the question itself is not worth
asking.
