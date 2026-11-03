---
name: ai-prompt-review
description: Review one prompt for an AI feature — unclear or conflicting instructions, missing context, gaps in the output format, missing refusal rules, and places where user input could override instructions — and return a rewritten version with the changes listed. Use when a team has a prompt and wants it checked before it ships. Not for designing a prompt from scratch; see /ai-prompt-design.
metadata:
  argument-hint: "<prompt or file> [project]"
---

# Prompt review

Review the prompt in "$ARGUMENTS" and return a better one.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The prompt: pasted, or a file path. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ai/`. With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, read none and continue.

Read `.singularskills/ai/<project>/01-define.md` for the job and failure modes and `.singularskills/ai/<project>/03-prompt.md` for the agreed design, when they exist.

## Process

1. **Restate the job** the prompt is for in one sentence; if the prompt does not make it clear, that is the first finding.

2. **Check each part**, as `references/prompt-and-context.md` describes:
   - instructions that are unclear, conflict with each other, or are buried
   - context the model needs but is not given, or is given but not delimited
   - the output format: missing, vague, or not checkable by code
   - refusal and uncertainty: what the model does when the answer is not in the context
   - untrusted input (the user's message, retrieved documents, tool results) that is not marked as data, so it could override the instructions
   - examples: missing, misleading, or all of one kind
   - failure modes from `01-define.md` the prompt does not address

3. **Rewrite the prompt,** keeping the team's wording where it works and changing only what a finding requires.

4. **List the changes**, each tied to its finding, and the ones to evaluate first.

## Output

In chat: the findings, most important first; the rewritten prompt; and the change list. Remind the user to give the new version a number and re-run its evaluation before it ships. This skill writes no file.
