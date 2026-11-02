---
name: ui-check
description: How to compare a Brain Games page with the approved design in docs/design.html using Chrome DevTools MCP. Use after any change to a .vue file, a CSS file in app/assets/css, or game JSON copy, when the ui-verifier agent runs, or when the user asks whether a page matches the design, works on mobile, or works in dark mode. Covers viewports, themes, the route-to-design map, and the CLAUDE.md rules 7 to 9 checklist.
---

# UI check against docs/design.html

`docs/design.html` is the approved design. The Nuxt app must match it. Compare the two side by side, state by state.

## 1. Start the servers

1. App: check if `http://localhost:3000` answers (`curl -s -o /dev/null -w '%{http_code}' http://localhost:3000`). If not, start it in the background:
   ```
   export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"; . "$NVM_DIR/nvm.sh"; nvm use --silent; npm run dev
   ```
   Wait until it answers. Note the port it prints if 3000 is taken. Stop it when you are done only if you started it.
2. Design: open `file://<repo>/docs/design.html` directly. If Chrome blocks it, serve it: `python3 -m http.server 4321 -d docs` and use `http://localhost:4321/design.html`.

## 2. Map routes to design views

design.html routes by hash.

| App route        | Design view                                                            |
| ---------------- | ---------------------------------------------------------------------- |
| `/`              | `design.html#`                                                         |
| `/games`         | `design.html#games`                                                    |
| `/games/<id>`    | `design.html#<id>`                                                     |
| `/profile`       | `design.html#profile`                                                  |
| `/anything-else` | no design view; check the friendly 404 copy and "Back to games" button |

## 3. Use your own Chrome tab

All agents share one Chrome.

1. `new_page` for the app and `new_page` for the design. Remember both page ids.
2. Call `select_page` before every action. Another agent may have switched tabs.
3. `close_page` on both tabs when you finish, even after an error.

## 4. Set the same state on both sides

Both read and write localStorage key `bgarden`, so the same state works on both.

- Seed state with `evaluate_script`:
  ```js
  localStorage.setItem(
    'bgarden',
    JSON.stringify({ name: 'Ana', av: '🦉', best: { math: 12 }, hist: [], days: [], xp: 130, theme: 'light' })
  )
  ```
  then reload. Use the same seed on both tabs. Test once with an empty store as well.
- Theme: set `theme` in the seed to `light`, `dark` or `auto`, then reload. For a quick switch without reload, set `document.documentElement.setAttribute('data-theme', 'dark')`, or remove the attribute for auto.
- Auto theme: use `emulate` with `prefers-color-scheme: dark` and then `light`, with `theme: 'auto'`.

## 5. The matrix

For each page, take a screenshot of app and design at:

| Viewport           | Themes                               |
| ------------------ | ------------------------------------ |
| 360×800 (mobile)   | light, dark, auto (with system dark) |
| 1280×800 (desktop) | light, dark, auto (with system dark) |

Use `resize_page` or `emulate` for the viewport. Full-page screenshots for scrolling pages; viewport screenshots for game pages.

For a game page, check three states: ready (with the demo running), playing (after a few moves), and result. Play the same moves on both sides where you can. For a result, a quick way is to finish fast or let the clock run.

## 6. What to compare

Look at the screenshots side by side and list concrete differences:

- Layout: grid columns, tile sizes (`big`, `wide`, `tall`, `normal`), sidebar position, stacking at ≤1000px and ≤640px.
- Copy: headings, labels, buttons, band labels, messages. Copy should come from the game JSON.
- Colour: tokens and category tints. Compare computed values with `get_css_styles` when unsure.
- Type: Baloo 2 for display, numbers and buttons; Lexend for body. Sizes and weights.
- Shape: radius 22px cards, 18px buttons, 14px icons; the pressable shadow on primary buttons.
- Motion: demo frames loop every 2.2s; confetti on a new best; none with reduced motion.

Ignore differences that come from different random values (questions, shuffles, daily picks).

## 7. Rules checklist (CLAUDE.md rules 7 to 9)

Check each item with `evaluate_script` or `get_css_styles`, not by eye alone.

1. **Tokens only.** Tailwind utilities that map to the tokens, or CSS variables. Look for hard-coded colours in the changed components: `grep -nE '#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\(' app/components app/pages`. Only `tokens.css` defines colours.
2. **Both themes work.** No unreadable text, no white boxes in dark mode, no missing tints. Check contrast of body text and buttons.
3. **Touch targets ≥44px** at 360px wide:
   ```js
   ;[...document.querySelectorAll('button, a, input, [role=button]')]
     .map(e => [e, e.getBoundingClientRect()])
     .filter(([, r]) => r.width && (r.width < 44 || r.height < 44))
     .map(([e, r]) => `${e.outerHTML.slice(0, 80)} ${r.width}x${r.height}`)
   ```
4. **Bottom tab bar does not cover content** at 360px: scroll to the bottom; the last element's bottom edge must sit above the tab bar's top edge.
5. **Inputs have font-size ≥16px** (stops iOS zoom):
   ```js
   ;[...document.querySelectorAll('input, textarea, select')].map(e => getComputedStyle(e).fontSize)
   ```
6. **Visible `:focus-visible`.** Press Tab through the page with `press_key`. Every focused control shows a ring. Take a screenshot of at least one.
7. **Keyboard play.** On a game page: Enter starts the game, the game is playable with Enter/Space/typing only, and Enter on the result replays.
8. **Real controls.** Every clickable thing is a `<button>` or `<a>`. Icon-only buttons have `aria-label`. The active nav tab has `aria-current="page"`.
9. **No horizontal scroll** at 360px: `document.documentElement.scrollWidth <= innerWidth`.
10. **Console clean.** `list_console_messages` shows no errors or Vue warnings.

## 8. Report

One block per finding:

```
[HIGH|MEDIUM|LOW] <route> @ <viewport> <theme>: <what is different or broken>
  App: <what the app shows>   Design: <what design.html shows>
  Rule: <CLAUDE.md rule number, if any>   Where: <file:line if you can find it>
  Evidence: <screenshot path or measured value>
```

- HIGH: broken behaviour, a rule 7 to 9 violation, unreadable in a theme, content hidden.
- MEDIUM: clear visual difference from the design (layout, colour, copy, size).
- LOW: small spacing or polish differences.

End with a verdict: `PASS` (no HIGH or MEDIUM) or `FAIL`, and the list of pages and states you checked.
