---
name: delivery-document-package
description: Use when the 文档/交付 role maintains client-facing project delivery document packages, especially Word/DOCX deliverables such as delivery lists, demo scripts, acceptance forms, change confirmations, quote notes, contract-adjacent materials, README/docs indexes, and internal handoff notes.
---

# Delivery Document Package

## Purpose

Maintain project delivery document packages with a clean split between external deliverables and internal working notes. External artifacts must read like formal client materials, not agent scratchpads.

Use this skill with the Documents skill when creating or editing `.docx` files.

## Package Workflow

1. Inventory the current document package and split files into external deliverables and internal working notes.
2. Confirm the project stage: presales, quote, contract/signing, development, acceptance, delivery, maintenance, or upgrade planning.
3. Align each document with the current architecture scope, implementation facts, QA results, and explicit exclusions.
4. Create or update only the documents needed for the current stage; keep commercial, legal, tax, and liability terms unchanged unless the user explicitly asks.
5. Verify DOCX text, names, links, boundaries, and temporary-file cleanup before calling the package ready.

## Format Rules

- External/customer-facing deliverables should be Word, Excel, PowerPoint, or another formal artifact format requested by the user.
- Internal indexes, implementation notes, and role handoff notes may be Markdown.
- README document indexes may link both internal Markdown and external Office files, but should label the split clearly.
- Do not leave temporary source drafts, render folders, or builder scripts in the final document package unless the user asked to keep them.

## External Wording Rules

External documents must use neutral, formal names and section labels.

Prefer:

- `演示脚本`
- `交付清单`
- `验收确认单`
- `需求变更确认单`
- `版本说明`
- `范围说明`
- `签署提示`

Avoid in external Word documents:

- `老板演示脚本`
- `让老板看懂...`
- `文档性质`
- `适用阶段`
- `版本口径`
- `对外 Word 文件`
- `内部提示`
- `推荐话术`
- agent/process narration such as "我会..." or "本次新增"

If stakeholder wording is needed, use neutral terms such as `甲方`, `接收方`, `客户`, `门店经营方`, or `使用方`.

## Boundary Statements

For trial/demo systems, every external document should plainly state the current version boundary in business-safe wording:

- current version is a local/static/demo/trial version when that is true;
- it is not a formal commercial SaaS unless the project actually is one;
- local browser data, mock data, or demo estimates are not formal business settlement, performance, finance, or long-term operating data;
- unimplemented capabilities must not be described as delivered.

Do not promise implemented support for platform accounts, messaging, payment, third-party POS/vendor integrations such as Keruyun, SMS, printers, large screens, real backend services, databases, cloud deployment, account permissions, realtime sync, audit logs, or commercial SLA unless verified in the current project.

For personal-subject contracts or contract-adjacent materials, include a concise lawyer/tax review reminder before formal signing, payment, invoices, taxes, liability limits, source-code ownership, or dispute terms are finalized. Do not rewrite legal/payment key terms unless the user explicitly requests it.

## DOCX Hygiene

- Avoid footers in generated Chinese Word deliverables unless they are necessary and verified. Footers are a common place for encoding or font fallback problems.
- If a footer/header is required, read the `.docx` back and verify it contains no `????`, missing glyphs, or mojibake.
- Do not include internal metadata at the top of external Word files. Put useful content first.
- Keep tables readable, with short labels, sufficient padding, and no fixed row heights that can clip text.
- Use formal section titles rather than callout-heavy agent notes.

## Verification Checklist

Before calling the package done:

1. Read each new/edited DOCX back with `python-docx` or an equivalent structured reader.
2. Search the extracted text and headers/footers for forbidden residue: `老板演示脚本`, `文档性质`, `适用阶段`, `版本口径`, `对外 Word 文件`, `内部提示`, `推荐话术`, `????`.
3. Confirm required boundary text appears where relevant: local/static/demo version, not formal commercial SaaS, unimplemented third-party/backend capabilities excluded, lawyer/tax review for personal-subject contract materials.
4. Verify external file names match formal titles and README/internal indexes point to the final names.
5. Confirm temporary drafts and render folders are removed.
6. Render DOCX pages with the Documents skill if LibreOffice/`soffice` is available. If it is unavailable, state that visual render QA was skipped and report the structural checks used instead.
7. Confirm business-code files and legal/payment clauses outside the allowed scope were not modified.

## README And Internal Indexes

When updating indexes:

- Separate `内部维护文档` from `对外交付文档`.
- Use external file names in links, not internal nicknames.
- Keep the index concise; detailed caveats belong in the relevant document or internal document-package checklist.
