---
name: css-cascade-discipline
description: CSS cascade, specificity, and selector-weight discipline for large legacy stylesheets (50+ plain-CSS files, no build-time scoping). Use when adding, changing, or reviewing CSS in wordpress-theme/skyyrose-flagship — a color/typography override, a new component rule, a scoped reset, or a "the style isn't applying" investigation. Do NOT use for React/CSS-Modules/Tailwind work where the compiler already scopes selectors (use frontend-patterns), and do NOT use it as the .min build checklist (that is theme-min-build) — this skill is about which selector wins, not which bytes ship.
---

# CSS Cascade Discipline

Plain-CSS codebases have no scoping compiler. Every new rule fights every existing rule. This skill exists because a shipped fix (`#719`) was silently defeated: `.hero-cta-primary { color: var(--void,#050505) }` (specificity 0,1,0) lost to a scoped reset `.homepage-v2 a { color: inherit }` (0,1,1) — white-on-white CTA in production while the "fix" sat in the served file.

## When to use

**Observable events:**

* You are adding a rule that sets a property some other rule already sets on the same element — any color, `font-family`, `display`, or spacing override in `wordpress-theme/skyyrose-flagship/assets/css/`.
* A declaration is present in the served CSS file but the browser paints something else ("the fix is in the file and the page still looks wrong").
* You are about to land a *scoped reset* (`.some-section a { … }`, `.page-class button { … }`) — the highest-blast-radius change in a plain-CSS tree.
* Review of a PR that touches two or more stylesheets that both style the same component.

**When NOT to use:**

* **React with CSS Modules, styled-components, or Tailwind** — the toolchain generates unique class names, so cross-file specificity fights do not arise. Use `frontend-patterns`.
* **Pure build/minification questions** — "did the `.min` get rebuilt", "is the version bumped". That is `theme-min-build`. This skill only answers *which selector wins*; the `.min` step appears here because a cascade fix that never reaches the `.min` is invisible, not because this skill owns the build.
* **Choosing a color/font value.** Brand canon is locked elsewhere (`design-qc`, `docs/brand/`). This skill governs whether the value you chose actually applies.

## Inputs

| Required before you start | How to confirm | If absent |
|---|---|---|
| The exact element + property in dispute | name it: `.hero-cta-primary` / `color` | **STOP.** Without a named property you cannot compute a winner, and "restyle the hero" is not a cascade task. |
| The full list of stylesheets the page enqueues | read `wordpress-theme/skyyrose-flagship/inc/enqueue.php` | **STOP.** Load order decides specificity ties. Guessing it produces a fix that loses to a file you did not know was there. |
| Every competing rule for that property | `grep -rn '<selector-fragment>' wordpress-theme/skyyrose-flagship/assets/css/ --include='*.css' \| grep -v '\.min\.'` | **STOP — never proceed on the assumption that no competitor exists.** That assumption *is* bug #719. Absent census = do not write the rule. |
| A pristine baseline for the linter | see Verification rule 4 | **STOP** before attributing any stylelint error to your change — the tree already has 452. |

Always exclude `.min.` from greps. The minified siblings are generated; matching them doubles every
result and tempts you to "fix" a build artifact by hand.

## Specificity math (memorize)

`(inline, id, class/attr/pseudo-class, element)` — compare left to right, first difference wins. Ties → later in source order wins (across files: later-enqueued file wins).

- `.hero-cta-primary` → (0,1,0)
- `.homepage-v2 a` → (0,1,1) — class + ELEMENT beats a lone class for that element
- `.hero-cta.hero-cta-primary` → (0,2,0) — the standard escalation
- `[data-collection="love-hurts"] .v7card__add` → (0,2,0); attribute selectors count as class-weight

## Procedure — before writing ANY override rule

1. **Find the competition.** Grep every stylesheet the page loads for rules that could set the same property on the same element: the element's classes, its tag scoped under ancestors (`.section-scope a`, `.page-class button`), and `*` resets. In skyyrose-flagship, the known scoped resets are in `homepage-v2.css` (`.homepage-v2 a { color: inherit }`), `main.css` and `commercial-polish.css` (`* { … !important }` inside `@media print` — inactive on screen, don't panic-match them).
2. **Compute both weights.** Your rule must beat the strongest competitor OR come later at equal weight. When targeting an element (`a`, `button`, `input`) under a scoped reset, you need ≥ (0,1,1): double-class the component (`.x.x-variant`) or scope it (`.page-scope .x-variant`).
3. **Never solve with `!important`.** It wins today and creates the next un-overridable fight. Escalate specificity structurally instead.
4. **Custom-property fallbacks don't fix cascade losses.** `var(--token, #literal)` protects against a missing token, NOT against a competing selector. Diagnose which failure you actually have before choosing the fix.

5. **Rebuild the `.min`** — production serves it. `cd wordpress-theme && npm run build`.
6. **Run the Verification checks below** and paste real output.

## Probing a CSS fix in the browser (why `getComputedStyle` lies)

`getComputedStyle` probes lie to you in three specific ways:

- **Transitions mask inline probes**: `el.style.color = 'red'` read synchronously returns the transition's t=0 value when the element has `transition: all`. Set `el.style.setProperty('transition','none','important')` first.
- **CSSOM walkers**: `CSSStyleRule.cssRules` is always truthy (CSS nesting API) — `if (r.cssRules) walk(...); continue;` skips every style rule. Check `r.selectorText && r.style` FIRST, recurse `r.cssRules` separately.
- **Browser/CDN cache**: the page's CSSOM may be a stale copy even after deploy. Verify the RULE TEXT in the page's own CSSOM (`r.style.cssText`), not just the file fetched by curl — curl gets a fresh edge copy, the browser may not.

Decisive experiment when a declaration mysteriously loses: set `color: red !important` ON THE RULE via CSSOM. If red applies, cascade defeat confirmed — hunt the winner by weight, not by vibes.

## Landing a scoped reset safely (the other direction)

Adding a rule like `.my-section a { color: inherit }` retroactively beats every (0,1,0) component rule inside that section. Before landing one: grep for component classes used inside the section that style the same property at (0,1,0) and pre-escalate them. A scoped reset without this census is a time bomb.

## skyyrose-flagship specifics

- Production serves `.min` — after ANY css edit: `cd wordpress-theme && npm run build`, verify the fingerprint in the `.min` output, not just source.
- Load order = enqueue order in `inc/enqueue.php`. A later-enqueued file wins specificity ties against an earlier one.
- Prefer scoping new component rules under the template's body/section class (e.g. `.homepage-v2 .hero-strip`) — both for weight and for blast-radius control.

## Verification

Run from `/Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon`. Four independent checks;
each can return "no".

1. **Lint the source, not the build.** The tree has a large pre-existing baseline, so `exits 0` is the
   wrong pass condition — it would fail every time and teach you to ignore it.

```bash
cd wordpress-theme && npx stylelint 'skyyrose-flagship/assets/css/**/*.css' --allow-empty-input
```
**PASS:** the *set of violation lines* is unchanged from the pristine baseline (see check 4) — no new
`file:line rule` entry attributable to your edit.
**Observed baseline 2026-07-28: `452 problems (452 errors, 0 warnings)`, 154 auto-fixable** `[repro]`.
A bare `--fix` across the tree would rewrite 154 unrelated sites — do not run it to "clean up".

2. **The shipped bytes match the source you edited.** Production serves `.min`; a source-only edit ships
   nothing, so a cascade fix can be perfect and still invisible.

```bash
cd wordpress-theme && npm run build && npm run verify:aspect min-sync
```
**PASS:** `[PASS] min-sync   every .min css/js byte-identical to a fresh build`.
**Observed 2026-07-28: PASS, `0 fail, 0 warn`** `[repro]`.

3. **The live document actually serves the version you think it does.** Batcache serves stale, so the
   cache-buster is not optional, and **never `WebFetch`** — it strips `<script>` and misleads.

```bash
curl -s "https://skyyrose.co/?cb=$(date +%s)" | grep -o 'skyyrose-flagship/style[^"]*ver=[0-9.]*' | head -1
```
**PASS:** the `ver=` value equals `SKYYROSE_VERSION` in `functions.php`.
**Observed 2026-07-28: `skyyrose-flagship/style.min.css?ver=1.12.8`** `[live]`. If your fix is not in
1.12.8, the live page cannot contain it regardless of what the working tree says — that gap is exactly
the `[repo]` → `[live]` jump the evidence rules ban (bug-287).

4. **Attribution before you claim a finding is yours (rule 4).** With a 452-error baseline, "stylelint
   is red" proves nothing. Extract the pristine tree and diff the violation *contents* — a new error
   hides as one more line inside an already-red check.

```bash
mkdir -p /tmp/css-attr && git archive HEAD wordpress-theme/skyyrose-flagship/assets/css | tar -x -C /tmp/css-attr
ln -s "$PWD/wordpress-theme/node_modules" /tmp/css-attr/node_modules 2>/dev/null
(cd /tmp/css-attr && npx stylelint 'wordpress-theme/skyyrose-flagship/assets/css/**/*.css' \
   --formatter unix 2>/dev/null | sed 's|^/tmp/css-attr/||' | sort) > /tmp/css-attr/before.txt
(cd wordpress-theme && npx stylelint 'skyyrose-flagship/assets/css/**/*.css' --formatter unix 2>/dev/null \
   | sed 's|^|wordpress-theme/|' | sort) > /tmp/css-attr/after.txt
diff /tmp/css-attr/before.txt /tmp/css-attr/after.txt
```
**PASS:** `diff` prints nothing, or only `>` lines you intended. `[test]`
**Never `git stash`** to make a pristine tree — the stash stack is shared across worktrees and a pop can
destroy another session's work.

**Prove the check can fail (rule 3).** Before trusting check 2, break it once: touch a source `.css`
without rebuilding, re-run `npm run verify:aspect min-sync`, and confirm it reports the file stale;
then `npm run build` to restore green. A gate never observed failing is decoration.

**A gate that dies is not a gate that passed (rule 1).** `verify:aspect` and `stylelint` both exit
non-zero on internal error as well as on findings. If either aborts (missing `node_modules`, killed
process), its output is an *artifact* — re-run it; do not record silence as clean. (bug-230, ×6.)

**A SKIP is not a PASS (rule 2).** Whether the fixed element is *visually* correct at 390px and on
desktop is **not** checked by anything above — `verify-theme.sh --list` classifies `responsive` and
`a11y-interactive` as BROWSER aspects the script does not execute. Name the closer: a Playwright or
Chrome DevTools pass by the caller. Reporting a cascade fix as "done" on CLI evidence alone repeats
the #719 failure in the opposite direction.

## Worked example

**The defect this skill exists for**, read from the real file on 2026-07-28:

```bash
$ grep -n "homepage-v2 a\|hero-cta-primary" wordpress-theme/skyyrose-flagship/assets/css/homepage-v2.css
55:.homepage-v2 a { color: inherit; text-decoration: none; }
377:.hero-cta.hero-cta-primary {
379:	   .hero-cta-primary (0,1,0) loses that cascade and inherits white-on-white. */
383:.hero-cta-primary:hover {
388:.hero-cta:not(.hero-cta-primary):hover {
```

The two competitors, verbatim:

```css
/* homepage-v2.css:55 — the scoped reset, specificity (0,1,1) */
.homepage-v2 a { color: inherit; text-decoration: none; }

/* homepage-v2.css:377 — the landed fix, specificity (0,2,0) */
.hero-cta.hero-cta-primary {
	/* Double-class beats `.homepage-v2 a { color: inherit }` (0,1,1) — a bare
	   .hero-cta-primary (0,1,0) loses that cascade and inherits white-on-white. */
	background: #fff;
	color: var(--void, #050505);
}
```

**The math, left to right:** `(0,1,1)` vs `(0,1,0)` → equal ids, equal classes, `1` element beats `0`
element, so the reset won and the original fix lost — a white CTA label on a white background, live,
while the "fix" sat in the served file. Escalating to `.hero-cta.hero-cta-primary` = `(0,2,0)`, which
beats `(0,1,1)` at the class column and never reaches the element column. Note what was *not* used:
no `!important`, and the `var(--void, #050505)` fallback was already there and never helped — a
custom-property fallback protects against a missing token, never against a competing selector.

Then the two gates that make the fix real:

```bash
$ cd wordpress-theme && npm run verify:aspect min-sync
[PASS] min-sync               every .min css/js byte-identical to a fresh build
VERIFY PASS — 0 fail, 0 warn.

$ curl -s "https://skyyrose.co/?cb=$(date +%s)" | grep -o 'skyyrose-flagship/style[^"]*ver=[0-9.]*' | head -1
skyyrose-flagship/style.min.css?ver=1.12.8
```

**Honest scope:** those two prove the source and the build agree `[repro]`, and that production serves
theme 1.12.8 `[live]`. They do **not** prove the CTA renders dark-on-white for a real visitor — that is
a pixel claim needing a browser (rule 2 SKIP, closed by the caller's Playwright pass).

## Failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Declaration is in the served file, browser paints something else | Cascade defeat — a higher-weight or later-source rule wins | Census both selectors, compute weights, escalate structurally (bug #719) |
| Fix works locally, production unchanged | `.min` not rebuilt, or `SKYYROSE_VERSION` not bumped so visitors hold a cached asset | `npm run build`; bump the version triple (`functions.php`, `style.css`, `readme.txt`) |
| `getComputedStyle` returns the pre-animation value | `transition: all` — a synchronous read gets t=0 | `el.style.setProperty('transition','none','important')` first |
| A CSSOM walker skips every rule | `CSSStyleRule.cssRules` is always truthy under the nesting API | Test `r.selectorText && r.style` first; recurse `r.cssRules` separately |
| `!important` fixes it today, nothing can override it tomorrow | Specificity escalated with a hammer | Revert; double-class or scope instead |
| Adding `var(--token, #fallback)` doesn't fix the color | The failure is a cascade loss, not a missing token | Diagnose which failure you have before choosing the fix |
| A new scoped reset silently breaks components inside the section | Reset at (0,1,1) retroactively outranks every (0,1,0) component rule | Census component classes in that section and pre-escalate them before landing the reset |
| Stylelint "went red because of my change" | 452-error pre-existing baseline | Attribute via `git archive`; diff violation lines, not counts |
| curl shows the old CSS right after deploy | Batcache stale copy | Cache-bust: `?cb=$(date +%s)`; never `WebFetch` (strips `<script>`) |
| Grep returns twice the expected hits | `.min.css` siblings matched | Add `\| grep -v '\.min\.'` |
