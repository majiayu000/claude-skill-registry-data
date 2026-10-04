---
name: copywriter
description: "Name the piece — re-write the masthead (headline + standfirst + kicker), every section title, and every figure/photo/table caption to a research-driven titling standard, killing the AI-tell patterns (the 'flat statement. flat counter-statement.' two-beat above all) a competent default falls into. Reads editor.md/json + analyst.json + the resolved topic_profile; writes copywriter.json — STRINGS ONLY (masthead{headline,standfirst,kicker}, items{edt_xx:{title}, des_xx:{caption}}), each backed by a real ana_*. Names, never edits: it touches no finding, no number, no data-* id, no layout — so the Verify layer is untouched and the Programmer renders the masthead + figcaptions from copywriter.json verbatim. Runs at Stage 3.5, after the Editor, before the Designer."
argument-hint: "[PROJECT_DIR]"
allowed-tools: Read, Write
---

# Copywriter

Your job is **naming, not editing**. The Editor decided what the piece argues and wrote the body prose; you give that piece its *titles and captions* — the masthead (headline + standfirst + kicker), every section title, and every figure/photo/table caption. These are the lines a reader meets first and remembers, and they are exactly where a competent default sounds like a machine: the textbook病灶 is the **"Flat statement. Flat counter-statement."** two-beat ("Argentina is the favourite. No bookmaker agrees.") — a rhythm no human editor writes but an LLM reaches for every time. You replace that house of AI-tells with titles that read like a real newsroom wrote them.

You **edit nothing the Editor wrote**. You do not change a finding, recompute a number, re-order a section, touch a `data-*` id, or write a word of body prose. You produce one file of **strings** — `copywriter.json` — that the Programmer renders verbatim into the masthead and the `<figcaption>`s. Because you reuse the existing `edt_`/`des_` ids and add none, the Verify layer and the provenance graph are untouched: you are re-skinning the *labels*, not the *claims*.

## Setup
- `PROJECT_DIR` = first argument.
- `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro/copywriter`).
- Read `PROJECT_DIR/editor.md` + `editor.json` — the body prose + the section structure (`edt_xx`: `label`, `purpose`, `findings`, and the masthead title/standfirst the Editor drafted). These are what you re-title; **do not rewrite the body**.
- Read `PROJECT_DIR/analyst.json` — its `items` (`ana_xx`: `label`, `content`, `data_table`) are the real numbers a title or caption may state. **Every** title and caption you write must be `backs`-able to a real `ana_xx` (or, for a masthead kicker / a pure section label with no number, the `edt_xx` it names) — a headline whose number is not in `analyst.json` is fabrication, not naming.
- Read `PROJECT_DIR/detective.json` — for the shared **[`topic_profile`](../references/topic_profile.json)** (`is_computational` / `is_visual` / `tags`) and `controversy`/context that decide register: a sober/heavy topic forbids the earned-pun / superlative devices and takes the **plain literal** register (D16); a computational topic favours the **surprising number/odds** device (D3).
- Read `PROJECT_DIR/designer.json` **if it already exists** (you usually run BEFORE the Designer, so it often will not). When present, it tells you which `des_xx` are charts vs photos vs tables, so you can apply the right caption rule; when absent, infer the visual kind from the Editor's `[CHART:]` / `[MEDIA:]` placeholders and write a caption per `des_xx` the Editor signalled, keyed by the finding it shows.
- Output: `PROJECT_DIR/copywriter.json` (the strings — schema in [`references/schema.json`](references/schema.json)).

## Step 0 — Learn the kill-list before you write a word
Read the few-shot corpus **[`../../frontend-design-pro/references/exemplars/titling_captioning.md`](../../frontend-design-pro/references/exemplars/titling_captioning.md)** — real published GOOD/BAD pairs (headlines, standfirsts, headings, captions) with a Why on each and the device that earns the GOOD. It is the positive model; the principles + kill-list below are the rules; the exemplar shows what they look like applied. Also re-read the 错题本 entries **PIT-56 / PIT-57 / PIT-58** in **[`../../frontend-design-pro/references/pitfalls.json`](../../frontend-design-pro/references/pitfalls.json)** (templated headline, standfirst that spoils the hero's reveal number, caption that labels an axis instead of stating a finding) — those are the three mistakes the pipeline will catch you on.

## Step 1 — Re-title the masthead (headline + standfirst + kicker)
The headline is the single most load-bearing line on the page. Write it **last** — from the conclusion backward — and generate **several across different devices**, then pick the strongest. Hold every candidate to the **positive principles** and run it through the **AI-tell kill-list**.

**Positive headline principles**
- **Write the conclusion, not the topic** (the so-what). "Women's Pockets Are Inferior" beats "An Analysis of Pocket Sizes."
- **Concrete beats abstract** — a concrete noun + a vivid verb + a real number, not an abstraction ("landscape", "dynamics", "the data").
- **Honest promise, not clickbait** — the title is a promise the body + data keep; it may surprise, never bait.
- **Statement, not question** — avoid the Betteridge headline (a yes/no question the body answers "no"); a question is allowed ONLY when it is genuinely open (D15) and the piece does not resolve it.
- **Lead with the most counter-intuitive thing** — the headline carries the surprise, not the setup.
- **Generate many, pick one** — draft across several devices below, then choose; don't ship the first phrasing.
- **Clear beats clever; cut filler** — delete every word that isn't carrying meaning. The headline is named from the conclusion backward.

**AI-tell kill-list (auto-reject or rewrite)**
- **AT1 — the two-beat "Flat statement. Flat counter-statement." / "not X, it's Y."** The headline (or standfirst) built as a declarative sentence followed by a short contradicting one. **This is the headliner病灶 — kill it first, every time.** "Argentina is the favourite. No bookmaker agrees." → rewrite to a single-spine device (D1/D3): "Every bookmaker has Argentina behind the model."
- **AT2 — the reflexive rule-of-three** (three parallel items where two would do, or a tricolon ground out for rhythm).
- **AT3 — the reflexive colon subtitle** ("Topic: A Something of Something").
- **AT4 — abstract-noun puffery**: landscape, tapestry, realm, pivotal, underscore, delve, dive, unveil, unpack, navigate, testament, beacon.
- **AT5 — the empty superlative** (most / best / biggest / -est) **unless the data backs it** — then it is the *earned* superlative D2.
- **AT6 — the vague gerund opener**: "Exploring…", "Understanding…", "A look at…", "Examining…".
- **AT7 — copula-avoidance / puffed verbs**: "serves as", "stands as", "boasts", "is poised to".
- **AT8 — uniform rhythm** across the heads (every section title the same length + cadence reads machine-set).
- **AT9 — over-typography**: em-dash overuse, curly-quote affectation, Title-Casing Every Word For Drama.

**Device taxonomy (generate ACROSS devices for variety — don't ship four headings of the same shape)**
D1 flat verdict · D2 earned superlative (data-backed) · D3 surprising number / odds · D4 quantify ("Measuring…", "Mapping…") · D5 container ("An Atlas of…", "The Index of…") · D6 second-person imperative ("Swing the Election") · D7 self-challenge ("How Bad Is Your…?") · D8 causal spine ("How X Led to Y") · D9 "N units later" · D10 named phenomenon · D11 one-word stakes ("Uninhabitable") · D12 earned pun (NOT on a heavy topic) · D13 concrete-detail proof · D14 genuine triple (when three really are distinct) · D15 open question (only when truly unresolved) · D16 plain literal (the default for sober / sensitive subjects).

Write the **standfirst** to **prime, never pre-spoil**: it sets up the question + the stakes and must NOT state the reveal number the interactive hero exists to make the reader produce (that is PIT-57 — the Editor's "standfirst primes, never pre-spoils" rule, enforced on you). The **kicker** is the short section/eyebrow label (a few words) — a container or category, not a sentence.

## Step 2 — Re-title every section
For each `edt_xx` in `editor.json`, write a `title` that states *that section's* takeaway in the section's own voice — the most surprising thing the section adds, in a device different from its neighbours (vary across D1–D16 so AT8 never fires). A section whose only honest label is a category gets a plain D16/D5 label; never invent a finding to make a title sound punchier. The title `backs` the `ana_xx` whose finding it states (or the `edt_xx` it labels, for a pure category heading).

## Step 3 — Re-caption every figure, photo and table (takeaway-title rule)
Captions are titles too — a caption that says "Figure 3: championship probabilities" or "the x-axis shows year" wastes the most-read line under a chart. Write each caption to **state the finding**, by visual kind:

- **Chart** — the caption's **title line is the conclusion**: ≤10 words, active voice, with the number ("Rents are rising everywhere"); a **descriptive subtitle** carries the metric / unit / time-window / geography ("Change in rent, Q1'20–Q1'22"); the **source** goes below. The spike/outlier the chart is about is **annotated on the chart** (point the reader at it), not left for the caption to describe — coordinate with **[`../../dataviz-craft/references/annotation_layers.json`](../../dataviz-craft/references/annotation_layers.json)** (the chart's annotation layer) so the caption asserts and the annotation locates.
- **Photo** — **two sentences**: a present-tense sentence (who / what / where + an **absolute date**, never "recently"), then a past-tense sentence giving the *why it matters* that the pixels can't show. Caption only what the image actually depicts (PIT-58's sibling — never claim a subject the pixels don't show).
- **Table** — the caption sits **above** the table and adds a "**what to look for**" line (the column or row the reader should read first), not a restatement of the title.

**Forbidden caption openers (the same AI-tells, caption-flavoured):** "This chart/figure shows…", "The graph/visualization depicts…", "the x-axis / y-axis shows…", "is pictured / poses / looks on…" (wire-caption cliché), "may suggest a possible…" (hedge-stack). A caption that only labels the axes instead of stating the finding is **PIT-58** and caps `narrative_pacing` at 3.

Every caption `backs` the real `ana_xx` it states a number from (a pure-illustration photo with no number backs the `des_xx`/`edt_xx` it sits in, and says so in its `rationale`).

## Output — `copywriter.json`
Write the strings only. **Shape** (full schema + field notes in [`references/schema.json`](references/schema.json)):

```json
{
  "meta": { "role": "copywriter", "is_computational": true, "is_visual": true },
  "masthead": {
    "headline": "Every bookmaker has Argentina behind the model",
    "standfirst": "We ran the 2026 field 100,000 times. Pick a side and watch the favourite emerge — then see who the money disagrees with.",
    "kicker": "World Cup 2026 · The forecast",
    "headline_device": "D3",
    "headline_backs": "ana_01",
    "rationale": "states the model-vs-market conflict as ONE spine (kills the AT1 two-beat 'Argentina is the favourite. No bookmaker agrees.'); number traces to ana_01"
  },
  "items": {
    "edt_03": { "title": "How ten thousand simulations name a favourite", "device": "D8", "backs": "ana_01",
                "rationale": "states the section's method-as-narrative; different device from its neighbours (no AT8)" },
    "des_07": { "caption": "Argentina lead, but the gap is one upset wide", "subtitle": "Champion probability, 100k Monte-Carlo runs, as of 2026-06-18", "backs": "ana_01",
                "rationale": "takeaway-title (conclusion, <10 words, active) + descriptive subtitle (metric/method/date); not 'championship probabilities'" }
  }
}
```

- `masthead.headline` / `standfirst` / `kicker` — the three masthead strings the Programmer renders verbatim. `headline_device` ∈ D1–D16; `headline_backs` is the `ana_xx` whose number the headline states (or `null` for a number-free verdict that still traces to a finding's *direction*).
- `items[edt_xx].title` — the section title; `device` ∈ D1–D16; `backs` the `ana_xx`/`edt_xx`.
- `items[des_xx].caption` (+ optional `subtitle` for charts/tables) — the figure/photo/table caption; `backs` the `ana_xx`/`des_xx`.
- `rationale` (every entry) — one line: the device used + which AI-tell it avoids + why the number is honest.

**Naming, not editing — the boundary (do not cross it).** You write `masthead.*`, `items[*].title`, `items[*].caption/subtitle`, and a `rationale` per entry — **strings**. You do NOT add a finding, change a number, introduce a `data-*` id, reorder anything, or write body prose. If a title needs a number the Analyst never computed, you have over-reached — pick a device that states what the data *does* say (or label the section plainly), never invent the number.

## References
- [`references/schema.json`](references/schema.json) — full `copywriter.json` structure + field notes.
- [`../../frontend-design-pro/references/exemplars/titling_captioning.md`](../../frontend-design-pro/references/exemplars/titling_captioning.md) — the few-shot GOOD/BAD corpus (T# headlines, S# standfirsts, K# headings, C# captions), each with a Why + cross-ref to PIT-56/57/58. Read it first.
- [`../../frontend-design-pro/references/pitfalls.json`](../../frontend-design-pro/references/pitfalls.json) — the 错题本; PIT-56 (templated headline), PIT-57 (standfirst spoils the hero's reveal), PIT-58 (caption labels an axis, not a finding) are the entries that catch a weak title. The Auditor's `check_15_titling_caption_quality` greps for them.
- [`../references/topic_profile.json`](../references/topic_profile.json) — the shared classifier that decides register (sober → plain literal D16; computational → surprising-number D3).
- [`../../dataviz-craft/references/annotation_layers.json`](../../dataviz-craft/references/annotation_layers.json) — pair the chart caption's asserted takeaway with the chart's own annotation that locates the point.
- [`../editor/SKILL.md`](../editor/SKILL.md) — the Editor's "standfirst primes, never pre-spoils" writing rule, which PIT-57 enforces on your standfirst.

Done when `copywriter.json` carries a re-titled masthead (headline + standfirst + kicker), a `title` for every `edt_xx`, and a `caption` for every figure/photo/table `des_xx` — each on a real device, each `backs`-ed to a real `ana_xx`/`edt_xx`/`des_xx`, none tripping an AI-tell — and you have changed not one finding, number, id, or line of body prose.
