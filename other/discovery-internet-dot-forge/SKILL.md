---
name: discovery
description: "Use when Forge begins requirements gathering. PM interviews the client one question at a time until all ambiguity is eliminated and a complete spec is produced."
---

<Purpose>
Phase 1 of the Forge pipeline. The PM conducts a structured interview with the client,
translating their idea into a complete, unambiguous spec. The client does NOT need to know
programming — the PM speaks their language and translates to technical requirements.
In Autonomous Company Mode, the PM minimizes customer burden: ask only what is needed to
avoid building the wrong thing, and route the rest internally.
</Purpose>

<Use_When>
- Automatically invoked after Phase 0 (intake) approval
- state.json phase=1
</Use_When>

<Core_Rule>
NO CRITICAL AMBIGUITY, NO START.
This Phase does NOT end until the team can proceed safely.
If the client gives a vague answer on a business-critical point, ask follow-up.
If answers contradict, point it out and resolve.
Do not burden the client with questions the company can answer internally through research,
design review, prototyping, or QA.
</Core_Rule>

<Progressive_Disclosure>
- Load `references/research-handoff.md` when PM needs external comparisons, reference products, or decision support grounded in outside evidence.
</Progressive_Disclosure>

<Steps>
1. Dispatch PM agent in the main session (not as subagent — PM talks directly to client)

2. PM conducts interview following this flow:
   - PM owns the conversation and spec at all times
   - PM asks the customer only what is necessary to set direction, define must-haves, and avoid product-level mistakes
   - Dispatch Researcher only when the answer depends on outside evidence:
     - the client asks for reference apps, competitor examples, or "what do similar products use?"
     - the PM needs grounded options for login, payments, chat, maps, search, analytics, CMS, or vendors
     - pricing, licensing, regional availability, compliance, or platform support affects the requirement
     - a vague preference needs real-world examples before the PM can ask the next question
   - PM sends Researcher a bounded question, project constraints, and the decision it should unblock
   - Researcher returns a concise brief with options, recommendation, evidence, and open unknowns
   - PM translates that brief into client-language choices and updates the spec

   Round 1 — Big Picture:
   - "What does this app/service do? Describe it in one sentence."
   - "Who will primarily use it?"
   - "What's the core value? Why would someone use this?"
   - "Any reference apps or websites you'd like to point to?"
   → **Understanding Check**: PM summarizes Big Picture back to client in 2-3 sentences.
     Client confirms or corrects before proceeding.

   Round 2 — Features (one at a time):
   - For each user type: "What does this type of user mainly do?"
   - "What should happen when this feature encounters an error?"
   - "Please separate must-have features from nice-to-have features."
   → **Understanding Check**: PM summarizes feature priorities back to client.
     "Here's what I understand: [core features A, B, C] are must-haves, [D, E] are for later. Is that correct?"

   Round 3 — Constraints (one at a time):
   - "Web? Mobile? Both?"
   - "Design feel? (a) Minimal (b) Rich/decorative (c) Reference app if you have one"
   - "Is login required? What method?"
   - "Do you need payment functionality?"
   - "Do you need real-time features? (chat, notifications, location tracking, etc.)"
   → **Understanding Check**: PM summarizes technical constraints.

   Round 4 — Validation:
   - Compile all answers into spec.md (using templates/spec.md)
   - Show the customer a concise summary only if a final business-level confirmation is needed
   - Resolve any critical mismatches
   - Record remaining non-critical unknowns as assumptions, internal validation targets, or QA checks

   Round 5 — Pre-Handoff Question Generation (NEW):
   - PM anticipates questions the Design team (CTO + Designer) will have:
     - Technical ambiguities: unclear data flows, missing integration details
     - UX ambiguities: unspecified user flows, missing edge-case behaviors
     - Business ambiguities: priority conflicts, unclear scope boundaries
   - PM attempts to answer from interview knowledge; unresolvable ones go to CEO
   - CEO triages: answer internally or ask client ONE focused question
   - Resolved questions are appended to spec.md as "Design Team Pre-Brief" section

3. Spec Completion Check:
   - Count critical customer-owned questions in spec
   - If > 0: continue interview
   - If = 0: proceed to internal approval

4. Approval Flow:
   a. CEO reviews spec (dispatch forge:ceo agent)
   b. CEO confirms scope is feasible and safe to advance internally
   c. If no customer-owned blocker remains, update state.json: phase=2, phase_id="design", phase_name="design", spec_approved=true
   d. Update company runtime for the next gate:
      - `node scripts/forge-lane-runtime.mjs set-company-gate --gate design_readiness --gate-owner cto --delivery-state in_progress`
   e. Only ask the customer again if a true business blocker remains unresolved

5. PM defines the session brief for the next handoff:
   - current_session_goal
   - session_exit_criteria
   - next_session_goal
   - next_session_owner
   - session_handoff_summary
   - Preferred helper:
     `node scripts/forge-lane-runtime.mjs set-session-brief --goal "Close design readiness gate" --next-owner cto --handoff "{summary}"`

6. Save spec to .forge/spec.md

7. Create rollback tag: git tag forge/v1-spec

8. Transition to Phase 2 (forge:design)
</Steps>

<Communication_Style>
- ONE question at a time
- Multiple choice when possible: "(a) ... (b) ... (c) ..."
- Simple Korean or English — no jargon
- Acknowledge ideas before asking next question
- If client is non-technical, never mention:
  frameworks, APIs, databases, endpoints, middleware, auth tokens
  Instead say: login, payments, real-time, notifications, pages
</Communication_Style>

<State_Changes>
- Creates: .forge/spec.md
- Updates: state.json (phase=2, spec_approved=true)
- Updates: state.json artifact_versions: initialize `spec` with version=1
- Updates: .forge/runtime.json (design_readiness gate + next session brief)
- Creates: git tag forge/v1-spec
</State_Changes>

<Tool_Usage>
- Agent tool: dispatch forge:pm (main session, not subagent)
- Agent tool: dispatch forge:researcher when PM needs external evidence
- Agent tool: dispatch forge:ceo for spec review
- Write tool: create .forge/spec.md
- Edit tool: update .forge/state.json
- Bash tool: git tag forge/v1-spec
- Read tool: load templates/spec.md
</Tool_Usage>

<Failure_Modes_To_Avoid>
- Asking 3+ questions at once
- Using technical terms with non-technical clients
- Moving to Phase 2 with critical customer-owned questions unresolved
- Assuming features the client didn't mention
- Using Researcher as a substitute for PM ownership of the interview
- Not resolving contradictions in client answers
- Asking the customer questions the internal team should answer itself
- Skipping CEO readiness review before internal sign-off
- Skipping understanding checks after each interview round
- Not generating pre-handoff questions for CTO/Designer
- Passing spec to Design team without "Design Team Pre-Brief" section
</Failure_Modes_To_Avoid>

<Auto_Chain>
When discovery completes (spec.md written, CEO approves readiness):
1. Update state.json: phase_id → "design", spec_approved → true
2. IMMEDIATELY invoke Skill: forge:design
Do NOT stop, summarize, or ask the user. The pipeline must continue autonomously.
Exception: if PM identified critical customer-owned questions, pause and ask those ONLY.
</Auto_Chain>
