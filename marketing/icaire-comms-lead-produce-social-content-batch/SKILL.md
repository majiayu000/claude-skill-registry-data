---
name: icaire-comms-lead-produce-social-content-batch
description: Draft and package a source-grounded ICAIRE social-content batch in the standard weekly folder and ZIP format. Use when a social-content plan is ready to turn into reviewable posts, visuals, XLSX, and PDF files.
---

Draft the next ICAIRE social-content batch and package it as a standardized weekly folder and ZIP for review.

## Contract Checklist

- Start from a completed `icaire-comms-lead-plan-social-content` handoff or stop and request one.
- Use `icaire-comms-lead-draft-social-posts` for the copy and approval notes for each selected idea.
- Use the available ICAIRE visual workflow for companion assets, keeping visuals shorter than the detailed captions.
- Store the batch under `~/projects/ICAIRE/social posts/<week>/` unless the user specifies another ICAIRE project root.
- Produce one XLSX row per post, a boxed PDF review, README, visual assets, and a ZIP containing the batch folder.
- Keep the output as draft or review material. Do not publish, schedule, send, or mark a post approved.

## Workflow

1. Validate the planning handoff.
   - Confirm every selected idea has a source slug, factual basis, audience, channel, visual direction, and approval owner.
   - Read the canonical source pages before drafting and mark any changed or unresolved claim.
   - If the handoff is missing or source evidence is stale, stop with the exact missing inputs.
   - Anti-patterns: drafting from a topic title alone, carrying forward stale claims, treating a previous PDF as approval.

2. Draft the post copy.
   - Run `icaire-comms-lead-draft-social-posts` for each selected idea and preserve channel and audience distinctions.
   - Keep the detailed social copy as the caption. Do not put a numeric label in the post copy.
   - Mark unconfirmed links, dates, handles, partner tags, guest details, and approvals inline in the review material.
   - Anti-patterns: inventing a CTA or public URL, copying one generic post across channels, using unsupported superlatives, hiding approval needs.

3. Produce the visual companion.
   - Create a concise landscape visual for each non-podcast post using ICAIRE branding and the approved brand accent `#4A9549` unless a current campaign system overrides it.
   - Treat the visual as a visual interpretation of the caption, not a duplicate of the full post text. Avoid filler subtext such as “the conversation continues.”
   - For podcast posts, use a confirmed real guest photo or record `PHOTO REQUIRED`; do not generate substitute portraits or imply episode details that are not confirmed.
   - Inspect every asset for clipping, overflow, contrast, logo treatment, unsupported text, and landscape dimensions.
   - Anti-patterns: pasting the full caption into the image, portrait outputs when landscape is required, invented partner marks, unreviewed AI text, synthetic podcast guests.

4. Build the standardized weekly folder.
   - Use `social posts/<week>/`, with an ISO week such as `2026-W34`, and keep stable filenames for assets that are referenced by the workbook.
   - Create `icaire-social-posts-<week>.xlsx` with one row per post and columns for post name, pillar, audience, channel, copy, CTA, hashtags, source, approval owner, visual asset, visual status, and publication status.
   - Create `icaire-public-facing-achievements-social-posts-review.pdf` with the post name as a heading outside each box, the post text in its own box, and the proposed visual directly below it. Do not put “Review note” inside the post box.
   - Include `README.md` with the source basis, date, review status, asset map, unresolved confirmations, and the exact ZIP path.
   - Keep the XLSX visual-asset paths, PDF visuals, and filesystem names aligned.
   - Anti-patterns: separate unsynchronized copies, missing source columns, headings inside post boxes, missing visual references, treating placeholders as final assets.

5. Package and verify the ZIP.
   - Run `scripts/package_social_content_batch.py` from this workbench to create the ZIP beside the weekly folder.
   - Confirm the ZIP contains the XLSX, PDF, README, and every referenced visual, with no `__MACOSX`, hidden files, or unrelated output.
   - Reopen or render the PDF and inspect representative pages, then read the XLSX back and confirm one row per post and valid visual paths.
   - Anti-patterns: zipping a parent directory with unrelated files, skipping PDF inspection, claiming a visual is present from a filename only, leaving stale ZIP contents.

6. Hand off for review.
   - Report the folder, PDF, ZIP, post count, visual count, source coverage, unresolved facts, and pillar-leader review owners.
   - State that the batch is ready for review only, not publication.
   - Anti-patterns: sending the ZIP, scheduling posts, changing public campaign state, or marking pillar approval complete.

## Anti-Patterns

- Do not produce a batch without source-grounded planning inputs.
- Do not publish, schedule, send, or represent draft copy as approved.
- Do not place detailed caption copy into the companion visual.
- Do not fabricate dates, links, handles, guest details, partner approval, or images.
- Do not leave the PDF, XLSX, visual paths, and ZIP out of sync.

## Output

Return:

- `Batch Folder`: absolute weekly folder path.
- `Files`: XLSX, PDF, README, visual assets, and ZIP paths.
- `Batch Summary`: post count, channels, pillars, and source coverage.
- `Visual QA`: dimensions, clipping/overflow, branding, caption-versus-visual check, and photo placeholders.
- `Packaging Verification`: ZIP contents and deterministic packaging command result.
- `Review Handoff`: pillar owners, unresolved confirmations, and explicit draft-only status.
