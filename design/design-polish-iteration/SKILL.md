---
name: design-polish-iteration
description: "Render→look→diagnose→fix loop for making a live web UI look right, judged from rendered pixels instead of class names/tokens, edited in place. Use when a layout is called tight/cramped/loose/off/unbalanced/plain/dated, after any UI/CSS change that must look right, when the user says 'polish this page' or wants the look leveled up (optionally toward codex-imagegen north-star mockups), or when the user hands over a visual reference (annotated screenshot, mockup, 'make it match this') — then the reference is the spec and success is a diff against it."
user-invocable: true
argument-hint: "[count] [route-or-url] [-n <directions>] [--no-imagegen] [--target <image>] [--cleanroom]"
---

# Design Polish Iteration

You edit the top of the chain (`token → utility → responsive variant → flex/grid → content → browser layout`); the look only exists at the bottom. Judging spacing from tokens produces confident, wrong results. So: render, look at the pixels, diagnose in design terms mapped onto the project's token scale, fix, look again.

**Routing:** this skill edits the live page in place and ends there. If the accepted design must then be *built* (epic + sub-issues), or the ask is alternative directions rather than refinement, use `/big-plan -pr`. If exploration itself is the deliverable, use `/protodev`.

## Three modes

| Mode | Trigger | Judged against |
| --- | --- | --- |
| **Diagnose** | "tight", "off", a CSS change needs to look right | design principles you supply (below) |
| **Reference-match** | user supplies a reference image, or `--target <image>` | the reference bitmap — fidelity, not taste |
| **Polish** | "polish this", "level up the look", plain/dated/flat | a north-star mockup (fuzzy reference) |

## Arguments (polish mode)

- **count**: polish rounds, default **2**.
- **route-or-url**: page to polish; if omitted, infer the single obvious WIP route or ask.
- **-n <directions>**: north-star mockups generated up front, default **2**.
- **--no-imagegen**: no mockups; self-judged diagnose loop only (free, but only nudges the current look).
- **--target <image>**: supplied image is the north-star; skips imagegen.
- **--cleanroom**: implement in a `/protodev` prototype, then port back deliberately. For directions that would fight the existing markup; default is in-place.

## Core principle

**Spacing encodes grouping. Bind tight, separate loose. The ratio between hierarchy levels is the design — not the absolute size.**

- "Tight" usually = too little contrast (all gaps similar → uniform wall). Fix: raise *separators* (between-group, around-heading); keep or tighten binders.
- "Loose" usually = oversized binders (within-group gaps dissolved the group). Fix: shrink the binders.
- Never uniformly scale a hierarchical layout.
- On larger viewports, escalate separators, hold binders.

Full vocabulary, symptom→cause→fix cheatsheet, mobile reflow failures, and the gap-measuring snippet: [references/design-knowledge.md](references/design-knowledge.md) — load it at the Diagnose step.

## The loop

### 0. Context

- **Token source:** a project `*design-system*` / `*design-tokens*` skill or doc (e.g. `/l-design-system`) defines allowed values. Never invent raw px/rem/hex where a token exists; with no system, the values already in the codebase are the de-facto scale.
- **Polish mode:** load `/css-wisdom` tight-token articles up front — `methodology/design-systems/tight-token-strategy/index.mdx` and `component-tokens.mdx`, plus `color-tokens.mdx` / `typography-tokens.mdx` / `token-preview.mdx` as needed.
- **Server:** find the dev/serve command and port; reuse a running server, don't spawn a duplicate. Note any auth cookie/header for gated previews.

### 1. Capture

`/headless-browser` screenshots at **~390 / ~760 / ~1300px** — one width misleads. **Capture the worst case, not the page top:** the longest title / most wrapping text, the longest list, AND the shortest near-empty group, at the narrowest viewport. Read every PNG.

### 2. Propose north-star directions (polish mode, unless `--no-imagegen` / `--target`)

A model handed the source over-anchors on it and "polish" collapses back to the original; a mockup generated from the *screenshot* breaks that anchor. Feed the baseline (usually desktop) to `/codex-imagegen`, once per direction:

```bash
$HOME/.claude/skills/codex-imagegen/scripts/codex-imagegen.sh \
  --in <baseline-desktop.png> --out direction-1.png \
  --prompt "Polished, premium redesign of this screen. Keep the same content, structure, and information. Elevate spacing rhythm, typographic hierarchy, color, depth, and detailing. Modern, restrained, on-brand — not generic AI gradient slop."
```

Vary the brief per direction ("editorial / high-contrast", "calm / airy", "denser / utilitarian"). Show the mockups and **let the user pick** — a taste call.

**Cost:** each mockup is ~90k–230k ChatGPT tokens. Generate once up front, not per round; re-invoke only for a new direction or a plateau.

**A mockup is direction, not spec.** It hallucinates text, numbers, and components. Match its intent (rhythm, hierarchy, palette, treatment); take content from the live page. An arbitrary `#hex` or `13px` to "match the mockup" is a regression even if it looks closer — find the token.

### 3. Look, then measure

- **Look** at each width: where do groups blur, what floats apart, what is misaligned or heavy. With any reference, looking is comparative — crop your render to the reference's framing and diff element by element; never judge your render alone.
- **Measure** close calls: real rendered gaps via `/verify-ui` or the bounding-box snippet in the reference file, then check the invariants below.
- **Never report a color or exact value from looking.** `rgb(214,211,209)` and `rgb(255,255,255)` look identical on a dark background; same for 1px vs 2px, opacity, near-miss alignment. Query `getComputedStyle(el)` — authoritative for any real element. If the user insists a value is wrong and you "can't see it," that is the tell: stop looking and sample.
- **Pixel sampling is the fallback** (pseudo-element, box-shadow, image, gradient, antialiased edge), and the harness lies unless robust: (a) Playwright `clip` is CSS pixels but the saved image is device pixels — don't multiply clip coords by `devicePixelRatio`; divide the *read* coords instead. (b) A 1px line sits at a sub-pixel y, so sample a ±5px band and take, per column, the pixel **furthest from the background color** (never hard-code "brightest"). (c) Sample a text-free region — glyphs read as a false line. When two probes disagree, the naive one is wrong.

### 4. Diagnose

Name the problem in design terms mapped to the token scale. Bad: "rows need more spacing" / "add shadow." Good: "within-series row gaps ≈ between-series gaps → no grouping contrast; tighten rows, raise the between-series gap two steps" / "cards read flat → raise elevation one step, tighten in-card gaps, widen between-card gap."

### 5. Fix, re-capture, compare

Minimal, targeted change with project tokens/components. Re-capture all breakpoints; confirm the fix did what the diagnosis predicted and broke nothing at another width. Usually 2–4 rounds converge. In polish mode, commit each accepted round (via `/co`) or stash before a risky one so every round is revertible; exit early when a round closes no meaningful gap.

### 6. Stop and hand to the human

Taste is the human's call. When the invariants pass and every width reads clean, stop and show before / after (plus north-star or reference side by side). Don't loop chasing a verdict only a person can give. Human checkpoints: picking the direction, accepting the result.

## Matching a reference

With a concrete reference, the failure mode is confirming your render against **your own restatement** of the request instead of the reference's pixels. Skipping any of these is the bug:

1. **Read presence AND absence.** A green line along the bottom edge says "border here" **and** "no border on any other edge." Write the spec both ways before coding. The classic miss: reading "border here" and adding a full perimeter.
2. **Apply the user's annotation legend verbatim** ("green = must have, red = must not"). If a mark is truly ambiguous, ask one question; don't guess.
3. **Verify by diff, never self-judgment.** Same region, same zoom, side by side; walk every element. Every "present in only one" is a defect — **including things in yours that the reference lacks**.
4. **Don't author pass/fail checks from your interpretation** — they only confirm your misread. If a subagent verifies, give it the **reference image**, never your paraphrased checklist.
5. **On "still wrong," re-derive the spec from the reference from scratch.** Repeated feedback on the same element means the underlying model is wrong, not one step short; patching it keeps it wrong.

## Computable invariants

Checked against measured px:

- **Contrast:** between-group gap ≳ **2×** within-group gap.
- **Cohesion:** sibling gap **≤** the item's own line-height / height.
- **Monotonic hierarchy:** spacing strictly increases up the grouping tree (atom < item < sibling-gap < group < section).
- **Reference fidelity (when a reference exists):** everything marked present is present, every unmarked region is unchanged, and nothing exists in your render that the reference does not show.
