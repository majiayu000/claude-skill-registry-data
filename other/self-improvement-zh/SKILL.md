---
name: self-improvement-zh
description: "捕获学习内容、错误和纠正以实现持续改进。使用场景：(1) 命令或操作意外失败时，(2) 用户纠正 AI 时（'不对，这样错了...', '实际上应该...'），(3) 用户请求不存在的功能时，(4) 外部 API 或工具失败时，(5) AI 意识到其知识过时或不正确时，(6) 发现重复任务的更好方法时。同时建议在执行重要任务前审查学习内容。"
metadata:
---

# 自我改进技能

将学习内容和错误记录到 Markdown 文件中以实现持续改进。编码代理稍后可以将这些处理成修复，重要的学习内容会被提升到项目记忆中。

## 快速参考

| 情况 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正你 | 记录到 `.learnings/LEARNINGS.md`，类别为 `correction` |
| 用户想要缺失的功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，包含集成详情 |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，类别为 `knowledge_gap` |
| 发现更好的方法 | 记录到 `.learnings/LEARNINGS.md`，类别为 `best_practice` |
| 简化/强化重复模式 | 记录/更新 `.learnings/LEARNINGS.md`，包含 `Source: simplify-and-harden` 和稳定的 `Pattern-Key` |
| 与现有条目相似 | 用 `**See Also**` 链接，考虑提升优先级 |
| 广泛适用的学习 | 提升到 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md` |
| 工作流改进 | 提升到 `AGENTS.md`（OpenClaw 工作区） |
| 工具陷阱 | 提升到 `TOOLS.md`（OpenClaw 工作区） |
| 行为模式 | 提升到 `SOUL.md`（OpenClaw 工作区） |

## OpenClaw 设置（推荐）

OpenClaw 是此技能的主要平台。它使用基于工作区的提示注入和自动技能加载。

### 安装

**通过 ClawdHub（推荐）：**
```bash
clawdhub install self-improvement-zh
```

**手动：**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improvement-zh
```

基于 OpenClaw 重新制作，原始仓库：https://github.com/pskoett/pskoett-ai-skills - https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### 工作区结构

OpenClaw 在每个会话中注入这些文件：

```
~/.openclaw/workspace/
├── AGENTS.md          # 多代理工作流，委托模式
├── SOUL.md            # 行为指南，个性，原则
├── TOOLS.md           # 工具能力，集成陷阱
├── MEMORY.md          # 长期记忆（仅主会话）
├── memory/            # 每日记忆文件
│   └── YYYY-MM-DD.md
└── .learnings/        # 此技能的日志文件
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 创建学习文件

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

然后创建日志文件（或从 `assets/` 复制）：
- `LEARNINGS.md` — 纠正、知识缺口、最佳实践
- `ERRORS.md` — 命令失败、异常
- `FEATURE_REQUESTS.md` — 用户请求的功能

### 提升目标

当学习内容被证明具有广泛适用性时，将其提升到工作区文件：

| 学习类型 | 提升到 | 示例 |
|---------|--------|------|
| 行为模式 | `SOUL.md` | "简洁明了，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "为长时间任务生成子代理" |
| 工具陷阱 | `TOOLS.md` | "Git push 需要先配置认证" |

### 会话间通信

OpenClaw 提供工具在会话间共享学习内容：

- **sessions_list** — 查看活动/最近的会话
- **sessions_history** — 读取另一个会话的记录
- **sessions_send** — 向另一个会话发送学习内容
- **sessions_spawn** — 生成子代理进行后台工作

### 可选：启用钩子

在会话开始时自动提醒：

```bash
# 复制钩子到 OpenClaw 钩子目录
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement-zh

# 启用它
openclaw hooks enable self-improvement-zh
```

详见 `references/openclaw-integration.md`。

---

## 通用设置（其他代理）

对于 Claude Code、Codex、Copilot 或其他代理，在项目中创建 `.learnings/`：

```bash
mkdir -p .learnings
```

从 `assets/` 复制模板或创建带标题的文件。

### 在代理文件 AGENTS.md、CLAUDE.md 或 .github/copilot-instructions.md 中添加引用，提醒自己记录学习内容。（这是基于钩子提醒的替代方案）

#### 自我改进工作流

当错误或纠正发生时：
1. 记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md`
2. 审查并将广泛适用的学习提升到：
   - `CLAUDE.md` - 项目事实和约定
   - `AGENTS.md` - 工作流和自动化
   - `.github/copilot-instructions.md` - Copilot 上下文

## 日志格式

### 学习条目

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 时间戳
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
学习内容的一行描述

### Details
完整上下文：发生了什么，哪里错了，什么是正确的

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (如果与现有条目相关)
- Pattern-Key: simplify.dead_code | harden.input_validation (可选，用于重复模式跟踪)
- Recurrence-Count: 1 (可选)
- First-Seen: 2025-01-15 (可选)
- Last-Seen: 2025-01-15 (可选)

---
```

### 错误条目

追加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 时间戳
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
失败内容的简要描述

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关的环境详情

### Suggested Fix
如果可识别，可能解决此问题的方法

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (如果重复)

---
```

### 功能请求条目

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 时间戳
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要做什么

### User Context
为什么需要它，正在解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何构建，可能扩展什么

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID 生成

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (学习), `ERR` (错误), `FEAT` (功能)
- YYYYMMDD: 当前日期
- XXX: 顺序号或随机 3 个字符（如 `001`, `A7B`）

示例：`LRN-20250115-001`, `ERR-20250115-A3F`, `FEAT-20250115-002`

## 解决条目

当问题被修复时，更新条目：

1. 更改 `**Status**: pending` → `**Status**: resolved`
2. 在 Metadata 后添加解决方案块：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 或 #42
- **Notes**: 所做工作的简要描述
```

其他状态值：
- `in_progress` - 正在积极处理
- `wont_fix` - 决定不处理（在 Resolution 注释中添加原因）
- `promoted` - 提升到 CLAUDE.md、AGENTS.md 或 .github/copilot-instructions.md

## 提升到项目记忆

当学习内容具有广泛适用性（不是一次性修复）时，将其提升到永久项目记忆。

### 何时提升

- 学习适用于多个文件/功能
- 任何贡献者（人类或 AI）都应知道的知识
- 防止重复错误
- 记录项目特定的约定

### 提升目标

| 目标 | 内容归属 |
|------|---------|
| `CLAUDE.md` | 所有 Claude 交互的项目事实、约定、陷阱 |
| `AGENTS.md` | 代理特定的工作流、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目上下文和约定 |
| `SOUL.md` | 行为指南、沟通风格、原则（OpenClaw 工作区） |
| `TOOLS.md` | 工具能力、使用模式、集成陷阱（OpenClaw 工作区） |

### 如何提升

1. **提炼**学习内容为简洁的规则或事实
2. **添加**到目标文件的适当部分（如需要则创建文件）
3. **更新**原始条目：
   - 更改 `**Status**: pending` → `**Status**: promoted`
   - 添加 `**Promoted**: CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

### 提升示例

**学习**（详细）：
> 项目使用 pnpm 工作区。尝试 `npm install` 但失败了。
> 锁定文件是 `pnpm-lock.yaml`。必须使用 `pnpm install`。

**在 CLAUDE.md 中**（简洁）：
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习**（详细）：
> 修改 API 端点时，必须重新生成 TypeScript 客户端。
> 忘记这一点会导致运行时类型不匹配。

**在 AGENTS.md 中**（可操作）：
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复模式检测

如果记录与现有条目相似的内容：

1. **先搜索**：`grep -r "keyword" .learnings/`
2. **链接条目**：在 Metadata 中添加 `**See Also**: ERR-20250110-001`
3. **提升优先级** 如果问题持续重复
4. **考虑系统性修复**：重复问题通常表明：
   - 缺少文档（→ 提升到 CLAUDE.md 或 .github/copilot-instructions.md）
   - 缺少自动化（→ 添加到 AGENTS.md）
   - 架构问题（→ 创建技术债务工单）

## Simplify & Harden 反馈

使用此工作流从 `simplify-and-harden` 技能中提取重复模式，并将其转化为持久的提示指导。

### 提取工作流

1. 从任务摘要中读取 `simplify_and_harden.learning_loop.candidates`。
2. 对于每个候选项，使用 `pattern_key` 作为稳定的去重键。
3. 在 `.learnings/LEARNINGS.md` 中搜索具有该键的现有条目：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 如果找到：
   - 增加 `Recurrence-Count`
   - 更新 `Last-Seen`
   - 添加 `See Also` 链接到相关条目/任务
5. 如果未找到：
   - 创建新的 `LRN-...` 条目
   - 设置 `Source: simplify-and-harden`
   - 设置 `Pattern-Key`、`Recurrence-Count: 1` 和 `First-Seen`/`Last-Seen`

### 提升规则（系统提示反馈）

当以下所有条件都为真时，将重复模式提升到代理上下文/系统提示文件：

- `Recurrence-Count >= 3`
- 至少在 2 个不同任务中出现
- 在 30 天的时间窗口内发生

提升目标：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md` 用于 OpenClaw 工作区级指导（如适用）

将提升的规则写为简短的预防规则（在编码之前/期间要做什么），而不是长篇事件报告。

## 定期审查

在自然断点处审查 `.learnings/`：

### 何时审查
- 在开始新的主要任务之前
- 在完成功能之后
- 在处理有过去学习内容的区域时
- 在活跃开发期间每周一次

### 快速状态检查
```bash
# 统计待处理项
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# 列出待处理的高优先级项
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# 查找特定区域的学习内容
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查操作
- 解决已修复的项目
- 提升适用的学习内容
- 链接相关条目
- 升级重复问题

## 检测触发器

注意以下情况时自动记录：

**纠正**（→ 类别为 `correction` 的学习）：
- "不对，不是这样..."
- "实际上，应该是..."
- "你错了..."
- "那个过时了..."

**功能请求**（→ 功能请求）：
- "你还能..."
- "我希望你能..."
- "有没有办法..."
- "为什么你不能..."

**知识缺口**（→ 类别为 `knowledge_gap` 的学习）：
- 用户提供你不知道的信息
- 你引用的文档过时了
- API 行为与你的理解不同

**错误**（→ 错误条目）：
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外的输出或行为
- 超时或连接失败

## 优先级指南

| 优先级 | 何时使用 |
|--------|---------|
| `critical` | 阻止核心功能，数据丢失风险，安全问题 |
| `high` | 影响重大，影响常见工作流，重复问题 |
| `medium` | 影响中等，存在解决方法 |
| `low` | 轻微不便，边缘情况，锦上添花 |

## 区域标签

用于按代码库区域过滤学习内容：

| 区域 | 范围 |
|------|------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | CI/CD、部署、Docker、云 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

## 最佳实践

1. **立即记录** - 问题发生后上下文最新鲜
2. **要具体** - 未来的代理需要快速理解
3. **包含复现步骤** - 特别是对于错误
4. **链接相关文件** - 使修复更容易
5. **建议具体修复** - 不仅仅是"调查"
6. **使用一致的类别** - 启用过滤
7. **积极提升** - 如有疑问，添加到 CLAUDE.md 或 .github/copilot-instructions.md
8. **定期审查** - 过时的学习内容失去价值

## Gitignore 选项

**保持学习内容本地**（每个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要添加到 .gitignore - 学习内容成为共享知识。

**混合**（跟踪模板，忽略条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 钩子集成

通过代理钩子启用自动提醒。这是**选择性加入** - 你必须明确配置钩子。

### 快速设置（Claude Code / Codex）

在项目中创建 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}
```

这会在每个提示后注入学习评估提醒（约 50-100 个令牌开销）。

### 完整设置（带错误检测）

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### 可用的钩子脚本

| 脚本 | 钩子类型 | 目的 |
|------|---------|------|
| `scripts/activator.sh` | UserPromptSubmit | 在任务后提醒评估学习内容 |
| `scripts/error-detector.sh` | PostToolUse (Bash) | 在命令错误时触发 |

详见 `references/hooks-setup.md` 进行详细配置和故障排除。

## 自动技能提取

当学习内容足够有价值成为可重用技能时，使用提供的助手提取它。

### 技能提取标准

当满足以下任一条件时，学习内容符合技能提取条件：

| 标准 | 描述 |
|------|------|
| **重复** | 有 `See Also` 链接到 2+ 个相似问题 |
| **已验证** | 状态为 `resolved` 且有有效修复 |
| **非显而易见** | 需要实际调试/调查才能发现 |
| **广泛适用** | 非项目特定；跨代码库有用 |
| **用户标记** | 用户说"把这个保存为技能"或类似 |

### 提取工作流

1. **识别候选项**：学习内容符合提取标准
2. **运行助手**（或手动创建）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义 SKILL.md**：用学习内容填充模板
4. **更新学习**：将状态设置为 `promoted_to_skill`，添加 `Skill-Path`
5. **验证**：在新鲜会话中读取技能以确保其自包含

### 手动提取

如果你更喜欢手动创建：

1. 创建 `skills/<skill-name>/SKILL.md`
2. 使用 `assets/SKILL-TEMPLATE.md` 中的模板
3. 遵循 [Agent Skills 规范](https://agentskills.io/specification)：
   - 带有 `name` 和 `description` 的 YAML 前置数据
   - 名称必须与文件夹名称匹配
   - 技能文件夹内没有 README.md

### 提取检测触发器

注意这些信号表明学习应该成为技能：

**在对话中：**
- "把这个保存为技能"
- "我一直遇到这个"
- "这对其他项目有用"
- "记住这个模式"

**在学习条目中：**
- 多个 `See Also` 链接（重复问题）
- 高优先级 + 已解决状态
- 类别：`best_practice` 具有广泛适用性
- 用户反馈赞扬解决方案

### 技能质量门

在提取之前，验证：

- [ ] 解决方案经过测试且有效
- [ ] 描述在没有原始上下文的情况下清晰
- [ ] 代码示例是自包含的
- [ ] 没有项目特定的硬编码值
- [ ] 遵循技能命名约定（小写，连字符）

## 多代理支持

此技能适用于不同的 AI 编码代理，具有代理特定的激活。

### Claude Code

**激活**：钩子（UserPromptSubmit、PostToolUse）
**设置**：带钩子配置的 `.claude/settings.json`
**检测**：通过钩子脚本自动

### Codex CLI

**激活**：钩子（与 Claude Code 相同的模式）
**设置**：带钩子配置的 `.codex/settings.json`
**检测**：通过钩子脚本自动

### GitHub Copilot

**激活**：手动（无钩子支持）
**设置**：添加到 `.github/copilot-instructions.md`：

```markdown
## Self-Improvement

After solving non-obvious issues, consider logging to `.learnings/`:
1. Use format from self-improvement skill
2. Link related entries with See Also
3. Promote high-value learnings to skills

Ask in chat: "Should I log this as a learning?"
```

**检测**：会话结束时手动审查

### OpenClaw

**激活**：工作区注入 + 跨代理消息
**设置**：参见上面的"OpenClaw 设置"部分
**检测**：通过会话工具和工作区文件

### 代理无关指导

无论使用什么代理，在以下情况下应用自我改进：

1. **发现非显而易见的东西** - 解决方案不是立即的
2. **纠正自己** - 初始方法错误
3. **学习项目约定** - 发现未记录的模式
4. **遇到意外错误** - 特别是如果诊断困难
5. **找到更好的方法** - 改进了原始解决方案

### Copilot Chat 集成

对于 Copilot 用户，在相关时将此添加到你的提示中：

> 完成此任务后，评估是否应使用自我改进技能格式将任何学习内容记录到 `.learnings/`。

或使用快速提示：
- "把这个记录到学习"
- "从这个解决方案创建技能"
- "检查 .learnings/ 中的相关问题"
