---
name: academic-citation
description: "Search, verify, and map citations for CS/AI/ML papers. Produces VERIFIED/UNVERIFIED reference lists with Citation-to-Claim maps and Exemplar Sets. Use when: finding references for a paper section, verifying citation accuracy, building exemplar sets for introduction/related work learning, checking if existing citations are real and accurate, supplementing local literature library. Triggers on: 找引用, 文献检索, citation pass, find references, reference check, 补文献, citation verification, Exemplar Set, search papers, verify citation, 核验文献, 查引用, literature search, reference verification, citation verification with reading, 引用确认, 全文阅读验证."
---

# Academic Citation

将此 skill 视为"文献取证代理"，而不是搜索结果搬运器。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines non-negotiable rules, source/inference boundary, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables per mode.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
4. If the user wants to use a local literature library, first distinguish:
   - `local_ref_md_dir`: an existing Markdown library containing `_index_ref.json`.
   - `local_ref_pdf_dir`: a PDF directory, or any local library directory that lacks `_index_ref.json`.
5. For `local_ref_pdf_dir`, stop before citation search. Tell the user to register a MinerU API token, set `MINERU_API_TOKEN`, run `scripts/convert-pdfs-to-md.py`, and return only after they confirm PDF→MD completion. Do not proceed to local reading until the generated MD directory has `_index_ref.json`.
6. Detect the workflow using the manifest's `workflow` axis. Literature reading output must separate source quotes from agent inference; only `source: 原文` or `source: 图片` content may be used as citation evidence.
7. Echo the selected mode to the user before executing.
8. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `full-citation-pass` | Complete coverage for a full paper or core section |
| `targeted-citation-search` | Specific claim, section, or topic |
| `exemplar-set-only` | Build Exemplar Set only, not full citation list |
| `citation-verification` | Verify metadata of existing candidate list |
| `local-citation-pass` | Local MD library first, then web supplement |
| `citation-verification-with-reading` | Full-text reading after paper draft completion |

## Agent Dispatch

| Agent | Purpose |
|---|---|
| `agents/citation_agent.md` | Literature search strategy (4-class query templates, output schema) |
| `agents/literature-reader-agent.md` | Literature reading & extraction (MD full-text → LiteratureReadingReport) |

Dispatched by `academic-paper-writer` orchestrator at Step 3. Subagents search and verify only; they must not modify project files or write paper prose independently. `literature-reader-agent` is dispatched in parallel by `citation_agent` or the orchestrator at Step 3a/3b.

## Independent Use

| Input | Mode | Priority | Behavior |
|---|---|---|---|
| Section + keywords | full-citation-pass | 1 (explicit) | Full 6-step workflow |
| Citation list / seed papers | citation-verification | 1 (explicit) | Metadata only, no extra search |
| `local_ref_md_dir` provided and `_index_ref.json` exists | local-citation-pass | 2 (path trigger) | Local MD + batch parallel reader agent dispatch |
| Local PDF library path provided, or local path lacks `_index_ref.json` | pdf2md-preflight | 1 (blocking preflight) | Instruct MinerU setup and script command; wait for user confirmation |
| Section only | targeted-citation-search | 3 (single feature) | Auto-keyword, 4-class query |
| Explicit Exemplar Set request | exemplar-set-only | 1 (explicit) | Exemplar Set only |

**Multi-condition**: lower priority number wins.

| Scenario | Recommended |
|---|---|
| Just searching/verifying citations | This skill (standalone) |
| Integrating into paper drafting | academic-paper-writer orchestrator |
| Existing draft needs citation review | This skill → academic-reviser |
