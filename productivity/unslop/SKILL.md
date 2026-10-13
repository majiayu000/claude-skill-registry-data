---
name: unslop
description: Polish substantial human-facing prose, such as emails, announcements, articles, and PR descriptions. Use when drafting or revising those deliverables. Excludes routine conversational replies, code, skills, prompts, workflows, and agent instructions.
---

# Unslop

Polish prose for its intended readers while preserving the author's meaning and voice.

## Scope

Apply this skill to substantial prose deliverables intended for people. Routine conversational replies, code, skills, prompts, workflows, and agent instructions are outside its automatic scope. In mixed documents, edit only the human-facing prose; preserve embedded instructions, code, and quoted material.

## Process

1. Identify the audience, purpose, and requested tone from the task and draft.
2. Use the checks below to find wording that obscures meaning or distracts those readers. These are editorial heuristics, not evidence of AI authorship or a checklist requiring a change for every item.
3. Revise where the edit improves clarity, specificity, or the intended voice. Preserve facts, uncertainty, technical meaning, and the author's position.
4. Read the result for coherence and fidelity. Finish when the prose serves the audience and the identified distractions are resolved; leave effective passages intact.

## Voice

Follow the author's voice and the requested style. Vary sentence length when it improves rhythm. Use first person, opinions, humour, or informality when they fit the author and audience. Preserve an existing point of view; ask for missing personal material only when the deliverable needs it. Ground specific details in the supplied material rather than inventing experiences, reactions, or measurements.

## Editorial checks

### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Give named sources a clear purpose. Retain names and citations that support the argument; trim lists included only for prestige.
3. **Empty elaboration.** Check phrases such as "highlighting" or "showcasing" for a concrete contribution. Trim them when they merely restate praise; keep explanations supported by the material.
4. **Promotional language.** Check whether words such as "groundbreaking" or "must-visit" fit the requested genre and have support. Prefer concrete descriptions where praise adds no information.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

### Language

7. **Inflated vocabulary.** Consider a familiar word when it conveys the same meaning more directly. Words such as "crucial", "enhance", or "interplay" can be useful; judge their function in the sentence.
8. **Roundabout verbs.** Prefer "is" or "has" when phrases such as "serves as" add no distinction. Keep the more specific verb when its meaning matters.
9. **Formulaic contrast.** State the point directly when "not just X, but Y" adds emphasis without a useful distinction. Keep contrasts that explain the argument.
10. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

### Style

13. **Punctuation.** Check whether repeated asides or interruptions make the prose hard to follow. Choose commas, periods, dashes, or parentheses according to the relationship between ideas and the requested style. Preserve punctuation that improves clarity.
14. **Colons.** Keep a colon when it clearly introduces an explanation, example, or list. Recast sentences where it obscures the grammatical connection.
15. **Boldface.** Use emphasis to help scanning. Reduce it when too many highlighted terms compete for attention.
16. **Inline headings.** Keep labels that help readers scan distinct points. Remove labels that merely repeat the sentence that follows.
17. **Heading case.** Follow the publication or author's convention consistently. Prefer sentence case when no convention is specified.
18. **Emojis.** Keep them when they suit the audience or convey useful meaning; trim decoration that distracts from the message.
19. **Quotation marks.** Follow the medium's typography consistently and preserve quoted wording.

### Communication artifacts

20. **Stock conversational phrases.** Trim generic openings and closings that add no purpose. Keep courtesy or an invitation to reply when it serves the relationship or the next step.
21. **Uncertainty.** Replace vague disclaimers with the specific limitation supported by the material. Preserve qualifications that affect accuracy.
22. **Automatic praise.** Prefer a direct response to unsupported agreement or flattery. Keep appreciation that is specific and appropriate to the relationship.

### Filler

23. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
25. **Generic conclusions.** End with the implication, action, or closing that the piece needs. Trim predictions and summaries that add no substance.

### Jargon

26. **Jargon and metaphors.** Prefer concrete wording when an abstract term obscures the mechanism or claim. Preserve established terminology, technical distinctions, and metaphors that help this audience. For example, "API surface" can be precise in an engineering document; it needs explanation only when the audience needs it.

### Plain speech

27. **Specificity.** Where the reader needs an explanation, name the behaviour or consequence using supported details. Keep evocative language when it serves the genre, and replace interchangeable filler with something particular to the subject.
28. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.
29. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Passive is fine only when the actor is unknown or genuinely doesn't matter.
30. **Adverbs.** Trim empty intensifiers or choose a more precise verb. Use a measurement when the source provides one, and retain modifiers that convey a real distinction.
31. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is rarely clearer.
