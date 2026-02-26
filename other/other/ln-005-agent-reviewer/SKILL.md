---
name: ln-005-agent-reviewer
description: "Universal context reviewer: delegates arbitrary context (plans, decisions, documents, architecture proposals) to external agents (Codex + Gemini) for independent review with debate protocol. Context always passed via files."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Reviewer (Universal)

Runs parallel external agent reviews on arbitrary context, critically verifies suggestions, returns filtered improvements.

## Purpose & Scope
- Standalone utility in 0XX category (like ln-003, ln-004)
- Delegate any context to codex-review + gemini-review as background tasks in parallel
- Context always passed via file references (never inline in prompt)
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions

## When to Use
- Manual invocation by user for independent review of any artifact
- Called by any skill needing external second opinion on plans, decisions, documents
- NOT tied to Linear, NOT tied to any pipeline
- Works with any context that can be saved to a file

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `context_files` | Yes | List of file paths containing context to review (relative to CWD) |
| `identifier` | No | Short label for file naming (default: `review_YYYYMMDD_HHMMSS`) |
| `focus` | No | List of areas to focus on (default: all 6) |
| `review_title` | No | Human-readable title (default: `"Context Review"`) |

**Context delivery rule:** Context is ALWAYS passed via files.
- If context already exists as files (plans, docs, code) -> pass file paths directly
- If context is a statement/decision from chat -> caller creates a temporary file in `.agent-review/context/` with the content, then passes the file path

## Workflow

**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol (Challenge Round 1 + Follow-Up Round).

1) **Health check:** `python shared/agents/agent_runner.py --health-check`
   - Filter output by `skill_groups` containing "005"
   - If 0 agents available -> return `{verdict: "SKIPPED", reason: "no agents available"}`
   - Display: `"Agent Health: codex-review OK, gemini-review OK"` (or similar)

2) **Resolve identifier:** If `identifier` not provided, generate `review_YYYYMMDD_HHMMSS`. Sanitize: lowercase, replace spaces with hyphens, ASCII only.

3) **Ensure .agent-review/:**
   - If `.agent-review/` exists -> reuse as-is, do NOT recreate `.gitignore`
   - If `.agent-review/` does NOT exist -> create it + `.agent-review/.gitignore` (content: `*` + `!.gitignore`)
   - Create `.agent-review/{agent}/` subdirs only if they don't exist
   - Create `.agent-review/context/` subdir if it doesn't exist (for materialized context files)
   - Do NOT add `.agent-review/` to project root `.gitignore`

4) **Materialize context (if needed):** If context is from chat/conversation (not an existing file):
   - Write content to `.agent-review/context/{identifier}_context.md`
   - Add this path to `context_files` list

5) **Build prompt:** Read template `shared/agents/prompt_templates/context_review.md`.
   - Replace `{review_title}` with title or `"Context Review"`
   - Replace `{context_refs}` with bullet list: `- {path}` per context file
   - Replace `{focus_areas}` with filtered subset or `"All default areas"` if no focus specified
   - Save to `.agent-review/{agent}/{identifier}_contextreview_prompt.md` (one copy per agent — identical content)

6) **Run agents (background, process-as-arrive):**

   a) Launch BOTH agents as background Bash tasks (run_in_background=true):
      - `python shared/agents/agent_runner.py --agent codex-review --prompt-file .agent-review/codex/{identifier}_contextreview_prompt.md --output-file .agent-review/codex/{identifier}_contextreview_result.md --cwd {cwd}`
      - `python shared/agents/agent_runner.py --agent gemini-review --prompt-file .agent-review/gemini/{identifier}_contextreview_prompt.md --output-file .agent-review/gemini/{identifier}_contextreview_result.md --cwd {cwd}`

   b) When first agent completes (background task notification):
      - Read its result file from `.agent-review/{agent}/{identifier}_contextreview_result.md`
      - Parse JSON between `<!-- AGENT_REVIEW_RESULT -->` / `<!-- END_AGENT_REVIEW_RESULT -->` markers
      - Parse `session_id` from runner JSON output; write `.agent-review/{agent}/{identifier}_session.json`: `{"agent": "...", "session_id": "...", "review_type": "contextreview", "created_at": "..."}`
      - Proceed to Step 7 (Critical Verification) for this agent's suggestions

   c) When second agent completes:
      - Read its result file, parse suggestions
      - Run Step 7 for second batch
      - Merge verified suggestions from both agents

   d) If an agent fails: log failure, continue with available results

7) **Critical Verification + Debate** (per Debate Protocol in `shared/references/agent_delegation_pattern.md`):

   For EACH suggestion from agent results:

   a) **Claude Evaluation:** Independently assess — is the issue real? Actionable? Conflicts with project patterns?

   b) **AGREE** -> accept as-is. **DISAGREE/UNCERTAIN** -> initiate challenge.

   c) **Challenge + Follow-Up (with session resume):** Follow Debate Protocol (Challenge Round 1 -> Follow-Up Round if not resolved). Resume agent's review session for full context continuity:
      - Read `session_id` from `.agent-review/{agent}/{identifier}_session.json`
      - Run with `--resume-session {session_id}` — agent continues in same session, preserving file analysis and reasoning
      - If `session_resumed: false` in result -> log warning, result still valid (stateless fallback)
      - `{review_type}` = review_title or "Context Review"
      - `{story_ref}` placeholder in challenge template = identifier
      - Challenge files: `.agent-review/{agent}/{identifier}_contextreview_challenge_{N}_prompt.md` / `_result.md`
      - Follow-up files: `.agent-review/{agent}/{identifier}_contextreview_followup_{N}_prompt.md` / `_result.md`

   d) **Persist:** all challenge and follow-up prompts/results in `.agent-review/{agent}/`

8) **Aggregate + Return:** Collect ACCEPTED suggestions only (after verification + debate).
   Deduplicate by `(area, issue)` — keep higher confidence.
   **Filter:** `confidence >= 90` AND `impact_percent > 2`.
   **Return** JSON with suggestions + agent_stats + debate_log. **NO cleanup/deletion.**

## Output Format

```yaml
verdict: CONTEXT_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "logic | feasibility | completeness | consistency | best_practices | risk"
    issue: "What is wrong or could be improved"
    suggestion: "Specific actionable change"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | accepted_after_followup | rejected"
agent_stats:
  - name: "codex-review"
    duration_s: 8.2
    suggestion_count: 2
    accepted_count: 1
    challenged_count: 1
    followup_count: 1
    status: "success | failed | timeout"
debate_log:
  - suggestion_summary: "Missing error handling for network failures"
    agent: "codex-review"
    rounds:
      - round: 1
        claude_position: "Error handling exists in middleware layer"
        agent_decision: "DEFEND"
        resolution: "follow_up"
      - round: 2
        claude_position: "Middleware covers all HTTP routes, agent cited only specific endpoint"
        agent_decision: "MODIFY"
        resolution: "accepted_after_followup"
    final_resolution: "accepted_after_followup"
```

## Fallback Rules

| Condition | Action |
|-----------|--------|
| Both agents succeed | Aggregate verified suggestions from both |
| One agent fails | Use successful agent's verified suggestions, log failure |
| Both agents fail | Return `{verdict: "SKIPPED", reason: "agents failed"}` |

## Verdict Escalation
- **No escalation.** Suggestions are advisory only.
- Caller decides how to apply accepted suggestions.

## Critical Rules
- Read-only review — agents must NOT modify project files (enforced by prompt CRITICAL CONSTRAINTS)
- Context always delivered via file references (never inline in agent prompt)
- Same prompt to all agents (identical input for fair comparison)
- JSON output schema required from agents (via `--json` / `--output-format json`)
- Log all attempts for user visibility (agent name, duration, suggestion count)
- **Persist** prompts, results, and challenge artifacts in `.agent-review/{agent}/` — do NOT delete
- Ensure `.agent-review/.gitignore` exists before creating files (only create if `.agent-review/` is new)
- **NO TIMEOUT KILL — WAIT FOR RESPONSE:** Do NOT kill agent background tasks. WAIT until agent completes and delivers its response — do NOT proceed without it, do NOT use TaskStop. Agents are instructed to respond within 10 minutes via prompt constraint, but the hard behavior is: wait for completion or crash. Only a hard crash (non-zero exit code, connection error) is treated as failure. TaskStop is FORBIDDEN for agent tasks.
- **CRITICAL VERIFICATION:** Do NOT trust agent suggestions blindly. Claude MUST independently verify each suggestion and debate if disagreeing. Accept only after verification.

## Definition of Done
- All available agents launched as background tasks (or gracefully failed with logged reason)
- Prompts persisted in `.agent-review/{agent}/` for each agent
- Raw results persisted in `.agent-review/{agent}/` (no cleanup)
- Each suggestion critically verified by Claude; challenges executed for disagreements
- Follow-up rounds executed for suggestions rejected after Round 1 (DEFEND+weak / MODIFY+disagree)
- Challenge and follow-up prompts/results persisted alongside review artifacts
- Accepted suggestions filtered by confidence >= 90 AND impact_percent > 2
- Deduplicated verified suggestions returned with verdict, agent_stats, and debate_log
- `.agent-review/.gitignore` exists (created only if `.agent-review/` was new)
- Session files persisted in `.agent-review/{agent}/{identifier}_session.json` for debate resume

## Reference Files
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/context_review.md`
- **Prompt template (challenge):** `shared/agents/prompt_templates/challenge_review.md`
- **Review schema:** `shared/agents/schemas/context_review_schema.json`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`
- **Agent registry:** `shared/agents/agent_registry.json`
- **Agent runner:** `shared/agents/agent_runner.py`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-25
