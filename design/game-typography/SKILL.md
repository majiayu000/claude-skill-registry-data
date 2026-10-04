---
name: game-typography
description: 'The arcade''s type system: the Fraunces and Outfit pairing, the roles each face plays, the numeric styling that game UI lives on, and the sizing floor set by measured contrast headroom. Use when adding or restyling any text, number, label or button in Payload, Ledger Lane or the hub, when choosing a size or weight, or when text feels cramped, illegible or off-brand.'
---

# Type in the arcade

Two faces, loaded from Google Fonts, with strictly separate jobs. Keep them
separate. Mixing the roles is what makes a game UI read as generic.

| Face | Role | Where |
|---|---|---|
| Fraunces, serif, 500/650/700 | Identity and result numbers. Anything the player should feel. | Wordmark, game titles, modal headline, big stat values, quota, rank titles |
| Outfit, sans, 400 to 700 | Everything operational. Anything the player should read. | Body copy, part rules, labels, buttons, banners, HUD text |

Fallbacks are declared and must stay: `'Fraunces', Georgia, serif` and
`'Outfit', 'Segoe UI', system-ui, sans-serif`. Google Fonts is the only external
host the CSP allows, and the service worker caches both, so a face added from
anywhere else silently falls back.

In Payload these are Tailwind's `font-display` and `font-sans`, configured in
`tailwind.config.js`. Ledger Lane and the hub still declare them in CSS.

## Numbers are the game

Payload is a game about numbers changing. Every digit that updates in place or
sits in a column needs `tabular-nums`, or the layout twitches on every drop.
Already applied to the score, quota, drop ticker, column projections, stat tiles
and totals. Do not add a new counter without it.

Reach for Fraunces when a number is a result the player earned: round score, the
quota they must beat, banked total, best drop. Reach for Outfit when it is
operational state: drops left, part badges like `+3` and `×2`, the projected
totals on the drop buttons. That split is what makes the modal's stat row feel
like a payout and the HUD feel like instrumentation.

## The scale, and its floor

Sizes in use, smallest first: 9.5px part badges, 10px stat captions and section
headings, 10.5px chips, 11 to 11.5px rule text, 12 to 13.5px banners, body and
buttons, 15 to 19px HUD values, 21 to 27px headlines.

The floor is set by contrast, not taste. Two pairs are close to it, and both were
measured rather than assumed:

- `steel` on `card` is 4.91:1, against the 4.5:1 that text requires. Never darken
  `steel` or lighten `card`.
- `edge` on `card` is 3.32:1, against the 3:1 that WCAG 1.4.11 requires for a
  component boundary. It was 2.39:1 until #31, under a comment claiming it passed.
  Measure before changing a border colour, and put the number in the comment
  rather than an adjective.

`card` is the tightest background for both, so check any new colour against
`#22262e` rather than against `panel` or `ground`.

Text below about 12px should not use `steel` on `card`; use `ink`, which measures
14.81:1. The 9.5px badges and 10px captions are the ones to watch. Anything both
secondary and tiny is better solved by removing it than by greying it further.

## Rules that keep it coherent

- Uppercase labels get letter-spacing, `.06em` to `.14em`. Uppercase without
  tracking looks broken.
- Headlines get `line-height: 1.15`, body gets 1.5 to 1.6. The modal headline and
  wordmark are tight, banners and rules text are loose. Nothing sits between.
- Never centre a paragraph. Only single-line labels and stat tiles are centred.
- Weight carries emphasis, not colour alone. Emphasis in banner copy switches to
  `ink` and 600 together, because colour alone fails for low-vision players. The
  same rule is why the placement preview puts its rating in the accessible name
  and not only in the shading.
- Sentence case for copy, Title Case for names. Part names such as Tuning Fork,
  rank titles and game names are Title Case; every sentence of explanation is
  sentence case.

## Known debt

Every size is `px`. Page zoom works, but a player who raises their browser's
default font size gets no scaling at all: setting root `font-size: 32px` changes
nothing, which was verified rather than assumed. Converting body copy to `rem` is
the fix. The board grid and the marble can stay `px`, since they are a
fixed-geometry play surface. Do it as a deliberate pass rather than
opportunistically, so the scale stays consistent.
