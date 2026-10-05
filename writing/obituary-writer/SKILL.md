---
name: obituary-writer
description: "Transforms a set of facts about a deceased person into a structured, dignified obituary suitable for publication in a newspaper, magazine, or website."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [obituary, death-notices, tribute, biography, news-writing]
---
# Obituary Writer

## What This Skill Does
Transforms a set of facts about a deceased person into a structured, dignified obituary suitable for publication in a newspaper, magazine, or website.

## When To Use This Skill
- You have confirmed biographical facts and need to shape them into a publishable obituary quickly
- A subject has died unexpectedly and you are working to deadline with notes gathered under pressure
- You need a draft to hand to a senior editor for final review within the hour
- You are writing an obituary for a private individual (not a celebrity) and want a professional framework to follow

## What You Need To Provide
**Required:**
- Full name of the deceased
- Age at death and date of death
- Cause of death (or note if not being disclosed)
- Career summary: main profession, significant roles or achievements
- Surviving family members (names and relationships)
- At least one direct quote or anecdote from someone who knew the subject

**Optional:**
- Place of birth and early life details
- Education
- Awards, honours, or notable recognition received
- A second quote or anecdote for texture
- Funeral or memorial service details
- Preferred pronouns and name the subject went by in life
- Publication's house style (broadsheet, tabloid, wire service)

## How the Assistant Approaches This
1. Opens with a lede that names the subject, identifies them by their defining role or achievement, states the age and date of death, and — if known — the cause. This sentence must be self-contained: a reader who reads nothing else will have the essential facts.
2. Develops the career arc in chronological or thematic order, selecting the two or three accomplishments most meaningful to the subject's field, not an exhaustive CV.
3. Places at least one human detail — a quote, a characteristic habit, a moment that reveals character — before the piece becomes too formal. Obituaries that read only as resumes fail the subject.
4. Closes with survivors, any service details, and a final sentence that is understated rather than sentimental.

## Output Format
- Length: 250–500 words for a standard newspaper obituary; up to 800 words for a feature-length appreciation
- Structure: lede paragraph → career body → human texture (anecdote or quote) → survivors → service details (if provided)
- Tone: dignified, factual, warm without being maudlin; past tense throughout
- No subheadings; continuous prose
- No invented facts: if information is missing, the assistant will flag it with a bracketed note (e.g., `[cause of death not provided — confirm before publication]`) rather than guess

## Quality Criteria
- [ ] Lede names the person, their defining role, age, date of death, and cause (or clearly notes it is not disclosed)
- [ ] Career body covers meaningful achievements without reading like a bullet-point resume
- [ ] At least one quote or anecdote gives the subject a human dimension
- [ ] All survivors listed with correct relationship labels
- [ ] No invented facts; missing information flagged in brackets
- [ ] Tone is consistent: professional and respectful, not sentimental or clinical
- [ ] Word count falls within the requested range

## Example

### Input
Name: Margaret Osei-Bonsu
Age: 74, died 14 March 2026
Cause of death: Complications following a stroke
Career: Environmental lawyer; founded the West African Environmental Advocacy Coalition (WAEAC) in 1998; argued landmark cases that led to two national pollution regulations; taught law at the University of Cape Coast for 22 years; awarded the African Bar Association Environmental Prize in 2011
Family: Survived by husband Kweku Osei-Bonsu; daughters Abena and Nana Ama; four grandchildren
Quote: "She never let you believe the law was an abstraction. She would say: 'Someone is drinking that water. Start there.'" — former student Josephine Armah
Service details: A public memorial will be held at the University of Cape Coast on 28 March

### Output
Margaret Osei-Bonsu, the environmental lawyer whose advocacy shaped pollution regulations across West Africa, died on 14 March 2026 following complications from a stroke. She was 74.

Over a career spanning four decades, Osei-Bonsu became one of the most consequential environmental litigators on the continent. In 1998 she founded the West African Environmental Advocacy Coalition, a body that went on to argue the cases behind two landmark national pollution regulations. The work was technical, protracted, and often thankless; she pursued it without interruption while also teaching law at the University of Cape Coast, where she remained on the faculty for 22 years.

The African Bar Association awarded her its Environmental Prize in 2011, though colleagues noted she was more pleased by her students' courtroom wins than by any honour she received herself.

Those students remember a teacher who insisted the law remain concrete. "She never let you believe the law was an abstraction," said Josephine Armah, who studied under Osei-Bonsu before building her own practice in environmental litigation. "She would say: 'Someone is drinking that water. Start there.'"

She is survived by her husband, Kweku Osei-Bonsu; daughters Abena and Nana Ama; and four grandchildren.

A public memorial will be held at the University of Cape Coast on 28 March.

## Known Limitations
- The assistant cannot verify facts. The user must confirm all dates, names, and claims before publication — errors in an obituary are among the most damaging a publication can make.
- Cause of death phrasing can be sensitive. The assistant will follow whatever phrasing the user provides; editorial decisions about disclosure remain with the journalist.
- The assistant will not write an obituary that speculates about character, relationships, or circumstances not supplied in the input. If a richer portrait is needed, more source material must be provided.
- For obituaries of public figures with contested legacies, the assistant defaults to factual reporting and will not adjudicate historical disputes without explicit instruction.

## Related Skills
- [profile-writer](../../../magazine-journalism/writing/profile-writer/SKILL.md)
- [interview-transcript-editor](../../../magazine-journalism/writing/interview-transcript-editor/SKILL.md)
