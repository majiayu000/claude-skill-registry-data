---
name: light-tool-selection
description: 工具选择与多工具协同。根据任务自动判断适合用什么工具——搜索、Python、R、MATLAB、LaTeX、Word、Excel、PowerPoint、Visio、Origin、数据库、Git、前端/后端框架、绘图工具、文献管理工具等（常驻，所有任务后台生效）。不盲目用工具，而是按实际任务选最高效、最稳定、最专业的实现方式。
user-invocable: false
---

# 工具选择与多工具协同

## 原则（常驻）
不为用工具而用工具。每个任务先问：**最高效、最稳定、最专业、最可复现的方式是什么？** 优先可复现(代码/脚本) > 一次性手工；优先项目已有的栈 > 引入新依赖。

## 任务 → 推荐工具映射
- **文献搜索**：arXiv/OpenAlex/Semantic Scholar/Crossref API、agent-browser/browser-use、Exa/Parallel Web。
- **浏览器自动化**：偏 CLI/稳定走 agent-browser(原生 Rust CLI、直连 CDP、accessibility-tree 快照+`@eN` 引用定位、命令间保活、4848 端口可观测面板，先 `agent-browser skills get core` 发现用法)；偏 Python 集成走 browser-use(`Agent(task,llm,browser)`+`await agent.run()`，基于 Playwright，`@tools.action` 加自定义工具，`use_cloud=True` 走 stealth 云浏览器)。**投稿系统网页操作**（OpenReview/Editorial Manager 等填表、上传、查状态）可装 agent-browser 类技能（约 438K 装，last_checked 2026-06），**Light 不自建浏览器自动化**，按需引入外部技能并评估来源安全。
- **数据处理**：pandas(中小) / polars(快) / DuckDB·polars streaming·dask(超内存)；质量 ydata-profiling/Deepchecks/Great Expectations。
- **统计/科学计算**：Python(statsmodels/scipy/sklearn)、R(高级统计/绘图)、MATLAB(信号/控制/数值)。
- **绘图**：matplotlib/seaborn/plotly/altair、ggplot2、Origin(期刊曲线)、TikZ/Graphviz/Mermaid(框架流程图)、**Draw.io**(框架/系统/架构图 diagram-as-code，有官方 MCP，XML 可版本控制)、Illustrator/Inkscape(精修)、Visio。
- **3D 可视化/渲染**：Blender(开源，程序化建模渲染非 AI 生图；3D 科学可视化用 Molecular Nodes/SciBlend 等插件、路演 3D 渲染；有社区/官方 MCP，需本地装)。配 m09 figure-planning / m16 slides。
- **排版**：LaTeX(latexmk/TinyTeX/TeX Live)、Word(python-docx)、Pandoc(互转)。
- **文档处理**：PDF/DOCX/PPTX/XLSX skill、MarkItDown、unstructured.io、Apache Tika。
- **PPT**：python-pptx/PptxGenJS、Marp、reveal.js、Beamer、PowerPoint/Canva/Gamma。
- **前端**：Next.js/React、shadcn/ui、Tailwind、ECharts/D3；有设计稿时用 **Figma MCP**(读稿→IDE 出码，Remote server 免费可读写)，配 a05 frontend-design。
- **后端**：FastAPI/Django/Spring Boot、Postgres/Redis、Docker。
- **API 调用**：有 OpenAPI 描述就按 `paths→operationId`+参数 schema+`securitySchemes` 确定性调用、按 response schema 解析，别靠散文文档猜（字段细节见 references.md）。
- **云算力**：Python serverless/GPU 训练/沙箱用 Modal（代码内 `@app.function(gpu=..., image=...)` 定义环境，按秒计费；命令与原语见 references.md）。
- **版本/实验**：Git、DVC、MLflow、W&B、Hydra、Snakemake。
- **自动化/CI**：仓库事件触发用 GitHub Actions（test-on-push、schedule 定时、自动构建论文 PDF/图、release）；本地数据依赖编排用 Snakemake/Make——二者互补（Actions 管"何事件触发"，Snakemake 管"步骤间数据依赖"，见 references.md）。
- **文献管理**：Zotero/pyzotero、JabRef、Better BibTeX。
- **环境**：纯 Python 优先 uv；编译科学库/CUDA/跨语言用 conda(mamba/miniforge)；已有 Poetry 项目延续 Poetry。

## 选择决策要点
- 数据规模 → 选库(pandas vs polars vs dask)。
- 一次性 vs 可复现 → 手工 vs 脚本。
- 输出去向 → 决定格式(矢量图投稿、png 演示)。
- 团队/复现需求 → 是否上版本与实验管理。
- 稳定性 > 新潮：选成熟、维护活跃的工具(CONVENTIONS 依赖安全)。

> 带**数值阈值**的完整决策矩阵(数据 <100MB pandas / 2-50GB polars / >TB Spark；投稿矢量 vs 演示 png≥150dpi；skill 安装量≥1K 等)见 references/decision_matrix.md，按需载入。

### 自动检测项目技术栈
进入一个已有项目、或用户问"这个项目该用什么工具"时，先跑检测脚本而非人工翻清单：
```bash
python scripts/detect_stack.py <项目目录>        # 读 package.json/pyproject.toml/requirements.txt/environment.yml
python scripts/detect_stack.py <项目目录> --json # 机器可读
python scripts/detect_stack.py --self-test       # 无项目时合成清单自检
```
脚本识别依赖→按类别给选型建议(命中内置规则的才给，未命中标 no signal 不臆造)，并据锁文件(uv.lock/poetry.lock/environment.yml/Dockerfile)给环境/复现建议。汇报照 assets/stack_detection_report.md。

### Python 环境选型
按依赖性质选 uv / conda / Poetry / Docker 的决策表（场景→工具→关键命令、互斥铁律）权威版见 references/decision_matrix.md 第 5 节；逐工具完整命令/参数/坑见 references.md（uv/Conda/Poetry/Docker 各段）。一句话口径：纯 Python/PyPI 优先 **uv**，编译科学库/CUDA/跨语言用 **conda(mamba/miniforge)**，已有 Poetry 项目延续 **Poetry**，可移植服务复现用 **Docker**；三者都靠锁文件保复现，**同一环境不混 pip+conda**。

## 多工具协同
一个任务常跨工具：如"实验→W&B 记录→pandas 汇总→seaborn 出图→LaTeX 排版→Zotero 引用"。规划好数据在工具间的流转格式(CSV/JSON/Parquet)，减少手工搬运。

## 工具发现
需要新能力时按序：
1. 先查现成 skill：先看 skills.sh 排行榜(按总安装量，顶部如 vercel-labs/agent-skills、anthropics/skills 均 100K+，last_checked 2026-06)，再 `npx skills find [关键词]` 搜索。**质量数值阈值(安装量/GitHub star/来源信誉)权威版见 references/decision_matrix.md 第 7 节**。给用户列 名称/用途/安装量/来源/链接/安装命令，同意后 `npx skills add <owner/repo@skill> -g -y`(-g 全局、-y 免确认)；无命中就坦白、转用通用能力、并建议 `npx skills init <name>` 自建。（安装量随时间变，引用具体数字一律带 last_checked。）
2. 接外部数据/工具：查可用 **MCP server**（参考款 Everything/Fetch/Filesystem/Git/Memory/Sequential-Thinking/Time；TS 用 `npx -y @modelcontextprotocol/server-*`、Python 用 `uvx mcp-server-*`，Windows npx 要 `cmd /c` 包裹；registry.modelcontextprotocol.io 更多）。先 `tools/list`/`resources/list` 看暴露了什么再调用。**科研设计/绘图/3D/计算类已选定推荐 MCP**（路由到对应技能时按需建议）：Figma(读设计稿→前端,a05)、Canva(路演 PPT/海报,m16/m17)、Draw.io(框架/系统/架构图 diagram-as-code,m09/a04/m15)、Blender(3D 科学可视化/路演渲染,m09/m16)、MATLAB(信号/控制/数值/Simulink)——能力/费用/star 单一真相源在 **README 推荐 MCP 表**，本节不复写数字（口径同 OpenAlex key）。
3. 自建 skill：用 **skill-creator** 路线——`SKILL.md`(frontmatter 仅 name/description)+`scripts/`+`references/`+`assets/`，三级渐进披露，description 枚举触发场景防欠触发，正文用祈使句解释"为什么"。评估闭环：真实测试 prompt → with-skill vs baseline 量化对比 → 读 transcript 泛化别过拟合 → 重复活抽进 `scripts/`。（skill-creator/Autoskill 细节见 references.md。）
引入任何第三方 skill/MCP server 都等于授权外部指令与代码，先评估来源与安全。详见 references.md。

## 资源清单(bundled)
- `scripts/detect_stack.py`（技术栈检测，`--self-test` 离线自检）、`references/decision_matrix.md`（带数值阈值的决策矩阵）、`references.md`（逐工具端点/命令/坑）。
- 呈现模板 `assets/`：`stack_detection_report.md`（检测汇报）、`skill_discovery_report.md`（发现 skill，单个/多候选/未命中兜底）、`mcp_discovery_report.md`（发现 MCP，含 tools/list、resources/list 探测清单）。两份发现模板附 2026-06 实测入口与 HTTP 码。

## 衔接
为所有技能提供"用什么做"的判断；与 a06(目录)、a02(版本工具)、a03(代码栈)协同。

> 逐工具硬信息(真实端点/命令/参数/坑)见同目录 references.md。
