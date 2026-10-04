---
name: sensitive-data-anonymization-gate
description: Use before sensitive, clinical, identifying, or raw interview data is placed in front of an AI tool, when transcripts or student materials need de-identification, or when a data-minimization gate must run before any analysis or drafting.
---

# Sensitive Data Anonymization Gate

## When to use

Use this skill before any sensitive, clinical, or identifying material — interview transcripts, clinical notes, student texts, field notes, or raw participant data — is shared with an AI tool or processed for analysis. It is the required gateway before qualitative-coding-discipline handles the de-identified copy, before open-science-release-packager packages shareable derivatives, and before statistical-consultation-protocol receives any individual-level data. Run it also when consent scope must be checked against the intended processing, or when GDPR, KVKK, or IRB conditions impose data-minimization obligations. It is not for anonymizing already-public data or for a simple name-removal pass that is then treated as complete de-identification.

## Inputs

- The data type and sensitivity level: clinical notes, interview transcript, student work, field log, survey responses.
- The consent scope as stated in the participant information sheet or ethics approval.
- Ethics board conditions that constrain processing, sharing, or retention.
- The data fields and their contents, or a representative excerpt for risk assessment.
- The intended downstream use: AI-assisted coding, statistical analysis, open-science release, or drafting.
- Country and institutional context that determines the applicable privacy regulation.

## Workflow

1. Classify the data type and its sensitivity tier before any content is read by an AI tool.
2. Extract or mask all direct identifiers: names, institutional affiliations, unique role descriptors, dates tied to individuals, contact details.
3. Audit for indirect identifiers that remain re-identifying in combination: rare occupation, small institution, geographic locality, distinctive event, unusual demographic pairing.
4. If a linkage key is needed to reconnect the anonymized copy with the original, record it in a separate, access-restricted file and never in the working copy.
5. Write the safe working copy to a location distinct from the raw source; record the file path, the date, and the anonymization decisions made.
6. Minimize the fields shared with the AI tool to those strictly required for the downstream task.
7. Produce an anonymization report and a human-review note flagging any residual risk that requires a decision the AI cannot make.
8. After the gate, hand the safe copy to qualitative-coding-discipline, statistical-consultation-protocol, or open-science-release-packager as appropriate; route ethics questions to ethics-irb-ai-protocol; hand persistent identifier records to source-passport-ledger.

## Output

Return:

- An anonymization report naming every direct identifier removed or masked, and every indirect identifier assessed.
- A masking table mapping the original field to its anonymized form, held separately from the working copy.
- A residual-risk list of indirect identifiers that remain and the rationale for retaining them.
- The safe working copy with a header stating its anonymization date, data type, and consent scope.
- A list of fields that must not be shared with any AI tool, with reasons.
- A human-review note marking decisions that require researcher or ethics-board judgment rather than AI processing.
- What to record at session end: the input data type and consent scope used, the path of the safe working copy, any decisions still awaiting human sign-off, and the handoff destination skill with its rationale.

## Verification

- Anonymization was not treated as complete after name removal alone; indirect identifiers were audited.
- The linkage key, if produced, is stored separately from the safe working copy.
- Consent scope was checked before processing; if the intended use falls outside that scope, the gate halted and flagged rather than proceeding.
- The AI tool received only the safe working copy, never the raw source.
- The anonymization report is traceable: every masked field has an entry explaining what was removed and why.
- Before closing: a researcher has reviewed the residual-risk list and confirmed the safe working copy is fit for the intended downstream use, and the anonymization decision log is archived with the project.

## Safety

Anonymization is not the removal of names alone; it is the reduction of any combination of features that makes an individual recognizable in context. Raw participant data, clinical notes, and student materials never reach an AI tool before this gate runs. Processing without consent is not remediated by anonymization after the fact — if consent scope does not cover the intended use, the gate stops and the researcher contacts the ethics board. AI contribution at this stage is confined to pattern detection and draft reports; every risk classification and every release decision belongs to the human researcher. AI involvement must be traceable: log the stage at which it was used, the model, what it contributed, and what human review confirmed afterward.

## Example prompt

"Bu mülakat dökümleri setini yapay zekâ destekli nitel kodlamaya göndermeden önce anonimleştirme kapısından geçir. Doğrudan ve dolaylı kimlik bilgilerini, maskeleme kararlarını, güvenli çalışma kopyasını ve modellerle paylaşılmaması gereken alanları raporla."

Expected smoke output:

- A sensitivity classification for the transcript set, with direct identifiers listed and masked.
- An indirect-identifier audit noting any re-identification risks from occupation, location, or event combinations.
- A safe working copy with a dated anonymization header and a residual-risk note.
- A human-review flag on any field where the researcher must decide before the copy is passed to qualitative-coding-discipline.

## Türkçe kullanım notu

Bu beceri, hassas materyalin — mülakat dökümü, klinik not, öğrenci metni, saha kaydı — herhangi bir yapay zekâ aracına ulaşmadan önce geçmesi gereken zorunlu kapıdır. Anonimleştirme yalnızca isim silmek değildir — kişiyi bağlamında tanınabilir kılan her özellik bileşimi bu kapıda değerlendirilir. Sık düşülen hata dolaylı kimlik bilgilerini — nadir meslek, küçük kurum, coğrafi yakınlık, kendine özgü olay — göz ardı etmektir. Onam kapsamı kontrol edilmeden işleme başlanmaz. Kullanım, onam sınırını aşıyorsa beceri ilerlemez — araştırmacıyı etik kurula yönlendirir. Güvenli çalışma kopyası ham kaynaktan ayrı bir klasörde tutulur, bağlantı anahtarı varsa ayrı erişime kapalı bir dosyada saklanır. İnsan kararı son noktadır — artık risk listesi ve her maskeleme kararı araştırmacı tarafından onaylanır. Nitel kodlama için qualitative-coding-discipline, açık bilim paketi için open-science-release-packager, etik kurul soruları için ethics-irb-ai-protocol'e devir bu kapının çıkışında gerçekleşir.
