---
name: patent-search
description: "专利著录检索：中国专利公布公告（发明人、申请人、分类号、名称、摘要；也可从单图或权利要求生成名称/摘要关键字后查询）；用户点名海外时，用 Google Patents 检索美欧日韩等海外专利。"
user-invocable: false
---
> [dsh-zrwang-plugin] 工作目录优先使用 `<当前项目根>/.agents/patent/` 下的对应子目录（oa / patent-map / obsidian_vault.txt），不要写 `~/Documents/patent-disclosure-skill`；Obsidian 库路径可用 `PATENT_READER_OBSIDIAN_VAULT` 覆盖。
# 著录检索

## 用途

公布站高级查询（发明人 / 申请人 / 分类号 / 名称 / 摘要等）。个人公开清单只是一种用法。单图或权要可先抽关键字再查。对照表派工时可按特征精排，另出覆盖旁路，**不改**列表报告。用户点名海外 / 指定局时，走 Google Patents 海外检索旁路（`gp_search.py`）。

## 何时用

用户要按著录字段查公布公告、个人公开清单、以图或权要生成检索式，或 `/patent-search`。对照表派工或用户点名「按特征精排」时再走 `covers_rank.md`。用户点名「海外检索」「查美国 / 欧洲 / 日本 / 韩国专利」「PCT 检索」「包含某国」时走 `global_search.md`；没提国家时仍走公布站。

## 输入

至少一项：发明人、申请人、分类号、名称、摘要/简要说明、申请号或公开号。单图必须 `--type design|utility_model|invention`，不能 `all`；用户没说类型时看图推断并加 `--type-inferred`。权要按文本选类型，可用 `all`。海外检索至少一项：英文关键词、名称 / 摘要 / 权要字段、CPC、申请人、发明人；局别按用户点名。

## 步骤

**先 `Read` `prompts/patent_search.md`。** 用户给单图或权要时再 `Read` `prompts/derived_query.md`。对照表派工或用户点名「按特征精排」时再 `Read` `prompts/covers_rank.md`。翻页口径以该文件「默认少翻页 / 完整性门禁」为准。用户点名海外时**只** `Read` `prompts/global_search.md`。

填表语法跟公布站高级查询说明走，**按字段区分**，不要混用（细则见 `prompts/patent_search.md`）。

```bash
python ../patent-search/tools/cnipa_search.py --inventor "姓名" --applicant "单位"
python ../patent-search/tools/cnipa_search.py --title "数据处理" --abstract "吸附 and 再生" --class B01J20 --max-pages 2
python ../patent-search/tools/cnipa_search.py --abstract "折叠 and 杯盖" --type design --derived-from image --type-inferred --derived-note "折叠杯盖"
python ../patent-search/tools/cnipa_search.py --inventor "姓名" --complete
python ../patent-search/tools/gp_search.py -q "(battery OR cell) (thermal runaway)" --country US,EP,JP --after 2020
```

单独拷走本包时：`python tools/cnipa_search.py …` / `python tools/gp_search.py …`。改版式只动 `tools/emit_search_report.py`。机读前缀：`EPUB_SEARCH_MD:` / `EPUB_SEARCH_JSON:` / `EPUB_SEARCH_NOTE:` / `EPUB_SEARCH_INCOMPLETE:`；海外 `GP_SEARCH_MD:` / `GP_SEARCH_JSON:` / `GP_SEARCH_NOTE:` / `GP_SEARCH_ERROR:`。对话里给出 Markdown 路径。

`tools/google_patents/` 与解读包同名目录内容一致，改动须同步两处。

## 护栏

- 结果不得冒充交底查新。
- 本包只做公布站高级查询与点名后的 Google Patents 海外检索。单图或权要只生成公布站布尔式。覆盖精排是列表之后的可选旁路。
- 海外检索每次运行一个请求、不重试；`gp_search.py` 退出码 4（限流）即结束本轮，细则见 `prompts/global_search.md`。

## 产出物

`outputs/patent-search/SEARCH-YYYYMMDD-HHMMSS.md`（及对应 json）。公布站与海外检索同目录，海外报告标题为「海外检索」。精排旁路另出 `SEARCH-*.covers.md` / `.covers.json`，不改列表报告。本包**不设**「交付后请确认」。
