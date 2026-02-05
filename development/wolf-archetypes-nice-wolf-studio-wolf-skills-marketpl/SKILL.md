---
name: wolf-archetypes
description: Behavioral archetypes for automatic agent adaptation based on work type
version: 1.2.0
triggers:
  - "select archetype"
  - "behavioral profile"
  - "work type"
  - "agent behavior"
  - "overlay lens"
---

# Wolf Archetypes Skill

This skill provides Wolf's behavioral archetype system that automatically adapts agent behavior based on work type. The system includes 11 core archetypes and 4 overlay lenses, refined over 50+ phases of development.

## When to Use This Skill

- **REQUIRED** at the start of any new work item
- When GitHub issue labels change
- For work type classification and prioritization
- When determining evidence requirements
- For applying specialized quality gates

## The 11 Behavioral Archetypes

### 1. product-implementer
**Triggers**: `feature`, `enhancement`, `user-story`
**Priorities**: Delivery speed, user value, completeness
**Evidence Required**: Acceptance criteria met, tests pass, documentation updated
**Use When**: Building new features or enhancing existing functionality

### 2. security-hardener
**Triggers**: `security`, `auth`, `crypto`, `vulnerability`
**Priorities**: Threat reduction, defense-in-depth, least privilege
**Evidence Required**: Threat model, security scan results, penetration test outcomes
**Use When**: Security-sensitive work requiring specialized threat analysis

### 3. perf-optimizer
**Triggers**: `perf`, `performance`, `optimization`, `slow`
**Priorities**: Latency reduction, throughput increase, resource efficiency
**Evidence Required**: Baseline metrics, post-change metrics, performance budgets
**Use When**: Performance work requiring measurement-driven approach

### 4. reliability-fixer
**Triggers**: `bug`, `regression`, `hotfix`, `incident`
**Priorities**: Root cause analysis, prevention, stability
**Evidence Required**: Root cause documented, tests prevent recurrence, monitoring added
**Use When**: Bug fixes requiring systematic analysis and prevention

### 5. research-prototyper
**Triggers**: `spike`, `research`, `explore`, `prototype`
**Priorities**: Learning, hypothesis validation, risk reduction
**Evidence Required**: Findings documented, recommendations provided, risks identified
**Use When**: Exploration work needing timeboxing and validation

### 6. repository-hygienist
**Triggers**: `hygiene`, `cleanup`, `dependencies`, `gitignore`
**Priorities**: Maintainability, consistency, prevention
**Evidence Required**: Before/after metrics, automation added, recurrence prevented
**Use When**: Repository maintenance requiring systematic cleanup

### 7. accessibility-champion
**Triggers**: `a11y`, `accessibility`, `wcag`, `inclusive-design`
**Priorities**: WCAG compliance, inclusive design, usability
**Evidence Required**: WCAG audit results, screen reader validation, keyboard navigation tests
**Use When**: Accessibility work requiring domain expertise

### 8. data-contract-steward
**Triggers**: `schema`, `migration`, `api`, `contract`, `breaking-change`
**Priorities**: Backward compatibility, safe migration, version management
**Evidence Required**: Migration plan, compatibility matrix, rollback procedure
**Use When**: Contract changes requiring compatibility planning

### 9. platform-gardener
**Triggers**: `infrastructure`, `ci-cd`, `build-system`, `platform`
**Priorities**: Developer productivity, system reliability, automation
**Evidence Required**: Productivity metrics, uptime stats, automation coverage
**Use When**: Platform work affecting team productivity

### 10. maintainability-refactorer
**Triggers**: `refactor`, `tech-debt`, `code-quality`, `patterns`
**Priorities**: Code clarity, pattern consistency, future-proofing
**Evidence Required**: Complexity reduction metrics, test coverage maintained, behavior unchanged
**Use When**: Refactoring requiring discipline to avoid behavior changes

### 11. ai-assist-conductor
**Triggers**: `ai-assist`, `prompt-engineering`, `model-coordination`
**Priorities**: Human oversight, validation, prompt optimization
**Evidence Required**: Human review completed, outputs validated, prompts documented
**Use When**: AI-assisted work requiring human validation

## The 4 Overlay Lenses

Lenses can be applied on top of any archetype to add specialized requirements:

### 🎯 Performance Lens
**Requirements**:
- Measurement before and after changes
- Performance budgets defined
- Benchmarks documented

**Evidence**:
- Baseline metrics captured
- Post-change metrics validated
- p95 latency targets met

**Apply When**: Work impacts system performance or has latency requirements

### 🔒 Security Lens
**Requirements**:
- Threat modeling completed
- Security validation performed
- Defense-in-depth applied

**Evidence**:
- Threat analysis documented
- Security scan results clean
- Penetration test passed

**Apply When**: Work touches authentication, authorization, data protection, or crypto

### ♿ Accessibility Lens
**Requirements**:
- WCAG compliance checked
- Inclusive design principles followed
- Screen reader support verified

**Evidence**:
- WCAG audit results documented
- Keyboard navigation tested
- Screen reader validation completed

**Apply When**: Work involves UI/UX or user-facing features

### 📊 Observability Lens
**Requirements**:
- Logging implemented
- Metrics collected
- Distributed tracing enabled

**Evidence**:
- Log coverage adequate
- Metric dashboards created
- Trace examples provided

**Apply When**: Work involves distributed systems or debugging requirements

## Archetype Selection Process

1. **Primary Selection**: Based on GitHub issue labels (first match wins)
   - Security labels → `security-hardener`
   - Performance labels → `perf-optimizer`
   - Bug labels → `reliability-fixer`
   - Feature labels → `product-implementer` (default)

2. **File-Based Triggers**: Secondary selection based on files modified
   - `**/auth/**` → `security-hardener`
   - `**/benchmark/**` → `perf-optimizer`
   - `.github/workflows/**` → `platform-gardener`

3. **Confidence Overrides**:
   - Low confidence (<5/10) → Force `research-prototyper`
   - High risk (multiple risk labels) → Upgrade to `reliability-fixer`

4. **Lens Application**: Stack lenses based on additional requirements
   - Can combine multiple lenses (e.g., security + performance)
   - Lenses add requirements, don't replace archetype

## How to Use Archetypes

### Automatic Selection
```javascript
// Based on GitHub labels
const labels = ['feature', 'security', 'performance'];
const archetype = selectArchetype(labels);
// Returns: 'security-hardener' (security takes precedence)
```

### Manual Override
```javascript
// Force specific archetype for special cases
const archetype = forceArchetype('research-prototyper', 'Unknown territory');
```

### With Lenses
```javascript
// Apply multiple lenses to an archetype
const profile = {
  archetype: 'product-implementer',
  lenses: ['performance', 'accessibility']
};
```

## Archetype Combinations

When multiple labels are present:

- **Security + Performance**: Primary = `security-hardener`, add performance evidence
- **Bug + Performance**: Primary = `reliability-fixer`, add performance checks
- **Refactor + Features**: Reject - should be separate PRs

### Good/Bad Examples: Archetype Selection

#### Example 1: Feature Development

<Good>
**Issue #123: Add user profile dashboard**

**Labels**: `feature`, `enhancement`, `user-story`

**How to Select**:
- Use Skill tool to load wolf-archetypes
- Based on labels: `feature`, `enhancement`, `user-story`
- Work description: "Create dashboard showing user profile, activity history, and settings"

**Selected Archetype**: `product-implementer`

**Why this is correct**:
- Primary label is `feature` → product-implementer
- Work is clearly additive (new functionality)
- Priorities align: delivery speed, user value, completeness

**Evidence Requirements**:
- ✅ Acceptance criteria met
- ✅ Tests pass (unit + integration + E2E)
- ✅ Documentation updated
- ✅ User-facing feature requires accessibility lens

**Execution**:
- Implements incrementally (Principle #9)
- Creates PR with tests + docs + journal
- Requests review from code-reviewer-agent
- Cannot merge own PR
</Good>

<Bad>
**Issue #124: Add user dashboard**

**Labels**: `feature`, `enhancement`, `user-story`, `refactor`, `performance`, `security`

**Mistake**: "I'll handle everything in one PR"

**Why this is wrong**:
- ❌ Mixed archetypes (product-implementer + maintainability-refactorer + perf-optimizer + security-hardener)
- ❌ Impossible to review - too many concerns
- ❌ Cannot determine primary priority order
- ❌ Evidence requirements conflict
- ❌ Violates Principle #9 (incremental value)

**Correct Approach**:
Split into separate PRs:
1. **PR #1**: Security review of existing code (`security-hardener`)
2. **PR #2**: Refactor for performance (`maintainability-refactorer` + performance lens)
3. **PR #3**: Add user dashboard feature (`product-implementer` + accessibility lens)

Each PR has clear archetype, focused scope, and distinct evidence requirements.
</Bad>

#### Example 2: Bug Fix

<Good>
**Issue #456: Login fails after 3rd retry**

**Labels**: `bug`, `regression`, `high-priority`

**How to Select**:
- Use Skill tool to load wolf-archetypes
- Based on labels: `bug`, `regression`, `high-priority`
- Work description: "Users cannot login after 3 failed attempts, need to investigate retry logic"

**Selected Archetype**: `reliability-fixer`

**Why this is correct**:
- Primary label is `bug` → reliability-fixer
- Work focuses on stability and prevention
- Priorities: root cause analysis, prevention, stability

**Evidence Requirements**:
- ✅ Root cause documented in journal
- ✅ Regression test added (watch it fail, then pass)
- ✅ Monitoring enhanced to prevent recurrence
- ✅ All tests passing

**Execution**:
- Documents root cause: race condition in retry counter
- Adds regression test reproducing the issue
- Fixes the bug
- Adds monitoring for retry failures
- Creates journal with learnings
</Good>

<Bad>
**Issue #457: Login broken**

**Labels**: `bug`

**Mistake**: Assumed `product-implementer` because "I'm adding better login"

**Why this is wrong**:
- ❌ Ignored `bug` label (should be `reliability-fixer`)
- ❌ "Better login" = feature addition during bug fix
- ❌ No root cause analysis (reliability-fixer requirement)
- ❌ Mixed fix + enhancement in one PR

**What happens**:
- Agent codes "improved" login flow
- Original bug still present
- Added new features without proper testing
- No regression test for original issue
- Cannot determine if bug was actually fixed

**Correct Approach**:
1. Use `reliability-fixer` archetype for Issue #457
2. Document root cause
3. Add regression test
4. Fix ONLY the bug
5. Create separate Issue #458 for login improvements (`product-implementer`)
</Bad>

#### Example 3: Security Work

<Good>
**Issue #789: SQL injection vulnerability in search**

**Labels**: `security`, `vulnerability`, `critical`

**How to Select**:
- Use Skill tool to load wolf-archetypes
- Based on labels: `security`, `vulnerability`, `critical`
- Work description: "User input in search not properly sanitized, allows SQL injection"

**Selected Archetype**: `security-hardener`

**Why this is correct**:
- Primary label is `security` → security-hardener
- Work requires specialized security analysis
- Priorities: threat reduction, defense-in-depth, least privilege

**Evidence Requirements**:
- ✅ Threat model: SQL injection attack vectors documented
- ✅ Security scan: Clean results after fix
- ✅ Penetration test: Manual SQL injection attempts blocked
- ✅ Defense-in-depth: Parameterized queries + input validation + WAF rules

**Execution**:
- Creates threat model
- Implements parameterized queries
- Adds input validation layer
- Updates WAF rules
- Runs security scan
- Manual penetration testing
- Documents in journal
- Requires security-agent review
</Good>

<Bad>
**Issue #790: Fix search**

**Labels**: `bug`, `search`

**Mistake**: Used `reliability-fixer` for security vulnerability

**Why this is dangerous**:
- ❌ Security vulnerability labeled as generic bug
- ❌ `reliability-fixer` doesn't require threat model
- ❌ No security-agent review required
- ❌ No penetration testing
- ❌ Might fix symptom without understanding threat

**What happens**:
- Agent adds basic input validation
- Doesn't understand full attack surface
- Single-layer defense (no depth)
- No security scan performed
- Vulnerability might remain exploitable via other vectors

**Correct Approach**:
1. **Re-label** Issue #790 with `security`, `vulnerability`
2. Use `security-hardener` archetype
3. Create threat model
4. Implement defense-in-depth
5. Require security-agent review
6. Run security scan + penetration test
</Bad>

#### Example 4: Research/Exploration

<Good>
**Issue #999: Explore GraphQL vs REST for new API**

**Labels**: `spike`, `research`, `architecture`

**How to Select**:
- Use Skill tool to load wolf-archetypes
- Based on labels: `spike`, `research`, `architecture`
- Work description: "Evaluate GraphQL vs REST for upcoming API redesign, need recommendation"

**Selected Archetype**: `research-prototyper`

**Why this is correct**:
- Primary label is `research` → research-prototyper
- Work is exploratory, not implementation
- Priorities: learning, hypothesis validation, risk reduction

**Evidence Requirements**:
- ✅ Findings documented (comparison matrix)
- ✅ Recommendations provided with rationale
- ✅ Risks identified for each option
- ✅ Prototype code (throwaway, not production)
- ✅ Timebox: 1-2 days max

**Execution**:
- Creates comparison matrix (performance, complexity, ecosystem)
- Builds small prototype of each
- Benchmarks typical operations
- Documents findings in journal
- Makes recommendation in ADR
- **Does not implement production code**
</Good>

<Bad>
**Issue #998: Try GraphQL**

**Labels**: `feature`

**Mistake**: Used `product-implementer` for research work

**Why this fails**:
- ❌ Research mislabeled as feature
- ❌ `product-implementer` expects production-ready code
- ❌ No timebox (research can expand infinitely)
- ❌ Prototype code might become production

**What happens**:
- Agent starts implementing GraphQL fully
- Weeks of work without validation
- No comparison with alternatives
- Prototype becomes "production" without proper testing
- No ADR documenting decision rationale

**Correct Approach**:
1. **Re-label** Issue #998 as `spike`, `research`
2. Use `research-prototyper` archetype
3. Timebox to 2 days
4. Create comparison ADR
5. **After research complete**, create Issue #1000: "Implement GraphQL" with `feature` label (`product-implementer`)
</Bad>

#### Example 5: Multiple Lenses

<Good>
**Issue #555: Add payment processing**

**Labels**: `feature`, `security`, `performance`, `critical`

**How to Select**:
- Use Skill tool to load wolf-archetypes
- Based on labels: `feature`, `security`, `performance`, `critical`
- Work description: "Integrate Stripe payment processing with encryption and sub-100ms latency"

**Selected Archetype**: `product-implementer` + **security lens** + **performance lens**

**Why this is correct**:
- Primary archetype: `product-implementer` (it's a feature)
- Security lens: Payment data requires security-hardener evidence
- Performance lens: Sub-100ms latency requires perf-optimizer evidence

**Evidence Requirements**:
- **Product-implementer**: AC met, tests, docs, journal
- **+ Security lens**: Threat model, security scan, PCI compliance
- **+ Performance lens**: Baseline metrics, post-change metrics, latency budgets

**Execution**:
- Implements Stripe integration (feature)
- Creates threat model for payment data (security lens)
- Encrypts payment details (security lens)
- Runs security scan (security lens)
- Benchmarks payment flow (performance lens)
- Optimizes to <100ms (performance lens)
- All evidence documented

**Assessment**: Properly handles multi-faceted requirements through lens stacking
</Good>

<Bad>
**Issue #556: Add payments**

**Labels**: `feature`

**Mistake**: Ignored security and performance requirements

**Why this fails**:
- ❌ Payment processing = critical security requirement (missing security lens)
- ❌ No threat model for sensitive data
- ❌ No performance validation
- ❌ Might violate PCI compliance

**What happens**:
- Agent implements basic Stripe integration
- No encryption consideration
- No security scan
- No performance benchmarking
- Latency might be 500ms+ (unusable)
- Fails security audit in production

**Correct Approach**:
1. **Add labels**: `security`, `performance` to Issue #556
2. Use `product-implementer` + security lens + performance lens
3. Complete evidence for all three: feature + security + performance
</Bad>

## Anti-Patterns to Avoid

### ❌ Cowboy Coder
- Skips process and quality gates
- Large PRs without justification (>500 lines)
- Missing tests on logic changes
- Bypasses required checks

**Prevention**: Archetype system enforces gates

### ❌ Analysis Paralysis
- Over-researching simple problems
- Excessive documentation for trivial changes
- Delayed delivery without value

**Prevention**: Time-boxed research archetypes

## Scripts Available

- `select.js` - Automatically select archetype based on labels/context
- `compose.js` - Combine archetype with overlay lenses
- `validate.js` - Validate work against archetype requirements

## Integration with Other Skills

- **wolf-principles**: Archetypes implement core principles
- **wolf-roles**: Each role adapts behavior per archetype
- **wolf-governance**: Archetypes enforce governance rules

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"Starting implementation without selecting archetype"** - STOP. Archetype selection is MANDATORY. Use MCP tool NOW.
- ❌ **"This work doesn't fit any archetype"** - Wrong. Use `research-prototyper` for unknown territory. Every work fits.
- ❌ **"Applying multiple archetypes to one PR"** - STOP. Split the work into separate PRs with distinct archetypes.
- ❌ **"Skipping archetype because 'it's obvious'"** - Selection is NOT optional. Evidence before assumptions.
- ❌ **"I'll select the archetype after I start coding"** - Too late. Archetype GUIDES implementation choices.
- ❌ **"This is a hotfix, no time for archetypes"** - Hotfixes use `reliability-fixer`. Still requires archetype.
- ❌ **"Archetypes are just documentation"** - NO. Archetypes enforce quality gates and evidence requirements.

**STOP. Use Skill tool to load wolf-archetypes BEFORE proceeding.**

## After Using This Skill

**REQUIRED NEXT STEPS:**

```
Sequential skill chain - DO NOT skip steps
```

1. **REQUIRED NEXT SKILL**: Use **wolf-governance** to identify Definition of Done and quality gates
   - **Why**: Archetype defines priorities and evidence. Governance defines concrete acceptance criteria and gates.
   - **Gate**: Cannot start implementation without knowing Definition of Done
   - **Tool**: Use Skill tool to load wolf-governance
   - **Example**: `security-hardener` requires threat model + security scan gates

2. **REQUIRED NEXT SKILL**: Use **wolf-roles** to understand role-specific behavior
   - **Why**: Archetypes define WHAT evidence is needed. Roles define HOW to produce it.
   - **Gate**: Cannot proceed without understanding collaboration patterns
   - **Tool**: Use Skill tool to load wolf-roles
   - **Example**: `pm-agent` translates archetype into acceptance criteria, `coder-agent` implements

3. **REQUIRED IF LENSES APPLIED**: Use **wolf-verification** to understand verification requirements
   - **Why**: Overlay lenses (security, performance, accessibility, observability) add verification steps
   - **Gate**: Cannot skip verification when lenses are active
   - **When**: Applied if security/perf/a11y/observability lenses detected
   - **Example**: Security lens requires threat modeling + scan validation

**DO NOT PROCEED to implementation without completing steps 1-3.**

### Verification Checklist

Before claiming archetype is properly applied:

- [ ] Archetype selected using MCP tool (not guessed)
- [ ] Evidence requirements identified for selected archetype
- [ ] Overlay lenses identified (security/perf/a11y/observability)
- [ ] Governance gates loaded for this archetype
- [ ] Role guidance loaded for collaboration patterns
- [ ] Definition of Done understood and documented

**Can't check all boxes? Archetype selection incomplete. Return to this skill.**

### Archetype-to-Governance Mapping Examples

**Example 1: product-implementer**
- Governance Gates: Acceptance criteria met, tests pass, documentation updated
- Definition of Done: Feature complete, tested, documented, deployed
- Skip If: Work is exploration (use `research-prototyper` instead)

**Example 2: security-hardener**
- Governance Gates: Threat model approved, security scan clean, pen test passed
- Definition of Done: Threats mitigated, scan results clear, monitoring active
- Skip If: No security impact (downgrade to appropriate archetype)

**Example 3: reliability-fixer**
- Governance Gates: Root cause documented, regression test added, monitoring enhanced
- Definition of Done: Bug fixed, prevention in place, recurrence impossible
- Skip If: Not a bug (likely `product-implementer` or `maintainability-refactorer`)

---

*Source: agents/archetypes/registry.yml, README.md*
*Last Updated: 2025-11-14*
*Phase: Superpowers Skill-Chaining Enhancement v2.0.0*