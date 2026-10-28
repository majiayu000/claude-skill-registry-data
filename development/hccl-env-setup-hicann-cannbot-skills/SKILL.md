---
name: hccl-env-setup
description: 触发：本机缺少可用的 HCCL 开发环境，需要 clone 仓库、探测或安装 CANN Toolkit+950 ops、生成环境变量文件时使用。
---

# HCCL 环境准备

负责 HCCL 开发环境一键准备：clone hccl/hcomm 仓库 + 探测或安装 CANN + 生成 `hccl-env.sh`。

clone、下载和安装会改变外部环境；调用方必须在执行相应模式前确认目标路径和授权。探测模式也可能 clone 缺失仓库，不是纯只读操作。

## 输入

- `WORKSPACE`（必选）：工作目录，`hccl` 仓、`hcomm` 仓、`Ascend` 安装目录均在此目录下。通过 `--workspace <path>` 参数或 `WORKSPACE` 环境变量传入；未提供时脚本报错退出。工作目录的布局约定由上层应用插件定义，本 Skill 不做假设。

## 前置依赖

- Python >= 3.7.0、pip3 >= 20.3.0
- gcc & g++ : 7.3.0 至 13.3.x
- cmake >= 3.16.0
- curl、wget（用于下载 CANN 包）

## 工作流程

### Step 1. 探测模式

```bash
bash communication/hccl-env-setup/scripts/setup-env.sh --workspace <WORKSPACE>
```

脚本完成：
- ★ 检查前置依赖（curl/wget/python3/pip3/gcc/g++/cmake），缺失则输出安装命令并退出（所有模式均执行，不区分探测/安装）
- 读取 `WORKSPACE`（由 `--workspace` 参数或 `WORKSPACE` 环境变量传入）
- clone 缺失的 hccl/hcomm 仓库；已存在时只输出 `EXISTS:hccl:<path>` / `EXISTS:hcomm:<path>`，不自动 `git pull`
- **仅探测 `$WORKSPACE/Ascend/cann-*`**（不扫描系统其他位置的 CANN）
- 找到 → 生成 `hccl-env.sh`，输出 `STATUS:CANN_FOUND`
- 找不到 → 输出 `STATUS:CANN_NOT_FOUND`

### Step 2. 根据探测结果决策

读取 `RESULT_START...RESULT_END` 块中的 `STATUS`：

- **`CANN_FOUND`** → 直接跳到 Step 4（加载环境变量），`source` 脚本已生成的 `hccl-env.sh`（不询问是否重装；如需升级由用户显式执行 `setup-env.sh --install`）
- **`CANN_NOT_FOUND`** → 执行 Step 3（安装模式）

### Step 3. 安装模式

安装模式会访问下载站、写入 `$WORKSPACE/Ascend` 并下载较大安装包。只有调用方已明确授权这些动作时执行。

```bash
bash communication/hccl-env-setup/scripts/setup-env.sh --install --workspace <WORKSPACE>
```

脚本完成：
- 抓取下载站最新日期目录
- 根据系统架构（`uname -m`）下载 toolkit 包 + 950 系列 ops 包
- `--quiet` 静默安装到 `$WORKSPACE/Ascend`
- 生成 `hccl-env.sh`，输出 `STATUS:CANN_INSTALLED`

下载地址：`https://ascend.devcloud.huaweicloud.com/artifactory/cann-run-mirror/software/master/`，此目录下可能包含多个日期目录。进入最新日期目录后，下载 `Ascend-cann-toolkit_<ver>_linux-${ARCH}.run` + `Ascend-cann-950-ops_<ver>_linux-${ARCH}.run`。如若没找到950 ops包，则刷新重新找一次。

安装命令（脚本内部执行）：
```bash
./Ascend-cann-toolkit_<ver>_linux-${ARCH}.run --full --quiet --install-path=${WORKSPACE}/Ascend
./Ascend-cann-950-ops_<ver>_linux-${ARCH}.run --install --quiet --install-path=${WORKSPACE}/Ascend
```

### Step 4. 加载环境变量

```bash
source ${WORKSPACE}/hccl-env.sh
```

环境变量包含：`unset ASCEND_OPP_PATH ASCEND_TOOLKIT_HOME ASCEND_AICPU_PATH`（清除系统 CANN 残留变量，防止 `build.sh` fallback 到 `/usr/local/Ascend`）+ `HCCL_ROOT`、`HCOMM_CODE_HOME`、`HCOMM_DOCS`、`CANN_HOME`、`ASCEND_HOME_PATH` + `source ${CANN_HOME}/set_env.sh`。

## 技术结果

`hccl-env.sh` 已生成，`HCCL_ROOT`、`HCOMM_CODE_HOME`、`HCOMM_DOCS`、`CANN_HOME`、`ASCEND_HOME_PATH` 已设置。

该结果只表示环境文件生成成功；使用前仍需按当前任务要求检查仓库结构、CANN 路径及环境变量一致性。
