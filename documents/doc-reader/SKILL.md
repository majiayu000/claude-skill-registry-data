---
name: doc-reader
description: |
  Translate an English technical article (web URL) or a local PDF into accurate Chinese, section by section with consistent terminology, keeping 100% of the images, and build a local three-column preview HTML (original · translation · AI slides). Slides are generated through the local Codex CLI built-in imagegen, so no image API key is needed. Use when the user shares an English blog post, paper, docs page or PDF and wants a faithful, side-by-side Chinese version, or says /doc-reader, 翻译这篇文章, 翻译文档, 翻译博客, 翻译 PDF, translate this article. Options: --no-ppt skips slide generation, --quick translates only.

---

# Doc Reader

**准确是翻译的生命线**。采用章节级翻译策略，在保证精准的同时最大化翻译效率。

## 使用方式

```
# 在线网页
/doc-reader <URL>
/doc-reader <URL> --no-ppt    # 跳过幻灯片生成
/doc-reader <URL> --quick     # 快速模式，仅翻译不生成预览

# 本地 PDF 文件
/doc-reader <PDF_PATH>
/doc-reader /path/to/document.pdf
```

## 核心能力

1. **章节级翻译** - 以章节为单位翻译，保持上下文连贯，术语全文一致
2. **图片 100% 保留** - 自动下载所有图片，失败时保留原始链接
3. **技术术语精准** - 首次出现标注原文，专有名词保留英文
4. **三栏预览** - 原文/翻译/PPT概要同步滚动
5. **AI 幻灯片生成** - 主 session 无关，通过本机 Codex CLI 的内置 imagegen 并发生成概要图

## 脚本说明

所有脚本位于 `scripts/` 目录：

| 脚本 | 用途 |
|------|------|
| `web_fetcher.py` | 高质量网页抓取，优于 WebFetch 工具 |
| `generate_slides.py` | 并发调用 Codex CLI（默认 4 路），由内置 `$imagegen` 生成整组幻灯片 |
| `build.py` | 构建三栏预览 HTML |

> **Python 依赖**：`pip install html-to-markdown`（`web_fetcher.py` 需要；已适配 3.x 的 ConversionResult API）。首次运行缺库时脚本会 fail-fast 并提示本命令。

**🚨 关键执行规则:**

每次执行 `generate_slides.py` 和 `build.py` 前，**必须**将脚本从本 skill 的 `scripts/` 目录复制到当前工作目录 `output/{slug}/`。`build.py` 还需同目录放置 `marked.min.js`（预览的内嵌渲染库，随 scripts/ 一起复制）。

图片生成要求 `codex` 位于 `PATH`、Codex CLI 已登录，并且当前版本和账号可使用内置 imagegen。安装 CLI 本身不等于已经具备图片生成权限。

脚本依赖相对路径查找文件，必须在输出目录内执行。`SKILL_DIR` 指本 `SKILL.md` 所在目录（全局安装、项目级安装、plugin 缓存目录均适用，不要硬编码绝对路径）：

```bash
# 步骤 7: 生成幻灯片前
cp "$SKILL_DIR/scripts/generate_slides.py" output/{slug}/
cd output/{slug}
python3 generate_slides.py

# 步骤 8: 构建 HTML 前
cp "$SKILL_DIR/scripts/build.py" output/{slug}/
cd output/{slug}
python3 build.py
```

## 输出结构

```
output/{article-slug}/
├── original.md        # 原文 Markdown
├── translated.md      # 翻译版本
├── combined.md        # 双栏对照版本
├── preview.html       # 三栏交互式预览
├── images/            # 原文图片
└── slides/            # AI生成的概要图
```

## 详细执行流程

详见 [instructions.md](instructions.md) - 包含 9 个步骤的完整执行规范。

`preview.html` 是流程的最终交付物，本地用浏览器打开即可；本 skill 不提供任何在线上传或分享链接。
