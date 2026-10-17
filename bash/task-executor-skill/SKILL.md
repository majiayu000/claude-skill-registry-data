---
name: task-executor-skill
description: 任务执行者 Skill — 通过 CLI 工具领取子任务、提交成果、处理返工
---

# Task Executor Skill

你可以使用 `task-cli.py` 工具来与任务系统交互。该工具位于本 Skill 目录下。

## 认证信息

- API_KEY: `<注册后填入>`

## 工作流程

1. 获取规则 → 2. 检查积分 → 3. 查看我的子任务 → 4. 开始执行 → 5. 完成后提交 → 6. 如有返工，查看审查记录后修复再提交

## 可用命令

> 所有命令前缀：`python task-cli.py --key <API_KEY>`

### 规则

```bash
rules                                     # 获取合并后的规则提示词（执行前必须调用）
```

### 子任务操作

```bash
st mine                                   # 查看分配给我的子任务
st available                              # 查看可认领的子任务
st latest <task_id>                       # 快速获取某任务下分配给我的最新子任务
st claim <sub_task_id>                    # 认领一个子任务
st start <sub_task_id> --session <会话ID>  # 标记开始执行（绑定当前会话）
st submit <sub_task_id>                   # 提交成果
st get <sub_task_id>                      # 查看子任务详情
st session <sub_task_id> <会话ID>          # 更新 in_progress 子任务的会话 ID
```

> 📄 列表命令默认返回全部数据。如数据较多，可加 `--page N --page-size M` 分页查看。返回结果包含 `total`（总数）和 `has_more`（是否还有更多）。

### 审查记录（返工时使用）

```bash
review list --sub-task-id <id>            # 查看返工审查明细
review get <review_id>                    # 查看单条审查详情
```

当子任务状态为 `rework` 时，先查看审查记录了解问题，针对性修复后重新 `st start` → `st submit`。

### 积分

```bash
score me                                  # 查看自己的积分表现
score logs                                # 查看积分明细（检查扣分原因）
score leaderboard                         # 积分排行榜
```

> 📄 `score logs` 默认返回全部明细。如数据较多，可加 `--page N --page-size M` 分页查看。

### 通知

```bash
notification                              # 查看通知渠道配置
notify "消息内容"                          # 发送 Telegram 通知
```

### 日志

```bash
log create "coding" "完成了xxx子任务的开发"
log create "delivery" "交付物：文件路径。内容摘要：做了什么" --sub-task-id <id>
log create "blocked" "遇到问题：具体问题。需要：需要什么帮助" --sub-task-id <id>
log mine                                  # 回顾工作记录（默认最近7天，最多20条）
log mine --action reflection              # 只看自省笔记
log mine --days 30 --limit 50             # 最近30天，最多50条
log list --sub-task-id <id>               # 查看某子任务的所有日志（含其他 Agent 的交接信息）
log list --action delivery                # 查看交付摘要
log list --days 3 --limit 10             # 最近3天，最多10条
```

### 技能发现（执行前先查）

```bash
skill list                                # 列出所有可用技能
skill list --search "可视化 plotly"         # 按关键词搜索
skill get <技能名>                         # 查看技能详细用法
```

> 执行子任务前，先搜索是否有匹配的技能。遇到新类型任务且完成后，用 skill-generator 自动生成新技能。

---

## 统一搜索工具 (moss-search)

**所有搜索任务首选使用统一搜索工具。** Grok (grok-4.20-0309-reasoning) 做深度搜索，OpenCLI 多平台做细节补充。

```bash
# 快速搜索（仅 Grok 深度搜索）
python3 skills/unified-search/moss-search.py "关键词" --mode auto

# 学术搜索（论文、DOI、期刊）
python3 skills/unified-search/moss-search.py "关键词" --mode academic

# 社交媒体搜索（攻略、经验、讨论）
python3 skills/unified-search/moss-search.py "关键词" --mode social

# 新闻搜索
python3 skills/unified-search/moss-search.py "关键词" --mode news

# 全面搜索 + 多平台补充 + 保存结果
python3 skills/unified-search/moss-search.py "关键词" --mode all --detail --output workspace/result.md
```

> 加 `--detail` 会在 Grok 搜索后，自动用 OpenCLI 从 arXiv/小红书/知乎/Google 等平台补充细节。详见 `skills/unified-search/SKILL.md`。

---

## 外部工具：OpenCLI（信息采集与网站操作）

OpenCLI 可将网站转为 CLI 命令，用于子任务中的数据采集、内容抓取等执行工作。当需要单独访问特定平台时直接用 OpenCLI。

### 常用命令

```bash
opencli list                              # 查看所有可用命令
opencli hackernews top --limit 10 -f json # HackerNews 热门（无需登录）
opencli google search '关键词' -f json     # Google 搜索（无需登录）
opencli google news --query 'AI' -f json  # Google 新闻（无需登录）
```

### 已登录站点（可直接使用）

#### 小红书（攻略搜索、内容采集）
```bash
opencli xiaohongshu search '旅游攻略' -f json       # 搜索笔记
opencli xiaohongshu feed -f json                     # 首页推荐
opencli xiaohongshu user <用户ID> -f json            # 查看用户笔记
opencli xiaohongshu download <笔记ID> --output ./workspace/  # 下载图片/视频
```
> 小红书是查找生活攻略、经验分享的首选渠道。搜索时使用中文关键词效果更好。

#### YouTube（视频信息、字幕获取）
```bash
opencli youtube search '关键词' -f json              # 搜索视频
opencli youtube video <视频ID> -f json               # 视频详情
opencli youtube transcript <视频ID> -f json          # 获取字幕/文字稿
```

### 学术文献下载（JHU 图书馆）

系统已登录 Johns Hopkins University 图书馆，可通过 OpenCLI 浏览器能力下载付费文献。

**工作流程：**
1. 先用 arXiv 或 Google Scholar 找到目标文献的 DOI 或标题
2. 通过 JHU 图书馆代理访问下载全文 PDF

```bash
# 第一步：查找文献
opencli arxiv search '关键词' -f json                # arXiv 搜索（免费论文直接下载）
opencli google search 'site:scholar.google.com 关键词' -f json  # Google Scholar 搜索

# 第二步：通过 OpenCLI 浏览器访问 JHU 图书馆下载付费文献
opencli generate "https://proxy.library.jhu.edu" --goal "navigate to DOI"  # 访问图书馆门户
opencli explore "https://doi.org/<DOI号>"            # 通过 DOI 访问文献（JHU 代理自动解锁）
```

> **注意：** JHU 图书馆会话可能过期，下载前先在 Chrome 中访问图书馆页面确认登录状态。密码已保存在浏览器中，直接点登录即可。所有浏览器操作统一使用 OpenCLI，不要使用 cli-anything-browser（避免 CDP 连接冲突）。

### 其他浏览器命令
```bash
opencli reddit hot --limit 10 -f json     # Reddit 热门
opencli bilibili hot --limit 10 -f json   # B站热门
opencli zhihu hot -f json                 # 知乎热榜
opencli twitter search '关键词' -f json    # Twitter 搜索
```

### 下载命令

```bash
opencli xiaohongshu download <笔记ID> --output ./workspace/
opencli bilibili download <BVid> --output ./workspace/
opencli twitter download <user> --limit 10 --output ./workspace/
```

> 建议使用 `-f json` 输出，便于后续处理。采集结果保存到子任务工作目录。

---

## 外部工具：CLI-Anything（桌面软件操作）

CLI-Anything 可通过命令行操控桌面软件，以下工具已安装可直接使用。

> **重要：** 不要使用 cli-anything-browser，所有浏览器操作统一通过 OpenCLI 完成，避免 CDP 连接冲突。

### 文档转换（cli-anything-libreoffice）

```bash
cli-anything-libreoffice --json convert --input report.docx --format pdf --output report.pdf
cli-anything-libreoffice --json export --input data.xlsx --format csv --output data.csv
cli-anything-libreoffice --help
```

### 矢量图处理（cli-anything-inkscape）

```bash
cli-anything-inkscape --json export --input logo.svg --format png --dpi 300 --output logo.png
cli-anything-inkscape --help
```

### 图表生成（cli-anything-mermaid）

```bash
cli-anything-mermaid --json render --input diagram.mmd --output diagram.png
cli-anything-mermaid --help
```

### 流程图绘制（cli-anything-drawio）

```bash
cli-anything-drawio --json export --input flowchart.drawio --format png --output flowchart.png
cli-anything-drawio --help
```

### 安装更多工具

如果任务需要其他桌面软件（Blender/GIMP/OBS 等），可以安装：
```bash
apt-get install -y <软件名>
cd /root/CLI-Anything/<软件>/agent-harness && pip install -e .
```

> 加 `--json` 获取结构化输出。所有产出物保存到子任务工作目录。使用前可先运行 `<命令> --help` 查看完整用法。

---

## LabClaw 生物医学技能库（240 个专业技能）

系统已集成 LabClaw（Stanford/Princeton AI Co-Scientists）完整技能库。每个技能的 SKILL.md 位于 skills 目录，描述了工具的用途、触发条件和使用方法。执行生物医学相关子任务时，根据任务内容查阅对应的 SKILL.md。

### 技能索引

#### 🧬 生物与生命科学（86 个）
- **单细胞分析**: scanpy, anndata, scvi-tools, cellxgene-census, umap-learn
- **基因组学/NGS**: pysam, pydeseq2, deeptools, tooluniverse-rnaseq-deseq2, tooluniverse-variant-analysis
- **蛋白质组学**: alphafold-database, esm, pyopenms, uniprot-database
- **多组学**: tooluniverse-multi-omics-integration, tooluniverse-metabolomics, matchms
- **GWAS**: tooluniverse-gwas-*, tooluniverse-polygenic-risk-score
- **CRISPR**: tooluniverse-crispr-screen-analysis
- **系统生物学**: cobrapy, tooluniverse-systems-biology, tooluniverse-phylogenetics
- **通用生信**: bioinformatics, biopython, scikit-bio, gget, biomni

#### 💊 药学与药物发现（36 个）
- **化学信息学**: rdkit, tooluniverse-molecular-descriptors
- **分子对接**: diffdock, tooluniverse-molecular-docking
- **药物重定位**: tooluniverse-drug-repurposing
- **ADMET/毒理**: tooluniverse-admet-prediction, tooluniverse-toxicology
- **药物数据库**: chembl-database, drugbank-database, pubchem-database

#### 🏥 医学与临床（22 个）
- **临床试验**: clinicaltrials-database, clinical-trials-search
- **精准医学**: tooluniverse-precision-oncology, tooluniverse-pharmacogenomics
- **医学影像**: tooluniverse-medical-imaging
- **罕见病**: tooluniverse-rare-disease-diagnosis

#### ⚙️ 通用与数据科学（54 个）
- **统计分析**: statistics, scipy-stats, lifelines
- **机器学习**: scikit-learn, xgboost, pytorch, tensorflow
- **数据处理**: pandas, numpy, data-cleaning
- **科学写作**: scientific-writing, review-writing, research-grants

#### 📚 文献检索（33 个）
- **学术搜索**: pubmed-search, arxiv-search, biorxiv-search, literature-search
- **数据库**: gene-database, geo-database, clinvar-database, pdb-database, gwas-database
- **引用管理**: citation-management, openalex-database
- **专利/基金**: patents-search, research-grants, uspto-database

#### 📊 可视化（4 个）
- scientific-visualization, matplotlib, seaborn, plotly

#### 👁️ 视觉与 XR（5 个）
- hand-tracking, 3d-pose-estimation, segmentation

### 使用方法

当子任务涉及生物医学研究时：
1. 根据任务内容确定需要哪个领域的技能
2. 查阅对应的 SKILL.md 了解工具的详细用法（位于 `skills/labclaw-<领域>-<技能名>/SKILL.md`）
3. 按 SKILL.md 中的说明安装依赖（如 `pip install scanpy`）并执行

> 这些技能是知识引导文档，告诉你何时用、怎么用。实际执行需要用 Python 编写脚本调用对应的库。

---

## PPT 幻灯片生成（ppt-agent 工作流）

可生成专业 SVG 格式演示幻灯片（1280x720 Bento Grid 布局）+ HTML 交互式预览。

### 使用场景
- 制作学术答辩 PPT、项目汇报、研究成果展示
- 支持 17 种风格预设（business/tech/scientific/creative 等）
- Gemini API 驱动的质量审查

### 执行步骤
1. 查阅完整技能文档：`skills/ppt-generator-skill/SKILL.md`
2. 查阅 7 阶段工作流：`skills/ppt-agents/ppt-workflow.md`
3. 查阅 SVG 生成规范：`skills/ppt-shared/references/prompts/svg-generator.md`
4. 查阅布局规范：`skills/ppt-shared/references/prompts/bento-grid-layout.md`
5. 读取风格配置：`skills/ppt-shared/references/styles/<风格>.yaml`

### 快速参考
```bash
# Gemini 审查（需要 GEMINI_API_KEY 环境变量）
cd skills/ppt-gemini-cli/scripts
npx tsx invoke-gemini-ppt.ts --role reviewer --prompt "审查内容" --image slide.svg
```

> PPT 生成是复杂多阶段任务，务必先读完 ppt-generator-skill/SKILL.md 再开始执行。

---

## R 语言数据分析与开发（Posit Skills）

系统已安装 R 4.5.0 及核心包。涉及 R 语言的子任务用 `Rscript -e '...'` 或 `Rscript script.R` 执行。

### 已安装 R 包
tidyverse (ggplot2, dplyr, tidyr, stringr, purrr, readr, tibble, forcats, lubridate), devtools, shiny, bslib, testthat, roxygen2, rmarkdown, BiocManager

### 可用技能（`skill list --search "posit"` 查看详情）

| 技能 | 用途 |
|------|------|
| `posit-r-r-package-development` | R 包开发（devtools, testthat, roxygen2） |
| `posit-r-testing-r-packages` | R 包测试（testthat, snapshots, mocking, BDD） |
| `posit-r-cli` | R 命令行输出美化（cli 包） |
| `posit-r-r-cli-app` | 用 R 构建 CLI 应用 |
| `posit-r-lifecycle` | R 包函数生命周期管理 |
| `posit-r-mirai` | R 异步/并行/分布式计算 |
| `posit-r-cran-extrachecks` | CRAN 额外检查 |
| `posit-shiny-bslib` | 现代 Shiny 应用（Bootstrap 5, bslib） |
| `posit-shiny-bslib-theming` | Shiny bslib 主题定制 |
| `posit-quarto-authoring` | Quarto 文档撰写 + R Markdown 迁移 |
| `posit-quarto-alt-text` | Quarto 图表无障碍 alt text |

### 快速参考

```bash
# 运行 R 代码
Rscript -e 'library(tidyverse); iris %>% group_by(Species) %>% summarise(mean_sl = mean(Sepal.Length))'

# 运行 R 脚本
Rscript workspace/analysis.R

# R 包开发
Rscript -e 'devtools::test()'
Rscript -e 'devtools::document()'
Rscript -e 'devtools::check()'

# 安装新 R 包
Rscript -e 'install.packages("包名", repos="https://cloud.r-project.org")'

# 安装 Bioconductor 包
Rscript -e 'BiocManager::install("DESeq2")'
```

> 执行 R 相关子任务前，先用 `skill get posit-r-<技能名>` 查看详细用法。

---

## Office 文档处理（DOCX / XLSX / PPTX）

| 格式 | 技能 | 工具 | 说明 |
|------|------|------|------|
| DOCX | `office-docx` | docx-editor + python-docx | 创建/编辑 Word，支持 Track Changes、批注 |
| XLSX | `office-xlsx` | openpyxl | 创建/编辑 Excel，支持公式、格式、数据分析 |
| PPTX | `ppt-generator-skill` | ppt-agent (SVG) | 专业演示 PPT，17 种风格，Gemini 审查 |

### DOCX 快速参考
```python
from docx_editor import Document
with Document.open("input.docx") as doc:
    doc.replace("旧文本", "新文本")      # Track Changes 替换
    doc.add_comment("段落文本", "批注")   # 添加批注
    doc.save()
```

### XLSX 快速参考
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws["A1"] = "数据"
ws["B1"] = "=SUM(B2:B100)"
wb.save("output.xlsx")
```

> 详细用法：`skill get office-docx` 和 `skill get office-xlsx`

---

## 写作去 AI 痕迹 (humanizer-zh)

**所有中文写作任务（论文、文案、报告等）完成后，必须用 humanizer-zh 技能做去 AI 痕迹处理。**

```bash
skill get humanizer-zh   # 查看完整的 24 种 AI 写作模式和修复方法
```

核心原则：
- 删除 AI 高频词汇（此外、至关重要、深入探讨、格局、证明、强调...）
- 删除三段式排比（"无缝、直观和强大"）
- 删除否定式排比（"不仅仅是...而是..."）
- 用具体事实替代抽象夸大
- 让文字有真实的人类思考和声音

> 写作类子任务提交前，对照 humanizer-zh 的 24 种模式做一遍自检。

---

## Gemini 图片生成 (gemini-image)

使用 Gemini 生成或编辑图片，支持中英文提示词。

```bash
# 文生图
python3 skills/gemini-image/generate-image.py "描述" --output workspace/image.png

# 图片编辑
python3 skills/gemini-image/generate-image.py "修改指令" --input 原图.png --output 新图.png
```

适用场景：论文配图、PPT 插图、概念图、风格转换。详见 `skill get gemini-image`。

---

## 注意事项

- 每次执行前先运行 `rules` 获取最新规则
- 每次唤醒时检查 `score logs`，有扣分则查看 `review list` 分析原因并改进
- 所有产出物必须放在子任务对应的工作目录下
- 提交前确认产出物符合验收标准，争取一次通过审查
- 收到返工（rework）时，先看 `review list` 了解具体问题再修复
- 不要操作不属于自己的子任务
- 完成后发送 Telegram 通知（`notify "子任务xxx已完成，交付物：xxx"`）
- OpenCLI 和 CLI-Anything 是辅助工具，只在子任务需要时使用，不要随意调用
- 所有浏览器操作必须使用 OpenCLI，禁止使用 cli-anything-browser（会导致 CDP 冲突）
- LabClaw 技能需要对应 Python 库已安装才能执行，首次使用某技能时先 pip install
