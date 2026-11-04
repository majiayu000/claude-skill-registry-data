---
name: troubleshoot
description: "Use when Forge needs deep bug diagnosis instead of a quick patch. Trigger on intermittent bugs, unclear root cause, multi-module breakage, repeated failed fixes, or requests like \"analyze this\", \"root cause\", \"why is this failing?\", and \"investigate this regression\". This skill must be used before broad changes on complex failures."
---

<Purpose>
Standalone diagnostic skill invoked by the fix skill (Phase 6) when an issue is
too complex for a simple fix. The Troubleshooter agent performs evidence-based
root cause analysis using a structured protocol: reproduce, hypothesize, gather
evidence, verify, identify root cause, propose minimal fix, and assess impact.
No guessing — only evidence-backed conclusions.
</Purpose>

<Use_When>
- Invoked by forge:fix skill when an issue is classified as complex
- KO: "분석해줘", "원인 찾아줘"  JA: "分析して", "原因を調べて"  ZH: "分析一下", "查找原因"
- Bug spans multiple modules or has unclear cause
- Bug reproduces intermittently
- Previous fix attempt failed (regression or incomplete fix)
</Use_When>

<Progressive_Disclosure>
- Load `references/rca-checklist.md` for the compact RCA checklist and must-have outputs.
</Progressive_Disclosure>

<Steps>
1. Dispatch troubleshooter agent with context:
   - .forge/holes/{issue-id}.md (issue details)
   - .forge/design/architecture.md (system overview)
   - .forge/contracts/*.ts (interface boundaries)
   - Previous attempt history (if any)

2. REPRODUCE — Confirm the bug exists:
   a. Follow the reproduction steps from the issue report
   b. If steps are incomplete, determine minimal reproduction path
   c. Document exact reproduction: inputs, state, sequence, output
   d. If cannot reproduce → document conditions tried, flag as intermittent

3. HYPOTHESIZE — Generate competing hypotheses:
   a. Formulate at least 2 competing hypotheses for root cause
   b. For each hypothesis:
      - Describe the proposed cause
      - Predict what evidence would confirm it
      - Predict what evidence would refute it
   c. Rank hypotheses by likelihood based on available evidence

4. EVIDENCE — Gather evidence for each hypothesis:
   a. For cross-module issues, dispatch Analyst first for dependency mapping —
      Analyst pre-computes call paths, dependency chains, and module boundaries
      so Troubleshooter can focus on runtime behavior rather than static structure
   b. Trace the execution path through affected code
   c. Check interface contract boundaries (is data crossing correctly?)
   d. Check state transitions (is state mutating unexpectedly?)
   e. Check timing/ordering (race conditions, async issues?)
   f. Check error handling paths (are errors swallowed silently?)
   g. Integrate Analyst's structural context with runtime evidence
   h. Record evidence for and against each hypothesis

5. VERIFY — Test the leading hypothesis:
   a. Design a test that isolates the suspected root cause
   b. Run the test to confirm or refute
   c. If refuted → move to next hypothesis, repeat from step 4
   d. If confirmed → proceed to root cause documentation

6. ROOT CAUSE — Document the confirmed root cause:
   a. What: the specific code/logic/state that causes the bug
   b. Why: why this code exists and why it's wrong
   c. Where: exact file(s) and line(s) affected
   d. When: under what conditions the bug manifests
   e. Impact: what other parts of the system are affected

7. MINIMAL FIX — Propose the smallest correct fix:
   a. Define the minimal code change that addresses root cause
   b. Explain why this fix is correct (not just suppressing symptoms)
   c. Identify what should NOT be changed (scope boundaries)
   d. Specify tests that must pass after the fix

8. IMPACT ANALYSIS — Assess ripple effects:
   a. Which modules does the fix touch?
   b. Which interface contracts are affected?
   c. Which existing tests need updating?
   d. What new tests are needed?
   e. Risk assessment: low/medium/high for regression potential

9. Write RCA report to .forge/evidence/rca-{issue-id}.md:
   - Summary (one paragraph)
   - Reproduction steps (confirmed)
   - Hypotheses considered (with evidence for/against each)
   - Confirmed root cause
   - Proposed fix (with code diff if applicable)
   - Impact analysis
   - Recommended review level (Lead only vs Lead + CTO)

10. Return control to forge:fix skill with RCA report
</Steps>

<State_Changes>
- Creates: .forge/evidence/rca-{issue-id}.md (root cause analysis report)
- Updates: .forge/holes/{issue-id}.md (adds diagnosis details)
</State_Changes>

<Failure_Modes_To_Avoid>
- Jumping to a fix without confirming the root cause
- Generating only one hypothesis (confirmation bias)
- Treating correlation as causation without verification test
- Proposing a large refactor when a minimal fix suffices
- Not documenting rejected hypotheses (they inform future debugging)
- Fixing symptoms instead of root cause
- Not assessing impact on other modules before proposing fix
- Skipping reproduction step and working from assumptions
- Not specifying which tests must pass after the fix
- Producing an RCA report without actionable fix recommendation
</Failure_Modes_To_Avoid>

<Auto_Chain>
When troubleshooting completes (root cause identified, RCA report written):
1. Update state.json: phase_id → "fix"
2. IMMEDIATELY invoke Skill: forge:fix
Do NOT stop, summarize, or ask the user. The repair pipeline must continue to the fix phase.
</Auto_Chain>
