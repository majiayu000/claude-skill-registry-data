---
name: issue-manager
description: 议题管理工具。从代码审查报告创建 GitHub Issues，跟踪和修复问题，管理技术债务。用于将审查结果转化为可执行任务、讨论特定问题、批量修复 issues。触发词：创建议题、管理 issue、修复问题、讨论 issue。
allowed-tools: Read, Write, Bash, Grep, Glob, Edit
---

# 议题管理 Issue Manager

## 目标
将代码审查发现的问题转化为可追踪的 GitHub Issues，并协助修复和管理这些问题。

## 核心功能

### 1. 从审查报告创建 Issues
- 读取 code-audit 生成的审查报告
- 将问题按严重程度分类
- 为每个问题创建结构化的 GitHub Issue
- 自动添加合适的标签（bug, enhancement, documentation, tech-debt）
- 设置优先级和里程碑

### 2. 讨论和分析 Issues
- 深入分析特定 issue 的根本原因
- 提供多种解决方案及其权衡
- 估算修复的影响范围
- 生成修复计划

### 3. 批量修复 Issues
- 选择一个或多个相关 issues 进行修复
- 自动创建修复分支
- 实施修复
- 运行测试验证
- 创建 Pull Request

## 使用方式

### 方式 1: 从审查报告创建议题
```
请用 /issue-manager 从最新的代码审查报告创建 issues
```

### 方式 2: 讨论特定问题
```
请用 /issue-manager 讨论 issue #42 的解决方案
```

### 方式 3: 修复单个问题
```
请用 /issue-manager 修复 issue #42
```

### 方式 4: 批量修复相关问题
```
请用 /issue-manager 修复所有组件一致性相关的 issues
```

### 方式 5: 查看问题状态
```
请用 /issue-manager 查看所有待修复的代码质量问题
```

## 工作流程

### 流程 1: 创建 Issues

当用户请求从审查报告创建 issues 时：

#### 步骤 1: 确认创建
**必须先获得用户明确同意**，使用 AskUserQuestion 询问：
- 是否要创建 issues？
- 创建哪个严重级别的问题？（严重/中等/低优先级/全部）
- 是否要添加特定标签或里程碑？

#### 步骤 2: 读取审查报告
- 查找最近的审查报告（或用户指定的报告）
- 解析问题列表

#### 步骤 3: 检查重复议题
**重要：创建前必须先查重，避免重复创建**

使用 `gh issue list` 搜索已有的相似议题：

```bash
# 搜索标题中包含关键词的议题
gh issue list --search "投放状态" --state all --json number,title,state

# 搜索特定标签的议题
gh issue list --label "tech-debt,code-quality" --json number,title,body
```

对于每个待创建的问题：
1. 提取关键词（如"投放状态"、"重复代码"、"组件一致性"）
2. 搜索已有 issues 的标题和内容
3. 如果找到相似的议题，询问用户：
   - 是否要在已有 issue 中补充信息？
   - 还是仍然创建新 issue？
4. 如果是重复议题，跳过创建，在已有 issue 中添加评论补充信息

示例输出：
```markdown
⚠️ 发现可能重复的议题：

待创建: "大量重复的投放状态检查逻辑"
已存在: #85 "投放状态验证逻辑需要统一" (open)

是否要：
1. 在 #85 中补充新发现的重复代码位置
2. 仍然创建新 issue（如果确实是不同的问题）
```

#### 步骤 4: 为每个问题创建 Issue
使用 `gh issue create` 创建结构化的 issue：

```bash
gh issue create \
  --title "🔴 [严重] 大量重复的投放状态检查逻辑" \
  --body "$(cat <<'EOF'
## 📍 位置
`actions/delivery.ts:145-180`

## ❌ 问题描述
大量重复的投放状态检查逻辑分散在不同函数中，导致维护困难，容易出现不一致。

## 💥 影响
- 代码维护困难
- 容易出现逻辑不一致的 bug
- 修改时需要同步多处代码

## ✅ 建议方案
抽离到统一的工具函数 `lib/utils/delivery-status.ts`

```typescript
// 建议创建
export function validateDeliveryStatus(status: DeliveryStatus) {
  // 统一的状态验证逻辑
}
```

## 📋 验收标准
- [ ] 创建 `lib/utils/delivery-status.ts`
- [ ] 实现统一的状态验证函数
- [ ] 重构所有调用点使用新函数
- [ ] 添加单元测试
- [ ] 验证所有功能正常

## 🔗 相关文件
- `actions/delivery.ts`
- 其他调用投放状态检查的文件

---
*由 code-audit 自动生成*
EOF
)" \
  --label "tech-debt,priority-high,code-quality" \
  --assignee "@me"
```

#### 步骤 5: 生成总结报告
创建完成后，输出 Markdown 报告：

```markdown
# ✅ Issues 创建完成

共创建 **12 个 issues**：

## 🔴 严重问题 (3 个)
- #123 - [严重] 大量重复的投放状态检查逻辑
- #124 - [严重] 组件中的业务逻辑应移至 Server Actions
- #125 - [严重] 'use client' 滥用导致 bundle 过大

## 🟡 中等问题 (6 个)
- #126 - [中等] 函数过长需要拆分
- #127 - [中等] 组件一致性问题
- #128 - [中等] 无效代码清理
- ...

## 🟢 低优先级 (3 个)
- #129 - [低] 依赖更新
- #130 - [低] 添加 Prettier
- ...

## 📊 标签分布
- `tech-debt`: 8 个
- `bug`: 2 个
- `enhancement`: 2 个
- `documentation`: 1 个

## 🔗 查看所有 issues
https://github.com/your-repo/issues?q=is:issue+is:open+label:code-quality
```

### 流程 2: 讨论 Issue

当用户请求讨论某个 issue 时：

#### 步骤 1: 获取 Issue 详情
```bash
gh issue view 42 --json title,body,labels
```

#### 步骤 2: 分析问题
- 读取相关文件
- 理解问题的上下文
- 分析根本原因

#### 步骤 3: 提供解决方案
生成详细的讨论报告：

```markdown
# 🔍 Issue #42 深度分析

## 问题回顾
[问题描述]

## 🎯 根本原因
经过分析，这个问题的根本原因是...

## 💡 解决方案

### 方案 1: 抽离公共函数（推荐）
**优点**:
- 易于维护
- 可复用
- 测试简单

**缺点**:
- 需要重构多处调用点

**实施步骤**:
1. 创建 `lib/utils/delivery-status.ts`
2. 实现统一的验证函数
3. ...

**预计工作量**: 2-3 小时

### 方案 2: 使用装饰器模式
**优点**:
- ...

**缺点**:
- ...

## 🔗 影响范围
需要修改的文件：
- `actions/delivery.ts` (3 处)
- `actions/campaign.ts` (2 处)
- ...

## ⚠️ 风险评估
- **风险等级**: 低
- **回归风险**: 需要充分测试投放流程
- **建议**: 在测试环境充分验证后再部署

## 🗳️ 建议
推荐使用方案 1，理由是...
```

#### 步骤 4: 等待用户决策
使用 AskUserQuestion 询问用户：
- 选择哪个方案？
- 是否立即开始修复？

### 流程 3: 修复 Issue

当用户请求修复 issue 时：

#### 步骤 1: 分析问题并制定修复方案
- 获取 issue 详情
- 读取相关文件了解上下文
- 制定详细的修复方案

#### 步骤 2: 在 Issue 评论区说明修复方案并等待确认
**重要：在实际修复前，必须先在 issue 评论区说明方案，等待用户确认**

使用 `gh issue comment` 发布修复方案：

```bash
gh issue comment 42 --body "$(cat <<'EOF'
## 🤖 AI 修复方案

我已分析了这个问题，建议采用以下方案进行修复：

### 📋 修复计划

**问题**: 大量重复的投放状态检查逻辑

**方案**: 抽离到统一的工具函数

**具体步骤**:
1. 创建 `lib/utils/delivery-status.ts`
2. 实现统一的 `validateDeliveryStatus` 函数
3. 重构以下文件使用新函数：
   - `actions/delivery.ts` (3 处调用)
   - `actions/campaign.ts` (2 处调用)
   - `app/api/delivery/route.ts` (1 处调用)

**预期效果**:
- ✅ 删除约 45 行重复代码
- ✅ 提高代码可维护性
- ✅ 统一状态验证逻辑

**影响范围**:
- 修改 3 个文件
- 不影响现有功能
- 无破坏性变更

**验证方式**:
- 运行 `pnpm tsc --noEmit` 确保类型正确
- 运行 `pnpm build` 确保构建成功
- 测试投放相关功能

### ⚠️ 风险评估
- **风险等级**: 低
- **建议**: 修复后需测试投放流程

---

**是否同意此修复方案？**

如果同意，请在评论中回复：
- 自然语言："修"、"同意"、"开始修复"（AI 会自动理解）
- 明确指令：`/confirm-fix` 或 `/approve`（快捷通道）

我将自动开始修复。如果需要调整，请说明具体要求。
EOF
)"
```

然后等待用户回复或确认：
- 用户回复"同意"或类似内容
- 或用户添加 `fix-approved` 标签
- 或用户在对话中明确表示同意

#### 步骤 3: 确认修复范围
获得用户初步同意后，使用 AskUserQuestion 再次确认细节：
- 是否需要创建新分支？
- 是否需要添加测试？
- 是否立即推送 PR？

#### 步骤 4: 创建修复分支（如果需要）
```bash
git checkout -b fix/issue-42-delivery-status-duplication
```

#### 步骤 5: 实施修复
- 根据讨论的方案进行代码修改
- 使用 Edit/Write 工具修改文件
- 添加必要的测试

#### 步骤 6: 验证修复
```bash
# 运行类型检查
pnpm tsc --noEmit

# 运行测试（如果有）
pnpm test

# 运行构建
pnpm build
```

#### 步骤 7: 提交和关联 Issue
```bash
git add .
git commit -m "$(cat <<'EOF'
fix: 抽离投放状态验证逻辑到公共函数

- 创建 lib/utils/delivery-status.ts
- 实现统一的 validateDeliveryStatus 函数
- 重构 actions/delivery.ts 使用新函数
- 重构 actions/campaign.ts 使用新函数

Fixes #42

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### 步骤 8: 报告修复结果
```markdown
# ✅ Issue #42 修复完成

## 📝 修复内容
- 创建了 `lib/utils/delivery-status.ts`
- 实现了统一的状态验证函数
- 重构了 3 个文件的调用点

## ✅ 验证结果
- TypeScript 类型检查: ✅ 通过
- 构建: ✅ 成功
- 测试: ✅ 通过（如果有）

## 📊 代码变更
- 新增文件: 1
- 修改文件: 3
- 删除重复代码: ~45 行

## 🔗 下一步
是否要：
1. 推送到远程并创建 PR？
2. 继续修复相关的 issue #43？
3. 运行 code-audit 验证修复效果？
```

### 流程 4: 批量修复

当用户请求批量修复时：

#### 步骤 1: 查找相关 Issues
```bash
gh issue list --label "组件一致性" --json number,title
```

#### 步骤 2: 展示并确认
使用 AskUserQuestion 让用户选择要修复的 issues

#### 步骤 3: 逐个修复
按照"流程 3"的步骤依次修复每个 issue

#### 步骤 4: 生成批量修复报告

## Issue 模板

### 严重问题模板
```
标题: 🔴 [严重] {问题简述}
标签: priority-high, tech-debt, code-quality
```

### 中等问题模板
```
标题: 🟡 [中等] {问题简述}
标签: priority-medium, tech-debt, code-quality
```

### 低优先级模板
```
标题: 🟢 [低] {问题简述}
标签: priority-low, enhancement
```

### 组件一致性问题
```
标签: ui-consistency, tech-debt
```

### 无效代码清理
```
标签: cleanup, tech-debt
```

### 文档缺失
```
标签: documentation
```

### 性能优化
```
标签: performance, enhancement
```

## 智能功能

### 1. 自动分类
根据问题类型自动添加合适的标签：
- 代码重复 → `tech-debt`, `refactoring`
- 组件一致性 → `ui-consistency`, `tech-debt`
- 性能问题 → `performance`, `enhancement`
- 文档缺失 → `documentation`
- 类型安全 → `type-safety`, `bug`
- 无效代码 → `cleanup`, `tech-debt`

### 2. 关联相关 Issues
创建时自动检测相关的 issues，在 body 中添加：
```markdown
## 🔗 相关 Issues
- #123 - 类似的重复代码问题
- #124 - 同一文件的其他问题
```

### 3. 优先级推荐
根据问题的影响范围和严重程度推荐优先级

### 4. 里程碑建议
根据问题类型建议合适的里程碑（如 "代码质量提升 Q1"）

## 查询和统计

### 查看待修复问题
```bash
gh issue list --label "code-quality" --state open
```

### 统计问题分布
```bash
gh issue list --label "tech-debt" --json labels --jq '.[].labels[].name' | sort | uniq -c
```

### 查看某个标签的所有问题
```bash
gh issue list --label "组件一致性"
```

## 特殊场景处理

### 场景 1: 没有 Git 仓库
如果项目不是 Git 仓库或没有配置 GitHub，改为：
1. 创建本地 TODO 文件 `.claude/issues/TODO.md`
2. 以 Markdown 格式记录问题
3. 提示用户后续可手动创建 issues

### 场景 2: 依赖问题
如果 `gh` CLI 未安装，提示用户：
```bash
# macOS
brew install gh

# 认证
gh auth login
```

### 场景 3: 用户取消
如果用户不同意创建 issues，提供其他选项：
- 导出为 Markdown 文件
- 导出为 CSV 文件
- 仅显示问题清单

## 输出格式

### 创建 Issue 时的输出
每创建一个 issue，显示进度：
```
✅ [1/12] 创建 Issue #123: 大量重复的投放状态检查逻辑
✅ [2/12] 创建 Issue #124: 组件中的业务逻辑应移至 Server Actions
...
```

### 修复 Issue 时的输出
显示清晰的步骤进度：
```
🔧 开始修复 Issue #42

[1/5] 📖 读取相关文件...
[2/5] ✏️ 创建 lib/utils/delivery-status.ts...
[3/5] ♻️ 重构 actions/delivery.ts...
[4/5] ✅ 运行验证...
[5/5] 💾 提交更改...

✅ 修复完成！
```

## 最佳实践

1. **始终获得用户同意**再创建 issues
2. **提供详细的上下文**在 issue body 中
3. **添加验收标准**让 issue 可执行
4. **关联相关文件和代码位置**方便定位
5. **一次只修复一个问题**避免改动过大
6. **修复后运行验证**确保没有引入新问题
7. **使用语义化的 commit message**
8. **在 commit 中关联 issue**（使用 `Fixes #42`）

## 与 code-audit 的协作

issue-manager 是 code-audit 的完美补充：

```
code-audit (发现问题)
    ↓
issue-manager (创建追踪)
    ↓
issue-manager (讨论方案)
    ↓
issue-manager (实施修复)
    ↓
code-audit (验证效果)
```

## GitHub Actions 自动化

issue-manager 包含多个 GitHub Actions 工作流，实现全自动的 issue 管理：

### 已部署的工作流

详细文档请查看 [workflows/README.md](./workflows/README.md)

1. **claude-code-pr-review.yml** - PR 代码审查
   - 使用 /code-audit 自动审查每个 PR
   - 检查 Next.js 最佳实践、代码重复等

2. **claude-code-issue-triage.yml** - Issue 自动分诊
   - 新 issue 打开时自动分析
   - 建议分类、优先级和标签

3. **claude-code-auto-fix.yml** - 两阶段自动修复
   - 阶段 1：AI 提出修复方案
   - 阶段 2：用户确认后执行修复
   - 自动创建修复 PR

4. **claude-code-issue-chat.yml** - Issue 对话
   - AI 自动回复 issue 中的评论
   - 支持多轮对话和代码查看

5. **claude-code-confirm-fix.yml** - 确认修复指令
   - 快速响应明确的确认指令（`/confirm-fix`、`/approve`）
   - 自动添加 `fix-confirmed` 标签触发修复
   - 自然语言确认由 issue-chat 智能处理

### 用户体验优化

通过评论指令确认修复方案，支持两种方式：

**方式 1：自然语言**（推荐）
1. AI 提出修复方案（发布在 issue 评论中）
2. 用户直接评论："修"、"同意"、"开始修复"等
3. `issue-chat` 工作流识别意图，检查标签，添加 `fix-confirmed`
4. 触发修复工作流执行修复
5. 创建草稿 PR

**方式 2：明确指令**（快捷通道）
1. 用户评论 `/confirm-fix` 或 `/approve`
2. `confirm-fix` 工作流快速添加 `fix-confirmed` 标签
3. 触发修复工作流

### 生成工作流文件

使用以下命令生成 GitHub Actions 工作流：

```
请用 /issue-manager 生成 GitHub Actions 工作流
```

这将在 `.github/workflows/` 目录下创建以下文件：

1. **code-audit-pr.yml** - PR 代码审查
   - 每次 PR 时自动运行代码质量检查
   - 在 PR 中发布审查评论
   - 严重问题自动创建 issue

2. **weekly-audit.yml** - 每周质量扫描
   - 每周一自动扫描代码库
   - 生成质量报告 issue
   - 统计代码指标和趋势
   - 自动创建改进建议 issue

3. **auto-fix.yml** - 自动修复
   - 对标记 `auto-fix` 的 issue 自动修复
   - 自动创建修复 PR
   - 支持批量修复简单问题

### 工作流详解

#### 1. PR 代码审查工作流

触发时机：
- 创建 PR
- PR 更新
- 手动触发

自动检查：
- TypeScript 类型错误
- 未使用的导入
- Console 调试语句
- TODO/FIXME 标记
- 文件大小

输出：
- PR 评论中的审查报告
- 严重问题自动创建 issue
- 上传审查报告为 artifact

#### 2. 每周质量扫描

触发时机：
- 每周一早上 9:00 (UTC)
- 手动触发

统计指标：
- 代码库规模（文件数、行数）
- 质量指标（TODO、console、any 类型）
- 依赖更新状态
- 构建状态

自动化：
- 创建每周报告 issue
- console 过多时自动创建清理 issue
- 趋势分析和建议

#### 3. 自动修复工作流

触发时机：
- issue 被标记为 `auto-fix`
- 手动指定 issue 编号

支持修复：
- 移除 console.log 调试语句
- 修复导入语句排序
- 代码格式化（通过 ESLint）

流程：
1. 创建修复分支 `auto-fix/issue-{number}`
2. 应用自动修复
3. 提交更改
4. 创建 PR 并关联原 issue
5. 在 issue 中评论 PR 链接

### 如何使用

#### 启用 PR 审查

1. 将工作流文件复制到 `.github/workflows/`
2. 每次创建 PR 时自动运行
3. 在 PR 评论中查看审查结果

#### 启用每周扫描

1. 工作流会在每周一自动运行
2. 在 Issues 中查看每周报告
3. 根据建议采取行动

#### 使用自动修复

1. 对于简单问题，添加 `auto-fix` 标签
2. GitHub Actions 自动创建修复 PR
3. Review 并合并 PR

示例：
```
# 创建一个需要清理 console 的 issue
gh issue create \
  --title "清理 console.log 语句" \
  --label "auto-fix,cleanup" \
  --body "自动移除调试用的 console 语句"

# GitHub Actions 会自动：
# 1. 检测到 auto-fix 标签
# 2. 创建修复分支
# 3. 移除 console.log
# 4. 创建 PR
```

### 工作流模板位置

所有工作流模板保存在：
`.claude/skills/issue-manager/workflows/`

使用 issue-manager 时可以一键复制到项目的 `.github/workflows/` 目录。

### 最佳实践

1. **逐步启用**：先启用 PR 审查，稳定后再启用其他工作流
2. **调整阈值**：根据项目实际情况调整触发条件（如文件行数限制）
3. **Review 自动修复**：自动修复的 PR 仍需人工 review
4. **定期查看报告**：关注每周报告中的趋势变化
5. **及时处理 issue**：不要让自动创建的 issue 积压太多

## 注意事项

- 创建 issues 前必须征得用户同意
- 修复代码时要充分测试
- 批量修复时注意不要一次改动过多
- 对于复杂的修复，先创建 PR 让团队 review
- 保持 issue 描述的清晰和可执行
- 定期回顾和关闭已解决的 issues
- GitHub Actions 工作流需要适当的权限配置
- 自动修复仅适用于简单的代码质量问题
