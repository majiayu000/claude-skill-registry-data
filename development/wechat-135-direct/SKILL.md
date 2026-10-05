---
name: wechat-135-direct
description: Directly build, revise, and save WeChat public-account drafts in 135 Editor using a controlled browser session and durable platform-hosted images. Use when the user asks for 135 Editor / 公众号排版, direct editing of 135 drafts, fixing broken images, inserting local work photos into 135, or saving a styled article without relying on localhost/file/base64 image URLs.
---

# Wechat 135 Direct

## Overview

Use this skill to create 135 Editor drafts that remain valid after local tools are closed. Treat local HTML as a preview or staging artifact only. The final article should live inside 135 Editor, and final images should use 135/WeChat platform-hosted URLs.

## Configuration

Use placeholders for local configuration. Do not hard-code personal paths, account details, cookies, tokens, article IDs, private material locations, browser profile paths, or local debugging ports in this public skill.

- Start script: `<PATH_TO_135_CHROME_START_SCRIPT>`
- Chrome profile: `<YOUR_CHROME_PROFILE>`
- DevTools endpoint: `<DEVTOOLS_ENDPOINT>`
- Editor URL: `https://www.135editor.com/beautify_editor.html`

Use a dedicated browser profile for 135 work if possible. It can preserve login state locally, but the profile itself is private user data and must never be committed or shared.

## Workspace Placement

Keep staging and temporary work outside sync drives or shared folders unless the user explicitly asks for that destination. Local previews, extracted images, screenshots, upload intermediates, QA reports, and automation scratch files should live in a disposable project workspace. Final deliverables can go to the user-requested location.

When source materials are already in a sync folder, read them in place but write temporary derivatives elsewhere. Do not move, reorganize, or delete the user's original photos, documents, or formal outputs as part of a layout job.

## Browser Control Priority

For production 135 article work, prefer the dedicated browser profile and DevTools endpoint configured for this workflow. This keeps draft editing, image upload, save verification, and visual QA in the same authenticated editor context.

Recommended priority:

1. Use the configured 135 browser entry and DevTools endpoint for creating, revising, image-uploading, saving, and verifying drafts.
2. Use local preview pages only for layout design, side-by-side visual checks, and non-authenticated review.
3. Use a generic browser automation plugin only when the user explicitly asks for it or when the dedicated endpoint is unavailable and the fallback is safe.

Do not delete or reset the dedicated browser profile. It may contain login state. If the endpoint is unavailable, ask the user to start the configured browser entry or run the agreed startup command.

## Do Not Use As Final Delivery

Do not use these as final image sources:

- `localhost` URLs
- `127.0.0.1` URLs
- `file://` URLs
- `data:image/...;base64` image URLs
- static local preview HTML as the final deliverable

Local HTML can be used to design, inspect, and stage a fragment, but final images must be inserted through 135 itself so 135/WeChat generates durable hosted image URLs.

## Direct 135 Workflow

1. Start or reuse the configured dedicated browser profile for 135 editing.
2. Connect to the configured DevTools endpoint and locate the 135 editor page.
3. Clear ordinary blocking UI such as ads, activity popups, guide layers, and non-essential overlays when they clearly block editing and are not login, permission, save, sync, publish, billing, or security dialogs.
4. Open or create the target 135 article through the native 135 article workflow.
5. Verify the target before editing by checking title, visible content markers, and article ID when available.
6. Write the article HTML directly into the 135 editor iframe. Do not rely on a local preview page as final state.
7. Insert each image through 135's own paste, upload, or material-library path.
8. Save with the editor's quick-save action.
9. Verify the saved editor state and the save response.
10. Close saved articles that are no longer being edited so the editor does not hit its simultaneous-open article limit.

Do not click synchronization, publishing, or account-binding actions unless the user explicitly asks for them.

## Safe Article Switching Workflow

Before opening another article or starting a new one, decide whether the currently open editor content is a draft created or edited in the current work session, or only stale browser-restored cache from an earlier session. Browser-restored cache is not automatically the authoritative saved draft.

Important distinction:

- If the article was created or intentionally edited in the current work session, save it before switching or closing.
- If 135 is opened for the first time in the current work session and shows a leftover article from an earlier period, treat it as browser-restored cache. Do not quick-save that restored content by default because doing so can overwrite an already-good saved article.
- When only one restored-cache article is open and the editor will not allow closing it, create a new blank article first, then close the stale editor card if the UI allows.

Use this order:

1. Read the current article metadata when available, including ID, title, and a short content marker.
2. Decide whether the current article is a current-session draft or stale restored cache.
3. For a current-session draft, save and confirm a successful save response.
4. For stale restored cache, do not save it; create or switch to a new blank article first if needed.
5. Create new articles through 135's native new-article entry or the editor's own article manager API when appropriate. Do not manually clear the old article body as a substitute for creating a new article.
6. Confirm the new draft is separate from the old one by checking title, body marker, and article ID when available.
7. When opening an old article, verify article ID, title, and body marker immediately after the switch.
8. After the current article is saved and no longer being edited, close its open editor tab/card.
9. Closing an open editor tab/card is not deleting the saved article. Never delete a draft unless the user explicitly asks for deletion.

## 135 DOM Notes

- The editable iframe name can vary; inspect available frames and identify the right one by visible title/body content, not by frame name alone.
- The quick-save button and article manager APIs may change. Prefer semantic checks and visible UI verification over brittle selectors.
- A successful save request commonly includes a 135 save endpoint and a success code or success message. Verify the actual response in the current editor version.
- If multiple articles/tabs are open, stop and re-check the title and article identity before writing.

## Image Insertion Workflow

Prefer platform upload or paste over HTML image URLs.

1. Convert local JPG/JPEG files to PNG before clipboard insertion when the browser clipboard API requires `image/png`.
2. Focus a temporary upload area inside the 135 editor iframe.
3. Write the PNG blob to the clipboard and paste it into the focused iframe.
4. Wait for the inserted image to change from temporary placeholders to a 135/WeChat platform-hosted URL.
5. Move or replace the final platform-hosted image into the intended article location.
6. Remove the temporary upload area and any leftover placeholders.

If paste does not upload the image, use the 135 upload control or material library as the fallback. If login, captcha, permission UI, or account checks block automation, ask the user to complete that UI step and then continue.

## Image Card Styling

If a main image shows an awkward white slab below it, inspect for `&nbsp;`, `<br>`, empty text nodes, empty `<p>`, or empty `<span>` after the `<img>`. Delete those nodes.

Use this card pattern for coordinated image styling:

```html
<section style="margin:0 0 18px;padding:6px;background-color:#d7eaf0;border:1px solid #c0dbe2;border-radius:12px;">
  <section style="margin:0;padding:0;background-color:#ffffff;border:1px solid #d4e6eb;border-radius:10px;box-shadow:0 10px 22px rgba(9,38,61,.18);line-height:0;font-size:0;overflow:hidden;">
    <img src="PLATFORM_IMAGE_URL" alt="" style="display:block;width:100%;height:auto;margin:0;padding:0;border:0;border-radius:10px;vertical-align:top;">
  </section>
</section>
```

Keep the outer padding small, usually `6px`. Keep shadow and border subtle. Put `line-height:0;font-size:0;overflow:hidden;` on the tight image wrapper to prevent invisible nodes from creating bottom whitespace.

## Subject-Protected Image Cropping

When cropping, beautifying, or building photo collages, protect the image's main subject first. Preserve people, work actions, key equipment, faces, bodies, hands, tools, and critical scene details. Do not cut off a subject just to force a uniform ratio.

After automatic cropping or collage export, visually review every photo. If a source photo does not fit the intended crop, change the layout instead of hard-cropping the subject. Use whitespace, a different grid, a single-image layout, or `object-fit:contain` when needed.

## Chinese Text Layout

- Use real two full-width spaces `　　` at the start of Chinese body paragraphs.
- Do not use `padding-left:2em` to fake paragraph indentation.
- Avoid `text-align:justify`; use `text-align:left`.
- Apply indentation only to narrative body paragraphs. Do not indent titles, section headings, buttons, image blocks, callout labels, list items, slogans, or signatures.

## Visual Quality Baseline

Do not treat a 135 article as a Word document with images inserted between paragraphs. Build a clear mobile-first public-account layout.

- Default to Chinese for public-account titles, column names, decorative text, labels, badges, and section marks. Use English only for necessary fixed brands, professional abbreviations, or explicit user requests.
- Before producing an article, reference strong public-account examples or editor templates that match the topic. Learn the theme characteristics, layout routines, and visual methods first, then decide the design direction.
- Choose the visual direction according to content type, such as safety education, activity record, profile story, process explanation, youth team feature, or formal notice.
- Redesign the layout around the current article. Keep the stable workflow, but make the body structure, title area, image placement, colors, and module rhythm serve the current theme.
- Use an intentional full-page background or atmosphere layer instead of a plain white document shell.
- Use generated images when they help the article read better, such as covers, atmosphere images, column headers, section openers, diagrams, and abstract visual explanations.
- Keep the boundary clear: never use generated images to fake real on-site photos or make an activity look documented when it was not.
- Give the article a column identity with a framed cover area, short lead card, numbered section headers, tag pills, dividers, quote boxes, keyword boxes, and a closing card.
- Vary section patterns. Avoid repeating the same title block and the same single-image card for every section.
- For multiple related photos, use designed image groups such as side-by-side cards, staggered pairs, before/after comparison modules, process strips, or grid collages.
- Check title-area readability carefully. Title text, names, organization names, and theme words must have enough contrast against the background.
- Preserve image expressiveness by using semi-transparent overlays, gradients, intentional whitespace, strokes, shadows, color blocks, offset cards, or similar treatments instead of covering artwork by default.
- Keep copy compact. Preserve facts, but remove report-like repetition and long image explanations.
- For display-first multi-station or multi-unit articles, curate photos instead of publishing every image. Prefer representative photos that cover different scenes, actions, and angles.
- Remove small image captions unless the user explicitly asks for them. If context is needed, put it in surrounding body text or a designed label/card.
- Keep cover and title-image wording short and exact. For long Chinese text, draw controlled HTML/SVG text rather than relying on generated images to render it.

## Information Component Design

Do not rely only on heading and paragraph styling. Before writing final HTML, scan the material for information that would read better as a designed component.

Use this decision step:

- If the source contains duties, checks, schedules, names, places, task lists, measurements, or status rows, consider a table-style module.
- If the source contains before/after, problem/measure, old/new, risk/consequence, or requirement/action pairs, consider a comparison module.
- If the source contains steps, closed-loop handling, process flow, training flow, review flow, or rectification path, consider a flow module or timeline.
- If the source contains counts, rankings, percentages, time nodes, coverage, inspection frequency, or completion status, consider a data card or chart.
- If the source contains key phrases, rules, reminders, or definitions, consider keyword cards, notice cards, or knowledge cards.

Do not paste raw Markdown tables as-is unless the table is tiny and readable on mobile. Convert tables into mobile-friendly visual components:

- Normal table -> card-style table with a colored header, row spacing, and clear cell hierarchy.
- Wide multi-column table -> stacked grouped cards, one card per row or item.
- Checklist -> tick-card list or two-column compact checklist.
- Rectification list -> before/after comparison cards with clear labels.
- Safety measures -> risk / measure / reminder triads instead of dense columns.
- Schedule -> vertical timeline or segmented date cards.
- Statistics -> number dashboard, progress bars, mini bar chart, or ring chart.

Use real HTML tables only when the table is narrow, important, and stable in WeChat preview. For richer visuals, prefer nested `section` layouts, inline SVG, or static images generated from a chart/table design. Avoid JavaScript-dependent charts inside the final article.

Quality rules:

- Choose components based on the content's structure, not because every article needs every component.
- One strong table or chart component is better than many weak decorations.
- Keep table text short. If a cell needs a long paragraph, it should probably be a card or normal body text.
- Match component color, border, icon, background, and title badge to the article's visual direction.
- Preview on mobile width and check that tables do not overflow, squeeze text, or look like pasted Word/Excel.

## Multi-Group Title Deduplication

For articles that show multiple stations, units, people, teams, or other repeated groups, keep one clear primary title per group.

- If the outer group title already shows the station, unit, person, or group name, do not repeat the same name inside image cards, collage cards, tag areas, or small labels in the same module.
- For display-first multi-group articles, use `outer group title + image group` by default. Do not add a second title inside each image card unless the user explicitly asks.
- Treat semantically repeated labels as duplication too. Labels such as "site scene", "work record", or similar status words are often redundant when the outer title already explains the scene.
- If the user has already pointed out repeated titles, verify both visible HTML text and any exported image pixels/screenshots, because duplicate wording may be baked into images.

## SVG Modules And Effects

SVG can be used for decoration, structure, and light interaction if compatible with 135/WeChat.

- Decorative uses: dividers, shield or warning icons, dashed process lines, corner stickers, small arrows, tag pills, and light geometric accents.
- Structural uses: reusable inline SVG modules for timelines, process maps, cards, layered image/text compositions, before/after comparison frames, and topic-specific opening screens.
- Light interaction or pseudo-interaction ideas: swipe-like display, long-press hint panels, layered text-over-image reveals, process motion, and before/after comparison.
- Prefer pure inline SVG, CSS animation, simple inline structure, and carefully tested SMIL.
- Do not depend on external JavaScript, remote libraries, editor-only runtime behavior, `localhost`, `file://`, or `data:image`.
- Treat compatibility as mandatory QA. After paste/save, verify in 135 and in WeChat preview that the SVG module does not break, disappear, overflow mobile width, lose images/text, or harm reading.
- Do not overuse effects. Pick the SVG pattern that serves the content.

## Safety Rules

- Browser-launch authorization, if agreed by the user, applies only to the configured 135 editing workflow. It does not authorize unrelated browser automation, profile changes, extension repair, or arbitrary browsing sessions.
- Uploading real local photos into 135 is file transmission. If the user has not clearly asked to upload or modify 135, confirm before doing it.
- Do not upload sensitive data or files unless the user explicitly asked for that specific upload.
- It is OK to automatically close ordinary 135 ads, promotions, activity popups, overlay masks, and guide layers that block editing, uploading, or saving. If uncertain, pause and ask the user instead of dismissing it.
- Do not clear or overwrite an uncertain article. First verify the title and article identity.
- Preserve user assets and existing drafts. When unsure, create a draft copy or ask before destructive replacement.
- Keep the dedicated browser profile private. Do not commit profile data, cookies, tokens, or logged-in state.

## Acceptance Checklist

Before reporting completion, verify:

- Staging and temporary artifacts were written to a non-sync/disposable workspace, except for final deliverables or user-explicit paths.
- No final article image `src` contains `localhost`, `127.0.0.1`, or `file://`.
- Main images use 135/WeChat platform-hosted URLs and each loaded image has `naturalWidth > 0`.
- No temporary upload area remains.
- No temporary placeholders remain in final image positions.
- No `text-align:justify` remains in body copy.
- Chinese body paragraphs start with real `　　` indentation.
- Main image cards use the adjusted small-padding card style and have no bottom white slab.
- Source material with checks, schedules, steps, comparisons, data, or lists was considered for table/card/timeline/flow/data modules instead of dense paragraphs.
- Any table or table-like module was checked on mobile width for overflow, cramped cells, and Word/Excel-like appearance.
- Multi-station, multi-unit, multi-person, and multi-group modules were checked for repeated names, inner labels, and duplicate titles.
- Display-first multi-group articles used selected representative images rather than every available image by default.
- Photo crops and collages were visually checked for subject protection.
- QA included visual inspection, not only text search. If labels or names are baked into exported images, inspect screenshots or image pixels for duplicate text, garbled Chinese, English remnants, or stuck-together wording.
- Exported collage/display images were checked at the bottom and edges for ghost remnants, dirty crops, unintended blank areas, or bottom white borders.
- The save action returned a successful response.
- Synchronization or publishing was not clicked unless explicitly requested.
