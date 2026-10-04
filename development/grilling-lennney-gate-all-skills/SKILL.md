---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, wants to be grilled, or says "is this ready", "review my plan", "有什么漏洞", "帮我审查一下这个方案".
disable-model-invocation: true
source: mattpocock
trigger: 需要严格审查计划或设计
input: 计划或设计文档
output: 审查反馈
next: 无
dependencies: 无
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.
