---
name: codex-reviewer
description: Patterns for using Codex CLI as an automated code reviewer. Covers review prompts, structured output parsing, issue tracking, and configuration. Use when implementing review gates or automated quality checks.
---

# Codex as Code Reviewer

Use OpenAI's Codex CLI to automate code review as a quality gate. This skill covers review prompt design, output parsing, and integration patterns.

## Prerequisites

Codex CLI must be installed and available in PATH:

```bash
which codex  # verify installation
```

## Basic Invocation

```bash
# Execute with prompt from stdin
echo "Review this code..." | codex exec - --sandbox read-only -o output.txt

# Key flags
codex exec - \
  --sandbox read-only \                    # read-only | workspace-write | danger-full-access
  -c 'approval_policy="never"' \           # untrusted | on-failure | on-request | never
  -o /tmp/review-output.txt                # output file (stdout is messy)
```

## Configuration

Store user preferences in `~/.claude/codex/config.json`:

```typescript
interface CodexConfig {
  sandbox?: "read-only" | "workspace-write" | "danger-full-access";
  approval_policy?: "untrusted" | "on-failure" | "on-request" | "never";
  bypass_sandbox?: boolean;      // --dangerously-bypass-approvals-and-sandbox
  extra_args?: string[];         // additional CLI args (DO NOT override -o)
  timeout_seconds?: number;      // default: 1200 (20 min), must be < hook timeout
}
```

**Recommended defaults for review:**
- `sandbox: "read-only"` - reviewer should inspect, not modify
- `approval_policy: "never"` - no human approval needed for read-only
- `timeout_seconds: 1200` - 20 minutes for thorough review (must be < hook timeout, typically 1800s)

## Review Prompt Structure

Structure prompts with the CRITICAL output requirement upfront to prevent malformed responses:

```markdown
# Code Review

## CRITICAL: Required Output Format

Your response MUST end with exactly one of these verdict tags:

<review>APPROVE</review>

OR

<review>REJECT</review>
<issues>
[ISSUE-N] severity: description
</issues>

The <review> tag is MANDATORY. Without it, your review cannot be processed and will be rejected. Do not output status messages like "Checked working directory" - you must complete the full review and output the verdict tag.

---

## Task to Review

Claude claims this task is complete and ready for review:

${taskDescription}

## Git Context

${filesSection}Run these commands to gather context:
- Working directory: run `pwd`
- Repository name: run `basename "$(git rev-parse --show-toplevel)"`
- Current branch: run `git branch --show-current`
- Uncommitted changes: run `git diff --stat`
- Staged changes: run `git diff --cached --stat`
- Recent commits: run `git log --oneline -5 --since="4 hours ago"`

${previousReviewHistory}

## Review Process

1. Understand the task (read referenced files as needed)
2. Review git changes (git diff, git diff --cached, git log)
3. Run verification commands from success criteria if applicable
4. Check ALL requirements - be thorough, not superficial
5. Output your verdict using the REQUIRED format below

## Output Format (MANDATORY)

If approved:
<review>APPROVE</review>
<notes>Optional notes for the record</notes>

If issues found:
<review>REJECT</review>
<resolved>
[ISSUE-1] How you verified this previous issue is now fixed
</resolved>
<issues>
[ISSUE-N] severity: Description of the issue
</issues>
<notes>Optional notes visible to future review cycles</notes>

Rules:
- Severity levels: critical (blocking), major (significant), minor (nice to fix)
- Issue IDs must be unique across all cycles - continue numbering from previous reviews
- <resolved> section: List previous issues verified as fixed (omit if none or first review)
- <notes> section: Optional, visible to future review cycles
- Be thorough - report ALL issues found

Review ${currentCycle}/${maxCycles}. Remember: your response MUST contain <review>APPROVE</review> or <review>REJECT</review>.
```

**Key prompt design decisions:**
- Output requirement at the TOP, not buried at the end
- Explicit anti-pattern warning ("Do not output status messages...")
- Commands as instructions ("run `pwd`") not inline templates
- Repeated reminder at the end

## Output Format Specification

### Verdict Tags

```xml
<!-- Approved - no blocking issues -->
<review>APPROVE</review>
<notes>Optional commentary for the record</notes>

<!-- Rejected - issues require resolution -->
<review>REJECT</review>
<resolved>
[ISSUE-1] Verified: test now passes after fix in auth.ts:45
[ISSUE-3] Verified: error handling added in api.ts:120
</resolved>
<issues>
[ISSUE-4] critical: API endpoint returns 500 on empty input
[ISSUE-5] major: Missing input validation in UserForm component
[ISSUE-6] minor: Typo in error message "recieved" -> "received"
</issues>
<notes>Good progress on previous issues. Focus on input validation.</notes>
```

### Issue Format

```
[ISSUE-{id}] {severity}: {description}
```

- **id**: Unique integer, monotonically increasing across cycles
- **severity**: `critical` | `major` | `minor`
- **description**: Clear, actionable description (can be multi-line)

### Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| `critical` | Blocking bug, security issue, data loss risk | Must fix before approval |
| `major` | Significant functionality gap, poor UX | Should fix before approval |
| `minor` | Code quality, style, minor improvements | Nice to fix, non-blocking |

## Parsing Codex Output

Parse from the END of output to avoid matching echoed examples in the prompt:

```typescript
interface ReviewIssue {
  id: number;
  severity: "critical" | "major" | "minor";
  description: string;
}

interface ResolvedIssue {
  id: number;
  verification: string;
}

interface ReviewResult {
  approved: boolean;
  issues: ReviewIssue[];
  resolved: ResolvedIssue[];
  notes: string | null;
}

function parseCodexOutput(output: string): ReviewResult {
  // Find LAST occurrence of each tag (avoids matching prompt examples)
  const reviewMatches = [...output.matchAll(/<review>\s*(APPROVE|REJECT)\s*<\/review>/gi)];
  const lastReview = reviewMatches.length > 0 ? reviewMatches[reviewMatches.length - 1] : null;
  const verdict = lastReview ? lastReview[1].toUpperCase() : null;

  // Parse notes
  const notesMatches = [...output.matchAll(/<notes>([\s\S]*?)<\/notes>/gi)];
  const lastNotes = notesMatches.length > 0 ? notesMatches[notesMatches.length - 1] : null;
  const notes = lastNotes ? lastNotes[1].trim() : null;

  if (verdict === "APPROVE") {
    return { approved: true, issues: [], resolved: [], notes };
  }

  if (verdict === "REJECT") {
    // Parse issues from last <issues> block
    const issues: ReviewIssue[] = [];
    const issuesMatches = [...output.matchAll(/<issues>([\s\S]*?)<\/issues>/gi)];
    const lastIssuesMatch = issuesMatches.length > 0 ? issuesMatches[issuesMatches.length - 1] : null;
    const issuesBlock = lastIssuesMatch ? lastIssuesMatch[1] : null;

    if (issuesBlock) {
      const issuePattern = /\[ISSUE-(\d+)\]\s*(critical|major|minor):\s*([\s\S]+?)(?=\[ISSUE-|\s*$)/gi;
      for (const match of issuesBlock.matchAll(issuePattern)) {
        issues.push({
          id: parseInt(match[1], 10),
          severity: match[2].toLowerCase() as "critical" | "major" | "minor",
          description: match[3].trim(),
        });
      }
    }

    // Parse resolved from last <resolved> block
    const resolved: ResolvedIssue[] = [];
    const resolvedMatches = [...output.matchAll(/<resolved>([\s\S]*?)<\/resolved>/gi)];
    const lastResolvedMatch = resolvedMatches.length > 0 ? resolvedMatches[resolvedMatches.length - 1] : null;
    const resolvedBlock = lastResolvedMatch ? lastResolvedMatch[1] : null;

    if (resolvedBlock) {
      const resolvedPattern = /\[ISSUE-(\d+)\]\s*([\s\S]+?)(?=\[ISSUE-|\s*$)/gi;
      for (const match of resolvedBlock.matchAll(resolvedPattern)) {
        resolved.push({
          id: parseInt(match[1], 10),
          verification: match[2].trim(),
        });
      }
    }

    // Handle REJECT with no parseable issues - auto-approve to avoid deadlock
    if (issues.length === 0) {
      return {
        approved: true,
        issues: [],
        resolved: [],
        notes: notes
          ? `[AUTO-APPROVED: REJECT with unparseable issues] ${notes}`
          : "[AUTO-APPROVED: REJECT with unparseable issues]",
      };
    }

    return { approved: false, issues, resolved, notes };
  }

  // Unclear response - default to approve
  return { approved: true, issues: [], resolved: [], notes: null };
}
```

## Review History Tracking

Maintain history across review cycles for context:

```typescript
interface ReviewHistoryEntry {
  cycle: number;
  decision: "APPROVE" | "REJECT";
  issues: ReviewIssue[];
  resolved: ResolvedIssue[];
  notes: string | null;
}

function buildReviewHistorySection(history: ReviewHistoryEntry[]): string {
  if (history.length === 0) return "";

  const sections = history.map((entry) => {
    const parts: string[] = [`### Cycle ${entry.cycle}: ${entry.decision}`];

    if (entry.resolved.length > 0) {
      parts.push(`**Resolved:**\n${entry.resolved.map(r =>
        `  - [ISSUE-${r.id}] ✓ ${r.verification}`
      ).join("\n")}`);
    }

    if (entry.issues.length > 0) {
      parts.push(`**Issues:**\n${entry.issues.map(i =>
        `  - [ISSUE-${i.id}] ${i.severity}: ${i.description}`
      ).join("\n")}`);
    }

    if (entry.notes) {
      parts.push(`**Notes:** ${entry.notes}`);
    }

    return parts.join("\n");
  });

  return `## Previous Reviews\n\n${sections.join("\n\n")}\n\n`;
}
```

## Spawning Codex CLI

```typescript
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";

function callCodexReview(
  prompt: string,
  cwd: string,
  config: CodexConfig
): ReviewResult {
  // Check availability
  const which = spawnSync("which", ["codex"], { encoding: "utf-8" });
  if (which.status !== 0) {
    console.error("Codex CLI not found, approving by default");
    return { approved: true, issues: [], resolved: [], notes: null };
  }

  const outputFile = `/tmp/codex-review-${Date.now()}.txt`;
  const args: string[] = ["exec", "-"];  // read from stdin

  if (config.bypass_sandbox) {
    args.push("--dangerously-bypass-approvals-and-sandbox");
  } else {
    args.push("--sandbox", config.sandbox ?? "read-only");
    args.push("-c", `approval_policy="${config.approval_policy ?? "never"}"`);
  }

  args.push("-o", outputFile);

  // WARNING: extra_args can override -o, which breaks output parsing
  // Filter out -o/--output to prevent this, or validate config upstream
  if (Array.isArray(config.extra_args)) {
    args.push(...config.extra_args.filter(a =>
      typeof a === "string" && a !== "-o" && !a.startsWith("--output")
    ));
  }

  // NOTE: timeout must be less than hook timeout (typically 1800s for Claude Code hooks)
  const timeoutMs = (config.timeout_seconds ?? 1200) * 1000;

  const result = spawnSync("codex", args, {
    cwd,
    encoding: "utf-8",
    timeout: timeoutMs,
    maxBuffer: 1024 * 1024,
    input: prompt,
  });

  if (!existsSync(outputFile)) {
    console.error("No output file created");
    return { approved: true, issues: [], resolved: [], notes: null };
  }

  const output = readFileSync(outputFile, "utf-8");
  return parseCodexOutput(output);
}
```

## Error Handling

### Fail Safe, Not Stuck

When errors occur, default to APPROVE to avoid trapping users in infinite loops:

```typescript
try {
  return callCodexReview(prompt, cwd, config);
} catch (e) {
  console.error("Codex review failed:", e);
  // Clean up any state files
  // Default to approve - don't block on review failure
  return { approved: true, issues: [], resolved: [], notes: null };
}
```

### Handle Unclear Responses

```typescript
// REJECT with no parseable issues = auto-approve to prevent deadlock
if (verdict === "REJECT" && issues.length === 0) {
  return {
    approved: true,
    issues: [],
    resolved: [],
    notes: "[AUTO-APPROVED: REJECT with unparseable issues]",
  };
}

// No clear verdict found = approve by default
if (!verdict) {
  return { approved: true, issues: [], resolved: [], notes: null };
}
```

## Feedback Loop Pattern

When review rejects, format structured feedback for the next iteration:

```typescript
function buildFeedbackPrompt(
  result: ReviewResult,
  originalPrompt: string,
  iteration: number,
  maxIterations: number,
  reviewCycle: number,
  maxReviewCycles: number,
  completionPromise: string
): string {
  const issuesList = result.issues
    .map(i => `- [ISSUE-${i.id}] ${i.severity}: ${i.description}`)
    .join("\n");

  const resolvedSection = result.resolved.length > 0
    ? `\n\n**Resolved from previous cycle:**\n${result.resolved
        .map(r => `- [ISSUE-${r.id}] ✓ ${r.verification}`)
        .join("\n")}`
    : "";

  const notesSection = result.notes
    ? `\n\n**Reviewer notes:** ${result.notes}`
    : "";

  return `# Ralph Loop - Iteration ${iteration}/${maxIterations}

## Review Feedback (Cycle ${reviewCycle}/${maxReviewCycles})

Your previous completion was reviewed and requires changes.
${resolvedSection}

**Open Issues:**
${issuesList}
${notesSection}

Address ALL open issues above, then output <promise>${completionPromise}</promise> when truly complete.

---

${originalPrompt}`;
}
```

## Integration Checklist

- [ ] Check Codex CLI availability before calling
- [ ] Use read-only sandbox for review tasks
- [ ] Set appropriate timeout (20+ minutes for complex reviews)
- [ ] Parse from END of output to avoid prompt echo matches
- [ ] Handle REJECT with no issues as auto-approve
- [ ] Handle unclear responses as approve (fail safe)
- [ ] Track issue IDs across cycles (monotonic, never restart)
- [ ] Include git context in review prompt
- [ ] Include previous review history for multi-cycle reviews
- [ ] Clean up temp files and state on errors
- [ ] Log for debugging (errors, timing, verdict)
