---
name: logline-writer
description: "Crafts a precise, irresistible one-sentence logline for a feature film or TV pilot that captures protagonist, inciting incident, central conflict, and stakes in under 40 words."
status: stable
category: screenwriting
subcategory: development
version: 1.0
eval_score: 4.5
tags: [screenwriting, development, logline, feature-film, TV]
---
# Logline Writer

## What This Skill Does
Crafts a precise, irresistible one-sentence logline for a feature film or TV pilot that captures protagonist, inciting incident, central conflict, and stakes in under 40 words.

## When To Use This Skill
- You have a premise but cannot distill it to a single sentence that makes someone want to read the script
- You are preparing for pitch meetings and need a logline that works as a verbal elevator pitch
- You want to test whether your story concept has a clear protagonist, conflict, and stakes — a premise that cannot be loglined cleanly usually has a structural problem
- You are writing a coverage report, one-pager, or treatment and need a locked logline to anchor it

## What You Need To Provide
**Required:** The protagonist (role or identity, not name), the inciting incident or central situation, and what is at stake
**Optional:** Genre or tone; the antagonistic force; the ironic or thematic twist that makes the concept distinctive; what the writer most wants to preserve in the logline

## How the Assistant Approaches This
1. Extracts the four logline elements from the input: protagonist (described by role or defining trait, not name), inciting incident (the disruption that starts the story), central conflict (what the protagonist must overcome or decide), and stakes (what is lost if they fail — ideally with a personal and external dimension)
2. Applies the standard logline test: can a producer hearing this sentence immediately see the movie and identify the audience? If not, the premise is either too thin or too complex and the skill flags why
3. Writes three logline variants: a direct dramatic version, an ironic or tonal version (leading with the genre's distinctive flavor), and a compressed version for verbal pitching (under 25 words)
4. Identifies which element is weakest in the input and provides one specific note on how to strengthen it

## Output Format
Three numbered logline variants (one per line), each under 40 words, with a two-word label (e.g., **Dramatic**, **Ironic**, **Compressed**). Followed by a brief diagnostic note (2–3 sentences) identifying the weakest element and what would sharpen the concept. No preamble. No "here are some options" framing.

## Quality Criteria
- [ ] Every logline contains all four elements: protagonist, inciting incident, conflict, and stakes
- [ ] No logline exceeds 40 words in the Dramatic and Ironic variants; no Compressed variant exceeds 25 words
- [ ] The protagonist is described by a trait or role that creates immediate dramatic irony or tension, not just a job title
- [ ] Stakes are specific — not "everything" or "his life" but a concrete relationship, identity, or irreversible consequence
- [ ] The diagnostic note names one specific missing or weak element, not a vague suggestion to "add more conflict"

## Example

### Input
**Format:** Feature film
**Premise:** A hostage negotiator discovers, mid-negotiation with a bank robber, that her estranged teenage son is one of the hostages. The robber figures this out halfway through and uses it against her.
**Genre:** Thriller
**Tone:** Tense, emotional, character-driven. Think Dog Day Afternoon meets Prisoners.
**Writer note:** "I want to keep the irony of her professional competence being destroyed by her personal failure."

### Output

**Dramatic**
An elite hostage negotiator must talk a desperate bank robber into releasing his hostages — while concealing from her supervisor that her estranged son is among them and the robber already knows.

**Ironic**
She has talked down armed men in fourteen cities. She has never successfully talked to her own son. Today she has to do both, simultaneously, while a gunman watches.

**Compressed**
A hostage negotiator discovers her estranged son is trapped inside — and the robber knows it.

---

*Diagnostic note:* The core irony is strong and clearly stated. The weakest element is stakes: what specifically happens if she fails? If her son dies, that is a stake — but what makes this beyond a tragedy is the professional/personal collision. Clarify whether the external stake is her career (she'll be pulled off the case if discovered), her son's life, or both — and the logline sharpens further. The "estranged" detail is doing a lot of work; a single additional word indicating *why* they're estranged (if that's a plot element) would make the irony land harder.

## Known Limitations
- Loglines for ensemble stories or plots with multiple equally-weighted protagonists are structurally difficult; the skill will default to identifying one primary protagonist and may not capture the full ensemble correctly — writers should specify whose story it is before running the skill
- The skill produces conventional three-act-structure loglines; experimental or non-linear narratives (anthology films, stories told in reverse) may produce loglines that accurately describe the concept but do not reflect the experience of the film
- A strong logline does not guarantee a strong script; the skill evaluates whether the concept is pitchable, not whether it is executable

## Related Skills
- [beat-sheet-builder](../beat-sheet-builder/SKILL.md)
- [treatment-writer](../treatment-writer/SKILL.md)
- [one-pager-writer](../../production/one-pager-writer/SKILL.md)
