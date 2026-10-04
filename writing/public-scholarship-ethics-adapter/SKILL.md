---
name: public-scholarship-ethics-adapter
description: Use when adapting academic findings for a public audience (op-ed, social post, podcast) and the simplification must stay evidence-faithful, avoid overclaiming, respect embargoes, and disclose AI assistance.
---

# Public Scholarship Ethics Adapter

## When to use

Use this skill when a journal article, dissertation chapter, or research report is being rewritten for a public-facing format — op-ed, blog post, social media carousel, press release, podcast script, or short magazine column — and the translation from academic to accessible language must not inflate the claim strength, flatten the study's limitations, or misrepresent what was actually found. It also applies when mental-health, minority, or other sensitive-community topics require particular care about stigma, labelling, or crisis-adjacent language. It is not for presenting academic findings as a clinical prescription, for asserting causal conclusions from correlational data, for writing in the voice of a medical authority the author does not hold, or for publishing under embargo without the journal's permission.

## Inputs

- The source academic text or a clear summary of its main findings.
- The target audience's knowledge level and likely prior beliefs about the topic.
- The publication channel and its format constraints.
- The list of original sources that underpin the claims.
- The required tone — explanatory, persuasive, narrative, or dialogic.
- Any sensitivity flags: mental health, political minority, clinical population, ongoing legal matter, pre-publication embargo.

## Workflow

1. Extract the study's main finding, the population it applies to, and the explicit limitations the authors stated.
2. Map the original claim strength — association, correlation, causal inference, replication, meta-analytic consensus — and set a ceiling: the public text may not claim more than the source warrants.
3. Flag any place where simplification would convert an association into a cause, a sample finding into a universal truth, or a preliminary result into settled science.
4. For mental-health or sensitive-community content, check for diagnostic language, prescriptive advice, stigmatising framing, or absent crisis-support signposting.
5. Rebuild the text in the target format and channel register, keeping the essential hedges intact while removing jargon.
6. Verify that every source cited in the public text appears in the original source list and that what the public text attributes to it is what the source actually says; route to apa-doi-verifier if any citation needs confirmation.
7. Draft the AI-use disclosure covering stage, model, contribution level, and human review.
8. If the adapted piece will also appear in another language or at a conference, hand off to conference-materials-bilingual.

## Output

Return:

- The adapted public-facing text in the requested format and channel register.
- A claim-strength audit noting every place where simplification was moderated and why.
- A source-fidelity note listing which original claims were kept, which were softened, and which were omitted and why.
- A sensitivity flag list: any remaining risk of overclaiming, stigmatising, crisis-adjacent language, or embargo violation.
- An AI-use disclosure draft for the author to review and sign.
- What to record at session end: the output file path, the open editorial decisions still requiring the author's judgment, and the handoff to ai-disclosure-auditor before the piece is published.

## Verification

- No claim in the public text exceeds the evidence level in the source material.
- Every source cited is in the original reference list; none is paraphrased beyond what the source actually states.
- Mental-health content carries no diagnostic assertion and includes a crisis-support signpost where the topic warrants it.
- The embargo status has been confirmed; nothing is published before the journal's release date.
- Before closing: an academic author, not only an AI, has reviewed the adapted text and the claim-strength audit, and the AI-use disclosure is drafted and ready for journal-fit-screening or ai-disclosure-auditor.

## Safety

Simplifying language does not reduce the researcher's responsibility for what is claimed: the author's name goes on the piece, and a public overclaim can mislead far more people than a journal article ever reaches. Mental health content must never diagnose, prescribe, or imply a universal solution; when the subject touches crisis risk, a referral to appropriate professional support is mandatory, not optional. AI may draft the adaptation, but the academic author reviews and approves every claim before publication. Source fidelity is a binary — either the public text represents what the study found, or it does not. Route to apa-doi-verifier for any reference that needs verification. The completed output goes to ai-disclosure-auditor before any submission. For bilingual or conference versions, route to conference-materials-bilingual.

## Example prompt

"Bu psikoloji araştırmasının bulgularını, Instagram'da yayınlanacak 6 slaytlık bir karoseye uyarla. Hedef kitle ebeveynler. Ruh sağlığı etik sınırlarını, kaynak sadakatini ve aşırı iddia risklerini ayrı bir raporla göster."

Expected smoke output:

- A six-slide script adapted for an Instagram carousel, with claim-hedging language preserved and jargon removed.
- A claim-strength audit noting which study limitations were carried forward and where the original wording was moderated.
- A sensitivity note flagging any slide that touches mental-health labelling or prescriptive language, with a suggested revision.
- An AI-use disclosure draft covering stage, model, contribution level, and the author's pending review.

## Türkçe kullanım notu

Bu beceri, akademik bulguyu kamuya aktarırken bilimsel dürüstlüğü korur. Sadeleştirmek, iddianın sorumluluğunu azaltmaz — o sorumluluğu yalnızca daha anlaşılır bir dile taşır. Kaynak metindeki korelasyon, kamu metninde nedenselliğe dönüşmez. Ön çalışma, yerleşik bilim gibi sunulamaz. Ruh sağlığı konularını içeren uyarlamalarda tanı koyulmaz, reçete sunulmaz, topluluk karikatürleştirilmez. Konu krize yakın bir zemine değdiğinde psikolojik danışmanlık ya da acil destek yönlendirmesi zorunludur. Bu bir tercih değil, asgari koşuldur. Ambargo süresi dolmadan hiçbir materyal yayınlanmaz. Yapay zekâ taslağı hazırlar, ancak akademisyen her iddiayı gözden geçirir ve onaylar — kamuya çıkan metin araştırmacının adını taşır. Atıf doğrulaması gereken kaynaklar apa-doi-verifier'a, yayın öncesi beyan ai-disclosure-auditor'a devredilir. Çok dilli ya da konferans versiyonu gerekiyorsa conference-materials-bilingual devreye girer.
