---
name: marty-spits-hot-fire
description: "Create lyrics from a markdown source file containing reviews, product details, or Wikipedia article details using lyric-writer, pronunciation-specialist, lyric-reviewer, and album-art-director skills. Ask one question at a time after the file is known: source type, then genre, then title before lyric creation. Suggest 3 title options when none is given, preserve any user-provided title exactly, save lyrics to markdown file with title as filename (underscores for spaces), and append song tags plus source tags at the bottom. Use the exact user title verbatim; do not invent a new title. After lyrics and QC are complete, derive a generic/ChatGPT album art prompt from the finished lyrics only. Prefer source files that contain full review text, full product details, or full article text, and preserve that text verbatim for downstream lyric writing. Triggers: create lyrics from source, make song from text, write lyrics from markdown, product details to lyrics, wikipedia article to lyrics"
risk: low
source: community
date_added: "2026-04-12"
---

# Marty Spits Hot Fire

> Generate lyrics from a source markdown file using professional lyric writing tools.

---

## When to Use

This skill is applicable when the user requests:

- Creating lyrics from a source text/markdown file
- Turning review text into lyrics
- Turning product details into lyrics
- Turning Wikipedia article details into lyrics
- "Write lyrics from [source file]"
- "Make a song from this text"
- "Create lyrics using my notes"
- Any variation of turning written content into song lyrics

**Trigger phrases:**

- "create lyrics from source"
- "make song from text"
- "write lyrics from markdown"
- "marty spits hot fire"
- "turn text into lyrics"
- "turn product details into lyrics"
- "turn wikipedia article into lyrics"
- "wikipedia article to lyrics"

---

## Required Skills

- **lyric-writer** is mandatory and must be invoked before saving.
- Do not bypass lyric-writer or generate lyrics directly.

---

## Question Pacing

- Ask exactly one question per turn.
- Never combine source file, source type, genre, or title into a single prompt.
- Wait for the user's answer before asking the next question.

---

## Workflow

```
Step 1: Ask for source markdown file
    ↓
Step 2: Ask what kind of data the file contains (review, product details, or Wikipedia article)
    ↓
Step 3: Ask for genre (with suggestions)
    ↓
Step 4: Ask for title in a separate turn after genre selection
    ↓
Step 5: Read source file
    ↓
Step 6: If no title was provided, suggest 3 based on the selected data type and source content, then finalize the choice
    ↓
Step 7: Use lyric-writer to create initial lyrics
    ↓
Step 8: Run pronunciation-specialist to resolve phonetic risks
    ↓
Step 9: Run lyric-reviewer to verify structure, pronunciation, and pacing
    ↓
Step 10: Use the finished lyrics to draft a generic/ChatGPT album art prompt
    ↓
Step 11: Save to markdown file with title as filename, song tags, and source tags at bottom
```

## Title Lock

- If the user provides a title, treat it as canonical.
- Use the user title verbatim.
- Do not generate alternate titles.
- Do not rename, improve, or "clean up" the title.
- Use the exact title in the filename, H1, metadata, and any prompt passed to another downstream model.
- If a downstream model suggests a different title, ignore it unless the user explicitly asks for a change.

---

## Step 1: Request Source File

Ask the user:

> What markdown file should I use as the source for the lyrics?

If they provide a file path, validate it exists. If not, ask again.

---

## Step 2: Identify the Source Data Type

After the file path is known, ask:

> Does this file contain a review, product details, or a Wikipedia article?

Use exactly one of these options unless the file clearly mixes both:

- Review
- Product Details
- Wikipedia Article

If the file mixes both, ask which one should be treated as the primary source.

---

## Step 3: Genre Selection

Present genre options and ask for selection:

**Recommended genres for source-based lyrics:**

1. Folk/Acoustic (Recommended) - Great for storytelling, spoken word sources
2. Hip-Hop/Rap - Good for dense text, lists, rants
3. Spoken Word - Natural fit for prose sources
4. Alternative/Indie - Versatile for various source materials
5. Custom - Specify your own genre

Use the `question` tool to get their choice.

---

## Step 4: Ask for Title in a Separate Turn After Genre Selection

Ask the user for the song title in a separate message after the genre is confirmed.

- If the user provides a title, treat it as canonical.
- Use the user title verbatim.
- Do not generate alternate titles.
- Do not rename, improve, or "clean up" the title.
- Use the exact title in the filename, H1, metadata, and any prompt passed to another downstream model.
- This title prompt happens every time, with no exceptions.
- Do not ask the title together with genre or any other question.

If the user does not provide a title, continue after reading the source and suggest **3** options based on the selected data type and source content:

- For reviews: extract key themes, phrases, or emotional angles from the review text
- For product details: pull out standout features, specs, use cases, or product imagery
- For Wikipedia articles: pull out the topic, central conflict, chronology, names, places, vivid facts, and recurring article language
- Create compelling, song-appropriate titles
- Keep each under 60 characters for good song titles
- Present exactly 3 options for the user to choose from

Use `question` tool for title selection if providing options.

---

## Step 5: Read Source File

Use the `read` tool to extract content from the provided markdown file. Preserve full review text blocks, full product detail blocks, or full article text blocks verbatim; do not trim them down to short snippets when the source already contains the complete text.

---

## Step 6: Initial Lyric Creation

Call the lyric-writer skill with the source content:

```
lyric-writer: [source content] [genre: selected genre]
```

When the source type is Review, prioritize the full review text sections over any summaries or metadata. Keep the original wording intact for lyric adaptation.

When the source type is Product Details, prioritize the product description, feature bullets, spec tables, warnings, and use-case language over marketing fluff. Keep the original wording intact for lyric adaptation and do not invent claims not present in the source.

When the source type is Wikipedia Article, prioritize the article title, lead summary, infobox facts, chronology, section headings, key entities, and vivid article phrasing. Keep factual claims grounded in the source, preserve notable wording where useful, and do not invent historical, biographical, scientific, or cultural details not present in the article.

If the source came from Marty Has an Idea, use the extracted review sections as the review path.
If the source came from Marty Has an Idea in Wikipedia Article mode, use the lead summary, infobox facts, article sections, and article text as the article path.

Then immediately run pronunciation-specialist and lyric-reviewer before saving. Do not skip QC, even if the draft looks complete. The lyric-writer skill is mandatory; never generate lyrics without invoking it.

This will:

- Apply professional prosody and rhyme craft
- Follow quality checks (13-point system)
- Create structured lyrics (verses, chorus, bridge)
- Resolve pronunciation risks via pronunciation-specialist
- Verify the final lyrics via lyric-reviewer
- Show refinement passes
- Generate Suno style prompt

---

## Step 7: Draft Album Art Direction

Only draft album art after the final lyrics have been generated and pronunciation-specialist plus lyric-reviewer have completed. Do not ask which AI art platform the user uses.

Use the finished lyrics as the primary inspiration for the visual direction. The source text may provide factual context, but the album art concept must be derived from the song's lyrical imagery, mood, title, genre, and recurring motifs rather than from the raw product/review details alone.

Target only a generic/ChatGPT image prompt style. If using album-art-director principles, apply only its composition, thumbnail-safety, and visual-clarity guidance; do not follow its platform-selection workflow.

Capture:

- A 2-3 sentence concept description
- The AI art platform as `Generic / ChatGPT`
- A conversational prompt written for ChatGPT-style image generation
- No negative prompt unless the user explicitly asks for one later
- Square 1:1, thumbnail-safe, 3000x3000px minimum specs

Keep the direction focused, low-clutter, and easy to read at small sizes.

---

## Step 8: Save Output

Create a markdown file with:

- Filename: [sanitized_title].md (spaces → underscores)
- Location: `/home/tully/Sync/marty/`
- Title must match the user-provided title exactly when one exists.
- Add a `## Tags` section at the bottom with 5-8 relevant hashtags for the song, written comma-separated on a single line.
- Add a `## Source Tags` section after `## Tags` with 5-8 relevant hashtags describing the original product/source item or Wikipedia article topic, written comma-separated on a single line.
- Tags must describe the song, source material, product, mood, genre, or lyrical themes. Do not include workflow, tool, model, platform, or generation tags such as `#suno`, `#ai`, `#chatgpt`, `#generated`, or skill names.
- Source tags must come from visible source facts such as product name, brand, category, material, size/count, retailer, primary use case, Wikipedia article title, article category, people, places, dates, events, works, organizations, or concepts. Do not invent claims.

File structure:

```markdown
# [Song Title]

**Genre:** [Selected Genre]
**Source:** [Source File Path]
**Source Type:** [Review / Product Details / Wikipedia Article]
**Created:** [Timestamp]

## Lyrics

[Final lyrics from lyric-writer]

## Suno Style Prompt

[Style prompt from lyric-writer]

## Album Art

**Platform:** Generic / ChatGPT
**Concept:** [2-3 sentence visual direction derived from the finished lyrics]
**Prompt:** [Conversational ChatGPT-style image prompt inspired by the lyrics]
**Negative Prompt:** Not included by default
**Specs:** Square 1:1, thumbnail-safe, 3000x3000px minimum

## Source Text

[Full source text or full review/product detail/article text from the markdown file, preserved verbatim when available]

---

_Generated by Marty Spits Hot Fire skill_

## Tags

#tag1, #tag2, #tag3, #tag4, #tag5

## Source Tags

#producttag1, #producttag2, #producttag3, #producttag4, #producttag5
```

---

## Quality Assurance

The process ensures:

1. Professional lyric structure (verse/chorus contrast)
2. Strong prosody for Suno generation
3. Show-don't-tell storytelling
4. No lazy rhymes or forced phrasing
5. Consistent POV and tense
6. Appropriate section lengths for genre
7. Title placement in chorus (first or last line)
8. Hook/worthy title emphasis
9. Pronunciation-specialist and lyric-reviewer both completed; no unresolved homographs or QC gaps.
10. Source type was prompted immediately after file selection, and title was prompted immediately after genre selection, with 3 suggestions when needed.
11. Album art prompt is created only after lyrics and QC are complete, uses the finished lyrics as inspiration, and targets `Generic / ChatGPT` only.
12. Song tags and source tags are both included at the bottom, with source tags grounded in visible source facts and no workflow/tool/platform tags.

---

## Example Output Structure

After completing the task, output:

```
Done. File saved to: `/home/tully/Sync/marty/[song_title].md`

Summary:
- Source: [filename]
- Source type: [review/product details/Wikipedia article]
- Genre: [selected]
- Title: [chosen title]
- Title exact match: [yes/no]
- Order: title, lyrics, prompt, album art, source text, song tags, source tags
- Sections: [verse/chorus/bridge count]
- Tags: [comma-separated list of relevant hashtags]
- Source tags: [comma-separated list of product/article/source hashtags]
```

---

## When to Use

This skill is applicable to execute the workflow or actions described in the overview.
