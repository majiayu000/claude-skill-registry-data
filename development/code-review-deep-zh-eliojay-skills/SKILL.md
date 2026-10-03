---
name: code-review-deep-zh
description: "全面的深度代码审查，覆盖 10 个维度：正确性、安全性、性能、可靠性、架构、数据完整性、可维护性、一致性、可观测性和文档。使用 7 个并行审查代理进行彻底分析并生成结构化报告。自动从差异(diff)中检测所有编程语言和框架。当用户请求深度代码审查、全面审查、完整审查、彻底审查、安全审计、架构评估、代码质量分析、性能审查，或提及 /code-review-deep-zh 时使用。同样适用于合并前的最终审查、重构后审查、新项目代码审计，或任何多维度代码审查请求。支持聚焦模式(--focus security,performance)和大差异(diff)分片。不要用于：读懂代码结构或某次变更但不做质量评判（用 code-read-deep-*）、定位单个具体故障根因（用 systematic-debugging）、设计或编写测试（用 code-testing）、删冗余代码（用 code-slimming）、判断该不该用设计模式（用 design-pattern-advisor）。"
---

# 深度代码审查 (code-review-deep-zh)

一个全面的、多维度的代码审查 skill，使用 7 个并行代理在 10 个审查维度上分析代码变更。支持所有编程语言，具备自动检测和动态适配能力。

## 审查维度

| # | 维度 | 代理 |
|---|-----------|-------|
| 1 | 正确性 | Agent 1 |
| 2 | 安全性 | Agent 2 |
| 3 | 性能 | Agent 3 |
| 4 | 可靠性 | Agent 3 |
| 5 | 架构与设计 | Agent 4 |
| 6 | 数据完整性 | Agent 5 |
| 7 | 可维护性 | Agent 6 |
| 8 | 文档 | Agent 6 |
| 9 | 一致性 | Agent 7 |
| 10 | 可观测性 | Agent 7 |

## 工作流程

按顺序执行以下 4 个阶段。不要跳过任何阶段。

---

### 阶段 1：上下文收集

**你（主代理）直接执行此阶段。** 在派发审查代理之前收集所有所需的上下文。

#### 步骤 1.1：确定审查范围

从用户输入中检测审查范围：

- **PR 差异(diff)**（默认）：运行 `git diff main...HEAD`，如果用户指定了基准分支则运行 `git diff <base>...HEAD`
- **暂存变更**：如果用户提及 "staged" 或 "cached"，运行 `git diff --cached`
- **工作树**：如果用户提及 "uncommitted" 或不存在上游分支，运行 `git diff HEAD`
- **特定文件/目录**：如果用户指定了文件路径，将审查范围限定到这些文件
- **PR 编号**：如果用户提供了 GitHub PR 编号，使用 `gh pr diff <number>`

如果差异(diff)为空，告知用户并停止。

#### 步骤 1.2：收集上下文

并行运行以下命令：

1. `git diff <scope>` — 获取完整的统一差异(diff)
2. `git log --oneline -20` — 最近的提交历史
3. 读取 CLAUDE.md 文件：根目录的 CLAUDE.md + 差异(diff)所触及目录中的任何 CLAUDE.md
4. 检查仓库中的框架配置文件（package.json、pom.xml、go.mod、Cargo.toml、requirements.txt、build.gradle 等）
5. `git diff <scope> --stat` — 获取文件变更统计（每个文件的增加/删除行数）

#### 步骤 1.3：自动检测语言与框架

从差异(diff)和配置文件中，识别：
- **语言**：从差异(diff)中的文件扩展名检测（例如 `.java`、`.go`、`.py`、`.rs`、`.js`、`.ts`、`.kt`、`.swift`、`.rb`、`.php`、`.cs`、`.cpp`、`.c`、`.scala`、`.dart` 等）
- **框架**：从导入语句/配置文件检测（例如 Spring、Django、Flask、React、Vue、Angular、Gin、Echo、Actix、Express、Next.js 等）
- **构建工具**：从配置文件检测（Maven、Gradle、npm、pip、cargo 等）

准备一个 `language_context` 摘要字符串，例如：
```
Languages: Java, TypeScript
Frameworks: Spring Boot, React
Build tools: Maven, npm
```

#### 步骤 1.4：文件风险分类

根据每个变更文件的路径和角色，将其归入一个风险层级：

| 风险层级 | 权重 | 示例 |
|-----------|--------|---------|
| **Critical（关键）** | 3x | 支付/计费、认证/安全、数据迁移、核心业务逻辑、加密、API 网关 |
| **High（高）** | 2x | 数据库模型/仓储、API 控制器/处理器、中间件、配置、基础设施 |
| **Normal（普通）** | 1x | 业务逻辑、服务、工具类、UI 组件 |
| **Low（低）** | 0.5x | 文档、静态资源、生成代码、CI 配置、README |

分类规则：
- 文件路径包含 `auth`、`security`、`payment`、`billing`、`crypto`、`migration`、`gateway` → **Critical（关键）**
- 文件路径包含 `model`、`entity`、`repository`、`dao`、`controller`、`handler`、`middleware`、`config`、`infra` → **High（高）**
- 文件路径包含 `test`、`spec`、`mock`、`fixture` → **Normal（普通）**（测试质量很重要；不要将测试文件视为低风险）
- 文件路径包含 `doc`、`README`、`.md`、`assets`、`.generated`、`.ci`、`.github` → **Low（低）**
- 其他所有情况 → **Normal（普通）**
- 如果不确定，归类为 **Normal（普通）**

准备一个 `risk_profile` 摘要：
```
Critical files: 2 (src/auth/jwt.go, src/payment/charge.go)
High files: 3 (src/models/user.go, src/api/handler.go, config/app.yaml)
Normal files: 5
Low files: 2
Overall risk tier: HIGH
```

#### 步骤 1.5：大差异(diff)处理

统计差异(diff)的总行数。采用以下策略之一：

- **小差异(diff)（≤ 500 行）**：将完整差异(diff)传给所有代理。无需特殊处理。
- **中等差异(diff)（501–2000 行）**：传递完整差异(diff)，但指示代理优先处理 Critical（关键）和 High（高）风险文件。包含 `risk_profile`，以便代理知道应该聚焦在哪里。
- **大差异(diff)（2001–5000 行）**：按文件拆分差异(diff)。将文件分组为 2-3 个分片，在分片 1 中优先放入 Critical/High 文件。每个代理接收所有分片，但被指示深入聚焦分片 1，并以更高层级扫描分片 2-3。
- **超大差异(diff)（> 5000 行）**：告知用户差异(diff)非常大，并建议分成更小的批次审查。如果用户仍希望进行完整审查，按文件风险层级拆分：
  - **第 1 轮**：仅审查 Critical + High 文件（完整深度）
  - **第 2 轮**：审查 Normal 文件（标准深度）
  - **跳过**：Low 风险文件（在报告中提及它们被跳过）

对于大/超大差异(diff)，在代理提示中包含此说明：
```
NOTE: This is a large diff. Focus your deepest analysis on the files marked as
Critical and High risk. For Normal/Low risk files, only flag P0 and P1 issues.
```

#### 步骤 1.6：聚焦模式检测

检查用户是否使用 `--focus` 指定了维度名称：
- `--focus security` → 仅派发 Agent 2（安全性）
- `--focus security,performance` → 仅派发 Agent 2 + Agent 3
- `--focus correctness,data` → 仅派发 Agent 1 + Agent 5

`--focus` 的维度名称映射：
| Input keyword | 派发的代理 |
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

如果未指定 `--focus`，派发全部 7 个代理（默认完整审查）。

#### 步骤 1.7：准备代理输入

准备以下数据传给代理：
- `diff`：完整的统一差异(diff)（对于大差异(diff)则为分片后的差异(diff)）
- `language_context`：检测到的语言/框架字符串
- `claude_md_rules`：相关 CLAUDE.md 文件的内容（或 "No CLAUDE.md found"）
- `file_list`：变更文件及其路径的列表
- `risk_profile`：来自步骤 1.4 的文件风险分类
- `diff_size`：差异(diff)总行数及所采用的处理策略

---

### 阶段 2：并行深度分析

使用 Agent 工具同时启动代理。在**单条消息**中发送全部代理，使它们并行运行。

- **完整审查**（无 `--focus`）：启动全部 **7 个代理**
- **聚焦模式**：仅启动匹配所聚焦维度的代理

对于每个代理，从 `references/agent-<name>.md` 读取其参考文件，并通过包含以下内容来构建提示：

1. 代理的角色和检查清单（来自参考文件）
2. `diff` 内容
3. `language_context`
4. `claude_md_rules`
5. `file_list`
6. `risk_profile`

**重要**：每个代理必须以 **JSON 数组**形式返回其发现项。指示每个代理在其响应末尾仅输出一个 JSON 数组，格式完全如下：

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

**字段说明：**
- `fix_suggestion`：用自然语言描述如何修复该问题
- `fix_code`：在可能的情况下，提供一段展示修正版本的具体代码片段。使用原始代码的语言和风格。如果修复过于依赖上下文而无法用代码表达，则设为 `""`（空字符串）。对于 P0 和 P1 问题，始终尝试提供 `fix_code`。

**代理 ID 前缀：**
- Agent 1（正确性）：`CORR-NNN`
- Agent 2（安全性）：`SEC-NNN`
- Agent 3（性能与可靠性）：`PERF-NNN` / `REL-NNN`
- Agent 4（架构与设计）：`ARCH-NNN`
- Agent 5（数据完整性）：`DATA-NNN`
- Agent 6（可维护性与文档）：`MAINT-NNN` / `DOC-NNN`
- Agent 7（一致性与可观测性）：`CONS-NNN` / `OBS-NNN`

**代理派发模板：**

```
你是一个专注于 [DIMENSION] 的专业代码审查代理。

## 你的角色
[读取并包含来自 references/agent-<name>.md 的内容]

## 上下文
- 语言与框架：{language_context}
- CLAUDE.md 规则：{claude_md_rules}

## 文件风险分类
{risk_profile}

## 变更文件
{file_list}

## 待审查的差异(diff)
{diff}

## 指令
1. 仔细阅读整个差异(diff)
2. 对于每个变更文件，同时 Read 完整文件以理解变更周围的上下文
3. 优先分析 Critical（关键）和 High（高）风险文件——它们值得最深入的审视
4. 应用你角色定义中的检查清单，适配检测到的语言
5. 对于每个发现项，根据你对它是真实问题的确定程度评估置信度(0-100)
6. 对于 P0 和 P1 发现项，你必须提供包含具体代码修复的 fix_code 字段
7. 对于 P2-P4 发现项，在修复直观明了时提供 fix_code
8. 仅返回你认为是真实问题且置信度 >= 50 的发现项
9. 在响应末尾以 JSON 数组形式输出你的发现项

## 输出格式
返回一个发现项的 JSON 数组。如果未发现问题，返回 []。
每个发现项必须包含：id, dimension, severity (P0-P4), file, line, summary, description, impact, fix_suggestion, fix_code, confidence, language
```

### 代理失败处理

在所有代理完成（或超时）后，应用以下规则：

1. **JSON 解析失败**：如果某个代理的响应不包含有效的 JSON 数组，按顺序使用以下回退方式尝试从响应中提取 JSON：
   - 查找响应中 `[` 与最后一个 `]` 之间的内容
   - 查找 ```json 代码围栏内部的内容
   - 如果两者均失败，将该代理的输出视为 `[]`（无发现项）并在报告中记录此失败
2. **代理超时或出错**：如果某个代理在分配的时间内未能返回，或返回了错误，将其维度视为 `[]` 并在报告中记录："Agent X (Dimension) did not complete — results may be incomplete for this dimension"
3. **部分结果**：使用代理实际返回的任何结果继续进行。即使覆盖不完整，审查仍然有价值。报告应清楚地指明哪些维度已被完整分析。
4. **所有代理失败**：如果全部 7 个代理都失败，告知用户并建议重试或使用更简单的审查范围。

---

### 阶段 3：交叉验证与去重

在所有代理完成（或超时）后，处理它们的结果：

#### 步骤 3.1：解析结果

使用上述失败处理规则从每个代理的响应中提取 JSON 数组。跟踪哪些代理返回了有效结果。

#### 步骤 3.2：合并与去重

将所有发现项合并到一个列表中，然后去重：
- **相同文件 + 相同行范围（5 行以内）+ 相同根因** → 保留置信度更高的那个，并记录相互印证
- 合并重复项时，每有一个相互印证的代理，就将存留发现项的置信度提升 +15

#### 步骤 3.3：置信度调整

对每个发现项的置信度评分应用以下调整：

**加分项：**
- **多代理相互印证**：每有一个额外代理标记了同一问题，+15
- **违反明确的 CLAUDE.md 规则**：如果该发现项直接违背了某条 CLAUDE.md 指令，+10
- **关键文件**：如果问题位于 Critical（关键）风险文件中，+10
- **高风险文件**：如果问题位于 High（高）风险文件中，+5

**减分项：**
- **既有问题**：如果问题位于差异(diff)未修改的行上，-30
- **无 CLAUDE.md 依据的纯风格问题**：如果纯粹是风格问题且无 CLAUDE.md 支撑，-20
- **可被 Linter/编译器捕获**：如果标准 linter 或编译器能捕获此问题，-15
- **低风险文件**：如果问题位于 Low（低）风险文件中且严重级别为 P2 或以下，-10

置信度上限为 100，下限为 0。

#### 步骤 3.4：过滤

移除所有调整后置信度 < 60 的发现项。

#### 步骤 3.5：排序

按以下顺序对剩余发现项排序：
1. 严重级别（P0 优先）
2. 文件风险层级（Critical 优先）
3. 置信度（最高优先）
4. 维度（正确性 > 安全性 > 性能 > ... > 文档）

---

### 阶段 4：报告生成

#### 步骤 4.1：计算总体风险评分

使用以下公式为整个变更计算风险评分(0-100)：

```
risk_score = 0

For each surviving finding:
  weight = severity_weight × file_risk_weight × (confidence / 100)
  risk_score += weight

Severity weights: P0=25, P1=15, P2=8, P3=3, P4=1
File risk weights: Critical=3, High=2, Normal=1, Low=0.5

Cap risk_score at 100.
```

将风险评分映射到风险等级：

| Score | 风险等级 | 标签 |
|-------|-----------|-------|
| 0 | None | 🟢 无风险 |
| 1-20 | Low | 🟢 低风险 |
| 21-40 | Medium | 🟡 中风险 |
| 41-60 | High | 🟠 高风险 |
| 61-80 | Very High | 🔴 很高风险 |
| 81-100 | Critical | 🔴 严重风险 |

#### 步骤 4.2：生成报告

以**中文**生成最终报告（依据用户的 CLAUDE.md 规则 #1）。使用以下模板：

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

列出 2-3 处代码做得好的地方。如果代码整体质量良好，明确说明这一点。
本节有助于平衡审查并肯定优秀的工作。

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

**当代理失败时**，在 审查信息 之后添加此小节：
```markdown
## ⚠️ 审查完整性说明
以下维度的审查代理未能正常返回结果，相关维度的审查可能不完整：
- {dimension}: {failure reason}
建议针对这些维度进行手动审查或重新运行。
```

如果过滤后没有发现项存留，输出一份简短报告：
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

## 误报指引

以下情况**不是**问题——不要将它们纳入发现项：

1. **既有问题**：位于差异(diff)未修改行上的问题
2. **Linter/编译器可捕获**：标准工具会捕获的问题（类型错误、格式问题、导入问题）。假设 CI 会运行这些工具。
3. **有意的变更**：在 PR 上下文中明显属于有意为之的行为变更
4. **主观偏好**："我会用不同方式来做"，但没有具体缺陷
5. **琐碎的吹毛求疵**：资深工程师在审查中不会标记的问题
6. **已被显式抑制**：带有显式抑制注释（lint ignore、type ignore 等）的问题
7. **测试风格**：对测试工具格式、mock 样板风格或 fixture 冗长度的过于严苛的审查。但是，测试正确性、覆盖完整性、断言质量、测试隔离性以及不稳定(flaky)测试模式仍然必须被彻底审查——这些是真实的质量问题，而非风格问题

---

## 范围修饰符

用户可以传递参数来自定义审查：

- 无参数：审查 `git diff`（自动检测最佳差异(diff)范围）
- `<branch>`：审查相对于指定分支的差异(diff)
- `<PR#>`：按编号审查一个 GitHub PR
- `<file-path>`：审查特定文件
- `--staged`：仅审查暂存的变更
- `--focus <dims>`：仅审查指定的维度（以逗号分隔）。示例：`--focus security,performance`
