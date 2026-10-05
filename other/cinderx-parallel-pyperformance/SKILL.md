---
name: cinderx-parallel-pyperformance
description: Use when 在 ARM64/Linux 大核主机按 NUMA/L3 隔离并行运行 CinderX pyperformance 或生成 dry-run 计划。
---

# CinderX Parallel Pyperformance

## 定位

把 CinderX pyperformance 全量或子集从单进程长跑改成可审计的并行验证流程。这个 skill 关注执行效率和环境正确性，不把繁忙机器上的数据自动解释成正式性能结论。

与 `pyperformance-suite-run` 的关系：

- 需要普通单条正式 `python -m pyperformance run` 时，优先用 `pyperformance-suite-run`。
- 需要在大核机器上拆队列并行跑多个 benchmark、避免 NUMA/L3/SMT 踩踏时，用本 skill。
- 调试单个 benchmark worker 环境时，回到 `pyperformance-worker-run`。

## 必读资源

运行真实任务前读取：

- `references/runbook.md`：8/16 模式策略、blue-server-53 拓扑、代理、venv/JIT proof、稳定性判读。

脚本资源：

- `scripts/parallel_pyperformance.py`：NUMA/L3-aware benchmark scheduler，可 `--dry-run`。
- `scripts/setup_and_run_cinderx_parallel_pyperf.sh`：在远端 Linux 上创建独立 `opt-venv`、安装 CinderX wheel、注入 pyperformance worker，并调用调度器。

## 核心约束

只支持两种正式并行模式：8 lane 和 16 lane。

- `--mode auto`：优先 16 lane；如果无法在有本地内存的 NUMA node 上分配出 16 个互不共享 L3 的 lane，则降到 8 lane。
- `--mode 8`：使用 8 个主 lane。
- `--mode 16`：必须真的满足 16 个主 lane；如果会使用无本地内存 NUMA、SMT sibling 或跨 lane L3 重叠，停止并报告原因。

不要为了凑核数使用没有本地内存的 NUMA CPU。不要把 L3 重叠当成默认可接受的正式口径；只有用户明确要求探索性超分时，才另写或修改调度参数，并在结论里标成非正式。

## 标准流程

1. 确认环境和输入。
   - 远端主机、目标 Python、CinderX wheel、runroot、benchmark subset 或 full。
   - 目标是否只是 dry-run、稳定性两跑、还是正式 baseline/candidate。
   - 机器是否正在被其他任务占用；占用时只输出趋势或验证观察。

2. 证明 CinderX 进了 manager 和 worker。
   - 使用独立 `opt-venv`。
   - `opt-venv` 安装 `pyperformance` 和目标 CinderX wheel。
   - pyperformance worker venv 也安装同一个 CinderX wheel，且 benchmark 过程中通过 `PYTHONPATH` + `sitecustomize.py` 让派生 worker venv 也能导入 `_cinderx_auto`。
   - 记录 manager/worker probe：`frame_evaluator=True`、`compile_after=2`、toy function compiled。

3. 先 dry-run 调度计划。
   - 打印每个 lane 的 CPU、membind node、benchmark 队列、尾部轨道、峰值活跃物理核。
   - 如果 53 自动选择 8 lane，这是预期行为：node1/node3 没有本地内存，不能拿来凑 16。

4. 再运行真实测试。
   - 从独立 `pyperf-work` 目录运行，避免误用当前工作目录下旧 worker venv。
   - 继承 `CINDERX_PLUGIN_ENABLE,PYTHONJITAUTO,AUTO_JIT,PYTHONJITLIGHTWEIGHTFRAME,PYTHONPATH,LD_LIBRARY_PATH`。
   - 保持 `PYTHONJITAUTO=2`、`AUTO_JIT=2`、`--warmup 3`，除非用户给出不同口径。

5. 输出结论。
   - 给出 runroot、result JSON、compare log、模式、CPU/lane 证据、JIT proof 摘要。
   - 对繁忙机器上的波动保持保守：优先说“稳定性观察/环境验证”，不要说“正式回归结论”。

## 常用命令

只看计划：

```bash
PYTHON=/path/to/opt-venv/bin/python \
  python3 scripts/parallel_pyperformance.py \
    --profile auto --mode auto --dry-run --plan
```

远端完整准备并跑两次稳定性：

```bash
CPY=/path/to/python3.14 \
CINDERX_WHEEL=/path/to/cinderx.whl \
RUNROOT=/home/guo/codex-work/parallel-pyperf-$(date +%Y%m%d-%H%M%S) \
MODE=auto PROFILE=auto REPEAT=2 \
REMOTE_PROXY=http://127.0.0.1:17890 \
  bash scripts/setup_and_run_cinderx_parallel_pyperf.sh
```

子集 dry-run：

```bash
PYTHON=/path/to/opt-venv/bin/python \
  python3 scripts/parallel_pyperformance.py \
    --mode 8 --benchmarks richards,go,raytrace \
    --dry-run
```

## 失败时先查

- worker probe 没有 `frame_evaluator=True`：先修 wheel 注入和 `PYTHONPATH`，不要继续解释性能。
- pyperformance 又创建了新的 `*-bm-*` worker venv：确认 `PYTHONPATH` 继承了 runroot 下 `cinderx-startup` 和 `opt-venv` site-packages。
- pip 代理变量无效：远端临时写入 scoped `pip.conf`，跑完恢复。
- 16 lane 分配失败：这是保护，不是脚本坏；换 8 lane 或换有足够 memory-backed L3 lane 的机器。
- compare 波动大：记录后台负载，重复运行或换安静窗口；不要只按 mean 下结论。
