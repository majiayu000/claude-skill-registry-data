---
name: openrouter-free-responder
description: Zero-cost OpenRouter responder that auto-discovers the best currently free model, retries on failures, and returns clean answers fast. Use this when a user asks to query OpenRouter, wants lowest-cost/free model routing, or explicitly requests a free-model OpenRouter response.
metadata: {"openclaw":{"emoji":"🆓","requires":{"bins":["python3"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY","homepage":"https://openrouter.ai"}}
---

Use the bundled script to execute prompts against free OpenRouter models.

## Workflow

1. Ensure `OPENROUTER_API_KEY` is set.
2. Run:
   ```bash
   python3 {baseDir}/scripts/openrouter_free_chat.py --prompt "<user prompt>"
   ```
3. If the user provided system guidance, pass `--system "..."`.
4. Return the `response` text and mention which model was used.

## Command Options

- `--prompt` (required): User prompt text.
- `--system` (optional): System instruction.
- `--max-attempts` (optional, default `8`): Number of top free models to try.
- `--temperature` (optional, default `0.3`): Sampling temperature.
- `--debug` (optional): Print model ranking and fallback attempts to stderr.

## Output Contract

The script prints one JSON object to stdout with:

- `selected_model`: Model that produced the final response.
- `response`: Final assistant text.
- `attempted_models`: Ordered list of tried models.
- `free_model_candidates`: Number of free models discovered.

If no model succeeds, the script exits non-zero with an error message.
