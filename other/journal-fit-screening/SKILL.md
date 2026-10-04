---
name: journal-fit-screening
description: Use when choosing a journal for a finished or nearly finished manuscript, when index status in Scopus, SSCI, ESCI, or TR Dizin must be confirmed, when a venue looks predatory, or when a cover letter needs drafting from the manuscript's actual claims.
---

# Journal Fit Screening

## When to use

Use this skill when the manuscript exists and the question is where to send it. It covers scope matching, index verification, predatory screening, and the cover letter. It does not improve the manuscript itself; for that, return to the writing and verification skills first. It is not for managing authorship contributions or open-science release decisions; those belong to authorship-contribution-ledger and open-science-release-packager.

## Inputs

- The abstract and the contribution claims of the manuscript.
- The indexing requirement that actually binds the author: institution, graduation rule, or incentive system, naming the index.
- Open access budget, if any.
- Candidate journals already under consideration, if any.

## Workflow

1. Extract the manuscript's contribution claims and its method profile from the abstract, and write them as a short fit profile.
2. Build the candidate list from journal scope statements and recent tables of contents. A journal title is marketing, the scope statement and what it actually published last year are evidence.
3. Verify index status in the index's own master list for the current year. Scopus, Web of Science, and TR Dizin each publish authoritative lists, and a journal's webpage claim is never sufficient.
4. Screen for predatory signals in the Think Check Submit discipline: a verifiable editorial board, transparent article processing charges, honest indexing claims, a real review timeline, and a publisher with a traceable record. Record the evidence behind each flag.
5. Rank the surviving candidates by fit, with the reason stated per journal: scope match, method fit, audience, timeline, cost.
6. Draft the cover letter from the fit profile. Every sentence in the letter must be supported by the manuscript, and the editor's name and journal scope reference must be current.
7. Record the screening evidence per journal so the decision can be audited later. When the selected journal requires open-access compliance or data sharing, hand the decision record to open-science-release-packager and flag any authorship order questions for authorship-contribution-ledger.

## Output

Return:

- The fit profile of the manuscript.
- A ranked candidate table with index status, verified in the index master list, cost, and fit reasons.
- Predatory screening notes with evidence per flag.
- A cover letter draft.
- The screening evidence record.
- What to record at session end: the ranked candidate table, any predatory flags with their evidence, the cover letter draft, and a one-line note for the AI-use disclosure.

## Verification

- Index status of every recommended journal was checked in the index's own current list, with the date of the check recorded.
- No journal is recommended on its self-description alone.
- Article processing charges are stated with their source.
- The cover letter contains no claim that is absent from the manuscript.
- Predatory flags are written as factual observations with evidence, never as bare accusations.
- Before closing: the screening evidence for every recommended journal is saved where the next session can find it, and any open-science or authorship obligations flagged by the selected journal have been routed to the appropriate skill.

## Safety

Index status comes only from the index's own current list, never from memory or the journal's webpage. Predatory screening output is a risk assessment for the author's decision, so keep its wording factual and evidence-bound. Submission itself, author agreements, and fee payments stay on the user's side.

## Example prompt

"Bu nitel çalışmayı Scopus kapsamında bir dergiye göndermem gerekiyor, üç aday belirle ve kapak mektubunu hazırla."

Expected smoke output:

- A fit profile and a ranked table of candidates with verified index status.
- Predatory screening notes for any flagged candidate.
- A cover letter skeleton built from the manuscript's claims.

## Türkçe kullanım notu

Bu beceri, bitmiş bir el yazması için dergi seçimini kanıta bağlar. Dizin durumu derginin kendi sayfasından değil dizinin güncel ana listesinden doğrulanır, Scopus, SSCI ve TR Dizin katmanları kurumunuzun gerçek şartına göre ayrıştırılır, şüpheli dergiler kanıtlı bayraklarla işaretlenir. Kapak mektubu el yazmasında olmayan hiçbir iddia içermez. Gönderim ve ücret işlemleri her zaman sizde kalır. Seçilen dergi açık erişim zorunluluğu veya veri paylaşımı gerektiriyorsa open-science-release-packager becerisi devreye girer.
