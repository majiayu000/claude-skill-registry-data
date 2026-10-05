---
name: ncpgr-software
description: NCPGR高性能计算集群软件使用注意事项与优化指南。聚焦各软件的坑点、加速技巧、资源节省建议与软件选型推荐。当用户询问集群上如何高效使用软件、编写LSF作业、或需要软件选型建议时使用。
trigger: 当用户问题中包含"集群"二字时，同时加载 ncpgr-software ncpgr-lsf 两个 skill。
solves: ["软件选型", "资源申请", "module使用", "singularity使用"]
related_to: [lsf-ncpgr, bio/alignment, bio/qc, bio/transcriptome]
---

# NCPGR HPC 集群软件使用注意事项与优化指南

## 总则

- 集群软件通过 **module** (`module av` / `module load`，http://hpc.ncpgr.cn/app/004-Module/) 或 **singularity**（镜像位于 `/share/Singularity/`，http://hpc.ncpgr.cn/app/007-singularity/）调用
- 公共数据库（NR/NT/Pfam/Rfam/swissprot）位于 `/share/database/`，http://hpc.ncpgr.cn/app/025-bioinformatics-database/
  - **使用方法**：`module av` 查看可用版本 → `module load` 加载 → 加载后自动设置环境变量（如 `$NR`、`$NT`、`$Pfam`）直接使用，**不需要自己 `makeblastdb` 建索引**
  - 示例：
    ```bash
    module load nr/20201013
    blastp -query proteins.fa -db $NR -out result.txt -num_threads 8 -outfmt 6

    module load nt/20201013
    blastn -query seqs.fa -db $NT -out result.txt -num_threads 8 -outfmt 6

    module load nr/20201013-diamond   # diamond 专用版本（比 blastp/blastx 快很多）
    ```
  - 可用版本：`nr/20201013`、`nr/20190625`、`nr/20171030`、`nr/20201013-diamond`、`nt/20201013`、`Pfam/32.0`、`Rfam/14.1`、`swissprot/20170604` 等
- 计算节点**无联网能力**，需联网的操作须在登录节点提前完成
- 编写 LSF 作业脚本时结合 `lsf-ncpgr` skill
- `module av` 支持模糊搜索，大小写不确定时都试试
- **不要在作业脚本中随意使用 `/tmp` 目录**，除非用户明确指定或软件文档中有明确提示。计算节点的 `/tmp` 为系统盘，大量临时文件积累会写满导致节点挂起。确需使用时，应创建用户专属临时目录并在作业结束时清理
- **作业脚本应保持简洁**，不可过度编码或使用高级技巧（如复杂的 sed/awk 变量替换、多重临时文件、嵌套逻辑等）。脚本需要让用户易于阅读、检查和自行修改

### 查询软件/数据库是否可用

当用户询问**某个软件**或**某个数据库**是否在集群上可用时，**不要仅凭 skill 中的信息回答**，应实际查询集群当前状态：

1. **查询软件（首选 `mii`）**：集群已安装 `mii`，可搜索 module 中的二进制命令
2. **查询 module**：`module av 软件名` 或 `module av \| grep -i 关键词`
3. **查询 singularity 镜像**：检查 `/share/Singularity/` 目录下的镜像文件
4. **查询数据库**：用 `module av` 查看最下方的数据库列表，或检查 `/share/database/` 目录

```bash
# 查询软件（推荐：mii 可搜索 module 中的所有二进制命令）
mii search bedCoverage        # 查找哪个 module 提供 bedCoverage
mii search bigWigToBedGraph   # 查找 UCSC 工具对应的 module
mii search gmx                # 子串匹配，搜 gmx 会显示 gmx_mpi
mii list                      # 列出所有已索引的 module

# module 模糊搜索
module av bwa
module av \| grep -i star

# 查询 singularity 镜像
ls /share/Singularity/ \| grep -i alphafold

# 查询数据库
module av               # 最下方会列出NR、NT、Pfam等数据库
ls /share/database/
```

**mii 说明**：
- 集群已安装，路径 `/public/home/software/opt/bio/software/mii/1.1.2/`
- 首次使用需 `mii build` 创建索引，后续更新用 `mii sync`
- `mii search <命令>` 可找到任意 module 中的二进制命令，包括工具集中的子命令（如 UCSC Kent Utils 中的 bedCoverage）

- 如果查询结果为空，告知用户集群上暂无该软件/数据库
- 如果找到相关软件/数据库，给出具体版本和使用方法

### 多样本多步骤流程的提交策略

当涉及**多样本 + 每个样本多步骤**的分析流程时（如1000样本变异检测：fastp → 比对 → 变异检测 → joint call），**必须先询问用户采用哪种策略**，再生成脚本：

| 策略 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| **逐步处理** | 每次提交所有样本的第1步，确认完成后提交第2步，以此类推 | 中间结果可控，某步出错可及时调整；便于中间检查 | 需要分多次操作 |
| **依赖链一次提交** | 用 `-w "ended(jobid)"` 建立样本内步骤依赖，一次提交所有样本所有步骤 | 一次提交全自动；中间步骤自动衔接 | 提交后难以中途干预；出错样本需单独处理 |

- **不确定时默认推荐逐步处理**，因为便于用户在中间步骤检查结果、调整参数
- 如果用户选择依赖链一次提交，需为每个样本创建独立的作业依赖链

---

## 常见软件资源推荐（核数与内存）

### 通用原则

1. **多样本优先"样本间并行"，不是单样本堆核数**：20个RNA-seq样本，与其每个STAR给32核，不如每个给8~12核、同时跑多个样本，集群吞吐量更高
2. **不是核越多越快**：多数生信软件在4~16核后收益明显变差，内存和磁盘I/O往往才是瓶颈
3. **Java程序要预留系统余量**：申请32GB内存时，`-Xmx` 设为28g左右，JVM、容器、native library、临时buffer都会额外占内存
4. **先跑1~2个代表样本测资源**：记录MaxRSS、CPU利用率、I/O wait；CPU利用率长期低于300%却给了16核 → 降核数、提并发样本数

### CPU 核数推荐

| 软件/场景 | 推荐核数 | 原因 |
|-----------|---------|------|
| **FastQC / MultiQC** | **1~2** | FastQC单文件并行更好；MultiQC基本不需要多核 |
| **fastp** | **4~8** | 速度已经很快，更多核意义不大；`--dont_eval_duplication`可省~1GB内存和10~20%时间 |
| **Trim Galore / cutadapt** | **4~8** | 多核收益有限，继续加核无运行时间收益 |
| **BLAST blastn** | **4~8** | CPU利用率不高，更多核几乎不加速 |
| **Salmon / kallisto** | **4~8** | 通常很快，适合多样本并行 |
| **faST-LMM** | **1**（单线程） | `-maxThreads` 多线程反而比单线程慢1倍 |
| **CNVnator** | **按需设置** | 默认用满整节点，**必须**设置 `MKL_NUM_THREADS=$LSB_DJOB_NUMPROC` |
| **samtools view/index/flagstat** | **2~8** | 压缩/解压相关，多给核有收益但通常不线性 |
| **samtools sort** | **4~8** | 8核以上加速效果有限；注意每线程内存（见下方） |
| **Picard MarkDuplicates** | **2~4** | Java堆内存要设`-Xmx`；大BAM更吃内存和临时盘 |
| **sambamba markdup/sort** | **4~8** | 多线程比Picard友好，但也别无限加核 |
| **GATK HaplotypeCaller** | **1~4**/分片 | 推荐按染色体/区间scatter并行，每shard 1~4核 |
| **GATK GenomicsDBImport / GenotypeGVCFs** | **2~8** | 样本数越多越吃内存；联合分型大队列应按染色体/区间拆分 |
| **Mutect2** | **1~4** | 肿瘤样本深度高时内存和时间显著上升 |
| **bcftools** | **4~8** | 多线程扩展性一般 |
| **BWA mem / BWA-MEM2** | **8~16** | 多线程扩展性好，但超过16核被排序/压缩/I/O抵消 |
| **Bowtie2 / HISAT2** | **8~16** | 剪接比对开销大，超16核收益递减；HISAT2比STAR省内存 |
| **STAR** | **16~24** | 内存带宽密集型，更多核帮助有限 |
| **minimap2** | **8~32** | 长读长比对可给较多核，但仍受I/O和压缩限制 |
| **Trinity** | **16~32** | 多阶段并行，32核内扩展性较好 |
| **BUSCO** | **8~32** | 单基因预测是单线程，多基因并行有效 |
| **MAKER** (MPI) | **50~100** | MPI并行，但过多核排队久 |
| **CellRanger** | **16~20** | 超过20核收益递减 |
| **InterProScan** | **8~16** | 多线程扩展性好，但IO也是瓶颈 |
| **Kraken2** | **16~24** | 分类器并行效果好 |
| **SPAdes / metaSPAdes** | **16~32** | 给内存比给核更重要；内存不足会失败或极慢 |
| **Bismark** | **按 `--multicore N` × 4** | `--multicore 4` → 实际16线程，需 `-n 16` |
| **RepeatModeler** | **按 `-pa N` × 4** | `-pa 5` → 实际20线程，需 `-n 20` |
| **GLnexus** | **16~36** | 内存需求大，用整节点 |
| **Parabricks** | **16** | GPU为主，CPU辅助16核足够 |
| **AlphaFold3 data pipeline** | **16~32** | MSA搜索并行好，32核内扩展性好 |
| **AlphaFold3 inference** | **8~16** | GPU为主，CPU辅助 |

### 内存需求推荐

| 软件/场景 | 内存需求 | 建议 |
|-----------|---------|------|
| **FastQC / MultiQC** | 2~8GB | normal队列足够 |
| **fastp** | 4~8GB；大样本8~16GB | normal队列足够 |
| **Trim Galore / cutadapt** | 4~12GB | normal队列足够 |
| **Salmon / kallisto** | 8~32GB | normal队列足够 |
| **samtools view/index** | 4~16GB | normal队列足够 |
| **samtools sort** | 16~64GB | `-@ 8 -m 3G` 约24GB缓冲+额外开销，建议申请32~40GB |
| **Picard MarkDuplicates** | 16~64GB | `-Xmx` 设为申请内存的80%~85% |
| **比对 (BWA/HISAT2)** | 人类基因组 ~16GB | normal队列 `-n 8` 通常足够 |
| **STAR 比对** | 人基因组 **40~64GB** | **必须用 smp 或 high 队列**；nf-core文档给出Human GRCh37约38GB典型需求 |
| **minimap2** | 16~64GB | 与参考基因组大小正相关 |
| **BUSCO** | 基因组 ~8GB | normal队列足够 |
| **GATK HaplotypeCaller** | WES ~8GB, WGS ~16GB | 按分片给16GB/分片 |
| **GATK GenomicsDBImport / GenotypeGVCFs** | **32~128+GB** | 样本数越多越吃内存；建议用 high/smp |
| **Mutect2** | 16~64GB | 肿瘤样本深度高时内存显著上升 |
| **bcftools** | 与VCF大小正相关 | 一般4GB足够 |
| **Trinity** | **128~512GB** | **必须用 smp 队列整节点** |
| **SPAdes / metaSPAdes** | **128~512GB** | 内存常是主要瓶颈，给内存比给核更重要 |
| **MAKER** | 大基因组 ~16GB/核 | 建议 smp 或 high |
| **CellRanger** | **64~128+GB** | 内存随细胞数、reads、参考而增大；**必须用 smp 或 high** |
| **GLnexus** | 大规模 joint call **50~200GB** | **必须用 high 或 smp 队列整节点** |
| **AlphaFold3 data pipeline** | 单蛋白 ~8GB | normal队列足够 |
| **AlphaFold3 inference** | 单蛋白 ~16GB | GPU队列已配 |
| **Kraken2 建库** | 标准库 ~100GB | **必须用 high 或 smp** |
| **Kraken2 分类** | 标准库 64~256+GB | 取决于数据库大小；大库常需整库进内存 |
| **InterProScan** | 大数据集 ~32GB | 建议 smp 队列 |
| **Parabricks** | ~16GB | GPU队列已配 |
| **Paragraph** | 与VCF大小正相关 | normal队列足够 |

### `samtools sort` 内存计算

`samtools sort -@ N -m MG` 的排序缓冲区约 `N × M` GB，加上压缩线程等额外开销：

```bash
# 稳妥写法：8线程 × 3G = ~24GB 缓冲，作业申请 32~40GB
samtools sort -@ 8 -m 3G -o sample.sorted.bam sample.bam

# 反面教材：不要在16GB作业里这样写
samtools sort -@ 16 -m 2G -o ...   # 仅缓冲就32GB，必定OOM
```

### 节点/队列选择速查

| 队列 | 资源特点 | 适用场景 |
|------|---------|---------|
| **normal** | 自动6~10GB | 大多数常规分析（质控、fastp、BUSCO、blast、BWA），内存需求 <10GB |
| **smp** | 自动12~20GB | 大内存作业（Trinity、STAR、大基因组MAKER、CellRanger） |
| **high** | 自动11~15GB | 超大内存作业（GLnexus、Kraken2建库、GenomicsDBImport） |
| **gpu** | 需确认 | GPU加速作业（Parabricks、AlphaFold3 inference、DeepVariant），**需向管理员申请权限** |

按节点资源快速决策：

| 节点资源 | 推荐策略 |
|----------|---------|
| 8核 / 32GB | HISAT2 / Salmon / kallisto / 小型WES可跑；STAR人基因组偏紧 |
| 16核 / 64GB | bulk RNA-seq、WES、普通WGS单样本比较舒适 |
| 32核 / 128GB | 单细胞、WGS多样本并行、部分宏基因组比较合适 |
| 64核 / 256+GB | 适合组装、大型宏基因组、大队列联合分型、Kraken2大库 |

### 推荐默认模板（不确定时先用这些）

| 软件 | 核数 | 内存 |
|------|------|------|
| fastp | 4 | 8G |
| STAR | 12 | 48G |
| HISAT2 / BWA | 12 | 24G |
| samtools sort | 8 | 32G |
| MarkDuplicates | 4 | 32G |
| HaplotypeCaller | 2/分片 | 16G/分片 |
| Salmon / kallisto | 4 | 16G |
| Cell Ranger | 16 | 128G |
| Kraken2 | 16 | 数据库大小 + 20~40G |
| SPAdes / metaSPAdes | 24 | 256G |

---

## 软件选型速查

### 变异检测

> **Parabricks 是变异检测的首选方案**，除非用户明确提及需要 DeepVariant，否则不要主动推荐 DeepVariant。

| 场景 | 推荐 | 速度 | 说明 |
|------|------|------|------|
| WGS/WES 变异检测（**首选**） | **Parabricks** (GPU) | 30x WGS ~25min | 比对+变异检测全流程GPU加速，学术免费。http://hpc.ncpgr.cn/app/098-parabricks/ |
| 大规模 gVCF joint call | **GLnexus** | 远快于 GATK | 替代 CombineGVCFs+GenotypeGVCFs。http://hpc.ncpgr.cn/app/126-glnexus/ |
| 变异结果基准测试 | **HAPpy** | - | Illumina官方工具，单倍型水平比较。http://hpc.ncpgr.cn/app/164-happy/ |
| 深度学习变异检测（仅用户主动提及） | DeepVariant | 准确率~99% | http://hpc.ncpgr.cn/app/100-deepvariant/ |

### 序列比对
| 场景 | 推荐 | 说明 |
|------|------|------|
| fq→bam (首选) | **Parabricks fq2bam** (GPU) | bwa+sort+dedup 一行完成，GPU加速 |
| fq→bam (CPU) | **BWA** + samtools | 常规方案 |
| RNA-seq 比对 | **HISAT2** | 剪接感知比对 |

### 质控
| 场景 | 推荐 | 说明 |
|------|------|------|
| 质控 | **fastp** | 速度快，同时输出质控报告 |

### 蛋白结构预测
| 场景 | 推荐 | 说明 |
|------|------|------|
| 最高精度 | **AlphaFold3** | Google DeepMind，支持蛋白复合物。http://hpc.ncpgr.cn/app/183-alphafold3/ |
| 快速/省资源 | **RoseTTAFold** | 内存和时间远低于AlphaFold。http://hpc.ncpgr.cn/app/085-RoseTTAFold/ |

### 覆盖度计算
| 场景 | 推荐 | 说明 |
|------|------|------|
| 覆盖度 | **PanDepth** | 比samtools快很多，cram输入比bam更快。http://hpc.ncpgr.cn/app/145-PanDepth/ |

---

## 各软件注意事项与加速技巧

### Parabricks (GPU加速 NGS 分析)
> 集群文档: http://hpc.ncpgr.cn/app/098-parabricks/

30x WGS 约 **25分钟**（传统方法约30小时），从v4.0起**学术用户免费**。

**版本选择**: 除非有特殊需求，**优先使用 `4.0.1-1` 版本**（`$IMAGE/clara-parabricks/4.0.1-1.sif`）。

```bash
#BSUB -J parabricks
#BSUB -n 16
#BSUB -R span[hosts=1]
#BSUB -gpu "num=1:gmem=11G"
#BSUB -q gpu

module load Singularity/3.7.3
singularity exec --nv $IMAGE/clara-parabricks/4.0.1-1.sif pbrun fq2bam \
  --low-memory --ref hg38.fa --in-fq sample.R1.fq.gz sample.R2.fq.gz \
  --out-bam sample.sorted.dedup.bam
```

`fq2bam` 一行完成：bwa mem → sort → mark duplicates → BQSR → 输出bam。

Parabricks 还支持 `haplotypecaller`、`deepvariant`、`genotypegvcf` 等变异检测工具，均基于 GPU 加速，相比开源版本速度有大幅提升。

---

### BWA / HISAT2 比对
> 比对建议: http://hpc.ncpgr.cn/app/071-fq2bam/ | SAM→BAM: http://hpc.ncpgr.cn/app/054-sam-to-bam/ | HISAT2: http://hpc.ncpgr.cn/app/064-hisat2/
- **无需解压 fq.gz**，大部分比对软件可直接读取
- **建议直接输出 bam**（只有 sam 的 1/3 大小），下游支持可进一步压缩为 cram
- 大规模比对需要较高存储带宽，建议在 **normal队列** 运行
```bash
bwa mem -t 8 genome.fa read1.fq.gz read2.fq.gz | samtools sort -@8 -o output_sorted.bam
```

**HISAT2 特别注意**:
- 找不到索引文件时**不会自动退出**，让人误以为还在运行！
- 提交作业后务必用 `bpeek <job_id>` 查看输出确认
- 有异常及时杀掉作业重投

---

### BLAST
> 集群文档: http://hpc.ncpgr.cn/app/041-blast/

- **NR/NT 等公共数据库已配置好，用 `$NR`、`$NT` 变量直接引用**（见总则部分）
- **用 diamond 替代 blastx/blastp**，速度极大提升；`module load nr/20201013-diamond` 有格式化好的 nr 库
- **blastn 运行慢时**: 将 query 分割多段提交多个作业并行跑，线程数设 **4~8** 即可（CPU利用率不高）
- 超短序列（<50nt）用 `-task blastn-short -word_size 4 -gapopen 1 -gapextend 1`
- 小参考序列不用建索引，用 `-subject` 直接比对

---

### BUSCO
> 集群文档: http://hpc.ncpgr.cn/app/042-BUSCO/

- **计算节点无网络，必须用离线模式**: 先在登录节点下载数据库，再提交作业
```bash
# 登录节点下载数据库
singularity exec $IMAGE/busco/5.5.0_cv1.sif busco --download embryophyta_odb10
# 计算节点离线运行
singularity exec -e $IMAGE/busco/5.5.0_cv1.sif busco -i MH63.fa -l ./busco_downloads/lineages/embryophyta_odb10 -o out -m genome -c 30 --offline
```

---

### Bismark (BS-seq 甲基化比对)
> 集群文档: http://hpc.ncpgr.cn/app/040-Bismark/
- **`--multicore N` 实际调用 4N 个 bowtie 线程**！LSF 申请核心数必须是 `--multicore` 值的 **4倍**
  - 如 `--multicore 4` → 实际16线程，需 `-n 16`
- `bismark2bedGraph` 中 sort 可手动添加 `--parallel=8` 加速，用 `--buffer_size` 控制内存

---

### BS-Seeker2
> 集群文档: http://hpc.ncpgr.cn/app/072-bs-seeker/
- **产生大量临时文件写入 `/tmp`，极易写满**（单作业可达 30~70GB）
- **务必使用 `--temp_dir`** 指向自己目录：
```bash
mkdir tmp
bs_seeker2-align.py -1 R1.fq -2 R2.fq -o sample.bam -g genome.fa --temp_dir=./tmp
```

---

### RepeatModeler
> 集群文档: http://hpc.ncpgr.cn/app/182-repeatmodeler/
- **`-pa N` 实际使用 4N 线程**（每个 rmblastn 用4线程）
- `-pa 5` → 20线程，作业脚本需申请 `-n 20`，否则节点过载挂起
- 版本 2.0.6 报错 `build_lmer_table failed. Exit code 256` 需修改 RepeatScout 2行代码重编译（见 commit c5193bb）

---

### MAKER (基因组注释)
> 集群文档: http://hpc.ncpgr.cn/app/050-maker/

- MPI并行，**必须用 parallel 队列**（需申请权限，每人限120核）
- 建议申请 100 核即可（过多排队时间长）；**资源紧张时拆分染色体**各跑一个作业
- **运行时需及时关注日志** `*_master_datastore_index.log`，出现 `FAILED` 程序不会停下但会空跑
- 小基因组出错直接杀掉重跑；大基因组将出错染色体单独重跑再合并

---

### CellRanger (单细胞)
> 集群文档: http://hpc.ncpgr.cn/app/077-cellranger/
**两种加速方式组合，可将运行时间从 8h 降至 2h**：

1. **结果输出到计算节点 `/tmp`**（本地磁盘IO更快）
   - 需指定 `rusage[tmp=XXG]`，经验值为输入 fq.gz 的 **2倍**
   - 运行完移回 home
2. **添加 `--no-bam`**（不需要bam文件时）
   - 一般表达矩阵分析无需bam，RNA速率分析才需要

```bash
#BSUB -J cellranger
#BSUB -n 20
#BSUB -R "rusage[tmp=70G]"
#BSUB -q normal
module load cellranger/7.0.0

workdir=`pwd`
tmpd="/tmp/`mktemp -u cellranger_XXXXX`"; mkdir ${tmpd}; cd ${tmpd}
cellranger count --id=sample --transcriptome=ref --fastqs=data --sample=sample \
  --force-cells=8000 --localcores $LSB_DJOB_NUMPROC
mv sample/ ${workdir}
```

---

### Paragraph (SV 基因型分型)
> 集群文档: http://hpc.ncpgr.cn/app/063-paragraph/
- **每个VCF位点生成3个临时文件到 `/tmp`，程序结束后不自动删除**，积累会写满系统盘导致节点挂掉
- **建议**: VCF超10万行拆分；在 **normal队列**（SSD系统盘）；单作业申请10核；脚本中创建专属临时目录并在结束时清理
```bash
tmpd="/tmp/`mktemp -u paragraph_XXXXX`"; mkdir ${tmpd}; export TMP=${tmpd}
multigrmpy.py -i input.vcf -r ref.fa --threads $LSB_DJOB_NUMPROC --scratch-dir ${tmpd} -o out
rm -r ${tmpd}   # 务必清理
```

---

### SqueezeMeta (宏基因组)
> 集群文档: http://hpc.ncpgr.cn/app/067-SqueezeMeta/
- **第六步(06.lca.pl)极度吃IO**，数据库在远程分区时速度仅 ~8kb/s（2天的数据量）
- **解决方案**: 用胖节点 s001 的 `/tmp/squeezemeta/db` 数据库，并指定节点 s001
- 集群已有副本: `/share/database/squeezemeta/db/`
- 已运行的修改 `SqueezeMeta_conf.pl` 中数据库路径，用 `restart.pl` 继续

---

### DeepVariant (深度学习变异检测)
> 集群文档: http://hpc.ncpgr.cn/app/100-deepvariant/

> **注意**: 仅当用户明确提及需要使用 DeepVariant 时才推荐此方案，否则默认推荐 Parabricks 进行变异检测。

- GPU版仅 `call_variants` 步骤可用GPU，`make_examples` 和 `postprocess_variants` 只能用CPU
- 三个步骤互相依赖：make_examples → call_variants → postprocess_variants
- 支持 Illumina、PacBio、Nanopore

---

### GLnexus (大规模 gVCF joint call)
> 集群文档: http://hpc.ncpgr.cn/app/126-glnexus/

- 替代 GATK CombineGVCFs + GenotypeGVCFs，**速度快很多**
- **内存需求大**，建议用 high 或 smp 队列整节点（`-q high -n 36`）
- WES 需用 `--bed` 指定目标区域；WGS可不指定
- 输出 bcf 格式，可用 bcftools 转 vcf
- 内存报错 `std::bad_alloc` 时寻求管理员协助

---

### HAPpy (变异检测基准测试)
> 集群文档: http://hpc.ncpgr.cn/app/164-happy/

```bash
hap.py truth.vcf query.vcf -r ref.fa -f chr1.bed --threads 8 -o truth_vs_query
```
- `-f` 指定比较区间（bed），只比较该区间内位点
- 输出 summary.csv（精度/召回率/F1）、ROC曲线、标注VCF等

---

### faST-LMM (群体遗传)
> 集群文档: http://hpc.ncpgr.cn/app/046-fastlmmc/
- **`-maxThreads` 多线程比单线程还慢**！**不要用该选项，默认单线程即可**
- 实测：单线程 2208s vs 20线程 4112s

---

### CNVnator (CNV 检测)
> 集群文档: http://hpc.ncpgr.cn/app/044-cnvnator/
- **默认用满整个节点CPU核**，必须用环境变量控制线程数：
```bash
export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1
# 或按申请的核心数
export MKL_NUM_THREADS=$LSB_DJOB_NUMPROC; export OMP_NUM_THREADS=$LSB_DJOB_NUMPROC
```

---

### OrthoMCL (同源基因簇)
> 集群文档: http://hpc.ncpgr.cn/app/076-orthomcl/
- MySQL 在 s004 节点，数据库建议命名为 `orthomcl_username` 避免冲突
- **运行完成后及时删除 MySQL 中创建的数据库**
```bash
orthomcl-setup-database.pl --user username --password password --host s004 --database orthomcl_username --outfile orthomcl.conf
orthomcl-pipeline -i pep/ -o out -m orthomcl.conf --nocompliant -s $LSB_DJOB_NUMPROC --yes
```

---

### Trinity (转录组组装)
> 集群文档: http://hpc.ncpgr.cn/app/060-trinity/
- 使用 singularity 镜像 `/share/Singularity/Trinity/2.12.0.sif`
```bash
bsub -o trinity.log -n 30 -q smp -J trinity \
  "module purge; module load Singularity/3.1.1; singularity exec $IMAGE/Trinity/2.12.0.sif Trinity --seqType fq --max_memory 400G --samples_file samples_file --CPU 30 --SS_lib_type RF --output trinity_out"
```

---

### HiC-Pro
> 集群文档: http://hpc.ncpgr.cn/app/049-HiC-Pro/
- 集群中 `HiC-Pro/2.11.14` 已配集群模式
- 生成的 LSF 脚本不能直接提交，需删除 `#BSUB -M/W/N/u/q` 行，添加 `module load HiC-Pro/2.11.4`
- 先提交 step1，日志无报错后再提交 step2（step2 可改 `-n 1`）
- 出错直接重新提交该脚本即可

---

### InterProScan (蛋白功能注释)
> 集群文档: http://hpc.ncpgr.cn/app/123-interproscan/

- **省资源方案**: 用网页API（`iprscan5.pl`），在登录节点运行，**不消耗集群计算资源**
```bash
./iprscan5.pl --multifasta test.fasta --maxJobs 25 --email test@test.com --outformat tsv
```
- 本地运行：`module load interproscan/5.55-88.0`，消耗计算资源

---

### HOMER (Motif发现)
> 集群文档: http://hpc.ncpgr.cn/app/112-homer/

- `module load homer/4.11`
- 支持 ChIP-Seq、RNA-Seq、DNase-Seq、Hi-C 等分析

---

### Augustus (基因预测)
> 集群文档: http://hpc.ncpgr.cn/app/083-augustus/
- `module load augustus/3.3.3`
- 自带模型路径：`$AUGUSTUS_CONFIG_PATH`
- 自定义模型：`export AUGUSTUS_CONFIG_PATH=$HOME/augustus_config`

---

### PASA (转录组注释)
> 集群文档: http://hpc.ncpgr.cn/app/084-pasa/
- 推荐用 sqlite 数据库（比 mysql 方便），配置文件中 `DATABASE=` 写绝对路径
```bash
module load PASA/2.5.2
Launch_PASA_pipeline.pl -c alignAssembly.config -C -r -R --ALT_SPLICE -g genome.fa -t all.fa.clean -T -u all.fa -f accession.txt --TDN TCN.acc --transcribed_is_aligned_orient --ALIGNERS blat,gmap --CPU 20
```

---

### FunGAP (真菌基因组注释)
> 集群文档: http://hpc.ncpgr.cn/app/103-fungap/

- **必须先拷贝配置文件到本地**，否则运行过程权限报错：
```bash
singularity exec $IMAGE/FunGAP/FunGAP.sif cp -r /opt/conda/config FunGAP_config
singularity exec -B ./FunGAP_config/:/opt/conda/config/ $IMAGE/FunGAP/FunGAP.sif \
  /workspace/FunGAP/fungap.py --output_dir fungap_out ...
```
- 离线运行需修改 `check_inputs.py` 中 `check_busco_dataset` 函数，注释掉 159-168 行（禁用 `busco --list-datasets`）

---

### Kraken2 (分类学序列分类)
> 集群文档: http://hpc.ncpgr.cn/app/178-kraken2/

- 数据库含 hash.k2d, opts.k2d, taxo.k2d 三个文件
- 标准库建库：`kraken2-build --standard --threads 24 --db $DBNAME`（下载超50GB，建库用超100GB磁盘）
- 可下载预构建数据库，节省时间

---

### vg (泛基因组分析)
> 集群文档: http://hpc.ncpgr.cn/app/138-vg/

- 支持图构建、比对（BWA-MEM/minimap2/Giraffe）、变异检测、可视化
- 更新快，运行问题多在 GitHub issues 中已有解答
- `module load vg/1.53.0`

---

### PanDepth (覆盖度计算)
> 集群文档: http://hpc.ncpgr.cn/app/145-PanDepth/

- 比 samtools 快很多，多线程加速好
- **cram 输入比 bam 更快**
```bash
module load PanDepth/2.21
pandepth -i test.bam -o test1 -t 6
```

---

### Kingfisher (公共测序数据下载)
> 集群文档: http://hpc.ncpgr.cn/app/135-kingfisher/

- 从 EBI ENA/NCBI SRA/Amazon AWS/Google Cloud 下载
- 三种模式：get（下载）、annotate（样本信息）、extract（sra→fastq）
```bash
module load kingfisher/0.3.1
kingfisher get -r SRR12118866 -m ena-ftp
# 或指定多种下载方式自动选最快的
kingfisher get -r ERR1739691 -m ena-ascp aws-http prefetch
```

---

### GROMACS (分子动力学)
> 集群文档: http://hpc.ncpgr.cn/app/121-gromacs/
- 单节点：`mpirun -np $LSB_DJOB_NUMPROC gmx_mpi mdrun -ntomp 1 -noappend`
- 多节点：需 parallel 队列，`-R "span[ptile=25]"` 每节点25核
- GPU版：`module load GROMACS/2018.3-GPU`，需 gpu 队列

---

### AlphaFold3 (蛋白结构预测)
> 集群文档: http://hpc.ncpgr.cn/app/183-alphafold3/

- 需 GPU 队列，**需向管理员申请 GPU 队列使用权限**
- 两步流程：data pipeline（MSA搜索+模板）→ inference（推理输出mmcif）
- 输入为 json 格式，集群中已有权重文件
- data pipeline 阶段可在 CPU 节点运行，仅 inference 需 GPU

---

### RoseTTAFold (蛋白结构预测)
> 集群文档: http://hpc.ncpgr.cn/app/085-RoseTTAFold/

- 精度略低于 AlphaFold，但**内存和时间需求大幅降低**
- 数据库已在 `/share/database/RosettaFold`，可软链接到自己目录
- 集群默认 cuda11.4，使用 `conda env create -f RoseTTAFold-linux.yml`
- PyRosetta 需额外许可证

---

### bgzip + tabix (VCF压缩与快速访问)
> 集群文档: http://hpc.ncpgr.cn/app/124-bgzip/
- bgzip 块压缩 + tabix 索引，支持按区域快速检索，无需解压全文
```bash
module load HTSlib/1.18
bgzip data.vcf              # 压缩 → data.vcf.gz
tabix -p vcf data.vcf.gz    # 建索引 → data.vcf.gz.tbi
tabix data.vcf.gz 11:2343540-2343596  # 快速访问指定区域
```

---

### Genozip (基因组数据压缩)
> 集群文档: http://hpc.ncpgr.cn/app/109-genozip/

- 压缩率为原始大小的 10%~20%，支持 FASTA/VCF/BAM/CRAM
- **学术用户免费**，需申请 license
- **建议用相同版本压缩和解压**
- 使用 `--reference` 参考基因组压缩可获得更高压缩率
- `genozip -@4 file.fq.gz --reference ref.fa`

---

### gzip 文件操作
> 集群文档: http://hpc.ncpgr.cn/app/056-api_read_write_gzip/
- Linux命令：`zcat`/`zless`/`zmore`/`less` 直接读取
- 合并：`cat file1.gz file2.gz > file3.gz`（直接拼接，无需解压）
- 管道处理，无需解压：
```bash
# 按列合并
paste <(gzip -dc file1.gz) <(gzip -dc file2.gz) | gzip > merge.gz
# blastn 直接读gz
blastn -query <(gzip -dc data.fa.gz) -db ./ref -outfmt 6 | gzip > out.gz
```
- Python：`gzip.open("file.gz", "rt")` / `gzip.open("file.gz", "wt")`
- Perl：`open FI, "<:gzip", "file.gz"` / `open FO, ">:gzip", "file.gz"`

---

### ELAI (局部祖源推断)
> 集群文档: http://hpc.ncpgr.cn/app/162-elai/

- 直接处理二倍体数据，无需相位推断，无需重组图谱
- 集群提供多线程版本：`module load Singularity/3.7.3 elai/1.21`
```bash
singularity exec -B $ROOT:/opt/ $IMAGE/debian/debian11.sif /opt/bin/elai-mt \
  -g geno.txt -p 10 -g parv.txt -p 11 -pos pos.txt -s 20 -o chr5 -C 3 -c 20 -mg 6000 -nthreads 4
```

---

### GCC / glibc
> GCC: http://hpc.ncpgr.cn/app/034-gcc/ | glibc: http://hpc.ncpgr.cn/app/095-glibc/
- CentOS7 glibc 为 **2.17**（10年前的版本），越来越多软件不兼容
- 预装GCC：4.8.5, 4.9.2, 5.4.0, 6.2.0, 6.4.0, 7.2.0, 9.4.0, 10.3.0, 11.2.0
- 高版本glibc编译的软件无法在低版本运行 → 用 **singularity容器** 解决
- 查看系统glibc：`ldd --version`

---

### R / RStudio
> R: http://hpc.ncpgr.cn/app/006-R/ | RStudio: http://hpc.ncpgr.cn/app/105-rstudio/
- 推荐优先用 `R/4.0.0`（内置大量R包），无高版本需求时不必换
- R包默认安装：`~/R/x86_64-pc-linux-gnu-library/4.0`
- 部分R包依赖高版本GCC，需先 `module load GCC/x.x.x`
- **RStudio 仅限校内使用**
- 计算节点无联网，R包须在登录节点安装：`install.packages("pkg", lib="~/R/rstudio/4.2/")`
- `rstudio_submit` 提交后用 `bpeek` 获取SSH隧道信息和登录密码

---

### Mamba (快速包管理)
> 集群文档: http://hpc.ncpgr.cn/app/099-mamba/

- C++编写，比 conda 快很多，兼容 conda 命令
- 推荐 **micromamba**（精简版，无需base环境和Python）：
```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
~/bin/micromamba shell init -s bash -p ~/micromamba
```
- 集群已有：`module load micromamba`
- 安装优先级：mamba → singularity → 源码编译

---

### Node.js
> 集群文档: http://hpc.ncpgr.cn/app/146-nodejs/
- CentOS7 需用非官方编译版本（`linux-x64-glibc-217` 后缀）
- `module load nodejs/21.6.0`
- 全局安装权限报错：`export NPM_CONFIG_PREFIX=~/.npm-global`

---

### Rust
> 集群文档: http://hpc.ncpgr.cn/app/153-rust/
- 用户调用 cargo 安装软件需设置 `CARGO_HOME` 到个人目录，否则权限拒绝
```bash
export CARGO_HOME=$HOME/.cargo
module load rust/1.76.0
cargo install ripgrep
export PATH="$HOME/.cargo/bin:$PATH"
```

---

### MySQL
> 集群文档: http://hpc.ncpgr.cn/app/014-mysql-database/
- Server 在 s005 节点，联系管理员获取账号密码
```bash
mysql -uUSERNAME -pPASSWORD -h s005
```

---

### 32位软件
> 集群文档: http://hpc.ncpgr.cn/app/101-run-32bit-software/
```bash
singularity exec -B ${PWD}:/opt/ $IMAGE/centos/centos7_32.sif /opt/32bitprogram -h
```

---

### VSCode Remote-SSH
> 集群文档: http://hpc.ncpgr.cn/app/188-vscode/
- CentOS7 glibc 低，最新版 Remote-SSH 无法使用
- **推荐版本 1.98**，提示"不受支持的OS版本"时点击 Allow，不影响使用
- 禁用自动更新：设置中 Update:Channel → 'manual'
- SSH config 添加 `KbdInteractiveAuthentication yes` 支持二次验证

---

### GitHub / Docker 加速
> 集群文档: http://hpc.ncpgr.cn/app/075-github/
- 代理：ghproxy.com, gh-proxy.com, ghfast.top, wget.la
- 多站加速：https://github.com/xixu-me/Xget
```bash
# 下载
wget https://xget.xi-xu.me/gh/samtools/samtools/releases/download/1.22.1/samtools-1.22.1.tar.bz2
# git clone
git clone https://xget.xi-xu.me/gh/samtools/samtools.git
# docker 镜像
singularity pull docker://docker.m.ixdev.cn/dfam/tetools
```

---

## 常见陷阱速查

| 陷阱 | 影响 | 解决 |
|------|------|------|
| GPU 队列权限 | 未申请权限作业会被拒绝 | 先向管理员申请 GPU 队列使用权限 |
| Parabricks 版本选择 | 新版可能有兼容性问题 | 优先使用 `4.0.1-1` 版本，除非有特殊需求 |
| 软件/数据库可用性查询 | 凭记忆或过时信息回答可能错误 | 实际运行 `mii search` 或 `module av` 查询，或检查 `/share/Singularity/`、`/share/database/` |
| BLAST 核数过多 | CPU利用率低，核多不加速 | blastn 设4~8核即可 |
| faST-LMM 多线程 | 多线程比单线程慢1倍 | **不要用** `-maxThreads`，单线程即可 |
| 多样本多步骤策略 | 未询问用户直接选择策略 | 必须先问：逐步处理 vs 依赖链一次提交 |
| 变异检测选型 | DeepVariant 慢且仅用户主动要求才用 | 默认使用 Parabricks，除非用户明确要求 DeepVariant |
| Bismark `--multicore N` | 实际使用 4N 线程 | 申请核心数设为 4N |
| RepeatModeler `-pa N` | 实际使用 4N 线程 | 申请核心数设为 4N |
| CNVnator | 默认用满整节点 | 必须设置 `MKL_NUM_THREADS`/`OMP_NUM_THREADS` |
| faST-LMM `-maxThreads` | 多线程比单线程慢1倍 | **不要用**，单线程即可 |
| Paragraph `/tmp` | 临时文件积累写满系统盘 | 创建专属tmp目录，运行完清理 |
| BS-Seeker2 `/tmp` | 单作业产生30~70GB临时文件 | 用 `--temp_dir=./tmp` |
| HISAT2 找不到索引 | 不报错不退出，假运行 | `bpeek` 检查作业输出 |
| MAKER FAILED | 程序空跑不停止 | 及时查看日志，出错杀掉重跑 |
| SqueezeMeta 第6步 | IO极慢(~8kb/s) | 用 s001 胖节点本地数据库 |
| CellRanger 慢 | 默认8h | 输出到/tmp + `--no-bam` → 2h |
| FunGAP 权限报错 | 运行时无法访问配置 | 先 `cp -r /opt/conda/config` 到本地 |
| BUSCO 离线 | 计算节点无网络 | 登录节点先下载数据库 |
| InterProScan | 本地运行消耗大量资源 | 用网页API，不消耗计算资源 |
| BLAST blastn | CPU利用率低 | 拆分query多作业并行，线程4~8 |
| NR/NT 公共数据库 | 自己下载并 makeblastdb 浪费时间 | `module load nr/xxx` 后直接用 `$NR` 变量引用，已格式化好 |
| blastx/blastp | 速度慢 | 用 diamond 替代 |
| 比对中间文件 | sam文件占空间大 | 管道直接输出bam，不存sam |
| fq.gz 解压 | 浪费存储和时间 | 比对软件多数直接支持 gz |
| RStudio R包 | 计算节点无法联网安装 | 在登录节点安装到指定目录 |
| Node.js >= 18 | 不支持 CentOS7 | 用 glibc-217 非官方编译版 |
| cargo install | Permission denied | 设 `CARGO_HOME` 到个人目录 |
| CentOS7 glibc 2.17 | 新软件不兼容 | 用 singularity 容器 |
| GitHub 下载慢 | 网络限制 | 用 ghproxy / xget 等加速 |
