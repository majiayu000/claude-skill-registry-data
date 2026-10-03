---
name: code-review-deep
description: "Comprehensive deep code review covering 10 dimensions: correctness, security, performance, reliability, architecture, data integrity, maintainability, consistency, observability, and documentation. Uses 7 parallel review agents for thorough analysis and generates a structured report. Auto-detects all programming languages and frameworks from the diff. Use when the user requests a deep code review, comprehensive review, full review, thorough review, security audit, architecture assessment, code quality analysis, performance review, or mentions /code-review-deep. Also suitable for pre-merge final review, post-refactor review, new project code audit, or any request for a multi-dimensional code review. Supports focus mode (--focus security,performance) and large diff chunking. Do not use for: understanding code structure or a change without quality judgement (use code-read-deep-*), diagnosing one concrete bug or incident (use systematic-debugging), writing or designing tests (use code-testing), slimming redundant code (use code-slimming), or deciding whether a design pattern is warranted (use design-pattern-advisor)."
---

# Deep Code Review (code-review-deep)

A comprehensive, multi-dimensional code review skill that uses 7 parallel agents to analyze code changes across 10 review dimensions. Supports all programming languages with automatic detection and dynamic adaptation.

## Review Dimensions

| # | Dimension | Agent |
|---|-----------|-------|
| 1 | Correctness | Agent 1 |
| 2 | Security | Agent 2 |
| 3 | Performance | Agent 3 |
| 4 | Reliability | Agent 3 |
| 5 | Architecture & Design | Agent 4 |
| 6 | Data Integrity | Agent 5 |
| 7 | Maintainability | Agent 6 |
| 8 | Documentation | Agent 6 |
| 9 | Consistency | Agent 7 |
| 10 | Observability | Agent 7 |

## Workflow

Execute the following 4 phases in order. Do NOT skip any phase.

---

### Phase 1: Context Gathering

**You (the main agent) perform this phase directly.** Gather all context needed before dispatching review agents.

#### Step 1.1: Determine Review Scope

Detect the review scope from user input:

- **PR diff** (default): Run `git diff main...HEAD` or `git diff <base>...HEAD` if user specifies a base branch
- **Staged changes**: If user mentions "staged" or "cached", run `git diff --cached`
- **Working tree**: If user mentions "uncommitted" or there's no upstream, run `git diff HEAD`
- **Specific files/dirs**: If user specifies file paths, scope the review to those files
- **PR number**: If user provides a GitHub PR number, use `gh pr diff <number>`

If the diff is empty, inform the user and stop.

#### Step 1.2: Collect Context

Run these commands in parallel:

1. `git diff <scope>` — get the full unified diff
2. `git log --oneline -20` — recent commit history
3. Read CLAUDE.md files: root CLAUDE.md + any CLAUDE.md in directories touched by the diff
4. Check for framework config files in the repo (package.json, pom.xml, go.mod, Cargo.toml, requirements.txt, build.gradle, etc.)
5. `git diff <scope> --stat` — get file change statistics (additions/deletions per file)

#### Step 1.3: Auto-Detect Languages & Frameworks

From the diff and config files, identify:
- **Languages**: Detect from file extensions in the diff (e.g., `.java`, `.go`, `.py`, `.rs`, `.js`, `.ts`, `.kt`, `.swift`, `.rb`, `.php`, `.cs`, `.cpp`, `.c`, `.scala`, `.dart`, etc.)
- **Frameworks**: Detect from imports/config files (e.g., Spring, Django, Flask, React, Vue, Angular, Gin, Echo, Actix, Express, Next.js, etc.)
- **Build tools**: Detect from config files (Maven, Gradle, npm, pip, cargo, etc.)

Prepare a `language_context` summary string like:
```
Languages: Java, TypeScript
Frameworks: Spring Boot, React
Build tools: Maven, npm
```

#### Step 1.4: File Risk Classification

Classify each changed file into a risk tier based on its path and role:

| Risk Tier | Weight | Examples |
|-----------|--------|---------|
| **Critical** | 3x | Payment/billing, auth/security, data migration, core business logic, encryption, API gateway |
| **High** | 2x | Database models/repositories, API controllers/handlers, middleware, configuration, infrastructure |
| **Normal** | 1x | Business logic, services, utilities, UI components |
| **Low** | 0.5x | Documentation, static assets, generated code, CI config, README |

Classification rules:
- File path contains `auth`, `security`, `payment`, `billing`, `crypto`, `migration`, `gateway` → **Critical**
- File path contains `model`, `entity`, `repository`, `dao`, `controller`, `handler`, `middleware`, `config`, `infra` → **High**
- File path contains `test`, `spec`, `mock`, `fixture` → **Normal** (test quality is important; do NOT treat test files as low-risk)
- File path contains `doc`, `README`, `.md`, `assets`, `.generated`, `.ci`, `.github` → **Low**
- Everything else → **Normal**
- If uncertain, classify as **Normal**

Prepare a `risk_profile` summary:
```
Critical files: 2 (src/auth/jwt.go, src/payment/charge.go)
High files: 3 (src/models/user.go, src/api/handler.go, config/app.yaml)
Normal files: 5
Low files: 2
Overall risk tier: HIGH
```

#### Step 1.5: Large Diff Handling

Count the total lines in the diff. Apply one of these strategies:

- **Small diff (≤ 500 lines)**: Pass the full diff to all agents. No special handling needed.
- **Medium diff (501–2000 lines)**: Pass the full diff but instruct agents to prioritize Critical and High risk files. Include the `risk_profile` so agents know where to focus.
- **Large diff (2001–5000 lines)**: Split the diff by file. Group files into 2-3 chunks, prioritizing Critical/High files in Chunk 1. Each agent receives all chunks but is instructed to focus deeply on Chunk 1 and scan Chunk 2-3 at a higher level.
- **Very large diff (> 5000 lines)**: Inform the user that the diff is very large and suggest reviewing in smaller batches. If the user still wants a full review, split by file risk tier:
  - **Pass 1**: Review only Critical + High files (full depth)
  - **Pass 2**: Review Normal files (standard depth)
  - **Skip**: Low-risk files (mention them in the report as skipped)

For large/very large diffs, include this note in agent prompts:
```
NOTE: This is a large diff. Focus your deepest analysis on the files marked as
Critical and High risk. For Normal/Low risk files, only flag P0 and P1 issues.
```

#### Step 1.6: Focus Mode Detection

Check if the user specified `--focus` with dimension names:
- `--focus security` → Only dispatch Agent 2 (Security)
- `--focus security,performance` → Only dispatch Agent 2 + Agent 3
- `--focus correctness,data` → Only dispatch Agent 1 + Agent 5

Dimension name mapping for `--focus`:
| Input keyword | Agent(s) dispatched |
|---------------|-------------------|
| `correctness` | Agent 1 |
| `security` | Agent 2 |
| `performance` | Agent 3 |
| `reliability` | Agent 3 |
| `architecture` | Agent 4 |
| `data` / `data-integrity` | Agent 5 |
| `maintainability` | Agent 6 |
| `documentation` / `docs` | Agent 6 |
| `consistency` | Agent 7 |
| `observability` | Agent 7 |

If no `--focus` is specified, dispatch all 7 agents (default full review).

#### Step 1.7: Prepare Agent Input

Prepare the following data to pass to agents:
- `diff`: The full unified diff (or chunked diff for large diffs)
- `language_context`: The detected languages/frameworks string
- `claude_md_rules`: Contents of relevant CLAUDE.md files (or "No CLAUDE.md found")
- `file_list`: List of changed files with their paths
- `risk_profile`: File risk classification from Step 1.4
- `diff_size`: Total diff line count and handling strategy applied

---

### Phase 2: Parallel Deep Analysis

Launch agents simultaneously using the Agent tool. Send all in a **single message** so they run in parallel.

- **Full review** (no `--focus`): Launch all **7 agents**
- **Focus mode**: Launch only the agent(s) matching the focused dimensions

For each agent, read its reference file from `references/agent-<name>.md` and construct the prompt by including:

1. The agent's role and checklist (from the reference file)
2. The `diff` content
3. The `language_context`
4. The `claude_md_rules`
5. The `file_list`
6. The `risk_profile`

**IMPORTANT**: Each agent must return its findings as a **JSON array**. Instruct each agent to output ONLY a JSON array at the end of its response in this exact format:

```json
[
  {
    "id": "CORR-001",
    "dimension": "Correctness",
    "severity": "P0",
    "file": "path/to/file.ext",
    "line": 123,
    "summary": "One-line description of the issue",
    "description": "Detailed explanation of what is wrong",
    "impact": "What happens if this is not fixed",
    "fix_suggestion": "Concrete fix recommendation in natural language",
    "fix_code": "```lang\n// Suggested code replacement\n```",
    "confidence": 85,
    "language": "Java"
  }
]
```

**Field notes:**
- `fix_suggestion`: Natural language description of how to fix the issue
- `fix_code`: When possible, provide a concrete code snippet showing the corrected version. Use the original code's language and style. If the fix is too context-dependent to express as code, set to `""` (empty string). For P0 and P1 issues, always attempt to provide `fix_code`.

**Agent ID prefixes:**
- Agent 1 (Correctness): `CORR-NNN`
- Agent 2 (Security): `SEC-NNN`
- Agent 3 (Performance & Reliability): `PERF-NNN` / `REL-NNN`
- Agent 4 (Architecture & Design): `ARCH-NNN`
- Agent 5 (Data Integrity): `DATA-NNN`
- Agent 6 (Maintainability & Documentation): `MAINT-NNN` / `DOC-NNN`
- Agent 7 (Consistency & Observability): `CONS-NNN` / `OBS-NNN`

**Agent dispatch template:**

```
You are a specialized code review agent focused on [DIMENSION].

## Your Role
[Read and include content from references/agent-<name>.md]

## Context
- Languages & Frameworks: {language_context}
- CLAUDE.md Rules: {claude_md_rules}

## File Risk Classification
{risk_profile}

## Changed Files
{file_list}

## Diff to Review
{diff}

## Instructions
1. Read the entire diff carefully
2. For each changed file, also Read the full file to understand context around the changes
3. Prioritize analysis on Critical and High risk files — these deserve the deepest scrutiny
4. Apply your checklist from your role definition, adapting to the detected language(s)
5. For each finding, assess confidence (0-100) based on how certain you are it's a real issue
6. For P0 and P1 findings, you MUST provide a fix_code field with a concrete code fix
7. For P2-P4 findings, provide fix_code when the fix is straightforward
8. Return ONLY findings you believe are real issues with confidence >= 50
9. Output your findings as a JSON array at the end of your response

## Output Format
Return a JSON array of findings. If no issues found, return [].
Each finding must have: id, dimension, severity (P0-P4), file, line, summary, description, impact, fix_suggestion, fix_code, confidence, language
```

### Agent Failure Handling

After all agents complete (or timeout), apply these rules:

1. **JSON parse failure**: If an agent's response does not contain a valid JSON array, attempt to extract JSON from the response using these fallbacks in order:
   - Look for content between `[` and the last `]` in the response
   - Look for content inside a ```json code fence
   - If both fail, treat this agent's output as `[]` (no findings) and note the failure in the report
2. **Agent timeout or error**: If an agent fails to return within the allotted time or returns an error, treat its dimensions as `[]` and note in the report: "Agent X (Dimension) did not complete — results may be incomplete for this dimension"
3. **Partial results**: Proceed with whatever agents did return. The review is still valuable with partial coverage. The report should clearly indicate which dimensions were fully analyzed.
4. **All agents failed**: If all 7 agents fail, inform the user and suggest retrying or using a simpler review scope.

---

### Phase 3: Cross-Validation & Deduplication

After all agents complete (or timeout), process their results:

#### Step 3.1: Parse Results

Extract the JSON array from each agent's response using the failure handling rules above. Track which agents returned valid results.

#### Step 3.2: Merge & Deduplicate

Combine all findings into a single list, then deduplicate:
- **Same file + same line range (within 5 lines) + same root cause** → keep the one with higher confidence, note corroboration
- When merging duplicates, boost the surviving finding's confidence by +15 for each corroborating agent

#### Step 3.3: Confidence Adjustment

Apply these adjustments to each finding's confidence score:

**Boosters:**
- **Multi-agent corroboration**: +15 per additional agent that flagged the same issue
- **Violates explicit CLAUDE.md rule**: +10 if the finding directly contradicts a CLAUDE.md instruction
- **Critical file**: +10 if the issue is in a Critical-risk file
- **High file**: +5 if the issue is in a High-risk file

**Reducers:**
- **Pre-existing issue**: -30 if the issue exists on lines NOT modified in the diff
- **Pure style without CLAUDE.md backing**: -20 if it's purely stylistic and not backed by CLAUDE.md
- **Linter/compiler catchable**: -15 if a standard linter or compiler would catch this
- **Low-risk file**: -10 if the issue is in a Low-risk file and severity is P2 or below

Cap confidence at 100, floor at 0.

#### Step 3.4: Filter

Remove all findings with adjusted confidence < 60.

#### Step 3.5: Rank

Sort remaining findings by:
1. Severity (P0 first)
2. File risk tier (Critical first)
3. Confidence (highest first)
4. Dimension (Correctness > Security > Performance > ... > Documentation)

---

### Phase 4: Report Generation

#### Step 4.1: Calculate Overall Risk Score

Compute a risk score (0-100) for the entire change using this formula:

```
risk_score = 0

For each surviving finding:
  weight = severity_weight × file_risk_weight × (confidence / 100)
  risk_score += weight

Severity weights: P0=25, P1=15, P2=8, P3=3, P4=1
File risk weights: Critical=3, High=2, Normal=1, Low=0.5

Cap risk_score at 100.
```

Map risk score to risk level:

| Score | Risk Level | Label |
|-------|-----------|-------|
| 0 | None | 🟢 无风险 |
| 1-20 | Low | 🟢 低风险 |
| 21-40 | Medium | 🟡 中风险 |
| 41-60 | High | 🟠 高风险 |
| 61-80 | Very High | 🔴 很高风险 |
| 81-100 | Critical | 🔴 严重风险 |

#### Step 4.2: Generate Report

Generate the final report in **Chinese** (per user's CLAUDE.md rule #1). Use the following template:

```markdown
# 深度代码审查报告

## 审查信息
- **审查范围**: {scope description}
- **变更文件**: {file_count} 个
- **变更行数**: +{additions} / -{deletions}
- **检测语言**: {languages}
- **检测框架**: {frameworks}
- **审查维度**: {n} 个维度 / {n} 个并行审查代理
- **审查模式**: {全量审查 | 聚焦审查: security, performance | 分片审查(大diff)}

## 变更风险评估

**风险评分**: {score}/100 {risk_emoji} {risk_label}

**风险依据**:
- {1-3 句话解释为什么给出这个风险评分，引用最关键的发现}

**文件风险分布**:
| 风险层级 | 文件数量 | 涉及文件 |
|---------|---------|---------|
| 🔴 关键 | {n} | `file1.ext`, `file2.ext` |
| 🟠 高 | {n} | `file3.ext`, `file4.ext` |
| 🟢 普通 | {n} | (省略列表) |
| ⚪ 低 | {n} | (省略列表) |

## 总体评估

**合并建议**: {recommendation}
- 若存在 P0: "❌ 不建议合并 — 存在严重问题需要修复"
- 若存在 P1 但无 P0: "⚠️ 修复后合并 — 存在高优先级问题"
- 若仅有 P2 及以下: "✅ 可以合并 — 建议关注以下改进点"
- 若无发现: "✅ 可以合并 — 未发现问题"

**问题统计**:
| 级别 | 数量 | 说明 |
|------|------|------|
| P0 严重 | {n} | 合并前必须修复 |
| P1 高 | {n} | 应在合并前修复 |
| P2 中 | {n} | 建议修复或创建跟进 |
| P3 低 | {n} | 建议改进 |
| P4 信息 | {n} | 仅供参考 |

## 发现详情

### P0 严重问题

#### [DR-001] {summary}
- **维度**: {dimension}
- **文件**: `{file}:{line}` ({risk_tier} 风险文件)
- **置信度**: {confidence}/100
- **问题描述**: {description}
- **影响分析**: {impact}
- **修复建议**: {fix_suggestion}
- **建议修复代码**:
{fix_code}

(repeat for each finding, grouped by severity level)
(for P2-P4, fix_code is optional — only include when provided)

## 代码亮点

List 2-3 things the code does well. If the code is generally good quality, say so.
This section helps balance the review and acknowledge good work.

## 维度总结

| 维度 | 状态 | 发现数量 | 简评 |
|------|------|---------|------|
| 正确性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 安全性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 性能 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 可靠性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 架构与设计 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 数据完整性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 可维护性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 一致性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 可观测性 | ✅/⚠️/❌ | {n} | {one-line summary} |
| 文档 | ✅/⚠️/❌ | {n} | {one-line summary} |

Status: ✅ = no issues, ⚠️ = P2-P4 issues only, ❌ = P0 or P1 issues

If an agent failed or timed out, mark its dimensions as:
⏳ = agent did not complete (results may be incomplete)
```

**When agents failed**, add this section after 审查信息:
```markdown
## ⚠️ 审查完整性说明
以下维度的审查代理未能正常返回结果，相关维度的审查可能不完整：
- {dimension}: {failure reason}
建议针对这些维度进行手动审查或重新运行。
```

If no findings survive filtering, output a short report:
```markdown
# 深度代码审查报告

## 审查信息
(same as above)

## 变更风险评估
**风险评分**: 0/100 🟢 无风险

## 总体评估
**合并建议**: ✅ 可以合并 — 未发现问题

已对代码进行 {n} 个维度的深度审查，未发现需要关注的问题。

## 代码亮点
(list good things about the code)
```

---

## False Positive Guidance

These are NOT issues — do not include them in findings:

1. **Pre-existing issues**: Problems on lines not modified by the diff
2. **Linter/compiler catches**: Issues that standard tooling would catch (type errors, formatting, import issues). Assume CI runs these.
3. **Intentional changes**: Behavior changes that are clearly intentional given the PR context
4. **Subjective preferences**: "I would have done it differently" without a concrete defect
5. **Trivial nitpicks**: Issues a senior engineer would not flag in a review
6. **Already silenced**: Issues with explicit suppression comments (lint ignore, type ignore, etc.)
7. **Test style**: Overly strict review of test utility formatting, mock boilerplate style, or fixture verbosity. However, test correctness, coverage completeness, assertion quality, test isolation, and flaky test patterns MUST still be thoroughly reviewed — these are real quality issues, not style

---

## Scope Modifiers

The user can pass arguments to customize the review:

- No arguments: Review `git diff` (auto-detect best diff range)
- `<branch>`: Review diff against specified branch
- `<PR#>`: Review a GitHub PR by number
- `<file-path>`: Review specific file(s)
- `--staged`: Review only staged changes
- `--focus <dims>`: Only review specified dimensions (comma-separated). Example: `--focus security,performance`
