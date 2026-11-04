---
name: intake
description: "Use when Forge receives a new project request. CEO evaluates feasibility, scope, and information completeness before starting discovery."
---

<Purpose>
Phase 0 of the Forge pipeline. The CEO evaluates the client's request to decide
if it's something we can build, if the scope is reasonable, and if we have enough
critical information to begin the discovery process. The CEO acts as the internal
operator for the company, not as a messenger waiting for customer approval at every step.
</Purpose>

<Use_When>
- Automatically invoked by forge:ignite skill at Phase 0
- Client submits a new project request
</Use_When>

<Fast_Path_Check>
Before full internal deliberation, CEO does a quick scope assessment:

**If ALL of these are true**:
- Task is clearly bounded (user specified what to build/fix)
- No multi-system integration needed
- No security/compliance concerns
- User wants speed ("quick", "express", "simple")

**Then**: Skip internal deliberation (CEO+CTO+PM meeting). Instead:
1. CEO acknowledges the request
2. Initialize .forge/ with mode appropriate to request (build/repair/express)
3. Set tier to "medium"
4. Route directly to next phase (express → forge:express, repair → troubleshooter)

**Otherwise**: Proceed with full internal deliberation below.
</Fast_Path_Check>

<Express_Interview>
When express fast-path is active, collapse the PM interview:
- Instead of 5 rounds of questions, do 1-2 rounds max
- Round 1: "What are you building or fixing? Any specific constraints?"
- Round 2 (if needed): "Anything else before we start?"
- Then generate minimal spec and proceed
</Express_Interview>

<Steps>
1. Read the client's request

2. **Fast-path gate**: Apply <Fast_Path_Check> — if all conditions met, skip to step 5 with express routing

3. Dispatch CEO agent to evaluate (full deliberation):
   a. Technical feasibility — Can this be built with available tools/frameworks?
   b. Scope assessment — Is this one project or should it be split into V1/V2?
   c. Information completeness — Do we have enough critical information to start safe discovery?

4. CEO Decision:
   - GO → Initialize .forge/ directory, set state.json phase=1, hand off to PM
   - HOLD → CEO asks the client only for missing business-critical information
   - NO-GO → CEO explains why and suggests alternatives
   Note: For REPAIR mode, after CEO evaluation, dispatch the Troubleshooter for diagnosis (aligned with ignite/SKILL.md repair routing).

5. Initialize project state:
   a. Create .forge/ directory structure:
      .forge/state.json, .forge/runtime.json, .forge/design/, .forge/contracts/, .forge/evidence/,
      .forge/holes/, .forge/tasks/, .forge/worktrees/,
      .forge/knowledge/, .forge/delivery-report/
   b. Copy templates/state.json → .forge/state.json
   c. Initialize `.forge/runtime.json` for helper-backed company coordination:
      - lanes / lane graph
      - active_worktrees
      - next_lane
      - internal gate metadata
      - blocker / readiness metadata
      - helper/runtime metadata
   d. Fill in project name, client name, created_at
   e. Set phase=1, phase_id="discovery", phase_name="discovery", status="active"

6. Transition to Phase 1 (forge:discovery)
</Steps>

<State_Changes>
- Creates: .forge/ directory with all subdirectories
- Creates: .forge/state.json (from template)
- Creates: .forge/runtime.json (lane/runtime scaffold)
- Sets: phase=1 on GO decision
</State_Changes>

<Tool_Usage>
- Agent tool: dispatch forge:ceo agent for evaluation
- Write tool: create .forge/ files
- Bash tool: mkdir for directory structure
- Read tool: load templates
</Tool_Usage>

<Failure_Modes_To_Avoid>
- Starting Phase 1 without CEO approval
- Skipping the feasibility check
- Proceeding with a request that's clearly out of scope
- Asking the client to manage internal phase transitions
- Not creating the full .forge/ directory structure
</Failure_Modes_To_Avoid>

<Auto_Chain>
When intake completes (CEO approves and .forge/ is initialized):
- BUILD mode: update state.json phase_id to "discovery", then IMMEDIATELY invoke Skill: forge:discovery
- REPAIR mode: update state.json phase_id to "reproduce", then IMMEDIATELY invoke Skill: forge:troubleshoot
- EXPRESS mode: update state.json phase_id to "plan", then IMMEDIATELY invoke Skill: forge:express
Do NOT stop, summarize, or ask the user. The pipeline must continue autonomously.
</Auto_Chain>
