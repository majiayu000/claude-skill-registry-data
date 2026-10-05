---
name: news-article-writer
description: "Write a hard news article from provided facts using the inverted pyramid structure — most important information first, supporting detail in descending order of importance, so the article can be cut from the bottom at any point."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.83
tags: [journalism, news, writing, hard-news, inverted-pyramid, articles]
---
# News Article Writer

## What This Skill Does
Write a hard news article from provided facts using the inverted pyramid structure — most important information first, supporting detail in descending order of importance, so the article can be cut from the bottom at any point.

## When To Use This Skill
- You need to convert a press release or wire copy into an original news article
- You are writing up facts from a press conference, official announcement, or event
- You have notes and quotes from a breaking story and need a first publishable draft quickly
- You are adapting a longer report, inquiry, or study into a concise news format

## What You Need To Provide
**Required:** The core facts (who, what, when, where, why/how); any direct quotes from named sources with their titles.

**Optional:** Word count target (default 300–500 words); publication type (broadsheet, tabloid, regional, digital); any background context to include; whether a standfirst or subheading is needed.

## How the Assistant Approaches This
1. Identifies the single most newsworthy fact — the "so what?" that makes this story worth publishing today
2. Writes a summary lede (25–35 words) that answers the key question and leads with the most important element, not the background
3. Structures the article in strict inverted pyramid order: paragraph 2 expands on the lede with the next most important detail; paragraph 3 provides context or a key quote; remaining paragraphs add background and secondary detail in descending importance
4. Applies AP-style news conventions: past tense for events, present tense for ongoing situations, attribution before the quote on first mention, full name and title on first reference

## Output Format
Inverted pyramid news article. Lede: 25–35 words. Total: 300–500 words (or specified target). Paragraphs: 1–3 sentences each. Quotes attributed with "said [Full Name], [title]" format on first mention, "[Surname] said" on subsequent mentions. No editorialising or opinion. Article ends with the least essential background detail — the material most likely to be cut by a subeditor.

## Quality Criteria
- [ ] Lede contains the single most newsworthy fact, written in 25–35 words
- [ ] The article can be cut at any paragraph break and still make complete sense
- [ ] Every fact was provided by the user — nothing invented or assumed
- [ ] Quotes are attributed clearly with name and title
- [ ] No editorialising, opinion, or emotive language injected by the assistant
- [ ] Follows AP-style news conventions (past tense for completed events, attribution format)

## Example

### Input
Facts: City fire department responded to a warehouse fire at approximately 3am on Tuesday. Two firefighters were treated for smoke inhalation at the scene and released. The building had been fully evacuated by the time crews arrived — it was unoccupied at that hour. The cause is under investigation. The warehouse stored commercial furniture awaiting distribution. The building is owned by a logistics company and is located in the city's industrial district.

Quote from the fire chief: "The response time was under four minutes. No civilians were at risk at any point during the incident."

Target: 350 words, regional newspaper.

### Output

Two firefighters were treated for smoke inhalation after a blaze broke out at a commercial warehouse in the city's industrial district early Tuesday, though no other injuries were reported.

Fire crews arrived at the scene at around 3am after receiving reports of a fire at the furniture storage facility. The building was unoccupied at the time and had been evacuated before crews arrived, said Fire Chief Marcus Delaney.

"The response time was under four minutes," Delaney said. "No civilians were at risk at any point during the incident."

Both firefighters were assessed at the scene and released without requiring hospital treatment. No further casualties were reported.

The warehouse, owned by a regional logistics company, stores commercial furniture awaiting distribution to retailers. The building is located in the industrial district, an area that houses several large storage and manufacturing facilities.

The cause of the fire remains under investigation. Fire department investigators were expected to begin a formal assessment of the site once the structure was confirmed safe to enter, according to a spokesperson for the department.

The logistics company had not responded to a request for comment at the time of publication. It is not known whether any stock was damaged or lost in the incident.

The city fire department said the blaze was brought under control within approximately 45 minutes of the first crews arriving on scene. No neighbouring properties were affected.

## Known Limitations
- Cannot assess the relative newsworthiness of facts without knowing the local context — what leads in a national newspaper may be buried in a regional one; the journalist should specify where in the article the most locally significant element should appear
- Does not fact-check any of the provided information; it reproduces what the user supplies
- Produces a single-source article structure — stories requiring multiple attributed sources and conflicting accounts need a more complex brief and a longer word count
- AP-style is the default; if the publication uses a different style guide (Guardian, BBC), specify this and provide key style rules in the brief

## Related Skills
- [lede-writer](../lede-writer/SKILL.md)
- [headline-writer](../headline-writer/SKILL.md)
- [feature-article-writer](../feature-article-writer/SKILL.md)
