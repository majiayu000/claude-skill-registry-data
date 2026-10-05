---
name: ask-me-questions
description: >-
  Systematic requirements discovery through multi-round questioning before
  taking action. Use when the user explicitly asks — "ask me questions",
  "ask me first", "interview me", "gather requirements", "understand what
  I need" — or when a request is genuinely ambiguous: multiple plausible
  interpretations leading to materially different implementations, and the
  right one isn't discoverable from the code or context. Do NOT use for
  clear requests, however large. The deliberate inverse of `yolo`.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
---

# Ask Me Questions

Understand before you act. Ask targeted questions in focused multi-round conversations
before proceeding with any task.

**Asking mechanism (portability).** Where your harness has a structured question tool (e.g.
Claude Code's `AskUserQuestion`), use it — the multiple-choice form gets far better answers
than open prose. Where it doesn't, ask in plain text: numbered questions, each with 2-4
labelled options and a recommended default. Everything below applies either way.

## Rules

1. **Never jump to solutions.** When this skill triggers, questioning comes FIRST.
2. **Never ask what you can verify.** Read the code, run the command, check the
   docs first. Ask only about intent, preferences, priorities, and trade-offs
   the code can't reveal.
3. **Offer options, not open prose.** Every question comes with concrete choices the user can
   pick from, plus your recommendation — never a bare "what do you want?".
4. **Max 4 questions per round.** Make each one count.
5. **Adapt rounds to complexity:**
   - Simple (single-file change, config tweak): 1 round (2-4 questions)
   - Medium (feature, multi-file change): 2 rounds (4-8 questions)
   - Complex (architecture, new system): 2-3 rounds (6-12 questions)
6. **Stop questioning when:** you have enough clarity to act confidently. Don't over-ask.
7. **Unattended runs don't block.** If running autonomously (background, cron,
   headless) where no one can answer, skip questioning: state your assumptions
   explicitly and proceed.

## Questioning Workflow

### Round 1: Scope & Intent

Establish what the user actually wants and why. These questions cut through ambiguity fast.

Focus areas:
- **What:** What specific outcome do they want? What does "done" look like?
- **Why:** What problem does this solve? What triggered this request?
- **Constraints:** Are there hard requirements (tech stack, timeline, compatibility)?
- **Scope:** What's explicitly OUT of scope?

Question design tips:
- Lead with the most disambiguating question — the one whose answer changes everything
- Use options with descriptions to surface hidden assumptions
- Put the recommended/most-common option first
- Use `multiSelect: true` when choices aren't mutually exclusive

Example:
```
question: "What should happen when the export fails midway?"
header: "Errors"
options:
  - label: "Retry from checkpoint"
    description: "Resume where it left off. Requires tracking progress state."
  - label: "Retry from scratch"
    description: "Simple but may be slow for large exports."
  - label: "Fail with partial output"
    description: "Return whatever was exported so far."
```

### Round 2+: Targeted Follow-ups

Based on Round 1 answers, ask about:
- **Edge cases** revealed by their choices
- **Trade-offs** between approaches they've implied
- **Specifics** that their answers left open (e.g., they said "fast" — how fast?)
- **Pattern conflicts** — follow existing codebase patterns by default without asking.
  Only ask when the codebase shows two conflicting patterns AND the choice
  materially affects the outcome.

Skip Round 2 if Round 1 answers were clear and complete.

### After Questioning: Proceed

Once you have sufficient clarity:
1. Briefly summarize what you understood (2-3 sentences in plain text, NOT a file)
2. Proceed directly with the task — no permission-asking, no "shall I proceed?"

## Writing Good Questions

### Option Design

Each option should represent a genuinely different path, not slight variations:

**Good options** (meaningfully different outcomes):
- "Server-side validation" vs "Client-side validation" vs "Both"
- "Add to existing table" vs "Create new table" vs "Use a JSON field"

**Bad options** (cosmetic differences):
- "Use camelCase" vs "Use snake_case" — too trivial for a question
- "Option A" vs "Option B" — labels must be self-explanatory

### Header Tips

Headers appear as chips/tags. Keep under 12 chars:
- Good: `"Scope"`, `"Auth"`, `"Data model"`, `"Error flow"`, `"API style"`
- Bad: `"Authentication method"`, `"How should we handle errors"`

### When to Use multiSelect

Use `multiSelect: true` for:
- Feature selection ("Which of these should we support?")
- Capability flags ("What constraints apply?")
- Inclusive lists ("Which environments need this?")

Keep `multiSelect: false` (default) for:
- Mutually exclusive approaches
- Architecture decisions
- Single-choice trade-offs
