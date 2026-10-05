---
name: project-memory
description: "Generate a project-specific context file from a brief so an AI assistant remembers your editorial constraints, voice, audience, and quality bar across sessions."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.5
tags: [workflow, project-setup, context, memory, editorial-voice, session-management]
---

# Project Memory

## What This Skill Does
Generates a structured context file from a short project brief so that an AI assistant loads your editorial voice, audience, constraints, and quality bar at the start of every session — without you re-explaining the project each time.

## When To Use This Skill
- At the start of a new editorial project (magazine, podcast series, documentary, newsletter, YouTube channel) when you want every future AI session to respect the same voice, rules, and standards
- When you have been re-explaining the same constraints — tone, audience, terminology, house rules — at the beginning of each chat session and want to stop
- When a project has multiple contributors or freelancers who all need to work within the same editorial frame, and you want a single reference document the assistant can load
- After a significant editorial pivot (new audience, rebrand, format change) when the old context file no longer reflects how the project works
- When onboarding a new editor, writer, or producer onto a project and you want them to see, in one place, how the project thinks and talks
- When you notice that AI-generated drafts for your project are inconsistent — some match the voice, some do not — and you want to eliminate that variance by giving the assistant a stable reference point

## What You Need To Provide

**Required:**
- A short project brief: what the project is, the format (magazine, podcast, newsletter, documentary series, YouTube channel, etc.), and what it covers
- Who the audience is — even a rough sketch helps ("urban professionals in their 30s who read on the train" is more useful than "general audience")
- The editorial voice and tone you want — either described in your own words or shown by example ("like the tone in this paragraph," or "think of how The Atlantic writes features, but shorter and funnier")

**Optional:**
- Specific do/don't rules ("never use the word 'content' to describe our journalism," "always capitalise Indigenous," "no listicles")
- Key terminology or a glossary — words the project uses in a specific way, or terms that must always appear in a particular form
- Recurring tasks you use AI for on this project (drafting headlines, editing transcripts, writing show notes, generating image prompts)
- Source and reference preferences (preferred citation format, trusted sources, sources to avoid)
- Quality benchmarks — published pieces, episodes, or issues that represent the standard you are aiming for
- Any legal or ethical constraints (anonymisation rules, embargo policies, advertising/editorial separation requirements)
- Format constraints — word counts, segment lengths, episode durations, or other hard limits the project works within
- Team structure notes — who signs off on what, how many writers contribute, whether the project has a single voice or multiple distinct voices within a shared framework

## How the Assistant Approaches This

1. **Reads the brief for structure.** Identifies the project type (magazine, podcast, newsletter, documentary, YouTube channel), format specifics (print or digital, audio or video, long-form or short), publication rhythm (weekly, monthly, seasonal), and subject territory. If the brief is thin on any of these four, asks one round of clarifying questions — never more than one round, and never more than five questions total. The goal is to establish enough context to write a file that a cold AI session can act on, not to conduct a full editorial consultation. If the brief already covers all four, the assistant proceeds without questions.

2. **Extracts the voice profile.** This is the most important step and the one most likely to determine whether the context file is useful or generic. Pulls the tone, register, vocabulary level, and narrative posture from whatever the user provided — their own description, a benchmark piece, or both. If the user supplied a benchmark publication or example text, analyses it for: sentence length distribution, use of contractions, formality markers, emotional register, use of first or second person, density of jargon, and paragraph rhythm. Translates all of this into concrete, reusable instructions — not descriptions of the voice ("warm and engaging") but operational parameters ("use contractions in features; average sentence length 15-20 words; avoid rhetorical questions; first person only in columns and editor's notes"). The distinction matters: a description tells the assistant how the voice feels; operational parameters tell it how to produce that feeling.

3. **Defines the audience in operational terms.** Converts the audience description into parameters an AI can act on. This means answering four questions:
   - What does the audience already know? (assumed knowledge — determines the jargon threshold)
   - What do they need explained? (context requirements — how much background to provide)
   - What do they care about? (editorial priorities — what makes a piece relevant to them)
   - How do they consume the content? (format constraints — reading on phones means shorter paragraphs; listening on commutes means signposted structure)

   The audience section should be specific enough that the assistant knows, for any given reference or term, whether to explain it, name-drop it, or skip it entirely. The best audience definitions include a calibration example: a reference the audience would recognise and one they would not. This gives the assistant a concrete threshold to work from.

4. **Builds the do/don't ruleset.** Organises all explicit rules the user provided into two testable lists: things the project always does, and things the project never does. Then infers additional rules from the voice profile and audience definition — for example, if the voice profile says "avoid jargon," the assistant might infer "do not use 'praxis,' 'liminal,' or 'discourse' outside direct quotes." Inferred rules are marked clearly with a comment or annotation so the user can approve, modify, or remove them before the file goes into production. The test for every rule: could an editor read a finished piece and objectively determine whether the rule was followed? If not, the rule is too vague and needs sharpening. "Write accessibly" fails this test. "Explain any term that would require a Google search for a university-educated reader outside the field" passes it.

5. **Structures the terminology section.** Collects any terms the user specified — house-style spellings, capitalisation preferences, banned words, field-specific vocabulary — and arranges them in a three-column table (Term, Usage, Notes). Adds a framework note at the bottom encouraging the user to extend the glossary over time, so the context file grows with the project rather than going stale after the first session. For projects with significant technical or domain-specific vocabulary, this section may be the longest in the file. Even for lighter projects, the glossary establishes a shared vocabulary that prevents drift — if the project calls its introductory paragraph a "standfirst" and not a "subheading," recording that in the glossary saves repeated corrections.

6. **Maps recurring tasks.** If the user listed tasks they regularly use AI for, writes a structured instruction block for each one. Each block specifies: what the task is, what inputs the assistant should expect, what the output should look like (format, length, tone), and any task-specific rules that override or supplement the general voice guidelines. Task blocks should be self-contained — a future session should be able to read just one block and produce the right output without cross-referencing other sections. If the user did not specify any recurring tasks, the assistant suggests three to five likely ones based on the project type — clearly marked as suggestions rather than mandates — so the user has a starting point to edit rather than a blank section to fill.

7. **Assembles the context file.** Writes the complete file in the structure described below, using plain language throughout. The file is addressed to the AI assistant that will read it at the start of future sessions. Every instruction is specific enough that a different AI instance — with no memory of this conversation — could follow it and produce work consistent with the project's standards. Includes HTML comments throughout explaining how to update each section as the project evolves. Closes with an empty update log so the user has a built-in mechanism for tracking editorial drift. Before delivering the file, the assistant reviews it against the quality criteria listed below — particularly the testability of every instruction and the clarity of the inferred-rule markings.

## Output Format
A single Markdown file (titled `CLAUDE.md` or whatever the user's system requires) structured in clearly labelled sections. The file is written in second person, addressed to the AI assistant that will read it. All instructions are concrete and testable — no vague directives like "be creative" or "maintain high quality." The tone of the file itself is direct and editorial: it reads like a briefing document from a senior editor, not like a technical specification or a marketing persona deck.

Length varies with the complexity of the project. A straightforward newsletter might produce a 100-line file. A magazine with multiple sections, format types, and a detailed house style might run 250-350 lines. The example below runs roughly 200 lines — a realistic middle-ground.

The file includes HTML comments (`<!-- -->`) at key points, explaining how to update each section as the project evolves. These comments are part of the deliverable — they turn the context file from a static snapshot into a living document that the user can maintain without needing to re-run this skill.

The structure adapts to the project type. A print magazine's context file will emphasise voice dimensions, format constraints, and terminology. A podcast's file will focus more on conversational register, segment structure, and the distinction between the host's voice and the show's brand voice. A documentary series will need sections on narrative arc, interview treatment, and the balance between narration and verité. The nine-section structure remains the same across all project types, but the depth and emphasis within each section shifts to match what matters most for the format.

One important constraint: the context file is designed to be read by an AI assistant, not by a human editor. While a human could read it and find it useful, its primary audience is the machine — and that shapes how instructions are written. Human style guides can rely on shared taste and editorial intuition ("you'll know it when you see it"). A context file cannot. Every instruction must be explicit enough to follow without editorial judgement, because the reader has none.

## Context File Structure
The generated file contains these sections, in this order. Each section has a specific purpose, and the assistant fills it with project-specific content drawn from the user's brief. The order is deliberate: the file opens with the broadest context (what the project is) and narrows progressively to operational detail (how specific tasks should be handled). An AI assistant reading the file from top to bottom absorbs the editorial identity before encountering the rules and tasks — which mirrors how a new editor would be onboarded to a publication.

Not every section will be equally long for every project. A podcast with a simple format might have a thin Terminology section but a detailed Recurring Tasks section. A literary magazine might have a long Voice and Tone section but few recurring tasks. The structure accommodates both — what matters is that every section is present, even if some are brief.

### 1. Project Overview
Three to five sentences. States what the project is, what format it takes, how often it publishes, and what territory it covers. Written so that an AI assistant reading this cold understands the editorial landscape immediately.

**Guidance:** Be specific about format and scope. "A monthly arts and culture magazine" is better than "a publication." "Covers visual art, architecture, design, film, and music — but not theatre or literary fiction" is better than "covers culture." Include the publication rhythm (weekly, biweekly, monthly, seasonal) and the primary distribution channel (print, web, email, audio, video). If the project has scope boundaries — topics it does not cover, formats it does not produce — state them here.

**Good:** "Foyer is a monthly arts and culture magazine covering visual art, architecture, design, film, and music. It does not cover theatre or literary fiction. Print-first, with a web edition. Ten issues per year."
**Bad:** "Foyer is an arts publication that covers culture."
**Also bad:** "Foyer is a dynamic new magazine at the intersection of art and culture." (Press-release language tells the assistant nothing operational.)

### 2. Audience
A paragraph defining who reads, watches, or listens — and what that means for the work. Covers: demographics (age range, professional context, location if relevant), assumed knowledge level, what they come to this project for, and how they typically encounter it (morning commute, weekend reading, background listening).

**Guidance:** The audience section is not a marketing persona. It is an operational definition that tells the assistant how to calibrate vocabulary, explanation depth, and cultural references. The most useful audience descriptions anchor on specific knowledge boundaries: "Assume the reader knows who Gerhard Richter is but would appreciate a one-sentence context line on Hilma af Klint" is more useful than "educated, culturally aware." Describe how the audience consumes the content — this affects paragraph length, sentence complexity, and structural signposting.

**Good:** "They read on commutes and lunch breaks, often on their phones. Assume they know who Ai Weiwei is but would appreciate a one-line reminder of why Vkhutemas matters."
**Bad:** "Our readers are smart, curious people who care about the arts." (This describes the audience's self-image, not their knowledge boundaries. It gives the assistant no basis for deciding what to explain.)
**Also good:** "Listeners are parents with young children who play the podcast during the school run. Episodes over 25 minutes lose them. Assume familiarity with mainstream parenting advice but not with child development research." (Concrete consumption context plus a knowledge boundary.)

### 3. Editorial Voice and Tone
The most detailed section. Defines the project's voice across five dimensions:

- **Register:** Where on the spectrum from academic to conversational. Not a single adjective ("warm") but a positioned description with boundaries on both sides ("informed but not scholarly; the voice of a well-read friend, not a professor and not a blogger").
- **Sentence style:** Average length, rhythm preferences, use of fragments, tolerance for long sentences. Quantify where possible: "average 15-20 words," "no sentence over 35 words."
- **Vocabulary level:** What words are welcome, what words are off-limits. This is about the jargon threshold — how specialised the vocabulary can get before the assistant should pause and explain.
- **Emotional temperature:** How much feeling the writing carries. Where enthusiasm is welcome and where it tips into promotion. Where scepticism is valued and where it turns cynical.
- **Narrative posture:** Point of view, use of "I" or "we," direct address to the reader. May vary by section or format within the project — if so, specify which posture applies where.

**Guidance:** Specificity here prevents voice drift across sessions. "Write naturally" tells the assistant nothing. "Use contractions, keep sentences under 25 words on average, avoid rhetorical questions, and never open a piece with a question" tells it everything. The most common failure mode in this section is vagueness disguised as style direction. Pressure-test each instruction: if two writers followed it, would they produce recognisably similar work? If not, it needs tightening.

When the user describes the voice with comparisons ("like The Atlantic but funnier"), the assistant should unpack that comparison into the five dimensions above. What, specifically, makes The Atlantic's voice what it is? Long sentences, third person, expert-to-expert register, low emotional temperature, high vocabulary level. What does "funnier" change? Probably the emotional temperature (warmer), possibly the register (slightly less formal), maybe the sentence style (shorter for comic timing). The context file should capture the unpacked version, not the shorthand — because the shorthand works only for people who already read The Atlantic.

If the project has multiple formats (features, columns, social posts, newsletters), each format may need its own voice parameters. The context file should define a base voice and then note how each format departs from it. For example: "Social posts use first person and direct address. The newsletter is warmer than print features and may use humour more freely. Reviews are the most opinionated format — the voice is still Foyer's, but the emotional temperature runs higher."

### 4. Do / Don't Rules
Two lists — one of explicit dos, one of explicit don'ts. Each rule is one sentence and testable against an output. Rules cover editorial policy, style conventions, ethical guardrails, and format requirements.

**Guidance:** Rules work best when they are observable. An editor should be able to read a finished piece and determine, for each rule, whether it was followed. "Do: Capitalise Indigenous when used as an adjective or noun referring to peoples" is testable. "Do: Write with integrity" is not.

Include both the rules the user stated explicitly and the ones inferred from the voice profile — marked differently (e.g., with a comment or italic annotation) so the user can review the inferences. Inferred rules are the assistant's best guesses based on the stated voice and audience; they need human approval before becoming permanent policy.

Group rules by type when the list exceeds ten items: style rules, editorial policy rules, format rules, ethical rules. This makes the list easier to scan and maintain.

**Good rule:** "Never open a feature with a rhetorical question." (Observable, testable, unambiguous.)
**Bad rule:** "Write engaging openings." (What does "engaging" mean? Two editors would disagree.)
**Good rule:** "Every feature must include at least one concrete detail the reader could not find on Wikipedia." (Testable against a specific source.)
**Bad rule:** "Include original reporting." (Too broad — does not specify what counts or how to verify.)

### 5. Key Terminology
A glossary table with three columns: Term, Usage, Notes. Contains words the project uses in a specific way, words that must be spelled or capitalised in a particular form, and words that are banned or restricted.

**Guidance:** Start with whatever the user provided, then add a framework note at the bottom: "Add new terms to this table as they arise during the project. Review quarterly." This keeps the context file alive rather than frozen at the moment of creation. For domain-heavy projects (medical journalism, architecture criticism, tech reporting), this section may grow to be the longest in the file — and that is fine. A precise glossary prevents more errors than any amount of voice guidance.

### 6. Recurring Tasks
A numbered list of tasks the user regularly asks the AI to perform on this project. Each task entry includes:
- A one-line description of the task
- The typical inputs the assistant should expect
- The expected output format (length, structure, tone)
- Any task-specific rules that override or supplement the general voice and tone

**Guidance:** Not every project has recurring tasks defined at the start. If the user did not specify any, include three to five likely tasks based on the project type — for a magazine: drafting headlines, editing interview transcripts, writing social teasers, generating image prompts, summarising research; for a podcast: writing show notes, drafting episode descriptions, preparing guest research briefs, writing ad-read scripts — and mark them as suggestions the user can keep, modify, or remove.

Each task block should be self-contained: a future AI session should be able to read just that block and know exactly what to produce, without needing to cross-reference other sections. However, all task blocks inherit the general voice and tone unless they explicitly override it.

### 7. Quality Bar
A short section that defines the minimum standard for work on this project. References a benchmark if the user provided one. States what "good enough to publish" means in concrete terms — not aspirational language, but a checklist the assistant can self-evaluate against before presenting output.

**Guidance:** The quality bar should be honest about the project's actual standards, not an idealised version. A daily news podcast has different quality requirements from a quarterly literary journal. A YouTube channel posting three times a week operates under different constraints from a monthly documentary series. Both are valid. The context file should reflect the real bar, not the aspirational one.

Frame criteria as pass/fail checks rather than quality scales. "Every claim is grounded in a concrete detail — a date, a place, a name" is a pass/fail check. "The writing should be high quality" is a quality scale that tells the assistant nothing actionable.

If the user provided a benchmark publication or piece, reference it here by name. The benchmark gives the quality bar a concrete anchor: instead of defining excellence in the abstract, the context file says "if this draft would not hold its own next to a piece from [benchmark], it needs more work." That comparison is more useful than any checklist — but include the checklist too, because the comparison requires editorial judgement while the checklist can be applied mechanically.

### 8. Sources and References
Defines how the project handles sourcing: preferred citation format (if any), trusted sources, sources to avoid or treat with caution, and any rules about attribution or linking.

**Guidance:** For journalism projects, this section is critical — it shapes how the assistant handles claims, quotes, and factual grounding. For creative projects (scripting, image prompting), it may be minimal. Either way, include it — even a single line ("No specific sourcing requirements for this project") prevents the assistant from inventing a policy or applying conventions from a different domain.

Organise sources into three tiers: trusted (use freely), caution (use with caveats), and avoid (do not cite unless the source itself is the story). This gives the assistant a clear decision framework when it encounters a reference it has not seen before.

For projects that handle sensitive material — investigative journalism, health reporting, legal affairs — this section should also address: anonymisation rules (when and how to protect sources), embargo policies (how to handle pre-release information), and the separation between editorial and commercial interests (whether advertiser-adjacent topics require disclosure or recusal). Even if the project is a lifestyle magazine with no investigative mandate, stating "no specific sensitivity constraints apply" is better than leaving the section silent — silence invites the assistant to make assumptions.

### 9. Update Log
An empty table with columns for Date, Section Changed, and What Changed. Placed at the end of the file so the user has a built-in mechanism for tracking how the context file evolves.

**Guidance:** Include a note: "Update this log whenever you change the context file. This helps you track editorial drift and understand why decisions were made." The log serves a dual purpose: it keeps the user honest about maintaining the file, and it creates a record that explains why the voice or rules shifted — useful when a new team member asks "why do we capitalise this word?"

Even small changes deserve a log entry. Adding a single term to the glossary, tweaking a word count limit, or removing an inferred rule — recording these prevents the context file from drifting silently. A file that changes without explanation eventually contradicts itself, because no one remembers why a rule was added or removed.

## Quality Criteria
- [ ] The generated context file is specific enough that two different AI sessions, both loading it, would produce work in the same voice and within the same constraints
- [ ] Every instruction in the file is concrete and testable — no vague directives like "be creative," "maintain quality," or "use good judgement"
- [ ] The voice and tone section translates the user's description (however informal) into precise, reusable parameters with measurable dimensions (sentence length, vocabulary level, emotional register)
- [ ] Inferred rules (those not explicitly stated by the user) are clearly marked as inferred so the user can accept, modify, or reject them before the file goes into production use
- [ ] The file reads as a briefing document from a senior editor — direct, clear, professional — not as a technical configuration file, a marketing persona deck, or a brand guidelines PDF
- [ ] The terminology glossary is structured for growth, with an explicit invitation to add terms over time, not frozen at the moment of creation
- [ ] The quality bar section reflects the project's actual standards, not an idealised aspiration, and frames criteria as pass/fail checks rather than subjective scales
- [ ] The complete file can be loaded by an AI assistant with no prior context about the project and followed without ambiguity — no instruction depends on knowledge not contained in the file itself

## Example

### Input

**Project brief:**
We are launching a monthly arts and culture magazine called *Foyer*. It covers visual art, architecture, design, film, and music — but not theatre or literary fiction (those are handled by a sister publication). Distribution is print-first with a web edition that publishes a subset of each issue's features plus web-exclusive shorter pieces. We publish ten issues per year (double issues in July/August and December/January).

**Audience:**
Urban professionals, 25-40. They visit galleries and go to gigs but do not work in the arts. They have degrees but not necessarily in the humanities. They want to understand what is happening and why it matters — not just what is new. They read on the train, in cafes, and on their phones during lunch. They subscribe because the magazine helps them feel informed without having to follow the art world full-time.

**Voice and tone:**
Curious but not breathless. Informed but not academic. We want the reader to feel like they are talking to a well-read friend who goes to a lot of exhibitions and has opinions — not a critic performing for other critics. Contractions are fine. Humour is welcome when it is earned but not forced. We never talk down to the reader and we never assume they already know the backstory. Think of a confident explainer piece in a good weekend supplement — not a review in an art journal.

**Rules:**
- Always use "artwork" (one word) not "art work" or "work of art"
- Capitalise art movements when used as proper nouns: Surrealism, Bauhaus, Art Deco. Lowercase when used as adjectives: surrealist, bauhaus-influenced
- Never describe an artwork as "stunning," "breathtaking," or "masterpiece" unless directly quoting someone
- Feature articles run 1,500-3,000 words. Web exclusives run 600-1,000 words.
- Every feature must include at least one concrete detail the reader could not find on Wikipedia
- No press-release language. If a sentence could appear in a gallery's promotional material, rewrite it.

**Recurring tasks:**
We use AI mostly for drafting headlines, writing standfirsts (the short intro paragraph below the headline), editing interview transcripts to readable Q&A format, and writing social media teasers for Instagram and Bluesky.

**Quality benchmark:**
The features in *Monocle* magazine and the culture writing in *The Guardian*'s Weekend section. We admire their ability to be accessible without being shallow.

### Output

```markdown
# Foyer — Project Context

<!-- This file is loaded at the start of every AI session for the Foyer project.
     It defines the editorial voice, audience, rules, and quality bar.
     Update it as the project evolves — the Update Log at the bottom tracks changes.
     Sections marked with guidance comments explain how and when to revise. -->

## Project Overview

Foyer is a monthly arts and culture magazine covering visual art, architecture, design, film, and music. It does not cover theatre or literary fiction — those belong to a sister publication. The magazine is print-first, with a web edition that republishes selected features and runs shorter web-exclusive pieces. Foyer publishes ten issues per year, with double issues in July/August and December/January.

<!-- Update this section if the magazine adds new subject areas, changes its publication
     rhythm, or shifts its primary distribution channel. -->

## Audience

Foyer's readers are urban professionals aged 25-40. They visit galleries, attend concerts, and care about design, but they do not work in the arts professionally. Most hold degrees, though not necessarily in the humanities. They subscribe because Foyer helps them stay informed about the arts without requiring them to follow the art world full-time. They read on commutes, during lunch breaks, and in cafes — often on their phones.

Assume the reader knows who Ai Weiwei is but would appreciate a one-line reminder of why Vkhutemas matters. Explain institutional context — who funds a museum, why a biennial matters politically, what a residency programme is — rather than assuming it. Cultural references outside the arts (a film, a news event, a tech product) land well when they are current and genuinely clarifying, not when they are shoehorned in for relatability.

When in doubt about whether to explain a term or reference, explain it. The reader will forgive a sentence of context they did not need. They will not forgive being made to feel excluded.

**Knowledge calibration examples:**
- Knows: Ai Weiwei, Banksy, Frank Gehry, Dieter Rams, the Tate, MoMA, the Venice Biennale.
- Probably knows: Zaha Hadid, Rem Koolhaas, the Serpentine Gallery, Art Basel. Mention with light context.
- Likely does not know: Vkhutemas, Superstudio, the Sonsbeek exhibitions, Forensic Architecture as an art practice. Explain on first reference.

These calibration points should be updated as the readership evolves. Review annually.

<!-- Revisit this section annually or when readership data reveals a demographic shift.
     The knowledge-boundary examples (Ai Weiwei vs. Vkhutemas) should be updated
     as the audience's baseline familiarity evolves. -->

## Editorial Voice and Tone

### Register
Informed but not scholarly. The voice of a well-read friend who goes to a lot of exhibitions and has opinions — not a critic performing for other critics, and not a blogger reacting in real time. The closest published equivalents are Monocle's feature writing and the culture pages of The Guardian's Weekend section: accessible without being shallow, opinionated without being combative.

### Sentence Style
Mix short declarative sentences with occasional longer ones for rhythm. Fragments are acceptable for emphasis — sparingly. No sentence should exceed 35 words. Average sentence length should sit between 14 and 20 words. Vary paragraph length: a one-sentence paragraph is fine when it carries weight; a five-sentence paragraph is fine when the argument needs room. Avoid stacking three or more short sentences in a row — it reads as breathless rather than punchy.

### Vocabulary Level
Use precise terminology when it earns its place — "chiaroscuro" is fine in a painting piece if it says something "contrast" does not. But explain any term the reader would need to look up. No jargon for its own sake. No art-world insider shorthand ("the work interrogates," "a praxis of," "liminal space") unless you are quoting someone and the phrasing reveals something about them. If a technical term appears, it should be followed — within the same sentence or the next — by enough context that the reader absorbs its meaning without needing to pause.

### Emotional Temperature
Curious and warm. Enthusiasm is welcome — the magazine exists because the editors care about this material. But never gushing, never breathless. The difference: "This is the most compelling group show the gallery has staged in years, and it is worth the trip across town" is fine. "This absolutely unmissable exhibition will blow your mind" is not. Scepticism and wit are valued. Cynicism is not. The reader should finish a piece feeling more interested in the subject, not more impressed by the writer.

### Narrative Posture
Third person for features and profiles. First person is permitted in columns, editor's notes, and personal essays — but first person should feel earned, not reflexive. Never address the reader as "you" in features. In standfirsts and social teasers, second person is acceptable ("Why you should pay attention to..."). Direct address in web headlines is fine.

<!-- When adding a new format (podcast episodes, video scripts, event copy), define its
     narrative posture here rather than letting it default to the feature voice. -->

## Do / Don't Rules

### Do
- Use "artwork" as one word in all contexts
- Capitalise art movements when used as proper nouns: Surrealism, Bauhaus, Art Deco, Impressionism
- Use lowercase when the movement name functions as an adjective: surrealist painting, bauhaus-influenced design
- Include at least one concrete detail per feature that the reader could not find on Wikipedia — an observation from a studio visit, a telling quote, a production fact
- Provide context for institutions, exhibitions, and cultural events — assume the reader is encountering them for the first time unless they are household names
- Attribute opinions. The magazine has a perspective, but it distinguishes between editorial judgement and reported fact
- Use metric measurements with imperial in parentheses where relevant to a physical description of an artwork or building
- Name the city and country on first reference to any institution not widely known: "the Pinakothek der Moderne in Munich," not just "the Pinakothek der Moderne"

### Don't
- Never describe an artwork as "stunning," "breathtaking," or "masterpiece" — unless directly quoting a named source
- Never use press-release language. If a sentence could appear in a gallery's promotional material unchanged, rewrite it. Common tells: "explores the intersection of," "invites the viewer to," "a bold new vision," "pushing boundaries"
- Never assume the reader follows the art calendar. Spell out why a show or event matters rather than relying on its reputation
- Never use "content" to describe the magazine's journalism. Foyer publishes features, profiles, reviews, columns, and essays — not "content"
- Never open a feature with a rhetorical question
- Never use "iconic" unless referring to actual icons (religious imagery)
- Avoid "space" as a catch-all for gallery, room, venue, or building — use the specific word
- Never use "creative" as a noun to describe a person ("the creative behind the project"). Use their actual role: architect, designer, filmmaker, painter

<!-- INFERRED RULES — not stated in the brief but consistent with the voice
     and audience profile. Review these and remove any that do not fit: -->

- Do not use "whilst" — use "while" *(inferred from the register: the magazine aims for natural, not formal)*
- Avoid semicolons in features — restructure as two sentences *(inferred from the sentence-length guidance and rhythm preference)*
- When referencing artists, give nationality and birth year on first mention in each piece: "the German painter Gerhard Richter (b. 1932)" *(inferred from the accessibility mandate — remove if the house style prefers a different format)*
- Do not use "in terms of" — restructure the sentence *(inferred from the preference for direct, verb-driven prose)*
- Avoid opening paragraphs with "It is worth noting that" or similar throat-clearing constructions — start with the observation itself *(inferred from the sentence style guidance favouring directness)*
- When listing artworks in a piece, give title (italicised), year, and medium on first mention: *Untitled (Cowboy)*, 2003, inkjet print *(inferred from the accessibility mandate — the reader needs these details to picture the work)*

## Key Terminology

| Term | Usage | Notes |
|------|-------|-------|
| artwork | One word, always. Never "art work" or "work of art." | Applies in all contexts: headlines, body text, captions. |
| Surrealism / surrealist | Capital for the movement, lowercase for the adjective. | Same pattern for all movements: Bauhaus / bauhaus-influenced, Art Deco / art deco motifs, Impressionism / impressionist brushwork. |
| standfirst | The short introductory paragraph below the headline. | Not "subheading," "deck," or "dek." Foyer's house term. |
| web exclusive | Two words, no hyphen. | A piece published only on the web edition, not drawn from the print issue. |
| feature | A piece of 1,500-3,000 words. | Do not use interchangeably with "article" — Foyer distinguishes features, profiles, reviews, columns, and essays. Each has a different format. |
| review | A critical assessment of a specific exhibition, album, film, or building. | Always includes a recommendation (see it / skip it / worth the detour). |
| profile | A piece built around a person — their work, their trajectory, their perspective. | Always includes direct quotes from the subject. |
| column | A recurring opinion piece by a named writer with a consistent perspective. | First person is permitted. Voice may differ from the feature register. |
| biennial / biennale | Use "biennial" in English-language text. Use "biennale" only when part of an official name (Venice Biennale, Istanbul Biennial). | Do not capitalise "biennial" when used generically. |
| retrospective | A survey exhibition covering a significant portion of an artist's career. | Not a synonym for "big exhibition." Use only when the scope genuinely covers a career arc. |
| group show | An exhibition featuring multiple artists, usually organised around a theme or curatorial argument. | Not "group exhibition" (too formal for Foyer's register). |
| gallery | The physical venue. | Do not use "gallery" and "museum" interchangeably — they are different institutions with different functions. If unsure which term applies, check the institution's own description. |
| curator | The person who selects and organises an exhibition. | Use on first mention with context: "the exhibition's curator, [Name]." Do not assume the reader knows what a curator does — weave in enough context to make the role clear. |
| catalogue | The publication accompanying an exhibition. | British spelling (not "catalog"). Italicise the title when referencing a specific catalogue by name. |

<!-- Add new terms to this table as they arise. Review the glossary at the start
     of each issue cycle. Common additions: new institutions, recurring event names,
     house-style decisions on controversial spellings. -->

## Recurring Tasks

### 1. Drafting Headlines
**Input:** The finished or near-finished feature text, plus the section it will appear in (visual art, architecture, design, film, music).
**Output:** Three to five headline options. Each headline should be specific to the piece — not generic enough to fit a different article on the same subject. Under 10 words. Free of puns unless the pun is genuinely good and not the obvious one. No colons. No "How [person] Is Changing [field]" constructions. No questions.
**Task-specific rules:** Headlines for print may differ from web headlines. Print headlines can be more allusive and assume the reader sees the accompanying image; web headlines should be searchable and clear about the subject without visual context.

### 2. Writing Standfirsts
**Input:** The finished feature text and the chosen headline.
**Output:** One standfirst of 25-40 words. It should tell the reader what the piece is about and why it matters now, without repeating the headline. It may name the writer. It should create enough curiosity to pull the reader into the first paragraph — but through specificity, not through withholding information.
**Task-specific rules:** No rhetorical questions. No first person. No superlatives. The standfirst should work whether or not the reader has seen the headline — it complements the headline rather than depending on it.

### 3. Editing Interview Transcripts
**Input:** A raw transcript (from a recording app or manual transcription) plus any notes about context or emphasis.
**Output:** A clean, readable Q&A formatted with the interviewer's questions in bold and the subject's answers in regular text. Remove filler words ("um," "like," "you know") and false starts. Preserve the subject's speech patterns and vocabulary — do not smooth their language into magazine prose. Flag any passages where the meaning is ambiguous and the editor should check the recording. Mark any factual claims that should be verified before publication.
**Task-specific rules:** Do not alter the substance of any answer. If a quote needs trimming for length, use [...] to indicate removed material. Keep the subject's contractions, colloquialisms, and sentence structures — they are part of the voice the reader encounters. The interviewer's questions may be lightly rewritten for clarity, since they serve the reader rather than representing quoted speech.

### 4. Writing Social Teasers
**Input:** The published feature, its headline, and the target platform (Instagram or Bluesky).
**Output:** One teaser per platform. Instagram: 1-3 sentences plus 3-5 relevant hashtags, no more. Bluesky: 1-2 sentences, no hashtags, may include a direct observation or opinion that would not appear in the magazine itself — the social voice is slightly more personal and opinionated than the print voice, as though the editor is recommending the piece to a friend.
**Task-specific rules:** Never use "link in bio." Never say "you won't believe" or "this will change how you think about." The teasers should sound like a recommendation from a friend, not a marketing department. The social voice can use contractions and first person where the magazine voice would not, but it should never feel like a different publication — the reader should recognise Foyer's personality.

### 5. Generating Image Prompts
**Input:** The finished feature text, the section, and any notes about the desired visual treatment (photograph, illustration, abstract, documentary).
**Output:** Two to three image prompt options, each written for the image generation tool the team uses. Each prompt should describe a visual that complements the article without illustrating it literally. Include guidance on mood, colour palette, and composition. Avoid cliches for the subject matter — no paintbrushes for a piece about a painter, no blueprints for a piece about an architect, unless the piece itself is about the tools.
**Task-specific rules:** All generated images must be clearly identifiable as illustrations or AI-generated visuals, not as photographs. Foyer does not use AI-generated images that could be mistaken for photojournalism.

## Quality Bar

A piece of writing meets the Foyer standard when it satisfies all of the following:

1. **Specific over general.** Every claim is grounded in a concrete detail — a date, a place, a name, an observable fact. No paragraph consists entirely of evaluative adjectives.
2. **Accessible without condescending.** A reader with no art-world background can follow the argument and come away knowing something they did not know before. Context is woven in, not bolted on as a sidebar or a parenthetical dump.
3. **Editorially independent.** The piece reads as journalism, not promotion. It includes critical perspective, acknowledges limitations or controversy where relevant, and does not read like a rewritten press release. The reader trusts the magazine because it tells them what it thinks, not what the gallery wants them to think.
4. **Structurally sound.** The piece has a clear entry point, a logical progression, and an ending that earns its position. The reader never wonders "why am I being told this now?" Transitions between sections feel motivated, not mechanical.
5. **Tonally consistent.** The voice does not drift between paragraphs. No sudden shifts to academic register, press-release phrasing, or informal blog tone. If the piece were read aloud, it would sound like one person speaking, not several.
6. **Within format constraints.** Features: 1,500-3,000 words. Web exclusives: 600-1,000 words. Headlines: under 10 words. Standfirsts: 25-40 words.

The published benchmark is the quality and accessibility of Monocle's features and The Guardian Weekend's culture writing. If a draft would not hold its own next to a piece from those publications, it needs more work.

**Self-check before delivery:** Before presenting any draft, review it against these six criteria. If any criterion is not met, revise before showing the work. Do not flag the failure and deliver anyway — fix it first.

<!-- Update the benchmark references if the magazine's aspirations shift or if
     better comparisons emerge. The benchmark should always be a publication
     the team actually reads and respects, not a theoretical ideal. -->

## Sources and References

- **Citation format:** No formal footnotes or academic citations. Sources are named in the text: "according to [person], [role] at [institution]" or "a [year] report by [organisation] found that..." When referencing a specific artwork, give the title (in italics), the year, and the medium on first mention.
- **Trusted sources:** Museum and gallery catalogues (for factual detail, not for evaluative language). Institutional archives. Published interviews with artists in reputable outlets. Government cultural policy documents. Peer-reviewed art history journals (for factual background, translated into accessible language).
- **Treat with caution:** Gallery press releases — useful for dates, dimensions, and exhibition logistics, but never for characterisation or evaluation. Artist statements — quote when revealing, but do not paraphrase uncritically as though the artist's framing is objective. Wikipedia — acceptable for quick fact-checks (birth dates, exhibition histories), but never as the sole source for a claim in a feature.
- **Avoid:** Anonymous art-market sources unless the story specifically concerns the market and anonymity is editorially justified. PR agencies speaking on behalf of artists without named attribution. Social media posts as primary sources unless the social media activity is itself the story. Auction price data presented without context about market dynamics.
- **Attribution standard:** Every factual claim in a feature should be traceable to a named source — a person, a document, or an institution. "Critics say" is not attribution. "The art historian [Name], writing in [Publication], argued that..." is.
- **Artwork references:** When citing a specific artwork, give the title in italics, the year, and the medium: *Guernica*, 1937, oil on canvas. This is not a citation style — it is a reader service.

## Update Log

| Date | Section Changed | What Changed |
|------|----------------|--------------|
| | | |

<!-- Update this log whenever you change the context file. Even small changes
     (a new term in the glossary, a tweaked rule) are worth recording. This log
     helps you track editorial drift over time and understand, six months from
     now, why a particular decision was made. -->
```

## Known Limitations
- The context file is only as good as the brief. A vague brief ("we want it to sound professional") produces a vague context file. The skill works best when the user provides a specific voice description, concrete rules, and at least one published benchmark. If the brief is thin, the assistant will ask clarifying questions — but the quality of the output still depends on the specificity of the answers. A two-sentence brief cannot produce a 200-line context file with genuine editorial depth.
- The generated file captures a snapshot of the project at one moment. Projects evolve — the voice sharpens, the audience shifts, new rules emerge. The context file includes an update log and growth mechanisms (the extendable glossary, the inferred-rules markers, the guidance comments), but the user must actually maintain it. An outdated context file is worse than no context file at all, because it enforces yesterday's standards on today's work. Schedule a quarterly review — the update log makes this easier, but the discipline is on you.
- Inferred rules are the skill's best guesses based on the voice profile and audience definition. They are clearly marked, but there is a risk that a user skims past them and ends up with constraints they never intended. Always review the inferred section before loading the file into production sessions. Remove or modify any rule that does not match the project's actual editorial judgement.
- The skill generates a context file for a single project. If you work on multiple projects simultaneously, you need a separate context file for each one and a reliable way to load the right one at the start of each session. This skill does not solve the "which context file should I load?" problem — that depends on your tools and workflow.
- If the brief contains contradictions (e.g., "we want an academic tone" paired with "keep it casual and fun"), the assistant will flag the tension and ask the user to resolve it rather than guessing which instruction takes priority. This means the skill may not produce a complete file on the first pass if the brief has internal conflicts — but it is better to surface the conflict than to bury it in a file that sends mixed signals to future sessions.

## Tips for Maintaining the Context File
- Review the file at the start of each production cycle (each issue, each season, each quarter). Does the voice description still match how the project actually sounds? Have any new terms or rules emerged that are not yet recorded?
- When you notice the assistant producing work that misses the mark in a consistent way, check whether the context file is the cause. Often, a vague instruction is the root — tightening one sentence in the context file fixes the pattern across all future sessions.
- If multiple people maintain the context file, designate one person as the owner who approves changes. A context file edited by committee without coordination will contradict itself within months.
- Treat the inferred-rules section as a staging area. After three months, any inferred rule that has survived review should be moved into the main Do/Don't lists — it has earned its place. Any inferred rule that keeps getting removed should be deleted permanently.

## Related Skills
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md) — verifies that a piece of writing stays within the voice parameters defined in the context file
- [multi-author-harmoniser](../multi-author-harmoniser/SKILL.md) — aligns multiple writers' voices to a shared standard, which the context file defines
- [copy-editor](../copy-editor/SKILL.md) — applies the do/don't rules and terminology glossary from the context file during line editing
- [terminology-consistency-checker](../terminology-consistency-checker/SKILL.md) — checks that the glossary terms in the context file are used correctly throughout a piece
