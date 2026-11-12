---
name: skill-authoring
description: The standard for writing new skills for the AI Edit Video system - file structure, frontmatter, tone of voice, and how to accumulate production lessons into skills. Read when the user asks to create a new skill (via chat or from the Skills page in the web UI) or when updating a skill after finishing a video.
---

# Skill Authoring - writing skills the right way

Skills are where production know-how accumulates. A good skill makes the next video automatically better than the last one without having to repeat anything in chat.

## Required structure

```
.claude/skills/<name-kebab-case>/
└── SKILL.md
```

```markdown
---
name: <matches the folder name, kebab-case>
description: <1-2 sentences: what the skill does + WHEN to use it. Claude decides whether to load the skill from this line alone - be specific, include keywords>
---

# Title

<skill body>
```

## Writing rules

1. **The description decides everything.** Claude only sees the description when choosing a skill - it must spell out the trigger situation: "Read when...", "Use when the user provides...". A vague description = a skill that never gets used.
2. **Write for the next use, not as a souvenir.** Every section must answer "what do I do differently next time". Do not transcribe debugging history - keep only the conclusion + how to apply it.
3. **Every fix needs its recognition condition.** The standard template for a lesson:
   - **Symptom:** Vietnamese gradient text loses its diacritics on the reveal frame
   - **Cause:** `background-clip: text` clips the diacritics that sit outside the line-box
   - **Fix:** add enough `padding-top` + `line-height` to contain the diacritics, then check the first/last frame of the reveal
4. **Specific beats exhaustive.** A runnable command > a general description. Concrete numbers (CRF 28, volume 0.3, stroke 1.5px) > adjectives ("appropriate", "moderate").
5. **Write skills in English; keep code/commands/technical names as-is.** Do not translate technical terms (frame, render, timeline...). Vietnamese strings that are literal data (sample captions, UI labels, on-screen text) stay verbatim.
6. **One skill, one topic.** Split a skill once it grows past ~200 lines. Reference other skills by name (`see the remotion-assemble skill`) instead of copying content across files.

## When to CREATE a new skill vs UPDATE an existing one

| Situation | What to do |
|---|---|
| A new repeatable video format (e.g. product comparison video) | Create a new skill, cloned from the closest existing one |
| Fixing a bug in a workflow that already has a skill | Update that skill, in its "Known issues" section |
| A new aesthetic/brand rule | Update `webui-design` (UI) or the relevant video format skill (video) |
| Knowledge that only applies to one specific video | DO NOT put it in a skill - write it in that project's NOTES.md |

## Creating a skill from the web UI

When the user creates a skill through the Skills page (describing it in their own words, often in Vietnamese):
1. Read this skill plus the closest existing skill of the same kind as a template.
2. Write a full `SKILL.md` in English, with complete frontmatter, following the rules above.
3. If the skill relates to Vietnamese-language video: inherit the verified fixes (Vietnamese diacritics, ffmpeg PATH) by reference, do not copy them.
4. Return it to the UI as a draft for the user to approve before writing the file.

## After every finished video

Ask yourself: is there a new symptom -> cause -> fix? Was there a step done manually more than twice (the sign it should become a skill)? If so, update the skill in that same session - do not defer it to the next one.
