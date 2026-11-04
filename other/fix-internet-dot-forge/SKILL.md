---
name: fix
description: "Use when Forge enters the bug fix loop. Routes simple issues to developers, complex issues to troubleshooter for root cause analysis."
---

<Purpose>
Phase 6 of the Forge pipeline. The fix loop triages discovered issues from QA and
security phases, routes them to the appropriate handler (simple fix or deep diagnosis),
and iterates until all blockers are resolved. Every fix worktree gets a runtime lane
record, and review/merge/rebase state must stay current in `.forge/runtime.json`.
Max 3 iterations before escalating to the client with alternatives.
</Purpose>

<Use_When>
- Automatically invoked when Phase 4 (QA) or Phase 5 (security) finds blockers
- state.json phase=6
</Use_When>

<Steps>
0. Analysis freshness check:
   - If saved analysis is stale, or repair/fix flow has no structural analysis yet, route to `forge:analyze` before continuing.
   - Fix work should not begin blind when impact radius is still unknown.

1. Load all open issues from .forge/holes/:
   a. Read each .forge/holes/{issue-id}.md
   b. Sort by severity: blocker → major → minor → cosmetic
   c. Focus ONLY on blockers (minor/cosmetic are deferred to known-issues)

2. Triage each blocker using the Fix Triage Rubric:

   Fix Triage Rubric — score each criterion (0 or 1):
   - [ ] Error message points to a specific file and line (+1) or unclear (+0)
   - [ ] Issue is isolated to one module/component (+1) or spans multiple (+0)
   - [ ] Similar issue has been fixed before in this project (+1) or novel (+0)
   - [ ] Reproduction steps are clear (+1) or intermittent/unclear (+0)

   Score 3-4: SIMPLE → fact-check → dev fix → QA re-verify
   Score 0-2: COMPLEX → troubleshooter RCA → dev fix → QA re-verify

   Layer Classification:
   - SIMPLE issues: dispatch developer (layer2_subagent, isolated worktree)
   - COMPLEX issues: dispatch troubleshooter + analyst in parallel (both layer2_subagent)
     - Analyst provides structural context: dependency graph, impact radius, related modules
       (see agents/analyst.md for full capabilities)
     - Troubleshooter does RCA: reproduce, hypothesize, verify
     - Combined output guides the fix — Analyst's impact report scopes the change,
       Troubleshooter's RCA report identifies the root cause

   a. Simple issue (triage score 3-4):
      - Fact-checker verifies the root cause is correct
      - Register or refresh the runtime lane record before dispatching work
      - Dispatch developer agent to fix in worktree:
        git worktree add .forge/worktrees/fix-{issue-id} -b forge/fix-{issue-id}
      - Developer implements fix
      - Write a handoff note before sending the fix lane into review
      - PR review (Tier 1 automated + Tier 2 Lead review)
      - Merge and cleanup worktree

   b. Complex issue (triage score 0-2: unclear cause, spans multiple modules, or reproduces intermittently):
      - Dispatch Analyst and Troubleshooter in parallel:
        - Analyst: dependency tracing + impact analysis for the affected area
        - Troubleshooter: root cause analysis via forge:troubleshoot skill
      - Troubleshooter produces RCA report in .forge/evidence/rca-{issue-id}.md
      - Analyst produces impact report scoping affected modules and callers
      - Register or refresh the runtime lane record before dispatching work
      - Dispatch developer agent with both RCA and impact reports to implement minimal fix
      - Record blocker/rebase/review notes in runtime if the fix is waiting on review, merge, or rebase
      - PR review (all 3 tiers — automated + Lead + CTO)
      - Merge and cleanup worktree

2b. **Lesson Extraction (after each COMPLEX fix)**:
    - If triage score was 0-2 (complex) and RCA was performed:
      a. Troubleshooter identifies the structural cause (not just the symptom)
      b. Lead Dev evaluates: is this a recurring pattern or one-off?
      c. If recurring → create pattern lesson in .forge/lessons/{issue-id}-lesson.md
      d. If the fix reveals a code-rules gap → note in lesson's prevention checklist
    - See `references/harness-learning.md` for lesson format

3. QA Re-verification:
   a. After each fix is merged, dispatch QA engineer to re-verify:
      - Does the specific issue reproduce? (must be NO)
      - Did the fix introduce any regressions? (run full test suite)
      - Are related features still working?
      - Does runtime still show the lane as merged/rebased/done accurately?
      - Update the linked hole status to `verified` or `closed` when confirmed
      - Run `node scripts/forge-sync-traceability.mjs` after status updates
   b. If re-verification fails:
      - Issue goes back to step 2 with additional context
      - Increment iteration counter for this issue

4. Iteration Tracking:
   - Each issue has a max of 3 fix attempts
   - Track in .forge/holes/{issue-id}.md:
     - attempt_count: N
     - attempt_history: what was tried and why it failed
   - Keep the lane handoff note in runtime aligned with the current attempt and review state

5. Max Iterations Exceeded:
   - If any blocker reaches 3 failed attempts:
     a. CEO agent compiles a report for the client:
        - What the issue is (non-technical explanation)
        - What was tried (3 attempts summary)
        - Alternatives:
          (a) Redesign the affected feature
          (b) Descope the feature to V2
          (c) Accept as known limitation with workaround
     b. Client decides which alternative to pursue
     c. If redesign → route back to Phase 2 (design) for the affected module
     d. If descope → move issue to known-issues, continue to Phase 7
     e. If accept → document workaround, continue to Phase 7

6. Gate Decision:
   - All blockers resolved (fixed or client-approved descope) → route to Phase 5 (Security) for re-review
   - Still has unresolved blockers → continue iteration
   - Update company runtime in the same step:
     - unresolved blockers:
       `node scripts/forge-lane-runtime.mjs set-company-gate --gate implementation_readiness --gate-owner lead-dev --delivery-state blocked --internal-blockers "{remaining blocker summaries}"`
     - resolved blockers:
       `node scripts/forge-lane-runtime.mjs set-company-gate --gate security_re_review --gate-owner security-reviewer --delivery-state in_progress`

7. Update state.json: phase=5, phase_id="security", phase_name="security"
   (Security must re-verify after fixes. If security passes, Security routes to Phase 7 delivery.)

8. Update session handoff:
   - unresolved blockers:
     `node scripts/forge-lane-runtime.mjs write-session-handoff --summary "{what remains blocked}" --next-goal "Continue blocker resolution" --next-owner lead-dev`
   - resolved blockers:
     `node scripts/forge-lane-runtime.mjs write-session-handoff --summary "Fix loop clear; re-running security review before delivery" --next-goal "Security re-review of fixed code" --next-owner security-reviewer`

9. Transition to Phase 5 (forge:security) — Security re-reviews after fixes.
   If security finds new issues → back to Phase 6 (fix loop).
   If security passes → Security skill advances to Phase 7 (forge:deliver).
</Steps>

<State_Changes>
- Creates: .forge/worktrees/fix-{issue-id}/ (temporary fix worktrees)
- Updates: .forge/holes/{issue-id}.md (attempt count, resolution status)
- Creates: .forge/evidence/rca-{issue-id}.md (for complex issues)
- Updates: .forge/state.json (phase=5 security re-review when all blockers resolved)
- Updates: .forge/runtime.json (implementation/security re-review gate result + next session handoff)
- Removes: fix worktrees after merge
</State_Changes>

<Tool_Usage>
- Agent tool: dispatch forge:troubleshooter (layer2_subagent) for root cause analysis on complex issues
- Agent tool: dispatch forge:analyst (layer2_subagent) for dependency tracing and impact analysis
- Agent tool: dispatch forge:developer (layer2_subagent, isolation="worktree") for fix implementation
- Agent tool: dispatch forge:fact-checker for verifying root causes before fixes
- Agent tool: dispatch forge:qa-engineer for re-verification after each fix merge
- Agent tool: dispatch forge:cto for Tier 3 reviews on complex multi-module fixes
- Bash tool: git worktree add/remove, git rebase, git tag
- CLI helper: `node scripts/forge-worktree.mjs` for worktree create/list/remove/prune
- CLI helper: `node scripts/forge-lane-runtime.mjs` for lane graph, owner, status, handoff, and company gate updates
- Read tool: load .forge/holes/*.md, .forge/evidence/rca-*.md
- Edit tool: update .forge/state.json, .forge/holes/{issue-id}.md (attempt tracking)
</Tool_Usage>

<Failure_Modes_To_Avoid>
- Attempting to fix a complex issue without root cause analysis
- Fixing symptoms instead of root causes
- Not re-verifying after each fix (assuming the fix works)
- Exceeding 3 iterations without escalating to client
- Fixing a blocker but introducing a new blocker (regression)
- Not tracking attempt history for each issue
- Skipping CTO review on complex multi-module fixes
- Sending a fix to review without a runtime handoff note
- Letting review, merge, or rebase state drift away from runtime
- Leaving orphan fix worktrees after Phase 6 completes
- Marking an issue as resolved without QA re-verification
- Resolving a hole without syncing requirement status back into traceability
- Not presenting alternatives when max iterations are exceeded
</Failure_Modes_To_Avoid>

<Auto_Chain>
When all fixes are merged and QA re-verified:
- Return to the phase that triggered the fix loop:
  - If came from QA: update state.json phase_id → "qa", invoke Skill: forge:qa (re-run full QA)
  - If came from Security: update state.json phase_id → "security", invoke Skill: forge:security (re-verify)
Do NOT stop, summarize, or ask the user. The fix loop continues until no blockers remain.
</Auto_Chain>
