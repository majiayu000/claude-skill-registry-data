---
name: pptxgenjs
description: Create visually designed, editable PowerPoint presentations with researched imagery, original artwork, diagrams, tables, and charts. Use pptx-edit for changes to an existing PPTX.
---

# New PowerPoint presentations

Use preinstalled PptxGenJS 4.0.1. Write CommonJS scripts in the workspace and run `pptxgenjs-run deck.cjs`; `require('pptxgenjs')` resolves through the wrapper. Keep the script and original assets for revisions. Preserve user templates and explicit visual preferences.

## Turn the subject into a visual story

For a short request, infer a sensible audience and scope and proceed. Choose the takeaway first, then decide what each slide contributes. Write titles that make a point. Move supporting detail into speaker notes with `slide.addNotes(...)`; keep the displayed story readable at presentation size.

Choose an art direction from the subject: palette, type hierarchy, photographic treatment, and a repeated visual detail that carries meaning. Use installed fonts that cover the requested language; `fc-list` lists them. A coherent deck can use different compositions. Repeating the same title, subtitle, and three rectangular text cards across the body slides is a weak default, even when it passes overflow checks.

When the brief leaves the style open, consider two genuinely different directions before choosing. Ground the choice in a recognizable detail of the subject, such as local signage, materials, archival imagery, maps, or a supplied brand. A generic "technology" topic does not by itself justify the familiar dark-navy-and-mint theme. Create a deliberate type scale and a few color roles; use changes in background or image scale where they strengthen the narrative. Plan the opening and one substantive body slide together so the design works beyond a title page.

For visually grounded subjects such as places, architecture, products, history, nature, or travel, acquire relevant imagery before composing the deck. The user does not have to request photos explicitly. Make selected images large enough to reveal the subject. A city presentation should let the audience see that city; generic boxes, decorative skyline bars, and tiny thumbnails do not serve that purpose. Text-led or purely diagrammatic slides are appropriate when the content or requested style calls for them.

Use generate_image only when the user clearly asks for newly invented imagery or a generative edit, including artwork explicitly requested for the deck. A presentation topic, speculative subject, or need for decoration does not itself request image synthesis. Otherwise use retrieved or supplied images and editable diagrams. For requested synthesis, specify aspect ratio, focal point, and crop space, inspect the preview, and embed the saved original. Label speculative scenes where they could be mistaken for real places or evidence. Use retrieved images for factual photographs and logos.

## Find usable image assets

- Call `web_search` with `include_images: true` and a precise subject query. It returns candidate image URLs with descriptions alongside reference pages. For a known page, `web_extract` with `include_images: true` can reveal its images. Official sources, museums, and Wikimedia Commons are useful starting points.
- Download selected URLs into `assets/` using Bash. Use URLs actually returned by tools or a public API. Check the response is an image, inspect its dimensions, and call `inspect_workspace_images` before placing it. Descriptions and filenames do not establish what an image depicts.
- Preserve source page URLs, image URLs, creator/license information when supplied, and attribution requirements in an asset manifest or speaker notes. Cite factual claims separately. Do not invent credits or assume that discovery grants unrestricted reuse.
- If a download fails, try another credible source or its image API. Use an appropriate editable diagram or explain the missing asset when retrieval is exhausted. Failed retrieval does not authorize image generation.

## Compose for the material

Select a composition that helps the audience understand each point. For example:

- An opening image can occupy the whole slide with a short title in its quiet area, or share space with a large typographic title. Choose a crop with a recognizable focal point.
- A real project can use one large photograph or plan with two or three short annotations anchored to visible details.
- A route or process can use an editable diagram whose connections carry information, instead of paragraphs placed in separate cards.
- A comparison can use two aligned images, a chart, or a before/after composition. Charts require real, cited values; do not fabricate data to fill space.
- A speculative scene can pair original artwork with a small, clearly labeled scenario. A closing slide should land the central idea; detailed sources belong in notes or a quiet appendix.

Choose among these as the story requires; this is not a prescribed slide sequence. Vary visual density and placement while retaining a common grid, type system, and palette. Let imagery, diagrams, or data carry a substantial part of the explanation. Keep text, labels, tables, and charts editable. Whole-slide raster generation loses that editability.

For a wide deck, leave roughly 0.5–0.7 inches at the edges unless intentionally bleeding artwork. Titles often need 32–48 pt and body copy 20–26 pt; these are starting points, not fixed rules. Cut copy before shrinking it. Use contrast and whitespace to establish a focal point, and keep captions subordinate but legible. Avoid laying text over visually busy areas.

Account for rendered line count: a two-line title needs a taller box and a lower starting position for the next block. Keep clear space between a wrapped heading, its subtitle, and the body. Do not reuse one-line heading geometry on every slide. At review time, inspect these gaps at full slide size, not just whether bounding boxes technically intersect.

## Author and review

The syntax contract at `/opt/office/node/example-deck.cjs` demonstrates text, tables, charts, and image placement. Read it when needed for API syntax; it is a capability fixture, not a design template. Helpers at `/opt/office/node/pptx-helpers.cjs` expose:

- `text(slide, value, {x,y,w,h}, options)` with geometry in inches and font size in points.
- `picture(slide, absolutePath, {x,y,w,h}, 'contain' | 'crop')`, preserving proportions. Use crop for a filled image area and contain when all of the image must remain visible.
- `await save(deck, fileName)`, the tested writer that removes unused slide-master content-type declarations emitted by 4.0.1. Put asynchronous work inside `async function main()` and surface failures with `main().catch(error => { console.error(error); process.exitCode = 1; })`.

Save the actual PPTX, run validate_office_file, and render every slide with render_office_preview in batches of up to four. Review both individual slides and the sequence. Check imagery relevance, meaningful visual hierarchy, presentation-size legibility, composition variety, image crops, and whether the title's point is evident at a glance, as well as clipping, overlap, contrast, and content accuracy. A slide may be mechanically clean and still need redesign. Revise weak slides before recording passing visual_reviews with the current source_sha256. Every edit requires fresh review.

After three unsuccessful repair cycles, explain the blocker and retain the workspace draft without attaching it. Otherwise deliver only the requested presentation through finish_response. Describe its useful content briefly. Validation metadata, renderer versions, hashes, and page-review counts are internal checks; include them in user-facing text or captions only when requested.
