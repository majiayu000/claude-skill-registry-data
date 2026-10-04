---
name: ethics-irb-ai-protocol
description: Use when an ethics committee or IRB application involves AI anywhere in the pipeline, when KVKK, GDPR, or EU AI Act duties must be mapped to a study, or when consent and disclosure language about AI use needs drafting before submission.
---

# Ethics IRB AI Protocol

## When to use

Use this skill when a research project uses AI in recruitment, consent, data handling, coding, analysis, writing, supervision, or participant-facing interaction. During coding work, qualitative-coding-discipline enforces the data rules this protocol sets. It is not for anonymizing identifiable participant data before it enters an AI tool, that is sensitive-data-anonymization-gate.

## Inputs

- Research design.
- Participant population.
- Data types.
- AI use case.
- Jurisdiction or institution.
- Whether data are identifiable, pseudonymized, anonymized, or synthetic.
- Submission target, such as ethics committee, IRB, journal, or grant body.

## Workflow

1. Separate screening, research design, data processing, analysis, and writing uses of AI.
2. Identify participant risk, vulnerability, consent implications, and data sensitivity.
3. Apply data minimization, purpose limitation, access control, retention, and deletion rules.
4. Map regulatory layers, including local ethics rules, KVKK, GDPR, EU AI Act transparency duties, and publisher disclosure rules when relevant.
5. Define what data must never enter an AI system.
6. Draft the AI-use disclosure for methods, ethics application, consent form, and manuscript note.
7. Produce a protocol checklist with approval blockers.
8. When identifiable data are involved, hand the data preparation step to sensitive-data-anonymization-gate before any AI processing begins.

## Output

Return:

- AI use map.
- Data flow summary.
- Ethics and legal checklist.
- Consent language draft.
- Disclosure language draft.
- Data minimization rules.
- Approval blockers.
- Questions for the ethics committee.
- What to record at session end: the protocol checklist file, any approval blockers still open, and a note on which data categories were flagged for sensitive-data-anonymization-gate.

## Verification

- Identifiable clinical or participant data are not sent to AI tools by default.
- Consent language names AI involvement clearly when participant data are affected.
- Jurisdictional claims are marked as checklist guidance unless a legal source was verified.
- High-risk or participant-facing AI use is escalated for human approval.
- Disclosure language matches the actual workflow.
- Before closing: every approval blocker is explicitly listed, identifiable data needing pre-processing are handed to sensitive-data-anonymization-gate, and the checklist is saved where the ethics committee reviewer can find it.

## Safety

Do not provide legal advice as a final authority. Do not process raw clinical records, identifiable participant data, or institution secrets. Ask for anonymized summaries when examples are needed.

## Example prompt

"Create an ethics committee AI-use checklist for a qualitative interview study where anonymized transcripts may be coded with AI assistance."

Expected smoke output:

- Data flow, consent, minimization, disclosure, and human oversight sections.
- A clear rule that non-anonymized transcripts must not be uploaded to AI systems.
- Approval blockers for vulnerable populations or identifiable data.

## Türkçe kullanım notu

Bu beceri, yapay zekânın karıştığı bir araştırma için etik kurul ve veri koruma hazırlığını tek kontrol listesinde toplar. Hangi verinin hiçbir koşulda yapay zekâ sistemine giremeyeceği açıkça yazılır, onam ve beyan dili gerçek iş akışına göre taslaklanır, KVKK, GDPR ve AB Yapay Zekâ Yasası katmanları çalışmaya eşlenir. Hukuki kesinlik gereken yerde son söz kurula ve hukukçuya bırakılır. Kimlik içeren verinin yapay zekâ öncesi işlenmesi sensitive-data-anonymization-gate'e devredilir. Oturum sonunda onay engelleyen maddeler ve hangi veri kategorisinin anonimleştirme gerektirdiği kayda geçirilir.
