---
name: pdf-visual-translate-zh-skill
description: 英文 PDF 版式保真中文翻译 Skill：为可提取文本的英文 PDF 创建中文交付件，尽量保留页数、页面尺寸、表格、图表、颜色、页眉页脚和整体布局。适用于研报、公告、白皮书、合同和图表密集型 PDF；目标是可视中文交付，而不是干净的中文可搜索文本层。
---

# PDF Visual Translate · 英文 PDF 版式保真中文翻译 Skill

[English version](SKILL.en.md)

## 这个 Skill 做什么

这个 Skill 把英文 PDF 转换成视觉上接近原文档的中文 PDF。

它以源 PDF 作为视觉底层，在原坐标覆盖可见英文，再把简洁中文绘制回去。适合可提取文本的 PDF，例如报告、研报、披露文件、白皮书、合同和类幻灯片 PDF。

这个工作流优先保证版式保真，而不是生成可搜索的中文文本层。覆盖模式可能保留底层英文文本；如果用户需要复制、搜索或二次编辑中文，要提前说明。

## 操作原则

- 翻译前先诊断 PDF。
- 把翻译状态保存在文件中，不依赖聊天上下文。
- 分小批导出、翻译、合并补丁到缓存。
- 除非上下文明确要求翻译，否则保留专有名词、股票代码、产品名、数据集名、URL、邮箱、数字和短代码。
- 交付前做视觉 QA，尤其检查密集表格、图表、彩色表头和法律/披露页。
- 不要把整份 PDF 栅格化，除非用户接受不可搜索的图片型 PDF。

## 决策指南

适合使用本路线的情况：

- PDF 有可提取的英文文本。
- 用户想要看起来像原文件的中文 PDF。
- 页数、页面尺寸、图表、表格、颜色、Logo、页眉页脚必须稳定。

需要暂停或换路线的情况：

- `diagnose_pdf.py` 显示文本密度很低：先 OCR，再重试。
- PDF 加密：向用户索要密码或解密后的源文件。
- PDF 含表单字段或注释：页面覆盖翻译可能不会更新字段值或注释内容，需要单独检查。
- 用户需要可选择、可搜索的中文文本：单纯覆盖模式不是理想最终格式，除非额外做干净文本层重建。

## 快速流程

设置路径：

```bash
PDF="/path/to/source.pdf"
WORK="/tmp/pdf-visual-translate-zh"
GLOSSARY="$WORK/glossary.json"
CACHE="$WORK/translations.json"
OUT="$WORK/output-zh.pdf"
mkdir -p "$WORK"
cp references/glossary-template.json "$GLOSSARY"
```

### 1. 诊断

运行预检：

```bash
python3 scripts/diagnose_pdf.py \
  --source "$PDF" \
  --json-output "$WORK/diagnosis.json"
```

再检查翻译抽取器看到的元数据：

```bash
python3 scripts/visual_translate_pdf.py --inspect --source "$PDF"
```

如果文档像扫描件或图片型 PDF，先 OCR。文本抽取不可用时，不要继续视觉翻译。

### 2. 建术语表

先导出一个小批次：

```bash
python3 scripts/visual_translate_pdf.py \
  --source "$PDF" \
  --glossary "$GLOSSARY" \
  --cache "$CACHE" \
  --export-batch "$WORK/batch-000.json" \
  --batch-index 0 \
  --batch-size 40 \
  --context-chars 1200
```

只读这个紧凑批次，识别名称、品牌、股票代码、产品名、数据来源、缩写、表头和重复术语。大量翻译前先更新 `GLOSSARY`。

### 3. 预览文本框

在代表性页面渲染候选文本框：

```bash
python3 scripts/render_text_box_preview.py \
  --source "$PDF" \
  --glossary "$GLOSSARY" \
  --cache "$CACHE" \
  --pages 1,4,6,12 \
  --output-dir "$WORK/box-preview"
```

用它提前发现抽取失败、旋转页、文本碎片化和过小表格单元格，避免翻译完才发现无法放回版面。

### 4. 分批翻译

导出下一批未翻译内容：

```bash
python3 scripts/visual_translate_pdf.py \
  --source "$PDF" \
  --glossary "$GLOSSARY" \
  --cache "$CACHE" \
  --export-batch "$WORK/batch-001.json" \
  --batch-index 0 \
  --batch-size 60 \
  --context-chars 1000
```

只翻译批次中的 `items`，写成 patch JSON：

```json
{
  "Exact English source string": "简洁、准确、能放回原坐标的中文"
}
```

合并补丁：

```bash
python3 scripts/visual_translate_pdf.py \
  --source "$PDF" \
  --cache "$CACHE" \
  --merge-patch "$WORK/batch-001.patch.json"
```

重复使用 `--batch-index 0`。脚本会跳过已有翻译，所以索引 `0` 表示“下一批未翻译内容”。导出结果包含 `0 items` 时停止。

### 5. 重建

```bash
python3 scripts/visual_translate_pdf.py \
  --source "$PDF" \
  --output "$OUT" \
  --cache "$CACHE" \
  --glossary "$GLOSSARY" \
  --render-dir "$WORK/qa" \
  --compare-pages 1,4,6,12,16,22,29,37
```

如果重建生成 `.missing.txt`，不要把整个文件读进聊天。继续导出紧凑批次、翻译、合并，再重建。

### 6. 验证

交付前检查渲染出的对照 PNG：

- 页数和页面尺寸与源 PDF 一致。
- 彩色区域上没有突兀白块。
- 没有明显英文段落残留，除非是有意保留。
- 品牌、产品名、股票代码、评级和数据来源没有被误译。
- 密集表格中的中文没有小到不可读。
- 页眉、页脚、页码、颜色、图表和表格几何结构保持稳定。

## 翻译约束

- 按页面和章节上下文翻译，不要孤立处理碎片。
- 表格单元格、图例、坐标轴、标题、脚注和页脚要用短中文。
- 除非文档明确采用中文译名，否则保留专有名词和标识符。
- JSON key 必须与英文源字符串完全一致。
- 文档特定规则写进 `GLOSSARY`，不要把一次性替换硬编码进脚本。
- 对短而含糊的大写词，宁可保留英文，也不要编造中文名。

## 批次大小建议

- 标签、表格、图表、数字密集页：`60-80` 项。
- 普通报告正文：`30-50` 项。
- 法律披露、风险章节、长脚注、密集叙述页：`20-30` 项。

如果输出过长，立即降低 `--batch-size`，继续从文件状态推进。

## 脚本索引

- `scripts/diagnose_pdf.py`：PDF 预检诊断和路线建议。
- `scripts/render_text_box_preview.py`：渲染候选文本框，用于视觉验证。
- `scripts/visual_translate_pdf.py --inspect`：输出面向翻译的元数据。
- `scripts/visual_translate_pdf.py --export-batch`：导出紧凑、文件化的翻译批次。
- `scripts/visual_translate_pdf.py --merge-patch`：把一个 patch JSON 合并到缓存。
- `scripts/visual_translate_pdf.py --output`：重建中文覆盖 PDF。
- `REFERENCE.md`：OCR、修复、抽取兜底、表单、注释和 QA 的高级路线。
- `references/glossary-template.json`：每个文档的术语表和 QA 扫描起点。
- `references/pdf-translation-qa.md`：失败模式、恢复方式和人工检查清单。

## 大文档硬规则

- 不要把完整 PDF 文本、完整缓存 JSON、完整 `translation_jobs.json`、完整 `.missing.txt` 或完整诊断 JSON 粘进聊天。
- 使用 `--export-batch` 做翻译工作。
- 控制每批大小，让模型能干净翻译。
- 写 patch JSON 文件，然后合并进缓存。
- 把 `CACHE`、`GLOSSARY` 和批次文件当作持久状态。
- 如果响应接近输出限制，停止当前批次，降低 `--batch-size` 后继续。

## 恢复策略

- 扫描件：先 OCR，再重新诊断和导出批次。
- 缺失翻译：导出下一批紧凑批次，不要读取完整 `.missing.txt`。
- 术语错误：更新 `GLOSSARY`，覆盖受影响缓存项，然后重建。
- 中文过小：手动缩短对应缓存译文。
- 表格或产品名被误译：添加精确术语或 `keep_as_source`。
- 搜索/复制仍是英文：说明覆盖模式限制，或改走干净文本层重建方案。
