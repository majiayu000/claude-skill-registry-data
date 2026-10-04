---
name: writer
description: SEO-friendly article writing, audit, and humanization workflow for Markdown content. Use when creating, outlining, editing, auditing, rewriting, or quality-checking blog posts, tutorials, comparisons, listicles, explainers, FAQ sections, excerpts, SEO titles, meta descriptions, tags, or Google-friendly content briefs that need clear topics, natural keyword use, on-page SEO review, reader-friendly prose, and iterative optimization.
---

# Writer

## Overview

Use this skill to produce and improve Google SEO-friendly articles that stay focused on one topic, use keywords naturally, and avoid invented facts or over-marketing. Default output language should match the user's request unless they specify another language.

When the requested destination is a Chinese WeChat Official Account (微信公众号、微信文章、公众号推文), load `wechat-writer/SKILL.md` and follow that workflow instead of applying this Google-first structure. When the destination is a LinkedIn Article, newsletter, LinkedIn long-form post, or LinkedIn thought-leadership package, use `linkedin-writer/SKILL.md`; its output contract overrides this file and stores the package under `linkedin-writer/output/<article-slug>/`. When the destination is Medium or another editorial third-party article, use `medium-writer/SKILL.md`; its output contract stores the package under `medium-writer/output/<story-slug>/`.

For a full reusable prompt and final article template, load `references/seo-article-template.md` when the user asks for a ready-to-copy prompt, a complete article, or a reusable writing template.

For article audits, existing-page reviews, or post-draft optimization, load `references/seo-audit-checklist.md`.

For fact-heavy articles, comparisons, product/category analysis, or style polishing, load `references/fact-check-and-style.md`.

After the SEO audit and audit-driven rewrite, load `references/humanization.md` for the final humanization pass. Preserve verified facts, search intent, required keywords, citations, code, URLs, and the author's voice while removing mechanical or overly AI-like writing patterns.

For deliverables that must be saved as files, use the output rules in this file and load `references/output-packaging.md`.

Cloudflare R2 is optional. Always create the article with local relative image paths first. If `writer/config/r2.config.json` exists and contains valid values, load `references/r2-image-upload.md`, upload the images, and replace the local paths with public URLs. If that local config is absent, keep the local image references and finish normally.

For Cloudflare R2 credential handling and leak-prevention rules, load `references/r2-security.md`.

## Article Task Card

Before outlining or writing, create or infer a task card in 10 lines or fewer:

- Target reader: beginner, industry practitioner, or potential customer.
- Article type: how-to, comparison, listicle, or explainer.
- Main keyword: one primary keyword.
- Supporting keywords: 3 to 5 related keywords unless the user provides more.
- Target length: usually 800 to 1500 words.
- Tone: objective, editorial, restrained, and low-hype.
- Must include: at least 3 subheadings, 1 conclusion, and 3 FAQ items.
- Must avoid: fake data, fake quotes, unsupported claims, and excessive sales language.
- Optional CTA: link and anchor text if provided.
- Output format: Markdown unless the user asks otherwise.

If critical inputs are missing, make conservative assumptions and show them in the task card. Ask a question only when the topic, audience, or article type is too ambiguous to proceed safely.

## Workflow

Follow this sequence for new articles:

1. Create the article task card.
2. Generate title options that naturally include the main keyword or a close grammatical variant, then select the clearest SEO title.
3. Generate the outline only: table of contents plus 1 to 3 bullet points for each section. Do not write body copy during this step unless the user explicitly asks for a full article immediately.
4. After the outline is approved or when the user asks to continue, write the article section by section in Markdown.
5. Generate article images with Codex's built-in image generation capability when available, then add the SEO meta pack: SEO Title, Excerpt, Meta Description, and Tags.
6. Run fact checks for objective claims, feature comparisons, statistics, definitions, dates, prices, legal or policy statements, and any claim that could mislead if wrong.
7. Run a writing SEO audit: check title, TDK, search intent, first 100 words, headings, keyword coverage, content depth, FAQ, internal-link opportunities, image alt suggestions, E-E-A-T signals, and unsupported claims.
8. Rewrite based on the audit, prioritizing factual accuracy, search intent, and high-impact SEO issues first.
9. Load `references/humanization.md` and humanize the audit-corrected draft. Match a user-provided voice sample when available; otherwise use a natural voice appropriate to the publication and audience.
10. Run a post-humanization integrity check on changed passages. Recheck claims, certainty, keyword placement, metadata lengths, citations, code, URLs, image paths, and CTA destinations.
11. Save the final Markdown article and image assets under `writer/output/<article-slug>/`.
12. Check for `writer/config/r2.config.json`. Upload only when it exists and is valid; otherwise keep local relative image paths without treating the missing config as an error.
13. Re-audit only the changed areas and report the main improvements, including the humanization pass.

When the user provides the topic and asks for a complete article in one go, still internally follow the outline-first structure, then output the full article without exposing unnecessary process notes.

## Audit-Driven Optimization

Use the audit loop whenever a draft, published page, URL, or pasted article needs SEO improvement:

1. Separate deterministic checks from semantic judgment.
2. Deterministic checks include SEO title length, excerpt length, meta description length, H1 count, heading counts, keyword placement, FAQ presence, and missing image alt suggestions.
3. Semantic judgment includes search intent match, H1/title relevance, heading usefulness, content depth, E-E-A-T signals, clarity, specificity, and whether the CTA is too promotional.
4. Produce findings with this shape: issue, evidence, impact, fix, priority.
5. Rank fixes as Critical, High, Medium, or Low.
6. Apply fixes to the article instead of stopping at the report when the user asks to optimize.
7. Preserve true claims and the user's original positioning; do not fabricate facts to improve SEO.
8. Humanize the corrected draft only after Critical and High issues are resolved, then verify that the style rewrite did not change facts, certainty, links, code, or SEO requirements.

For URL audits, do not claim robots.txt, sitemap, PageSpeed, schema, canonical, status code, or crawlability results unless a tool or source actually verifies them. If technical checks are unavailable, mark them as "needs tool verification" and focus on content-level SEO.

## Post-Audit Humanization

Humanization is the final editorial stage, not a substitute for fact-checking or SEO auditing. Load `references/humanization.md` after the audit-driven rewrite and follow its draft, critique, revision, and integrity-check sequence.

During this pass:

- Preserve the article's meaning, verified claims, limitations, citations, technical tokens, URLs, and required search intent.
- Use an approved writing sample for voice calibration when the user provides one. Match rhythm and register without copying distinctive phrases.
- Remove clusters of mechanical writing such as significance inflation, unsupported promotional language, vague attribution, repetitive transitions, forced three-item lists, synonym cycling, uniform paragraph rhythm, generic conclusions, chatbot artifacts, and excessive formatting.
- Prefer concrete details and direct verbs. Vary sentence and paragraph length when it improves reading, but do not introduce fake personality, deliberate errors, or theatrical fragments.
- Never invent first-person testing, personal experience, customer stories, quotes, opinions, or anecdotes to make the article sound human.
- Do not promise that the result is undetectable or can bypass AI detectors. The goal is reader quality and an appropriate editorial voice.

After rewriting, ask internally what still feels templated or over-produced, revise those passages once more, and recheck only the affected facts and SEO elements.

## Fact Check and Evidence

Use a fact-check pass before finalizing articles that include claims beyond common knowledge:

1. Extract checkable claims: numbers, dates, rankings, definitions, product specs, policies, price, availability, legal/medical/financial statements, and competitive comparisons.
2. Mark each claim as verified, needs verification, softened, or removed.
3. Prefer primary or authoritative sources for verification: official documentation, product pages, standards bodies, government pages, research papers, or direct company statements.
4. Use web research when facts may have changed or when the user asks to reference current external analysis.
5. Synthesize external analysis in original language; do not copy another author's structure, phrasing, rankings, or conclusions directly.
6. Cite or name sources when factual support materially affects the reader's decision.
7. If reliable evidence is unavailable, rewrite the claim cautiously or omit it.

When using external sources, separate facts from interpretation. Facts should be traceable; recommendations can include the writer's own judgment as long as the reasoning is explicit.

When the user provides UI reference images to guide an article, use them as private reference material only. In the article body, captions, alt text, source note, SEO metadata, and audit notes, do not mention that visual references were provided or name their file/source format. Prefer natural phrasing such as "the interface shows," "the visible controls include," or "the live interface may change."

## Objective Comparison

For comparison articles, make the comparison deep and evidence-aware:

- Define comparison criteria before judging options.
- Compare by user scenario, strengths, limitations, cost or effort, output quality, learning curve, integrations, risk, and best-fit use cases when relevant.
- Avoid declaring one option "best" without explaining for whom and under what conditions.
- Include trade-offs and limitations, not only benefits.
- Distinguish verified facts from editorial judgment.

## Paragraph Quality Pattern

Use this paragraph pattern for main sections:

1. Conclusion sentence: state the practical point first.
2. Explanation: add 2 to 3 sentences with context or reasoning.
3. Example or steps: add 1 to 3 concrete examples, checks, or actions.
4. Mini-wrap: close with one sentence that connects back to the section topic.

Avoid filler openings, repeated definitions, and keyword stuffing. Use bullets only when they make scanning easier.

## Type-Specific Rules

### How-To

Use a four-step shape:

1. What to do: define the goal and destination.
2. What is needed: list materials, access, assumptions, or prerequisites.
3. How to do it: provide numbered steps.
4. Common questions: answer FAQ clearly.

### Comparison

Compare across five dimensions:

- Who it is for.
- Ease of use.
- Output or result quality.
- Key features or practical differences.
- Recommendation by use case.

### Listicle

Include 6 to 10 items unless the user asks for a different count. Each item should include a short explanation and a "best for" line when useful.

### Explainer

Include a plain-language definition, why it matters, common misconceptions, and practical application.

## SEO Requirements

- Include the main keyword or a natural close variant in the article title unless it would make the title grammatically awkward or misleading.
- Include the main keyword in the H1 or first paragraph.
- Include the main keyword in at least one H2.
- Include the main keyword once in the conclusion.
- Use each supporting keyword at least once naturally across the article.
- Let H2 headings be moderately longer when useful for SEO clarity, especially for comparison, tutorial, review, and news-analysis articles.
- Include the main keyword, a close variant, or a supporting keyword in H2 headings when natural; prioritize readability and search intent over exact-match stuffing.
- Generate an attractive SEO title related to the content, 65 to 70 characters.
- Generate a short excerpt related to the content, 155 to 160 characters.
- Generate an attractive SEO meta description related to the content, 55 to 160 characters.
- Prefer clear search intent over clever wording.
- Do not invent numbers, quotes, research, rankings, product specs, or citations.
- If a fact is uncertain, phrase cautiously with terms like "often," "in many cases," or omit it.

## SEO Audit Requirements

Always evaluate these writing-level checks before final delivery:

- Search intent: title, intro, and sections answer the same query.
- Title/H1: clear, specific, and includes the main keyword naturally.
- First 100 words: main keyword and value proposition appear early.
- Heading structure: at least 3 useful subheadings; H2s are descriptive, specific, and may be longer when that helps include keywords naturally.
- Keyword distribution: main and supporting keywords appear naturally without repetition.
- Content depth: the article gives practical details, examples, steps, or comparison criteria.
- FAQ: at least 3 concise questions that match likely search follow-ups.
- SEO meta pack: SEO Title, Excerpt, and Meta Description are within limits, related to the content, attractive, and not generic.
- Image SEO: suggest relevant image types and alt text using natural keywords.
- Trust: add authorial clarity, limitations, prerequisites, or verification notes when relevant.
- Risk: flag unsupported data, vague claims, fake citations, and exaggerated marketing language.
- Humanization: after resolving audit findings, check voice consistency, sentence rhythm, repetitive templates, promotional tone, generic conclusions, and chatbot artifacts without changing verified meaning.

## SEO-Friendly Language

Write in a style that is clear to readers and easy for search engines to interpret:

- Put the main idea early in each section and paragraph.
- Use short and medium sentences most of the time, with occasional longer sentences for nuance.
- Keep transitions explicit: explain cause, contrast, condition, sequence, and result.
- Use natural variations of the main keyword instead of repeating the same phrase.
- Prefer specific verbs and nouns over vague intensifiers.
- Avoid empty openings such as "In today's fast-paced world" or "It is worth noting that."
- Keep paragraphs focused on one point; split paragraphs when the topic shifts.
- Use comparison language carefully: "better for," "more suitable when," "less ideal if," and "trade-off" are usually more accurate than absolute claims.
- Add brief context before examples so the example has SEO value, not just decorative detail.
- Preserve a neutral editorial tone; avoid hype, exaggerated certainty, and sales-heavy phrasing.

## Output Rules

- Output clean Markdown for articles and prompts.
- Use one H1, then H2/H3 headings.
- Keep natural paragraph spacing with blank lines between paragraphs.
- Add FAQ and Conclusion near the end.
- Add the SEO meta pack at the bottom with SEO Title, Excerpt, Meta Description, and Tags.
- Do not include extra commentary when the user asks for copy-ready output.

## File Output Rules

When producing a final article, save it as files instead of only returning chat text:

- Create a directory at `writer/output/<article-slug>/`.
- Derive `<article-slug>` from the article title: lowercase, ASCII when possible, hyphen-separated, no punctuation.
- Save the final article as `writer/output/<article-slug>/article.md`.
- Save any audit notes, if requested or useful, as `writer/output/<article-slug>/seo-audit.md`.
- Save generated image assets in the same article directory.
- Use image filenames such as `hero-16x9.png`, `section-01-16x9.png`, and `comparison-chart-16x9.png`.
- For R2 uploads and final public URLs, image object filenames should be SEO-friendly and topic-aware while containing only letters and numbers before the extension. Use the article keyword, image role, and subject when naming. Example: `Seedance 2.0 AI video hero` becomes `seedance20AiVideoHero.png`.
- Reference local images from `article.md` with relative Markdown paths, for example `![Alt text](./hero-16x9.png)`.
- Insert images into the article at contextually useful positions: hero after the H1 or intro, section images before the relevant section, and chart images next to the corresponding comparison/chart section.
- Treat local relative image references as the default final format.
- Check whether `writer/config/r2.config.json` exists before attempting an R2 upload. When it exists and is valid, upload generated images with `writer/scripts/upload-r2.mjs`; the script compresses PNG/JPEG/WebP images locally before upload, collects public URLs, and replaces matching local Markdown references.
- When `writer/config/r2.config.json` does not exist, do not request credentials, do not attempt a remote config lookup, and do not fail the article task. Keep references such as `![Alt text](./hero-16x9.png)`.
- Save upload results or URL mappings as `writer/output/<article-slug>/image-urls.json` when images are uploaded.
- If the user asks for the article content in chat as well, provide a short summary and file links, not a full duplicate unless explicitly requested.

## Image Generation Rules

For article images:

- Use Codex's built-in image generation capability to generate article images when available; do not substitute hand-drawn SVGs or placeholder images unless Codex image generation is unavailable.
- Generate every article image at a 16:9 aspect ratio.
- When Codex saves generated images outside the article folder, copy the generated PNG into `writer/output/<article-slug>/` and leave the original generated file in place.
- Generate images that match the article topic, search intent, and section context.
- Use 16:9 aspect ratio for all article images unless the user explicitly asks otherwise.
- Prefer a hero image plus 1 to 3 supporting images for comparison, tutorial, or review articles.
- Avoid generic stock-like visuals when the article needs model, tool, workflow, product, or comparison clarity.
- Do not create misleading product UI captures, fake UI claims, fake logos, or fabricated charts that look like measured data.
- For charts, use clearly labeled editorial comparison graphics based only on facts stated in the article.
- Provide concise alt text for every image using the image topic and natural keywords, not keyword stuffing.
- Store all generated images under `writer/output/<article-slug>/`.
- Insert each saved image into `article.md` using a relative Markdown path immediately near the section it supports.
- Verify generated image dimensions when possible; accepted dimensions must reduce to 16:9, such as `1600x900`, `1792x1024`, or another 16:9 equivalent.
- If `writer/config/r2.config.json` exists, upload final images with `node writer/scripts/upload-r2.mjs`, then use returned public URLs in `article.md`. A custom local config may be supplied explicitly with `--config <path>`.
- Before R2 upload, rely on `writer/scripts/upload-r2.mjs` to create a local compressed upload copy by default. It uses high-quality WebP compression (`--compressionQuality 88`) for PNG/JPEG/WebP inputs, writes a sibling `*-r2.webp` file, uploads the compressed copy only when it is meaningfully smaller, and keeps the original generated image for backup.
- Use `--noCompress` only when the user explicitly asks to upload the original file. Use `--compressionQuality 90` or higher when the image has fine UI details or text-like labels that must remain extra crisp.
- Do not search for or download remote R2 credentials. This skill supports only a local ignored config file or a local path explicitly passed with `--config`.
- R2 image keys should use the configured blog directory and date path: `blog/yyyy/mm/dd/<filename>` by default. Override with `blogDirectory`, `--blogDir`, `--date`, or `--key` only when the user asks for a different storage layout.
- R2 object filenames must be SEO-friendly, keyword-aware, and sanitized to alphanumeric-only basenames, preserving a normal extension such as `.png`, `.jpg`, `.jpeg`, or `.webp`.
- When uploading images to R2, pass image metadata when available: `--seoName`, `--keyword`, `--topic`, and `--alt`. Save this metadata and the compression summary in `image-urls.json`.
- Final delivery should include Cloudflare R2 storage information for uploaded images: bucket, object key, date path, public URL, image alt text, and the compression result when available. Never include access keys or secrets.
- Never print R2 access keys or config contents. Use `writer/config/r2.config.example.json` as the tracked template and keep `writer/config/r2.config.json` local-only.
- If Codex image generation cannot save usable local files in the current environment, create an image generation plan with prompts and filenames, and clearly state that the image assets still need generation.

## Editorial Check

Before finalizing, check:

- The article answers the search intent promised by the title.
- The first 100 words make the topic and value clear.
- The title includes the main keyword or a close grammatical variant without sounding stuffed.
- H2 headings are specific, not generic, and include keywords or close variants where natural.
- Keywords read naturally.
- No unsupported data, fake attribution, or exaggerated claims appear.
- FAQ answers are concise and not repetitive.
- SEO Title, Excerpt, and Meta Description meet length limits.
- Audit findings have been resolved or explicitly marked as remaining risks.
- Fact-check findings have been resolved, softened, cited, or removed.
- The post-audit humanization pass is complete and any remaining mechanical patterns have been revised without inventing experience or changing meaning.
- Claims, certainty, keywords, metadata, citations, code, URLs, image paths, and CTAs changed during humanization have been rechecked.
- If user-provided UI reference images guided the article, published copy describes the interface directly and never mentions the reference format.
- Sentence flow uses varied length, clear transitions, and natural keyword phrasing.
- `article.md` and related images are saved in the expected `writer/output/<article-slug>/` directory.
- Codex-generated image assets are inserted into `article.md` with relative Markdown paths.
- If local R2 configuration is absent, `article.md` still works with local relative image paths and the task is complete.
- If R2 upload was used, `article.md` uses public R2 image URLs and the URL mapping is saved locally.
