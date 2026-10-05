---
name: imessage-nine-grid-hypercard
description: Create narrow iMessage/PTT Border-Light HyperCard style nine-grid cards in Chinese or mixed Chinese-English. Use when the user says "iMessage 九宮 HyperCard", "iMessage 九宮", "做成 iMessage 九宮", "用 iMessage 九宮 HyperCard 整理", asks for a phone-readable short card with Context below, or wants Mandala/九宮/HyperCard content formatted for blue-bubble/iMessage sharing with long links, paths, and rules moved out of the card.
---

# iMessage 九宮 HyperCard

## Overview

Turn notes, plans, links, system status, or Mandala-style content into an iMessage-ready short card. Keep the phone card narrow and readable; put long data in a separate Context block after the card.

## Output Workflow

1. Extract the central topic and up to eight surrounding nodes.
2. Write a short header/status section for the iMessage card.
3. Write a compact "phone-readable" summary section.
4. Write the nine-grid section in three row groups separated only by blank lines.
5. Move long URLs, file paths, detailed rules, full explanations, and overflow data into `Context` after the card.

When responding in chat, put the card in a plaintext fenced block so spacing survives. When sending through an actual messaging tool, send raw text without the fence.

## Hard Rules

- Use this exact 18-stroke horizontal border unit: `──────────────────`.
- Use only these frame lines:
  - `╭──────────────────╮`
  - `├──────────────────┤`
  - `╰──────────────────╯`
- Do not use left or right vertical borders on content lines.
- Indent every content line with two spaces.
- Use frame dividers only between the main short-card sections.
- Inside the nine-grid section, separate the three row groups with blank lines only.
- Never insert a bare `──────────────────` line inside the card.
- Keep each card line phone-readable. If a line becomes long, shorten it or move details to Context.
- Use `◎` for the center when a Mandala center is needed.
- Use circled numerals `①` to `⑧` for surrounding nodes when helpful.
- Output the finished card first. Put `Context` after it only when there is extra data.

## Card Template

Use this structure as the default shape, adapting labels and details to the user's content:

```text
╭──────────────────╮
  HERMÈS／iMessage
  永錫.OS ONLINE
  {status}
  {action}
├──────────────────┤
  {short title}
  ＋{short subtitle}

  手機版：短卡在上
  長資料：下放Context

  [[①{node}]] 代表
  Context有完整資料
├──────────────────┤
  ①{A} ②{B} ③{C}
  {A note} {B note} {C note}

  ④{D}   ◎   ⑤{E}
  {D note} {center note} {E note}

  ⑥{F} ⑦{G} ⑧{H}
  {F note} {G note} {H note}
╰──────────────────╯
```

## Context Block

Use Context for data that would make the card heavy:

```text
Context
① {A}: {full detail, path, link, or rule}
② {B}: {full detail}
③ {C}: {full detail}
④ {D}: {full detail}
⑤ {E}: {full detail}
⑥ {F}: {full detail}
⑦ {G}: {full detail}
⑧ {H}: {full detail}
```

Skip empty Context entries. If all information fits cleanly in the card and the user did not request Context, omit the Context block.

## Style

Prefer warm, concise Chinese. Mixed Chinese-English labels are fine when they match the source material, such as `TARS`, `Codex`, `Hermes`, `Context`, `Apple`, or `iMessage`. Keep the card practical and copyable rather than decorative.
