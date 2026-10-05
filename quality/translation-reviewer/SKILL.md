---
name: translation-reviewer
description: "Reviews a translated text against its source original, producing a structured quality report that flags accuracy errors, fluency issues, and cultural mismatches — each with a specific correction and rationale."
status: stable
category: translation
subcategory: quality
version: 1.0
eval_score: 4.50
tags: [translation, quality, review, accuracy, editing, proofreading]
---
# Translation Reviewer

## What This Skill Does
Reviews a translated text against its source original, producing a structured quality report that flags accuracy errors, fluency issues, and cultural mismatches — each with a specific correction and rationale.

## When To Use This Skill
- You received a translation from a translator or agency and need a systematic quality check before publication
- You translated a document yourself and want an independent review pass before it goes to an editor
- You need to compare two competing translations of the same source text and identify which is more accurate
- You are quality-assuring a batch of translations and need a standardized review format for each

## What You Need To Provide
**Required:** The source text in the original language; the translated text in the target language; the source and target languages.

**Optional:** The intended audience and publication context (news article, press release, social media, legal document); the style standard the translation should follow (AP, house style, formal institutional); a glossary of approved translations for key terms; specific areas of concern (e.g., "check the financial terminology," "verify that quotes match the original," "flag any overly literal phrasing").

## How the Assistant Approaches This
1. **Reads both texts in full before flagging anything.** Understands the source text's meaning, tone, and structure, then reads the translation as a complete document. This prevents false flags caused by reading sentence-by-sentence without understanding the translator's overall strategy.

2. **Categorizes issues into three tiers.** Tier 1: Accuracy errors — meaning has been changed, omitted, or added (must fix before publication). Tier 2: Fluency issues — the translation is accurate but reads unnaturally, uses awkward phrasing, or contains grammatical errors in the target language (should fix). Tier 3: Style suggestions — the translation is accurate and fluent but could be improved for register, idiom, or cultural fit (optional refinement).

3. **For each flagged item, provides the source passage, the current translation, the suggested correction, and a one-line rationale.** Rationales cite specific translation principles (e.g., "false cognate," "undertranslation," "register mismatch") so the translator can learn from the feedback, not just apply the fix.

4. **Assesses overall translation quality.** After the itemized review, provides a summary verdict: how many Tier 1/2/3 issues were found, whether the translation is ready for publication, needs a revision pass, or requires significant rework. Includes an overall quality rating on a 1–5 scale.

5. **Recommends next steps.** Specifies whether to fix Tier 1 items and publish, send back for a full revision pass, or re-translate from scratch. If a glossary was not provided but should have been, recommends building one before the next translation in the series.

## Output Format
Numbered list of flagged items in document order, each formatted as:

**[Tier 1/2/3] [Location cue]**
- **Source:** "original passage"
- **Translation:** "current translation"
- **Suggested:** "corrected translation"
- **Rationale:** *One-line explanation citing the translation principle involved*

Summary section at the end with: issue counts by tier, overall quality rating (1–5), publication readiness verdict, and recommended next steps. For a typical 800-word translation, expect 5–15 flagged items. Tone: professional and constructive — written as colleague-to-colleague feedback, not as criticism.

## Quality Criteria
- [ ] Every flagged item includes source passage, current translation, suggested correction, and rationale
- [ ] Tier classifications are accurate — style preferences not misclassified as accuracy errors
- [ ] No false positives — items flagged as errors that are in fact valid translation choices
- [ ] Location cues are specific enough to find the passage in both source and translated text
- [ ] Summary verdict is honest — does not understate serious accuracy problems or overstate minor style issues
- [ ] The review is constructive and professional in tone
- [ ] Recommended next steps are specific and actionable

## Example

### Input
**Source language:** French
**Target language:** English
**Context:** News feature for a general-interest magazine
**Source text (excerpt, 180 words):**

Les habitants du quartier de la Rive-Sud n'ont pas attendu les promesses de la mairie. Depuis trois ans, ils organisent eux-memes le ramassage des dechets, l'entretien des espaces verts et meme la renovation de la place centrale. « On en avait marre d'attendre », explique Fatima Benali, presidente de l'association Quartier Vivant. « La mairie nous disait chaque annee que c'etait prevu au budget. Au bout d'un moment, on a decide de faire sans eux. »

Le resultat est frappant. La place, autrefois un parking sauvage envahi par les mauvaises herbes, est devenue un lieu de rencontre avec des bancs, un terrain de petanque et un jardin partage. L'association a leve 28 000 euros aupres des commercants du quartier pour financer les travaux.

**Translation to review:**

The inhabitants of the South Shore neighborhood didn't wait for promises from city hall. For three years, they have organized themselves the garbage collection, the maintenance of green spaces, and even the renovation of the central square. "We were fed up with waiting," explains Fatima Benali, president of the Quartier Vivant association. "City hall told us each year it was planned in the budget. At some point, we decided to do without them."

The result is striking. The square, formerly a wild parking lot invaded by weeds, has become a meeting place with benches, a petanque court, and a shared garden. The association raised 28,000 euros from neighborhood shopkeepers to finance the work.

### Output

**Translation Quality Review — Rive-Sud Neighborhood Feature**
*Languages: French → English | Context: Magazine feature*

---

1. **[Tier 1] Para 1, sentence 1:** "the South Shore neighborhood"
   - **Source:** "le quartier de la Rive-Sud"
   - **Translation:** "the South Shore neighborhood"
   - **Suggested:** "the Rive-Sud neighborhood" or "the Rive-Sud district"
   - **Rationale:** *"Rive-Sud" is a proper noun — the name of a specific neighborhood. Translating it to "South Shore" creates a false equivalent (there is no neighborhood called "South Shore" in this context). Retain the French name with a brief gloss if needed on first reference.*

2. **[Tier 2] Para 1, sentence 2:** "they have organized themselves the garbage collection"
   - **Source:** "ils organisent eux-memes le ramassage des dechets"
   - **Translation:** "they have organized themselves the garbage collection"
   - **Suggested:** "they have been organizing garbage collection themselves"
   - **Rationale:** *Calque from French reflexive structure. In English, "themselves" modifies the subject (they did it themselves), not the verb phrase. The current phrasing is unnatural and momentarily confusing.*

3. **[Tier 2] Para 2, sentence 2:** "a wild parking lot invaded by weeds"
   - **Source:** "un parking sauvage envahi par les mauvaises herbes"
   - **Translation:** "a wild parking lot invaded by weeds"
   - **Suggested:** "an informal parking area overrun with weeds"
   - **Rationale:** *"Parking sauvage" means unauthorized/informal parking — not a "wild" parking lot. "Wild" is a false cognate of "sauvage" in this context. "Invaded" is also overly literal for "envahi"; "overrun" is the standard English collocation.*

4. **[Tier 3] Para 2, sentence 2:** "a shared garden"
   - **Source:** "un jardin partage"
   - **Translation:** "a shared garden"
   - **Suggested:** "a community garden"
   - **Rationale:** *"Community garden" is the standard English term for this concept and is immediately understood by English-language readers. "Shared garden" is not wrong but sounds like a garden shared between two households rather than a communal growing space.*

5. **[Tier 3] Para 2, sentence 3:** "to finance the work"
   - **Source:** "pour financer les travaux"
   - **Translation:** "to finance the work"
   - **Suggested:** "to fund the renovations"
   - **Rationale:** *Register adjustment. "Finance the work" is technically correct but reads slightly formal and vague for a magazine feature. "Fund the renovations" is more natural in English feature writing and more specific.*

---

**Summary**

- **Tier 1 (accuracy errors):** 1 — the mistranslation of the neighborhood name must be corrected before publication.
- **Tier 2 (fluency issues):** 2 — the calque in sentence 2 and the false cognate "wild parking lot" both need fixing to read naturally.
- **Tier 3 (style suggestions):** 2 — optional improvements that would strengthen the piece but are not blockers.
- **Overall quality rating:** 3.5/5 — The translation captures the essential meaning and most of the tone, but the Tier 1 proper-noun error and two noticeable fluency issues would distract a native English reader.
- **Publication readiness:** Not yet. Fix the three Tier 1 and Tier 2 items, then the piece is publishable. The Tier 3 suggestions are recommended but not required.

**Next Step:** Correct the five items above (prioritizing Tier 1 first), then do a final read-through of the full translated piece for any additional fluency issues not captured in this excerpt.

## Known Limitations
- The assistant reviews translation quality based on the source and target texts provided. If the source text itself contains errors, the assistant may flag a correct translation of an incorrect original as accurate — it does not fact-check the source material.
- For highly specialized domains (medical, legal, financial), the assistant can identify obvious mistranslations but may not catch subtle terminological errors that only a domain specialist would recognize. Supplement this review with subject-matter expertise for regulated content.
- The quality rating is calibrated for general professional translation. Different contexts (literary translation, marketing transcreation, legal certified translation) have different quality standards that may require adjusted scoring criteria.

## Related Skills
- [article-translator](../../text/article-translator/SKILL.md) — translate an article that can then be reviewed with this skill
- [translation-glossary-builder](../../reference/translation-glossary-builder/SKILL.md) — build a glossary to use as a reference during review
- [copy-editor-assistant](../../../magazine-journalism/editing/copy-editor-assistant/SKILL.md) — edit the target-language text for grammar and style after translation review
- [regional-variant-adapter](../../localization/regional-variant-adapter/SKILL.md) — adapt the reviewed translation for a specific regional market
