---
name: cinderx-jit-entry-check
description: Use when 核实 benchmark 本体是否进入 CinderX JIT，排除启动期和第三方编译干扰。
---

# CinderX JIT Entry Check

先确认 benchmark 本体进入 CinderX JIT，再分析 HIR/LIR 或收益。

## 误判来源

- 启动期函数进入 JIT，但 benchmark 本体没有。
- 第三方包或 import-time 代码触发 compile storm。
- jit.log 有内容，但没有目标 benchmark 函数。
- HIR dump 来自简化命令，不来自真实 worker。

## 检查项

- 真实 worker 命令
- `../using-cpython-optimize/references/pyperformance-env-contract.md` 中的 driver/worker 环境变量传递是否成立
- worker 可见的 CinderX `.pth`、`site-packages` 和 `pyvenv.cfg` / `include-system-site-packages`
- worker 内 `import cinderx`、`import _cinderx`、`cinderx.__file__`、`cinderx.get_import_error()`、`cinderx.is_initialized()`
- jit.log 中目标函数
- HIR 中 benchmark 本体片段
- AutoJIT 阈值和 JIT flags
- `PYTHONJITHUGEPAGES`、`PYTHONJITAUTO` 等平台护栏

输出 `entered_cinderx_jit`、证据片段、排除项和下一步。若 `entered_cinderx_jit=false`、目标热函数不进入 gate 或主要解释执行，下一步转 `cinderx-interpreter-case-analyze`，不要硬套 HIR/LIR 结论。
