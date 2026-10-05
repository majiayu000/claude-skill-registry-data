---
name: medium-publisher
description: Draft, format, and safely publish Medium stories through an authenticated browser. Use for Medium article preparation, editor formatting, draft creation, or publication; do not use for generic blog writing with no Medium delivery.
---

# Medium Publisher

Use this skill to turn an approved article into a well-formatted Medium draft, or to publish an already reviewed draft. Preserve the user's publication authority: drafting, publishing, scheduling, submitting to a publication, and sharing are distinct actions.

## Authority and browser boundary

- If the user specifies the in-app browser, Chrome, or Edge, use that exact browser through its corresponding browser-control skill. Do not switch browser families just because one is easier to access.
- Never inspect cookies, local storage, saved passwords, or session stores.
- Treat a Medium draft as a third-party cloud write. Obtain the confirmation required by the active browser-control policy immediately before creating or materially editing a draft, even when the user previously approved the general work.
- Never click a final `Publish`, `Schedule for later`, `Submit`, `Share`, or equivalent action without an immediate, action-specific user confirmation.
- Do not upload local images, private files, customer screenshots, or proprietary logs unless the user explicitly authorizes the exact asset. Do not put secrets, personal data, internal hostnames, paths, account identifiers, or private source code in a draft.

## Prepare before opening the editor

1. Identify the requested mode: local draft only, Medium cloud draft, final publication, scheduling, or submission to a publication.
2. Confirm the audience, language, title, byline expectations, and whether sensitive details must be generalized.
3. Give the user a compact preflight summary for any external write: proposed title, subtitle, topics, publication target if any, and whether images or embeds will be used.
4. Prefer a complete local Markdown draft before browser entry. Keep the source of truth local until the user authorizes a Medium draft.
5. Run a sensitive-content pass. Generalize organization and product names when needed; remove credentials, IPs, filesystem paths, internal URLs, customer data, and raw proprietary code.

## Format the Medium draft

Read [the verified editor capabilities](references/editor-capabilities.md) and [the source-backed layout guidance](references/layout-recommendations.md) before operating the editor.

- Use a concise title and subtitle. In the currently verified UI, the publish panel limits preview title to 100 characters and subtitle to 140 characters.
- Populate Medium's native leading title block as a dedicated first action before inserting a rich body. A whole rich block pasted into a blank editor can leave the native title empty and create an ordinary H3 that only looks like a title. After saving, reload and require the page title and native title block to identify the intended story, with no duplicate title in the body.
- Keep hierarchy shallow. Use the large T on the first line for the title; elsewhere it is a primary section header. Use the small T for a subtitle below the title, a kicker above it, or a secondary header. Do not use bold body text as a substitute for a header.
- Use short paragraphs, meaningful headings, lists for sequences, quotations for central claims, and code blocks only for public, minimal examples.
- Use links for sources rather than pasting long URLs into prose. Check each destination before inserting it.
- Treat images as part of the argument, not decoration. Use a cover image only when it adds context; a relevant original visual is preferable, and no cover is better than a generic or misleading one. Place explanatory diagrams, charts, or annotated screenshots immediately after the claim they explain, with a caption and alt text.
- For local image uploads, use the verified two-stage active-empty-paragraph flow in [the editor capabilities reference](references/editor-capabilities.md). First wait until the left-side `+` is geometrically visible and active; after clicking it, wait until the expanded menu is scaled open and the local-image button has nonzero geometry. Only then register the file-chooser listener and click the image button. DOM presence or an automation API's generic `visible` result is not sufficient.
- Use an image at least 1192px wide when placement choice matters; otherwise the editor may hide some placements. After inserting it, inspect its live contextual controls and report what is actually available.
- Verified image controls have appeared as inset/normal, outset/wide, and fill-width icons, but may have no accessible labels. Do not infer a layout from icon order or an internal value; keep the current placement unless the live control can be identified reliably.
- Use a multi-image grid only when readers benefit from comparing several images. Medium creates a grid from a multi-file upload in filename order, so choose filenames deliberately and verify the final order before publishing.
- Prefer simple, accessible visuals: readable labels, high contrast, no tiny text, and no sensitive information.

## Choose the write order

- Text-only stories may use one atomic, formatted whole-body insertion after a sensitive-content pass.
- For illustrated stories, prefer the evidence-derived section-hybrid workflow: insert one complete formatted text section, immediately add its image at the verified story tail, then establish and verify a fresh tail paragraph before the next section. The 2026-08-24 baseline completed this workflow with two images and survived reload; treat the live editor as authoritative if its behavior differs.
- Never cross an existing image to backfill earlier text. Experiments showed that visible focus does not reliably move Medium's contenteditable caret, so text can land in the title or a caption.
- Prefer native editor controls or a rich formatted section insertion for headings, lists, and code. Do not send an entire `# heading`, repeated `* item`, or fenced-code string as one automated write and assume Medium will convert it.
- Explicit-marker replacement has not been verified and must not be presented as a tested workflow.

## Draft workflow

1. Create or open the intended story only after the required confirmation.
2. Choose text-only atomic insertion or the illustrated section-hybrid workflow above. Use the actual editor controls or a formatted section block instead of relying on whole-string Markdown shortcut conversion.
3. Add only authorized visuals or embeds. Insert local images from an active empty paragraph through the verified `+` menu flow, then set alt text and a caption. For video or embed links, verify their target and do not submit a link whose public visibility the user has not approved.
4. After every media insertion, alt-text edit, or layout action, verify the active insertion point. Attempt the true tail with `ControlOrMeta+End` on the article textbox, re-read the DOM, then enter one unique printable sentinel character absent from the article (for example `⟡`). Require it to be the sole content of the intended tail paragraph and outside the title, figure, and caption. Remove it with exactly one Backspace and require zero occurrences before continuing. Stop after two failed recoveries.
5. Wait for a saved-draft state and record the draft URL, but also inspect error banners. If `Story could not be saved` appears, wait and re-read the live state before retrying because the editor may settle independently. Do not treat `DraftSaved` as sufficient while the error remains visible.
6. Reload the saved draft before final handoff. Read it back visually and structurally: native title identity, absence of a duplicate body title, heading hierarchy, paragraph breaks, list and code fidelity, image order, links, captions, alt text, and mobile-friendly density. Read alt text and captions back from the figure; do not trust the Save action alone.
7. Report exactly what was created, any contradictory save state, and which visual or editor capabilities were observed versus unverified.

## Distribution-aware editorial check

- Titles, subtitles, and cover images must accurately represent the story; avoid sensational, vague, or clickbait framing.
- When the user wants broader Medium distribution, check that the story is original, well sourced where needed, and that visuals add value with credit and alt text.
- Do not promise Boost or General Distribution. Medium's current public guidelines say content that appears AI-generated is not eligible for those distribution categories; disclose this limitation when the user asks about reach or eligibility, and never misrepresent authorship.

## Publication workflow

1. Before opening final publication settings, present the candidate preview title, subtitle, up to five topics, and publication destination. Ask for corrections.
2. In the current UI, the publication panel may expose preview title, subtitle, estimated read time, topics (maximum five), a publication-submission path, `Publish`, and `Schedule for later`.
3. Do not claim that SEO, canonical URL, or a standalone preview field exists unless it is visible in the current editor session.
4. Immediately before the irreversible click, ask for a fresh confirmation that states the exact action: publish now, schedule for a stated time, or submit to a named publication.
5. After the confirmed action, verify the visible outcome and report the resulting URL, publication state, and any warnings. If the confirmation is absent, stop at the ready-to-publish draft.

## Failure handling

- If editor features, Unsplash search, media insertion, or formatting controls fail, record the observed failure and continue with a text-only draft when possible. Do not invent a workaround or claim an unverified layout.
- Before classifying local-image insertion as a file-chooser failure, verify both menu-readiness stages. If either stage does not become interactive, re-establish the tail paragraph and menu once; classify that as an editor menu-readiness failure, not a chooser or network failure. Stop media insertion or insertion-point recovery after two failed attempts rather than continuing into an uncertain state.
- If authentication is unavailable in the user-selected browser, ask the user to sign in or reactivate that exact browser; do not bypass it with another account or browser.
- If any draft contains sensitive content, stop before external save or publication and ask for a sanitized replacement.
