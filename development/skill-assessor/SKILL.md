---
name: skill-assessor
description: Orchestrate comprehensive assessment of newly created skills to determine if they should auto-trigger using context-gathering, code-analyzer, and optional research-expert agents with prioritized evaluation criteria
schema_version: 1.0
---

# skill-assessor

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK
**Priority:** Medium

## Trigger Reference

This skill activates on:
- **Keywords:** "assess skill", "skill assessment", "evaluate skill", "should this skill auto-trigger", "add skill to rules", "analyze skill", "skill auto-invoke"
- **Intent Patterns:** `(assess|evaluate|analyze).*?skill`, `skill.*?(assessment|evaluation|analysis)`, `auto.*?trigger.*?skill`, `should.*?skill.*?(auto|trigger)`

From: `skill-rules.json` - skill-assessor configuration

## Purpose

Orchestrate comprehensive assessment of newly created skills to determine if they should be added to `skill-rules.json` for auto-invocation. This skill provides systematic evaluation using multiple specialized agents and prioritized criteria to ensure only valuable skills auto-trigger while preventing skill bloat.

## Core Behavior

When a new skill file is detected in `.claude/skills/`, this skill coordinates a multi-phase assessment process:

1. **Deep Context Analysis** - Invoke context-gathering agent to thoroughly understand:
   - The skill's stated purpose and intended behavior
   - What problem it solves or what guidance it provides
   - Expected interaction patterns with users
   - Technical domain and scope

2. **Codebase Pattern Analysis** - Invoke code-analyzer agent to identify:
   - How frequently the skill's domain appears in the codebase
   - Specific file patterns, code structures, or scenarios where skill applies
   - Edge cases where skill should/shouldn't trigger
   - Estimated token cost impact of loading skill frequently

3. **Optional Domain Research** - Invoke research-expert agent (when appropriate) for:
   - Domain-specific best practices and terminology
   - Common workflows in the industry that should trigger the skill
   - External validation for trigger keyword selection
   - Community standards and patterns

4. **Prioritized Evaluation** - Assess skill against three-tier criteria:
   - **(c) Guardrails/Safety** (HIGHEST) - Does it prevent mistakes or enforce framework rules?
   - **(b) Frequency** (MEDIUM) - Does it apply to common scenarios (>60% relevance)?
   - **(a) Convenience** (LOWEST) - Does it merely save time without protection or frequency?

5. **Token Cost Analysis** - Calculate value score using formula:
   ```
   Value Score = (Relevance Rate × Impact) - (Token Cost × Noise Rate)

   Where:
   - Relevance Rate = % of triggers where skill is actually useful (0.0-1.0)
   - Impact = Benefit level (Guardrail=1.0, Frequent=0.6, Convenience=0.3)
   - Token Cost = Skill file size in tokens / 1000 (normalize)
   - Noise Rate = % of triggers where skill is not useful (1.0 - Relevance Rate)

   Threshold: Value Score > 0.4 for auto-invocation consideration

   Example (350-token skill, 70% relevant, frequent use):
   Value Score = (0.70 × 0.6) - (0.35 × 0.30) = 0.42 - 0.105 = 0.315 → MANUAL-ONLY
   ```

6. **Generate Recommendation** - Produce structured assessment with:
   - Clear AUTO-INVOKE or MANUAL-ONLY recommendation
   - Detailed rationale with supporting evidence
   - Suggested trigger configuration (keywords + intent patterns)
   - Confidence level (HIGH/MEDIUM/LOW)
   - Next steps for implementation

## Assessment Process (Step-by-Step)

### Phase 1: Skill Understanding

**Invoke context-gathering agent** with prompt:
```
Analyze the skill file at `.claude/skills/[skill-name]/SKILL.md` and provide:
1. Comprehensive summary of skill's purpose and behavior
2. Identification of the problem domain it addresses
3. Expected user interaction patterns
4. Technical scope and dependencies
5. Any stated constraints or limitations
```

**Expected output:** Verbose narrative explaining what the skill does and when it would be valuable.

### Phase 2: Codebase Analysis

**Invoke code-analyzer agent** with prompt:
```
Search the codebase for patterns related to [skill domain]. Identify:
1. How frequently these patterns appear (file count, occurrence count)
2. Specific locations where skill would apply (file:line examples)
3. Edge cases where skill should NOT trigger
4. Estimated token cost impact if skill loads on every match
```

**Expected output:** Structured data on pattern frequency, locations, and token considerations.

### Phase 3: Domain Research (Optional)

**Invoke research-expert agent** (only when domain is specialized) with prompt:
```
Research industry best practices for [skill domain]:
1. Common terminology developers use when discussing this domain
2. Standard workflows that should trigger this skill
3. Tools, frameworks, or patterns commonly associated with this domain
4. Keywords that naturally indicate user intent in this area
```

**Expected output:** External validation for trigger keywords and intent patterns.

### Phase 4: Evaluation Against Criteria

**Guardrails/Safety Assessment (Highest Priority):**
- **Question:** Does this skill prevent framework violations, enforce SoT discipline, or catch errors before they occur?
- **Examples:** framework_version_check (prevents drift), write-gating enforcement
- **Decision:** If YES → Recommend AUTO-INVOKE regardless of frequency
- **Score:** HIGH/MEDIUM/LOW

**Frequency Assessment (Medium Priority):**
- **Question:** How often do users work on tasks in this domain?
- **Metric:** Codebase coverage % (>10% files = frequent, <5% = rare)
- **Metric:** Relevance rate (% of matches where skill truly applies)
- **Threshold:** >60% relevance for auto-invocation consideration
- **Decision:** If frequent AND relevant → Recommend AUTO-INVOKE
- **Score:** HIGH/MEDIUM/LOW

**Convenience Assessment (Lower Priority):**
- **Question:** Does this skill merely save time without protection or frequency?
- **Decision:** If ONLY convenience → Recommend MANUAL-ONLY
- **Score:** HIGH/MEDIUM/LOW

**Token Cost Analysis:**
- Measure skill file size in tokens (use context-gathering output)
- Estimate trigger rate based on keyword frequency in typical conversations
- Calculate token waste: (Token Cost × Noise Rate)
- If token waste is high (>0.3), downgrade recommendation

### Phase 5: Generate Recommendation

Produce assessment in this structured format:

```markdown
# Skill Assessment: [skill-name]

## Assessment Summary
- **Skill Type**: [ANALYSIS-ONLY | WRITE-CAPABLE]
- **Purpose**: [one-sentence description]
- **Recommendation**: [AUTO-INVOKE | MANUAL-ONLY]
- **Confidence**: [HIGH | MEDIUM | LOW]

## Evaluation Criteria

### Guardrails/Safety: [HIGH | MEDIUM | LOW]
[Explanation of safety impact with specific examples]

### Frequency: [HIGH | MEDIUM | LOW]
- **Codebase Coverage**: [X]% of files contain relevant patterns
- **Pattern Occurrences**: [Y] instances found
- **Relevance Rate**: [Z]% of triggers would be useful
- **Example Locations**:
  - [file:line]
  - [file:line]

### Convenience: [HIGH | MEDIUM | LOW]
[Explanation of time-saving impact]

### Token Cost Analysis
- **Skill File Size**: [X] tokens
- **Estimated Trigger Rate**: [Y]% of messages
- **Value Score**: [calculated score]
- **Token Waste Risk**: [ACCEPTABLE | CONCERNING | HIGH]

## Recommended Trigger Configuration

```json
{
  "promptTriggers": {
    "keywords": [
      "keyword1",
      "keyword2",
      "keyword3"
    ],
    "intentPatterns": [
      "pattern1",
      "pattern2"
    ]
  }
}
```

**Rationale for triggers:**
- Keywords chosen based on [reasoning]
- Intent patterns capture [use cases]

## Rationale

[Detailed explanation of recommendation with supporting evidence from:
- Context analysis findings
- Codebase analysis data
- Domain research insights (if applicable)
- Token cost calculations]

## Next Steps

If you approve this recommendation:
1. Add the above configuration to `.claude/skills/skill-rules.json` under `skills.[skill-name]`
2. Set `skillType`, `daicMode.allowedModes`, `enforcement`, and `priority` appropriately
3. Test auto-triggering by using suggested keywords in a message
4. Monitor effectiveness over next 10-20 usages
5. Adjust triggers if auto-trigger rate is too low (<60%) or too high (>80% noise)

**Log this decision**: Copy this assessment to `context/decisions.md` using the template below.
```

## Safety Guardrails

This skill enforces critical safety rules:

1. **NEVER auto-modifies skill-rules.json** - All changes require explicit user approval
2. **Conservative bias** - When in doubt, recommend MANUAL-ONLY
3. **Token cost awareness** - Always analyze and report token impact
4. **LCMP logging required** - Every assessment must be logged for pattern learning
5. **No write tools** - ANALYSIS-ONLY skill cannot call Edit/Write/MultiEdit

## LCMP Logging Template

After each assessment, the following should be added to `context/decisions.md`:

```markdown
### Skill Assessment: [skill-name] - [YYYY-MM-DD]

**Skill File:** `.claude/skills/[skill-name]/SKILL.md`
**Assessed By:** skill-assessor (context-gathering + code-analyzer [+ research-expert])

**Purpose**: [Brief description of what skill does]

**Evaluation Criteria**:
- Guardrails/Safety: [HIGH/MEDIUM/LOW]
- Frequency: [HIGH/MEDIUM/LOW] ([percentage]% of codebase)
- Convenience: [HIGH/MEDIUM/LOW]
- Token Cost: [tokens] ([ACCEPTABLE/CONCERNING/HIGH])
- Value Score: [calculated score]

**Codebase Analysis**:
- Patterns found: [number] occurrences in [number] files
- File types: [list]
- Example locations: [file:line examples]

**Trigger Recommendations**:
```json
{
  "keywords": ["keyword1", "keyword2"],
  "intentPatterns": ["pattern1", "pattern2"]
}
```

**Final Recommendation**: [AUTO-INVOKE | MANUAL-ONLY]

**Rationale**: [1-2 sentence summary]

**User Decision**: [APPROVED | REJECTED | DEFERRED]
**Decision Date**: [YYYY-MM-DD]
**Notes**: [Any additional context or follow-up actions]
```

## Usage Examples

**Example 1: User creates new skill and asks for assessment**

User: "I just created a new skill for database schema migrations. Should I add it to auto-trigger?"

skill-assessor response:
- Invokes context-gathering to understand the skill
- Invokes code-analyzer to search for migration patterns
- Evaluates: Frequency is LOW (migrations are infrequent), Convenience is MEDIUM
- Recommendation: MANUAL-ONLY (infrequent use doesn't justify auto-trigger)

**Example 2: Hook detects new skill creation**

[Hook detects `.claude/skills/api-design-assistant/SKILL.md` was created]
Hook stderr: "[New Skill Detected] api-design-assistant/SKILL.md created but not yet in skill-rules.json..."

Claude: "I'll assess this skill using skill-assessor."

skill-assessor response:
- Invokes context-gathering to understand the skill
- Invokes code-analyzer to find API route patterns
- Evaluates: Frequency is HIGH (30% of files contain routes), Convenience is HIGH
- Recommendation: AUTO-INVOKE with triggers ["api design", "endpoint", "route"]

**Example 3: Guardrail skill (highest priority)**

User: "Should my new framework_repair_suggester skill auto-trigger?"

skill-assessor response:
- Invokes context-gathering to understand the skill
- Evaluates: Guardrails/Safety is HIGH (prevents framework errors)
- Recommendation: AUTO-INVOKE (guardrail skills always recommended regardless of frequency)

## Integration with Hook System

This skill works in conjunction with the `post_tool_use.js` hook:

1. Hook detects new skill file creation in `.claude/skills/*/SKILL.md`
2. Hook prints stderr suggestion to assess the skill
3. Claude sees the suggestion and invokes skill-assessor
4. skill-assessor orchestrates agent analysis and evaluation
5. User reviews recommendation and approves/rejects
6. If approved, user manually adds configuration to `skill-rules.json`
7. Assessment is logged in `context/decisions.md` for future reference

## Related Skills

This skill works in conjunction with:

- **context-gathering** - Used to deeply understand new skill's purpose, domain, and expected behavior patterns
- **code-analyzer** - Used to find codebase patterns where skill applies and analyze frequency/relevance
- **research-expert** - Optionally used for domain-specific research and external validation of trigger keywords
- **framework_health_check** - To validate that the skill system is working correctly after assessment
- **skill-developer** - If skill system modifications or improvements are needed based on assessment findings
- **framework_repair_suggester** - If assessment reveals framework issues that need REPAIR tasks

## Notes

- This skill itself is ANALYSIS-ONLY and can run in any DAIC mode
- It provides recommendations but never modifies `skill-rules.json` automatically
- Conservative approach: when uncertain, recommend MANUAL-ONLY
- Token cost analysis is mandatory for every assessment
- All assessments must be logged in `context/decisions.md` for pattern learning and future reference