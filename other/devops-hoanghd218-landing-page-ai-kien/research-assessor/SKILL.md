---
name: research-assessor
description: Extracts and assesses research methodology, claims, evidence, and infrastructure from research papers in HASS disciplines. Evaluates transparency, reproducibility, and credibility through systematic extraction (eight-pass workflow, Pass 0-7) and credibility assessment (research approach classification, quality gating, and repliCATS Seven Signals evaluation adapted for HASS).
version: "2.6"
license: Apache 2.0
---

# Research Assessor

Systematic extraction and assessment framework for research methodology, argumentation, and reproducibility infrastructure in HASS disciplines (archaeology, palaeoecology, ethnography, ecology, literary studies, philology, etc.).

## What This Skill Does

This skill enables comprehensive extraction of research content and infrastructure from academic papers, followed by credibility assessment, through a structured multi-pass workflow:

**Extraction Phase (Passes 1-7):**

1. **Claims & Evidence Extraction** (Passes 1-2) - Extract observations, measurements, claims, and implicit arguments
2. **RDMAP Extraction** (Passes 3-5) - Extract Research Designs, Methods, and Protocols
3. **Infrastructure Extraction** (Pass 6) - Extract PIDs, FAIR compliance, funding, permits, author contributions
4. **Validation** (Pass 7) - Verify structural integrity and cross-reference consistency

**Assessment Phase (Passes 8-9):**

5. **Research Approach Classification** (Pass 8) - Classify research approach (deductive/inductive/abductive) with expressed vs revealed methodology comparison and HARKing detection
6. **Credibility Assessment** (Pass 9) - Quality-gated assessment using repliCATS Seven Signals adapted for HASS with approach-specific scoring anchors

The extracted data enables systematic assessment of research transparency, reproducibility, and credibility.

## When to Use This Skill

Use when users request:
- "Extract methodology from this paper"
- "Assess research transparency"
- "Extract claims and evidence"
- "Evaluate reproducibility"
- "Extract research designs and methods"
- Any task involving systematic analysis of research papers for methodology, argumentation, or credibility assessment

## Core Workflow

The complete workflow follows this sequence:

```
Blank JSON Template
    ↓
Pass 1: Evidence extraction (liberal)
    ↓
Pass 2: Claims + implicit arguments extraction + rationalization
    ↓
Pass 3: RDMAP extraction (liberal)
    ↓
Pass 4: RDMAP rationalization
    ↓
Pass 5: Research designs extraction
    ↓
Pass 6: Infrastructure extraction (PIDs, FAIR, funding, permits)
    ↓
Pass 7: Validation (integrity checks)
    ↓
extraction.json (complete)
    ↓
Pass 8: Research approach classification
    ↓
classification.json (approach + HARKing detection)
    ↓
Pass 9: Credibility assessment (quality-gated)
    ↓
assessment/ (cluster files + credibility report + assessment.json)
```

**Key principles:**

- **Passes 1-7:** Single extraction.json document flows through all passes. Each pass populates or refines specific sections, leaving others untouched.
- **Pass 8:** Classification reads extraction.json, outputs classification.json
- **Pass 9:** Assessment reads extraction.json + classification.json + metrics.json, outputs assessment directory with cluster files, report, and canonical assessment.json

## Using This Skill

### Architecture: Skill + Runtime Prompts

This skill provides:
- **Core decision frameworks** (how to distinguish evidence/claims, assign tiers, consolidate items)
- **Schema definitions** (object structures, field requirements)
- **Reference materials** (checklists, examples)

The user provides:
- **Extraction prompts** (detailed instructions for each pass, provided at runtime)
- **Source material** (research paper sections to extract from)
- **JSON document** (template or partially populated from previous passes)

**Why this separation?** Extraction prompts evolve frequently through testing and refinement. This architecture allows prompt tuning without modifying the skill package, minimizing versioning conflicts.

### Step 1: Identify the Task

Users will typically request extraction at a specific pass. Listen for:
- "Extract claims/evidence Pass 1" → Liberal claims extraction
- "Rationalize the claims" → Claims Pass 2
- "Extract RDMAP" → RDMAP Pass 1
- "Extract methodology" → RDMAP Pass 1
- "Validate the extraction" → Pass 3

### Step 2: Receive the Extraction Prompt

The user will provide the extraction prompt for the specific pass they want. These prompts are:

**Claims/Evidence Extraction:**
- **Pass 1:** Liberal extraction prompt (comprehensive capture with over-extraction)
- **Pass 2:** Rationalization prompt (consolidation and refinement)

**RDMAP Extraction:**
- **Pass 1:** Liberal extraction prompt (three-tier hierarchy with over-extraction)
- **Pass 2:** Rationalization prompt (consolidation and verification)

**Validation:**
- **Pass 3:** Unified validation prompt (structural integrity checks across all arrays)

The prompts contain detailed instructions, examples, and decision frameworks for that specific extraction pass. Follow the prompt provided.

### Step 3: Consult Supporting References As Needed

If you encounter uncertainty during extraction, consult:

**Core Extraction Principles:**
- `references/extraction-fundamentals.md` - Universal sourcing requirements, explicit vs implicit extraction, systematic implicit RDMAP patterns, systematic implicit arguments patterns with 6 recognition patterns (ALWAYS read first for Passes 1-5)
- `references/verbatim-quote-requirements.md` - Strict verbatim quote requirements (prevents 40-50% validation failures)
- `references/verification-procedures.md` - Source verification for Pass 7 validation

**Schema & Structure:**
- `references/schema/schema-guide.md` - Complete object definitions with inline examples

**Decision Frameworks:**
- `references/checklists/tier-assignment-guide.md` - Design vs Method vs Protocol decisions
- `references/research-design-operational-guide.md` - Operational patterns for finding all Research Designs (4-6 expected)
- `references/checklists/consolidation-patterns.md` - When to lump vs split items, cross-reference repair procedure (CRITICAL for Passes 2 & 4)
- `references/checklists/expected-information.md` - Domain-specific completeness checklists

**Infrastructure Assessment** (Pass 6):
- `references/infrastructure/pid-systems-guide.md` - Persistent identifiers (DOI, ORCID, RAiD, IGSN, software PIDs), PID graph connectivity scoring, HASS adoption context
- `references/infrastructure/fair-principles-guide.md` - FAIR principles framework, metadata richness, controlled vocabularies, software-specific FAIR (FAIR4RS), computational reproducibility spectrum, machine-actionability, context-dependent assessment
- `references/infrastructure/fieldwork-permits-guide.md` - Permit types, CARE principles integration, ethical restrictions assessment
- `references/infrastructure/credit-taxonomy.md` - CReDIT contributor roles taxonomy (14 roles), format variations

**Examples:**
- `references/examples/sobotkova-example.md` - Complete worked example

### Step 4: Execute and Return

Follow the workflow guidance to:
1. Extract or rationalize content
2. Populate appropriate arrays in JSON
3. Leave other arrays untouched
4. Return the updated JSON document

## Key Extraction Principles

### Iterative Accumulation
- Single JSON document flows through all passes
- Each pass handles specific arrays only
- No merging step needed
- Flexible ordering (claims first OR RDMAP first)

### Liberal Then Rationalize
- **Pass 1:** Over-extract (40-50% more items expected) - comprehensive capture
- **Pass 2:** Consolidate (15-20% reduction target) - refined quality

### Separation of Concerns
- **Claims/Evidence passes:** Touch evidence, claims, implicit_arguments arrays ONLY
- **RDMAP passes:** Touch research_designs, methods, protocols arrays ONLY
- **Validation pass:** Reads all, modifies none

### Cross-Reference Architecture
- Simple string ID arrays: `["M003", "M007"]`
- Bidirectional consistency enforced
- Works across object types (methods reference claims, protocols reference evidence)

## Core Decision Frameworks

### Evidence vs. Claims

**Evidence** = Raw observations requiring minimal interpretation (measurements, observations, data points)

**Claims** = Assertions that interpret or generalize (require reasoning or expertise to assess)

**Test:** "Does this require expertise to assess or just checking sources?"

**For complete decision framework with examples and edge cases:**
→ See `references/checklists/evidence-vs-claims-guide.md`

### RDMAP Three-Tier Hierarchy

Research Designs (WHY), Methods (WHAT), Protocols (HOW).

**For complete tier assignment guidance:** See `references/checklists/tier-assignment-guide.md`

### Consolidation Logic

Evidence items with **identical claim support patterns** that are **never cited independently** should be consolidated.

**For complete algorithm, examples, and cross-reference repair:**
→ See `references/checklists/consolidation-patterns.md`

## Pass 8: Research Approach Classification

### Purpose

Classify research approach (inductive/deductive/abductive) with expressed vs revealed methodology comparison and HARKing detection.

### Inputs

- extraction.json (complete from Pass 7)

### Process

1. **Detect expressed approach** - What paper explicitly states about its methodology
2. **Infer revealed approach** - What paper actually does (independent of what it says)
3. **Compare expressed vs revealed** - Detect HARKing (Hypothesising After Results are Known) or methodological confusion
4. **Generate classification** with confidence and justification

### Outputs

- classification.json

### References

**Classification guidance:**

- `references/credibility/approach-taxonomy.md` - Definitions of deductive/inductive/abductive approaches, mixed-method characterisation, "none_stated" handling
- `references/credibility/harking-detection-guide.md` - Expressed vs revealed comparison, mismatch types, assessment integration
- `references/schema/classification-schema.md` - Complete output structure specification

---

## Pass 9: Credibility Assessment (Quality-Gated)

### Purpose

Assess paper credibility using repliCATS Seven Signals adapted for HASS with approach-specific scoring anchors. Quality-gated workflow ensures assessment viability.

### Inputs

- extraction.json (from Pass 7)
- classification.json (from Pass 8)
- metrics.json (if available)

### Process

**Step 1: Track A quality gating** - Determines assessment pathway

- Evaluate extraction quality, metric-signal alignment, classification confidence
- Output quality_state: "high|moderate|low"
- Route to appropriate pathway:
  - **HIGH:** Full assessment with approach-specific anchors, precise scores
  - **MODERATE:** Caveated assessment with 20-point score bands, warnings
  - **LOW:** Abort assessment, generate Track A report only

**Step 2: Signal cluster assessment** (if quality ≥ moderate)

Assessment is organised into **three pillars** (see `references/credibility/assessment-pillars.md`):

- **Cluster 1: Foundational Clarity** (Transparency pillar: Comprehensibility + Transparency)
- **Cluster 2: Evidential Strength** (Credibility pillar: Plausibility + Validity + Robustness + Generalisability)
- **Cluster 3: Reproducibility** (Reproducibility pillar: Reproducibility signal only)
- Apply approach-specific scoring anchors (0-100 scale varies by research approach)

**Step 3: Report generation**

- Synthesise seven signals
- Apply quality caveats if moderate quality
- Generate canonical assessment.json for corpus analysis

### Outputs

**If quality_state = "high" or "moderate":**

- `track-a-quality.md` - Quality assessment
- `cluster-1-foundational-clarity.md` - Transparency pillar assessment
- `cluster-2-evidential-strength.md` - Credibility pillar assessment
- `cluster-3-reproducibility.md` - Reproducibility pillar assessment
- `credibility-report-v1.md` (or `-CAVEATED.md` if moderate)
- `assessment.json` - Canonical consolidation

**If quality_state = "low":**

- `track-a-only.md` - Quality assessment
- `assessment-not-viable.md` - Explanation of why assessment aborted

### References

**Credibility assessment guidance:**

- `references/credibility/assessment-pillars.md` - Three pillars framework (Transparency, Credibility, Reproducibility)
- `references/credibility/signal-definitions-hass.md` - Seven Signals with approach-specific scoring anchors (0-100 scale for deductive/inductive/abductive)
- `references/credibility/assessment-frameworks.md` - Framework selection and signal emphasis by research approach
- `references/credibility/track-a-quality-criteria.md` - Quality gating decision logic (HIGH/MODERATE/LOW states)
- `references/schema/assessment-schema.md` - Cluster file and assessment.json structure specifications

**🚨 CRITICAL: Where to Find Code/Data Availability**

For Transparency signal assessment, code/data availability is in `reproducibility_infrastructure` (NOT in `evidence[]`):

```
extraction.json → reproducibility_infrastructure
├── code_availability
│   ├── statement_present: true|false
│   ├── repositories: [{name, url, access_conditions}]
│   └── machine_actionability: {rating, rationale}
├── data_availability
│   ├── statement_present: true|false
│   ├── repositories: [{name, url, access_conditions}]
│   └── machine_actionability: {rating, rationale}
├── persistent_identifiers
│   └── software_pids: [{software_name, repository, doi, url}]
├── preregistration
│   └── preregistered: true|false
└── fair_assessment (if populated)
    └── total_fair_score, fair_percentage
```

Always check these sections when assessing Transparency. Do NOT rely on `evidence[]` for code/data information.

### Key Adaptations for HASS

**Reproducibility = Analytic or Computational Reproducibility** (NOT beginning-to-end reproducibility)

- Can others reproduce analytical outputs given same inputs?
- "Can you replicate the entire study?" (often impossible in HASS) vs "Can you reproduce the analysis?" (expected)

**Approach-Specific Anchors:**

- Score of 75 on Transparency means different things:
  - Deductive: Data + code sharing, pre-registration
  - Inductive: Workflow transparency, sampling documentation
  - Abductive: Framework clarity, reasoning traceability

**CARE Principles Integration:**

- Indigenous/community data: Appropriate restrictions do NOT penalise Reproducibility
- CARE principles (Collective benefit, Authority to control, Responsibility, Ethics) alongside FAIR

---

## Schema Field Names Quick Reference (v2.6)

**Use these exact field names. Do not improvise variants.**

### Evidence Object

- `evidence_id` (pattern: E###)
- `evidence_text`
- `evidence_type`
- `verbatim_quote` ← REQUIRED
- `location`, `supports_claims`, `source_verification`

### Claim Object

- `claim_id` (pattern: C###)
- `claim_text`
- `claim_type`: empirical | interpretation | methodological_argument | theoretical
- `claim_role`: core | intermediate | supporting
- `verbatim_quote` ← REQUIRED
- `location`, `supported_by`, `supports_claims`, `source_verification`

### Implicit Argument Object

- `implicit_argument_id` (pattern: IA###)
- `argument_text`
- `type`: logical_implication | unstated_assumption | bridging_claim | design_assumption | methodological_assumption
- `trigger_text` ← REQUIRED (array of verbatim passages)
- `trigger_locations` ← REQUIRED (parallel array)
- `inference_reasoning` ← REQUIRED
- `supports_claims`, `source_verification`

### Research Design Object

- `design_id` (pattern: RD###)
- `design_text`
- `design_type`
- `design_status`: explicit | implicit
- `verbatim_quote` (if explicit) OR `trigger_text` + `inference_reasoning` (if implicit)

### Method Object

- `method_id` (pattern: M###)
- `method_text`
- `method_type`
- `method_status`: explicit | implicit
- `implements_designs`, `realized_through_protocols`

### Protocol Object

- `protocol_id` (pattern: P###)
- `protocol_text`
- `protocol_type`
- `protocol_status`: explicit | implicit
- `implements_methods`, `produces_evidence`

### Classification Object (assessment/classification.json)

- `paper_id` - paper identifier (e.g., "penske-et-al-2023")
- `run_id` - run identifier (pattern: run-XX)
- `classification_date` - ISO date (YYYY-MM-DD)
- `paper_type`: empirical | methodological | theoretical | review
- `paper_type_confidence`: high | medium | low
- `research_approach`: deductive | inductive | abductive | interpretive
- `research_approach_confidence`: high | medium | low
- `mixed_methods`: boolean
- `context_flags`: array (e.g., ["📦", "🔧"])
- `classification_justification` - brief rationale for classification

**For complete field definitions:** See `references/schema/schema-guide.md`

---

## Important Notes

**For testing/debugging:**
- Can validate partial extractions (RDMAP-only or claims-only)
- Each pass can be tested independently
- Start with blank template OR pre-populated arrays

**Expected outcomes:**
- Pass 1: Comprehensive (intentional over-capture)
- Pass 2: ~15-20% reduction through consolidation
- Pass 3: Validation report (no modifications)

**Token efficiency:**
- Only load workflow file needed for current pass
- Schema/examples load only when uncertain
- Minimal context bloat

## Quick Reference

**Common user patterns:**
- User provides extraction prompt + source material → Extract according to prompt
- "Help me understand this extraction" → Consult schema and examples
- "Should I consolidate these?" → Check consolidation-patterns.md
- "Is this a Design, Method, or Protocol?" → Check tier-assignment-guide.md
- "What information is expected?" → Check expected-information.md

**Working with prompts:**
- User provides the full extraction prompt for the current pass
- Follow the prompt's instructions precisely
- Use skill references to resolve ambiguities
- Document uncertainties in extraction_notes

**Always:**
- Preserve other arrays unchanged
- Document consolidations with metadata
- Flag uncertainties in extraction_notes
- Return complete JSON document

---

**The user will provide the detailed extraction prompt for each pass. Use this skill's reference materials to support decision-making during extraction.**
