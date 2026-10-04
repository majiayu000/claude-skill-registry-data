---
name: pdlc-api-mock
description: API Mock 数据生成
argument-hint: <接口路径 | OpenAPI 文件>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: engineering
produces: []
requires: []
next_step: null
terminal_state: null
---

# API Mock 数据生成

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

根据 API 设计文档生成 Mock 数据和 Mock 服务配置，供前端联调使用。

## 工作流程
1. **阅读 API 设计**: 阅读 `docs/02_design/api/` 下的 API 设计文档
2. **生成 Mock 数据**: 为每个接口生成符合数据模型的 Mock 响应
3. **生成 Mock 配置**: 根据技术栈生成对应的 Mock 服务文件
4. **输出到指定位置**: 前端应用的 `mock/` 或 `src/services/__mocks__/` 目录

## Mock 数据要求
- 数据要贴近真实场景，不要用 "test1"、"aaa" 之类的无意义数据
- 列表接口至少生成 5-10 条数据
- 覆盖各种状态：正常数据、边界数据、空数据
- 包含分页信息
- 错误响应也要生成 Mock

## 输出格式
```json
{
  "code": 0,
  "message": "成功",
  "data": { ... }
}
```

## 要求
- Mock 数据中的中文内容要有实际含义
- 时间字段使用合理的时间范围
- ID 字段使用合理的格式（UUID/数字）
- 生成完成后告知前端同学如何启用 Mock 服务

目标接口: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ API Mock 数据 完成
📦 产出：（生成到前端应用 mock/ 目录）
👉 下一步：（本次流程结束，无后续）
```
