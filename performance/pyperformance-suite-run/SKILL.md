---
name: pyperformance-suite-run
description: Use when 正式运行 pyperformance 子集或全量并生成 run.json；单 worker 调试用 pyperformance-worker-run。
---

# pyperformance Suite Run

负责正式 pyperformance 运行。单 benchmark 调试先用 `pyperformance-worker-run`。

## 三类测试边界

- RuntimeTests 是功能测试。
- test_cinderx/lib test 是集成测试。
- pyperformance 是性能测试；正式性能测试前必须说明功能测试和集成测试是否已通过、跳过或仍待验证。

## 使用场景

- L3 相关子集
- L4 full 全量性能验证
- baseline/candidate 正式对照
- 生成 `run.json`

## 规则

- 用 `python -m pyperformance run`。
- 运行前必须读取 `../using-cpython-optimize/references/pyperformance-env-contract.md`，先列出 driver env、`--inherit-environ`、worker env 和 baseline/candidate 差异轴。
- 使用 `--affinity` 前必须读取 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md`，说明它是 CPU 绑核参数；先检查当前可用 CPU，再把用户真实命令中的 affinity 映射到当前环境，不要逐字照抄不可用核号。
- CinderX JIT 口径必须证明真实 worker 启用 JIT：检查 CinderX `.pth`、worker `pyvenv.cfg` / `include-system-site-packages` 或等价 `PYTHONPATH`、worker 内 `import cinderx` / `_cinderx`、`cinderx.__file__`、`cinderx.get_import_error()` 和 `cinderx.is_initialized()`。
- 正式非 debug 命令形态必须包含 `--affinity`、`--warmup`、`-b <benchmark-selector>`（subset 时）、`-o <result.json>` 和 `--inherit-environ`。
- `--affinity` 必须落在当前 `nproc` / `lscpu` / `taskset -pc $$` / 容器 cpuset 显示的可用 CPU 内；高核号不可用时，重分配可用 CPU 并记录原始 affinity -> 实际 affinity。
- `--inherit-environ` 至少覆盖代理、`LD_LIBRARY_PATH`、`PYTHONPATH`、插件开关和 JIT 关键变量。
- 若 `validation-skill-router` deny 了 pyperformance 命令，不要把它当测试失败；先补齐 `pyperformance-env-contract.md` 要求的 worker venv / `.pth` / `--inherit-environ` / JIT 初始化证据，再用 `CPYTHON_OPTIMIZE_HOOK_ACK=1` 前缀重试同一条正式命令。
- 不能在未完成前置证据时提前加 `CPYTHON_OPTIMIZE_HOOK_ACK=1` 绕过 hook；ACK 只表示已经完成环境契约检查。
- 记录 warmup、loops、CPU affinity、容器线、Python、CinderX commit。
- 正式数据关闭 HIR/JIT dump、`--debug-single-value` 和临时诊断变量；这些只用于 L2 调试，不进入正式性能结论。
- subset/full 根据用户范围、受影响用例和已有证据选择；需扩大验证时再参考 `validation-strategy`。
- 可复用示例使用占位符；实际命令和报告记录真实 benchmark、参数与结果路径。

## 命令形态

目标集合正式性能测试：

```bash
<env-vars> <python> -m pyperformance run \
  --affinity=<cpu-list-or-set> \
  --warmup <n> \
  -b <benchmark-selector> \
  --inherit-environ <comma-separated-env-list> \
  -o <result.json>
```

全量性能测试：去掉 `-b <benchmark-selector>`，在用户已要求 full 或预算覆盖时执行；否则按 `validation-strategy` 先明确是否需要扩大范围。

性能对比：

```bash
<python> -m pyperf compare_to <baseline.json> <candidate.json> --table -G
```

## 故障排查 Checklist

- `run.json` 缺失或损坏：先查 stdout/stderr、exit status、输出目录和 pyperformance worker 日志，不要立即重跑全量。
- `--affinity` 核号不存在或被容器 cpuset 限制：按 `pyperformance-affinity-guidance.md` 重映射到可用 CPU；A/B CPU 不足时改串行或询问降级口径。
- 环境变量不生效：先按 `pyperformance-env-contract.md` 检查变量是否只到 driver、未进 `--inherit-environ`，或在 worker/bench_command 子进程中丢失。
- worker 导入 CinderX 或 JIT 初始化失败：回到 `pyperformance-worker-run` 检查 `.pth`、系统 site-packages、`pyvenv.cfg`、`PYTHONPATH`、`--inherit-environ` 和 worker 内 `cinderx.is_initialized()`。
- 结果波动大：检查 CPU 绑核、governor、后台任务、容器资源隔离、warmup/loops 和 baseline/candidate 唯一差异轴。
- 正式运行中发现 debug 变量：丢弃该结果，重新用非 debug 命令运行。

## 反问 Gate

- 全量运行不在用户请求内，且预计显著增加成本时，说明子集方案并询问；已明确要求 full 时不重复确认。
- benchmark、baseline 含义或正式/调试目标查证后仍不明时询问。warmup、loops 沿用可比口径或工具默认值并记录，不要求用户选择内部参数。
- 可用 CPU 不足时默认串行并保持同一实际 affinity；无法满足用户明确固定的口径时再询问。
- 正式运行在命令局部关闭 HIR/JIT dump 和临时诊断变量，保留诊断产物，不为此再次索取授权。
