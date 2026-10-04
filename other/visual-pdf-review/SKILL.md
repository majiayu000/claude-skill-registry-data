---
name: visual-pdf-review
description: 论文 PDF 视觉排版审稿。把已编译的 PDF 逐页渲染成图片，做确定性几何检查（空白页、页边距溢出、图超宽、页底孤立标题、Overfull/Float too large 等），再用用户可选的视觉后端（Codex 自身视觉/OAuth 登录、GitHub Copilot、OpenCode Go、任意 OpenAI 兼容接口如 New API）逐页看图，产出带页码、截图证据、严重级别和 LaTeX 修复建议的排版审查报告。用于审稿阶段、投稿前终检、S12 三轮审查的视觉维度、S11 排版后验收；触发词：视觉审稿、排版审稿、看 PDF、PDF 排版、layout review、visual review、页面留白、图注分离、孤立标题、联系表。
---

# Visual PDF Review（PDF 视觉排版审稿）

## 作用

对已编译的论文 PDF 做一轮“用眼睛看”的排版审稿：

1. 渲染每页为 PNG，并生成联系表（contact sheet）便于总览；
2. 脚本做确定性几何检查；
3. 用用户选择的视觉后端逐页审图；
4. 产出结构化报告（页码、严重级别、截图证据、LaTeX 修复建议）并写入 `.research/`。

只审查排版/布局，不审查科学内容。若同时需要内容审稿，用 academic-research-suite(academic-paper-reviewer)。

## 选择视觉后端（用户可选）

先用 `scripts/configure_provider.py` 选择后端并写入 `.codex/visual-review.json`；也可以每次运行用 `--provider` 临时指定。后端：

| provider | 说明 | 密钥 |
|---|---|---|
| `codex` | Codex 自身视觉（桌面端直接看图；OAuth/ChatGPT 登录态即可用） | 无 |
| `custom` | 任意 OpenAI 兼容接口（New API、xindu、自建网关等） | `VR_API_KEY` |
| `opencode-go` | OpenCode Go 订阅（默认视觉模型 mimo-v2.5） | `OPENCODE_GO_API_KEY` |
| `copilot` | GitHub Copilot（api.githubcopilot.com，OAuth 或 gh 登录） | `COPILOT_TOKEN` 或 `gh auth token` |

细节、端点、默认模型见 [references/providers.md](references/providers.md)。密钥一律走环境变量，不写入配置文件。

## 标准流程

按顺序执行。先让用户点名课题，再运行 `research-ledger/scripts/project_context.py --project <id>` 取得该项目的 `project_memory`；所有产物放在 `<project_memory>/visual_review/<run-timestamp>/`（不存在则创建）。用户未点名课题时提示指定，禁止把审稿报告写入共享层。

### 1. 渲染页面

```bash
python scripts/render_pdf.py <paper.pdf> --out-dir <run_dir>/pages --dpi 110
```

输出 `page_001.png ...`、`contact_sheet.png`、`render_meta.json`。需要 `pymupdf`；缺省时回退 `pdftoppm`。

### 2. 几何检查（确定性）

```bash
python scripts/geometry_check.py <paper.pdf> --out-dir <run_dir>/pages \
  --tex-log <main.log>   # 可选，有 LaTeX log 时提供
```

检查：空白页、内容覆盖率过低、文本块越界、图片超文本宽度、页底孤立标题、log 中的 Overfull/Underfull/Float too large/未定义引用。结果写入 `geometry_findings.json` 与 `geometry_report.md`。

### 3. 视觉审稿（模型/Codex 看图）

```bash
# 用户已配置好的后端：
python scripts/vision_review.py --images-dir <run_dir>/pages

# 或临时指定：
python scripts/vision_review.py --images-dir <run_dir>/pages \
  --provider custom --base-url https://xindu.xyz/v1 --model gpt-5.6
```

`provider=codex` 时脚本只生成审稿提示；**你（Codex）必须真正用图像查看工具逐张打开 `page_*.png` 和联系表来审**，不允许只看文件名或文本。逐页按 [references/review-checklist.md](references/review-checklist.md) 记录问题。

### 4. 合并报告

汇总几何检查与视觉审稿，写 `visual_review_report.md`：

- 每个问题：页码、严重级别（P0/P1/P2）、类型、描述、截图证据（引用 `pages/page_XXX.png`）；
- 按严重级别排序，P0 必须修复，P1 投稿前修复，P2 建议优化；
- 对每个 P0/P1 给出可执行的 LaTeX 修复建议；排版修复按 venue-templates 的模板约束与本文检查清单执行（浮动体松散、孤立标题、`[H]`/`\clearpage` 使用、宽扁图重绘等）；
- 明确区分“几何脚本发现”与“视觉模型判断”，不要混为一谈；
- 若目标期刊/模板已知，先按 venue-templates 的模板要求校准检查标准。

### 5. 回写与收敛

- 报告写入当前项目 `<project_memory>/visual_review/<run-timestamp>/`；
- 若有 P0/P1，回 S11 修复并重新编译后**再跑一轮**，直到无 P0、P1 低于阈值；
- 在 research-ledger 记录本次审稿结论；作为 S12 三轮审查的视觉维度纳入终检。

## 红线

- 只报告真实可见的问题：几何检查必须来自真实测量，视觉问题必须来自实际看图，禁止编造截图或问题；
- 不替用户修改论文，除非用户明确要求修复；修复后必须重新编译复检；
- 密钥不写入报告、配置或日志。
