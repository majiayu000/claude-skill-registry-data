---
name: thrunt-do
description: Route freeform text to the right hunt or THRUNT command automatically
argument-hint: "<description of what you want to do>"
allowed-tools: Read, Bash, AskUserQuestion
---

<objective>
Analyze freeform natural language input and dispatch to the most appropriate hunt or THRUNT command.

Acts as a smart dispatcher — never does the work itself. Matches intent to the best command using routing rules, confirms the match, then hands off.

Use when you know what you want but don't know which `/thrunt:*` or `/hunt:*` command to run.
</objective>

<execution_context>
@.github/thrunt-god/workflows/do.md
@.github/thrunt-god/references/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the do workflow from @.github/thrunt-god/workflows/do.md end-to-end.
Route user intent to the best hunt or THRUNT command and invoke it.
</process>
