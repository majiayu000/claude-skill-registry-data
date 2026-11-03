---
name: glow-intro-caption
description: Add a two-line stylistic intro title, and the camera move that goes with it, to the opening of a talking-head video with Remotion, in a style measured frame by frame from a finance short. A white setup line sits over a red punch line ("ARE WE FACING A / BEAR MARKET?") in Montserrat Black at fixed reference sizes, with a soft pink-white glow. The facecam and the title open punched in 25% and pull back together on one exponential curve, with a few frames of zoom blur at the start, while the title fades up. Use this whenever the user wants an intro caption, hook title, opening headline or title overlay on a Reel, TikTok, Short or vertical video, wants "the glowing two-line intro text" or the zoom-out intro, wants a stylised question or hook on screen at the start, or names this style, even if they never mention Remotion.
---

> **Video Studio:** how this skill runs here (these lines win over the steps below where they differ).
> - **Project folder:** `projects/remotion/glow-intro-caption-<job id or slug>/`, a fresh Remotion project each time as below (`projects/` is never committed). It is its own project, separate from `engines/split-screen`, so it runs whatever `styles/engines.json` says. Run every `npx` command from inside it.
> - **Footage from a studio job:** copy (never move) `jobs/<id>/source.*` into the project's `public/`.
> - **Colour:** line 2 (the punch line) uses the brand purple (`styles/brand.json` accent #8B5CF6, glow from accentLight #C4B5FD) instead of the reference red, unless Bryan asks for the original red.
> - **The title:** a hook about the video's topic, from the Content OS script's `[HOOK]` line when there is one (Notion page body), written in the 14-16 / 10-12 character pattern below.
> - **Where it fits:** the opening 3-5 s of any 9:16 talking-head style. Render the intro section here and splice it onto the rest of the edit, or build the whole edit in this project.
> - **Remotion licence:** free for individuals and companies of up to 3 people; above that it needs a company licence (remotion.dev/license).
> - **Deliver:** copy the rendered MP4 into the job folder (`jobs/<id>/preview.mp4` while reviewing, `final.mp4` when approved) or `outputs/`, and log what was added in `edits.json` so the review page can take notes on it.

# Glow intro caption

A two-line hook title over the first few seconds of a vertical talking-head video, plus the intro camera move. The white top line sets up the question and the red bottom line lands it.

Everything moves as one shot. The facecam and the title both open punched in 25%, then pull back together on the same curve, pivoting at a point a third of the way down the frame. The first few frames ghost with zoom blur while the move is fastest, the title fades up over about 0.6 s, and the whole thing is still gently settling seconds later.

The words are a stylistic choice, a headline for the video's topic. They are **not** a transcript of what the speaker says. The reference also had an animated stock-chart panel under the text. That is a separate graphic and not part of this skill.

## The original brief

> I want to create an intro caption animation based on the style, study of motion, and overall design and aesthetic that's present in this folder. Using Remotion best practices, help me create a dynamic skill file that can create these intro caption overlays in the style of the motion that's presented in the series of screenshots that showcases how this works and what it looks like. Make sure to identify the font being used as well as the movement. And also the subtle glow effect that the text has as well to test your capability, use this raw clip that I have for the intro so you can edit it. You don't need to use the whole clip.

Inputs were a folder of 69 PNG frames from the reference (720x1280, 23.976 fps, about 2.9 s, with a `timestamps.csv`) and `RAW.mp4`, a 56.5 s, 1080x1920, 30 fps talking-head clip.

How each part of the brief was read, including the review rounds:

- **"Intro caption overlays"**: one two-line title (white setup line, red punch line), not word-by-word captions. The chart panel in the reference was left out.
- **"Dynamic"**: any two lines of text, any accent colour, any resolution. Every size, gap and glow value is relative to the frame or the font size.
- **"Identify the font"**: Montserrat Black (900). See "How the look was measured".
- **"The movement"**: measured from the frames and fitted to curves, not eyeballed.
- **"Subtle glow"**: a tight bloom plus two wide hazes.
- **Review round 1.** The first version wrote the title from the speaker's own hook, fitted both lines to one width, and added an embossed bevel. The user's feedback:
  - The bevel isn't needed, so it was removed.
  - Size and placement drifted from the reference, so sizes are now **fixed** at the reference values.
  - The text should be "a stylistic kind of choice", not the spoken words, so headlines are now written as titles.
- **Review round 2.** The user noticed that "there's some zooming and effects going on in the raw video facecam itself as well". Tracking the reference's background showed the footage zooming out on the same curve, around the same point, as the title, with zoom blur on the first few frames and no colour or exposure change. That camera move is now part of the style, and the title and footage share one curve.
- **"You don't need to use the whole clip"**: the test edit is the first 7.7 s, with the title on screen for 0–4 s.

## The style spec

All values are at rest (scale 1). Sizes are shares of the frame, so it works at any resolution.

| Element | Value |
|---|---|
| Font | Montserrat Black 900, uppercase, letter-spacing 0 at rest (`@remotion/google-fonts/Montserrat`) |
| Setup line size | **8.02% of frame width** (font size) |
| Punch line size | **9.28% of frame width** (font size), about 1.16x the setup line |
| Overflow guard | A line shrinks only if it would be wider than 80% of the frame at rest. The reference lines are both 79% |
| Line boxes | `line-height: 0.7` (Montserrat cap height), so each box hugs the caps |
| Gap between lines | 0.07 × punch font size |
| Placement | Centred horizontally; block centre at **58% of frame height** at rest |
| Setup line colour | Near-white with a faint pink cast: gradient `#FFF8FB → #FFF1F6 → #FFEBF1` from cap top to baseline |
| Punch line colour | `#DE1832`: 3% lighter at the cap top, 6% darker at 68%, 13% darker at the baseline |
| Glow | `0 0 0.15em` at 0.2 alpha + `0 0 1.1em` at 0.6 + `0 0 2.2em` at 0.6 (setup line) or 0.25 (punch line). Setup glow colour is `rgb(255,232,242)`; punch glow is the accent tinted 15% toward white. Both glows paint under both lines. |
| Dark grade | A bottom gradient (clear at 30% of frame height → 0.6 at 48% → 0.82 at 62% → 0.92 at the bottom) × `scrim` 0.8. It keeps the glow readable on bright footage. The reference footage was already dark there. |

### Motion

| Channel | Curve |
|---|---|
| Camera (footage **and** title) | `scale(t) = 1 + 0.0463·e^(−t/0.070 s) + 0.2038·e^(−t/1.11 s)`: 1.25 at the start, ~1.13 at 0.5 s, ~1.016 at 2.8 s, settled by ~6 s |
| Pivot | `transform-origin: 50% 31.6%` of the frame for both layers, so everything drifts **up** as it shrinks |
| Footage zoom blur | Radial blur centred on the pivot, sized to how far the image moved during the half frame **before** each frame (a trailing 180° shutter). Frame 0 is sharp; frames 1–4 ghost by a few px; it is gone by ~frame 10. |
| Title tracking | +0.035 em → 0 on the camera curve |
| Title opacity in | `1 − e^(−t/0.17 s)`: ~28% on the first visible frame, ~85% at 0.37 s, solid by ~0.65 s |
| Grade in | 0 → 1 over 0.3 s, ease-out |
| Footage colour | Unchanged: no exposure, saturation or colour shifts in the reference |
| Title exit (not in the reference, designed to match) | Text fades out over the last 0.25 s (ease-in), the grade over the last 0.3 s. The camera keeps settling. |

There is no bounce, no overshoot and no per-word stagger.

## Workflow

### 1. Scaffold a fresh Remotion project

Always start from a fresh scaffold. Don't reuse other projects on the machine.

```bash
npx create-video@latest --yes --blank --no-tailwind intro-caption
cd intro-caption
npx skills add remotion-dev/skills -a claude-code -y --copy
npx remotion add @remotion/google-fonts @remotion/media @remotion/layout-utils @remotion/effects
```

Read the installed `remotion-best-practices` skill (it routes to `remotion-markup`, `remotion-interactivity`, `google-fonts.md`, `measuring-text.md` and `effects.md`) and follow it. The code below uses inline `interpolate()` styles, `scale`/`translate` properties, `premountFor={fps}`, an `effects` array on `<Video>`, and `Interactive.withSchema({ wrapInSequence: true })` registered as a connected composition.

`zoomBlur()` needs WebGL during renders, so add the last line of this `remotion.config.ts`:

```ts
/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// zoomBlur() from @remotion/effects needs WebGL during renders.
Config.setChromiumOpenGlRenderer("angle");
```

### 2. Bring in the clip and probe it

`ffmpeg` may not be on PATH. Use Remotion's bundled copies:

```bash
cp /path/to/video.mp4 public/RAW.mp4
npx remotion ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration -of compact public/RAW.mp4
```

Match the composition to the clip (here: 1080x1920, 30 fps). The camera move scales the footage up to 1.25x and settles at exactly 1x, so the footage must fill the frame at 1x (`objectFit="cover"`). It never shows an edge.

### 3. Write the title

This is a stylistic headline about the video's topic, the way a thumbnail title is. It is not a quote of the speaker. Use the user's text if they give it. Otherwise write it from the topic: ask in one line if the topic isn't known, and offer two or three options.

The reference pattern is "ARE WE FACING A / BEAR MARKET?":

- **Line 1 (white)**: the setup, usually the start of a question. Aim for **~14–16 characters** including spaces, e.g. "ARE WE FACING A", "IS AI GOING FULL", "IS THIS THE END OF".
- **Line 2 (accent)**: the topic or the punch, ending in "?". Aim for **~10–12 characters**, e.g. "BEAR MARKET?", "SWARM MODE?", "SOLO AGENTS?".
- Those lengths are what make both lines land at ~75–80% of the frame width at the reference sizes, which is what makes the block look like the reference. A longer line gets shrunk by the overflow guard (so it looks smaller than the reference). A much shorter one leaves the block lopsided. Montserrat Black is wide, so count characters.
- Measured widths at rest, as a share of frame width:

  | Line | Width |
  |---|---|
  | ARE WE FACING A (line 1) | 0.79 |
  | IS AI GOING FULL (line 1) | 0.74 |
  | IS THIS THE END OF (line 1) | 0.85, shrinks 6% |
  | ARE YOU READY FOR (line 1) | 0.92, too long |
  | BEAR MARKET? (line 2) | 0.79 |
  | SWARM MODE? (line 2) | 0.80 |
  | SOLO AGENTS? (line 2) | 0.77 |
  | AGENT SWARMS? (line 2) | 0.90, too long |

  If unsure, render a still and check.
- For RAW.mp4 (a video about AI agent swarms) the title was **IS AI GOING FULL / SWARM MODE?**: on topic, without quoting the speaker.

### 4. Time it

- The camera move and the title both start at frame 0 of the video.
- The title holds for **~3–5 s**; the default is 4 s. The reference was on screen for at least 2.9 s. The fade-out lives inside the title's last 0.25 s, so set `durationInFrames` to where it should be fully gone.
- The camera move doesn't end with the title. It keeps settling (to within 0.6% by 4 s), so the footage after the title never jumps.
- Cut the video wherever suits the edit. The test cut runs 7.7 s to the end of the speaker's first sentence.

### 5. The shared camera move: `src/introMotion.ts`

```ts
// The intro's camera move, fitted to the reference by tracking its background frame by frame.
// The footage and the title zoom out together on one curve, like a single camera pulling back:
//   scale(t) = 1 + 0.0463 * e^(-t / 0.070s) + 0.2038 * e^(-t / 1.11s)
// A fast component gives the jump in the first few frames, a slow one the long settle.
// Both layers scale about the same point: centred, 31.6% down the frame.

const FAST_AMP = 0.0463;
const FAST_SECONDS = 0.07;
const SLOW_AMP = 0.2038;
const SLOW_SECONDS = 1.11;

export const ZOOM_START = 1 + FAST_AMP + SLOW_AMP; // 1.25
export const ZOOM_WINDOW = 6; // seconds the move is spread over (it is 99.9% settled by then)
export const ZOOM_ORIGIN = "50% 31.6%";
export const ZOOM_CENTER: [number, number] = [0.5, 0.316];

// Remaining zoom above 1 at time t (seconds).
const excess = (t: number) =>
  FAST_AMP * Math.exp(-t / FAST_SECONDS) + SLOW_AMP * Math.exp(-t / SLOW_SECONDS);

// Easing for interpolate(frame, [0, ZOOM_WINDOW * fps], [ZOOM_START, 1]).
export const zoomEase = (p: number) =>
  (ZOOM_START - 1 - excess(p * ZOOM_WINDOW)) / (ZOOM_START - 1 - excess(ZOOM_WINDOW));

// Scale at time t; the shot holds still before the move starts.
const scaleAt = (t: number) => 1 + excess(Math.max(0, t));

// Zoom blur for the footage: the share of each pixel's distance to the zoom centre that the
// image travelled during the half frame before this one (a 180-degree shutter trailing the
// motion). Frame 0 stays sharp, the next few frames ghost, and it fades as the move slows,
// which is what the reference shows.
export const zoomBlurShare = (frame: number, fps: number) => {
  const t = frame / fps;
  return (scaleAt(t - 0.5 / fps) - scaleAt(t)) / scaleAt(t);
};
```

### 6. The title: `src/IntroCaption.tsx`

```tsx
import type React from "react";
import { useEffect, useMemo, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
  type InteractivitySchema,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { measureText } from "@remotion/layout-utils";
import { ZOOM_ORIGIN, ZOOM_START, ZOOM_WINDOW, zoomEase } from "./introMotion";

// Montserrat Black, matched to the reference: its horizontal strokes are 0.25 of the cap
// height (ExtraBold is 0.22), and the glyph proportions line up letter for letter.
const { fontFamily, waitUntilDone } = loadFont("normal", {
  weights: ["900"],
  subsets: ["latin"],
});
const FONT_WEIGHT = "900";

// Montserrat's cap height is 0.70em. A 0.7 line-height makes each line box hug the
// caps, so the measured gap between the two lines can be applied directly.
const CAP = 0.7;

// Type sizes measured on the reference, as a share of frame width (at rest).
// They are fixed so the caption looks the same size whatever the words are.
const SETUP_SIZE = 0.0802;
const PUNCH_SIZE = 0.0928;
// A line only shrinks if it would be wider than this at rest (the reference lines
// are 0.79). At the 1.2x start scale this still leaves a margin at the frame edges.
const MAX_LINE_WIDTH = 0.8;

// Exponential ease-out normalised to [0, 1]: k is the time constant as a share of the
// interpolate() range.
const expoOut = (k: number) => (p: number) => (1 - Math.exp(-p / k)) / (1 - Math.exp(-1 / k));

// Opacity was fitted to the reference frame by frame: opacity(t) = 1 - e^(-t / 0.17s).
// The scale is the shared camera move in introMotion.ts.
const FADE_SECONDS = 0.17;
const FADE_WINDOW = 0.8;
const fadeIn = expoOut(FADE_SECONDS / FADE_WINDOW);

type IntroCaptionProps = {
  readonly line1: string;
  readonly line2: string;
  readonly accentColor: string;
  readonly textScale: number;
  readonly centerY: number;
  readonly glow: number;
  readonly scrim: number;
  readonly style?: React.CSSProperties;
};

type LineLook = {
  readonly text: string;
  readonly fontSize: number;
  readonly fill: string; // vertical gradient for the letter faces
  readonly solid: string; // flat colour under the glow
  readonly glowRgb: string;
  readonly widest: number; // alpha of the 2.2em haze
};

// A tight bloom plus two wide hazes. The haze is the look: in the reference it lifts the
// background by ~+46 at the letter edge, ~+31 at 0.4em and is still ~+12 a full em away.
// The accent line gets less of the widest haze, so the area above the white line stays
// neutral as it does in the reference.
const glowShadow = (rgb: string, strength: number, widest: number) =>
  [
    `0 0 0.15em rgba(${rgb}, ${Math.min(1, 0.2 * strength)})`,
    `0 0 1.1em rgba(${rgb}, ${Math.min(1, 0.6 * strength)})`,
    `0 0 2.2em rgba(${rgb}, ${Math.min(1, widest * strength)})`,
  ].join(", ");

const Line: React.FC<{
  readonly look: LineLook;
  readonly pass: "glow" | "face";
  readonly glow: number;
}> = ({ look, pass, glow }) => (
  <div
    style={{
      display: "grid",
      justifyItems: "center",
      fontSize: look.fontSize,
      lineHeight: CAP,
      whiteSpace: "nowrap",
    }}
  >
    {pass === "glow" ? (
      <span style={{ color: look.solid, textShadow: glowShadow(look.glowRgb, glow, look.widest) }}>
        {look.text}
      </span>
    ) : (
      // Gradient clipped to the glyphs. Padding keeps overshoot and punctuation inside
      // the painted box; the gradient stops (21% to 79%) land on cap top and baseline.
      <span
        style={{
          padding: "0.25em 0.1em",
          margin: "-0.25em -0.1em",
          color: "transparent",
          backgroundImage: look.fill,
          backgroundClip: "text",
          WebkitBackgroundClip: "text",
        }}
      >
        {look.text}
      </span>
    )}
  </div>
);

// Defaults keep the component rendering if a field is cleared in Studio's props editor.
const IntroCaptionInner: React.FC<IntroCaptionProps> = ({
  line1 = "",
  line2 = "",
  accentColor = "#DE1832",
  textScale = 1,
  centerY = 0.58,
  glow = 1,
  scrim = 0.8,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();

  // measureText needs the real font metrics, so hold the render until Montserrat is in.
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Loading Montserrat"));
  const [fontReady, setFontReady] = useState(false);
  useEffect(() => {
    waitUntilDone()
      .then(() => {
        setFontReady(true);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
  }, [handle, continueRender, cancelRender]);

  const top = line1.toUpperCase();
  const bottom = line2.toUpperCase();

  // Reference sizes, shrunk only when a line would run wider than MAX_LINE_WIDTH.
  const sizes = useMemo(() => {
    if (!fontReady) return { s1: 0, s2: 0 };
    const sized = (text: string, share: number) => {
      const fontSize = share * textScale * width;
      if (!text) return fontSize;
      const measured = measureText({ text, fontFamily, fontWeight: FONT_WEIGHT, fontSize }).width;
      return fontSize * Math.min(1, (MAX_LINE_WIDTH * width) / measured);
    };
    return { s1: sized(top, SETUP_SIZE), s2: sized(bottom, PUNCH_SIZE) };
  }, [fontReady, top, bottom, textScale, width]);

  const lines: LineLook[] = [];
  if (top) {
    lines.push({
      text: top,
      fontSize: sizes.s1,
      fill: "linear-gradient(180deg, #FFF8FB 21%, #FFF1F6 50%, #FFEBF1 79%)",
      solid: "#FFF1F6",
      glowRgb: "255, 232, 242",
      widest: 0.6,
    });
  }
  if (bottom) {
    lines.push({
      text: bottom,
      fontSize: sizes.s2,
      fill: `linear-gradient(180deg, ${tint(accentColor, 0.03)} 21%, ${accentColor} 50%, ${shade(accentColor, -0.06)} 68%, ${shade(accentColor, -0.13)} 79%)`,
      solid: accentColor,
      glowRgb: hexToRgb(tint(accentColor, 0.15)),
      widest: 0.25,
    });
  }

  const block = (pass: "glow" | "face") => (
    <div
      style={{
        gridArea: "1 / 1",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 0.07 * PUNCH_SIZE * textScale * width,
        letterSpacing: `${interpolate(frame, [0, ZOOM_WINDOW * fps], [0.035, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: zoomEase,
        })}em`,
      }}
    >
      {lines.map((look, i) => (
        <Line key={i} look={look} pass={pass} glow={glow} />
      ))}
    </div>
  );

  return (
    <AbsoluteFill style={{ pointerEvents: "none", ...style }}>
      {/* Dark grade under the text so the glow reads on bright footage */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(180deg, rgba(0,0,0,0) 30%, rgba(0,0,0,0.6) 48%, rgba(0,0,0,0.82) 62%, rgba(0,0,0,0.92) 100%)",
          opacity:
            scrim *
            interpolate(frame, [0, 0.3 * fps], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.out(Easing.quad),
            }) *
            interpolate(frame, [durationInFrames - 0.3 * fps, durationInFrames], [1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.in(Easing.quad),
            }),
        }}
      />
      {/* Text layer: rides the shared camera move, scaling about a point 31.6% down the
          frame, so it drifts up as it shrinks */}
      <AbsoluteFill
        style={{
          transformOrigin: ZOOM_ORIGIN,
          scale: interpolate(frame, [0, ZOOM_WINDOW * fps], [ZOOM_START, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: zoomEase,
          }),
          opacity:
            interpolate(frame, [0, FADE_WINDOW * fps], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: fadeIn,
            }) *
            interpolate(frame, [durationInFrames - 0.25 * fps, durationInFrames], [1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.in(Easing.quad),
            }),
        }}
      >
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: `${centerY * 100}%`,
            translate: "-50% -50%",
            display: "grid",
            fontFamily,
            fontWeight: FONT_WEIGHT,
            visibility: fontReady ? "visible" : "hidden",
          }}
        >
          {/* Both glows first, then both faces, so no glow tints the other line */}
          {block("glow")}
          {block("face")}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const parseHex = (hex: string) => {
  const h = hex.replace("#", "");
  const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
const toHex = (rgb: number[]) =>
  "#" +
  rgb
    .map((v) => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, "0"))
    .join("");
const hexToRgb = (hex: string) => parseHex(hex).join(", ");
// Darken toward black (amount is negative, e.g. -0.13).
const shade = (hex: string, amount: number) => toHex(parseHex(hex).map((v) => v * (1 + amount)));
// Lighten toward white.
const tint = (hex: string, amount: number) =>
  toHex(parseHex(hex).map((v) => v + (255 - v) * amount));

const introCaptionSchema = {
  line1: { type: "text-content", default: "ARE WE FACING A", description: "Setup line (white)" },
  line2: { type: "text-content", default: "BEAR MARKET?", description: "Punch line (accent)" },
  accentColor: { type: "color", default: "#DE1832", description: "Accent colour" },
  textScale: {
    type: "number",
    default: 1,
    min: 0.5,
    max: 1.5,
    step: 0.01,
    description: "Text size (1 = reference)",
    hiddenFromList: false,
  },
  centerY: {
    type: "number",
    default: 0.58,
    min: 0.1,
    max: 0.9,
    step: 0.005,
    description: "Vertical centre (share of frame height)",
    hiddenFromList: false,
  },
  glow: {
    type: "number",
    default: 1,
    min: 0,
    max: 2,
    step: 0.05,
    description: "Glow strength",
    hiddenFromList: false,
  },
  scrim: {
    type: "number",
    default: 0.8,
    min: 0,
    max: 1,
    step: 0.05,
    description: "Dark grade under text",
    hiddenFromList: false,
  },
} as const satisfies InteractivitySchema;

export const IntroCaption = Interactive.withSchema({
  Component: IntroCaptionInner,
  componentName: "<IntroCaption>",
  schema: introCaptionSchema,
  wrapInSequence: true,
});
```

### 7. The video: `src/Intro.tsx`

The footage gets the same scale, pivot and easing as the title, plus the zoom blur:

```tsx
import { zoomBlur } from "@remotion/effects/zoom-blur";
import { Video } from "@remotion/media";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { IntroCaption } from "./IntroCaption";
import { ZOOM_CENTER, ZOOM_ORIGIN, ZOOM_START, ZOOM_WINDOW, zoomBlurShare, zoomEase } from "./introMotion";

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* The footage rides the same camera move as the title, with zoom blur while it is fast */}
      <Video
        name="Talking head"
        src={staticFile("RAW.mp4")}
        trimBefore={0}
        premountFor={fps}
        objectFit="cover"
        effects={[
          zoomBlur({
            amount: zoomBlurShare(frame, fps) * Math.min(width, height),
            center: ZOOM_CENTER,
            samples: 16,
          }),
        ]}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          transformOrigin: ZOOM_ORIGIN,
          scale: interpolate(frame, [0, ZOOM_WINDOW * fps], [ZOOM_START, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: zoomEase,
          }),
        }}
      />
      <IntroCaption
        name="Intro caption"
        from={0}
        durationInFrames={4 * fps}
        premountFor={fps}
        line1="Is AI going full"
        line2="Swarm mode?"
        accentColor="#DE1832"
        textScale={1}
        centerY={0.58}
        glow={1}
        scrim={0.8}
      />
    </AbsoluteFill>
  );
};
```

If the title starts later than frame 0, start the camera move with it: use `frame - start` in the footage's `interpolate()` and `zoomBlurShare()`.

### 8. Register the compositions: `src/Root.tsx`

`IntroCaption` is registered as its own connected composition so it can be previewed and edited alone in Studio:

```tsx
import { Composition } from "remotion";
import { Intro } from "./Intro";
import { IntroCaption } from "./IntroCaption";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Intro"
        component={Intro}
        durationInFrames={231}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="IntroCaption"
        component={IntroCaption}
        durationInFrames={120}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          line1: "Are we facing a",
          line2: "Bear market?",
          accentColor: "#DE1832",
          textScale: 1,
          centerY: 0.58,
          glow: 1,
          scrim: 0.8,
        }}
      />
    </>
  );
};
```

Set `durationInFrames` on `Intro` to the length of the cut (231 frames = 7.7 s here).

### 9. Preview, check stills, render

```bash
npx remotion studio --no-open --port 3128      # open http://localhost:3128/Intro
npx remotion still Intro check.png --frame=85 --scale=0.5
npx remotion render Intro out/Intro.mp4
```

Check before you hand it over:

- Frame 0 shows the footage punched in (~1.25x) and **sharp**, with no title yet. Frames 1–4 are slightly ghosted. By frame ~10 the footage is crisp again.
- The footage and the title shrink together and drift up. By 3 s the footage is at ~1.013x.
- At ~2.8 s the setup caps sit at ~54.5–57.8% of frame height and the punch caps at ~58–62%, with both lines ~75–80% of the frame width. If a line is noticeably narrower or smaller, the title text is the wrong length, so go back to step 3.
- The glow lifts the background around both lines. The area above the white line stays neutral, not pink.
- The letter faces are flat gradient fills: no bevel, no outline.
- The audio is intact (`npx remotion ffprobe` shows an aac stream).

### Adapting it

- Different accent: change `accentColor`. The gradient and glow tint derive from it.
- Busy or bright background: raise `scrim` (up to 1). Dark footage like the reference can go down to 0–0.3.
- Different framing (face lower or higher): nudge `centerY`. Keep the title on the chest, below the chin. At 1.25x the pivot keeps a centred head in frame. Check frame 0 if the head sits very high.
- Bigger or smaller overall: `textScale` (1 = reference). Prefer fixing the text length first.
- Landscape 16:9: set `textScale` to ~0.6.
- One line only: pass `line1=""`.

## How the look was measured

These numbers came from measuring the reference frames, and the same method works on a new reference (Python with OpenCV, Pillow and numpy).

1. **Camera move.** Track SIFT features on the reference's static background (window, monitors, building), masking out the person and the text area. Then fit a similarity transform (`cv2.estimateAffinePartial2D` with RANSAC) from frame 1 to every frame.
   - The scale went 1.000 → 0.975 → 0.961 → 0.945 (frame 5) → 0.902 (frame 13) → 0.866 (frame 25) → 0.834 (frame 41) → 0.809 (frame 69), with no rotation.
   - A double exponential fits it with 0.002 rms error (a single exponential leaves twice that and misses the fast first frames).
   - Solving the translation against the scale puts the pivot at (0.50, 0.316).
   - The title's own size curve, measured separately, matches the footage's to within ~0.3%, so they are one move.
2. **Verify on the render.** Track the rendered footage against the untouched source frames the same way. The applied curve matched the reference within ~0.3% through the main move, with the pivot at (0.50, 0.32).
3. **Calibration composition.** Register a 720x1280 / 23.976 fps composition that puts the title over the reference's own first frame (which has no text yet), with `scrim={0}`. Then render stills at the reference's frame numbers and measure each line's width and position against the reference. Final result: red-line widths 640/639, 601/602, 580/581, 570/570 px at frames 12/30/50/69, with the centre within 1.5 px.

```tsx
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { IntroCaption } from "./IntroCaption";

// Reference frame 1 (no text yet) with the caption on top, at the reference's
// 720x1280 / 23.976fps, so stills can be compared 1:1 against the reference frames.
export const Calibrate: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Img src={staticFile("ref/clean.png")} style={{ width: "100%", height: "100%" }} />
      <IntroCaption
        name="Caption"
        from={0}
        durationInFrames={4 * fps}
        premountFor={fps}
        line1="Are we facing a"
        line2="Bear market?"
        accentColor="#DE1832"
        textScale={1}
        centerY={0.58}
        glow={1}
        scrim={0}
      />
    </AbsoluteFill>
  );
};
```

4. **Opacity.** Measure the brightest white-line pixels on frames 2–17 against the background. That gave 28%, 42%, 52%, 67%, 85% and 98%, which fits `1 − e^(−t/0.17 s)`.
5. **Font.** The glyph shapes (spurred G, straight-legged R, wide A and M) say Montserrat. Stroke thickness separates the weights: the reference E arms are 0.25 × cap height, against 0.255 for Montserrat 900 and 0.219 for 800. Fitting letter positions to Montserrat 900 metrics then matched every letter within ~1 px.
6. **Glow.** Take a vertical profile from the letter edge outward: +46 brightness at the edge, +31 at 0.4 em and +12 at a full em. A two-Gaussian fit gave the 1.1 em and 2.2 em hazes.
7. **Effects check.** Track whole-frame brightness, window brightness, saturation and background sharpness over the frames. Exposure and colour are flat. Background sharpness dips only on frames 2–5, where the monitor lights visibly ghost, and that is the zoom blur.

## Lessons learned

- **Look at the footage too, not just the text.** The reference's "text motion" was really a camera move on the whole shot. Tracking the static background measured it more precisely than the text ever could, and it revealed the fast first-frame component.
- **One curve, one pivot.** Drive the footage and the title from the same `introMotion.ts` so they can't drift apart.
- **A trailing shutter keeps frame 0 sharp.** Blur on the move's first frame reads as a smeared start. Sizing the blur by the motion during the half frame *before* each frame matches the reference: sharp first frame, then ghosting.
- **`zoomBlur()` amount is in pixels per pixel-of-distance × the shorter side.** Blur length = distance to centre × amount / min(width, height), so `amount = share × min(width, height)`. It needs `Config.setChromiumOpenGlRenderer("angle")` to render.
- **Fixed sizes, not fit-to-width.** Fitting both lines to one width reproduces the reference only for text of the same length. Lock the sizes and control the look through the title's length.
- **Stylistic title, not transcript.** The title is a headline about the topic, not a quote.
- **No bevel.** A soft emboss was tried and dropped at review as unnecessary.
- **`background-clip: text` and `text-shadow` don't mix.** Put the glow on a separate solid-colour copy underneath. Paint all glows before all faces so the red glow doesn't tint the white line.
- **Pad the clipped face.** With `line-height: 0.7` the box is cap-height tall, so use `padding: 0.25em 0.1em` with matching negative margins, and put the gradient stops at 21%–79%.
- **`measureText` needs the real font.** Hold the render with `useDelayRender()` until `waitUntilDone()` resolves.
- **`useVideoConfig().durationInFrames` inside a `wrapInSequence` component is the sequence's length**, so the title's exit lands at its own end.
- **Give props defaults.** Clearing a field in Studio's props editor passes `undefined`. Defaults keep the component rendering.
