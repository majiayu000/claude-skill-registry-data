---
name: paper-reading-management
description: Manage academic paper reading workflows from local PDFs, URLs, web search, Zotero, Obsidian/Dataview, or optional Feishu/Lark publishing. Use when Codex is asked to find papers, read and summarize papers, run an independent paper-reading agent, create annotated reading notes, generate quick retrieval entries, organize papers into local folders, look up/import papers in Zotero, capture citation metadata, plan paper tags, edit Zotero tags, or mirror paper notes to cloud docs.
---

# Paper Reading Management

## Overview

Use this skill to turn a paper request into a reproducible reading packet: Zotero-first source resolution, mandatory independent paper reading, local note organization, a one-sentence summary for retrieval and Zotero Style 简记, manual figure/table placeholders without image extraction, optional Zotero tagging/import, and optional cloud publishing.

Default to one management workflow. Split work into a separate Zotero-focused skill only if the user mainly asks for long-running library curation, duplicate cleanup, collection restructuring, or tag taxonomy maintenance without reading papers.

## Workflow

1. Resolve the paper source.
   - Prefer Zotero when available. Search Zotero first for known papers and use Zotero as the primary library of record.
   - If a Zotero item has a PDF attachment, read the attachment in place instead of copying it into the local note folder. Use `scripts/zotero_pdf_path.py <item-key> --first` to get the local PDF path.
   - If the paper is not in Zotero, use user-provided PDF/URL/DOI/arXiv/OpenReview/publisher page or web search to find the official source. Prefer arXiv, OpenReview, publisher, DOI, project, or author pages.
   - When a reliable BibTeX/RIS/connector route exists, import the paper into Zotero before organizing notes. If import or PDF attachment is blocked, keep the official source URL in metadata and report the blocker.
   - If working in a project with local paper-index instructions, follow that local index before web search.
   - Use web search when the paper is not local or metadata needs verification; prefer official sources such as arXiv, OpenReview, publisher pages, project pages, or DOI landing pages.
   - Do not use unauthorized PDF sources.

2. Capture metadata before reading.
   - Record title, authors, date, venue/source, URL/DOI/arXiv id, local PDF path, Zotero item key, BibTeX key when available, and retrieval date. Use `date` for the paper's first public release date when available, preferably the arXiv v1 submission date for preprints.
   - Verify the latest formal publication/version online before finalizing `publication`, folder name, and index label. Prefer OpenReview/conference/publisher records over arXiv when a paper has since been accepted.
   - Verify official project and GitHub/code links online. Leave `github_url` blank if no official repository is found; do not use unrelated repos.
   - Do not invent missing metadata. Mark unknown fields explicitly.

3. Read and summarize with a subagent.
   - Always spawn a fresh subagent for paper reading tasks with no inherited conversation context; do not reuse the main conversation as the reading context.
   - This is a hard gate. If a fresh isolated subagent is unavailable, do not create or update `note.md`; report the blocker and stop before producing a reading note.
   - For batches, spawn one independent subagent per paper. A subagent must not read or summarize multiple papers unless the user explicitly asks for a cross-paper comparison.
   - Pass only the paper source, verified metadata, and the exact reading prompt. Do not pass unrelated project chat history, previous notes, earlier summaries, or the main thread's conclusions.
   - Explicitly instruct the subagent not to read existing `note.md`, `retrieval.md`, `metadata.json`, prior generated reports, or any previous conversation context. The subagent should read the PDF/source itself.
   - After receiving the subagent's final result and integrating it into `note.md`, close the subagent.
   - Use `references/reading-report-prompt.md` as the single source of truth for the reading report prompt. Do not paraphrase, translate, restructure, or duplicate this prompt in another reference file.
   - Use `references/blank-agent-prompt.md` only as the mandatory subagent handoff scaffold.
   - Require claims to be grounded in the paper text. Separate paper claims from the reader's interpretation.
   - The subagent reading report is the source of truth for `note.md`. Do not prepend YAML frontmatter, metadata blocks, prompt text, tags, index entries, or extra sections to `note.md`.
   - Preserve the reading report's section order and heading structure from `references/reading-report-prompt.md`; the body may be Chinese because the prompt requests Chinese output.
   - Ensure `## 0. Concise Summary` includes `Topic`, `Problem`, `Method`, `Innovation`, `Significance`, and exactly one `**One-sentence summary**:` line. The entire reading report must be written in Chinese.
   - Record the isolated reading provenance in `metadata.json` when possible: `reading_agent_isolated: true`, `reading_agent_fork_context: false`, and the subagent id/name if available.

4. Organize files locally.
   - Use `scripts/organize_paper.py` to create a stable folder with `metadata.json`, `note.md`, and optional `retrieval.md`. Do not create or populate a `figures/` directory.
   - Keep machine-readable fields only in `metadata.json`. Do not duplicate them as Markdown frontmatter in `note.md` or `retrieval.md`.
   - Put exactly four front-link fields before `## 0. Concise Summary` in `note.md`, separated from the report by `---`: `Title`, `Paper link`, `Web/project link`, and `GitHub link`.
   - Put exactly the same four fields before `## Core Content` in `retrieval.md`: `Title`, `Paper link`, `Web/project link`, and `GitHub link`.
   - Build `## Core Content` by extracting `Topic`, `Problem`, `Method`, `Innovation`, and `Significance` from section `0. Concise Summary` of the generated report. Do not independently rewrite these fields unless extraction fails.
   - Extract the five concise-summary fields and the one-sentence summary into `metadata.json`. Never add a missing `One-sentence summary` line to `note.md`; the isolated reading report must supply it.
   - Put other useful bibliographic/management fields after `## Core Content`, under a secondary metadata section. This can include authors, publication, date, identifiers, PDF path, Zotero key, BibTeX key, and note path. Do not put tags or index-entry prose in `retrieval.md`.
   - Do not copy PDFs by default. Record the Zotero PDF path or source URL in metadata. Copy a PDF only when the user asks or when `--copy-pdf` is explicitly used.
   - Default local note root is `${PAPER_LIBRARY_ROOT:-$HOME/paper}`. The user may override it with `PAPER_LIBRARY_ROOT` or `--library-root`.
   - Use a project-specific root only when the user explicitly specifies one or project instructions explicitly require one. For example, use a SpaceVLN folder only when the user asks to store the note under SpaceVLN or the project task says to do so.
   - Mirror the primary Zotero collection path physically under the configured paper-library root.
   - Keep one paper per folder using `<short-title>--<publication-year>/`, e.g. `vision-language-navigation--cvpr2018`.
   - Maintain a single root `INDEX.md` tree directory. Keep it minimal: classification path plus paper short title/version linking to `note.md`.
   - For classification fields, read `references/classification-taxonomy.md`. Use layered tags: `domain_tags`, `method_tags`, `project_tags`, and a separate lightweight `zotero_tags` list for tags that should be mirrored into Zotero. `zotero_tags` must contain only the two Zotero-facing hashtag labels described in the Zotero update step.
   - For Obsidian and Dataview conventions, read `references/obsidian-dataview.md`.

5. Update Zotero.
   - Reads/search/export are safe.
   - For this skill, a user request to read and organize a paper implies permission to add the paper to Zotero when missing and to apply reading-management tags generated from the note, unless the user asks for dry-run/no-write behavior.
   - When a paper has a verified formal publication newer than its imported arXiv/preprint record, prefer updating Zotero's bibliographic metadata to the formal record. For conference papers, use Zotero item type `conferencePaper`, set `conferenceName` to the compact venue label such as `ICLR 2026`, set `proceedingsTitle` to the full venue name when known, and keep arXiv information in DOI/archive/extra fields when useful.
   - Keep Zotero tags lightweight and user-facing. Unless the user explicitly asks for a different tag taxonomy, replace all existing Zotero tags so each item has exactly two Zotero-facing hashtag tags:
     1. one kind tag: `#会议论文`, `#期刊论文`, `#预印本`, or `#网页资料`;
     2. one venue/source/version tag: for example `#NeurIPS 2025`, `#ICLR 2026`, `#arXiv 2026`, `#TMLR 2024`, or a compact web/source label such as `#Anthropic`.
     Remove legacy and unrelated Zotero tags during confirmed sync. Do not mirror collection/project tags such as `#Embodied Agent`, and do not mirror detailed `domain_tags`, `method_tags`, `project_tags`, or free-form topic/search tags into Zotero. Keep those detailed tags only in local `metadata.json`.
   - Zotero's local `/api/` routes are read-only. For writes, prefer a Zotero MCP/write bridge or connector import. Change item type only through Zotero-supported write tools or an explicitly requested, backed-up local database migration.
   - For broad library cleanup, duplicate removal, collection restructuring, or destructive changes, show the planned item keys and changes first.
   - Use the Zotero helper for search, export, import-bibtex/import-ris, children, fulltext, and file-url.
   - Use `scripts/zotero_sync_note.py` to sync `metadata.one_sentence_summary` into Zotero Style 简记, stored as a `remark:` line in Zotero `Extra`. Preserve all existing non-`remark:` lines in `Extra`; do not write the overview into `abstractNote`. The script is dry-run by default; pass `--yes` only after confirming the target item. With `--sync-tags`, require exactly two `metadata.zotero_tags` and replace all existing Zotero tags with them.
   - Use `scripts/zotero_tag_items.py --set` to replace all tags, or its add/remove/replace modes for explicitly requested ad hoc edits.

6. Return a concise handoff.
   - Include local folder path, paper source, Zotero item key if any, tags added/planned, and the `note.md` path.
   - Mention any metadata gaps, missing PDF, paywall, failed import, or unverified claims.
   - If the user asks to publish or mirror to Feishu/Lark, read `references/feishu-sync.md` and prefer `scripts/feishu_sync.py` for search/create/update/write-back orchestration; use the appropriate Lark document skill for manual follow-up edits.

## Local Organization

Create reading packets with:

```bash
python3 <skill-dir>/scripts/organize_paper.py \
	  --library-root "${PAPER_LIBRARY_ROOT:-$HOME/paper}" \
	  --title "<paper title>" \
	  --date "<first-public-release-date>" \
  --pdf "<zotero-or-local-paper.pdf>" \
  --url "<source-url>" \
  --zotero-key "<item-key>" \
  --bibtex-key "<bibtex-key>" \
  --publication "CVPR 2026" \
  --paper-url "<official-paper-url>" \
  --web-url "<project-page-if-any>" \
  --github-url "<github-repo-if-any>" \
  --collection-path "VLN/Classic" \
  --short-title "Vision-and-Language Navigation" \
  --tag "vln" --tag "spatial-memory" \
  --domain-tag "embodied-ai" \
  --method-tag "spatial-memory" \
  --project-tag "SpaceVLN-related" \
  --zotero-tag "#会议论文" \
  --zotero-tag "#CVPR 2026" \
  --topic "vision-language navigation" \
  --index-summary "Use this paper when comparing zero-shot VLN methods with explicit spatial memory." \
  --problem "continuous navigation with sparse spatial grounding" \
  --method "structured VLM reasoning with spatial memory" \
  --innovation "explicit spatial topology for zero-shot navigation" \
  --significance "improves retrieval and comparison for SpaceVLN related work" \
  --one-sentence-summary "本文聚焦视觉语言导航，针对连续环境中的稀疏空间 grounding 问题，提出带空间记忆的结构化 VLM 推理方法，创新在于显式空间拓扑建模，意义在于支持 SpaceVLN 相关工作检索和对比。" \
  --summary "<summary.md>"
```

If the PDF is not local yet, omit `--pdf` and store the verified source URL in metadata. If the PDF is in Zotero, pass the Zotero attachment path as `--pdf`; it will be recorded but not copied. Use `--copy-pdf` only when a standalone archive copy is desired. Add `--dry-run` before making folders when planning a large batch.

Get a Zotero PDF path:

```bash
python3 <skill-dir>/scripts/zotero_pdf_path.py <zotero-item-key> --first
```

## Figure/Table Placeholders

Never extract, render, crop, save, or embed paper figures/tables/screenshots in `note.md`. Immediately after the paragraph that discusses a significant original figure/table, keep one placeholder for the user to replace manually later.

Use exactly:

```markdown
<!-- figure: Figure 2 -->
```

```markdown
<!-- table: Table 1 -->
```

Omit minor figures/tables and do not add a separate screenshot appendix.

## Mandatory Figure/Table and Isolation Audit

Before returning a paper-reading task as complete, run a local audit for every paper folder. Treat failures as blockers and fix them before final handoff.

Use the bundled audit helper when possible:

```bash
python3 <skill-dir>/scripts/audit_reading_packet.py \
  --require-isolated \
  "<paper-folder-1>" "<paper-folder-2>"
```

- Isolation:
  - Confirm the reading report came from a fresh subagent with `fork_context=false`.
  - Confirm one subagent handled exactly one paper.
  - Confirm `note.md` was integrated from that subagent report, not synthesized from previous notes or main-thread history.
- Note structure:
  - Exactly one `**One-sentence summary**:` line under `## 0. Concise Summary`.
  - Required headings exist in the exact order from `references/reading-output-template.md`.
- Figure/table completeness:
  - Every Figure/Table that the note explicitly discusses must have a matching nearby `<!-- figure: Figure X -->` or `<!-- table: Table X -->` marker.
  - Keep the markers in `note.md` for the user's later manual image insertion.
  - `note.md` must not contain Markdown image embeds or local screenshots.
  - Do not mention a Figure/Table in prose and omit its marker. If it is not important enough to mark, do not highlight it.
- Batch integrity:
  - Run the audit across all target folders, not just one example.
  - Update `INDEX.md` only after the per-paper audits pass.

## Zotero Tag Editing

Dry-run first. Replace all Zotero tags with exactly the two Zotero-facing hashtag tags; keep detailed technical tags in local metadata fields:

```bash
python3 <skill-dir>/scripts/zotero_tag_items.py \
  --item-key UKRJFRVC \
  --set "#会议论文" \
  --set "#CVPR 2026" \
  --dry-run
```

Write only after confirmation:

```bash
python3 <skill-dir>/scripts/zotero_tag_items.py \
  --item-key UKRJFRVC \
  --set "#会议论文" \
  --set "#CVPR 2026" \
  --yes
```

For normal reading packets, use `--set` so no legacy tags remain. For explicitly requested ad hoc edits, use `--replace "old tag=new tag"` or `--remove "<tag>"`. Avoid library-wide cleanup unless the affected item keys have been shown.

Sync the one-sentence summary to Zotero Style 简记 (`remark:` in `Extra`):

```bash
python3 <skill-dir>/scripts/zotero_sync_note.py \
  --paper-folder "<paper-folder>" \
  --sync-tags \
  --yes
```

Mirror the reading packet to Feishu/Lark after confirming the target:

```bash
python3 <skill-dir>/scripts/feishu_sync.py \
  --paper-folder "<paper-folder>" \
  --yes
```

Run a non-mutating readiness check:

```bash
python3 <skill-dir>/scripts/diagnose.py
```

## Output Shape

Use `references/reading-report-prompt.md` for the exact subagent reading prompt, `references/reading-output-template.md` for the local `note.md` shape, `retrieval.md` for per-paper quick search cards, and root `INDEX.md` for the tree directory. `note.md` is the reading report with exactly one one-sentence summary supplied by the subagent; `retrieval.md` is a concise search card; `metadata.json` is the only machine-readable metadata store. For paper batches, keep final chat output compact and point to created files instead of pasting every summary.

## Safety Rules

- Do not invent results, citations, datasets, or ablation outcomes.
- Keep metadata provenance clear: local PDF, Zotero, official web source, or user-provided text.
- Never expose API keys or secrets found in Zotero preferences or exported files.
- Do not mutate Zotero without explicit write confirmation for the concrete items and changes.
- If a web source and Zotero/local metadata conflict, report the conflict and keep both values in metadata until resolved.
