---
name: dsgvo-ai-act-labeling
description: "Apply GDPR workflows and EU AI Act Article 50 disclosure decisions for Ottili flows: processing register entries, human-review evidence and AI labeling. Use when an agent must classify a data processing activity under GDPR, decide whether an AI system requires an Article 50 disclosure with human-review evidence, or update the processing register. Not for general privacy policy or non-EU AI systems."
license: MIT-compat
compatibility: "framework-agnostic; GDPR Art. 30/6, EU AI Act Art. 50; offline validation"
metadata: {}
allowed-tools: []
---

# dsgvo-ai-act-labeling

## When to use this skill

Use this skill when an agent must sort a data processing activity into its
GDPR bucket, work out whether an AI system triggers an EU AI Act Article 50
disclosure that needs human-review evidence, or keep the GDPR processing
register up to date for Ottili flows. Do **not** use it for general privacy policy text, non-EU AI
systems, or member-state-specific law beyond the EU baseline.

## Procedure

1. **GDPR gate.** Capture controller, purpose, data subjects and categories,
   recipients, retention and security measures (Art. 30(1)). Even an activity
   with no personal data gets an entry, marked `personal_data: false`, so the
   decision is auditable. Exactly one Art. 6(1) legal basis per activity; the
   script rejects bases it does not recognise.
2. **Register.** Append the entry to the JSONL register. Editing an entry in
   place breaks GoBD immutability, so never do it. When something changes,
   append a fresh entry with a new `recorded_at` and a note that points at the
   entry it supersedes.
3. **AI Act gate.** Run four gates in order: (1) no AI → not-ai, no Art. 50;
   (2) transparency-only (chatbot, emotion-recognition, deep-fake,
   biometric-categorization) → Art. 50(1)-(4) disclosure with human review;
   (3) high-risk / Annex III (Art. 6) → Art. 50(5), human review mandatory
   together with an evidence file whose digest the script computes; (4)
   general AI → Art. 95, document only. Unknown `ai_type` blocks rather than
   inventing a class.
4. **Human-review evidence.** Record `reviewer_id`, an ISO-8601 `reviewed_at`
   and `evidence_path`. For high-risk the file must exist when the label is
   produced and the label carries its `sha256` digest. A review has to name the
   system, the risk class and the mitigations checked — a checkbox with no
   content behind it counts as missing.
5. **Label and store.** Emit the machine-readable label next to the system
   artefact. Re-run classification on every material change and every release
   cycle; a label emitted for v1 is not valid for v2.

## Decision tables

### AI Act risk classes

| ai_type | Risk class | Art. 50 | Human review |
|---|---|---|---|
| `none` | not-ai | not required | n/a |
| `chatbot`, `emotion-recognition`, `deep-fake`, `biometric-categorization` | transparency-only | 50(1)-(4) | required |
| `high-risk` / Annex III (Art. 6) | high-risk | 50(5) | required, evidence file mandatory |
| anything else | general | not required | not required |

### GDPR legal bases (Art. 6(1))

| Key | Label |
|---|---|
| `art6_1a_consent` | Consent (Art. 6(1)(a)) |
| `art6_1b_contract` | Contractual necessity (Art. 6(1)(b)) |
| `art6_1c_legal` | Legal obligation (Art. 6(1)(c)) |
| `art6_1d_vital` | Vital interests (Art. 6(1)(d)) |
| `art6_1e_task` | Public task (Art. 6(1)(e)) |
| `art6_1f_legit` | Legitimate interests (Art. 6(1)(f)) |

## Pitfalls from research

- **Never auto-approve high-risk.** A missing evidence file blocks the label;
  the script raises and the agent must not bypass it.
- **Transparency-only systems still need human review.** A chatbot label with
  no reviewer is rejected, not warned.
- **Re-run classification on material change.** A label emitted for v1 is not
  valid for v2; re-verify on every release cycle.
- **Inherit GoBD retention from `gobd-archive`.** Label artefacts are business
  records under HGB/AO; coordinate retention timing with that skill.
- **Member-state additions are unverified.** Germany (BDSG), France and the
  Netherlands may add requirements beyond the EU baseline; flag them until
  local counsel confirms.

## Verification checklist

- [ ] Processing activity classified; personal data present or not
- [ ] Art. 30 entry complete; legal basis valid
- [ ] Register is append-only; never edited in place
- [ ] AI Act gate run; risk class determined
- [ ] High-risk label has reviewer, date and evidence file with checksum
- [ ] Transparency label has reviewer and date
- [ ] Label re-verified on release change; no stale reuse
- [ ] Retention inherited from gobd-archive

## Near-miss triggers (stop and re-read)

- "I'll auto-approve this high-risk label" → BLOCKING; evidence file required.
- "A chatbot doesn't need a reviewer" → transparency-only still requires one.
- "The label from v1 is still valid" → re-run on every release cycle.
- "BDSG doesn't apply to us" → member-state additions are unverified until
  local counsel confirms.


## Related skills

[gobd-archive](../gobd-archive/) — processing-register entries and human-review evidence are correspondence (6y)

## References

- [Procedures, worked examples and AI Act summaries](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
- [Scripts](scripts/)

## Worked examples

### Good output — no-AI system, no disclosure
Input: `invoice-export` with `ai_type: "none"`, a plain export script.
`scripts/disclosure_label.py --system system.json` emits:
`{"system": "invoice-export", "risk_class": "not-ai",
"article_50_required": false, "human_review_status": "n/a",
"label": "no-ai-act-scope"}` and exits 0. No reviewer, no evidence file.
The decision is recorded so the Art. 30 register can show why no label was
needed.

### Bad output — transparency chatbot with no reviewer
Input: `support-bot` with `ai_type: "chatbot"` and an empty
`human_review` block.
`scripts/disclosure_label.py` exits 2 with:
`transparency system 'support-bot' requires human-review evidence`
Fix: add `reviewer_id` and an ISO-8601 `reviewed_at`. A chatbot is
transparency-only under Art. 50(1)-(4) and still needs a human reviewer —
the label is not optional just because the risk class is low.

### Good output — chatbot label with reviewer
Input: `support-bot`, `ai_type: "chatbot"`, reviewer `ops-1`,
`reviewed_at: "2026-10-09T10:00:00Z"`, no evidence file.
The label carries `risk_class: "transparency-only"`,
`article_50_paragraph: "1-4"`, `human_review_status: "approved"`,
`label: "article-50-disclosure"`. Exit 0.

### Bad output — high-risk auto-approved without evidence
Input: `recruiter-ai` with `ai_type: "high-risk"`, reviewer set, but no
`evidence_path` and no evidence file.
`scripts/disclosure_label.py` exits 2 with:
`high-risk system 'recruiter-ai' BLOCKING: human-review evidence missing`
Fix: produce the evidence file (the documented review record naming the
system, the risk class and the mitigations checked) and re-run. A high-risk
label with no evidence file is never issued — the script blocks, and the
agent must not bypass the block.

### Good output — high-risk label with checksummed evidence
Input: `recruiter-ai`, `ai_type: "high-risk"`, reviewer `lawyer-1`,
`reviewed_at: "2026-10-09T11:00:00Z"`, `evidence_path: "review-1.md"`.
The label carries `risk_class: "high-risk"`, `article_50_paragraph: "5"`,
`evidence_sha256: <digest of review-1.md>`, `retention_years: 10`,
`human_review_status: "approved"`. The digest lets an auditor re-derive the
file's identity without re-running the classification.

### Bad output — unknown ai_type classified as general AI
Input: `fraud-detector` with `ai_type: "fraud-detection"`, a real system
that is neither in the transparency set nor marked `high-risk`.
`scripts/disclosure_label.py` exits 2 with:
`unknown ai_type 'fraud-detection' for system 'fraud-detector'; choose from
none, ['biometric-categorization', 'chatbot', 'deep-fake',
'emotion-recognition'], high-risk, 'Annex III high-risk (Art. 6)', general`
Fix: decide the risk class explicitly (it may well be Annex III — fraud
screening is a candidate) and set `ai_type` accordingly. Never let an
unknown type fall through to "general AI": that silently documents a
decision nobody made.

### Good output — general AI documented, not disclosed
Input: `report-ml` with `ai_type: "general"`, an internal analytics model.
The label carries `risk_class: "general"`, `article_50_required: false`,
`article_95_documented: true`, `human_review_status: "not-required"`,
`label: "ai-act-general"`. Exit 0. The decision is documented under Art. 95
even though no disclosure label is emitted.

### Bad output — label from v1 reused for v2
Input: the v1 label for `recruiter-ai` is copied unchanged when the model is
retrained to v2.
The skill rejects this: a label emitted for v1 is not valid for v2.
Re-run `scripts/disclosure_label.py` on every material change and every
release cycle; re-verify the evidence file's checksum, since the review may
no longer describe the new model.

### Good output — entry superseded, never edited
Input: the retention period for an activity changes from 6y to 10y.
The register is append-only: a new entry is appended with a fresh
`recorded_at` and a `supersedes` note pointing at the earlier entry id.
The earlier line is never modified. `scripts/process_register.py` always
sets `recorded_at` from `datetime.now(timezone.utc)` — it never copies the
caller's timestamp, so a caller-supplied `recorded_at` cannot fake the
audit trail.
