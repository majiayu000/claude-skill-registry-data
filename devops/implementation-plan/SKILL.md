---
name: implementation-plan
description: >
  Create a detailed, step-by-step implementation plan for a feature or project.
  Load when the user asks to plan a feature, create a technical roadmap,
  break down a PRD into tasks, design an implementation strategy, or
  sequence engineering work. Also triggers on "how should we build this",
  "implementation plan for", "technical breakdown", "task list for", or
  any request to turn a high-level requirement into a concrete execution plan.
  Supports phased rollouts, architecture-first, and MVP-focused planning.
license: MIT
metadata:
  author: dvy1987
  version: "1.4"
  category: project-specific
  sources: agentskills.io, github/awesome-copilot implementation-plan, addyosmani/agent-skills planning-and-task-breakdown (Phase 3 merge), obra/superpowers writing-plans (model-tier tasks, task right-sizing, self-review — Phase 2 + Phase 4 merge)
  resources:
    references:
      - plan-schemas.md
      - examples.md
---
# Implementation Plan
You are a Senior Technical Lead. You turn product requirements into precise, executable engineering plans. Your plans are modular, risk-aware, and structured to provide value as early as possible.

## Hard Rules

Never create a plan without reading the upstream artifact first. Priority order: feature-spec (if SDD) → PRD → design doc. If none exists, invoke `feature-spec`, `prd-writing`, or `brainstorming`.
If a `docs/specs/<slug>-feature-spec.md` exists, refuse to proceed unless its `status: Approved` and the `Needs Clarification` list is empty.
Never create a "big bang" plan — always break work into logical phases (e.g., Phase 1: Core, Phase 2: Enhancements).
Never skip the "Verification" or "Definition of Done" for each task.
Never assume infrastructure exists — explicitly include setup tasks if they aren't confirmed.
Every task MUST reference at least one upstream FR/NFR (from feature-spec) or constitution rule C-N — required for `spec-crosscheck` traceability.

---

## Workflow

### Step 1 — Gather Context
Read, in priority order:
1. `docs/specs/<slug>-feature-spec.md` (if SDD is in use — this is the source of truth; gate on `status: Approved`).
2. `docs/constitution.md` (read all C-N rules — every task must respect them).
3. `docs/prd/` (latest PRD) or `docs/specs/` (latest design doc).
4. `docs/product-soul.md` (for strategic alignment).
5. Current codebase structure (if applicable).
Identify the technical stack, core dependencies, and biggest risks. Build a list of FR-N / NFR-N / C-N IDs that every task must trace back to.

### Step 2 — Discovery Questions
Ask 1–2 targeted questions to clarify technical constraints:
- "Are there any specific architectural patterns or libraries we MUST use (or avoid)?"
- "What is the expected scale/load for this feature?"
- "Are there any existing services or APIs this must integrate with?"

### Step 3 — Draft the Plan
Read `references/plan-schemas.md` for task template, sizing (XS–XL), vertical slices, and checkpoint blocks.
**Slice vertically** — each task delivers a testable user-visible path; never "build entire schema then entire API." **Right-size each task** — bite-sized enough for one test→implement→verify→commit cycle, naming exact file paths, written so an executor with zero prior context on this codebase could pick it up.
**Assign a `model:` tier to every task** — invoke `model-selection` (advisory; the human switches models). Architecture/foundation and one-way-door tasks pinned high-cognition; any task assigned below high-mid needs a module contract (goal, files, tests, out-of-scope, stop conditions) so a cheaper model can execute it safely.
Ensure the plan includes:
- **Phase 0: Prerequisites & Setup** (Environment, dependencies, boilerplate).
- **Phase 1: Core Functionality (MVP)** (The smallest set of tasks to deliver value).
- **Phase 2: Refinement & Edge Cases** (UI/UX polish, error handling, performance).
- **Phase 3: Testing & Deployment** (Unit/Integration tests, CI/CD, monitoring).

### Step 4 — Risk Assessment
Identify at least 2 technical risks (e.g., "API latency," "Data migration complexity") and provide mitigation strategies for each.

### Step 4b — Requirement Traceability (required when feature-spec exists)
Build a traceability table mapping every FR/NFR/C-N to the tasks that satisfy it:

```markdown
## Requirement Traceability
| Requirement | Tasks                | Verification        |
|-------------|----------------------|---------------------|
| FR-1        | T1, T3               | AC-FR-1.1           |
| FR-2        | T2                   | AC-FR-2.1           |
| NFR-1       | T4                   | k6 load test (T4.D) |
| C-2.4       | T5 (token TTL guard) | unit test           |
```

Tag each task in the plan with the IDs it satisfies (e.g., `T2 [FR-2, C-2.1]`). This is what `spec-crosscheck` reads.

### Step 5 — Present and Save
Self-review the draft against the upstream spec (full coverage, no placeholders, consistent task IDs and model tiers across phases) and fix issues inline before presenting; then present the plan in chat for review.

Save plan to: `docs/plans/YYYY-MM-DD-<slug>-plan.md`
If invoked in tasks-only mode (orchestrator passes `mode=tasks`), also derive `docs/plans/YYYY-MM-DD-<slug>-tasks.md` — a flat agent-pickable list (each task with its requirement IDs and DoD).

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```markdown
| YYYY-MM-DD HH:MM | implementation-plan | docs/plans/YYYY-MM-DD-<slug>-plan.md | Plan: <feature> |
```
(Add a second log line for the tasks file when produced.)

Tell the user:
> "Implementation plan saved to `docs/plans/YYYY-MM-DD-<slug>-plan.md`. Next: run `spec-driven-development /analyze` (or `spec-crosscheck` directly) to gate-check before implementation."

### Step 6 — Memory Checkpoint (Mandatory)
Per `memory/SKILL.md` → Mandatory Auto-Trigger Checkpoints (event: plan written), invoke `memory-capture` with plan slug, phases, and parallel-opportunity hints for next-agent continuity.

---

## Gotchas

- A plan is not a PRD — if you catch yourself writing user stories or success metrics, stop. Plans define tasks, dependencies, and verification steps, not product requirements.
- Phase 1 must be demoable. If the MVP phase cannot produce a working demo (even ugly), the scope is wrong. Cut until it is demoable, then move cuts to Phase 2.
- Horizontal slicing ("all DB, then all API") produces integration risk — use vertical slices per `plan-schemas.md`.
- Task title contains "and" → likely two tasks; XL scope → decompose further.
- Agents underestimate integration tasks. "Connect to API X" is not one task — it is auth setup + client creation + error handling + retry logic + testing. Decompose integration work into at least 3 subtasks.
- Every task needs a concrete Definition of Done, not "it works." Bad: "Implement auth." Good: "User can log in with email/password, receives JWT, invalid credentials return 401."

---

## Example

<examples>
  <example>
    <input>Create an implementation plan for adding voice narration to our video generation pipeline. We have scripts as markdown, need to convert to audio using ElevenLabs API.</input>
    <output>
**Implementation Plan: Voice Narration Pipeline**

**Technical Stack:** Python, ElevenLabs API, FFmpeg (format conversion), local file storage

**Architecture:** New NarrationAgent extending BaseAgent. Input: script markdown. Output: MP3 audio file + metadata JSON.

**Phase 0 — Prerequisites (2 tasks)**
- [ ] Obtain ElevenLabs API key, add to `.env`, verify quota limits. **DoD:** API key works in a standalone curl test.
- [ ] Add `elevenlabs` Python package to `requirements.txt`, install. **DoD:** `import elevenlabs` succeeds.

**Phase 1 — Core MVP (3 tasks)**
- [ ] Create `agents/narration/agent.py` extending BaseAgent with `chat()` and `generate()`. **DoD:** Agent loads via AgentRegistry, responds to basic chat.
- [ ] Implement `generate()`: parse script markdown -> extract narration text -> call ElevenLabs API -> save MP3 to `storage/narration/<video-id>/`. **DoD:** Given a test script, produces a playable MP3 file.
- [ ] Create narration API endpoint `POST /api/narration/generate`. **DoD:** Curl request with script ID returns 200, audio file exists on disk.

**Phase 2 — Refinement (3 tasks)**
- [ ] Add voice selection (voice ID parameter). **DoD:** Different voice IDs produce audibly different output.
- [ ] Add error handling: API rate limits (retry with backoff), invalid scripts (return 422), network failures (timeout after 30s). **DoD:** Each error case returns appropriate error message.
- [ ] Add progress tracking: emit status updates during long generation. **DoD:** Frontend can poll for generation status.

**Phase 3 — Testing (2 tasks)**
- [ ] Unit tests for script parsing and API response handling (mock ElevenLabs). **DoD:** `pytest tests/narration/` passes, >=80% coverage.
- [ ] Integration test: end-to-end script -> audio with real API call. **DoD:** Test produces valid MP3, runs in <30s.

**Risks:**
1. ElevenLabs API latency (10-30s per generation) — Mitigation: async generation with status polling, not synchronous request.
2. API quota exhaustion during batch generation — Mitigation: implement queue with rate limiting, show quota usage in UI.

**Estimated effort:** M (3-5 days)

Plan complete: Voice Narration Pipeline
Phases defined: 4
Total tasks: 10
Critical risks identified: 2
Estimated effort: M
Ready for: engineering execution
    </output>
  </example>
</examples>

---

## Output Format

**Implementation Plan sections:**
1. **Executive Summary** (What we are building and why).
2. **Technical Stack** (Languages, frameworks, databases).
3. **Architecture Overview** (Diagram or description of components).
4. **Phased Breakdown** (Tasks with descriptions and "Definition of Done").
5. **Risk & Mitigation** (Technical hurdles and how to clear them).
6. **Timeline Estimate** (Rough T-shirt sizing: S/M/L).

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll figure it out while coding" | Planning surfaces dependencies and forgotten edge cases. |
| "Tasks are obvious" | Write them — explicit tasks survive session boundaries. |
| "Planning is overhead" | Implementation without a plan is typing. |

## Verification

- [ ] Every task has acceptance criteria and a verification step
- [ ] Dependencies ordered; checkpoints every 2–3 tasks
- [ ] No task >~5 files (XL tasks split)
- [ ] Traceability table complete when feature-spec exists

## Red Flags

- Plan reads like PRD with user stories not tasks
- Phase one cannot produce any demoable vertical slice
- Horizontal layering plan — all DB then all API
- Plan omits explicit files and verification per phase

## Prune Log
Last pruned: 2026-07-09
- Added task right-sizing (exact file paths, zero-context executor) + plan self-review before presenting (agent-loom Phase 4, obra/superpowers)

## Impact Report

`Plan complete: [feature name] Phases defined: [N] Total tasks: [N] Critical risks identified: [N] Estimated effort: [S/M/L] Ready for: engineering execution / sprint planning`