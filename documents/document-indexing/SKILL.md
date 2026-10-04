---
name: document-indexing
description: 多源文档（PDF/PPTX/DOC/XLSX/图片）向量化索引与检索。当用户需要把一批文档提取文本、建索引、向量化、建库、检索查询时使用。含扫描页 OCR、TF-IDF 索引、余弦相似度检索。
---

# document-indexing（文档向量化索引与检索）

## 触发条件
当用户出现以下意图时使用本 skill：
- "把这份 PDF 索引/向量化/建库"
- "提取 PDF/PPTX/DOC/XLSX 文本"
- "扫描页 OCR"
- "建索引/检索/查询文档"
- "给一批文档建检索系统"
- "文档分块/embedding/TF-IDF"

## 适用范围
- ✅ 多源文档：PDF（含扫描页）、PPTX、.doc/.docx、.xlsx、图片（JPG/PNG）
- ✅ 中文为主、英文数字混杂的文档（单字分词 + 连续字母数字词）
- ✅ 离线环境（TF-IDF 稀疏向量，无需预训练模型）
- ❌ 不适用：纯英文文档（分词器针对中文优化）、需要 dense embedding 语义检索的场景（见"升级路径"）

## 工具链位置
- 脚本目录：`~/.voyah/skills/document-indexing/scripts/`
- 数据目录：`~/.voyah/skills/document-indexing/data/`（自动创建）
- 依赖：见同目录 `package.json`，首次使用前需 `npm install`

## 核心流程（5 阶段）

```
[1. 提取]  按文件类型选脚本 → 输出 data/docs/<doc>/pages/*.json + *.png
   │
   ▼
[2. 扫描页识别]  scan-pages-report.mjs → data/docs/<doc>/scan-pages-to-ocr.json
   │
   ▼
[3. OCR]  ocr-scan-pages.mjs → data/docs/<doc>/ocr-results.json（无扫描页可跳过）
   │
   ▼
[4. 分块+合并]  chunking.mjs → merge-ocr.mjs → data/docs/<doc>/chunks-merged.json
   │
   ▼
[5. 全局合并+索引]  merge-chunks.mjs → index-tfidf.mjs → data/chunks-merged.json + data/index.json
   │
   ▼
[查询]  query.mjs "问题" 5 → Top-K 结果（含 sourceDoc/pageNo/chunkId）
```

## 阶段 1：提取（按文件类型选脚本）

| 文件类型 | 脚本 | 命令 |
|---|---|---|
| PDF | `extract-pdf.mjs` | `node extract-pdf.mjs --pdf=<path> --doc=doc1 [--max=152]` |
| PPTX | `extract-pptx.mjs` | `node extract-pptx.mjs --pptx=<path> --doc=doc4` |
| .doc/.docx | `extract-doc.mjs` | `node extract-doc.mjs --docx=<path> --doc=doc5` |
| .xlsx | `extract-xlsx.mjs` | `node extract-xlsx.mjs --xlsx=<path> --doc=doc6` |
| 图片 | `extract-image.mjs` | `node extract-image.mjs --image=<path> --doc=doc7` |

**强制 checkpoint**：
- 每份文档必须用 `--doc=<name>` 指定独立子目录名（如 doc1, doc2），避免覆盖
- `--max` 仅 PDF 需要（大文件分批处理），其他类型自动全量
- 输出结构统一：`data/docs/<doc>/pages/page-NNN.json` + `manifest.json`

## 阶段 2：扫描页识别

```bash
node scan-pages-report.mjs --doc=doc1
```
- 识别"文本极少但含图片"的扫描页
- 输出 `data/docs/<doc>/scan-pages-to-ocr.json`
- **跳过条件**：PPTX/.doc/.xlsx/纯文本 PDF 无扫描页，此阶段可跳过直接进入阶段 4

## 阶段 3：扫描页 OCR

```bash
node ocr-scan-pages.mjs --doc=doc1 [--max=152]
```
- 用 tesseract.js + chi_sim 对扫描页图片做 OCR
- 增量处理：已 OCR 的图片跳过，每 10 张保存一次防中断
- 输出 `data/docs/<doc>/ocr-results.json`
- **跳过条件**：无扫描页时跳过（merge-ocr.mjs 会自动处理）

## 阶段 4：分块 + 合并 OCR

```bash
node chunking.mjs --doc=doc1
node merge-ocr.mjs --doc=doc1
```
- chunking：按段落切分，目标 500 字、重叠 80 字
- merge-ocr：把 OCR 文本附加到对应 chunk；**无 OCR 时自动复制 chunks.json → chunks-merged.json**
- 输出 `data/docs/<doc>/chunks-merged.json`

## 阶段 5：全局合并 + 索引

```bash
node merge-chunks.mjs
node index-tfidf.mjs
```
- merge-chunks：合并所有 `data/docs/*/chunks-merged.json`，chunkId 加文档前缀（如 `doc1:p091-c000`）
- index-tfidf：构建 TF-IDF 索引
- 输出 `data/chunks-merged.json` + `data/index.json`

## 查询

```bash
node query.mjs "查询问题" 5
```
- 返回 Top-K 结果，含 score、sourceDoc、pageNo、chunkId、text 预览
- 支持简体中文查询繁体内容（相似度略低）

## 完整示例（处理一份新 PDF）

```bash
cd ~/.voyah/skills/document-indexing/scripts

# 首次使用：安装依赖
npm install

# 处理 doc1
node extract-pdf.mjs --pdf="C:/path/to/file.pdf" --doc=doc1 --max=152
node scan-pages-report.mjs --doc=doc1
node ocr-scan-pages.mjs --doc=doc1
node chunking.mjs --doc=doc1
node merge-ocr.mjs --doc=doc1

# 处理第二份
node extract-pdf.mjs --pdf="C:/path/to/file2.pdf" --doc=doc2
node scan-pages-report.mjs --doc=doc2
node ocr-scan-pages.mjs --doc=doc2
node chunking.mjs --doc=doc2
node merge-ocr.mjs --doc=doc2

# 重建全局索引
node merge-chunks.mjs
node index-tfidf.mjs

# 查询
node query.mjs "光伏发电项目" 5
```

## 关键踩坑（必读）

### 1. 多文档数据覆盖
- **坑**：单目录模式下，处理第二份文档会覆盖第一份
- **解**：每份文档用 `--doc=<name>` 指定独立子目录，merge-chunks.mjs 自动加前缀

### 2. 无扫描页时 merge-ocr 行为
- **坑**：无 OCR 文件时 merge-ocr 退出，导致 chunks-merged.json 不生成，后续 merge-chunks 跳过该文档
- **解**：merge-ocr.mjs 已修复，无 OCR 时自动复制 chunks.json → chunks-merged.json

### 3. PPTX HTML 文本污染
- **坑**：pptxtojson 的 content 字段是 HTML，直接用会污染 chunks、TF-IDF 被标签词干扰
- **解**：extract-pptx.mjs 的 stripHtml 已剥离标签、解码实体；表格 cell.text 也是 HTML，同样处理

### 4. .doc 旧格式
- **坑**：.doc（OLE 二进制）无法用 pdfjs 解析，系统无 LibreOffice/Word
- **解**：word-extractor 直接解析二进制，按 ~800 字生成"虚拟页"，不提取图片

### 5. 繁体中文
- TF-IDF 单字分词对繁体同样适用（按 Unicode Unified_Ideograph 判断）
- 简体查询能命中繁体内容，用繁体关键词可提升召回

### 6. 图片对象异步解析（PDF）
- pdfjs 的图片 XObject 是异步解析的，getOperatorList 之后未必 resolved
- extract-pdf.mjs 的 getImageObject 用 callback + 8 秒超时兜底

## 升级路径（可选）
1. **Dense Embedding**：有网络时可换 `vectra` + `TransformersEmbeddings`（Xenova/all-MiniLM-L6-v2）
2. **OCR 升级**：图片预处理（二值化、放大）+ `chi_sim_best` 或 PaddleOCR / 多模态大模型
3. **服务化**：query.mjs 包装为 HTTP API 或飞书 bot

## 与其他 skill 协作
- `official-document-generation` skill 在"建数据字典"阶段可调用 `query.mjs` 从已索引文档中检索关键数据
- 查询结果含 sourceDoc/pageNo，便于在正文中标注数据来源
