---
name: iterate
description: Fast iterative development loop. Investigate, implement, review, repeat. Optimized for UI/UX work. Invoke with /iterate followed by what you want done.
---

# Iterate — Fast Development Loop

## Overview
Rapid iterative development skill. Takes a request, investigates just enough to act, implements via subagent, reviews for consistency via another subagent, and reports back concisely. Optimized for UI/UX work and quick successive changes.

## Principles
- **Action over analysis.** Do first, refine after. Ship something in the first pass.
- **Minimal questions.** Only ask when truly ambiguous (multiple valid interpretations). If one interpretation is clearly more likely, go with it.
- **State tracking.** Maintain a running log of changes across iterations so the user never has to repeat context.
- **Simple fixes.** No over-engineering. No tests unless asked. No abstractions for single-use logic.
- **UX focus.** When working on UI, prioritize user experience — spacing, alignment, readability, interaction feedback, accessibility basics.

## Workflow

### Step 1: Understand the Request

Read the user's instruction after `/iterate`. Determine:
- **What** needs to change (component, behavior, style, layout, etc.)
- **Where** it likely lives (use Glob/Grep to locate quickly)

If the request is clear enough to act on (>70% confident), skip to Step 2.
If genuinely ambiguous, ask **one** focused clarifying question — never more than one at a time.

### Step 2: Plan (Main Agent — Brief)

Produce a short internal plan (2-5 bullets max). Do NOT present this to the user as a proposal to approve. Just state what you're about to do in 1-2 sentences, then do it.

Format:
```
Doing: [1-2 sentence summary of the change]
```

### Step 3: Implement (Subagent — Implementer)

Dispatch a subagent to make the changes. The implementer subagent prompt MUST include:
- The exact files to modify (with paths)
- What to change and why
- Current relevant code context (paste key snippets or line ranges)
- Any constraints (keep consistent with existing patterns, don't break X)

The implementer makes the edits directly. No dry runs, no proposals.

### Step 4: Review (Subagent — Consistency Reviewer)

Dispatch a review subagent that checks:
- **Code consistency**: Does the change match surrounding code style, naming, patterns?
- **UX quality**: If UI work — does spacing, alignment, color usage, interaction look right?
- **No regressions**: Did the change accidentally break adjacent functionality?
- **Simplicity**: Is this the simplest way to achieve the goal?

The reviewer either approves or returns specific fixes (not suggestions — concrete edits).
If fixes are needed, the reviewer applies them directly.

### Step 5: Report (Main Agent)

Give the user a concise summary:
```
Done: [what changed]
Files: [list of modified files]
```

If the reviewer made additional fixes, mention them briefly.

### Step 6: Update State

Maintain a running state of this iteration session. Track:
- Changes made (file + what changed)
- Current state of the feature/component being worked on
- Any decisions made along the way

This state is kept in conversation context (not written to disk) so subsequent `/iterate` calls in the same session build on prior work without re-investigating.

## Subagent Delegation Rules

- **Main agent** plans and coordinates. It reads code to understand context but does NOT edit files directly.
- **Implementer subagent** receives precise instructions and makes all edits.
- **Reviewer subagent** checks consistency and applies fixes if needed. Runs AFTER implementer completes.
- Never run implementer and reviewer in parallel — reviewer needs to see implementer's output.
- If the reviewer finds issues, it fixes them directly rather than bouncing back to the implementer.

## State Tracking Format (Internal)

Keep this updated in your working memory across iterations:

```
## Iteration State
- Working on: [feature/component]
- Files touched: [list]
- Changes so far:
  1. [iteration 1 summary]
  2. [iteration 2 summary]
- Current status: [what's done, what's pending]
- Decisions: [any choices made that affect future iterations]
```

## UX Guidelines (When Doing UI Work)

- Consistent spacing — use the project's existing spacing scale
- Visual hierarchy — headings, labels, and content should have clear size/weight differentiation
- Interactive elements need hover/focus/active states
- Error states and empty states matter — handle them
- Animations should be subtle (150-300ms) unless the project uses different conventions
- Mobile-first if the project supports responsive layouts
- Match existing component patterns before creating new ones

## Guardrails
- No tests unless explicitly asked
- No documentation files unless explicitly asked
- No refactoring beyond the scope of the request
- No new abstractions for single-use code
- No type annotations or comments on unchanged code
- If the user says "undo" or "revert", revert the last iteration's changes
- If the user says "try again" or "different approach", redo the last iteration differently

## Anti-Patterns to Avoid
- Asking multiple questions before starting
- Presenting a plan and waiting for approval (just state and do)
- Over-investigating when the change is straightforward
- Adding error handling for impossible scenarios
- Creating utility functions for one-time operations
- Touching files unrelated to the request

## Example Flow

User: `/iterate make the sidebar nav items have more padding and a hover effect`

```
Doing: Adding padding and hover effect to sidebar nav items.
```

→ Subagent investigates, finds sidebar component, adds padding + hover styles
→ Reviewer confirms consistency with existing hover patterns in the app
→ Main agent reports:

```
Done: Added 12px vertical / 16px horizontal padding to sidebar nav items
      and a subtle background hover effect matching the existing button hovers.
Files: src/components/Sidebar/Sidebar.module.css
```

User: `/iterate actually make the hover a bit more prominent`

→ Already knows the file and current state, immediately adjusts.
