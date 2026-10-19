---
name: prompt-refiner
description: Refine a short or incomplete user request into a safe, structured, directly reusable prompt. Use when the user asks to create, improve, standardize, or review a prompt; do not use when they ask to perform the underlying task directly.
metadata:
  version: 1.1.0
  language: follow-user-language
---

# Prompt Refiner

Turn rough intent into an implementation-ready prompt. Refine first; generate from scratch only when the user has supplied no usable draft.

## Trigger and routing

Use this skill when the user asks to:

- refine, polish, generate, standardize, or review a prompt;
- turn a requirement into a prompt, template, or agent instruction;
- add scope, constraints, output format, placeholders, or validation criteria to a prompt.

Do not use it when the user directly asks to execute the underlying task, for example: "compare these GKE clusters". Execute that task under the host agent's normal rules unless the user first asks for a prompt.

## Modes

- `generate` (default): return a polished prompt only. Do not execute it.
- `plan`: return an execution plan, commands, and risk notes; do not make changes.
- `execute`: run the task only after the user explicitly requests execution. Obey host-agent permissions and require any applicable approval before production changes.

Never interpret `execute` as permission to modify production resources without explicit authorization.

## Workflow

1. Identify the user's objective, intended audience/agent, domain, desired result, constraints, and output format.
2. Preserve every explicit requirement. Remove contradictions only after calling them out or choosing the safer interpretation.
3. Ask only for blocking information that cannot safely be represented as a placeholder. Do not ask optional questions by default.
4. For unprovided resource identifiers, use explicit placeholders such as `{{PROJECT_ID}}`, `{{CLUSTER_NAME}}`, and `{{LOCATION}}`. Never guess names, IDs, accounts, regions, or permissions from context.
5. Apply relevant domain rules from `references/` when the request calls for them. For GCP/GKE, read `references/gcp-gke.md`.
6. Produce the prompt in the user's language. Keep commands, flags, YAML keys, APIs, and other technical syntax in their native form. Honor an explicit language request.
7. Run the self-check before emitting the final prompt.

## Backfill policy

Classify missing information before asking:

| Class | Handling |
| --- | --- |
| Blocking | Ask only if neither a safe default nor a clear placeholder can make the prompt usable. |
| Sensitive or resource-specific | Use a placeholder; never infer a value. |
| Optional | Use a stated default or an optional section; do not ask by default. |
| Preference | Follow an explicit request; otherwise use concise Markdown output. |

State defaults in the generated prompt where they affect behavior. Add a short **Missing information** section when unresolved placeholders remain.

## Prompt shape

Use the following sections when applicable:

1. Role and operating mode
2. Objective and success criteria
3. Context and confirmed inputs
4. Scope and explicit exclusions
5. Constraints and safety boundaries
6. Required process or evidence collection
7. Output format
8. Validation, failure handling, and rollback considerations
9. Missing information / placeholders

Avoid decorative detail. Match depth to the requested task: concise prompts should remain concise.

## Self-check before emit

Confirm all applicable items are present:

- role, objective, context, constraints, process, output, and acceptance criteria;
- confirmed values are distinguished from placeholders and unknowns;
- read/write boundary and approval requirements are explicit;
- failure, unavailable access, and insufficient-permission paths are defined;
- language follows the user request;
- commands are safe for the declared mode;
- no resource identifier, credential, or environment value has been invented.

Automatically repair omissions. If a repair would change scope materially, present it as an assumption rather than silently adding it.

## Iteration and versioning

For an incremental request such as "add DNS audit" or "remove workload checks", modify the current prompt while preserving unchanged requirements. When asked to compare versions, show a concise, meaningful diff. Suggest saving durable prompts as `prompts/YYYYMMDD-<task-name>.md` only when it would be useful; do not write files unless asked.

## Reference freshness

References may contain stable patterns rather than exhaustive, current product-field lists. If a referenced file is more than six months past `last_verified`, add: "Verify product-specific flags and fields against current official documentation before execution."
