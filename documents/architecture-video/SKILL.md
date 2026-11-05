---
name: architecture-video
description: >
  Architecture Video — a short explainer video of the documented architecture, narrated by Alia on screen:
  what the system is, who it talks to, how it is organized in layers, each use case phase by phase with its
  budget, the decisions in force and the debt it declares open. Motion graphics built by code from the
  documents (no 3D, no recording) in the Alia Guide look, rendered to MP4 with HyperFrames. Use for
  "architecture video", "video de la arquitectura", "explainer video", "video explicativo", "make a video of
  the architecture", "onboarding video", or any request to explain the architecture as a video. Requires
  ARCHITECTURE.md. Not for the interactive 3D model (architecture-command-center) or Word exports.
triggers:
  - architecture video
  - video de la arquitectura
  - video explicativo de la arquitectura
  - explainer video
  - make a video of the architecture
  - architecture explainer
  - onboarding video
---

# Architecture Video Skill

A two-to-four-minute video of the architecture for people who will not read it first: a sponsor, a new
team member, a team that will consume the system. Every scene is cut from the documents by code; the
only words written in the session are **Alia's lines** — the tagline, the problem and the answer, one
line per chapter, one optional tip per use case, the closing — each held to a limit and to its sources.

| Scene | From | Alia |
|---|---|---|
| Title | `ARCHITECTURE.md` markers (name, type, version, status) | her cover pose, the escudo once |
| What it is | docs/01 Problem Statement and Solution | explaining pose |
| Who it talks to | systems and the docs/05 integrations crossing a system boundary | chapter codec |
| How it is organized | docs/03 § 4.1 layers and their containers | chapter codec |
| One per use case (≤ 5) | docs/04 flows: phases in order, owner chains, budgets, target, governing ADRs | chapter codec once, a tip per flow (point-left) |
| Decisions | ADRs in status `Accepted` — the project's (101+), else the institutional ones | explaining pose |
| What stays open | TDRs not `Resolved` / `Won't Fix`, by status | warning pose |
| Closing | version, status, release date | happy pose |

A scene with no material is left out and named (`left out:`). A chapter card is Alia's talking codec at
the video size (160 px — the Alia Guide's `AliaCodec` rule for video); a `worried` call does not talk, it bobs.

## Step 0 — Resolve the directories and check HyperFrames

```bash
bun "$HOME/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts"
```

`[plugin_dir]` is its answer; the skill's scripts are under `[plugin_dir]/plugins/sa-visualization/skills/architecture-video/scripts/`
(`[video_dir]`). Then:

```bash
bunx hyperframes@0.8.223 --version
```

HyperFrames renders the video (Chrome, headless, through its own install) and needs the network on the first
run and at render time (GSAP from jsDelivr, fonts from Google Fonts). If the command fails, stop and name it:
the storyboard and the project can still be built (Steps 1–3) and rendered later.

## Step 1 — The storyboard (code)

```bash
bun [video_dir]/video-prepare.js <project_root>
```

Writes `.cache/sa-skills/video/storyboard.json` and `lines.request.md`, and prints the scenes and what was
left out. Report the `left out:` lines to the user; never fill a missing scene from memory.

## Step 2 — Alia's lines (the session)

Read `.cache/sa-skills/video/lines.request.md` — it lists every slot with its limit and purpose, and the
sources each line may be written from — and write `.cache/sa-skills/video/lines.json`: one key per slot,
a plain-text string in the architecture's language (`DOC_LANGUAGE`).

- From the listed sources only: no fact, figure or name they do not state; components by their canonical full name.
- One line each, no Markdown, within the limit; Alia speaks to the viewer in the first person, present tense.
- `flow.<code>.tip` slots are optional: write one only when the flow block gives something worth noticing.

## Step 3 — Build the project (code)

```bash
bun [video_dir]/video-build.js <project_root>/.cache/sa-skills/video/storyboard.json \
  <project_root>/.cache/sa-skills/video/lines.json --out <project_root>/visualizations/architecture-video
```

Exit 1 names each refused line (`refused <slot>: <why>`): fix it in `lines.json` — an edit of that line — and
run the build again. The project is `index.html`, `compositions/<scene>.html` and `assets/` (Alia's poses,
faces and escudo, copied from the skill).

**Her music**: under the whole video a quiet neon-night bed, `assets/music/bed.wav`, composed by code
(`scripts/music.js` — original, no third-party track): a warm pad, a soft arpeggio with a ping-pong echo, a round
bass, light drums, rain behind it and her sparkle when she arrives and leaves, at 84 bpm. It follows her mood
scene by scene, changing on a bar line — the intro without drums, calm and thinking moving, pleased lifting,
worried and stern darker with fewer drums — and ends on a held chord at the video's length. It waits with the viewer and never
leads: `--music-volume <0..1>` sets its gain (default 0.3), `--no-music` leaves the video silent.

## Step 4 — Check, look, render

```bash
cd <project_root>/visualizations/architecture-video
bunx hyperframes@0.8.223 check --json
bunx hyperframes@0.8.223 snapshot --frames 12
```

Fix every check error before rendering. Look at the contact sheet: text inside its box, nothing overlapping,
every scene with something on it. Then:

```bash
bunx hyperframes@0.8.223 render -o ../architecture-video.mp4
```

Report the file, its length and the scenes. Offer `bunx hyperframes@0.8.223 preview` to watch it before
sharing. Never publish or upload the video: it is a local file the user shares.

## Permissions Required

```json
"Bash(bun *)",
"Bash(bunx hyperframes*)",
"Read(visualizations/**)",
"Edit(visualizations/**)",
"Read(.cache/sa-skills/**)",
"Edit(.cache/sa-skills/**)"
```

The skill writes under `visualizations/` and `.cache/sa-skills/video/`. It reads `ARCHITECTURE.md`, `docs/**`,
`adr/**` and `tdr/**` and never writes to them. It reads nothing compliance writes.
