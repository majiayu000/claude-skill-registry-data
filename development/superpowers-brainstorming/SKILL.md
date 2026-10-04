---
name: superpowers-brainstorming
description: 'Use before writing any code, scaffolding, or taking implementation action
  — explore intent, requirements, and design through structured Socratic questioning,
  trade-off analysis, and formal spec writing. Purpose: Replace assumptions with verified
  understanding by asking one clarifying question per message, proposing 2-3 approaches
  with explicit trade-offs, getting approval on each design section, and writing a
  formal spec before any code is written. Key capabilities: Socratic questioning to
  expose unknown unknowns; explicit trade-off framing with AI effort compression (human
  time vs. AI time) so the human partner can calibrate scope; "Boil the Lake" — completeness
  is cheap when AI handles the boilerplate; Search Before Building to check existing
  patterns before reasoning from first principles; spec document written to disk and
  reviewed by a subagent before proceeding. When to trigger: before implementing anything
  that touches new code or changes existing behavior; when requirements are ambiguous;
  during the Explore phase of a new feature or refactor; before scaffolding a new
  module or service; when the user says build X without a clear design; before acting
  on a vague or high-level request. Also for: scope reduction (unbundle); technical
  debt discussions where intent is unclear; spike investigations for high-uncertainty
  areas; onboarding new contributors to a codebase.'
---

# Brainstorming Skill

**Purpose:** Explore user intent, requirements, and design before any implementation begins.

## The Iron Rule

**HARD-GATE:** Do NOT invoke any implementation skill, write code, scaffold, or take implementation action until user approves the design.

## Workflow

### Step 1: Explore Project Context
Read existing files, docs, recent commits, and any relevant project state to understand the landscape.

Also load these project-level phase files if they exist:
- `STATE.md` — cross-session decisions, blockers, current state
- `ROADMAP.md` — phases, milestones, progress
- `REQUIREMENTS.md` — scoped requirements with phase traceability
- `{phase}-CONTEXT.md` — implementation decisions for the current phase

These files live in the project root alongside PROJECT.md. They capture context
that should persist across sessions.

### Step 2: Visual Companion (Optional)
Offer once (own message) if visual questions are expected. If accepted, decide per-question whether to use browser vs. terminal based on whether the question would be better understood by seeing vs. reading.

### Step 3: Clarifying Questions
Ask **one question per message**. Refine understanding through Socratic questioning. Explore alternatives and trade-offs.

### Step 4: Propose Approaches
Present 2-3 approaches with trade-offs and a recommendation. Get approval after each section.

### Step 5: Present Design in Sections
Scale each design section to its complexity. Get explicit approval after each section before proceeding.

### Step 6: Write Design Document
Save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit. Include:
- Problem statement
- Proposed approach
- Key decisions and rationale
- File structure
- API contracts (if applicable)

### Step 7: Spec Review Loop
Dispatch a `spec-document-reviewer` subagent to review the written spec. Fix issues. Max 3 iterations, then surface to human for guidance.

### Step 8: User Reviews Written Spec
User reviews the written spec before proceeding.

### Step 9: Invoke Writing Plans
**Terminal state:** invoke `superpowers-writing-plans` — the only skill to invoke at the end.

## Anti-Pattern

> "This Is Too Simple To Need A Design" — every project goes through this process regardless of perceived simplicity.

## Boil the Lake

When presenting approaches or options, **always recommend the complete implementation** when AI makes the marginal cost near-zero.

**Lake vs ocean:** A lake is boilable (100% coverage, full feature, all edge cases). An ocean is not (system rewrites, multi-quarter migrations).

Show both effort scales: human time vs AI time.

**Compression reference:**
| Task | Human | AI | Compression |
|------|-------|-----|-------------|
| Boilerplate | 2 days | 15 min | ~100x |
| Tests | 1 day | 15 min | ~50x |
| Feature | 1 week | 30 min | ~30x |
| Bug fix | 4 hours | 15 min | ~20x |
| Architecture | 2 days | 4 hours | ~5x |
| Research | 1 day | 3 hours | ~3x |

**Anti-patterns to avoid:**
- Recommending shortcuts when complete costs minutes more
- Deferring tests to follow-up PR
- Quoting only human effort ("This would take 2 weeks")

## Search Before Building

Before proposing solutions, check what exists. Three layers:

- **Layer 1** (tried and true): Standard patterns already in the ecosystem
- **Layer 2** (new and popular): Search for current best practices — but scrutinize them
- **Layer 3** (first principles): Your original reasoning about the specific problem

When Layer 3 reasoning reveals conventional wisdom is wrong, name it:
```
EUREKA: Everyone does X because [assumption]. But [evidence] shows Y is better.
```

Log eureka moments to project memory for future reference.

## Integration

- **Required sub-skill:** `superpowers-writing-plans` — invoked at the end
- **Called by:** `superpowers-using-superpowers`
- **Creates:** design document at `docs/superpowers/specs/`
