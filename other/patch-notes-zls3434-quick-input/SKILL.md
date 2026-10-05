---
name: patch-notes
description: "生成面向用户的更新说明，将技术性变更日志转换为非技术语言。"
license: MIT
metadata:
  model: haiku
  argument-hint: "[版本号]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /patch-notes}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# patch-notes — 面向用户更新说明

## 技能目的

将技术性的变更日志转换为面向最终用户的更新说明，使用非技术语言描述用户可感知的变更，作为发布说明、应用商店更新文案或公告草稿。

## 参数说明

- `[版本号]`：可选，指定生成更新说明的版本号。省略时使用最新版本。

## 分阶段工作流

### 阶段 1：读取变更日志

- **输入**：版本号参数
- **处理**：
  1. 使用 Glob 查找 `CHANGELOG.md` 或 `docs/release/changelog*`
  2. 使用 Read 读取变更日志，定位目标版本章节
  3. 若未指定版本，取文件顶部最新版本
  4. 提取该版本的全部变更条目
- **输出**：目标版本变更条目

### 阶段 2：提取用户可见变更

- **输入**：目标版本变更条目
- **处理**：
  1. 过滤纯内部重构、依赖升级、CI 配置等用户不可感知项
  2. 保留新功能、界面变更、行为变更、问题修复
  3. 使用 Grep 识别含用户影响的关键词（`UI`、`API`、`workflow`、`performance`）
  4. 标注每条变更的受众：所有用户 / 高级用户 / 管理员
- **输出**：用户可见变更清单

### 阶段 3：转换为非技术语言

- **输入**：用户可见变更清单
- **处理**：
  1. 将技术描述改写为用户视角的收益描述
  2. 例如："feat: 添加导出 CSV" → "您现在可以将数据导出为 CSV 文件"
  3. 例如："fix: 修复登录超时" → "修复了部分情况下登录超时的问题"
  4. 标注是否需要用户操作（迁移、配置变更）
  5. 对 BREAKING CHANGE 用醒目方式提示
- **输出**：非技术语言更新说明

### 阶段 4：生成发布说明

- **输入**：非技术语言更新说明
- **处理**：
  1. 按新功能、改进、问题修复、注意事项分组
  2. 添加版本号与日期标题
  3. 补充感谢语与反馈渠道
  4. 使用 Write 生成文件 `docs/release/patch-notes-{版本}.md`
  5. 同时生成简洁版用于应用商店或公告
- **输出**：面向用户的发布说明

## 协作协议引用

- 遵循 `.claude/docs/coding-standards.md` 编码规范
- 发布说明写入 `docs/release/` 目录
- 内容需用户确认后方可对外发布
- 不自动提交

## 推荐下一步

使用 `/changelog` 生成或更新技术性变更日志。使用 `/launch-checklist` 执行最终发布验证。使用 `/day-one-patch` 准备首日已知问题补丁说明。