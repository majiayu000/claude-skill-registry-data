---
name: ncpgr-bio-router
description: Use when users need bioinformatics analysis on the NCPGR cluster, especially when converting analysis requests into local software choices, resource plans, and LSF job scripts.
trigger: 当用户描述一个完整的生信分析需求（如"帮我做RNA-seq分析"、"变异检测流程"、"基因组组装"）且涉及集群执行时加载本 skill。本 skill 会自动协调 bioSkills、ncpgr-software、ncpgr-lsf 三个 skill。
---

# NCPGR 生信路由

## 用途

本 skill 作为 NCPGR 集群生信分析的路由层，协调三个知识层，不重复它们的细节：

1. `bioSkills`：决定生物学工作流、工具选择、文件格式和方法级参数。
2. `ncpgr-software`：将工作流适配到 NCPGR 的 module、Singularity 镜像、公共数据库、本地软件可用性和资源指导。
3. `ncpgr-lsf`：将计算步骤转化为简洁的 LSF 脚本、提交策略、监控命令和故障排查步骤。

## bioSkills 路径解析

bioSkills 在磁盘上的存储路径为：
`/public/home/software/.claude/skills/bioSkills/`

当 `workflow-map.md` 引用形如 `read-qc/quality-filtering` 的 skill 时，完整路径为：`/public/home/software/.claude/skills/bioSkills/read-qc/quality-filtering/SKILL.md`

在生成分析指导之前，始终使用 Read 工具加载对应的 bioSkill SKILL.md —— 不要仅依赖训练知识。


## 执行顺序

处理 NCPGR 集群生信请求时：

1. 识别分析类型、输入文件、物种/参考基因组、样本数量和预期输出。
2. 加载或查阅对应分析方法的 `bioSkills` 指导。
3. 应用 `ncpgr-software` 本地化软件调用、数据库、容器和资源建议。
4. 应用 `ncpgr-lsf` 生成 `.lsf` 脚本、数组作业、依赖策略和作业监控命令。
5. 返回用户可在集群上运行的本地执行方案。

如果请求仅涉及安装公共软件，使用 `ncpgr-install-software` 而非本 skill。

## 严格模式

当用户请求严格模式（或传入 `--strict`）时，以下规则覆盖所有默认行为：

### 门控规则

**禁止在未读取 bioSkill SKILL.md 的情况下编写或执行该步骤的脚本。**

每个流程步骤在执行前必须通过以下门控：

```
1. 读取该步骤对应的 bioSkill SKILL.md（使用 Read 工具加载文件）
2. 从 SKILL.md 中提取推荐的参数、方法和工具用法
3. 在跟踪日志中记录加载信息：bioSkill 路径、步骤名称、"已加载"、使用的关键参数
4. 然后才能编写该步骤的 LSF/R 脚本
```

如果某步骤没有对应的 bioSkill，记录"未加载 | 无对应bioSkill"后继续。

### 验证清单

每个步骤执行前，用结构化条目确认完成情况：

```
[STRICT] 步骤: <步骤名称>
  bioSkill: <SKILL.md 路径>
  已读取: 是/否
  来自 skill 的关键参数: <列表>
  与 skill 的偏差: <列表或"无">
```

### 严格模式违规

以下行为在严格模式下视为违规：
- 未先读取 bioSkill SKILL.md 就编写该步骤的脚本
- 使用与 bioSkill 矛盾的参数但未记录偏差
- 跳过 workflow-map.md 中为该分析类型列出的 bioSkill

## 优先级规则

1. 用户显式约束覆盖默认值。
2. NCPGR 本地执行规则覆盖通用 `bioSkills` 示例。
3. `bioSkills` 负责生物学正确性和分析逻辑。
4. `ncpgr-software` 负责软件可用性、`module load`、Singularity、数据库路径、队列和资源估算。
5. `ncpgr-lsf` 负责 LSF 脚本结构、提交、监控和作业状态故障排查。

## 冲突规则

- **R 语言版本规则**：所有 LSF 脚本中 R 相关步骤优先使用 `module load R/4.0.0`。R/4.0.0 已内置 clusterProfiler、DESeq2、edgeR、limma、ggplot2、pheatmap 等 758 个包，**这些已内置的包不需要额外执行 `install.packages()` 或 `BiocManager::install()`**。仅当所需包不在 R/4.0.0 内置列表中时，才考虑使用其他 R 版本。
- 优先使用集群提供的 `module` 软件。
- 不要假设软件存在；当可用性重要时，用 `mii search`、`module av`、`/share/Singularity/` 或数据库 module 检查来验证。
- 不要将依赖网络的任务提交到计算节点。下载、包安装和 API 调用在登录节点执行。
- `/share/database/` 下的公共数据库应在合适时复用，而非重建。
- LSF 脚本应保持简洁可读。除非用户明确要求，避免复杂的 shell 元编程。
- 除非平台指导明确要求，不要设置 LSF 内存或时间限制。
- 对普通生信工具使用 `#BSUB -R "span[hosts=1]"`，除非该工具已知支持多节点 MPI。
- 避免在计算作业中使用 `/tmp`，除非工具要求且会自行清理。

## 输出规范

生成分析回答时，应包含：

1. 工作流概述。
2. 所需输入文件和前提假设。
3. 软件/module/数据库检查。
4. 队列和核心数建议。
5. 涉及计算时的 LSF 脚本。
6. 提交、监控和检查命令（参见下方"作业监控清单"）。
7. 结果校验和常见失败点。

对于多样本多步骤工作流，在生成所有脚本之前，询问用户选择逐步提交还是依赖链提交。默认推荐逐步提交，因为更易于检查和恢复。

## 作业监控清单

生成 LSF 脚本后，始终生成针对该工作流定制的监控清单。**不要**重复 `ncpgr-lsf` 中的通用 LSF 命令；重点放在**每个分析步骤需要验证什么**。

### 结构

工作流中的每个步骤，包含：

```
步骤 N: <步骤名称> (作业名: <job_name>)
  查看输出:  bpeek <jobid>
  检查要点:  <该步骤特有的成功/失败标志>
  输出文件:  <预期产出文件及大小范围>
  常见问题:  <该步骤典型的失败模式和解决方法>
```

### 示例：RNA-seq 流程监控

```
步骤 1: 质控 (作业名: fastp)
  查看输出:  bpeek <jobid>
  检查要点:  末尾应出现 "total reads" 统计；过滤后 reads 数不应骤降超过 50%
  输出文件:  *.clean.fastq.gz + *.json 报告
  常见问题:  输入文件路径错误 → PEND 或秒退 EXIT

步骤 2: 比对 (作业名: STAR)
  查看输出:  bpeek <jobid>
  检查要点:  "Uniquely mapped reads %" 应 > 70%（模式生物）；Log.final.out 中 "Number of input reads" 与步骤1一致
  输出文件:  Aligned.sortedByCoord.out.bam (~原始 fq.gz 的 0.5-1 倍大小)
  常见问题:  内存不足 → EXIT，换 smp 队列；索引路径错 → 假运行无输出

步骤 3: 定量 (作业名: featureCounts)
  查看输出:  bpeek <jobid>
  检查要点:  "Successfully assigned" 比例应 > 60%；所有样本的 assigned 比例应大致一致
  输出文件:  counts.txt（行数 ≈ 基因数 + 几行表头）
  常见问题:  GTF 文件与参考基因组版本不匹配 → assigned 比例极低

步骤 4: 差异表达 (作业名: DESeq2)
  查看输出:  bpeek <jobid>
  检查要点:  R 脚本无 Error 或 Warning；MA plot 和火山图正常生成
  输出文件:  diff_results.csv + 质控图
  常见问题:  未使用 R/4.0.0 时可能缺少 DESeq2/clusterProfiler 等内置包 → 优先切换到 R/4.0.0
```

### 编写原则

1. **每一步的"检查要点"必须包含该步骤特有的数值指标**（如比对率、assigned 比例），不能只写"看日志无报错"
2. **输出文件应给出预期大小范围**，帮助用户判断是否正常完成
3. **常见问题应针对该步骤**，不要笼统写"检查内存/核数"
4. 通用 LSF 操作（bjobs 查状态、bkill 终止、bpeek 看输出）由 `ncpgr-lsf` 提供，此处不重复语法

## 常用路由

工作流映射请查阅 `references/workflow-map.md`。该文件包含两层：

1. 覆盖每个 `bioSkills` 场景家族的全量映射表。
2. 常见端到端工作流的详细路由说明。

如果用户请求匹配的 `bioSkills` 场景在详细工作流章节中未覆盖，先通过全量映射表路由，然后查阅对应的 `bioSkills/<family>/<skill>` 指导，再应用 `ncpgr-software` 和 `ncpgr-lsf`。
