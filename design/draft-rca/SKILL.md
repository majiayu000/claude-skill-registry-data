---
name: draft-rca
description: Trace a reported defect from symptom to specific root cause — the file, the logic, and why it is wrong — and author rca.yaml plus resolution-trace.yaml (when LTM context provided). Used by tech-designer in the fix-it play.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob, Bash
---

# draft-rca

Model-invocable skill for root-cause analysis artifact authorship.

## Purpose

Given an issue description and codebase access, trace the reported symptom through the call chain to the specific line/logic/assumption that is wrong, enumerate blast radius, and write `rca.yaml`. When `ltm_context` is provided, also write `resolution-trace.yaml` per the R1–R4 resolution protocol.

This is the RCA-authoring mechanism for the fix-it play — tech-designer invokes it instead of authoring YAML inline.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `issue_read_path` | yes | Path to issue-read.yaml produced by manage-issue (title, body, state) |
| `project_root` | yes | Codebase root for read-only exploration |
| `ltm_context` | optional | `{project_base, core_base, query_domains, locked_artifacts}` for R1–R4 resolution |
| `output_base` | yes | Directory to write rca.yaml (and resolution-trace.yaml if ltm_context provided) |

## Process

1. **Read the issue.** Extract title, body, reported symptoms, stack traces, user-reported behavior.

2. **Reproduce understanding.** State the failure in one sentence, separating symptom from the assumed cause.

3. **Trace the symptom.** Use Grep/Glob/Read/`git log`/`git blame` to walk from where the error manifests back through the call chain to the originating logic.

4. **Pinpoint root cause.** Identify the specific file + line range + the exact logic or assumption that is wrong. Restating the issue title is NOT a root cause — the output must name a file path and describe the wrong logic.

5. **Map blast radius.** Enumerate every file affected by a fix to this root cause with its role and what would need to change.

6. **LTM resolution (when ltm_context present).** Follow R1–R4 from `standards/rules/resolution.md`:
   - R1: Identify decision domains
   - R2: Search `project_base` — LOCKED authoritative, DRAFT advisory
   - R3: Search `core_base` via `_index.md` and `Search patterns:` headers
   - R4: Unresolved → LLM, flag as `resolved_from: "llm"`
   - Write `resolution-trace.yaml` with per-domain `resolved_from`.

7. **Emit rca.yaml:**

   ```yaml
   issue_number: {n}
   summary: "{one-sentence failure description, symptom vs. cause separated}"
   root_cause:
     file: "{path}"
     logic: "{what the code does}"
     why_wrong: "{why it produces the observed failure}"
     line_range: "{start}-{end}"
   trace:
     - step: "{symptom observed in X}"
     - step: "{follows to Y because...}"
     - step: "{originates at Z}"
   blast_radius:
     - path: "{file}"
       role: "{what this file does}"
       change_needed: "{what must change}"
   produced_at: "{ISO-8601}"
   ```

## Output

```yaml
rca_path: "{output_base}/rca.yaml"
resolution_trace_path: "{output_base}/resolution-trace.yaml"  # only when ltm_context present
root_cause_file: "{path}"
blast_radius_count: {n}
status: written
```

## Failure Modes

| What failed | Cause | Return |
|-------------|-------|--------|
| Cannot locate referenced code from issue | Symbol/path doesn't exist | `status: failed`, `reason: symbol_not_found`, `searched_for` |
| Root cause inconclusive after 2 self-recovery passes | Trace does not converge | `status: failed`, `reason: rca_inconclusive`, `paths_explored` |
| Issue file unreadable | I/O | `status: failed`, `reason: missing_input` |

## Boundaries

- Read-only against the codebase. No git commit, branch, checkout, push, or any file write outside `{output_base}`.
- Restating the issue title as the root cause is forbidden — must name a file + logic + why-wrong.
- You do not design the fix (that is `draft-fix-design`'s job) and do not author tests (that is `author-regression-test`'s job).
