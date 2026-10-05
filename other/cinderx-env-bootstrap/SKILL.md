---
name: cinderx-env-bootstrap
description: Use when 新建或重建 CPython/CinderX lab，准备 Docker 双线、依赖和 smoke。
---

# CinderX Env Bootstrap

负责从零或清理后建立 CPython/CinderX lab。远端 SSH/tmux/rsync 由 `cinderx-remote-lab-ops` 提供。

## 目标形态

- `cinderx-test`：CinderX 功能验证、HIR dump、crash 复现、调试。
- `cpython-baseline`：stock CPython / CPython JIT 与 CinderX 正式对照。
- CinderX editable install：`python -m pip install -e . --no-build-isolation --no-deps --force-reinstall`。
- pyperformance：固定源码、依赖和 worker 环境。
- pip mirror/cache：优先镜像源和已有缓存，不无限等待在线安装。
- 容器排障工具：按 `../using-cpython-optimize/references/container-tooling-guidance.md` 准备或补装 `gdb`、`ripgrep` / `rg`、`strace`、`perf`、`binutils` 等关键工具；缺工具时先探测网络和 cache，不要直接绕开取证路径。
- CPython baseline 源码：优先复用已验证的本地 clone、worktree、tarball/cache 或已有容器源码；远端下载是最后选项。
- AArch64 RuntimeTests / JIT TLS：`/opt/python314` 必须使用非共享 libpython 形态构建，避免 `_PyThreadState_GetCurrent` 经 PLT 或 TLSDESC 动态 TLS 序列导致 `DetectsThreadStateOffset` 失败。

## AArch64 TLS 约束

构建 RuntimeTests 可用的 Python 时，不要为了通用嵌入场景构建共享 libpython。CinderX AArch64 TLS offset 探测当前依赖 `_PyThreadState_GetCurrent` 的固定 TLS offset 指令形态；共享/PIC Python 可能让 CMake 的 `Python::Python` 指向 `libpython3.14.so`，或让真实函数体变成 TLSDESC 动态 TLS，最终使 `tstate_offset = -1`。

bootstrap 完成后必须自检：

- `sysconfig.get_config_var("Py_ENABLE_SHARED")` 不是 `1`。
- `/opt/python314/lib` 下不存在 `libpython3.14*.so*`。
- RuntimeTests 相关 CMake 输出不应把 `_Python_LIBRARY_RELEASE` 解析到 `libpython3.14.so`。

## 本地来源优先

外部网络不佳时，不要因为当前本地 CPython checkout 不是 3.14.3 就直接下载源码。先让 `cinderx-env-validate` 检查是否能安全切换：

- 本地 clone 有 3.14.3 tag/branch/ref：用独立 worktree 或专用目录切换。
- 已有 tarball/cache：校验 hash/来源记录和 `Include/patchlevel.h` 后解压到专用目录。
- 已有容器内源码：校验容器线、`patchlevel.h`、目标解释器和 include 路径后复用。
- 本地来源不可用时，在环境准备授权和网络限制内按需 fetch/download；远端下载仍是最后选项。

## 反问 Gate

- host、目标源码或 Python 口径查证后仍无法确定时，询问实验目标。
- 用户已要求准备环境时，可在隔离目录复用本地来源、创建 worktree、按需 fetch 或安装依赖；不覆盖当前 checkout。
- 网络异常先按 `cinderx-remote-lab-ops` 诊断并复用现成 cache。需改变已指定镜像源、扩大成本或覆盖已有产物时才询问。
- 已证明会影响其他任务或删除用户数据的重建，先列明具体对象并取得相应授权。

## 内置资源

- `templates/cpython-baseline/Dockerfile`
- `templates/cpython-baseline/docker-compose.yml`
- `templates/cinderx-test/docker-compose.yml`
- `scripts/setup.sh`
- `scripts/smoke.sh`

## 完成条件

bootstrap 后必须调用 `cinderx-env-validate` 和 `cinderx-smoke-check`，返回可复用环境句柄：host、workspace、container line、Python、CinderX commit、pyperformance 路径。
