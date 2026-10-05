---
name: release-notes-cn
description: Use when drafting Chinese release notes or changelogs from commits, PRs, or diffs with clear user-facing impact and upgrade notes.
---

# Release Notes CN

用在根据 commits、PR、diff 或变更清单生成中文 release notes、CHANGELOG 或版本公告时。目标是让用户知道“变了什么、影响谁、要不要行动”。

## 适用场景

- 用户说“帮我写 release notes”“整理 changelog”“发版说明怎么写”。
- 需要把技术提交翻译成用户能理解的中文说明。
- 开源项目需要补升级说明、破坏性变更和迁移步骤。

## 不适用场景

- 没有任何变更来源，用户只是要营销文案。
- 涉及未公开安全修复细节，不能披露可被利用的信息。
- 用户需要英文公告，除非明确要求双语。

## 工作流

1. 收集变更来源。
   - 优先读取 `git log`、PR 标题、merge commits、CHANGELOG、diff。
   - 区分功能、修复、文档、内部重构、依赖、破坏性变更。

2. 提炼用户影响。
   - 每条说明回答：用户会看到什么变化？是否需要升级动作？是否有兼容影响？
   - 不把内部实现细节堆给用户，除非它影响使用。

3. 标出升级风险。
   - Breaking changes。
   - 配置、数据库、环境变量、权限、迁移脚本。
   - 已知问题和回滚建议。

4. 生成中文版本说明。
   - 简洁、可扫描。
   - 避免夸张宣传。

## 输出格式

```text
## vX.Y.Z

### 新增
- ...

### 修复
- ...

### 改进
- ...

### 破坏性变更
- ...

### 升级说明
- ...
```

只包含实际存在的分类；没有内容的分类不要硬写。

## 验证方式

- 每条 release note 应能追溯到 commit、PR、issue 或 diff。
- 如果有推断，明确标注“根据变更推断”。
- 不要编造版本号、日期或贡献者。
