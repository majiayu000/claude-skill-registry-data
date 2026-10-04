---
name: figma-capture-local
description: Organizes a user-supplied reference image and reference code (any language/framework, not fetched from Figma MCP) into `.figma/` as `<name>.png`/`<name>.jpg` and `<name>.jsx`/`<name>.<ext>`, plus a JSX/preview wrapper when the source isn't already JSX. Use when the user says "tenho uma imagem e um codigo de referencia", "captura isso localmente", "salva essa referencia local", "organiza essa imagem e codigo como referencia", "capture this local reference", or any variation providing a local reference image + code pair (no Figma URL involved). Do NOT use when the source is a Figma node URL — use figma-capture-mcp for that.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# figma-capture-local

Takes a user-supplied reference image + reference code (already on disk, or pasted inline) and organizes both into `.figma/` for side-by-side viewing, same shape as `figma-capture-mcp` output but with no Figma MCP call — input comes straight from the user.

## Steps

| #   | Step             | Action                                                                                                                                                                                                                                                                                                                                 | Output / Gate                                      |
| --- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1   | Collect inputs   | Ask user for: reference image path, reference code (path or pasted inline), and an output `<name>` (kebab-case; derive from image filename if not given). If either image or code is missing, ask — do not guess content.                                                                                                              | image path, code source, `<name>`                  |
| 2   | Detect code kind | If code is JSX/TSX already exporting a component, use as-is. Otherwise (HTML, CSS, vanilla JS, Vue, Swift, plain markup, etc.) keep the original file untouched AND wrap/convert into a JSX preview per [jsx-template.md](references/jsx-template.md) so the viewer can render it. Note the source language in the JSX header comment. | decision: direct copy vs wrap                      |
| 3   | Copy image       | `mkdir -p .figma && cp <source_image> .figma/<name>.<ext>` preserving original extension (png/jpg/jpeg/webp)                                                                                                                                                                                                                           | `.figma/<name>.<ext>`                              |
| 4   | Write code files | Copy the original reference code verbatim to `.figma/<name>.original.<ext>` (skip if input was pasted inline with no source file). Write `.figma/<name>.jsx` per Step 2's decision.                                                                                                                                                    | `.figma/<name>.jsx` (+ optional `.original.<ext>`) |
| 5   | Copy viewer      | `cp -n <skill_dir>/index.html .figma/index.html` (no-clobber — never overwrite existing)                                                                                                                                                                                                                                               | `.figma/index.html`                                |
| 6   | Verify           | `ls -lh .figma/<name>.* .figma/index.html`                                                                                                                                                                                                                                                                                             | confirm all files exist, non-empty                 |

## Examples

**JSX input**: user gives `hero.png` + `Hero.jsx` (valid React component) → copy image to `.figma/hero.png`, copy `Hero.jsx` to `.figma/hero.jsx` unmodified → copy viewer → verify.

**Non-JSX input**: user gives `card.png` + a Vue SFC → copy image to `.figma/card.png`, keep original at `.figma/card.original.vue`, write a JSX approximation at `.figma/card.jsx` (per template) with a header comment noting "Source: Vue SFC, converted for preview" → copy viewer → verify.

## Notes

- Never fetch or invent design data — every pixel/line of content in the output must trace back to what the user provided.
- If the reference code is pasted inline (no file), skip the `.original.<ext>` copy — there is no source file to preserve.
- `index.html` is identical to `figma-capture-mcp`'s viewer — it renders any `.jsx` alongside its same-named image, regardless of how the pair was produced.
- Use `rtk` for terminal commands when available (e.g. `rtk ls -lh .figma/`); `cp` exempt (no verbose output).

## Reference files

- [jsx-template.md](references/jsx-template.md) — JSX wrapping rules for non-JSX source code.
