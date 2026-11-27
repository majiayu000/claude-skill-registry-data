---
name: patent-oa
description: "审查答复辅助：审查意见问答与草稿；库薄时引导案例入库。须显式触发。"
user-invocable: false
---
> [dsh-zrwang-plugin] 工作目录优先使用 `<当前项目根>/.agents/patent/` 下的对应子目录（oa / patent-map / obsidian_vault.txt），不要写 `~/Documents/patent-disclosure-skill`；Obsidian 库路径可用 `PATENT_READER_OBSIDIAN_VAULT` 覆盖。
# 审查答复辅助

## 用途

审查意见问答与内部草稿；用户确认采纳后才出意见陈述 Word。案例入库是让检索变准的配套。草稿须复核后递交，不替代代理签字。

## 何时用

须用户点名（审查意见 / OA / 入库，或 `/oa`）。库薄时先引导入库，不要挂进交底或解读的默认步骤。

## 输入

审查意见通知书、本申请文件、可选对比文件 PDF；向量配置可选。新颖性/创造性且通知书列了对比文件时，另用本包对照副本收三件套。

## 步骤

1. **`Read`** `prompts/guardrails.md` → `intake.md`
2. 向量可选：`prompts/configure_embedding.md` + `tools/config.py`
3. 答复：`prompts/respond_office_action.md` + `tools/search_cases.py --pdf`；有对比文件的实体缺陷用**本包** `write_intake.py` / `emit_chart.py` 导出驳回映射（同一会话目录）
4. 用户确认采纳：`assets/opinion_statement.md` → 本包 `tools/emit_opinion_docx.py`
5. 入库（用户同意后）：`tools/ingest_case.py`

依赖：`pip install -r tools/requirements-oa.txt`。每次答复完整回答的末块为 **`## 交付后请确认`**，按 `prompts/soft_nudge.md` 看库是否太薄（历史案少于 3），再决定是否加「案例入库」。

## 护栏

- 细则 `prompts/guardrails.md`。对照导出用本包 `write_intake.py` / `emit_chart.py`。意见陈述 Word 用本包 `emit_opinion_docx.py`。

## 产出物

`outputs/oa/{案件}/{会话}/`：意见陈述草稿 Markdown；确认后的 `.docx`；有对比文件时另有 `对照表-审查答复-{时间戳}.xlsx`（「驳回映射」页，表不写入陈述正文）。对话末块标题 **交付后请确认**。
