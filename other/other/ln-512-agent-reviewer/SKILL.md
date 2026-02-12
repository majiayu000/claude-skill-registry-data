---
name: ln-512-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on code changes. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions with confidence scoring."
---

# Agent Reviewer (Code)

Runs parallel external agent reviews on code implementation, critically verifies suggestions, returns filtered improvements.

## Purpose & Scope
- Worker in ln-510 quality coordinator pipeline (invoked by ln-511 Step 7)
- Run codex-review + gemini-review as background tasks in parallel
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions with confidence scoring
- Health check + prompt execution in single invocation

## When to Use
- **Invoked by ln-511-code-quality-checker** Step 7 (Agent Review)
- All implementation tasks in Story status = Done
- Code quality analysis (Steps 1-6) already completed by ln-511

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, and Agent Timeout Policy.

1) **Health check:** `python shared/agents/agent_runner.py --health-check`
   - Filter output by `skill_groups` containing "512"
   - If 0 agents available -> return `{verdict: "SKIPPED", reason: "no agents available"}`
   - Display: `"Agent Health: codex-review OK, gemini-review UNAVAILABLE"` (or similar)

2) **Get references:** Call Linear MCP `get_issue(storyId)` -> extract URL + identifier. Call `list_issues(filter: {parent: {id: storyId}, status: "Done"})` -> extract Done implementation Task URLs/identifiers (exclude label "tests").
   - If project stores tasks locally (e.g., `docs/tasks/`) -> use local file paths instead of Linear URLs.

3) **Ensure .agent-review/:** Create `.agent-review/{agent}/` dirs for each available agent (e.g., `codex/`, `gemini/`). Create `.agent-review/.gitignore` with content `*` + `!.gitignore`. Add `.agent-review/` to project root `.gitignore` if missing.

4) **Build prompt:** Read template `shared/agents/prompt_templates/code_review.md`.
   - Replace `{story_ref}` with `- Linear: {url}` or `- File: {path}`
   - Replace `{task_refs}` with bullet list: `- {identifier}: {url_or_path}` per task
   - Save to `.agent-review/{agent}/{identifier}_codereview_prompt.md` (one copy per agent — identical content)

5) **Run agents (background, process-as-arrive):**

   a) Launch BOTH agents as background Bash tasks (run_in_background=true):
      - `python shared/agents/agent_runner.py --agent codex-review --prompt-file .agent-review/codex/{identifier}_codereview_prompt.md --output-file .agent-review/codex/{identifier}_codereview_result.md --cwd {cwd}`
      - `python shared/agents/agent_runner.py --agent gemini-review --prompt-file .agent-review/gemini/{identifier}_codereview_prompt.md --output-file .agent-review/gemini/{identifier}_codereview_result.md --cwd {cwd}`

   b) When first agent completes (background task notification):
      - Read its result file from `.agent-review/{agent}/{identifier}_codereview_result.md`
      - Parse JSON between `<!-- AGENT_REVIEW_RESULT -->` / `<!-- END_AGENT_REVIEW_RESULT -->` markers
      - Proceed to Step 6 (Critical Verification) for this agent's suggestions

   c) When second agent completes:
      - Read its result file, parse suggestions
      - Run Step 6 for second batch
      - Merge verified suggestions from both agents

   d) If an agent fails: log failure, continue with available results

6) **Critical Verification + Debate:**

   For EACH suggestion from agent results:

   a) **Claude Evaluation:** Independently assess the suggestion:
      - Is the issue real? (check codebase and git diff yourself)
      - Is the suggestion actionable and correct?
      - Does it conflict with project patterns or architectural decisions?

   b) **Decision:**

      | Claude Assessment | Action |
      |-------------------|--------|
      | AGREE | Accept suggestion as-is |
      | DISAGREE or UNCERTAIN | Initiate challenge (step 6c) |

   c) **Challenge Round** (1 round max per suggestion):
      - Build prompt from `shared/agents/prompt_templates/challenge_review.md`
      - Fill placeholders: `{review_type}` = "Code Implementation", `{story_ref}`, `{area}`, `{issue}`, `{suggestion}`, `{reason}`, `{confidence}`, `{counterargument}` = Claude's specific objection
      - Save to `.agent-review/{agent}/{identifier}_codereview_challenge_{N}_prompt.md`
      - Run: `python shared/agents/agent_runner.py --agent {same_agent} --prompt-file .agent-review/{agent}/{identifier}_codereview_challenge_{N}_prompt.md --output-file .agent-review/{agent}/{identifier}_codereview_challenge_{N}_result.md --cwd {cwd}`
      - Parse challenge response

   d) **Resolution:**

      | Agent Response | Action |
      |----------------|--------|
      | DEFEND + convincing evidence (cites standard/code Claude missed, confidence >= 85) | Accept agent's suggestion |
      | DEFEND + weak evidence | Reject (Claude's position wins) |
      | WITHDRAW | Reject suggestion |
      | MODIFY + acceptable revision | Accept modified version |
      | MODIFY + still disagree | Reject |

   e) **Persist:** challenge prompts and results in `.agent-review/{agent}/`

7) **Aggregate + Return:** Collect ACCEPTED suggestions only (after verification + debate).
   Deduplicate by `(area, issue)` — keep higher confidence.
   **Filter:** `confidence >= 90` AND `impact_percent > 2`.
   **Return** JSON with suggestions + agent_stats + debate_log to parent skill. **NO cleanup/deletion.**

## Output Format

```yaml
verdict: CODE_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | correctness | best_practices"
    issue: "What is wrong"
    suggestion: "Specific fix"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | rejected"
agent_stats:
  - name: "codex-review"
    duration_s: 12.4
    suggestion_count: 3
    accepted_count: 2
    challenged_count: 1
    status: "success | failed | timeout"
debate_log:
  - suggestion_summary: "N+1 query in UserRepository.GetAll()"
    agent: "gemini-review"
    claude_position: "Query uses Include() which resolves N+1"
    agent_decision: "WITHDRAW"
    resolution: "rejected"
```

## Fallback Rules

| Condition | Action |
|-----------|--------|
| Both agents succeed | Aggregate verified suggestions from both |
| One agent fails | Use successful agent's verified suggestions, log failure |
| Both agents fail | Return `{verdict: "SKIPPED", reason: "agents failed"}` |
| Parent skill (ln-511) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- Findings with `area=security` or `area=correctness` -> parent skill can escalate PASS -> CONCERNS
- This skill returns raw verified suggestions; escalation decision is made by ln-511

## Critical Rules
- Read-only review — agents must NOT modify project files (enforced by prompt CRITICAL CONSTRAINTS)
- Same prompt to all agents (identical input for fair comparison)
- JSON output schema required from agents (via `--json` / `--output-format json`)
- Log all attempts for user visibility (agent name, duration, suggestion count)
- **Persist** prompts, results, and challenge artifacts in `.agent-review/{agent}/` — do NOT delete
- Ensure `.agent-review/.gitignore` exists before creating files
- **MANDATORY INVOCATION:** Parent skills MUST invoke this skill. Returns SKIPPED gracefully if agents unavailable. Parent must NOT pre-check and skip.
- **NO TIMEOUT KILL:** Do NOT kill agent background tasks if they are running. Agents have no time limit as long as they have not crashed with an error. Only a hard crash (non-zero exit code, connection error) is treated as failure. TaskStop is FORBIDDEN for agent tasks.
- **CRITICAL VERIFICATION:** Do NOT trust agent suggestions blindly. Claude MUST independently verify each suggestion and debate if disagreeing. Accept only after verification.

## Definition of Done

- Health check executed; available agents identified (or SKIPPED returned if none)
- Story + Done implementation Tasks fetched from Linear (or local files)
- `.agent-review/` directory created with `.gitignore` and per-agent subdirs
- Prompt built from template with story/task references, saved per agent
- All available agents launched as background tasks; raw results saved to `.agent-review/{agent}/`
- Each suggestion critically verified by Claude; challenges executed for disagreements
- Challenge prompts and results persisted alongside review artifacts
- Suggestions aggregated, deduplicated by (area, issue), filtered (confidence >= 90, impact > 2%)
- JSON result returned to parent skill with verdict, suggestions list, agent_stats, and debate_log

## Reference Files
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/code_review.md`
- **Prompt template (challenge):** `shared/agents/prompt_templates/challenge_review.md`
- **Agent registry:** `shared/agents/agent_registry.json`
- **Agent runner:** `shared/agents/agent_runner.py`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
