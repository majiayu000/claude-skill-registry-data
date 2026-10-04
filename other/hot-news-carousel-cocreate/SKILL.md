---
name: hot-news-carousel-cocreate
description: "Co-create a source-backed Chinese 1080x1440 news carousel through three sequential editorial checkpoints: narrative angle, stance and cover title, then visible visual direction boards. Use only when the user explicitly asks for 共创一期、共创版、共同决定叙事/标题/视觉、先选方向再出图, or invokes $hot-news-carousel-cocreate. Preserve automated research, drafting, pagination, rendering, inspection, and publication-copy delivery outside the three user decisions."
---

# Hot News Carousel Co-create

Turn one timely topic into a publishable Chinese news carousel while preserving the user's editor-in-chief decisions. Keep research and production automatic. Pause exactly three times, in order, for choices that materially affect the work:

1. narrative angle;
2. stance and cover title;
3. visible visual direction.

Do not collapse the checkpoints into one questionnaire. Do not add routine approval steps between them. Read [references/cocreate-checkpoints.md](references/cocreate-checkpoints.md) before presenting any checkpoint, [references/production-brief.md](references/production-brief.md) before drafting, and [references/visual-system.md](references/visual-system.md) before making direction boards or final pages.

## Fixed production contract

- Export final pages as PNG at exactly 1080 x 1440 pixels.
- Determine page count from reporting density, normally 4-8 pages; never add filler.
- Resolve `account_attribution` from explicit instruction, `hot-news-carousel.config.yaml`, then no attribution.
- Generate `video-description.md` and `video-description.txt` with the same self-contained title and publishable copy. End the final non-empty line with exactly five relevant hashtags.
- Keep facts, attributed claims, inference, opinion, and unresolved unknowns distinct.
- Inspect facts, Chinese text, visuals, dimensions, attribution, and publication copy before delivery.
- End with a clickable absolute output-folder path.

## Co-creation state

Create the dated topic folder early under `outputs/YYYY-MM-DD-topic-slug/`. Maintain `cocreate-state.md` there so the work can resume across turns. Record:

- topic and source input;
- current status;
- completed checkpoint decisions in the user's own words;
- current mother draft and page-plan file locations;
- pending next action.

Use these statuses:

```text
researching
awaiting_narrative
drafting
awaiting_stance_title
planning_visuals
awaiting_visual
producing
complete
```

At the start of every resumed turn, read `cocreate-state.md` and continue from the recorded status instead of restarting. Update it immediately before ending a checkpoint turn and after receiving a choice.

## Explicit rejection log

Use `hot-news-carousel.cocreate-log.md` in the current project root for explicit negative choices. Create it only when the user explicitly rejects a narrative, title, visual direction, or expression pattern and provides or clearly implies a reason.

Record:

| 日期 | 主题 | 被否方向 | 否决原因 | 可复用规则 |
|---|---|---|---|---|

Do not treat an unselected option as rejected. Do not infer a permanent preference from one choice. Read existing entries before proposing candidates, but allow the user to override or revise them.

## Workflow

### 1. Accept or discover the topic

Accept a topic, URL, raw notes, screenshots, source material, or a request to discover a timely topic. Browse because hotspot facts are time-sensitive. For AI topic discovery, use `$aihot` when available, then independently verify the selected story.

Prefer:

1. primary sources such as official announcements, filings, product pages, regulators, court documents, transcripts, and company statements;
2. reliable independent reporting;
3. clearly labeled commentary for interpretation only.

Use at least one primary source and one independent source when available. Verify event date, publication date, names, product status, quotations, numbers, and whether a statement is an allegation, denial, inference, or final finding.

Create a research ledger:

- `已确认`: directly supported;
- `一方主张`: attributed claim;
- `分析判断`: interpretation, not fact;
- `待确认`: excluded from final artwork until resolved.

Never invent dates, case numbers, quotations, specifications, verdicts, UI states, release status, or documentary imagery.

### 2. Checkpoint 1 — narrative angle

After baseline research, create three materially different editorial angles. They must differ in core question, audience benefit, and likely conclusion—not merely headline wording.

For each candidate include:

- core question;
- primary audience;
- reader value;
- likely conclusion;
- what this direction intentionally de-emphasizes;
- editorial opportunity and risk.

Offer a recommendation with a short evidence-based reason, but preserve all three as viable choices. Allow selection, rejection, or mixing such as “B 为主，吸收 C 的结论”.

Write the candidates to `checkpoint-1-narrative.md`, set status to `awaiting_narrative`, present the mature options, ask one concise choice question, and stop the turn. Do not draft the mother article until the user responds.

### 3. Write the mother draft

After the user selects or mixes a narrative angle, record the decision and set status to `drafting`. Write one coherent Chinese mother draft covering what happened, background, core mechanism or evidence, why it matters, impact, uncertainty, and what to watch next.

Build a three-layer editorial map from that draft:

- **事实层**: claims directly supported by sources;
- **推演层**: plausible consequences derived from mechanism, precedent, or trend;
- **观点层**: the value judgment or stance the edition may express.

Do not promote inference or opinion into fact. Save the draft and layered map in `brief.md`.

### 4. Checkpoint 2 — stance and cover title

Show the three-layer editorial map first so the user can calibrate certainty, aggression, and emotion. Then provide 2-3 cover-title directions that include at least:

- restrained news framing;
- conflict/传播 framing;
- explicit viewpoint framing.

For every title include:

- exact title and optional subtitle;
-传播 advantage;
- factual or rhetorical risk;
- which fact, inference, or viewpoint it foregrounds;
- recommended expression intensity: `克制`, `鲜明`, or `尖锐`.

Intensity changes rhetoric, never the evidence threshold. Allow responses such as “强度选鲜明，标题 2，但删掉终于”.

Write the options to `checkpoint-2-stance-title.md`, set status to `awaiting_stance_title`, ask for one combined stance/title decision, and stop the turn. Do not paginate or design before the user responds.

### 5. Derive page plan and asset inventory

After checkpoint 2, lock the selected stance and working cover title. Split the mother draft by editorial questions, not equal word counts. Make each page answer one question and advance the story.

Write 80-160 Chinese characters per content page by default, with 180 as a hard ceiling. Use natural paragraphs, not PPT bullet dumps. Attribute claims explicitly.

Create an asset inventory before visual exploration:

- available official images, screenshots, documents, logos, or portraits;
- which page each asset can legitimately support;
- pages that require a diagram or conceptual visual;
- restrictions, attribution, and unresolved visual gaps.

Save the page plan and asset inventory in `brief.md`, then set status to `planning_visuals`.

### 6. Checkpoint 3 — visible visual direction

Create 2-3 visible direction boards before final rendering. Do not offer text-only labels such as “杂志风” or “科技感”. Each board must use the selected title, real copy excerpts, and available subject assets to show the same three roles for fair comparison:

- cover;
- representative content page;
- conclusion or turning-point page.

Save boards under `previews/direction-a.png`, `direction-b.png`, and optionally `direction-c.png`. A board is a comparison artifact, not a publishable page; it may place three reduced page mockups plus type, palette, contrast rhythm, and density notes on one canvas.

Make directions materially different across at least three axes:

- typography voice;
- light/dark rhythm;
- page structure and image ratio;
- information density;
- image treatment;
- accent strategy.

Do not make every direction use dark cover + light body + dark conclusion. At most one candidate may use that rhythm. Include an all-light, all-dark, or content-driven contrast alternative when appropriate. Treat exact fonts, palette, and layout as selectable proposals, not prior hard constraints.

For every board state its strengths, tradeoffs, and content fit. Allow full selection or mixing such as “A 的字体和留白，B 的图片处理，C 的深浅节奏”.

Write the explanation to `checkpoint-3-visual.md`, set status to `awaiting_visual`, present the images and concise comparison, ask one visual decision question, and stop the turn.

### 7. Lock the visual contract

After checkpoint 3, record the selected or mixed direction in `visual-contract.md`:

- contrast rhythm;
- headline and body typography;
- palette and accent use;
- page archetypes and density;
- image treatment;
- explicit prohibitions;
- user wording that determined the choice.

Use the contract for this series only. Do not promote it into a permanent account rule without repeated explicit approval.

### 8. Produce automatically

Set status to `producing` and complete the remaining workflow without another approval pause:

1. finalize page copy;
2. source or generate necessary visuals without long embedded Chinese text;
3. typeset Chinese deterministically with HTML/CSS, SVG, canvas, Pillow, or equivalent;
4. export every final page at exactly 1080 x 1440;
5. create `copy.md`, `sources.md`, `video-description.md`, and `video-description.txt`;
6. inspect every page at phone scale;
7. run `scripts/validate_carousel.py OUTPUT_DIR --width 1080 --height 1440 --validate-copy`.

If a generated visual contains invented micro-details, replace, crop, or blur it. Do not explain the defect in a caption.

### 9. Deliver

The output folder must contain:

- `brief.md`;
- `cocreate-state.md`;
- `checkpoint-1-narrative.md`;
- `checkpoint-2-stance-title.md`;
- `checkpoint-3-visual.md`;
- `visual-contract.md`;
- `copy.md`;
- `sources.md`;
- `video-description.md`;
- `video-description.txt`;
- `previews/` direction boards;
- all numbered final PNG pages.

Set status to `complete`. Report the final page count, verified dimensions, publication-copy delivery, remaining `待确认` items, and the clickable absolute output-folder path.

## Interaction rules

- Pause only at the three named checkpoints and always in order.
- End the turn after each checkpoint question; never assume the user's choice.
- Provide mature, clearly differentiated candidates instead of asking the user to invent a direction from scratch.
- Let the user select, mix, edit, or reject candidates in natural language.
- If the user explicitly says “直接完成” during co-creation, use the current decisions and recommended remaining options, record that override, and finish without further pauses.
- If facts materially change after a checkpoint, explain the conflict and revisit only the affected decision.
- Preserve the original `hot-news-carousel` as the direct-production path; never modify or slow it from this skill.

## Invocation examples

- “用共创版做一期这个新闻。”
- “共创一期今天最值得讲的 AI 热点。”
- “这条新闻先让我选叙事、标题和视觉，再出完整图。”
- “Use $hot-news-carousel-cocreate on this link.”
