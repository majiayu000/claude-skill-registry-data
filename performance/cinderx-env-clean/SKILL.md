---
name: cinderx-env-clean
description: Use when 已证实 CPython/CinderX lab 污染，需要清理错误安装或构建环境。
---

# CinderX Env Clean

只清理被破坏的 CPython/CinderX 实验环境。先由 `cinderx-env-validate` 证明不可复用，再执行清理。

## 清理对象

- 错误 `editable install`、残留 wheel、旧 `cinderx.__file__` 指向。
- 旧 `build 目录`、CMake/Ninja 产物、错版本 generated headers。
- 污染 `venv`、错误 `PYTHONPATH`、坏 `LD_LIBRARY_PATH`。
- 错误 Docker 容器、挂错源码的 bind mount、残留 `pyperformance env`。
- `patchlevel.h`、`SOABI`、解释器微版本不一致造成的错版本头文件。
- AArch64 RuntimeTests 中 `/opt/python314` 构建为共享/PIC Python，导致 `_Python_LIBRARY_RELEASE` 指向 `libpython3.14.so`、`_PyThreadState_GetCurrent@plt`、`TLSDESC` 或 `DetectsThreadStateOffset` 失败。

## 保留对象

默认保留 cache：pip cache、Docker layer、可复用源码 checkout、历史 `run.json` / `speedup.json` / 日志。要删除 cache 必须说明原因。

## 反问 Gate

- 先定位被污染的对象。目标仍不明确，或清理会删除未获授权的源码、历史日志、`run.json`、core、HIR/jit.log 时，询问具体对象。
- 可证明由当前任务生成且可重建的污染项，按已有清理/修复授权处理；不因进入清理阶段重复询问。
- 原因未查明且仍需现场时保留现场，继续只读取证。

## 输出

- 清理前环境指纹
- 清理了什么
- 保留了什么 cache
- 清理后需要调用的 bootstrap 步骤

不要用重新安装掩盖环境漂移；漂移原因要写清楚。
