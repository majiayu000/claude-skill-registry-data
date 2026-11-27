---
name: patent-reader
description: "专利通俗解读：中国或海外（美欧日韩等）公开号 / PDF 成通俗笔记、图谱与 Obsidian 入库。"
user-invocable: false
---
> [dsh-zrwang-plugin] 工作目录优先使用 `<当前项目根>/.agents/patent/` 下的对应子目录（oa / patent-map / obsidian_vault.txt），不要写 `~/Documents/patent-disclosure-skill`；Obsidian 库路径可用 `PATENT_READER_OBSIDIAN_VAULT` 覆盖。
# 专利通俗解读

## 用途

把公开号 / PDF / 全文读成通俗笔记、图谱，并可写入 Obsidian。独权拆成稳定特征行（`claim_features.json`），说明书段落可机读（`description_paragraphs.json`），给对照表当输入。海外公开号（US / EP / WO / JP / KR 等）一次请求取结构化全文，机翻文献同时保留原文。

## 何时用

用户说读专利、给出公开号或 PDF 且目标是「读懂」，或 `/patent-read`、`/读专利`。用户给的公开号本身是海外号，即按海外件读，不另需口令；只读这一件，不顺带做海外检索。对照表派工缺 `claim_features.json` 或 `description_paragraphs.json` 时由对照表点名进入。对照表只要这两份文件，不写笔记、不入库。

## 输入

公开号（中国或海外）、专利 PDF、或粘贴的权利要求/说明书。对照表派工时默认把从属权也拆进 `claim_features.json`，并保留 `description_paragraphs.json`。

## 步骤

1. **`Read`** `prompts/patent_plain_reader.md`。对照表派工只做到该文件「对照表派工」段，不写笔记
2. 用户要读懂、且为实用新型或外观：**`Read`** `prompts/type_hooks.md` + `prompts/fill_*`
3. 笔记 / 自检：`obsidian_ofm_companion.md`、`patent_reader_self_check.md`

工具在本包 **`tools/`**（`extract/` · `analyze/` · `vault/` · `google_patents/`）。中国件 PDF：`tools/extract/fetch_patent_pdf.py`；海外件全文：`tools/extract/fetch_gp_fulltext.py`；入库：`tools/vault/write_patent_obsidian_note.py`。特征行校验：`tools/analyze/validate_claim_features.py`。`tools/google_patents/` 与检索包同名目录内容一致，改动须同步两处。

## 护栏

- 笔记、PDF 与特征行只用本包 `tools/`。
- Google Patents 请求不重试：限流（退出码 4 / 「限流」报错）即停止本轮取证，请用户稍后再试或提供 PDF。

## 产出物

工作区 **`outputs/patent_reader/`**：通俗笔记、图谱中间产物、`claim_features.json`、`description_paragraphs.json`（含 `source_url`）。海外件另有 `source/{公开号}.gp_detail.json` 与 `fetch_gp_status.json`。有库则另写入 Obsidian。对话给出笔记路径。
