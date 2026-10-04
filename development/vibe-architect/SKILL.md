---
name: vibe-architect
description: >
  Architecture planning workflow for establishing code structure, patterns, and principles
  before any code is written. Runs after brainstorm: and before new: on every project.
  Triggers on "architect:" prefix, "plan the architecture", "architect this",
  "how should we structure this", "what patterns should we use".
  Runs on every project — architecture is never skipped (it can proceed without
  BRIEF.md by asking the stack questions directly, but the architecture step itself
  is not optional).
  Reads BRIEF.md stack decisions and confirms them explicitly before asking any questions —
  prevents scaffolding with wrong framework (e.g. Next.js when React+Vite is specified).
  Produces ARCHITECTURE.md from canonical template — structurally consistent so
  review:, fix-bug:, and add-feature: can parse it reliably every session.
  review: uses ARCHITECTURE.md as its primary reference for drift detection.
  Handles gracefully if BRIEF.md is missing. Detects existing ARCHITECTURE.md before overwriting.
---

# Vibe Architect Skill

Establishes the architectural foundation before a single line of spec or code is written.
Every pattern, convention, and structural decision made here becomes the law for the entire build.

**Always run in Plan Mode (Shift+Tab). No code. No project files.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principle this enforces

Spec before code — and architecture before spec. Without deliberate architecture decisions,
agents make reasonable but unconsidered defaults. Folder structure, naming conventions,
state management, error handling — these just happen, inconsistently.

ARCHITECTURE.md is the agent's constitution for the project.
Not what gets built (SPEC.md does that) — how everything gets built.
Every task from Phase 1 through Phase 3 is measured against it.
`review:` detects drift from it at every phase gate.

Good architecture on a small project costs 20 minutes.
Bad architecture on a small project costs days of refactoring.

---

## Step 0 — Read BRIEF.md, confirm stack, classify project type

**Check for existing ARCHITECTURE.md first:**
If ARCHITECTURE.md already exists at the project root:
> "An ARCHITECTURE.md already exists for this project.
> Do you want to update it (add new decisions) or start fresh (replace it entirely)?"
Wait for answer before proceeding.

**Check for BRIEF.md:**
If BRIEF.md does not exist:
> "BRIEF.md not found. Ideally run `brainstorm:` first — it captures the problem,
> user, stack preferences, and constraints that make architecture decisions meaningful.
>
> I can proceed without it by asking those questions now, or you can run brainstorm: first.
> Which do you prefer?"
- If proceeding without: ask for app name, core purpose, platform, and rough stack preference before Step 1.
- If running brainstorm first: stop here and tell user to run `brainstorm:` then return.

**If BRIEF.md exists:** read it fully. Extract:
- Core problem and user
- Platform (mobile-first, desktop, both)
- v1 feature set and complexity
- Tech stack preferences or mandates ← CRITICAL
- Compliance requirements (affects architecture choices)
- Known risks
- Agentic flag (if true — agent: should have run before this)

**Stack confirmation — mandatory before asking any questions:**

After reading BRIEF.md, immediately confirm the stack out loud:

> "Stack from BRIEF.md:
>   Frontend: [exact value from brief]
>   Backend:  [exact value from brief]
>   Database: [exact value from brief]
>   Auth:     [exact value from brief]
>
> Proceeding with this stack. I will NOT suggest alternatives unless
> a technical constraint discovered during this session requires it."

This one explicit confirmation step prevents the most common architect: failure:
silently defaulting to a popular framework (Next.js, Create React App) instead of
the stack already decided in brainstorm:.

If the stack seems mismatched for the requirements (e.g. brief says
"mobile app" but stack says "Next.js") — flag it now:
> "I notice the brief specifies [requirement] but the stack is [choice].
> This may cause [issue]. Recommend [alternative]. Proceed with brief's choice or switch?"

Wait for answer before continuing.

**Classify project type:**
- **Web app** — frontend (React/Vue/Svelte/Next.js etc) + optional backend
- **Mobile app** — React Native / Expo / Flutter
- **API service** — backend only, no UI
- **CLI tool** — command line
- **Static site** — HTML/CSS/JS, minimal interactivity
- **Library / package** — reusable code

Tell the user: "This is a [type] project. I'll ask about [relevant areas]."

Branch questions:
- Web app / Mobile app → Steps 1, 2 (if backend), 3, 4, 5
- API service → Steps 2, 3, 4, 5
- CLI / Library → Steps 3, 4, 5
- Static site → Step 1 (light), 4, 5

---

## Step 1 — Frontend architecture (web/mobile only)

Present as recommendations. User says "sounds good" or overrides.

> **Frontend structure — my recommendations:**
>
> 1. **Folder approach:** [Feature-based / Type-based] — I recommend [choice]
>    because [one sentence reason based on BRIEF.md size and complexity].
>    Sound good, or do you have a preference?
>
> 2. **State management:** For [app name], data is [describe from brief].
>    I recommend [Context+localStorage / Zustand / Redux / other]
>    because [one sentence reason]. Sound good?
>
> 3. **TypeScript:** Strict mode, no `any` — the O'Reilly framework requires this.
>    Any reason to deviate?
>
> 4. **Component library:** [Recommend based on design direction —
>    Tailwind only / shadcn/ui / Radix / none / existing if mandated].
>    Does this fit?

Lock in recommendations if user agrees. Note any overrides.

---

## Step 2 — Backend architecture (if project has backend)

Skip entirely if client-only with no API.

> **Backend structure — my recommendations:**
>
> 1. **API style:** REST with clear resource naming.
>    Reason to use tRPC or GraphQL instead?
>
> 2. **Business logic:** [Route handlers / Service layer] —
>    I recommend [choice] because [reason based on complexity].
>
> 3. **Input validation:** [Zod / Joi / yup] at route entry before any logic.
>    For this stack, [Zod] is the best fit. Agree?
>
> 4. **Error responses:** Consistent envelope —
>    `{ success: false, error: { code, message } }`.
>    This is what review: checks for. Agree?

---

## Step 3 — Testing philosophy

> **Testing approach:**
>
> My recommended approach for [app name]:
> - Unit: pure functions, utilities, calculations — always
> - Component: user interactions, state changes, conditional rendering — always
> - Integration: [if backend] API endpoints with real DB — always
> - E2E: skip for v1 unless a flow is genuinely high-risk
>
> The O'Reilly framework requires tests for every task —
> what gets tested matters more than coverage numbers.
> Stricter or lighter than this?

Lock the testing philosophy.

---

## Step 4 — Code quality and git conventions

> **Code quality:**
>
> 1. **Linter:** ESLint strict — `no-any`, `no-unused-vars`, `react-hooks/exhaustive-deps`.
>    Existing config to follow?
>
> 2. **Formatter:** Prettier — single quotes, semicolons, 2-space indent,
>    100 char line length. Standard?
>
> 3. **Dependencies:** Pin exact versions, `npm audit` before every commit,
>    prefer packages >1M weekly downloads. Sound reasonable?
>
> 4. **Git commits:** Conventional format — `feat(scope)`, `fix(scope)`,
>    `docs(scope)`, `design(scope)`. Doc commits always separate from code.
>    This is what the framework uses throughout. Agree?
>
> 5. **Pre-commit hooks:** Linter + tests before every commit?

---

## Step 5 — Synthesise and confirm

> 🧠 **Effort:** architecture trade-offs are one-shot and load-bearing — `review:`
> enforces this document every phase. Reason at high/xhigh effort with adaptive
> thinking; weigh the alternatives explicitly before committing to patterns.

> **Architecture summary for [App Name]:**
>
> **Project type:** [type]
> **Frontend:** [structure] · [state] · TypeScript strict · [component library]
> **Backend:** [API style] · [logic layer] · [validation] · [error format]  *(if applicable)*
> **Testing:** [philosophy summary]
> **Quality:** ESLint strict + Prettier + conventional commits + pre-commit hooks
> **Dependencies:** pinned, npm audit before commit
>
> Does this look right? Any changes before I write ARCHITECTURE.md?

Wait for confirmation.

---

## Step 6 — Generate ARCHITECTURE.md

Read `references/ARCHITECTURE_MD.md` for the full canonical template.

Generate ARCHITECTURE.md by filling every section of the template:
- **Project type section:** Copy stack from BRIEF.md verbatim. Include the
  "Do NOT scaffold with alternatives" warning with the specific stack chosen.
- **Folder structure:** Generate the actual project tree, not a generic example.
  Match what PLAN.md will define in the next step.
- **Never list:** Always include the 6 universal P0 items plus 2 project-specific
  ones derived from the conversation (e.g. "no direct Supabase calls outside repositories").
- **Testing table:** Adjust for project complexity (S/M/L from BRIEF.md).
- **Architecture decisions log:** Fill with the decisions made in Steps 1-5.
- **Delete inapplicable sections:** Backend section for client-only projects,
  database section if no DB, etc.

If updating existing ARCHITECTURE.md: add changelog entry and update
affected sections only. Never overwrite the Never list or decisions log.

Save as `ARCHITECTURE.md` at project root.
*(Moved to `vibe/ARCHITECTURE.md` when `new:` runs.)*

---

## Step 7 — Update BRIEF.md

Append to BRIEF.md:

```
---
## Architecture decisions
> Decided during architect: — [date]
> Full detail in ARCHITECTURE.md

- Project type: [type]
- Frontend structure: [choice] — [reason]
- State management: [choice] — [reason]
- TypeScript: strict mode, no any
- Testing: [philosophy summary]
- Backend: [choice if applicable]
- Code quality: ESLint strict + Prettier + conventional commits
- Dependencies: pinned, npm audit before commit
```

---

## Step 7.5 — Spec review gate

ARCHITECTURE.md is a load-bearing document — `review:` audits every phase against
it. Audit it now, the same way `brainstorm:` audits BRIEF.md and `vibe-agent`
audits AGENT_ARCH.md, rather than leaving it to be checked indirectly later when
`new:` runs.

> "Architecture drafted. Running spec-review before you scaffold..."

Invoke `vibe-spec-review` with:
- Trigger source: `architect`
- Scope: ARCHITECTURE.md + BRIEF.md (all that exist)

Present findings. If P0s are raised, offer to fix them before moving on. Then
continue to Step 8.

---

## Step 8 — Tell the user

---
> ✅ **Architecture locked.**
>
> **Decisions made:** [N]
> **O'Reilly principles:** enforced in every session via ARCHITECTURE.md
>
> Every task Phase 1 through Phase 3 follows these patterns.
> No agent defaults. No inconsistent conventions. No architectural drift.
> `review:` uses ARCHITECTURE.md as primary reference — drift caught at every gate.
>
> **To generate your project kit:**
> ```
> new: [your app description]
> ```
---

---

## How the agent uses ARCHITECTURE.md every session

Session startup order:
1. Read CLAUDE.md
2. Read vibe/CODEBASE.md
3. Read vibe/ARCHITECTURE.md — check patterns for today's task
4. Read vibe/SPEC_INDEX.md
5. Read vibe/TASKS.md

Before writing code: does this follow ARCHITECTURE.md patterns?
After writing code: did I introduce a new pattern not in ARCHITECTURE.md?
→ Yes: update ARCHITECTURE.md before marking task done.
→ Yes, and it was a necessary deviation: log in DECISIONS.md, update ARCHITECTURE.md.

## Document update rules

| Document | Updated when |
|----------|-------------|
| ARCHITECTURE.md | New pattern, library added, tech decision changed |
| BRIEF.md | Scope changes, core value refined, stack changed |
| SPEC.md + SPEC_INDEX.md | Always together — any scope change |
| PLAN.md | Architecture changes, phase structure changes |
| TASKS.md | After every single task — no exceptions |
| CODEBASE.md | New file, route, schema, or pattern added |
| DECISIONS.md | Every drift, scope change, tech choice mid-build |
| FEATURE_TASKS.md | Task done, decisions filled, checklist ticked |
| CLAUDE.md | Conventions change, active feature changes |

**The rule:** if something changed in the codebase, something changed in the docs.
If the docs aren't updated, the task isn't done.
