---
name: browse
preamble-tier: 1
version: 1.1.0
description: |
  面向 QA 测试与真实站点试用的快速无头浏览器。可打开 URL、交互、校验页面状态、
  对比前后差异、截图留证、检查响应式布局与表单上传。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /browse

这是 gstack 的浏览器基础设施 skill，适合“我需要真实浏览器证据，但还不到完整 QA 修复闭环”的场景。

## 核心模式

1. **页面验证**：确认页面是否正确加载、关键文案是否出现、按钮是否可交互。
2. **用户流程测试**：沿着登录、注册、结账、设置等路径逐步执行并验证结果。
3. **视觉证据收集**：截图、带标注截图、对比截图，用于 bug report 或给用户展示。
4. **环境对比**：同一路径下对比不同环境或不同版本页面。
5. **响应式检查**：在手机 / 平板 / 桌面视口下查看布局和交互状态。

## 用户接管

遇到 headless 处理不了的场景时：

- 打开可见 Chrome，把当前页面和上下文交给用户。
- 让用户完成 CAPTCHA、MFA、手动登录等动作。
- 用户说“done”后重新 snapshot，再继续自动化流程。

## Snapshot 与 CSS Inspector

- snapshot 适合读页面结构、元素标签、可交互目标。
- CSS Inspector 用于查看某个元素的样式来源。
- 也支持 live style modification 和 clean screenshot。

## 何时切换到别的 skill

- 需要“测试 -> 修复 -> 再验证”的完整闭环：转 `/qa`
- 只想出报告不改代码：转 `/qa-only`
- 需要真实 Chrome 联机共驾：转 `/connect-chrome`
