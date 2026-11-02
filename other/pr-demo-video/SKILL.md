---
name: pr-demo-video
description: Record a short demo video of a UI change with Playwright and embed it in the PR description or a PR comment with `gh --attach`. Use when a PR changes something a reviewer should see move, or when the user asks for a demo clip.
---

# PR demo video

Record the flow once with Playwright (video is a config flag, no screen recorder), turn the recording into a small mp4, and upload it straight into the PR body with the GitHub CLI. Nothing is committed to the repo; the clip lives on GitHub's attachment CDN and renders as an inline player.

## When to use

- A PR changes how something looks or moves (new card, animation, multi-step flow, popup) and a still screenshot would not convince a reviewer.
- The user asks to "prove it works" or for a demo of an end-to-end flow.
- Offer it proactively for UI-facing PRs; skip it for pure refactors and backend changes.

## Prerequisites

- `gh` **2.99.0 or newer** (`gh --version`). The `--attach` flag is what uploads media; older versions have no supported upload path.
- Write access to the repo with the token `gh auth login` already holds.
- `ffmpeg` on PATH for the webm → mp4 step (Playwright ships one under `~/.cache/ms-playwright/ffmpeg-*` if the system lacks it).
- Do not run `npm run build`; record against the dev server the E2E harness starts (or the live probe harness for real-container flows).

## 1. Record

Playwright records one `.webm` per page when `video` is on. Use a dedicated config so the recording run never touches the normal suite's settings:

```ts
// playwright.<name>.config.ts
export default defineConfig({
  testDir: './e2e/<where the demo spec lives>',
  workers: 1, retries: 0,
  use: {
    baseURL,
    viewport: { width: 1440, height: 900 },
    video: { mode: 'on', size: { width: 1440, height: 900 } },
    trace: 'retain-on-failure',      // 'on' writes a large zip alongside the video
    screenshot: 'only-on-failure',
  },
})
```

Write the demo as a normal spec, then pace it for a viewer:

- Type with `locator.pressSequentially(text, { delay: 8 })` instead of `fill()` so the prompt is readable.
- Add short pauses at the moments a viewer needs to read (a card appearing, a button about to be clicked). `page.waitForTimeout()` is fine here and only here; put an `eslint-disable-next-line local-rules/no-brittle-playwright-selectors` on it with a comment saying it is pacing, not synchronization. Every real wait still goes through `expect(...).toBeVisible()`.
- Hold 2–3 s on the final state before the test ends, or the video cuts on the last assertion.
- Keep the whole thing under ~60 s. Mock-container flows (`E2E_MOCK=true`) are fast and deterministic; real-container flows go through a live harness (see `e2e/live/mcp-hot-add/run.mjs` for the pattern: seed a data dir, boot the host, run the spec, capture the container log).

Run it and pipe the output through `tee` as usual:

```bash
E2E_MOCK=true npx playwright test --config playwright.<name>.config.ts 2>&1 | tee /tmp/demo-run.txt
```

The recordings land under the config's `outputDir`, in a folder named after the test: `video.webm` for the first page, `video-1.webm` for the second, and so on.

### Popups and second pages

A `window.open` popup (OAuth login, external link) is its own page and gets its own video file. To fold it into one clip, note wall-clock marks in the spec (`Date.now()` at test start, at popup open, at test end), write them to `test.info().outputDir` (create the dir first: Playwright makes it lazily), and overlay the popup recording on the main one. `e2e/live/mcp-hot-add/compose-video.mjs` does exactly that with ffmpeg: it corrects for the main recording starting a few seconds after the test body, crops the popup to its centred content, and places it top-right so it never covers the composer area.

## 2. Convert

GitHub accepts webm, but mp4 plays everywhere and is smaller:

```bash
ffmpeg -y -loglevel error -i video.webm \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 25 -movflags +faststart -an \
  demo.mp4
```

Check the result before uploading: `ffprobe -v error -show_entries format=duration -of csv=p=0 demo.mp4`, and pull a couple of frames (`ffmpeg -ss 12 -i demo.mp4 -frames:v 1 frame.png`) and look at them. A clip that starts on a blank page or ends before the final state is worth re-recording.

Limits: 10 MB for images and GIFs; video is 10 MB on Free plans and 100 MB on paid plans. A 45 s 1440×900 clip at CRF 20 is about 1 MB.

## 3. Upload into the PR

Reference the local file in the PR body markdown and pass the same path to `--attach`. `gh` uploads the file and rewrites the reference in place to a `https://github.com/user-attachments/assets/...` URL, which GitHub renders as an inline player when it sits on its own line.

```markdown
## Demo

One sentence on what the viewer will see, in order.

![Demo](./demo.mp4)
```

```bash
gh pr edit <number> --body-file pr-body.md --attach ./demo.mp4
# or on creation:
gh pr create --title "..." --body-file pr-body.md --attach ./demo.mp4
# or as a comment, e.g. a before/after on a follow-up push:
gh pr comment <number> --body "After the fix:" --attach ./after.mp4
```

Rules that bite:

- **Videos take no alt text.** `--attach './demo.mp4#alt'` fails with `cannot set alt text on video`; the `#alt` suffix is for images only.
- A path not referenced in the body is appended at the end of it. Put the reference where you want the player.
- Match the path string exactly between the body and `--attach` (both relative or both absolute).
- Supported types: png, jpeg, gif, webp, svg, mp4, mov, webm. Nothing else uploads.
- GitHub Enterprise Server is not supported.

Verify the rewrite happened:

```bash
gh pr view <number> --json body --jq .body | grep -n user-attachments
```

## 4. Say what the clip shows

In the PR body, above the player, describe the sequence in one or two sentences and name what the reviewer should notice (the thing that used to be there and is not, or the state that now appears). A video without that line is a puzzle.

## Cleanup

- Recordings, traces and screenshots under `test-results/` are gitignored. Do not commit the mp4 or a GIF of it; the upload is the artefact.
- If the recording came from a live harness that seeded credentials, make sure the harness removed its data dir.
