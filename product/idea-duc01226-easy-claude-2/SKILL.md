---
name: idea
description: '[Project Management] Use when a workflow step or the user asks for an idea to be captured: ideas, feature requests, concepts for refinement.'
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Run declared skill steps in order. NEVER skip, reorder, or merge without explicit user approval.
> **[BLOCKING]** Update task tracking before/after each step or sub-skill: `in_progress` → `completed`.
> **[BLOCKING]** Completed steps need brief evidence; skipped steps need an explicit reason.
> **[BLOCKING]** If Task tools are unavailable, maintain an equivalent tracker with synchronized statuses.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

> **AI-SDD Artifact Contract (M1–M7):** Ideas stay tech-agnostic business intent; logical IDs belong downstream, and abstract `[Source: namespace/service/id]` anchors stay in a separate evidence carrier. Keep physical code coordinates and repository paths out of portable narrative.
> MUST ATTENTION READ `.claude/skills/shared/sdd-artifact-contract.md` for full mandate and carrier rules.
> **Project Protocol Overlay:** Resolve only the most-specific matching tier; derive body paths from overlay names, report malformed or missing bodies, and apply surviving rules additively without waiving framework or user-confirmation gates.
> MUST ATTENTION READ `.claude/skills/project-skill-protocol/references/registry.md` for the full resolution contract.

## Quick Summary

**Goal:** Turn a vague product idea into a validated, tech-agnostic, module-anchored backlog artifact ready for `$pbi --mode=refine` to convert into a PBI — preserving problem intent without leaking solution or stack choices.

**Summary:**

- **Purpose:** capture raw idea as structured, validated backlog artifact; preserve problem intent, keep the problem statement tech-agnostic with no solution/stack/IDs, and hand clean narrative to `$pbi --mode=refine`.
- **Main steps/tasks (run in order):** (1) Gather problem/value/users/scope; (2) Generate `IDEA-{YYMMDD}-{NNN}` draft from `idea-template.md`; (3) Capture problem/value/users; (4) Detect module by globbing `*/README.md` under the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path) silently, prompting only if ambiguous/no match; (5) Load feature context (8-12K tokens: entities, BR-/TC patterns); (6) Save canonical artifact; (6.5) **Discovery Interview** — ONE interview of 4-6 ask user tool questions; (7) **Validation Summary** — written from those answers, then ONE short unconditional ask user tool confirming the revised problem statement / scope (not a second interview); (8) Suggest `$pbi --mode=refine`.
- **Modes/gates:** Existing repo → silently detect module and load context; Greenfield → skip module detection and structure reads, use market/WebSearch context, ask business questions more often, and NEVER ask about tech stack. The Discovery Interview (Step 6.5: 4-6 questions incl. always-on testability, each category asked once) and the Validation Summary with its one confirm question (Step 7) are NON-NEGOTIABLE.
- **Output:** Persist to `ideas/{YYMMDD}-{role}-idea-{slug}.md` under the team-artifacts root (default `team-artifacts`; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides the path) with `t_shirt_size`; downstream PBI owns `FR-`/`BR-` IDs and inherits the clean narrative.

> **MANDATORY IMPORTANT MUST ATTENTION** task tracking task to READ `project-structure-reference.md` — project patterns and structure. Not found → search project documentation, coding standards, architecture docs.

**Workflow:**

1. **Gather Info** — Ask problem, value, scope, target users
2. **Generate Artifact** — Create `IDEA-YYMMDD-NNN` file from template with `draft` status
3. **Capture Details** — Record problem statement, value, target users
4. **Detect Module** — Auto-match module and load feature context from docs
5. **Load Context** — Read related module/feature docs within the 8-12K budget
6. **Save Artifact** — Persist to the canonical ideas path
6.5. **Discovery Interview** — ONE interview: ask user tool 4-6 structured questions (MANDATORY)
7. **Validation Summary** — derived from the interview answers, then ONE unconditional confirm ask user tool on the revised problem statement / scope (MANDATORY)
8. **Suggest Next** — Point to `$pbi --mode=refine` for PBI creation

**Key Rules:**

- Output: `ideas/{YYMMDD}-{role}-idea-{slug}.md` under the team-artifacts root (default `team-artifacts`; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides the path)
- Validation NEVER optional — MANDATORY.
- Auto-detect module silently; prompt only when ambiguous or no match.
- MUST ATTENTION include `t_shirt_size` (XS/S/M/L/XL) in artifact for early sizing
- **[BLOCKING] Tech-agnostic output (M1):** Keep the problem statement tech-agnostic in all modes per `spec-principles.md` §3 in the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path); name no framework/product/language/design-pattern; defer stack preference to tech research.
- **M3 Logical-ID Assignment (forward to PBI):** Ideas assign no logical IDs. When advanced via `$pbi --mode=refine`, the PBI assigns `FR-`/`BR-` IDs as the PRIMARY citation spine and carries `[Source: namespace/service/id]` abstract anchors separately from business-intent prose; never put physical code coordinates or repository-root paths in the idea. Keep problem/value narrative free of source identifiers so the PBI inherits it cleanly.

## Greenfield Mode

> **Auto-detected:** No codebase means no discovered source directories, manifest files, or populated `project-config.json`; planning artifacts (`docs/`, `plans/`, `.claude/`) don't count. Require actual code directories with content.

**Greenfield actions:**

1. Skip module detection (no modules exist yet)
2. Skip `project-structure-reference.md` (won't exist)
3. Focus on market gap, competitors, differentiation
4. Keep problem statement tech-agnostic
5. Enable WebSearch for market/competitor context
6. Increase ask user tool frequency — capture vision, constraints, team profile, scale expectations
7. **[CRITICAL] NEVER ask about tech stack during idea capture.** Stack is a research-driven decision AFTER full business analysis (business-evaluation phase); acknowledge volunteered preferences, then defer to tech-stack research.

## Detailed Workflow

### Step 1: Gather Information

- No title → ask: "What's the idea in one sentence?" Ask: "What problem does this solve?" "Who benefits from this?" "Any initial scope thoughts?"

### Step 2: Generate Artifact

- Template: `.claude/docs/team-artifacts/templates/idea-template.md` (framework-owned path — NOT the configurable team-artifacts root in `docs/project-config.json`); ID: `IDEA-{YYMMDD}-{NNN}` (sequential); status: `draft`.

### Step 3: Capture Details

- Document problem statement, expected value, and target users.

### Step 4: Detect Project Module

**Dynamic Discovery:**

1. Glob `*/README.md` under the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path); extract module names from paths; match idea keywords against module keywords.

| Scenario             | Action                                                                          |
| -------------------- | ------------------------------------------------------------------------------- |
| Clear match          | Auto-detect — NEVER show confidence levels                                      |
| Ambiguous / no match | Prompt: "Which project module?" + Glob results + "Cross-cutting/Infrastructure" |
| 2+ modules detected  | Load ALL modules, add all to `related_features`                                 |

**If module detected:**

1. Read `{module}/README.md` under the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path) (first 200 lines); extract its Quick Navigation feature list.
2. Add frontmatter: `module: {detected_module}`, `related_features: [Feature1, Feature2]`.

### Step 5: Load Feature Context

1. Read module README overview (~2K tokens); identify closest matching feature(s).
2. Read corresponding feature doc (3-5K tokens); extract related entities, existing business rules (`BR-{MOD}-XXX`), and test patterns (`TC-{FEATURE}-{NNN}`).

**Token Budget:** Target 8-12K tokens total.

### Step 6: Save Artifact

- Path: `ideas/{YYMMDD}-{role}-idea-{slug}.md` under the team-artifacts root (default `team-artifacts`; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides the path); infer role from context or ask; include detected domain context.

> **Artifact Path (canonical convention)** — Command `$idea` → base path `ideas/` inside the team-artifacts root (default `team-artifacts`; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides the path), role token `po`, type `idea`. Filename pattern: `{YYMMDD}-{role}-{type}-{slug}.md` → e.g. `260119-po-idea-dark-mode-toggle.md`. Slug = lowercased basename, non-alphanumeric → `-`, trimmed, max 50 chars.

### Step 6.5: Discovery Interview (MANDATORY — the ONE interview)

Use ask user tool for 4-6 structured questions, batched into as few calls as the tool allows; each question MUST ATTENTION have 2-4 options, one marked "(Recommended)". Every category is asked AT MOST ONCE across this skill — there is no second question round on the same category.

| Category        | Purpose                           | Example                                   |
| --------------- | --------------------------------- | ----------------------------------------- |
| Problem Clarity | Distinguish problem from solution; confirm the statement is user-focused | "What problem does this solve?" + options |
| User Persona    | Identify primary user             | "Who benefits most?" + role options       |
| Scope           | MVP vs full vision; boundaries to settle now | "What's the smallest valuable version?"   |
| Testability     | Define done?                      | "How would you verify this works?"        |
| Impact / Value  | Business value sizing             | "What value, and how many users/processes affected?" |
| Constraints     | Known blockers                    | "Any technical/business constraints?"     |
| Scale           | Expected load/growth              | "How many users/transactions expected?"   |
| Stakeholders    | Who else should review            | "Who else should review this idea?"       |

> **Greenfield:** NEVER include tech-stack questions; focus on business problem, users, scale, constraints.

**Testability Question (ALWAYS include):** "How would you verify this feature works correctly?" — Options: manual test steps, automated test criteria, metric thresholds.

Document all answers under `## Discovery Interview` (`$pbi --mode=refine` reads this section and asks only the categories it leaves unanswered).

### Step 7: Validation Summary (MANDATORY — derived summary + ONE confirm question, not a second interview)

Write `## Validation Summary` from the Discovery Interview answers: the confirmed decisions and the follow-up action items, and update the artifact from them. Then ALWAYS ask ONE short ask user tool ("Is the revised problem statement / scope right?") confirming it, whether or not the answers changed the Step 3 text; no other question is asked in this step.

**Validation Output Format:**

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed

- {decision}: {user choice}

### Action Items

- [ ] {follow-up if any}
```

### Step 8: Suggest Next Step

After capture, use ask user tool:

1. `$pbi --mode=refine` — Refine into PBI (Recommended)
2. `$spec [mode=tests]` — Jump straight to test spec
3. `$plan` — Start implementation planning

Output: "Idea captured! To refine into a PBI, run: `$pbi --mode=refine {filename}`". If detected, add: "Module context from {module} will be used during refinement."

## Output Formats

### Domain Context Section

```markdown
## Domain Context (Project Features)

### Module

{module_name}

### Related Features

- {Feature1} - [docs link]
- {Feature2} - [docs link]

### Domain Entities

- **Primary:** {Entity1}, {Entity2}
- **Related:** {Entity3}

### Existing Business Rules

- BR-{MOD}-XXX: {Brief description}
```

### UI Sketch Section

```markdown
## UI Sketch

### Layout

{Rough ASCII wireframe — see UI wireframe protocol}

### Key Components

- **{Component}** — {purpose} _(tier: common | domain-shared | page/app)_
```

> Search existing libs before proposing new components.
> Backend-only idea: `## UI Sketch` → `N/A — Backend-only change. No UI affected.`

## Examples

Paths below show the default team-artifacts root; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides it.

```bash
$idea "Dark mode toggle for settings"
# Creates: <team-artifacts root>/ideas/260119-po-idea-dark-mode-toggle.md

$idea "Add goal progress tracking notification"
# Creates with module context: <team-artifacts root>/ideas/260119-po-idea-goal-progress-notification.md
```

---

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** After completion, use ask user tool:

- **"$pbi --mode=refine (Recommended)"** — Transform idea into actionable PBI
- **"$web-research"** — Idea needs market research first
- **"Skip, continue manually"** — user decides

---

> **[IMPORTANT]** Before starting, use task tracking for small tasks, including each file read. For simple tasks, AI MUST ATTENTION ask whether to skip.

> **External Memory:** For complex/lengthy research, analysis, scans, or reviews, write intermediate findings to `tmp/reports/` — prevents context loss and preserves a deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, or recommendation needs `file:line` proof or traced evidence; confidence >80% acts, <80% verifies first.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `sequential-thinking-protocol` — Structured multi-step reasoning with revision, branch and hypothesis markers; planning, debugging or reviewing complex or ambiguous work → .claude/skills/shared/protocols/sequential-thinking-protocol.md
- `ui-wireframe` — Wireframe from the design inputs using the project's component owners; sketching a user interface → .claude/skills/shared/protocols/ui-wireframe.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** use structured reasoning for complex or ambiguous work, implicitly when visible markers would clutter. Verify hypotheses, revise assumptions, and close with confidence, assumptions, open questions and a concrete next action.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** Run declared steps in order; NEVER skip, reorder, or merge without explicit user approval.
**IMPORTANT MUST ATTENTION** Set task `in_progress` before each step/sub-skill; set `completed` after.
**IMPORTANT MUST ATTENTION** Completed steps need concise evidence; skipped steps need explicit reasons.
**IMPORTANT MUST ATTENTION** If Task tools unavailable, maintain an equivalent synchronized tracker.

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Turn a vague product idea into a validated, tech-agnostic, module-anchored backlog artifact ready for `$pbi --mode=refine` to convert into a PBI — preserving problem intent without leaking solution or stack choices.

**IMPORTANT MUST ATTENTION — Main steps (run in order, NEVER skip/reorder):** (1) Gather info; (2) Generate artifact `IDEA-{YYMMDD}-{NNN}` draft from `idea-template.md`; (3) Capture problem/value/users; (4) Detect module by globbing `*/README.md` under the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path); (5) Load feature context (8-12K budget); (6) Save to canonical path; (6.5) Discovery Interview (ONE interview, ask user tool 4-6); (7) Validation Summary derived from its answers + ONE confirm ask user tool; (8) Suggest next → `$pbi --mode=refine`. — why: AI keeps dropping the skill's own mid-pipeline steps; the interview and module detection are the most-forgotten.

**IMPORTANT MUST ATTENTION** Mode gate: existing codebase → detect module and load context; Greenfield → skip module and structure reads, use market/WebSearch context, ask business questions more often, and NEVER ask about tech stack.

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **UI Wireframe:** classify each component into ONE tier; search libs first, reuse ≥80% match.
- **AI-SDD M1–M3:** Keep idea prose tech-agnostic business intent; defer logical IDs and `[Source: ...]` carriers to the downstream PBI.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers and confidence closer.

**IMPORTANT MUST ATTENTION** Discovery Interview (Step 6.5) + Validation Summary (Step 7) NEVER optional — run the ONE ask user tool interview and the ONE Step 7 confirm question even for "simple" ideas and never re-ask a category — why: discovery uncovers hidden constraints and confirms problem framing, and a repeated question burns the PO's time.
**IMPORTANT MUST ATTENTION** ALWAYS keep problem statement tech-agnostic (M1, `spec-principles.md` §3, all modes) — name no framework/product/language/design-pattern; defer any stack preference to the later tech-research phase — why: PBI inherits the narrative cleanly downstream
**IMPORTANT MUST ATTENTION** in greenfield mode NEVER ask about tech stack — acknowledge a volunteered preference, then defer to the business-evaluation phase — why: stack is a research-driven decision after business analysis, not a capture-time guess
**IMPORTANT MUST ATTENTION** task tracking break ALL work into small tasks BEFORE starting — including a task to READ `project-structure-reference.md` (skip in greenfield — it won't exist)
**IMPORTANT MUST ATTENTION** validate all decisions with user using ask user tool — NEVER auto-decide — and NEVER show confidence levels on an auto-detected module match
**IMPORTANT MUST ATTENTION** auto-detect module silently by globbing `*/README.md` under the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path) — prompt only when ambiguous or no match; greenfield → skip module detection — why: confirm with `Glob()` evidence, not assumption
**IMPORTANT MUST ATTENTION** assign NO logical IDs (M3) — an idea is tech-agnostic business intent only; the downstream PBI owns `FR-`/`BR-` assignment and `[Source: namespace/service/id]` anchors — why: keep the problem/value narrative free of source identifiers so the PBI inherits it cleanly
**IMPORTANT MUST ATTENTION** include `t_shirt_size` (XS/S/M/L/XL) in the artifact and keep the feature-context load within the 8-12K token budget — why: early sizing feeds prioritization; over-budget reads dilute attention
**IMPORTANT MUST ATTENTION** persist to `ideas/{YYMMDD}-{role}-idea-{slug}.md` under the team-artifacts root (default `team-artifacts`; a `docsRoots.teamArtifacts.path` entry in `docs/project-config.json` overrides the path), then hand off to `$pbi --mode=refine` for PBI conversion — why: canonical path keeps downstream tooling aligned
**IMPORTANT MUST ATTENTION** search existing component libraries before proposing any new UI component (≥80% match = reuse); classify each into exactly ONE tier — why: duplicate UI code = wrong tier
**IMPORTANT MUST ATTENTION** cite `file:line` proof or traced evidence for every claim/recommendation, confidence >80% to act, <80% verify first — why: certainty without evidence is the root of hallucination
**IMPORTANT MUST ATTENTION** add a final review task to verify work quality

**Anti-Rationalization:**

| Evasion                                   | Rebuttal                                                                 |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| "Idea is simple, skip interview"          | NEVER skip — discovery uncovers hidden constraints                       |
| "Module is obvious, skip detection"       | Still run `Glob()` — confirm with evidence not assumption                |
| "Validation is redundant after interview" | ALWAYS run both — the confirm question checks the derived problem statement / scope, not a new category |
| "Greenfield check is optional"            | Auto-detect is MANDATORY — no manual override                           |
| "User mentioned a framework, capture it"  | Stay tech-agnostic — acknowledge, defer to tech-research phase           |
| "I'll assign FR-/BR- IDs now"             | NO logical IDs at idea stage — the PBI assigns them downstream           |
| "Reuse an existing component? new is faster" | Search libs first — ≥80% match = reuse; new without search = wrong tier |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

**IMPORTANT MUST ATTENTION** the 3 rules to never skip: (1) run BOTH Discovery + Validation ask user tool gates; (2) keep the problem statement tech-agnostic (no stack/IDs); (3) cite `file:line` evidence, confidence >80% to act.
