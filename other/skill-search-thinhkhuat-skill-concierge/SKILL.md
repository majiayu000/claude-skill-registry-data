---
name: skill-search
user-invocable: true
description: Find the right skills for a task before acting. Use at the start of any multi-step or unfamiliar request to retrieve relevant skills by meaning, not name. Triggers when the user asks to build, set up, design, deploy, fix, or automate something and the right skill isn't obvious.
argument-hint: "[task description]"
license: MIT
compatibility: Requires the skill-search MCP server (provides the search_skills tool) registered in Claude Code. See https://github.com/sowhan/skill-search
metadata:
  author: Sowhan Mohammed
  version: 0.1.1
  mcp-server: skill-search
---

# skill-search

Before tackling this task, call the `search_skills` MCP tool with a short query
describing the user's goal. It returns ranked skills by semantic relevance.

Then:
1. Read the returned names + descriptions. Each row also carries `origin` (which harness's
   roots hold the copy) and, when present, `disabled_in`. A row whose `disabled_in` names your
   harness is not a hit. Otherwise: a skill your harness lists is invoked by name; one it does not
   list is loaded with `get_skill(name)` and followed inline.
2. Invoke the genuinely relevant ones by name (e.g. /frontend-design).
3. Ignore low-score results — do not load skills that aren't relevant.
4. If a result looks promising but the description is thin, call `get_skill`
   on it before deciding.

Prefer 2-4 high-relevance skills over loading many. Precision keeps context lean.
