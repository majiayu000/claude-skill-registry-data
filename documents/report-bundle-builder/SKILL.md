---
name: report-bundle-builder
description: >
  把多页 HTML 报告(主页 + N 子页 + PNG 资产)合并为单一独立 HTML / PDF / XLSX 三件交付物。
  Use when finalizing a disease market sizing report and need shareable deliverables —
  single-file HTML for email/IM(零依赖,双击浏览器开), optional PDF for print/archive,
  XLSX for data export. 领域无关、跨疾病通用。
  下游 of disease-market-sizing-html-template;上游 of email/IM/print 分发。
  Use proactively whenever the user says "做交付物" / "生成 PDF" / "导 Excel" / "合并单文件 HTML"。
license: MIT
---

# report-bundle-builder · 报告交付物 L2 skill

## 一句话定义

把市场调研项目的 `main.html + page_*.html + flowchart_*.png` 资产组装成
"双击即可阅读 / 邮件可发 / Excel 可分析"交付物。所有图片 base64 内嵌、XLSX schema 驱动；PDF 仅在用户明确要求或调用方显式 `skip_pdf=False` 时生成。

Production delivery must reject report-shaped shells: sub-pages with only a few hundred bytes, source inventory masquerading as body content, deferred worker/model language, and shallow Mermaid blocks are bundle blockers even when `verification_report.json` is `ok`.

PDF is optional and must stay disabled by default unless the caller/user explicitly requests it. XLSX is part of the production evidence pack: the `Sources` sheet must cover every non-raw file under `.cache/<slug>/sources/**`, merged with `source_manifest.json` metadata when available. Listing only the primary guideline is an incomplete delivery.

Production report runs must write into their own `output/<slug>/` directory and keep previous run folders intact. Do not place new production deliverables directly in a shared root output folder.

Embedded or linked subpage material must not insert complete nested HTML documents into `report_standalone.html`; persist subpages as standalone files, but embed only sanitized body fragments when a main-report anchor section is needed.

Production XLSX must be an analysis workbook, not a placeholder export. Required sheets include `Summary`, `Sources`, `Verification`, `Staging`, `MarketModel`, `LPFramework`, `CohortMatrix`, `CitationAudit`, and `MermaidAssets` when the corresponding inputs exist.

`delivery_manifest.json` must record `deliverables.html.validation.placeholder_checked=true`. HTML is checked against visible placeholder/deferred-language terms before bundling, and production smoke blocks manifests that leave HTML placeholder validation unchecked.

---

## 何时调用

- 用户说"生成 standalone HTML / PDF / XLSX"
- 多页 HTML 报告完工,要做最后的交付物组装
- 邮件/即时通讯/网盘分享前的"合并 + 内嵌"
- 需要把数据导出 Excel 给同事做透视

## 何时不调用

- 还在生成 HTML 内容 → 用 `disease-market-sizing-html-template`
- 还没召回数据 → 用 7 retrieval skill 走 `disease-market-sizing-orchestration` 流水线
- 只要 Markdown 不要 HTML/PDF → 用 `article-writing` 或 `docx`

---

## 与其他 skill 的协作

```
召回层 (7 retrieval skill: pubmed-eutils / europepmc-search / clinical-trials-v2 /
        aact-bulk-trials / bioc-fulltext-fetch / pubtator-entity-search /
        medical-evidence-grading)
        ↓
内容层 (disease-market-sizing-html-template + market-sizing-mece-foundation
        + decision-tree-with-lp-embedding + evidence-appendix-sync)
        ↓ 输出: main.html, page_*.html, flowchart_*.png
交付层 (本 skill: report-bundle-builder)  ← YOU ARE HERE
        ↓ 输出: report_standalone.html, .pdf, _data.xlsx, delivery_manifest.json
分发层 (邮件 / IM / 网盘 / 打印)
```

---

## 4 个核心函数

### 1. build_standalone_html

```python
from pathlib import Path
from build_standalone_html import build_standalone_html

result = build_standalone_html(
    main_html=Path("output/report.html"),
    sub_pages=[
        ("AML", Path("output/page_AML.html")),
        ("MDS", Path("output/page_MDS.html")),
    ],
    png_dir=Path("output"),
    out_path=Path("output/report_standalone.html"),
    intra_page_anchors=["decision", "calc", "lp", "evidence"],  # 血液项目用,通用场景留 None
)
# {"ok": True, "size_mb": 9.3, "png_count": 8,
#  "missing_pngs": [], "validation": {...}}
```

**关键参数:**

- `sub_pages`: `[(slug, path), ...]` · slug 用作 anchor id(`#page-{slug}`)
- `png_dir`: PNG 资产目录(`<img src="X.png">` 相对此目录解析)
- `intra_page_anchors`: 子页内部 `href="#decision"` 等改写为 `href="#page-{slug}-decision"` 的 anchor 名列表;None/空时不改写
- `auto_validate`: 默认 True · size > MIN_BUNDLE_BYTES(1 MB)+ anchor_count == 子页数
- 缺失 PNG 不抛错,记录在 result["missing_pngs"](见 [bundle-manifest-spec.md](references/bundle-manifest-spec.md))

### 2. build_pdf

```python
from build_pdf import build_pdf

# 单遍模式(快)
result = build_pdf(
    html_path=Path("output/report_standalone.html"),
    out_path=Path("output/report.pdf"),
)

# 两遍模式(注入 TOC 页码)
result = build_pdf(
    html_path=Path("output/report.html"),
    out_path=Path("output/report.pdf"),
    toc_anchors=[
        ("#ch1", "一、执行摘要"),
        ("#ch2", "二、研究方法"),
    ],
)
# {"ok": True, "size_mb": 9.6, "pages": 32, "mode": "two-pass"}
```

**安全保证:**

- 两遍模式自动备份 html_path,Pass 2 失败时从备份恢复
- pass1 临时 PDF 用 `tempfile.mkstemp` 避免并发碰撞
- pypdf 不可用时 `pages=None`,`pages_ok=True`(不算失败)

详见 [chrome-headless-setup.md](references/chrome-headless-setup.md)。

### 3. build_xlsx

```python
from build_xlsx import build_xlsx

result = build_xlsx(
    data={
        "overview": [["总 PMID", 200, "PubMed"], ["NCT", 30, "CT.gov"]],
        "lp_ranking": [["LP1", 8.5, "GRADE A"]],
    },
    schema_yaml=Path("data/xlsx_schema.yaml"),
    out_path=Path("output/report_data.xlsx"),
)
# {"ok": True, "sheets": ["T1_overview", "T2_lp_ranking"]}
```

**Schema YAML 格式:**

```yaml
sheets:
  - name: T1_overview
    headers: ["指标", "值", "来源"]
    column_widths: [22, 16, 28]
    data_key: overview

  - name: T2_lp_ranking
    headers: ["LP 名称", "得分", "证据等级"]
    column_widths: [30, 12, 18]
    data_key: lp_ranking
```

- 调用方在 `data` dict 用 `data_key` 索引,值是 `[[row...], [row...]]`
- 缺字段(name/headers/data_key)→ 带索引的 ValueError(`Sheet #2 missing 'headers'`)
- out_path 父目录自动 mkdir

### 4. build_all_deliverables(一键封装)

```python
from build_all import build_all_deliverables

manifest = build_all_deliverables(
    report_dir=Path("output"),
    out_dir=Path("output"),
    sub_pages=None,           # None → 自动扫描 page_*.html
    toc_anchors=[("#ch1","一、执行摘要")],  # 给 PDF
    xlsx_schema=Path("data/xlsx_schema.yaml"),
    xlsx_data={...},
    disease_slug="lung-tb-china",
)
# 写入 output/delivery_manifest.json
# 任一失败不阻塞其余,manifest 记录详情
```

**自动检测顺序**(main.html):

1. `report_dir/main.html`
2. `report_dir/report.html`
3. `report_dir/report_v<N>.html` 中版本号最大的(`report_v25.html` > `report_v9.html`)

**部分失败处理:**

- HTML 失败 → PDF 用 main.html fallback,manifest 标 `pdf.fallback_input=True`
- PDF 失败 → XLSX 仍尝试
- xlsx_schema 或 xlsx_data 缺一 → xlsx 跳过,标 `ok=False, error=skipped`

详见 [bundle-manifest-spec.md](references/bundle-manifest-spec.md)。

---

## 自动验证规则

| 函数 | 默认验证 | auto_validate=False 时 |
|-----|---------|----------------------|
| build_standalone_html | size > 1 MB,anchor_count == 子页数 | 跳过 |
| build_pdf | size > 1 MB,pages ≥ 1(或 pypdf 不可用 → 不算失败) | 跳过 |
| build_xlsx | size > 1 KB,sheet_count ≥ 1 | 跳过 |

阈值常量集中在 `_validate.py`:`HTML_MIN_SIZE_BYTES` / `PDF_MIN_SIZE_BYTES` / `PDF_MIN_PAGES` / `XLSX_MIN_SIZE_BYTES` / `XLSX_MIN_SHEET_COUNT`。

---

## 失败模式速查

| 症状 | 原因 | 修复 |
|------|------|------|
| `RuntimeError: No Chrome/Edge/Chromium found` | PDF 渲染缺浏览器 | 装 Chrome 或显式 `chrome_path=` · 见 [chrome-headless-setup.md](references/chrome-headless-setup.md) |
| `ValueError: Main HTML missing <body>` | 主页 HTML 不含 `<body>` | 检查 main_html 是否真页面 |
| `ValueError: Sheet #N missing 'X'` | xlsx schema 字段缺失 | 补全 schema 的 name/headers/data_key |
| `KeyError: data['xxx'] missing` | xlsx schema 引用 data_key 在 data dict 中缺失 | 对齐 schema.sheets[].data_key 与 data 的 key |
| HTML size < 1 MB,validation.size_ok=False | 内容太少或 PNG 丢失 | 检查 png_dir 是否对、PNG 文件存在 |
| PDF pages 远低于预期 | HTML 渲染异常或 Chrome 崩溃 | 用 Chrome 手动开 HTML 看是否正常,看 Chrome stderr |
| anchor_count < anchor_target | 子页 HTML 不含 main 标签或 slug 命名冲突 | 子页必须有 `<main>` 包裹主体内容 |
| build_all 报 xlsx skipped | xlsx_schema 或 xlsx_data 任一为 None | 同时传两个,或接受 xlsx ok=False |
| Output HTML 在浏览器打不开 | 主页编码非 UTF-8 | 重新生成主页保证 UTF-8 BOM 无 |
| `result["missing_pngs"]` 非空 | 主页/子页引用了 png_dir 不存在的 PNG | 检查 PNG 文件名拼写或是否生成 |
| 两遍模式 Pass 2 失败但 HTML 未损坏 | 备份恢复机制工作正常 | 排查 Chrome 错误,原 HTML 已自动从备份恢复 |

---

## 跨平台兼容

- Windows / Linux / macOS 全部支持(Chrome 检测分平台,见 [chrome-headless-setup.md](references/chrome-headless-setup.md))
- Python 3.10+(PEP 604 `X | None` 语法)
- 依赖:`httpx` + `lxml` + `pyyaml` + `openpyxl` + 可选 `pypdf`(无则 PDF 不能测量页数,但仍能渲染)

---

## 版本

- v1.0(2026-04-25):从血液科 IFI v2.5.3 项目下沉而来,首个领域无关版本
  - build_standalone_html(parametric API,intra_page_anchors 可配)
  - build_pdf(单/两遍模式,跨平台 Chrome,备份恢复)
  - build_xlsx(schema YAML 驱动)
  - build_all_deliverables(一键封装 + delivery_manifest.json)
