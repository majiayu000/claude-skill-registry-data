---
name: 自更新
description: This skill should be used when the user wants to "improve a skill", "update skill based on feedback", "optimize skill after use", or says "自更新", "/自更新". Collects user feedback after using a skill and automatically updates that skill with improvements.
tools: Read, Glob, Grep, Edit
---

# Skill 自更新

基于使用反馈，自动优化和更新 skill 内容。

## 触发场景

- 用户刚使用完某个 skill，想要改进它
- 用户说"自更新"、"优化这个 skill"、"更新刚才的 skill"
- 用户对 skill 执行结果有反馈意见

## 工作流程

### Phase 1: 识别最近使用的 Skill

从当前会话上下文中识别最近使用的 skill：

1. **检查会话历史** - 查找最近调用的 `/skill-name` 或被触发的 skill
2. **确认目标 skill** - 向用户确认要优化的是哪个 skill

```
识别到最近使用的 skill: [skill-name]
确认要对这个 skill 进行优化吗？
```

### Phase 2: 收集反馈

引导用户提供具体反馈：

**反馈维度：**

| 维度 | 问题示例 |
|------|----------|
| 执行效果 | 这次执行结果符合预期吗？哪里不符合？ |
| 缺失功能 | 有什么功能是你期望但 skill 没做到的？ |
| 多余步骤 | 有哪些步骤是不必要的或可以简化的？ |
| 表述问题 | skill 的指令有歧义或不够清晰的地方吗？ |
| 新增场景 | 有没有新的使用场景需要覆盖？ |

**简化收集（默认）：**

如果用户已经明确说出问题，直接进入下一阶段，无需逐一询问。

### Phase 3: 定位 Skill 文件

搜索对应的 SKILL.md 文件：

```bash
# 优先级顺序
# 1. 个人级 skills
~/.claude/skills/<skill-name>/SKILL.md

# 2. 项目级 skills
.claude/skills/<skill-name>/SKILL.md

# 3. 插件中的 skills
~/.claude/plugins/**/skills/<skill-name>/SKILL.md
```

读取当前 SKILL.md 内容，分析结构。

### Phase 4: 分析优化点

对比使用过程和反馈，识别优化点：

**分析维度：**

1. **触发描述** - description 中的触发词是否需要补充
2. **流程步骤** - 工作流程是否需要调整
3. **边界条件** - 是否需要增加异常处理
4. **示例补充** - 是否需要添加新的使用示例
5. **资源引用** - 是否需要添加 references/ 或 scripts/

**输出格式：**

```markdown
## 优化分析

### 问题定位
- [具体问题描述]

### 优化方案
1. [优化点1]: [具体改动]
2. [优化点2]: [具体改动]

### 影响评估
- 改动范围: [小/中/大]
- 风险等级: [低/中/高]
```

### Phase 5: 执行更新

展示 diff 并请求确认：

```markdown
### 更新预览: ~/.claude/skills/[skill-name]/SKILL.md

**改动原因:** [简述为什么需要这个改动]

```diff
- 原内容
+ 新内容
```

确认应用这些更新吗？
```

用户确认后，使用 Edit 工具应用更改。

### Phase 6: 验证更新

更新完成后：

1. 读取更新后的文件，确认改动已生效
2. 输出更新摘要

```markdown
## 更新完成

**Skill:** [skill-name]
**更新内容:**
- [改动点1]
- [改动点2]

**下次使用时生效**
```

## 更新原则

**应该更新的：**
- 遗漏的触发词或使用场景
- 不清晰或有歧义的指令
- 缺失的步骤或流程
- 需要的错误处理
- 有价值的使用技巧

**不应该更新的：**
- 一次性的特殊情况
- 用户个人偏好（除非明确要求）
- 与 skill 核心功能无关的内容
- 会破坏现有功能的改动

## 特殊处理

### 插件中的 Skill

如果目标 skill 位于 `~/.claude/plugins/` 下：

1. **警告用户** - 插件更新可能覆盖本地修改
2. **建议方案**:
   - 复制到 `~/.claude/skills/` 作为个人版本
   - 或记录修改，等插件更新后重新应用

### 无法定位 Skill

如果找不到对应的 SKILL.md：

1. 列出可能的候选 skill
2. 让用户确认或手动指定路径

## 用户交互示例

**示例 1: 简单反馈**
```
用户: 刚才那个 commit skill 少了一个场景，我想让它也支持 amend
助手: 收到，我来更新 commit skill，添加 amend 场景支持...
[执行更新流程]
```

**示例 2: 详细反馈**
```
用户: /自更新
助手: 识别到最近使用的 skill: code-review
      请问这次使用有什么需要改进的地方？
用户: 它没有检查安全问题，我希望加上安全审查的步骤
助手: 明白，我来分析并更新...
[执行更新流程]
```

## 注意事项

- 保持 SKILL.md 简洁，详细内容放 references/
- 更新后保持原有格式风格
- 使用祈使句，避免第二人称
- description 使用第三人称
