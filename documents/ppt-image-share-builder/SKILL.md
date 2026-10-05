---
name: ppt-image-share-builder
description: Build image2-first classroom PPT page images from a topic, source files, reference PPT style, and iterative user feedback. Use when Codex needs to create image2-ready per-page prompts, generate polished PPT page images, QA a contact sheet, insert the final images into a PPTX wrapper, and write a timed presentation script for a course report or lecture-style PPT.
---

# PPT Image Share Builder

Use this skill for image2-first PPT image work:

```text
source files + reference PPT style
  -> sourced page outline
  -> image2-ready per-page prompts
  -> generated 16:9 PPT page images
  -> contact-sheet QA
  -> targeted fixes only if QA fails or user asks
  -> full-bleed PPTX wrapper
  -> timed speaking script
```

Keep the workflow source-backed, style-aware, and human-reviewed. Helper scripts are for post-generation steps; they do not replace image2.

## Core Rules

- Treat generated PPT page images as the visual source of truth. The PPTX is only a delivery wrapper.
- Optimize for a non-expert user. Do not require the user to know prompt engineering terms; translate vague feedback into concrete content, style, and cleanup actions.
- Before writing prompts or generating images, run bounded grill-me style intake. If a real grill-me skill/tool is available, use it; otherwise use `references/intake-grillme.md`.
- Do not begin deck planning or image generation until essential decision branches are resolved or explicit assumptions are recorded.
- Extract and verify source facts before writing prompts. Use official or primary sources for recent rules, cases, data, or dates.
- Match the user's reference PPT style: layout rhythm, title system, color palette, page markers, diagram grammar, and information density.
- Default to one-pass delivery: generate the full useful deck in one run unless the user explicitly asks for staged confirmation or the request is too ambiguous to proceed safely.
- Use internal gates instead of user-visible rounds: content depth gate, style lock gate, and cleanup QA gate.
- Never let the first delivered version be merely decorative. Each non-cover/non-closing page needs a claim, 2-4 substantive points, and a meaningful visual structure.
- Create a style lock before generating the full image set; every page prompt must repeat that style lock.
- In final QA, remove meaningless elements: stray X/check marks, random labels, fake legends, unrelated icons, decorative charts with no data role, duplicate badges, and any unrequested Q&A text.
- Keep generated Chinese text short. Recommend adding exact long text manually in PPT if precision matters.
- For dense Chinese or source-critical text, use image2 for the visual page or background and compose exact text locally, then treat the exported full-page image as the final slide.
- Do not generate government seals, company logos, QR codes, or watermarks unless the user supplied verified assets and explicitly requests them.
- On Windows PowerShell 5.x, avoid Bash-style command chaining such as `&&`; run multi-step commands separately.
- For Chinese paths, do not put non-ASCII path literals inside here-strings piped to native programs. Pass paths as arguments or use `-LiteralPath`.

## Workflow

1. **Run grill-me style intake**
   - Inspect provided files, paths, and messages first; do not ask questions that can be answered from available material.
   - Track essential branches as `[OPEN]` or `[RESOLVED]`: topic/title, audience, duration or page count, sources, reference style, required content, forbidden content, and requested outputs.
   - Ask 1-3 missing questions per batch, with recommended defaults when possible.
   - Treat optional details as defaults when they are missing; state assumptions instead of adding avoidable back-and-forth.
   - Read `references/intake-grillme.md` before starting a new deck or major revision.

2. **Extract sources**
   - For Chinese `.doc`, `.docx`, `.txt`, `.csv`, or government-style documents, use a reliable UTF-8 extraction path.
   - If the current environment provides a document extraction helper, prefer it over ad hoc encoding guesses.

3. **Plan the deck**
   - Build a thesis and page sequence before prompting image2.
   - For 8-12 minute classroom reports, usually use 10-14 page images.
   - Read `references/workflow-checklist.md` when planning a full image set.

4. **Run the one-pass delivery loop**
   - Build the full outline, style lock, image prompts, page images, contact sheet, PPTX, and talk script in one run by default.
   - Use three internal gates before delivery: content-rich gate, style-lock gate, and meaningless-element cleanup gate.
   - Regenerate only failed pages when the internal QA gate catches an issue.
   - Read `references/iteration-playbook.md` before generating or revising a multi-page image set.

5. **Write image2 prompts**
   - Create one unified visual prompt, then per-page prompts.
   - Include a style lock block before generating the full image set.
   - Each page prompt should include title, required text, visual structure, style constraints, and forbidden text.
   - Read `references/prompt-patterns.md` when drafting or revising prompts.

6. **Generate and save images**
   - Use image2 or the available raster image-generation tool.
   - Save final page images with stable names such as `slide-01-cover.png`, `slide-02-agenda.png`, and so on.
   - Regenerate only affected page images when user feedback is local.

7. **QA with a contact sheet**
   - Build a contact sheet after each major batch:

     ```powershell
     python scripts\make_contact_sheet.py --input-dir outputs\<topic-slug>-images -o outputs\<topic-slug>-images\contact-sheet.jpg
     ```

   - Read `references/qa-checklist.md` before final delivery.

8. **Insert images into PPTX**
   - After the final image2 pages pass QA, insert them as full-bleed PPT pages:

     ```powershell
     python scripts\images_to_pptx.py --input-dir outputs\<topic-slug>-images -o <topic>.pptx
     ```

   - Do not rebuild the visual design as editable PPT shapes unless the user explicitly asks for editable slides.

9. **Write the talk script**
   - Write the script after slide content stabilizes.
   - Add spoken bridges, background logic, and selected examples that are not fully written on the slides.
   - Match the requested duration and final closing wording.

## Expected Outputs

- `<topic>_image2逐页大纲.md`
- `outputs/<topic-slug>-images/slide-XX-*.png`
- `outputs/<topic-slug>-images/contact-sheet-*.jpg`
- `<topic>.pptx`
- `<topic>_<duration>汇报稿.md`
