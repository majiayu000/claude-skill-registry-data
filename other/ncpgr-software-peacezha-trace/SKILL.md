---
name: ncpgr-software
description: NCPGR高性能计算集群软件使用注意事项与优化指南。聚焦各软件的坑点、加速技巧、资源节省建议与软件选型推荐。当用户询问集群上如何高效使用软件、编写LSF作业、或需要软件选型建议时使用。
trigger: 当用户问题涉及以下任一场景时加载本 skill，并联动加载 ncpgr-lsf：
  1. 提到"集群"、"HPC"、"计算节点"、"登录节点"
  2. 提到 module 命令（module load / module av / module use）或 singularity 容器
  3. 提到 bsub、#BSUB、作业脚本、队列（normal/smp/high/gpu）
  4. 询问某个软件在集群上如何安装、使用、配置、加速、排错
  5. 询问核数、内存、队列选择等资源分配问题
  6. 提到集群路径如 /share/Singularity/、/share/database/、/public/home/
---

# NCPGR HPC 集群软件使用注意事项与优化指南

## 总则

- 集群软件通过 **module** (`module av` / `module load`，http://hpc.ncpgr.cn/app/004-Module/) 或 **singularity**（镜像位于 `/share/Singularity/`，http://hpc.ncpgr.cn/app/007-singularity/）调用
- **有同一软件多版本时，必须用 skill 中明确推荐的版本**，不要自行选最新版。**R 语言尤其重要**：`R/4.0.0` 内置 758 个 R 包（含 clusterProfiler、ggplot2、DESeq2、edgeR、limma、pheatmap、EnhancedVolcano 等），而 `R/4.5.1` 仅有 120 个包。**LSF 脚本中一律写 `module load R/4.0.0`**，不得使用 R/4.5.1 或其他版本，除非用户明确要求
- **禁止为 R/4.0.0 已内置的包执行 `install.packages()` 或 `BiocManager::install()`**。以下包在 R/4.0.0 中已预装，直接使用即可：clusterProfiler、DESeq2、edgeR、limma、ggplot2、pheatmap、EnhancedVolcano、tidyr、dplyr、GO.db、AnnotationDbi、DOSE、enrichplot、org.Hs.eg.db、org.Mm.eg.db、GenomicRanges、DEGreport、clusterProfiler、ReactomePA、pathview、stringdb。如果在写 R 脚本时发现需要 `library(clusterProfiler)` 等，正确做法是 `module load R/4.0.0`，而不是安装这个包
- **R 包系统依赖（.deps.yml）**：R 包可能依赖系统级库（如 HDF5、libpng、GCC 等），这些依赖关系记录在 module 文件旁的 `.deps.yml` 文件中：
  - 路径格式：`/public/home/software/opt/bio/modules/all/R/<版本>.deps.yml`（如 `R/4.0.0.deps.yml`）
  - **使用 R 包前**：在 R 脚本中 `library()` 加载非预装包时，**必须先读取对应的 `.deps.yml` 文件**，检查是否有系统级 module 依赖需要加载。LSF 脚本中也应包含这些 `module load` 命令
  - **其他软件同理**：`/public/home/software/opt/bio/modules/all/` 下其他软件的 module 目录也可能存在 `.deps.yml` 文件，遇到时也应读取参考
  - **安装 R 包后**：如果新安装的 R 包有系统级依赖，应更新或创建对应的 `.deps.yml` 文件记录这些依赖
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
- 编写 LSF 作业脚本时结合 `ncpgr-lsf` skill
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

## 各软件详细注意事项 → `app/_overview.md`

当用户询问某个具体软件的集群使用问题时，按以下步骤查找：

1. **先查阅 `app/_overview.md`** — 包含各软件的坑点、加速技巧、版本推荐和示例脚本
2. **如需更完整信息**，再读取 `app/` 目录下对应的详细文档（如 `app/077-cellranger.md`）

`app/_overview.md` 涵盖以下软件：

| 类别 | 软件 |
|------|------|
| **变异检测/比对** | Parabricks、BWA、HISAT2、BLAST、DeepVariant、GLnexus、HAPpy、Paragraph |
| **质控/定量** | BUSCO |
| **基因组组装/注释** | Trinity、MAKER、RepeatModeler、FunGAP、Augustus、PASA |
| **表观/群体** | Bismark、BS-Seeker2、faST-LMM、CNVnator、OrthoMCL、ELAI |
| **单细胞/宏基因组** | CellRanger、SqueezeMeta、Kraken2 |
| **蛋白结构** | AlphaFold3、RoseTTAFold |
| **分析工具** | PanDepth、InterProScan、HOMER、vg、GROMACS、bgzip/tabix、Genozip、gzip 操作 |
| **开发/环境** | R/RStudio、Mamba、GCC/glibc、Node.js、Rust、MySQL、32位软件、VSCode |
| **下载/加速** | Kingfisher、GitHub/Docker 加速 |

---

## 常见陷阱速查

| 陷阱 | 影响 | 解决 |
|------|------|------|
| **R 版本选错** | R/4.5.1 仅 120 个包，缺 clusterProfiler 等 → 临时安装 30+ 依赖链，极易失败 | **必须用 `module load R/4.0.0`**，已内置 758 个包。**禁止为已内置的包执行 `install.packages()`** |
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
| 使用 R 包时未检查 .deps.yml | R 包运行时找不到系统级库报错 | 使用前先读取 `R/<版本>.deps.yml` 检查系统依赖并 `module load` |
| `GLIBCXX_x.x.x not found` | 运行时 GCC 版本低于编译时版本，程序无法启动 | 在运行环境或 LSF 脚本中加载对应的 GCC module（如 `module load GCC/9.4.0`），详见 http://hpc.ncpgr.cn/cluster/062-FAQ/#9-glibcxx-xxx-not-found |
| Node.js >= 18 | 不支持 CentOS7 | 用 glibc-217 非官方编译版 |
| cargo install | Permission denied | 设 `CARGO_HOME` 到个人目录 |
| CentOS7 glibc 2.17 | 新软件不兼容 | 用 singularity 容器 |
| GitHub 下载慢 | 网络限制 | 用 ghproxy / xget 等加速 |
