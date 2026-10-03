---
skill_id: notebooklm-py
name: NotebookLM Integration
description: "Research synthesis from sources — \"summarize these URLs or papers\", \"research this topic with these sources\", \"create a podcast about\", \"audio overview\", \"mind map\", \"quiz from these sources\", \"flashcards\", \"deep research on\". Wraps Google NotebookLM via notebooklm-py."
version: 1.0.0
category: research-synthesis
type: external-tool-wrapper
upstream:
  name: teng-lin/notebooklm-py
  repo: https://github.com/teng-lin/notebooklm-py
  license: MIT
  community_pack: community-packs/notebooklm-py/
mcp_server: mxm-notebooklm
mcp_tools: 38
frameworks:
  - ADR-007 behavioral-moat-framing-doctrine
  - ADR-018 external-tool-integration-pattern
  - Diátaxis (Procopiou) — distinct artifact types for distinct learning modes
  - Diffusion of Innovations (Rogers) — multi-format artifacts let each adopter category consume in their preferred mode
  - Dual Coding Theory (Paivio) — pairing audio + visual artifacts increases retention
triggers:
  - "summarize these urls/papers/sources"
  - "research this topic with these sources"
  - "create a podcast about X"
  - "audio overview of these sources"
  - "generate a video explainer for X"
  - "mind map of [concepts/papers]"
  - "quiz from these sources"
  - "flashcards for [topic]"
  - "infographic from research"
  - "deep research on [topic]"
  - "add these sources to NotebookLM"
  - "knowledge synthesis from [sources]"
collaborates_with:
  - cino-office (primary — research synthesis)
  - cmo-office (audio/video/infographic production from research)
  - cpo-office (quiz/flashcards/onboarding artifacts)
  - cso-office (ethics gate on source upload to Google API)
ethics_required: true
super_user_bypass: false
priority: high
tags: [research-synthesis, notebooklm, audio-overview, video-overview, podcast, mind-map, quiz, flashcards, mcp-routed, external-tool, adr-018]
adr: ADR-018
created: 2026-05-20
updated: 2026-05-20
---

# NotebookLM Integration

## Purpose

Programmatic research-synthesis layer wrapping `teng-lin/notebooklm-py` (MIT) for Google's NotebookLM. Ingests sources (URLs, PDFs, YouTube, Google Drive, audio/video/text), produces synthesized artifacts (podcasts, video overviews, slide decks, infographics, quizzes, flashcards, reports, mind maps, data tables), and runs deep research agents with auto-import.

This skill is the load-bearing piece of ADR-018 (External Tool Integration Pattern). It is Maxim's first canonical wrapper around a third-party CLI tool with full MCP coverage and ADR-007 behavioral framing on top.

## Architecture (the dispatch story)

Per ADR-017 + ADR-018, this skill is reached three ways:

1. **Direct MCP invocation** (cross-surface — Code · Desktop · Web · Cowork): operator or agent calls one of 38 `mxm-notebooklm` MCP tools directly.
2. **Office-routed dispatch** (Code primary): a writing/research verb on a "sources + synthesis" task routes through `cino-office` (default) or `cmo-office` (content production) or `cpo-office` (learning artifacts) which embody this skill.
3. **Community-pack reference** (per ADR-008): the upstream skill ships verbatim at `community-packs/notebooklm-py/` for operators who want the raw upstream contract.

**Critical:** this skill never short-circuits the upstream — every operation is a wrapped CLI invocation. Maxim's value-add is ROUTING, ETHICS GATE, AUDIT TRAIL, FRAMEWORK CITATION — not reimplementing upstream features.

## Pre-flight (mandatory before any non-auth operation)

```
1. mxm-notebooklm.auth_check → verify Google auth is live
   ↓
2. If auth fails: HALT with install + login instructions:
     pip install "notebooklm-py[browser]"
     playwright install chromium
     notebooklm login
   ↓
3. cso-office ethics gate on source content (PII, regulated data, third-party content)
   ↓
4. Proceed with operation
```

## Office Routing Logic

### Primary route — CINO Office (research synthesis)

The default. Most NotebookLM use cases are research-driven: ingest sources → synthesize artifacts → extract knowledge.

| Task pattern | Specialist embodied (within CINO) |
|---|---|
| "research X with these sources" | `innovation-researcher` invoking research_web/research_drive |
| "synthesize these papers" | `innovation-researcher` + generate_report |
| "what's the competitive landscape for X" | `competitive-intel-analyst` + research_web |
| "patent landscape for X" | `patent-researcher` + research_web |
| "horizon scan emerging tech in X" | `horizon-scanner` + research_web |

### Secondary route — CMO Office (content production from research)

When the goal is producing a consumable artifact from synthesized research:

| Task pattern | Specialist embodied (within CMO) |
|---|---|
| "create a podcast about X" | `nk-writer` (operator voice for intro/outro) + generate_audio_overview |
| "audio overview for our team about X" | `content-strategist` + generate_audio_overview (deep-dive format) |
| "generate a video explainer for X" | `content-strategist` + generate_video_overview |
| "infographic of [research]" | `behavioral-designer` + generate_infographic (visual hierarchy via behavioral framing) |
| "blog post synthesizing [sources]" | `nk-writer` (operator voice) + generate_report + reformat in voice |

### Secondary route — CPO Office (learning artifacts)

For artifacts designed for user-facing learning (onboarding, training, education):

| Task pattern | Specialist embodied (within CPO) |
|---|---|
| "quiz from these sources" | `onboarding-designer` + generate_quiz |
| "flashcards for [topic]" | `ux-researcher` + generate_flashcards |
| "study guide from [sources]" | `accessibility-auditor` + generate_report (accessibility-first template) |
| "interactive learning module from X" | `product-strategist` + multi-artifact (slides + quiz + flashcards) |

### Auto-loop — CSO Office (mandatory ethics gate)

EVERY source-upload operation triggers `compliance-orchestrator` auto-loop:

- Source content scanned for PII / regulated data BEFORE upload
- Google AI ingestion = data flows to Google → applicable GDPR / PIPEDA / HIPAA / SOC2 / UAE-PDPL framework checks fire
- Block on compliance signal until operator confirms data-processing posture
- Audit logged to `.mxm-skills/compliance-audit.jsonl`

## Behavioral Framing (per ADR-007)

**Diátaxis (Procopiou):** NotebookLM produces four distinct artifact families that map to Diátaxis's four documentation modes —
- Tutorials (interactive learning): flashcards · quiz
- How-to (task-driven): video explainers · slide decks (explainer format)
- Reference (information lookup): mind map · data table
- Explanation (understanding): audio overview · video overview (narrative format) · reports

Skill output explicitly cites which Diátaxis mode the chosen artifact serves.

**Diffusion of Innovations (Rogers):** Multi-format artifacts let different adopter categories consume the same research in their preferred mode — innovators (mind map for connection-spotting), early adopters (deep-dive audio while commuting), early majority (slide deck for skim), late majority (quiz to validate understanding), laggards (flashcards for spaced repetition). When multiple artifacts are generated from one notebook, this is the framework that justifies the redundancy.

**Dual Coding Theory (Paivio):** Audio + visual artifacts pair non-redundantly. Retention research shows verbal + visual encoding outperforms either alone by ~50–65%. When the operator's goal is durable understanding (training material, executive briefing), generate audio + slides/infographic together.

## Fragility Disclosure (per ADR-018 § Mandatory Disclosure)

Upstream `teng-lin/notebooklm-py` explicitly states:

> *"Unofficial library using undocumented Google APIs. Not affiliated with Google. API endpoints can change without notice. Rate limiting applies to heavy usage. Best suited for prototypes, research, personal projects rather than production systems."*

Maxim ships this wrapper "by default" per operator directive but inherits this fragility. Every output produced via this skill carries the audit-trail line:

```
fragility_disclosure: ADR-018 · upstream uses undocumented Google APIs · production use at operator risk
```

If a Google API change breaks the upstream, this skill degrades gracefully — `auth_check` and CLI invocations return structured errors with the operator's remediation path (`pip install --upgrade notebooklm-py` and check upstream issues).

## Confidence Tagging

🟢 HIGH — auth check passed · source ingestion confirmed · artifact generated · ethics gate cleared · framework cited
🟡 MEDIUM — partial source ingestion · ambiguous artifact selection (operator clarified) · compliance REVIEW (not BLOCK) · framework selection required tie-breaking
🔴 LOW — auth failed · upstream CLI not installed · compliance BLOCK · generation task FAILED status · fragility-disclosure trigger (Google API change suspected)
🔵 SUPER USER — N/A (compliance-orchestrator does NOT honor super_user bypass per CSO doctrine; ethics still fires)

## Auto-Trigger Patterns (the skill fires WITHOUT explicit /notebooklm invocation)

- Operator says "summarize / research / synthesize" + provides URLs or file references
- Task contains "podcast" or "audio overview" or "audio explainer"
- Task contains "video overview" or "video explainer" with reference to source material
- Task contains "mind map" or "knowledge map" of multiple concepts
- Task contains "quiz" or "flashcards" + reference to source material
- Task contains "study guide" or "training material" derived from research
- Task contains "deep research" or "research agent" or "competitive landscape research"

## Operator Setup (one-time per machine)

```bash
# Install upstream (the CLI binary)
pip install "notebooklm-py[browser]"

# Install Chromium for browser-based Google auth
playwright install chromium

# Authenticate to Google
notebooklm login
# (Opens browser for sign-in. Alternative: notebooklm login --cookies-from-browser chrome)

# Verify
notebooklm auth check
```

After setup, the `mxm-notebooklm` MCP server in Maxim picks up authentication automatically. No additional Maxim-specific config required.

**Cross-surface availability:**
- Claude Code: native via `.mcp.json` auto-discovery (38 tools available immediately after restart)
- Claude Desktop: add via `bootstrap/mxm-desktop-config.{sh,ps1}` (script handles automatically)
- Claude.ai Web: via MCP-over-API integration when surface support lands
- Cowork: bundled in v1.2.1.0+ plugin manifest

## Example Workflows (operator-facing patterns)

### Workflow 1 — Research synthesis for a startup pitch
```
1. notebook_create("Maxim Series A Research")
2. source_add_url × N (competitor sites · industry reports · regulatory filings)
3. research_web("competitive landscape for AI-assisted clinical decision support 2026")
4. research_wait → returns synthesized report
5. generate_audio_overview(format="deep-dive", language="en") → podcast for operator commute consumption
6. generate_slides(topic="competitive moat") → pitch deck section
7. artifact_wait → artifact_download each
```

### Workflow 2 — Customer onboarding curriculum
```
1. notebook_create("Maxim Customer Onboarding")
2. source_add_file(documentation PDFs)
3. source_add_url(landing page · ADRs)
4. generate_quiz(num_questions=15) → onboarding quiz
5. generate_flashcards(num_cards=25) → SRS flashcards for new operators
6. generate_video_overview(format="explainer", style="tutorial")
7. artifact_download → ship to onboarding portal
```

### Workflow 3 — Compliance research
```
1. notebook_create("UAE-PDPL Compliance Posture")
2. source_add_url(legal sources · regulatory guidance · best practice docs)
3. cso-office auto-loop fires (regulated subject matter)
4. compliance-orchestrator scans sources for PII before Google ingestion
5. research_web("UAE-PDPL controller obligations vs GDPR Article 5") with auto-import
6. generate_report(template="compliance-gap-analysis")
7. chat_ask("what changes do we need to make to our consent flow?")
8. Output tagged 🟢 HIGH only if compliance-orchestrator returned PASS on every source
```

## Skill Dependencies

- **Upstream:** `notebooklm-py` MIT package (operator installs separately)
- **Maxim MCP:** `mxm-notebooklm` (9th MCP, ships in v1.2.1.0+)
- **Community pack mirror:** `community-packs/notebooklm-py/` (faithful upstream SKILL.md per ADR-008)
- **Required Maxim auto-loops:** `compliance-orchestrator` (CSO) · `ethics-orchestrator` (general) · `behavioral-overlay-orchestrator` (framework citation per ADR-007) · `confidence-tagger` (ADR-010)

## Frameworks Cited (the audit trail requirement)

Every emission from this skill must cite at least one of:
- ADR-018 External Tool Integration Pattern (always — by definition)
- Diátaxis (Procopiou) — when artifact-type selection requires justification
- Diffusion of Innovations (Rogers) — when multi-format generation is justified
- Dual Coding Theory (Paivio) — when pairing audio + visual artifacts
- Applicable compliance framework (when CSO auto-loop fires) — GDPR / PIPEDA / HIPAA / SOC2 / UAE-PDPL / etc.

## Output Format

```
NotebookLM Operation: <operation_name>
─────────────────────────────────────
[result content — quiz JSON / audio download path / report markdown / etc.]

─────────────────────────────────────
Audit Trail:
  Notebook: <notebook_id>
  Operation: <CLI subcommand>
  Sources touched: <count> · <ids>
  Artifact generated: <type> · <artifact_id>
  Ethics gate: <PASS | REVIEW | BLOCK>
  Compliance frameworks: <applicable list from project-manifest>
  Diátaxis mode: <tutorial | how-to | reference | explanation>
  Framework citation: <ADR-018 · plus secondary if applicable>
  Confidence: 🟢 HIGH | 🟡 MEDIUM | 🔴 LOW
  Fragility disclosure: ADR-018 § Mandatory Disclosure (upstream undocumented Google API)
─────────────────────────────────────
```

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1 (wrapper). Upstream notebooklm-py: MIT (teng-lin). Ratified by ADR-018 (2026-05-20)._
