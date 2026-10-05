---
name: bio-research
description: "Automatically handle molecular and cellular biology research about genes, proteins, variants, pathways, omics, cells, model organisms, mechanisms, disease biology, and preclinical biomedical literature. Use when the user names a gene/protein/pathway, asks how a biological mechanism works, wants database/evidence mapping, or needs early-stage findings separated from established biology. Use research-medical-evidence for human clinical effectiveness, diagnosis, treatment, rehabilitation, or publication workflows; do not let this broad umbrella displace the clinical specialist. Turkish triggers: gen/protein araştır, biyolojik mekanizma, varyant veya yolak, preklinik kanıt."
---

# Bio Research

Use this skill when the task is biological or biomedical research rather than generic web lookup.

## Workflow
- Clarify entity, disease area, and evidence question.
- Prefer primary or structured scientific sources.
- Use installed life-science research skills when appropriate.
- Use `$evidence-integrity-guard` for identity, citation, and claim verification when available.

## Deliverables
- A biology-focused evidence brief.
- Open questions or uncertainty notes.

## Guardrails
- Do not overstate early-stage evidence.
- Do not mix speculation with established findings.
