---
name: which-model
description: 当用户需要调研某个 skill 的模型选择最佳实践时使用：分析目标技能的源代码与工作流 → 通过联网搜索（Tavily/SearXNG/DuckDuckGo）收集官方文档与社区经验 → 总结出哪些场景该用什么模型/参数 → 生成 WHICHMODEL 小节插入目标技能的 README.md。

metadata:
  author: Bensz Conan
  short-description: 自动调研并生成技能的模型选择最佳实践指南
  keywords:
    - which-model
    - 模型选择
    - 最佳实践
    - model selection
    - best practice
    - 参数配置
    - 推理强度
    - thinking mode
    - Claude
    - Opus
    - Sonnet
    - Haiku
    - WHICHMODEL
    - 模型调研
    - 文档生成
---

# Which Model - 模型选择最佳实践调研工具

## 目标

当用户需要调研某个 skill 的模型选择最佳实践时使用：分析目标技能的源代码与工作流 → 通过联网搜索（Tavily/SearXNG/DuckDuckGo）收集官方文档与社区经验 → 总结出哪些场景该用什么模型/参数 → 生成 WHICHMODEL 小节插入目标技能的 README.md。

## 流程

### 输入

#### 角色

你是一位专精 AI 模型应用与性能优化的技术研究员，擅长：
- **证据收集**：从官方文档、技术博客、社区讨论中提取可靠信息
- **模式识别**：识别不同任务类型与模型性能之间的关联模式
- **知识综合**：将分散的建议整合成结构化的最佳实践指南
- **清晰表达**：用简洁准确的语言传达技术建议

#### 触发条件

- 用户要求调研某个 skill 的模型选择最佳实践
- 用户要求生成 WHICHMODEL 文档
- 用户询问"某某 skill 应该用什么模型"

#### 你需要确认的输入

1. `{目标技能名称}`（必需）
2. `{目标厂商列表}`（可选，默认：Anthropic、OpenAI）
   - 支持的厂商：Anthropic、OpenAI、Google、Meta、Mistral、DeepSeek
   - 检索词会自动包含这些厂商的模型名（如 Claude、GPT-4、Gemini 等）
   - 可在 `config.yaml` 的 `research.target_vendors` 中配置默认值
3. `{目标 README.md 路径}`（可选，默认自动查找）

### 执行步骤

#### 工作流（5 步）

##### 0) 准备与守则
- **最高原则**：基于真实证据，拒绝猜测
- **记录时间戳**：所有输出包含生成时间，便于追踪时效性
- **验证目标技能**：确认技能目录存在且包含有效的 SKILL.md

**混合模式设计**：
- **AI 自主规划部分**：检索策略、场景识别、内容组织由 AI 根据指南自主判断
- **硬编码稳定性部分**：来源可信度评分、营销倾向检测使用硬编码公式

**必读参考资料**（首次执行前快速阅读）：
1. [references/SEARCH_STRATEGY.md](references/SEARCH_STRATEGY.md) - 检索策略指南（AI 自主规划）
2. [references/SCENARIO_ANALYSIS.md](references/SCENARIO_ANALYSIS.md) - 场景分析指南（AI 自主规划）
3. [references/CONTENT_ORGANIZATION.md](references/CONTENT_ORGANIZATION.md) - 内容组织指南（AI 自主规划）

**硬编码配置**（scripts 自动应用）：
- 来源可信度权重：定义在 `config.yaml` 的 `source_credibility.domain_weights`
- 营销倾向检测：定义在 `config.yaml` 的 `bias_detection.marketing_words`
- 综合评分公式：定义在 `config.yaml` 的 `scoring.formula`

##### 1) 静态分析：AI 理解目标技能（无硬编码规则）

**AI 直接阅读并理解 SKILL.md**，基于语义理解（而非关键词匹配）识别任务特征：

1. **理解技能的核心目标**
   - 阅读技能描述，理解其用途和价值主张
   - 理解工作流步骤的语义含义
   - 从触发条件、示例、输出规范中推断隐含需求

2. **识别任务特征**（AI 基于理解自由判断）
   ```
   分析示例（仅供 AI 参考，非硬规则）：

   输入：systematic-literature-review/SKILL.md

   AI 理解：
   - "AI 自定检索词 → 去重 → 逐篇阅读并评分 → 资深专家写作"
     → 这是一个多步骤的学术写作流程
     → 任务类型：文本生成、数据处理、多步骤推理、学术写作
   - "6 个工作流步骤 + 资深领域专家风格"
     → 复杂的工作流 + 高质量要求
     → 复杂度：high
   - "阅读大量文献并生成综述"
     → 需要处理大量输入并保持连贯性
     → 上下文需求：long
   - "质量优先：AI 不得偷懒或短视"
     → 明确的质量要求
     → 性能优先级：质量优先
   - "输出 LaTeX + PDF + Word"
     → 输出要求：latex, pdf, docx

   初步模型建议：
   - 长文本生成 + 高复杂度 + 质量优先
     → Claude Opus 4.5（主任务）
     → 理由：需要最强推理能力和连贯性
   - 数据处理（评分、选文）
     → Claude Sonnet 4.5（子任务）
     → 理由：结构化任务，性价比高
   ```

3. **生成分析结果**
   - AI 直接生成 `skill_analysis.json`
   - 包含 `task_features`、`model_recommendations`、`_reasoning`（分析过程）

**关键原则**：
- ✅ 基于语义理解，无硬编码规则
- ✅ AI 自由判断任务类型和复杂度
- ✅ 记录分析过程，便于追溯
- ❌ 不使用关键词匹配
- ❌ 不使用固定阈值判断

##### 2) 模型调研：证据收集 + 硬编码评分

**AI 自主规划检索策略**（参考 [references/SEARCH_STRATEGY.md](references/SEARCH_STRATEGY.md)）：
- 基于任务特征生成检索词
- 必须包含：任务特定查询、社区反馈查询、缺点查询、对比查询
- 避免营销陷阱（如"best practices"）
- 即使单厂商，也要包含跨厂商对比查询（避免回音室）

**执行联网搜索**（按优先级尝试）：
1. **Tavily**（深度搜索，获取最新信息）
2. **SearXNG**（多源聚合，覆盖面广）
3. **DuckDuckGo**（备选方案）
4. **降级**：如 MCP 工具不可用，使用内置搜索

**硬编码评分**（scripts/score_sources.py 自动执行）：
```
综合评分 = 相关性 × 30% + 可信度 × 50% + 中立性 × 20%

其中：
- 相关性：基于查询匹配（research_models.py 计算）
- 可信度：基于域名类型（config.yaml 硬编码权重）
  - 学术论文：1.0
  - 社区讨论：0.85
  - 官方文档：0.3
  - 厂商博客：0.25
- 中立性：检测营销倾向（config.yaml 硬编码关键词）
  - 过度正面且无平衡词汇：扣 0.4 分
  - 绝对化词语过多：扣 0.3 分
```

**输出**：`research_results_scored.json`（包含 impartial_score 和 score_details）

##### 3) 知识提取：场景分析（AI 自主规划）

**AI 自主分析场景**（参考 [references/SCENARIO_ANALYSIS.md](references/SCENARIO_ANALYSIS.md)）：
- 从评分后的搜索结果中提取真实使用场景
- 聚类相似场景，确保场景独立性
- 为每个场景提取：触发条件、推荐模型、推荐参数、适用/避免场景、来源依据
- 识别并处理冲突观点（并列展示，不偏向任何一方）

**关键原则**：
- 基于真实场景，不凭空想象
- 场景之间有明显区别
- 每个场景都有来源依据
- 冲突观点透明展示

**输出**：`scenarios.json`（结构化的场景列表）

##### 4) 文档生成：WHICHMODEL 小节（AI 自主规划）

**AI 自主组织内容**（参考 [references/CONTENT_ORGANIZATION.md](references/CONTENT_ORGANIZATION.md)）：
- 确定结构：完整结构 vs 简化结构（基于证据充足度）
- 生成披露信息：时间戳、覆盖范围、来源构成、局限性
- 组织场景建议：按什么顺序排列、用什么格式（表格/列表/混合）
- 添加对比总结：表格形式对比不同模型
- 提炼通用原则：3-5 条核心原则
- 处理争议点：展示冲突观点和平衡建议

**披露信息模板**：
```markdown
### 披露信息
- **最后更新**：{YYYY-MM-DD}
- **覆盖厂商**：{列表}（{覆盖数}/{总数} = {百分比}%）
- **来源构成**：{社区 X%, 学术 Y%, 官方 Z%}
- **数据时效**：{时间范围}
- **局限性**：{本次调研的局限性}
```

**输出**：`WHICHMODEL_section.md`

##### 5) 插入与验证
- **定位插入位置**：
  - 在目标 `README.md` 中查找合适位置（通常在"设计理念"或"档位选择指南"之后）
  - 如已存在 WHICHMODEL 小节，提示用户选择：覆盖 / 追加 / 取消
- **生成插入建议**：
  - 输出插入位置的行号
  - 显示插入前后的对比预览
- **等待用户确认**：
  - 询问用户是否插入
  - 用户确认后，执行插入
- **验证**：
  - 检查 Markdown 格式是否正确
  - 检查链接是否有效
  - 确认文档整体结构完整

### 输出

#### 输出规范

##### 必需输出
- `WHICHMODEL_section.md`：生成的 WHICHMODEL 小节
- `skill_analysis.json`：技能分析结果
- `research_results.json`：调研原始数据
- `extracted_knowledge.json`：提取的结构化知识

##### 可选输出
- `{目标技能}/README.md`：更新后的 README（需用户确认）
- `which_model_report.md`：完整调研报告（包含所有中间结果）

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 验证标准

- [ ] 所有模型建议都有明确来源标注
- [ ] 至少覆盖 3 个典型使用场景
- [ ] 通用原则部分包含 3-5 条核心建议
- [ ] 更新记录包含生成时间戳
- [ ] Markdown 格式正确，链接有效

### 失败与恢复

#### 错误处理

##### 常见错误与处理方式
| 错误类型 | 处理方式 |
|---------|---------|
| 目标技能不存在 | 立即返回，提示用户检查技能名称 |
| MCP 工具不可用 | 降级到内置搜索，记录降级原因 |
| 无相关搜索结果 | 提示用户调整检索词或手动补充经验 |
| README.md 找不到 | 输出 WHICHMODEL_section.md，由用户手动插入 |
| 插入位置冲突 | 提供多个可选位置，由用户选择 |


## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->

### Skill 专属约束

#### 最高原则与约束

##### 证据要求
- **拒绝猜测**：每条建议必须有明确来源
- **来源标注**：必须标注来源（官方文档/博客/社区）
- **时效性**：明确标注生成时间，模型建议可能随时间变化

##### 内容质量
- **简洁性**：每个场景的建议不超过 5 行
- **准确性**：不夸大模型能力，不承诺不确定的性能
- **可操作性**：参数建议具体，避免模糊表述

##### 用户交互
- **非破坏性**：不自动覆盖用户文档，需确认后插入
- **透明性**：展示调研过程和原始数据
- **可追溯**：保留更新记录，方便回溯
