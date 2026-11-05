---
name: ai-code-review-catalog
description: available code reviewers, review prompts and model routing
disable-model-invocation: true
---

<reviewers>

- `/cross-harness-sub-agent` with a short broad review prompt written by the main agent
- native sub-agent reading and following [/thermo-nuclear-code-quality-review](../thermo-nuclear-code-quality-review/SKILL.md)
- native sub-agent using `prompts/ponytail-review.md`
- native sub-agent using `prompts/code-review.md`
- harness's native code review agent
- `codex` cli native review through the shared launcher:
  ```bash
  bin/codex-native-review origin/develop
  # optional evidence and output location:
  bin/codex-native-review origin/develop playground/review-handoffs playground/checks.md
  ```
  - when using exact-commit verification evidence, run from a clean, committed checkout; output is a fresh directory containing `review.md` and `review.log`
  - when the parent harness is sandboxed, launch the helper outside that parent sandbox with an escalated shell command; the reviewer itself remains `--sandbox read-only`
  - the helper supplies source-inspection instructions through `developer_instructions`, since `codex review --base` rejects a positional prompt
  - verification belongs to the caller or CI. supply existing evidence with its exact commit, commands or CI links, scope and pass/fail/pending status; the reviewer reports gaps instead of running write-dependent checks
  - retain the report and log on failure; launcher permission failures need the correct parent launch context, not another identical attempt

</reviewers>

<prompts>

- code review prompt: `prompts/code-review.md`
- ponytail review prompt: `prompts/ponytail-review.md`
- bug-class review prompt: `prompts/bug-class-review.md`

</prompts>

native sub-agent model routing:

| harness     | model                       | reasoning                   |
| ----------- | --------------------------- | --------------------------- |
| codex       | gpt-6.1-sol                 | high                       |
| claude code | claude-opus-5-5              | high                        |
| other       | what the harness recommends | what the harness recommends |

don't use fast mode
if a command fails, try similar variants
if a cli tool is not installed/authenticated, skip it
