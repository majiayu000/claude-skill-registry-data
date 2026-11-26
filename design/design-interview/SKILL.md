---
name: design-interview
description: >-
  Builds 3 different visual variants side by side in the browser and records the pick in DESIGN.md. Use when the user wants a new look, UI, screen design or game feel and the style isn't fixed. Not for styling within an existing design system.
license: Apache-2.0
metadata:
  level: "process"
  uses: ""
  agents: ""
  tokens: "994"
---

Turns "make it look good" into a visual choice: a short interview, 3 variants that differ in direction, a gallery in the browser, and the user's pick or mix written down as tokens. Builds no product code.

## Steps
1. *Always.* Read the CLAUDE.md contract, an existing `DESIGN.md`, `docs/design/`, the spec if one exists, and the stack: CSS framework, theme or token files, component library, game engine. An existing design system binds every variant.
2. *Always.* Say the mode and path in one line. Mode: web, mobile (ask iOS or Android) or game. Path: one component inside an existing system → 2 variants; a new screen or look → 3.
3. Interview, at most 2 rounds of ≤4 questions, recommended answer first; skip what step 1 answered:
   - what screen or moment, for whom, the one thing it must make easy;
   - 3 feeling words, and references: sites, apps, games, plus one from outside screens (a receipt, a shop sign, a toy);
   - the anti-reference: what it must never feel like, what they hate;
   - hard constraints: brand colours, fonts, platform, real content and data to use.
4. Turn every adjective into specs and play them back as one table for ok: type (families, scale), colour (base, text, one accent and where it may appear), spacing scale, radius, motion (what moves, how long), layout idea. "Calm" is not a spec; "16px base, 1.25 scale, one accent on primary buttons only" is.
5. Write 3 briefs from the same specs with different lenses: **safe** (the best-practice answer closest to the references), **bold** (one strong idea pushed hard), **odd** (an unexpected reference from another domain). Lenses differ in layout, hierarchy and type, not only colour.
6. Build: one fresh subagent per variant, all started in one message, `model: opus` unless CLAUDE.md or the user states a model or plan limit (then `sonnet`). Each writes `docs/design/<feature>/<a|b|c>.html` and answers in ≤10 lines.
7. Check each file before showing: no `src`/`href` to anything except Google Fonts, no lorem, John Doe, Acme or round fake stats, no avoid-list tell (grep). Fix by re-briefing that agent once.
8. Gallery: copy `${CLAUDE_SKILL_DIR}/assets/gallery.html` to `docs/design/<feature>/index.html` and fill the config block at the top (feature, mode, variants, parts). Open it (`open`, `xdg-open` or `start ""`); if that fails or the session is remote, print the path.
9. The user picks or mixes and pastes the gallery's "Copy choice" text. A mix → one more Opus agent builds `d.html` from the picked parts, then pick again. Stop after 2 rounds: the user picks from what exists.
10. Record: `docs/design/<feature>/choice.md` and the tokens in `DESIGN.md`. Edit an existing DESIGN.md in place and show the diff first.

## Rules
- Never write product code here; variants are throwaway files under `docs/design/`.
- Never build variants yourself: a fresh context per variant keeps them apart; one context converges them.
- No adjective reaches a brief; only spec values and the avoid-list do.
- Variants are self-contained: inline CSS and JS, no CDN, no fetch or modules (they break under `file://`); real content from the project or the user.
- Never show variants that differ only in colour or radius; regenerate the closest pair with a sharper lens.
- An existing design system wins: variants vary inside it and name every place they break it.
- Mobile follows the platform: Apple HIG for iOS, Material 3 for Android.
- Never pick for the user. Your recommendation is one line, after they have looked.

## Branches
If the mode is game, read `references/game.md`.
If writing variant briefs, read `references/brief.md`.
If recording the choice, read `references/output.md`.

## Report
- Mode, path, variant files, gallery path.
- Choice (pick or mix) and where it was recorded.
- Not checked: <e.g. real-device rendering, accessibility contrast beyond the accent>

Next: build it with a plan (foma-skills:planning); the spec stays the source of what, DESIGN.md of how it looks.
