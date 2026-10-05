---
name: workflow-feature-driven-optimization
description: Use when 实施已知 CPython/CinderX 性能优化，完成代码、功能测试和收益验证。
---

# Feature Driven Optimization Workflow

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| 功能/集成测试 | `cinderx-jit-analyst` / orchestrator | `cpython-runtime-test-run`、`cinderx-smoke-check` |
| JIT/路径分析 | `cinderx-jit-analyst` | `cinderx-jit-entry-check`、`cinderx-hir-lir-analyze` |
| 性能验证 | `pyperformance-candidate-runner` | `pyperformance-worker-run` / `pyperformance-suite-run` |
| 结果分析 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| 报告 | `pyperformance-benchmark-analyst` | `cinderx-optimization-report` |

## TDD 要求

修改代码前先做测试缺口判断：

- 对行为变化检查是否需补充或修改 RuntimeTests 功能用例，覆盖具体语义或层级契约。
- 跨层 Python 行为变化检查 test_cinderx/lib test 集成用例；复用已有有效覆盖，纯文档或注释改动不另加镜像测试。
- 新增或修改的功能用例必须使用 Python `unittest` 框架，不能改成 pytest 风格或只写脚本式断言。
- 功能用例和集成用例先于性能验证；没有对应行为覆盖时，不能只靠 pyperformance 收益证明特性正确。

## Gate

先功能后性能。L1 功能/集成测试未通过时，不讨论性能收益；目标 benchmark 无收益时，先解释假设失败原因。
