---
name: wolf-verification
description: Three-layer verification architecture (CoVe, HSP, RAG) for self-verification, fact-checking, and hallucination prevention
version: 1.1.0
category: quality-assurance
triggers:
  - verification
  - fact checking
  - hallucination detection
  - self verification
  - CoVe
  - HSP
  - RAG grounding
dependencies:
  - wolf-principles
  - wolf-governance
size: large
---

# Wolf Verification Framework

Three-layer verification architecture for self-verification, systematic fact-checking, and hallucination prevention. Based on ADR-043 (Verification Architecture).

## Overview

Wolf's verification system combines three complementary approaches:

1. **CoVe (Chain of Verification)** - Systematic fact-checking by breaking claims into verifiable steps
2. **HSP (Hierarchical Safety Prompts)** - Multi-level safety validation with security-first design
3. **RAG Grounding** - Contextual evidence retrieval for claims validation
4. **Verification-First** - Generate verification checklist BEFORE creating response

**Key Principle**: Agents **MUST** verify their own outputs before delivery. We have built sophisticated self-verification tools - use them!

---

## 🔍 Chain of Verification (CoVe)

### Purpose
Systematic fact-checking framework that breaks complex claims into independently verifiable atomic steps, creating transparent audit trails.

### Core Concepts

#### Step Types (5 types)
```python
class StepType(Enum):
    FACTUAL = "factual"           # Verifiable against authoritative sources
    LOGICAL = "logical"            # Reasoning steps following from conclusions
    COMPUTATIONAL = "computational" # Mathematical/algorithmic calculations
    OBSERVATIONAL = "observational" # Requires empirical validation
    DEFINITIONAL = "definitional"   # Meanings, categories, classifications
```

#### Step Artifacts
Each verification step produces structured output:
```python
StepArtifact(
    type=StepType.FACTUAL,
    claim="Einstein was born in Germany",
    confidence=0.95,
    reasoning="Verified against biographical records",
    evidence_sources=["biography.com", "britannica.com"],
    dependencies=[]  # List of prerequisite step IDs
)
```

### Basic Usage

```python
from src.verification.cove import plan, verify, render, verify_claim

# Simple end-to-end verification
claim = "Albert Einstein won the Nobel Prize in Physics in 1921"
report = await verify_claim(claim)
print(f"Confidence: {report.overall_confidence:.1%}")
print(report.summary)

# Step-by-step approach
verification_plan = plan(claim)  # Break into atomic steps
report = await verify(verification_plan)  # Execute verification
markdown_audit = render(report, "markdown")  # Generate audit trail
```

### Advanced Usage with Custom Evidence Provider

```python
from src.verification.cove import CoVeVerifier, EvidenceProvider, StepType

class WikipediaEvidenceProvider(EvidenceProvider):
    async def get_evidence(self, claim: str, step_type: StepType):
        # Your Wikipedia API integration
        return [{
            "source": "wikipedia",
            "content": f"Wikipedia evidence for: {claim}",
            "confidence": 0.85,
            "url": f"https://wikipedia.org/search?q={claim}"
        }]

    def get_reliability_score(self):
        return 0.9  # Provider reputation (0.0-1.0)

# Use custom provider
config = CoVeConfig()
verifier = CoVeVerifier(config, WikipediaEvidenceProvider())
report = await verifier.verify(verification_plan)
```

### Verification Workflow

```
1. PLAN: Break claim into atomic verifiable steps
   └─> Identify step types (factual, logical, etc.)
   └─> Establish step dependencies
   └─> Assign verification methods

2. VERIFY: Execute verification for each step
   └─> Gather evidence from providers
   └─> Validate against sources
   └─> Compute confidence scores
   └─> Track dependencies

3. AGGREGATE: Combine step results
   └─> Calculate overall confidence
   └─> Identify weak points
   └─> Generate audit trail

4. RENDER: Produce verification report
   └─> Markdown format for humans
   └─> JSON format for automation
   └─> Summary statistics
```

### Performance Targets
- **Speed**: <200ms per verification (5 steps average)
- **Accuracy**: ≥90% citation coverage target
- **Thoroughness**: All factual claims verified

### When to Use CoVe
- ✅ Factual claims about events, dates, names
- ✅ Technical specifications or API documentation
- ✅ Historical facts or timelines
- ✅ Statistical claims or metrics
- ✅ Citations or references
- ❌ Subjective opinions or preferences
- ❌ Future predictions (use "hypothetical" step type)
- ❌ Creative content (fiction, poetry)

**Implementation Location**: `/src/verification/cove.py`
**Documentation**: `/docs/public/verification/chain-of-verification.md`

---

## 🛡️ Hierarchical Safety Prompts (HSP)

### Purpose
Multi-level safety validation system with sentence-level claim extraction, entity disambiguation, and security-first design.

### Key Features
- **Sentence-level Processing**: Extract and validate claims from individual sentences
- **Entity Disambiguation**: Handle entity linking with disambiguation support
- **Security-First Design**: Built-in DoS protection, injection detection, input sanitization
- **Claim Graph Generation**: Structured relationships between claims
- **Evidence Integration**: Multiple evidence providers with reputation scoring
- **Performance**: ~500 claims/second, <10ms validation per claim

### Security Layers

#### Level 1: Input Sanitization
```python
# Automatic protections
- Unicode normalization (NFKC)
- Control character removal
- Pattern detection (script injection, path traversal)
- Length limits (prevent resource exhaustion)
- Timeout protection (configurable limits)
```

#### Level 2: Sentence Extraction
```python
from src.verification.hsp_check import extract_sentences

text = """
John works at Google. The company was founded in 1998.
Google's headquarters is in Mountain View, California.
"""

sentences = extract_sentences(text)
# Result: [
#   "John works at Google",
#   "The company was founded in 1998",
#   "Google's headquarters is in Mountain View, California"
# ]
```

#### Level 3: Claim Building
```python
from src.verification.hsp_check import build_claims

claims = build_claims(sentences)
# Result: List[Claim] with extracted entities and relationships
# Each claim has:
# - claim_text: str
# - entities: List[Entity]  # Extracted named entities
# - claim_type: str  # factual, relational, temporal, etc.
# - confidence: float  # Initial confidence score
```

#### Level 4: Claim Validation
```python
from src.verification.hsp_check import validate_claims

report = await validate_claims(claims)
# Result: HSPReport with:
# - validated_claims: List[ValidatedClaim]
# - overall_confidence: float
# - validation_failures: List[str]
# - evidence_summary: Dict[str, Any]
```

### Custom Evidence Provider

```python
from src.verification.hsp_check import HSPChecker, EvidenceProvider, Evidence
import time

class CustomEvidenceProvider(EvidenceProvider):
    async def get_evidence(self, claim):
        evidence = Evidence(
            source="your_knowledge_base",
            content="Supporting evidence text",
            confidence=0.85,
            timestamp=str(time.time()),
            provenance_hash="your_hash_here"
        )
        return [evidence]

    def get_reputation_score(self):
        return 0.9  # Provider reputation (0.0-1.0)

# Use custom provider
checker = HSPChecker(CustomEvidenceProvider())
report = await checker.validate_claims(claims)
```

### Hierarchical Validation Levels

```
Level 1: Content Filtering (REQUIRED)
└─> Harmful content detection
└─> PII identification and redaction
└─> Inappropriate content filtering

Level 2: Context-Aware Safety (RECOMMENDED)
└─> Domain-specific validation
└─> Relationship verification
└─> Temporal consistency checks

Level 3: Domain-Specific Safety (OPTIONAL)
└─> Industry-specific rules
└─> Compliance requirements
└─> Custom validation logic

Level 4: Human Escalation (EDGE CASES)
└─> Ambiguous claims
└─> Low-confidence assertions
└─> Contradictory evidence
```

### Performance Targets
- **Throughput**: ~500 claims/second
- **Latency**: <10ms per claim validation
- **Security**: Built-in DoS protection, injection detection
- **Accuracy**: ≥95% entity extraction accuracy

### When to Use HSP
- ✅ Multi-sentence generated content
- ✅ Entity-heavy claims (names, organizations, places)
- ✅ Safety-critical applications
- ✅ PII detection and redaction
- ✅ High-volume claim validation
- ❌ Single atomic claims (use CoVe instead)
- ❌ Non-factual content (opinions, creative writing)

**Implementation Location**: `/src/verification/hsp_check.py`
**Documentation**: `/docs/public/verification/hsp-checking.md`

---

## 📚 RAG Grounding

### Purpose
Retrieve relevant evidence passages from Wolf's corpus to ground claims in contextual evidence.

### Core Functions

#### Retrieve Evidence
```python
from lib.rag import retrieve, format_context

# Retrieve top-k relevant passages
passages = retrieve(
    query="security best practices",
    n=5,
    min_score=0.1
)

# Format with citations
grounded_context = format_context(
    passages,
    max_chars=1200,
    citation_format='[Source: {id}]'
)
```

### Integration with wolf-core-ip MCP

```typescript
// RAG Retrieve - Get relevant evidence
const retrieval = await rag_retrieve(
  'security best practices',
  { k: 5, min_score: 0.1, corpus_path: './corpus' },
  sessionContext
);

// RAG Format - Format with citations
const formatted = rag_format_context(
  retrieval.passages,
  { max_chars: 1200, citation_format: '[Source: {id}]' },
  sessionContext
);

// Check Confidence - Multi-signal calibration
const confidence = check_confidence(
  {
    model_confidence: 0.75,
    evidence_count: retrieval.passages.length,
    complexity: 0.6,
    high_stakes: false
  },
  sessionContext
);

// Decision based on confidence
if (confidence.recommendation === 'proceed') {
  // Use response with RAG grounding
} else if (confidence.recommendation === 'abstain') {
  // Need more evidence, retrieve again with relaxed threshold
} else {
  // Low confidence, escalate to human review
}
```

### Performance Targets
- **rag_retrieve** (k=5): <200ms (actual: ~3-5ms)
- **rag_format_context**: <50ms (actual: ~0.2-0.5ms)
- **check_confidence**: <50ms (actual: ~0.05-0.1ms)
- **Full Pipeline**: <300ms (actual: ~10-20ms)

### Quality Metrics
- **Citation Coverage**: ≥90% of claims have supporting passages
- **Retrieval Precision**: ≥80% of retrieved passages are relevant
- **Calibration Error**: <0.1 target

### When to Use RAG
- ✅ Claims requiring Wolf-specific context
- ✅ Technical documentation references
- ✅ Architecture decision lookups
- ✅ Best practice queries
- ✅ Code pattern searches
- ❌ General knowledge facts (use CoVe with external sources)
- ❌ Real-time events (corpus may be stale)

**Implementation Location**: `servers/wolf-core-ip/tools/rag/`
**MCP Access**: `mcp__wolf-core-ip__rag_retrieve`, `mcp__wolf-core-ip__rag_format_context`

---

## ✅ Verification-First Pattern

### Purpose
Generate verification checklist BEFORE creating response to reduce hallucination and improve fact-checking.

### Why Verification-First?

Traditional prompting:
```
User Query → Generate Response → Verify Response (maybe)
```

Verification-first prompting:
```
User Query → Generate Verification Checklist → Use Checklist to Guide Response → Validate Against Checklist
```

### Checklist Sections (5 required)

```python
{
  "assumptions": [
    # Implicit beliefs or prerequisites
    "User has basic knowledge of quantum computing",
    "Latest = developments in past 12 months"
  ],
  "sources": [
    # Required information sources
    "Recent quantum computing research papers",
    "Industry announcements from major tech companies",
    "Academic conference proceedings"
  ],
  "claims": [
    # Factual assertions needing validation
    "IBM achieved 127-qubit quantum processor in 2021",
    "Google demonstrated quantum supremacy in 2019",
    "Quantum computers can break RSA encryption"
  ],
  "tests": [
    # Specific verification procedures
    "Verify IBM qubit count against official announcements",
    "Cross-check Google's quantum supremacy paper",
    "Validate RSA encryption vulnerability claims"
  ],
  "open_risks": [
    # Acknowledged limitations
    "Quantum computing field evolves rapidly, information may be outdated",
    "Technical accuracy depends on source reliability",
    "Simplified explanations may omit nuances"
  ]
}
```

### Basic Usage

```python
from verification.checklist_scaffold import create_verification_scaffold

# Initialize verification-first mode
scaffold = create_verification_scaffold(verification_first=True)

# Generate checklist BEFORE responding
user_prompt = "Explain the latest developments in quantum computing"
checklist_result = scaffold.generate_checklist(user_prompt)

# Use checklist to guide response generation
print(checklist_result["checklist"])
```

### Integration with Verification Pipeline

```python
# Step 1: Generate checklist
checklist = scaffold.generate_checklist(user_prompt)

# Step 2: Use CoVe to verify claims from checklist
for claim in checklist["claims"]:
    cove_report = await verify_claim(claim)
    if cove_report.overall_confidence < 0.7:
        print(f"Low confidence claim: {claim}")

# Step 3: Use HSP for safety validation
sentences = extract_sentences(generated_response)
claims = build_claims(sentences)
hsp_report = await validate_claims(claims)

# Step 4: Ground in evidence with RAG
passages = retrieve(user_prompt, n=5)
grounded_context = format_context(passages)

# Step 5: Check overall confidence
confidence = check_confidence({
    "model_confidence": 0.75,
    "evidence_count": len(passages),
    "complexity": assess_complexity(user_prompt)
})

# Step 6: Decide based on confidence
if confidence.recommendation == 'proceed':
    # Deliver response
elif confidence.recommendation == 'abstain':
    # Mark as "needs more research", gather more evidence
else:
    # Escalate to human review
```

### When to Use Verification-First
- ✅ **REQUIRED**: Any factual claims about historical events, dates, names
- ✅ **REQUIRED**: Technical specifications, API documentation, code behavior
- ✅ **REQUIRED**: Security recommendations or threat assessments
- ✅ **REQUIRED**: Performance claims or benchmarks
- ✅ **REQUIRED**: Compliance or governance statements
- ✅ **RECOMMENDED**: Complex multi-step reasoning
- ✅ **RECOMMENDED**: Novel or unusual claims
- ✅ **RECOMMENDED**: High-stakes decisions
- ❌ **OPTIONAL**: Simple code comments
- ❌ **OPTIONAL**: Internal notes or drafts
- ❌ **OPTIONAL**: Exploratory research (clearly marked as such)

**Implementation Location**: `/src/verification/checklist_scaffold.py`
**Documentation**: `/docs/public/verification/verification-first.md`

---

## 🔄 Integrated Verification Workflow

### Complete Self-Verification Pipeline

```python
# Step 1: Generate verification checklist FIRST (verification-first)
scaffold = create_verification_scaffold(verification_first=True)
checklist = scaffold.generate_checklist(task_description)

# Step 2: Create response/code/documentation
response = generate_response(task_description, checklist)

# Step 3: Verify factual claims with CoVe
factual_verification = await verify_claim("Your factual claim from response")

# Step 4: Safety check with HSP
sentences = extract_sentences(response)
claims = build_claims(sentences)
safety_check = await validate_claims(claims)

# Step 5: Ground in evidence with RAG
passages = retrieve(topic, n=5)
context = format_context(passages)

# Step 6: Check confidence
confidence = check_confidence({
    "model_confidence": 0.75,
    "evidence_count": len(passages),
    "complexity": assess_complexity(task_description),
    "high_stakes": is_high_stakes(task_description)
})

# Step 7: Decision
if confidence.recommendation == 'proceed':
    # Deliver output with verification report
    deliver(response, verification_report={
        "cove": factual_verification,
        "hsp": safety_check,
        "rag": passages,
        "confidence": confidence
    })
elif confidence.recommendation == 'abstain':
    # Mark as "needs more research"
    mark_for_review(response, reason="Medium confidence, need more evidence")
else:
    # Escalate to human review
    escalate(response, reason="Low confidence, human review required")
```

### Confidence Calibration

```python
# Multi-signal confidence assessment
confidence_signals = {
    "model_confidence": 0.75,    # LLM's self-reported confidence
    "evidence_count": 5,          # Number of supporting passages
    "complexity": 0.6,            # Task complexity (0-1)
    "high_stakes": False          # Is this safety-critical?
}

result = check_confidence(confidence_signals)

# Result recommendations:
# - 'proceed': High confidence (>0.8), use response
# - 'abstain': Medium confidence (0.5-0.8), need more evidence
# - 'escalate': Low confidence (<0.5), human review required
```

---

## Hallucination Detection & Elimination

### Detection

```typescript
import { detect } from './hallucination/detect';

const detection = await detect(generated_text, sessionContext);

// Returns:
// {
//   hallucinations_found: number,
//   hallucination_types: string[],  // e.g., ["factual_error", "unsupported_claim"]
//   confidence: number,
//   details: Array<{ text: string, type: string, severity: string }>
// }
```

### Elimination

```typescript
import { dehallucinate } from './hallucination/dehallucinate';

if (detection.hallucinations_found > 0) {
    const cleaned = await dehallucinate(
        generated_text,
        detection,
        sessionContext
    );
    // Use cleaned output instead
}
```

**Implementation Location**: `servers/wolf-core-ip/tools/hallucination/`

---

## Best Practices

### CoVe Best Practices
- ✅ Break complex claims into atomic steps
- ✅ Establish step dependencies clearly
- ✅ Use appropriate step types (factual, logical, etc.)
- ✅ Provide evidence sources for factual steps
- ❌ Don't create circular dependencies
- ❌ Don't combine multiple claims in one step

### HSP Best Practices
- ✅ Process text sentence-by-sentence
- ✅ Leverage built-in security features
- ✅ Configure timeouts for production
- ✅ Monitor validation failure rates
- ❌ Don't bypass input sanitization
- ❌ Don't ignore security warnings

### RAG Best Practices
- ✅ Set appropriate minimum score threshold
- ✅ Retrieve enough passages (k=5-10)
- ✅ Format with clear citations
- ✅ Check confidence before using
- ❌ Don't retrieve too few passages (k<3)
- ❌ Don't ignore low relevance scores

### Verification-First Best Practices
- ✅ Generate checklist BEFORE responding
- ✅ Use checklist to guide response structure
- ✅ Validate response against checklist
- ✅ Include open risks and limitations
- ❌ Don't skip checklist generation for "simple" tasks
- ❌ Don't ignore checklist during response creation

---

## Performance Summary

| Component | Target | Actual | Status |
|-----------|--------|--------|--------|
| CoVe (5 steps) | <200ms | ~150ms | ✅ |
| HSP (per claim) | <10ms | ~2ms | ✅ |
| RAG retrieve (k=5) | <200ms | ~3-5ms | ✅ |
| RAG format | <50ms | ~0.2-0.5ms | ✅ |
| Confidence check | <50ms | ~0.05-0.1ms | ✅ |
| Full pipeline | <300ms | ~10-20ms | ✅ |

---

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"This is low-stakes, no need for verification"** - STOP. Unverified claims compound. All factual claims need verification.
- ❌ **"I'll verify after I finish the response"** - NO. Use Verification-First pattern. Generate checklist BEFORE responding.
- ❌ **"The model is confident, that's good enough"** - Wrong. Model confidence ≠ factual accuracy. Always verify with external evidence.
- ❌ **"Verification is too slow for this deadline"** - False. Full pipeline averages <20ms. Verification saves time by preventing rework.
- ❌ **"I'll skip CoVe and just use RAG"** - NO. Each layer serves different purposes. CoVe = atomic facts, RAG = Wolf context, HSP = safety.
- ❌ **"This is just internal documentation, no need to verify"** - Wrong. Incorrect internal docs are worse than no docs. Verify anyway.
- ❌ **"Verification is optional for exploration"** - If generating factual claims, verification is MANDATORY. Mark speculation explicitly.

**STOP. Use verification tools BEFORE claiming anything is factually accurate.**

## After Using This Skill

**VERIFICATION IS CONTINUOUS** - This skill is called DURING work, not after

### When Verification Happens

**Called by wolf-governance:**
- During Definition of Done validation
- As part of quality gate assessment
- Before merge approval

**Called by wolf-roles:**
- During implementation checkpoints
- Before PR creation
- As continuous validation loop

**Called by wolf-archetypes:**
- When security lens applied (HSP required)
- When research-prototyper needs evidence
- When reliability-fixer validates root cause

### Integration Points

**1. With wolf-governance (Primary Caller)**
- **When**: Before declaring work complete
- **Why**: Verification is part of Definition of Done
- **How**:
  ```javascript
  // Governance checks if verification passed
  mcp__wolf-core-ip__check_confidence({
    model_confidence: 0.75,
    evidence_count: passages.length,
    complexity: 0.6,
    high_stakes: false
  })
  ```
- **Gate**: Cannot claim DoD complete without verification evidence

**2. With wolf-roles (Continuous Validation)**
- **When**: During implementation at checkpoints
- **Why**: Prevents late-stage verification failures
- **How**: Use verification-first pattern for each claim
- **Example**: coder-agent verifies API docs are accurate before committing

**3. With wolf-archetypes (Lens-Driven)**
- **When**: Security or research archetypes selected
- **Why**: Specialized verification requirements
- **How**:
  - Security-hardener → HSP for safety validation
  - Research-prototyper → CoVe for fact-checking
  - Reliability-fixer → Verification of root cause analysis

### Verification Checklist

Before claiming verification is complete:

- [ ] Generated verification checklist FIRST (verification-first pattern)
- [ ] Used appropriate verification layer:
  - [ ] CoVe for factual claims
  - [ ] HSP for safety validation
  - [ ] RAG for Wolf-specific context
- [ ] Checked confidence scores:
  - [ ] Overall confidence ≥0.8 for proceed
  - [ ] 0.5-0.8 = needs more evidence (abstain)
  - [ ] <0.5 = escalate to human review
- [ ] Documented verification results in journal
- [ ] Provided evidence sources for claims
- [ ] Identified and documented open risks

**Can't check all boxes? Verification incomplete. Return to this skill.**

### Verification Examples

#### Example 1: Feature Implementation

```yaml
Scenario: Coder-agent implementing user authentication

Verification-First:
  Step 1: Generate checklist BEFORE coding
    - Assumptions: User has email, password requirements known
    - Sources: OAuth 2.0 spec, bcrypt documentation
    - Claims: bcrypt is secure for password hashing
    - Tests: Verify bcrypt parameters against OWASP recommendations
    - Open Risks: Password requirements may need to evolve

  Step 2: Implement with checklist guidance

  Step 3: Verify claims with CoVe
    - Claim: "bcrypt is recommended by OWASP for password hashing"
    - CoVe verification: ✅ Confidence 0.95
    - Evidence: [OWASP Cheat Sheet, bcrypt documentation]

  Step 4: Check overall confidence
    - Model confidence: 0.85
    - Evidence count: 3 passages
    - Complexity: 0.4 (low)
    - Result: 'proceed' ✅

Assessment: Verified implementation, safe to proceed
```

#### Example 2: Security Review (Bad)

```yaml
Scenario: Security-agent reviewing authentication without verification

❌ What went wrong:
  - Skipped verification-first checklist generation
  - Assumed encryption was correct without verifying
  - No HSP safety validation performed
  - No evidence retrieved for claims

❌ Result:
  - Claimed "authentication is secure" without evidence
  - Missed hardcoded secrets (HSP would have caught)
  - Missed deprecated crypto usage (CoVe would have caught)
  - High confidence but no verification = hallucination

Correct Approach:
  1. Generate verification checklist for security claims
  2. Use HSP to scan for secrets, PII, unsafe patterns
  3. Use CoVe to verify crypto library recommendations
  4. Use RAG to ground in Wolf security best practices
  5. Check confidence before approving
  6. Document verification evidence in journal
```

### Performance vs Quality Trade-offs

**Verification is NOT slow:**
- Full pipeline: <20ms average
- CoVe (5 steps): ~150ms
- HSP (per claim): ~2ms
- RAG (k=5): ~3-5ms

**Cost of skipping verification:**
- Merge rejected due to factual errors: Hours of rework
- Security vulnerability shipped: Days to patch + incident response
- Documentation errors: Weeks of support burden + reputation damage

**Verification is an investment, not overhead.**

## Related Skills

- **wolf-principles**: Evidence-based decision making principle (#5)
- **wolf-governance**: Quality gate requirements (verification is DoD item)
- **wolf-roles**: Roles call verification at checkpoints
- **wolf-archetypes**: Lenses determine verification requirements
- **wolf-adr**: ADR-043 (Verification Architecture)
- **wolf-scripts-core**: Evidence validation patterns

## Integration with Other Skills

**Primary Chain Position**: Called DURING work (not after)

```
wolf-principles → wolf-archetypes → wolf-governance → wolf-roles
                                            ↓
                                    wolf-verification (YOU ARE HERE)
                                            ↓
                                    Continuous validation throughout implementation
```

**You are a supporting skill that enables quality:**
- Governance depends on you for evidence
- Roles depend on you for confidence
- Archetypes depend on you for lens validation

**DO NOT wait until the end to verify. Verify continuously.**

---

**Total Components**: 4 (CoVe, HSP, RAG, Verification-First)
**Test Coverage**: ≥90% required (achieved: 98%+)
**Production Status**: Active in Phase 50+

**Last Updated**: 2025-11-14
**Phase**: Superpowers Skill-Chaining Enhancement v2.0.0
**Version**: 1.1.0
