---
name: daf-game
description: Build today's Daf Yomi game — fetch the daf from Sefaria, study it with its commentaries, design a fresh game mechanic out of the daf's actual content, and ship it as a page at /daf/<slug>. Use when the user says /daf-game, "today's daf game", "build the daf", or names a specific daf to turn into a game.
---

# Daf Game — the daily playbook

Every day of Daf Yomi gets its own small game/app at `/daf/<slug>` on this site.
The game must grow out of what THIS daf actually says — never a generic Talmud quiz.

## 1. Fetch the daf bundle (the harness)

```bash
node scripts/daf-yomi/fetch-daf.mjs             # today's daf from the Sefaria calendar
node scripts/daf-yomi/fetch-daf.mjs "Chullin 71" # or a specific daf
```

This writes `src/data/daf-yomi/<slug>.json` with both amudim (Hebrew + English,
segment by segment), all linked works (Rashi, Tosafot, etc. with counts and refs),
and Sefaria topics. If it fails, the Sefaria API endpoints it uses are:
`GET /api/calendars`, `GET /api/texts/<ref>`, `GET /api/links/<ref>`.

## 2. Actually learn the daf

Read every segment of the bundle (English is fine; check the Hebrew where the game
will quote it). Identify:
- The central sugya/mechanic of the daf — the idea a game could embody.
- The concrete CASES, disputes, lists, chains of reasoning, numbers, and vivid images.
- Machlokot: who holds what, and why.

When a point is unclear or you want commentary color, fetch it directly, e.g.:
`https://www.sefaria.org/api/texts/Rashi%20on%20Chullin%2071a?context=0`
(the bundle's `links` array tells you which commentaries exist and where they anchor).

**Accuracy is a hard requirement.** Every ruling, attribution, and source ref in the
game must match the daf. When a case is disputed, either frame the question as
"according to X" or pick an undisputed case instead. Link every case to its Sefaria ref.

## 3. Check history, then hunt for inspiration

- Read `src/data/daf-yomi/games.json` — the manifest of every past daf game with its
  `mechanic` field. **Do not repeat a mechanic used in the last ~14 games.**
- Explore GitHub for fresh ideas: search for small JS game mechanics, browser toys,
  and interaction patterns (WebSearch/WebFetch, e.g. "javascript <mechanic> game
  site:github.com", or trending repos). Borrow *ideas and interactions*, not code
  with incompatible licenses, and **no new npm dependencies** — pages are
  self-contained vanilla JS + Tailwind.

Mechanic ideas to rotate through (grow the list as you invent more): verdict/judgment
cards, sorting into categories, sequencing a chain of reasoning, matching sage↔opinion,
spot-the-difference between similar cases, resource/simulation toys, map or timeline
play, word games on an Aramaic term, memory pairs, choose-your-own-sugya, physics toys,
hidden-object in a scene the daf describes.

## 4. Build the page

- Create `src/pages/daf/<slug>.astro` using `Layout.astro`, matching the site's dark
  aesthetic but with an identity drawn from the daf's own world (load the
  `frontend-design` skill first; `dataviz` too if the game charts anything).
- Self-contained: inline `<script>` vanilla JS, inline case data, Tailwind classes,
  optional `<style>` block. Mobile-first, keyboard accessible, respects
  `prefers-reduced-motion`.
- Include after the game: a "learn the real daf" section — link to
  `https://www.sefaria.org/<ref>` and surface the top linked commentaries from the
  bundle so the game is a door into the daf, not a replacement.
- Hebrew text: use `dir="rtl"` and a proper Hebrew-capable font
  (Frank Ruhl Libre via Google Fonts works well).
- **Gotcha:** this site's `global.css` forces dark-mode text colors on
  `h1–h6, p, li, span, div` with `.dark <el>` specificity that beats plain Tailwind
  utilities. Write every text-color utility with the important modifier —
  `!text-amber-400`, `hover:!text-...` — including class strings built in JS
  (this is the established parsha-explorer/siddur pattern).

## 5. Register, verify, ship

1. Add an entry to `src/data/daf-yomi/games.json` (newest first):
   `{ slug, ref, heRef, date, title, tagline, emoji, mechanic }` —
   the `/daf` index page renders from this manifest.
2. Verify: run `npx astro dev`, curl `/daf/<slug>` and `/daf/`, fix errors; play the
   game in the browser if browser tools are available.
3. Commit with a message like `Add daf game: <ref> — <title>` (include the
   Co-Authored-By line per repo convention).

## Constraints

- One page per daf, forever reachable at `/daf/<slug>` — the archive grows daily.
- 5–15 minutes of play; delightful, not exhaustive.
- No new dependencies, no external game engines, no API keys.
- Sefaria API is public and unauthenticated — be gentle (the harness batches what's needed).
