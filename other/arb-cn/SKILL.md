---
name: arb-cn
description: >-
  Reviews architecture proposals, ADRs, 设计文档, or architecture changes as an
  Architecture Review Board (ARB). Use when the user invokes $arb-cn, or asks
  for ARB 评审, 架构评审委员会评审, or architecture decision review. 评审准则待定；不自拟政策，
  也不给出通过/否决结论。
disable-model-invocation: true
license: Apache-2.0
compatibility: Requires repository file read/write access.
metadata:
  language: zh-CN
  translation_of: arb
  version: "0.1.0"
---

# 架构评审委员会（ARB）

对指定的架构方案、ADR、设计文档或架构变更，以 Architecture Review Board 身份评审。

仅在用户点名 `$arb-cn` 或本技能时启动。

## 工作准则

歧义仅问改查证路径者；已述/已决不重问；可自证则推进；须裁断则一次一问。

## 现状

评审准则、结论档位与结论模板尚未写入。先陈述评审对象与已掌握证据，然后停止。
自拟 ARB 政策、打分或替代评审框架超出本技能范围。

被调用时：

1. 从用户请求与仓库证据中确认评审对象。
2. 对象或证据边界缺失且会改变评审路径时，只问一个阻塞问题。
3. 陈述对象、已掌握证据，并说明准则待定后停止。

## 完成条件

对象已确认、可用证据已列出、准则待定已报告，即完成。通过/否决结论须等准则写入本技能后再给。
