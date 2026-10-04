---
name: find-best-skill
description: 当用户明确要求搜索、寻找、查找或推荐某个领域的 Agent Skill 时使用。对候选 Skill 进行多来源检索与比较后给出推荐。⚠️ 不适用：只想查看已有技能列表，或没有明确搜索/推荐意图。
metadata:
  author: Bensz Conan
  keywords:
    - find-best-skill
---

# Find Best Skill

## 目标

当用户明确要求"搜索技能"、"寻找 Agent Skill"、"查找某个领域的 skill"、"推荐最佳 skill"时使用。支持多平台搜索（GitHub、SkillsMP、Reddit）和社区/AI 双维度评价，推荐数量可根据用户指令动态调整（默认 5-10 个，支持 3-20 个）。⚠️ 不适用：用户只是询问"有没有某个技能"（应直接回答）、只是想了解技能列表（应直接列举）、没有明确"搜索/寻找/查找/推荐"意图。

## 流程

### 输入

#### 使用场景

当用户需要：
- 寻找特定功能的 Agent Skill
- 了解社区中某个领域的最佳实践方案
- 对比不同技能的优劣
- 发现已有技能的替代方案

#### 依赖关系

**可选依赖**：
- **get-review-theme** skill：用于需求解构（第 1 步）
  - 如果用户未安装该 skill，可直接分析用户需求提取主题和关键词

### 执行步骤

#### 核心工作流

##### 1. 需求解构

分析用户需求，提取核心主题和关键词：

**优先使用** **get-review-theme** skill（如已安装）：
```bash
/skill get-review-theme "用户原始需求描述"
```

**如未安装**：直接分析用户需求，从用户输入中提取核心主题、关键词、具体问题。

##### 2. 缓存查询

**优先检查本地缓存**，快速匹配历史技能：

```bash
# 使用缓存管理器搜索匹配技能
python scripts/cache_manager.py --search "关键词1" "关键词2" --limit 10
```

说明：
- 默认缓存参数来自 `config.yaml:cache`（单一真相来源）
- CLI 参数（如 `--cache-dir`）会覆盖 `config.yaml`

**命中策略**：

| 情况 | 处理方式 |
|------|----------|
| **有命中** | 展示本地结果 → 询问用户"是否联网扩展？" → 用户选择 |
| **无命中** | 直接进入联网搜索（第 3 步） |

**用户交互话术**：
```markdown
基于本地缓存，我找到 {N} 个相关技能：

{展示本地结果}

💡 发现 {N} 个候选，是否联网扩展搜索以获取更多最新结果？
- 回复"是"或"联网"进行在线搜索
- 回复"否"或"直接使用"直接输出以上结果
```

##### 3. 社区调研

基于解构结果，使用 **WebSearch 类工具**或**搜索类 MCP 工具**（如 SearXNG、Tavily）进行多平台搜索。

**搜索平台**：

| 平台 | 搜索语法示例 | 搜索重点 |
|------|-------------|----------|
| **GitHub** | `site:github.com "SKILL.md" {关键词}` | 开源项目、Stars、Forks |
| **SkillsMP** | `site:skillsmp.com {关键词} skill` | 技能市场、人气排序 |
| **awesome-claude-skills** | 直接访问 `github.com/VoltAgent/awesome-claude-skills` | 社区精选 |
| **Reddit** | `site:reddit.com/r/ClaudeCode {关键词}` | 用户讨论、真实反馈 |

**搜索关键词组合**（见 `config.yaml:search_keywords`）：
- `{topic} claude skill`（如 `TDD claude skill`）
- `{topic} agent skill`
- `{topic} claude code`

**搜索示例**：

```
# GitHub 搜索 TDD 相关技能
site:github.com "SKILL.md" TDD claude

# 搜索测试驱动开发技能
"test driven development" agent skill github

# Reddit 社区讨论
site:reddit.com/r/ClaudeCode TDD skill
```

**辅助脚本**（可选）：
```bash
# 生成研究检查清单模板
python scripts/get_skill_info.py "repo1,repo2,repo3"
```

##### 4. 结果合并与缓存更新

**如果联网搜索**：将本地缓存结果与联网搜索结果合并：

| 操作 | 说明 |
|------|------|
| **去重** | 基于 skill_name 或 GitHub URL 去重 |
| **数据源标记** | 本地/联网分别标记（`source: local/online`） |
| **排序优化** | 联网结果优先（最新数据），本地结果补充 |

**缓存更新**：将联网搜索到的新技能写入缓存

```python
from scripts.cache_manager import CacheManager

manager = CacheManager()
manager.add_skill(
    skill_name="skill-name",
    meta={
        "url": "https://github.com/xxx/skill",
        "description": "技能描述",
        "stars": 1234,
        "last_updated": "2026-01-18",
        "source": "online"
    },
    keywords=["tdd", "testing"],
    tags=["official", "workflow"]
)
```

##### 5. 社区舆情分析

对每个候选 skill，收集以下信息：

**社区评价维度**：
- GitHub Stars 数量
- 最近更新时间
- Issue 响应速度
- Fork/Watch 比例
- 社区讨论热度

**质量信号**：
- 是否有官方支持（Anthropic、OpenAI）
- 是否被知名团队使用（Sentry、Vercel）
- 文档完整性
- 代码质量

##### 6. AI 评价

从 AI 视角评估每个 skill：

**技术维度**：
- 工作流设计的合理性
- YAML frontmatter 质量
- Progressive Disclosure 实现程度
- 与现有生态的兼容性

**实用性维度**：
- 使用场景覆盖度
- 配置灵活性
- 扩展性
- 维护活跃度

##### 7. 生成推荐报告

按最合适至最不合适排序，推荐 skills。

**推荐数量规则**（详细参数见 `config.yaml:recommendation`）：

1. **优先级1：用户明确指定**
   - 解析用户指令中的数量关键词（如"推荐 3 个"、"给我 15 个候选"）
   - 示例：`"找 5 个最好的 TDD skill"` → 推荐数量 = 5

2. **优先级2：使用默认范围**
   - 默认目标数量：见 `config.yaml:recommendation.target_count`
   - 可调整范围：见 `config.yaml:recommendation.default_min/default_max`

3. **边界约束**：
   - 最少：见 `config.yaml:recommendation.absolute_min`
   - 最多：见 `config.yaml:recommendation.absolute_max`

每个 skill 包含：

```markdown
## N. {Skill Name}

**GitHub**: [项目地址](https://github.com/xxx/xxx)

### 推荐理由

**社区评价**：
- ⭐ {Stars} | 🍴 {Forks} | 📅 {最后更新}
- {社区使用情况、知名团队引用等}

**AI 评价**：
- {技术优势}
- {工作流设计亮点}
- {与需求匹配度}

### 局限性

- {潜在短板}
- {适用场景限制}
- {依赖或平台要求}
```

#### 辅助脚本

##### 缓存管理

```bash
# 查看缓存统计
python scripts/cache_manager.py --stats

# 搜索缓存中的技能
python scripts/cache_manager.py --search "关键词1" "关键词2" --limit 10

# 清理特定技能缓存
python scripts/cache_manager.py --clear "skill-name"

# 清理所有缓存
python scripts/cache_manager.py --clear
```

##### 批量获取技能信息

```bash
# 生成研究检查清单模板
python scripts/get_skill_info.py "repo1,repo2,repo3"
```

#### 参考资源

- [Agent Skills 调研报告](references/agent-skills-research.md)
- [SkillsMP 搜索指南](references/skillsmp-guide.md)

#### 示例

**用户输入**：`找一个能做 TDD 的 skill`

**输出示例**：

```markdown
基于您的需求 "测试驱动开发（TDD）"，我为您推荐以下 skills：

## 1. test-driven-development

**GitHub**: [obra/test-driven-development](https://github.com/VoltAgent/awesome-claude-skills)

### 推荐理由

**社区评价**：
- ⭐ 1.2k+ | 🍴 150+ | 📅 2周前更新
- 被多个团队采用，社区活跃讨论

**AI 评价**：
- 强制 Red-Green-Refactor 循环，确保 TDD 严格执行
- 支持多种测试框架
- 渐进式加载设计，性能优秀

### 局限性

- 对测试框架有预设（可能不支持您使用的框架）
- 初次使用需要适应其严格的流程要求

## 2. tdd-workflow

**GitHub**: [anthropics/tdd-workflow](https://github.com/anthropics/skills)

### 推荐理由

**社区评价**：
- ⭐ 官方维护 | 📅 持续更新
- Anthropic 官方最佳实践

**AI 评价**：
- 与 Claude Code 深度集成
- 简洁的工作流设计
- 灵活的测试适配

### 局限性

- 功能相对基础，高级特性较少
- 专注于 Claude Code 生态

[... 继续推荐 3-8 个 skills]
```

### 输出

#### 输出规范

##### 推荐数量

**动态确定规则**：

1. **优先级 1：用户明确指定**
   - 解析用户指令中的数量关键词（如"推荐 3 个"、"给我 15 个候选"）
   - 示例：`"找 5 个最好的 TDD skill"` → 推荐数量 = 5

2. **优先级 2：使用默认范围**
   - 用户未指定时，使用 5-10 个
   - 根据候选质量和相关性灵活调整

3. **边界约束**：
   - **最少**：3 个（确实找不到更多时）
   - **最多**：20 个（避免信息过载）

**排序**：按推荐度降序排列

##### 筛选标准

**必须满足**：
- 有 GitHub 仓库地址
- 有有效的 SKILL.md 文件
- 有明确的功能描述

**优先推荐**：
- 官方维护（Anthropic、OpenAI）
- 高 Stars（>100）
- 最近更新（6个月内）
- 有完整文档

**排除条件**：
- 没有 GitHub 链接
- 仓库已归档
- 超过 1 年未更新
- 文档严重缺失

##### 数量解析示例

| 用户指令 | 解析结果 | 说明 |
|---------|---------|------|
| `"推荐 3 个 TDD skill"` | 3 个 | 明确数字 |
| `"给我 15 个候选"` | 15 个 | 超出默认范围但有效 |
| `"找一些 debug 技能"` | 5-10 个 | 未指定，使用默认 |
| `"只要最好的一个"` | 1 个 | 少于最少边界，但用户意图明确 |
| `"列出所有相关的"` | 5-10 个 | 无明确数量，使用默认 |

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 质量检查清单

**触发验证**（执行前）：
- [ ] 用户明确要求"搜索/寻找/查找/推荐"技能
- [ ] 非简单询问"有没有某个技能"（应直接回答）

**输出验证**（执行后）：
- [ ] 每个推荐都有 GitHub 链接
- [ ] 推荐理由包含社区和 AI 双重视角
- [ ] 局限性分析真实客观
- [ ] 排序逻辑清晰可解释
- [ ] 总数符合"输出规范"的约束（见上文"推荐数量规则"）

### 失败与恢复

#### 搜索、缓存与候选失败

- `get-review-theme` 未安装时直接从用户需求提取主题和关键词，不把可选依赖故障当作任务失败。
- 本地缓存无命中时进入联网搜索；联网来源不可用或部分失败时，明确标记失败来源并使用仍可验证的缓存/搜索结果，不虚构 Stars、更新时间、链接或社区评价。
- 候选缺少 GitHub 链接、有效 `SKILL.md`、明确功能描述，或命中排除条件时剔除并在数量不足时说明原因，不用低质量结果填充数量。
- 缓存写入、辅助脚本或单个平台失败时保留已收集的结果和错误信息；只有满足来源可追溯、排序和数量约束的候选才进入最终推荐报告。


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
