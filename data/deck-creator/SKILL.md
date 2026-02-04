---
name: deck-creator
description: Create, update, and translate Dify X Reveal.js slide decks in this repo. Use when asked to draft slides, extract outlines, or maintain bilingual CN/EN parity for the ctrip/paypal/pupu/milvus/aispeech/dentsply/oceanbase/legalai decks, including deck HTML (index.html/index_en.html) and legal workflow YAMLs.
---

# Deck Creator

## Overview

Use existing decks as the source of truth to create outlines, edits, or translations. Keep CN and EN versions aligned while preserving deck-specific structure and styling.

## Workflow

1. Identify the topic and target audience based on the user's request.
2. Identify the theme of the deck based on the user's request.
2. Use reveal.js to create a new deck.
3. Use the following structure:
   - 01. Title
   - 02. Introduction
   - 03. Content
   - 04. Conclusion
   - 05. Q&A
   - 06. References
   - 07. Contact
4. Enrich the deck with the topic and content from the user's request.
    - For the content, use vertical stack to present the content.
    - For the content, use $infographic-creator to create infographics when needed to visualize data or concepts.
5. Add support for speaker notes, and add speaker notes for each slide.
6. Add xiaohongshu and bilibili qr code to the contact slide.


## Output Expectations

- Deliver CN and EN versions as separate outputs when generating new content.
- Keep slide order, numbering, and vertical stack structure aligned across languages.
- Call out any ambiguous translations or terminology conflicts.


## Brand & Assets

- Brand: use Dify Blue `#0033ff`; logo in `assets/logo.svg`.
- Fonts: prefer Söhne / Söhne Mono; fallbacks Inter, JetBrains Mono, Mi Sans / Noto Sans SC / Noto Sans Mono SC.
- Assets: `assets/` contains `logo.svg`, `bilibili.png`, `xiaohongshu.png` for brand and contact slides.

## References


