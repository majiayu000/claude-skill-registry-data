---
name: task-planner-skill
description: SuperClaw 第六代 Skill — 主助手 + 任务规划 + 技能发现 + 信息搜索
---

# SuperClaw 第六代 Skill

你可以使用 `task-cli.py` 工具来管理任务系统。该工具位于本 Skill 目录下。

## 认证信息

- API_KEY: `<注册后填入>`

## 工作流程

1. 获取规则 → 2. 检查积分 → 3. 查看/创建任务 → 4. 创建模块 → 5. 创建子任务并分配 → 6. 收尾交付 → 7. 记录日志

## 可用命令

> 所有命令前缀：`python task-cli.py --key <API_KEY>`

### 规则

```bash
rules                                     # 获取合并后的规则提示词（执行前必须调用）
```

### 任务管理

```bash
task list                                 # 查看所有任务
task list --status active                 # 按状态过滤
task create "任务名" --desc "描述" --type once  # 创建任务
task get <task_id>                        # 查看任务详情
task edit <task_id> --name "新名" --desc "新描述"  # 编辑任务（仅 planning/active）
task status <task_id> active              # 更新任务状态
task cancel <task_id>                     # 取消任务
```

### 模块管理

```bash
module list <task_id>                     # 查看任务下的模块
module create <task_id> "模块名" --desc "描述"  # 创建模块
```

### 子任务管理

```bash
st list --task-id <task_id>               # 查看某任务下的子任务
st list --status blocked                  # 查看被标记 blocked 的子任务
st create <task_id> "子任务名" --deliverable "交付物" --acceptance "验收标准" --assign <agent_id>
st get <sub_task_id>                      # 查看子任务详情
st edit <sub_task_id> --name "新名" --acceptance "新标准"  # 编辑子任务（仅 pending/assigned）
st cancel <sub_task_id>                   # 取消子任务
st reassign <sub_task_id> <agent_id>      # 重新分配（blocked → assigned）
```

> 📄 列表命令默认返回全部数据。如数据较多，可加 `--page N --page-size M` 分页查看。返回结果包含 `total`（总数）和 `has_more`（是否还有更多）。

### Agent 查看

```bash
agents                                    # 查看已注册 Agent（角色、状态、积分）
agents --role executor                    # 按角色过滤
```

### 积分

```bash
score me                                  # 查看自己的积分
score logs                                # 查看积分明细（检查是否有扣分）
score leaderboard                         # 积分排行榜，分配时参考
```

> 📄 `score logs` 默认返回全部明细。如数据较多，可加 `--page N --page-size M` 分页查看。

### 通知

```bash
notification                              # 查看通知渠道配置
notify "消息内容"                          # 发送 Telegram 通知
```

### 技能发现（分配任务前先查）

```bash
skill list                                # 列出所有可用技能
skill list --search "搜索 学术"            # 按关键词搜索技能
skill get unified-search                  # 查看指定技能详情
skill get ppt-generator-skill             # 查看 PPT 生成技能
```

> 分配子任务时，先搜索匹配技能，在子任务描述中注明推荐使用的技能。

### 日志

```bash
log create "plan" "规划了xxx任务，分配给了xxx"
log mine                                  # 回顾工作记录（默认最近7天，最多20条）
log mine --action reflection              # 只看自省笔记
log list --sub-task-id <id>               # 查看某子任务的所有日志
log list --action blocked --days 3        # 扫描执行者求助日志
log list --days 30 --limit 50             # 最近30天，最多50条
```

---

## 统一搜索工具 (moss-search)

**Planner 调研首选统一搜索。** Grok 深度搜索 + OpenCLI 多平台补充，一条命令完成调研。

```bash
# 学术调研（评估研究可行性）
python3 skills/unified-search/moss-search.py "关键词" --mode academic

# 新闻调研（了解行业动态）
python3 skills/unified-search/moss-search.py "关键词" --mode news

# 全面调研 + 多平台补充
python3 skills/unified-search/moss-search.py "关键词" --mode all --detail
```

> Planner 仅在任务规划阶段使用搜索做调研，不做具体执行工作。调研结果用于：
> - 评估任务可行性和复杂度
> - 拆分模块和子任务时提供依据
> - 制定验收标准时参考行业标准

---

## Executor 可用工具清单（分配任务时参考）

分配子任务时，请根据 Executor 的工具能力来描述任务要求和验收标准：

### OpenCLI（浏览器操作，51 个站点 293 条命令）
- **小红书**（已登录）— 搜索笔记、获取推荐、下载图片/视频，适合查找攻略和经验分享
- **YouTube**（已登录）— 搜索视频、获取视频详情和字幕文字稿
- **JHU 图书馆**（已登录）— 通过学校代理下载付费学术文献 PDF（会话过期需重新登录，密码已保存）
- **arXiv** — 搜索和获取开放获取论文（无需登录）
- **Google** — 搜索、新闻、趋势（无需登录）
- **其他已支持站点** — Twitter、Reddit、B站、知乎、豆瓣、微博、HackerNews、Bloomberg 等

### CLI-Anything（本地桌面软件，无需登录）
- **LibreOffice** — 文档格式转换（docx→pdf、xlsx→csv 等）
- **Inkscape** — SVG 矢量图导出为 PNG
- **Mermaid** — 用代码生成流程图、时序图、架构图
- **Draw.io** — 导出 drawio 格式图表为 PNG

### 分配任务时的写法示例

```
好的示例：
  子任务名：搜集日本东京旅游攻略
  交付物：workspace/tokyo-guide.md
  验收标准：使用 opencli xiaohongshu search 搜索至少 3 个相关笔记，整理为 Markdown

  子任务名：下载 Attention Is All You Need 论文
  交付物：workspace/papers/attention.pdf
  验收标准：通过 arXiv 或 JHU 图书馆下载 PDF 全文

  子任务名：将调研报告转为 PDF
  交付物：workspace/report.pdf
  验收标准：使用 cli-anything-libreoffice 将 docx 转为 PDF，确认格式正确
```

> 在子任务描述中可以提及具体工具名，帮助 Executor 快速定位该用什么工具。

### LabClaw 生物医学技能（240 个，Executor 可用）

系统已集成 Stanford/Princeton LabClaw 完整技能库，Executor 可执行以下领域的研究任务：

| 领域 | 技能数 | 典型任务 |
|------|--------|---------|
| 🧬 生物/生信 | 86 | 单细胞分析(scanpy)、基因组变异分析、蛋白质结构预测、GWAS、CRISPR筛选 |
| 💊 药学/药物发现 | 36 | 分子对接(diffdock)、ADMET预测、药物重定位、化学信息学(rdkit) |
| 🏥 医学/临床 | 22 | 临床试验查询、精准肿瘤学、药物基因组学、罕见病诊断 |
| ⚙️ 数据科学 | 54 | 统计分析、机器学习(sklearn/pytorch)、科学写作、数据清洗 |
| 📚 文献检索 | 33 | PubMed/arXiv/bioRxiv 搜索、GEO数据库、专利检索、引用管理 |
| 📊 可视化 | 4 | matplotlib/seaborn/plotly 科学可视化 |
| 👁️ 视觉/XR | 5 | 手部追踪、3D姿态、分割 |

**分配生物医学任务时的写法示例：**
```
子任务名：对 GSE12345 数据集进行单细胞 RNA-seq 分析
交付物：workspace/scrna_analysis/results/
验收标准：使用 scanpy 完成 QC、归一化、聚类、UMAP 可视化，输出细胞类型注释结果

子任务名：查找 BRCA1 基因相关药物靶点
交付物：workspace/brca1_targets.md
验收标准：使用 PubMed + ChEMBL 数据库查询，整理候选靶点和已有药物信息

子任务名：对候选分子进行 ADMET 预测
交付物：workspace/admet_report.csv
验收标准：使用 rdkit + tooluniverse-admet-prediction 评估候选分子的吸收、分布、代谢、排泄、毒性
```

> Executor 首次使用某技能时需要 pip install 对应 Python 库，可在子任务描述中注明。

### PPT 幻灯片生成能力

Executor 可生成专业 SVG 格式演示幻灯片（1280x720），含 HTML 交互式预览。

- 17 种风格预设：business（商务）、tech（科技）、scientific（学术）、creative（创意）、minimal（极简）等
- Gemini API 驱动的布局和美学审查
- 输出 SVG 文件 + HTML 预览页 + 演讲者备注

**分配 PPT 任务时的写法示例：**
```
子任务名：制作 CRISPR 基因编辑研究成果汇报 PPT
交付物：workspace/crispr-ppt/output/
验收标准：使用 scientific 风格，10-12 页，包含研究背景、方法、结果、结论，生成 SVG + HTML 预览

子任务名：制作团队季度工作汇报 PPT
交付物：workspace/quarterly-report/output/
验收标准：使用 business 风格，8-10 页，包含项目进展、数据统计、下季度规划
```

> PPT 是多阶段任务（调研→大纲→草稿→设计→审查→交付），建议分配充足时间。可在描述中指定风格和页数。

### R 语言数据分析与开发能力

系统已安装 R 4.5.0 + tidyverse + devtools + shiny + BiocManager。Executor 可执行 R 相关任务。

- 11 个 Posit 官方技能（R 包开发、测试、Shiny 应用、Quarto 文档）
- 用 `skill list --search "posit"` 查看完整列表

**分配 R 任务时的写法示例：**
```
子任务名：用 tidyverse 分析实验数据
交付物：workspace/analysis/results.html
验收标准：用 dplyr 清洗数据，ggplot2 可视化，rmarkdown 生成 HTML 报告

子任务名：构建 Shiny 数据仪表盘
交付物：workspace/dashboard/app.R
验收标准：使用 bslib Bootstrap 5 布局，包含数据筛选和交互式图表
```

---

## 注意事项

- 每次执行前先运行 `rules` 获取最新规则
- 每次唤醒时检查 `score logs`，有扣分则分析原因改进
- 创建任务后状态默认为 `planning`，拆分完成后用 `task status` 改为 `active`
- 分配子任务时参考 `score leaderboard`，优先选择高分 Agent
- 留意 `st list --status blocked`，及时重新分配
- `type=recurring` 且 `status=done` 的子任务 → 创建同名新子任务开启下一轮
- 所有子任务 done → 执行收尾交付（汇总交付物 → 任务状态改 completed → `notify "任务xxx已完成"`）
- OpenCLI 仅用于规划阶段的调研，不要用它执行具体任务
