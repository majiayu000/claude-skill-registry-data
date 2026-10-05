---
name: tone-rewriter
description: "Rewrite a piece of text in a different tone or register while preserving all factual content, direct quotes, and meaning — adapting the same information for a different audience, publication, or context."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [editing, tone, rewriting, adaptation, journalism, content-repurposing]
---
# Tone Rewriter

## What This Skill Does
Rewrite a piece of text in a different tone or register while preserving all factual content, direct quotes, and meaning — adapting the same information for a different audience, publication, or context.

## When To Use This Skill
- You need to adapt a formal institutional report or press release into editorial copy that reads naturally
- An editor has given feedback that the tone is wrong for the publication — too stiff, too casual, too academic, too tabloid
- You are repurposing an article for a different publication with a different voice (serious broadsheet to casual newsletter, trade journal to consumer magazine)
- You want to test how the same information reads in two different registers before committing to one
- You need to adjust the tone of an opinion piece — sharpening it, softening it, or making it more authoritative

## What You Need To Provide
**Required:** The text to rewrite; the target tone (formal, conversational, authoritative, empathetic, urgent, dry, ironic, provocative, warm, clinical).

**Optional:** The source tone, so the assistant knows what is changing and by how much; target publication or audience (which provides implicit tone guidance); specific phrases, quotes, or data points to preserve unchanged; a target word count if the rewrite should also be shorter or longer.

## How the Assistant Approaches This
1. Identifies the current tone markers: sentence length and rhythm, vocabulary register (Latinate vs Anglo-Saxon words, technical vs everyday), use of first and second person, presence of emotional or evaluative language, formality indicators (contractions, colloquialisms, hedging phrases)
2. Maps the gap between current and target tone — a shift from "formal academic" to "conversational newsletter" is much larger than "formal broadsheet" to "authoritative long-form"; the scale of change determines how much structural adjustment is needed alongside vocabulary changes
3. Rewrites by adjusting vocabulary choice, sentence length and rhythm, rhetorical devices (questions, short emphatic sentences, direct address), and formality level — while keeping every fact, figure, direct quote, and the logical structure of the argument unchanged
4. Returns the rewritten text with a tone shift note identifying the main changes made, so the author can confirm the rewrite landed in the right register

## Output Format
The rewritten text in full, followed by a tone shift note of two to three sentences describing the main changes: what was done to vocabulary, sentence structure, and voice. Word count comparison shown as a single line.

## Quality Criteria
- [ ] All facts, data, and figures are preserved exactly as in the original
- [ ] The tone has clearly shifted — a reader who knows neither version would identify the new tone without being told
- [ ] No direct quotes have been altered
- [ ] The logical structure and argument of the original are unchanged
- [ ] Word count is within 20% of the original unless a target was specified

## Example

### Input

**Text to rewrite:**

> Northgate Media Group is pleased to announce the launch of The Signal Network, a new portfolio of five podcast titles spanning technology, culture, science, international affairs, and personal finance. The Signal Network represents a significant strategic investment by Northgate Media Group in the audio content sector, and reflects the company's commitment to delivering high-quality, editorially independent journalism across a broad range of subject areas. The network's inaugural slate of titles will be available on all major podcast platforms from the first of next month. Northgate Media Group invites media professionals and potential partners to contact the company's business development team for information regarding commercial and partnership opportunities.

**Target tone:** Conversational newsletter for media industry insiders

**Source tone:** Corporate press release

### Output

**Rewritten text:**

Northgate Media Group is launching The Signal Network next month — five new podcast titles covering technology, culture, science, international affairs, and personal finance. It's the company's biggest bet on audio yet, and they're billing it as editorially independent across the board.

The shows will land on all major platforms from the first of next month. If you're interested in partnerships or commercial opportunities, Northgate's business development team is the place to start.

---

**Tone shift note:** Converted from press release register (passive constructions, formal announcement language, institutional voice) to direct, conversational copy suited to an industry newsletter. Contractions introduced, sentence length shortened, and the final paragraph reframed as a practical action item rather than a formal invitation. All facts and the launch date preserved.

Original: 114 words → Rewritten: 95 words

## Known Limitations
- Extreme tone shifts — such as formal legal language to casual social media copy — may require structural changes that go beyond vocabulary and rhythm adjustment; the skill will flag when the structure of the original is itself a barrier to the target tone, rather than silently forcing an unsuitable structure into a new register.
- Some tones are culturally specific and may not carry equally across all English-language markets — "dry British irony" does not translate directly to American editorial conventions; specify the target market if regional register matters.

## Related Skills
- [paragraph-clarity-rewriter](../paragraph-clarity-rewriter/SKILL.md)
- [copy-editor](../../../editing/copy-editor/SKILL.md)
- [caption-writer](../../../social-media/content/caption-writer/SKILL.md)
