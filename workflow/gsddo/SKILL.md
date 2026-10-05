---
name: gsddo
description: "Route freeform text to the right GSD command automatically"
allowed-tools: "Read Bash AskUserQuestion"
category: general-purpose
source_repo: davepoon/buildwithclaude
source_path: "plugins/gsd/skills/do/SKILL.md"
source_url: https://github.com/davepoon/buildwithclaude/blob/HEAD/plugins/gsd/skills/do/SKILL.md
---

<objective>
Analyze freeform natural language input and dispatch to the most appropriate GSD command.

Acts as a smart dispatcher — never does the work itself. Matches intent to the best GSD command using routing rules, confirms the match, then hands off.

Use when you know what you want but don't know which `/gsd-*` command to run.
</objective>

<execution_context>
@${CLAUDE_PLUGIN_ROOT}/workflows/do.md
@${CLAUDE_PLUGIN_ROOT}/references/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the do workflow from @${CLAUDE_PLUGIN_ROOT}/workflows/do.md end-to-end.
Route user intent to the best GSD command and invoke it.
</process>

---

**Source:** [`davepoon/buildwithclaude`](https://github.com/davepoon/buildwithclaude) → `plugins/gsd/skills/do/SKILL.md`
