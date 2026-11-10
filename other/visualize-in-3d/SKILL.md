---
name: visualize-in-3d
description: Visualize anything in 3D - a place, an operation or system (airport, data center, port, factory, hospital), an object or product, a creature or character, a story or event in time, something spreading over real land, or how a thing works. Builds a live three.js app with a dashboard and a 30 s film, a lesson app, a quick no-Blender prototype, a live embed on real data, a documentary film, an action short, a showcase film or stills of one object, an interactive cutaway plate or book, or a playable web game. Looks come in four families (clean product, real and cinematic, technical, stylized art), from clean ops world and isometric dioramas to photoreal terrain, white model, point cloud, cutaway plate, space-time cube, pixel, ASCII, glow and layer build. Models come from ready sources or Blender builds made from real references, and the skill checks its own frames before showing anyone. Use for "visualize X in 3D", "make a 3D film of X", "show this event on a 3D map", "a live 3D dashboard of X", "a 3D lesson on how X works", "show off this model", "a quick 3D prototype", "two creatures fight in 3D", "dựng 3D cái này", "app nhìn như game", "làm phim 3D về", "cho 2 con đánh nhau", "pixel battle", "theme point cloud", "kiểu wildfire tool".
license: MIT
---

# Visualize in 3D (Dựng mọi thứ thành 3D)

If `references/local.md` exists, read it first: it sets the folders and house rules for this machine. Then read
`{{WORK_DIR}}/viz3d-lessons.md` if it exists: rules learned from this user's past corrections (`references/learning.md`).

Take any subject and make it 3D: models from real references, a seeded simulation or a scripted timeline
driving them, a look chosen for the subject, and a film checked frame by frame. The user can also start it with
`/viz3d <mode> <subject>` (modes: app, lesson, prototype, embed, film or doc, action, showcase, book, game).
Paths use `{{WORK_DIR}}` for the folder where projects live (the current directory unless the user names one) and
`{{SKILL_DIR}}` for this skill's folder, with forward slashes on every platform.

## Before you start

1. **Blender** (not needed for a quick prototype, an embed, or the pixel look): run `blender --version` or look in
   the usual install folder. If it is missing, say it gives much better models, is free at blender.org, and ask
   whether to wait or go on without it. Without it, follow `references/no-blender.md` and say in the report that
   model quality is lower.
2. **Node 20+ and Playwright with Chromium** for recording; **ffmpeg** for encoding and checks. **67js** renders
   films and stills: when one is the deliverable, read `references/67js.md` for setup and when to use it.
3. **Subagents:** where the harness has them, give each pass to a fresh subagent with its brief and keep it inside
   about 80 tool calls. Where it does not, run the passes one after another in this session, finish and check one
   before starting the next, and re-read the plan file at the start of each.
4. **Downloads** (elevation, map data, models, reference images, sounds): name the source, count and rough size,
   and get the user's OK first. If the user approved downloads ahead or is away, take open files only (CC0, CC BY,
   public domain, open data), list each in `CREDITS.md` and go on.

## 1. Pick the shape

Read what the user wants people to see, then pick one shape (or combine two) and read its reference:

| The subject is | Shape | Read |
|---|---|---|
| A place or system that runs (units, tasks, flows) | Live app with dashboard and a 30 s film | `references/brief.md`, `examples/`; a built world shown as render, then clay model, then render: `references/clay-reveal.md` |
| How a thing works (aircraft, circuit board, engine) | Lesson app: 3 to 5 lessons, one control each, a "Build your own" sandbox | `references/brief.md` (parts, flow overlays, sandboxes) |
| Something spreading over real land | Terrain app with a time scrubber | `references/looks.md` (photoreal terrain), `examples/wildfire-valley.md` |
| A story, case or piece of history | Documentary film | `references/documentary.md`, `references/film.md`, `references/67js.md` |
| Characters, creatures or machines doing something | Action short | `references/action.md`, `references/67js.md` |
| One object, product, model or creature to show off | Showcase film or stills | `references/looks.md` (Dither + ASCII showcase, Gradient glow ASCII), `references/film.md`, `references/67js.md` |
| One object cut open or exploded | Cutaway film, or an app with a section view | `references/film.md`, `references/looks.md`, `references/67js.md` |
| One big object or building with many rooms, as a page or a book | Book: interactive illustrated cutaway plate, with quizzes | `references/book.md`, `references/looks.md` |
| A game people play in the browser (steer a creature, survive, grow) | Playable web game, bot-balanced | `references/game.md` |
| A demo for leaders in about an hour | Quick prototype from ready models, no Blender | `references/live-embed.md` |
| A live view inside an existing dashboard or product | Embed (web component or iframe) on real data | `references/live-embed.md`, `scripts/mock-feed.mjs` |

Pick the look in `references/looks.md` (Choosing: four families, a default per shape; a named look wins). Then pick a
style reference, never build from words alone: the user's image, video or page, else two or three you find and show
(`references/style-reference.md`). Its style card goes in the plan file, and every review round compares against it.

## 2. Write the plan file

Write one file in `{{WORK_DIR}}` before anything is built: the topic file for an app (the `examples/` shape), the
fact file for a documentary, the action sheet for an action short. It names the real parts of the subject, what
moves or changes, the beats or features to show, the look, and the camera view that shows the subject best (a
cutaway for depth, top-down for flows, low side for arrivals).

Research the real subject first: real dimensions, steps, rules and moves. Use made-up names for companies and
people unless the user asks for real ones. For a real named place, follow "A real place" in
`references/real-objects.md`.

## 3. Pass 1: assets and stage

Models follow `references/asset-sources.md`: ready models first, then scans, packs, AI-generated models, and
Blender builds from a reference sheet (`references/real-objects.md`). The pass reports stills at film scale.
A review loop that reads many frames runs them through a `frame-reader` agent; open only the frames a decision hangs on.

## 4. Pass 2: build and film, with the self-review loop

Build the app or the film from the plan file with the brief in `references/brief.md`. Before reporting, run
`references/self-review.md` for up to three rounds: `scripts/frame-guard.js` measurements, frame sheets and the
mode's fault list. Run the two passes separately; one pass doing both runs too long.

## 5. Check, then show

Open the final sheets and peak stills yourself (`scripts/contact-sheet.sh`, sheets newer than the video). Look for
what the loop can miss: a subject wrong for the real thing, a dull beat, broken UI rules, toys or programmer art.
Learn the same turn (`references/learning.md`): every user correction and every fault you caught becomes a dated
rule with a check in `{{WORK_DIR}}/viz3d-lessons.md`, applied to this piece before you report.

## 6. Polish

Give fixes to one more pass ("everything else is approved, change nothing else"), re-record, publish on the user's word.

## Rules

- Every round, fixes included: a fast low-quality preview of the whole cut first; full render after the user's OK.
- Original names and designs by default. Real brands, liveries and known characters only when the user asks, with
  licensed models and a credit line.
- Every main asset matches a reference of the real thing. Models from memory read as toys.
- Every frame is a function of time (a virtual clock, clips set from it), so any frame renders the same in any
  order. Real clicks on that clock drive an app's film, not a camera moved in code.
- Render and encode at low priority, one heavy job at a time, and stop every server you start.
- Real people and real harm: facts from sources, victims named with respect, no gore (`references/documentary.md`).
- The public copy of this skill is mirrored from this folder. Edit only this folder; never put personal paths, names
  or tools outside `references/local.md`. A nightly sync script mirrors the rest.
