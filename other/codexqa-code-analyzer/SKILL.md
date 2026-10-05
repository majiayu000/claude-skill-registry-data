---
name: codexqa-code-analyzer
description: >
  Queries a local CodexQA symbol graph for change review, regression scope,
  test gaps, error location, and entry risk. Use when the user mentions
  codexqa-code-analyzer, code-analyzer, codexqa, 符号图, 代码知识图谱, 建索引, 查调用, 影响面,
  --diff-base, 变更审查, 回归范围, 测试缺口, or asks to install / run the
  codexqa CLI (index, query). Former skill name: code-analyzer. Not CodexQA evidence-pack HTML review (that is codexqa-code-reviewer), not SAST + Agent LLM Detection code-risk scan reports (that is codexqa-defect-analyzer),
  and not architecture wiki reports (that is codexqa-code-wiki), and not full exception RCA reports (that is codexqa-rootcause-analyzer).
license: Apache-2.0
compatibility: >
  Requires Node.js >= 18 and the `codexqa` CLI
  (`npm i -g @openqa-cn/codexqa`) on PATH. Index and query need no LLM.
  Data lives in ~/.codexqa/.
metadata:
  author: open-source
  version: "1.0.0"
  open-standard: agentskills
---

# Code Analyzer

Local symbol graph for **quality work**: index first, then answer what changed, who is hit, what is untested, and where an error comes from.

There is **no** `codexqa diff` or `codexqa review`. Review a change with:

```text
index --diff-base <ref>  →  change-groups  →  symbol-diff  →  callers / tests / entries
```

Pick the scenario before acting. Do not query or review a diff until an index exists. Do not run full-text search unless the user asked.
`README.md` / `README.zh-CN.md` are human-facing. Do not load them at runtime.

## Documents (load on demand)

Read this file first. Read another file only when the row below applies. Do not preload the whole tree.

| File | Load when |
|---|---|
| `SKILL.md` (this file) | always: routing, report contract, reject conditions |
| [references/playbook.md](references/playbook.md) | entering a scenario (index health / change / defect / implementation / architecture) |
| [references/diagrams.md](references/diagrams.md) | before drawing; copy `init` and `classDef` verbatim |
| [references/cli.md](references/cli.md) | CLI missing, PATH, LLM, or maintenance |
| [references/mcp.json](references/mcp.json) | graph-query tool schema is needed |
| `README.md`, `README.zh-CN.md` | human-facing; not needed by the agent |

## Scenario routing

Open [references/playbook.md](references/playbook.md) and jump to the named section.

| User is asking… | Playbook section |
|---|---|
| Review a PR / what changed / vs main | **Review one change** (index health first) |
| Who is hit / what to regression-test | **Regression scope** under that change section |
| Any unit tests / coverage gaps | **Test gaps** under that change section |
| Which HTTP / RPC / MQ path reaches this | **Entry risk** under that change section |
| Auth, payments, password, token | **Sensitive paths** under that change section |
| Logs, stack, error text, comments | **Locate a defect** |
| How does this function work / who calls it | **Understand an implementation** |
| Module ownership / wrong layer | **Architecture drift** |
| Results are empty / every change is `default` | **Index health** / **Analysis blockers** |

## Report contract

Deliver a **Mermaid evidence report** (graph conclusions + diagrams). Not a product review, and not Archify / interactive HTML.
Read [references/diagrams.md](references/diagrams.md) before drawing. A diagram that misses the quality bar fails the report.

Report body is only these blocks:

- Must-read groups (by risk)
- What changed (trust only `symbol-diff` / `file-source` vs `file-base`)
- Must-test callers / entries (must come from `edges` / `reach` / `path` / `tagged`)
- Test gaps (a tests directory is not a `tests` edge)
- Sensitive paths (write "none" if there are none)
- **Diagrams**: at least one, and it must pass the quality bar

Reject the whole report and rewrite if any of these hold:

- Written as a generic project review (product intro, use cases, scored pros/cons)
- Evidence comes from README / a website / guesswork, not this run of `summary` / `imports` / `source` / `edges` / `reach` / `change-groups` / `symbol-diff`
- Only names large files or high fan-in; never uses `edges` / `reach` to say who is hit
- Infers "covered" from a tests directory name; never checked `tested_count` or `reach --direction in --edge-kinds tests`
- Mermaid is missing the Claude paper `init`, the three `classDef` lines, or a core module that should be `risk` has no `class ... risk`
- Architecture `subgraph` titles are package names (Renderer / Compiler / Shared) instead of **Entry → Application → Domain → Storage**
- Interactive HTML / Archify canvas was generated (this skill does not ask for that)
