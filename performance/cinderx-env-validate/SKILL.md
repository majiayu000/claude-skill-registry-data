---
name: cinderx-env-validate
description: Use when 校验 CPython/CinderX lab 的版本、ABI、源码和 worker 环境是否可复用。
---

# CinderX Env Validate

可由主 Agent 或 `cinderx-environment-verifier` 执行。环境三态为 `reusable`、`needs_bootstrap` 或 `needs_clean_bootstrap`。

## 版本事实源

目标 Python 版本固定为 `Python 3.14.3`。环境校验必须以目标解释器、容器内头文件和 `patchlevel.h` 为事实源，不能把更高 patchlevel 才有的 C API 当成可用能力。

当前 checkout 不是事实源本身。比如本地 CPython 仓当前显示 `3.16.0a0`，只能说明当前工作树不符合目标版本，不能直接判定本地 CPython 仓整体不可信，也不能立刻改走远端下载。先尝试安全切换到本地已有的 3.14.3 可信来源。

## Baseline Source 门禁

涉及 A/B baseline 时，先读取 `../using-cpython-optimize/references/baseline-source-contract.md`。远程 SSH、tmux、Docker 容器或 pyperformance 可运行，只能证明执行环境可用，不能自动证明远程 workspace 当前源码可作为 baseline。

baseline 必须单独校验：

- 口径 baseline 与提交 baseline：例如 CPython 解释执行、CPython JIT、CinderX JIT，以及 baseline commit/ref。
- 源码来源：用户指定的 baseline commit/ref、CPython 3.14.3 release source、干净 git worktree、可信 tarball/cache，或 `cpython-baseline` 容器 bind mount 指向的明确源码。
- 仓库状态：`git status --short`、`git show -s --format=%H`、`git describe --tags --always --dirty`。
- 版本证据：`patchlevel.h`、`SOABI`、目标解释器和 include 路径。
- 污染检查：baseline 不能误继承 candidate editable install、CinderX `.pth`、`PYTHONPATH`、JIT hook 或 `CINDERX_*`。

若远程源码 dirty、ref 不明、版本不符、bind mount 指向不明或混入 candidate 污染，返回 `baseline_source_untrusted`，先查证来源；目标 ref 已知时可创建独立干净 worktree 并复验，只有 baseline 含义仍不明确时才询问。验证通过前不能把该源码交给 A/B runner。

## 本地 CPython 仓安全切换

当用户给出 `/opt/Codex/cpython`、`CPYTHON_ROOT` 或其它本地 CPython clone 时，按顺序检查：

- 仓库身份：`git remote -v`、`git show -s --format=%H`、`git describe --tags --always --dirty`。
- 污染风险：`git status --short`；有未提交改动时不能直接 `git checkout`。
- 本地 3.14.3 来源：本地 tag、branch、ref、现有 worktree、tarball/cache 或已有容器中的源码。
- 版本证据：`Include/patchlevel.h`、目标解释器 `sys.version`、`SOABI` 和 include 路径。

安全切换规则：

- 优先用 `git worktree add <dedicated-dir> <3.14.3-ref>` 或专用目录，不污染用户当前 checkout。
- 只有在专用目录或明确授权的干净仓库中，才能切换 ref。
- 切换后必须重新读取 `Include/patchlevel.h` 并运行目标解释器校验；通过后才可作为 baseline 事实源。
- 已授权环境准备时可按需 fetch 缺少的目标 ref；仅在无法隔离 dirty 状态、需覆盖已有产物或违反网络限制时询问。
- 外部网络不佳时，优先复用本地 clone、worktree、tarball/cache 和已有容器；远端下载/extract Python-3.14.3 只作为最后选项。

## 按实验需要校验

- Python：目标解释器路径、`Python 3.14.3`、`SOABI`、include 路径、`patchlevel.h`。
- A/B 实验的 baseline source：按 `baseline-source-contract.md` 校验口径 baseline、提交 baseline、source path、commit/ref、dirty 状态和唯一差异轴。
- AArch64 RuntimeTests TLS：检查 `Py_ENABLE_SHARED`、`CONFIG_ARGS`、`LIBDIR`、`LIBRARY`、`LDLIBRARY` 和 CMake `_Python_LIBRARY_RELEASE`；若解析到 `libpython3.14.so`、出现 `_PyThreadState_GetCurrent@plt`、`TLSDESC`、`DetectsThreadStateOffset` 失败或 `tstate_offset = -1`，判定为环境形态不满足 CinderX AArch64 TLS offset 探测，不要继续用该环境跑 RuntimeTests。
- CinderX：commit、branch、`cinderx.__file__`、`cinderx.is_initialized()`、`cinderx.get_import_error()`、`_cinderx`。
- 运行 pyperformance 时：路径、`pyperformance 1.13.0`、benchmark 源码和 worker 能否继承环境。
- toolchain：GCC、libstdc++、openEuler / 宿主发行版、Docker 可用性。
- 使用 Docker 双线时：`cinderx-test` 与 `cpython-baseline` 是否存在且 bind mount 指向正确源码。
- JIT flags：`PYTHONJITAUTO`、`PYTHONJITHUGEPAGES`、HIR/JIT dump 变量是否污染正式跑分。

## 判定

- `reusable`：依赖齐全、版本符合、smoke 通过，能直接交给 runner；若涉及 A/B，还必须有 `baseline_source_verified`。
- `needs_bootstrap`：目标目录或容器不存在，需要初始化。
- `needs_clean_bootstrap`：存在但版本漂移、错误 editable install、错版本头文件、CinderX 导入异常，或 AArch64 RuntimeTests 发现共享/PIC/TLSDESC Python 形态导致 TLS offset 探测不可用。
- `baseline_source_untrusted`：执行环境可用但 baseline 源码事实源缺失或不可信；不能进入正式 A/B。

输出必须带环境指纹和失败项，不能只写“环境正常”。
