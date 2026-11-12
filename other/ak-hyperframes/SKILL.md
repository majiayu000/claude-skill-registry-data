---
name: ak-hyperframes
description: "Wrap the HeyGen HyperFrames CLI to render short social videos, launch clips and motion graphics from HTML compositions."
when_to_use: "Invoke for HTML-first video; remotion is the React-based alternative."
category: media
keywords: [video, hyperframes, heygen, html, vertical, social, motion-graphics]
license: Proprietary
argument-hint: "[composition or command]"
metadata:
  author: agentkit
  version: "1.1.0"
---

# ak-hyperframes

Wrap HeyGen's [`hyperframes`](https://github.com/heygen-com/hyperframes) CLI
for HTML-first programmatic video generation. This skill is docs+wrap only —
no vendored HeyGen source, no copied HeyGen agent skills. Every command below
runs the published npm package through `npx`, pinned to a known-good version.

## When to use

- Short vertical/social videos (1080×1920, 9:16) rendered from HTML/CSS.
- Product-launch clips, promo loops, motion graphics authored as HTML
  composition rather than React components or timeline editors.
- Any task where the composition source of truth is HTML markup with
  `data-composition-id` / `data-start` timing attributes (see
  [references/composition-basics.md](references/composition-basics.md)).

Not a fit for React-first compositions, frame-accurate interpolation curves,
or Remotion's audio/caption ecosystem — see also the installed remotion skill
for that alternative (React-based programmatic video). Not a fit for pure
FFmpeg/ImageMagick encode-only tasks — see also the ak-media-processing skill.

## Prerequisites

- Node.js 22+
- FFmpeg and FFprobe on `PATH`; headless Chrome (`hyperframes browser ensure`)
- Optional: HeyGen credentials (`HEYGEN_API_KEY` or `hyperframes auth login`)
  for cloud rendering; local rendering works without them.

Run the bundled verifier before starting any render work:

```bash
node scripts/verify-prereqs.mjs
# or, for machine-readable output:
node scripts/verify-prereqs.mjs --json
```

See [references/env-and-deps.md](references/env-and-deps.md) for install
instructions per platform and the pinned-version verification note.

## Version and render route

`references/render-workflow.md` owns the pinned CLI invocation/version. Use that pin for
reproducibility; it is not a claim of latest availability. A mismatch requires reporting
installed versus expected version and resolving the invocation, not silently upgrading.
Load that reference for init/edit/preview/lint/check/render. Always pass `check` (which reruns
lint) before render because render depends on valid composition attributes. Reuse successful prerequisite diagnostics
until the environment changes, and stop only preview processes started for this task.

## Composition contract

HyperFrames compositions are plain HTML files. The root carries
`data-composition-id`, `data-start="0"`, `data-width`, `data-height`, and
usually `data-duration`; each timed clip carries `id`, `data-start`, and
`data-duration`. See
[references/composition-basics.md](references/composition-basics.md) for the
full attribute reference and a complete vertical 1080×1920 example.

## Reference material

- [references/heygen-skills.md](references/heygen-skills.md) — the 21 HeyGen
  agent skills this wrapper defers to instead of re-implementing; install
  them using the pinned command in the render-workflow reference when deeper HyperFrames-specific
  expertise (animation, keyframes, captions, product-launch templates, etc.)
  is needed.
- [references/composition-basics.md](references/composition-basics.md) — HTML
  composition attribute contract with a full vertical-preset example.
- [references/render-workflow.md](references/render-workflow.md) — the full
  `init → edit → preview → lint/check → render` flow with every pinned invocation.
- [references/env-and-deps.md](references/env-and-deps.md) — Node/FFmpeg/FFprobe/Chrome
  and HeyGen credential setup per platform.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `command not found: ffmpeg` | Run `node scripts/verify-prereqs.mjs` for the exact remediation for your platform. |
| `npx hyperframes` reports an unknown flag | The pinned version in the render-workflow reference may be behind upstream; run the pinned CLI with `--help` to confirm current flags before updating the pin. |
| `render` fails with a blank/short MP4 | Run `check` first; most render failures are malformed `data-start`/`data-duration`/`data-composition-id` attributes or a missing timeline registration caught by lint/check. |
| Remote/cloud render needed | Configure HeyGen credentials per [references/env-and-deps.md](references/env-and-deps.md), then use `hyperframes cloud render` (a separate top-level command, not a `render` flag) — see [references/render-workflow.md](references/render-workflow.md). |

## See also

- The installed remotion skill (`ak-remotion`) — React-based programmatic
  video generation; use it when the composition is naturally a React
  component tree rather than HTML markup.
- [references/nexu-html-video-alternative.md](references/nexu-html-video-alternative.md)
  — the `nexu-io/html-video` template/Studio CLI, an alternative HTML-to-MP4
  engine; use it only when its template catalog or an existing install fits
  the request better than a HyperFrames composition.
- The ak-motion-graphics skill — router across all in-repo video/motion
  skills plus external motion-skills packs.
