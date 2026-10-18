---
name: tizhuang-local-bank
description: "老师的本地题库（Obsidian 兼容，不需要账号或插件）：把 PDF 试卷还原成可编辑题目入库、下载题庄知识树并给题目分类、按教材/章节/考点/标签检索、核对后组卷并生成无答案 Word/打印稿与教师答案稿。用于“本地题库、Obsidian 题库、PDF 试卷入库、题目分类、找题、组卷、出 Word 试卷、导出题目包”。仅供教师备课打印，不做学生端。在线取题属于可选的旧 question-bank skill。Teacher-side local question bank: PDF import, knowledge-tree classification, search, paper assembly (DOCX/HTML)."
---

# 题庄 · 我的本地题库（教师版）

教师自用的本地工具：Markdown 是唯一真源，SQLite 只是可重建索引。Obsidian 与插件都是可选的。不创建学生账号、在线作答或作业。

## 先做这三件事（每次会话开头）

1. **定位工具**：以本 SKILL.md 所在目录的 `scripts/local_bank.py` 为 `<cli>`，用独立虚拟环境的 Python 为 `<python>`（Python 3.10+；优先读 `.tizhuang-install.json` 里的 `runtime.python`）。不要写死开发者的机器路径，不要把依赖装进别的 skill 环境。
2. **定位题库**：只用老师指定的目录；没有就建议在当前工作区新建 `题庄本地题库`。不猜已有 vault，不扫整盘。
3. **体检**（严格只读：`doctor.py`、`status`、`show`、`search` 都不写任何文件，不刷新索引；要刷新首页/索引用 `dashboard`）：
   ```text
   <python> <skill>/scripts/doctor.py --vault <vault>
   ```
   环境缺失时它只依赖标准库也能运行，并给出修复命令；环境正常则带出题量、待核对、待分类、知识树和**下一步建议**。需要安装/升级/修复时读 [安装](references/install.md)；安装完成后必须再体检一次，通过才算装好。老师自己也可在插件设置里点“检查环境”。

所有命令格式：`<python> <cli> --vault <vault> <命令> ...`，输出 JSON。`ok:false` 或退出码非 0 就是失败：读 `error` 与 `hint`，修好原因再继续，**不要静默放宽筛选条件，不要重复执行写入命令**。V1 是中文子串＋结构化检索，不要声称有向量/语义检索；单写入者，写操作要串行。

## 怎么跟老师说话

- 用老师的话汇报：“已存入 12 道题，其中 3 道还没有答案”，而不是贴 JSON、ID 或命令。
- 一次只问阻塞性的问题（学科学段、教材版本、题库位置）；能从 `status` 和已有数据判断的不要问。
- 每次写入后回报三件事：做了什么、文件/题目在哪、还差什么（待核对？待分类？）。路径用老师的真实 vault 路径。
- 不确定就如实说“不确定”，并把原因写进待核对，不要编。
- 对话示例与常见问题话术见 [对话指南](references/conversation-guide.md)；给新老师做使用介绍时分享 [图文说明](https://github.com/weishao2/tizhuang-agent-skills/blob/main/docs/local-bank/USER_GUIDE.md)（起步包内有离线 `先看这里.html`）。

## 常见任务 → 怎么走

| 老师想做的事 | 做法 |
| --- | --- |
| 初始化 / 整理旧题库 | `init`；已有中文题库 `organize`（自动完整备份）；`dashboard` 刷新首页；`repair-papers` 修复旧打印稿入口。英文旧目录先 `migrate-cn`。不要自己搬文件夹。→ [教师工作台](references/teacher-workspace.md) |
| 下载知识树 / 教材章节 | `catalog` → `tree` / `editions` → `chapters`。知识树不是教材目录，版本必须是老师的真实版本。→ [知识树与教材](references/tree-and-textbook.md) |
| PDF 试卷入库 | `pdf-prepare` → 逐页看原图 → 写 v2 分题清单 → `pdf-import`。→ [PDF 流程](references/pdf-import.md) |
| 存入已有题目 | `import --file <questions.json 或 .zip>`。→ [题目协议](references/question-contract.md) |
| 给题目分类 | 先 `auto-classify`（只做精确标签匹配），剩余的 `show --ids …` 读题 → 判断真实节点 → `classify --plan` → `classify` |
| 找题 | `search`（`--subject --phase --edition --chapter --knowledge --tag --type --status --query --unused --limit`） |
| 读题 / 核对 | `show --ids …` 看完整题干、答案、解析；老师明确确认后才 `review --confirm`（插件里对应列表中的“标记为已核对”） |
| 组卷 | `search` → `paper … --plan` → 写 basket JSON → `paper --basket`。→ [组卷篮](references/paper-basket.md) |
| 交给别的 Agent / 视频素材 | `export`（默认不含答案；含答案须老师授权 `--include-solutions`）。→ [家族关系](references/family.md) |

## 不可违反的规则

| 规则 | 原因 |
| --- | --- |
| 导入的题一律 `draft`；**只有老师明确说“核对好了”才 `review --confirm` 或 `--confirm-reviewed`** | 答案/图片可能识别错，组卷发给学生会出事故 |
| 不把 AI 生成的答案当作原答案；AI 内容标 `source.kind: ai` 且待核对 | 来源可追溯 |
| 原卷没有答案就留空；识别不清写 `[待核对：位置]` 并列入 `uncertainties`，不猜字 | 诚实 |
| 缺题/缺教材/缺知识节点要报错并说明，**不自动扩大范围或改教材** | 老师的范围不被悄悄改变 |
| 教材版本、章节只来自老师或已确认目录；未知就保持未知；只要求知识点时不碰 `edition_id`/`chapter_ids` | 不同版本不等价 |
| 分类只写真实 `knowledge_tree_ids`；标签不等于知识点；已有题不重新导入、不改正文 | 分类不能破坏原题 |
| 不上传整个题库；不导入含 Key/Cookie/Token 的响应；不改动旧 `question-bank` | 隐私与凭证 |
| 发给学生只给无答案 Word 或 `打印稿/` 子目录；父目录含教师答案和 manifest | 防止泄题 |
| 本地存储不等于本地推理：如实说明哪些内容发给了当前 Agent/模型 | 诚实 |

## PDF 入库（要点）

所有 PDF 一律走可编辑 v2 流程：逐页看原图，还原 Markdown/LaTeX 正文，配图独立裁切；原卷题号和“第几题图”不进正文（只留在来源记录）；只用原答案，没有就留空；有本地知识树时同时写真实 `knowledge_tree_ids`。旧图片草稿只在老师明确要求时用 `--image-draft`；升级旧草稿用带备份的 `--upgrade-to-editable`。“文件已复制”不等于入库成功，以题数、渲染检查和 `search` 验证为准。

## 存题与核对（要点）

读 [题目协议](references/question-contract.md) 构造 JSON；保留老师的内容、网站选项顺序和母子题。网站题用 `import --website --subject … --phase …`（可加 `--download-images`，未解决的图片会阻止核对与打印）。导入请求本身不是答案核对的证明。草稿仍可存储和检索。

## 检索与组卷（要点）

- 树节点筛选包含子孙，需同时给 `--subject --phase`；章节筛选需 `--edition`。
- 组卷前先 `--plan` 检查供题量；选定后写 basket（每卷分值独立，不改题库原分值），再生成。Agent 组卷用新的请求 JSON，不覆盖老师在插件里正在编辑的篮子。
- 生成后**打开并检查**输出再说“可以打印”：复杂公式/版式可能需手工调整；图片公式和 PDF 裁图仍是图片，不能说“全部可编辑”；Word 里的修改不会回写题库，要新版请开始新请求。
- 返回路径：`试卷/<名称>/试卷.md`、`打印稿/试卷.html|docx`（无答案）、`教师稿/试卷.html|docx`（含答案），并告诉老师哪个能发给学生。

## 其它约定

- 数据位置以 `.bank/config.json` 为准；`teacher/v2` 布局中：题目在 `题目库`，知识/教材目录与附件在 `资料`，个人笔记在 `教学笔记`。老师的笔记刷新时不会被覆盖。
- 插件“自动分类”不是模型推理；收到它的 Agent 交接单后，要真正读题再 `classify`，不要把“已复制指令”说成“已分类”。
- Obsidian 菜单语言是应用自己的设置，改文件夹名不会改它。
