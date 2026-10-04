---
name: simple-chinese
description: >-
  Write or polish Traditional Chinese in concise, natural written Chinese (書面語)
  for Hong Kong readers. Covers docs and guides (help pages, README, product
  docs) and UI copy (modals, warnings, confirmations, loading states,
  notifications). Use when the user asks for 書面語, 精簡, 去歐化, 去 AI 化,
  親切, or clearer Chinese. Not for spoken Cantonese.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Chinese

Turn bloated, translated, or AI-sounding Chinese into concise, natural written Chinese that Hong Kong readers can scan quickly.

## Core rule

精簡不等於生硬。Cut filler and translationese. Keep clarity, rhythm, and the facts readers need.

Use standard 書面語 structure. Not brochure hype, not telegram notes, not heavy 文言, and not spoken Cantonese.

## Pick the context

| | Docs and guides | UI copy |
|---|-----------------|---------|
| Where | Help pages, README, product docs, long explanations | Modals, warnings, confirmations, loading states, notifications, setting descriptions |
| Tone | Neutral, plain, informative | 親切: polite, reassuring, respectful |
| Length | Short sentences, one idea each, about 25 characters | Extremely concise, the action or consequence first |
| Address | Impersonal, or 你 when needed | 請…, or 你, never 您 stacked with 之 |

Both stay in written Chinese. UI copy is warmer, not more colloquial.

Not for this skill:
- Tutorials, tips, onboarding, 口語 tone: `simple-cantonese`
- Short buttons and labels (`確定`、`取消`): keep minimal
- Legal, privacy, and technical disclaimers: keep precise, do not polish

## Three failure modes

| Too AI / 歐化 / stiff | Too colloquial or too clipped | Right balance |
|-----------------------|-------------------------------|---------------|
| 在當前複雜多變的環境下，企業必須對其策略進行檢討 | 環境多變，檢討策略。 | 環境多變，企業應檢討策略。 |
| 值得注意的是，此功能至關重要，在使用之前必須進行設定 | 呢個功能好重要，用之前記得設定 | 此功能很重要，使用前請先完成設定。 |
| 請選擇您欲匯出之檔案格式以進行下載之操作。 | 揀個格式下載啦。 | 請選擇要匯出的檔案格式。 |
| 若您執行登出操作，則未儲存之變更將不予保留。 | 你登出咗就冇晒未儲存嘅嘢㗎。 | 確定要登出？未儲存的變更將會遺失。 |

## What to cut

Europeanized habits:
- `的` overload: 參差的斑駁的 → 參差而斑駁
- Weak verb + abstract noun: 作出貢獻、進行討論、進行支付 → 貢獻、討論、支付
- Bloated nouns: 支付之操作、付款之行為 → 支付、付款
- Passive when active is clearer: 被通過、不被允許 → 獲通過、無法使用
- Long pre-modifiers: move the detail to a second short clause
- Stacked connectors: 由於…因此、關於…我們認為、存在著
- Redundant words: 成功地完成 → 完成

AI and brochure habits:
- `不是 A 而是 B` templates
- 深入探討、至關重要、值得注意的是、顯而易見、關鍵在於
- 充滿挑戰、令人興奮、完美體驗、積極影響
- Empty adjectives: 全新體驗、全方位、一站式
- 以及 between every list item when commas suffice

Over-formal habits:
- 務必、方可、須知, unless a warning tone is needed
- Legal padding and double negatives in casual copy

Too colloquial (wrong skill):
- Particles like 嘅、㗎、咗、嚟、唔使驚. In UI copy use 的、了、不用、選擇 instead of 嘅、咗、唔使、揀
- Slang, unless the product already uses it

## What to keep

- Exact numbers, timings, values, exceptions, and consequences (`50MB`、`3 次`、`30 天`)
- Exact labels users see elsewhere (**設定**、**通知**、**訂閱**)
- Active voice and parallel structure in lists
- Cross-references that help navigation

Use `8 - 10` for numeric ranges.

## Workflow

1. Scope: only the section or strings the user named. Do not rewrite whole projects unless asked.
2. Pick the context, docs or UI.
3. Read nearby copy and reuse the terms already in use.
4. Diagnose: `的` pile-ups, weak verbs, AI patterns, passive, fluff, or too slangy.
5. Rewrite: same meaning, fewer words, clearer order.
6. Run a light `simple-text-cleanup` pass. Do not over-apply: keep good sentences, do not split clear short lines, do not make UI copy sound like a command, do not remove `→` in step flows. Meaning and voice first, punctuation second.
7. Verify: facts intact, variables (`{name}`, `{time}`), HTML tags, and links unbroken.

## Before / after

Docs:

```text
Before: 在使用本功能之前，用戶必須要對帳戶資料進行確認，以確保能夠順利完成驗證。
After:  使用前請先確認帳戶資料，以便順利完成驗證。

Before: 值得注意的是，若用戶在檔案超過 50MB 的情況下進行上傳，則系統將拒絕該次上傳，且該次嘗試不計入每日上傳次數。
After:  檔案超過 50MB 將無法上傳。該次嘗試不計入每日上傳次數。

Before: 此功能不是為了限制用戶，而是為了讓用戶能夠享有更安全的使用體驗。
After:  此功能用於保障帳戶安全。
```

UI:

```text
Before: 系統已偵測到您的裝置處於離線狀態，故無法進行同步之操作。
After:  目前沒有網絡連線，恢復後會自動同步。

Before: 您確定要執行刪除操作嗎？此操作將無法被還原。
After:  確定要刪除嗎？刪除後無法還原。

Before: 你要唔要啟用通知㗎？開咗就唔會錯過訊息喇。
After:  要開啟通知嗎？開啟後不會錯過新訊息。
```

## Output

Apply the rewrite in the file. Optionally note 2 or 3 main changes, such as 刪去「進行」、拆短句、去除「不是…而是…」. No long diagnostic essay unless asked.

## Checklist

- Scope and context (docs or UI) match the request
- Concise, scannable, standard written Chinese
- No AI, brochure, or heavy 歐化 patterns
- Not too colloquial, not a telegram note
- Numbers, labels, and exceptions preserved
- Variables and links intact
