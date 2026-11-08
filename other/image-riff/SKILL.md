---
name: image-riff
description: Turn one or more reference images into original art in that reference's own visual language, then cut it to whatever surface it's for. Use when you paste or point at art and say "use this as the base image", "generate art from this", "riff on this", "some creative ideation with these images", "make me a channel banner / avatar / cover / plate", "wilder version of this", or want a spread of options off one piece of reference. This is the TASK skill; the engine is the `make-art` tool skill.
---

# image-riff — original art in a borrowed visual language

The engine, its API key, its flags and its gotchas live in the **`make-art`** skill.
Read that first. This skill is the *method*: how to turn a reference image into a set of
real options, and how to land them on the surface they're actually for.

**Done** is not four pretty images. Done is: N plates generated, every frame looked at,
ranked with honest critique, **the destination crops cut**, and the work landed in the
source folder below. A run that stops at "here are four images" hands the user the last
two jobs.

## Where the work lands

```
art/<source-slug>/
  README.md                 dated title, the brief, a rank -> plate table, and WHY the pick won
  1-<slug>.jpg ...          the finals, full-resolution masters, numbered BY RANK
  upload-1024/              the actual sized deliverables, when the surface needs a specific size
  small-size-test.png       the proof, when legibility at size decided it
  prompts/                  the finals' prompts exactly as sent
  candidates/<round>/       the rounds that lost, each with its own prompts/
```

`<source-slug>` is the body of work, not the date. If sibling folders already exist,
match their convention.

- **The README is not optional.** The folder gets reviewed cold, weeks later. Without it
  a folder of numbered JPEGs can't say which one shipped, which was rejected, or why.
- **Keep the losing rounds.** `candidates/` is where the reusable knowledge is.
- **Keep the prompts verbatim.** They're the reproduction instructions and the provenance.
- **Number the finals by rank, not by generation order.** The filename is where the
  ranking survives after the conversation is gone.
- Keep generated art out of a personal photo library unless asked; it mixes with real
  photographs.

## Ask two questions, then spend

At roughly $0.24 per 4K image, a four-plate spread is about $1: cheap enough that two
questions is the whole gate, expensive enough that zero questions is a waste. Both
answers change every plate, so neither can be inferred:

1. **What is it for?** Decides aspect, and whether to leave negative space for type.
2. **How far from the base?** Faithful reproduction <-> wild reinterpretation.

Ask on the subjective axis; decide the technical one yourself.

## The prompt is three parts, and only one of them varies

Build it in code, one file per subject:

```
STEM    (identical for every plate)  — the rendering language, read off the image
SUBJECT (the only variable)          — one paragraph, one composition
TAIL    (identical for every plate)  — geometry + the negatives
```

A STEM template, as *moves* rather than words:

> Use the attached image strictly as the style and colour anchor. Reproduce its exact
> rendering language: **<period + medium>**, **<how colour is laid down>**, **<line
> behaviour>**, **<texture / shading technique>**, **<named pigments, 2-3 max, plus the
> small accent>**, **<what the light does>**. **Do NOT copy the subject of the attached
> image. Compose something new.**
>
> SUBJECT:

And the TAIL:

> <aspect> composition, full bleed edge to edge. No border, no frame, no paper texture,
> no white margin. No text, no lettering, no signature, no logo.

**A photographic base is the harder case: probe at 2K before spending on a spread.**
"Reproduce the rendering language, change the subject" reliably yields art from a
stylized base (a comic panel, a print). From a photograph it can execute perfectly and
still disappoint. Ask a third question when the base is a photograph — *should this end
up looking like a photograph, or like something else?* — and spend one or two 2K plates
before four 4K ones.

**When the base is a photograph, the STEM's slots change but its job doesn't.** Swap the
mark-making slots for the six things a camera decides: *<stock + format>, <shadow
response>, <quality and angle of light>, <palette, 3-4 named colours plus the one
accent>, <grain / halation / vignette>, <what it is NOT>*. The last slot matters most,
because the engine's default for any photographic prompt is contemporary digital: say
*no HDR, no lifted shadows, no digital clarity, no cinematic teal-and-orange grade*. A
clause like **"deep crushed blacks that hold no shadow detail at all"** can be the most
load-bearing line in the prompt.

Also read the base for its **implied subject**, not just its rendering (e.g. *a private
place, seen from above, with nobody in it*). Name it in one sentence before writing any
SUBJECT; put invariants like `no people visible anywhere in the frame` in the TAIL.

Why it's built this way:

- **The image carries the style; the STEM only names what is visibly there.** Describe
  the mark-making you can see — *hard black contour lines of varying weight, visible
  ben-day halftone dot shading, airbrushed mechanical blends only, no photographic
  light*. Naming the technique stops the model modernising it.
- **"Do NOT copy the subject... compose something new" is load-bearing.** Without it you
  get a variation of the base. With it you get original compositions in the base's
  language, and the best of them *quote* the base rather than repeat it.
- **Name pigments, and cap the accent.** Say "small" about the accent specifically, or it
  takes over the frame.
- **The negatives are not boilerplate.** The engine adds a paper/riso border on its own
  initiative; four negatives in the TAIL cost nothing.
- **Identical STEM + TAIL makes the set comparable.** Every difference between plates is
  one you asked for.

## The subjects must be VANTAGES, not decorations

The single most important creative decision. Four subjects that differ in *where the
camera is*:

| plate | vantage | example |
|---|---|---|
| spire | looking straight **up** a vertical axis | a tower rising out of a cloud sea, narrowing into perspective |
| wreck | looking **across** an empty plain | a half-buried wreck, one tiny figure walking to it |
| descent | looking steeply **down** through cloud | an ocean of plates to a curved horizon, one figure falling away |
| mandala | looking **at** pure pattern, no horizon | a symmetrical rosette, corner to corner |

Plates ship *for their vantage*: a vertical column survives a letterbox banner crop; a
single silhouette against sky survives a square avatar crop. Four plates that differ only
in furniture all crop the same way — one option in four costumes. One idea per plate.

## Rank against the brief — then say which one each SURFACE wants

Two separate orderings. Rank honestly against the base and name the plate that drifted;
then add one line per destination surface saying which plate that surface wants and why
the crop makes it so. The plate you rank last on fidelity can be the right banner. A low
rank is not a veto; it's one axis.

## Cut the crops. Every surface has a geometry.

Deliver files sized for the destination, not source plates.

**YouTube channel banner** — one 16:9 upload; YouTube serves a different slice per device.
- Stored / TV: **2560x1441**.
- Desktop strip: **2560x424**, the vertical **middle ~29.4%** (top 35.3% -> bottom 64.7%).
  Everything that must be seen lives in that band.
- A tall 9:16 plate has ~3x the height a 16:9 crop needs: pick the band, don't accept the
  middle by default.

**Channel avatar** — square, served from 900x900 down to **88x88**. Judge at 88px.

To read back what a channel actually serves:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
curl -sL -A "$UA" "https://www.youtube.com/@<channel>" | grep -o '"banner".\{0,400\}'
# the fcrop64 hex is four 16-bit fractions of 0xffff: left, top, right, bottom
python3 -c "h='00005a57ffffa5a8'; print([round(int(h[i:i+4],16)/0xffff,4) for i in range(0,16,4)])"
```

For other surfaces, measure the real served asset before cropping; don't trust a
remembered spec sheet.

## Mechanics

- **A pasted base image is not on disk.** Extract it from the session transcript's base64
  (`make-art` has the snippet), then look at it before spending a 4K gen on the wrong image.
- **Generate the spread in parallel**, one shell call per plate. Four 4K plates land in ~2 minutes.
- **`--out foo.png` can write a JPEG.** Check the printed mime and rename.
- **Look at every frame yourself before the user does**, and probe for the paper border
  rather than eyeballing it: asymmetric near-white edge runs are sky or cloud hitting the
  bleed, not a frame.

## When there is no base image

The same three-part prompt works with no anchor: the STEM becomes a house style you
*define*. Give it a thematic anchor from the user's own material (a quote collection, a
mood board) so it isn't generic.

## Icons and avatars: the small-size test is the only test

The ranking can **invert between full size and real size**. Build the contact sheet before
you have an opinion: downscale to true render size, circle-crop like the app does, then
nearest-neighbour upscale to see what survives.

```python
from PIL import Image, ImageDraw
for s in (110, 44, 32):                      # IG: profile / DM row / feed+story ring
    small = Image.open(f"{n}.jpg").convert("RGB").resize((s, s), Image.LANCZOS)
    mask = Image.new("L", (s*4, s*4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s*4-1, s*4-1), fill=255)
    out = Image.new("RGB", (s, s), (245, 245, 247))
    out.paste(small, (0, 0), mask.resize((s, s), Image.LANCZOS))
    out.resize((s*5, s*5), Image.NEAREST).save(f"{n}_{s}.png")   # NEAREST = see the pixels
```

A gorgeous plate at 110px can be an unreadable smear at 44px. **Instagram geometry:**
upload square (1024x1024 works), rendered as a **circle**, ~110px on the profile, 44px in
a DM row, 32px in a feed or story ring. Judge at 32.

Four constraints that make the difference, all invisible at full size:

1. **Three flat colours, and no more.** Every extra colour is a mid-tone, and mid-tones merge.
2. **Nothing thinner than 1/40 of the frame.** Say it in the prompt as a number.
3. **The emblem must fill >=85% of the width.** State it in caps; otherwise the engine
   centres a modest mark in a lot of empty ground.
4. **The hot colour belongs to the GROUND, not to a glint.** A specular highlight is worth
   nothing at 32px; a full flat field of a hot colour stops a thumb. Metallic-sheen
   instructions read as mud when shrunk.

## Two things the engine adds on its own initiative

- **Never mention the circle crop in the prompt.** It will *draw the circle*. Say instead:
  *"flat unbroken ground runs all the way to all four edges of the square; the emblem is
  contained well within the central three quarters"*, and put `no circle, no ring, no
  roundel, no enclosing shape` in the TAIL.
- **It adds a radial vignette unless forbidden.** Demand *"every fill absolutely flat — no
  gradient, no vignette, no radial darkening at the corners or edges."*

## Never credit the base image from a style description

A style phrase you wrote ("in the Moebius tradition") is not an attribution; don't let it
become a credit downstream. If a credit is going anywhere public, ask for the real artist.
A wrong credit on a real artist is worse than a blank.

## More than one base image

`--image` is repeatable, so multiple anchors are possible but less tested. Say in the
prompt which image supplies what ("image 1 is the colour and line language; image 2 is
the structure") and treat the first spread as a probe.

## See also

`brand-direction-plates` (the inverse spread: several LANGUAGES across one subject) ·
`make-art` (the engine, the flags, the paste extraction, the border probe).
