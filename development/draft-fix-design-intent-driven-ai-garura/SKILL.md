---
name: draft-fix-design
description: Given a completed rca.yaml, design a fix with at least one alternative considered and rejection reason, affected-files map with change specifications, and a self-sufficient execution plan. Writes design.yaml.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob, Bash
---

# draft-fix-design

Model-invocable skill for fix design artifact authorship.

## Purpose

Given a root-cause analysis, design the minimal safe fix, document at least one alternative and its rejection reason, produce an affected-files map with concrete change specifications, and write a step-by-step execution plan. Emit `design.yaml`.

This is the fix-design authoring mechanism for the fix-it play — tech-designer invokes it instead of authoring YAML inline.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `rca_path` | yes | Path to rca.yaml produced by draft-rca |
| `project_root` | yes | Codebase root for read-only exploration |
| `ltm_context` | optional | Same shape as draft-rca's ltm_context; surfaced so the design can cite LTM-backed patterns |
| `output_base` | yes | Directory to write design.yaml |

## Process

1. **Read RCA.** Extract root-cause file + logic + why-wrong + blast-radius.

2. **Explore change context.** Read the affected files. Understand the surrounding patterns, error-handling conventions, and test structure.

3. **Choose fix strategy.** Select the minimal intervention that resolves the root cause without widening scope. Prefer local fixes over refactors unless the root cause is structural.

4. **Consider alternatives.** Generate at least one alternative approach. For EACH alternative, record a concrete `rejection_reason` (not "less clean" — name the tradeoff: risk, scope, compatibility, test complexity).

5. **Affected-files map.** For every file the fix will touch:
   - `path`
   - `role` — what this file does
   - `action` — `create | modify | delete`
   - `change` — specific change in the form "X → Y" or describing the inserted/removed block
   - `risk` — low | medium | high
   - `risk_rationale` — one line

6. **Execution plan.** Ordered steps that a code-builder can follow without additional context. Each step:
   - `id`
   - `description`
   - `files` list with action + details
   - `expected_outcome`
   - `self_test` — how to verify the step worked (may reference the regression test that `author-regression-test` will produce)

7. **Confidence.** `high | medium | low` + one-line rationale.

8. **Emit design.yaml:**

   ```yaml
   based_on_rca: "{rca_path}"
   strategy: "{one-paragraph fix approach}"
   alternatives_considered:
     - option: "{name/description}"
       rejection_reason: "{concrete tradeoff}"
   affected_files:
     - path: "{file}"
       role: "{what it does}"
       action: create | modify | delete
       change: "{specifics}"
       risk: low | medium | high
       risk_rationale: "{one line}"
   execution_plan:
     - id: step-1
       description: "{what to do}"
       files: [ {path, action, details} ]
       expected_outcome: "{what success looks like}"
       self_test: "{verification}"
   confidence: high | medium | low
   confidence_rationale: "{one line}"
   produced_at: "{ISO-8601}"
   ```

## Output

```yaml
design_path: "{output_base}/design.yaml"
alternatives_count: {n}  # MUST be >= 1
affected_files_count: {n}
execution_steps: {n}
status: written
```

## Failure Modes

| What failed | Cause | Return |
|-------------|-------|--------|
| RCA file missing | I/O | `status: failed`, `reason: missing_input` |
| RCA root_cause absent/empty | Upstream contract broken | `status: failed`, `reason: invalid_rca` |
| Alternatives list empty after self-recovery | Could not generate an alternative | `status: failed`, `reason: no_alternatives` (blocks F3) |

## Boundaries

- Read-only against the codebase.
- Every alternative must carry a concrete `rejection_reason`. A list with only the chosen strategy is a failure (violates F3 of /fix-it).
- You do not implement the fix and do not author the regression test.
