---
name: dify-python-code-node
description: Create, modify, review, and test Python3 code used inside Dify Code nodes. Use for every new or materially changed Python Code node, including input/output contract design, deterministic parsing, validation, normalization, array/object handling, and source-file maintenance. Do not use for graph wiring, node placement, or whole-workflow YAML authoring.
---

# Dify Python Code Node

Own the Python source and its input/output contract. The companion `dify-dsl` skill owns workflow graph wiring, YAML serialization, and layout.

## Scope Boundary

- Apply this skill to every new or materially revised Python Code node. Do not rely on a subjective "complex code" threshold.
- Reusing an unchanged registered script does not require rewriting it.
- Prefer native Dify nodes such as Template Transform for trivial templating instead of creating unnecessary Code nodes.
- Do not edit the whole DSL. Return a source artifact and a contract that `dify-dsl` can bind into the graph.

## Source Storage

1. Follow repository instructions when they define a Code source registry.
2. When the target DSL is under `dev-dsl/`, store source under `docs/dify-code-nodes/`. This repository mode is strict: every Code node must include `Code source: <path>` in `data.desc` and the embedded code must match the file.
3. Otherwise, store reusable sources under `dify-code-nodes/` at the project root unless the user requests chat-only code.
4. Use descriptive snake_case filenames and group workflow-specific scripts in a subdirectory.

## Implementation Requirements

- Define a top-level `main(...)` function and return a dictionary.
- Keep input parameter names identical to Dify Code node input names.
- Keep every statically returned key represented in the output contract.
- Prefer Python standard library dependencies unless the target sandbox is known to include more.
- Do not use CLI arguments, stdin/stdout, shell commands, local file I/O, or environment variables inside Code node code.
- Do not make network calls unless the user explicitly requires them and the target sandbox behavior is known.
- Use deterministic parsing and transformation logic. Return branchable validation fields for expected input errors instead of raising.
- Keep deep or installation-specific payloads shallow when returned as Object values. Add a JSON String twin only when a real downstream consumer needs the full payload.
- Do not hardcode a universal maximum array length. Instance limits are configurable; use a target-specific limit only when the target runtime or repository policy establishes one.
- Include concise `Dify input variables:` and `Dify output variables:` comments before `main(...)`.

## Workflow

1. Read the downstream requirements supplied by `dify-dsl` or the user.
2. Define the smallest useful input/output contract.
3. Write or update the canonical `.py` source.
4. Add focused tests for parsing, invalid input, boundary behavior, and output shape when a test structure exists.
5. Run Python syntax/tests without executing unavailable Dify services.
6. Return the handoff contract described in [references/handoff-contract.md](references/handoff-contract.md).

## Final Handoff

Always report:

- canonical source path;
- inputs with Dify type, required status, and expected selector/value source;
- outputs with Dify type and downstream purpose;
- branch and iteration fields, when present;
- tests executed and any target-runtime assumptions.

The caller must embed the exact source text into `data.code`; do not provide a second independently edited inline implementation.
