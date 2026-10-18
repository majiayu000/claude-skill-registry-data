---
name: design-ship-gate
description: "Done-gate for a web page built by a small model. Run it before saying a landing page is finished: brief coverage, then nine executable checks, one per defect seen in Qwen3.8-27B pages (fonts, OG tags, dark mode, 390 px overflow, number wrapping, hero collisions, tracking, language, a script that does not parse). Commands and pass conditions, no design theory."
triggers:
  - /design-ship-gate
  - ship gate
  - design done gate
  - before I say the page is done
  - ตรวจก่อนส่งหน้าเว็บ
  - ก่อนบอกว่าหน้าเสร็จ
  - เช็คหน้า landing ก่อนส่ง
---

# Ship gate (`design-ship-gate`)

**Run this before you say a page is finished.** Read the brief again, then run every check below and paste each command's output. A check you did not run is a check that failed. Fix, re-run, then report `GATE: 9/9` with the outputs. **Run check 9 first**: it needs only `node`, and a page whose script does not parse is not a page.

Why a gate and not more rules: the design rules were loaded and the pages still broke them. Nine pages from one brief, audited with real renders: more than two font families **5 / 9**, no Open Graph tags **6 / 9**, hero elements colliding **3 / 9**, a number split from its unit **3 / 9**. Every one of those was found by a command, never by re-reading the rule.

## 0. Brief coverage — write the list first

Before the checks, write this table in your answer and fill every row:

| the brief names | element(s) that deliver it |
|---|---|
| each style word in the brief (e.g. "Liquid Glass") | selector or section |
| dark mode | `prefers-color-scheme` block or toggle — **a deliverable even when the brief does not say it** (4 of 5 pages skipped it unasked) |
| Open Graph tags | `<meta property="og:...">` — same, a deliverable when unnamed |
| the brief's language | the page copy is in it (2 / 9 answered a Thai brief in English) |

A row with an empty right-hand cell is a missing deliverable, not a stylistic choice. A page in one generic direction (a SaaS card grid for an editorial brief) fails this table before any check runs.

## 1–9. The checks

Set `P=index.html` (the page) and `G=<this skill's directory>` (where `gate-dark.js`, `gate-390.js`, `gate-hero.js` live). Node with Playwright is needed for 4–6 (`npm i -D playwright` in the page's folder, or `NODE_PATH` to an existing install); if it is absent say so in the report instead of skipping silently.

**1. At most two font families.** Count what is *loaded and primary*: every family in a Google Fonts `family=` link, plus the FIRST name of each `font-family` / `--font-*` declaration. Fallbacks after the comma (`Segoe UI`, `SF Mono`, `Helvetica Neue`, `system-ui`) are not families — a first draft of this check counted them and called a two-font page a five-font page. Pass: the list has `<= 2` entries.
```sh
{ grep -oE "family=[A-Za-z+]+" "$P" | sed 's/family=//; s/+/ /g'; grep -oiE "(font-family|--font[a-z0-9-]*|--ff[a-z0-9-]*)[[:space:]]*:[^;},]+" "$P" | sed -E "s/^[^:]+:[[:space:]]*//; s/['\"]//g; s/[[:space:]]+$//" | grep -viE "^(var\(|sans-serif|serif|monospace|system-ui|ui-|inherit|initial|-apple)" ; } | sort -u
```

**2. Open Graph present.** Pass: all three lines print.
```sh
grep -oE 'property="og:(title|description|image)"' "$P" | sort -u
```

**3. Dark mode exists.** Pass: at least one match.
```sh
grep -cE "prefers-color-scheme|data-theme|\.dark\b|theme-toggle" "$P"
```

**4. In dark mode every stat is visible.** The failure was `color: var(--paper)` on a stats band after dark mode was added later — in the dark theme `--paper` went dark too and the numbers vanished. The script reads text nodes, because a stat is written `9.4<span>B</span>` and an element-level test skips it; "invisible" is a luminance distance under 60 to the effective background, which is what the audit saw. Pass: `invisible: 0`.
Pass: `invisible: 0` **with `candidates:` above zero** — a run that examined nothing prints the same `invisible: 0` as a clean page. A stat is any text node under 40 characters carrying a digit, so `9.4B users` counts; and where no element paints a background the comparison is against the real canvas, not white (both #359).
```sh
node "$G/gate-dark.js" "$P"   # invisible: 0 candidates: n
```

**5. No horizontal overflow at 390 px — with `overflow-x:hidden` removed for the test.** One page hid a 56 px overflow behind that rule. Pass: `overflow: 0` **and** `clipped: 0` — an inner wrapper with `overflow-x: hidden` does not scroll the page, it throws the content away, and reading only the page width called that clean (#359).
```sh
node "$G/gate-390.js" "$P"
```

**6. No text collides with the headline.** A column ruler `01–12` sat across the `h1`; a glass lens sat over "EST. 1998". Both were text over text, and the ruler was even below the headline in z-order, so the script does not look at z-index: any positioned element carrying its own visible text whose box overlaps the `h1` box is a collision. Decorative blobs and glows carry no text and pass. Pass: `colliding: 0`. The fix is to move the text (the ruler into the gutter, the lens off the tagline), not to hide it.
```sh
node "$G/gate-hero.js" "$P"
```
A page with no `h1` prints `colliding: 0` and `note: no h1 found` — the check cannot run, and reporting that as a collision sent the model looking for one to fix (#359).

Known miss: a glass lens (no text of its own) over a tagline that is not the `h1` is not caught — 2 of the 3 audited collisions are. Look at the hero once with your eyes as well.

**7. A number stays on one line with its unit.** `100B+` split into `100` / `B+` because `.big span{display:block}` also matched the unit's `<span>`. Pass: nothing prints (no descendant `span` rule under a numeric block), and `≈5B+/day`-style stats use `white-space:nowrap`.
```sh
grep -nE "\.(big|stat|num|n|value)[a-z-]* +span *\{" "$P"
```
Use `.big > span` for a deliberate line break, and put the unit inside the same `nowrap` element as the number.

**8. Nothing under 24 px is tracked tighter than −0.025em.** A wordmark at 22 px with `-0.03em` read "Goole". The command lists every tighter value, `em` and `px` alike (the first version stopped at `-0.09em`, so `-0.1em` and `-1px` — the tightest values there are — were invisible to the check that exists to find them; review 2026-09-06); grep cannot see the font size, so for each line printed, name the selector's font size in the report. Pass: every printed line is a heading or display number at ≥ 24 px (the tracking hack is for those only); anything smaller goes back to `letter-spacing: 0`.
```sh
grep -nE "letter-spacing: *-(0\.(0(2[6-9]|[3-9])|[1-9])[0-9]*em|[0-9.]+px)" "$P"
```

**9. Every script the page ships parses.** A Qwen3.8-27B page passed checks 1, 2, 3, 7 and 8 (no Playwright for 4–6) while `js/blob.js` could not load — `Private field '#rippleCursor' must be declared in an enclosing class`, left behind when the model deleted an "unused" field in a self-review edit (#375). An ES module that fails to parse takes every module that imports it down with it, so the page rendered no scene at all, and no grep sees that. A file with `import`/`export` is parsed **as a module**: `node --check file.js` on a `.js` with no `package.json` exits 0 on that very error, so it cannot be the fallback. Pass: nothing prints. A printed line **fails the gate whatever the other checks say** — fix it and re-run all nine. Needs only `node`, so run it first.
```sh
find "$(dirname "$P")" -type d -name node_modules -prune -o \
     -type f \( -name '*.js' -o -name '*.mjs' \) -print |
while read -r f; do
  if grep -qE '^[[:space:]]*(import|export)[[:space:]{*]' "$f"; then
    node --input-type=module --check < "$f" 2>/dev/null     # a module, parsed as one
  else
    node --check "$f" 2>/dev/null                           # a classic script
  fi || echo "FAIL $f"
done
```

## Report

```
GATE: n/9  (parse 0 failed · fonts 2 · og 3/3 · dark yes · invisible 0 of n candidates · overflow 0 clipped 0 · colliding 0 · span-rule none · tracking ok)
brief table: k rows, all filled
```
Paste the command outputs under it. `GATE: 9/9` with no outputs is not a pass.

## What this does not touch

Design choices, copy, colour, layout — `design-rules` and `design-audit` own those. This file only says whether the page may be called finished. It was calibrated on nine pages from one brief and one model; the counts above are what was seen, not a rate.
