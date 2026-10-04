---
name: hot-news-carousel
description: Research, write, structure, design, generate, inspect, and deliver Chinese 1080x1440 vertical news carousels plus titled, detailed, ready-to-paste publication copy ending in exactly five hashtags. Use when the user provides a current topic, link, announcement, lawsuit, product release, person, or raw material and asks for 热点新闻、抖音图文、科技新闻海报、杂志感图文、小红书新闻长图、AI热点出图、视频简介、发布文案，or wants to discover a timely topic and turn it into a credible multi-page visual story. Determine page count from the reporting instead of forcing five pages.
---

# Hot News Carousel

Turn one timely topic into a source-backed mother draft, a content-driven page structure, and a publishable Chinese news carousel. Run the full workflow by default without pausing between stages unless facts conflict, the protagonist is unclear, or the user requests an approval checkpoint.

## Fixed production contract

- Export every page as PNG at exactly 1080 x 1440 pixels.
- Never mix sizes or aspect ratios inside a series.
- Determine page count from information density; normally use 4-8 pages, but do not add filler to reach a number.
- Make the cover title-led and protagonist-led.
- Make every following page a magazine-like combination of a related visual, a headline, and substantive natural-paragraph copy.
- Resolve an optional account attribution before layout. If configured, typeset it exactly on every page in a consistent safe-area position; if absent, omit it consistently rather than inventing a handle.
- Generate a titled, detailed, ready-to-paste publication description with the carousel. The title must work when the copy is published alone and when it accompanies the carousel. End its final non-empty line with exactly five topic-relevant hashtags.
- Inspect facts, text, visuals, and dimensions before delivery.
- End with a clickable output-folder path.

Read [references/production-brief.md](references/production-brief.md) when building the mother draft and page manifest. Read [references/visual-system.md](references/visual-system.md) before composing or generating pages.

Resolve `account_attribution` in this order: an explicit user instruction, `hot-news-carousel.config.yaml` in the current project, then no attribution. Do not pause a direct-production request only to ask for a handle. A minimal project config is:

```yaml
account_attribution: "@账号名"
```

## Workflow

### 1. Accept or discover the topic

Accept any of these inputs:

- a topic or headline;
- a URL;
- raw notes, screenshots, or source material;
- a request to find today's most worthwhile topic.

If topic discovery is requested, use a current news radar first. For AI news, use `$aihot` when available, then independently verify the selected story. If the user provides a topic or link, begin from it but still search for current corroboration.

### 2. Research and write the mother draft

Browse because hotspot facts are time-sensitive. Prefer:

1. primary sources such as official announcements, filings, product pages, regulators, court documents, transcripts, and company statements;
2. reliable independent reporting;
3. clearly labeled commentary for interpretation only.

Use at least one primary source and one independent source when available. Verify event date, publication date, names, product status, quotes, numbers, and whether a statement is an allegation, denial, inference, or final finding.

Create a fact ledger:

- `已确认`: supported directly by sources;
- `一方主张`: attributed allegation or company claim;
- `分析判断`: explicit analysis, not fact;
- `待确认`: omit from artwork until resolved.

Then write one coherent Chinese mother draft before splitting pages. Cover what happened, background, core facts, key actor or mechanism, why it is hot, consequences, uncertainty, and what to watch next. Do not draft pages independently from scattered search results.

Never invent case numbers, dates, quotations, specifications, verdicts, UI states, release status, or product imagery. Do not present a generated scene as a documentary news photograph.

### 3. Derive page count and story structure

Split the mother draft by editorial questions, not equal word counts. Make each page answer one question and advance the story.

Use this pool only as needed:

- cover: what happened and why it matters;
- background: how the story began;
- core facts: what changed, launched, or is being claimed;
- key person, product, or mechanism;
- why the public or industry is watching;
- user or industry impact;
- dispute and uncertainty;
- conclusion and next development.

Normally produce 4-8 pages. Use fewer for a small event and more for a genuinely complex story. If a body page would exceed about 180 Chinese characters, split by meaning instead of shrinking the font. If a planned page repeats an earlier page, remove or merge it.

### 4. Write final page copy

Keep the cover sparse: one strong headline, one explanatory subtitle, and a page marker. Make the headline factual but attention-worthy.

For content pages:

- use one clear headline;
- write 80-160 Chinese characters by default, with 180 as a hard ceiling;
- split copy into 2-3 natural paragraphs of 1-2 sentences each;
- add at most one keyword label or compact data callout;
- attribute claims with wording such as “官方公告显示”“诉状称”“该公司表示”;
- preserve reading rhythm instead of using PPT bullet dumps.

Do not repeat the cover language on every page. Do not use hype, verdict language, or titles that exceed the evidence.

### 5. Write the publication description

Generate `video-description.md` and a plain-text `video-description.txt` from the same verified mother draft. Treat this as a default deliverable, not an optional follow-up.

- Start both files with the same publication title. Use `# 标题` as the first non-empty line in Markdown and the plain title without Markdown syntax as the first non-empty line in TXT.
- Write a concrete, self-contained title that names the subject or event and carries the core tension. It must make sense without the carousel, but should add context rather than mechanically repeat the cover headline when both appear together.
- Do not use vague titles such as “这件事值得关注”“完整解析” or titles that depend on a preceding image to identify the subject.
- Write roughly 500-900 Chinese characters by default; expand when the story genuinely needs more context.
- Make it more detailed than the artwork without merely concatenating page copy.
- Open with a readable hook, then explain what happened, the key mechanism or evidence, why it matters, and the main uncertainty or next development.
- Preserve the fact ledger. Attribute company claims and allegations, and do not promote `待确认` material into fact.
- Make the text ready to paste into a Douyin video or carousel description. Do not add internal production notes or a source appendix inside it.
- Put exactly five topic-relevant hashtags on the final non-empty line. Do not place any text after the hashtags and do not pad the set with unrelated trending tags.
- Keep the Markdown and plain-text versions substantively identical after removing the Markdown heading marker; TXT should remain clean copy-paste text.

### 6. Compose at exactly 1080 x 1440

Use the editorial baseline in [references/visual-system.md](references/visual-system.md): oversized typographic hierarchy, high contrast, restrained rules, generous whitespace, one accent color, and clear phone-scale readability.

Choose the cover protagonist by story type:

- product or software: product name plus logo, interface, device, or official key visual;
- person-centered event: the central person;
- company event: company identity, headquarters, or relevant product;
- lawsuit or policy: the actual parties or institution plus restrained legal or policy context.

The protagonist is not always a person. Never add a celebrity or executive merely to fill the page.

For content pages, use one visual directly related to that page's claim. Prefer official press assets or properly attributed source imagery. Label clearly conceptual or generated imagery when it could be mistaken for an unreleased product or documentary photograph.

Use the reliable rendering path by default:

1. source or generate the dominant visual without long embedded text;
2. typeset verified Chinese with HTML/CSS, SVG, canvas, or another deterministic method;
3. export the composed page as PNG;
4. crop or pad deliberately to 1080 x 1440 without distortion.

Allow one-shot image generation only for a sparse cover when exact Chinese is still inspected afterward. Do not ask an image model to render long Chinese body copy.

### 7. Apply the editorial visual system

Keep one system across the series:

- warm white, black, and gray foundation;
- one topic-specific accent color;
- bold display headline and restrained sans-serif body text;
- thin rules, strong grid, generous safety margins;
- content pages with roughly 45-60% related visual and 40-55% text;
- fixed page-marker position and consistent paragraph width.
- when `account_attribution` is configured, use its exact text in one fixed safe-area position on every page.

Avoid PowerPoint cards, flowcharts, arrow networks, dense icon grids, cyberpunk effects, decorative filler, and repeated hero portraits. Use magazine and long-read references as hierarchy guidance without copying a publication's exact trade dress.

### 8. Perform two-pass inspection

Open every exported image and inspect it at phone scale.

Fact pass:

- verify names, dates, products, quotes, and numbers;
- keep allegations, denials, findings, and analysis distinct;
- remove unsupported case numbers, UI, products, logos, people, and micro-details;
- confirm that every consequential claim appears in `sources.md`.

Visual pass:

- verify exact Chinese and remove garbled or accidental text;
- verify image-copy relevance and no needless protagonist repetition;
- verify readable type, safe margins, hierarchy, accent, and page markers;
- if `account_attribution` is configured, verify every page contains that exact, legible text inside the safe area; if absent, verify no placeholder or invented handle appears;
- verify that every PNG is exactly 1080 x 1440.

Publication-copy pass:

- verify that the first non-empty line is a self-contained publication title in both files;
- verify that the normalized Markdown and TXT titles match and work both with and without the carousel;
- verify that the publication title does not merely duplicate the cover headline when the two would appear together;
- verify that the description matches the same fact ledger and sources as the artwork;
- verify that claims and uncertainty retain correct attribution;
- verify that `video-description.md` and `video-description.txt` contain the same publishable copy;
- verify that the final non-empty line contains exactly five hashtags and nothing follows it.

If a generated visual contains invented micro-details, replace, crop, or blur the visual instead of explaining the error in a caption.

Run:

```bash
python3 scripts/validate_carousel.py OUTPUT_DIR --width 1080 --height 1440 --validate-copy
```

Pass `--count N` only when the editorial plan intentionally fixes a page count.

### 9. Package and send the address

Create a dated topic folder under the current project's `outputs/` directory:

```text
outputs/YYYY-MM-DD-topic-slug/
```

Use numbered filenames such as `01-cover.png`, `02-background.png`, and `03-core-facts.png`. Include:

- `brief.md`: fact ledger, mother draft, and page plan;
- `copy.md`: exact final text by page;
- `video-description.md`: titled, detailed ready-to-paste publication copy ending in five hashtags;
- `video-description.txt`: plain-text copy with the same title and publication description;
- `sources.md`: claim-level source links;
- all numbered PNG pages.

Report the page count, verified 1080 x 1440 dimensions, publication-copy delivery, any remaining `待确认` item, and a clickable absolute folder link. Do not claim readiness until visual inspection, dimension validation, and the five-hashtag check pass.

## Invocation examples

- “用今天最值得讲的 AI 热点做一套抖音图文，页数你根据内容决定。”
- “把这个链接做成1080×1440的杂志感新闻图文，直接完成并给我地址。”
- “把这个热点做成抖音图文，并同步生成一份详细简介，末尾带五个tag。”
- “先完成搜索、母稿和分页结构，暂时不出图。”
- “沿用这个封面方向，把这条新品新闻做成完整系列。”
