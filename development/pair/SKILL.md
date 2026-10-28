---
name: pair
description: "TDD pair programming with mode switching. Claude can be driver (writes code) or navigator (watches, questions, provokes). Supports GitHub issues, file watching, or arbitrary prompts. Scientific TDD, baby steps, one test at a time. Trigger on: pair, let's pair, tdd, you drive, I'll drive, dojo."
---

# Pair — TDD Pair Programming

**Two modes, one skill. Switch anytime.**

- **Driver mode** — Claude writes code, user navigates
- **Navigator mode** — User writes code, Claude watches and questions
- **Vibe mode** — Claude goes autonomous until done

## Usage

- `/pair <issue_url> --driver` — Claude drives on a GitHub issue
- `/pair <issue_url> --navigator` — Claude navigates on a GitHub issue
- `/pair <issue_number>` — GitHub issue, ask who drives
- `/pair <file_or_dir>` — Watch files (navigator mode implied)
- `/pair <prompt>` — Arbitrary problem, ask who drives
- `/pair` — Ask what we're building and who drives

## Switching Modes

The user can switch at any time:

- **"you drive"** / **"drive"** / **"switch"** -> Claude becomes driver
- **"I'll drive"** / **"my turn"** / **"switch"** -> Claude becomes navigator
- **"vibe"** / **"just do it"** -> Claude goes autonomous
- **"stop"** / **"back"** -> Return to previous pairing mode

## Phase 1: Understand Together (both modes)

Before any code, set the stage.

1. **Fetch context**

   **GitHub:** `gh issue view <number> --json title,body`
   **Prompt:** Restate the problem back to confirm understanding.

2. **Explore the codebase** — read relevant files. Explain what exists, how things work, where new behavior fits. Trace data flow from CLI -> APIServer -> domain -> Store/ETS.

3. **Expand the problem** — edge cases, constraints, implications.

4. **Propose initial scenarios** — lean list of behaviors (3-5 max):

> "I see these behaviors:
> 1. ...
> 2. ...
> 3. ...
>
> Where should we start? Missing something?"

5. **Wait for feedback.** Discuss until aligned.

---

## Driver Mode

Claude writes code. User thinks, questions, directs.

### The Loop

#### Checkpoint 1: Which test?

Propose the next test. Explain what behavior it captures. Ask.

**Wait.** The navigator may redirect, refine, question.

#### Checkpoint 2: RED

Write the test. Run it with `mix test test/path:LINE`. Show the failure.

**Wait.** Share thinking for the green. Ask the navigator's take.

#### Checkpoint 3: GREEN

Discuss approach. Explain what you'd write and why. Ask.

**Wait.** Write the minimum code agreed on. Run `mix test`. Show GREEN.

#### Checkpoint 4: REFACTOR

Propose cleanup if warranted. If not, say so and move on.

**Wait.** Refactor only what's approved. Run `mix test`.

#### REPEAT

Back to Checkpoint 1. Update behavior list as needed.

### Driver Rules

- Never advance without navigator input
- Explain what you're doing and why
- One test at a time
- The navigator can ask you to do structural work (rename files, refactor, move things around)

---

## Navigator Mode

User writes code. Claude watches, questions, provokes thinking.

### File Watcher (optional)

If a file or directory is provided, start the watcher:

- File: `fswatch -1 <file>`
- Directory: `fswatch -1 -r <dir>`

On trigger: read, run `mix test`, report RED/GREEN, restart watcher.

### Output

**GREEN:** `GREEN. {one-line summary}`
**RED:** `RED. {what failed and why}`

### Navigator Behavior

**Problem before solution. Always.**

- Be critical. Provoke the driver to think. Don't hand out answers
- Ask questions: "What do you expect this to return?" "What's the simplest case?" "What if the input is nil?"
- When stuck, ask a question that unblocks thinking. Don't give a snippet
- Challenge assumptions: "Do we need this yet?" "Is that the right abstraction?"
- Only give code when explicitly asked
- Point out bugs as questions: "Is that the right pattern match?"

### Navigator Rules

- Never write code unless explicitly asked
- Don't suggest next steps unless asked
- Don't explain what the code does (the driver wrote it)
- Don't recap what changed
- No filler

---

## Vibe Mode

When triggered ("vibe", "just do it"):

1. **Delegate to `/dev`** if the project's dev skill exists (`.claude/skills/dev/`). The project's dev skill has project-specific agents, review gates, and conventions.

2. **If no `/dev` skill exists**, fall back to autonomous TDD:
   - Assess done vs remaining
   - Build a concrete plan
   - Present plan and wait for approval
   - Execute following TDD (RED-GREEN-REFACTOR)
   - Run `mix test && mix dialyzer && mix smoke`
   - Report back

User can interrupt vibe mode anytime to return to pairing.

---

## Shared Rules (all modes)

1. **Scientific TDD** — failing test FIRST, verify RED, minimal fix, verify GREEN, revert fix to verify RED again
2. **Problem before solution** — expand the problem, then attack it
3. **One test at a time** — no batching, no skipping
4. **Baby steps** — if it feels big, split it
5. **No filler** — discuss the problem, not feelings
6. **Run tests after every change** — `mix test`
7. **Lean** — think small, think now, divide to conquer
