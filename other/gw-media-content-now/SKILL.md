---
name: gw-media-content-now
description: "Produce one unpublished post piece (texts per channel plus images) in a dated folder, from a proposal id or a free topic. Use when the user picks a proposal from gw-media-content, or asks for a single post, announcement or image about something that just happened."
license: MIT
compatibility: "Needs Python 3, git, Node with Playwright and ImageMagick (convert with WebP) for the media step."
metadata:
  version: "0.4.3"
  source: "Galivelop workshop; generalised from a project's social-media skill"
---

# gw-media-content-now

If `.claude/gw/gw-media-content-now.md` exists in the project, read it first: it holds what is specific to the project.
Then read `.claude/gw/gw-media-content.md` if it exists, and its shape in `.claude/skills/gw-media-content/nota.md`
(folder `<dir>`, languages, channels, extra channels, palette, screenshots, task prefixes, Reddit rules).

You make **one piece**: `<dir>/AAAA-MM-DD/NN-<tema>/`, with texts for each channel and the images that go with
them. Pieces accumulate in the day's folder. Nothing is ever published: the user posts and records where. Shared
material is in `.claude/skills/gw-media-content/`: `catalogo.md`, `reglas.json`, `nota.md`, `plantilla/`, `scripts/`.

## Steps

1. **Input.** A proposal id (`AAAA-MM-DD/P3`: read its block in `<dir>/propuestas/AAAA-MM-DD.md`) or a free topic
   (pick the row of `catalogo.md` that fits; with no repo data behind it, say so and stop). Done when you can name
   the topic, the facts to use and the channels: the proposal's networks (or the request's) among the active ones.
2. **Folder.** `<dir>/AAAA-MM-DD/` for today; `NN` is the next free two-digit number there (01 if none); `<tema>` is a
   lowercase slug (`a-z`, `0-9`, `-`). Copy `.claude/skills/gw-media-content/plantilla/` into `NN-<tema>/` and shape it:
   - delete the channel files not in use; for an extra channel of own format, copy its template (note) as `<canal>.md`;
   - in `ficha.md` set `Idiomas:` (the first language is the main one) and `## Canales`, delete the `## Reddit` block
     when `reddit` is not a channel, and delete the example rows of `## Hechos comprobados` and `## Imágenes`;
   - replace every `<tema>`, `AAAA-MM-DD` and `{{...}}` placeholder in the folder, or delete its line.
   Done when the piece folder holds `ficha.md` plus one file per channel, with no placeholder left.
3. **Facts first: `ficha.md`.** Every claim in the piece goes in the table `Hechos comprobados` with its source.
   Numbers come from `python3 .claude/skills/gw-media-content/scripts/cifras.py [--desde REF]`; the rest from a cited
   file and line or commit. Only what is merged; if the project has a canon (lore, design docs), claims about it come
   only from there. Task ids, branches and internal notes go in `Uso interno`. Done when each fact a channel will use
   has a source cell.
4. **Media.** Every image a channel carries exists in `medios/` and is listed in `## Imágenes` with alt text in
   every language; a text-only piece leaves `## Imágenes` with no rows.
   - From the template: `mv` (not `cp`) the source for the chosen format in `medios/fuente/` to its final name, delete
     the other template sources, and fill every `{{...}}`. Names per language: the first language
     `medios/fuente/<n>.html`; any other language that needs its own image `medios/fuente/<n>.<lang>.html` (never a
     suffix for the first language: `comprobar.py` rejects it). Apply the palette from the note.
   - Screenshots: steps in the note; crop to what matters, save in `medios/fuente/` as `.png` or `.jpg`; no
     personal data, no placeholder or broken text on screen.
   - Render: `node .claude/skills/gw-media-content/scripts/render.mjs <piece-folder>` (it names what is missing and the
     command to fix it). From `medios/fuente/<n>.html` it writes `medios/<n>.webp`, `medios/<n>-mini.webp` and
     `medios/<n>.png`; from `<n>.<lang>.html`, `medios/<n>.<lang>.webp` (+ `-mini`, `.png`); a `carrusel*.html` gives a
     `.pdf`. Use the `.png` for LinkedIn (it takes `.png`, `.jpg`, `.gif`, not WebP), the `.webp` for X, Reddit and
     Discord, `.webp`, `.png` or `.jpg` for an extra channel, the `.pdf` carousel for LinkedIn only. Read each render
     image before using it.
5. **Channels.** Write each channel file in every language, from the ficha only, in the shape of its template file and
   within `reglas.json` (`comprobar.py` enforces it). Each post names its image on an `Imagen:` line; in an
   own-format channel there is no `Imagen:` line: the image path (`medios/x.webp`) appears in the file's text.
   - **Reddit** (`## Reddit` in `ficha.md`): the `- **Subreddit:** r/<x>`, `- **Normas leídas:** AAAA-MM-DD` and
     `- **Autopromoción:**` lines go before the first `###`, then one `### Normas de r/<x>` per subreddit holding the
     rules the user pasted (at least `reddit.normas_min_caracteres` characters, no `#` headings inside: paste them as
     plain lines). `Normas leídas:` is counted from the piece's date folder and is at most `reddit.normas_dias` days
     old. Take the rules from the note or the ficha when they are dated within that limit; otherwise ask the user to
     paste them (Reddit cannot be read automatically, and rules are never invented), then continue.
   - **Extra channels** (declared in the note): one `<canal>.md` as the note says: a section per language within its
     `límite`, or the copied own-format template filled in. If the note gives neither, ask.
6. **Check.** Build the command from the note as `nota.md` says (`--prefijos-tarea`, and `--limite <canal>=N` or
   `--formato-propio <canal>` for each extra channel of the piece) and run
   `python3 .claude/skills/gw-media-content/scripts/comprobar.py [options] <piece-folder>`; it prints `OK`, and each
   line it prints is a fix to make. Then reread the English: natural, not a literal translation.
   Done when `OK` is printed and the reread found nothing to change.
7. **Close.** Mark the proposal `**Status:** done → <piece folder>`. Commit with the project's commit format; the log
   row names the folder, its channels and that it is ready to publish. Show the user the texts and image paths.
   After publishing, the user fills `## Publicado` in `ficha.md`.
