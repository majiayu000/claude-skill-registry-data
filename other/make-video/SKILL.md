---
name: make-video
description: >
  Build a HyperFrames video composition from a brief/script autonomously.
  Uses separated builder and critic subagents — builders never review their own
  work. Quality decisions are grounded in project context (identity, audience,
  goals) and established visual/motion design principles. Measurable criteria
  (text size, contrast, overflow) are verified with tooling, not visual judgment.
  Use when the user says "make this video", "implement this brief", "build this
  composition", or provides a video script/brief to implement.
---

# Make Video — Brief to Polished Composition (Autonomous)

You are the **director**. You manage phases, dispatch designers, builders, and
critics, and make quality decisions grounded in project context, tooling output,
and design principles — not subjective agent taste.

## Why This Skill Exists

Agents cannot judge visual aesthetics from taste. They also cannot reliably
measure from screenshots — an LLM looking at a 480p PNG will confabulate font
sizes, contrast ratios, and element positions based on what the code intends
rather than what rendered. This skill splits evaluation into two layers:

1. **Measurable criteria** (text size, contrast, overflow, font family) —
   verified by tooling (`hyperframes inspect --json`, `magick identify`, lint).
   These produce machine-readable ground truth. No LLM judgment involved.
2. **Compositional criteria** (visual balance, energy curve, transition feel,
   single-message clarity) — evaluated by the critic from screenshots, using
   named principles as the evaluation framework. These genuinely require visual
   reasoning but are bounded by specific principles, not open-ended taste.

## The Iron Laws

```
1. BUILDERS NEVER REVIEW THEIR OWN WORK.
2. MEASURABLE CRITERIA USE TOOLING, NOT VISUAL JUDGMENT.
3. COMPOSITIONAL CRITERIA CITE PRINCIPLES, NEVER TASTE.
4. DESIGN BEFORE CODE. ALWAYS.
5. ONE BEAT AT A TIME. NEVER BUILD ALL BEATS THEN REVIEW.
```

## Inputs

The user provides:

1. **Brief or script** — a file path (e.g. `content/pace/briefs/script-launch-v2.md`)
2. **Duration** (optional) — time budget for Phase 3 polish. If not given, Phase 3 runs one pass only.

## Quality Framework

Every quality decision must trace to one of these sources. No evaluation may
rely on subjective preference ("I think it looks better").

### Source 1: Project Context

Read BEFORE the design phase and thread through every evaluation:

- **Project identity** (`content/<project>/identity.md`) — palette, typography, motion language, tone
- **Brief/script** — intended message, audience, emotional arc, CTA
- **Styleguide** (`content/styleguide.md`) — structural rules (resolutions, pacing, hook timing, CTA placement)
- **Target audience** — inferred from the brief; determines complexity ceiling, visual density, and pacing

### Source 2: Established Principles

Reference these by name when justifying a decision. The critic and director
cite the specific principle when flagging an issue.

| Domain | Principle | Source | Application |
|--------|-----------|--------|-------------|
| Typography | Minimum readable size at target resolution | WCAG | Text must be legible at 480p downscale — minimum ~18px effective at 1080p |
| Layout | Visual hierarchy through scale, weight, position | Müller-Brockmann, *Grid Systems in Graphic Design* | Primary element should command >40% visual weight at peak frame |
| Motion | Easing communicates physicality; linear motion feels mechanical | Disney's 12 Principles of Animation (ease-in/ease-out) | All motion uses easing curves; no linear tweens except for mechanical/digital effects |
| Motion | Anticipation before major action | Disney's 12 Principles | Beat entries use subtle scale/opacity anticipation before the main reveal |
| Pacing | Viewer attention resets need 0.3–0.5s breathing room | Krasner, *Motion Graphic Design* | Minimum 0.3s gap between dense information beats |
| Color | Contrast ratio for text legibility | WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large) | All text-on-background combinations must meet contrast ratios |
| Color | Palette coherence within brand identity | Project identity file | All colors used must trace to the project palette or be a computed derivative |
| Composition | Rule of thirds / visual balance | Basic compositional theory | Key elements should align to grid; frame should not feel lopsided |
| Transitions | Continuity of motion direction and energy | Krasner, *Motion Graphic Design* | Outgoing element motion direction should relate to incoming element entry |
| Information density | One idea per screen moment | Duarte, *slide:ology* | Each beat's peak should communicate one clear message, not multiple competing elements |

### Source 3: Design Plan Compliance

The design plan (produced in Phase 0) is the contract. Every deviation is logged.
Deviations are acceptable ONLY when the plan itself violated a Source 2 principle
— in which case the critic notes both the deviation and the principle.

### Source 4: Styleguide Compliance

Structural rules from `content/styleguide.md` that apply to the full sequence,
checked in Phase 2:

- First 3 seconds must establish context (hook)
- Project name/logo visible within first 5 seconds
- End with a clear CTA
- No orphan frames (isolated single-frame content between beats)
- Audio levels per styleguide if audio is present

## Criteria Split: Tooling vs. Visual

This is the critical distinction. Getting this wrong reintroduces the echo chamber.

### Tooling-verified criteria (machine-readable, no LLM judgment)

These criteria are checked by running tools and reading their structured output.
The critic MUST use the tool output as ground truth, not its own visual impression.

| Criterion | Tool | Command | What to check |
|-----------|------|---------|---------------|
| text-overflow | `hyperframes inspect` | `npx hyperframes inspect --json --at <times>` | Any `overflow` issues in the JSON output |
| container-overflow | `hyperframes inspect` | same | Container elements exceeding bounds |
| element-presence | `hyperframes inspect` | same | Expected elements exist at expected timestamps |
| text-size | `hyperframes inspect` | same | Bounding box heights indicate sufficient font size |
| lint-errors | `hyperframes lint` | `npx hyperframes lint --json` | Zero errors; warnings acceptable |
| contrast-ratio | builder audit | Builder outputs a contrast table (see builder prompt) | All pairs ≥4.5:1 (normal) or ≥3:1 (large) |
| font-loading | builder audit | Builder verifies computed font families match identity | No fallback font substitution |
| render-success | `hyperframes render` | Exit code 0, non-zero file size | Render completes without error |

### Visually-evaluated criteria (critic reads PNGs, cites principles)

These criteria genuinely require looking at the rendered frame. The critic
evaluates from the PNG but MUST include the specific principle and a measurable
observation (not just "looks fine").

| Criterion | Principle | What the critic reports |
|-----------|-----------|------------------------|
| visual-hierarchy | Müller-Brockmann | "headline occupies ~50% of frame height, subtitle ~20% — ratio 2.5x (threshold: ≥1.5x)" |
| composition | Rule of thirds | "headline sits at upper-third intersection, CTA at lower-third" |
| single-message | Duarte | "one element dominates: the feature demo. No competing focal points" |
| motion-continuity | Krasner | "beat 2 exits right, beat 3 enters right — directional continuity maintained" |
| energy-curve | Krasner | "visual density drops between beats 3→4, providing breathing room per plan" |
| palette-visual | Identity file | "visible colors: dark navy background, coral accent on headline — matches identity" |
| plan-compliance | Design plan | "layout matches ASCII sketch: headline centered, rule below, empty lower third" |

**Every PASS must include the measured or observed value and the threshold it passes.**
`PASS visual-hierarchy: headline ~50% frame, subtitle ~20%, ratio 2.5x (threshold ≥1.5x)` —
not `PASS visual-hierarchy: headline dominates correctly`.

## Roles

There are exactly four roles. Never combine them.

| Role | What it does | What it NEVER does |
|------|-------------|-------------------|
| **Designer** | Produces the design plan from the brief, identity, and principles | Writes composition code, evaluates rendered output |
| **Builder** | Writes HTML/CSS/JS, implements animations, outputs audit data, commits code | Reviews visual quality, evaluates output |
| **Critic** | Runs tooling, takes snapshots, evaluates against criteria, produces structured verdicts | Makes code changes, uses subjective language, reads composition source code |
| **Director** (you) | Manages phases, makes go/fix decisions based on critic reports, dispatches | Writes composition code, overrides criteria with taste |

### Critic verdicts

The critic produces structured evaluations in two sections.

**Section 1: Tooling verdicts** (from `hyperframes inspect --json` and lint output):

```
TOOLING at 9.0s — Beat 3 peak:
PASS  text-overflow: no overflow issues reported by inspect
PASS  container-overflow: all containers within bounds
PASS  lint: 0 errors, 2 warnings (non-blocking)
PASS  contrast-ratio: builder audit shows all pairs ≥4.5:1
      (headline #e94560 on #1a1a2e = 5.2:1, subtitle #cccccc on #1a1a2e = 9.1:1)
PASS  font-loading: builder confirms JetBrains Mono loaded (no fallback substitution)
FAIL  text-overflow: inspect reports "text overflows container by 12px at .subtitle"
      Fix: reduce subtitle text or increase container width
```

**Section 2: Visual verdicts** (from reading the downscaled PNGs):

```
VISUAL at 9.0s — Beat 3 peak:
PASS  visual-hierarchy: headline ~50% frame height, subtitle ~18%, ratio 2.8x (threshold ≥1.5x)
PASS  composition: headline at upper-third, CTA at lower-third intersection
FAIL  single-message: two competing focal points — headline and animated sidebar both demand attention
      Principle: Duarte — one idea per screen moment
      Fix: reduce sidebar opacity or delay its entrance by 0.5s
PASS  palette-visual: navy (#1a1a2e) background, coral (#e94560) headline — matches identity
DEVIATION: plan specifies 1px rule at 60% width — image shows no rule element
```

### Director decisions

The director acts on critic reports as follows:

- **All PASS, no deviations** → proceed to next beat
- **Any FAIL** → dispatch builder with the specific fix from the critic's report
- **DEVIATION from plan** → proceed if the rendered result still satisfies all principles; dispatch fix if it doesn't
- **Rendering error** (blank/black/partial frame) → fix before any evaluation

The director does NOT second-guess PASS verdicts or invent issues the critic didn't flag.

## The Process

```
Phase 0: DESIGN PLAN          ← designer produces, director validates against principles
Phase 1: BEAT-BY-BEAT BUILD   ← critic evaluates each beat (tooling + visual)
Phase 2: FLOW REVIEW          ← critic evaluates full sequence continuity + styleguide
Phase 3: POLISH               ← one targeted pass (or timeboxed if duration given)
```

### Phase 0: Design Plan

Before writing a single line of HTML, produce a visual design document.

**Dispatch a DESIGNER subagent** to create the design plan. Give it:
- The brief/script file path
- The project identity file path (e.g. `content/<project>/identity.md`)
- The styleguide file path (`content/styleguide.md`)
- The v1 composition path if it exists (for reference patterns)
- The quality framework principles table (above) — the plan must not contradict them
- Instruction: produce a design plan, NOT code. Think as a visual communicator designing for the target audience.

The designer prompt:

```
You are a DESIGNER. You create visual design plans for video compositions.
You think about audience, message, and visual communication — not code.

Brief: <path to brief>
Identity: <path to identity.md>
Styleguide: <path to styleguide.md>
Reference composition: <path if exists, or "none">

Your task: Design a composition that communicates the brief's message to its
target audience. Read all input files. Produce a design plan, NOT code.

For EACH beat, provide:

### Beat N: <title> (<start>–<end>)

**Layout sketch** (ASCII art showing element positions at peak moment)
**Key visual effect**: what makes this beat visually interesting
**Motion sequence**: ordered list of animations with timing and easing curves
**Audience consideration**: how this beat serves the target viewer specifically
**Principle compliance**: which quality framework principles this beat relies on
**What could go wrong**: known risks — overflow, invisible elements, contrast failure
**Reference**: if reusing a pattern from v1 or another composition, cite it

Also provide:
- **Audience profile**: one paragraph — who watches this, what they know, what they need to feel
- **Transition plan**: how each beat flows into the next (specific motion direction,
  overlapping elements, energy continuity — per Krasner)
- **Visual energy curve**: one-line-per-beat visual weight description
- **Canvas/effect inventory**: which canvases exist, what they draw, when they're active
- **Styleguide checklist**: verify hook within 3s, logo within 5s, CTA at end,
  no orphan frames

If the brief includes audio: note where audio events align with visual beats.

Do NOT write HTML, CSS, or JavaScript. Do NOT describe implementation details.
Think about what the viewer SEES and FEELS, not how it's coded.
```

**Director validates the design plan** against the quality framework:
- Does every beat have a clear single message? (Duarte)
- Does the energy curve have breathing room between dense beats? (Krasner, 0.3–0.5s)
- Are font sizes large enough for 480p legibility? (WCAG, ≥18px at 1080p)
- Does the palette match the identity file?
- Do transitions maintain motion continuity? (Krasner)
- Styleguide: hook within 3s? Logo within 5s? CTA at end?

If any principle is violated, dispatch the designer to revise before proceeding.
Otherwise, proceed to Phase 1. The builder must commit the design plan as its
own git commit before writing any composition code.

**Show the user the finalized design plan** as an informational summary (not a gate).
Continue immediately — do not wait for approval.

### Phase 1: Beat-by-Beat Build

Build ONE beat at a time. For each beat:

#### Step 1: Build

Dispatch a **builder** subagent:
- Give it the design plan
- Give it the composition file path
- Give it the project identity file path
- Instruction: implement ONLY Beat N. Follow the design plan exactly. Commit.
- **The builder MUST return:** what it built, actual implemented timestamps for
  this beat (entry, peak, exit), a contrast audit table, font verification
  results, and any deviations from the plan.

#### Step 2: Critique

Dispatch a **critic** subagent (DIFFERENT agent — never the builder).

**The critic does NOT receive the composition source code path.** It receives:
- The design plan path
- The identity file path
- The builder's returned data (actual timestamps, contrast audit, font verification)
- The composition DIRECTORY path (for running tools and accessing snapshots)
- The quality framework principles table

The critic's workflow:

**Step 2a: Tooling pass** (machine-readable, no visual judgment):

```bash
# Run inspect at builder's actual timestamps (not design plan timestamps)
cd <composition-dir> && npx hyperframes inspect --json --at <entry>,<peak>,<exit>

# Run lint
cd <composition-dir> && npx hyperframes lint --json
```

Parse the JSON output. For each timestamp:
- Check for text-overflow, container-overflow issues
- Verify element presence (expected elements from design plan exist)
- Cross-reference builder's contrast audit (flag if any pair < thresholds)
- Cross-reference builder's font verification (flag any fallback substitution)

**Step 2b: Visual pass** (snapshot + principle-based evaluation):

```bash
# Snapshot at builder's actual timestamps
cd <composition-dir> && npx hyperframes snapshot --at <entry>,<peak>,<exit>

# Downscale preserving aspect ratio (no distortion)
magick <input> -resize 854x480 <output>
```

Read each downscaled PNG with the Read tool. Evaluate ONLY the visually-evaluated
criteria (visual-hierarchy, composition, single-message, palette-visual, plan-compliance).
Every PASS must include a measured/observed value and the threshold.

**Do NOT read the composition's index.html or any source files.**
If you cannot see an element in the PNG, it is not there.

**Step 2c: Regression check (beat 2+)**

If this is not the first beat:
- Run `hyperframes inspect --json --at <previous-beat-peak>` and diff against
  the previous beat's inspect output (kept in `snapshots/beat-N-1/inspect.json`)
- Re-snapshot previous beat's peak and compare side-by-side with the kept
  previous screenshot (both PNGs open via Read tool)
- If inspect JSON shows new overflow or missing elements:
  `REGRESSION: Beat N-1 at Xs — inspect shows <specific change>`
- If visual comparison shows layout shift:
  `REGRESSION: Beat N-1 at Xs — visual comparison shows <specific change>`

**Step 2d: Transition mini-review (beat 2+)**

Snapshot the transition boundary: last 0.5s of beat N-1, first 0.5s of beat N.
Evaluate for:
- Motion continuity (Krasner): does outgoing motion relate to incoming?
- Energy continuity: does the transition match the planned energy curve?
- No black frames, visual gaps, or element doubling

**Cap: maximum 5–7 frames per beat** (key frames + transition + regression).

#### Step 3: Director decision

The director reads the critic's structured report and decides:

**If all criteria PASS and no regressions:**
- Log the beat as complete in the progress file (include inspect JSON summary)
- Proceed to next beat

**If any criteria FAIL:**
1. Dispatch a new builder with the specific fix (from the critic's FAIL entry)
2. Dispatch a new critic to re-evaluate
3. Maximum 3 fix iterations per beat — if still failing after 3, log to the
   **UNRESOLVED** list with the last critic verdict and proceed

**If regression detected:**
1. Dispatch a builder to fix the regression specifically
2. Re-critique both the current and regressed beat

### Phase 2: Flow Review

After all beats pass individually, do a full-sequence review.

#### Step 1: Transition and continuity check

Dispatch a **critic** subagent:
- Run `hyperframes inspect --json` with samples across the full duration
  (use `--samples 15` or `--at` with all transition timestamps)
- Take snapshots at every beat transition (±0.5s around each boundary)
- Take one "peak" snapshot per beat
- Downscale all preserving aspect ratio: `magick <input> -resize 854x480 <output>`
- Evaluate each transition for: motion continuity, energy curve adherence, no black frames/gaps/doubling
- Evaluate the full sequence for: pacing rhythm, consistent visual language, palette coherence

**Additionally check styleguide structural rules (Source 4):**
- Snapshot at 1.0s, 2.0s, 3.0s — does context establish within first 3s?
- Snapshot at 4.0s, 5.0s — is project name/logo visible by 5s?
- Snapshot at the final beat — is a clear CTA present?
- Check inspect output across all samples for orphan frames

The critic produces a sequence-level report:

```
SEQUENCE TOOLING:
  Inspect: 0 overflow issues across 15 samples
  Lint: 0 errors

SEQUENCE VISUAL:
  Pacing: PASS — 0.4s average gap between dense beats (Krasner minimum: 0.3s)
  Palette coherence: PASS — all beats use identity palette exclusively
  Energy curve: FAIL — beats 3→4 both peak density with no relief
    Principle: Krasner — viewer attention reset needs 0.3–0.5s breathing room
    Fix: add 0.3s visual pause between beats 3 and 4
  Motion language: PASS — all transitions use consistent left-to-right flow

STYLEGUIDE:
  Hook (3s): PASS — product name and tagline visible at 1.5s
  Logo (5s): PASS — logo appears at 2.0s
  CTA: PASS — "Try it free" CTA visible in final beat
  Orphan frames: PASS — no isolated single-frame content detected

TRANSITION VERDICTS:
  Beat 1→2: PASS — fade-out left matches fade-in left
  Beat 2→3: FAIL — beat 2 exits right but beat 3 enters from top (discontinuity)
    Principle: Krasner — continuity of motion direction
    Fix: change beat 3 entry to right-side entrance
  ...
```

#### Step 2: Director decision

- Fix all FAIL items (dispatch builder, re-critique, max 3 iterations per issue)
- Items hitting the cap go to the **UNRESOLVED** list
- Log the storyboard frame paths in the progress file

**Show the user the storyboard** (peak frame per beat + transition frames) as an
informational summary. Continue immediately.

#### Step 3: Render test

Dispatch a **builder** subagent to do a full render (WebM if MP4 unavailable).
Report: duration, resolution, file size, any errors.

If render fails, dispatch builder to fix and re-render. Max 3 attempts.

### Phase 3: Polish

This phase runs a single targeted pass over any remaining issues.

If a **duration** was given, timebox to that duration — iterate until time runs out.
If no duration was given, run exactly one pass.

The polish loop:

1. **Director reviews** the UNRESOLVED list and the accumulated progress log
2. If issues remain, prioritize by severity (rendering errors > tooling FAILs > visual FAILs > plan deviations)
3. Dispatch a **builder** to fix the highest-priority issue
4. Dispatch a **critic** to verify the fix with before/after evaluation
5. If timeboxed: check the clock. Time left and issues remain? Go to 2. Otherwise, proceed.
6. If single-pass: after addressing all logged issues once, proceed.

**If no issues remain from the earlier phases**, run a final hardening pass:
- Run `hyperframes inspect --json --samples 20` across the full duration
- Critic takes one peak frame per beat at full resolution AND at 480p downscale
- Cross-check for any issues not caught with fewer samples
- Reports any new findings

### Error Recovery

If a snapshot renders a blank/black frame where content is expected:
1. Flag it: `ERROR: frame at Xs rendered blank, possible JS error or rendering failure`
2. Dispatch a builder to run `npx hyperframes lint --json` and check for JS errors
3. Do not proceed with evaluation until rendering errors are resolved

If a canvas element exists in the DOM but renders as empty/single-color at the
expected timestamp, treat this as a rendering error — not an intentional design
choice. The builder should check for WebGL initialization failures and increase
the snapshot `--timeout` to 10000 for canvas-heavy beats.

### Audio

If the brief specifies audio (music, voiceover, sound effects):
- The builder implements audio elements per the design plan
- Audio quality (levels, sync, mixing) **cannot be verified by tooling or screenshots**
- The director logs: `AUDIO PRESENT — levels and sync require manual review`
- Include this in the completion output so the user knows to check it

Audio is explicitly out of scope for autonomous evaluation. Do not claim audio
"sounds good" or report PASS on audio criteria.

### Completion

The composition is done when:
- All beats pass all tooling criteria
- All beats pass all visual criteria (or are on the UNRESOLVED list)
- All transitions pass continuity checks
- Styleguide structural rules pass
- The render completes without errors
- Phase 3 pass is complete (one pass or timeboxed)

**Output to the user:**

1. The final rendered video path
2. A one-paragraph summary: what was built, beat count, duration
3. The storyboard frame paths for reference

**If the UNRESOLVED list is non-empty, output a mandatory section:**

```
## UNRESOLVED ISSUES

These items failed criteria and exhausted the 3-iteration fix cap in both
their original phase and Phase 3. They require manual review.

1. Beat 3, 9.0s — single-message: two competing focal points (headline + sidebar)
   Last critic verdict: FAIL — Duarte principle violated
   Last attempted fix: reduced sidebar opacity to 40% — still competing
   
2. Transition 5→6 — motion-continuity: beat 5 exits upward, beat 6 enters from left
   Last critic verdict: FAIL — Krasner principle violated
   Last attempted fix: changed beat 6 entry to top — caused regression in beat 6 layout
```

Do NOT bury unresolved issues in "known limitations." They get their own section
with the last critic verdict and last attempted fix for each.

## Subagent Prompts

### Builder prompt template

```
You are a BUILDER. You write code. You do not evaluate visual quality.

Composition: <path to index.html>
Design plan: <path or inline>
Brief: <path to brief>
Identity: <path to identity.md>

Your task: Implement Beat N according to the design plan.
- Read the design plan's Beat N section carefully
- Read the brief's Beat N section for text content and timing values
- Read the identity file for palette, typography, and motion language
- Read the current index.html
- Implement the beat using eased animations (no linear tweens except for
  deliberate mechanical/digital effects)
- Ensure all text is ≥18px effective at 1080p for 480p legibility
- Use only colors from the identity palette or computed derivatives
- Commit your changes

REQUIRED OUTPUT — you MUST return ALL of the following:

1. **What you built**: brief description of elements and animations
2. **Actual timestamps**: the exact entry, peak, and exit seconds for this beat
   as implemented (these may differ from the design plan if you needed to adjust)
3. **Contrast audit table**: for EVERY text-on-background combination in this beat:
   | Text element | Text color | Background color | Ratio | Meets AA? |
   Compute ratios using the relative luminance formula.
4. **Font verification**: for each font family used, confirm the font file/CDN
   loads successfully. If using a web font, verify the @font-face src resolves.
   List: | Element | Specified font | Verified loaded? |
5. **Deviations from plan**: any differences from the design plan and why
6. **Commit hash**: the git commit SHA

Do NOT take snapshots. Do NOT evaluate your own work visually.
```

### Critic prompt template (DOM-heavy beats)

Use for beats where the visual content is HTML elements (dashboard panels,
terminal, YAML text, CTA cards).

```
You are a CRITIC. You evaluate rendered output against objective criteria.
You do not write code. You do not read composition source code.

Design plan: <path or inline>
Identity: <path to identity.md>
Composition directory: <dir path> (for running tools and reading snapshots ONLY)
Beat: N (<entry>s to <exit>s) — timestamps from builder's actual implementation
Builder audit data:
  Contrast table: <inline from builder output>
  Font verification: <inline from builder output>

YOUR WORKFLOW:

PART 1 — TOOLING (machine-readable, no judgment):

Run these commands and parse the output:

  cd <composition-dir> && npx hyperframes inspect --json --at <entry>,<peak>,<exit>
  cd <composition-dir> && npx hyperframes lint --json

From the inspect JSON, evaluate:
- text-overflow: any text overflow issues? (PASS if none, FAIL with details if any)
- container-overflow: any container overflow? (PASS/FAIL)
- element-presence: do expected elements from the design plan exist at each timestamp?

From the builder's contrast audit:
- contrast-ratio: all pairs ≥4.5:1 (normal text) or ≥3:1 (large text ≥24px)?
  Report each pair's ratio. If builder omitted pairs, flag as FAIL.

From the builder's font verification:
- font-loading: all specified fonts confirmed loaded? Any fallback substitution?

PART 2 — VISUAL (from screenshots, principle-based):

Take snapshots and downscale (preserve aspect ratio — NO ! flag):

  cd <composition-dir> && npx hyperframes snapshot --at <entry>,<peak>,<exit>
  magick <input> -resize 854x480 <output>

READ each downscaled PNG with the Read tool. Evaluate:
- visual-hierarchy: primary element dominates by ≥1.5x scale ratio over secondary
  (Müller-Brockmann). Report approximate ratios.
- composition: key elements aligned to thirds grid, frame balanced.
  Report element positions (top/center/bottom, left/right).
- single-message: beat peak communicates one clear idea, not competing elements (Duarte).
  Name the focal point. If multiple compete, FAIL.
- palette-visual: visible colors match identity palette. List colors observed.
- plan-compliance: rendered layout matches design plan ASCII sketch.
  List matches and deviations.

Every PASS must include the measured/observed value and the threshold.

CRITICAL RULES:
- Do NOT open, read, or reference index.html or any .js/.css source files
- Do NOT describe what code "should" render — describe what the PNG shows
- If you cannot see an element in the PNG, it is not there
- Banned words: "good", "great", "clean", "polished", "nice", "solid", "well"

Save snapshots to <composition-dir>/snapshots/beat-N/ (not the root snapshots dir).
Save the inspect JSON output to <composition-dir>/snapshots/beat-N/inspect.json
for regression comparison by later beats.
```

### Critic prompt template (canvas-heavy beats)

Use for beats dominated by canvas drawing (chaos animation, pixel grids,
procedural effects). Individual elements cannot be listed — evaluate the
aggregate visual effect.

```
You are a CRITIC evaluating canvas-heavy content.

Same tooling pass as DOM-heavy template (inspect, lint, contrast audit, font check).

For the VISUAL pass, use canvas-specific criteria instead:
- visual-density: what % of the frame has visible canvas content? Report approximate coverage.
  Does density match the energy curve position for this beat? (Krasner)
- color-range: are canvas colors within the identity palette range?
  Use magick to extract dominant colors:
    magick <png> -colors 5 -define histogram:unique-colors=true -format %c histogram:info:
  Compare extracted colors against identity palette.
- text-overlay-legibility: if text overlays the canvas, is it readable?
  Use the builder's contrast audit for the text-on-canvas combinations.
  Visually confirm the text stands out from the canvas texture in the PNG.
- plan-compliance: does the visual effect match the plan's description?

For canvas beats, increase snapshot timeout:
  cd <composition-dir> && npx hyperframes snapshot --at <times> --timeout 10000

Do NOT attempt to list individual canvas-drawn items. Evaluate the aggregate.
```

## Snapshot Management

Snapshots are stored per-beat in `<composition-dir>/snapshots/beat-N/`:
- `entry.png`, `peak.png`, `exit.png` — downscaled frames
- `inspect.json` — tooling output at beat timestamps
- Transition frames (beat 2+): `transition-from-N-1.png`, `transition-to-N.png`

Previous beat directories are KEPT until Phase 2 completes (needed for regression
comparison). Only clean all snapshot directories after Phase 2 flow review passes
and the storyboard is logged to the progress file.

## Anti-Patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Build all beats, then review | Structural problems compound. Beat 9 depends on Beat 1-8 being right. | Build and evaluate one beat at a time. |
| Builder reviews own work | "Looks good" is the default answer when you just wrote the code. | Separate builder and critic. Always. |
| LLM measures from screenshots | Agents confabulate font sizes, contrast ratios, and positions from PNGs. | Use `hyperframes inspect --json` for measurable criteria. Reserve visual evaluation for compositional judgment. |
| Critic reads source code | Knowing what the code intends causes confirmation bias — the critic "sees" what it expects. | Critic receives NO source code paths. Only design plan, PNGs, and tooling output. |
| Taste-based evaluation | "I think the spacing looks off" with no principle citation is unfalsifiable. | Every FAIL cites a specific principle and threshold. Every PASS includes the measured value. |
| Unbounded fix loop | 35 iterations of fix→check→fix with no convergence signal. | Max 3 fix iterations per issue. Log to UNRESOLVED and move on. |
| Silent broken output | Burying failures in "known limitations" paragraph the user skims. | Mandatory UNRESOLVED ISSUES section with last verdict per item. |
| Distorted downscale | `magick -resize 854x480!` destroys aspect ratio on non-16:9 compositions. | Use `magick -resize 854x480` (no `!`) to preserve aspect ratio. |
| Using design plan timestamps | Builder may shift timing during implementation. Critic snapshots wrong moments. | Builder returns actual timestamps. Critic uses those, not the plan. |
| No design phase | Jumping to code locks in structural decisions before evaluation. | Design plan validated against principles before any HTML. |

## Director Red Flags — STOP and Reread This Skill

If you catch yourself doing any of these, you have broken role separation:

- You're about to take a snapshot yourself instead of dispatching a critic
- You're about to evaluate what a frame "looks like" based on reading the HTML
- You're about to say "looks good", "looks correct", or "the beat renders properly"
- You're about to skip the critic because the builder "probably got it right"
- You're about to "just quickly fix" something in the HTML instead of dispatching a builder
- You're issuing a FAIL verdict based on taste ("feels off") rather than a named principle
- You're overriding a PASS verdict because something "seems wrong" without a criteria violation
- You're reporting a contrast ratio or font size based on looking at a PNG instead of tooling output
- You're giving the critic the path to index.html or any source code file

**Any of these = full stop. Reread the Iron Laws.**

## Orchestrator Checklist

Before each phase transition, verify:

- [ ] Phase 0 → 1: Design plan passes all principle checks AND styleguide structural checks
- [ ] Each beat in Phase 1: All tooling criteria PASS. All visual criteria PASS (or on UNRESOLVED list)
- [ ] Phase 1 → 2: ALL beats evaluated, no unresolved regressions, per-beat snapshot dirs preserved
- [ ] Phase 2 → 3: Sequence continuity passes, styleguide structural rules pass, render completes
- [ ] Phase 3 exit: All logged issues addressed (one pass or timeboxed). UNRESOLVED list finalized.

## Quick Reference

| Item | Value |
|---|---|
| Progress file | `/tmp/make-video-<slug>-<timestamp>.md` |
| Design plan | Written to `<composition-dir>/design-plan.md` (committed separately) |
| Snapshots | `<composition-dir>/snapshots/beat-N/` (per-beat, kept until Phase 2 done) |
| Inspect | `npx hyperframes inspect --json --at <times>` |
| Lint | `npx hyperframes lint --json` |
| Downscale | `magick <input> -resize 854x480 <output>` (no `!` — preserve aspect ratio) |
| Snapshot timeout | 5000ms default, 10000ms for canvas-heavy beats |
| Phases | Design → Beat-by-beat → Flow → Polish |
| Quality gate | Tooling verdicts (machine) + visual verdicts (principle-cited) |
| Max fix iterations | 3 per issue per phase (prevents infinite loops) |
| Unresolved output | Mandatory section with last verdict per capped item |
| Designer rule | Produces the plan, thinks about audience and message, never writes code |
| Builder rule | Never evaluates own work. Returns timestamps, contrast audit, font verification |
| Critic rule | Never reads source code. Uses tooling for measurable criteria. Cites principles for visual criteria. |
| Director rule | Never writes code, decides based on critic reports, never overrides with taste |
