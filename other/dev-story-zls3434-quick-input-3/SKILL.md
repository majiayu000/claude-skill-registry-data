---
name: dev-story
description: "核心实现技能。读取 Story 文件并按 7 阶段工作流实现功能：找到 Story、加载上下文、路由到正确程序员、实现、测试证据、收集总结、更新会话状态。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[故事路径]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
    - Task
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /dev-story}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# dev-story —— Story 实现技能

## 技能目的

将一份"已就绪"的 Story 从入口文件推进到代码落地、测试通过、会话状态更新。
本技能是工作室的"核心引擎"，负责协调各 specialist 程序员 Agent 完成具体实现工作，
并保证实现过程可追溯、可审计、可回滚。

## 参数说明

- `[故事路径]`：指向待实现的 Story Markdown 文件，例如 `docs/stories/PAY-301.md`。
  若仅给出 Story ID，则在 `docs/stories/` 下按 ID 模糊匹配定位文件。

## 分阶段工作流

### 阶段 1：找到 Story

- **输入**：用户提供的 `[故事路径]` 或 Story ID。
- **处理**：使用 Read 读取目标文件；若路径不存在则用 Glob 在 `docs/stories/` 下匹配。
- **输出**：确认 Story 文件绝对路径，并解析其 frontmatter 中的 ID、标题、Epic、验收标准。

### 阶段 2：加载上下文

- **输入**：Story 文件中引用的相关文档。
- **处理**：并行加载以下上下文：
  1. Story 本体（已在阶段 1 读取）
  2. 技术需求注册表（`docs/registry/TR-*.md`）
  3. 相关架构决策记录（`docs/adr/ADR-*.md`）
  4. 控制清单（`docs/checklists/`）
  5. `.claude/docs/technical-preferences.md`
- **输出**：一份"上下文摘要"写入临时工作区，供后续阶段引用。

### 阶段 3：路由到正确程序员

- **输入**：Story 中声明的层级与领域标签。
- **处理**：依据路由表分发到对应 specialist：
  - 基础层 → 对应 specialist（database-programmer / auth-programmer / api-programmer）
  - UI 层 → `ui-programmer`
  - 业务逻辑 → `service-programmer`
  - 集成层 → `integration-programmer`
  - 基础设施 → `infra-programmer`
- **输出**：确定主程序员 Agent，必要时使用 Task 工具派发子任务。

### 阶段 4：实现

- **输入**：路由结果与上下文摘要。
- **处理**：按协作协议先展示草稿，获用户审批后再 Write；多文件变更需对完整变更集单独审批。
- **输出**：实际写入的源代码与配置文件清单。

### 阶段 5：测试证据

- **输入**：阶段 4 产生的代码变更。
- **处理**：运行 `Bash` 执行单元/集成测试；收集命令输出与覆盖率摘要。
- **输出**：测试通过的证据片段，附命令与退出码。

### 阶段 6：收集总结

- **输入**：阶段 2-5 的所有产物。
- **处理**：生成"实现总结"：变更文件、关键决策、测试结果、遗留 TODO。
- **输出**：总结 Markdown，写入 Story 文件的"实现记录"小节。

### 阶段 7：更新会话状态

- **输入**：阶段 6 的总结。
- **处理**：更新会话状态文件（如 `.claude/state/session.md`）标记 Story 状态为 `implemented`。
- **输出**：确认状态已写入，并提示用户下一步推荐操作。

## 协作协议引用

- 用户驱动协作，非自主执行。每个阶段关键决策点使用 AskUserQuestion 询问用户偏好。
- 在使用 Write 前必须询问："我可以将此写入 [文件路径] 吗？"
- 请求审批前必须展示草稿或摘要；多文件修改需针对完整变更集获得明确审批。
- 未经用户指示不得执行 Git 提交。

## 推荐下一步

- 实现完成后运行 `/story-done [故事路径]` 进行完成审查。
- 若需多人交叉审查代码，运行 `/code-review [文件路径]`。
- 若发现 Story 描述与实际需求偏差，运行 `/scope-check [故事路径]` 检测范围蔓延。