---
name: imandalart
description: "Create iMandalArt 2.2 pure-text 3x3 Mandala index cards with a five-character center axis, eight orthogonal surrounding angles labeled Ⓐ-Ⓗ, compact title cells such as Ⓐ健康復節, hard-line CJK layout, optional の字型 ordering, and 井字號 compass ordering. Use when the user asks for iMandalArt, iMandalart, I MandalArt, の字型, ◊字型, 井字號, 中國城市方位, 64＋8＋1, 手機方形曼陀羅, 正方形九宮索引卡, 五字定格, ◎中心, Ⓐ-Ⓗ 九宮卡, TheBrain/Cerebro preview-safe hard-line cards, or a square 3x3 card that is not a Markdown table, visible-border PE2 card, or 81-cell Mandala."
---

# iMandalArt 2.2

## Purpose

Use this skill to turn any source material into one iMandalArt 2.2 pure-text 3x3 card.

iMandalArt 2.2 is:

- One center idea.
- Eight orthogonal surrounding angles.
- A pure-text 3x3 card with hard line breaks.
- Three lines per cell: a short title row and two content rows.
- A center axis that displays `◎◎◎◎◎`, one five-Han-character center line, then `◎◎◎◎◎` again.
- A note-friendly thinking object for TheBrain, Hermes, Discord, Codex, other LLM chat surfaces, or clipboard use.

iMandalArt 2.2 is not:

- A Markdown table.
- A visible-border PE2 card.
- An HTML-only visual artifact.
- An 81-cell Mandala.
- A long explanatory essay.

## Default Deliverable

Default to an iMandalArt 2.2 pure-text hard-line card.

1. Read the source material first. If the user provides a file path, JSON, note, article, or pasted text, inspect the content before generating.
2. Identify the central thought and compress it into one five-Han-character center line.
3. Orthogonally decompose the material into eight surrounding angles. Avoid synonym-only repeats.
4. Give each surrounding angle a four-Han-character title directly prefixed by `Ⓐ` through `Ⓗ`.
5. Write two modern, plain-language five-Han-character lines for each surrounding cell.
6. Render the center as `◎◎◎◎◎`, one five-Han-character center line, then `◎◎◎◎◎`.
7. Render the final answer as the 11-line 3x3 card only.

For LLM chat surfaces such as ChatGPT, Claude, Gemini, Codex, or Discord, wrap the card in a fenced `text` code block so hard line breaks and full-width spaces survive rendering.

For TheBrain/Cerebro direct note insertion or clipboard-only workflows, emit the raw 11-line card without a Markdown fence.

## Three Kings 2.2 Integration

iMandalArt is the **compression king** in the three-skill publishing chain:

`source material -> iMandalArt 2.2 eight angles -> BIRD 2.2 addresses and Routes -> A4 Booklet 2.2`

- Compress one source into one center and eight orthogonal retrieval angles.
- Preserve の字型 identities so BIRD indexes and booklet Routes can reuse the same positions.
- Pass the full 11-line card, center identity, source references, and ordering mode to downstream skills.

## 2.2 Card Contract

The final card has exactly 11 physical text lines:

```text
Ⓐ四字標題　Ⓑ四字標題　Ⓒ四字標題
五字內容一　五字內容一　五字內容一
五字內容二　五字內容二　五字內容二

Ⓓ四字標題　◎◎◎◎◎　Ⓔ四字標題
五字內容一　中心五字句　五字內容一
五字內容二　◎◎◎◎◎　五字內容二

Ⓕ四字標題　Ⓖ四字標題　Ⓗ四字標題
五字內容一　五字內容一　五字內容一
五字內容二　五字內容二　五字內容二
```

Line rules:

- Line 1, 5, and 9 are title lines.
- Lines 2, 3, 10, and 11 contain three five-Han-character surrounding phrases.
- Line 6 contains left and right five-Han-character surrounding phrases plus one five-Han-character center phrase.
- Line 7 contains left and right five-Han-character surrounding phrases plus the center marker `◎◎◎◎◎`.
- Line 4 and line 8 are completely blank.
- Use one full-width space `　` between columns.
- The first visible character of the card is `Ⓐ`.
- The center title cell on line 5 is exactly `◎◎◎◎◎`.
- The center cell on line 7 is also exactly `◎◎◎◎◎` unless the user explicitly asks for a second center sentence.
- Do not add explanations above or below the card unless the user explicitly asks.

## Cell Rules

Surrounding title rows:

- Use the labels `Ⓐ`, `Ⓑ`, `Ⓒ`, `Ⓓ`, `Ⓔ`, `Ⓕ`, `Ⓖ`, `Ⓗ` in that order.
- Do not put a space after the label.
- Use exactly four Han characters after the label when possible, e.g. `Ⓐ輸入來源`.
- Titles should work like index labels, not sentences.
- Titles may preserve a functional role, but must be rewritten to fit the material.

Content rows:

- Every surrounding content phrase must be exactly five Han characters.
- The center line on line 6 must be exactly five Han characters.
- The center line on line 7 should be `◎◎◎◎◎` by default.
- Do not use English, digits, punctuation, emoji, or spaces in surrounding content phrases or the line 6 center phrase.
- Rewrite terms such as AI, Agent, FIRE, Hermes, JSON, API, and app names into compact Chinese when possible.
- Write in modern plain language. Avoid over-classical phrasing.
- If source material is thin, infer responsibly from the surrounding meaning.

Center cell:

- Use `◎◎◎◎◎` only as the displayed center title.
- Internally choose a specific center title of about five Han characters to guide the card.
- The line 6 center content must summarize and integrate the eight surrounding angles.
- The line 7 center marker creates a visual axis and should remain `◎◎◎◎◎` in 2.2 default output.
- The center should not repeat a surrounding title.

## Orthogonal Eight-Angle Map

Use this order unless the user gives a different map:

- `Ⓐ` source / trigger: Where does this begin?
- `Ⓑ` input / material: What is being read or transformed?
- `Ⓒ` recognition / method: How is the pattern identified?
- `Ⓓ` output / expression: What form does it become?
- `Ⓔ` process / thread: What sequence makes it work?
- `Ⓕ` storage / place: Where is it saved or remembered?
- `Ⓖ` constraint / avoid: What must be avoided?
- `Ⓗ` next action: What is the next concrete move?

## の字型 Ordering

Use this layout when the user asks for `の字型`, `◊字型`, a 64＋8＋1 index, or explicitly supplies the same spatial order. `の字型` is the name of the ordering pattern; `◎` remains the visible center marker.

For a directory or route card, place the lettered cells exactly as follows:

```text
Ⓕ　Ⓒ　Ⓖ
Ⓑ　◎　Ⓓ
Ⓔ　Ⓐ　Ⓗ
```

For the eight keywords inside any child nine-grid, place the numbered cells exactly as follows:

```text
⑥　③　⑦
②　◎　④
⑤　①　⑧
```

Apply these rules:

- Preserve semantic identity: `Ⓐ` or `①` remains the first assigned directory or keyword even though it is displayed at bottom center.
- Treat `Ⓘ` as the ninth, center-level directory identity in a 64＋8＋1 system, but display the center cell as `◎`, not `Ⓘ`.
- Use the same spatial mapping recursively: the total directory uses letters, and each child grid uses numbers.
- Override the default first-character rule in this mode: the first visible label is `Ⓕ` for a directory card or `⑥` for a numbered child grid, not `Ⓐ`.
- Put citations, source marks, or cross-route notes after the card or inside the relevant cell only when the user asks; do not disturb the spatial order.
- Do not silently convert this layout into reading order such as `ⒶⒷⒸ / Ⓓ center Ⓔ / ⒻⒼⒽ` or `①②③ / ④ center ⑤ / ⑥⑦⑧`.
- Keep the 11-line hard-line contract: the physical top, middle, and bottom rows follow the の字型 positions while content-line lengths and blank lines remain governed by the 2.2 rules.

## 井字號 Ordering

Use this layout when the user asks for `井字號`, a Chinese-city compass arrangement, or explicitly describes `Ⓒ在上、Ⓑ在左、Ⓐ在下、Ⓓ在右`.

Treat the center as the city center and place the four main gates on the cardinal axes:

```text
Ⓕ　Ⓒ　Ⓖ
Ⓑ　◎　Ⓓ
Ⓔ　Ⓐ　Ⓗ
```

Apply these fixed directions:

- `Ⓒ` is north / top.
- `Ⓑ` is west / left.
- `Ⓐ` is south / bottom.
- `Ⓓ` is east / right.
- `Ⓕ`, `Ⓖ`, `Ⓔ`, and `Ⓗ` occupy northwest, northeast, southwest, and southeast respectively.
- Preserve each letter's semantic identity when moving it into this layout.
- Override the default first-character rule: the first visible label is `Ⓕ`, not `Ⓐ`.
- Keep the 11-line hard-line contract and all five-Han-character content rules.
- Do not reinterpret `Ⓐ` as north/top. In 井字號 mode, `Ⓒ在上` is the defining rule.

Example title rows for a の字型 card:

```text
Ⓕ四字標題　Ⓒ四字標題　Ⓖ四字標題
五字內容一　五字內容一　五字內容一
五字內容二　五字內容二　五字內容二

Ⓑ四字標題　◎◎◎◎◎　Ⓓ四字標題
五字內容一　中心五字句　五字內容一
五字內容二　◎◎◎◎◎　五字內容二

Ⓔ四字標題　Ⓐ四字標題　Ⓗ四字標題
五字內容一　五字內容一　五字內容一
五字內容二　五字內容二　五字內容二
```

## Weekly Plan Layout

When the source is a weekly plan (`週計劃`, `週計画`, `Weekly Plan`, `2026Wxx`, or an eight-domain week card) and the user does not request the default orthogonal map, use this fixed weekly eight-domain layout:

```text
Ⓕ內在　Ⓒ財流　Ⓖ學習
...
...

Ⓑ工作　◎◎◎◎◎　Ⓓ家庭
...　中心五字句　...
...　◎◎◎◎◎　...

Ⓔ社群　Ⓐ健康　Ⓗ休閒
...
...
```

Weekly labels map to the user's recurring life domains:

- `Ⓐ` health / body / exercise: 健康第一.
- `Ⓑ` work / writing / book: 書稿推進.
- `Ⓒ` finance / money / subscriptions: 財流降噪.
- `Ⓓ` family / partner / children: 家人互動.
- `Ⓔ` community / people / relationships: 人脈路徑.
- `Ⓕ` inner life / letting go / teacher stance: 去我內在.
- `Ⓖ` learning / Japanese / indexing: 日文沉澱.
- `Ⓗ` leisure / music / joy / recovery: 開心休閒.

This weekly layout overrides the default title-label order in the 2.2 card contract and validation gate. All other constraints still apply: 11 physical lines, blank lines 4 and 8, one full-width separator between columns, compact titles, five-Han-character content phrases when possible, and the center marker on lines 5 and 7.

For non-process topics, keep the spatial order but rename the titles semantically. The eight angles must still be different kinds of attention, not eight synonyms.

Orthogonality test:

1. Restate the eight roles internally in one short list.
2. Check whether any two cells answer the same question.
3. If two cells overlap, split them by function, time, object, risk, or action.
4. Only output the card after the eight cells are distinct.

## CJK And Hard-Line Rules

Hard line breaks are part of the artifact.

- Do not rely on automatic wrapping to create rows.
- Use actual newline characters between the 11 physical lines.
- Keep each title compact so TheBrain and chat previews are less likely to wrap.
- Use full-width column separators, not tabs.
- Avoid ambiguous layout based on repeated half-width spaces.
- If a preview collapses whitespace, the clipboard text can still be correct; prefer code blocks in chat and raw hard-line text in TheBrain insertion.

## Forbidden Output

Do not output:

- Markdown tables.
- Vertical rails such as `|`.
- ASCII borders such as `+----------+`.
- Box drawing.
- HTML as the primary answer.
- Numbered explanations before the card.
- The internal orthogonality checklist.
- Multiple alternate cards unless asked.

## Example

```text
Ⓐ健康復節　Ⓑ書稿收束　Ⓒ財流降噪
羽球慢回身　書章拉中心　訂閱先盤點
跑走養節奏　青蛙先寫書　現流養書路

Ⓓ家人點火　◎◎◎◎◎　Ⓔ人脈成路
問夢不說教　二九週計劃　約談留三卡
陪走百年路　◎◎◎◎◎　好友接技能

Ⓕ內在放下　Ⓖ日文沉澱　Ⓗ休閒充電
少說更點火　句子先編號　合唱鬆心身
不急證明我　接詞成路徑　吉他聽太陽
```

## Validation Gate

Before returning a 2.2 card, check:

- There are exactly nine cells.
- The output has exactly 11 physical lines.
- Lines 4 and 8 are blank.
- Title rows use `Ⓐ` through `Ⓗ` and center `◎◎◎◎◎`.
- Weekly plan mode may use the fixed row order `ⒻⒸⒼ / Ⓑ center Ⓓ / ⒺⒶⒽ`.
- の字型 mode must use `ⒻⒸⒼ / Ⓑ center Ⓓ / ⒺⒶⒽ`; numbered child grids must use `⑥③⑦ / ② center ④ / ⑤①⑧`.
- 井字號 mode must use `ⒻⒸⒼ / Ⓑ center Ⓓ / ⒺⒶⒽ`, with `Ⓒ` north, `Ⓑ` west, `Ⓐ` south, and `Ⓓ` east.
- Every surrounding title has four Han characters directly after its label when possible.
- Every surrounding content cell has exactly five Han characters.
- Line 6 center content has exactly five Han characters.
- Line 7 center cell is `◎◎◎◎◎` by default.
- The eight surrounding cells are orthogonal and not synonym repeats.
- No Markdown table, rails, ASCII border, HTML, or explanatory text appears in the default output.

If any check fails, rewrite the card instead of explaining the failure.

## Legacy Modes

Use legacy PE2, bordered, HTML, or renderer-based output only when the user explicitly asks for:

- PE2.
- Boxed text.
- Visible borders.
- Old mobile UI.
- HTML preview.
- Deterministic renderer debugging.

For legacy rendering, use `scripts/imandalart_card.py` and read `references/imandalart-style.md` only when those legacy modes are relevant. Do not use the PE2 renderer for the default 2.2 pure-text card.
