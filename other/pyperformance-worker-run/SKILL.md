---
name: pyperformance-worker-run
description: Use when 复现单个 pyperformance worker，或排查 bench_command/sitecustomize 环境继承。
---

# pyperformance Worker Run

负责单 benchmark L2 复现，是 crash、HIR、JIT 分析的真实命令来源。

## 三类测试边界

- RuntimeTests 是功能测试，失败时先回到 `cpython-runtime-test-run`。
- test_cinderx/lib test 是集成测试，失败时不要用 pyperformance 结果遮盖。
- pyperformance 是性能测试；功能测试和集成测试未过时，只能输出调试观察，不能输出可提交性能结论。

## Worker 架构 Checklist

- 先读取 `../using-cpython-optimize/references/pyperformance-env-contract.md`，确认 driver、manager、worker 和 `bench_command()` 子进程看到的环境变量一致。
- 使用真实 `run_benchmark.py --worker`，不要用交互式 import 替代。
- `python -m pyperformance run` 不是单进程执行：先有 driver/manager，再进入 benchmark worker；`bench_command()` 还可能生成下一层子进程。
- `sitecustomize`、`LD_LIBRARY_PATH`、`PYTHONPATH`、插件开关、JIT flags 必须传到真实 worker。
- CinderX worker 必须能看到系统 site-packages：确认 worker venv 的 `pyvenv.cfg` 中 `include-system-site-packages = true`，或用等价 `PYTHONPATH` 把系统 site-packages 放进 worker 环境。
- CinderX `.pth` 必须安装在 worker 可见的 `site-packages`，且指向当前 candidate 的 CinderX；记录 `.pth` 路径和内容摘要。
- 判断 CinderX JIT 是否启用必须在 worker 内取证：`import cinderx`、`import _cinderx`、`cinderx.__file__`、`cinderx.get_import_error()`、`cinderx.is_initialized()`，并和 jit.log/HIR 中的目标 benchmark 本体对应。
- Python baseline 不应误继承 CinderX 安装；如果故意比较 CinderX baseline，必须在口径里写清。
- `--inherit-environ` 至少继承代理、`LD_LIBRARY_PATH`、`PYTHONPATH`、插件开关和 JIT 关键变量。
- `validation-skill-router` 对单 worker 注入环境提醒，不额外要求审批。helper 范围不明或命令还会改写环境时可触发 deny；先核对范围、补齐 worker 证据，再用 `CPYTHON_OPTIMIZE_HOOK_ACK=1` 重试原命令。
- 不能在未完成前置证据时提前加 `CPYTHON_OPTIMIZE_HOOK_ACK=1`；ACK 只表示已经确认真实 worker 环境可用。
- 分析阶段只增减 debug 变量，尽量保持同一真实 worker 命令。

## 快速 L2 命令形态

优先用仓库或容器内已有 bm/test-benchmark 快速脚本做 L2 复现，形态保持抽象：

```bash
BENCHMARK=<benchmark-selector> WARMUP=<n> PYTHONJITAUTO=<threshold> DIAG=0 /scripts/test-benchmark.sh
```

- `DIAG=0` 是非 debug 性能口径；只有 crash、HIR、JIT 日志定位时才切 `DIAG=1`。
- 快速 L2 可用于验证方向、复现异常或生成 worker 命令；正式性能结论仍要回到 `pyperformance-suite-run` 的非 debug 正式命令。
- 可复用示例使用占位符；实验报告记录真实 benchmark、命令和产物路径。

## 故障排查 Checklist

- worker import 成功但 driver 失败：查 pyperformance venv、`pyvenv.cfg`、`include-system-site-packages`、`.pth`、`PYTHONPATH` 和 `--inherit-environ`。
- driver 环境正确但 worker 行为不对：按 `pyperformance-env-contract.md` 对比 driver env、inherit list、worker env 和 helper 变量，先修环境传递再分析性能。
- driver 成功但 benchmark worker 失败：保留 driver 命令、worker 命令、stdout/stderr、exit status，再进入 `cinderx-gdb-core-triage` 或 `cinderx-hir-dump`。
- 性能数据异常慢：先确认 CPU 绑核、`.pth`、worker venv、JIT flags、debug dump、系统 site-packages 和 baseline/candidate 唯一差异轴。
- 非 debug 运行不得混入 HIR/JIT dump、`--debug-single-value` 或临时诊断变量。

## 参考资源

- `references/run-benchmark-worker-realenv.sh`
- `../using-cpython-optimize/references/pyperformance-env-contract.md`
- `scripts/benchmark_harness.py`
- `scripts/test-benchmark.sh`

输出 benchmark、真实 worker 命令、环境变量、`.pth` / `pyvenv.cfg` / `cinderx.is_initialized()` 证据、stdout/stderr、exit status 和产物路径。
