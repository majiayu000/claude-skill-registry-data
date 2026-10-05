---
name: fire-analysis-card
description: "Analyze Chinese notes, articles, manuscripts, and digital card-box material with FIRE 2.0: Full-D numbering, Index keyword webs, Route thinking paths, and Evolution over time. Use when Codex needs to prepare material for semantic search, turn temporary notes into permanent or project notes, build table-of-contents/index/search structures, create compact Chinese FIRE cards, or maintain this skill's original discussion thread provenance."
---

# FIRE Analysis Card 2.0

Transform Chinese notes, short articles, manuscripts, or book-system material into semantic-search-ready digital card-box structure using FIRE 2.0:

- `F = Full-D`: give every temporary note a stable full number, then refine it into a permanent note; if publishing, turn it into a project note with complete book/project numbering.
- `I = Index`: build keyword indexes and re-entry points so a tree-shaped manuscript can also become a spider-web knowledge structure.
- `R = Route`: design thinking routes through the material so cards can support narrative, search paths, and the next creative card.
- `E = Evolution`: track how notes evolve through time grids, plans, reviews, and conversations with the digital card box.

Strategic frame:

> 戰場上核心戰略只有一個：火力與移動。
> 不移動，局勢就由別人決定。不開火，就會被別人釘在原地。
> ─ Joel Spolsky

FIRE 2.0 treats `Full-D` and `Index` as search firepower, and `Route` and `Evolution` as knowledge movement. The goal is not just to summarize source text, but to prepare it for table-of-contents search, exact keyword search, and semantic search.

## Version

- Current version: `2.0`
- v2 meaning: `Full-D / Index / Route / Evolution`
- Legacy v1 meaning: `Fact / Index / Relation / Encyclopedia`
- When an older prompt expects v1, preserve the old card style if explicitly requested; otherwise prefer v2.
- If source text writes `Eolution`, normalize it to `Evolution` unless quoting the source.

## Source Discussion Thread

- Original Codex thread id: `019ed5d7-9b24-7581-b98e-9e29027e85f3`
- Title fragment: `各章節內容Desktop的改善 目標 $fire-analysis-card $pdca $project-...`
- Date: `2026-06-17`
- Index evidence: `/Users/twhsi/.codex/session_index.jsonl` has `updated_at: 2026-06-17T13:49:43.934892Z`.
- Role: this thread used `fire-analysis-card` with `pdca` and `project-note-json-to-epub` to produce a Skill-ecology EPUB, placing FIRE as the card-analysis layer in the user's Skill ecosystem.

## Provenance Lookup Workflow

When the user asks to find, verify, or update the original discussion thread for this skill:

1. Prefer Codex thread tools: run `list_threads` with query `fire-analysis-card`, then read thread `019ed5d7-9b24-7581-b98e-9e29027e85f3`.
2. Distinguish that source thread from later maintenance threads by title, date, and the `/goal` prompt that invokes `$fire-analysis-card`, `$pdca`, and `$project-note-json-to-epub` together.
3. If thread tools are unavailable, search local history with `rg` for `fire-analysis-card`, `FIRE Analysis Card`, `知識成頁`, or `Fact 事實` in `~/.codex/session_index.jsonl`, `~/.codex/archived_sessions`, and `~/Documents/Codex`.
4. Report the thread id, title fragment, date, and evidence path before making provenance claims. Mark weaker candidates as `待證`.

## Core Rules

- For article, note, manuscript, or card-box analysis requests, always render the main FIRE card in a fenced `text` code block.
- For maintenance or provenance requests about this skill, do not render a FIRE card; inspect or update the skill and cite the source thread evidence instead.
- Use FIRE 2.0 by default: `Full-D / Index / Route / Evolution`.
- Use full-width spaces `　` for visual alignment.
- Use half-width spaces only inside English labels such as `Full-D 全編號`.
- Keep the center phrase at 8 Chinese characters or fewer, prefixed with `◎`.
- Prefer Chinese phrases of 4 to 8 characters in the card.
- Analyze the source as search infrastructure, not merely as prose summary.
- Preserve the author's main claim, but rewrite it into stable knowledge-system language.
- When source evidence is weak or missing, mark it as `待編`, `待證`, `推論`, or `需補例`.
- Render only one main card unless the user asks for explanation, debug spacing, or multiple versions.

## FIRE Meaning

- `Ⓕ Full-D 全編號`: assign stable IDs to temporary notes, convert them into permanent notes, and when publishing, produce project notes with complete part/chapter/section/item numbering.
- `Ⓘ Index 索引`: create keyword indexes, categories, tags, questions, aliases, and retrieval handles. For book-scale material, prefer eight major keyword categories and 64 core keywords when the source supports it.
- `Ⓡ Route 路徑`: build thinking paths through the material. Routes can follow table of contents, keyword webs, narrative arcs, or target-person formulas, and should help generate the next card.
- `Ⓔ Evolution 演化`: show how cards change through present notes, daily plans, weekly plans, yearly plans, life plans, reviews, and Mandala-style time grids until the card box becomes a dialogue partner.

Use the flow:

`Raw Notes -> Full-D -> Index -> Route -> Evolution -> Semantic Search -> AI Dialogue`

## Fixed Template

Copy this template first, then replace the phrases.

```text
　　　　　　　　　　【Ⓕ Full-D 全編號】
　　　　　　　　　　編號：＿＿＿＿
　　　　　　　　　　定稿：＿＿＿＿
　　　　　　　　　　出版：＿＿＿＿


　　　　　↗　　　　　　　　　　　　　　　↘
　　【Ⓘ Index】　　　中【◎核心】　　　【Ⓡ Route】
　　　關鍵字網　　　　◎＿＿＿＿　　　　思考路徑
　　　────────　────────　────────
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿


　　　　　↖　　　　　　　　　　　　　　　↙
　　　　　　　　　　【Ⓔ Evolution】
　　　　　　　　　　當下：＿＿＿＿
　　　　　　　　　　計劃：＿＿＿＿
　　　　　　　　　　對話：＿＿＿＿
```

## Compass Mapping

- Top `Ⓕ Full-D`: the numbered source tree: temporary note, permanent note, project note, and full part/chapter/item path.
- Left `Ⓘ Index`: the keyword web: categories, aliases, questions, and exact-search handles.
- Right `Ⓡ Route`: the thinking route: narrative path, search path, cross-branch path, and next-card path.
- Bottom `Ⓔ Evolution`: the time process: now, day, week, year, review, life plan, and card-box conversation.
- Center `◎核心`: the search object or knowledge object, not the mood or slogan.

Arrow meanings:

- `↘` means Full-D -> Route: numbered notes become traversable paths.
- `↙` means Route -> Evolution: routes generate next cards and long-term change.
- `↖` means Evolution -> Index: evolved notes create better keywords and re-entry points.
- `↗` means Index -> Full-D: indexes reveal missing notes, duplicate notes, or notes needing better numbers.

## Construction Workflow

1. Read the source once for topic, stance, and knowledge-system purpose.
2. Extract the center `◎核心詞` in 8 Chinese characters or fewer.
3. Fill `Ⓕ Full-D` with a numbering proposal, note status, and project/book path. Mark unknown IDs as `待編`.
4. Fill `Ⓘ Index` with retrieval handles: one title-like entry, one tag/category entry, and one question or exact-search keyword.
5. Fill `Ⓡ Route` with three route lines: one table-of-contents or structural route, one keyword/cross-link route, and one semantic or next-card route.
6. Fill `Ⓔ Evolution` with time-based movement: present state, plan/review rhythm, and how the card box becomes a dialogue partner.
7. Compress long phrases before widening the layout.
8. If the user asks for a full analysis, add a short prose section after the card with `Full-D / Index / Route / Evolution` bullets.

## Search Modes

Use FIRE 2.0 to support three kinds of digital card-box search:

- `目錄索引搜尋`: use Full-D numbering and book/project structure to find material by part, chapter, section, or item.
- `精確關鍵字搜尋`: use Index categories and exact keywords like Google-style search handles.
- `語意搜尋`: use FIRE's attention-friendly structure: numbered nodes, keyword signals, route paths, and evolving contexts.

## 1000-Character Article Handling

For an article around 1000 Chinese characters:

- Extract 3 to 7 stable knowledge units, but put only the best 3 into the card.
- Create one Full-D proposal: note number, permanent-note status, and project-note path if relevant.
- Create 3 index handles: one title-like entry, one tag/category entry, and one question-like search cue.
- Create 3 route lines: one structural route, one keyword route, and one semantic/next-card route.
- Write evolution language as if it were an Obsidian or digital card-box concept page: neutral, reusable, revisable, and ready for future search.
- Do not quote long passages. Convert source wording into compact knowledge-system units.

## Phrase Compression

Prefer concise compounds:

- `幫每一張臨時筆記加上編號` -> `全編號`
- `把臨時筆記加工成永久筆記` -> `永久化`
- `出版時生成專案筆記並保留完整編號` -> `專案全碼`
- `部章節項目構成整本書目錄` -> `樹狀目錄`
- `八大類與六十四個核心關鍵字` -> `八類六四`
- `從樹狀結構變成蜘蛛網狀結構` -> `樹網互轉`
- `八大分類形成八條思考路徑` -> `八路徑`
- `靶心人公式的敘事結構` -> `靶心敘事`
- `數位卡片盒自生產生成下一張卡片` -> `下一卡`
- `當下、日計劃、週計劃、年計劃、百年人生計劃` -> `時間九宮`
- `語意搜尋的肥沃土壤` -> `語搜土壤`

## Full Analysis Add-On

If the user asks for more than a card, append this compact structure after the `text` card:

```markdown
**F｜Full-D**
- ...

**I｜Index**
- ...

**R｜Route**
- ...

**E｜Evolution**
- ...

**搜尋判斷**
- ...
```

Keep this add-on short unless the user asks for a long encyclopedia entry or book-system plan.

## Visible Spacing Debug

If the user asks for a visible spacing version, show a second debug block where:

- `□` means one full-width space `　`.
- `·` means one half-width space.

Visible debug example:

```text
□□□□□□□□□□【Ⓕ·Full-D·全編號】
□□□□□□↗□□□□□□□□□□□□□□□□□↘
□□【Ⓘ·Index】□□□中【◎核心】□□□【Ⓡ·Route】
□□□關鍵字網□□□□◎語搜土壤□□□□思考路徑
```

## Example

```text
　　　　　　　　　　【Ⓕ Full-D 全編號】
　　　　　　　　　　編號：部章節項
　　　　　　　　　　定稿：永久筆記
　　　　　　　　　　出版：專案全碼


　　　　　↗　　　　　　　　　　　　　　　↘
　　【Ⓘ Index】　　　中【◎核心】　　　【Ⓡ Route】
　　　關鍵字網　　　　◎語搜土壤　　　　思考路徑
　　　────────　────────　────────
　　　八類六四　　　　樹狀目錄　　　　　目錄路徑
　　　精確搜尋　　　　蜘蛛網索　　　　　靶心敘事
　　　語意入口　　　　時間九宮　　　　　下一卡


　　　　　↖　　　　　　　　　　　　　　　↙
　　　　　　　　　　【Ⓔ Evolution】
　　　　　　　　　　當下：臨時筆記
　　　　　　　　　　計劃：日週年宮
　　　　　　　　　　對話：卡盒夥伴
```
