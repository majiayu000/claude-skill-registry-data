---
name: gw-media-content
description: "Propose up to 10 varied, unpublished posts about a project (app, updates, development, AI-workflow data) for its own social channels. Use when the user asks what to post, for post ideas, a content plan or proposals for X, Reddit, LinkedIn, Discord or another channel the project declares."
license: MIT
compatibility: "Needs Python 3 and git for the figures; the pieces themselves are made by gw-media-content-now (Node with Playwright, ImageMagick with WebP)."
metadata:
  version: "0.4.3"
  source: "Galivelop workshop; generalised from a project's social-media skill"
---

# gw-media-content

If `.claude/gw/gw-media-content.md` exists in the project, read it first: it holds what is specific to the project.

You **propose**; the user picks; `gw-media-content-now` produces each picked piece. Nothing is ever published: the
user posts and records where. Every number in a proposal comes from `cifras.py` or from a cited file and line or
commit, never from memory.

Shared material in `.claude/skills/gw-media-content/`: `catalogo.md` (post types), `reglas.json` (per-network limits),
`plantilla/` (the piece template), `nota.md` (the project note), `scripts/` (`cifras.py`, `comprobar.py`, `render.mjs`).

## Project note

`.claude/gw/gw-media-content.md` (shape in [`nota.md`](nota.md)) sets `<dir>`, the folder below, and the active
channels and languages.

## Steps

1. **Read the ground.** Done when you can list what is already published, already a piece or still `proposed`: every
   `<dir>/propuestas/*.md` (its `Base:` commit, the topic and status of each proposal; the newest file gives the
   `Base:` for step 2), and the title, `## Canales` and `## Publicado` of every `ficha.md` in `<dir>/*/*/`.
2. **Gather what happened.** From the repo root, run `python3 .claude/skills/gw-media-content/scripts/cifras.py`
   with `--desde <Base>` set to the newest `Base:` (no proposals file yet: no `--desde`).
   - Without `--desde` it starts at the last version tag; when that tag points at HEAD it uses the previous one and
     says so in `desde` and in the note «points at HEAD» of `ultima_etiqueta`.
   - A `Base` that git no longer knows (rebased, garbage-collected) makes it exit 2: run it again without `--desde`
     and tell the user the range changed.
   - A shallow clone exits 2 as well: run `git fetch --unshallow --tags`, then again.
   - A note «found, but its version is not readable» on `version_proyecto`: pass `--version-file <path>` or leave the
     version out of the proposals.
   Then read what the figures point at: the CHANGELOG section, the log file, the commits, ADRs, plan or roadmap, test
   and CI results, `/opt-tokens` and `/retro` reports, new screenshots. Done when each candidate has a fact you can
   cite. What is presented as done is merged work; the roadmap and behind-the-scenes types may use open plans,
   labelled as plans and never as shipped.
3. **Choose.** Match the facts to rows of `catalogo.md`. Drop what step 1 found published, in a piece or `proposed`.
   Done when the set has **at most 10** proposals, **no more than 2 of one topic**, and a topic mix (a set that is
   all releases has missed the catalog); fewer than 10 when the facts run out.
4. **Write `<dir>/propuestas/AAAA-MM-DD.md`** (today; folder created if missing). A new file starts with
   `# Proposals AAAA-MM-DD` and `Base: <HEAD short sha>`. If today's file exists, append a section that opens with
   its own `Base:` line and continue the numbering after its last `P<n>`; the file is never overwritten and the
   newest `Base:` counts. One block per proposal:

   ```
   ## P1: <short title>
   - **Topic:** <catalog row>
   - **Hook:** <the angle in one sentence>
   - **Format:** <template source, screenshot or text only>
   - **Networks:** <channels, from the active ones>
   - **Facts:** <each fact> (<cifras.py name, file:line or commit>)
   - **Value now:** <why this week and not another>
   - **Status:** proposed
   ```

   A Reddit proposal also names the subreddit and says whether the note holds its dated rules; without them the
   proposal says the user must paste them before the piece.
5. **Present and wait.** Show the list as a table (id, topic, hook, networks) and ask which to produce. Each picked
   one goes to `gw-media-content-now` with its id (`AAAA-MM-DD/P3`). Commit the proposals file with the project's
   commit format and a log row.

## Choosing well

- **One audience per post.** The project's users and the readers of its AI-workflow data are different audiences.
- **Value first.** A proposal gives readers something to use, check or answer; announcement-only posts come last.
- **Honest numbers.** A figure that does not flatter stays if it is true; `cifras.py` is the single source.
- **Channel fit.** `catalogo.md` lists the best networks per topic; `reglas.json` marks which limits are verified
  (`P`, `S`) and which are not (`NV`, `C`). Say so when a proposal leans on an `NV` limit.
