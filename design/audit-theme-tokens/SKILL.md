---
name: audit-theme-tokens
description: Audit a project's theme, design tokens, and colour accessibility — WCAG contrast across every theme, focus indicators, and design-system hygiene (hardcoded colours bypassing tokens, orphan/unwired tokens, theme parity drift, diluted text utilities) — then fix what's broken and prove it with a rendered-DOM sweep. Use this whenever the user mentions a theme audit, design tokens, colour contrast, WCAG or a11y for colour, dark mode parity, "is my palette accessible", CSS variables organization, hardcoded colours, or asks to review/clean up/reorganize a design system's colours — and also when they ask to check accessibility of a site's look, fix unreadable or washed-out text, make focus states visible, or audit a theme they just built, even if they never say "tokens" or "contrast".
---

# Theme & design-token audit

Two questions, answered with measurements rather than impressions:

1. **Is it legible?** Does every token pair clear its WCAG threshold, in every theme, as actually rendered — at both AA (the normative floor) and AAA (the enhanced target)?
2. **Is the system holding together?** Or are colours hardcoded around the tokens, tokens defined and never used, themes quietly drifted apart?

Both matter, and they fail differently: a palette can be perfectly accessible and structurally rotten, or beautifully organised and unreadable.

## Before anything else

**Find the token layer and enumerate the themes.** An unaudited theme is worse than no audit, and every subsequent step depends on getting this right. `references/stacks.md` covers how to locate tokens per stack (Tailwind v4/v3, plain CSS, CSS-in-JS, JSON design tokens) and what to do when the static scripts can't read them.

```bash
grep -rln --include=*.css -e ':root' -e '@theme' -e 'data-theme' . | grep -v node_modules
grep -rhoE "\[data-theme=['\"]?[\w-]+|\.dark\b|prefers-color-scheme:\s*\w+" <token-file> | sort -u
```

If the project has more themes than the scripts report finding, stop and widen `--css` before continuing.

## The passes

Run all three. They fail in different directions, and any one alone will miss things the others catch.

### 1. Static token matrix — `scripts/token_matrix.mjs`

Scores the semantic pairs the naming convention implies, for every theme, from the definitions alone.

```bash
node .claude/skills/audit-theme-tokens/scripts/token_matrix.mjs src/styles/global.css --fail-only
```

Catches what a crawl never renders: error text, destructive buttons, empty states, disabled rows. Scores every text pair against **both** AA and AAA at once — `XX` for an AA violation (real defect), `A-` for a pair that clears AA but misses AAA (7:1 / 4.5:1 large — an opportunity, not a violation, and never double-counted against the same `XX`), `~~` for advisory (decorative boundaries, which have no AAA tier at all since 1.4.11 never raises). Suggests a concrete replacement value for whichever threshold is unmet — a solved alpha for translucent tokens, a lightness-adjusted `oklch()` for solid ones.

`--fail-only` shows both AA violations and AAA-only misses (tagged separately); `--fail-on-aaa` also makes AAA misses exit non-zero, for a project that has said it targets AAA. `--json` for machine-readable output; `--config pairs.json` to replace the inference entirely when a project doesn't follow the `-foreground` convention.

### 2. Token hygiene — `scripts/token_audit.py`

The structural half. No colour math, no dependencies, runs in a second.

```bash
python3 .claude/skills/audit-theme-tokens/scripts/token_audit.py \
  --css src/styles/global.css --src src
```

Reports undefined references, unwired tokens (declared but absent from `@theme`, so no utility can reach them), orphans, theme parity gaps, duplicate values, Tailwind palette leaks, hardcoded colours, and **diluted text tokens** (`text-muted-foreground/70`) — which are the single most common source of real contrast failures and are invisible to the static matrix.

Use `--ignore-orphan` for token families that are legitimately consumed dynamically.

### 3. Rendered sweep — `scripts/a11y_sweep.mjs` + `scripts/probe.js`

Walks every text node in a running app, resolves what is actually painted behind it, and reports what misses threshold. This is the pass that catches compositing the definitions can't predict, plus vendor CSS that never appears in the token file.

```bash
node .claude/skills/audit-theme-tokens/scripts/a11y_sweep.mjs \
  --base http://localhost:8080 \
  --paths / /blog/ /tools/ \
  --themes "default:" "developer:data-theme=developer"
```

Reports `failuresAA` and `failuresAAA` as two separate, non-overlapping lists (a node failing AA is never also listed as an AAA miss). `--fail-on-aaa` makes the run exit non-zero on AAA misses too, not just AA violations.

Needs a dev server and Playwright. **No Playwright?** Read `probe.js`, pass its body to any browser tool's `evaluate` (Playwright MCP, Chrome DevTools MCP), then call `window.__contrastProbe()`. The probe is deliberately self-contained for exactly this — it returns `{ checked, failuresAA, failuresAAA, failures (alias of failuresAA), all }`.

Pick paths that cover distinct layouts, not distinct content — one blog post, not twelve.

## Then: triage

This is the judgment step, and it is where the audit earns or loses trust. The scripts measure; they cannot tell you which measurements are _requirements_.

Read `references/wcag-thresholds.md` before writing up findings. The critical distinction: 1.4.11 asks **"if this were invisible, could you still identify the control?"** A card outline at 1.4:1 is exempt decoration. An input border at 1.4:1 on a transparent field is a real violation, because it is the only thing making the field visible. Same ratio, opposite verdicts — and the naming heuristic in the scripts is a starting guess, not the answer. Check what actually consumes the token.

Chasing exempt decoration is not a harmless excess of rigour. Raising a decorative border to 3:1 puts hard lines around every card in the product — a visible redesign, justified by a rule that did not apply.

Also flag, though it isn't contrast: **information carried by colour alone** (1.4.1) — chart series identified only by hue, calendar states only by fill. It surfaces from the same review and nobody else will catch it.

**Keep AA and AAA as two different severities, never one merged list.** An AA failure is a real defect regardless of what the project has said about its ambitions — 1.4.3/1.4.11 are the normative floor. An AAA miss (`A-`) is only ever reported on a pair that already clears AA, and is an opportunity, not a defect, unless the project has explicitly said it targets AAA. Reporting the two with equal weight inflates the finding count and buries the AA violations that actually need fixing first.

## Then: present before fixing

Give the user the prioritised findings and let them choose. Rank by user impact, not by ratio: unreadable body text and form errors first, then controls with no visible boundary, then focus indicators, then meaningful graphics — and put every AAA-only miss below all of that, in its own section, clearly labeled as aspirational.

Say plainly which findings you consider exempt and why. That list is evidence you knew where the line was.

## Then: fix

`references/remediation.md` covers how to choose values. The three traps worth knowing before you start:

- **Fix the token, not the call site**, when the failure reaches many components. One edit to `--muted-foreground` beats twenty component edits that drift apart.
- **The foreground flip.** Brightening a fill to fix it as _text_ frequently breaks the text sitting _on_ it — a lighter `--destructive` can push `--destructive-foreground: white` below threshold. Re-run the matrix after every token edit; the `--x-foreground on --x` pair is always in it.
- **Theme inheritance cuts both ways.** A token only declared in `:root` is fixed once for every theme. A token overridden per theme is _not_ — fix the base and the override silently keeps the broken value.

Leave margin. A value landing at 4.52:1 will be re-flagged by the next audit.

## Finally: verify, with a negative control

Re-run all three passes. Then do the step that makes a clean result mean something:

```bash
git stash                                   # back to the pre-fix state
node .../a11y_sweep.mjs --base ... --paths ... --themes ...
git stash pop
```

**A sweep reporting zero failures is worthless until you have shown it can report a non-zero one.** A probe that silently matched nothing looks exactly like a perfect score. This check costs a minute and it is the difference between a verified fix and a hopeful one — it has caught real bugs in the probe itself.

Then write up using `references/report-template.md`, and state the negative control explicitly:

> 8 pages × 2 themes, 1052 text nodes, 0 failures. Validated against the pre-fix tree, which reports 59 failures across the same pages.

## Traps that produce confidently wrong results

Worth knowing even if you never read the script internals, because they are the reason hand-rolled contrast checks are usually wrong:

- **`getComputedStyle().color` does not return authored syntax.** Chromium normalises modern colour spaces to `oklab(0.93 -0.013 0.004 / 0.7)`. Regex-scraping the first three numbers as RGB gives near-black for everything and a report full of 1.01:1 phantoms. `probe.js` round-trips every colour through a canvas so the browser resolves it.
- **Never apply ancestor `opacity` to the foreground alone.** A fade-in wrapper at 0.3 dims text and background together — the ratio is unchanged. Multiplying only the text invents failures on any page with reveal animations.
- **Vendor themes must be measured against the overridden background.** A syntax theme that fails on its own default background often passes once the project restyles the code block — and vice versa. Check the real composite.
- **Alpha tokens composite differently over every surface.** Check the darkest and lightest surface a translucent border lands on, not just one.
- **Hover must never reduce contrast.** `hover:text-primary/80` makes a link harder to read on hover. Always a bug; grep `hover:text-.*/[0-9]` early.

## Files

```
scripts/
  contrast.mjs      colour math library (oklch/oklab/hsl/hex, WCAG, alpha & lightness solvers)
  token_matrix.mjs  static per-theme pair matrix, with suggested replacements
  token_audit.py    structural hygiene — no deps, any stack
  probe.js          in-page contrast probe; usable standalone via any browser tool
  a11y_sweep.mjs    Playwright driver for probe.js across pages × themes
references/
  wcag-thresholds.md  thresholds, exemptions, the border-vs-input distinction
  remediation.md      choosing replacement values without breaking something else
  stacks.md           locating tokens in Tailwind v4/v3, CSS-in-JS, JSON tokens
  report-template.md  report shape, and why the negative control belongs in it
```
