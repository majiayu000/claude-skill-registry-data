---
name: develop
description: "Use when Forge starts implementation after design approval, or when the user asks for parallel module development with worktrees, scoped tasks, PR review, and living-standard enforcement. Trigger on requests to split implementation, dispatch developers, or enforce consistent multi-agent coding."
---

<Purpose>
Phase 3 of the Forge pipeline. The Lead Developer splits the approved design into
independent tasks. Each developer/publisher works in an isolated git worktree —
physical file-system separation, not just branches. All code goes through a 3-tier
PR-based review pipeline with code-rules enforcement. The first merged PR becomes
the "living standard" that all subsequent PRs must match. Lane orchestration is
runtime-backed: `.forge/runtime.json` stores the lane graph, owners, statuses,
active worktrees, handoff notes, and review/merge/rebase signals. Common Forge
paths should update that runtime automatically through the standard helpers, but
the process remains human-led and review-gated; it is not an autonomous merge bot.
</Purpose>

<Use_When>
- Automatically invoked after Phase 2 (design) completes
- state.json phase=3
</Use_When>

<Core_Rules>
1. Every developer works in their own git worktree (physical isolation)
2. No Evidence, No Code — developers must verify via fact-checker before writing
3. Code that violates code-rules.md = REJECTED
4. Code inconsistent with already-merged code = REJECTED
5. First merged PR becomes the "living standard"
6. Developers load ONLY: spec subset + relevant contracts + code-rules.md (minimal context)
7. Every created worktree/task must have a runtime lane record before dispatch
8. Handoff notes are required before review or reassignment
9. Explicit review, merge, and rebase states must be reflected in runtime
10. Zero merge debt before new scope — approved or merge-ready lanes must be landed before starting more implementation work unless a blocker is explicitly recorded
</Core_Rules>

<Hybrid_Dispatch>
Forge uses a 3-layer dispatch model. AgentRecommendation from
scripts/lib/forge-state.mjs classifies agents automatically into the
appropriate layer. Choose the lightest layer that meets the need.

Layer 0 — Prompt Switch (in-conversation):
  Lead-dev operates in the main conversation, not as a separate subagent.
  Claude switches to the lead-dev role by loading agents/lead-dev.md context.
  Use for: task splitting, lane-graph management, code review, merge decisions.
  No isolation needed — the lead works on the main branch.

Layer 1 — Team (iterative collaboration):
  When multiple agents need multi-turn back-and-forth (e.g., Developer ↔ Lead
  review cycles), use TeamCreate + SendMessage.
  Use for: review rounds, design discussions, cross-lane coordination.
  Context is preserved across rounds — no re-dispatch needed.

Layer 2 — Isolated Subagent (parallel execution):
  Developers and fact-checkers dispatch with Agent tool using
  isolation: "worktree" or subagent_type: "forge:developer" / "forge:fact-checker".
  Use for: module implementation, technical verification.
  Each agent gets its own worktree and minimal context.
</Hybrid_Dispatch>

<Progressive_Disclosure>
- Load `references/review-pipeline.md` when you need the full review tiers or worktree rules.
- Load `references/lane-runtime.md` when you need the standard runtime helper commands and lane graph rules.
</Progressive_Disclosure>

<Steps>
-1. **Staleness Check (constraint propagation)**
    - Read state.json.staleness — if architecture, contracts, code_rules, components, or tokens are stale, BLOCK.
    - Read analysis metadata — if saved analysis is stale or missing for an existing-code path, route to `forge:analyze` first.
    - Route to CTO/Designer to update stale artifacts before implementation proceeds.
    - Only continue when all staleness entries relevant to this phase are cleared.

0. **Handoff Interview — Implementation Intake (BEFORE task splitting)**
   a. Lead Developer reads ALL design artifacts:
      - .forge/design/architecture.md
      - .forge/contracts/*.ts
      - .forge/code-rules.md
      - .forge/design/components.md
      - .forge/design/tokens.json
      - CTO's pre-generated questions from handoff brief

   b. Lead generates implementation questions:
      - Ambiguous module boundaries: "Does module X own this shared state, or module Y?"
      - Missing contracts: "The spec mentions feature Z but no contract exists for it"
      - Dependency ordering: "Can module A start before module B's types are available?"
      - Testing gaps: "What's the test strategy for [integration point]?"
      - Performance budgets: "Is there a response time target for [critical path]?"
      Format: "Q: ... | Domain: architecture/contract/testing | Blocker: yes/no | Default assumption: ..."

   c. CEO triages questions:
      - CTO answers architecture/contract questions
      - Designer answers UX/component questions
      - PM answers business logic questions
      - CLIENT → only if truly customer-owned (rare at this stage)

   d. Lead writes understanding statement:
      "I will split the implementation into [N] modules: [list with boundaries].
       Critical path: [ordering]. Key risk: [risk]. Test strategy: [approach]."

   e. CTO reviews Lead's understanding statement against architecture intent.
      Mismatches → correct immediately. Accurate → sign off.

   f. Understanding confirmed → task splitting begins.

1. Lead Developer reads:
   - .forge/design/architecture.md
   - .forge/contracts/*.ts
   - .forge/code-rules.md

2. Dispatch Analyst (forge:analyst) for impact analysis:
   - Analyst uses codebase-memory-mcp (search_graph, trace_call_path, get_architecture)
     to map existing module boundaries and dependencies
   - Output: impact report showing which existing code will be affected by each planned module
   - Lead uses this to make informed lane splitting decisions
   - Skip if project is greenfield (no existing codebase to analyze)

3. Lead runs **auto-decompose** to generate the lane graph:
   ```
   node scripts/forge-lane-runtime.mjs auto-decompose --description "<task summary from spec/architecture>"
   ```
   This automatically:
   - Analyzes the task (type, areas, complexity)
   - Identifies parallelizable components with file ownership (scope)
   - Creates lanes in runtime.json with dependencies and model_hint
   - Calculates execution order (batches)

   Lead reviews the output and adjusts if needed:
   - Override lanes: `node scripts/forge-lane-runtime.mjs init-lane --lane {id} --title "{title}" --depends-on {deps}`
   - For manual splitting (complex cases): skip auto-decompose and define lanes manually as before

4. For each lane, Lead creates a task definition:
   `.forge/tasks/{lane-id}.md` containing:
   - Scope: file patterns from lane.scope (auto-populated by decomposer)
   - Contracts: relevant .forge/contracts/ files for this lane
   - Tests: what must pass before PR
   - Dependencies: upstream lanes (auto-populated)

   Update lane with task file:
   ```
   node scripts/forge-lane-runtime.mjs init-lane --lane {id} --task-file .forge/tasks/{id}.md
   ```

5. Lead dispatches agents per **execution batch**:
   Auto-decompose provides `executionOrder` — batches of lanes that can run in parallel.

   **For each batch**, dispatch all lanes simultaneously:
   ```
   Agent(
     subagent_type="forge:developer",  // or "forge:publisher" for UI lanes
     isolation="worktree",
     run_in_background=true,
     prompt="Implement lane {id}: {title}. Follow .forge/code-rules.md and .forge/contracts/."
   )
   ```
   The subagent-start hook automatically injects lane-scoped context:
   - Lane scope (file patterns to work on)
   - Lane dependencies (what this depends on)
   - Model hint (sonnet for implementation, opus for review)
   - Task file content (up to 2000 chars)

   **Wait for each batch to complete before starting the next batch.**
   If any lane in the batch reaches `review_state=approved`, `merge_state=ready`, or `merge_state=queued`,
   stop opening more implementation scope and land that lane first. Merge debt is a control-tower blocker,
   not background work for later.
   Batches with dependencies must run sequentially; lanes within a batch run in parallel.

   Lane owner assigned via:
   ```
   node scripts/forge-lane-runtime.mjs assign-owner --lane {module} --owner {agent}
   ```

6. Lead monitors completion:
   ```
   node scripts/forge-lane-runtime.mjs summarize-lanes --json
   ```
   - When all lanes in a batch are merged/done → start next batch
   - If a lane is blocked for 3+ iterations → escalate to CEO
   - When ALL lanes are merged → transition to Phase 4 (QA)

   **Context budget** (see `references/context-budget.md`):
   - T0 (mandatory): tasks/{module}.md, contracts/{relevant}.ts, code-rules.md
   - T1 (relevant):  living standard reference (patterns from first merged PR)
   - T2 (on-demand): architecture.md (module boundaries section only)
   - EXCLUDED: full spec, other modules' tasks, design docs, other worktrees

7. Each developer implements their module:
   a. Read assigned task definition (.forge/tasks/{module}.md)
   b. Read relevant contracts (.forge/contracts/)
   c. Read code-rules.md
   d. Fact-check any uncertain technical claims before coding
   e. Update lane status to `in_progress`
   f. Implement the module
   g. Run tests locally in the worktree
   h. Write a handoff note before review:
      node scripts/forge-lane-runtime.mjs write-handoff --lane {module} --note "{verification summary}"
   i. Update lane status to `in_review`
   j. If review requests changes, or the lane needs merge/rebase follow-up, reflect that state in runtime immediately instead of leaving it implicit in chat.
   k. Create PR when all local tests pass

8. PR Review Pipeline (3 tiers):

   Teams-based review (recommended for multi-turn feedback):
   - Create a review team: TeamCreate(team_name="forge-review-{module}")
   - Add Developer and Lead as team members
   - Tier 2 review via SendMessage:
     Lead -> Developer: "Please align to fetchUser()" (specific correction)
     Developer -> Lead: "Fixed, please re-review"
     Lead -> Developer: "LGTM" -> merge
   - Benefits: context preserved across review rounds, no re-dispatch needed
   - Handoff notes still required in forge-lane-runtime.mjs (audit trail)

   Sequential review (fallback — ALL tiers must approve):

   Tier 1 — Automated Checks (instant):
   - Lint passes
   - TypeScript typecheck passes
   - All tests pass
   - No secrets or credentials in diff
   -> Fail = instant reject, developer fixes and resubmits

   Tier 2 — Lead Developer Review:
   - code-rules.md compliance (naming, patterns, structure)
   - Consistency with already-merged code
   - Contract implementation correctness
   - No scope creep (only touches files in task definition)
   -> Violate = reject with specific instructions:
     "Developer B uses fetchUser() but you used getUser(). Please align to fetchUser()"

   Tier 3 — CTO Review (architecture):
   - Module fits the overall architecture
   - No hidden coupling or circular dependencies
   - Performance and scalability concerns
   - Only invoked if Lead flags architectural concerns
   -> Reject = CTO provides redesign guidance

   All tiers approve -> mark the lane review-approved / merge-ready in runtime, then merge to main:
   ```
   node scripts/forge-lane-runtime.mjs mark-review-state --lane {module} --state approved --note "Lead/CTO review approved"
   node scripts/forge-lane-runtime.mjs mark-merge-state --lane {module} --state ready --note "Ready to merge after review approval"
   ```
   Leaving approved lanes unmerged creates merge debt and weakens the living standard for later lanes.

9. After each merge, update the lane record, then rebase all other active worktrees:
   node scripts/forge-lane-runtime.mjs update-lane-status --lane {module} --status merged --note "Merged to main"
   node scripts/forge-lane-runtime.mjs update-lane-status --lane {module} --status done --note "Worktree cleaned up"
   cd .forge/worktrees/{other-module} && git rebase main
   - Do not accumulate multiple approved lanes for a later mega-merge. The moment a lane is approved or merge-ready,
     land it, rebase the remaining worktrees, and only then continue the next batch.
   - If rebase conflicts: developer resolves in their worktree
   - If conflict is architectural: escalate to Lead
   - If a lane is waiting on rebase, mark that in runtime so status/continue can surface it as an active control-tower signal.

10. Repeat steps 7-9 until all PRs are merged
    - Use `node scripts/forge-lane-runtime.mjs summarize-lanes` to review the lane graph and blocked lanes
    - Update the session handoff so the next session knows what remains and who owns the first move

11. Cleanup worktrees:
    node scripts/forge-worktree.mjs remove --lane {module}
    (for each completed module)

12. Update state.json: phase=4, phase_name="qa"
    - Update company runtime for QA:
      `node scripts/forge-lane-runtime.mjs set-company-gate --gate qa --gate-owner qa --delivery-state in_progress`
    - Update session handoff toward QA:
      `node scripts/forge-lane-runtime.mjs write-session-handoff --summary "{what remains to verify}" --next-goal "Run QA and classify blockers" --next-owner qa`

13. Create git tag: forge/v1-dev

14. Transition to Phase 4 (forge:qa)
</Steps>

<Worktree_Management>
Create worktree:
  node scripts/forge-worktree.mjs create --lane {module} --branch forge/{module}

List active worktrees:
  node scripts/forge-worktree.mjs list

Rebase worktree after merge:
  cd .forge/worktrees/{module} && git rebase main

Remove worktree after merge:
  node scripts/forge-worktree.mjs remove --lane {module}

Prune stale worktrees:
  node scripts/forge-worktree.mjs prune
</Worktree_Management>

<Lane_Runtime>
Lane graph summary:
  node scripts/forge-lane-runtime.mjs summarize-lanes

Assign lane owner:
  node scripts/forge-lane-runtime.mjs assign-owner --lane {module} --owner {agent}

Update lane status:
  node scripts/forge-lane-runtime.mjs update-lane-status --lane {module} --status in_progress --note "{status note}"

Write handoff note:
  node scripts/forge-lane-runtime.mjs write-handoff --lane {module} --note "{handoff summary}"

Review and merge states:
  - Keep `in_review`, `blocked`, `merged`, and `done` current in runtime as the lane moves through review and integration.
  - Use runtime notes to capture rebase blockers, reviewer requests, and merge completion.
</Lane_Runtime>

<PR_Review_Checklist>
Tier 1 — Automated:
  [ ] Lint: no warnings, no errors
  [ ] TypeScript: tsc --noEmit passes
  [ ] Tests: all test suites pass
  [ ] Secrets: no API keys, tokens, or credentials in diff
  [ ] Build: project builds successfully

Tier 2 — Lead Developer:
  [ ] Naming conventions match code-rules.md
  [ ] File structure matches code-rules.md
  [ ] Import patterns match code-rules.md
  [ ] Error handling matches code-rules.md
  [ ] Consistent with already-merged PRs (the living standard)
  [ ] Only touches files within assigned task scope
  [ ] Implements all required interface contracts
  [ ] No TODO/FIXME/HACK comments left unresolved

Tier 3 — CTO (when flagged):
  [ ] Module boundaries respected
  [ ] No circular dependencies introduced
  [ ] No hidden coupling between modules
  [ ] Performance implications acceptable
  [ ] Scalability concerns addressed
</PR_Review_Checklist>

<Code_Consistency_Rule>
The FIRST merged PR sets the living standard for the entire project.

All subsequent PRs must match:
- Naming: if PR #1 uses fetchUser(), everyone uses fetchUser(), not getUser()
- Patterns: if PR #1 uses try/catch with custom errors, everyone follows
- Structure: if PR #1 puts hooks in /hooks, everyone puts hooks in /hooks
- Imports: if PR #1 uses absolute imports, everyone uses absolute imports
- Types: if PR #1 exports interfaces from /types, everyone does the same

When inconsistency is found, Lead rejects with explicit correction:
  "The already-merged code uses {pattern}. Please align to this standard:
   - Before: {developer's code}
   - After: {corrected code}"
</Code_Consistency_Rule>

<State_Changes>
- Creates: .forge/runtime.json lane records for each active lane
- Creates: .forge/worktrees/{module}/ (git worktrees, one per task)
- Creates: .forge/tasks/{module}.md (task definitions)
- Updates: state.json (phase=4, phase_name="qa")
- Updates: .forge/runtime.json (qa gate + QA session handoff)
- Creates: git tag forge/v1-dev
- Removes: all worktrees after completion
</State_Changes>

<Tool_Usage>
- Layer 0: Load agents/lead-dev.md context for task splitting, review, merge decisions
- Layer 1: TeamCreate + SendMessage for iterative Developer <-> Lead review cycles
- Layer 2: Agent tool with subagent_type="forge:developer", isolation="worktree" (parallel, one per module)
- Layer 2: Agent tool with subagent_type="forge:publisher", isolation="worktree" (parallel, for UI modules)
- Layer 2: Agent tool with subagent_type="forge:analyst" for codebase impact analysis
- Layer 2: Agent tool with subagent_type="forge:fact-checker" for technical verification
- Agent tool: dispatch forge:cto for Tier 3 reviews
- Bash tool: git rebase, git tag
- CLI helper: `node scripts/forge-worktree.mjs` for worktree create/list/remove/prune (manual worktree path)
- CLI helper: `node scripts/forge-lane-runtime.mjs` for lane graph, owner, status, and handoff updates
- Write tool: create `.forge/tasks/{module}.md` from `templates/task.md`
- Read tool: load contracts, code-rules.md, architecture
- Edit tool: update `.forge/state.json` and `.forge/runtime.json`
</Tool_Usage>

<Failure_Modes_To_Avoid>
- Starting task splitting before Handoff Interview is complete
- Lead not writing understanding statement before splitting work
- CTO rubber-stamping Lead's understanding without reviewing it
- Developers modifying files outside their worktree scope
- Skipping any tier of code review
- Merging without all 3 tiers approving
- Failing to register a lane in `.forge/runtime.json` before dispatch
- Leaving lane status stale after ownership, review, or merge changes
- Sending work to review without a handoff note in runtime
- Reassigning a lane without a handoff note in runtime
- Not rebasing other worktrees after a merge
- Leaving orphan worktrees after Phase 3 completes
- Developers loading full project context instead of minimal subset
- Not enforcing code-rules.md on every PR
- Allowing inconsistent patterns between merged PRs
- Letting merge/rebase state drift out of sync with runtime
- Treating helper-backed runtime updates as optional instead of mandatory on the common path
- Starting Phase 4 before all worktrees are cleaned up
- Not creating the forge/v1-dev tag before transition
</Failure_Modes_To_Avoid>

<Auto_Chain>
When development completes (all lanes merged, worktrees cleaned, forge/v1-dev tag created):
1. Update state.json: phase_id → "qa"
2. IMMEDIATELY invoke Skill: forge:qa
Do NOT stop, summarize, or ask the user. QA Engineer will test automatically.
</Auto_Chain>
