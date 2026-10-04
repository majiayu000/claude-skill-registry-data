---
name: design-system
description: Generate or audit a design-token system, score visual consistency, and detect AI-slop patterns. Use when starting a project that needs tokens, auditing a codebase for palette/type/spacing drift, or reviewing a PR that touches styling. Do NOT use for one-off component styling (use frontend-design) or for SkyyRose brand-taste judgments (use luxury-design-taste — the tokens there are already locked and are not yours to regenerate).
origin: ECC
---

# Design System — Generate & Audit Visual Systems

## When to Use

- Starting a new project that needs a design system
- Auditing an existing codebase for visual consistency
- Before a redesign — understand what you have
- When the UI looks "off" but you can't pinpoint why
- Reviewing PRs that touch styling

**When NOT to use:** on skyyrose.co the token system already exists and is canon — `wordpress-theme/skyyrose-flagship/theme.json` plus the per-collection identity in `data/logo-registry.json` → `collections.<slug>`. Audit mode applies there; **generate mode does not**. Generating a parallel token set for a surface that already has one is the single most damaging outcome of this skill. For SkyyRose taste calls (restraint, motion, imagery) use `luxury-design-taste`; for framework-grounded implementation use `frontend-design`.

## Inputs

| Input | Where | If absent |
|---|---|---|
| Existing token source | `theme.json`, `tokens.css`, `design-tokens.css`, `tailwind.config.*`, `data/logo-registry.json` (`collections`) | Search first with the census command below. **If tokens exist, generate mode is off** — switch to audit |
| The stylesheets to audit | the repo's real CSS/SCSS/TSX, excluding built `.min`/`dist` output | Stop — auditing build output reports the compiler's opinion, not the author's |
| Brand constraints doc | `CLAUDE.md`, `.impeccable.md`, `docs/brand/*` | Stop — an audit with no target palette can only report "it is what it is" |
| Target contrast level | WCAG 2.2 AA unless the project states higher | Default AA; state that you defaulted |

Never proceed on an assumed palette. If you cannot name the intended tokens from a file you read this session, you cannot score drift against them.

## How It Works

### Mode 1: Generate Design System

Analyzes your codebase and generates a cohesive design system:

```
1. Scan CSS/Tailwind/styled-components for existing patterns
2. Extract: colors, typography, spacing, border-radius, shadows, breakpoints
3. Research 3 competitor sites for inspiration (via browser MCP)
4. Propose a design token set (JSON + CSS custom properties)
5. Generate DESIGN.md with rationale for each decision
6. Create an interactive HTML preview page (self-contained, no deps)
```

Output: `DESIGN.md` + `design-tokens.json` + `design-preview.html`

### Mode 2: Visual Audit

Scores your UI across 10 dimensions (0-10 each):

```
1. Color consistency — are you using your palette or random hex values?
2. Typography hierarchy — clear h1 > h2 > h3 > body > caption?
3. Spacing rhythm — consistent scale (4px/8px/16px) or arbitrary?
4. Component consistency — do similar elements look similar?
5. Responsive behavior — fluid or broken at breakpoints?
6. Dark mode — complete or half-done?
7. Animation — purposeful or gratuitous?
8. Accessibility — contrast ratios, focus states, touch targets
9. Information density — cluttered or clean?
10. Polish — hover states, transitions, loading states, empty states
```

Each dimension gets a score, specific examples, and a fix with exact file:line.

### Mode 3: AI Slop Detection

Identifies generic AI-generated design patterns:

```
- Gratuitous gradients on everything
- Purple-to-blue defaults
- "Glass morphism" cards with no purpose
- Rounded corners on things that shouldn't be rounded
- Excessive animations on scroll
- Generic hero with centered text over stock gradient
- Sans-serif font stack with no personality
```

## Procedure

1. **Detect existing tokens before anything else.** Run the census (Verification #1). Non-empty result → audit mode; generate mode is disabled.
2. Read the brand-constraints doc and write down the intended palette hexes and font stacks explicitly. This list is what you score against.
3. Score the 10 audit dimensions. Every finding carries `file:line` and the intended value it deviates from. A score with no file:line is an opinion, not an audit.
4. Measure contrast numerically for each text/background pair you flag (Verification #2). Never assert a ratio you did not compute.
5. Run the slop-detection greps (Verification #3) rather than reading for vibes — the patterns have exact CSS signatures.
6. If the codebase carries a generated-token pipeline, edit the **source** (the registry's `collections` entry on SkyyRose), never the generated artifact, then re-run the drift guard (Verification #4).
7. For theme CSS, any accepted fix requires `cd wordpress-theme && npm run build` — production serves `.min`.

## Verification

Every check states its command, its pass condition, and its evidence scope.

1. **Token-source census** — does a system already exist?

```bash
ls wordpress-theme/skyyrose-flagship/theme.json \
   wordpress-theme/skyyrose-flagship/data/logo-registry.json 2>/dev/null
```

   **PASS (audit mode):** files listed → a system exists, do not generate a second one.
   **PASS (generate mode):** command prints nothing AND `tokens.css`/`tailwind.config.*` are also absent. `[repo]`

2. **Palette-drift census** — measure, do not eyeball:

```bash
grep -rhoE '#[0-9a-fA-F]{6}\b' wordpress-theme/skyyrose-flagship/assets/css/*.css \
  | grep -v '.min.css' | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -8
```

   **PASS:** the top ranks are declared tokens plus neutrals. Any undeclared hue in the top ranks is a drift finding with a count attached. `[repo]`

3. **Contrast measurement** for every pair the audit flags:

```bash
python3 -c "
def lum(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b); return 0.2126*r+0.7152*g+0.0722*b
for fg,bg in [('DC143C','0A0A0A'),('B3B3B3','0A0A0A')]:
    l1,l2=sorted((lum(fg),lum(bg)),reverse=True)
    print(fg,bg,f'{(l1+0.05)/(l2+0.05):.2f}:1')
"
```

   **PASS:** body text ≥ 4.5:1, large text and UI components ≥ 3:1. `[repro]`

4. **Generated-artifact drift guard** — proves the generated files still match their source:

```bash
rtk proxy pytest tests/collections/ -q
```

   **PASS:** `24 passed, 1 skipped` with zero failures (observed 2026-07-28 `[test]`).
   The 1 skip is `tests/collections/test_verify_drift.py:17` — excluded in sparse worktrees. **A SKIP is not a PASS:** that aspect is closed by CI or a full checkout, not by this run. Report it as open, never as green.

5. **Slop signature greps** (adapt the path to the audited tree):

```bash
grep -rnE 'background-clip:\s*text|backdrop-filter:\s*blur|border-(left|right):\s*[2-9]' \
  wordpress-theme/skyyrose-flagship/assets/css/*.css | grep -v '.min.css' | head
```

   **PASS:** zero hits, or every hit is justified in writing at its `file:line`. `[repo]`

Inherited rules: a check that errors or times out produced an artifact, not a pass — re-run it by hand. Before claiming a drift finding is caused by the change under review, run the same census against a pristine tree via `git archive HEAD wordpress-theme | tar -x -C <scratch>` and diff the *contents* — never `git stash` (the stack is shared across worktrees).

## Examples

**Audit an existing UI (real, this repo; census re-run 2026-09-18, CSS counts 2026-07-28):**

```bash
$ ls wordpress-theme/skyyrose-flagship/theme.json wordpress-theme/skyyrose-flagship/data/logo-registry.json
wordpress-theme/skyyrose-flagship/data/logo-registry.json
wordpress-theme/skyyrose-flagship/theme.json
$ python -c "import json;print(sorted(json.load(open('wordpress-theme/skyyrose-flagship/data/logo-registry.json'))['collections']))"
['black-rose', 'kids-capsule', 'love-hurts', 'signature']
```

A token system exists → **generate mode is off**, audit only. Census then returned `478 #b76e79 · 146 #0a0a0a · 103 #d4af37 · 49 #050505 · 48 #ffffff · 46 #dc143c · 31 #c0c0c0 · 14 #2a2a2a` across 52 non-minified stylesheets — top ranks all declared tokens or neutral surface steps, so color-consistency scores high with no drift finding `[repo]`. The drift guard ran `24 passed, 1 skipped` `[test]`.

**Generate for a greenfield app** (only after check #1 prints nothing):

```
/design-system generate --style minimal --palette earth-tones
```

**Check for AI slop:**

```
/design-system slop-check
```

## Failure modes

- **Generating a parallel token system on top of an existing one.** The most damaging outcome; the two systems then fight forever. Check #1 exists to make this impossible — run it first, always.
- **Editing a generated artifact.** On SkyyRose, `design-tokens.css` and `sot.json` are generated from the registry's `collections` section (see `data/collections/README.md`). Editing the output means the next regeneration silently reverts your fix. Edit the source.
- **Scoring contrast by eye.** `#DC143C` on `#0A0A0A` reads confident and measures 3.97:1 — below AA. Compute it (check #3).
- **Auditing minified output.** `.min.css` is machine-formatted; findings there are noise. Filter with `grep -v '.min.css'` as every command above does.
- **Reading a SKIP as green** — `test_verify_drift` skips in sparse worktrees (bug-257 class: sparse-checkout guards must skip narrowly and be reported, not swallowed). Name who closes it.
- **Fail-open audit** — no brand doc found, so the audit proceeds against an assumed palette and reports "consistent". Absent input = stop (bug-230, ×6).
