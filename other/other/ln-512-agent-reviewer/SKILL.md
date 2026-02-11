---
name: ln-512-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on code changes. Reference-based prompts. Returns filtered suggestions with confidence scoring."
---

# Agent Reviewer (Code)

Runs parallel external agent reviews on code implementation, returns filtered suggestions.

## Purpose & Scope
- Worker in ln-510 quality coordinator pipeline (invoked by ln-511 Step 7)
- Run codex-review + gemini-review in parallel on code changes
- Return filtered, deduplicated suggestions with confidence scoring
- Health check + prompt execution in single invocation (minimal timing gap between availability check and actual API call)

## When to Use
- **Invoked by ln-511-code-quality-checker** Step 7 (Agent Review)
- All implementation tasks in Story status = Done
- Code quality analysis (Steps 1-6) already completed by ln-511

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern and Review Persistence Pattern.

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
5) **Run agents in parallel** (two Bash calls simultaneously):
   - `python shared/agents/agent_runner.py --agent codex-review --prompt-file .agent-review/codex/{identifier}_codereview_prompt.md --cwd {cwd}`
   - `python shared/agents/agent_runner.py --agent gemini-review --prompt-file .agent-review/gemini/{identifier}_codereview_prompt.md --cwd {cwd}`
6) **Save results:** Save each agent's raw response to `.agent-review/{agent}/{identifier}_codereview_result.md`
7) **Aggregate + Return:** Collect suggestions from all successful responses. Deduplicate by `(area, issue)` — keep higher confidence.
   **Filter:** `confidence >= 90` AND `impact_percent > 2`.
   **Return** JSON with suggestions + agent stats to parent skill. **NO cleanup/deletion.**

## Output Format

```yaml
verdict: CODE_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | correctness | best_practices"
    issue: "What is wrong"
    suggestion: "Specific fix"
    confidence: 95
    impact_percent: 15
agent_stats:
  - name: "codex-review"
    duration_s: 12.4
    suggestion_count: 3
    status: "success | failed | timeout"
```

## Fallback Rules

| Condition | Action |
|-----------|--------|
| Both agents succeed | Aggregate suggestions from both |
| One agent fails | Use successful agent's suggestions, log failure |
| Both agents fail | Return `{verdict: "SKIPPED", reason: "agents failed"}` |
| Parent skill (ln-511) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- Findings with `area=security` or `area=correctness` -> parent skill can escalate PASS -> CONCERNS
- This skill returns raw suggestions; escalation decision is made by ln-511

## Critical Rules
- Read-only review — agents must NOT modify files (enforced by prompt CRITICAL CONSTRAINTS)
- Same prompt to all agents (identical input for fair comparison)
- JSON output schema required from agents (via `--json` / `--output-format json`)
- Log all attempts for user visibility (agent name, duration, suggestion count)
- **Persist** prompts and results in `.agent-review/{agent}/` — do NOT delete
- Ensure `.agent-review/.gitignore` exists before creating files

## Definition of Done

- Health check executed; available agents identified (or SKIPPED returned if none)
- Story + Done implementation Tasks fetched from Linear (or local files)
- `.agent-review/` directory created with `.gitignore` and per-agent subdirs
- Prompt built from template with story/task references, saved per agent
- All available agents executed in parallel; raw results saved to `.agent-review/{agent}/`
- Suggestions aggregated, deduplicated by (area, issue), filtered (confidence >= 90, impact > 2%)
- JSON result returned to parent skill with verdict, suggestions list, and agent_stats

## Reference Files
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template:** `shared/agents/prompt_templates/code_review.md`
- **Agent registry:** `shared/agents/agent_registry.json`
- **Agent runner:** `shared/agents/agent_runner.py`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-08
