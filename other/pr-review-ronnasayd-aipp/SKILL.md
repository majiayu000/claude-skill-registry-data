---
name: pr-review
description: Systematic PR review using GitHub MCP tools. Produces structured report with summary of changes, critical bugs, minor issues, code examples, and external references. Use when user says "review PR", "analyze PR", "check PR", "give feedback on PR", or shares a GitHub PR URL to evaluate. Works for any language or framework.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# PR Review

Systematic pull request review using GitHub MCP tools. Produces a structured report covering what the PR does, critical bugs, minor issues, code fixes, external references, and merge recommendation.

## Steps

| #   | Step                | Action                                                               | Output / Gate                                                                       |
| --- | ------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 1   | Metadata (parallel) | `pull_request_read method: get` + `method: get_files` simultaneously | title, description, author, base branch, file count, +/- lines, requested reviewers |
| 2   | Full diff           | `pull_request_read method: get_diff`                                 | authoritative source for exact line numbers — `get_files` patches are truncated     |
| 3   | Map files → layer   | Classify each changed file against layer table below                 | flag any file working outside its layer as 🟡 minimum                               |
| 4   | Review each file    | Apply correctness/architecture/security/consistency checklist below  | list of findings per file                                                           |
| 5   | Classify findings   | Severity table below                                                 | every finding tagged 🔴/🟡/⚪                                                       |
| 6   | External references | `WebSearch` per 🔴 and significant 🟡, using query patterns below    | link per finding                                                                    |
| 7   | Fix examples        | Write minimal surgical fix per 🔴/🟡 (format below)                  | code block per finding                                                              |
| 8   | Deliver report      | Structured report (template below)                                   | done                                                                                |

## Layer map (Step 3)

| Layer                                  | Expected responsibility                |
| -------------------------------------- | -------------------------------------- |
| Entry point (controller/handler/route) | Receive input, delegate, return output |
| Service / use case                     | Business logic                         |
| Worker / job / task / queue            | Isolated async processing              |
| Model / entity / schema                | Data structure                         |
| Repository / DAO                       | Data access                            |
| Adapter / client                       | External communication                 |
| Config / infra / scheduler             | Configuration, scheduling              |

## Review checklist (Step 4)

- **Correctness**: vars used before init; null/empty/zero handled before use; return values checked; edge cases covered (empty list, zero, null)
- **Architecture**: file only does its layer's job; deps injected not instantiated internally; no illegal cross-layer coupling
- **Security**: external input validated/sanitized; no hardcoded secrets; no injection vectors (SQL/command/template); destructive ops permission-gated
- **Consistency**: names correct across files; comments/docs match actual behavior; style matches surrounding code

## Severity (Step 5)

| Symbol | Severity | Criterion                                                |
| ------ | -------- | -------------------------------------------------------- |
| 🔴     | Critical | Runtime failure, data loss, or security breach           |
| 🟡     | Minor    | No immediate breakage, future risk or maintenance burden |
| ⚪     | Debt     | Architectural/quality issue — separate task              |

Rule: wrong behavior in production with no visible error → 🔴 automatically.

## WebSearch query patterns (Step 6)

| Category              | Query pattern                              |
| --------------------- | ------------------------------------------ |
| Language behavior     | `[language] [behavior] spec`               |
| Framework antipattern | `[framework] [pattern] best practice`      |
| Security              | `[vulnerability name] OWASP`               |
| Performance           | `[operation] performance [db/runtime]`     |
| Future breakage       | `[language] RFC [behavior] future version` |

## Fix format (Step 7)

```
File: path/to/file.ext — line N

// PROBLEM: one-line description
[problematic code]

// FIX
[corrected code — minimum necessary change]
```

Rules: surgical fix only; larger refactors → ⚪ debt as separate task; never mix bug fix with style cleanup in one example.

## Report template (Step 8)

```markdown
## What the PR does

| # | Feature | Detail |

## Problems Found

### 🔴 Critical

For each: **Cause** / **Impact** / **Fix** (code block) / **Reference** (link)

### 🟡 Minor

| File | Line | Problem |

### ⚪ Technical Debt

- bullet list of what to handle separately

## Fix Priority

| Priority | Fix | Effort |

## Recommendation

One line: safe to merge / do not merge / merge after fixing X
```

## Reference files

- `references/examples.md` — three worked examples (undefined variable, architecture violation, doc/code mismatch)
- `references/troubleshooting.md` — empty diff, truncated patches, missing line numbers, oversized output pagination
