---
name: cinderx-fast-validation
description: Use when CinderX release 构建或 gate 重复编译缓慢，需要用 ccache 复用构建。
---

# CinderX Fast Validation

用 repo 外部的 `ccache` compiler wrapper 加速重复的 CinderX release / wheel / gate 验证。目标是缩短调试循环，不改变 CinderX 源码树、不把缓存配置写进项目文件。

## 适用场景

- `ci_pipeline/run_gate.py --suite cinderx_local`
- `ci_pipeline/run_gate.py pr --coverage` 中的 `cinderx_local.setup_release`
- `test_cinderx_release`、`setup.py bdist_wheel`、`python -m build --wheel`
- pyperformance candidate wheel 反复构建

不默认用于 `runtime_tests` 或无关 CMake 构建；这些路径可能有独立的 build dir、测试数据路径或环境约束。

## 核心规则

先安装或刷新外部 prelude，再显式 source 它。prelude 只在以下条件之一满足时启用 compiler wrapper：

```bash
CINDERX_INCLUDE_TEST_PACKAGE_DATA=1  # cinderx_local.setup_release
CINDERX_CCACHE_FORCE=1               # 手动 wheel build 显式 opt-in
```

如果没有这些信号，prelude 应保持 inert，避免污染其它验证任务。

## 安装 Prelude

在目标机器或容器中运行 bundled script：

```bash
bash skills/cinderx-fast-validation/scripts/install-ccache-prelude.sh
```

默认写入：

```text
$HOME/cinderx-setup-release-ccache-prelude.sh
```

需要固定路径时：

```bash
CINDERX_CCACHE_PRELUDE_PATH=/opt/cinderx-setup-release-ccache-prelude.sh \
  bash skills/cinderx-fast-validation/scripts/install-ccache-prelude.sh
```

`ccache` 不存在时脚本不会失败；prelude 会保持 inert。正式使用前应通过系统包管理器或容器模板安装 `ccache`。

## Gate 用法

把 prelude 传给 gate，让它只在 `setup_release` job 的环境变量出现时生效：

```bash
python ci_pipeline/run_gate.py \
  --suite cinderx_local \
  --prelude "source $HOME/cinderx-setup-release-ccache-prelude.sh"
```

PR gate 也可以使用同一个 prelude，因为 prelude 会自我门控：

```bash
python ci_pipeline/run_gate.py \
  pr --coverage \
  --prelude "source $HOME/cinderx-setup-release-ccache-prelude.sh"
```

## 手动 Wheel 构建

手动构建必须显式 opt-in：

```bash
export CINDERX_CCACHE_FORCE=1
export CINDERX_CCACHE_BASEDIR="$PWD"
export CINDERX_CCACHE_DIR="${CINDERX_CCACHE_DIR:-$HOME/.cache/ccache-cinderx}"
source "$HOME/cinderx-setup-release-ccache-prelude.sh"

python setup.py bdist_wheel -d "$WHEELHOUSE"
```

如果已有 build dir 是用真实 compiler 配置的，首次切到 wrapper compiler 时可能需要清理对应 CMake build dir，让 `CMakeCache.txt` 重新生成。

## 验证收益

围绕两次重复构建检查 `ccache` stats：

```bash
CCACHE_DIR="$HOME/.cache/ccache-cinderx" ccache -z

export CINDERX_CCACHE_FORCE=1
export CINDERX_CCACHE_BASEDIR="$PWD"
source "$HOME/cinderx-setup-release-ccache-prelude.sh"
python setup.py bdist_wheel -d "$WHEELHOUSE"

CCACHE_DIR="$HOME/.cache/ccache-cinderx" ccache -s
```

期望 warm build 出现 direct hits；如果命中数一直为零，先检查 `ccache` 是否存在、prelude 是否被 source、`CINDERX_CCACHE_FORCE=1` 或 `CINDERX_INCLUDE_TEST_PACKAGE_DATA=1` 是否生效，以及 `CC/CXX` 是否指向 wrapper。

## 失败信号

- `ccache -s` 始终为零：prelude 没启用、`ccache` 不在 PATH、或 CMake 仍使用真实 compiler。
- `runtime_tests` 行为变化：停止使用该 prelude，检查是否误设置了 `CINDERX_CCACHE_FORCE=1`。
- 切换 wrapper 后 CMake 重新 configure 并丢失变量：清理对应 build dir 后重跑一次。
- warm build 仍大量 miss：检查 compiler 版本、源码路径、`CCACHE_BASEDIR`、生成路径和 build dir 是否频繁变化。
