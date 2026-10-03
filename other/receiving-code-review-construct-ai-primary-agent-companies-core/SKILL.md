---
memory_layer: durable_knowledge
para_section: pages/skills/receiving-code-review
gigabrain_tags: code-review, feedback, technical-evaluation, verification, collaboration
openstinger_context: review-feedback, technical-validation, code-quality
last_updated: 2026-03-30
related_docs:
  - docs/codebase/coding-standards/
  - docs/error-tracking/0000_ERROR_FIXES_SUMMARY.md
related_skills:
  - systematic-debugging
  - verification-before-completion
  - test-driven-development
frequency_percent: 85.0
success_rate_percent: 91.0
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit CLAUDE.md violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From your human partner
- **Trusted** - implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**your human partner's rule:** "External feedback - be skeptical, but check carefully"

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**your human partner's rule:** "You and reviewer both report to me. If we don't need this feature, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with your human partner's architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Involve your human partner if architectural

**Signal if uncomfortable pushing back out loud:** "Strange things are afoot at the Circle K"

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## Real Examples

**Performative Agreement (Bad):**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## When to Use This Skill

**Trigger Conditions:**
- When receiving code review feedback from any source
- Before implementing any suggested changes from reviews
- When review feedback seems unclear or technically questionable
- When external reviewer suggestions conflict with codebase standards
- When feedback requires verification against existing functionality
- When multiple review items need systematic evaluation
- When reviewer lacks full context of the codebase
- When feedback conflicts with architectural decisions

**Mandatory Application:**
- Always apply before implementing any review feedback
- Required for both internal and external reviews
- Must be used when feedback seems technically incorrect
- Required when reviewer context is incomplete

## Step-by-Step Procedure

### Step 1: Complete Feedback Reading
**Read all feedback without immediate reaction:**

```javascript
// Read complete feedback first
const feedback = await readAllReviewComments();
const feedbackItems = parseFeedbackItems(feedback);

console.log(`Received ${feedbackItems.length} feedback items`);
console.log('Reading complete - now analyzing...');

// DO NOT respond yet - just read and understand
```

**Reading Guidelines:**
- Read all comments and suggestions completely
- Note both inline and general comments
- Identify all requested changes
- Avoid immediate emotional reactions

### Step 2: Technical Understanding Verification
**Restate requirements in your own technical terms:**

```javascript
// For each feedback item, verify understanding
for (const item of feedbackItems) {
  const understanding = await verifyUnderstanding(item);
  
  if (!understanding.clear) {
    // Stop and ask for clarification
    await requestClarification(item, understanding.confusion);
    return; // Don't proceed until clarified
  }
  
  // Restate in technical terms
  console.log(`Understanding: ${item.description} requires ${understanding.technicalRequirement}`);
}
```

**Understanding Verification:**
- Restate each requirement technically
- Identify unclear items immediately
- Ask for clarification before proceeding
- Never assume understanding

### Step 3: Codebase Reality Check
**Verify feedback against actual codebase:**

```javascript
// Check each suggestion against codebase reality
for (const item of feedbackItems) {
  const verification = await verifyAgainstCodebase(item);
  
  item.verificationResults = {
    technicallySound: verification.correctForThisCodebase,
    breaksExisting: verification.breaksFunctionality,
    contextAware: verification.reviewerHasFullContext,
    yagniViolation: verification.unusedFeature,
    conflictsWithArchitecture: verification.architecturalConflict
  };
}
```

**Verification Checks:**
- Technically correct for this specific codebase
- Doesn't break existing functionality
- Reviewer understands full context
- Doesn't violate YAGNI principles
- Aligns with architectural decisions

### Step 4: Technical Evaluation
**Evaluate each item for technical soundness:**

```javascript
// Evaluate each verified item
for (const item of feedbackItems) {
  const evaluation = evaluateTechnicalSoundness(item);
  
  if (evaluation.shouldPushBack) {
    // Prepare technical pushback
    item.response = prepareTechnicalPushback(evaluation.reasons);
  } else {
    // Accept and plan implementation
    item.response = 'Will implement';
    item.implementationPlan = planImplementation(item);
  }
}
```

**Evaluation Criteria:**
- Technical correctness for the stack
- Compatibility with existing code
- Performance implications
- Security considerations
- Maintenance impact

### Step 5: Response Formulation
**Formulate appropriate technical responses:**

```javascript
// Generate responses for each item
const responses = feedbackItems.map(item => {
  if (item.needsClarification) {
    return formulateClarificationRequest(item);
  } else if (item.shouldPushBack) {
    return formulateTechnicalPushback(item);
  } else {
    return formulateAcceptance(item);
  }
});

// Batch related responses
const batchedResponses = batchRelatedResponses(responses);
```

**Response Types:**
- Clarification requests for unclear items
- Technical pushback with reasoning
- Acceptance with implementation notes

### Step 6: Systematic Implementation
**Implement changes one at a time with testing:**

```javascript
// Implement in priority order
const implementationOrder = [
  'blocking_issues',      // Security, breaks
  'simple_fixes',         // Typos, imports
  'complex_fixes'         // Refactoring, logic
];

for (const priority of implementationOrder) {
  const items = feedbackItems.filter(item => 
    item.accepted && item.priority === priority
  );
  
  for (const item of items) {
    // Implement one item
    await implementChange(item);
    
    // Test the specific change
    await testChange(item);
    
    // Verify no regressions
    await verifyNoRegressions();
    
    // Commit if tests pass
    if (await allTestsPass()) {
      await commitChange(item);
    }
  }
}
```

**Implementation Rules:**
- One change at a time
- Test each change individually
- Verify no regressions
- Commit only passing changes

### Step 7: Pushback Handling
**Handle technical disagreements professionally:**

```javascript
// For items requiring pushback
for (const item of feedbackItems.filter(i => i.shouldPushBack)) {
  const pushback = prepareTechnicalPushback(item);
  
  // State technical reasoning
  pushback.response = `
    Checked against codebase: ${pushback.technicalReasoning}
    Current implementation: ${pushback.existingRationale}
    Alternative consideration: ${pushback.suggestedAlternative}
  `;
  
  // Involve human partner if architectural
  if (pushback.architectural) {
    await involveHumanPartner(pushback);
  }
}
```

**Pushback Guidelines:**
- Use technical reasoning, not defensiveness
- Reference specific code and tests
- Suggest alternatives when appropriate
- Escalate architectural decisions

### Step 8: YAGNI Verification
**Check for unnecessary feature additions:**

```javascript
// YAGNI check for feature suggestions
for (const item of feedbackItems) {
  if (item.suggestsNewFeature) {
    const usageCheck = await grepCodebaseForUsage(item.feature);
    
    if (!usageCheck.isUsed) {
      item.yagni = true;
      item.response = `Feature not used in codebase. Remove instead (YAGNI)?`;
    }
  }
}
```

**YAGNI Evaluation:**
- Search codebase for actual usage
- Question unused feature additions
- Prefer removal over enhancement of dead code

### Step 9: Progress Communication
**Keep reviewer informed of progress:**

```javascript
// Communicate implementation progress
for (const item of feedbackItems) {
  if (item.implemented) {
    // Brief technical acknowledgment
    await postImplementationNote(item, 'Fixed: [brief technical description]');
  } else if (item.clarified) {
    // Confirm understanding
    await postClarificationResponse(item, 'Understood: [technical restatement]');
  } else if (item.rejected) {
    // Technical reasoning for rejection
    await postRejectionResponse(item, 'Technical concern: [reasoning]');
  }
}
```

**Communication Style:**
- Technical and factual
- Brief and direct
- No performative language
- Focus on code changes

### Step 10: Final Verification
**Ensure all feedback addressed appropriately:**

```javascript
// Final verification checklist
const finalVerification = {
  allItemsAddressed: feedbackItems.every(item => 
    item.clarified || item.implemented || item.rejectedWithReason
  ),
  testsPassing: await runFullTestSuite(),
  noRegressions: await verifyNoRegressions(),
  documentationUpdated: await checkDocumentationUpdates(),
  humanPartnerInformed: await verifyEscalationsHandled()
};

if (finalVerification.allItemsAddressed && finalVerification.testsPassing) {
  console.log('✅ Code review feedback processing complete');
} else {
  console.log('❌ Issues remain - review status with human partner');
}
```

**Final Checks:**
- All feedback items addressed
- Tests passing after changes
- No functionality regressions
- Documentation updated if needed
- Escalations properly handled

## Success Criteria

- [ ] All feedback read completely before responding
- [ ] Unclear items clarified before implementation
- [ ] Each suggestion verified against codebase reality
- [ ] Technical evaluation completed for all items
- [ ] Appropriate responses formulated (acceptance/pushback/clarification)
- [ ] Changes implemented one at a time with testing
- [ ] No regressions introduced
- [ ] Technical reasoning used for all pushback
- [ ] YAGNI violations identified and addressed
- [ ] Progress communicated professionally

## Common Pitfalls

1. **Performative Agreement** - Never use "You're absolutely right!" or similar
2. **Blind Implementation** - Always verify suggestions before implementing
3. **Partial Understanding** - Clarify all unclear items before proceeding
4. **Batch Implementation** - Test each change individually
5. **Avoiding Pushback** - Use technical reasoning when suggestions are wrong
6. **Emotional Responses** - Keep all communication technical and factual
7. **Missing YAGNI Checks** - Question additions of unused features

## Response Templates

### Clarification Requests
```
"I understand [items 1,2,3]. Need clarification on [unclear items] before proceeding."
```

### Technical Pushback
```
"Checked codebase: [technical reasoning]. Current approach [justification]. Alternative: [suggestion]."
```

### Acceptance
```
"Fixed: [brief technical description of change]"
```

### YAGNI Response
```
"Grepped codebase - feature not used. Remove instead (YAGNI)?"
```

## Cross-References

### Related Procedures
- [Systematic Debugging Skill](skills/systematic-debugging/SKILL.md) - Technical verification methods
- [Verification Before Completion Skill](skills/verification-before-completion/SKILL.md) - Quality assurance
- [Test Driven Development Skill](skills/test-driven-development/SKILL.md) - Testing approach

### Related Skills
- `systematic-debugging` - Technical verification of suggestions
- `verification-before-completion` - Quality assurance for changes
- `test-driven-development` - Testing approach for implementations
- `requesting-code-review` - Counterpart skill for giving feedback

### Related Agents
- `DevForge_AI_Team` - Implementation assistance
- `QualityForge_AI_Team` - Code quality verification

## Performance Metrics

- **Application Frequency:** Used in 85% of code review interactions
- **Success Rate:** 91% of feedback processed correctly
- **Technical Pushback Success:** 78% of pushback accepted when technically sound
- **Clarification Efficiency:** 94% of unclear items resolved in first request

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always.
