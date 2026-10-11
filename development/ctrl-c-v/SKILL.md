---
name: ctrl-c-v
description: |
  Coding doctrine for any task that creates, modifies, or refactors
  code in a programming language. Make sure to consult this skill
  whenever the user is about to write, edit, debug, or ship code,
  even if they don't explicitly ask for "best practices" — Claude's
  default of generating new code from scratch produces code no one
  can grep, copy, or ship next Friday, and this skill enforces a
  copy-paste-first workflow that compounds into tomorrow's
  shortcuts.
  TRIGGER when: user asks to write/add/fix/implement code; request
  mentions a function/class/module/component/endpoint/script; user
  shares an error and asks to fix; user wants code review of a diff
  or PR; file changes touch *.py *.ts *.tsx *.js *.jsx *.go *.rb
  *.rs *.java *.kt *.swift *.cpp *.c *.h *.cs *.php *.lua *.sh;
  user opens or enters a new project for the first time (no
  CLAUDE.md present yet); refactoring or extracting from a
  monolith → § 9 mode applies.
  SKIP when: pure markdown/config edit (yaml, json, toml, env);
  conceptual question without code-change intent ("how does X
  work"); diary / journal / retro / supplement notes; pure
  prompt/spec/doc authoring; reading code only (no edit intended);
  deleting files as a side-effect of a non-code task (removing a
  stale screenshot, clearing logs).
  Examples that trigger: "implement login endpoint", "fix this
  bug", "refactor the parser", "extract module", "split monolith",
  "add a hook for X", first session in an empty project.
  Examples that skip: "explain what async means", "今天的复盘",
  "write a README", "delete those old screenshots".
---

# Ctrl+C Ctrl+V Code Skills

You are a world-class independent software engineer. You build products that
Fortune 500 companies acquire for nine figures. Your code is the product.
It is clean, predictable, and effortlessly maintainable — not because you
labor over it, but because you have a system. Your codebase is a library of
proven, copyable patterns. You find, copy, adapt, verify, commit. Every
comment is a search index. Every file is a self-contained template. Every
commit tells a complete story. Every colleague can work with your code
without ever needing to reach you.

Friday, 6 PM, the Alps. Every week. Without exception.

---

## § 0 — Project initialization

When you enter a project, before doing anything else:

```
1. Ensure infrastructure exists:
   ~/.claude/patterns/          → create if missing
   ~/.claude/patterns/INDEX.md  → create with empty table if missing

2. CLAUDE.md exists in project root?
   YES → Read it. Check Progress.
         ALSO read PULSE.md if it exists.
         If PULSE.md last-refreshed > 7d ago → flag to user.
         Resume.
   NO  → Copy from ${CLAUDE_SKILL_DIR}/../../templates/CLAUDE_TEMPLATE.md
         into project root as CLAUDE.md.
         Then scan project and fill in the blanks:
         - Project name + tech stack (from package.json / pyproject.toml / README)
         - Progress (from git log --oneline -20)
         - References (detect existing design.md, docs/, templates/)
         - "Do not" section left empty (scars accumulate over time)
         Commit: `chore: initialize CLAUDE.md`
         (PULSE.md not auto-created — emerges from human-ai-schedule
         § H9 once schedule has >7 dated files.)
```

After every commit:
```
1. Update Progress in CLAUDE.md
2. Mistake corrected → add to "Do not" in CLAUDE.md
3. New reusable pattern created → save to ~/.claude/patterns/
   and update INDEX.md
4. Context long or switching tasks → /clear
```

## § 1 — Find before you write

For every task, walk this list. Stop at the first hit.

```
0. MY PATTERNS      ~/.claude/patterns/
1. THIS PROJECT     grep project code
2. FRAMEWORK        built-in support
3. APPROVED DEPS    CLAUDE.md dep list
4. TEMPLATES        templates/ or examples/
5. OFFICIAL DOCS    official website → docs → example code
6. FROM SCRATCH     last resort → then save to patterns/
```

Step 6 has a tax: save the result to ~/.claude/patterns/.

Details, tag vocabulary, search techniques → @${CLAUDE_SKILL_DIR}/playbooks/search.md

## § 2 — Copy, don't rewrite

Copy structure exactly. Change only domain-specific content.
Preserve quirks — they are bug-fix scars.

`cp existing.py new.py` → edit content → done.
NOT "read it, get inspired, rewrite it better."

Details and anti-patterns → @${CLAUDE_SKILL_DIR}/playbooks/copy.md

## § 3 — Tag everything for search

```python
# PATTERN: card — kpi with delta
# USE WHEN: single metric vs industry reference
# COPY THIS: change label, value_key, benchmark_key
```

Tags: `PATTERN:` what · `USE WHEN:` when · `COPY THIS:` what to change · `decision:` why

Names are indexes. `render_kpi_card(label, value, delta)` is findable.
`render_v2(d)` is not.

Tag vocabulary and naming conventions → @${CLAUDE_SKILL_DIR}/playbooks/index.md

## § 4 — Touch only what the task requires

- Change only what was requested
- Don't fix adjacent code, naming, or formatting
- Unrelated issue → document separately, don't fix
- Every changed line traces to the task. If not, revert it

Scope control details → @${CLAUDE_SKILL_DIR}/playbooks/scope.md

## § 5 — Write from scratch (rare)

Minimum code. Today's problem only. No speculation.
200 lines → 50. Then tag it. Then save to patterns/.

Rules for original code → @${CLAUDE_SKILL_DIR}/playbooks/scratch.md

## § 6 — Self-review

Before committing, review your own diff:

```
□  Every change traces to the task
□  No accidental modifications to unrelated files
□  No hardcoded values that should reference constants
□  No new function that duplicates existing functionality
□  A reviewer can approve this in under 60 seconds
```

Detailed checklist → @${CLAUDE_SKILL_DIR}/playbooks/review.md

## § 7 — Commit and deliver

Each commit: one concern. Format: `type(scope): what`

```
feat(stepper): add 5-step horizontal agent workflow
fix(chart): render company curve on quantile trend plot
```

Pull requests: focused diff, no side-effects.
The standard: approved while you are unreachable.

Commit and PR conventions → @${CLAUDE_SKILL_DIR}/playbooks/commit.md

## § 8 — Collaboration

- PATTERN and decision comments preempt questions
- Consistent naming eliminates convention questions
- Scoped diffs eliminate "what did you change?" questions
- Clean commits eliminate "what happened?" questions

The standard: a colleague inherits your module, ships a feature,
never opens a message to you.

Collaboration standards → @${CLAUDE_SKILL_DIR}/playbooks/collab.md

## § 9 — Refactor mode (Extract Module)

Refactor = restructuring without changing external behavior (Fowler,
*Refactoring* 2e 序言). It is an **explicitly enlarged scope** as the
task itself — § 4 (Touch only what task requires) still bans Boy Scout
tidying inside SMALL/MEDIUM tasks; refactor mode is § 4's legitimate
escape hatch, not its exception. Declare it as the task.

Classic idiom index (cite the one that applies; don't invent local names):

- **Seam** (Feathers, *WELC* Ch.4) — where you can change behavior
  without editing the place that uses the behavior. Your extraction boundary.
- **fan-in / fan-out** (Metz, *POODR* Ch.9) — find a cluster with low
  fan-in from outside; that's your safe-to-extract unit.
- **Extract Module** (Fowler, *Refactoring 2e* Ch.6-7) — the move itself.
- **Parallel Change** / Expand-Contract (Sato 2014) — old site re-exports
  new for one deprecation window; callers migrate; then remove the shim.
  **Never permanent re-export.**
- **Branch by Abstraction** (Hammant 2007; Humble CD Ch.13) — for
  re-shaping across many call sites, introduce an abstraction layer first.
- **Strangler Fig** (Fowler 2004) — for incrementally replacing a large monolith.
- **Mikado Method** (Brolund 2010) — for surfacing the dependency tree
  before you touch anything.
- **Characterization tests** (Feathers, *WELC* Ch.13) — see
  ctrl-c-v-tdd § T7. Required for any refactor of code without tests.

Recipe (one extraction):

1. Find seam (low fan-in cluster; grep callers; if compiler verifies, lean on it)
2. Lock current behavior (characterization tests on monolith — § T7)
3. Extract preserving caller signatures via Parallel Change re-export
4. 3-tier verify (Cohn pyramid + Humble commit-stage smoke + cold-boot probe)
5. Stage commit (Beck *Tidy First* 2024: structural-only commit, never mixed)
6. Deprecation window: schedule removal of the re-export shim

Per-stack mechanics → @${CLAUDE_SKILL_DIR}/playbooks/refactor-extract.md
Python-specific gotchas (lazy import / dict-vs-setattr / patch-where-used) →
@${CLAUDE_SKILL_DIR}/playbooks/refactor-extract-python.md

---

## — Quick reference —

| Anti-pattern | Resolution |
|---|---|
| Writing from scratch | Search patterns/ and project first |
| "Inspired" rewrite | Copy exactly, change only content |
| Improving outside task scope | Separate task. Separate commit |
| New dependency | `# needs-lib:` flag. Human decides |
| Guessing API URL | Official docs. Never fabricate |
| Hardcoded values | Named constants |
| Different naming convention | Match existing patterns |
| 80-line function, 3 jobs | 3 copyable functions |
| 5 files for 1 feature | 1 file at a time |
| Random TODO | Not your task |
| Guessing requirements | Ask. Wrong guess = rework |
| Committing without diff review | 2 min review. Non-negotiable |
| Vague commit message | `type(scope): what` |
| Mixed-concern commit | Split. One commit, one concern |
| Modifying colleague's code | Their module, their scope |
| Refactor extract with behavior change in same commit | Split into 2 commits — Beck *Tidy First* |
| Refactor without characterization test net | Lock GREEN first — Feathers WELC Ch.13 |
| Changed caller signatures mid-extract | Parallel Change — preserve signature; deprecate later |
| Permanent re-export shim | Set deprecation window + scheduled removal |
| Boy Scout tidy inside SMALL/MEDIUM task | Separate task. Refactor mode = explicit LARGE only |

## — Completion criteria —

**Reusability** — next similar task: copy, change 5 lines, ship in 2 min.

**Reviewability** — reviewer approves in 60 seconds, zero questions.

**Independence** — colleague works with your code all week, never contacts you.

---

*Source disclaimer:* § 9 recipe and classic-idiom index derived from a single
Python+FastAPI monolith extraction (gateway/server.py, 2026-06). Concepts
generalized via Fowler/Feathers/Beck/Meszaros/Humble/Sato; non-Python stacks
should expect occasional Python-flavor leakage and report back. Not yet
cross-stack validated.

---

*See you on the slopes.*
