---
name: canary
preamble-tier: 2
version: 1.0.0
description: |
  部署后的金丝雀监控。借助 browse daemon 持续观察线上应用的控制台错误、
  性能回归和页面故障，并定期截图、对比基线。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /canary

这是部署后的“盯盘” skill。目标不是发布，而是确认发布后真实线上表现仍然健康。

## 参数与模式

- 默认：监控给定 URL
- `--baseline`：先为部署前页面建立视觉与状态基线
- `--pages`：指定要监控的页面列表

## 核心流程

1. setup：确认 browse 可用。
2. baseline capture：如有需要，先抓部署前快照。
3. page discovery：如果用户没指定页面，自动发现关键页面。
4. pre-deploy snapshot：没有 baseline 时先补一个参考快照。
5. continuous monitoring loop：持续检查控制台、页面失败、性能异常与视觉变化。
6. health report：汇总当前健康结论。
7. baseline update：如果部署稳定，询问是否把这次结果升格为新基线。

## 关键规则

- `curl` 或 HTTP 健康只是最低门槛，真实页面加载和交互结果更重要。
- 一旦发现线上异常，要明确说明是否建议回滚。
- 监控结果要能服务 `/land-and-deploy` 的最终发布判定。
