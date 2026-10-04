---
name: delegate-agy
description: >-
    Gemini dispatch via Antigravity: image generation and Nano Banana, visual
    judgment of images, visual artifacts, screenshots, diagrams, and second-model
    critique returning taste and quality related findings. Use for "generate an image",
    "make a mockup", "visually confirm", for competing-design synthesis, visual validation,
    counterexample hunts, and on any mention of Gemini, Antigravity, or Nano Banana.
---

# [DELEGATE_AGY]

Antigravity is an external Gemini call admitted only where it adds capability beyond the local toolchain. Print mode runs the wrapper — one bounded prompt in, one JSON receipt out — yet executes tools and lands file writes without any permission flag, so safety is prompt discipline: a review or judgment prompt names no save path and directs inspect-only work; a generation prompt binds every save path to a throwaway scratch root, never a repo path or `$HOME`.

## [01]-[ROUTING]

[SCRIPTS]:
- [01]-[RUNNER](scripts/agy.py): wraps the CLI this skill invokes; carries `prompt` and `models` subcommands.

## [02]-[CAPABILITY]

| [INDEX] | [TRIGGER]                                                         | [WHY_GEMINI]                                      |
| :-----: | :---------------------------------------------------------------- | :------------------------------------------------ |
|  [01]   | Screenshots, generated images, UI states, visual diffs, diagrams  | Native multimodal judgment over `--add-dir` files |
|  [02]   | Critique or red-team stage wanting an independent second reviewer | Read-only findings from a different model lineage |
|  [03]   | Image generation, mockup and diagram iteration                    | Native `generate_image` rendering (Nano Banana)   |
|  [04]   | Competing designs, ambiguous tradeoffs, long-context synthesis    | Independent perspective outside the main context  |
|  [05]   | Vague requirements needing constraints and edge cases             | Ambiguity reduction as a separate pass            |
|  [06]   | Counterexamples, risk inventories, blind spots on gathered facts  | Adversarial second reading                        |
|  [07]   | Redacted log or dataset distillation in a scratch directory       | Pattern finding without polluting main context    |
|  [08]   | Explicit requests for Gemini, Antigravity, or Google Ultra        | User-directed routing                             |

## [03]-[MODEL_POLICY]

Wrapper defaults pin the strongest Gemini reasoning model at its highest tier; that pin is the carrier of a standing operator policy, never a tunable preference. Agents never choose models in ordinary use; `models` lists the live catalog for capability accounting and skill maintenance.

## [04]-[INVOCATION]

Run from this skill directory:

```sh copy-safe
uv run scripts/agy.py models
uv run scripts/agy.py prompt "Compare these two approaches and return the top 3 tradeoffs." --timeout 5m
uv run scripts/agy.py prompt "Assess the screenshot at /abs/path/shot.png and return concrete UI defects." --add-dir /abs/path --timeout 10m
```

Both halves bind the multimodal contract: `--add-dir` grants the bounded directory, and the prompt names each file by ABSOLUTE path — a granted directory with a bare filename in the prompt resolves nothing. `--add-dir` grants only directories that answer the prompt, and the only writes a wrapper prompt ever requests are generation artifacts under a scratch root.

`--log-file` routes the CLI log to an explicit path; a sandboxed or scratch-rooted environment passes a writable scratch path there instead of relying on the default log location. `AGY_BIN` overrides the binary path (default `agy`), `AGY_MODEL` overrides the pinned model, `AGY_LOG_FILE` sets the default log path, and `AGY_PRINT_TIMEOUT` overrides the default `5m` timeout.

Each `prompt` run returns one JSON receipt:

```json generated
{"op":"prompt","output":"..."}
{"op":"prompt","fault":"auth_required","detail":"..."}
```

`scripts/agy.py` owns the fault vocabulary the receipt's `fault` field carries: a new failure class is one `_Fault` row with its classifier tokens, and an unmatched failure classifies as `process_error`. `auth_required` resolves through interactive `agy` in a real TTY with Google OAuth as the account holding the Antigravity subscription.

## [05]-[PROMPT_CONTRACT]

- State the task, its context, and the exact output shape in one self-contained prompt; Antigravity sees only what that prompt carries.
- Carry the constraints that bind the answer: audience, files already inspected, limits, and facts not to assume.
- Ask for ranked options, deltas, typed findings, or a direct answer; open-ended commentary is never the request.

## [06]-[REVIEW]

A second-perspective review runs bounded critique and red-team: freeze the evidence, invert the objective, demand falsifiable findings. It inverts the every-agent-writes law at exactly this boundary — the Gemini reviewer inspects and returns typed findings, and a Claude writer adjudicates each finding against source before applying the fix; the repair rail never crosses to the reviewer.

- [EVIDENCE]: Subject arrives frozen — exact files under `--add-dir`, invariants under test, executed check output, known constraints.
- [CONTAMINANT]: A conversation transcript and a producer's self-justification never reach the reviewer.
- [OBJECTIVE]: Prompt directs disproof — violated invariants, omitted consumers, false assumptions, failure paths, visual-contract breaks.
- [BURDEN]: Work stays naive until it survives the attack, so a clean verdict is earned by an attack that finds nothing.
- [FINDINGS]: Each finding carries `{severity, invariant, evidence, failure_path, minimal_fix}`.
- [REJECTED]: Praise, style preference, and ungrounded speculation are shapes the prompt names rejected.
- [ADJUDICATION]: Claude re-derives each finding from disk, fixes true positives at the root, and refutes false ones with source, never by vote.

```sh copy-safe
uv run scripts/agy.py prompt "ROLE: read-only adversarial reviewer. SUBJECT: /abs/path/target. INVARIANT UNDER TEST: <invariant>. AUTHORITY: inspect only; propose, never edit. OUTPUT: a JSON array of findings only, each {severity, invariant, evidence, failure_path, minimal_fix}; reject praise, style preferences, and ungrounded speculation. Return [] only if a real attack finds nothing." --add-dir /abs/path --timeout 5m
```

## [07]-[GENERATION]

Image generation is the default agent's built-in `generate_image` tool, fired from inside an ordinary print-mode prompt — no CLI flag, subcommand, plugin, or `models` row invokes it. Every generation prompt carries three obligations: name the tool and forbid code-drawing (an unnamed request lets the agent fall back to scripting Pillow when the render fails), state the visual spec, and give an absolute save path under a scratch root the caller creates. Each render also persists as `<image_name>_<epoch-ms>.jpg` under `~/.gemini/antigravity-cli/brain/<conversation-id>/`.

```sh copy-safe
uv run scripts/agy.py prompt "Use your generate_image tool (never code-drawing) to generate: <visual spec>, aspect ratio 16:9. Save to /abs/scratch/name.png." --add-dir /abs/scratch --timeout 5m
```

Prompt prose carries everything; the agent maps it onto tool parameters: `Prompt`, `AspectRatio` (`1:1` default at 1024x1024; `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9` — `16:9` renders 1376x768), `ImagePaths` (up to 3 absolute paths to edit, combine, or reference — the edit modality: name the source by absolute path, state the change), and `ImageName`.

No tier selector exists in tool schema, CLI flags, or model catalog: the backend serves Nano Banana Pro where the account has access, Nano Banana otherwise; `--model` picks only the reasoning agent driving the tool.

Every render passes two gates. `magick identify` proves a real raster at the expected dimensions — the payload is JPEG whatever the extension unless the agent converts, so the filename is never format proof — and a wrapper read-back describes the artifact against the visual contract. A ~1KB file is the failure signature: the backend returned no image (`CORTEX_STEP_TYPE_GENERATE_IMAGE: no image generated in response` in the `--log-file`) and the agent code-drew a placeholder; the never-code-drawing clause and the size gate catch it, and one re-run resolves a transient backend miss.

Generated mockups and diagrams are inputs to the realizing skill, never deliverables: agy drafts the spec, renders, and read-back-critiques, then mermaid-diagramming realizes the fence. A closed loop is the strongest pattern — visual contract, render, read-back critique against the contract, targeted correction — never a single "make it pretty" round.

## [08]-[REFUSAL]

- [SECRETS]: OAuth codes, tokens, credential files, and unredacted sensitive logs never enter a prompt.
- [AUTHORITY]: Facts owned by local source, official docs, MCPs, or repo commands come from those owners, never from Antigravity recall.
- [ROUTINE]: Edits, formatting, git operations, package upgrades, and checks the local toolchain owns stay local.
- [SCOPE]: `prompt` and `models` are the wrapper's only surface; agent selection, background tasks, and shell-login subcommands stay outside it.

Interactive `agy` in a real TTY owns the outside surfaces — ongoing conversations, workspace tool permissions, resume, plugin management, sandboxed project work; `agy --help` is the flag and subcommand contract. `gsd-*` personas are interactive-runtime composition only: they hang under plain print mode and emit process narration rather than bounded answers under `--mode plan`, so a bounded one-shot runs the default agent with a strong prompt, never a gsd persona.

GSD's artifact pipeline — mapper, researcher, planner, checker, executor, verifier — composes inside a live session where each role consumes only the prior role's artifact.
