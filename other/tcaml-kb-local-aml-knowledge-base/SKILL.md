---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-KB"
title: "Local AML Knowledge Base Skill"
risk_area:
  - general_aml
human_review_required: true
final_decision_allowed: false
paid_source_boundary: false
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---

---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-KB"
title: "Local AML Knowledge Base"
risk_area:
  - cdd
  - edd
  - sanctions
  - pep
  - adverse_media
  - kyb
  - ubo
  - crypto
  - trade
  - domain_ip
human_review_required: true
final_decision_allowed: false
paid_source_boundary: true
embedded_wiki_version: "0.3.15"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---

# TCAML-KB — Local AML Knowledge Base Skill

## Purpose

This skill embeds the Tom Custos AML Wiki v0.3.15 knowledge base inside TCAML so an agent can load the public AML knowledge layer together with operation, source, connector and channel skills.

The wiki knowledge is a reference layer. It does not grant source access, replace an implementation profile, replace legal advice or replace MLRO/compliance review.

## Contents

- `KNOWLEDGE_BASE.md` — consolidated local AML knowledge base.
- `wiki-pages/` — individual source wiki pages used to build the knowledge base.
- `wiki-pages/ai-index.md` — wiki-specific AI entrypoint.
- `wiki-pages/rag-ingestion.md` — wiki-specific RAG ingestion guide.
- `wiki-pages/canonical-topics.md` — topic map and aliases.
- `wiki-pages/knowledge-ecosystem.md` — public knowledge ecosystem map.

## Usage

Load this skill when the agent needs AML background knowledge, terminology, red flag context, evidence practices, CDD/EDD guidance, UBO guidance, sanctions/TFS/CPF context, adverse media logic, crypto AML, TBML, geographic exposure, digital jurisdiction exposure, decision matrices or runbooks.

## Boundary

The agent must use this knowledge to structure review and evidence, not to make final compliance decisions.
