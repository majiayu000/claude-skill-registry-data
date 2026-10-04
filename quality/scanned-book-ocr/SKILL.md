---
name: scanned-book-ocr
description: 将纯图片或扫描版书籍 PDF 转为确定性、页码可追溯的文本，并在不降低识别质量的前提下基准测试并发、执行完整性校验和视觉抽检。用于整本扫描书 OCR、OCR 工具选型落地和给后续拆书/检索准备可信文本；不用于已有可靠文字层的普通 PDF，也不把未经回看原页的 OCR 当作精确引文。
---

# 扫描书 OCR

把原始扫描 PDF 视为证据源，把 OCR 文本视为可搜索的派生层。默认运行固定版本的本地 `pdf-inspector + PP-OCRv6 Small`，不会上传页面。

## 运行前检查

- 当前固定运行时仅支持 Apple Silicon macOS（arm64），使用 Python 3.12 或更新版本。
- 质量抽检需要 Poppler 的 `pdftoppm`；旋转纠错使用 macOS 自带 `sips`。先检查命令可用，缺失时说明依赖，不自动进行全局安装。
- 从本 SKILL.md 所在目录解析脚本路径；输入 PDF、基准报告和输出目录由任务指定，输出放在 skill/仓库目录之外。
- 只发布通用代码与合成样例。PDF、OCR 正文、纠错文件、含本地绝对路径的 manifest/基准报告、QA 图片与运行时缓存都留在本地，不随 skill 提交。

## 核心约束

- 质量优先：先冻结模型、300 DPI 与文本规范化，再调页面并发。候选并发的逐页文本必须与单进程基线逐字节一致，否则淘汰。
- 保留页码：每页独立落盘，合并文本必须含 `=== PDF_PAGE NNNN ===` 标记。
- 可审计：`manifest.json` 记录原 PDF SHA-256、运行时版本、配置、逐页哈希、置信度、警告和耗时。
- 已完成结果可复用：转换命令检查来源哈希、运行时、DPI 和页数后返回已有 manifest；之后必须运行 validate 校验逐页及合并文件。当前不支持中途断点续跑；运行中断后保留原目录排查，使用新的输出目录重跑。
- 精确引文回看原页：OCR 可支持整书理解和候选检索，最终引用仍须核对 PDF 页面。

## 工作流

1. 先运行 `scripts/ocr_book.py benchmark`。使用代表页测试 1/2/3 个外部进程；只从输出完全等价的配置中选择中位耗时最低者。
2. 运行 `scripts/ocr_book.py convert`。输出 `pages/`、`book.txt` 与 `manifest.json`。
3. 运行 `scripts/ocr_book.py validate --render-samples`。自动检查页数、哈希、低置信度、短页、重复页和合并文件，并渲染目录页、章节首页、固定间隔页及所有异常页。
4. 如果视觉抽检发现方向错误、噪声或实词错误，把旋转、整页替换和唯一匹配替换写进来源专属 corrections JSON，再运行 `scripts/ocr_book.py apply-corrections`；不要直接编辑页文件。应用后必须重新验证。
5. 人工查看全部抽检图片后，用 `scripts/ocr_book.py record-qa` 记录通过或失败。只有 `quality-report.json.status=passed` 才能交给下游蒸馏。

脚本会把固定版本运行时放到用户缓存，不修改系统 Python，不全局安装包。首次运行会下载并校验固定 SHA-256 的 wheel、PDFium、ONNX Runtime 和 OCR 模型。

## 判停

- 任一下载哈希不符、页面缺失、页文件哈希不符、合并文本不一致或并发输出变化：立即失败。
- OCR 报告建议转云端、出现异常短页/重复页或人工抽检发现实词错误：不得宣布通过；回到 OCR 配置或原页复核。
- 不为速度降低 DPI、换小模型或跳过质量页。

## 输出与命令

在 skill 目录运行以下命令，将尖括号参数替换为任务实际路径：

```bash
python3 scripts/ocr_book.py benchmark "<扫描 PDF>" --report "<基准报告.json>"
python3 scripts/ocr_book.py convert "<扫描 PDF>" --benchmark-report "<基准报告.json>" --output-dir "<输出目录>"
python3 scripts/ocr_book.py validate --output-dir "<输出目录>" --render-samples
```

查看报告要求的全部抽检页后，使用 `python3 scripts/ocr_book.py record-qa --output-dir "<输出目录>" --status passed --reviewed-pages "<已核对页码，如 1-3,20>" --note "<核对结果>"` 记录；未通过时用 `--status failed`。完整参数见各子命令 `--help`。

供 AI 读取的主产物是 `book.txt`；如需 Markdown，在最终校验通过后将其复制为 `book.md`，保留页码标记和原文，不改写内容。当前不生成带文字层的可搜索 PDF。
