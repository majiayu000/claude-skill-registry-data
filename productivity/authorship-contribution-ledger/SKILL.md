---
name: authorship-contribution-ledger
description: Use when authorship order, CRediT contribution roles, or AI-assistance attribution must be recorded transparently for a manuscript, when an author dispute needs an evidence trail, or before a contributorship statement is required at submission; this skill maintains the human-attribution ledger of who contributed what and in which role (authorship order, CRediT taxonomy, revision responsibilities), which is distinct from the disclosure-metadata audit owned by ai-disclosure-auditor.
---

# Authorship Contribution Ledger

## When to use

Use this skill at the start of a multi-author project and update it at every major milestone, so that authorship order and CRediT roles are established on evidence rather than negotiated in the submission week. It is also the right tool when an existing collaboration needs a retrospective contribution audit, when a rebuttal round introduces new writing responsibilities that shift contribution balance, or when a journal's submission system requires a structured contributorship statement. Its output feeds directly into ai-disclosure-auditor, which needs the AI-use log the ledger maintains, and into open-science-release-packager, which needs the CRediT table for the README. Route ethics questions that arise from the contribution record to ethics-irb-ai-protocol. It is not a performance-management instrument and must not be framed as one; it records contributions for transparency, not for evaluation.

## Inputs

- Team members and their institutional affiliations.
- Roles discussed or assigned at project outset, even if informally.
- The task list: study design, data collection, instrument development, analysis, interpretation, writing, reviewing, supervision, funding acquisition.
- File-change history or version-control logs where available.
- Notes on AI-tool use: which tool, at which stage, for which contribution type, and what human review followed.
- The authorship-order principle agreed by the team: contribution-ranked, alphabetical, seniority-convention, or journal-mandated.
- Revision rounds and who took responsibility for responding to each reviewer.

## Workflow

1. At project start, write the role and expectation for each team member before any task begins; this becomes the baseline the ledger is checked against.
2. For each major task, record the lead contributor, the contribution type using CRediT taxonomy, the output artifact, and the date.
3. Log AI-tool use as a distinct contribution type separate from human authorship: record the tool, the stage, the contribution category (e.g., Writing — draft, Formal analysis — code generation), and the human review step that followed.
4. Update the ledger at each milestone: data collection complete, analysis complete, first draft complete, revision submitted.
5. Before submission, draft the authorship-order rationale using the ledger record, not from memory or seniority assumption alone.
6. Produce the CRediT table mapping each author to their taxonomy roles, and a separate AI-use summary for ai-disclosure-auditor.
7. If a disagreement arises, use the ledger as the shared factual ground for the conversation rather than adjudicating it through the ledger itself.

## Output

Return:

- A contribution log with columns for task, lead contributor, contribution type (CRediT), output artifact, date, and notes.
- A CRediT table ready for journal submission, with each author mapped to their roles using the fourteen-category taxonomy.
- An authorship-order discussion note stating the agreed principle and the evidence from the ledger that supports the proposed order.
- An AI-use contribution record distinguishing AI-assisted work from human authorship at the task level, formatted for handoff to ai-disclosure-auditor.
- A pre-submission contributorship statement drafted in the format the target journal specifies.
- A revision responsibility matrix recording which author responded to which reviewer comments, for use if authorship questions arise after submission.
- What to record at session end: the current state of the contribution log, any authorship-order question still unresolved and the agreed next step, the handoff to ai-disclosure-auditor with the AI-use record, and the handoff to open-science-release-packager with the CRediT table.

## Verification

- Every team member has reviewed and confirmed their own contribution entries before the ledger is used for submission.
- AI-tool contributions are logged separately and are not attributed to any human author in the CRediT table.
- The authorship-order rationale cites specific ledger entries rather than seniority or assumption alone.
- The CRediT table uses the fourteen standard taxonomy categories without invention of new ones.
- No contribution category is left blank for an author listed in the author line; if a category was not applicable, that is stated explicitly.
- Before closing: the pre-submission contributorship statement has been reviewed by all authors, and the AI-use record has been passed to ai-disclosure-auditor for the manuscript's disclosure section.

## Safety

Authorship is an ethical responsibility, not a technical file-management task. The ledger creates transparency; it does not make authorship decisions. AI tools do not meet authorship criteria under ICMJE or equivalent standards — they may be acknowledged but must not appear in the author line. The ledger must not be used as a surveillance or performance tool; its purpose is shared clarity, not accountability enforcement. If a dispute cannot be resolved using the ledger record, the appropriate next step is institutional research-integrity guidance, not further AI processing. Every entry in the ledger requires a human to confirm it; the AI drafts the structure and populates it from provided information, but no entry is finalized without researcher review.

## Example prompt

"Bu çok yazarlı proje için ortak yazarlık ve katkı izleri defteri oluştur. Ekip üyelerini, görevleri ve CRediT rollerini, yapay zekâ katkısını ayrı bir alan olarak, yazar sırası gerekçesini ve gönderim öncesi katkı beyanını planla."

Expected smoke output:

- A contribution log table covering each major task with lead contributor, CRediT role, output artifact, and date columns.
- A CRediT table mapping each author to their fourteen-taxonomy roles, with AI-tool use recorded separately.
- An authorship-order discussion note citing ledger evidence for the proposed order.
- A pre-submission contributorship statement and a reminder to pass the AI-use record to ai-disclosure-auditor before finalizing the manuscript's disclosure section.

## Türkçe kullanım notu

Ortak yazarlık, makale gönderim haftasında değil projenin başında konuşulur — bu beceri tam da bunu mümkün kılar. Katkı günlüğü, CRediT tablosu ve yazar sırası gerekçesi proje boyunca güncellenerek tutulur, böylece anlaşmazlık çıktığında tartışma bellekten değil kayıttan yürütülür. Yapay zekâ katkısı ayrı bir alan olarak girilir, hiçbir koşulda insan yazarlığıyla aynı satıra konmaz — ICMJE ve eşdeğer standartlar yapay zekânın yazar olarak listelenmesine izin vermez. Beceri bir denetleme aracı değildir, şeffaflık için vardır. Katkı kaydı kişi değerlendirmesine dönüştürülmez, katkıları tartışmak için paylaşılan olgusal zemin işlevi görür. Gönderim öncesi CRediT tablosu ai-disclosure-auditor'a, açık bilim paketi için de open-science-release-packager'a devredilir. Kurumsal araştırma-bütünlüğü kanalına gidilmesi gereken anlaşmazlıklarda beceri içinde çözüm aranmaz — beceri sınırını tanır ve araştırmacıyı doğru kuruma yönlendirir.
