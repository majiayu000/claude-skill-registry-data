---
name: webnovel-hot-memes
description: "Use when male Chinese web novel writing or 男频小说写作 needs contemporary Chinese 热梗, 网络流行语, 轻笑话, 网络热门事件模板, 网络热门人物口头禅, 知名人物事件的安全化改写或模仿, 弹幕, 评论区, 角色对白, 短视频文案, Fanqie male-rank market radar, or work-study notes on writing style, characters, background, outline, and themes for AI-assisted fiction writing."
---

# Novel Hot Memes

## Overview

Use this skill to adapt Chinese internet hot memes, light jokes, virtualized web-event patterns, public-personality catchphrase energy, platform voice, and reusable male-channel craft notes into fiction without breaking character voice, genre tone, or scene logic. Treat these references as social texture and craft memory: use them to shape dialogue, danmu, comment sections, forum posts, short-video scripts, inner monologue, light comedy beats, character pressure, worldbuilding rhythm, and theme echoes.

## Workflow

1. Identify the scene surface: character dialogue, group chat, danmu, comment section, platform post, chapter title, or narrator voice.
2. Identify constraints: genre, era, character age, education, region, platform, emotional intensity, and whether the text should feel current or timeless.
3. Load only the needed reference:
   - Broad lookup: `references/hot-memes-2026.md`
   - Category and usage tone: `references/hot-meme-categories.md`
   - Platform-specific tone: `references/platform-scenes.md`
   - Fiction adaptation rules: `references/novel-usage-guide.md`
   - Web-event adaptation and risk boundaries: `references/web-event-adaptation.md`
   - New meme intake: `references/evolving-hot-memes.md`
   - Shared platform voice: `references/shared/platform-voice-shared.md`
   - Male market style: `references/male-market-style-bible.md`
   - Male craft foundation: `references/male-craft-foundation/`
4. Choose a meme intensity:
   - Low: one softened phrase or paraphrase.
   - Medium: direct meme in dialogue/comment/danmu.
   - High: dense comment-section, livestream, parody, or comedic pile-up.
5. Rewrite for character fit. Preserve the character's vocabulary and relationship dynamics before preserving the exact meme wording.
6. If the user asks for latest/current hot memes, verify with fresh sources before updating this skill because the bundled 2026 list is a dated snapshot.

## Public Package References

This open-source package keeps reusable craft guidance and excludes source-limited work-study batches, monthly rank snapshots, local source cards, and refresh scripts that depend on private files. Use these included references instead:

- `references/hot-memes-2026.md` for the dated meme snapshot.
- `references/hot-meme-categories.md` for category and usage tone.
- `references/platform-scenes.md` for platform-specific scene surfaces.
- `references/novel-usage-guide.md` for fiction adaptation rules.
- `references/web-event-adaptation.md` for event-template safety boundaries.
- `references/evolving-hot-memes.md` for newly observed meme intake.
- `references/shared/platform-voice-shared.md` for common platform voice.
- `references/male-market-style-bible.md` and `references/male-craft-foundation/` for reusable male-channel craft patterns.

## Writing Rules

- Prefer "meme-compatible situations" over random insertion: proof-demanding scenes can use `我要验牌`; absurd reversals can use `啊？`; workplace friction can use `班味` or `真没空陪你闹了`.
- In fantasy, xianxia, historical, or solemn scenes, use memes through modern interfaces, transmigrator POV, system notices, forums, audience comments, or deliberately comic contrast.
- Do not use meme slang as exposition filler. If a line explains worldbuilding, keep it clear; add meme voice around the reaction, not inside the rule itself.
- A single book should use the same recognizable meme phrase, joke pattern, or web-event template at most twice by default. Space repeated uses far apart, preferably across different chapters or plot units. Avoid repeating the same meme in adjacent paragraphs, adjacent scenes, or adjacent chapters unless the repetition itself has a clear story function.
- If a meme, joke, or event template has already been used twice in the book, paraphrase it into plain character voice, choose a different reaction, or remove it. Do not disguise unlimited reuse by making tiny wording changes.
- Public-personality catchphrases and variety-show lines may be used directly when they are short, public, non-defamatory, and fit the scene surface. Keep direct catchphrase use sparse and count it under the book-level reuse limit. Avoid turning one fictional character into a near-duplicate of a real creator by combining the real name, persona, catchphrase, region-coded delivery, and incident context together.
- For recent short-video events or creator catchphrases, verify public facts if recency matters. Real events may be imitated as plot/event templates, but adapt them into the fictional world and do not invent harmful claims about real people.
- Real hot events and public-figure incidents may be imitated for structure, rhythm, public reaction, and comedy mechanics. Use real names only for neutral factual mention or clearly fictional commentary when the user asks for it; otherwise prefer fictional names and settings.
- Do not make jokes from disasters, deaths, victims, illness, public-safety incidents, vulnerable groups, or ordinary people's fear. Avoid real-world insinuations that could read as rumor, defamation, political provocation, or harassment.
- Keep dated memes out of long-lived core lore unless the user wants a specifically 2026-flavored work.
- Preserve copyright hygiene: use the reference summaries and examples as writing aids; do not copy protected novel text into outputs.

## Updating the Meme Base

Use `scripts/append_hot_meme.py` to append newly observed hot memes to `references/evolving-hot-memes.md`.

Required fields:

```text
date, meme, platform, source, meaning, usage, heat, include
```

Allowed heat values: `A`, `B`, `C`.

Use `include` as `是` or `否` to mark whether the meme should later be promoted into the main table.

## Updating Public References

Use `scripts/append_hot_meme.py` to append newly observed hot memes to `references/evolving-hot-memes.md`. Work-study refresh scripts and source-limited batches are intentionally excluded from this public package.

## Common Mistakes

- Overusing fresh slang in every character voice; it makes characters sound identical.
- Repeating the same meme, joke structure, or event template across a book until it becomes noise.
- Using platform-specific expressions outside their natural surface, such as Xiaohongshu lifestyle terms in a battlefield narration.
- Directly importing real public figures, real organizations, or identifiable controversy details into fiction when a fictionalized pattern would work.
- Treating the 2026 snapshot as always current; check live sources when recency matters.
- Adding new memes without date, platform, source, and heat level; this prevents the skill from evolving cleanly.
- Treating work-study notes as a source for imitation or text reuse; use them only for structural, thematic, and stylistic learning.
