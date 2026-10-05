---
name: pr-review-cn
description: Use when reviewing a pull request or local diff and the user wants Chinese findings focused on bugs, regressions, tests, and maintainability risks.
---

# PR Review CN

用在审查 Pull Request、本地 diff、补丁或待合并分支时。优先找真实风险，不把格式偏好包装成问题。

## 适用场景

- 用户说“review 这个 PR”“看这个 diff 有没有问题”“合并前帮我检查”。
- 开源维护者需要快速判断 PR 是否可合并。
- 需要用中文给贡献者可执行的反馈。

## 不适用场景

- 用户只想要代码解释，不需要审查。
- 还没有 diff 或变更范围。
- 纯设计讨论，尚未进入代码阶段。

## 工作流

1. 明确变更范围。
   - 查看 `git status`、`git diff`、PR 描述或相关 issue。
   - 先理解意图，再判断实现。

2. 优先检查高风险问题。
   - 行为回归、边界条件、错误处理、并发/事务、权限、安全、数据迁移、兼容性。
   - 检查测试是否覆盖新行为和失败路径。

3. 验证可运行性。
   - 能跑测试就跑最相关测试。
   - 不能跑时说明原因，并指出残留风险。

4. 给出中文 review。
   - 发现问题时，按严重程度排序。
   - 每条问题包含文件/行号、影响、建议修法。
   - 没发现问题也要说明测试覆盖和未验证部分。

## 输出格式

优先输出 findings：

```text
发现：
- [P1] file:line 问题标题
  影响：...
  建议：...

开放问题：
- ...

验证：
- 已运行 ...
- 未运行 ...
```

如果没有发现问题：

```text
没有发现阻塞合并的问题。
验证：...
残留风险：...
```

## 安全边界

- 不要建议忽略失败测试来合并。
- 不要泄露 diff 中的密钥或隐私内容。
- 不要为了显得“review 过”而制造低价值意见。
