---
name: html-to-video
description: "Make a video from code: render an HTML page (CSS, Web Animations, SVG, canvas, three.js) to a deterministic mp4 with vawe, an open-source programmatic video and motion graphics framework for coding agents, and a free alternative to Remotion, HyperFrames and Motion Canvas. Load when asked for an HTML to video render, a launch video, a title sting, an explainer or motion graphics as code, and no film exists yet."
effort: low
license: Apache-2.0
---

# html-to-video: start here

When you talk to the person, use plain words: describe what the viewer sees, not the harness terms (map: harness/lib/plain-words.mjs).
vawe turns one HTML page into one mp4. You write the page in HTML, CSS, Web Animations, SVG, canvas or three.js. The renderer seeks the page to each frame time, screenshots it in headless Chrome, mixes the page's `<audio>` tags offline and encodes the video with ffmpeg. The same page gives the same frames in any order. There is no hosted API and no account.

## Install

```bash
git clone https://github.com/vawe-hq/vawe.git
cd vawe
npm install
bin/vawe new <name> --request "<the ask>"   # also checks Node, ffmpeg and Chrome and prints the install line for each missing tool
```

## Make a video

```bash
bin/vawe new hello --request "a 6 second title sting for a note-taking app"
bin/vawe dev films/hello/page.html       # draft mp4 in out/: half size, 30 fps, with sound
```

Edit `films/hello/page.html`, then run `dev` again. Time is the seek, never the clock: use CSS keyframes, `element.animate()` or `window.seek(t)` as a pure function of t. No timers, no state between frames, no unseeded random.

## Which skill next

| you are at | load |
|---|---|
| a request and no `brief.md` | `vawe-brief` |
| writing or editing `page.html` | `vawe-page` |
| the cuts between scenes | `vawe-transitions` |
| a draft rendered, before any fix | `vawe-critique` (in a session that did not write the page) |
| a reference mp4 to match | `vawe-reference` |

The page contract and the ten-step loop are in `AGENTS.md`. Every command is listed by `bin/vawe --help`.
