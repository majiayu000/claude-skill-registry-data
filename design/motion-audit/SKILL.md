---
name: motion-audit
description: Use when the user asks to audit, test or QA the motion, animations or microinteractions of a running page or app, says it feels janky, dead, stutters or jumps, or asks whether reduced motion works. Measures in a real browser what is wrong - no hover, press or focus feedback, snapping or janky transitions, long frames, animations that jump or restart, broken prefers-reduced-motion.
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
  - Bash(node "${CLAUDE_SKILL_DIR}/scripts/*")
  - Bash(npx --no-install motion-audit *)
---

# Motion audit

Motion bugs are invisible in code review and in still screenshots: the CSS says `transition: transform
200ms` and the button still snaps, because the hover rule sets a property the transition does not list.
Run the audit against the page, then fix at the cause.

**Stance.** Every interactive control owes a visible, quick response to hover, press and keyboard focus;
frequency decides *how much* motion (a list row gets a 120 ms tint, a primary CTA gets lift and press),
never *whether* there is feedback. A response with no transition (`snaps`) is a warning to review, not
always a defect. Motion must never cost legibility, input latency or accessibility.

## What is measured and what is read

| Source | What it covers |
|---|---|
| `frames` | Position, size, opacity and transform of the element and its descendants sampled on every animation frame: measured duration, curve shape, overshoot, jumps, animated layout, Long Animation Frames (with the scripts that caused them) |
| `pixels` | Computed-style and screenshot comparison at rest, hover, press and focus: whether anything visibly changes |
| `css` | Declared `transition` duration and easing, `:hover` rules outside `@media (hover: hover)`, reduced-motion rules: read from the stylesheet, so JS-driven motion (Motion, GSAP) is only judged from `frames` |
| `events` | Animation objects and DOM events: a keyframe animation that restarts or is cancelled mid-way, infinite animations under reduced motion, entrances |

`:active` and `:focus-visible` are forced through the DevTools protocol (no pointer or focus event is
dispatched). Hover is a real pointer move after a hit test, so a control covered by a cookie banner or
sticky header is skipped (`NOT RUN covered`) instead of producing a false finding.

## What counts as a finding

Levels are the defaults; the config file can change any of them.

| Kind (script output) | What the user feels | Default level | Source |
|---|---|---|---|
| `no-feedback` | Hover changes nothing on a button: the UI feels dead (links: warning; inputs: not reported) | error | pixels |
| `no-press-feedback` | Press changes nothing on a button (links and inputs: not reported) | warning | pixels |
| `no-focus-feedback` | Keyboard focus is invisible | error | pixels |
| `hover-only-control` | A control revealed only by pointer hover stays invisible when it gets keyboard focus | warning | pixels |
| `snaps` | Feedback exists but jumps: the changed properties have no transition | warning | css |
| `layout-animated` | Width, height, top, margin, padding or font animate: neighbours shift and layout runs every frame | error | frames |
| `long-frame` | A frame over 50 ms during hover, a click transition or scroll, from an application script or from style, layout and paint with no script; a warning on a development build | error | frames |
| `ease-in` | The response starts slow: declared curve or measured trajectory | error | css |
| `duration` | Declared duration outside the band for the gesture (hover 80-300, press 50-200, focus up to 250 ms) | warning | css |
| `linear` | A transform or opacity transition declared linear: mechanical | warning | css |
| `transition-all` | `transition: all` animates whatever changes, layout included | warning | css |
| `inconsistent-duration` | Same kind of control and gesture with declared durations 1.5x and 60 ms apart | warning | css |
| `jump` | A frame moves several times faster than a smooth curve allows: a teleporting animation | error | frames |
| `interrupt-jump` | Leaving hover mid-way, or clicking again mid-transition, jumps instead of reversing | error | events |
| `not-interruptible` | A toggle clicked back part-way through its motion restarts from the other end (needs `--interact`) | error | events |
| `ungated-hover` | `:hover` moves things outside `@media (hover: hover)`: it sticks after a tap on touch screens | warning | css |
| `reduced-motion-moves` | With prefers-reduced-motion a press still translates, rotates or scales by more than 6 % | error | css |
| `reduced-motion-residue` | With prefers-reduced-motion a transform stays after release (needs `--interact`) | error | css |
| `reduced-motion-loop` | An infinite moving animation keeps running under reduced motion (small rotate-only spinners excepted) | error | events |
| `reduced-motion-hidden` | Content waits for an entrance that reduced motion skipped: it stays at opacity 0 | error | pixels |
| `reduced-motion-missing` | Things move and no readable stylesheet has a reduced-motion rule (info when some sheets are unreadable) | warning | css |
| `no-entrance` | A section below the fold appears without an entrance (opt-in with `--entrances`; never fails the run) | info | events |
| `inconclusive` | The frames were too sparse to confirm or rule out a finding (its `check`, with the fingerprint of that finding): the reason gives the median and longest interval; never fails the run | warning | frames |
| `click-target` | The `--click` selector matches nothing visible | error | pixels |

`info` never fails a run. Missing `:active` or hover on links and inputs is never an error.

## Method

### 1. Measure on the running page

Audit a **production build** (`next start`, `vite preview`, a deployed preview), not a dev server. Dev
builds add HMR, overlays and unminified work: the audit detects them, says so, and downgrades
`long-frame` to a warning, but only a production build gives frame timings that mean something.

If the project has `motion-audit` as a devDependency, prefer `npx --no-install motion-audit <url> ...`: it runs
the version the project pins. Otherwise run the script bundled with this skill. The same command works in Git Bash, other POSIX shells and
PowerShell (`${CLAUDE_SKILL_DIR}` is substituted before the shell runs it; the single-quoted selectors are literal in both):

```bash
node "${CLAUDE_SKILL_DIR}/scripts/motion-audit.mjs" http://localhost:3000/orders
node "${CLAUDE_SKILL_DIR}/scripts/motion-audit.mjs" http://localhost:3000/orders --cpu 4 --click '[aria-controls=filters]' --interrupt
node "${CLAUDE_SKILL_DIR}/scripts/motion-audit.mjs" http://localhost:3000/orders --only 'nav a' --only '.toolbar button' --frames '.btn-primary'
```

Exit 0 clean, 1 findings, **2 could not run, audited nothing or audited incompletely** - a 2 is never a
pass. The summary says `audited N of M controls` and lists every skip with its reason (`NOT RUN hidden`,
`covered`, `beyond --max 40`...); when N is lower than M, say which controls were not audited.
`--min-coverage 0.8` turns a low ratio into exit 2; controls beyond `--max` count as not audited, so
raise it too (`--max 200 --min-coverage 0.8`). Controls that appear after the audit counted them (a late
fetch) make the run exit 2 with `INCOMPLETE`: re-run with `--wait-for`. A URL that redirects, from the
server or from script (a session check, a router), exits 2 instead of auditing another page; a login
page is never audited (use `--storage-state`), another page only with `--allow-redirect`.

**Observe-only by default.** The audit hovers, forces `:active` and `:focus-visible`, scrolls and reads.
It does not click, so it cannot toggle a Follow button, open a menu that opens on `pointerdown`, submit a
form, switch a tab that switches on `mousedown`, or run focus and keyboard handlers. It does move the
real pointer and scroll the real page, so handlers bound to hover (`mouseenter`, `mouseover`,
`pointerenter` that send a beacon or write storage), scroll-bound `IntersectionObserver` callbacks and
`beforeunload` beacons run: audit a throwaway or staging environment, not one where an impression or a
hover event is billed or irreversible. `--interact` is opt-in and adds a real press and the
toggle probes (`not-interruptible`, `reduced-motion-residue`); a denylist skips submit and reset
controls (inside their form or tied to it with `form=`), buttons with no accessible name, every link
whose `href` is not `#` or the `#id` of an element of the page (hash routes included; and any control inside one), destructive or payment wording in
English, Spanish, Portuguese, French, German and Italian (including `aria-labelledby` and image alt
text), `[draggable]`, sliders and separators; a press is released where it was made (the pointer never
moves while it is down, so nothing is dragged), cancelled with a `pointercancel` before the release and with clicks cancelled for a moment after it (longer than the 80 ms a library waits for the native click), so libraries that act on pointerup (React Aria) do not fire; a plain `mouseup` handler on the control still runs; the
page is reloaded between probes, the run stops if a gesture navigates, every toggle is clicked as the
same node an even number of times, and the denylist is checked again before each click and before the
reduced-motion pass presses a control. Use it only
against a disposable environment.

`--click <selector>` is an explicit click on the control you name, and it clicks more than once: twice
(a pass without the tracer for long frames, one with it for trajectories), four times with
`--interrupt`. A step the frames were too coarse to judge adds up to two more recordings (one press each,
two with `--interrupt`), and when a flaky aspect is found the measurement is repeated twice more, two presses
each: at most eight clicks, sixteen with `--interrupt` (the count is always even: an odd one, after a retry without `--interrupt`, gets one more press that restores the state, provided each press's effect lands within the 1.5 s of its recording: a request still pending at the next reload is reported in the notes, one a timer sends later cannot be seen). Run
it only against a throwaway environment: a "Save" or "Delete" target is saved or deleted several times.

- `--cpu 4` throttles like a mid-range phone. Jank that only shows throttled is still jank.
- `--click <sel>` records everything that moves for 1.5 s after a real click, including overlays mounted
  into `<body>` on open; `--interrupt` clicks again at 160 ms. Do it for every overlay the screen opens.
- `--frames <sel>` writes a contact sheet through hover, press and release with the real time of each
  frame. Look at it: the numbers say *that* it moved, the sheet shows *how*.
- `--storage-state <file>` runs logged in (a Playwright storage state); a redirect to a login page exits 2.
- `--wait-for <sel>` waits for the selector before auditing (apps that hydrate late).
- `--entrances` also reports sections that appear without an entrance, as info.
- `--max 40` is the default; with more controls the summary says `audited 40 of 200`. Narrow with `--only`.
- Inner scroll containers are scrolled and their controls audited; hidden-until-hover controls are found.
- Flaky kinds (`long-frame`, `jump`, `interrupt-jump`, `not-interruptible`) are re-measured twice and kept
  only when two of three runs agree.
- `inconclusive` rows appear when a machine drops so many frames that a check (`ease-in`, `interrupt-jump`,
  `jump`) cannot be decided even after re-recording. They are listed with the findings, counted in
  `coverage.inconclusive` and never fail the run. Rerun on a quieter machine, or without `--cpu` throttling.
- `report.json` (printed with `--json`, `schemaVersion: 1`) has the coverage, `loafSupported`, every
  element's measurements, the findings with stable ids, baselined and suppressed findings.

States the first load does not show (open menus, toasts, loading, error) need the page put in that state:
run against a route or story that renders it, or use `--click` to open it.

### 2. Diagnose: name the cause before editing

For each finding: which element, which gesture, which property moved (or failed to), and **who drives
it** - a CSS transition, `@keyframes`, WAAPI, a JS library, or a rAF loop writing styles. A jump during a
click is usually a JS animation fighting a CSS transition on the same property, or an element re-mounted
mid-animation (React `key` change). Open `references/fixes.md` for the row that matches the cause.

### 3. Fix at the cause, in the component or the tokens

Load `references/fixes.md` only now: it maps each root cause to the fix and to the tempting wrong fix.
Do not add motion to silence an `info`, and do not add a scale to every control to clear a `warning`.

### 4. Verify and close

1. Re-run with the same flags.
2. Re-run with `--cpu 4` on the screens that had long frames, on a production build.
3. Look at a contact sheet (`--frames`) of the primary control and one frequent control.
4. **Finish with 0 errors, or each remaining finding suppressed in `motion-audit.config.json` with its reason.**

```json
{
  "bands": { "reason": "Carbon micro-interactions run at 70 ms", "hover": [60, 300] },
  "tokens": { "reason": "design-system duration tokens", "durations": [70, 120, 200] },
  "severity": { "inconsistent-duration": { "level": "info", "reason": "size-scaled durations are intended" } },
  "ignore": [
    { "kind": "no-feedback", "element": "a \"Skip to content\"*", "reason": "visible only on focus, by design" },
    { "id": "no-feedback:3f2a9c1d07", "reason": "tracked in the design-system backlog" }
  ]
}
```

Anything that loosens the audit (bands, tokens, a lowered or `off` severity, an ignore) needs a
`reason`; ids are the `kind:hash` shown after each finding, never a wildcard; a kind rule must name an
element. Raising a severity needs no reason. `--baseline report.json` accepts the findings an earlier
report already had, so CI fails only on new ones; `compare <ref.json> <mine.json>` lines two reports up
control by control (measured duration, curve, overshoot) and lists new and gone findings.

### Lock it in with a test

From a project that installed the package (`npm i -D github:NahuelMosse/motion-audit#v1.0.0`) next to
`@playwright/test`; the test's own `page`, `baseURL` and `storageState` are used:

```js
// motion.spec.mjs
import { test, expect } from '@playwright/test';
import { audit } from 'motion-audit';

test('orders: motion', async ({ page }) => {
  test.setTimeout(240_000); // each control takes a few seconds of real time
  await page.goto('/orders');
  const report = await audit(page, { only: ['main button', 'nav a'], max: 20, out: 'test-results/motion' });
  expect(report.coverage.audited).toBeGreaterThan(0);
  expect(report.findings.filter((f) => f.level === 'error')).toEqual([]);
});
```

Or the CLI: `npx motion-audit http://localhost:3000/orders --max 200 --min-coverage 0.8 --baseline motion-baseline.json`.

## Limits

- Chromium only. Safari renders some transitions differently; check gesture-heavy UI there by hand.
- Colour and shadow transitions are judged from computed styles and pixels, not traced per frame.
- Long Animation Frames need Chromium 123+; when unsupported the report says
  `loafSupported: false` - never read that as clean.
- Cross-origin stylesheets (and linked ones under `file://`) cannot be read for the `:hover` and
  reduced-motion rule checks: they are counted, and `reduced-motion-missing` becomes `info` with the count.
- `not-interruptible` and `interrupt-jump` rely on Animation objects (keyframe restarts, cancelled
  animations) at any sampling density; for JS-driven motion (rAF, spring libraries) a teleport is only
  detected when frames are sampled about every 16 ms, so a slow or throttled run can miss a small one.
- A component re-mounted mid-animation (a changed React `key`) is seen when the old node and the new one
  have the same tag and role, share a parent and are one to four frames apart; other replacements are
  separate series.
- Long frames are the page's own: the time of the audit's injected scripts (the tracer, `page.evaluate`)
  is taken out of each frame, so a heavy page under heavy machine load can still show an unattributed one.
- On a machine that drops frames (a loaded or virtualised runner), a teleport that lands in a frame of 66 ms or
  more is indistinguishable from a steep easing: the audit re-records the click while some steps are
  undecidable and, if it still cannot be decided, reports an `inconclusive` row.
- Shadow DOM and iframes are not entered; canvas and WebGL motion is not measured.
- Durations are compared within the same element kind (`button`, `a`, `tab`...): put deliberate
  differences in `tokens.durations` or ignore them with a reason.

## Reporting back

Per finding fixed: element, gesture, cause, fix, and the measured value before and after. Findings left
in place: the suppression and its reason. The script result as exit code and its summary line; if it
could not run or audited fewer controls than the page has, say so - never report an unrun audit as passed.
