---
name: simple-cantonese
description: >-
  Write or polish Traditional Chinese copy in natural Hong Kong spoken Cantonese,
  verbal, warm, and local. Use when the user asks for colloquial, 口語, 廣東話,
  地道, natural, or conversational tone, or when editing tutorials, onboarding,
  tips, about copy, or user-facing help. Also use to de-AI copy without making
  it stiff or over-concise.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Cantonese

Make copy sound like someone talking beside the reader. Not a brochure, not a telegram, not ChatGPT.

## Core rule

口語不等於短。Natural Cantonese can be a full sentence or two. The goal is spoken flow, not word count.

Cut marketing filler and 書面語. Keep verbal rhythm, warmth, and local phrasing. De-AI means removing hype and translationese, not stripping particles, reassurance, or spoken connectors.

## When to use

| Use this voice | Keep standard Chinese |
|----------------|-----------------------|
| Tutorials and first-run help | Buttons, errors, form labels |
| Short tips and onboarding | Legal, privacy, admin |
| Friendly about and welcome copy | Long reference docs |
| Encouraging explanations | Setting names and toggles |

Only apply where the user or section clearly wants a spoken tone. Do not rewrite whole apps unless asked.

## Voice

- Register: Hong Kong spoken Cantonese in Traditional Chinese
- Mood: friendly, clear, lightly reassuring, like explaining to a friend
- Length: as long as needed to sound natural, 1 or 2 flowing sentences per idea
- Reader: someone skimming on a phone

Write how you would say it out loud. If it sounds like a product page or a bullet list, loosen it.

## Three failure modes

| Too AI | Too stiff (over-cut) | Right balance |
|--------|----------------------|---------------|
| 充滿創意嘅智能筆記體驗 | 筆記同步。支援多裝置。 | 你寫低嘅筆記會自動同步，手機、電腦都睇到。 |
| 我哋為您提供便捷嘅密碼重設服務 | 密碼忘記，按此重設。 | 唔記得密碼？唔使驚，撳一下就可以重設。 |
| 隨時隨地輕鬆管理待辦事項 | 逾期任務標紅。 | 過咗期嘅任務會變紅色，一眼就睇到，唔怕漏咗。 |

## Sound local, not AI

Cut (brochure and AI):
- Stacked adjectives: 節奏明快、充滿活力、各式各樣
- Empty hype: 精彩體驗、盡情、輕鬆上手、隨時隨地、非常方便
- Mission-statement tone: 我哋嘅目標係想提供一個完全…
- Fake enthusiasm: 一起探索、絕對, unless the product already uses it
- Translationese: 透過…、針對…重新設計、提供…體驗
- Mandarin wording: 點擊 (use 撳 or 按)、這樣 (use 咁樣)、咱們、哦、啥

Keep (spoken and local):
- Time markers: 打開嗰陣、儲存嗰陣、完成之後
- Soft connectors: 但係、不過、如果要…就…
- Light reassurance when it fits: 放心、唔使驚、好平常
- Natural particles: 嘅、嗰、咗、嚟、㗎、啫、就得
- Question hooks: `唔識用？`、`搵唔到？唔使驚`
- Concrete verbs: 加入、開返、睇返、儲起、搞掂、匯出、退返

Avoid:
- Written words in casual sections: 若…則…、須、方可、查閱、進行
- Telegram style, dropping subjects and connectors to save words
- Three exclamation marks on one screen
- Slang pile-ups or rude slang

## Terminology

Reuse exact labels from the project's existing copy, and bold UI terms users see on screen, such as **設定**、**教學**、**使用說明**.

- Match nearby product terms, do not invent looser translations
- Do not paraphrase fixed feature names
- Keep amounts, limits, and consequences, do not soften rules to sound friendly

## Structure

Headings: short, spoken, sometimes a question, such as `第一步：新增你嘅第一個項目`、`唔記得密碼？唔使驚`、`隨時開返出嚟睇`.

Body:
1. Lead with what the user does or should know, in full spoken sentences
2. Add one caveat if needed (`但要留意…`)
3. Add reassurance when users commonly worry (`放心…`)

Use `**bold**` for actions, numbers, and UI labels, and `→` for step flows.

## Workflow

1. Read nearby copy for tone and fixed terms.
2. Keep the facts: numbers, limits, consequences.
3. Replace 書面語 with spoken phrasing. Expand if the draft is too clipped.
4. Cut brochure hype, not conversational glue.
5. Read aloud. If it sounds like notes or a slogan, add a connector or particle.
6. Run a light `simple-text-cleanup` pass: remove `；` and connector dashes, fix ranges as `8 - 10`, fold interrupting brackets into the sentence. Do not strip particles or reassurance, do not collapse connectors into notes, do not remove `→` in step flows, do not flatten natural `！`. Spoken flow first, punctuation second.
7. Bold UI labels and key numbers. Run the project build or lint if source files changed.

## Examples

```text
打開之後：**先登入** → **新增項目** → **設定提醒**。每一步都會自動儲存，唔使再撳儲存掣。

你可以喺**設定**入面撳**通知**，開關提醒。但要留意，如果關咗提醒，到期嘅任務就唔會再通知你㗎。

搵唔到個任務？唔使驚，**資料仲喺度㗎**！你隨時可以喺**封存**入面搵返出嚟。

未熟手？撳右上角個選單，隨時可以重睇呢個教學，或者睇下**快速鍵**同**使用說明**。
```

Before / after:

```text
Before (書面語): 若停用提醒，到期任務將不再發出通知。
Too stiff:       停提醒，任務不通知。
After:           如果關咗提醒，到期嘅任務就唔會再通知你。

Before (AI):     我哋嘅目標係想提供一個完全免費、免註冊、功能完整、而且介面簡潔嘅任務管理體驗，等大家隨時隨地都可以高效管理工作！
Too stiff:       免費免註冊。功能齊全。開啟即用。
After:           免費、唔使註冊，功能樣樣齊，一打開就用得。

Before (書面語): 若匯入失敗導致資料不完整，系統將自動還原至上一個版本。
Too stiff:       匯入失敗，還原上版本。
After:           如果匯入失敗，搞到資料唔齊，系統會自動退返去上一個版本。
```

## Quality bar

Each line should sound like natural speech to a Hong Kong reader, not marketing and not a memo.

```text
Good:
新增項目、設定提醒，**每日完成 3 件事**就好！
你可以喺**設定**入面撳**通知**，開關提醒。

Too stiff:
於設定內點擊通知以切換提醒。
未儲存變更須先保存。

Too AI:
充滿效率嘅智能管理體驗，隨時隨地輕鬆上手！
我哋致力為您提供優質服務體驗。
```

## Checklist

- Scope matches the request
- Sounds spoken and local, not clipped or formal
- Brochure clichés removed, verbal warmth kept
- UI labels match existing copy
- Numbers, limits, and exceptions preserved
- No broken placeholders, links, or string syntax
