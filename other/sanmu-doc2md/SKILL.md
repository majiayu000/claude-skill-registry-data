---
name: sanmu-doc2md
description: 把 PDF、PPTX 和扫描件整理成保留 LaTeX 公式、高清图表和来源页码的 Markdown 知识库，适配 Obsidian。适用于教材按章拆分、课件转笔记、期刊论文和学位论文入库（含补充材料 SI 双链）、OCR 后的公式与图表回源修复，以及与 Zotero 同步元数据、笔记和 PDF 批注。只要用户想把学术文档转成 Markdown、做 OCR、把论文或教材放进知识库，或者抱怨转换后公式乱码、图片丢失、标题层级错乱，就使用本技能。Converts academic PDF/PPTX/scanned documents to Markdown with MinerU OCR.
---

# 学术文档转 Markdown 知识库

把教材、课件、论文这类公式和图表密集的文档，转成人能读、Agent 能检索、以后还能维护的 Markdown。难点不在“转出来”，而在于转得对：公式语义不能变，图要完整，页码要能追回原文。所以整个流程都围绕两件事展开：尽量从源文件拿到最可靠的内容，拿不准的地方就回原页核对。

下文命令都从本技能目录运行。

## 首次使用

通过完整插件安装时，优先使用随包 MCP 的 `run_doc2md`、`manage_doc2md`；首次解析会在私有数据目录准备 Python 依赖和 KaTeX。CLI 可从包根运行 `node scripts/sanmu.mjs doc2md <脚本名> ...`，例如 `doc2md build-research-document --help`；运行前确认本技能目录上两级确实存在 `scripts/sanmu.mjs`。`node scripts/sanmu.mjs setup` 可预先准备依赖，`doctor` 只检查；`SANMU_NO_AUTO_SETUP=1` 可关闭自动安装。OCR 凭证仍由用户在工作台配置。

单独安装技能时，脚本依赖和 OCR 凭证不会自动就位。第一次用（或命令报缺依赖时）先检查：

```bash
python scripts/doctor.py
```

全部 `[pass]` 就直接开始，之后的任务不必每次都检查。有 `[fail]` 时，先用一两句话告诉用户缺什么、影响什么，征得同意后再安装；用户多半不熟悉命令行，你来执行，用户只做必须本人完成的事。按 [setup.md](references/setup.md) 处理：

- **缺 Python 或 Node 依赖**：在虚拟环境里装 `requirements.txt`，再装 KaTeX（`npm --prefix scripts install --ignore-scripts --no-audit --no-fund`）。
- **缺 `MINERU_API_TOKEN`**：只有云端 OCR 需要它，已有 OCR 结果时可以先跳过。需要时带用户去 MinerU 免费申请，再给出一条命令让用户在自己的终端里用隐藏输入保存 Token，这样 Token 不会留在聊天记录里。设置后要重启助手才能读到。

## 开始之前

花一分钟看源文件，这一步决定后面走哪条路：

- **有没有原生文字层**（PyMuPDF `page.get_text()`，PPTX 用 `python-pptx`）。有的话可以拿来校对 OCR；但要分清是真正的原生文字，还是别人以前叠上去的 OCR 层，后者同样会出错。完全没有文字的就是扫描件，交付时说明内容来自 OCR。
- **有没有内嵌原图**（PPTX 的 `shape.image.blob`，PDF 的 `page.get_images()`）。能独立还原整幅图的原图最清晰；由多个矢量或位图对象拼成的图，单取其中一张会缺东西，要按整幅区域裁切。
- **目标客户端是什么**。Obsidian 用 MathJax，本技能的本地校验用 KaTeX，两者支持的语法不完全一样，最后要在真实客户端看一眼。

## 选择处理路线

| 文档 | 入口 | 产出 | 详细指南 |
| --- | --- | --- | --- |
| 教材、专著、长篇讲义 | `build_markdown.py --mode book` | `00-目录.md` + 按章文件 + `images/` | [book-workflow.md](references/book-workflow.md) |
| 课件、PPT、复习讲义 | `build_markdown.py --mode slides` | 按讲次组织，图片置顶并用 PPT 原文校对 | 本文件即可 |
| 期刊论文、学位论文、预印本、研报 | `build_research_document.py` | 单篇目录：`作者 - 年份 - 标题.md` + `00-目录.md` + `images/` | [research-documents.md](references/research-documents.md) |

教材和课件的差别很大：课件一页一个主题，页顶短句往往就是标题；教材是连续行文，同样的短句多半只是上一页没说完的话。用错模式会把正文误升成标题、把图挤到错误位置。

输出默认放到一个全新目录（如 `<源目录>/<书名>-知识库`）。重复构建时，脚本只更新自己生成且未被人工改过的文件，不会清空目录。遇到人工改动，先比较差异再决定怎么合并，不要用 `--overwrite` 硬盖过去，那样会抹掉用户的修订。

## 工作流程

复杂任务可以复制这份清单跟踪进度：

```
- [ ] 1. OCR（长文档先切片）
- [ ] 2. 用原生文字校对 OCR
- [ ] 3. 处理图表：原图优先，碎图缝合
- [ ] 4. 公式归一化
- [ ] 5. 装配 Markdown
- [ ] 6. 结构与公式校验 → 修复 → 重跑
- [ ] 7. 浏览器预览，再到目标客户端终验
- [ ] 8. （可选）Zotero 同步
```

### 1. OCR

超过约 200 页或 100 MB 的文档先切片。提交时脚本会做预检：加密 PDF、单文件超过 600 页或 200 MB、单批超过 200 份都会被拒绝，这些是 MinerU 的接口限额。

```bash
python scripts/mineru_ocr.py split <源PDF> --out-root ./ocr-work --chunk-size 96
python scripts/mineru_ocr.py submit --out-root ./ocr-work --id-file ./ocr-work/ids.tsv
```

英文文档加 `--language en`；这个参数只是声明语言，识别后仍要核对变量、专有名词和化学式。中断后用 `resume` 续传或补下载原批次，用 `status` 查看进度，不要重新 `submit`，那样会新建批次、重复消耗 OCR 额度。接口字段、结果结构和坐标系见 [mineru-api.md](references/mineru-api.md)。

### 2. 用原生文字校对 OCR

OCR 常把形近字、同音字和希腊字母认错，比如“轫致辐射”认成“韧致辐射”、`ν` 认成 `v`。课件模式下，装配脚本会把位置重叠（重叠度 > 0.5）且文字相似（相似度 ≥ 0.9）的 PPTX 原文自动替换进来，差异大的记进 `build-report.json` 的 `review` 字段等人工复核。有文字层的 PDF 目前不会自动替换，需要自己对照。

### 3. 图表

按可靠程度取图：

1. **源文件内嵌原图**：未经旋转、裁剪、未与其他对象重叠时直接用。PPTX 里被裁剪、旋转、翻转或放在组合里的图片改用 PDF 渲染裁切，否则会把幻灯片上本来藏起来的部分也露出来。
2. **从原 PDF 按整幅区域裁切**，至少 3 倍缩放，适用于扫描件和多对象拼成的图。
3. **表格里的图片**（如章末二维码）会被提取成独立图片，避免转表格时被吞掉。
4. **复杂大表、环状化学键这类二维结构**：加 `--keep-table-images`，Markdown 表格和原版裁图同时保留，前者便于搜索，后者用来核对。

图片按内容哈希（SHA-256 / SHA-1）去重，挂图讲解里反复出现的同一张图只存一份。完全落在图片区域内（重叠度 > 0.6）且少于 12 个字符的文字块视为图内标签，不再重复写进正文。

多面板图常被 OCR 拆成碎块。单篇论文流程默认开启 `--auto-repairs`，但只合并证据充分的情况：同页、同图号或有明确 `(a)/(b)` 标记、空间相邻且中间没有正文，并且必须同时提供原 PDF 和 manifest。跨栏、离得远、缺题注的候选只导出草稿，由人核对：

```bash
python scripts/audit_figures.py <raw目录> --manifest manifest.json --out-repairs repairs-draft.json
```

补充材料编号（`Figure S1`、`Fig. S1`、`Table S1`、`Scheme S1`、`Supplemental/Supplementary Figure 1`、`Supplementary Note 1`、`附图 S1`）会被放进独立的 `supplemental:` 命名空间，避免和正文的 `Figure 1` 混在一起，编号和归属仍需核对。

### 4. 公式

保留行内 `$...$` 和独立 `$$...$$`。装配器会做一轮保守的语法归一化（中文改用 `\text{}`、拆开 `\vertz`、`\vertj`、`\vertHg`、`\cdotkg` 这类粘连命令、`<`/`>` 转为 `\lt`/`\gt`、`<<`/`>>` 转为 `\ll`/`\gg`、HTML 表格里的不等号先实体化等）；涉及式号、化学结构或符号含义的改动，要回原页确认后通过 repairs 修，不要凭猜。标题里的化学式保留 `$\mathrm{CO}_2$`，纯文本位置（图片 alt、纯文本大纲）用 `CO₂`，不要留下 `CO_2` 这种半成品。

15 条规则和真实前后对照见 [math-normalization.md](references/math-normalization.md)。

### 5. 装配

```bash
# 课件
python scripts/build_markdown.py --raw ./ocr-work/raw --out ./知识库 \
    --mode slides --source-dir ./课件 --pdf-dir ./课件PDF

# 教材（chapters.json 的写法见 book-workflow.md）
python scripts/build_markdown.py --raw ./ocr-work/raw --out ./知识库 \
    --mode book --manifest ./ocr-work/manifest.json --chapters ./chapters.json \
    --pdf <整本PDF> --keep-table-images

# 论文（有 SI 时加 --si-doc；构建 SI 本身时用 --supplement-to 指回主文）
python scripts/build_research_document.py --pdf <论文PDF> --raw <OCR目录> \
    --out "./科研知识库/第一作者 等 - 年份 - 标题" \
    --metadata ./library.json --id <条目key> \
    --si-doc "第一作者 等 - 年份 - 标题 - SI"
```

装配时值得留意的几点：

- **段落和标题宁可保守**。不要因为缺句末标点就跨页拼接，那样容易把正文和习题粘在一起。`1. 晶胞概念` 是小节标题，`1. 计算这个数` 是习题题干；以“。？！”结尾或位于习题区的编号行保留为列表或正文。
- **页脚要区分**。`page_footnote` 常装着学术注释、数据来源和公式说明，确认是运行页脚、页码或扫描噪声后才能删；`ref_text` 按正文保留。
- **回源修复**用 `--repairs repairs.json`：每条修复都带原值 `old` 作守卫，原值对不上就停止，原始 OCR 不动。文字、图块、题注、跳过碎块的写法都在 [repairs.md](references/repairs.md)。
- **交付目录保持干净**：只放导航、正文和图片；构建状态默认在旁边的 `.<目录名>.build/`，可用 `--state-dir` 改到别处。清理旧切图用 `--prune-orphans`，它只删 `.build-ownership.json` 记录为本工具生成且已不再引用的文件。
- **给 Agent 检索用**：只有用户明确要做 RAG 或后续检索时才加 `--agent-index`，生成 `agent/` 分块和原页映射。需要主题入口时可交给 `sanmu-paper-reader` 的 `topic_tools.py`；没装那个技能也不影响转换。

### 6. 校验

```bash
python scripts/validate_output.py ./知识库 --images-dir images
python scripts/extract_formulas.py ./知识库 --out formulas.json
node scripts/validate_math.cjs formulas.json
```

主文和 SI 分在不同目录时，加 `--resource-root <共同父目录>`，否则跨目录双链会报目标缺失。修完失败项再重跑。几点解读：

- KaTeX 通过只说明语法被接受，不代表公式和原文一致；遇到 MathJax 支持而 KaTeX 不支持的写法，记下原式和实际显示，不要为了通过检查改坏原式。
- 源图片候选数、解析出的图片数和正文引用数含义不同，不必相等。未被引用的图片会列出来，默认保留。
- 校验器会屏蔽公式区域，避免把化学式里的方括号误报成失效链接；文档里故意展示的图片语法要放进标注了语言的代码块。

### 7. 渲染验收

```bash
python scripts/preview_server.py ./知识库 --port 8766 --katex-dir scripts/node_modules/katex/dist
```

打开 `http://127.0.0.1:8766/`，确认 `document.documentElement.dataset.ready === "true"` 且 `.math-error` 数量为 0，再看各章图片是否都加载出来。图片能显示只代表文件没坏，面板是否完整、题注是否配对仍要对照原页。

本地通过之后，再到用户实际使用的客户端（通常是 Obsidian 的阅读视图和实时预览）检查公式、伪链接和图片。做不到时，在交付说明里写明“客户端终验未完成”。

### 8. Zotero 同步（可选）

`scripts/zotero_sync.py` 对比 Markdown 与 Zotero 条目的元数据、阅读笔记和 PDF 批注。该脚本对本地 HTTP API 只执行读取；写入计划经宿主 Zotero MCP 工具执行。完整插件也提供 `zotero_library`，可将计划中的 `update_item` / `add_note` 映射为同名 `action`，将计划的 `version` 传入 `expectedVersion`，保留库身份、父条目和 `expected_html`（传入 `html`），取得 Zotero 写入授权并回读核验。执行后重跑同一命令回读确认，退出码 `0` 才算完成（`2` 表示还有待执行的 MCP 操作，`1` 是冲突或失败）。这样即使计划有误，也不会绕过 Zotero 自身的校验直接改库。首次同步要用 `--initial-direction` 指定以哪边为准；之后两边改了同一字段会报冲突，不会静默覆盖。用户自己写的笔记不受影响。命令、字段映射和群组库用法见 [zotero-sync.md](references/zotero-sync.md)。

## 经验与陷阱

这些都是实际转换中踩过的坑：

- **下载结果时 TLS 握手 EOF**：本机代理用 fake-IP 接管 DNS 时，`cdn-mineru.openxlab.org.cn` 会被解析成 `198.18.x.x`，而 `mineru.net` 照常能通，很容易误判成网络正常。脚本已内置回退：用公共 DoH 查真实 IP，再用 `curl --resolve` 下载，TLS 校验保持开启。
- **坐标系混用**：`content_list.json` 的 bbox 是 0–1000 归一化坐标；`layout.json` 是页面点坐标，要按每页实际宽高换算，不能写死全书尺寸。定位图题要用 layout 里题注自己的框，不能用整个图块的框。
- **`image` 和 `chart` 是两种块**，题注字段名也不同（`image_caption` / `chart_caption`），只处理 `image` 会漏掉所有曲线图。
- **跨页续表**：MinerU 会把后续页内容并进首页表格，后页只剩空占位块。先对照原页确认内容确实已并入，再保留空块。
- **模型说明混进正文**：空白页偶尔会冒出 `The Ground Truth image displays...`、`According to Rule 2...` 这类模型说明。装配器会过滤，交付前再扫一眼。
- **扫描边缘噪声**：藏书章、条形码会被认成“用应从请勿填清文件中？”这样的乱句，常见于章首、章末几行和页面上下边缘（y < 80 或 y > 920）。确认后用 repairs 清空，做法见 [repairs.md](references/repairs.md)。
- **配合物物态被当成链接**：`[Fe(CN)6](aq)` 在 Markdown 里会被解析成指向 `aq` 的链接，要放进数学环境。解释性方括号确实与链接语法冲突时，核对后改成全角 `［...］`。
- **公式过了 KaTeX，Obsidian 里照样出错**：两个引擎不一样，语法通过不等于显示正常。
- **Obsidian 找不到刚写入的图片**：一次写入几百张图时，文件监视器可能跟不上。先确认路径和图片本身没问题，再重载 Obsidian。
- **Windows 长路径**：只在写入时加 `\\?\` 前缀、枚举时却用普通 `rglob`，会漏掉超长路径下的文件。枚举、读取、写入、校验要走同一套路径处理，目录访问错误不能静默吞掉。
- **用字符拼凑化学结构**：三元环、多边形骨架用 `\begin{array}` 加 `\backslash` 硬拼，结果既解析不了也看不懂，直接保留原图裁切。
- **私人材料别进仓库**：用户的 PDF、文献库元数据、未公开数据都不要提交到版本控制。

## 参考文件

按需读取：

- [setup.md](references/setup.md)：首次配置，包括安装依赖、申请和保存 MinerU Token、常见配置问题
- [book-workflow.md](references/book-workflow.md)：长篇教材的切片、章节重组和常见问题
- [research-documents.md](references/research-documents.md)：论文命名、元数据 frontmatter、SI 双链、双栏阅读顺序
- [math-normalization.md](references/math-normalization.md)：15 条公式规则和前后对照
- [repairs.md](references/repairs.md)：回源修复的全部写法（文字、图块、题注、合图拆图、边缘噪声）
- [mineru-api.md](references/mineru-api.md)：MinerU 接口、结果结构、坐标系、下载回退
- [zotero-sync.md](references/zotero-sync.md)：同步安全模型、字段映射、批注与附件审计

实测案例（在线）：

- [课件与教材](https://github.com/luffysolution-svg/sanmu-skills/blob/main/examples/sanmu-doc2md/RESULTS.md)：《材料分析测试方法》PPT 课件、《物理化学（第六版）下册》556 页教材
- [论文与 SI](https://github.com/luffysolution-svg/sanmu-skills/blob/main/examples/sanmu-doc2md/RESEARCH-VALIDATION.md)：中文学位论文、英文双栏论文与补充材料
