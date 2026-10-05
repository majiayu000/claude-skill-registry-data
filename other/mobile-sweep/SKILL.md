---
name: mobile-sweep
description: "Runtime sweep that catches mobile-layout bugs: content clipped off the edge of a phone screen, touch targets smaller than 44×44px, text inside a button or input that overflows its visible width, and modals that extend past the viewport.."
version: "1.1.1"
category: ux
platforms: [CLAUDE_CODE]
---

# mobile-sweep

Open a running web app in headless Chromium at three phone/tablet breakpoints
(360×640, 390×844, 768×1024), walk every interactive element + every visible
dialog, and flag the four high-impact mobile-layout failure modes:

1. **Off-screen overflow** — an element extends past `document.documentElement.clientWidth`.
2. **Tiny touch targets** — interactive elements under 44×44 CSS px on touch viewports.
3. **Clipped text** — `scrollWidth > clientWidth` on a button / input / link (visible label is being cut).
4. **Modal width / off-screen modals** — dialogs wider than `100vw - 16px` or that hang off either side.

Plus an optional static CSS scan that flags `grid-template-columns` patterns
packing 3+ fixed-pixel widths summing to >200px without a `@media (max-width: ...)`
override — the exact pattern that caused today's rewards-edit-row clipping bug.

The actual sweep is done by a bundled Playwright script (`scripts/sweep.py`).
The skill body just orchestrates running it, interprets the findings, and
proposes fixes the user can apply directly.

## What the scanner exempts by default

These elements are intentionally tiny or off-screen and should not be
flagged. The scanner skips them automatically; pass `--no-default-ignores`
to see them anyway.

- **Visually-hidden a11y elements** — `.skip-to-content`, `.sr-only`,
  `.visually-hidden`, `.screen-reader-text`, anything with `aria-label`
  starting with "skip", and structurally-detected SR-only elements (1×1
  absolutely-positioned with `overflow: hidden` / `clip-path`).
- **Inline text links in prose** — anchors whose nearest block ancestor
  is `<p>`, `<li>`, `<td>`, `<dd>`, `<blockquote>`, or any element with a
  class containing `prose`. WCAG 2.5.8 explicitly exempts these from the
  24×24 target size rule. Exempted only from the small-touch-target
  check; off-screen and clipped-text still apply.

============================================================
=== PRE-FLIGHT ===
============================================================

Before running, verify:

- [ ] The user can name a URL where the app is currently reachable — a
      Firebase Hosting URL, a `localhost:NNNN` dev server, or a `file://` path
      to a static `index.html`. If the user only said "check mobile" with no
      context, look in the conversation: is there a recently deployed URL, or
      a `firebase deploy` output? Use that.
- [ ] Python 3.8+ is available (`python3 --version`).
- [ ] Playwright + a Chromium browser are installed. Quick probe:
  ```bash
  python3 -c "from playwright.sync_api import sync_playwright" 2>&1
  ```
  If that errors, run:
  ```bash
  pip install playwright && playwright install chromium
  ```
- [ ] If the app requires sign-in to reach the screens being reviewed, the
      user must say so — Playwright will land on the sign-in modal otherwise.
      Options: (a) sign in once with a saved storage state, (b) point at a
      deep-linked screen, (c) use `--open-selectors` to dismiss the sign-in
      modal in-page.

Recovery:

- URL missing → ask for it once. Do not invent one.
- Playwright missing → run the install commands above. The skill is
  worthless without it.
- Auth gate → tell the user; offer to test only the sign-in surface and
  the public landing.

VALIDATION: `python3 scripts/sweep.py --help` exits 0.
FALLBACK: if Playwright install fails (network, sandbox), stop and tell
the user. Do not fake findings.

============================================================
=== PHASE 1: SWEEP THE APP ===
============================================================

Run the bundled scanner:

```bash
python3 ~/.claude/skills/mobile-sweep/scripts/sweep.py <URL>
```

Useful flags:

| Flag                                                      | When to use                                                                                                                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--breakpoints 360,390,768`                               | Override the default breakpoints. Width-only; the script picks a matching height (small Android 360×640, iPhone 390×844, iPad 768×1024, otherwise `width × width*1.78`). |
| `--open-selectors "#open-rewards-btn,#open-settings-btn"` | Click each selector before sweeping. Use this to reach modals/menus that aren't visible on first load. The skill calls these in sequence at each breakpoint.             |
| `--wait-selectors ".board"`                               | Wait for these to appear before sweeping (handy when content is fetched after first paint).                                                                              |
| `--static-css <path>`                                     | Path to scan for rigid-grid CSS issues. Defaults to `.`; pass an empty string `""` to disable.                                                                           |
| `--out mobile-sweep-out`                                  | Output directory for the report + screenshots. Default `mobile-sweep-out/`.                                                                                              |
| `--ignore-selectors ".chip-marketing,.fab-decoration"`    | Add custom selectors to skip during checks. Useful for known decoration-only elements that aren't worth flagging.                                                        |
| `--no-default-ignores`                                    | Disable the built-in WCAG exemptions (skip-to-content links, sr-only/visually-hidden elements, inline prose anchors). Use when you want a strict baseline.               |

The script writes:

- `<out>/mobile-sweep-report.md` — the formatted report
- `<out>/finding-<width>-<state>-<i>.png` — a tight screenshot crop of each finding

Exit code: nonzero if any **errors** are found, so this can gate CI.

VALIDATION: the report file exists and contains at least the header.
FALLBACK: if the script crashes (timeout loading the URL, browser launch
failure), capture the stderr and surface it to the user before guessing
what's wrong.

============================================================
=== PHASE 2: INTERPRET AND FIX ===
============================================================

Open the generated report. Each finding has:

- The selector + label + breakpoint + state (which click triggered it)
- A 1-line measurement (`scrollWidth 320 > clientWidth 80, clipped by 240px`)
- A concrete fix suggestion
- A screenshot crop of the offending area

For **off-screen** and **clipped-text** findings, the dominant pattern is a
rigid CSS grid or flex layout. Don't paper over with `overflow: hidden`.
Instead:

- Switch `grid-template-columns: <pile of fixed px>` to `grid-template-areas`
  that **stack** rows under `@media (max-width: 640px)` so the wide field
  gets its own row.
- For inputs, ensure `min-width: 0` on the parent and `width: 100%` on the
  field so the input fills the available row width.

For **small-touch-target** findings, add:

```css
@media (hover: none) {
  .my-btn {
    min-width: 44px;
    min-height: 44px;
  }
}
```

44px is the iOS HIG minimum. 48px is Material's guidance — both are safe.

For **modal-too-wide** findings, change the modal width to:

```css
width: min(<desktop-width>, calc(100vw - 16px));
```

For the **rigid-grid** static warnings, those are the _latent_ version of
the runtime issues — the user might not have hit them yet because the
modal isn't open, but they will. Apply the same `grid-template-areas`
mobile override.

VALIDATION: a second run of the sweep on the fixed code shows the
specific findings resolved. (Don't claim a fix worked without re-running.)
FALLBACK: if a fix you applied moved a finding instead of removing it,
that's the same bug in a different place — keep iterating until the
report is clean.

============================================================
=== PHASE 3 (OPTIONAL): WIRE INTO CI ===
============================================================

If the user wants this to gate deploys, the script's nonzero exit makes
that easy:

```yaml
# .github/workflows/ci.yml
- name: Mobile sweep
  run: python3 ~/.claude/skills/mobile-sweep/scripts/sweep.py "$DEPLOY_PREVIEW_URL"
```

Only suggest this when the user has indicated CI is set up.

============================================================
=== SELF-REVIEW ===
============================================================

Score the output (1–5):

- **Complete**: Did the sweep run successfully across all three breakpoints?
  Did the report surface findings or confirm clean?
- **Robust**: Did `--open-selectors` reach the modals the user actually
  cares about? Were findings de-duplicated across breakpoints (the same
  element clipped at 360 and 390 should not double-count)?
- **Clean**: Is the report concise? Each finding actionable? No noise like
  decoration-only elements being flagged as touch targets?

If any score < 4:

- Add `--open-selectors` to reach unseen modals, or `--wait-selectors`
  if content was being captured before it loaded.
- If touch-target warnings include obvious non-interactive icons, suppress
  them by adding their parent button class to a future ignore list (for
  now, mention them as "likely false positives" in the report).

============================================================
=== LEARNINGS CAPTURE ===
============================================================

After completing, append one entry to
`~/.claude/skills/mobile-sweep/LEARNINGS.md`:

```markdown
## <YYYY-MM-DD> — <project + scan scope>

- **What worked:** <concrete fix suggested by the report that landed
  immediately, or a `--open-selectors` value that reached the right modal>
- **What was awkward:** <false positives, scroll-clipped inputs that were
  intentional, modals that needed a multi-step click sequence to open>
- **Suggested patch:** <one concrete improvement — "default `--wait-selectors`
  for SPAs to `body[data-loaded]`", "add `--ignore-selectors` for known
  decorative icons", "auto-detect modal open buttons">
- **Verdict:** [Smooth / Minor friction / Major friction]
```

---

## Anti-patterns this skill refuses

- Running on a static screenshot — the whole point is to use a real layout
  engine. If Playwright is not installable, stop and say so.
- Auto-applying fixes without showing the report first. The user wants
  to see what's broken.
- Suggesting `transform: scale()` or `zoom` as fixes. Both break touch
  hit-areas and accessibility — fix the layout instead.
- Flagging hover-only elements that legitimately don't need a touch target
  (decorative pseudo-elements, etc.). The scanner already filters by
  visibility + `isInteractive`; if a class of false positives slips
  through, surface them in LEARNINGS so /evolve can add an ignore.
- Suggesting `overflow: hidden` on a parent as a fix for clipped text. It
  hides the bug, doesn't fix it.
