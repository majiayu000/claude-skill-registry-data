---
name: pyperformance-result-compare
description: Use when 比较已有 pyperformance run.json 或 speedup.json，判断收益、回归与噪声；不启动跑分。
---

# pyperformance Result Compare

负责解释结果，不负责跑 benchmark。

## 输入

- baseline `run.json`
- candidate `run.json`
- `speedup.json`
- 提交 baseline / candidate commit
- 口径 baseline：CPython JIT、CinderX JIT、解释执行等

## 判断

- 命令口径是否一致
- 按 `../using-cpython-optimize/references/baseline-source-contract.md` 核对 baseline source 是否 `baseline_source_verified`，包括口径 baseline、提交 baseline、source path、commit/ref、dirty 状态、`patchlevel.h`、`SOABI` 和容器 bind mount。
- 按 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md` 核对 baseline/candidate 的原始/实际 `--affinity`、可用 CPU 映射和并行/串行口径是否一致。
- 先按 `../using-cpython-optimize/references/pyperformance-env-contract.md` 核对 baseline/candidate 的 `--inherit-environ`、driver/worker env 和唯一差异轴。
- CinderX JIT 口径必须核对 worker 内证据：`.pth`、`pyvenv.cfg` / `include-system-site-packages`、`import cinderx` / `_cinderx`、`cinderx.__file__`、`cinderx.get_import_error()`、`cinderx.is_initialized()`。
- baseline/candidate 是否只在目标变量上不同
- 方差、噪声和异常值
- 收益范围、无收益范围、未验证范围
- 需要回到 `pyperformance-worker-run` 的异常用例
- 如果 baseline source、affinity 口径、环境契约、worker JIT 证据缺失或 baseline/candidate 不一致，先降级结论，不把 `run.json` 写成可信性能收益。

## 反问 Gate

- 无法确定 baseline/candidate 配对或比较含义时，询问缺失事实；不凭文件名猜测实验轴。
- baseline source、worker 或 affinity 证据缺失时照实报告受限观察与补证要求，不把它当可信收益。
- 不稳定数据直接标为噪声或证据不足。已有数据分析不启动远程补跑；只有用户要求补测或扩大收益声明时，按已有授权与预算决定运行范围。
