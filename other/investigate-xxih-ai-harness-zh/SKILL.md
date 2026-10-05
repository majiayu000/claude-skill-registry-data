---
name: investigate
preamble-tier: 4
version: 1.0.0
description: |
  系统化 root-cause debugging。遵守“没有调查就没有修复”的铁律，
  先锁范围、看模式、测假设，再实现修复与验证。 (gstack)
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

# /investigate

`/investigate` 是 gstack 的排障铁律：**没有调查，就没有修复。**

## Iron Law

- 不允许先拍脑袋改代码，再事后编造原因。
- 必须先定位根因，再进入实现。

## 核心流程

1. `Phase 1: Root Cause Investigation`
   - 复现问题
   - 追踪数据流 / 调用链
   - 读日志、错误、相关文件
2. `Prior Learnings`
   - 查历史 learnings，看是不是重复问题
3. `Scope Lock`
   - 把调查范围锁到相关模块，避免“顺手修别处”
4. `Phase 2: Pattern Analysis`
   - 看这是个单点 bug、系统性模式、还是已知架构味道
5. `Phase 3: Hypothesis Testing`
   - 列假设
   - 一个个证伪 / 证实
6. `Phase 4: Implementation`
   - 只有在根因足够明确后才开始修
7. `Phase 5: Verification & Report`
   - 证明修复有效，写清证据
8. `Capture Learnings`
   - 把这次调查的可复用洞察沉淀下来

## 关键规则

- 连续 3 次失败修复后要停下来，重新诊断，不许继续乱试。
- 没有验证证据，就不能宣布完成。
