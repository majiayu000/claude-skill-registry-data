---
name: plugin-visual
description: "Create the compact purpose SVG for a Canvas plugin during authoring, including passive markup, package-local references and accessible presentation."
metadata:
  version: "1.0.0"
  author: canvas-studios
---

# Plugin purpose graphic

Create a small editable illustration that communicates the plugin's actual job. Load this member at the graphic stage of Plugin Creator. Use the current exact plugin `draftRef`, its latest revision and common package file tools. No extra illustration installation or external asset service is needed.

## Choose a useful motif

Express the plugin's input, operation or useful result with two or three recognizable forms. For an account brief, CRM rows and a research document can flow into a short brief. For document conversion, show the actual source and result types. Avoid a generic cube, app logo collage, tiny prose or reusing the Creator's own icon for every plugin.

Default to a square `viewBox="0 0 256 256"` with enough inner margin for small cards. Use a restrained palette, consistent strokes and simple solid shapes. The 256-square size is an authoring convention, not a rule for historical packages. Check that the purpose remains readable at roughly 24–32 pixels as well as in a detail view and against light/dark surrounding UI.

## Write portable passive SVG

- Root `svg` uses `xmlns="http://www.w3.org/2000/svg"` and a finite positive `viewBox` that encloses the content.
- Include a meaningful `<title>` and `<desc>`. Use `role="img"` and `aria-labelledby` pointing to their IDs when appropriate.
- Use paths, basic shapes and groups. Keep geometry and text within the viewBox. If text is useful, set explicit size/fill and a portable font fallback; escape XML characters. Prefer little or no text and no emoji.
- Keep the file self-contained and passive: no scripts, event handlers, `foreignObject`, external resources/fonts, remote URLs, data-URL images, embedded HTML or active animation. Use only the SVG elements/attributes accepted by the server's passive-image validator. Stay below 2 MiB; a compact purpose graphic should be much smaller.

Write actual image bytes at `assets/logo.svg` with the draft file tool; set `interface.logo: "./assets/logo.svg"` in the existing manifest. `interface.icon` can point to a separately authored compact variant when useful. Do not add a new image field, store an absolute path or place a remote provider logo in this purpose slot.

## Verify and repair

Validate the complete current draft through `validate_canvas_package_draft`. Check the returned SVG/path/schema errors and repair the actual file. Validation belongs to that exact draft revision; deleting or changing the image afterward needs fresh validation and final publish rechecks it.

Inspect the graphic in the actual package preview, card and inline presentation when the available runtime supports visual inspection. Check clipping, scaling, contrast and legibility; source validation alone cannot prove good design. Preserve the draft and report an outstanding visual check when you cannot inspect it.

Internal SVG metadata does not replace a host-level alternative. A meaningful preview needs descriptive alt text or an adjacent semantic equivalent. In a small inline reference next to the already visible plugin name, a decorative image should avoid a redundant screen-reader announcement. Use the existing package presentation service so access and exact version remain enforced.

Return the written package-relative path, concise explanation of the motif, validation result and honest visual-inspection state to Plugin Creator. The graphic is one part of a valid package; it does not prove connection setup or workflow success.
