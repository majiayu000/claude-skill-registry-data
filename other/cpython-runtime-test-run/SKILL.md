---
name: cpython-runtime-test-run
description: Use when 运行或重跑 CinderX RuntimeTests 功能测试、test_cinderx/lib test 集成测试。
---

# CPython Runtime Test Run

负责 RuntimeTests 功能测试和 test_cinderx/lib test 集成测试，不负责 pyperformance 性能测试。

## 三类测试用语

- RuntimeTests = 功能测试。
- test_cinderx/lib test = 集成测试。
- pyperformance = 性能测试，交给 `pyperformance-worker-run` 或 `pyperformance-suite-run`。

## 验证等级

- L1 smoke：`import cinderx`、最小 JIT、目标单元测试、目标功能测试。
- L3 相关子集：受影响 RuntimeTests 功能测试、test_cinderx/lib test 集成测试、失败用例集合。
- L4 全量：近千条 CPython Runtime / CinderX 聚合测试，按明确请求或广泛行为风险选择。

## 命令形态

- RuntimeTests 功能测试：`$CINDERX_TEST_PYTHON ci_pipeline/run_gate.py --suite runtime [--coverage]`。
- test_cinderx/lib test 集成测试：`CINDERX_LOCAL_RUN_LIBTEST=1 $CINDERX_TEST_PYTHON ci_pipeline/run_gate.py --suite cinderx_local`。
- 只跑受影响集合时，保留同一解释器、同一容器线、同一 JIT flags，并记录裁剪理由。

## 规则

- L1 未过，不讨论性能收益。
- 失败重跑保持可比命令和环境变量，使用新的日志路径并记录 exit status，避免覆盖首次失败证据。
- `SIGSEGV` / `exit 139` 转 `cinderx-gdb-core-triage`。
- AArch64 上出现 `DetectsThreadStateOffset` 失败、`tstate_offset = -1`、`_PyThreadState_GetCurrent@plt` 或 `TLSDESC` 时，先转 `cinderx-env-validate` / `cinderx-env-bootstrap` 检查 `/opt/python314` 是否错误构建为共享/PIC Python；不要先归因到 AutoJIT 新代码。
- 测试前后记录 Python、CinderX commit、容器线和 JIT flags。
- 功能测试或集成测试未通过时，不把 pyperformance 性能测试结果写成可提交结论。

输出测试范围、真实命令、失败列表、晋级理由和下一步。
