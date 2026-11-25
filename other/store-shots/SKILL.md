---
name: store-shots
description: Store screenshots as framed, captioned App Store and Google Play images, and Play's feature graphic, built by the store-shots tool. Use when setting the tool up for an app, planning new store screenshots, changing or translating their text, designing their look or adjusting it, re-capturing app screens after an app change, or adding a store device or language.
---

# Store shots

The `store-shots` tool turns app screens and their copy into store images: screenshots per store,
device and language, and Play's feature graphic. The approved images in `out/` are its result.

A project is the folder holding `store-shots.yaml`; this skill's `example/` folder is a complete
one. The command is `bin/store-shots.py` in this skill's folder, run through uv on every OS:
`uv run --quiet --script <this skill's folder>/bin/store-shots.py <command>`, written
`store-shots <command>` below. It needs [uv](https://docs.astral.sh/uv/) and Google Chrome,
Chromium or, on Windows, Edge (or `STORE_SHOTS_CHROME` set to any of them). Run it from the
project folder (or pass `--project <folder>`); `--help` lists the commands and their options.

## First step: status

Run `store-shots status` before anything else. It names every stale output by stage (`capture`,
`compose`) and the input that made it stale. Then find your change in the table below
and open only that stage's file. When it finds no `store-shots.yaml`, the app has no project yet:
open setup.

The tool decides what is redone. Every raw and image keeps a `<name>.inputs.json` sidecar of the
hashes it was made from, and `build` runs capture, compose, check and sheet, redoing only what is
stale. Your part is to edit the stage's input files and run `build`; the files connect the
stages, so you can enter at any stage whose inputs exist.

Each command prints one line per stage and an exit code. A `FAILED` line names the first problem;
the full output is in `.store-shots/logs/<stage>.log`, which you read only then.

## Grilling: talking to the owner

The owner is the person whose app it is. Every stage asks them something. Ask the same way each
time:

- **Plain words.** Talk the way a person would. Name the screenshots and what you will do to them
  ("the third screenshot", "the editor screen"). This skill's own terms (grilling, storyboard,
  stage, scene, card, adapter, target, slot, raw, sidecar, contact sheet) stay out of what you say.
- **Look first.** Whatever the app's code, its store listing and its current screenshots show,
  you settle yourself. Only what they leave open goes to the owner, as a recommendation to confirm.
- **Ask tool.** Ask through your harness's tool for multiple-choice questions, putting as many in
  one call as it allows. Ask a question only once the answers it depends on are in. If you have no
  such tool, ask in plain text as a numbered list, each with its recommended answer first, and end
  your turn.
- **Open questions in plain text.** A question whose answer has no short list of choices ("Do you
  have a look in mind?") goes in plain text, and you end your turn. Its choices come after, from
  what the owner said.
- **Recommend.** Every question lists the recommended answer first, marked as recommended, so one
  click accepts it. Word each question so that "yes" accepts the recommendation. Agreeing must
  never mean answering "no".
- **One sentence of why** when an answer changes what store visitors see or what you have to
  build ("A Play listing also needs a feature graphic: the banner at the top of the page.").

## Between steps: say what comes next

The owner should never be surprised by what you start doing. Before you start a stage, and before
any step that adds code to the app's own folders or runs for minutes (writing the adapter,
`adapter test`, `build`, any capture), tell the owner in plain words what you will do next, what
it changes and about how long it takes. Then ask whether to go ahead and wait for the answer:
"Next I write the code that opens each screen in the simulator and saves it. It adds files under
`tool/capture/` in the app and takes a few minutes. Shall I go ahead?"

Once the owner says go, the commands inside that step run without asking again, and so does
re-running a step to fix what it failed on. When the step is done, say in a sentence or two what
it did, then announce the next step.

## Stages

| Stage | You edit | The tool writes | Instructions |
|---|---|---|---|
| Setup | the adapter | the project, with `init` | [stages/setup.md](stages/setup.md) |
| Storyboard | `storyboard.yaml` | | [stages/storyboard.md](stages/storyboard.md) |
| Design | `layout/`: the page, its stylesheets, fonts, icons and placement | `.store-shots/preview/`, with `preview` | [stages/design.md](stages/design.md) |
| Copy | `texts/<lang>.yaml` | | [stages/copy.md](stages/copy.md) |
| Layout | `layout/placement.yaml` | | [stages/layout.md](stages/layout.md) |
| Capture | the adapter, its scenes and demo content | `raw/<target>/<lang>/` | [stages/capture.md](stages/capture.md) |
| Compose | | `out/<store>/<code>/`, `.store-shots/sheets/` | [stages/compose.md](stages/compose.md) |
| Review | | | [stages/review.md](stages/review.md) |

Everything under `raw/`, `out/` and `.store-shots/` is output: change it through the stage that
writes it.

The folder names here and in every stage file are the defaults, relative to the project folder. A
project's `paths:` ([docs/config.md](docs/config.md#paths)) can move any of them, even outside the
project (copy files kept with the app's other store texts, say): read it before you edit, and use
the moved folder wherever a file names the default.

## Change to stage

| Change | Stage |
|---|---|
| The app has no project yet | setup, then the new screenshot set below |
| A new screenshot set: panels, claims, scenes | storyboard, then design, copy, capture, compose, review |
| A new or changed panel, claim or shown screen | storyboard, then each stage `status` and `build` name |
| A screen wanted as it is, with no frame (an in-app purchase review screenshot) | `unframed:` in the config ([docs/config.md](docs/config.md)), then capture |
| A headline, subline, badge or feature graphic text | copy |
| A new language | copy (its "New language" section) |
| The look: background, typography, colours, the card's or badge's look, the feature graphic's design | design |
| A device, card, badge, cluster member or copy block's position or size | layout |
| The app's UI changed; a scene or demo content changed | capture |
| The adapter itself changed, or fails `store-shots adapter test` | capture ([docs/adapter.md](docs/adapter.md)) |
| A new device slot | layout (its "New device" section) |
| A device's screenshots turned to landscape or back | its target's `size` and `screen` ([docs/config.md](docs/config.md#targets)), then capture and layout |
| An image fails `check`, or looks wrong | compose |
| The owner approves a set of images | review |
| Uploading images, listing text or in-app purchases | the project's release tooling |

## Reference

- [docs/config.md](docs/config.md): `store-shots.yaml`, every key.
- [docs/storyboard.md](docs/storyboard.md): `storyboard.yaml`, every field.
- [docs/layout.md](docs/layout.md): the panel and feature graphic pages, `placement.yaml`.
- [docs/adapter.md](docs/adapter.md): the adapter contract, its gates, choosing the capture tool.
- [docs/checks.md](docs/checks.md): what `check` reports and how to fix each problem.
