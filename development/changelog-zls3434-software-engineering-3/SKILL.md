---
name: changelog
description: "从 Git 历史生成变更日志，按 Conventional Commits 分类为 Added/Changed/Fixed/Removed。"
license: MIT
metadata:
  model: haiku
  argument-hint: "[起始版本] [结束版本]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /changelog}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# changelog — 变更日志生成

## 技能目的

从 Git 提交历史生成结构化变更日志，按 Conventional Commits 规范分类为 Added（新增）、Changed（变更）、Fixed（修复）、Removed（移除），为版本发布提供可追溯的技术变更记录。

## 参数说明

- `[起始版本]`：可选，变更日志的起始标签（如 `v1.1.0`）。省略时从上一个版本标签开始。
- `[结束版本]`：可选，变更日志的结束标签（如 `v1.2.0`）。省略时到当前 HEAD。

## 分阶段工作流

### 阶段 1：读取 Git 日志

- **输入**：版本范围参数
- **处理**：
  1. 使用 Bash 执行 `git tag` 获取已有版本标签
  2. 使用 Bash 执行 `git log {起始}..{结束} --pretty=format:"%h %s"` 获取提交
  3. 若无标签，使用 Bash 执行 `git log --since` 按日期范围获取
  4. 捕获全部提交哈希与消息
- **输出**：原始提交清单

### 阶段 2：按 Conventional Commits 分类

- **输入**：原始提交清单
- **处理**：
  1. 解析提交消息前缀：`feat:` → Added，`fix:` → Fixed
  2. `refactor:` / `perf:` / `chore:` → Changed
  3. `revert:` / `BREAKING CHANGE` → Removed 或 Changed
  4. 使用 Grep 过滤非规范提交，标注为 Uncategorized
  5. 对每条提交补充作用域（scope）与简要说明
- **输出**：分类后的变更条目

### 阶段 3：生成变更日志

- **输入**：分类后的变更条目
- **处理**：
  1. 按 Added / Changed / Fixed / Removed 分组排序
  2. 每条含：提交哈希、作用域、描述
  3. 标注 BREAKING CHANGES 单独成节
  4. 使用 Read 读取现有 `CHANGELOG.md` 保留历史内容
  5. 使用 Write 在文件顶部插入新版本章节
- **输出**：更新后的 CHANGELOG.md

## 协作协议引用

- 遵循 `.claude/docs/coding-standards.md` 编码规范
- 变更日志写入项目根目录 `CHANGELOG.md`
- 遵循 Keep a Changelog 格式规范
- 不自动提交，需用户确认后提交

## 推荐下一步

使用 `/patch-notes` 将技术性变更日志转换为面向用户的发布说明。使用 `/release-checklist` 验证发布前检查清单。使用 `/launch-checklist` 执行最终发布验证。