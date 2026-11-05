---
name: console-ui
description: Use whenever you create or change any page of the Agent Console or Docs page (dashboard, panel, card, step bar, table). Starts from the kit's shared tokens and components so every page looks and pulses the same.
---

# Console UI: build from the kit's pieces, never from scratch

1. Open `references/tokens.css` and paste the `:root` block unchanged. Never retype a colour; add a new token there first, then use it.
2. Take each element from `references/components.md` (card, dot, step bar, tick row, table). If a piece is missing, add it to the file, then use it. Do not make a one-off.
3. Colour means status: green done, amber needs you, red blocked, cyan live, grey not started. The look is dark with neon in three tones (`--neon-hi`, `--neon-mid`, `--neon-lo`): one hi card per page.
4. Make it pulse, cheaply: only `transform` and `opacity` animate. Add reduced-motion.
5. Numbers use `tabular-nums`. Text lines at most 65 characters wide. Labels in sentence case, never shouting capitals; plain header (no `>`, `_`, `#`).
6. Words are for a business owner: no tool names, no ids first.
7. Verify what is built: muted text at least 4.5:1 contrast; every control has a visible keyboard focus; selection colour is themed.
8. Never: a coloured side stripe wider than 1px, an eyebrow label above each heading, nested cards, the big-number-plus-tiny-label template as the page structure, gradient text anywhere except the page title. The owner's brief wins over any generic default: neon, glow, rings and the indigo/violet palette are declared choices (see `docs/console/DESIGN.md`).
9. The default look is deep indigo surfaces with a Violet accent (`--bg #0c0820`, `--panel #16123a`, accent from `--acc`). Status colours keep their meaning and are never themed.
10. Responsive is structural: every page has `<meta name="viewport">`; under 900px the header wraps and the tab bar scrolls inside itself; under 640px tables scroll inside their own box and margins shrink; on touch screens controls are at least 40px. The page itself never scrolls sideways. Check 390px and 820px.
11. Every component has its states: default, hover, focus, disabled, loading (a skeleton or a plain "Reading..." that really goes away), error with the way out, and an empty state that says what to do next.
12. Before saying done, run `python Claude/hooks/ui_lint.py`, fix every line it prints, and look at each page at 390, 820 and 1280px in a real browser tab.

A page that cannot be built from these pieces is a sign a piece is missing: add the piece, do not bend the page.
