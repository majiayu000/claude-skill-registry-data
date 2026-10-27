---
name: hccl-env-check
description: 触发：在 HCCL 算子开发、构建或测试前，需要只读检查 HCCL/HCOMM 仓库、CANN 路径和环境变量是否满足调用方约束时使用；只读输出 READY/NOT_READY、检查证据和缺项。
---

# HCCL 环境检查

对调用方提供的 HCCL、HCOMM 和 CANN 环境执行只读检查，输出可追溯的 `READY` 或 `NOT_READY` 技术结果。

## 能力边界

- 只检查路径、仓库结构、环境脚本和路径一致性，不 clone、pull、下载、安装或覆盖文件。
- 输出实际路径、逐项检查结果与证据，不修改被检查环境。
- 缺项时返回实际值、失败检查和最小修复条件。

## 输入

要求调用方提供或预先加载：

- `HCCL_ROOT`
- `HCOMM_CODE_HOME`
- `HCOMM_DOCS`
- `CANN_HOME`
- `ASCEND_HOME_PATH`
- 可选的 workspace 约束：检查 CANN 是否位于调用方指定 workspace 的 `Ascend/cann-*` 下。该约束为非阻塞项，默认检查，不通过时按 `WARNING` 告警，不影响 `READY` 判定。

变量未设置时记录为缺项，不猜测家目录或系统级 CANN。

## 检查项

### HCCL

```bash
test -d "${HCCL_ROOT}/.git"
test -d "${HCCL_ROOT}/src/ops"
test -f "${HCCL_ROOT}/build.sh"
git -C "${HCCL_ROOT}" branch --show-current
git -C "${HCCL_ROOT}" rev-parse HEAD
```

记录具名分支、HEAD 和工作区状态。detached HEAD 不是路径缺失，但必须在结果中明确标记。

### HCOMM 文档

```bash
test -d "${HCOMM_DOCS}"
test -d "${HCOMM_DOCS}/comm_op_dev_guide"
test -d "${HCOMM_DOCS}/api_ref/comm_opdev"
```

若当前 HCOMM 版本采用不同文档布局，记录实际版本和候选路径，不把猜测写成通过。

### CANN

```bash
test -d "${CANN_HOME}"
test -r "${CANN_HOME}/set_env.sh"
test -d "${ASCEND_HOME_PATH}"
```

启用 workspace 约束时，使用解析后的绝对路径比较 `${CANN_HOME}` 是否位于 `<workspace>/Ascend/cann-*`，不要用未转义的正则拼接路径。该检查为非阻塞项，不通过时输出 `WARNING`，不导致整体 `NOT_READY`。

## 输出契约

结果至少包含：

- `status: READY|NOT_READY`
- 检查时间、主机和 workspace 约束
- 五个输入变量的解析后路径（含 `HCOMM_CODE_HOME`）
- HCCL 分支、HEAD、工作区状态
- 每项检查的命令、退出码和失败原因
- 未检查项及原因

只有所有当前任务必需项通过时才输出 `READY`。该结果只证明环境前置条件，不代表构建、Checker、Review 或整个任务通过。

## 常见修复方向

- 变量或仓库缺失：由调用方在取得所需授权后执行环境准备能力。
- CANN 不满足 workspace 约束：加载目标 workspace 生成的环境文件，不混用系统安装。
- HCOMM 文档布局不匹配：核对当前仓版本和真实目录，再更新检查输入或环境；不自动 `git pull`。
