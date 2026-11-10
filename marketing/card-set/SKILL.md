---
name: card-set
zh_name: "卡牌套组"
en_name: "Card Set"
emoji: "🃏"
description: "A set of game cards from one card list and the designer's own frame and art: one front design filled per card, a back, a proof sheet of every card, and print-ready files at the print house's exact size, with text kept clear of the cut and the rounded corners."
zh_description: "用一份卡牌清单和设计师自己的牌框与插画, 做出整套游戏卡: 一张按卡填充的正面设计、一张背面、一张全卡校样, 以及符合印厂尺寸的印刷文件, 文字避开裁切线和圆角"
en_description: "A set of game cards from one card list and the designer's own frame and art: one front design filled per card, a back, a proof sheet of every card, and print-ready files at the print house's exact size, with text kept clear of the cut and the rounded corners."
category: card
scenario: marketing
aspect_hint: "63.5×88.9 mm trading card, bleed included"
tags: ["cards", "trading cards", "game cards", "tcg", "board game", "card game", "tarot", "proxy", "print and play", "卡牌", "桌游"]
triggers:
  - "trading card"
  - "game cards"
  - "card game"
  - "card set"
  - "board game cards"
  - "tarot cards"
  - "print house"
  - "卡牌"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - color
      - anti-ai-slop
  surface: web
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "I design cards for a board game and print them at Board Games Maker. Here's my card list and the art folder. Make the fronts from my frame, one back, and a proof sheet so I can check every card before I order."
---

# Card Set

**Intent.** A card designer has a game, a card list and their art. They want every card in one frame, files their print house accepts, and a way to catch a typo before paying for a print run. The front is **one design with fields**, exported once per card from their list.

## 1. Start from what they have

Ask once, in plain words:

- **The card size and the printer.** Poker-size game cards are `trading-card` (2.5×3.5 in); tarot is `tarot-card`; small cards are `mini-card`. Ask which print house they use and call `list_open_design_print_houses`: if it's listed, export with its id; if not, export at 300 dpi and tell them to check the size against the printer's upload page.
- **Their frame and style.** A frame image, a brand document or a few cards they've made. If they give a document or site, make their style first (`read_open_design_source`, then `extract_open_design_design_system`).
- **The card list.** A CSV or spreadsheet, one row per card: name, cost, type, rules text, art, number. Without one, offer to write `cards.csv` with them.
- **Their art.** A folder of card art. This recipe lays out **their own frame and art; it never generates card art**, and it never uses frames, logos, mana symbols or icons from published games. Say once that they're responsible for what they print and sell.

## 2. Map the columns, once

Propose which column fills which field (`name`, `cost`, `type`, `rules`, `art`, `flavor`, `number`…) and show the mapping in one short list before designing. Never bind a column for cost price, supplier or internal notes (a game's own "cost" stat is fine; ask if unsure). Ask about any column you can't place. Art columns hold workspace-relative paths; with no art yet, mark the art window and ask for the files.

## 3. The front

Pass the card format to `prepare_open_design_brief` and `register_open_design_artifact`. The front is one `[data-od-card]` at the bleed box:

- **Bleed and safe area.** Art and frame colour run into the bleed. Name, cost, rules and set number stay inside the safe area.
- **Corners.** The printer cuts the corners round. Keep the card itself square (never `border-radius`), and keep cost and other corner details clear of the curve; the check warns with `corner-clearance`.
- **Rules text.** Give the rules box a fixed size and mark the text `data-od-fit` so long rules shrink a little to fit, never below the format's minimum type size. A card that still doesn't fit is reported by name: suggest shorter wording rather than smaller type.
- **Hierarchy.** Name and cost first, art second, type line, rules, then flavour and number. Few sizes: it's read in the hand.

## 4. The back

Add the back in the same file, after the front: `<div data-od-card data-od-side="back">`, the same size. A back with no fields is the same on every card and is written once, unless the printer wants one back per card. Numbered or per-card backs use fields like the front.

## 5. The proof sheet

Make a second artifact: a contact sheet showing every card small, in a grid, from the same list (one cell per row, the same fields), so they can spot a wrong cost or a typo in one look before ordering. It's a screen piece; export it as one PNG.

## 6. Check and export

- Check with `export_open_design_artifact`, `checkOnly: true`, `data` set to the list and `nameField` to the name column. Every card is checked and named; fix errors, and tell them which cards still overflow.
- Export with the same `data` and `nameField`, plus `printHouse` when their printer is listed (or `format: "png"` for 300 dpi images). The faces come out as `<name>-front` and `<name>-back`. For a printer that wants a PDF, export the print PDF: each back follows its front.
- Offer mockups for their shop or socials: an HTML/CSS sleeve, a hand or a fan of cards holding the exported fronts. No generated photos.
