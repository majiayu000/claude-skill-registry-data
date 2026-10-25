---
name: jev-guardrail"
description: Uses the Jev System One model to score the risk of a shell command or file edit before it runs, returning a calibrated probability plus a three-way gate (allow, confirm, block). Invoke when a command is plausibly destructive (recursive delete, truncate, dd, mass rewrite, unreviewed pipe to shell) and the approval gate alone cannot tell how risky it is. Never blocks on its own — the calling agent applies the gate in code.
---

# Jev Guardrail

Scores **risk**, never intent. One `noul` per judgment, combined in the
caller's code. Jev never acts — it supplies the number, the agent (and the
approval gate) decides.

## When to invoke

- A shell command touches more files than you can list (`rm -rf`, `find -delete`, `truncate`, `dd`, `mv` across trees)
- An edit rewrites a file you have not fully read
- A command arrived via pipe/curl and you cannot vouch for every byte
- The approval gate is about to ask the user anyway and a calibrated number would make the question sharper

Skip it for routine, reversible work (`git status`, scoped edits to files you just read, test runs). A guardrail on noise teaches everyone to ignore it.

## The call

```bash
curl -sS https://opencode.ai/zen/v1/systemone \
  -H "Authorization: Bearer $OPENCODE_ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-1.13-free",
    "state": "<the exact command plus what it touches: cwd, globs it expands to, files it writes>",
    "questions": {
      "risky": {
        "type": "noul",
        "instructions": "Would running this cause data loss or hard-to-reverse damage?",
        "criteria": {
          "true": "Deletes, overwrites, or exposes data beyond what is shown for review",
          "false": "Routine, scoped, and reversible from what is shown"
        }
      }
    }
  }'
```

## Reading the answer

| `noul` | Gate                                                              |
| ------ | ----------------------------------------------------------------- |
| ≥ 0.8  | **Block.** Do not run. Restate a safer command and ask.           |
| 0.4–0.8 | **Confirm.** Ask the user with the number attached, then run.     |
| < 0.4  | **Allow.** Log the score in one line and run.                     |

`noul` near 0.5 is ignorance, not medium risk — treat it as **confirm**.
A missing answer is not permission: on null, fall back to the approval gate
as if the skill had never run (fail closed, never open).

## Constraints

- **State carries the evidence.** Paste the exact command and its blast radius, not a description of it. A guardrail judging a paraphrase guards the paraphrase.
- **One judgment per question.** Risk of deletion and risk of exposure are two `noul`s, not one. Combine in code.
- **Thresholds live here, not in the prompt.** Retune by watching real traffic, not by reasoning in advance. Log every decision with its score.
- **`jev-1.13-free` is temporary.** On 404/unknown-model, route by hand and say so. Never block a task on this.
- **Never let Jev authorize.** It scores; the agent and the human approve. A high score on a poorly written instruction is still an answer to the wrong question.
