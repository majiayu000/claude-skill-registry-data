---
name: notebooklm-ppt-producer
description: Experimental skill for planning, writing, or packaging PowerPoint/slide-deck production workflows that rely on NotebookLM, Gamma, or another slide generator from source materials. Use when turning long reports, course materials, lecture notes, industry research, policy materials, paper notes, or mixed documents into batched slide prompts, upload packages, page-level outlines, generation batches, visual style instructions, and post-generation merge/review checklists.
---

# NotebookLM PPT Producer

Use this skill to turn source materials into a controlled slide-production package for NotebookLM-style tools. The goal is not only to write prompts, but to keep the deck structure, batch boundaries, source mapping, visual style, and QA loop explicit.

Status: experimental. For the first real use on a new deck type, produce a plan or prompt package first and ask for confirmation before creating many files or rewriting an existing deck workflow.

## Core Workflow

1. Clarify the deck goal:
   - audience, occasion, duration, language, slide count, output tool, and whether the user wants prompts only or a finished deck workflow.
   - if slide count is large, plan batches before writing prompts.

2. Inventory source materials:
   - list each source file, its role, and the sections it supports.
   - flag missing sources, weak evidence, duplicate materials, and private/client-specific content that should be removed before upload.

3. Build the story spine:
   - define the main thesis, section order, and slide-level claims.
   - avoid letting NotebookLM decide the whole structure from raw files.

4. Split into generation batches:
   - use stable batches such as 8-12 slides for dense academic decks, 10-15 slides for lecture decks, and 5-8 slides for design-sensitive executive decks.
   - each batch needs scope, source references, slide numbers, output format, and style rules.
   - read `references/batching-patterns.md` when planning more than one batch.

5. Write prompts:
   - make every prompt include deck context, batch scope, slide count, language, page-level output contract, citation/source constraints, and visual style.
   - read `references/prompt-template.md` before generating NotebookLM/Gamma prompts.

6. Add merge and QA instructions:
   - specify naming, versioning, slide-number continuity, repeated layout cleanup, and final deck review.
   - read `references/slide-package-checklist.md` before delivering a production package.

## Output Modes

- `prompt-package`: create upload instructions, source index, batch plan, and copy-ready generation prompts.
- `page-outline`: create a slide-by-slide outline without tool-specific prompts.
- `deck-production-plan`: create the full workflow from source preparation to final merge and QA.
- `revision-plan`: diagnose an existing generated PPT and write instructions to regenerate or repair specific batches.

## Writing Rules

- Use Chinese by default when the user writes in Chinese. Keep product names, method names, company names, benchmarks, and short technical terms in English when clearer.
- Never invent facts, metrics, or citations that are not in the source materials. Mark uncertain items as `[需核对]`.
- Keep source mapping visible: every major section should say which source file or note supports it.
- For teaching decks, include teaching rhythm: concept -> example -> exercise/demo -> recap.
- For industry/report decks, include business logic: background -> problem -> evidence -> framework -> cases -> implications.
- For academic decks, include claim/evidence boundaries and avoid marketing language.

## Batch Prompt Contract

Each generation batch should include:

```text
Deck context:
- Topic:
- Audience:
- Total deck target:
- Current batch:
- Source materials to use:
- Do not use:

Slide output:
- Slide numbers:
- Slide titles:
- For each slide: claim, 3-5 bullets, suggested visual, speaker note if needed.

Style:
- Language:
- Layout style:
- Typography and color:
- Forbidden styles:

Quality rules:
- Do not fabricate facts.
- Keep source-grounded claims.
- Mark uncertain claims as [需核对].
- Avoid duplicated slides across batches.
```

## Deliverable Structure

When creating files, prefer this structure:

```text
notebooklm_ppt_package/
  00_upload_instructions.md
  01_source_index.md
  02_story_spine.md
  03_batch_plan.md
  prompts/
    batch_01.md
    batch_02.md
  qa/
    merge_checklist.md
    revision_notes.md
```

If the user only asks for text in chat, return the same sections without creating files.
