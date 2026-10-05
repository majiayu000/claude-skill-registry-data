---
name: libel-risk-checker
description: "Reviews a draft for statements that carry a credible risk of defamation, producing a flagged checklist of red-flag passages with a plain-language explanation of why each is potentially problematic."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, legal, risk, defamation, pre-publication]
---
# Libel Risk Checker

## What This Skill Does
Reviews a draft for statements that carry a credible risk of defamation, producing a flagged checklist of red-flag passages with a plain-language explanation of why each is potentially problematic.

## When To Use This Skill
- Before publishing any article, script, or report that makes negative claims about a named individual, company, or organisation
- When a source has made a serious allegation and you are deciding whether to include it
- When a subject has threatened legal action and you need to locate the specific passages at issue
- As a final pre-publication check alongside your standard copy-editing pass
- When commissioning editors want a structured risk overview before sending a piece to a lawyer

## What You Need To Provide
**Required:** The full draft text to be reviewed.
**Optional:** The jurisdiction in which the piece will be published (e.g., England and Wales, United States, Australia) — different countries have different defamation standards, and naming a jurisdiction improves the relevance of the flags; the name of any individual or organisation who has been given a right of reply, and what their response was.

## How the Assistant Approaches This
1. Reads the full draft and identifies statements that could be understood as factual allegations — as opposed to clearly labelled opinion — about a named or identifiable individual, company, or organisation.
2. For each flagged passage, assesses it against a standard checklist of defamation red flags: whether the claim is verifiably false or unverified; whether it could lower the subject's reputation in the eyes of a reasonable person; whether the subject is identified or identifiable; whether the source of the claim is attributed or left anonymous; and whether any public-interest or fair-comment defence is apparent from the text.
3. Produces a numbered red-flag report listing each passage, the specific concern, and a practical suggestion for reducing risk (e.g., attribute to a named source, add the subject's response, reframe as confirmed rather than alleged, or seek legal review before publishing).

## Output Format
- A numbered list of red-flag passages. Each entry includes: the flagged text in quotation marks, a plain-language explanation of why it is a concern, a risk level indicator (Low / Medium / High), and a suggested editorial action.
- A short summary at the end: total flags, number by risk level, and an overall pre-publication recommendation.
- Tone is direct and practical, written for a working editor — not legal language, not alarmist.
- This output is a structured editorial aid. It is not a legal opinion.

## Quality Criteria
- [ ] Every flagged passage contains an actual claim about a named or identifiable party — no flags on clearly attributed quotes, clearly labelled opinion, or purely descriptive statements
- [ ] Risk levels are calibrated: not every negative statement is rated High
- [ ] Each suggested editorial action is specific and actionable, not generic advice to "be careful"
- [ ] The subject's right of reply is noted where relevant (or flagged as absent where it matters)
- [ ] The summary makes a clear pre-publication recommendation

## Example

### Input
**Draft text:**
"Three former employees told us that Marcus Delacroix, the finance director, had been systematically falsifying expense reports for at least two years. The company denied any wrongdoing when approached, but declined to address the specific allegations. Sources say Delacroix is also known to have a drinking problem that affects his work. His deputy, Carla Voss, is widely regarded in the industry as incompetent. The CEO confirmed that an internal audit is underway, but described it as 'routine'."

**Jurisdiction:** England and Wales

### Output
**Libel Risk Report**

1. **"had been systematically falsifying expense reports for at least two years"**
   Flagged text: *"Marcus Delacroix, the finance director, had been systematically falsifying expense reports for at least two years."*
   Concern: This is stated as established fact, not allegation. If it cannot be proven to the civil standard of proof, this sentence is high-risk. The denial from the company is noted but the specific allegation is not attributed to named sources — only "three former employees."
   Risk level: **High**
   Suggested action: Rewrite as allegation rather than fact ("three former employees allege that…"). Confirm whether sources are willing to be named. If not, consider whether anonymous sourcing is sufficient to support publication. Seek legal advice before publishing.

2. **"Sources say Delacroix is also known to have a drinking problem that affects his work."**
   Concern: This is a serious personal allegation — implying unfitness for his role — attributed to unnamed "sources." It is not connected to any documented incident, formal complaint, or on-the-record account. In England and Wales, truth is a full defence to defamation, but the burden of proof lies with the publisher. If this cannot be substantiated, it should not be published.
   Risk level: **High**
   Suggested action: Remove unless you have documented evidence (medical records, disciplinary records, on-the-record eyewitness accounts). If there is supporting evidence, consult a lawyer about how to publish it safely.

3. **"His deputy, Carla Voss, is widely regarded in the industry as incompetent."**
   Concern: "Incompetent" is a factual-sounding claim capable of damaging a professional reputation. "Widely regarded" implies general consensus but provides no evidence for it. Carla Voss does not appear to have been approached for comment, which weakens any public-interest defence.
   Risk level: **Medium**
   Suggested action: Either remove this sentence, or provide the evidential basis (e.g., cite specific failures, name sources), and give Voss a right of reply. If this is meant as editorial opinion, it must be clearly framed as such.

4. **"The company denied any wrongdoing when approached, but declined to address the specific allegations."**
   Concern: Not a defamation risk in itself — publishing a denial is standard practice. However, the company's specific denial should be quoted accurately, not paraphrased. If you have a written denial, quote it directly. If their response was verbal, note that.
   Risk level: **Low**
   Suggested action: Replace with a direct quote from the company's response, or note clearly whether it was written or verbal.

5. **"described it as 'routine'"**
   Concern: If the CEO's use of the word "routine" is in quotation marks, confirm this is a verbatim quote, not a paraphrase. Misquoting a named source in a context that implies a cover-up creates an additional legal exposure beyond defamation.
   Risk level: **Low**
   Suggested action: Verify the quote against your notes or recording. If it is a paraphrase, remove the quotation marks.

---

**Summary**
Total flags: 5
Risk breakdown: 2 High · 1 Medium · 2 Low
Overall recommendation: **Do not publish in current form.** The two High-risk passages — the expense-report allegation stated as fact, and the unsubstantiated personal allegation about drinking — require either stronger on-the-record sourcing or removal before this piece is ready for legal review. Send to a media lawyer with the High and Medium flags highlighted.

---

*This report is an editorial aid only. It identifies passages that warrant closer scrutiny. It is not a legal opinion and does not constitute advice from a qualified solicitor or attorney. Always consult a media lawyer before publishing material that carries legal risk.*

## Known Limitations
- This skill is not a substitute for qualified legal advice. A media lawyer must review any high-risk material before publication. No AI tool can replicate the judgment of a qualified legal professional or assess jurisdiction-specific case law.
- Defamation law differs significantly between countries. Flags are more accurate when you specify a jurisdiction; without one, the assistant applies general common-law principles.
- The assistant cannot assess whether your supporting evidence is sufficient to mount a truth defence — it can only flag that evidence would be needed.
- Satire, clearly labelled opinion, and privileged reporting (e.g., court reports, parliamentary proceedings) are subject to different rules. This skill may flag them unnecessarily if context is not provided.
- The assistant cannot contact subjects for a right of reply. That remains the editor's responsibility.

## Related Skills
- [libel-check-brief](../../magazine-journalism/legal/libel-check-brief/SKILL.md)
- [defamation-risk-checker](../../magazine-journalism/legal/libel-check-brief/SKILL.md)
- [unattributed-claims-checker](../unattributed-claims-checker/SKILL.md)
- [fact-check-prompt](../../magazine-journalism/editing/fact-check-prompt/SKILL.md)
