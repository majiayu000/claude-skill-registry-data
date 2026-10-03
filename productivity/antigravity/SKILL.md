---
name: antigravity
description: Use Google Antigravity CLI (`agy`) for independent code or plan review, large-context analysis, and a second-model opinion. Trigger on Antigravity CLI, agy, Google CLI review, or requests that previously used the Gemini CLI runtime.
---

# Antigravity CLI

Google Antigravity CLI is the Google command-line runtime. Gemini remains a model family; do not invoke the retired `gemini` executable.

## Workflow

1. Verify the runtime with `agy --version`. If it is unavailable, report that Antigravity CLI must be installed or repaired; do not fall back to `gemini`.
2. Run `agy models` when model choice matters. Use a currently listed model and never hardcode a preview model from memory.
3. Give Antigravity a bounded prompt that names the files, question, required evidence, and output format.
4. Prefer read-only review. Grant write or command permissions only when the user asked Antigravity to modify or execute something.
5. Capture the result, verify actionable claims against the repository or tests, and distinguish Antigravity findings from confirmed facts.

## Headless usage

```bash
agy -p "Review the authentication flow. Cite file:line evidence and list only actionable findings." --output-format json
```

Optional controls:

- `--model <id>`: choose an ID returned by `agy models`.
- `--effort <level>`: tune reasoning effort when supported by the selected model.
- `--output-format text|json|stream-json`: select machine-readable output for automation.
- `--continue` or `--conversation <id>`: resume an existing Antigravity conversation.

Use a timeout supplied by the host runner for background jobs. Never use obsolete Gemini CLI flags such as `--approval-mode`, `--sandbox`, `--yolo`, or `-i`.

## Permission boundary

Use Antigravity's configured permission policy for routine automation. `--dangerously-skip-permissions` bypasses safety prompts and is allowed only when the user explicitly authorized unrestricted tool execution for that run. A request for review or analysis alone is not that authorization.

## Result contract

Return:

- the model ID used, when explicitly selected;
- the useful findings or recommendation;
- which claims were independently verified;
- any timeout, authentication, permission, or parse failure.

Do not present an Antigravity opinion as test evidence.
