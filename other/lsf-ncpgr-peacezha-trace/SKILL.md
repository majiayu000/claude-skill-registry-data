---
name: lsf-ncpgr
description: NCPGR高性能计算集群LSF作业调度系统使用指南。用于提交、管理和监控LSF批处理作业，包括串行作业、多线程作业、MPI并行作业、GPU作业、数组作业等。当用户需要编写LSF作业脚本、提交计算任务、查询作业状态、调整作业参数或排查作业问题时使用此skill。
---

# NCPGR LSF 作业调度使用指南

## 编写规范（重要）

提交LSF作业前必须遵守以下规范：

### 0. 网络访问规范

**由于计算节点没有联网，所有需要网络的任务都必须在当前登录节点进行，不得提交到计算节点。**

| 任务类型 | 执行位置 | 说明 |
|---------|---------|------|
| 需要网络（下载数据、下载参考基因组、安装软件包等） | **登录节点** | 直接在登录节点执行，不能通过bsub提交 |
| 纯计算（比对、定量、组装、分析等） | 计算节点（通过LSF提交） | 通过编写 `.lsf` 脚本提交到计算节点 |

### 1. 脚本命名规范

**LSF作业脚本后缀必须使用 `.lsf`**

```bash
# 正确命名
my_job.lsf
bwa_mem.lsf
rnaseq_pipeline.lsf

# 避免使用
my_job.sh          # 不推荐
my_job.bash        # 不推荐
```

### 2. 极简编写规范

**核心原则：由于队列已配置资源限制，作业脚本应尽可能简化**

#### 规则2.1：不设置内存参数

所有队列都已配置内存限制，**不需要**在作业脚本中设置 `-M` 和 `rusage[mem=...]`：

```bash
# 正确的简化写法（推荐）
#!/bin/bash
#BSUB -J my_job
#BSUB -q normal
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o %J.out
#BSUB -e %J.err

your_program --threads $LSB_DJOB_NUMPROC

# 错误的冗余写法（不推荐）
#BSUB -M 8G                 # 不需要！
#BSUB -R "rusage[mem=8G]"   # 不需要！
```

#### 规则2.2：不设置时间限制

不需要设置 `-W` 运行时间限制：

```bash
# 正确的简化写法（推荐）
#!/bin/bash
#BSUB -J my_job
#BSUB -q normal
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o %J.out
#BSUB -e %J.err

# 错误的冗余写法（不推荐）
#BSUB -W 12:00             # 不需要！
```

#### 规则2.3：资源规划（设置核数前查看资源）

```bash
# 第1步：查看当前集群资源
bhosts | grep -E "ok|closed" | head -10

# 第2步：根据结果决定核数
# 多数节点为 closed → 申请2-4核（易调度）
#BSUB -n 2

# 有空闲节点且核心充足 → 可申请8+核
#BSUB -n 8
```

| 场景 | 建议策略 |
|------|----------|
| 多数节点状态为`closed` | 申请2-4核，提高调度优先级 |
| 有空闲节点(`ok`)且有较多空核心 | 可申请8-16核加速计算 |
| 急需作业跑上 | 申请1-2核，几乎可以立即调度 |

**警告**：盲目申请过多核心（如32核）会导致作业长时间排队

## 快速参考

### 常用命令速查

| 命令 | 用途 |
|------|------|
| `bsub < job.lsf` | 提交作业脚本 |
| `bjobs` | 查看作业状态 |
| `bjobs -l <jobid>` | 查看作业详细信息 |
| `bpeek <jobid>` | 查看作业输出 |
| `bkill <jobid>` | 终止作业 |
| `bstop <jobid>` / `bresume <jobid>` | 挂起/恢复作业 |
| `bmod -n 4 <jobid>` | 修改作业参数 |
| `lsload` | 查看节点负载 |
| `bhosts` | 查看节点状态 |
| `bqueues` | 查看队列信息 |

### 推荐别名

添加到 `~/.bashrc`：

```bash
alias bbjobs='bjobs -o "jobid:10 user:6 stat:6 queue:6 exec_host:10 job_name:10 max_mem:14 submit_time:12"'
alias bbs='bjobs -o "jobid:8 user:8 stat:6 queue:6 exec_host:10 job_name:8 nreq_slot:6 slots:5 max_mem:12 submit_time:12 start_time:12 run_time:16 cpu_used"'
```

## 作业提交

### 1. 软件环境规范（重要）

**如果用户使用集群已安装的软件，必须使用 `module` 命令加载：**

```bash
# 查看可用软件
module av bwa          # 查看bwa相关模块
module av star         # 查看STAR相关模块
module av              # 查看所有可用模块

# 在作业脚本中加载
module load BWA/0.7.17-foss-2018b
module load STAR/2.6.0a-foss-2016b
```

**规则**：
- **优先原则**：只要应用软件已通过module安装在集群，**必须优先**使用module版本
- 当用户说"使用集群已安装的bwa/star/samtools"等时，**不要**假设软件已在PATH中
- 必须使用 `module load` 加载对应的模块
- 先用 `module av 软件名` 查看具体模块名

### 2. 极简串行/多线程作业模板（推荐）

```bash
#!/bin/bash
#BSUB -J job_name          # 作业名
#BSUB -n 4                  # 申请4个核心（根据bhosts结果调整）
#BSUB -R "span[hosts=1]"    # 限制在单节点运行
#BSUB -o %J.out             # 输出文件
#BSUB -e %J.err             # 错误文件
#BSUB -q normal             # 队列名

# 加载集群已安装的软件（如果有）
# module load SoftwareName/Version

# 使用 $LSB_DJOB_NUMPROC 自动获取申请的核心数
your_program --threads $LSB_DJOB_NUMPROC
```

**极简原则**：
- ✅ 不设置 `-M` 和 `rusage[mem=...]`（队列已自动管理）
- ✅ 不设置 `-W` 时间限制
- ✅ 使用 `module load` 加载集群已安装的软件
- ✅ 只保留最核心的参数

**重要**: 生物信息软件大多不支持跨节点并行，务必使用 `-R "span[hosts=1]"` 限制在单节点运行。

### 2. 其他作业类型模板

#### MPI并行作业（多节点）

```bash
#!/bin/bash
#BSUB -J MPIJob
#BSUB -q normal
#BSUB -n 400
#BSUB -R "span[ptile=20]"   # 每节点20核
#BSUB -o stdout_%J.out
#BSUB -e stderr_%J.err

module load intel/2018.4
module load mpi/intel/2018.4

mpirun -np $LSB_DJOB_NUMPROC ./MPI_program
```

**警告**: 生物软件绝大多数不支持MPI，请勿随意使用多节点并行。

#### GPU作业

```bash
#!/bin/bash
#BSUB -J gpu_job
#BSUB -q gpu
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=shared"
#BSUB -o %J.out
#BSUB -e %J.err

python train.py
```

#### 交互式作业

```bash
# 基础交互
bsub -q interactive -Is bash

# 带X11转发（图形界面）
bsub -q interactive -XF -Is bash
```

限制：只能在interactive队列，最长48小时。

## 批量作业提交

### 方式1: Shell循环提交（推荐）

```bash
for sample in /path/to/data/*_1.fq.gz; do
    index=$(basename $sample | sed 's/_1.fq.gz//')
    bsub -J ${index} -n 8 -R span[hosts=1] -o %J.${index}.out \
        "your_program -t 8 -i $sample"
    sleep 10  # 避免瞬间提交过多
done
```

### 方式2: 流程脚本 + 批量提交（带依赖）

使用 `-K` 参数让作业按顺序执行：

```bash
# 在流程脚本内
bsub -K -J step1 -n 8 ... "command1"   # -K等待完成
bsub -K -J step2 -n 1 ... "command2"   # step1完成后执行
bsub -K -J step3 -n 2 ... "command3"
```

### 方式3: 数组作业

```bash
#BSUB -J array[1-100]  # 提交100个任务

# 使用 $LSB_JOBINDEX 区分不同任务
input="sample_${LSB_JOBINDEX}.fq"
```

## 作业查询与监控

### 作业状态说明

| 状态 | 含义 |
|------|------|
| PEND | 排队中 |
| RUN | 运行中 |
| DONE | 正常完成 |
| EXIT | 异常退出 |
| SSUSP | 系统挂起（节点内存不足等） |
| USUSP | 用户挂起 |

### 排查作业问题

**查看排队原因**:
```bash
bjobs -p <jobid>
```

常见原因：
- `User has reached the pre-user job slot limit`: 用户作业数达队列上限
- `The user has reached his job slot limit`: 用户总作业数达系统上限
- `The queue has reached its job slot limit`: 队列总核数已满

**检查作业效率**:
```bash
# 比较 run_time (walltime) 和 cpu_used (cputime)
# 若 cpu_used << run_time * 核数，说明作业可能空跑或出错
```

**作业运行异常/资源不合理检查原则**：

当分析已完成作业的 `bjobs` 输出时，如果同时满足以下两个条件，必须提醒用户：

1. **walltime (实际运行时间) 远小于 cputime (CPU总时间)**  
   - walltime ≈ cputime → 程序实际上只使用了单核，多核心未被利用
   - 例如：申请了8核，walltime=1小时，cputime=1.2小时 → 说明只用到约1核

2. **单核实际内存使用 < 队列单核内存限制**

**提醒内容应包括**：
- 指出资源申请不合理：程序没有充分利用申请的所有核心
- 建议减少核数重新提交，这样排队更快且不浪费集群资源
- 可能原因：程序本身不支持多线程，或多线程参数配置不正确

**判断示例**：

| 申请核数 | walltime | cputime | 实际内存 | 队列限制 | 结论 |
|---------|---------|---------|---------|---------|------|
| 8核 | 60分钟 | 70分钟 | 2GB | 6GB | **提醒**：只用到1核，建议减少核数 |
| 8核 | 60分钟 | 420分钟 | 2GB | 6GB | 正常：有效利用了约7核 |
| 4核 | 30分钟 | 35分钟 | 1GB | 6GB | **提醒**：只用到1核，建议减少核数 |

## 作业控制

```bash
bkill <jobid>           # 终止作业
bkill 0                 # 终止用户所有作业
bstop <jobid>           # 挂起作业
bresume <jobid>         # 恢复作业
bmod -n 8 <jobid>       # 修改核心数
bmod -q high <jobid>    # 修改队列
btop <jobid>            # 作业移到队首
bbot <jobid>            # 作业移到队尾
brequeue <jobid>        # 重新提交作业
```

## 集群特定信息

### 队列选择

| 队列 | 用途 | 特点 |
|------|------|------|
| normal | 普通计算 | 默认队列，自动内存限制(6-10GB) |
| smp | 大内存 | 大内存节点(s001-s006)，自动内存限制(12-20GB) |
| high | 384GB内存 | 大内存作业，自动内存限制(11-15GB) |
| q2680v2 | 计算队列 | 自动内存限制(6-10GB) |
| gpu | GPU计算 | gpu01-04，自动内存限制(需确认) |
| parallel | MPI并行 | 跨节点并行，自动内存限制(需确认) |
| interactive | 交互调试 | 限48小时，自动内存限制(30-500GB) |

### 队列自动资源限制

**所有队列都已配置资源限制，用户无需在脚本中设置**：

| 队列 | 内存限制 | 时间限制 | 说明 |
|------|---------|---------|------|
| **normal** | 默认6GB，最大10GB | 无默认 | 用户无需设置内存和时间 |
| **smp** | 默认12GB，最大20GB | 无默认 | 用户无需设置内存和时间 |
| **high** | 默认11GB，最大15GB | 无默认 | 用户无需设置内存和时间 |
| **q2680v2** | 默认6GB，最大10GB | 无默认 | 用户无需设置内存和时间 |
| **interactive** | 默认30GB，最大500GB | 48小时 | 仅限48小时交互 |

**使用原则**：
- ✅ **不要设置** `-M` 和 `rusage[mem=...]`（队列已自动管理）
- ✅ **不要设置** `-W` 时间限制（除非是测试性作业）
- ✅ **只设置** `-n` 核心数和 `-q` 队列名

**内存超限处理**：
- 超出默认限制：作业会被挂起(SSUSP)，稍后自动恢复
- 超出最大限制：作业会被终止(EXIT)
- 频繁被挂起：考虑换到smp/high队列或优化程序

### 重要系统变量

| 变量 | 说明 |
|------|------|
| `$LSB_JOBID` | 作业ID |
| `$LSB_JOBINDEX` | 数组作业索引 |
| `$LSB_DJOB_NUMPROC` | 申请的核心数 |
| `$LSB_QUEUE` | 队列名 |

## 参考资料

- [完整文档](references/lsf-guide.md)
- [作业模板脚本](scripts/) （后缀均为 `.lsf`）
- [常见问题](references/faq.md)
- [快速参考](references/quick-ref.md)
