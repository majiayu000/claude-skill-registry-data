---
name: ai-privacy-pii-compliance
description: Review an AI system's compliance with GDPR, CCPA, and sector-specific privacy regulations — covering lawful basis for AI processing, PII in training data and prompts, data subject rights in AI contexts, automated decision-making disclosure requirements, and cross-border model API transfers.
last_reviewed: 2026-04-29
---

# AI Privacy and PII Compliance

## First Principle

**An AI system that processes personal data is subject to privacy law. The model does not know what GDPR is. Your application does, and must enforce it.**

LLMs process personal data in two ways that traditional software does not: they ingest it during training (creating a statistical encoding in model weights), and they process it at inference time in ways that are difficult to audit, bound, or reverse. Privacy regulations designed for structured databases — where "delete this record" has a clear implementation — do not map cleanly onto model training. But the legal obligations still apply, and regulators are increasingly enforcing them on AI systems.

## Attack Mental Model

Privacy compliance failures in AI systems typically follow three patterns:

1. **Unintended PII ingestion** — personal data enters the training pipeline or RAG corpus without classification, resulting in model memorization or retrieval of PII that was never intended to be accessible.
2. **Cross-border data transfer** — prompt data containing personal data of EU residents is sent to a model API hosted in a jurisdiction without an adequacy decision or appropriate safeguards, violating GDPR Article 46.
3. **Automated decision-making without disclosure** — the AI system makes or significantly influences decisions about individuals (credit, hiring, healthcare) without the disclosures required by GDPR Article 22 or CCPA.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every AI processing activity involving personal data has a documented lawful basis, data subject rights procedure, and retention limit — reviewed by legal before production. |
| **Scope** | PII classification runs on all data entering the AI pipeline: training data, RAG corpus, prompt templates, and user inputs. Classified PII is handled according to its sensitivity tier. |
| **Isolate** | Personal data of EU residents is processed only in jurisdictions with adequacy decisions or under SCCs — and only by model APIs whose data processing terms explicitly cover GDPR compliance. |
| **Enforce** | Data subject rights (access, deletion, correction) are implementable within the response timelines required by applicable law — with a documented procedure for each right. |

## APC.1 Lawful Basis, Data Classification, and Cross-Border Transfers

**The core vulnerability:** Teams deploy AI systems that process personal data without identifying the lawful basis for processing under GDPR Article 6. "Legitimate interests" is frequently claimed without a legitimate interests assessment (LIA). Consent, where required, is often not obtained before AI processing begins.

### Check

- Has a Data Protection Impact Assessment (DPIA) been completed for AI processing activities that involve personal data, automated decision-making, or large-scale processing?
- Is the lawful basis for each AI processing activity documented — and is the documentation current, not a one-time artifact from the design phase?
- For EU personal data sent to non-EU model APIs: are Standard Contractual Clauses (SCCs) or another Article 46 mechanism in place — not just a general DPA?

### Action

- **Complete a DPIA for each AI processing activity.** The DPIA must cover: what personal data is processed, why, on what legal basis, what the risks to data subjects are, and what mitigations are in place. For AI systems, include: model training data sources, inference-time data processed, and any automated decisions made.

- **Build a data processing inventory for AI activities:**

```yaml
processing_activity: "customer_support_llm"
personal_data_categories: ["name", "email", "account_number", "support_history"]
data_subjects: ["customers", "prospective_customers"]
lawful_basis: "contract_performance"  # GDPR Art. 6(1)(b)
third_country_transfers:
  - vendor: "Anthropic"
    mechanism: "SCCs"
    scc_version: "2021"
    dpa_signed: true
retention_period: "session_only_no_training"
automated_decision: false
```

- **Verify SCCs for every third-party model API processing EU data.** SCCs alone may not be sufficient without a Transfer Impact Assessment (TIA) confirming that US law does not impair the protections the SCCs provide. Document the TIA.

### Failure Modes

- A chatbot processes health-related queries from EU residents. The team claims "legitimate interests" as the lawful basis without completing a LIA. Under GDPR, health data may require explicit consent (special category, Article 9).
- Prompt data containing EU resident names and account details is sent to a US-hosted model API. The vendor's DPA covers GDPR in general terms but does not include SCCs. The transfer is unlawful.

## APC.2 Data Subject Rights and PII in AI Outputs

**The core vulnerability:** GDPR grants data subjects the right to erasure (Article 17), access (Article 15), and rectification (Article 16). For a conventional database, these rights are implemented by deleting or updating rows. For a model trained on personal data, "erasure" is not straightforward — the data is encoded in weights across millions of parameters. This gap must be addressed procedurally and disclosed.

### Check

- Is there a documented procedure for responding to data subject access requests (DSARs) that covers all AI-processed personal data — including what is stored in prompt logs, retrieval indices, and model training data?
- Is there a documented position on model unlearning — specifically, whether the organization commits to retraining or fine-tuning to remove memorized personal data upon erasure request, and under what conditions?
- Does the application's privacy notice disclose AI processing — including automated decision-making, the categories of personal data processed, and any cross-border transfers?

### Action

- **Implement a DSAR response procedure for AI systems:**
  - Prompt logs: can be deleted from the audit log store within 30 days of receipt of a valid DSAR.
  - RAG index: documents containing the data subject's PII can be removed from the retrieval index and the document store within 30 days.
  - Model weights: disclose the organization's position. If the model was trained on data that included the subject's PII, state that retraining is not feasible for individual erasure requests and document the alternative safeguards (PII removal from training data before future training runs).

- **Scan AI outputs for incidental PII disclosure.** Model outputs can contain personal data from training memorization or retrieval. Run output through a PII detector before delivery:

```python
import presidio_analyzer

analyzer = presidio_analyzer.AnalyzerEngine()

def scan_output_for_pii(output: str) -> list[dict]:
    results = analyzer.analyze(text=output, language="en")
    return [
        {"entity_type": r.entity_type, "start": r.start, "end": r.end, "score": r.score}
        for r in results if r.score > 0.7
    ]
```

Alert and redact when high-confidence PII is detected in output.

- **Update the privacy notice to disclose AI processing.** The notice must describe: that AI is used, what categories of personal data are processed, whether automated decision-making occurs, and data subjects' rights in relation to AI processing. Vague language ("we use advanced technology") is insufficient under GDPR.

### Minimum Deliverable Per Review

- [ ] DPIA: completed for each AI processing activity involving personal data
- [ ] Data processing inventory: lawful basis, third-country transfer mechanism, and retention period per activity
- [ ] SCC/TIA documentation: for each non-EEA model API processing EU data
- [ ] DSAR procedure: documented response steps for prompt logs, retrieval index, and model weights
- [ ] Output PII scanning: automated detection on all model responses before delivery
- [ ] Privacy notice: updated to disclose AI processing, automated decision-making, and cross-border transfers

## Quick Win

**Run Presidio (or equivalent) on a sample of your model's outputs today.** Take 100 recent responses from your production logs and run them through a PII detector. If any contain names, email addresses, phone numbers, or account identifiers that the user did not provide in their query, you have an incidental disclosure issue that requires investigation.

## References

- PII in RAG systems → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Data leakage controls → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Third-party vendor DPA requirements → [third-party-model-risk/SKILL.md](../third-party-model-risk/SKILL.md)
- Audit logging for compliance → [ai-audit-logging/SKILL.md](../ai-audit-logging/SKILL.md)
- Model memorization and inversion → [model-inversion-membership-inference/SKILL.md](../model-inversion-membership-inference/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
