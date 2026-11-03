---
name: high-quality-captions
description: Add high-quality animated captions to a talking-head video with Remotion, in a style measured frame by frame from a top-performing short-form video. Plain captions are 1–2 lowercase words in bold Inter, cut exactly on each spoken word. Emphasis pairs put a serif italic setup word over an orange-gradient punch word that flickers on. An optional ALL-CAPS serif look is available. Use this whenever the user wants captions, subtitles or animated text on a Reel, TikTok, Short or any vertical talking-head video, asks for "high quality captions", wants word-by-word or karaoke-style captions, wants to caption a video from a transcript, or wants captions that look like the ones top creators use, even if they never mention Remotion.
---

> **Video Studio:** how this skill runs here (these lines win over the steps below where they differ).
> - **Project folder:** `projects/remotion/high-quality-captions-<job id or slug>/`, a fresh Remotion project each time as below (`projects/` is never committed). It is its own project, separate from `engines/split-screen`, so it runs whatever `styles/engines.json` says. Run every `npx` command from inside it.
> - **Footage from a studio job:** copy (never move) `jobs/<id>/source.*` into the project's `public/`.
> - **Word timings: never transcribe again.** Convert the job's WhisperX words: `node studio/words-convert.mjs captions projects/<id>/transcript/words.json <project>/public/captions.json [from] [to]` (from/to in seconds when the project uses a trimmed copy). Skip this skill's own transcription steps. That `Caption[]` file is step 3's input; go straight to step 4.
> - **Colour:** the punch-word gradient uses the brand, not the reference orange: `styles/brand.json` accentLight #C4B5FD at the top to accent #8B5CF6 at the bottom (accentDeep #4C1D95 for any glow). Everything else stays as measured.
> - **Where it fits:** a caption option for any 9:16 talking-head style (personal-reel, natural-story, relatable reels). Offer it next to fitted-captions and embedded-captions.
> - **Remotion licence:** free for individuals and companies of up to 3 people; above that it needs a company licence (remotion.dev/license).
> - **Deliver:** copy the rendered MP4 into the job folder (`jobs/<id>/preview.mp4` while reviewing, `final.mp4` when approved) or `outputs/`, and log what was added in `edits.json` so the review page can take notes on it.

# High-quality captions

This skill puts captions on a video and changes nothing else. The footage plays
untouched underneath. The fonts, placement, chunking and motion were measured
frame by frame from a reference short-form video and checked against it side by
side.

## The original brief

The skill came out of this request:

> Analyze this video to figure out the fonts that are used for the captions
> present in this video, and also analyze the motion of the captions and the
> style of the captions used as well.

> Yes, let's build out a complete Remotion caption component that can
> consistently caption entire videos using unique styling, animation, motion,
> and movements that we've derived from our analysis here. Make sure to use
> Remotion best practices, and you can show me an example using this sample
> video file.

The first build added split-screen layouts, camera moves, punch-in zooms and a
B-roll card. The user cut it back:

> I was more so just looking for the actual captions, the placements of them,
> and the motion behind them. We don't need all the extra animations and things
> that are going on here.

How the ambiguous parts were read:

- **"Captions"** means typography, placement, chunking and caption animation
  only. Do not add layouts, camera moves, zooms or B-roll unless the user asks
  for them separately.
- **"Remotion best practices"** means scaffolding a fresh project, installing
  Remotion's official agent skills into it and following them. In practice:
  `@remotion/media` for video, `@remotion/google-fonts`, Mediabunny metadata in
  `calculateMetadata`, and captions in the `Caption` type, inlined on the caption
  component so Studio's caption editor can edit them.
- **"Consistently caption entire videos"** means every spoken word is captioned
  by the same deterministic rules. The only judgement calls are which moments
  become emphasis pairs, and these are proposed to the user for confirmation.

## The look

Every caption is centred horizontally, with its centre at **69% of the frame
height**, which sits on the chest below the face. The pixel values below are
for a 1080px-wide frame and scale with the video's width.

| Look | Font | Style | Motion |
|---|---|---|---|
| Plain (default) | Inter Bold (text optical size), 95px, -0.03em tracking | Lowercase except names and acronyms. White with a soft dark shadow. | None. A hard cut exactly when the first word is spoken. |
| Emphasis pair | DM Serif Display Italic 108px, then Inter Bold 135px | The setup word is white. The punch word sits below it, overlapping the setup word's lower half, in a vertical gradient from #FDE9D4 to #F78C48 with an orange rim and a dark halo. | **Setup:** appears at 117%, holds one frame, then settles to 100% over 0.53s (ease-out cubic). **Punch:** a five-beat flicker at 30 beats per second (soft ghost, on, almost off, on, half, then solid) while rising 22px. On the punch's first full beat, the setup word dims to a white-to-grey fade. |
| ALL CAPS (optional) | Instrument Serif Italic 118px | Thickened with a 0.05em outline in the fill colour and stretched 108% wide. White with a soft shadow. | None. Hard cut. |

Chunking rules:

- A caption holds 1–2 words and at most 13 characters.
- Each caption stays up until the next one starts. After a pause longer than
  1s, it lingers 0.3s and clears.
- Two words share a caption only if:
  - they are less than 120ms apart,
  - there is no comma or full stop between them, and
  - one of them is a short function word ("into your", "so everything") or both
    are four letters or fewer ("goes live").
- A leading word such as "into", "your" or "the" joins the word after it
  rather than the word before.
- Trailing commas and full stops are dropped; `?` `!` quotes and apostrophes
  stay.

## Workflow

### 1. Scaffold a fresh project

Always start a new project. Don't reuse other Remotion projects on the machine.

```bash
npx create-video@latest --yes --blank --no-tailwind captions-project
cd captions-project
npx skills add remotion-dev/skills -a claude-code -y --copy
npx remotion add @remotion/media @remotion/captions @remotion/google-fonts @remotion/layout-utils mediabunny zod
```

Read the installed `remotion-best-practices` skill and follow it. Delete the
scaffold's `src/Composition.tsx`.

### 2. Add the footage

Copy the video into `public/`, for example `public/video.mp4`. The kit is built
for vertical 9:16 footage. The composition takes its size and length from the
file.

### 3. Get word-level timing

The captions need a start and end time for every word.

- **The user has a word-level transcript.** Use it if it's either:
  - JSON in the shape `{ segments: [{ words: [{ text, start, duration }] }] }`
    with times in seconds, or
  - a `Caption[]` array.

  Go to step 4.
- **The user has no transcript.** Follow `transcribe-captions.md` in the
  installed `remotion-captions` skill (Whisper via `@remotion/whisper-webgpu`,
  model `small.en` for English). It writes a `Caption[]` JSON file. Whisper can
  split a word into pieces (" Anth" + "ropic"); the converter in step 4 joins
  them back together.

### 4. Convert, correct and case the words

Save this converter as `scripts/transcript-to-captions.mjs`:

```js title="scripts/transcript-to-captions.mjs"
#!/usr/bin/env node
// Converts a word-level transcript into Remotion's Caption[] format.
//
//   node scripts/transcript-to-captions.mjs <transcript.json> [--fixes fixes.json] [--ts]
//
// Input: either { segments: [{ words: [{ text, start, duration, confidence }] }] }
// (seconds) or a Caption[] array, such as the output of Remotion's Whisper
// transcription.
// --ts prints an array literal to paste inline into <CaptionTrack captions={[...]}>.
//
// fixes.json:
// {
//   "replace": [{ "from": "throbbing", "to": "Anthropic" },
//               { "from": "all of a sudden", "to": "I'll send" },
//               { "from": "of them", "to": "of the", "punctuation": "" }],
//   "casing": { "claude": "Claude", "opus": "Opus" }
// }
// Captions are lowercase except names, acronyms and "I" forms, as in the
// reference style. "casing" lists the names to keep capitalised.

import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
const fixesIndex = args.indexOf("--fixes");
const fixesPath = fixesIndex === -1 ? null : args[fixesIndex + 1];
const inputPath = args.find(
  (a, i) => !a.startsWith("--") && (fixesIndex === -1 || i !== fixesIndex + 1),
);
const asTs = args.includes("--ts");

if (!inputPath) {
  console.error(
    "Usage: transcript-to-captions.mjs <transcript.json> [--fixes fixes.json] [--ts]",
  );
  process.exit(1);
}

const input = JSON.parse(readFileSync(inputPath, "utf8"));
const fixes = fixesPath ? JSON.parse(readFileSync(fixesPath, "utf8")) : {};

const key = (text) =>
  text
    .toLowerCase()
    .replace(/’/g, "'")
    .replace(/[^a-z0-9.']/g, "")
    .replace(/\.+$/, "");

// 1. Flatten to { text, startMs, endMs, confidence }.
let words;
if (Array.isArray(input)) {
  // Caption[] (e.g. from Whisper). A token without a leading space continues
  // the previous word (" Anth" + "ropic"), so stitch those back together.
  words = [];
  for (const c of input) {
    const previous = words[words.length - 1];
    if (previous && !/^\s/.test(c.text) && c.text.trim().length > 0) {
      previous.text += c.text.trim();
      previous.endMs = c.endMs;
      continue;
    }
    if (c.text.trim().length === 0) continue;
    words.push({
      text: c.text.trim(),
      startMs: c.startMs,
      endMs: c.endMs,
      confidence: c.confidence ?? null,
    });
  }
} else {
  words = input.segments.flatMap((segment) =>
    segment.words
      // Disfluencies ("um", "uh") come through as empty words; skip them.
      .filter((w) => (w.type ?? "word") === "word" && w.text.trim().length > 0)
      .map((w) => ({
        text: w.text.trim(),
        startMs: Math.round(w.start * 1000),
        endMs: Math.round((w.start + w.duration) * 1000),
        confidence: w.confidence ?? null,
      })),
  );
}

// 2. Phrase replacements. The new words share the old time span, weighted by
// length, and inherit the trailing punctuation of the last replaced word
// unless "punctuation" sets it ("" drops it).
for (const { from, to, punctuation } of fixes.replace ?? []) {
  const fromKeys = from.split(/\s+/).map(key);
  const toWords = to.split(/\s+/);
  for (let i = 0; i <= words.length - fromKeys.length; i++) {
    const match = fromKeys.every((k, j) => key(words[i + j].text) === k);
    if (!match) continue;
    const span = words.slice(i, i + fromKeys.length);
    const startMs = span[0].startMs;
    const endMs = span[span.length - 1].endMs;
    const trailing =
      punctuation ?? span[span.length - 1].text.match(/[,.;:?!]+$/)?.[0] ?? "";
    const total = toWords.reduce((sum, w) => sum + w.length, 0);
    let cursor = startMs;
    const replacement = toWords.map((text, j) => {
      const share = Math.round(((endMs - startMs) * text.length) / total);
      const wordEnd = j === toWords.length - 1 ? endMs : cursor + share;
      const word = {
        text: j === toWords.length - 1 ? text + trailing : text,
        startMs: cursor,
        endMs: wordEnd,
        confidence: null,
      };
      cursor = wordEnd;
      return word;
    });
    words.splice(i, fromKeys.length, ...replacement);
    i += replacement.length - 1;
  }
}

// 3. Casing: lowercase, except listed names, acronyms and "I" forms.
const casing = Object.fromEntries(
  Object.entries(fixes.casing ?? {}).map(([k, v]) => [k.toLowerCase(), v]),
);
const recase = (text) => {
  const match = text.match(/^(["“‘(]*)(.*?)([,.;:?!"”’)]*)$/);
  const [, lead, core, trail] = match;
  const lookup = casing[core.toLowerCase()];
  if (lookup) return lead + lookup + trail;
  if (/^I('|’|$)/.test(core)) return text;
  if (core.length > 1 && core === core.toUpperCase() && /[A-Z]/.test(core))
    return text;
  return lead + core.toLowerCase() + trail;
};

const captions = words.map((w) => ({
  text: ` ${recase(w.text)}`,
  startMs: w.startMs,
  endMs: w.endMs,
  timestampMs: Math.round((w.startMs + w.endMs) / 2),
  confidence: w.confidence,
}));

if (asTs) {
  const lines = captions.map(
    (c) =>
      `{text: ${JSON.stringify(c.text)}, startMs: ${c.startMs}, endMs: ${c.endMs}, timestampMs: ${c.timestampMs}, confidence: ${c.confidence}},`,
  );
  console.log(lines.join("\n"));
} else {
  console.log(JSON.stringify(captions, null, 2));
}
```

Read the transcript before converting. Transcription mishears names and
phrases. In the reference build, "Anthropic" came back as "throbbing" and
"I'll send" as "all of a sudden". Write a `fixes.json` with the corrections and
the names to keep capitalised. Everything else is lowercased, as in the
reference.

```json
{
  "replace": [
    { "from": "throbbing", "to": "Anthropic" },
    { "from": "all of a sudden", "to": "I'll send" },
    { "from": "of them", "to": "of the", "punctuation": "" }
  ],
  "casing": { "anthropic": "Anthropic", "claude": "Claude" }
}
```

How the converter applies fixes:

- A replacement keeps the trailing punctuation of the last word it replaces,
  so a misheard "them." would become "the.". Set `"punctuation"` to choose it
  yourself; `""` drops it.
- Empty words that some transcribers emit for "um" and "uh" are skipped.

If you're unsure what a word should be, ask the user rather than guessing.
Then generate the caption lines:

```bash
node scripts/transcript-to-captions.mjs transcript.json --fixes fixes.json --ts > captions.txt
```

### 5. Add the caption files

Create these files exactly as written.

```ts title="src/captions/tokens.ts"
// Every number here was measured from the reference video (720x1280, 30fps)
// and scaled to a 1080px-wide frame. Components multiply px values by
// `width / 1080`, so the look holds at any resolution.

export const BASE_WIDTH = 1080;

// Caption centre, as a fraction of frame height: on the chest, below the face.
export const positionY = 0.69;

// Plain captions: lowercase bold sans, 1-2 words, hard cuts.
export const sans = {
  fontSize: 95,
  letterSpacing: "-0.03em",
  // Inter's text cut (opsz 14) matched the reference better than Display.
  fontVariationSettings: "'opsz' 14",
  maxWidth: 940,
  color: "#FFFFFF",
  shadow: "0 3px 18px rgba(0, 0, 0, 0.45), 0 1px 4px rgba(0, 0, 0, 0.35)",
} as const;

// Optional ALL-CAPS italic serif look, hard cuts.
export const caps = {
  fontSize: 118,
  // Synthetic bold: an outline in the fill colour.
  strokeWidth: "0.05em",
  // The reference renders wider than stock Instrument Serif.
  stretchX: 1.08,
  letterSpacing: "0em",
  maxWidth: 960,
  color: "#FFFFFF",
  shadow: "0 3px 18px rgba(0, 0, 0, 0.45), 0 1px 4px rgba(0, 0, 0, 0.35)",
} as const;

// Emphasis pair: serif setup word, then a gradient sans punch word below it.
export const emphasis = {
  setupFontSize: 108,
  setupLetterSpacing: "-0.01em",
  setupColor: "#FFFFFF",
  // After the punch lands the setup word fades from white to grey at its foot.
  setupDimmed:
    "linear-gradient(180deg, #FFFFFF 0%, #F7F2EF 55%, #D5CBC6 80%, #A9A19C 100%)",
  setupShadow: "drop-shadow(0 3px 14px rgba(0, 0, 0, 0.4))",
  punchFontSize: 135,
  punchLetterSpacing: "-0.03em",
  // Sampled from the reference glyphs, top to bottom. The glyphs sit between
  // about 20% and 80% of the text box, so the stops are placed there.
  punchGradient:
    "linear-gradient(180deg, #FDE9D4 0%, #FDE9D4 20%, #FCDFC3 35%, #FCCAA2 50%, #F7AC75 65%, #F78C48 80%, #F37A35 100%)",
  // A warm orange rim, then a wide dark halo that also darkens the setup word
  // where the punch overlaps it.
  punchShadow:
    "drop-shadow(0 0 12px rgba(250, 140, 70, 0.4)) drop-shadow(0 4px 10px rgba(40, 14, 2, 0.55)) drop-shadow(0 10px 30px rgba(30, 10, 0, 0.6))",
  // Distance from the setup centre to the punch centre. The punch overlaps the
  // lower part of the setup word.
  punchOffsetY: 74,
  maxWidth: 960,
} as const;

// Emphasis motion, in seconds unless noted.
export const motion = {
  // Setup word: appears big, holds one frame, settles with a long ease-out.
  setupScaleFrom: 1.17,
  setupHold: 1 / 30,
  setupSettle: 16 / 30,
  // Punch word: a five-beat flicker-on at 30 beats per second while it rises.
  // Beat 0 is a soft ghost, then on / almost off / on / half / on.
  punchFlickerOpacity: [0.3, 1, 0.08, 1, 0.5] as const,
  punchGhostBlur: 3,
  punchRiseFrom: 22, // px at beat 1
  punchRiseBeats: 4, // rise finishes at beat 5
  beatsPerSecond: 30,
} as const;

// Chunking: 1-2 words per caption, cut exactly on the spoken word.
export const chunking = {
  maxChars: 13,
  maxGapMs: 120, // words further apart than this never share a caption
  holdGapMs: 1000, // a caption holds until the next one if the pause is shorter
  tailMs: 300, // otherwise it lingers this long after the last word
} as const;
```

```ts title="src/captions/fonts.ts"
import { loadFont as loadDMSerifDisplay } from "@remotion/google-fonts/DMSerifDisplay";
import { loadFont as loadInstrumentSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

// The three faces identified in the reference video. Loading at module level
// blocks rendering until they are ready.
const inter = loadInter("normal", { weights: ["700"], subsets: ["latin"] });
const instrumentSerif = loadInstrumentSerif("italic", {
  weights: ["400"],
  subsets: ["latin"],
});
const dmSerifDisplay = loadDMSerifDisplay("italic", {
  weights: ["400"],
  subsets: ["latin"],
});

export const fonts = {
  // Plain captions and the punch word of an emphasis pair.
  sans: inter.fontFamily,
  // Optional ALL-CAPS captions.
  capsSerif: instrumentSerif.fontFamily,
  // The setup word of an emphasis pair.
  setupSerif: dmSerifDisplay.fontFamily,
} as const;

export const waitForFonts = () =>
  Promise.all([
    inter.waitUntilDone(),
    instrumentSerif.waitUntilDone(),
    dmSerifDisplay.waitUntilDone(),
  ]);
```

```ts title="src/captions/beats.ts"
import type { Caption } from "@remotion/captions";

// Type-only imports keep this file runnable with plain `node` for tests.

// Captions that start inside one of these ranges use the ALL-CAPS serif look.
export type CapsSection = {
  readonly startMs: number;
  readonly endMs: number;
};

export type EmphasisSpec = {
  // Spoken words that open the pair, e.g. "completely".
  readonly setup: string;
  // Spoken words that land as the punch, e.g. "from scratch". Words between
  // setup and punch are absorbed into the pair.
  readonly punch: string;
  // Optional display override for the punch, e.g. "“Opus”". Empty = as spoken.
  readonly punchLabel: string;
  // "next": hold until the next caption. "end": hold to the end of the video.
  readonly hold: "next" | "end";
};

export type ChunkOptions = {
  readonly maxChars: number;
  readonly maxGapMs: number;
  readonly holdGapMs: number;
  readonly tailMs: number;
};

type Word = {
  readonly raw: string;
  readonly text: string;
  readonly key: string;
  readonly startMs: number;
  readonly endMs: number;
  readonly pageBreakAfter: boolean;
};

export type PlainBeat = {
  readonly kind: "plain";
  readonly text: string;
  readonly startMs: number;
  readonly endMs: number;
  readonly caps: boolean;
};

export type EmphasisBeat = {
  readonly kind: "emphasis";
  readonly setup: string;
  readonly punch: string;
  readonly startMs: number;
  readonly punchStartMs: number;
  readonly endMs: number;
};

export type Beat = PlainBeat | EmphasisBeat;

// Short words that read as part of their neighbour.
// prettier-ignore
const FUNCTION_WORDS = new Set([
  "a", "an", "the", "and", "or", "but", "so", "if", "as", "at", "by", "for",
  "from", "in", "into", "of", "on", "onto", "to", "up", "with", "about", "it",
  "it's", "its", "is", "are", "was", "be", "been", "am", "i", "i'm", "i'll",
  "you", "you're", "your", "my", "me", "we", "our", "us", "they", "their",
  "them", "he", "his", "she", "her", "this", "that", "these", "those", "can",
  "do", "does", "will", "just", "now", "all", "any", "no", "not", "than",
  "then", "what", "who", "how", "when", "like", "even",
]);

// Function words that lean forward onto the next word ("into | your profile").
// prettier-ignore
const LEADING_WORDS = new Set([
  "a", "an", "the", "your", "my", "our", "their", "his", "her", "its", "this",
  "that", "these", "those", "to", "into", "on", "in", "at", "for", "from",
  "of", "with", "by", "about",
]);

const BREAK_AFTER = /[,.;:?!]["”’]?$/;

// Captions drop trailing commas and full stops but keep ? ! quotes and
// apostrophes, as in the reference ("yourselves?", "LINKEDIN'S"). A lookahead
// keeps a closing quote without a "$" + digit replacement string, which a
// skill loader would replace with its first argument.
export const displayText = (raw: string): string =>
  raw.replace(/[,.;:]+(?=["”’]?$)/, "");

const matchKey = (raw: string): string =>
  raw
    .toLowerCase()
    .replace(/[’]/g, "'")
    .replace(/[^a-z0-9.']/g, "")
    .replace(/\.+$/, "");

const isFunctionWord = (w: Word) => FUNCTION_WORDS.has(w.key);
const isShort = (w: Word) => w.text.length <= 3;

const toWords = (captions: readonly Caption[]): Word[] =>
  captions
    .map((c) => {
      const raw = c.text.trim();
      return {
        raw,
        text: displayText(raw),
        key: matchKey(raw),
        startMs: c.startMs,
        endMs: c.endMs,
        pageBreakAfter: c.pageBreakAfter === true,
      };
    })
    .filter((w) => w.raw.length > 0);

type EmphasisGroup = {
  readonly spec: EmphasisSpec;
  readonly setupFrom: number;
  readonly punchFrom: number;
  readonly punchTo: number; // exclusive
};

const findPhrase = (
  words: readonly Word[],
  phrase: string,
  from: number,
  to: number,
  taken: ReadonlySet<number>,
): number => {
  const keys = phrase.split(/\s+/).map(matchKey).filter(Boolean);
  if (keys.length === 0) {
    return -1;
  }
  for (let i = from; i <= Math.min(to, words.length - keys.length); i++) {
    let ok = true;
    for (let k = 0; k < keys.length; k++) {
      if (taken.has(i + k) || words[i + k].key !== keys[k]) {
        ok = false;
        break;
      }
    }
    if (ok) {
      return i;
    }
  }
  return -1;
};

const findEmphasisGroups = (
  words: readonly Word[],
  specs: readonly EmphasisSpec[],
): EmphasisGroup[] => {
  const taken = new Set<number>();
  const groups: EmphasisGroup[] = [];
  let cursor = 0;
  for (const spec of specs) {
    const setupLength = spec.setup.split(/\s+/).filter(Boolean).length;
    const punchLength = spec.punch.split(/\s+/).filter(Boolean).length;
    const setupFrom = findPhrase(
      words,
      spec.setup,
      cursor,
      words.length,
      taken,
    );
    if (setupFrom === -1) {
      continue;
    }
    // The punch must follow within a few words of the setup.
    const punchFrom = findPhrase(
      words,
      spec.punch,
      setupFrom + setupLength,
      setupFrom + setupLength + 6,
      taken,
    );
    if (punchFrom === -1) {
      continue;
    }
    const punchTo = punchFrom + punchLength;
    for (let i = setupFrom; i < punchTo; i++) {
      taken.add(i);
    }
    groups.push({ spec, setupFrom, punchFrom, punchTo });
    cursor = punchTo;
  }
  return groups.sort((a, b) => a.setupFrom - b.setupFrom);
};

const canPair = (a: Word, b: Word, options: ChunkOptions): boolean => {
  if (a.pageBreakAfter || BREAK_AFTER.test(a.raw)) {
    return false;
  }
  if (b.startMs - a.endMs > options.maxGapMs) {
    return false;
  }
  if (a.text.length + 1 + b.text.length > options.maxChars) {
    return false;
  }
  return (
    isFunctionWord(a) ||
    isFunctionWord(b) ||
    isShort(a) ||
    isShort(b) ||
    // Two tiny content words read as one ("goes live", "form work").
    (a.text.length <= 4 && b.text.length <= 4)
  );
};

type DraftBeat =
  | { kind: "plain"; words: Word[] }
  | { kind: "emphasis"; group: EmphasisGroup; words: Word[] };

export const buildBeats = ({
  captions,
  capsSections,
  emphasis,
  durationMs,
  options,
}: {
  readonly captions: readonly Caption[];
  readonly capsSections: readonly CapsSection[];
  readonly emphasis: readonly EmphasisSpec[];
  readonly durationMs: number;
  readonly options: ChunkOptions;
}): Beat[] => {
  const words = toWords(captions);
  const groups = findEmphasisGroups(words, emphasis);
  const groupAt = new Map(groups.map((g) => [g.setupFrom, g]));
  const isCaps = (w: Word) =>
    capsSections.some((c) => w.startMs >= c.startMs && w.startMs < c.endMs);

  const drafts: DraftBeat[] = [];
  let i = 0;
  while (i < words.length) {
    const group = groupAt.get(i);
    if (group) {
      drafts.push({
        kind: "emphasis",
        group,
        words: words.slice(group.setupFrom, group.punchTo),
      });
      if (group.spec.hold === "end") {
        break;
      }
      i = group.punchTo;
      continue;
    }

    const a = words[i];
    const b = words[i + 1];
    const c = words[i + 2];
    let pair =
      b !== undefined &&
      !groupAt.has(i + 1) &&
      isCaps(a) === isCaps(b) &&
      canPair(a, b, options);

    // Let a leading word ("into", "your") join the word after it instead.
    if (
      pair &&
      c !== undefined &&
      !isFunctionWord(a) &&
      LEADING_WORDS.has(b.key) &&
      !isFunctionWord(c) &&
      !groupAt.has(i + 2) &&
      isCaps(b) === isCaps(c) &&
      canPair(b, c, options)
    ) {
      pair = false;
    }

    drafts.push({ kind: "plain", words: pair ? [a, b] : [a] });
    i += pair ? 2 : 1;
  }

  return drafts.map((draft, index): Beat => {
    const first = draft.words[0];
    const last = draft.words[draft.words.length - 1];
    const next = drafts[index + 1];

    let endMs: number;
    if (draft.kind === "emphasis" && draft.group.spec.hold === "end") {
      endMs = durationMs;
    } else if (
      next &&
      next.words[0].startMs - last.endMs <= options.holdGapMs
    ) {
      endMs = next.words[0].startMs;
    } else {
      endMs = last.endMs + options.tailMs;
      if (next) {
        endMs = Math.min(endMs, next.words[0].startMs);
      }
    }

    if (draft.kind === "plain") {
      return {
        kind: "plain",
        text: draft.words.map((w) => w.text).join(" "),
        startMs: first.startMs,
        endMs,
        caps: isCaps(first),
      };
    }

    const { group } = draft;
    const setupWords = words.slice(
      group.setupFrom,
      group.setupFrom + group.spec.setup.split(/\s+/).filter(Boolean).length,
    );
    const punchWords = words.slice(group.punchFrom, group.punchTo);
    return {
      kind: "emphasis",
      setup: setupWords.map((w) => w.text).join(" "),
      punch:
        group.spec.punchLabel.length > 0
          ? group.spec.punchLabel
          : punchWords.map((w) => w.text).join(" "),
      startMs: first.startMs,
      punchStartMs: punchWords[0].startMs,
      endMs,
    };
  });
};
```

```tsx title="src/captions/styles/SansCaption.tsx"
import { fitText } from "@remotion/layout-utils";
import type React from "react";
import { useVideoConfig } from "remotion";
import { fonts } from "../fonts";
import { BASE_WIDTH, sans } from "../tokens";

// Plain captions: lowercase bold sans with a soft shadow, one or two words at
// a time. No animation: each caption is a hard cut on the spoken word.
export const SansCaption: React.FC<{
  readonly text: string;
  readonly y: number;
}> = ({ text, y }) => {
  const { width } = useVideoConfig();
  const s = width / BASE_WIDTH;
  const fontSize = Math.min(
    sans.fontSize * s,
    fitText({
      text,
      withinWidth: sans.maxWidth * s,
      fontFamily: fonts.sans,
      fontWeight: 700,
      letterSpacing: sans.letterSpacing,
    }).fontSize,
  );

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
        translate: "0 -50%",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <span
        style={{
          fontFamily: fonts.sans,
          fontWeight: 700,
          fontSize,
          letterSpacing: sans.letterSpacing,
          fontVariationSettings: sans.fontVariationSettings,
          lineHeight: 1,
          whiteSpace: "pre",
          color: sans.color,
          textShadow: sans.shadow,
        }}
      >
        {text}
      </span>
    </div>
  );
};
```

```tsx title="src/captions/styles/CapsCaption.tsx"
import { fitText } from "@remotion/layout-utils";
import type React from "react";
import { useVideoConfig } from "remotion";
import { fonts } from "../fonts";
import { BASE_WIDTH, caps } from "../tokens";

// Optional ALL-CAPS look: Instrument Serif Italic, thickened with an outline in
// the fill colour and stretched slightly wider, as measured on the reference.
// Hard cuts, no animation.
export const CapsCaption: React.FC<{
  readonly text: string;
  readonly y: number;
}> = ({ text, y }) => {
  const { width } = useVideoConfig();
  const s = width / BASE_WIDTH;
  const fontSize = Math.min(
    caps.fontSize * s,
    fitText({
      text,
      withinWidth: (caps.maxWidth * s) / caps.stretchX,
      fontFamily: fonts.capsSerif,
      fontWeight: 400,
      letterSpacing: caps.letterSpacing,
      textTransform: "uppercase",
      additionalStyles: { fontStyle: "italic" },
    }).fontSize,
  );

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
        translate: "0 -50%",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <span
        style={{
          display: "inline-block",
          fontFamily: fonts.capsSerif,
          fontStyle: "italic",
          fontWeight: 400,
          fontSize,
          letterSpacing: caps.letterSpacing,
          textTransform: "uppercase",
          lineHeight: 1,
          whiteSpace: "pre",
          color: caps.color,
          WebkitTextStroke: `${caps.strokeWidth} ${caps.color}`,
          textShadow: caps.shadow,
          scale: `${caps.stretchX} 1`,
        }}
      >
        {text}
      </span>
    </div>
  );
};
```

```tsx title="src/captions/styles/EmphasisCaption.tsx"
import { fitText } from "@remotion/layout-utils";
import type React from "react";
import { Easing, interpolate, useVideoConfig } from "remotion";
import { fonts } from "../fonts";
import { BASE_WIDTH, emphasis, motion } from "../tokens";

const BEAT_MS = 1000 / motion.beatsPerSecond;

// Style 3: the emphasis pair. A serif italic setup word settles in from 117%,
// then the gradient sans punch word flickers on below it, overlapping its
// bottom edge, while the setup word dims to a white-to-grey fade.
export const EmphasisCaption: React.FC<{
  readonly setup: string;
  readonly punch: string;
  readonly y: number;
  // Time since the setup word was spoken, and since the punch word was.
  // The punch is hidden while msSincePunch < 0.
  readonly msSinceSetup: number;
  readonly msSincePunch: number;
}> = ({ setup, punch, y, msSinceSetup, msSincePunch }) => {
  const { width } = useVideoConfig();
  const s = width / BASE_WIDTH;

  const setupFontSize = Math.min(
    emphasis.setupFontSize * s,
    fitText({
      text: setup,
      withinWidth: emphasis.maxWidth * s,
      fontFamily: fonts.setupSerif,
      fontWeight: 400,
      letterSpacing: emphasis.setupLetterSpacing,
      additionalStyles: { fontStyle: "italic" },
    }).fontSize,
  );
  const punchFontSize = Math.min(
    emphasis.punchFontSize * s,
    fitText({
      text: punch,
      withinWidth: emphasis.maxWidth * s,
      fontFamily: fonts.sans,
      fontWeight: 700,
      letterSpacing: emphasis.punchLetterSpacing,
    }).fontSize,
  );

  // Punch timing runs on 30 beats per second at any frame rate.
  const beat = msSincePunch < 0 ? -1 : Math.floor(msSincePunch / BEAT_MS);
  const punchVisible = beat >= 0;
  const punchOpacity =
    beat >= 0 && beat < motion.punchFlickerOpacity.length
      ? motion.punchFlickerOpacity[beat]
      : 1;
  const punchRise =
    beat === 0
      ? motion.punchRiseFrom * 1.1 * s
      : interpolate(
          msSincePunch,
          [BEAT_MS, (1 + motion.punchRiseBeats) * BEAT_MS],
          [motion.punchRiseFrom * s, 0],
          {
            easing: Easing.bezier(0.25, 0.46, 0.45, 0.94),
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          },
        );
  const setupDimmed = beat >= 1;

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          translate: "0 -50%",
          display: "flex",
          justifyContent: "center",
          filter: emphasis.setupShadow,
          scale: interpolate(
            msSinceSetup,
            [
              motion.setupHold * 1000,
              (motion.setupHold + motion.setupSettle) * 1000,
            ],
            [motion.setupScaleFrom, 1],
            {
              easing: Easing.bezier(0.215, 0.61, 0.355, 1),
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              output: "perceptual-scale",
            },
          ),
        }}
      >
        <span
          style={{
            fontFamily: fonts.setupSerif,
            fontStyle: "italic",
            fontWeight: 400,
            fontSize: setupFontSize,
            letterSpacing: emphasis.setupLetterSpacing,
            lineHeight: 1.1,
            whiteSpace: "pre",
            // Padding keeps italic overhangs inside the clipped gradient.
            padding: "0.08em 0.18em",
            backgroundImage: setupDimmed
              ? emphasis.setupDimmed
              : `linear-gradient(${emphasis.setupColor}, ${emphasis.setupColor})`,
            backgroundClip: "text",
            WebkitBackgroundClip: "text",
            color: "transparent",
            WebkitTextFillColor: "transparent",
          }}
        >
          {setup}
        </span>
      </div>
      {punchVisible ? (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: emphasis.punchOffsetY * s,
            translate: `0 calc(-50% + ${punchRise}px)`,
            display: "flex",
            justifyContent: "center",
            opacity: punchOpacity,
            filter: `${emphasis.punchShadow}${
              beat === 0 ? ` blur(${motion.punchGhostBlur * s}px)` : ""
            }`,
          }}
        >
          <span
            style={{
              fontFamily: fonts.sans,
              fontWeight: 700,
              fontSize: punchFontSize,
              letterSpacing: emphasis.punchLetterSpacing,
              lineHeight: 1.1,
              whiteSpace: "pre",
              padding: "0.04em 0.08em",
              backgroundImage: emphasis.punchGradient,
              backgroundClip: "text",
              WebkitBackgroundClip: "text",
              color: "transparent",
              WebkitTextFillColor: "transparent",
            }}
          >
            {punch}
          </span>
        </div>
      ) : null}
    </div>
  );
};
```

```tsx title="src/captions/CaptionTrack.tsx"
import type { Caption } from "@remotion/captions";
import type React from "react";
import { useEffect, useMemo, useState } from "react";
import {
  AbsoluteFill,
  Interactive,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
  type InteractiveTransformProps,
  type InteractivitySchema,
} from "remotion";
import { buildBeats, type CapsSection, type EmphasisSpec } from "./beats";
import { waitForFonts } from "./fonts";
import { CapsCaption } from "./styles/CapsCaption";
import { EmphasisCaption } from "./styles/EmphasisCaption";
import { SansCaption } from "./styles/SansCaption";
import { chunking, positionY as defaultPositionY } from "./tokens";

type CaptionTrackProps = InteractiveTransformProps & {
  readonly captions: Caption[];
  // Emphasis pairs, matched against the spoken words in order.
  readonly emphasis: readonly EmphasisSpec[];
  // Time ranges that use the ALL-CAPS serif look. Empty = never.
  readonly capsSections?: readonly CapsSection[];
  // Caption centre as a fraction of frame height.
  readonly positionY?: number;
  readonly maxChars?: number;
};

const captionTrackSchema = {
  ...Interactive.captionsSchema,
  positionY: {
    type: "number",
    min: 0,
    max: 1,
    step: 0.005,
    default: defaultPositionY,
    description: "Caption height (fraction of frame)",
    hiddenFromList: false,
  },
  maxChars: {
    type: "number",
    min: 4,
    max: 30,
    step: 1,
    default: chunking.maxChars,
    description: "Max characters per caption",
    hiddenFromList: false,
  },
} as const satisfies InteractivitySchema;

// fitText() measures with the real fonts, so wait for them before the first
// caption is laid out.
const useFontsReady = () => {
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Loading caption fonts"));
  const [ready, setReady] = useState(false);

  useEffect(() => {
    waitForFonts()
      .then(() => setReady(true))
      .catch((err) => cancelRender(err));
  }, [cancelRender]);

  useEffect(() => {
    if (ready) {
      continueRender(handle);
    }
  }, [ready, continueRender, handle]);

  return ready;
};

const CaptionTrackContent: React.FC<CaptionTrackProps> = ({
  captions,
  emphasis,
  capsSections = [],
  positionY = defaultPositionY,
  maxChars = chunking.maxChars,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps, height, durationInFrames } = useVideoConfig();
  const fontsReady = useFontsReady();

  const beats = useMemo(
    () =>
      buildBeats({
        captions,
        capsSections,
        emphasis,
        durationMs: (durationInFrames / fps) * 1000,
        options: { ...chunking, maxChars },
      }),
    [captions, capsSections, emphasis, durationInFrames, fps, maxChars],
  );

  const ms = (frame / fps) * 1000;
  const beat = beats.find((b) => ms >= b.startMs && ms < b.endMs);
  const y = positionY * height;

  let content: React.ReactNode = null;
  if (fontsReady && beat) {
    if (beat.kind === "emphasis") {
      content = (
        <EmphasisCaption
          setup={beat.setup}
          punch={beat.punch}
          y={y}
          msSinceSetup={ms - beat.startMs}
          msSincePunch={ms - beat.punchStartMs}
        />
      );
    } else if (beat.caps) {
      content = <CapsCaption text={beat.text} y={y} />;
    } else {
      content = <SansCaption text={beat.text} y={y} />;
    }
  }

  return (
    <AbsoluteFill
      name="Caption layer"
      style={{ pointerEvents: "none", ...style }}
    >
      {content}
    </AbsoluteFill>
  );
};

export const CaptionTrack = Interactive.withSchema({
  Component: CaptionTrackContent,
  componentName: "<CaptionTrack>",
  schema: captionTrackSchema,
  wrapInSequence: true,
});
```

```ts title="src/captions/schema.ts"
import { z } from "zod";

// Editable in the Studio props panel for any captioned video.

export const emphasisSchema = z.object({
  // Spoken words that open the pair, e.g. "completely".
  setup: z.string(),
  // Spoken words that land as the punch, e.g. "free".
  punch: z.string(),
  // Display override for the punch, e.g. "“Agent”". Empty = as spoken.
  punchLabel: z.string(),
  // "next": hold until the next caption. "end": hold to the end of the video.
  hold: z.enum(["next", "end"]),
});

export const capsSectionSchema = z.object({
  startMs: z.number().min(0),
  endMs: z.number().min(0),
});

export const captionedVideoSchema = z.object({
  src: z.string(),
  emphasis: z.array(emphasisSchema),
  // Time ranges captioned in the ALL-CAPS serif look. Empty = never.
  capsSections: z.array(capsSectionSchema),
});

export type CaptionedVideoProps = z.infer<typeof captionedVideoSchema>;
```

### 6. Create the composition

Paste the lines from `captions.txt` into the `captions` array, one caption per
line. Keep the captions inline on `<CaptionTrack>`: Studio's caption editor
writes edits back to that array. Set `src` to the footage's file name in
`public/`.

```tsx title="src/Captioned.tsx"
import { Video } from "@remotion/media";
import { ALL_FORMATS, Input, UrlSource } from "mediabunny";
import type React from "react";
import {
  AbsoluteFill,
  Composition,
  staticFile,
  useVideoConfig,
  type CalculateMetadataFunction,
} from "remotion";
import { CaptionTrack } from "./captions/CaptionTrack";
import {
  captionedVideoSchema,
  type CaptionedVideoProps,
} from "./captions/schema";

export const Captioned: React.FC<CaptionedVideoProps> = ({
  src,
  emphasis,
  capsSections,
}) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill name="Captioned" style={{ backgroundColor: "#000000" }}>
      <Video
        name="Footage"
        src={staticFile(src)}
        objectFit="cover"
        premountFor={fps}
        style={{ position: "absolute", width: "100%", height: "100%" }}
      />
      <CaptionTrack
        name="Captions"
        premountFor={fps}
        emphasis={emphasis}
        capsSections={capsSections}
        // prettier-ignore
        captions={[
          // Paste the lines from captions.txt here.
        ]}
      />
    </AbsoluteFill>
  );
};

// Length and size come from the footage.
const calculateMetadata: CalculateMetadataFunction<
  CaptionedVideoProps
> = async ({ props }) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(staticFile(props.src)),
  });
  const durationInSeconds = await input.computeDuration();
  const videoTrack = await input.getPrimaryVideoTrack();
  input.dispose();
  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
    ...(videoTrack
      ? { width: videoTrack.displayWidth, height: videoTrack.displayHeight }
      : {}),
  };
};

export const CaptionedComposition: React.FC = () => {
  return (
    <Composition
      id="Captioned"
      component={Captioned}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
      schema={captionedVideoSchema}
      calculateMetadata={calculateMetadata}
      defaultProps={{
        src: "video.mp4",
        emphasis: [],
        capsSections: [],
      }}
    />
  );
};
```

```tsx title="src/Root.tsx"
import { CaptionedComposition } from "./Captioned";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <CaptionedComposition />
    </>
  );
};
```

For several videos, copy `Captioned.tsx` under a new name, give it a unique
`id`, and register it in `Root.tsx` too.

### 7. Propose the emphasis pairs (the user confirms)

Emphasis pairs are the only judgement call. Read the transcript and propose
them as a short list. Don't add them before the user agrees.

- **How many:** use them sparingly, about one every 8–12 seconds, and at most
  three or four a minute. The reference used three in 36 seconds: the hook
  ("completely / free"), the proof ("20 proven / formulas") and the call to
  action ("comment / “Agent”").
- **Which words:**
  - The setup is the lead-in word or words spoken just before the payoff.
  - The punch is the payoff itself, 1–2 words: a number, a name, the keyword or
    the CTA word.
  - The punch must start within six words of the setup. Any words between them
    are absorbed into the pair and not shown.
- **CTA pairs:** for a "comment X" call to action, set `punchLabel` to the
  keyword in curly quotes (`"“Opus”"`) and `hold: "end"`, so the pair stays up
  to the end of the video.
- **Where they go:** add the confirmed pairs to `emphasis` in `defaultProps`,
  in spoken order:

```tsx
emphasis: [
  { setup: "Opus", punch: "5.5", punchLabel: "", hold: "next" },
  { setup: "completely", punch: "from scratch", punchLabel: "", hold: "next" },
  { setup: "comment", punch: "Opus", punchLabel: "“Opus”", hold: "end" },
],
```

ALL-CAPS sections are optional and off by default. Offer them only for a
statement run of a few captions, or where the user's edit cuts away from their
face. They're time ranges in milliseconds:
`capsSections: [{ startMs: 4300, endMs: 7767 }]`.

### 8. Check, preview and render

1. Run `npx tsc` and `npx eslint src`.
2. Render stills at a plain caption, at an emphasis pair about 0.3s after its
   punch word, and at a caps section if there is one:

   ```bash
   npx remotion still Captioned out/check.png --frame=110
   ```

   Look at them. Each caption should be centred on the chest, the punch word
   should overlap the lower half of the setup word, and nothing should be
   clipped at the edges.
3. Open Studio for the user to scrub through (`npx remotion studio`, or follow
   the installed `remotion-studio` skill).
4. Render only when the user asks:

   ```bash
   npx remotion render Captioned out/captioned.mp4
   ```

## Lessons learned

- **Captions only.** The first build added layouts, camera moves, zooms and a
  B-roll card, and the user rejected all of it. Keep the footage untouched.
- **Fonts were identified by overlay, not by eye.**
  - Rendered candidates were scored against the reference glyphs. Inter Bold
    at its text optical size matched best (92%), ahead of SF Pro, Helvetica and
    Inter Display. `fontVariationSettings: "'opsz' 14"` keeps it on that cut at
    large sizes.
  - The ALL-CAPS face is Instrument Serif Italic with a synthetic bold, which
    is why it has an outline and a horizontal stretch.
  - The setup serif is DM Serif Display Italic. Its "2" has a ball terminal;
    Playfair's and Instrument's don't.
- **Gradient text** needs `background-clip: text` with a transparent fill. That
  breaks `text-shadow`, so shadows go on a wrapper as `filter: drop-shadow()`.
  Padding on the span keeps italic overhangs inside the clipped gradient.
- **`fitText()` measures with the loaded font.** `CaptionTrack` waits for the
  fonts (`useDelayRender`) before it lays out captions. Measuring early caches
  the wrong widths.
- **The punch overlap is deliberate.** With a 112px offset there was a visible
  gap; 74px matches the reference, where the punch covers the setup word's lower
  half.
- **The flicker runs on 30 beats per second**, not on frames, so it looks the
  same in a 60fps render.
- **Every word is captioned** except words absorbed into an emphasis pair, and
  everything after a `hold: "end"` pair.
- **Never put a dollar sign followed by a digit in this file.** When the skill
  is invoked with arguments (attached files, for example), the loader replaces
  each such token with an argument. An earlier version used one as a regex
  replacement string in `displayText`, and invoking the skill with a file
  attached broke every caption. `displayText` now uses a lookahead instead.
