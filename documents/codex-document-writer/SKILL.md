---
name: codex-document-writer
description: Use for documents, reports, memos, guides, academic papers, or formal text that needs clear structure, reliable tone, formatting, and diagrams.
load_priority: on-demand
---

## TL;DR
Load before writing or revising any document, report, proposal, memo, guide, academic paper, or long-form explanation. The goal is reader clarity: correct context, full meaning, professional structure, reliable tone, compact wording, proper diagrams, and polished formatting — without making the reader infer missing intent.

## Activation

1. Activate when the task involves drafting, rewriting, summarizing, formatting, or improving documents, reports, memos, proposals, guides, handoffs, emails, academic papers, or formal text.
2. Activate on `$doc`, `$report`, `$write`, `$diagram`, `$báo-cáo`, "soạn tài liệu", "viết báo cáo", "làm văn bản chuyên nghiệp", "viết rõ ràng hơn", "vẽ sơ đồ".
3. Auto-load with `codex-reasoning-rigor` when the document is decision-heavy, high-stakes, or evidence-based.
4. Auto-load with `codex-doc-renderer` when the deliverable is `.docx`.

## Hard Rules

- Always identify purpose, audience, context, and expected use before choosing wording.
- Start with the document outcome, not background narration.
- Use complete sentences with explicit actor, action, object, and outcome.
- Keep each paragraph focused on one message; do not make the reader infer the point.
- Be detailed where meaning depends on detail, but remove filler, repeated framing, and synonym stacking.
- Use humble, reliable wording: state what is verified, what is inferred, and what remains uncertain.
- Do not overclaim. Avoid "clearly", "obviously", "guaranteed", "always", and "never" unless evidence supports them.
- For Vietnamese, use natural UTF-8 Vietnamese, correct context labels, and professional but readable wording.
- Every diagram must answer a specific question. No decorative diagrams.
- Every report section must earn its place. No empty sections or placeholder text.

## Document Flow

Before drafting:

1. Determine document type and reader.
2. Pick the matching structure:
   - For reports → `references/report-structures.md`
   - For general documents → `references/document-types.md`
   - For academic/university work → `references/academic-report-patterns.md`
3. Add diagrams where visual explanation is needed → `references/diagram-patterns.md`
4. Apply content writing patterns → `references/content-writing-patterns.md`
5. Apply sentence rules from `references/sentence-quality.md`.
6. Apply reliability rules from `references/tone-reliability.md`.
7. Apply Vietnamese wording rules from `references/vietnamese-style.md` when writing Vietnamese.
8. Apply formatting rules from `references/formatting.md`.

## Diagram Integration Protocol

When the document needs visual explanation:

1. Check `references/diagram-patterns.md` → Diagram Selection Decision Table
2. Choose the simplest diagram type that answers the reader's question
3. Use Mermaid syntax for rendered documents, ASCII for plain text
4. Add a caption/title before every diagram
5. Limit: max 15 nodes per diagram, split if larger
6. Verify render before delivering

### Quick Diagram Dispatch

| Need | Diagram Type | Mermaid Keyword |
|---|---|---|
| System architecture | Flowchart with subgraphs | `flowchart TB` |
| API interaction flow | Sequence diagram | `sequenceDiagram` |
| Database schema | ER diagram | `erDiagram` |
| Status/workflow transitions | State diagram | `stateDiagram-v2` |
| Project timeline | Gantt chart | `gantt` |
| Branch strategy | Git graph | `gitGraph` |
| Feature breakdown | Mind map | `mindmap` |
| Distribution/proportion | Pie chart | `pie` |
| Milestone overview | Timeline | `timeline` |

## Report Type Router

| Signal in User Request | Load Reference |
|---|---|
| "báo cáo tiến độ", "progress report" | `references/report-structures.md` → Progress Report |
| "phân tích", "analysis", "analytical" | `references/report-structures.md` → Analytical Report |
| "đề xuất", "proposal" | `references/report-structures.md` → Proposal |
| "sprint report", "release notes" | `references/report-structures.md` → Sprint Report |
| "incident", "postmortem", "sự cố" | `references/report-structures.md` → Incident Report |
| "đồ án", "assignment", "bài tập lớn", "luận văn" | `references/academic-report-patterns.md` |
| "memo", "update", "thông báo" | `references/document-types.md` → Business Memo |
| "hướng dẫn", "guide", "tutorial" | `references/document-types.md` → User Guide |
| "handoff", "bàn giao" | `references/document-types.md` → Session Handoff |
| "README", "documentation" | `references/content-writing-patterns.md` → README Template |

## Quality Gate (Before Delivery)

Before delivering any document:

- [ ] First section answers the reader's primary question
- [ ] Every claim backed by evidence
- [ ] Tables used for comparisons, not narratives
- [ ] Every diagram has a caption and answers a specific question
- [ ] Metrics shown with target vs actual
- [ ] Clear "Next Steps" or "Required Decision" section
- [ ] Risks listed with severity AND mitigation
- [ ] For Vietnamese: proper section headings and figure/table numbering
- [ ] Scannable: headings + tables alone convey the gist
- [ ] No wall-of-text paragraphs (max 5-6 lines per paragraph)
- [ ] No "empty calories" phrases ("it is important to note that...", "in order to...")

## Reference Files

- `references/document-types.md`: templates for reports, memos, proposals, guides, handoffs, summaries, and executive updates.
- `references/report-structures.md`: 8 report types — progress, analytical, proposal, comparison, sprint, incident, research, and Vietnamese academic.
- `references/diagram-patterns.md`: complete Mermaid diagram reference — flowchart, sequence, ER, state, Gantt, C4, journey, mindmap, pie, gitGraph, timeline + ASCII alternatives + quality rules.
- `references/content-writing-patterns.md`: PREP framework, heading hierarchy, active voice, "So What?" test, Vietnamese content patterns, anti-patterns, and README template.
- `references/academic-report-patterns.md`: Vietnamese university report template — 6 chapters, cover page, TOC, figure/table lists, formatting standards, citation guide, and common academic phrases.
- `references/sentence-quality.md`: sentence patterns that keep meaning complete, compact, and easy to read.
- `references/tone-reliability.md`: humility, evidence wording, uncertainty, and confidence calibration.
- `references/vietnamese-style.md`: Vietnamese document labels, wording patterns, and anti-filler rules.
- `references/formatting.md`: professional headings, tables, bullets, spacing, and scan-friendly layout rules.
