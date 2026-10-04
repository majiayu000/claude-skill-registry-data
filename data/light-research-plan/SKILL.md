---
name: light-research-plan
description: 对已确认可行的 idea 制定极其详细的研究方案、实验设计与执行规划。当用户的 idea 已通过 m04 审查、需要把 idea 拆成可执行可复现的完整科研流程时使用。覆盖研究目标、技术路线、数据流程、实验/消融/敏感性/鲁棒性/显著性检验、时间安排、风险与备选，并保证全程可复现。
---

# 研究方案与实验执行规划

## 前置
仅对 m04 已放行的 idea 执行。开工前确认数据(m02)与方法(db03)就绪。

## 方案内容（逐项写实，不写空话）
1. **研究目标 & 核心问题**：可证伪的假设 H1/H2…。验证性研究（事先有假设要检验）可做**预注册**锁定假设/主指标/分析计划，防 HARKing/p-hacking；探索性分析须在论文里如实区分、不包装成验证（最小流程与字段映射见 references「预注册」节，样本量依据复用功效分析）。
2. **技术路线**：整体框架图（交 m09/m11），关键模块与数据流。
3. **数据**：来源、处理流程(引 m02 流水线)、划分方式、统计。
4. **模型/方法**：算法流程、公式、伪代码、复杂度。
5. **实验设计**：每个实验条目按 EXP-Bench 四要素写全 —— 研究问题(对应哪条假设)、设计(自/因/控变量+数据集+baseline+指标)、实现(代码+运行配置)、结论判定(用什么结果回答该假设)。"设计"和"结论"最易跑偏，重点核。
   - 主实验：任务、数据集（来自 db04，**分层取用**：规模/划分等事实信本地卡；被引/license/下载链接是薄缓存，开工前跑 `databases/db04-datasets/scripts/dataset_signal.py` 按 citation 锚点 oa_id=/doi= 实时校验、**冲突信在线**，本地快照仅无网降级；bias_risk/known_issues 按本项目方向读 `domain_scope=` 子串过滤，方向外偏科判断不当通用坑预判）、baselines/评价指标（来自 db03，**分层取用**：common_baselines/evaluation_metrics/core_assumption 等方法论留本地直接取；representative_papers 的 cited 是薄缓存，要最新被引跑 `databases/db03-methods/scripts/method_signal.py` 按 doi 锚点实时查、**冲突信在线**；maturity 的"过时/被替代"判断读其括号内域限定，按本项目方向经 `domain_scope=` 过滤，别把 CV 时间线判断套到非 CV 方法）。划分遵 m02 命名锚点 SPLIT-01/02、LEAK-01。
   - 消融实验：逐个移除创新组件，证明贡献来源。
   - 对比实验：与 SOTA 公平比较（同数据/同设置）。
   - 参数敏感性：关键超参网格 + 趋势分析。用 Hydra multirun（`-m lr=0.01,0.1 model=a,b` 笛卡尔积）或 W&B Sweeps（method=grid/random/bayes + metric goal + parameters）系统扫参。
   - 泛化测试：跨数据集/跨域/跨规模。
   - 鲁棒性：噪声/对抗/缺失/分布漂移。
   - 统计显著性：**≥5 个随机种子；算力受限 ≥3 且须在 m06 报告显式标注**（与 m06 必查清单同口径）；推断用 statsmodels（OLS/Logit，看 summary 的 p 值与 95% 置信区间，记得 `add_constant`）或 scipy（t-test/Wilcoxon）；需不确定性量化时上 PyMC（看 r_hat≈1、ESS 足够）。报均值±标准差 + 误差棒。**种子/样本数先做功效分析（强制前置，非脚注）**：跑 `python scripts/power_check.py --effect <d> --target-power 0.8`（或 `--n <重复数>` 看实际 power）反推最小重复数——脚本实跑印证"少量种子只够检测大效应(d≈0.8 约 26/组)，中效应(d≈0.5)需每组 **64**，而 5 种子对 d=0.5 仅 power≈0.11"。**实验矩阵的种子数应填 power_check 反推值，别用模板默认的 5 应付中小效应**。statsmodels 缺失时脚本降级正态近似并标 [APPROX]；ANOVA/比例/相关等复杂设计用 statsmodels 对应 Power 类。
   - 防泄漏：所有依赖训练集统计量的预处理（标准化/填补/编码）必须封进 sklearn Pipeline + ColumnTransformer，再交给交叉验证，禁止对全量数据先 fit。
6. **可视化方案**：要出哪些图表（交 m09）。
7. **时间安排**：里程碑 + 甘特，对齐 deadline。
8. **风险点 & 备选方案**：每个风险配 plan B。
9. **算力/成本预算**：idea 放行后第一环节必须算账——逐实验估 GPU 时数 × 卡数 × 单价，汇总对照预算上限（模板 experiment_matrix.md 已带预算表）。单价记来源+日期（对齐 db08），禁凭记忆；扫参×多种子是预算放大器，超支则砍范围。承接 m04 rubric 维度7。
   - **参考价区间（起算锚点，非报价；务必现查最新价 + 记日期）**：消费级 4090≈¥2–4/卡·时、A100 80G≈¥8–18/卡·时、H100≈¥20–40/卡·时（云厂商/竞价实例差异大，2026 量级粗估）。**这是给"心里没数"的人一个起算锚，落预算前必到目标云厂商现查并记来源日期**——价随供需大幅波动，过期锚点只用于量级估算不作报价。
10. **预期成果**：论文层次/竞赛/专利/软著。

## 复现已有论文（复现也是一种研究方案）
复现一篇论文的结果是合法的研究方案（验证/教学/作为自己 baseline）。与从 0 设计共享可复现规划，多了对标原文的五步（详见 references「复现已有论文协议」节）：
1. **定复现目标**：锚定哪张表/图的哪个数（如 Table 2 top-1 76.5%），不说"复现这篇论文"这种无法验收的目标。
2. **资产盘点**：代码/权重/数据/配置四类可得性，决定复现难度与归因空间。
3. **偏差预算**：事先定"差多少算成功"（如原文 ±0.5% 内），不预设就会陷入扯皮。
4. **复现日志**：逐次记 {改了什么/得到的数/与目标的差/下一步假设}，每次只改一个变量。
5. **失败诚实归因（三分）**：达不到偏差预算时归到 实现差异 / 数据差异 / 原文问题，禁笼统说"没复现出来"；指向"原文问题"须多方交叉、走 research-ethics，勿轻率公开指控。
复现代码与调试走 a03(light-backend-coding)；复现作 baseline 时结果回 m06。

## 可复现规划（硬性）
**先按项目规模选档位，别给小课题套重型工具（否则落地成本远超收益、整套被弃用）**：
- **轻量档**（单机/单数据集/小模型，多数本科生&小课题）：`requirements.txt` 锁版本 + 固定随机种子 + CCDS 目录约定 + **一个跑批脚本**（`run.py`/`Makefile`），够了。不上 DVC/Snakemake/MLflow。
- **标准档**（多实验/需对比追踪）：轻量档 + Hydra 配置 + MLflow 或 W&B 日志。
- **完整档**（大型/多人/数据版本敏感/长周期）：标准档 + DVC 数据版本 + Snakemake/流水线 DAG。
- **Windows 环境注意**：本仓运行环境是 Windows——**Snakemake 在 Windows shell 兼容性差（references 已自承），建议 WSL2 或改用 Windows 友好替代**：纯 Python driver / `invoke`（`tasks.py`）/ `make`(GnuWin/scoop)。流水线工具按此并列选，别硬套 Snakemake。

逐项落实，给出具体配置而非工具名（以下为完整档全集，按上面档位裁剪）：
- **环境**：OS/驱动/CUDA 记录；依赖锁版本（requirements.txt 固定版本 / environment.yml / lockfile）。
- **目录脚手架**：按 Cookiecutter Data Science 布局——`data/{raw,interim,processed,external}`(raw 只读不改)、`src/`(可复用逻辑下沉，notebook 不放核心逻辑)、`models/`、`reports/figures/`、`Makefile`、`README`。
- **配置管理**：Hydra 分层配置（conf/ 下 model、dataset 分组 + defaults 列表组合），命令行可覆盖 `lr=0.1`，run 自动存最终合成配置。
- **数据/模型版本**：DVC——`dvc add` 跟踪大文件(git 只存 .dvc 指针)，`dvc.yaml` 定义 stages(cmd/deps/params/outs/metrics)，`dvc repro` 增量复现，`dvc.lock` 锁哈希；`dvc exp run/show` 对比实验。
- **流水线**：Snakemake rule(input/output/params/wildcards) 自动推 DAG + 增量重跑，每个 rule 用 `conda:`/`container:` 锁环境。
- **实验日志**：MLflow（`set_experiment`→`start_run`→`log_param/log_metric(step=)/log_artifact`，或 `autolog()`）或 W&B（`init(config=)`→`log()`，Artifacts 管血缘；敏感数据用 offline 模式避免外发）。
- **固定项**：随机种子、数据划分、超参、训练策略、结果文件命名规范、运行命令。

## 执行纪律（落地与验证，借鉴工程实践）
- **先计划后执行**：方案按 phase 分段，每段写明可验证的成功标准；执行时一次推进一个 phase，做完对照标准勾验再进下一段，偏离写回 decision_log。
- **关键代码 TDD**：数据处理、指标计算、统计检验等关键函数先写测试(给"已知输入→已知输出"金标准用例)、看它失败、再实现，警惕"测试全绿但实现错"。
- **系统化排错**：bug 按 复现→读完整报错→二分定位根因→验证假设→修复后回到复现确认 的顺序；同一思路失败两次即停下找根因换打法，不连续打补丁。
- **完成前验证**：声明"做完"前过 checklist——build 通过、相关测试通过、产出逐条对上成功标准、清理临时文件。

## 产出
1. 完整方案文档（上述全部）。**标准工件：`PROJECT_PLAN.md`**（交 a03/m06，工件契约见 CONVENTIONS §6.1）。
2. 实验矩阵表（实验 × 数据集 × 指标 × 状态）。**标准工件：`experiments/experiment_matrix.md`**（下划线命名，与契约一致）。
3. 复现清单 checklist。
4. 交 a03 落地代码、a06 建目录、a02 登记里程碑与里程碑到 db09。

现成模板见同目录 `templates/`（research-plan.md / experiment_matrix.md / reproducibility-checklist.md）。填完实验矩阵后可跑 `python scripts/plan_lint.py --file experiments/experiment_matrix.md` 自查每行四要素（假设/变量/指标/停止条件）是否齐全。**除四要素齐全（硬 gate，缺项退出码 1）外，还做语义弱校验（warning，不翻退出码但提示"形式齐全≠语义正确"）：① 完成判定是否含可量化阈值（数字/不等号/p值，纯定性词如"效果好"会被 warn）；② 完成判定是否提及该行指标关键词（防判定与指标脱节）；③ 假设-实验覆盖度（每个假设是否有 ABL 消融，缺则 warn——无消融难归因增益来自创新点）。把 EXP-Bench 最难的"结论判定与假设对齐"从盲区变成可提示。**并汇成严谨性评分卡（借 ARA Rigor Reviewer，0-100 经验扣分制 + 分项：四要素齐全/判定可量化/判定指标对齐/有消融覆盖），非真值但可审计，给方案一个客观严谨度起点。**

## 衔接
方案交 a03 实现 → 实验跑完 → m06 result-analysis；方案变更回写 db09 decision_log。
**派生数据回边**：实验矩阵中鲁棒性/泛化/敏感性所需的派生评测集（加噪/缺失/跨域/扫参），作为派生数据规格回 m02（light-data-engineering）构建，产出数据集 + dataset_card 回填 db04。派生规格写成 JSON（基础集 + 变换 noise/missing/subset/scale + 参数 + eval_dim），m02 用其 derive_eval_set.py 脚本可执行生成（铁律：只动特征不碰标签、固定种子、仅评测不回流训练折），规格样例见 light-data-engineering 的 derive_spec.example.json。
**复现已有论文**：用 `templates/reproduction-log.md` 逐次记录（改了什么/得到的数/与目标差/下一步假设）+ 失败三分归因，配合上文五步协议。

### 衔接技能速查表（编号 → 技能 → 交什么；脱离 CONVENTIONS 也能自解释）
| 编号 | 技能 | 本技能与它的接口 |
|---|---|---|
| m02 | data-engineering | 开工前确认数据就绪；派生评测集规格回它构建 |
| m04 | idea-critique | 上游放行闸门 + 承接其 Revision Roadmap must-fix |
| m06 | result-analysis | 实验跑完交它做显著性/功效（口径与其 BH-FDR 对齐） |
| m09 | figure-planning | 框架图/技术路线图交它规划 |
| a02 | memory-pm | 里程碑/决策登记 |
| a03 | backend-coding | PROJECT_PLAN/实验矩阵交它落地代码与调试 |
| a06 | project-structure | 目录脚手架交它生成（本技能不重复列任务清单） |
| a10 | research-ethics | 复现失败归因指向原文问题时走它，勿轻率公开指控 |
| db03 | 方法库 | 开工前查方法就绪度（按 domain_scope 过滤） |
| db04 | 数据集库 | 数据可行性对齐 + 派生数据集卡回填 |
| db08 | 经费预算库 | 算力成本预算口径对齐 |
| db09 | 项目库 | decision_log 落档方案与变更 |

---
工具细节（真实端点/参数/命令、已知坑）见同目录 `references.md`。
