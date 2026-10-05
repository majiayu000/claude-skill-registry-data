---
name: wheatomics-query
description: WheatOmics 平台（wheatomics.sdau.edu.cn）数据查询技能。当用户需要查询小麦/麦族基因信息、表达谱、共表达、蛋白互作、同源与共线性、序列获取、BLAST、GO/KEGG 富集、变异数据、文献检索或引物设计时使用。
trigger: 当用户问题涉及小麦（wheat/小麦/普通小麦/麦族/Triticeae）的基因、表达、同源、变异、文献等数据查询，或提到 WheatOmics/wheatomics 平台时加载本技能。
solves: ["小麦基因查询", "表达谱与共表达查询", "同源与共线性分析", "GO/KEGG富集分析", "变异数据查询", "麦族文献检索", "引物设计", "BLAST序列比对"]
related_to: [bio/analysis-report, ncpgr-bio-router]
---

# WheatOmics 数据查询

WheatOmics（https://wheatomics.sdau.edu.cn）是小麦多组学数据平台，提供 REST API（前缀 `/api`，交互式文档 https://wheatomics.sdau.edu.cn/api/docs）。本技能提供：

- 本文件：全部 17 个模块、64 个端点的参数/返回/示例说明；
- 零依赖 CLI：`scripts/wheatomics.py`（仅 Python 标准库，3.8+），覆盖各模块主要端点。

统一约定：

- 响应信封：多数端点返回 `{"success": true, "data": ...}`；CLI 默认把 `data` 部分 pretty-print 到 stdout，`success=false` 时打印错误并以非零码退出。
- 平台地址覆盖：CLI `--base` 参数或环境变量 `WHEATOMICS_BASE`。
- 超时：CLI 默认 30 秒，`--timeout` 覆盖；网络错误给出中文报错。
- 退出码：0 成功；1 接口返回错误（success=false / HTTP 错误）；2 网络或用法错误；4 异步作业等待超时。

---

## 使用铁律（必须遵守，优先级最高）

### 铁律 1：实时核实，禁止臆测

凡回答涉及**具体基因 ID**（如 `TraesCS...`）、**通路 ID**（`GO:...` / KEGG `map...`）、**引用文献**（PMID / DOI）时，**必须实际调用本技能提供的接口实时核实**，严禁凭模型记忆、训练数据印象或"大概是这样"作答。

- 没有真正调用接口并拿到返回结果之前，任何基因 ID、通路 ID、文献信息都**不得当作既成事实**写进结论、报告或对用户的回复；
- 接口返回为空（如 `records: []`、`genes_not_found` 非空）或报错时，**如实告知**"查询无结果 / 接口异常"，绝不允许编造补全基因名、通路名、PMID 或 DOI；
- 本文档中的示例 ID（如 `TraesCS5A02G391700`）来自官方 API 文档，但用于正式回答前仍须实时调用验证其当前有效性。

### 铁律 2：结果自动落地保存

凡产生**可供用户后续引用或复现的查询结果**（基因详情、表达谱、共表达、BLAST、富集分析、变异、文献条目等），**必须默认使用 `-o` 参数写入本地文件**，不得只停留在对话上下文中：

```bash
python scripts/wheatomics.py gene TraesCS5A02G391700 -o wheatomics_results/gene_TraesCS5A02G391700.json
```

- 保存内容为接口返回的**完整 JSON 原始结果**（写盘后 CLI 会打印一行 `已保存: <绝对路径>`）；如需 Markdown 报告，可在 JSON 落地后另行整理生成；
- 输出目录约定：对话中的临时查询 → 当前工作目录下 `wheatomics_results/`；在 HPClaw 流程运行目录（RUN 目录）内执行 → 该 RUN 目录下的 `results/`；
- 写盘后把文件路径一并告知用户，便于后续引用与复现。

---

## CLI 速览

```bash
python scripts/wheatomics.py <子命令> [参数] [-o 输出文件] [--timeout 秒] [--base 平台地址]
```

- GET 类子命令：必填项多为位置参数或命名参数，另支持 `--param KEY=VALUE` 附加任意 query 参数（可重复）；
- POST 类子命令：用命名参数（如 `--genes`、`--padj`）或 `--json '<JSON>' / --json @文件` 构造 JSON body；
- 异步作业（BLAST / PrimerServer2）：`submit` → `status` → `result` 三个动作；`submit --wait` 自动轮询直到完成（上限 `--wait-timeout` 秒，默认 600）；
- 完整子命令列表见文末「CLI 子命令速查表」，或运行 `python scripts/wheatomics.py --help`。

---

## 1. Known Genes 克隆基因检索（4 端点）

已知功能克隆基因数据库的搜索与详情。

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/genes/known/search` | 按关键词模糊搜索克隆基因 |
| GET | `/api/genes/known/all` | 获取全部已知功能基因列表（约 850 条） |
| GET | `/api/genes/known/by-chromosome/{chromosome}` | 列出指定染色体上的克隆基因 |
| GET | `/api/genes/known/{gene_id}` | 单个克隆基因完整信息 |

关键参数：

- `searchid`（query，必填）：搜索关键词，在 gene_id / gene_name / chrom_pos / gene_phenotype / gene_species / paper_doi 多字段中部分匹配；
- `chromosome`（path，必填）：支持 `5A`、`chr5A`、`Chr5A` 等常见格式；
- `gene_id`（path，必填）：如 `TraesCS5A02G391700`。

返回结构：

- search：`{query, total, records: [{gene_id, gene_name, chrom_pos, phenotype, species, dois: [...]}]}`
- 详情：`{gene_id, gene_name, chrom_pos, phenotype, species, paper_title: [...], references: [{doi, title}], key_result: [...], author, submission_date}`

示例：

```bash
python scripts/wheatomics.py known-search VRN1
python scripts/wheatomics.py known-gene TraesCS5A02G391700 -o wheatomics_results/known_VRN-A1.json
curl "https://wheatomics.sdau.edu.cn/api/genes/known/search?searchid=VRN1"
```

## 2. GeneHub 基因详情（1 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/genes/detail/{gene_id}` | 基因标准化详细信息 |

关键参数：`gene_id`（path，必填），**支持 IWGSC v1/v2/v3 三种版本格式**，如 `TraesCS5A02G391700`、`TraesCS5A02G391700.1`、`TraesCS5A03G1158600`。

返回结构：`{query_gene, gene_ids: [v1/v2/v3 对应ID], description, genome, chromosome, start, end, strand, protein_length, molecular_weight, isoelectric_point, functions, jbrowse_links, external_links}`（含 JBrowse 基因组浏览器链接与 Ensembl 外链）。

示例：

```bash
python scripts/wheatomics.py gene TraesCS5A02G391700 -o wheatomics_results/gene_detail.json
```

## 3. PfamSearch 结构域检索（1 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/genes/functions/pfam` | 按 PFAM 结构域搜索基因（gene family） |

关键参数：

- `ID`（query，必填）：PFAM 结构域 ID，以 PF 开头，如 `PF00319`；
- `table`（query，可选，默认 `Genefunc_table`）：查询表，可选 `Genefunc_IWGSC03G_table`。

返回结构：`{table, domain, count, records: [{chromosome, start_mb, end_mb, gene_primary, ...}]}`。

示例：

```bash
python scripts/wheatomics.py pfam PF00319 -o wheatomics_results/pfam_PF00319.json
curl "https://wheatomics.sdau.edu.cn/api/genes/functions/pfam?ID=PF00319"
```

注意：

- 对应网页工具 https://wheatomics.sdau.edu.cn/tools/proteinfamily.html ；
- **实测提醒（2026-08）**：文档默认表 `Genefunc_table` 在当前线上服务已不存在（报 `Unknown gene function table`）。使用前先用 `genefunc-tables` / `genefunc-registry` 查看当前可用表名（中国春如 `Genefunc_CS_IWGSCv1.0_table`、`Genefunc_CS_IWGSC03G_table`），再用 `--table` 显式指定。

## 4. IntervalTool 区间工具（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/genes/functions/interval` | 按染色体区间搜索基因 |
| GET | `/api/genes/functions/tables` | Genefuncdb 全部表名、行数与字段列表 |
| GET | `/api/genes/functions/examples` | 各基因组的示例 Region/Gene ID/Pfam ID |
| GET | `/api/genes/functions/registry` | 已注册基因功能表的元数据 |

关键参数（interval）：

- `ID`（query，必填）：染色体区间，格式 `chr5A:587000000..587200000`；
- `table`（query，可选，默认 `Genefunc_table`）。

返回结构（interval）：`{table, region, count, records: [{chromosome, start_mb, end_mb, gene_primary, ...}]}`；registry 返回 `{count, records: [{table_name, display_name, Subgenome, Polyploidy, chromosome_level, Doi, title, Abstract, example_chr, example_id, ...}]}`。

示例：

```bash
python scripts/wheatomics.py interval "chr5A:587000000..587200000" --table Genefunc_CS_IWGSCv1.0_table
python scripts/wheatomics.py genefunc-registry
```

注意：

- 对应网页工具 https://wheatomics.sdau.edu.cn/tools/intervalTools.html ；
- 服务端表名大小写敏感（Linux MySQL `lower_case_table_names=0`），查询表名须与 registry 中的 `table_name` 完全一致；
- **实测提醒（2026-08）**：文档默认表 `Genefunc_table` 在当前线上服务已不存在（报 `Unknown gene function table`）。使用前先用 `genefunc-tables` / `genefunc-registry` 查看当前可用表名（中国春如 `Genefunc_CS_IWGSCv1.0_table`、`Genefunc_CS_IWGSC03G_table`），再用 `--table` 显式指定。

## 5. Expression 表达谱（2 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/expression/projects` | 获取可用表达谱项目列表 |
| GET | `/api/expression/query` | 查询基因在指定项目中的表达量 |

关键参数（query）：

- `gene_ids`（query，必填）：逗号分隔的基因 ID 列表；
- `project`（query，可选，默认 `PRJEB5314_paired_tbl`）：表达项目表名，如 `PRJEB25639_tbl`、`ABA_JA_6BA_DMSO3h_mean_tbl`。

返回结构：`{project, genes_found, genes_not_found, genes_converted, results: [{gene_id, project, points: [{label, value, std, error_bar}]}]}`（points 为各实验条件下的表达量点数据，含误差棒）。

⚠️ 基因 ID 版本说明（重要）：

- 表达量数据基于**中国春 IWGSC v2.1 注释**（基因 ID 含 `02G` 格式）；
- 输入 v1（`01G`）或 v3（`03G`）格式的 ID 时，API **自动转换为 v2 后再查询**，转换结果记录在响应的 `genes_converted` 字段；
- 转换失败则按原始 ID 查询，大概率返回"基因未找到"（出现在 `genes_not_found`）。

示例：

```bash
python scripts/wheatomics.py expr-projects -o wheatomics_results/expr_projects.json
python scripts/wheatomics.py expr-query --genes TraesCS5A02G391700 --project PRJEB5314_paired_tbl
curl "https://wheatomics.sdau.edu.cn/api/expression/query?gene_ids=TraesCS5A02G391700&project=PRJEB5314_paired_tbl"
```

## 6. Coexpression 共表达（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/coexpression/databases` | 可用共表达数据库列表 |
| GET | `/api/coexpression/query` | 查询基因的共表达关系对 |
| GET | `/api/coexpression/projects` | bioproject 元数据列表 |
| GET | `/api/coexpression/projects/{accession}` | 单个 bioproject 元数据（不存在则 404） |

关键参数（query）：

- `gene_ids`（query，必填）：逗号分隔的基因 ID 列表；
- `database`（query，可选，默认 `CO_PRJEB25639`）：共表达数据库 ID，来自 databases 端点（如 `CO_result2`、`CO_PRJEB25639`）；
- `filter_value`（query，可选，默认 `300`）：**两种筛选模式**——小数（如 `0.8`）按 PCC 筛选，返回 `|PCC| >= filter_value`；整数（如 `5`）按 MR（Mutual Rank）筛选，返回 `MR <= filter_value`。

projects 参数：`source`（可选，NCBI/ENA/CNGB 过滤）、`q`（可选，标题/描述/物种子串模糊搜索）。

示例：

```bash
python scripts/wheatomics.py coexpr-databases
python scripts/wheatomics.py coexpr-query --genes TraesCS5A02G391700 --database CO_PRJEB25639 --filter 0.9   # PCC 模式
python scripts/wheatomics.py coexpr-query --genes TraesCS5A02G391700 --filter 5                              # MR 模式
python scripts/wheatomics.py coexpr-project PRJNA976214
```

## 7. PPI 蛋白互作（1 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/ppi/query` | 查询蛋白质互作关系（wheatPPI） |

关键参数：

- `gene_ids`（query，必填）：逗号分隔的**转录本 ID**（基因 ID 加 `.1` 后缀），如 `TraesCS6D02G084800.1`；
- `table`（query，可选，默认 `PPI_result`）；
- `min_score`（query，可选，默认 `0.5`）：CF-MS 互作得分阈值，`0.5` 中等置信度、`0.2` 低置信度、`0` 不筛选返回全部。

返回结构：互作对记录，含互作双方基因 ID、eggNOG ID、功能注释和互作得分 Score。

⚠️ 注意：本模块基于中国春 IWGSC v2.1 注释；**输入不带 `.1` 后缀的基因 ID 将匹配不到结果**。

示例：

```bash
python scripts/wheatomics.py ppi --genes TraesCS6D02G084800.1 --min-score 0.5
curl "https://wheatomics.sdau.edu.cn/api/ppi/query?gene_ids=TraesCS6D02G084800.1&table=PPI_result&min_score=0.5"
```

## 8. 比较基因组：homologs / synteny / id-conversion / blastp（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/homologs/wheat-rice-arabidopsis` | 小麦基因在水稻和拟南芥中的同源基因 |
| GET | `/api/synteny/search` | 小麦与其他麦族物种的共线性信息 |
| GET | `/api/id-conversion` | 旧版本基因 ID 转换为 IWGSC v1.1（02G） |
| GET | `/api/blastp` | 小麦族蛋白预计算 blastp 结果 |

关键参数：

- homologs：`gene_id`（必填，小麦或其他物种基因 ID）；`max_targets`（可选，默认 3，范围 1-100，每个物种返回上限）。返回 `{query_gene, count, hits: [{target_gene, description, Qcovs, Identity, E-value, Score, ...}]}`；
- synteny：`ID`（必填，**两种模式**：基因组区间 `chr5A:100000-200000` 或单个基因 ID 精确查找）；`table`（可选，默认 `CSsymaptbl`）。结果为每个基因在 Chinese Spring、Durum wheat、Wild emmer、Triticum urartu、Aegilops tauschii 中的共线性对应关系；
- id-conversion：`ID`（必填，**转录本 ID 带 `.1` 后缀**，多基因用 URL 编码换行 `%0D%0A` 分隔，CLI 用 `--ids` 逗号分隔自动处理）；`gene_version`（必填，三选一）：`MIPS_result`（MIPS v2.2，如 `Traes_1AS_E6058767A.1`）/ `TGACv1_result`（如 `TRIAE_CS42_6BL_TGACv1_501926_AA1621570.1`）/ `IWGSCv1_result`（IWGSC v1.0，如 `TraesCS6B01G342500.1`）。返回每个基因的映射结果（`reference_gene` 为 02G 格式、`code`、`length`），未找到的列在 `not_found`；
- blastp：`gene`（必填）；`limit`（可选，默认 5000）；`offset`（可选，默认 0）。在 `all_protein_blastp` 表中同时匹配 query_id 和 subject_id，自动处理带 `.1`、`transcript:` 前缀、`.cds` 后缀等多种 ID 格式，结果按 bit_score 降序、evalue 升序排列。可用于同源基因搜索或不同基因组版本/材料间的基因 ID 转换。

示例：

```bash
python scripts/wheatomics.py homologs TraesCS5A02G391700 --max-targets 3
python scripts/wheatomics.py synteny TraesCS5A02G391700
python scripts/wheatomics.py id-conversion --ids TraesCS6B01G342500.1 --version IWGSCv1_result
python scripts/wheatomics.py blastp TraesCS5A02G391700 --limit 100
```

## 9. OrthoFinder（3 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/orthofinder/search` | 按蛋白 ID / orthogroup ID 搜索，物种目录，OG 成员 |
| GET | `/api/orthofinder/download` | 下载基因树（Newick）或多序列比对（FASTA） |
| GET | `/api/orthofinder/neighborhood` | 基因上下游邻居及同源簇信息 |

关键参数：

- search：`action`（可选，默认 `search`）：`search` / `species_catalog` / `members`；`q`（action=search 时的蛋白/基因/OG ID）；`og`（action=members 必填的 Orthogroup ID）；`sub`（可选，亚基因组过滤 A/B/D，配合 members）；`species`（可选，物种过滤）；
- download：`og`（必填，如 `OG0001897`）；`type`（可选，默认 `tree`，可选 `alignment`）；`cluster`（可选，1-7，0=完整 OG）；`type_tree`（可选，`type1`/`type2`，仅 cluster 下载）。返回文件内容（非 JSON）；
- neighborhood：`q`（必填，基因 ID，如 `TraesCS1A02G219700.1`）。返回查询基因 + 上下游各 5 个邻居（共 11 个基因）在 OrthoFinder 分析所有基因组中的 cluster 归属。

示例：

```bash
python scripts/wheatomics.py orthofinder --q TraesCS5A02G391700
python scripts/wheatomics.py orthofinder --action members --og OG0001897 --sub A
python scripts/wheatomics.py orthofinder-download --og OG0001897 --type tree -o wheatomics_results/OG0001897.nwk
python scripts/wheatomics.py orthofinder-neighborhood TraesCS1A02G219700.1
```

## 10. SynTeny Viewer（5 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/syntenyview/genomes` | 可用基因组列表 |
| GET | `/api/syntenyview/gene-search` | 基因搜索 |
| GET | `/api/syntenyview/status` | 服务状态 |
| GET | `/api/syntenyview/triticeae` | 麦族数据 |
| GET | `/api/syntenyview/neighborhood` | 基因邻域共线性 |

关键参数：

- gene-search：`q`（必填）；`limit`（可选，默认 20）；
- neighborhood：`q`（必填，基因 ID）；`upstream`（可选，默认 5）；`downstream`（可选，默认 5）；`targets`（可选，逗号分隔的目标基因组标签）；`window`（可选，默认 5）。

示例：

```bash
python scripts/wheatomics.py syntenyview-genomes
python scripts/wheatomics.py syntenyview-gene-search TraesCS5A02G391700
python scripts/wheatomics.py syntenyview-neighborhood TraesCS5A02G391700 --upstream 5 --downstream 5
```

## 11. Sequences 序列获取（3 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/sequence/by-gene` | 按基因 ID 取基因（CDS）和蛋白序列（FASTA） |
| GET | `/api/sequence/by-interval` | 按染色体区间取基因组 FASTA |
| GET | `/api/sequence/batch` | 批量取多个基因/区间的 FASTA |

关键参数：

- by-gene：`gene_id`（必填，如 `TraesCS5A02G391700`；不以 `.1` 结尾时自动追加 `.1` 查找）；`gene_db`（可选，默认 `all_gene`）；`protein_db`（可选，默认 `all_protein`）。返回 `{gene_id, gene_sequence: ">...\nATG...", protein_sequence: ">...\nMAG..."}`；
- by-interval：`region`（必填，如 `chr1A:200-500`）；`database`（必填，区间查询推荐聚合库 `all_genomes`；另可选 `all_gene` / `all_protein`）。⚠️ 染色体命名随基因组而异：`Chr1A_Abo:200-500`（Abbondanza）、`chr1A:200-500`（Chinese Spring）、`chr1H_Barley3:200-500`（大麦 v3）、`chr1D_Aegilops_tauschii_TA1675:200-500`、`chr1A_Wild_emmer:200-500`（野生二粒小麦），完整列表见 https://wheatomics.sdau.edu.cn/doc/getsequence_search.txt ；全部库名见 `blast-databases`；
- batch：`ID`（必填，空格分隔多个基因 ID 或区间，URL 中可用 `%20` 或 `+`；CLI 用 `--ids` 逗号/空格分隔自动处理）；`database`（必填）。基因 ID 自动补 `.1`，区间格式 `chr:start-end`。返回 `{database, records: [{sequence_id, fasta}]}`。

示例：

```bash
python scripts/wheatomics.py seq-gene TraesCS5A02G391700 -o wheatomics_results/seq_VRN-A1.json
python scripts/wheatomics.py seq-interval --region chr1A:200-500 --database all_genomes
python scripts/wheatomics.py seq-batch --ids "TraesCS5A02G391700,TraesCS5A02G391701" --database all_gene
```

## 12. BLAST 异步比对（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| POST | `/api/blast/search` | 提交 BLAST 搜索（表单），结果生成下载链接 |
| GET | `/api/blast/status/{job_id}` | 轮询作业状态（wait=false 提交的 job） |
| GET | `/api/blast/databases` | 可用数据库列表（按蛋白/核酸分组） |
| GET | `/api/blast/status` | 检查 BLAST 环境 |

⚠️ 异步作业说明：所有 job 由独立的 blast daemon 执行，不受 API worker 回收/重启影响。表单字段 `wait=true`（服务端默认）时提交后由服务端轮询到完成直接返回 download_url；`wait=false` 立即返回 `job_id`，再轮询 status。**CLI 固定以 `wait=false` 提交并自行轮询**（`blast submit ... --wait`），避免长任务撑爆单次 HTTP 超时。

提交表单字段（application/x-www-form-urlencoded）：

- `database`（必填）：数据库名，多个用逗号分隔，如 `Fielder_protein,AK58_protein.fasta`；
- `query`（必填）：FASTA 格式查询序列（CLI 支持 `--query @文件`）；
- `program`（可选，默认 `blastp`）：blastp / blastn / blastx / tblastn / tblastx；
- `evalue`（可选，默认 10，范围 0-1000）；`max_target_seqs`（可选，默认 1000，范围 1-50000）；
- `word_size`、`matrix`（可选）；`outfmt`（可选，默认 `tabular`，另有 `traditional` / `both`）。

状态返回：`{success, job_id, status: pending|running|done|error|stale, message, download_urls}`；`done` 时 `download_urls` 填充，`error`/`stale` 看 `message`。⚠️ `job_id` 必须为 uuid4 格式，否则 404。

示例：

```bash
python scripts/wheatomics.py blast-databases --program blastp
python scripts/wheatomics.py blast submit --database Fielder_protein --query @seq.fa --wait -o wheatomics_results/blast_job.json
python scripts/wheatomics.py blast status <job_id>
python scripts/wheatomics.py blast result <job_id>
curl -X POST "https://wheatomics.sdau.edu.cn/api/blast/search" -d "program=blastp" -d "database=Fielder_protein" --data-urlencode "query=>test
MSSSTG..."
```

## 13. GO/KEGG 富集（4 端点，POST）

| 方法 | 路径 | 用途 |
|------|------|------|
| POST | `/api/go-kegg/go` | GO 富集分析 |
| POST | `/api/go-kegg/kegg` | KEGG 通路富集分析 |
| GET | `/api/go-kegg/go-genes` | 查询列表中匹配某 GO term 的基因 |
| GET | `/api/go-kegg/kegg-genes` | 查询列表中匹配某 KEGG 通路的基因 |

请求体（JSON）：`{"genes": ["TraesCS1A02G045300.1", ...], "padj_threshold": 0.05}`，`genes` 必填，`padj_threshold` 默认 0.05。

统计方法与背景：

- 超几何检验 + Benjamini-Hochberg FDR 多重检验校正；
- GO 背景集：`wheat_function.gene_go` 中所有有 GO 注释的基因；KEGG 背景集：`wheat_function.gene_kegg`，映射链 gene_id → KO → pathway；
- ⚠️ 输入基因 ID 为 **IWGSC RefSeq v1.1** 格式（如 `TraesCS1A02G045300.1`，带 `.1` 转录本后缀）。

返回结构：`{N, n, gene_count, results: [{id, term, ontology, k, K, ratio, pvalue, padj}]}`（N=背景基因数，n=输入有效基因数，K=背景中该 term 基因数，k=输入中命中数）。

go-genes / kegg-genes 参数：`go_id` / `pathway`（必填），`genes`（可选，逗号分隔的查询列表）。

示例：

```bash
python scripts/wheatomics.py enrich-go --genes TraesCS1A02G045300.1,TraesCS1A02G104700.1,TraesCS1A02G118400.1 -o wheatomics_results/go_enrich.json
python scripts/wheatomics.py enrich-kegg --json '{"genes": ["TraesCS1A02G045300.1"], "padj_threshold": 0.05}'
python scripts/wheatomics.py go-genes GO:0043425 --genes TraesCS1A02G045300.1
```

## 14. VariantHub 变异数据（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/VariantHub/datasets` | VCF 数据集列表（按参考基因组分组） |
| GET | `/api/VariantHub/dataset_info` | 数据集的 VCF 头（## meta 行）与样本 ID |
| GET | `/api/VariantHub/samples` | 数据集样本元数据（可按字段过滤） |
| GET | `/api/VariantHub/query` | 按基因组区间或变异 ID 查询变异 |

关键参数：

- dataset_info / samples / query 均需 `dataset`（数据集 key，来自 datasets 端点）；
- samples：**任意额外 query 参数视为元数据过滤**（精确匹配、不区分大小写），如 `&country=Turkey&status=Landrace` 或 `&group=LR`（CLI 用 `--param country=Turkey`）；
- query：`region`（如 `chr1A:1000-50000`）与 `variant_id`（ID 列精确匹配）**二选一必填**；`samples`（可选，逗号分隔样本 ID，缺省全部）；`limit`（默认 200）、`offset`（默认 0）。

⚠️ 注意：region 查询走 tabix 索引（快）；variant_id 查询是全文件扫描，大群体 VCF 上可能很慢；`samples` 显式指定与元数据过滤两种方式互斥。

示例：

```bash
python scripts/wheatomics.py variant-datasets
python scripts/wheatomics.py variant-dataset-info <dataset_key>
python scripts/wheatomics.py variant-samples <dataset_key> --param country=Turkey
python scripts/wheatomics.py variant-query <dataset_key> --region chr1A:1000-50000 --limit 200
```

## 15. Triticeae Papers 文献（4 端点）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/papers` | 搜索麦族论文元数据 |
| GET | `/api/papers/{pubmedid}` | 按 PMID 取单篇论文元数据 |
| GET | `/api/papers/{pmid}/annotation` | 按 PMID 取 LLM 细粒度标注 |
| GET | `/api/papers/stats` | 数据集聚合统计 |

关键参数（/api/papers，均为可选）：

- `q` 全文关键词（title/abstract/journal/authors/pubmed_keywords/ai_tags/function_gene_tags）；`title` / `abstract` / `journal` / `authors` / `pubmed_keywords` / `ai_tags` / `function_gene_tags` / `gene_name` 字段级模糊匹配；`pmid` 精确匹配；
- `functional_gene_flag` / `functional_gene_source` / `function_gene_flag` 论文级功能基因标记过滤；
- `pub_date_start` / `pub_date_end` 发布年份范围；`since_days` 按**入库时间**（papers.created_at）过滤最近 N 天（用于"本周新增论文"）；
- `limit`（默认 20）、`offset`（默认 0）；默认排序 paper_created_at DESC（最近入库优先）；
- **NOT 语义**：所有文本参数支持 `<参数>_exclude` 形式（如 `q_exclude`、`title_exclude`），CLI 用 `--param q_exclude=xxx` 传递。

annotation 返回：标注层全部字段（is_functional_gene, confidence, gene_name, gene_type, trait_label, function_summary, evidence_type, new_tags, llm_reason, source_method, review_status 等）；无论文标注时返回 `has_annotation: false`。stats 返回年份分布、期刊 top-20、AI 标签 top-30、功能基因比例、审核状态分布。

示例：

```bash
python scripts/wheatomics.py papers --q "vernalization" --limit 20 -o wheatomics_results/papers_vrn.json
python scripts/wheatomics.py papers --gene-name VRN1 --pub-date-start 2020
python scripts/wheatomics.py paper 42105133
python scripts/wheatomics.py paper-annotation 42105133
python scripts/wheatomics.py papers-stats
```

## 16. PrimerServer2 引物设计（12 端点，异步作业）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/PrimerServer2/config` | 公共配置（输入限制、系统标志） |
| GET | `/api/PrimerServer2/databases` | 可用特异性检查数据库（分组、文件名与别名） |
| GET | `/api/PrimerServer2/server-info` | 服务器时间与外部工具版本（samtools/blastn/primer3） |
| POST | `/api/PrimerServer2/jobs` | 提交引物设计+特异性检查作业，返回 jobId |
| POST | `/api/PrimerServer2/jobs/check` | 提交仅特异性检查作业，返回 jobId |
| GET | `/api/PrimerServer2/jobs/{job_id}` | 作业状态与元数据 |
| DELETE | `/api/PrimerServer2/jobs/{job_id}` | 终止并删除作业 |
| GET | `/api/PrimerServer2/jobs/{job_id}/progress` | 完成百分比与当前阶段 |
| GET | `/api/PrimerServer2/jobs/{job_id}/result` | 最终结果（`job_type=design` 或 `check`） |
| POST | `/api/PrimerServer2/jobs/cleanup` | 手动清理过期作业目录 |
| GET | `/api/PrimerServer2/jobs/{job_id}/result-html` | 原始 HTML 结果页 |
| GET | `/api/PrimerServer2/jobs/{job_id}/specificity/{filename}` | 下载特异性结果文件（如比对图） |

⚠️ 异步作业流程：提交返回 `jobId`（UUID）→ 轮询 `jobs/{job_id}`（status: `pending/running/done/error/stopped`）或 `progress`（`{total, finished, percent, stage}`）→ `result` 取结果。CLI `primer submit --wait` 自动完成全流程。各端点支持可选请求头 `x-api-key`（CLI `--api-key`）。

设计作业请求体（DesignJobRequest，JSON）关键字段：

- 必填：`app-type: "design"`、`selectTemplate`（模板数据库名，如 `primer_Chinese_Spring2.1.genome`，或 `custom` 配合 `custom-template-sequences`）；
- `template-regions`（selectTemplate 非 custom 时必填）：每行一个区域 `TemplateID TargetPos TargetLength [ProductSizeMin] [ProductSizeMax]`；
- `selected-databases`：特异性检查库文件名列表（来自 databases 端点），默认 `["primer_Chinese_Spring2.1.genome"]`；可含 `custom` 配合 `custom-db-sequences`；
- 产物与位点：`product_size_min`（默认 100）/ `product_size_max`（默认 1000）、`region_type`（默认 `SEQUENCE_TARGET`，另有 `SEQUENCE_INCLUDED_REGION` / `FORCE_END`）；
- Primer3 参数（默认值）：`PRIMER_MIN_SIZE=18 / PRIMER_OPT_SIZE=20 / PRIMER_MAX_SIZE=23`、`PRIMER_MIN_TM=57 / PRIMER_OPT_TM=60 / PRIMER_MAX_TM=63`、`PRIMER_PAIR_MAX_DIFF_TM=3`、`PRIMER_MIN_GC=35 / PRIMER_OPT_GC_PERCENT=50 / PRIMER_MAX_GC=65`、`PRIMER_NUM_RETURN=30` 等；
- 特异性检查参数（默认值）：`size_start=50`、`size_stop=5000`、`min_Tm_diff=20`、`retain=10`、`blast_e_value=30000`、`blast_word_size=7`、`blast_identity=60`。

检查作业请求体（CheckJobRequest）：必填 `app-type: "check"`、`check-primers`（每行一组 `PrimerID LeftSeq RightSeq [AdditionalSeq ...]`），其余特异性参数同上。

示例（提交 JSON 可用 `--json @文件` 从文件读取）：

```bash
python scripts/wheatomics.py primer-config
python scripts/wheatomics.py primer-databases
python scripts/wheatomics.py primer submit --json '{
  "app-type": "design",
  "selectTemplate": "primer_Chinese_Spring2.1.genome",
  "template-regions": "chr1A 100000 200\nchr1B 200000 300 150 800",
  "selected-databases": ["primer_Chinese_Spring2.1.genome"],
  "product_size_min": 150,
  "product_size_max": 800
}' --wait -o wheatomics_results/primer_design.json
python scripts/wheatomics.py primer submit-check --json '{"app-type": "check", "check-primers": "Primer1 TTCGATGCTGAGGAAGGCTG AGGAGAGAACGGAGACGAAG"}' --wait
python scripts/wheatomics.py primer status <jobId>
python scripts/wheatomics.py primer result <jobId> --job-type design
```

## 17. 平台信息（about / health / track）

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/about` | 应用名称、版本、文档地址、API 前缀、服务器时间 |
| GET | `/api/health` | 服务健康检查（探活/监控） |
| POST | `/api/track/visit` | 记录一次页面访问（同一 ip+UA 当日幂等），body `{"page": "..."}` |
| GET | `/api/track/stats` | 公开访问统计：今日 PV/UV、累计 PV/UV、当前在线 |

示例：

```bash
python scripts/wheatomics.py health
python scripts/wheatomics.py about
python scripts/wheatomics.py track-stats
```

---

## CLI 子命令速查表

| 子命令 | 对应端点 | 说明 |
|--------|----------|------|
| `about` | GET /api/about | 应用基本信息 |
| `health` | GET /api/health | 健康检查 |
| `track-stats` | GET /api/track/stats | 访问统计 |
| `known-search <关键词>` | GET /api/genes/known/search | 克隆基因模糊搜索 |
| `known-all` | GET /api/genes/known/all | 全部克隆基因 |
| `known-chrom <5A>` | GET /api/genes/known/by-chromosome/{chr} | 按染色体列出 |
| `known-gene <gene_id>` | GET /api/genes/known/{gene_id} | 克隆基因详情 |
| `gene <gene_id>` | GET /api/genes/detail/{gene_id} | GeneHub 基因详情（v1/v2/v3） |
| `pfam <PF00319> [--table]` | GET /api/genes/functions/pfam | PFAM 结构域搜基因 |
| `interval <chr:start..end> [--table]` | GET /api/genes/functions/interval | 区间搜基因 |
| `genefunc-tables` | GET /api/genes/functions/tables | Genefuncdb 表信息 |
| `genefunc-examples` | GET /api/genes/functions/examples | 各基因组示例 |
| `genefunc-registry` | GET /api/genes/functions/registry | 功能表注册元数据 |
| `expr-projects` | GET /api/expression/projects | 表达项目列表 |
| `expr-query --genes ... [--project]` | GET /api/expression/query | 表达量查询（02G 自动转换） |
| `coexpr-databases` | GET /api/coexpression/databases | 共表达库列表 |
| `coexpr-query --genes ... [--database] [--filter]` | GET /api/coexpression/query | 共表达查询（PCC/MR） |
| `coexpr-projects [--source] [--q]` | GET /api/coexpression/projects | bioproject 列表 |
| `coexpr-project <accession>` | GET /api/coexpression/projects/{acc} | 单个 bioproject |
| `ppi --genes <.1 ID> [--min-score]` | GET /api/ppi/query | 蛋白互作查询 |
| `homologs <gene_id> [--max-targets]` | GET /api/homologs/wheat-rice-arabidopsis | 水稻/拟南芥同源基因 |
| `synteny <基因ID或区间> [--table]` | GET /api/synteny/search | 麦族共线性 |
| `id-conversion --ids ... --version ...` | GET /api/id-conversion | 旧版 ID 转 02G |
| `blastp <gene_id> [--limit] [--offset]` | GET /api/blastp | 预计算 blastp 结果 |
| `orthofinder [--q] [--action] [--og] [--sub]` | GET /api/orthofinder/search | OrthoFinder 搜索 |
| `orthofinder-download --og ... [--type]` | GET /api/orthofinder/download | 下载基因树/比对 |
| `orthofinder-neighborhood <gene_id>` | GET /api/orthofinder/neighborhood | 邻居基因与同源簇 |
| `syntenyview-genomes` | GET /api/syntenyview/genomes | 基因组列表 |
| `syntenyview-gene-search <q> [--limit]` | GET /api/syntenyview/gene-search | 基因搜索 |
| `syntenyview-status` | GET /api/syntenyview/status | 服务状态 |
| `syntenyview-triticeae` | GET /api/syntenyview/triticeae | 麦族数据 |
| `syntenyview-neighborhood <gene_id> [...]` | GET /api/syntenyview/neighborhood | 邻域共线性 |
| `seq-gene <gene_id> [--gene-db] [--protein-db]` | GET /api/sequence/by-gene | 基因+蛋白 FASTA |
| `seq-interval --region ... --database ...` | GET /api/sequence/by-interval | 区间基因组 FASTA |
| `seq-batch --ids ... --database ...` | GET /api/sequence/batch | 批量 FASTA |
| `blast-databases [--program]` | GET /api/blast/databases | BLAST 库列表 |
| `blast-env` | GET /api/blast/status | 检查 BLAST 环境 |
| `blast submit --database ... --query ... [--wait]` | POST /api/blast/search | 提交 BLAST（异步） |
| `blast status <job_id>` | GET /api/blast/status/{job_id} | 轮询 BLAST 状态 |
| `blast result <job_id>` | GET /api/blast/status/{job_id} | 取 BLAST 结果（download_urls） |
| `enrich-go --genes ... [--padj]` | POST /api/go-kegg/go | GO 富集 |
| `enrich-kegg --genes ... [--padj]` | POST /api/go-kegg/kegg | KEGG 富集 |
| `go-genes <GO:...> [--genes]` | GET /api/go-kegg/go-genes | GO term 命中基因 |
| `kegg-genes <pathway> [--genes]` | GET /api/go-kegg/kegg-genes | 通路命中基因 |
| `variant-datasets` | GET /api/VariantHub/datasets | VCF 数据集列表 |
| `variant-dataset-info <dataset>` | GET /api/VariantHub/dataset_info | VCF 头与样本 |
| `variant-samples <dataset> [--param k=v]` | GET /api/VariantHub/samples | 样本元数据 |
| `variant-query <dataset> (--region|--variant-id)` | GET /api/VariantHub/query | 变异查询 |
| `papers [--q] [--limit] [...]` | GET /api/papers | 论文搜索 |
| `paper <pmid>` | GET /api/papers/{pmid} | 单篇论文元数据 |
| `paper-annotation <pmid>` | GET /api/papers/{pmid}/annotation | LLM 标注 |
| `papers-stats` | GET /api/papers/stats | 聚合统计 |
| `primer-config` | GET /api/PrimerServer2/config | 服务器配置 |
| `primer-databases` | GET /api/PrimerServer2/databases | 特异性检查库 |
| `primer-server-info` | GET /api/PrimerServer2/server-info | 运行时信息 |
| `primer submit --json ... [--wait]` | POST /api/PrimerServer2/jobs | 提交设计作业 |
| `primer submit-check --json ... [--wait]` | POST /api/PrimerServer2/jobs/check | 提交检查作业 |
| `primer status <jobId>` | GET /api/PrimerServer2/jobs/{id} | 作业状态 |
| `primer progress <jobId>` | GET .../jobs/{id}/progress | 作业进度 |
| `primer result <jobId> [--job-type]` | GET .../jobs/{id}/result | 作业结果 |
| `primer delete <jobId>` | DELETE /api/PrimerServer2/jobs/{id} | 终止并删除 |
| `primer result-html <jobId>` | GET .../jobs/{id}/result-html | HTML 结果页 |

通用选项（所有子命令）：`-o/--output 文件`（完整 JSON 写盘，自动建父目录）、`--timeout 秒`（默认 30）、`--base 地址`（或环境变量 `WHEATOMICS_BASE`）、`--api-key`（x-api-key 请求头）、`--param KEY=VALUE`（附加 query 参数，可重复）。
