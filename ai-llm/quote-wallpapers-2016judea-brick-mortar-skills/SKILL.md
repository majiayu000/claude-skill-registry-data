---
name: quote-wallpapers
description: Turn a list of saved book quotes into a rotating set of iPhone lock-screen wallpapers — bold AI-generated backgrounds with brutalist type — ready for iOS Photo Shuffle. Use when you want to make or refresh quote wallpapers, add quotes to the lock-screen rotation, or restyle the cards. Input is a JSON list of {quote, author, book}; uses the make-art engine (Gemini) for backgrounds and Pillow for composition.
---

# quote-wallpapers — literary quote lock screens

Turns saved book quotes into a shuffle of iPhone lock-screen cards: **bold AI art background +
brutalist type**, delivered as a folder of PNGs (or a Photos album) that iOS **Photo Shuffle**
rotates through.

## Aesthetic that works

Serif/Didot themes read as boring on a lock screen. The keeper is **brutalist**: left-aligned
Futura, a single orange accent rule, tracked small-caps author + book, lots of negative
space — over **bold high-contrast art**: saturated colour-fields with a hard black wedge
(vermilion/oxblood work best), eclipses/celestial, stark B&W, surreal double-exposures. Not
muted film-horizon gradients.

## Pipeline

1. **Export quotes** to a JSON list `[{"quote","author","book"}]` (from Notion, Kindle highlights,
   Goodreads, a spreadsheet).
2. `python3 scripts/build_render_set.py quotes.json render_set.json` — drops quotes containing any
   word in `scripts/blocklist.txt` (create it: one word per line; slurs and explicit terms you don't
   want on a phone — they stay in your source list) and excerpts long passages (>~210 chars) to a
   punchy core.
3. `python3 scripts/gen_backgrounds.py <bg_dir>` — generates ~35 bold backgrounds via the
   **make-art** engine (needs `GEMINI_API_KEY` and network; set `MAKE_ART_GEN` if `gen_art.py`
   isn't at `~/.claude/skills/make-art/scripts/`). ~2K images, ~$4, ~20 min. Weighted to colour-fields.
4. `python3 scripts/compose_cards.py render_set.json <bg_dir> <cards_dir>` — composes cards at
   **1290x2796** (6.1-6.9" iPhones, 19.5:9), one per quote, named `lit_###.png`. Rotates
   backgrounds; text in the lower ~55% so the clock zone stays clear. Fonts come from macOS
   `/System/Library/Fonts/Supplemental/` (Futura etc.); swap paths on other systems.
5. **Delivery.** Default: hand over `<cards_dir>` (AirDrop / Files). Photo Shuffle needs a Photos
   album, so if asked: `scripts/import_to_photos.sh <cards_dir> "Literary Quotes"` — that puts generated art in the photo library, so do it only on request.
6. **On iPhone:** Settings -> Wallpaper -> Add New Wallpaper -> **Photo Shuffle** -> the album ->
   frequency.

## Gotchas

- **Cream border:** Gemini sometimes renders a light "paper frame" (esp. colour-field prompts).
  `compose_cards._trim_border()` detects and crops it before the full-bleed cover, and `cover()`
  adds a small overscan. Don't ask for a "paper border" in prompts. White edges still showing =
  loosen the trim threshold.
- **Photos AppleScript can import and make/delete albums, but CANNOT delete library media items**
  (-1700 / -10000). To clean up junk imports, gather them into a throwaway album and delete by hand
  (open album -> Cmd-A -> Delete). Name cards distinctively (`lit_###`) so stray imports stay
  separable.
- Guard `None` author/book in the compositor (some quotes are unattributed).
- **A reused pool (~35 backgrounds)** rotated across all quotes looks varied enough in a shuffle;
  unique-per-quote costs ~15x more for no visible gain.
- `compose_cards.py` keeps three text styles (`style_A` serif, `style_C` Didot, `style_B`
  brutalist); `STYLES=[style_B]` selects brutalist only.

See also `make-art` (the image engine) and `apple-photos`.
