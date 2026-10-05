---
name: storyboard-html-preview
description: Render a shotkit storyboard (shots.json, text-overlays.json, brand-lock.snapshot.md) into one self-contained HTML preview that a reviewer can open, share or print. Use when the user asks to preview, share, export or print a storyboard or shot list, for example "preview the storyboard", "share this storyboard", "export the storyboard to HTML" or "a print version of the shot list". A request to share, export or print something that is not a storyboard is not for this skill. It runs when the user asks for it; storyboard-architect offers it and does not start it.
---

# Storyboard HTML Preview

You are turning structured storyboard files into a single shareable HTML document. The output is what an editor, stakeholder, or client opens in a browser without thinking about it.

The constraint is non-negotiable: **single file, no build step, no server, works offline.** Any time the output requires "run this build command" or "host this somewhere," the skill has failed.

## When to use

Trigger when the user:

- Asks to preview, share, or export a storyboard or shot list
- Wants a printable version of a storyboard
- Says yes when storyboard-architect offers a preview
- Hands off `storyboard.md` + `shots.json` + asks for a deliverable for review

Share, export and print requests about anything else are not for this skill. It does not
start on its own after a storyboard-architect run; the architect offers it and the user
picks.

## Where the tools and packs are

After `./install.sh`, the validators and helpers are in `~/.claude/shotkit-tools/` and the
brand packs are in `~/.claude/shotkit-brand-packs/`. A `--project` install puts both
under `./.claude/` instead. From a repo clone they are `tools/` and `brand-packs/`. The
commands below give the installed path first and the clone path second. The tools need
`pip install pyyaml jsonschema`.

## What you produce

One file: `preview.html`. Self-contained. Inline CSS. No JavaScript dependencies (vanilla JS only, embedded). The brand fonts are linked from Google Fonts, with a system fallback stack behind each one, so the page reads the same offline in the fallback fonts. No external images (placeholder slots; if generated images exist, embed as base64 OR reference relative paths).

```
output/
├── run.json                   # input, for the run id and date
├── storyboard.md              # input
├── shots.json                 # input
├── text-overlays.json         # input
├── brand-lock.snapshot.md     # input
├── frames/round-N/            # input, if generation has happened
├── critiques/round-N/         # input, for the verdict badges
└── preview.html               # ← what this skill produces
```

If the user has generated frames, the HTML references them via relative paths so the file
works when the whole `output/` folder is shared. Resolve a shot's frame in this order:

1. An entry in `shot.assets.generated` marked `accepted: true`
2. The newest entry in `shot.assets.generated`
3. `frames/round-{highest}/{shot_id}.{png,jpg,jpeg,webp}`
4. `generated/{shot_id}.{ext}`, the pre-3.0.0 flat layout

Data first, convention second. The data says which frame was accepted; the path convention
only says which file sits in the folder.

If no frames exist yet, the HTML uses styled placeholder cards with the shot spec, still
useful for review and handoff.

## Workflow

### Step 1. Read inputs

Required:

- `shots.json`
- `text-overlays.json`
- `brand-lock.snapshot.md`

Optional:

- `run.json` (for the run id and date; without it the page says "not recorded")
- `storyboard.md` (for narrative context, surface the brief at the top)
- `frames/round-N/{shot_id}.{png,jpg,jpeg,webp}` (if generation has happened)
- `critiques/round-N/{shot_id}.critique.json` (for verdict badges)

Validate before rendering, and stop if it fails:

```bash
python ~/.claude/shotkit-tools/validate_shots.py output/
# from a repo clone:
# python tools/validate_shots.py output/
```

### Step 2. Extract brand parameters

From `brand-lock.snapshot.md`, extract:

- Palette (hex values), mapped by role onto the CSS variables
- Display, body, and mono fonts
- Brand voice / mood, used in subtle copy choices

A font value in a brand-lock carries more than a family, for example
`Archivo Bold 700 wdth 80`. Split it before it goes into CSS:

- the family (`Archivo`) goes into `font-family`, in quotes, ahead of a system fallback
  stack: `"Archivo", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- the weight (`700`, or a name such as `Bold`) goes into `font-weight`
- a width (`wdth 80`) goes into `font-stretch` as `80%`

Writing the whole value into `font-family` makes the declaration invalid, and the page
renders in the browser default. Use the brand-lock's mono font for labels, ids and
timings. When it declares none, use the system mono stack.

The HTML preview should *feel* like the brand without going overboard. Quiet branding, not loud.

### Step 3. Generate the HTML

When the tools are installed, render with the CLI. It does every step below and writes
`preview.html` into the output folder:

```bash
python ~/.claude/shotkit-tools/shots-to-html.py output/
# from a repo clone:
# python tools/shots-to-html.py output/
```

Build the page by hand, following the steps below, only where the tools are not available
(for example a Claude.ai upload).

Use `templates/preview.html.tpl` as the structural template. Read it before generating.

The HTML structure:

```
<!DOCTYPE html>
<html>
<head>
  <meta>
  <title>{project title}</title>
  <style>
    /* All CSS inline. ~200 lines. Brand-aware. */
    /* Print stylesheet included. */
  </style>
</head>
<body>
  <header>
    <!-- Project title, duration, aspect, generated timestamp -->
  </header>

  <section class="brief">
    <!-- Brief summary if storyboard.md provides one -->
  </section>

  <section class="series-lock">
    <!-- Character / environment / lighting / color grade -->
  </section>

  <section class="shots">
    <!-- One card per shot -->
    <article class="shot" id="shot_01">
      <div class="shot-frame">
        <!-- generated image OR styled placeholder -->
      </div>
      <div class="shot-meta">
        <!-- timestamp, framing, angle, motion -->
      </div>
      <div class="shot-subject">
        <!-- subject description -->
      </div>
      <div class="shot-text-overlay">
        <!-- if on_screen_text exists, show overlay content with timing -->
      </div>
      <div class="shot-rationale">
        <!-- rationale text -->
      </div>
    </article>
    <!-- ... -->
  </section>

  <footer>
    <!-- audit trail: brand-lock snapshot reference, timestamp -->
  </footer>

  <script>
    /* Vanilla JS only. Optional: keyboard nav, jump-to-shot, expand/collapse. */
  </script>
</body>
</html>
```

### Step 4. Embed frames if available

Resolve each shot's frame by the order in "What you produce" above, then reference it by a
path relative to the output root:

```html
<img src="frames/round-2/shot_01.png" alt="shot_01: hook" loading="lazy" />
```

This works when the whole output folder is zipped and shared.

For hard-copy print (a single file with no folder structure), the skill can offer to inline
frames as base64. Ask the user which they prefer if frames are present.

If a shot's `assets.generated` entry carries a `sha256` and the file no longer matches it,
render the frame but say so on the page. That mismatch means the frame changed after it was
recorded, which is exactly the case where a preview quietly showing the new file is worse
than one that flags it.

If no frames exist, render styled placeholder cards showing the framing, subject, and shot
spec. These are still useful for stakeholder review at the storyboard stage.

**Template flag convention.** When composing the per-shot context for `preview.html.tpl`, set exactly one of:

- `has_image: true` and `image_path: "frames/round-2/shot_NN.png"`, when a frame exists
- `has_no_image: true`, when none does (renders the placeholder card)

The template uses two parallel `{{#if}}` blocks rather than `{{#if}}/{{else}}` to keep the rendering portable across template engines.

For text overlays, set `has_overlays: true` and an `overlays` array on the shot. Each entry
carries `id`, `content`, `font`, `weight`, `color`, `size`, `position_class`,
`position_label`, `enter_at`, `enter_animation`, `exit_at`, `exit_animation`. The template
iterates that array with `{{#each overlays}}`.

It is an array because `shots.json` and `text-overlays.json` both let a shot carry several
overlays, and every one of them has to render.

For verdict badges, set `has_verdict`, `verdict`, `verdict_round`, and `verdict_class`
(the lowercased verdict) from the newest critique for that shot under `critiques/`. Omit
them when the shot has no critique.

**Escape everything.** Subjects, rationales, VO lines, and overlay copy are model-generated
prose that lands in both text and attribute contexts. One angle bracket in a rationale, or
one quote in an overlay font name, breaks the page a client is reading.
`shots-to-html.py` escapes every substitution by default and reserves raw output for
the inlined CSS alone.

### Step 5. Render text overlays visually

For every shot with an `on_screen_text` reference, the HTML shows:

- The text content rendered in approximately the brand font (or visible fallback)
- The position indicated visually (lower-third, center, etc.)
- Timing info (enter/exit beats)

This gives the reviewer a sense of what the final composited frame will look like, even before final compositing happens.

### Step 6. Print stylesheet

Include `@media print` rules that:

- Hide nav, footer scripts, expand/collapse UI
- Force one shot per page (or two if compact)
- Ensure text overlays render legibly
- Use black-on-white where brand colors won't print well

The user should be able to hit Cmd-P / Ctrl-P and get a clean PDF.

## Hard rules

### Rule 1. Single file, no exceptions

The output is one `.html` file. If you find yourself wanting a separate stylesheet or JS file, inline it. If you find yourself wanting a build step, you're solving the wrong problem.

### Rule 2. No external dependencies at runtime, except the brand fonts

No CDN scripts. No external CSS frameworks. The file must work with no internet connection.

One exception: the page links the brand's fonts from Google Fonts, one stylesheet per
family, so a reader who is online sees the real typefaces. Offline, or for a family
Google does not host, each font falls back to the system stack named after it and
nothing else on the page changes. When the user wants a page that makes no network
request at all, leave the links out (`shots-to-html.py --no-web-fonts`).

### Rule 3. Print must work

Hit Cmd-P. The result should be a clean PDF. If layout breaks across page boundaries, the print stylesheet is broken.

### Rule 4. Brand-aware but quiet

The palette's `background` role is the page background, and its `ink` role is the text.
For a dark brand that means a dark page: its ground is its background, not an accent,
and a light page would not look like the brand. Every other color is an accent: a
rule, a label, a badge, an id. Never flood a section with the accent color. The
reviewer's job is to read the storyboard, not admire the design.

### Rule 5. Mobile-readable

Stakeholders open links on phones. The HTML should be readable on mobile without horizontal scroll. Simple responsive CSS.

## Templates

- `templates/preview.html.tpl`, the structural template
- `templates/styles.css.tpl`, the CSS to inline
- `templates/print.css.tpl`, the print rules

The skill reads all three and assembles them into a single `preview.html`.

## Quality bar

Before declaring done, verify:

- [ ] File opens in any browser (Chrome, Safari, Firefox) with no errors
- [ ] The only network requests on load are the Google Fonts links, and there are none
      with `--no-web-fonts`
- [ ] Print preview produces a clean PDF
- [ ] Mobile viewport (375px) renders without horizontal scroll
- [ ] Brand colors and fonts come from the brand-lock, not from a fallback
- [ ] Every shot from `shots.json` is present
- [ ] Every overlay referenced by a shot is rendered, including second and third overlays
- [ ] `brand_lock_ref` from `shots.json` is what the footer links to, not a hardcoded name
- [ ] The run date and the render date are both shown, and labelled differently
- [ ] No `{{` remains anywhere in the output

The CLI renderer checks the mechanical half of that list against itself:

```bash
python ~/.claude/shotkit-tools/shots-to-html.py --selftest
# from a repo clone:
# python tools/shots-to-html.py --selftest
```

## Two timestamps, not one

"Run" is when the storyboard was produced, read from `run.json`. "Rendered" is when the page
was written. They are separate lines in the footer and they must stay separate.

A single "Generated" date would restamp the run as today every time the page is
re-rendered, and the footer would name a brand-lock date that has nothing to do with the
frames above it.

If the brand-lock on disk no longer hashes to what `run.json` recorded, say so on the page.
The reader is looking at frames built against a brand state they can no longer see.

## Examples

Generated `preview.html` files ship next to the storyboards that produced them:

- `../storyboard-architect/examples/30s-pain-proof-promise/preview.html`
- `../storyboard-architect/examples/60s-founder-explainer/preview.html`
- `../visual-asset-critic/examples/worked-run/preview.html`, with frames and verdict badges

Open them in a browser to calibrate quality. All three are re-rendered in CI with pinned
timestamps and the build fails if the output moves, so they are also the regression test for
this skill's output.
