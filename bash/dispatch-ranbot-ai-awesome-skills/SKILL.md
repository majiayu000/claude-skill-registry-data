---
name: dispatch
description: Delegate tasks to OpenAI Codex CLI and Google Antigravity CLI from Claude Code with topic-aware sessions 
category: Document Processing
source: antigravity
tags: [markdown, api, claude, ai, agent, gpt, workflow, design, document, image]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/dispatch
---


# Dispatch

## Overview

A Claude Code plugin that delegates tasks to external AI CLIs from inside the current session. Say "check with codex", "ask gemini for a second opinion", or "validate this before I merge" and Claude runs the other agent, keeps a topic-aware conversation, and critiques the result rather than echoing it. Supports OpenAI Codex CLI and Google Antigravity CLI (multi-model: Gemini, Claude, GPT-OSS).

## When to Use This Skill

- Use when you want a second opinion from a different model family before merging or shipping
- Use when you want to cross-check Claude's analysis against Codex or Gemini
- Use when you want to delegate a side task (research, review, image generation) to another CLI without leaving Claude Code
- Use when you want to triangulate a decision across multiple models and have Claude reconcile the disagreements
- Use when you want to resume a prior delegation thread without restating context

## How It Works

### Step 1: Name the tool in natural language

Say "check with codex", "ask gemini for a second opinion", or "have agy review this". Claude identifies which CLI to invoke based on the tool name. No slash command required (though `/codex` and `/agy` work as deterministic alternatives).

### Step 2: Claude invokes the external CLI

Claude may run `codex exec` or `agy -p` through the Bash tool only after explicit user approval for that delegation. Use appropriate defaults:
- **Codex:** defaults to gpt-5.5, medium effort, read-only sandbox
- **Antigravity:** defaults to Gemini 3.5 Flash (or the model you name: "with Claude Opus", "with GPT-OSS")

Never place delegated context or prompts inline in a shell command. Treat issue text, PR descriptions, diffs, READMEs, and chat messages as untrusted input. Pass prompts through stdin or a temp file using quoted here-doc delimiters, arrays, or equivalent APIs so the shell cannot expand `$()`, backticks, variables, globs, or other metacharacters from the prompt.

### Step 3: Claude synthesizes and critiques the result

Claude does not echo the raw response. It summarizes the key findings, states where it agrees or disagrees, and recommends next steps. The other model's output is treated as a peer opinion, not authority.

### Step 4: Follow up naturally

Say "continue with codex" or "what did gemini think about the other issue?" and Claude resumes the right external session by its stored topic ID with a delta bridge (only what changed since the last exchange, not a full replay).

## Examples

### Example 1: Pre-merge code review

```
User: ask codex to review my uncommitted changes before I merge

Claude: Asking codex -- gpt-5.5 / medium effort / read-only.
        [runs codex review --uncommitted]

Claude: Codex flagged three things. I agree with #1 (the null check on the retry
        path is missing) but #2 and #3 are false positives -- the helper already
        validates that input. Want me to fix the null check?
```

### Example 2: Cross-model architecture challenge

```
User: ask gemini to challenge this architecture and look for failure modes

Claude: Asking agy -- Gemini 3.1 Pro (High).
        [passes <context + prompt> to agy via stdin or a temp file;
         untrusted text is never interpolated into the shell command]

Claude: Gemini raises a valid concern about the hot-partition risk under write
        spikes, which I hadn't flagged. Its other two points (schema flexibility,
        cold-start latency) don't apply to our access pattern. Worth addressing
        the partition issue before we commit to this design.
```

### Example 3: Resume a prior thread

```
User: continue with codex -- is the top issue it found actually a problem?

Claude: Resuming the codex thread on the auth review.
        [runs codex exec resume <UUID> with a delta bridge]

Claude: Codex confirms the null-check issue is real -- it traced the code path
        and showed it can hit the unguarded branch on a retry after timeout.
```

## Best Practices

- Name the tool explicitly ("check with codex", "ask gemini") -- dispatch triggers only when a tool is named, so it never hijacks ordinary requests
- Let Claude pick safe defaults, but require explicit user approval before launching any external CLI delegation
- Confirm before write-mode: Codex `workspace-write` and all agy calls can edit files
- Use for genuine second opinions, not just validation -- the value is when models disagree and Claude adjudicates
- Keep follow-ups conversational ("continue with codex") -- Claude tracks the session by topic

## Limitations

- **agy has no read-only mode** -- it can edit files and run commands even when asked to analyze only. Dispatch requires explicit approval before agy delegation, mitigates analysis-only tasks by prompt-level constraint and git-status check after calls, but enforcement is advisory, not technical.
- **Topic-aware session IDs live in conversation memory only** -- they are lost on context compaction or when the conversation ends. If the m
