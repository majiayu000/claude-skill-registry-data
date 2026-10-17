---
name: prompt-injection-detector
description: "Prompt injection vulnerability scanner: statically detects LLM API call sites, traces untrusted data flowing into system prompts and user messages, and classifies injection countermeasures (none/weak/adequate). Read-only. Trigger: /prompt-inspect"
trigger: /prompt-inspect
---

## What this is for

Prompt injection is the OWASP #1 LLM vulnerability. Every place where
user-controlled data meets an LLM prompt is a potential injection vector.
Unlike SQL injection, there is no universal escaping function - defense is
architectural: separate instructions from data, add injection guards,
validate inputs.

This skill finds every LLM API call site in your codebase, traces what data
flows into the prompt, and checks for countermeasures.

**Audience:** Senior > Vibe
- Seniors use it as a pre-deployment security review for AI features.
- Vibe-coders get a systematic check that their LLM integrations aren't
  trivially jailbreakable.

### Trigger: `/prompt-inspect`

## PROTECTION RULE - never `~/.claude/`

Read-only skill.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
If invoked with `-help` or `-h`, print the usage block below and stop.

### Step 2 - Confirm `-ProjectDir`
If not provided, prompt the user. Print: `Prompt injection scan on <path> ...`

### Step 3 - Run Collector
```powershell
& .\scripts\prompt-scan.ps1 -ProjectDir "<path>"
```

### Step 4 - Validate each finding
For each finding:
1. Read the context block
2. Confirm the API call is genuinely an LLM endpoint
3. Trace the variable source: is it truly user-controlled?
4. Assess the guard: is it effective or cosmetic?

### Step 5 - Architecture review
- Check if system prompt and user message are clearly separated
- Check if user content is wrapped in delimiters
- Check for input validation before prompt construction

### Step 6 - Generate report
Write `prompt-injection-report.md` to the working directory.

## Usage

```powershell
& .\scripts\prompt-scan.ps1 -ProjectDir "C:\Projects\my-ai-app"
& .\scripts\prompt-scan.ps1 -ProjectDir "C:\Projects\my-ai-app" -Exclude "test,spec,fixtures"
```
