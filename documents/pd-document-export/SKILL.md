---
name: pd-document-export
display_name: 文档导出路由
description: 教 Agent 何时用 export_document 一键交付，何时用 anth-* / compose / OCR 专用工具。
major_category: office
category_subtag: office_docs
integration_level: L1
availability: ready
document_export:
  providers: []
---

# 文档导出路由（pd-document-export）

## 何时用 `export_document`（优先）

- 已有 **Markdown 或 HTML** 源文件，需要 **PDF / Word / PPTX / Excel** 交付
- 报告、简报、落地页 HTML 的**一键导出**
- PPTX 需要**可编辑文字**（结构化 MD/HTML → python-pptx；扫描件走 MinerU）

```json
{
  "source_path": "artifacts/reports/brief.md",
  "output_format": "pdf",
  "options": { "quality": "balanced" }
}
```

## 不要用 `export_document` 的场景

| 场景 | 正确工具 |
|------|----------|
| 多张图每页一图 PDF/PPT | `compose_images_to_document` |
| 仅扫描图/PDF 转可编辑 PPT | `ocr_to_editable_pptx` 或 `export_document` + `pptx` |
| Word 模板 unpack、批注、复杂样式 | `anth-docx` skill |
| PPT 母版深度改稿 | `anth-pptx` skill |
| 财务模型公式 Excel | `anth-xlsx` skill |
| PDF 表单填写 | `minimax-pdf` fill / `anth-pdf` |
| HTML 动效视频 | `render_html_video` |

## 质量档位

- `fast` / `balanced`：本机 Playwright / docx-js / python-pptx / exceljs
- `fidelity`：可触发 Nutrient（HTML）或 minimax-pdf（PDF 设计感）

## 工作流建议

1. `write_file` 写好 `artifacts/.../*.md` 或 `.html`
2. `export_document` 按用户要求的格式导出（可多次调用不同 `output_format`）
3. 成果路径写在 `artifacts/documents/` 或用户指定 `output_path`

## UI 一键导出（与用户自助分工）

- 用户在**成果预览 / 右栏**点彩色 PDF/Word/PPT/Excel 图标时，由 UI Server 异步 Job 调用同一套引擎，**无需 Agent 权限弹窗**。
- **配图幻灯**（`artifacts/slides-*/slide-*.png`）：UI 默认整套 `compose_images` → PDF/PPTX；可编辑文字走 OCR。
- Agent 仍负责：批量多文件、自定义 `output_path`、对话内编排；用户单文件交付优先引导点预览区导出按钮。
