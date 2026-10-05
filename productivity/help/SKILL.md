---
name: ha:help
description: "Recommend the right /ha: command for planning, review, debug, submit, or test tasks. Use when \"which command\", \"what should I use\", or \"how do I\". NOT for /help."
argument-hint: "[description of what you want to do]"
effort: low
---

# Plugin Help — Interactive Command Advisor

Helps users find the right command, skill, or agent for their situation.

## Usage

```
/ha:help                          # Analyze context, suggest commands
/ha:help how do I debug this?     # Route to /ha:investigate
/ha:help add a new feature        # Route to /ha:plan -> /ha:work
```

## Arguments

- `$ARGUMENTS` — optional description of what the user wants to do
- Empty = analyze current context (git status, existing plans, file patterns)

## Execution Flow

### Step 1: Gather Context

If `$ARGUMENTS` is non-empty, use it as primary signal.

Always gather ambient context (run in parallel):

1. Check for existing plans: use Glob on `.claude/plans/*/plan.md` — active work in progress?
2. Check git status: uncommitted changes? which files?
3. Check for solution docs: use Glob on `.claude/solutions/**/*.md` — prior knowledge?

### Step 2: Classify Intent

Read `${CLAUDE_SKILL_DIR}/references/tool-catalog.md` for the full routing table.

Map the user's situation to one of these categories:

| Category | Signals | Primary Commands |
|----------|---------|-----------------|
| **Starting out** | No plans, new to plugin | `/ha:intro` |
| **Ideation** | "explore", "brainstorm", "not sure", "how to approach", "vague idea" | `/ha:brainstorm` |
| **New feature** | "add", "build", "implement", multi-file | `/ha:plan` → `/ha:work` |
| **Quick change** | Single file, <50 lines, "fix typo" | `/ha:quick` |
| **Bug** | Error, stack trace, "broken", "failing" | `/ha:investigate` |
| **Review** | "check", "review", PR ready | `/ha:review` |
| **Performance** | "slow", "blocking I/O", "memory", "event loop" | `/ha:perf`, `/ha:blocking-io-check`, `/ha:lit-render-audit` |
| **Research** | "how to", "best practice", "evaluate lib" | `/ha:research` |
| **Resume work** | Existing plan with unchecked tasks | `/ha:work --continue` |
| **Post-fix** | "that worked", solved a hard bug | `/ha:compound` |
| **Full cycle** | Large feature, new domain area | `/ha:full` |
| **Project health** | "audit", "tech debt", "overall quality" | `/ha:audit`, `/ha:techdebt` |
| **Dep update audit** | "audit deps", "supply chain", "after a requirements bump", "review manifest requirements PR" | `/ha:deps-audit` |
| **Manual dep vetting** | "vet this package", "approve dep", "trust ledger", "after /ha:deps-audit findings" | `/ha:deps-vet` |
| **Submit a PR** | "submit", "open a PR", "ready for core", "breaking change" | `/ha:verify` then `/ha:submit` |
| **Permissions** | "too many prompts", "allow", "permission fatigue" | `/ha:permissions` |
| **Returning after time off** | "what did I miss", "back from vacation", "catch up", "what changed while I was out" | `/catchup` (companion plugin, separate install) |

### Step 3: Respond or Clarify

**If high confidence** (clear match to one category):
Present the recommendation with:

- The command to run (with exact syntax)
- One-line explanation of what it does
- What artifacts it creates (if any)
- Suggested next step after it completes

**If medium confidence** (2-3 possible matches):
Use `AskUserQuestion` with the top options, each with a one-line explanation.

**If low confidence** (vague or no signal):
Ask ONE focused clarifying question. Examples:

- "Are you starting something new or continuing existing work?"
- "Is this a bug fix or a new feature?"
- "How many files do you expect to change?"

Then recommend based on the answer.

### Step 4: Offer Follow-up

After recommending, always add:

- "Run `/ha:help` anytime to get routing advice"
- If they seem new: "Try `/ha:intro` for a full plugin walkthrough"

## Iron Laws

1. **ONE recommendation** — don't dump the full catalog, pick the best match
2. **MAX ONE clarifying question** — don't interrogate, make your best guess
3. **Show exact syntax** — `/ha:plan Add a new cloud integration` not just "use the plan command"
4. **Context over keywords** — existing plans + git state matter more than word matching
5. **NEVER block** — if user already knows what they want, DO NOT redirect

## Integration

- Complements `intent-detection` (auto-trigger) with explicit invocation
- References same routing logic but adds interactive clarification
- Can recommend `/ha:intro` for onboarding
