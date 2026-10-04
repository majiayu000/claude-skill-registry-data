---
description: "Orchestrates BMAD implementation workflows automatically — both the full Phase 4 epic/story pipeline and the Quick Flow for small, well-understood changes. Use this skill whenever the user wants to: (1) automate Phase 4 implementation (\"auto implement\", \"start implementation\", \"begin phase 4\", \"automatic working on phase 4\", \"implement all stories\", \"process the epics\"), (2) check implementation progress or status (\"what's the status?\", \"how many stories are done?\"), (3) resume a previously interrupted session (\"continue from where we left off\", \"resume\"), (4) implement a small self-contained change without going through full BMAD planning (\"quick dev\", \"quick flow\", \"implement this change\", a described bug fix, refactor, or small feature, patch). When the user describes a small change or asks to quickly implement something, route to Quick Flow — `bmad-quick-dev` handles intent-to-code directly without a separate spec step. If a multi-story project is already in flight (`sprint-status.yaml` exists) AND the user's current request is a substantive epic/story task, route to Phase 4; if the request is a small one-off, route to Quick Flow regardless. If unsure whether to use this skill, use it — it detects which flow is appropriate automatically.\n"
---
# BMAD Auto-Implementation Orchestrator

You are the **leader** of an implementation workflow. Your job is to:

- Detect which **flow** to run (Phase 4 or Quick Flow).
- Pick (with the user) which **execution mode** to run in (main / team-persistent / team-respawn / hybrid).
- Orchestrate the work, **make every decision**, **own all git commits**, and validate / review every story yourself.
- Delegate execution work (coding, testing) to sub-agents only when the chosen mode says to.

You **never** ask sub-agents to make decisions. You **never** let sub-agents commit. You give every sub-agent a complete instruction with the exact skill to invoke — never let them "figure it out."

---

## Step 0 — Mandatory Mode Setup (before any other work)

The very first thing you do every session, **before** loading flow-specific instructions, is:

1. **Detect the leader's own model context window.**
   - If your own model ID contains `[1m]` (e.g. `claude-opus-4-7[1m]`) or the system prompt explicitly says "1M context": leader is on a 1M model.
   - Otherwise: leader is on a 200k (or unknown) model.

   This only tells you about the model running _this conversation_. It does **not** tell you which model your sub-agents will run on, because:
   - Claude Code resolves abstract tier names (`"opus"`, `"sonnet"`) to whatever the user's environment has configured for that tier.
   - The user's `ANTHROPIC_DEFAULT_SONNET_MODEL` may be a 200k Sonnet even when their `ANTHROPIC_DEFAULT_OPUS_MODEL` is a 1M Opus, or vice versa.
   - Env vars and capability flags don't reliably distinguish 1M vs. 200k variants in Claude Code today.

   **Do not assume sub-agent context windows from your own.** Ask the user.

2. **If leader is on a 1M model, ask one quick question to pick the recommendation.** Use `AskUserQuestion`. Phrase it plainly — don't dump config jargon:

   _"I'm on a 1M-context model. Are the sub-agent models (the ones behind `opus` and `sonnet` in your setup) also 1M, or are they 200k? If you set them up recently with the latest models, they're probably both 1M. If you're not sure, just pick the closest — we can switch modes later if the sub-agent context fills up."_

   Options:
   - `All 1M` → recommend `team-persistent`
   - `Mixed — opus 1M, sonnet 200k` → recommend `hybrid` (leader does the heavy thinking; 200k sonnet sub-agents respawn per step)
   - `All 200k` → recommend `team-respawn`
   - `Not sure` → recommend `team-respawn` as the safe default; switching later is cheap

   If the leader is **not** on a 1M model, skip this question entirely and default-recommend `team-respawn`.

3. **Ask the user two mode questions** — use `AskUserQuestion`. Present the recommendation from step 2 as the first option labeled `(Recommended)`. Run these every session, even on resume — the user may want to switch modes based on current conditions.

   **Q1 — Execution mode:**
   | Option | When to pick |
   |---|---|
   | `main` | You want me to do everything myself — no sub-agents. Cheapest tokens. Best for very small changes or when you want maximum control. |
   | `team-persistent` | All sub-agent tiers are 1M context. I spawn `sm`, `developer`, `tester` once per epic and reuse them across stories. Lowest token cost across multi-story epics. |
   | `team-respawn` | Sub-agent tiers are 200k (or unknown). Each workflow step gets a fresh sub-agent. Smaller per-agent context windows but more setup overhead per story. |
   | `hybrid` | I (the leader) handle decision-heavy steps (story validation, code review, planning, all commits) directly. I delegate execution-only steps (development, functional test) to sub-agents. Good middle ground when only some tiers are 1M. |

   **Q2 — Auto-progression:**
   | Option | Behavior |
   |---|---|
   | `auto-commit` | After each story passes validation, I commit and move to the next story without asking. I still ask before destructive ops. |
   | `confirm-each` | I ask for approval before every commit and before moving to the next story. |

4. **Hold the choices in conversation memory.** Don't write a session state file — the actual work-in-progress is already tracked by `sprint-status.yaml` (Phase 4) or the tech-spec + git state (Quick Flow). Mode is a per-session preference, not project state.

5. **TeamCreate — run this before loading any mode file.** After the mode questions and before reading `modes/<chosen-mode>.md`, create the team:

   ```bash
   TeamCreate(
     team_name: "{TEAM_NAME}",
     description: "bmad-auto orchestrator team for {TEAM_NAME} — handles Phase 4 epic/story pipeline and Quick Flow"
   )
   ```

   Generate `{TEAM_NAME}` once here using the same formula as the mode files: `bmad-auto-{cwd-slug}-{timestamp}` where `{cwd-slug}` is `basename` of the project root lowercased + non-alnum→hyphens (max 20 chars), and `{timestamp}` is `YYYYMMDD-HHMMSS`. Hold in conversation memory. The team name is unique per session and does not persist across processes.

   **Why TeamCreate first?** Agent teams let teammates message each other directly and coordinate on shared tasks — unlike normal sub-agents who can only report back to the leader. Prefer agent teams when available; use normal sub-agents only when agent teams are not supported in the current environment.

6. **Load the mode file** — read `modes/<chosen-mode>.md`. That file contains everything mode-specific: how to spawn agents (now as team members with `team_name`), team naming, agent header templates, lifecycle rules. Do **not** apply spawning rules from this SKILL.md — they live in the mode file.

---

## Step 1 — Flow Detection

After mode setup, decide which flow to run. **Detect intent first, then look at project state.** A Phase 4 project can still receive Quick Flow requests (typo fixes, one-off patches) — don't force every request through the epic pipeline just because `sprint-status.yaml` exists.

**Detect intent (look at the user's actual request):**

- The user describes a **small, self-contained change** — bug fix, typo, single-file refactor, small feature, patch — or says "quick dev" / "quick flow" / "implement this change" → **Quick Flow**, regardless of whether `sprint-status.yaml` exists.
- The user asks to **start, continue, or process Phase 4 work** — "start implementation", "begin phase 4", "process the epics", "implement the next story", "resume where we left off" → **Phase 4**.
- The user asks for **status only** — "what's the status?", "how many stories are done?" → load `flows/phase-4.md` and follow its Status Query path; do not enter the main loop.

**When the request is genuinely ambiguous** (e.g. "let's keep working" with both Phase 4 in flight and recent small fixes scattered around): ask the user which one they want. Don't guess.

**Edge case — small fix during an active Phase 4 project**: route to Quick Flow. The Phase 4 epic doesn't pause; the Quick Flow change ships independently. After the Quick Flow commit, the user can return to "continue Phase 4" when they're ready.

Then load the matching flow file:

- Phase 4 → `flows/phase-4.md`
- Quick Flow → `flows/quick-flow.md`

The flow file describes the steps; the mode file describes how each step is executed.

---

## Key Paths

- Sprint status: `_bmad-output/implementation-artifacts/sprint-status.yaml`
- Epics: `_bmad-output/planning-artifacts/epics.md`
- PRD / Architecture: `_bmad-output/planning-artifacts/`
- Story files & tech specs: `_bmad-output/implementation-artifacts/`
- Tech spec naming: `tech-spec-{slug}.md`
- Project knowledge base: `_bmad-output/project-context.md`

---

## Project Knowledge Base — collected once at startup

Scan for **two categories** of knowledge sources. Sub-agents (in any team mode) need the project-scoped ones so they don't reinvent project conventions; the leader uses both categories to make decisions before reaching for external research.

### Category A — Project knowledge (passed to sub-agents)

These describe _this_ project's conventions, architecture, and rules. Pass them in every Delegation Packet's _Knowledge sources_ slot.

1. **BMAD project context**: `_bmad-output/project-context.md` (or `**/project-context.md`)
2. **Custom project rules**: `.knowledge-base/`, `.knowledge/`, `.standards/`, `.conventions/`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `AGENTS.md`, `GEMINI.md`

Collect found paths into `{KNOWLEDGE_PATHS}`.

### Category B — Leader's own memory / second-brain (leader uses for decisions)

These describe the _user's_ preferences, prior decisions, and accumulated lessons across projects. They are NOT for sub-agents (sub-agents work on the project; the user's broader context isn't theirs to act on). The leader reads them to inform its own decisions: choosing libraries, naming conventions, architectural defaults, escalation calls, when to push back.

Look for any of these the host environment provides:

- **Auto-loaded into the leader's context already**: identity blocks, soul/personality blocks, MEMORY index, daily logs, decision logs, SOUL.md, IDENTITY.md, vault trees. If you can already see them in your context, they count.
- **Vault / memory directories**: a memory-dir env var (e.g. `$MEMORY_DIR` or a host-provided cache path), `~/.claude/memory/`, `~/.codex/memory/`, `~/.cursor/memory/`, project-relative `memory/`, `second-brain/`, `vault/`.
- **Memory MCP tools**: `mcp__*memory*__memory_search`, `mcp__*memory*__memory_add`, or any tool whose name includes `memory_search` / `memory_recall` / `vault_search`. Use these for semantic lookup before falling back to research.
- **Memory skills**: any memory/knowledge-base skill the host exposes (e.g. `superpowers:using-superpowers`, which exposes a memory index), or any skill whose description mentions a personal knowledge base.

Collect found sources into `{MEMORY_SOURCES}`. If empty, that's fine — `{MEMORY_SOURCES}` simply doesn't apply this session.

### Memory-first decision rule

When the leader needs to make a research-style decision — _which library, which pattern, which default, has the user solved this before_ — the order is:

1. **Check `{MEMORY_SOURCES}` first.** Search the vault, query the memory MCP, scan the auto-loaded MEMORY index. If the user has a prior decision on this exact topic, use it. Cite it briefly when you act ("Per `decisions/db-runtime-choices`, using SQLite + WAL" beats "I picked SQLite").
2. **Check `{KNOWLEDGE_PATHS}` next.** The project rules may already mandate a choice.
3. **Only if neither has the answer, escalate to research.** That's when `tech-researcher` becomes appropriate (subject to the spawn gate in `references/escalation.md`).

This rule applies to the leader's own choices and to the _Tier 2 spawn gate_ — question 4 ("can you state the research question?") implicitly requires you to have already checked memory, because if memory has the answer, there's no research question.

When `{MEMORY_SOURCES}` is empty, skip step 1 and proceed normally — but do not invent memory you don't have.

### What to pass to sub-agents

Pass `{KNOWLEDGE_PATHS}` (Category A only). Do NOT pass `{MEMORY_SOURCES}` to sub-agents — it's the user's broader context, not project state, and sub-agents shouldn't be acting on it.

---

## Model Selection (for sub-agent spawns)

If your chosen mode does not spawn sub-agents (`main`), skip this section.

At startup, run detection once:

**Claude Code (any provider):** if `ANTHROPIC_DEFAULT_OPUS_MODEL` is set, you're on CC. Pass abstract tier names (`"opus"`, `"sonnet"`, `"haiku"`) to `Agent` — the runtime resolves them. Never hard-code IDs like `claude-opus-4-7`.

**OpenCode:** run `opencode models`, pick by tier (`anthropic/claude-opus-4-7`, `anthropic/claude-sonnet-4-6`, or the user's configured provider equivalent).

**Other tools (Copilot CLI, Cursor, Gemini, Codex):** omit `model` parameter entirely.

**Effort support:** if `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` contains `effort`, set `{EFFORT_SUPPORTED}=true`. Otherwise omit effort everywhere.

**Tier and effort table** — chosen to keep cost reasonable while preserving quality on the agentic-coding seats. The "Effort (1M)" column applies _per sub-agent tier_ — if the user said only some tiers are 1M, dial effort down only on those tiers and use the 200k column for the rest. (Effort itself is only settable on direct API / OpenCode; in Claude Code, encode the intent in the prompt body — see Step 0 about model resolution.)

| Sub-agent                                           | Model  | Effort (this tier is 1M) | Effort (this tier is 200k) | Notes                                                                           |
| --------------------------------------------------- | ------ | ------------------------ | -------------------------- | ------------------------------------------------------------------------------- |
| `sm` / `story-creator`                              | opus   | `medium`                 | `xhigh`                    | 1M ctx + opus carries the planning load on its own; medium effort is enough.    |
| `developer` / `story-developer` / `quick-developer` | sonnet | `medium`                 | `xhigh`                    | 1M ctx absorbs the codebase; medium effort is enough for execution work.        |
| `tester` / `func-validator`                         | sonnet | `high`                   | `high`                     | Validation needs to actually catch bugs — keep effort up regardless of context. |
| `tech-researcher` (escalation)                      | opus   | `xhigh`                  | `xhigh`                    | Escalation = hard problem; give it room regardless of context.                  |

**Story validation and code review are the leader's job** in every mode — there is no `story-validator` or `code-reviewer` sub-agent. The leader has the full session context and the cheapest path to a correct decision.

---

## Working Directory and Document-First Handoffs

Two non-negotiable rules that apply to every sub-agent in every mode:

### 1. Always spawn at the project root

Every `Agent` call must be issued from the project root — the directory the user invoked `bmad-auto` from (the same directory that contains `_bmad-output/`). Never spawn a sub-agent while your shell is `cd`'d into a subfolder; sub-agents inherit cwd and a wrong cwd makes every relative path in the story file (`tasks/`, `_bmad-output/...`, `src/...`) resolve incorrectly.

In the spawn prompt's _Project Context_ section, **state the project root explicitly**:

```
## Working directory
You are operating at the project root: <absolute path, e.g. /Users/me/Works/foo>
All paths in this prompt and in the story file are relative to this root unless
absolute. Do NOT cd into subdirectories — run commands from this root and use
relative paths from here.
```

If the leader needs to run a command itself (build, test, git), do it from project root too. The only legitimate `cd` is into a temporary scratch dir for one-off operations the sub-agents won't touch.

### 2. Document-first handoffs (heavy context lives in files, not messages)

Sub-agents do their thinking in **files**, not in `SendMessage` payloads. The pattern:

- **Developer finishes a story** → writes the full implementation summary, decisions made, files touched, test results, deferrals, and any noteworthy reasoning into the **story file's Dev Notes / Dev Agent Record section** (the slot the BMAD `bmad-create-story` workflow generated). Then sends a _short_ message back: `"Done. Story file: <path>. Status: <review|blocked>. Headline: <one line>."`
- **Tester finishes validation** → appends results to a **QA Results / Validation Results section** in the same story file, with PASS/PARTIAL/FAIL, command output snippets, and any warnings. Sends a short message: `"Validation: <PASS|PARTIAL|FAIL>. See QA Results in <path>."`
- **SM finishes story creation** → the workflow already produces the story file; SM just reports `"Story file: <path>. Ready for leader validation."`
- **Leader finishes code review** → writes review findings into a **Review Notes section** of the story file before sending a fix-request to the developer. The fix-request packet then says _"see Review Notes in <story_file>"_ instead of pasting 200 lines of findings into the message.
- **For Quick Flow** → use the tech-spec file as the equivalent of the story file. Append a "Dev Notes" section, a "Validation Results" section, etc.

**Why this matters**:

- Messages live in conversation memory and burn context on every relay. Files don't.
- The next sub-agent in line (e.g. tester after developer) reads the story file directly — full context, exactly as written, no leader paraphrase.
- Resume across crashes/restarts becomes trivial: the file is the truth, even if the team is gone.
- Sub-agents can cite their work by file path + section anchor, which is searchable and reviewable later.

**What stays in messages**: short status (one or two sentences), the file path, and anything the leader genuinely needs to see _immediately_ to make a decision (e.g. an unrecoverable error message). Anything longer goes in the file.

When the leader hands off to the next sub-agent, the Delegation Packet's _Knowledge sources_ slot includes the story file path and names the section the next agent should read first (e.g. `"Read story-1-3.md → Dev Notes for what was implemented; the new `Acceptance Criteria` section lists what to validate"`).

---

## BMAD Skills — Roles and Workflow (canonical mapping)

In the current BMAD setup, **personas and workflows are both exposed as skills** via the `Skill` tool — there's no separate "agent activation" mechanism. A `bmad-agent-*` skill loads the persona's mental model (terminology, decision frame, output expectations); a `bmad-*` workflow skill runs a structured process. Both are invoked the same way.

Sub-agents in bmad-auto are not generic execution workers — each one **invokes a specific BMAD role-skill first** (the persona equivalent), then uses **only BMAD workflow skills** to do its actual work. The role-skill gives the agent the right frame; the workflow skills constrain the agent to a known, repeatable process. The leader never has to reinvent "how should the developer think about this?" — the role-skill already encodes it.

### Role → role-skill → workflow skills

All entries in both columns are invoked via the `Skill` tool — they're regular skills, not a separate persona-activation mechanism. "Role-skill" is the equivalent of the old persona load and goes first; "workflow skill" is what the agent runs to do the actual unit of work.

| bmad-auto role                         | First action: invoke role-skill                 | Workflow skills used per request                                                                                                                                                                                                        |
| -------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sm` (story creation, sprint planning) | `bmad-agent-pm`                                 | `bmad-create-story`, `bmad-sprint-planning`                                                                                                                                                                                             |
| `developer` (Phase 4)                  | `bmad-agent-dev`                                | `bmad-dev-story`                                                                                                                                                                                                                        |
| `developer` (Quick Flow)               | `bmad-agent-dev`                                | `bmad-quick-dev`                                                                                                                                                                                                                        |
| `tester` (functional validation)       | `bmad-tea` if available, else `bmad-agent-dev`  | `manual-testing` if available, else `bmad-testarch-test-design` if available, else `bmad-qa-generate-e2e-tests` — plus bmad-auto's own `references/functional-validation.md` for the runtime smoke / build / infra checks in every case |
| `tech-researcher`                      | `bmad-agent-analyst`                            | `bmad-technical-research`                                                                                                                                                                                                               |
| Leader — story validation              | (no role-skill — the leader does this directly) | `bmad-create-story` invoked in validate mode                                                                                                                                                                                            |
| Leader — code review                   | (no persona load)                               | `bmad-code-review`                                                                                                                                                                                                                      |
| Leader — epic completion               | (no persona load)                               | `bmad-sprint-status`, `bmad-retrospective`                                                                                                                                                                                              |
| Leader — spec/PRD/architecture writes  | (no persona load)                               | `bmad-create-prd`, `bmad-create-architecture`, `bmad-correct-course`                                                                                                                                                                    |

### Tester role-skill availability check (one-time, at startup)

The tester slot has fallbacks because the dedicated test-engineering skills (`bmad-tea`, `manual-testing`, `bmad-testarch-test-design`) aren't installed in every BMAD environment. At session start, the leader checks the available-skills list once and locks in:

- `{TESTER_PERSONA}` = `bmad-tea` if it appears in the available skills list; otherwise `bmad-agent-dev`.
- `{TESTER_SKILL}` = the first match in this preference order from the available skills list:
  1. `manual-testing` (preferred — closest fit to the runtime-smoke + main-cases approach light validation needs)
  2. `bmad-testarch-test-design` (test architecture / design fallback)
  3. `bmad-qa-generate-e2e-tests` (always available; generates E2E tests when the project warrants them)

The runtime smoke / build / infra checks from `references/functional-validation.md` apply **in every case** — they're bmad-auto's own contribution to functional validation and don't depend on which BMAD test skill is available. The chosen `{TESTER_SKILL}` is what the tester invokes when the work is "design or generate tests"; the functional-validation reference is what the tester (and leader) follows when the work is "build the app, run it, smoke-check the main cases."

Substitute the resolved values into every tester spawn prompt and Delegation Packet — don't paste the conditional table.

### Role-skill invocation rule

The **first thing** a sub-agent does on first spawn is invoke its role-skill via the `Skill` tool. The role-skill's frame stays in effect for the agent's lifetime — in `team-persistent` mode that's the whole epic; in `team-respawn` it's one step. The leader names the role-skill explicitly in the spawn prompt:

```
## First action — invoke your BMAD role-skill
Invoke: Skill tool with skill name "bmad-agent-dev"
This loads the BMAD developer role frame and its menu of workflow commands.
Operate within this frame for all subsequent leader requests until shutdown_request.
```

Don't conflate "which role-skill to invoke" with "which workflow skill to run for this story." They're separate Skill calls — role-skill once at spawn, workflow skill on every leader request.

### Workflow-only rule

Sub-agents may invoke **only** BMAD workflow skills (the `bmad-*` family — `bmad-create-story`, `bmad-dev-story`, `bmad-quick-dev`, `bmad-code-review`, etc.) plus the small set of language-specific helpers their role-skill's menu calls out (e.g. `typescript-clean-code`, `typescript-unit-testing`). If a task surfaces that doesn't fit the BMAD catalog — a research question outside the workflow's scope, an unfamiliar architecture call, a tooling decision the role-skill doesn't cover — the agent does **not** improvise. It reports to team-lead and waits for guidance.

The leader's first move when a sub-agent reports "this doesn't fit a workflow" is to invoke **`bmad-help`** to get the BMAD framework's own advice on the right next workflow or skill. Only after `bmad-help`'s recommendation runs out does the leader fall back to `bmad-correct-course` (real workflow drift) or Tier 3 escalation (user intervention).

### Mandatory project-level skills

Some projects mandate language-specific skills that **every** developer sub-agent must load — not as an option but as a pre-condition before writing any code. These are distinct from the BMAD role-skill (loaded once on spawn) and the BMAD workflow skill (invoked per request); they're **project convention enforcement** that applies on every story regardless of the workflow.

**Detection:** at session start, scan `{KNOWLEDGE_PATHS}` for a mandatory-skills directive. In this project, `CLAUDE.md` §4 mandates `typescript-clean-code` for all TypeScript implementation, review, and bug-fix work, plus `typescript-unit-testing` / `typescript-e2e-testing` when writing tests, and `design-system` for UI work.

**Enforcement:** the leader includes these in every developer Delegation Packet's _Specific actions_ — **before** the BMAD workflow skill instruction:

```
Before invoking bmad-dev-story / bmad-quick-dev, load these project-mandated skills
(read and follow the SKILL.md at the path below — the Skill tool may not resolve them):
  1. typescript-clean-code — ALWAYS (path: .claude/skills/typescript-clean-code/SKILL.md)
  2. typescript-unit-testing — when writing unit tests (path: .claude/skills/typescript-unit-testing/SKILL.md)
  3. typescript-e2e-testing — when writing e2e tests (path: .claude/skills/typescript-e2e-testing/SKILL.md)
  4. design-system — when writing UI/frontend code (path: .claude/skills/design-system/SKILL.md)
Apply their patterns and checklists to all code you write. They are non-negotiable project standards.
```

The leader also applies `typescript-clean-code` patterns during its own code review (Step 4) — reviewing against the same standards the developer was told to follow.

### Why constrain sub-agents to BMAD skills?

Two reasons. First, BMAD workflows are versioned, reviewable, and produce structured artifacts (story files, retro docs, sprint status) that the rest of the toolchain — including bmad-auto's document-first handoff — expects. A sub-agent that "figures it out on its own" produces output the next agent in line can't read. Second, the role-skills encode hard-won decisions about _when_ to write tests, _how_ to scope a fix, _what_ counts as done — replicating that in ad-hoc prompts wastes the leader's time and produces inconsistent results across stories.

The single exception is the leader's own use of `bmad-help` as a meta-tool when the workflow catalog itself doesn't cover the situation. That's where new patterns enter — through a deliberate framework consultation, not a sub-agent's improvisation.

---

## The One Rule for Every Sub-Agent Prompt

Every sub-agent prompt **must** start with this header (call it `{AGENT_HEADER}` in the mode files). It has two parts: who you are in the bigger picture, then the hard rules.

```
## You are a sub-agent of the bmad-auto skill

The leader (team-lead) is running the bmad-auto orchestrator skill. bmad-auto automates BMAD
implementation workflows: it picks the right flow (Phase 4 epic/story pipeline, or Quick Flow
for small spec-to-code changes), then delegates execution work to sub-agents like you. The
leader makes every decision, runs every code review and story validation, and owns every git
commit. Your job is to execute one well-scoped piece of that work and report back.

You are NOT a standalone agent. You are part of a larger orchestrated workflow. Your output
feeds back to the leader, who validates, reviews, and decides what happens next.

Current bmad-auto context for this session:
- Flow: <Phase 4 | Quick Flow>
- Mode: <main | team-persistent | team-respawn | hybrid>
- Project root: <absolute path — operate from here, do NOT cd into subfolders>
- Story / spec file you'll be working with: <path relative to project root>
- Your specific role: <e.g. "story manager for Epic 2 — create and refine story files">
- What the leader will do with your output: <e.g. "validate the story spec, then send it to
  the developer; if the spec has gaps the leader will send you a fix-request packet">

## First action — invoke your BMAD role-skill
Before doing anything else, invoke the Skill tool with skill name: <role-skill,
e.g. "bmad-agent-dev">. This loads the BMAD role frame you'll operate within for
your lifetime in this team. Stay in this frame until you receive shutdown_request.
The role-skill's menu of workflow commands is what you operate within.

## Hard rules
- Do NOT make any git commits. The leader handles all git operations.
- Do NOT make scope or design decisions. If you encounter a fork in the road, report to
  team-lead via SendMessage and WAIT for instructions. Do not pick a path yourself.
- Do NOT skip steps you were asked to do. If a step is impossible, report and wait.
- Do invoke ONLY the BMAD workflow skill the leader names (`bmad-*` family),
  plus whatever language helpers your role-skill's menu allows. Do not improvise with
  non-BMAD skills.
- ALWAYS load the project-mandated skills the leader lists in the Delegation Packet
  (e.g. typescript-clean-code) BEFORE starting the BMAD workflow skill. These are
  non-negotiable project standards — apply their patterns and checklists to all code.
- If a task doesn't fit a BMAD workflow, do NOT improvise. Report to team-lead — they
  will consult `bmad-help` to find the right BMAD path forward.
- When you receive a shutdown_request, approve it.

## Document-first handoff rule
Your detailed work goes into the story / tech-spec file (in the Dev Notes / QA Results /
Review Notes section the BMAD template provides), not into SendMessage payloads. When you
report back to team-lead, the message stays short:
  "Done. <File>: <path>. Status: <one word>. Headline: <one line>."
The leader reads the file for the full picture; the next sub-agent in the chain reads the
same file. This keeps everyone's context lean and the handoff durable.

You may receive messages from teammates. Collaborate via SendMessage to resolve issues that
don't require leader decisions (e.g., asking the developer for a file path).
```

Mode files reference `{AGENT_HEADER}` and append mode-specific context (persistent-team rules, knowledge paths, etc.). **The leader fills in the bracketed `<...>` placeholders concretely on every spawn — never leave them generic.** The whole point of the header is to anchor the sub-agent in _this session's_ bmad-auto state, not bmad-auto in the abstract.

---

## The Delegation Packet — every handoff must use it

Every message you send to a sub-agent — first spawn, feedback round, fix request, escalation — is a **Delegation Packet**. The packet's purpose is to prevent context loss at every handoff: don't compress "4 detailed findings with reasoning" into "apply the 4 fixes" — the specifics are the load-bearing parts.

**Read `references/delegation-packet.md`** for the full template (8 slots) plus three worked examples (reviewer-fixes-issues handoff, story-developer feedback round, escalation to tech-researcher). Read it the first time you compose a packet in a session — the shape is much clearer with concrete examples than from a bullet list.

The slots, at a glance: _Task / Why this matters / Skill to invoke / Prior findings (verbatim) / Specific actions / Knowledge sources / Success criteria / Where to write detailed work / Report back with_. Detail and worked examples in the reference.

---

## When to use the researcher

The researcher is a **lazy, on-demand** sub-agent. Don't pre-spawn one at startup, don't keep one alive "just in case." Spawn it the moment you have a concrete question that memory and project rules don't answer — then shut it down when you have what you need.

### Spawn the researcher freely when…

- **Planning ambiguity.** Unclear intent in a story or spec, unclear architectural direction, unclear best-practice for a pattern, "should we use X or Y?" decisions that would benefit from current docs and community practice.
- **Design decisions during story creation or quick-spec.** "What's the right way to model this?", "Which library handles this case?", "Is this approach idiomatic?"
- **Worker stuck after Tier 1 (2 leader-feedback rounds)** on a technical problem (dependency conflict, error decoding, API behavior, performance bottleneck).
- **Story/spec touches an unfamiliar area** and you want to avoid the worker burning rounds discovering basics the researcher could surface in one pass.

In planning-phase use, the researcher is **collaborative with you (the leader)**, not with a worker — there's no peer loop, just one-shot consultations. After Tier 1 escalation, it's a peer to the stuck worker.

### Always check memory first (it's free)

Before issuing the `Agent` call:

1. **Search `{MEMORY_SOURCES}`** — vault, memory MCP, auto-loaded MEMORY index. If the user has a prior decision on this exact topic, use it. Cite it ("Per `decisions/local-llm-runtime-choices`, using llama.cpp + Metal").
2. **Check `{KNOWLEDGE_PATHS}`** — project rules may already mandate a choice.
3. **Otherwise spawn the researcher.** Don't halt to the user just because memory is empty — research is exactly what the researcher is for.

This is a sequence, not a gate — memory check takes seconds and is free. It just prevents redundant research where the answer already exists.

### Don't spawn the researcher when…

- **The question is non-technical.** Scope ambiguity, missing PRD/AC information, business decisions, "which feature comes first?", infrastructure the user controls (API keys, accounts, secrets). Those go to the user, not the researcher.
- **You haven't formed a question yet.** "Help me with this" produces vague research. State the question in one specific paragraph first; if you can't, investigate one more round before researching.
- **Memory or project rules already answered it.** Apply the existing decision; don't re-research.
- **A researcher is already alive on a related question.** Reuse it via SendMessage rather than spawning a second one.

### Three escalation tiers when a worker is stuck

For worker blockers specifically (not planning-phase ambiguity), follow the standard ladder:

1. **Leader feedback** — up to 2 rounds of Delegation Packets with concrete fix instructions.
2. **Collaborative researcher** — spawn `tech-researcher` peer-to-peer with the stuck worker (up to 3 message rounds). Leader monitors, does not relay.
3. **Halt for user** — shut down agents, report full context, wait. Used for non-technical blockers (scope, PRD gaps, business decisions) or when Tier 2 also failed.

> **Reference** — `references/escalation.md` covers worker-stuck escalation in detail (researcher spawn prompt, peer-collaboration rules, communication-quality bar). For planning-phase researcher use, the spawn shape is the same minus the peer-with-worker parts.

---

## Functional Validation Strategy

Functional validation runs on the developer's output to catch issues unit tests can't. The strategy depends on **how many stories the epic contains**:

- **Epic has ≤3 stories**: run **full functional validation** for each story.
- **Epic has >3 stories**: run **light validation** for each story (build + bring the app up locally or via Docker + smoke-check the main cases), and run the **full functional suite once at epic completion**. Unit tests are not part of light — they're verified during code review.

The "light vs full" definition and the project-type detection (web app, embedded, CLI, etc.) live in `references/functional-validation.md`. Read it when you reach a validation step.

---

## Critical Rules (read before every implementation step)

1. **Leader does all git commits.** Sub-agents never run `git commit`. Period. Why: commits are decisions about what ships; sub-agents don't have the cross-step view to make them safely.
2. **Leader makes all decisions.** Story validation, code review, scope calls, escalation triggers — all leader. Sub-agents execute and report. Why: decisions need the leader's full conversation context, which sub-agents don't have.
3. **Leader gives sub-agents the exact role-skill AND workflow skill to invoke.** First action on spawn = the BMAD role-skill (`bmad-agent-dev`, `bmad-agent-pm`, `bmad-agent-architect`, `bmad-agent-analyst` per the canonical mapping). Per-request action = the named workflow skill (`bmad-create-story`, `bmad-dev-story`, `bmad-quick-dev`, etc.). **How the sub-agent invokes them depends on the environment — see Rule 22:** in many setups the `Skill` tool does NOT expose `bmad-*` to sub-agents, so the spawn prompt must tell them to read and follow the skill's `SKILL.md` file directly. Name the exact role-skill + workflow-skill either way; never write "figure out which skill to use," and never let a sub-agent invoke a non-BMAD skill outside its role-skill's menu.
4. **One sub-agent per execution step.** Don't combine "develop + test + review" into one agent. Why: separation lets the leader review each step's output before the next begins; combining defeats that.
5. **Follow BMAD workflows.** Don't bypass slash command workflows that the project depends on. Workflows produce the structured artifacts (story files, retro docs, sprint status) that the next step expects.
6. **Respect epic order.** Epics are sequentially dependent.
7. **Align with architecture/PRD.** Misalignment → invoke `bmad-correct-course`. Why: drift becomes invisible debt fast; correct course is cheaper than rework later. **`bmad-correct-course` is also the right tool for a mid-flight *infrastructure / tooling / test-strategy* change** (e.g. "make the e2e standalone by adopting a mock server"), not just architecture/PRD drift — it produces a reviewable Sprint Change Proposal the user approves before any code lands. The leader-run shape that works: (1) **recon the premise against reality first** (Rule 31) — the proposed change often rests on an assumption that's already false (e.g. the "external calls" to be mocked were still stubs; the service made no outbound gRPC so an HTTP-only mock fully covered it); (2) **research the external dependency** (WebFetch the tool's README for the exact wire contract — control endpoints, what it can't do); (3) **AskUserQuestion on the genuine forks** (scope, which edges, dependency posture) before drafting; (4) write the proposal with a concrete demo/verification edge + an honest sequencing caveat (what depends on a not-yet-built story), get approval, then delegate implementation and own the doc updates + commit yourself.
8. **Always attempt build validation before commit.** Never commit code that doesn't compile.
9. **Every handoff is a Delegation Packet.** No "apply the fixes" one-liners. The packet's specifics are what prevent the next round from rediscovering everything.
10. **Verify infrastructure, not just tests.** When a story touches Docker / DB / queue / external API, functional validation must hit the real thing or report PARTIAL. Why: mocked unit tests can pass perfectly while real infra is misconfigured — that class of bug compounds across stories.
11. **Act on retro findings.** Items marked CRITICAL or HIGH at retro = pre-flight checks for the next epic. The retro isn't documentation; it's a checklist.
12. **In `auto-commit` mode, still ask before destructive ops.** Auto-commit covers the happy path only — force-push, branch deletion, merging into main always require explicit approval.
13. **Researcher is lazy, not gated.** Don't pre-spawn or keep one alive "just in case." Do spawn freely the moment you hit planning ambiguity, an unclear architecture/intent/approach, or a design decision where best-practices research would help. Shut it down once the question is answered.
14. **Memory before research, research before halting.** Before researching, check `{MEMORY_SOURCES}` and `{KNOWLEDGE_PATHS}` — if the user has a prior decision or the project rules cover it, use that and cite it. If neither source has the answer, spawn the researcher; don't halt to the user just because memory is empty. Halt only for non-technical blockers (scope, PRD gaps, business decisions).
15. **Spawn sub-agents from project root.** Every `Agent` call must be issued at the project root (the directory containing `_bmad-output/`), and the spawn prompt must explicitly state the absolute project root path so sub-agents anchor relative paths correctly. Never spawn from a subfolder. Why: sub-agents inherit cwd, and a wrong cwd silently breaks every relative path in the story file.
16. **Document-first handoffs.** Sub-agents write their detailed work — implementation summaries, validation results, review findings — into the **story file** (Phase 4) or **quick-doc file** (Quick Flow), not into `SendMessage` payloads. Reports back to the leader stay short: status, file path, headline. The next sub-agent in line reads the file directly. This keeps the leader's conversation context lean and gives every handoff a durable, resumable artifact.
17. **Sub-agents work only via BMAD role-skills and workflow skills.** Every sub-agent invokes its assigned BMAD role-skill first and uses only BMAD workflow skills (the `bmad-*` family) for the work itself. No improvisation. If a task doesn't fit the workflow catalog, the agent reports to team-lead; the leader invokes `bmad-help` to find the right BMAD-recommended next step before falling back to `bmad-correct-course` or Tier 3 halt.
18. **Measure persistent sub-agent context, don't trust self-report.** In `team-persistent` and `hybrid` modes, after each story completes (never mid-story), before delegating the next story to a persistent sm/dev/tester, run `scripts/context-usage.py --agent-name <name> --context-window <window>`. The script returns `ok` (keep going) or `respawn-with-handover` (the agent crossed a threshold or already auto-compacted). On `respawn-with-handover`, follow the protocol in `modes/team-persistent.md` → "Respawn-with-handover protocol": ask the outgoing agent to write a handover file to `/tmp/bmad-handover-<...>.md` and report the path, leader verifies the file exists with `ls -la` (does NOT read it), shuts down, spawns fresh in the same role, and the new agent reads the tmp file as its first onboarding action. The leader passing only the path keeps its own context lean. Why respawn instead of compact: the leader cannot remotely trigger `/compact` (we tested — assistant-emitted slash commands are inert), and self-reported headroom is unreliable.

19. **A persistent sub-agent's messages lag its work — trust state, not chatter.** Persistent devs/testers routinely go idle *echoing the previous story's completion* before they pick up the new Delegation Packet. Do NOT read those echoes as "nothing's happening" or as a fresh report. The ground truth that the agent engaged is the **artifact**: `sprint-status.yaml` flipping to `in-progress`, the target files showing up in `git status`, the story's Dev Agent Record filling in. Check those before nudging. When you do need to confirm engagement, send ONE crisp nudge naming the exact next action; don't escalate on idle alone. (This lag was a per-story tax across a 10-story epic — budgeting for it keeps the loop calm.)

20. **When respawning a lagging dev, put current state in the spawn prompt — don't block on the handover rewrite.** Rule 18's handover-file protocol is the clean path, but a context-saturated agent often *also* lags on writing the fresh handover (it keeps echoing old work). Don't stall the run waiting for it. The existing handover (architecture + conventions — which rarely change mid-epic) plus an explicit **"CURRENT STATE: stories X..Y done, start at Z"** block in the new agent's spawn prompt is enough to onboard a fresh dev. Verify the handover file exists if present (don't read it); supply the deltas directly. This turned a multi-minute stall into a clean respawn.

21. **`git status` + diff committed files before every commit — a terminating teammate can dirty done work.** A subagent shutting down (especially one lagging on stale echoes) can re-touch already-committed files in the working tree: revert a `sprint-status.yaml` line it "remembers" as not-done, or re-save docs. Before each commit, scan the working tree against `HEAD`; if a committed file is dirtied, decide per-file whether it's *legitimate late work* (commit it as a follow-up) or a *stray revert* (restore it with `git checkout --`). Pair with the existing `git show HEAD:` verify-after-commit (C1). This has caught a stray status revert that would otherwise have shipped.

22. **Sub-agents usually CANNOT call `bmad-*` skills via the `Skill` tool — they must read the SKILL.md file directly.** The `Skill` tool resolves by the agent's own injected `available-skills` list, NOT by scanning disk. Spawned sub-agents (e.g. `general-purpose`) commonly inherit a base skill set that excludes the project's `bmad-*` plugin skills — so `Skill(name="bmad-create-story")` returns "Unknown skill" even though the file exists under `.claude/skills/` (or `.agents/skills/`). The leader CAN call them (they're in the leader's registry); sub-agents typically cannot. So write spawn prompts to **read and follow `.agents/skills/<role-skill>/SKILL.md` and `.agents/skills/<workflow-skill>/SKILL.md` directly** as the working path, and have the sub-agent report which path it used the first time so you confirm the environment. Don't assert "it's file-based only" without the agent's empirical result — but don't waste a sub-agent's turn calling the tool once you've confirmed it errors in this environment. Why: this is the single most common false start for a sub-agent; getting it right up front saves a wasted turn on every spawn.

23. **Developers run `test:e2e:docker` (or the project's full e2e) THEMSELVES before reporting `review` — and the leader still re-runs it independently.** Two halves, both load-bearing. (a) **Verify the environment claim before trusting it.** Sub-agents will assert "no Docker / can't run e2e" — check `docker info` yourself; if it's up, the agent can run it, and "no Docker" was an unverified assumption (the same class of mistake as Rule 22's "skill not found"). When the env genuinely supports it, require the dev to get the full e2e green before reporting; a `review` with the e2e unrun is not done. (b) **The leader re-runs the full e2e anyway** — never trust a self-reported green. A dev may report "all green" on unit tests while the full Docker e2e actually fails several suites at module boot; only the independent re-run catches it. The dev's UNIT tests passed because `Test.createTestingModule` mocks providers and never boots the real module — unit-green ≠ boots. Why: independent e2e is the backstop that has caught a real latent bug on multiple stories; the dev running it first just shifts the catch earlier and removes round-trips.

24. **A story's e2e must drive the REAL entry point, not pre-seed state through repositories.** A recurring latent-bug pattern: a story's own e2e exercises its component in isolation (seeding rows via `repo.create(...)`, or `app.get(SomeService)` directly) but never drives the actual intake/command path the app uses in production — so a wiring defect (a DI two-instance split; a service that never stamped required fields; a module that fails to boot when imported standalone) stays invisible until the *next* story drives the full path. When validating a story's tests, check that at least one e2e goes through the genuine entry point (the pipeline / command / HTTP-or-message-queue intake), and that the test module boots the real module the way the app composes it (Rule 25). Why: "isolated component passes" is a weaker guarantee than "the real path works," and the gap compounds across stories.

25. **A module must be self-contained enough to boot wherever it's imported — watch for app-level-only providers.** A common boot failure: `SomeModule.forRoot()` registers a sub-module (a distributed lock, a message producer) that injects a provider (e.g. a shared client token) which is actually registered separately at the **app** level. The full app boots fine (the provider is global there), but every e2e that imports `SomeModule.forRoot()` standalone fails at module init with a "can't resolve dependencies of X" error. Fix the MODULE once — have `forRoot()` import what it needs (configured from app config, often marked global) and reconcile any double-registration with the app root module — rather than patching N e2e files. Verify the full app still boots after the reconciliation. Why: unit tests with mocked providers hide this entirely; it only surfaces under a real e2e boot, so it's exactly the class of bug Rule 23/24 exist to catch.

26. **Before adopting a library — even an org-internal or precedent-set one — verify its underlying client/runtime matches the target repo's.** A precedent ("service X already uses this lib") doesn't transfer if service X is on a different stack. Example: a shared lock library correct in spirit but depending on a different client version/family than the target repo already uses — adopting it would bundle a parallel client + connection. Check the lib's `dependencies`/`peerDependencies` (and what it imports) against the repo's installed stack; prefer a library in the SAME family the repo already standardized on (often it's already transitively present). Confirm `typecheck`/boot, not just `install` succeeding (install can succeed while two clients silently coexist). Why: a mismatched transitive client is a subtle, lasting architectural wart that compounds.

27. **Never edit a sub-repo/source file while a teammate is live and working it — check the roster + file mtime first.** The "apply the trivial fix yourself instead of round-tripping" shortcut (justified for a shut-down or genuinely-stuck agent) becomes a race if the agent is still alive and editing the same file. Before the leader touches a file a sub-agent owns: confirm the agent is shut down / idle-with-no-pending-work (team roster) AND the file isn't being actively written (recent mtime, or you just messaged the agent to fix it). If a teammate is live on it, send a Delegation Packet and let them finish; the leader edits directly only when no teammate is working that file. Why: two writers on one file corrupts work and wastes both efforts — and the "file modified since read" error is the late signal you already raced.

28. **Keep the status fields and the decision log honest as you go — there are TWO status fields, and decisions accrue fast.** (a) Every story has both a `sprint-status.yaml` entry (the orchestration truth) AND a `Status:` header line in the story `.md` (set by the creator/dev during their steps, then goes stale). At each transition — especially at commit — update BOTH; the file header is what a human reads when they open the story directly. **Re-read the story file right before you edit its `Status:` header at commit** — the dev is often *concurrently* filling its Dev Agent Record, so a stale read produces a "file modified since read" error; a quick re-read also lets you confirm the dev's record is complete before you stamp `done`. (b) Maintain a running `DECISION-LOG.md` (under the implementation-artifacts dir) and append to it on the fly: session-level choices, every per-story seam ruling you make at validation, any latent bug independent validation caught, and process corrections. **(c) On every HALT (user-directed or end-of-scope), write an explicit `Resume point:` line into the DECISION-LOG** — what's done, what's next, and any scope ruling already decided for the next unit of work. The DECISION-LOG *is* the cross-session resume artifact: a clean halt+resume (e.g. HALT after an epic, then again mid-next-epic) works precisely because the next session can read the resume point + the per-story recon already banked, and pick up without re-deriving anything. Why: the leader makes dozens of consequential calls across an epic; without an on-the-fly log they're invisible to the user and unreviewable later, a stale story header silently misleads anyone reading it, and a resume without a recorded resume-point re-litigates settled decisions.

29. **A sub-agent's "green" must be reproducible from a CLEAN invocation — verify it yourself in a clean shell, not a warm/ambient one.** Independent re-runs routinely catch a non-reproducible green whose root cause is not bad logic but a pass that depended on **ambient state the leader's clean re-run didn't share**: a stray shell env var (the e2e only passed because the dev's shell had it set; a clean checkout/CI failed), a *warm* message broker (the suite passed second in an ordering but failed as the first cold-boot suite), an already-seeded DB. When you re-run a sub-agent's e2e for the backstop, strip the ambient: run from a fresh shell, unset inherited env that matters (`env -u SOME_VAR …`), and from a cold infra state. If your clean run disagrees with the dev's, the dev's pass was ambient — the fix is to make the test *self-contained* (a dedicated script that sets its own flags and loads its own `.env.test`), not to accept the ambient pass. Why: "passes on my machine" is precisely the failure CI surfaces; the authoritative check is one that carries its own preconditions.

30. **Use the project's ATOMIC e2e command for the authoritative verdict — never hand-juggle infra up/down or run overlapping Docker cycles.** The atomic command (a `test:e2e:docker`-style target and friends) owns its own `up → test → down`. Trying to *isolate* a cold-start flake by running several overlapping `infra:up`/`down` cycles + manual test runs against the same broker/ports produces **false failures** (a timeout run where even a known-green suite "failed" is pure self-induced contention) and burns real time chasing a non-bug. Discipline: (a) one atomic e2e at a time; confirm no leftover containers (`docker ps | grep e2e-test` empty) before starting; (b) for the authoritative result run the FULL suite via the atomic command (a cherry-picked subset changes which suite hits the cold broker first and can spuriously trip a cold-start race); (c) if a flake is suspected, re-run the same atomic command ONCE clean rather than dissecting it with manual infra commands; (d) **capture the full run to a file** (`<atomic e2e command> > /tmp/e2e.log 2>&1`) rather than piping through `| tail -N` — when a suite fails you need the full `PASS/FAIL test/...` list to name the failer, and a tail truncates exactly the lines you need, forcing a wasteful re-run. Pair with Rule 29: contention is just another ambient-state difference. (Note: per a user directive, some services may be designated **skip-e2e** — unit + quality only; honor any such per-repo directive in the DECISION-LOG and don't block those stories on e2e.)

31. **Recon the design docs against the REAL codebase before writing the story/code — when they drift, build reality and (leader) fix the doc.** Project conventions say "align to the design," but design docs routinely go *wrong about mechanism* once code exists — a file path the real loader doesn't scan (the convention moved, but the doc didn't), a composition/transport mechanism the repo doesn't actually use (the doc names a generic library; the repo wired a specific adapter pattern), a contract the installed code contradicts (a config-edge case the doc never anticipated breaks a shared util). The pattern that worked: the story-creator *empirically verifies* the contract against installed code (grep the loader, `diff` the generated artifacts, compose the real thing) and surfaces the drift; the leader **verifies the drift itself** (never on the agent's word — read the real module), rules to **build the reality**, and **owns the doc correction** (planning docs aren't the dev's to edit — fix the design doc post-commit). Why: a story built to a wrong doc compiles but mis-wires; catching the drift at recon is far cheaper than at the next story's seam.

32. **A pre-existing repo-infra gap is NOT the current story's failure — verify the claim, self-contain the new test, log the gap as tech-debt.** A dev may correctly *stop to flag* a blocker that turns out to be a pre-existing breakage: e.g. a service's `test:e2e` that can't even compile (it imports a config module + a migration chain deleted in a prior refactor), or a repo that has **never run a component test** (its test setup references an API the testing library has since dropped, or a dependency is ESM-only and untransformed by the existing config). The leader's move: (a) **verify the breakage yourself** (Rule 23 discipline — don't trust "it's broken" any more than "it works"; grep for the missing imports, run it); (b) if genuinely pre-existing, rule to **build a self-contained test** (an in-process stub + a minimal `.env.test`; or enable the missing test infra) that satisfies the AC's *intent* without reviving the broken scaffolding; (c) **do not let it block the story** — log it as repo tech-debt for the retro. Why: forcing the story to fix unrelated repo rot expands scope unboundedly; a self-contained test proves the new behavior and the gap is tracked separately.

33. **When a story must touch SHARED code, the leader independently runs the FULL existing suite as the blast-radius proof before approving.** A story sometimes crosses the usual "mirror the existing module, change nothing shared" boundary for a *justified* reason: a shared parsing utility with a latent bug on an input shape no existing caller uses yet, or a repo's test config that was never wired for a new test type the story needs. Each is a legitimate shared change — but shared means *every consumer is in the blast radius*. Before approving, the leader applies the exact change and runs the **whole** existing test suite himself (not just the new tests) — every pre-existing test must stay green despite the shared edit (even a *global* config addition). Only a green full-suite proves the shared edit is backward-compatible. Require the change be minimal + provably back-compat (e.g. the new branch is a no-op for the existing/common path), and have the dev add a unit cell asserting the unchanged case. Why: a shared edit that "fixes my case" can silently regress the other N consumers; the full-suite re-run is the only honest proof, and it's the leader's to run.

34. **For any repo whose `format` script globs the whole tree, tell the dev UP FRONT to format only touched paths — never run the repo-wide `npm run format`.** A frequent process failure: a repo's `npm run format` (or a `lint --fix` with a broad glob) reformats dozens of *committed, unrelated* files — e.g. a single story churning dozens of files (unrelated test specs, committed DB-migration files, including large pure-reformat diffs) — all pure formatter noise (quotes/indent/semicolons), zero functional change. Rule 21 *catches* this at commit (diff the working tree, `git checkout --` the churn), but the catch costs a full revert round-trip with the dev. **Prevent it instead:** at first touch of a target repo, check its `package.json` `format`/`lint` scripts; if the glob is repo-wide (`./**/*`, or `{src,test}/**/*` *without* a path filter), the Delegation Packet's _Specific actions_ must say verbatim: *"format ONLY the files you touched — `npx prettier --write <space-separated touched paths>` — NEVER `npm run format` (its glob is repo-wide)."* A narrowly-scoped format script (one that only globs the story's own area, like a per-module path) doesn't need the warning. Why: prevention is one sentence in the packet; the cure is a revert round-trip plus the risk the churn ships if Rule 21's scan misses it under a large diff.

35. **A pure / single-unit fold cannot write across aggregate boundaries — anticipate this fork class, and route cross-entity writes through the command/orchestration layer.** A recurring architectural trap in event-sourced / aggregate-based designs: a design doc describes a state change happening "on the child / target / other entity" inside a *pure single-entity* computation (a fold on one aggregate, a reducer on one record, a pure handler) — but a pure unit only sees and mutates *its own* state, built from *its own* history. It cannot reach another entity's state (no cross-read) nor write it. Typical instances: (a) a split/combine event keyed on the parent aggregate described as "the child's processor resolves the reciprocal" / "each child settles" — impossible, the event only lands on and folds the parent; (b) a reciprocal relation on a *target* aggregate can't be written by the *source* aggregate's fold. **The settled pattern (write it into the design once and reuse it): pure folds do single-entity work + leave a durable marker (a `pendingX[]` field, a relation, a flag); all genuine cross-entity writes go through the COMMAND / orchestration layer** (a handler that dispatches a second command at the target, or an intake/usecase that reacts to the committed result and dispatches follow-ups) — never from inside the fold (folds emit effects/intents, not commands). When a story's design says "do X to the *other* entity in the fold," **stop and rule** — that's a cross-aggregate write, not a fold step. Have the dev *escalate* it (Rule 36) rather than force an impure cross-read. Why: forcing a cross-entity read/write into a pure unit either doesn't compile, silently mis-wires, or (worse) passes a fabricated test (Rule 37) and breaks at the next story's seam. Recognizing the boundary up front turns a multi-round design-fix into a one-line ruling.

36. **On a cross-cutting or architectural fork, the dev MUST ask-and-wait; the leader rules from VERIFIED reality — this is the cheapest path, not a delay.** The stories that go cleanest are the ones where the dev *stops and asks* on a genuine fork (how does the child-side reciprocal get written? which event settles a combine child? where does the orchestration trigger live?) instead of guessing — and the leader resolves each by *reading the real code to verify the seam* (the single intake path; processors emit intents-not-commands; the command's own dedup note), then ruling with the answer pre-decided. The stories that need multiple fix rounds are ones where a cross-entity mechanism was *guessed* and built wrong. So: in every dev Delegation Packet for a story with real wiring, say verbatim *"if you hit a genuine fork on cross-entity mechanics, the orchestration trigger, or a seam the design leaves ambiguous — SendMessage me and WAIT; do not guess."* And when the dev asks, the leader **verifies the relevant real code before ruling** (Rule 31 discipline applied to the fork, not just the story) and writes the ruling into the DECISION-LOG + the story ACs so it's durable. Encourage parallelism: the dev builds the *unambiguous* ACs while waiting on the fork ruling. Why: a wrong guess on cross-cutting mechanics costs a full fix round (often two) plus a stale test; a 2-message fork ruling costs minutes. Ask-and-wait is a feature of a well-run loop, not friction.

37. **Review the e2e for FABRICATED delivery — a test that hand-synthesizes an event N times (or seeds a shape production never emits) to make an assertion pass is a silent false-green.** Distinct from Rule 24 (isolated-component-vs-real-path): here the test *does* drive the real seam, but feeds it a **delivery shape the production pipeline will never produce**. A representative case: a combine e2e that publishes the same event **multiple times** (once per child + once to the parent) so a child-settle branch fires — but production emits *one* event keyed on the parent only, so the children would never receive it; the repeated publish fabricates a fan-out that doesn't exist. The test is green and the code is wrong. When reviewing a story's e2e, check: does each event get published the way the *real upstream* emits it (same key, same cardinality, one message per real occurrence)? If the test publishes an event multiple times or to correlations the real keying wouldn't reach, that's a red flag — the assertion is testing a fiction. Pair this with Rule 35: the *reason* the dev fabricated the delivery is usually that the real single-event path can't do what the design asked (a cross-aggregate write) — so the fabrication is a symptom pointing at the design fork. Why: a fabricated-delivery green is more dangerous than a red, because it ships a broken mechanism with a passing test guarding it.

38. **A "pre-existing flake / unrelated failure" attribution is itself an unverified claim — re-run independently and confirm it really is the known flake (and not a regression you just introduced).** A dev may report a story `review` with a note like "suite X has 2 pre-existing failures, unrelated to my story" — but if the harness flake that suite *used* to have was already fixed, and the dev's checkout has the fix, the leader's independent clean cold run may show that suite GREEN: the attribution was simply wrong (a transient on the dev's machine, or a stale memory of the old flake). Treat *every* failure-attribution from a sub-agent — "flake," "pre-existing," "unrelated," "environment" — with the same skepticism as a self-reported green (Rule 23): verify it yourself. The danger is the opposite of a false-green: a *real regression your story introduced* gets dismissed as "the known flake" and ships. Especially scrutinize the claim when (a) you recently fixed that exact flake, or (b) the story touched code the "unrelated" suite's app boots (a shared module, an intake usecase, a DI wiring). Why: "it's just the flaky suite" is the most comfortable and most dangerous thing to believe — it's how a genuine regression hides behind a reputation.

39. **Fix recurring infra/harness flakiness at the FIRST sighting — tolerating it taxes every subsequent story; a one-time root-cause fix pays for itself fast.** A representative case: a cold-start message-broker leadership flake (a rotating subset of e2e suites failing because the app's consumer subscribed before the broker finished leader election) *tolerated* across an epic boundary — noticed and worked-around story after story (re-runs, judgment calls on "is this real or the flake," self-induced contention while diagnosing) before finally being root-caused and fixed (pre-create every inbound topic and wait for leaders before starting the app's consumers). The fix was a few dozen lines in the shared harness and made the full suite reproducibly green for the rest of the run, removing a per-story tax. The lesson: when a flake recurs across **two** stories, stop absorbing it and fix the root cause — a flaky gate isn't just slow, it *erodes the signal* (Rule 38: you start dismissing real failures as "the flake"). Surface it to the user as a focused fix between stories (it's often a small, self-contained harness change), or log it as the top retro item and gate the next epic on it (Rule 11). A reliable gate is a force-multiplier on every story after it. Why: the cost of the flake is paid N times (once per story) and compounds via mis-attribution; the cost of the fix is paid once.

> Note on `sprint-status.yaml`: re-read it after every Phase 4 sub-agent report. It's the ground truth for "what step are we on" and surviving crash-resume (and, per Rule 19, the truth about whether a lagging agent actually engaged). (Not a numbered rule because every Phase 4 step in `flows/phase-4.md` already calls this out at the point of use.)

> Note on append-vs-regenerate when adding an epic to an in-flight project: workflows like `bmad-create-epics-and-stories` are built to (re)generate `epics.md` from a template — which would **clobber existing epics**. When the project already has committed epics and you're adding one (e.g. a new security/remediation epic), do NOT run the from-scratch generator over the live file. Append the new epic to `epics.md` in the established template, add its FRs/NFRs to the PRD, and add its entries to `sprint-status.yaml` directly (the precedent earlier epics were folded in with). Recognize this fork before invoking the skill.

---

## Where to read next

- `modes/<your-chosen-mode>.md` — how to execute steps in your mode (sub-agent spawning, lifecycle, when to reuse).
- `flows/phase-4.md` or `flows/quick-flow.md` — the actual step-by-step.
- `references/delegation-packet.md` — handoff template + examples.
- `references/escalation.md` — tier 2/3 details.
- `references/functional-validation.md` — light vs full validation, project-type detection.
- `references/guides/` — project-type-specific validation playbooks (read on-demand).
- `scripts/context-usage.py` — measure a persistent sub-agent's actual context usage from its session transcript. Run between stories to decide keep-alive vs compact vs respawn. See Critical Rule #18 and `modes/team-persistent.md` → "Context-budget check between stories".
