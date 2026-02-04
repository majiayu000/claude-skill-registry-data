---
name: check-constitutional-alignment
description: Verify feature requests align with project constitutional principles - applies decision framework systematically and provides clear align/reject/revise recommendation with detailed reasoning
---

# Check Constitutional Alignment

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: check-constitutional-alignment | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: check-constitutional-alignment | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



You are evaluating whether a proposed feature or change aligns with the project's constitutional principles, serving as a firewall against scope creep and principle violations.

## Purpose

The constitution exists to prevent:
- Scope creep from "interesting but misaligned" features
- Violations of core design values
- Decisions that contradict established principles
- Accumulation of inconsistent patterns

This skill provides systematic, documented evaluation using the project's own decision framework.

## When to Use

Invoke this skill:
- **Before creating specifications** for new features
- **During feature discussions** when user proposes new work
- **When reviewing PRs** that introduce significant changes
- **Before roadmap updates** that add new phases/features
- **When uncertain** whether something fits the project

## Evaluation Process

### Phase 1: Read the Constitution

**Load constitutional principles:**

```bash
cat .wrangler/CONSTITUTION.md
```

**Extract key information:**

1. **North Star Mission**: What is the core purpose?
2. **Core Principles**: List all principles (typically 3-7)
3. **Decision Framework**: What questions must be answered?
4. **Anti-patterns**: What explicitly should NOT be done?

**Store mentally** for application in next phases.

### Phase 2: Understand the Proposal

**Gather complete picture of proposed feature:**

**Ask clarifying questions if needed:**
- "What problem does this solve for users?"
- "Who benefits from this feature?"
- "What's the simplest version of this that provides value?"
- "Are there existing features that already solve this?"
- "What would happen if we didn't build this?"

**Document proposal clearly:**

```markdown
## Proposal Summary

**Feature**: [Name/title]

**Description**: [What it does in 2-3 sentences]

**User Value**: [Problem it solves]

**Scope**: [What's included/excluded]

**Alternatives Considered**: [Other approaches, if any]
```

### Phase 3: Apply Decision Framework

**The constitution has a decision framework (5 standard questions).**

**For EACH question, provide detailed analysis:**

#### Question 1: Constitutional Alignment

"Does this align with our core principles?"

**Process:**
1. List each principle from constitution
2. For each principle, analyze alignment:
   - ✅ **Aligns**: How this feature supports the principle
   - ❌ **Conflicts**: How this feature violates the principle
   - ⚠️ **Neutral**: Principle doesn't apply to this feature

**Example analysis:**

```markdown
### Principle 1: Simplicity Over Features

**Assessment**: ❌ **Conflicts**

**Reasoning**: This feature adds 12 new configuration options, violating the principle "Prefer convention over configuration." The constitution explicitly lists "configuration for every possible option" as an anti-pattern.

**Relevant Quote**: "Delete code before adding configuration options" - This adds configuration instead of removing it.
```

```markdown
### Principle 2: Privacy by Default

**Assessment**: ✅ **Aligns**

**Reasoning**: Feature requires explicit user consent before data collection, following the "opt-in, not opt-out" principle. Aligns with anti-pattern "Collecting data without clear user benefit."

**Relevant Quote**: "Users MUST explicitly enable telemetry" - This feature follows that pattern.
```

**Repeat for all principles.**

#### Question 2: User Value

"Does this solve a real user problem?"

**Criteria:**
- Evidence of user pain (GitHub issues, support tickets, user feedback)
- Clear user benefit (what gets better/faster/easier)
- NOT just "nice to have" or "might be useful someday"

**Analysis template:**

```markdown
### User Value Assessment

**Problem Statement**: [What user problem exists?]

**Evidence**:
- [GitHub issue #X]: 10 users requested this
- [Support tickets]: 5 tickets per week about this pain point
- [User research]: 70% of users struggle with [problem]

**Benefit**:
- Users can now [action] in [time/effort savings]
- Eliminates [pain point]
- Improves [metric] by [amount]

**Score**: ✅ Strong user value / ⚠️ Speculative value / ❌ No clear value
```

#### Question 3: Simplicity

"Is this the simplest solution that works?"

**Criteria:**
- Can it be simpler and still solve the problem?
- Does it add essential complexity or accidental complexity?
- Could we solve this with existing features + docs?
- Is there a "boring" solution we're overlooking?

**Analysis template:**

```markdown
### Simplicity Assessment

**Proposed Complexity**:
- [N] new API endpoints
- [N] new database tables
- [N] new configuration options
- [N] new dependencies

**Simpler Alternatives Considered**:
1. **[Alternative 1]**: [Why rejected or why this is already the simple version]
2. **[Alternative 2]**: [Why rejected]

**Justification for Complexity**:
[Explain why this complexity is essential, not accidental]

**Score**: ✅ Simplest solution / ⚠️ Could be simpler / ❌ Unnecessarily complex
```

#### Question 4: Maintainability

"Can we maintain this long-term?"

**Criteria:**
- Do we have expertise to maintain this?
- Will this require ongoing updates (e.g., new browser features, API changes)?
- Does this create tech debt?
- How does this affect test surface area?

**Analysis template:**

```markdown
### Maintainability Assessment

**Ongoing Maintenance**:
- Requires expertise in: [technologies/domains]
- Expected update frequency: [how often needs changes]
- Dependencies that might break: [external APIs, libraries]
- Test coverage required: [unit/integration/e2e]

**Team Capacity**:
- Current expertise: [✅ Have it / ⚠️ Can learn / ❌ Don't have it]
- Time to maintain: [hours/week estimated]

**Tech Debt Created**:
- [Acceptable/concerning debt description]

**Score**: ✅ Maintainable / ⚠️ Requires investment / ❌ Unsustainable
```

#### Question 5: Scope

"Does this fit our mission, or is it scope creep?"

**Criteria:**
- Does this align with North Star mission?
- Is this core to the product or peripheral?
- Would users still want our product if we removed this?
- Is this something users expect from us, or would they be surprised?

**Analysis template:**

```markdown
### Scope Assessment

**Mission Alignment**:
[North Star mission from constitution]

**This Feature**:
- Core to mission: [Yes/No - explain why]
- User expectation: [Expected/Surprising/Delightful]
- Without this feature: [Product still viable? Yes/No]

**Scope Classification**:
- ✅ **Core**: Essential to product value proposition
- ⚠️ **Complementary**: Enhances core but not essential
- ❌ **Scope Creep**: Interesting but misaligned

**Score**: [Classification from above]
```

### Phase 4: Check Anti-Patterns

**Constitution lists explicit anti-patterns.**

**For each anti-pattern, check if proposal violates it:**

```markdown
## Anti-Pattern Check

### Anti-Pattern 1: "[Quote from constitution]"

**Violation**: ✅ Yes / ❌ No

**Evidence**: [If yes, explain how proposal violates this anti-pattern]

### Anti-Pattern 2: "[Quote from constitution]"

**Violation**: ✅ Yes / ❌ No

**Evidence**: [If yes, explain how]
```

**ANY anti-pattern violation = automatic ❌**

### Phase 5: Review Good/Bad Examples

**Constitution includes examples of good and bad compliance.**

**Compare proposal to examples:**

```markdown
## Example Comparison

### Similar to Good Example: "[Quote good example from constitution]"

**Similarity**: [How proposal resembles this good example]

### Different from Bad Example: "[Quote bad example from constitution]"

**Difference**: [How proposal avoids this bad pattern]

**OR**

### Concerning Similarity to Bad Example: "[Quote bad example]"

**Similarity**: [How proposal resembles this bad pattern - red flag]
```

### Phase 6: Generate Recommendation

**Based on all analysis, provide one of three recommendations:**

#### ✅ APPROVE: Proposal Aligns

**Criteria for approval:**
- ALL 5 decision framework questions = ✅ or mostly ✅
- NO anti-pattern violations
- Aligns with most/all principles
- Resembles good examples from constitution

**Output:**

```markdown
# Constitutional Alignment: ✅ APPROVED

## Summary

This proposal aligns with project constitutional principles and passes all decision framework criteria.

## Key Alignments

- **Principle [N]**: [How it aligns]
- **Principle [M]**: [How it aligns]

## Decision Framework Results

1. Constitutional Alignment: ✅
2. User Value: ✅
3. Simplicity: ✅
4. Maintainability: ✅
5. Scope: ✅

## Recommendation

**PROCEED** with specification and implementation.

This feature fits our mission, solves real user problems, and follows our design principles. Create specification with constitutional alignment section documenting this analysis.

## Next Steps

1. Create specification (use specification template)
2. Include this alignment analysis in Constitutional Alignment section
3. Proceed to implementation planning
```

#### ⚠️ REVISE: Proposal Needs Modification

**Criteria for revision:**
- SOME questions = ⚠️ or ❌ but fixable
- Aligns with core principles but has concerning aspects
- No anti-pattern violations, but close to edge

**Output:**

```markdown
# Constitutional Alignment: ⚠️ NEEDS REVISION

## Summary

This proposal has merit but needs modification to fully align with constitutional principles.

## Concerns

### [Principle/Question that scored ⚠️ or ❌]

**Issue**: [What's wrong]

**Constitutional Reference**: "[Quote relevant principle]"

**Suggested Revision**: [How to fix this concern]

## Decision Framework Results

1. Constitutional Alignment: ⚠️
2. User Value: ✅
3. Simplicity: ❌ (needs revision)
4. Maintainability: ⚠️
5. Scope: ✅

## Recommended Changes

1. **Simplify**: [Specific simplification needed]
2. **Reduce scope**: [What to cut or phase]
3. **Add safeguards**: [How to mitigate maintainability concerns]

## Revised Approach

**Suggested**: [Describe modified version that would align]

**Key Changes**:
- [Change 1]
- [Change 2]

## Next Steps

1. Discuss revisions with team
2. Update proposal to address concerns
3. Re-run constitutional alignment check on revised proposal
```

#### ❌ REJECT: Proposal Does Not Align

**Criteria for rejection:**
- MULTIPLE questions = ❌
- Violates anti-patterns
- Conflicts with core principles
- Scope creep (doesn't fit mission)

**Output:**

```markdown
# Constitutional Alignment: ❌ REJECTED

## Summary

This proposal does not align with project constitutional principles and should not proceed.

## Conflicts

### Principle [N]: [Name]

**Conflict**: [How proposal violates this principle]

**Constitutional Quote**: "[Quote from constitution]"

**Cannot Be Resolved Because**: [Why revision won't fix this]

### Anti-Pattern Violation

**Anti-Pattern**: "[Quote anti-pattern from constitution]"

**Violation**: [How proposal violates this]

## Decision Framework Results

1. Constitutional Alignment: ❌
2. User Value: ⚠️
3. Simplicity: ❌
4. Maintainability: ⚠️
5. Scope: ❌ (scope creep)

## Why This Doesn't Fit

[Explain at high level why this proposal is fundamentally misaligned with project direction]

**Mission Misalignment**: [How it doesn't serve North Star mission]

**Precedent Risk**: [What accepting this would signal]

## Alternative Approaches

Rather than this feature, consider:

1. **[Alternative 1]**: [Aligned approach that solves similar problem]
2. **[Alternative 2]**: [Different framing that fits better]

## Next Steps

1. Document this rejection for future reference (avoid revisiting)
2. If user value is real, explore aligned alternatives
3. Update roadmap changelog to note why this was rejected
```

## Documentation

**After completing check, create permanent record:**

### If Approved

**Add to specification** when created:

```markdown
## Constitutional Alignment

**Evaluated**: [YYYY-MM-DD]
**Skill**: check-constitutional-alignment
**Result**: ✅ APPROVED

[Include full analysis from Phase 3-5]
```

### If Rejected

**Create issue for record-keeping:**

```typescript
issues_create({
  title: "[REJECTED] [Feature Name] - Constitutional Misalignment",
  description: `[Include full rejection analysis]`,
  type: "issue",
  status: "cancelled",
  priority: "low",
  labels: ["governance", "rejected-feature", "constitutional-violation"],
  project: "Governance"
})
```

**Purpose**: Prevent revisiting rejected ideas without addressing root concerns.

## Edge Cases

### Proposal Is Partially Outside Scope

**Situation**: Core feature aligns, but requested "extras" don't

**Response**:
- Recommend ⚠️ REVISE
- Approve core, suggest phasing or removing extras
- Document which parts align and which don't

### No Clear User Evidence

**Situation**: Feature seems aligned but no hard evidence of user need

**Response**:
- Flag Question 2 (User Value) as ⚠️
- Suggest: "Validate user need before specification"
- Recommend user research or hypothesis testing

### Constitution Is Ambiguous

**Situation**: Can't determine alignment because principle is vague

**Response**:
1. Note ambiguity explicitly
2. Make best judgment call
3. **Recommend**: "Run `constitution` skill to refine Principle [N]"
4. Document assumption made for this check

### Proposal Would Require Constitutional Amendment

**Situation**: Good idea but violates current principles intentionally

**Response**:
```markdown
# Constitutional Alignment: ⚠️ REQUIRES AMENDMENT

This proposal conflicts with current principles but may justify updating the constitution itself.

## Conflict
[Which principle it violates]

## Case for Amendment
[Why this feature is important enough to change principles]

## Recommendation
1. Create constitutional amendment proposal (use `constitution` skill)
2. If amendment approved, re-evaluate this feature
3. Do NOT proceed without formal amendment
```

## Collaboration with User

**This is a conversation, not a dictation.**

**If you assess ❌ REJECT but user disagrees:**
1. Review your analysis - did you miss something?
2. Check if constitution is ambiguous (might need refinement)
3. Present reasoning clearly, but defer to user's judgment
4. If user overrides, document: "Approved despite [concern] per user decision"

**If you assess ✅ APPROVE but user has concerns:**
1. Ask what concerns them
2. Re-analyze with their perspective
3. Update recommendation if their concerns are valid
4. Constitutional governance is collaborative, not dogmatic

## Success Criteria

Alignment check is complete when:

- [ ] Constitution fully read and understood
- [ ] Proposal clearly documented
- [ ] All 5 decision framework questions analyzed
- [ ] All principles checked for alignment/conflict
- [ ] All anti-patterns checked for violations
- [ ] Examples compared
- [ ] Clear recommendation provided (✅/⚠️/❌)
- [ ] Detailed reasoning documented
- [ ] Next steps specified
- [ ] Record created (in spec or as rejected issue)

## Output Format

Always provide:

1. **Top-line recommendation**: ✅ APPROVE / ⚠️ REVISE / ❌ REJECT
2. **Summary** (2-3 sentences)
3. **Detailed analysis** for each framework question
4. **Principle alignment breakdown**
5. **Anti-pattern check results**
6. **Next steps** (what to do with this information)

## Related Skills

- **constitution** - For refining ambiguous principles encountered during check
- **writing-plans** - For creating specification after approval
- **brainstorming** - For revising proposals that need modification

## Remember

You are the constitutional guardian. Be rigorous but not dogmatic. The goal is alignment with principles, not rejection of ideas. When something doesn't align, help the user understand why and suggest aligned alternatives.

The constitution exists to serve the project, not to block progress. But it must be respected - bypassing it for "just this once" destroys its value.
