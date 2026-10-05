---
name: qa
preamble-tier: 4
version: 2.0.0
description: |
  系统化 QA 测试并修复发现的问题。先测试，再按 bug 逐个修、逐个重新验证，
  并为每个修复补回归测试。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /qa

`/qa` 是 gstack 的“测试 -> 修复 -> 再验证”闭环。

## 模式

- `Diff-aware`
- `Full`
- `Quick`
- `Regression`

## 核心流程

1. setup：浏览器与测试基础设施检查。
2. 若仓库没有测试框架，可执行 `Test Framework Bootstrap`。
3. 建立 QA baseline：
   - 初始化
   - 鉴权
   - 定向浏览
   - 探索
   - 记录
   - 收尾
4. 计算 health score。
5. `Triage`
6. `Fix Loop`
   - 定位源码
   - 修复
   - 提交
   - 复测
   - 分类
   - 补 regression test
7. `Final QA`
8. `Report`
9. `TODOS.md Update`

## 关键规则

- 每个 bug 修复都要重新验证。
- 修复应尽量原子化，方便回滚和归因。
- `qa` 不只是发现问题，还默认尝试把高价值问题解决掉。
