---
name: github-callout
description: Add an animated GitHub callout to a raw talking-head video with Remotion. When the speaker mentions a GitHub repo, the video cuts to that repo's README in GitHub dark mode. The title blurs in, the README fills in block by block, and a salmon torn-edge highlighter sweeps across the repo name while the camera eases out and back in, then it cuts back to the footage. It takes the raw video file, transcribes it locally to find the callout moments, fetches the README and renders an MP4. Captions are not part of it. Use this whenever the user wants to show, call out, feature or highlight a GitHub repo, README or open-source project inside a video, Reel, TikTok, Short or YouTube video. It also covers requests for a "GitHub overlay", "repo callout", "README pop-up", "show the GitHub page on screen" or "animate a GitHub screenshot", even if they never mention Remotion.
---

> **Video Studio:** how this skill runs here (these lines win over the steps below where they differ).
> - **Project folder:** `projects/remotion/github-callout-<job id or slug>/`, a fresh Remotion project each time as below (`projects/` is never committed). It is its own project, separate from `engines/split-screen`, so it runs whatever `styles/engines.json` says. Run every `npx` command from inside it.
> - **Footage from a studio job:** copy (never move) `jobs/<id>/source.*` into the project's `public/`.
> - **Word timings: never transcribe again.** Convert the job's WhisperX words: `node studio/words-convert.mjs captions projects/<id>/transcript/words.json <project>/public/raw/<slug>.words.json [from] [to]` (from/to in seconds when the project uses a trimmed copy). Skip this skill's own transcription steps. That file is exactly what step 4 would write.
> - **Colour:** the salmon highlighter and GitHub dark mode stay as measured (it has to look like GitHub).
> - **Where it fits:** any style, whenever the speaker names a GitHub repo or open-source tool.
> - **Remotion licence:** free for individuals and companies of up to 3 people; above that it needs a company licence (remotion.dev/license).
> - **Deliver:** copy the rendered MP4 into the job folder (`jobs/<id>/preview.mp4` while reviewing, `final.mp4` when approved) or `outputs/`, and log what was added in `edits.json` so the review page can take notes on it.

# GitHub Callout

This skill turns a raw video into a finished one. Wherever the speaker calls out a GitHub repo, a stylised GitHub overlay pops in over the footage, and the original audio keeps playing underneath.

## The brief

This skill was built from this request, along with 8 screenshots of a reference video:

> Using Remotion best practices, I need help creating a skill that I can give to my Skool community members that specifically helps design this specific style of motion graphics when people call out GitHubs inside of a video. The existing reference images I've given you are a series of screenshots from a full connected video that showcases the motion of a GitHub screenshot that was taken and then animated to look more stylized in the video. Basically, a user could drop in a raw video, and then the parts where they call out the GitHub repo could have an animated section just like this, where this type of overlay pops in, and the animated sections and sequences also pop in. I don't have an existing video file that you can pull this from, but you can use the Eleven Labs connector and use my professional voice clone to create a quick little section that calls out GitHub. That way, you have an audio track to make this too.
>
> However, remember people will be uploading raw video files to create these

Three follow-ups shaped the result:

> the screenshot that's pulled in the video that you're referencing with the screenshots is basically just the GitHub repo homepage, screenshotted in that format.

> this looks great but it needs be a bit slowler and also the highlight needs to be eaiser to see the animation for as it scrolls across the word. The highlight animation at current place is a bit too fast

> For this one, can we actually not include captions in the final skill file? It'll just be the actual GitHub part.

The reference frames show a vertical video, in this order:

1. A near-black GitHub dark page where only the repo title shows, blurred and dim.
2. The title sharpens, then the README paragraphs fill in under it.
3. An install section with a code block appears.
4. A salmon marker with torn edges sweeps left to right behind the title.
5. The whole page pushes in a little.

The reference also has big serif-italic word captions under the page. They are left out on purpose (see the last follow-up).

## How the brief was read

- **"A GitHub screenshot … the repo homepage"**: the overlay is the README panel of the repo's homepage in GitHub's dark theme. It is rebuilt from GitHub's own rendered README HTML (from GitHub's API) styled with GitHub's own dark markdown CSS, rather than a flat image. It looks the same as a screenshot, stays sharp when the camera pushes in, lets each block stagger in, and lets the highlighter sit behind the title text the way a real marker would.
- **"Drop in a raw video"**: the user gives one video file, in any orientation. The output takes its size and length from that file. The overlay cuts in over the footage at each callout and the original audio plays throughout.
- **"The parts where they call out the GitHub repo"**: these are found from a transcript made locally. Claude proposes each callout window and the repo, the user confirms, and then it renders.
- **"Overlay pops in, animated sections pop in"**: the dark page cuts in hard, and then everything inside it animates (title, blocks, highlighter, camera). It cuts out hard too.
- **No captions**: this skill is only the GitHub part. The README stops around 72% of the frame height, as in the reference, so the lower part stays clear for captions the creator adds with another tool.
- **Transcription is still used**, but only to find where each callout starts and ends and when to fire the highlighter. None of the text is shown on screen.
- **The ElevenLabs voice clone** was only used to make a test clip while building this. Users of the skill don't need ElevenLabs.
- **"A bit slower"**: the first version swept the highlighter in 0.5s and filled the README in about 1s. After review, the sweep takes 1.2s at a steady speed, and the reveal and camera run about 60% slower. Keep these timings unless the user asks for a change.

## The look (measured from the reference)

| Element | Spec |
| --- | --- |
| Background | GitHub dark `#0d1117`, full frame, hard cut in and out |
| README | GitHub's rendered README HTML + `github-markdown-dark.css`, in a 450px column scaled 1.6× (vertical) so text wraps like a phone screenshot. It starts at the first heading, skips logo and badge rows, and stops at about 72% of the height (never on a dangling heading). Code blocks get GitHub's copy icon. |
| Opening | Title only, camera at 1.1×. The title fades in over 0.6s and un-blurs from 7px over 0.73s. |
| Fill-in | Blocks after the title fade in, un-blur from 5px and rise 10px. They start at 0.67s, one every 7 frames, 0.6s each. |
| Camera | 1.1× → 1.0× from frame 14 to frame 50, then a slow drift to 1.03× until the highlight, then an ease to 1.09× and 2.5% lower by the end of the callout. |
| Highlighter | `#E08C71` solid block with torn edges (SVG turbulence + displacement) and a dark chipped rim, behind the title text. It sweeps left to right in 36 frames (1.2s), gentle at both ends and steady in the middle. |

## What to ask the user for

1. **The raw video file** (mp4 or mov, vertical or horizontal).
2. **The GitHub repo link(s)** they call out, if they know them. If they don't, find candidates after transcribing and ask them to confirm.

Don't ask about timing or style up front. Propose the callouts after transcribing.

## Workflow

### 1. Set up a fresh Remotion project

Skip this step if the project already exists from an earlier video.

```bash
npx create-video@latest --yes --blank --no-tailwind github-callout
cd github-callout
npm i
npx skills add remotion-dev/skills -a claude-code -y --copy
npx remotion add @remotion/media @remotion/captions mediabunny @remotion/whisper-webgpu @huggingface/transformers @mediabunny/server
npm i github-markdown-css
rm src/Composition.tsx
```

`npx skills add` installs Remotion's official agent skills into the project; follow them when changing anything. Then create the files in step 2.

### 2. Add the files

The project ends up like this:

```
public/raw/            the user's videos + their transcripts
public/github/         one README file per repo
scripts/               transcription helpers (plain Node, no build step)
src/github-callout/    the overlay (shared by every video)
src/videos/            one file per raw video
src/Root.tsx
```

#### `src/github-callout/readme.ts`

Loads the README HTML and splits it into the title and the blocks under it.

```ts
import { useEffect, useState } from "react";
import { useDelayRender } from "remotion";

export type ReadmeContent = {
  // Text of the first heading, drawn by React so the highlighter can sit behind it
  readonly title: string;
  // outerHTML of every top-level block after the title, in order
  readonly blocks: string[];
};

// GitHub's "copy" octicon, shown top-right of code blocks like on github.com
const COPY_BUTTON = `<div class="gc-copy" aria-hidden="true"><svg viewBox="0 0 16 16" width="16" height="16"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></div>`;

// Turns the HTML that GitHub's API returns for a README into a title + blocks.
// Everything before the first heading (logos, badges, notes) is dropped, and so
// are badge-only paragraphs and rules, so the overlay opens on the repo's name.
export const parseReadme = (html: string, repo: string): ReadmeContent => {
  const doc = new DOMParser().parseFromString(html, "text/html");
  const root = doc.querySelector(".markdown-body") ?? doc.body;

  root.querySelectorAll("a.anchor").forEach((a) => a.remove());
  root.querySelectorAll("img").forEach((img) => {
    const src = img.getAttribute("src") ?? "";
    if (src !== "" && !/^(https?:|data:)/.test(src)) {
      img.setAttribute(
        "src",
        `https://github.com/${repo}/raw/HEAD/${src.replace(/^\.?\//, "")}`,
      );
    }
  });
  root
    .querySelectorAll(".highlight, .snippet-clipboard-content")
    .forEach((el) => el.insertAdjacentHTML("beforeend", COPY_BUTTON));

  const children = Array.from(root.children);
  const titleIndex = children.findIndex((el) =>
    el.matches(".markdown-heading, h1, h2, h3"),
  );
  const title =
    titleIndex === -1
      ? (repo.split("/")[1] ?? repo)
      : (children[titleIndex].textContent ?? "").trim();

  const blocks = children
    .slice(titleIndex + 1)
    .filter((el) => {
      if (el.matches("hr")) return false;
      const text = (el.textContent ?? "").trim();
      // Badge rows and logo-only paragraphs have images but no text
      if (text === "" && !el.matches("pre, .highlight, table")) return false;
      return true;
    })
    .map((el) => el.outerHTML);

  return { title, blocks };
};

// Loads a README saved in public/ (or a URL) and holds the render until it is parsed
export const useReadme = (src: string, repo: string) => {
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender(`Loading README ${src}`));
  const [content, setContent] = useState<ReadmeContent | null>(null);

  useEffect(() => {
    fetch(src)
      .then((res) => {
        if (!res.ok) throw new Error(`Could not load ${src} (${res.status})`);
        return res.text();
      })
      .then((html) => {
        setContent(parseReadme(html, repo));
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
  }, [src, repo, handle, continueRender, cancelRender]);

  return content;
};
```

#### `src/github-callout/Highlighter.tsx`

The torn-edge marker.

```tsx
import { useId } from "react";

type Props = {
  // Size of the highlighted text box in layout px (measured, so the edges stay crisp)
  readonly width: number;
  readonly height: number;
  // 0 = nothing drawn, 1 = fully drawn, sweeping left to right
  readonly progress: number;
  readonly color: string;
};

// A solid marker block with torn, speckled edges, drawn behind the text.
// The rough edge is an SVG displacement of a plain rectangle, so the leading
// edge is ragged while it sweeps, like a real brush stroke.
export const Highlighter: React.FC<Props> = ({
  width,
  height,
  progress,
  color,
}) => {
  const id = useId().replace(/:/g, "");
  const padX = height * 0.2;
  const padTop = height * 0.08;
  const padBottom = height * 0.06;
  const w = (width + padX * 2) * progress;
  const h = height + padTop + padBottom;

  if (progress <= 0) {
    return null;
  }

  return (
    <svg
      width={width + padX * 2 + 20}
      height={h + 20}
      style={{
        position: "absolute",
        left: -padX - 10,
        top: -padTop - 10,
        overflow: "visible",
        pointerEvents: "none",
      }}
    >
      <defs>
        <filter id={`${id}-torn`} x="-10%" y="-30%" width="120%" height="160%">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.12"
            numOctaves="2"
            seed="11"
            result="noise"
          />
          <feDisplacementMap
            in="SourceGraphic"
            in2="noise"
            scale="6"
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
        <filter id={`${id}-rim`} x="-10%" y="-30%" width="120%" height="160%">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.12"
            numOctaves="2"
            seed="11"
            result="noise"
          />
          <feDisplacementMap
            in="SourceGraphic"
            in2="noise"
            scale="6"
            xChannelSelector="R"
            yChannelSelector="G"
            result="displaced"
          />
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.3"
            numOctaves="2"
            seed="4"
            result="grain"
          />
          <feColorMatrix
            in="grain"
            type="matrix"
            values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 8 -4"
            result="specks"
          />
          <feComposite in="displaced" in2="specks" operator="in" />
        </filter>
      </defs>
      <rect
        x={10}
        y={10}
        width={w}
        height={h}
        rx={4}
        fill={color}
        filter={`url(#${id}-torn)`}
      />
      <rect
        x={12}
        y={12}
        width={Math.max(0, w - 4)}
        height={h - 4}
        rx={4}
        fill="none"
        stroke="#2b140e"
        strokeWidth={4}
        filter={`url(#${id}-rim)`}
      />
    </svg>
  );
};
```

#### `src/github-callout/GithubCallout.tsx`

The overlay itself: background, camera, README reveal and highlighter.

```tsx
import "github-markdown-css/github-markdown-dark.css";
import "./github-callout.css";
import { useLayoutEffect, useRef, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  staticFile,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
  type InteractivitySchema,
} from "remotion";
import { Highlighter } from "./Highlighter";
import { useReadme } from "./readme";

type Props = {
  // "owner/name", used to fix relative image links in the README
  readonly repo: string;
  // README HTML saved from GitHub's API into public/ (or a full URL)
  readonly readmeSrc: string;
  // Frame (counted from the start of the callout) where the highlighter starts sweeping
  readonly highlightAt: number;
  readonly highlightColor: string;
  readonly style?: React.CSSProperties;
};

// Natural width of the README column in CSS px. 450px wraps text like a phone
// screenshot of the repo page; the column is then scaled up to fill the frame.
const COLUMN_WIDTH = 450;

// How long the highlighter takes to sweep across the title (1.2s at 30fps)
const HIGHLIGHT_FRAMES = 36;

const GithubCalloutInner: React.FC<Props> = ({
  repo,
  readmeSrc,
  highlightAt,
  highlightColor,
  style,
}) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const readme = useReadme(
    /^https?:/.test(readmeSrc) ? readmeSrc : staticFile(readmeSrc),
    repo,
  );

  const columnRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLSpanElement>(null);
  const { delayRender, continueRender } = useDelayRender();
  const [measureHandle] = useState(() => delayRender("Measuring README"));
  const [layout, setLayout] = useState<{
    visibleBlocks: number;
    titleWidth: number;
    titleHeight: number;
  } | null>(null);

  // Vertical video is the reference format. Horizontal video gets a column
  // sized from the height. The README stops around 72% of the height (as in
  // the reference), keeping the lower part clear for the creator's captions.
  const portrait = height >= width;
  const k = portrait ? (1.6 * width) / 1080 : (1.15 * height) / 1080;
  const top = portrait ? 0.105 * height : 0.08 * height;
  const contentBottom = portrait ? 0.72 * height : 0.74 * height;
  const maxColumnHeight = (contentBottom - top) / k;

  // Measure once the README and its images are in: keep only the blocks that
  // fit, and size the highlighter to the title.
  useLayoutEffect(() => {
    if (readme === null || layout !== null) return;
    const column = columnRef.current;
    const title = titleRef.current;
    if (column === null || title === null) return;

    const images = Array.from(column.querySelectorAll("img"));
    Promise.all(
      images.map((img) =>
        img.complete
          ? Promise.resolve()
          : new Promise((resolve) => {
              img.onload = resolve;
              img.onerror = resolve;
            }),
      ),
    ).then(() => {
      const blocks = Array.from(
        column.querySelectorAll<HTMLElement>(":scope > .gc-block"),
      );
      let visibleBlocks = 0;
      for (const block of blocks) {
        if (block.offsetTop + block.offsetHeight > maxColumnHeight) break;
        visibleBlocks++;
      }
      // Never end on a heading with nothing under it
      while (
        visibleBlocks > 0 &&
        blocks[visibleBlocks - 1].querySelector(
          ":scope > .markdown-heading, :scope > h1, :scope > h2, :scope > h3, :scope > h4",
        ) !== null
      ) {
        visibleBlocks--;
      }
      setLayout({
        visibleBlocks,
        titleWidth: title.offsetWidth,
        titleHeight: title.offsetHeight,
      });
      continueRender(measureHandle);
    });
  }, [readme, layout, maxColumnHeight, measureHandle, continueRender]);

  // Keyframes need increasing frames, so keep the sweep after the README has
  // filled in, and finished (with a beat to read it) before the callout ends.
  const hl = Math.min(Math.max(highlightAt, 60), durationInFrames - 50);
  const end = Math.max(durationInFrames, hl + HIGHLIGHT_FRAMES + 1);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1117", ...style }}>
      {/* Camera: opens pushed in on the title, pulls back as the README
          fills in, drifts, then pushes in again after the highlight */}
      <AbsoluteFill
        style={{
          transformOrigin: "50% 0%",
          scale: interpolate(
            frame,
            [0, 14, 50, hl, end],
            [1.1, 1.1, 1, 1.03, 1.09],
            {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.45, 0, 0.25, 1),
            },
          ),
          translate: `0px ${interpolate(
            frame,
            [0, 14, 50, hl, end],
            [-0.039 * height, -0.039 * height, 0, 0, 0.025 * height],
            {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.45, 0, 0.25, 1),
            },
          )}px`,
        }}
      >
        <div
          ref={columnRef}
          className="markdown-body gc-readme"
          style={{
            position: "absolute",
            width: COLUMN_WIDTH,
            left: (width - COLUMN_WIDTH * k) / 2,
            top,
            scale: String(k),
            transformOrigin: "0 0",
          }}
        >
          <div
            className="markdown-heading"
            style={{
              opacity: interpolate(frame, [0, 18], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
              filter: `blur(${interpolate(frame, [0, 22], [7, 0], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.out(Easing.quad),
              })}px)`,
            }}
          >
            <h1 className="heading-element" dir="auto">
              <span
                ref={titleRef}
                style={{
                  position: "relative",
                  display: "inline-block",
                  isolation: "isolate",
                }}
              >
                {layout !== null ? (
                  <span style={{ position: "absolute", inset: 0, zIndex: -1 }}>
                    <Highlighter
                      width={layout.titleWidth}
                      height={layout.titleHeight}
                      color={highlightColor}
                      progress={interpolate(
                        frame,
                        [hl, hl + HIGHLIGHT_FRAMES],
                        [0, 1],
                        {
                          extrapolateLeft: "clamp",
                          extrapolateRight: "clamp",
                          // Gentle at both ends, steady in the middle, so the
                          // sweep can be followed across each word
                          easing: Easing.bezier(0.33, 0, 0.67, 1),
                        },
                      )}
                    />
                  </span>
                ) : null}
                {readme?.title}
              </span>
            </h1>
          </div>
          {readme?.blocks.map((html, i) =>
            layout === null || i < layout.visibleBlocks ? (
              <div
                key={i}
                className="gc-block"
                dangerouslySetInnerHTML={{ __html: html }}
                style={{
                  opacity: interpolate(
                    frame,
                    [20 + i * 7, 38 + i * 7],
                    [0, 1],
                    {
                      extrapolateLeft: "clamp",
                      extrapolateRight: "clamp",
                    },
                  ),
                  filter: `blur(${interpolate(
                    frame,
                    [20 + i * 7, 40 + i * 7],
                    [5, 0],
                    {
                      extrapolateLeft: "clamp",
                      extrapolateRight: "clamp",
                    },
                  )}px)`,
                  translate: `0px ${interpolate(
                    frame,
                    [20 + i * 7, 42 + i * 7],
                    [10, 0],
                    {
                      extrapolateLeft: "clamp",
                      extrapolateRight: "clamp",
                      easing: Easing.bezier(0.16, 1, 0.3, 1),
                    },
                  )}px`,
                }}
              />
            ) : null,
          )}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const githubCalloutSchema = {
  repo: {
    type: "text-content",
    default: "",
    description: "Repo (owner/name)",
  },
  readmeSrc: {
    type: "text-content",
    default: "",
    description: "README file in public/",
  },
  highlightAt: {
    type: "number",
    default: 75,
    min: 0,
    step: 1,
    hiddenFromList: false,
    keyframable: false,
    description: "Highlighter start (frame)",
  },
  highlightColor: {
    type: "color",
    default: "#E08C71",
    description: "Highlighter color",
  },
} as const satisfies InteractivitySchema;

export const GithubCallout = Interactive.withSchema({
  Component: GithubCalloutInner,
  componentName: "<GithubCallout>",
  schema: githubCalloutSchema,
  wrapInSequence: true,
});
```

#### `src/github-callout/github-callout.css`

Small overrides on top of GitHub's dark markdown CSS.

```css
/* github-markdown-dark.css gives the exact GitHub dark README look.
   These overrides adapt it to video. */
.gc-readme.markdown-body {
  background-color: transparent;
}

.gc-readme.markdown-body .markdown-heading h1 {
  margin-top: 0;
}

.gc-readme.markdown-body .highlight,
.gc-readme.markdown-body .snippet-clipboard-content {
  position: relative;
}

/* No scrollbars in a video frame: long code lines are cut off at the edge */
.gc-readme.markdown-body pre {
  overflow: hidden;
  padding-right: 48px;
}

.gc-readme .gc-copy {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-readme .gc-copy svg {
  fill: #9198a1;
}
```

#### `src/github-callout/raw-video-metadata.ts`

Sizes each video composition from its raw file.

```ts
import { ALL_FORMATS, Input, UrlSource } from "mediabunny";
import { staticFile, type CalculateMetadataFunction } from "remotion";

type RawVideoProps = {
  readonly videoSrc: string;
};

// The output takes its size and length from the raw video, so any upload
// (vertical or horizontal) works without editing the composition.
export const rawVideoMetadata: CalculateMetadataFunction<
  RawVideoProps
> = async ({ props }) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(staticFile(props.videoSrc)),
  });
  const [durationInSeconds, videoTrack] = await Promise.all([
    input.computeDuration(),
    input.getPrimaryVideoTrack(),
  ]);
  input.dispose();
  if (videoTrack === null) {
    throw new Error(`${props.videoSrc} has no video track`);
  }

  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
    width: videoTrack.displayWidth,
    height: videoTrack.displayHeight,
  };
};
```

#### `src/videos/MyVideo.tsx`

One file per raw video. This is the worked example from the test clip; replace the video, timings and repo.

```tsx
import { Video } from "@remotion/media";
import {
  AbsoluteFill,
  Composition,
  staticFile,
  useVideoConfig,
} from "remotion";
import { GithubCallout } from "../github-callout/GithubCallout";
import { rawVideoMetadata } from "../github-callout/raw-video-metadata";

type Props = {
  readonly videoSrc: string;
};

// One file like this per raw video. Copy it, rename MyVideo, and write one
// <GithubCallout> node per callout (not a .map()), so each one can be moved,
// trimmed or edited on its own in Remotion Studio.
export const MyVideo: React.FC<Props> = ({ videoSrc }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Video
        name="Raw footage"
        src={staticFile(videoSrc)}
        objectFit="cover"
        premountFor={fps}
        style={{ position: "absolute", width: "100%", height: "100%" }}
      />
      {/* "So, Remotion just put their official agent skills on GitHub ...
          ... render videos with code." (3.87s to 14.30s) */}
      <GithubCallout
        name="GitHub callout: remotion-dev/skills"
        from={116}
        durationInFrames={313}
        premountFor={fps}
        repo="remotion-dev/skills"
        readmeSrc="github/remotion-dev-skills.html"
        highlightAt={91}
        highlightColor="#E08C71"
      />
    </AbsoluteFill>
  );
};

export const MyVideoComposition: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={516}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{ videoSrc: "raw/my-video.mp4" }}
      calculateMetadata={rawVideoMetadata}
    />
  );
};
```

#### `src/Root.tsx`

Registers each video, plus the callout on its own for previewing.

```tsx
import { Composition, Folder } from "remotion";
import { GithubCallout } from "./github-callout/GithubCallout";
import { MyVideoComposition } from "./videos/MyVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* One line per raw video */}
      <MyVideoComposition />
      {/* The callout on its own, to preview and tweak the look in Studio */}
      <Folder name="Scenes">
        <Composition
          id="GithubCallout"
          component={GithubCallout}
          durationInFrames={240}
          fps={30}
          width={1080}
          height={1920}
          defaultProps={{
            repo: "remotion-dev/skills",
            readmeSrc: "github/remotion-dev-skills.html",
            highlightAt: 75,
            highlightColor: "#E08C71",
          }}
        />
      </Folder>
    </>
  );
};
```

#### `scripts/transcribe.mjs`

Local Whisper transcription (Remotion's official recipe).

```js
// Transcribes a raw video (or audio) file to word-level timings with Whisper,
// running locally on the GPU. The timings are used to place each GitHub
// callout and its highlight. Adapted from Remotion's official recipe
// (remotion-captions/transcribe-captions.md) to plain JavaScript so it runs on
// any recent Node version.
// Usage: node scripts/transcribe.mjs public/raw/my-video.mp4
// Writes the word timings next to the video as my-video.words.json
import { registerMediabunnyServer } from "@mediabunny/server";
import {
  WHISPER_WEBGPU_SAMPLE_RATE,
  canUseWhisperWebGpu,
  disposeWhisperModel,
  downloadWhisperModel,
  loadWhisperModel,
  toCaptions,
  transcribe,
} from "@remotion/whisper-webgpu";
import {
  ALL_FORMATS,
  Conversion,
  FilePathSource,
  Input,
  NullTarget,
  Output,
  WavOutputFormat,
} from "mediabunny";
import { writeFile } from "node:fs/promises";

const inputPath = process.argv[2];
if (!inputPath) {
  throw new Error(
    "Pass the video path, e.g. node scripts/transcribe.mjs public/raw/my-video.mp4",
  );
}
const outputPath = inputPath.replace(/\.[^.]+$/, "") + ".words.json";

registerMediabunnyServer();

const support = await canUseWhisperWebGpu();
if (!support.supported) {
  throw new Error(support.detailedReason);
}

// Decode the audio track to a 16kHz mono waveform
const chunks = [];
const input = new Input({
  formats: ALL_FORMATS,
  source: new FilePathSource(inputPath),
});
try {
  const audioTrack = await input.getPrimaryAudioTrack();
  if (audioTrack === null) {
    throw new Error("The media does not contain an audio track.");
  }

  const conversion = await Conversion.init({
    input,
    output: new Output({
      format: new WavOutputFormat(),
      target: new NullTarget(),
    }),
    video: { discard: true },
    audio: (track) => {
      if (track.id !== audioTrack.id) {
        return { discard: true };
      }

      return {
        codec: "pcm-f32",
        forceTranscode: true,
        numberOfChannels: 1,
        sampleFormat: "f32",
        sampleRate: WHISPER_WEBGPU_SAMPLE_RATE,
        process: (sample) => {
          const waveform = new Float32Array(
            sample.allocationSize({ format: "f32", planeIndex: 0 }) /
              Float32Array.BYTES_PER_ELEMENT,
          );
          sample.copyTo(waveform, { format: "f32", planeIndex: 0 });
          chunks.push({
            startFrame: Math.round(
              sample.timestamp * WHISPER_WEBGPU_SAMPLE_RATE,
            ),
            waveform,
          });
          return sample;
        },
      };
    },
  });

  if (!conversion.isValid) {
    throw new Error("The audio track cannot be decoded.");
  }

  await conversion.execute();
} finally {
  input.dispose();
}

const waveformLength = chunks.reduce(
  (max, chunk) => Math.max(max, chunk.startFrame + chunk.waveform.length),
  0,
);
const channelWaveform = new Float32Array(waveformLength);
for (const chunk of chunks) {
  const destinationStart = Math.max(0, chunk.startFrame);
  const sourceStart = Math.max(0, -chunk.startFrame);
  const availableLength = Math.min(
    chunk.waveform.length - sourceStart,
    channelWaveform.length - destinationStart,
  );

  if (availableLength > 0) {
    channelWaveform.set(
      chunk.waveform.subarray(sourceStart, sourceStart + availableLength),
      destinationStart,
    );
  }
}

// small.en is the recommended English model. For other languages use "small"
// and pass `language` to transcribe().
const model = "small.en";
await downloadWhisperModel({ model });
await loadWhisperModel({ model });
let captions;
try {
  const transcription = await transcribe({ channelWaveform, model });
  captions = toCaptions({ whisperWebGpuOutput: transcription }).captions;
} finally {
  await disposeWhisperModel({ model });
}

await writeFile(outputPath, JSON.stringify(captions, null, 2));
console.log(`Wrote ${captions.length} words to ${outputPath}`);
```

#### `scripts/print-transcript.mjs`

Prints the transcript one word per line with its time and frame.

```js
// Prints a transcript one word per line with its time, to find where each
// GitHub callout starts and ends and the frame to fire the highlighter on.
// Usage: node scripts/print-transcript.mjs public/raw/my-video.words.json
import { readFile } from "node:fs/promises";

const file = process.argv[2];
if (!file) {
  throw new Error(
    "Usage: node scripts/print-transcript.mjs public/raw/my-video.words.json",
  );
}

const words = JSON.parse(await readFile(file, "utf8"));
for (const w of words) {
  const seconds = (w.startMs / 1000).toFixed(2).padStart(7);
  const frame = String(Math.round((w.startMs / 1000) * 30)).padStart(6);
  console.log(`${seconds}s  frame ${frame}  ${w.text.trim()}`);
}
```

#### `scripts/srt-to-words.mjs`

Fallback when Whisper can't run: turns an .srt into word timings.

```js
// Fallback when local Whisper can't run: turns an .srt exported from any editor
// (CapCut, Premiere, Descript, YouTube...) into word timings. Each subtitle's
// time is shared across its words by length, which is close enough to place a
// callout and its highlight.
// Usage: node scripts/srt-to-words.mjs public/raw/my-video.srt
// Writes public/raw/my-video.words.json (same format as transcribe.mjs)
import { parseSrt } from "@remotion/captions";
import { readFile, writeFile } from "node:fs/promises";

const srtPath = process.argv[2];
if (!srtPath) {
  throw new Error(
    "Usage: node scripts/srt-to-words.mjs public/raw/my-video.srt",
  );
}
const outputPath = srtPath.replace(/\.[^.]+$/, "") + ".words.json";

const { captions: cues } = parseSrt({ input: await readFile(srtPath, "utf8") });
const words = [];
for (const cue of cues) {
  const parts = cue.text.split(/\s+/).filter((w) => w !== "");
  const totalLetters = parts.reduce((sum, w) => sum + w.length, 0);
  let t = cue.startMs;
  for (const word of parts) {
    const d = ((cue.endMs - cue.startMs) * word.length) / totalLetters;
    words.push({
      text: ` ${word}`,
      startMs: Math.round(t),
      endMs: Math.round(t + d),
      timestampMs: Math.round(t + d / 2),
      confidence: null,
    });
    t += d;
  }
}

await writeFile(outputPath, JSON.stringify(words, null, 2));
console.log(`Wrote ${words.length} words to ${outputPath}`);
```

### 3. Bring in the raw video

Copy (never move or edit) the user's file to `public/raw/<slug>.mp4`, where the slug is lowercase with hyphens, e.g. `public/raw/repo-review.mp4`. Keep the original extension if it's `.mov`.

### 4. Transcribe it locally

```bash
node scripts/transcribe.mjs public/raw/<slug>.mp4
```

This writes `public/raw/<slug>.words.json` with word-level timings. The first run downloads the Whisper model once, which takes a minute. After that, a short clip takes seconds. Print the transcript one word per line, with seconds and the matching frame at 30fps:

```bash
node scripts/print-transcript.mjs public/raw/<slug>.words.json
```

If `transcribe.mjs` stops with a WebGPU / unsupported-GPU message, ask the user to export subtitles as an `.srt` from their editor (CapCut, Premiere, DaVinci, Descript, YouTube Studio…). Put it at `public/raw/<slug>.srt` and run:

```bash
node scripts/srt-to-words.mjs public/raw/<slug>.srt
```

That writes the same `<slug>.words.json`, with word times spread across each subtitle line.

### 5. Find the callouts and confirm them

Read the transcript and mark every place the speaker introduces a GitHub repo. For each one, decide:

- **Start**: the first word of the sentence that introduces the repo ("So somebody on GitHub…", "This repo…"). Start 1 to 3 frames before that word's `startMs`.
- **End**: the end of the last sentence that is still about the repo (what it does, how to install it). Cut back to the footage before the speaker moves on (price, call to action, next topic).
- **Length**: 4 to 12 seconds. The overlay needs about 2s to fill in, 1.2s to highlight and a beat to read. If a mention is shorter than 4s, extend it to the end of the sentence. If there's nothing to extend into, tell the user it's too short for this effect.
- **Highlight frame** (`highlightAt`, counted from the callout's first frame): when the speaker names the repo or says where it lives ("…on GitHub", the project name). It must be at least 60 frames in and 50 before the end, and the component clamps it into that range.
- **Repo**: the `owner/name`. If the user didn't give a link, search and suggest:
  `curl -s "https://api.github.com/search/repositories?q=<spoken+name>&per_page=5"`.

Show the user a short table before building, and wait for a yes or for corrections:

| # | From → to | What's said | Repo | Highlight on |
| --- | --- | --- | --- | --- |
| 1 | 3.87s → 14.30s | "So, Remotion just put their official agent skills on GitHub … render videos with code." | remotion-dev/skills | "GitHub" (6.90s) |

Frames are at 30fps: `from = Math.round(startSeconds * 30)`, which `print-transcript.mjs` already shows next to each word.

### 6. Fetch each README

```bash
curl -sL -H "Accept: application/vnd.github.html+json" https://api.github.com/repos/OWNER/REPO/readme -o public/github/OWNER-REPO.html
head -c 120 public/github/OWNER-REPO.html
```

A good file starts with `<div id="readme"`. If it's JSON saying `Not Found`, the name is wrong or the repo is private. For a private repo, ask the user to paste the README text into `public/github/OWNER-REPO.md`, then render it with GitHub's markdown endpoint:

```bash
node -e 'const fs=require("fs");fs.writeFileSync("md.json",JSON.stringify({text:fs.readFileSync("public/github/OWNER-REPO.md","utf8"),mode:"gfm",context:"OWNER/REPO"}))'
curl -sL -X POST -H "Accept: application/vnd.github+json" https://api.github.com/markdown -d @md.json -o public/github/OWNER-REPO.html && rm md.json
```

Anonymous GitHub API calls are limited to 60 an hour. If that limit is hit and the GitHub CLI is logged in, use `gh api repos/OWNER/REPO/readme -H "Accept: application/vnd.github.html+json" > public/github/OWNER-REPO.html`.

### 7. Write the video file

Copy `src/videos/MyVideo.tsx` to `src/videos/<Name>.tsx`. Then:

- rename `MyVideo`;
- set `defaultProps.videoSrc`;
- add the composition to `src/Root.tsx`;
- write one `<GithubCallout>` per confirmed callout, with `from`, `durationInFrames`, `repo`, `readmeSrc` and `highlightAt`. Put the spoken lines above it as a comment.

Point the `GithubCallout` composition in Root at the first repo's README so it previews in Studio.

### 8. Check, then render

```bash
npx tsc --noEmit && npx eslint src
```

For each callout, render stills and look at them:

- just before the callout
- 10 frames in (title only)
- `from + 60` (README filled in)
- `from + highlightAt + 18` (mid-sweep)
- the callout's last frame
- just after it (footage back)

Check that:

- the README ends with clear space below it;
- the highlighter sits behind the title text;
- the footage returns.

```bash
npx remotion still <Name> out/check.png --frame=<frame>
```

Then render the video:

```bash
npx remotion render <Name> out/<slug>-github-callout.mp4
```

To show the user an interactive preview first, run `npx remotion studio`. The callout scene is also registered on its own under "Scenes".

Finish by telling the user the output path and each callout's time range, and offer to adjust a window, the highlight moment or the repo.

## Tweaks users ask for

- **Different highlight colour**: `highlightColor` on the callout.
- **Faster or slower sweep**: `HIGHLIGHT_FRAMES` in `GithubCallout.tsx`. The reveal speed is the `20 + i * 7` / `38 + i * 7` keyframes on the blocks.
- **Highlight a different moment**: change `highlightAt`.
- **Horizontal video**: works as is. The column is sized from the height, and the README trims itself to fit.
- **Captions**: not part of this skill. Add them afterwards with a separate captions tool or skill. The lower part of the frame is left clear for them.

## Lessons from building it

- `useVideoConfig().durationInFrames` inside the callout is the callout's own length, because it's wrapped in a sequence. That's what the closing push-in keys off.
- The README is measured only after its images load. Blocks past about 72% of the height are dropped, and so is a heading left with nothing under it.
- The highlighter is drawn at the measured size of the title in layout pixels. Stretching one SVG with `preserveAspectRatio="none"` smears the torn edges.
- `@remotion/rough-notation` (Remotion's usual highlighter) draws sketchy pen strokes. The reference is a solid block with torn edges, so this skill draws its own SVG.
- The first transcription downloads the model. Later runs on the same machine are fast. Whisper sometimes slips on names ("ReMotion"); that doesn't matter here because nothing from the transcript appears on screen.
- An early version also rebuilt the reference's serif-italic captions. They were removed at the user's request so the skill does one job.
- Remotion's bundled ffmpeg has no `select` filter. To grab a frame from a rendered MP4, seek instead: `npx remotion ffmpeg -ss <seconds> -i out/video.mp4 -frames:v 1 frame.png`.
- The scripts are plain `.mjs` so they run without TypeScript tooling on any recent Node.

### How it was tested

1. A 17.2s test line was generated in a cloned voice (ElevenLabs, Eleven v4) and wrapped into a stand-in 1080×1920 "raw video".
2. `transcribe.mjs` found all 52 words.
3. One callout was confirmed: 3.87s → 14.30s, `remotion-dev/skills`, highlight on "GitHub".
4. The render came out as 1080×1920 with the original audio, cutting back to the footage on "It's completely free."
5. A 1920×1080 still checked the horizontal layout.
6. The pasted-README route and the `.srt` route were each run once. The `.srt` word times landed within 0.21s of Whisper's.
7. Windows was not tested.
