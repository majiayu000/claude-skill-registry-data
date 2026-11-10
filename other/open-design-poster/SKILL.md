---
name: open-design-poster
description: Design a poster or flyer for print or screen, check it, and export print-ready PDFs or upload-ready images, including other sizes and one version per row of a spreadsheet — use whenever the user wants a poster, flyer, event or gig poster, print piece, handout, certificate or name card set, or wants an existing design in other sizes or as a print-ready PDF, even if they don't mention Open Design
---

<!-- generated:open-design-agent-kit -->

Design a poster with Open Design, check it, and export files that are ready to print or post.

Brief: the rest of the user's message (if there is none, ask the user: "What is the poster for, and is it for print (which size) or screens?")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Pick the medium and a default shape

Decide whether this is for **print** or **screens**. If the brief doesn't say, ask the user before doing anything else. Don't guess between print and screen: the units, bleed and type sizes are different.

You don't need the final size yet. The poster is built **fluid**: it reflows to any shape, so the user can pick or change the size later, when exporting. Use the size the user names as the default shape; otherwise use `a3` for print and `ig-portrait` for screens, and tell the user they can change it at any time.

| Use | Format id | Size |
|---|---|---|
| Print, small: flyer, handout | `a4` · `letter` | 210×297 mm · 8.5×11 in |
| Print, medium: notice-board poster | `a3` · `tabloid` | 297×420 mm · 11×17 in |
| Print, large: wall poster | `a2` · `a1` · `poster-18x24` · `poster-24x36` | 420×594 mm · 594×841 mm · 18×24 in · 24×36 in |
| Print, conference or research poster | `a0` | 841×1189 mm |
| Instagram portrait | `ig-portrait` | 1080×1350 px |
| Story / Reels / TikTok cover | `story` | 1080×1920 px |
| X single image | `x-image` | 1600×900 px |
| Square (Instagram / LinkedIn) | `ig-square` | 1080×1080 px |

A handout and a wall poster carry different amounts of text, so if the user says which it is, write the copy for that; the shape itself can still change.

## 2. Generate

If the user asked for options ("show me a few directions"), run a design exploration first and build out the direction they pick, with the same `format` and `fluid: true`.

Otherwise call `prepare_open_design_brief` with:

- a `skillId`: `od:prototype:poster-hero` for a bold marketing poster, `od:prototype:magazine-poster` for an editorial or type-led one, or another skill whose style fits better (`list_open_design_skills` with query "poster");
- the brief, in the user's words;
- `format`: the default shape from step 1;
- `fluid: true`.

Call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active.

Author the file yourself, following the returned instructions. Their **Canvas** section is authoritative: one `data-od-card data-od-fluid` element sized by `--od-w`/`--od-h`, everything inside sized in container units, and layout rules for wide and tall shapes. Also:

- Use real copy from the brief, with no lorem ipsum. A poster is read from a distance: one dominant headline, then the what / when / where, then the call to action.
- If the user gives a list of names, sessions or locations to make one poster each, mark the changing text with `data-od-field="<column name>"` (and a per-person QR slot with `data-od-qr-field="<column>"`), and fill the design with the first row's values.
- No external image URLs unless the user supplied them. No emoji as key visuals; draw them as inline SVG.

## 3. Add a QR code, if it needs one

Register the artifact first (step 4), then call `create_open_design_qr_code` with the entry path and the URL, and paste the returned inline SVG where the code goes. Never draw a fake or placeholder QR code.

## 4. Register

Call `register_open_design_artifact` with the entry path, kind `html`, a title, `sourceSkillId`, and `format` set to the default shape.

## 5. Check and fix

Call `check_open_design_artifact` with the entry path. It returns the poster as an image plus preflight findings. Fix every **error** in its findings (text cut off, overlapping or in the bleed, a QR code that doesn't decode), and fix warnings where you reasonably can (sizes that don't scale with the poster, small type, low contrast, low-resolution images). Look at the image too: the headline should dominate and nothing important should be cramped or cut. Check again until there are no errors (at most two fix rounds; tell the user about anything left).

## 6. Other shapes

When the user wants other sizes, or before the final export of a print piece, call `export_open_design_artifact` with `shapeSheet: true` and `checkOnly: true` (add `presets` with just the shapes they care about, or leave it out for every shape). It writes one image of the poster at each shape, marking shapes with errors; show it to the user. If you can view images, look at it too: the headline should dominate every shape and nothing important should be cropped.

For a shape that has errors or looks wrong, call `adapt_open_design_artifact` with the entry path and those format ids. For a fluid poster it returns **tune** instructions: fix that shape inside the same file with its `@container` rule, then check every shape again with a shape sheet. Don't create new files for other sizes.

## 7. Export

- **One shape:** call `export_open_design_artifact` with the entry path and `preset` set to the format id. A print format gives a PDF the size of the bleed box, with trim and bleed boxes set and the bleed added automatically; add `cropMarks: true` if the user's printer wants crop marks. A screen format gives a PNG within the platform's size limit.
- **Several shapes:** pass `presets` with the format ids instead: one file per shape, named `<name>-<format>`.
- **One per row of a list:** add `data` with the workspace path of the user's CSV, XLSX or JSON file, and `nameField` with the column to name files by. Images come out one per row; print PDFs come out as one multi-page PDF per shape (add `split: true` for one file per row).

## 8. Report

List each exported file's path, size and any remaining warnings. For print files, also give the trim size and bleed, and tell the user the PDF is RGB: most print shops convert it, but they should ask if theirs needs CMYK. Mention that the poster can be exported at any other size later without regenerating it. Don't print, post, upload or order anything yourself.
