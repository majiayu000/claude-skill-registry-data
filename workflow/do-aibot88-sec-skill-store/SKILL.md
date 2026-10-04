---
name: do
description: Enforce CLAUDE.md framework compliance. Re-reads rules, displays applicable rules, processes request with full compliance.
argument-hint: "[user request]"
disable-model-invocation: true
---

# Enforce Framework Compliance

## CRITICAL ENFORCEMENT PROTOCOL

**BEFORE PROCESSING ANY REQUEST:**
1. Re-read ~/.claude/CLAUDE.md completely
2. Display ALL applicable rules for the operation
3. Process the user's request with FULL compliance
4. Verify rule adherence after completion

## Boy Scout Principle
- Compliance checks must always leave the workspace cleaner: fix misfiled rules, stale configs, or missing evidence as soon as you notice them
- If you uncover sloppy prior responses or unchecked boxes, correct them before moving forward so future runs inherit a healthy baseline
- Document each cleanup in the final verification block so the improvement is provable, not implied

## MANDATORY COMPLIANCE CHECKLIST

### PRE-EXECUTION
- [ ] Display relevant rules
- [ ] Classify operation type
- [ ] Display ALL relevant rule sets
- [ ] Re-read CLAUDE.md if needed
- [ ] Assess whether the planned workflow preserves separation of concerns, keeps each actor's responsibility singular, and avoids introducing tight coupling

### DURING EXECUTION
- [ ] Before EVERY tool use: verify rule compliance
- [ ] After EVERY tool use: confirm rules followed
- [ ] Maintain rule display in responses
- [ ] Follow workflows exactly

### POST-EXECUTION
- [ ] Verify all rules were followed
- [ ] Confirm deliverables match requirements
- [ ] Check for any rule violations

## REINFORCEMENT MANTRA

**REPEAT INTERNALLY BEFORE EVERY ACTION:**
- I MUST display rules at the start of EVERY response
- I MUST classify operations and show appropriate rules
- I MUST verify technical claims with evidence
- I MUST respect agent boundaries
- I MUST NOT create random markdown files
- These rules apply to ALL interactions, ALL tool uses

## USER REQUEST PROCESSING

After enforcing compliance above, process the user's actual request:

---

$ARGUMENTS

---

## FINAL VERIFICATION

Before completing response:
1. Did I display relevant rules?
2. Did I classify the operation type?
3. Did I display all relevant rule sets?
4. Did I follow the rules throughout?
