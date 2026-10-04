---
license: BSL-1.1
name: windags-librarian
description: Maintain consistency across all winDAGs documentation surfaces — corpus documents, marketing copy, README files, site content, skill files, API docs, and derivative documents. Enforces the canonical terminology table, voice guidelines, architectural accuracy, and cross-reference integrity. Activate on "windags docs", "documentation consistency", "windags copy", "terminology check", "docs audit", "windags readme", "site copy", "docs sync", "content review", "windags librarian". NOT for writing new architecture (use windags-architect), creating new skills (use skill-architect), or running the recursive synthesis process (use recursive-synthesis).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
metadata:
  category: Productivity & Meta
  pairs-with:
    - skill: windags-architect
      reason: Architect defines truth; Librarian propagates it
    - skill: recursive-synthesis
      reason: Synthesis produces source documents; Librarian maintains them
    - skill: skill-documentarian
      reason: Documentarian creates website pages; Librarian ensures accuracy
  tags:
    - documentation
    - consistency
    - windags
    - terminology
    - copy
    - librarian
category: Agent & Orchestration
tags:
  - windags
  - library
  - skill-management
  - catalog
  - search
---

# winDAGs Librarian

The guardian of consistency across every surface where winDAGs content appears. You enforce canonical terminology, voice, and structural truth from the 6-phase synthesis against all derivative surfaces.

## Decision Points

When you find an inconsistency, follow this decision tree:

```
Inconsistency Detected
├── Is it TERMINOLOGY drift?
│   ├── Academic term leaked (cognitive_core, PreMortem, etc.)
│   │   └── → AUTO-FIX with canonical substitution
│   └── New/unclear term
│       └── → FLAG for terminology committee review
│
├── Is it STRUCTURAL mismatch?
│   ├── Agent count ≠ 11, Phase count ≠ 6, Libraries ≠ 3
│   │   └── → ESCALATE as critical error (blocks publishing)
│   ├── Cross-reference broken (section moved/renamed)
│   │   └── → FLAG for immediate fix with suggested target
│   └── Minor version drift (outdated implementation detail)
│       └── → QUEUE for next maintenance cycle
│
├── Is it VOICE violation?
│   ├── Marketing copy using forbidden terms ("AI-powered", "revolutionary")
│   │   └── → AUTO-FIX with approved messaging
│   ├── Technical surface using marketing speak
│   │   └── → FLAG with suggested technical alternative
│   └── Wrong formality for audience
│       └── → SUGGEST rewrite with correct voice level
│
└── Is it CLAIM accuracy?
    ├── Cannot trace to Constitution/Practitioner's Guide
    │   └── → FLAG as unsupported claim, request source
    ├── Exaggerated/distorted claim (says "revolutionary" for "iterative")
    │   └── → FLAG with corrected factual statement
    └── Outdated claim (refers to old architecture)
        └── → QUEUE for update with current truth
```

## Failure Modes

### Schema Bloat
**Detection Rule**: If you see more than 12 agents, more than 6 phases, or more than 3 libraries mentioned
**Symptoms**: Documentation describes capabilities not in Constitution, inflated numbers
**Fix**: Cross-check against Constitution Ch.14.2, reduce to canonical counts
**Prevention**: Always verify structural claims against Tier 1 sources before publishing

### Terminology Drift
**Detection Rule**: If you see academic terms (cognitive_core, PreMortem, Sensemaking, commitment_strategy) in user-facing content
**Symptoms**: User confusion, barrier to adoption, sounds "too academic"
**Fix**: Replace with canonical practitioner terms from the term table
**Prevention**: Run terminology scan before any external publication

### Phantom Feature Marketing
**Detection Rule**: If marketing claims cannot be traced to Constitution or Practitioner's Guide
**Symptoms**: Promises features that don't exist, creates support burden
**Fix**: Remove or qualify claims, add traceability to source
**Prevention**: Require source citation for every factual claim in marketing content

### Reference Rot
**Detection Rule**: If cross-references point to sections that don't exist or say different things
**Symptoms**: Broken links, readers can't verify claims, documents feel outdated
**Fix**: Update references to current section structure and content
**Prevention**: Automated link checking in publication pipeline

### Voice Mismatch
**Detection Rule**: If technical docs use marketing language or marketing uses technical jargon
**Symptoms**: Wrong audience engagement, credibility loss, confusion
**Fix**: Rewrite with appropriate voice for surface type (technical/marketing/reference)
**Prevention**: Voice checklist in review process based on surface type

## Worked Examples

### Example 1: Terminology Drift in Marketing Copy

**Found**: Marketing site says "Our PreMortem Analyzer catches edge cases before they bite you."

**Decision Process**:
1. Scan for terminology violations → Found "PreMortem Analyzer"
2. Check term table → Maps to "Risk Analyzer" 
3. Classify severity → Auto-fix (clear substitution)
4. Check voice appropriateness → "bite you" is too casual for professional marketing
5. Apply both fixes

**Fixed**: "Our Risk Analyzer identifies potential failures before they impact your workflow."

**What novice misses**: Only fixes terminology, leaves casual voice
**What expert catches**: Voice mismatch creates credibility gap with senior engineers

### Example 2: Cross-Reference Mismatch

**Found**: README says "See Constitution Ch.15.3 for agent details"

**Decision Process**:
1. Validate reference → Constitution only has 14 chapters
2. Search for agent details → Found in Ch.14.2 "The 11-Agent Architecture"
3. Check content match → Claims match, just wrong section number
4. Classify → Flag for immediate fix (broken navigation)

**Fixed**: "See Constitution Ch.14.2 for the 11-agent architecture details"

**Action Log**: Also search for other references to "Ch.15" across all surfaces

### Example 3: Voice Violation in Technical Docs

**Found**: API docs say "Revolutionary Thompson sampling powers our learning engine"

**Decision Process**:
1. Check audience → Technical/reference (developers)
2. Scan for forbidden marketing terms → "Revolutionary" is banned
3. Check technical accuracy → Thompson sampling is correct
4. Determine appropriate voice → Factual, no hype
5. Verify claim source → Constitution Ch.12.4 confirms Thompson sampling

**Fixed**: "Thompson sampling algorithms optimize skill selection based on historical performance"

## Quality Gates

Before marking a surface as "verified consistent":

- [ ] All academic terms replaced with canonical practitioner terms
- [ ] Agent count = 11, Phase count = 6, Library count = 3 throughout
- [ ] No forbidden messaging terms (AI-powered, revolutionary, groundbreaking)
- [ ] All factual claims traceable to Constitution or Practitioner's Guide
- [ ] Cross-references point to existing sections with matching content
- [ ] Voice matches surface type (technical/marketing/reference/casual)
- [ ] No structural contradictions with Tier 1 sources
- [ ] Update propagation completed for any fixes made
- [ ] Document Registry updated with verification date

## NOT-FOR Boundaries

**Do NOT use this skill for**:
- Writing new architecture → Use `windags-architect` instead
- Creating new skills → Use `skill-architect` instead  
- Running the recursive synthesis process → Use `recursive-synthesis` instead
- Building the actual product → Use `windags-architect` instead
- Making marketing strategy decisions → Those come from derivative_marketing.md
- Fixing code bugs → This is documentation-only consistency checking
- Creating new content from scratch → This maintains existing content only

**Delegate these tasks**:
- Architecture changes → `windags-architect`
- New skill development → `skill-architect`  
- Website page creation → `skill-documentarian`
- Content strategy → Refer to derivative_marketing.md
- Technical implementation → Refer to derivative_build_roadmap.md