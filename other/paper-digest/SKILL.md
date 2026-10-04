---
name: paper-digest
description: >
  Produce a content/knowledge digest of ONE paper for fast absorption of its full content — not a
  quality critique. Use when the user wants to "整理內容", "快速吸收", "知識整理", "內容平讀", or when
  /paper-sync dispatches a 📚內容 pick. The digest reorganizes the paper's full text into a teaching-style
  structured note (structure routed by paper type) plus self-test review cards pushed to the 複習頁
  (configured `review_site.url`). REQUIRES full text: no full text → STOP and report 缺全文, never
  produce an abstract-only digest. NOT a critical appraisal (that is /paper-review) and NOT a
  multi-paper synthesis.
---

# Paper Digest — 單篇論文內容整理（快速吸收）

## What this is (and is NOT)

`/paper-review` answers **「這篇可不可信、做得好不好」**. `/paper-digest` answers
**「這篇講了什麼、我怎麼最快把全部內容吸收進腦袋」**. It is for papers read as **content / knowledge
material**（綜論、技術介紹、機制整理、指引）. The two are independent and can both run on one paper
(combined note). A digest additionally feeds the **複習迴圈**: it generates self-test cards that go to
the review web page so learning doesn't end at "note written".

Tone, language, and clinical framing are driven by `${persona}` (see Configuration). Follow vault
note rules (Tab indent, `> [!type]` callouts, `${persona.highlight_style}` for cut-offs, no code
blocks for clinical content).

## Configuration (read FIRST, every run)

Read **`config.yaml`** in the sibling `paper-review/` skill directory (shared config; copy
`config.example.yaml` → `config.yaml` on first setup). Keys this skill uses:
`${vault.papers_dir}`, `${vault.medicine_dir}`, `${vault.inbox_note}`, `${vault.daily_section}`,
`${review_site.url}`, `${review_site.push_script}`, `${persona}`. Substitute every `${...}` with the
config value; a blank value means "skip that route" (e.g. empty `review_site.push_script` → no card push).

## Input
DOI / PMID / title / PDF path / pasted full text. Optional flags:
- `--into <note path>` — instead of creating a standalone note, **prepend** the digest as a
  `## 內容整理（快速吸收）` section into an existing note (used by /paper-sync when both 🔬+📚 picked,
  so content sits above the appraisal in one file).
- `--no-cards` — skip review-card generation/push (default is to generate).

## Phase 0 — Full text is MANDATORY (hard gate)

Acquire full text per the shared protocol **`~/.claude/skills/paper-review/fulltext-acquisition.md`**
(user-provided → `${fulltext.inbox_dir}` → Zotero → OA auto-fetch → Elsevier TDM → institutional SFX resolver).

**If no route yields full text → STOP.** Do NOT write an abstract-only digest. Report:
`缺全文：{title} — 需要 PDF 才能做內容整理`. When called from /paper-sync this routes to the 缺全文 handoff
(logged to `${vault.inbox_note} # 缺全文待補`; user supplies PDF then says「繼續」). Abstract-only is
exactly the over-simplification this skill exists to avoid.

## Phase 1 — Build the digest（三層漸進揭露）

Goal: a reader can absorb **all the substantive content** without opening the PDF. Reorganize, don't
transcribe. Every digest has THREE layers (user's Esor 三層筆記法):

1. **30 秒層** — `> [!summary] 一句話 + 重點` callout (between frontmatter and first heading):
   one-line takeaway + 3–5 bullets of the highest-value facts (mechanisms, numbers, conclusions).
   End the callout with one quality pointer line:
   `品質未評讀（內容整理）；需可信度判斷 → /paper-review` — or, if a 品質快照 already exists in the
   combined note, `品質 → 見上方品質快照`.
2. **5 分鐘層** — each `##` section OPENS with a one-line `**要點**：…` bold summary before its
   bullets, so scanning only the 要點 lines reconstructs the paper.
3. **完整層** — the full structured bullets/tables below each 要點.

### Section structure — ROUTED BY PAPER TYPE (pick one, don't force-fit)

**A. Empirical study（RCT / 觀察性 / diagnostic…）** — default:
- `## 研究問題 / 背景` — gap, why it matters, key prior context.
- `## 方法` — design, population, intervention, measures — concise, only what's needed to read the
  findings (deep methods scrutiny belongs to /paper-review).
- `## 主要發現` — the core. **Tabulate** numeric results (effect sizes, ==cut-offs==, CIs, p). One row
  per finding. Pull the actual numbers out of the text.
- `## 臨床意義 / 怎麼用` — so-what for a PMR clinician / teachable points.

**B. Narrative review / 機制整理** — concept-map style:
- `## 全文地圖` — how the author carves the topic into sections; one line per block.
- `## 各主題重點` — one `###` per theme: core claims, key numbers, the studies it leans on.
- `## 機轉白話講解` — for the hardest mechanism(s), a Feynman-style plain-Chinese walkthrough
  (analogy allowed); anything beyond the paper's own content marked `⚠️ 補充`. Written to be reusable
  when teaching residents.
- `## 臨床意義 / 怎麼用`

**C. Guideline / consensus**:
- `## 建議條文表` — table: recommendation / 強度 / 證據等級 / 適用族群, one row per recommendation.
- `## 與前版或他版差異` — what changed vs the previous edition or competing guideline (if stated).
- `## 實務落地` — how it maps to the user's practice setting.

**D. 技術 / 方法學論文**:
- `## 這個技術是什麼 / 解決什麼問題`
- `## Step-by-step protocol` — restated so it could be followed without the PDF.
- `## 適用時機與限制` — when to reach for it, failure modes, alternatives.

### Sections common to ALL types
- `## 重要圖表重述` — restate what each key figure/table shows in words. If a figure is essential,
  flag it for `/figure-remap` rather than embedding blindly.
- `## 與既有認知的對照` — run `vault_search` on the note's core concepts; where an existing
  `${vault.medicine_dir}` / `${vault.papers_dir}` note says something this paper updates, refines, or contradicts, list
  `舊認知（[[note]]）→ 本篇`. This is the knowledge-delta layer — also the candidate list for a later
  `/note-supplement`. Nothing to compare → one line「vault 無相關既有筆記」, don't pad.
- `## 概念 / 名詞整理` — teaching layer: define and connect the concepts/terms a learner needs. Link
  related vault notes `[[NoteName]]`.
- `## 自我測驗` — see Phase 2.
- `## Reference` — the paper itself (`` `Author 2026, Journal` `` + doi); pivotal citations it leans on.

Citation discipline: every claim in the digest comes from THIS paper's full text. Outside context added
to explain a concept → mark `⚠️ 補充`.

## Phase 2 — Self-test cards（主動回憶層）

The user's known failure mode is over-organizing and under-recalling — the digest must end with
retrieval practice, not just structure.

1. Write `## 自我測驗` in the note: 3–5 questions as folded callouts —
   ```
   > [!question]- Q1：{題目——偏臨床決策/機轉理解，不是背數字}
   > {答案，2-4 行，含關鍵數值與理由}
   ```
   Question quality bar: answerable from this paper alone; tests understanding ("為什麼選 X 而不是 Y",
   "什麼情況下這結論不適用") over recall of trivia; one question may target the paper's single most
   exam/practice-relevant number.
2. **Push to the 學習中樞** (unless `--no-cards` OR `${review_site.push_script}` is blank): write the
   cards to a JSON file in the scratchpad —
   `[{"citekey","note","title","question","answer","tags":["topic",...],"deck":"論文","source":"paper"}, ...]`
   (`note` = vault filename without .md; `title` = 中文短標; `deck` 固定 `"論文"`、`source` 固定 `"paper"`) — then:
   ```bash
   python ${review_site.push_script} <cards.json>
   ```
   The push script is idempotent (card_id = citekey + question hash, INSERT OR IGNORE) and prints the
   pushed count. Report:「已推 N 張複習卡 → ${review_site.url}」.
   Push failure (or blank push_script) → note still stands; report it and leave the JSON path for a
   manual retry — never block the digest on the card push.

## Output

- **Standalone** (default): write `${vault.papers_dir}{中文短標}.md`. Frontmatter `tags: [research/digest, …topic]`,
  `citekey`, `doi`, `aliases` for the English title if useful. Return the note filename to the caller.
- **`--into <path>`**: insert the `## 內容整理（快速吸收）` section (the body above, minus its own
  frontmatter) directly after the target note's `> [!summary]` callout / before its first appraisal
  heading, so content reads first and the /paper-review appraisal follows. Cards still get pushed.
- One line to today's daily note `${vault.daily_section}` is handled by /paper-sync (don't double-write when called
  from it). Standalone manual runs: add the daily-note line yourself.

## Notes
- This is a **new-note creation** task → normally show a draft for review. **Exception when invoked by
  /paper-sync**: write directly (the user already opted in by pressing 📚 and confirming the batch).
- Heavy (full-text + synthesis). Run on a capable model; for a /paper-sync batch, one subagent per paper.
- Don't duplicate `/paper-review`'s appraisal. If the user really wants both, that's the combined note —
  keep the digest descriptive and leave judgement to the appraisal section.

## Self-Check (before finalizing)
- [ ] 結構用對 paper type（A/B/C/D），沒有硬套 empirical 模板
- [ ] 三層齊：summary callout（含品質指標一行）/ 每節 **要點** 行 / 完整內容
- [ ] 主要發現有實際數值（不是「有顯著差異」）
- [ ] `## 與既有認知的對照` 跑過 vault_search（或標明無相關筆記）
- [ ] `## 自我測驗` 3-5 題、folded callout、偏理解型
- [ ] 複習卡已推（或回報失敗 + JSON 路徑）
