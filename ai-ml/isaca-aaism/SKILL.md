---
name: isaca-aaism
description: Use when preparing for ISACA Advanced in AI Security Management (AAISM) — eligibility through an existing security management credential, the three domains (AI governance and program management, AI risk management, AI technologies and controls), mapping questions to frameworks such as the NIST AI RMF, the EU AI Act, OWASP's LLM risks and MITRE ATLAS, and answering from a security manager's point of view. Also use when writing or verifying AI security management practice questions.
---

# ISACA Advanced in AI Security Management (AAISM)

Bottom line: **answer as the security manager, not the engineer**. ISACA-style questions reward the option that establishes governance, assesses risk or aligns with business objectives before the one that applies a specific technical fix.

## Exam shape (confirm on ISACA's AAISM page)

- Eligibility: an active CISM or CISSP is required.
- 90 multiple-choice questions in 2.5 hours; scaled score with a passing mark of 450 on a 200–800 scale; no penalty for wrong answers, so answer every question. Offered at test centres or remotely, in several languages including Japanese.
- Domains: AI Governance and Program Management, AI Risk Management, AI Technologies and Controls (largest). Check the exam content outline for weights and task statements.
- After passing, apply for certification and maintain it with continuing professional education.

Primary sources: ISACA AAISM page and exam content outline (https://www.isaca.org/credentialing/aaism), the ISACA review manual and question database, and the public frameworks below.

## Frameworks to map against

| Source | Use it for |
|---|---|
| NIST AI Risk Management Framework (Govern, Map, Measure, Manage) and its generative AI profile | Risk process vocabulary |
| EU AI Act | Risk tiers (prohibited, high-risk, limited, minimal), obligations of providers and deployers, general-purpose AI |
| ISO/IEC 42001 | AI management system structure (policy, roles, risk treatment, continual improvement) |
| OWASP Top 10 for LLM Applications (check the edition; names changed between 2023 and 2025) | Prompt injection, sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency |
| MITRE ATLAS | Adversarial tactics and techniques against ML systems |
| National AI guidelines (e.g. Japan's AI Guidelines for Business) | Governance expectations for developers, providers and users |

## Domain checklists

- **Governance and program:** AI inventory, ownership and accountability, acceptable-use policy, roles (data owner, model owner), training and awareness, third-party/vendor AI, metrics reported to the board.
- **Risk management:** risk identification for data, models and use cases; impact assessment; risk appetite; treatment (avoid, mitigate, transfer, accept); monitoring for drift and misuse; incident response for AI.
- **Technologies and controls:** data protection and lineage, model access control, secure development and MLOps, adversarial testing and red teaming, input/output filtering, human oversight, logging, explainability, supply chain (models, datasets, libraries).

## Study loop

1. Read the content outline; write one scenario per task statement.
2. For each practice question, decide first which domain and which lifecycle stage it belongs to.
3. Eliminate options that act before understanding (e.g. "deploy a tool" before "assess the risk") unless the question says the assessment is done.
4. Check facts against the framework texts, not summaries.

## Writing practice questions

- Verify every claimed obligation or definition against the primary text (law, standard, framework) and keep the reference.
- Use management-level scenarios with realistic constraints; avoid trivia about a specific vendor product.

## Pitfalls

- Choosing the most technical answer when the question asks what the manager should do **first** or **best**.
- Confusing provider and deployer obligations under the EU AI Act.
- Treating AI risk as only security risk (fairness, transparency, safety and legal risks belong too).
- Forgetting third-party models and data in the inventory.

## Self-check

- A full-length practice exam in 2.5 hours with margin above the passing line.
- For any AI use case, list governance owner, top three risks, and controls mapped to a framework.
- Explain the NIST AI RMF functions and give one activity for each.
