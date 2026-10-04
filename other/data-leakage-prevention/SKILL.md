---
name: data-leakage-prevention
description: Review an AI system for leakage of secrets, PII, tenant data, hidden prompts, embeddings, logs, traces, memory, evaluation sets, and training artifacts across languages, frameworks, and deployment models.
last_reviewed: 2026-04-27
---

# Data Leakage Prevention

## First Principle

**Data doesn't leak through breaches alone — it leaks through features working exactly as designed.**

The most dangerous leakage in AI systems is not caused by bugs. It is caused by features: retrieval that returns more than intended, logging that captures more than necessary, embeddings that encode more than expected, and training pipelines that reuse more than is safe. Every capability that makes the system smarter — retrieval, memory, personalization, observability — is also a potential leakage path. The question is not "can this system be hacked?" but "what does this system expose when it works correctly?"

## Attack Mental Model

Leakage in AI systems follows four primary patterns:

1. **Retrieval over-reach** — a semantically similar query retrieves documents from a different tenant, user, or classification level because the metadata filters are too loose or enforced only in application code
2. **Prompt reflection** — a user crafts input that causes the model to recite or rephrase its system prompt, internal context, or retrieved documents (effectively reading restricted data through the model's output)
3. **Observability pipeline exposure** — logs, traces, and analytics capture raw prompts, retrieved chunks, and model outputs that contain PII, secrets, or internal policy — and these streams are accessible to broader audiences than the system itself
4. **Training and evaluation data reuse** — production prompts, user interactions, or retrieved documents are collected into fine-tuning or evaluation datasets without sanitization, creating a long-lived copy of sensitive data outside normal access controls

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every piece of data — prompt, retrieved chunk, memory entry, log event, export, dataset — is checked for sensitivity and authorization fit before it is processed or stored. |
| **Scope** | Only approved users, tenants, sessions, and workflows can access specific classes of data. Scope is enforced at every hop: retrieval, prompt assembly, logging, analytics, training. |
| **Isolate** | A leakage at one layer cannot cascade through memory, observability, analytics, or training pipelines into broad disclosure. Each layer has independent access control. |
| **Enforce** | Redaction happens before storage, not after exposure. Deterministic pipelines — not model-layer instructions — apply masking, access policy, and retention rules. |

## Core Leakage Controls

### Data Inventory First

Before implementing any control, produce a sensitivity inventory:

| Data Type | Examples | Where It Flows | Sensitivity Level |
|---|---|---|---|
| PII | Names, emails, IDs | User input → prompts → logs → traces | High |
| Secrets | API keys, tokens | Config → prompts → logs | Critical |
| Business data | Internal docs, financials | RAG corpus → retrieved chunks → prompts | High |
| System prompts | Role instructions | System turn → model → potential reflection | Medium |
| Evaluation sets | Test cases, expected outputs | Dev datasets → model → potential memorization | Medium |

Map every copy path for each category. Leakage you do not trace is leakage you cannot prevent.

### Check

- Does every retrieval query enforce tenant, user, and document-class scope as a hard datastore filter — not as a prompt instruction?
- Is PII masked before retrieved chunks, tool results, or user inputs enter the prompt?
- Do logs and traces capture only redacted identifiers, not raw prompt content, raw retrieved chunks, or raw model output?
- Are fine-tuning and evaluation datasets sanitized before they leave the production data pipeline?

### Action

- **Trace every copy path.** Map: raw data → preprocessing → prompt → retrieval result → cache → model output → log → trace → analytics → training dataset. Every hop where sensitive data persists is a leakage surface.
- **Mask at ingestion, not at display.** Apply PII masking and sensitivity labeling when data first enters the pipeline — before it reaches retrieval, memory, or prompt assembly. Masking at display is too late; the data already persists in logs and caches.
- **Redact logs by default.** Log structured metadata — request IDs, template hashes, retrieval document IDs, tool names, policy outcomes, authorization results — not raw content. When debugging requires raw content, route it to a higher-security, shorter-retention audit log with stricter access control.

```python
# Wrong — raw content in standard logs
logger.info(f"Prompt: {assembled_prompt}, Response: {model_output}")

# Right — structured, redacted audit event
audit_log.record(
    request_id=req.id,
    prompt_template_hash=hash(template),
    retrieval_doc_ids=[c.id for c in chunks],
    policy_outcome="allowed",
    user_tenant=current_user.tenant_id,
)
```

- **Tenant isolation is a datastore-level control.** Memory stores, vector stores, caches, and observability views must enforce tenant boundaries in their query parameters. Relying on application-layer tenant filtering means a single bug in that layer breaks every tenant's isolation simultaneously.
- **Sanitize evaluation and fine-tuning datasets.** Before any production data is used in training or evaluation: strip PII, remove secrets, anonymize identifiers, obtain appropriate consent or apply appropriate legal basis, and quarantine the sanitized dataset from the production environment.

### What To Look For

- Secrets hardcoded in system prompts, few-shot examples, config files, or tool output templates
- PII flowing through logging, tracing, analytics, or prompt replay pipelines without masking
- Cross-session or cross-tenant memory accessible through vector similarity queries without scope filters
- Embeddings encoding more information than intended (embeddings of PII-containing text still encode that PII)
- Summaries or condensations that distill sensitive information from a broader document and surface it to users who could not access the full document
- Hidden prompts or internal documents reflected back through model output in response to crafted inputs

### Minimum Deliverable Per Review

- [ ] Sensitive data inventory by type, classification, and flow path
- [ ] Leakage surface map by component: retrieval, prompt assembly, output, logs, traces, memory, analytics, training
- [ ] Unauthorized visibility matrix: which users/tenants can reach which data under which conditions
- [ ] Remediations: redaction pipeline, access control gaps, retention policy, egress controls

## Quick Win

**Audit your logging pipeline first.** Logs are the most overlooked leakage path. If your standard log stream captures raw prompts or raw model outputs, you likely have a leakage channel to every person with log access — which is usually a much broader group than those with application-level data access. Switch to structured, redacted audit events today.

## References

- Framework-specific review notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
