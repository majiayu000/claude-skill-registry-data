---
name: ln-311-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on Story/Tasks. Reference-based prompts. Returns filtered suggestions for Story validation."
---

# Agent Reviewer (Story)

Runs parallel external agent reviews on validated Story and Tasks, returns editorial suggestions.

## Purpose & Scope
- Worker in ln-310 validation pipeline (invoked in Phase 5)
- Run codex-review + gemini-review in parallel on Story/Tasks
- Return filtered, deduplicated suggestions for Story/Tasks improvement
- Health check + prompt execution in single invocation (minimal timing gap between availability check and actual API call)

## When to Use
- **Invoked by ln-310-story-validator** Phase 5 (Agent Review)
- After Phase 4 auto-fixes applied, Penalty Points = 0
- Story and Tasks are in their final form before approval

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern and Review Persistence Pattern.

1) **Health check:** `python shared/agents/agent_runner.py --health-check`
   - Filter output by `skill_groups` containing "311"
   - If 0 agents available -> return `{verdict: "SKIPPED", reason: "no agents available"}`
   - Display: `"Agent Health: codex-review OK, gemini-review OK"` (or similar)
2) **Get references:** Call Linear MCP `get_issue(storyId)` -> extract URL + identifier. Call `list_issues(filter: {parent: {id: storyId}})` -> extract child Task URLs/identifiers.
   - If project stores tasks locally (e.g., `docs/tasks/`) -> use local file paths instead of Linear URLs.
3) **Ensure .agent-review/:** Create `.agent-review/{agent}/` dirs for each available agent (e.g., `codex/`, `gemini/`). Create `.agent-review/.gitignore` with content `*` + `!.gitignore`. Add `.agent-review/` to project root `.gitignore` if missing.
4) **Build prompt:** Read template `shared/agents/prompt_templates/story_review.md`.
   - Replace `{story_ref}` with `- Linear: {url}` or `- File: {path}`
   - Replace `{task_refs}` with bullet list: `- {identifier}: {url_or_path}` per task
   - Save to `.agent-review/{agent}/{identifier}_storyreview_prompt.md` (one copy per agent — identical content)
5) **Run agents in parallel** (two Bash calls simultaneously):
   - `python shared/agents/agent_runner.py --agent codex-review --prompt-file .agent-review/codex/{identifier}_storyreview_prompt.md --cwd {cwd}`
   - `python shared/agents/agent_runner.py --agent gemini-review --prompt-file .agent-review/gemini/{identifier}_storyreview_prompt.md --cwd {cwd}`
6) **Save results:** Save each agent's raw response to `.agent-review/{agent}/{identifier}_storyreview_result.md`
7) **Aggregate + Return:** Collect suggestions from all successful responses. Deduplicate by `(area, issue)` — keep higher confidence.
   **Filter:** `confidence >= 90` AND `impact_percent > 2`.
   **Return** JSON with suggestions + agent stats to parent skill. **NO cleanup/deletion.**

## Output Format

```yaml
verdict: STORY_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | feasibility | best_practices"
    issue: "What is wrong or could be improved"
    suggestion: "Specific change to Story or Tasks"
    confidence: 95
    impact_percent: 15
agent_stats:
  - name: "codex-review"
    duration_s: 8.2
    suggestion_count: 2
    status: "success | failed | timeout"
```

## Fallback Rules

| Condition | Action |
|-----------|--------|
| Both agents succeed | Aggregate suggestions from both |
| One agent fails | Use successful agent's suggestions, log failure |
| Both agents fail | Return `{verdict: "SKIPPED", reason: "agents failed"}` |
| Parent skill (ln-310) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- **No escalation.** Suggestions are editorial only — they modify Story/Tasks text.
- Parent skill (ln-310) Gate verdict remains unchanged by agent suggestions.

## Critical Rules
- Read-only review — agents must NOT modify files (enforced by prompt CRITICAL CONSTRAINTS)
- Same prompt to all agents (identical input for fair comparison)
- JSON output schema required from agents (via `--json` / `--output-format json`)
- Log all attempts for user visibility (agent name, duration, suggestion count)
- **Persist** prompts and results in `.agent-review/{agent}/` — do NOT delete
- Ensure `.agent-review/.gitignore` exists before creating files

## Definition of Done
- All available agents executed (or gracefully failed with logged reason)
- Prompts persisted in `.agent-review/{agent}/` for each agent
- Raw results persisted in `.agent-review/{agent}/` (no cleanup)
- Suggestions filtered by confidence >= 90 AND impact_percent > 2
- Deduplicated suggestions returned to parent skill with verdict and agent_stats
- `.agent-review/.gitignore` exists; `.agent-review/` added to project `.gitignore`

## Reference Files
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template:** `shared/agents/prompt_templates/story_review.md`
- **Agent registry:** `shared/agents/agent_registry.json`
- **Agent runner:** `shared/agents/agent_runner.py`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-08
