---
name: mentor
description: >
  Generate an /insights-style HTML report across MANY of your agent coding sessions
  (Claude Code and OpenAI Codex): what you work on, how you use the agent, your wins,
  your friction points, and concrete fixes to become more effective — precise
  goal-setting, not trusting output blindly, scoping, context hygiene, right-sizing
  models. Reads local session history and writes one self-contained report.html. Use
  when the user asks to "разбери мои сессии", "оцени как я работаю с агентом", "мой
  insights", "session insights report", "review how I work", "на что обратить
  внимание", or runs "/mentor", "/mentor claude", "/mentor codex", "/mentor both".
  Do NOT use for reviewing the CODE produced (that's code-review) or building the agent.
---

# Mentor — /insights-style report on how you work with agents

## Why this exists
Agents now do what juniors used to. But juniors became seniors by getting feedback
from seniors. Give agents to juniors and fire the seniors, and nobody gets that
feedback loop anymore. This skill *is* that loop: it reads your own local session
history and hands back a single report — what you build, where you lose time, and
concrete changes to get better. Effectiveness, not token-golf.

**The deliverable is the rendered `report.html` file — always.** The eight-section
analysis is intermediate: it goes into `analysis.json` and gets rendered, never
pasted into chat. A wall of analysis text in the reply is the failure this skill
exists to fix. If you cannot run the scripts, say so plainly — do not substitute a
text summary. Modeled on Claude Code's built-in `/insights`.

## Agents

| Agent | arg | Logs |
|---|---|---|
| Claude Code | `claude` | `~/.claude/projects/<slug>/<uuid>.jsonl` |
| OpenAI Codex | `codex` | `~/.codex/sessions/**/rollout-*.jsonl` (+ `~/.codex/archived_sessions/`) |
| both | `both` (default) | union of the two |

## Workflow — build the report

1. **Collect** every session in the window into one stats bundle (deterministic):
   ```bash
   uv run --no-project python ~/.claude/skills/mentor/scripts/collect.py \
     --agent <claude|codex|both> --days <N> --out /tmp/mentor-stats.json
   ```
   Default `--agent both --days 30`. It writes `stats.json` and prints a compact
   digest: headline numbers, tool mix, languages, projects, and every session's
   verbatim first prompt. Read that digest — it is your evidence.

2. **Analyze into eight sections.** Read `references/best-practices.md` for the canon,
   then write `/tmp/mentor-analysis.json` (schema in `scripts/render_report.py` header).
   Ground every claim in the digest (numbers, project names, prompt patterns). The
   eight sections, mirroring `/insights`:
   - **what_you_work_on** — sessions clustered into themes, with rough share.
   - **how_you_use** — patterns: tool ratios (Bash/exec vs Read), languages, both-agent split, checkpoints.
   - **impressive** — real wins, handed back.
   - **friction** — where time leaks. Each: problem, evidence, concrete fix. This section earns the report.
   - **features_to_try** — existing features they under-use.
   - **claude_md_additions** — copy-paste CLAUDE.md lines that kill a recurring friction.
   - **new_ways** — new ways to use the agent(s).
   - **on_the_horizon** — where the workflow is heading.
   Also write a `summary` that does not flatter — name what is hindering them.

3. **Render** the self-contained HTML:
   ```bash
   uv run --no-project python ~/.claude/skills/mentor/scripts/render_report.py \
     --stats /tmp/mentor-stats.json --analysis /tmp/mentor-analysis.json \
     --out ~/.claude/usage-data/mentor-report.html
   ```

4. **Deliver the file.** Open or hand over `~/.claude/usage-data/mentor-report.html`:
   in Claude Code use SendUserFile with display `render`; in Codex or a shell, open it
   (`open <path>`) and print the path. Then add at most two spoken lines: the single
   highest-leverage fix. The report carries the detail; the chat does not repeat it.

## Quick single-session mode (only on explicit request)
Only when the user explicitly points at ONE session ("разбери вот эту сессию"), skip
collect/render and run the per-session digest, then give a short text read (TL;DR,
what worked, what dragged down, one habit). Any "разбери мои сессии" / "/mentor" goes
through the report pipeline above, not this.
```bash
uv run --no-project python ~/.claude/skills/mentor/scripts/digest.py <path|last> --agent <claude|codex>
```

## Rules
- The report.html is the answer. Never paste the eight sections as a chat message.
- Analyze the process, not the code produced. Don't re-review what was built.
- Evidence or it didn't happen — every section ties to the stats digest (numbers, projects, prompts). No generic advice.
- Codex routes almost everything through one `exec` tool, so exec-heavy is normal there — judge read-before-edit, not tool name.
- Some judgments are model-inferred (satisfaction, themes) — the report footer already flags this; don't overclaim.
- Write the report content in the user's language, defaulting to English. Set the analysis `lang` field ("en" | "ru") so the static chrome matches. Keep prose clean, concrete, and free of AI-slop; for Russian, hold it to the humanizer-ru standard.
- The friction section is the point. Each friction gets a concrete, copy-pasteable fix (a CLAUDE.md line, a hook, a habit).
