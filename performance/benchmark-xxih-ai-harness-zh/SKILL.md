---
name: benchmark
preamble-tier: 1
version: 1.0.0
description: |
  基于 browse daemon 的性能回归检测。建立页面加载时间、Core Web Vitals、
  资源体积的基线，并在 PR 前后做对比。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /benchmark

用于做“现在有多快、改完变快还是变慢了”的性能基线与回归检测。

## 参数与模式

- 默认模式：采集当前页面的性能数据
- `--baseline`：把当前结果保存为基线
- `--diff`：对比基线与当前状态
- `--trend`：看长期趋势

## 核心流程

1. setup：确认 browse 可用。
2. 页面发现：决定要 benchmark 哪些 URL。
3. 数据采集：页面加载时间、Core Web Vitals、资源大小、关键资源时长。
4. baseline capture：把当前结果落盘。
5. comparison：输出前后差异和回归项。
6. slowest resources：找出最慢资源。
7. performance budget：检查是否超预算。
8. trend analysis：如果历史数据存在，展示趋势。
9. save report：保存报告供后续追踪。

## 关键规则

- 性能对比要尽量在同一环境、同一路径下做。
- 只要出现明显回归，就要在报告里点名资源、指标和差值。
- 这是部署和 PR 前的护栏，不只是一次性测速。
