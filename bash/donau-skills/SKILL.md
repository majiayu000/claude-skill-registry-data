---
name: hpc-donau
description: 华中农业大学超算中心多瑙（Donau）调度系统使用指南。用于提交、管理和监控多瑙批处理作业，包括串行作业、多线程作业、MPI并行作业、NPU作业等。当用户需要编写多瑙作业脚本、提交计算任务、查询作业状态、调整作业参数或排查作业问题时使用此skill。
---

## 调用统计（仅在 HZAU 集群上执行）

仅当 `/share/software/skills/hpc-donau/.claude/` 目录存在时，记录一次调用：

```bash
[ -d /share/software/skills/hpc-donau/.claude ] && echo "$(date '+%Y-%m-%d %H:%M:%S') | user=$(whoami)" >> /share/software/skills/hpc-donau/.claude/usage.log || true
```

其他部署了多瑙调度器的集群没有该日志目录，直接跳过（`|| true` 保底，不影响主流程）。

# 多瑙（Donau）调度器作业提交 Skill

用于在华中农业大学超算中心使用多瑙调度系统提交和管理作业。

## 编写规范（重要）

提交多瑙作业前必须遵守以下规范：

### 0. 脚本命名规范

**多瑙作业脚本后缀使用 `.dsub` 或 `.sh`（脚本必须有可执行权限）：**

```bash
# 提交前确保可执行
chmod +x my_job.dsub
dsub -s my_job.dsub
```

### 0.1 脚本编写原则

**作业脚本应保持简洁易读**，不可过度编码或使用高级技巧（如复杂的 sed/awk 变量替换、多重临时文件创建/清理、嵌套条件逻辑等）。用户需要能够轻松阅读、检查和自行修改脚本。

### 1. 强制性规则

#### 规则1.1：`-q` 和 `-aa` 必须一起使用

`-q` 选项和 `-aa` 选项**必须同时出现**，否则作业无法调度到计算节点运行。

```bash
# 正确（推荐）
#DSUB -q arm -aa

# 错误：缺少 -aa，作业无法调度
#DSUB -q arm
```

#### 规则1.2：网络访问规范

**由于计算节点没有联网，所有需要网络的任务都必须在当前登录节点进行，不得提交到计算节点。**

| 任务类型 | 执行位置 | 说明 |
|---------|---------|------|
| 需要网络（下载数据、下载参考基因组、安装软件包等） | **登录节点** | 直接在登录节点执行，不能通过 dsub 提交 |
| 纯计算（比对、定量、组装、分析等） | 计算节点（通过多瑙提交） | 通过编写 `.dsub` 脚本提交到计算节点 |

#### 规则1.3：资源规划（设置核数前查看资源）

```bash
# 第1步：查看当前集群资源
dnode | head -20

# 第2步：查看队列情况
dqueue

# 第3步：根据结果决定核数
# 多数节点繁忙 → 申请较少核数（易调度）
# 有空闲节点且核心充足 → 可申请较多核数
```

| 场景 | 建议策略 |
|------|----------|
| 队列中 PENDING_JOBS 数量很大 | 申请较少核数（2-4核），提高调度优先级 |
| 队列中 RUNNING_JOBS 较少、节点空闲 | 可申请较多核数加速计算 |
| 急需作业跑上 | 申请1-2核，几乎可以立即调度 |

**警告**：盲目申请过多核心会导致作业长时间排队，且浪费集群资源。

#### 规则1.4：优先使用集群已安装的软件

**如果用户使用集群已安装的软件，必须使用 `module` 命令加载：**

```bash
# 查看可用软件
module av bwa          # 查看bwa相关模块
module av star         # 查看STAR相关模块
module av              # 查看所有可用模块

# 在作业脚本中加载
module load arm/bwa/0.7.18
module load arm/samtools/1.21
```

**规则**：
- **优先原则**：只要应用软件已通过 module 安装在集群，**必须优先**使用 module 版本
- 当用户说"使用集群已安装的软件"时，**不要**假设软件已在 PATH 中
- 必须使用 `module load` 加载对应的模块
- 先用 `module av 软件名` 查看具体模块名

#### 规则1.5：多样本处理优先每样本一个作业

**处理多个样本时，优先为每个样本单独提交一个作业（通过 Shell 循环调用 `dsub`），而不是在一个作业脚本内用 for 循环串行处理所有样本。**

```bash
# 正确（推荐）：每个样本一个作业，利用集群调度并行
for sample in /path/to/data/*_R1.fastq.gz; do
    index=$(basename $sample | sed 's/_R1.fastq.gz//')
    dsub -n "bwa_${index}" -aa -q arm -R 'cpu=40' \
        -o bwa_${index}_%J.out \
        "module load arm/bwa/0.7.18; bwa mem -t 40 ref.fa ${sample} ..."
done

# 不推荐：单个作业内循环处理所有样本，串行执行，无法并行
#DSUB -n process_all ...
for sample in /path/to/data/*_R1.fastq.gz; do
    bwa mem -t 40 ref.fa ${sample} ...
done
```

**理由**：
- 单独作业可被调度器分配到不同节点**并行执行**，大幅缩短总时间
- 单个样本失败不影响其他样本，**独立重试**即可
- 每个作业有独立的日志和资源监控，**便于排查问题**

### 2. 内存规划规则

系统按核数**强制限制**内存，超出会被杀掉（errCode: 143）。各队列每核限制见 [队列与节点信息](references/node-states.md)。

**操作步骤**：
1. 估算程序需要多少内存
2. 选择合适队列（参考[队列与节点信息](references/node-states.md)）
3. 用 `需要内存 ÷ 每核限制` 计算最少申请核数
4. 核数不能超过单节点总核数（见[队列与节点信息](references/node-states.md)）

**队列选择建议**：
- 内存 < 500GB → 使用普通队列（arm/x86）
- 内存 ≥ 500GB → 使用大内存队列（fat_arm/fat_x86）
- 不建议 < 500GB 的作业使用 fat 队列，以免排队时间过长

## 快速参考

### 常用命令速查

| 命令 | 用途 |
|------|------|
| `dlogin` | 登录获取 token |
| `dsub` | 提交作业 |
| `djob` | 查看作业状态 |
| `dpeek` | 查看运行作业的输出 |
| `dkill` | 终止作业 |
| `djctl` | 作业控制（挂起/恢复/重启） |
| `dnode` | 查看节点信息 |
| `dqueue` | 查看队列信息 |
| `dmod` | 修改作业资源 |

完整命令列表见 [辅助命令](references/commands.md)。

### 重要系统变量

| 变量/占位符 | 说明 |
|-------------|------|
| `%J` | 作业ID（用于日志文件名） |
| `%U` | 用户名 |
| `%G` | TaskGroupName |
| `%I` | Index |
| `%A` | UserName_JobID_TaskGroupName_Index |
| `$CCS_MPI_OPTIONS` | MPI 运行时选项（含 hostfile 等） |

### 日志输出说明

多瑙使用 `-o` 选项指定日志文件，**stdout 和 stderr 合并输出到同一文件**（与 LSF 的 `-o`+`-e` 分离不同）：

| 选项 | 说明 |
|------|------|
| `-o file` | 指定输出日志，以**追加**方式写入 |
| `-oo file` | 指定输出日志，以**覆盖**方式写入 |

```bash
# 推荐：使用 %J 避免重名覆盖
#DSUB -o myjob_%J.out
```

完整选项见 [dsub 完整选项](references/dsub-options.md)。

## 作业提交模板

### 1. 极简串行/多线程作业模板（推荐）

```bash
#!/bin/bash
#DSUB -n job_name             # 作业名
#DSUB -R 'cpu=4'              # 申请4个CPU核（根据内存需求调整）
#DSUB -q arm                  # 队列
#DSUB -aa                     # 任意架构（必须与-q一起用）
#DSUB -o %J.out               # 输出日志（stdout+stderr合并）

# 加载集群已安装的软件（如果有）
# module load arm/bwa/0.7.18 arm/samtools/1.21

# 运行程序
your_program --threads 4
```

**重要**：生物信息软件大多不支持跨节点并行，不要随意使用多节点选项。

### 2. MPI并行作业（多节点）

以 lammps 为例：

```bash
#!/bin/bash
#DSUB -n lammps
#DSUB -N 256                  # MPI总进程数
#DSUB -nn 2                   # 使用2个节点
#DSUB --mpi hmpi              # MPI类型：openmpi/intelmpi/hmpi/mpich
#DSUB -q arm
#DSUB -aa
#DSUB -o lammps_%J.out

module load arm/lammps/29Aug2024_hmpi

mpirun $CCS_MPI_OPTIONS -x OMP_NUM_THREADS=1 lmp_mpi -in in.lj
```

**警告**: 生物软件绝大多数不支持MPI跨节点并行，请勿随意使用。

### 3. NPU作业

> **注意**: 使用 AI 节点前需向管理员申请使用权限。

```bash
#!/bin/bash
#DSUB -n npu_job
#DSUB -R 'npu=1'              # 申请1个NPU
#DSUB -q AI
#DSUB -aa
#DSUB -o npu_job_%J.out

python npu.py
```

查看 NPU 使用情况：
```bash
dnode --npu
```

### 4. 交互作业

```bash
# 普通交互调试
dsub -q interactive -I bash

# AI 节点交互（需申请）
dsub -aa -q AI -I bash
```

## 脚本提交流程（完整步骤）

写好作业脚本后：

```bash
# 第1步：赋予可执行权限
chmod +x my_job.dsub

# 第2步：提交脚本
dsub -s my_job.dsub
```

> **注意**：脚本提交方式只支持 `dsub -s <脚本文件>`，不能直接 `dsub -s script`（会当作命令字符串而非文件）。

## 批量作业提交

### 方式1: Shell循环提交

```bash
for sample in /path/to/data/*_R1.fastq.gz; do
    index=$(basename $sample | sed 's/_R1.fastq.gz//')
    dsub -n "bwa_${index}" -aa -q arm -R 'cpu=40' \
        -o bwa_${index}_%J.out \
        "module load arm/bwa/0.7.18 arm/samtools/1.21; \
         bwa mem -t 40 hg38.fa ${sample} ${index}_R2.fastq.gz | samtools sort -@ 40 -o ${index}_srt.bam"
    sleep 10  # 避免瞬间提交过多
done
```

### 方式2: 阻塞式作业（-w 选项）

使用 `-w` 让作业按顺序执行（类似 LSF 的 `-K`）：

```bash
# 在流程脚本内
dsub -w -n step1 -q arm -aa -R 'cpu=8' "command1"   # 等待完成
dsub -w -n step2 -q arm -aa -R 'cpu=4' "command2"   # step1完成后执行
```

### 方式3: 作业依赖（-D 选项）

```bash
# 依赖单个jobid
dsub -D "1=RUNNING" "echo 'hello'"

# 依赖jobname（支持通配符）
dsub -D "job_*=SUCCEEDED" "echo 'hello'"

# 多条件组合
dsub -D "(1=RUNNING||2=SUCCEEDED)&&3=ENDED" "echo 'hello'"

# 纯数字JobName（加单引号区分）
dsub -D "'12'=RUNNING" "echo 'hello'"
```

依赖状态值：`STARTED`、`RUNNING`、`SUCCEEDED`、`FAILED`、`ENDED`。
完整依赖语法见 [dsub 完整选项](references/dsub-options.md)。

## 作业查询、监控与控制

详见 [djob 作业查询与监控](references/djob.md)，包含：
- 作业状态说明
- `djob -l` / `djob -ll` 排查流程
- CPU 利用率判断规则（cpuUtil avg/recent）
- 日志关键字段解读（EXEC_NODE/EXIT_MESSAGE/MRUN_TIME/MEM_MAX_SUM）
- 作业控制命令（dkill/djctl/dmod）

## 常见故障

### 作业提交后立即结束，无日志输出

```bash
djob -ll <jobid>
# 如果看到 "Job execution environment build failed, err: container save failed"
# 可能是节点根目录写满，联系管理员处理
```

### 内存超限

日志显示：`EXIT_MESSAGE: Job was terminated due to reaching the mem limit, errCode: 143`

解决：根据内存限制规则，申请更多 CPU 核数。
例：arm 队列程序需要 50GB 内存 → 应申请 `-R 'cpu=10'`（50÷5=10）

### 作业排队时间过长

1. 检查 `djob -l <jobid>` 查看排队原因
2. 检查 `dqueue` 查看队列负载
3. 考虑减少申请核数或换队列

## 作业资源申请规则

| 程序类型 | 申请方式 | 说明 |
|---------|---------|------|
| 串行单线程 | `-R 'cpu=1'` | 只用1核 |
| 串行多线程 | `-R 'cpu=N'` | N = 程序使用线程数，不超过节点总核数 |
| MPI并行 | `-N <总进程数> -nn <节点数> --mpi <类型>` | 需要程序支持MPI |

- 单作业 CPU 核数**不能超过**单节点总核数（arm=128, x86=64）
- 申请的核数应与程序实际使用的线程数相等

## Snakemake 集成

```bash
# v8 之前
snakemake --cluster 'dsub -R "cpu={threads}"' -s Snakefile
```
