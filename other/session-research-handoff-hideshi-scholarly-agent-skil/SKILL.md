---
name: session-research-handoff
version: 2.7.0
description: Use when ending a session or resuming long-term writing to summarize and restore research context, open questions, active thought state, and pending tasks. Supports multi-paper repositories with context-aware routing. v2.6.0 adds the artifact index (INDEX.md) update responsibility. v2.7.0 adds the friction log check (friction-driven-skill-improvement integration) at handoff generation.
---

# Research Session Handoff Skill

## Purpose
Apply session handoff discipline to preserve research context, active draft state, unverified citations, active thought context, and pending literature checks across long writing sessions and AI Agent context resets. Supports multi-paper repositories by routing handoff records to the appropriate paper-specific or root-level file.

## Invariant (v2.5.0): Commit Message Language and Agent / Model Recording

> **Invariant**: **Every Git commit MUST end with `Agent:` and `Model:` lines.** Routine model traceability uses `git log` as the source of truth; §5 double-logging is not required.

### Commit message language (added in v2.5.0)

- **Write the subject and body in the executor's native language.** Follow `native_language` in `config/user_preferences.json` (e.g., if `"Japanese"`, write commit messages in Japanese).
- Applies both to commits in the target (paper-writing) repository and to scholarly-agent-skills itself.
- Machine-readable trailers such as `Agent:` / `Model:` keep English keys and values for portability.

### Required commit message footer

```text
<subject (native language)>

<body (optional; native language)>

Agent: Cursor
Model: Cursor / Composer / 2.5
```

| Field | Format | Example |
| :--- | :--- | :--- |
| **Agent** | Execution environment (IDE/CLI) | `Cursor`, `Claude Code` |
| **Model** | `Provider / Model name / Version` | `Moonshot AI / Kimi / K3` |

- **Before committing**: Complete Step 2 identity checklist (self-ID → UI → user confirmation; no guessing).
- Apply the same footer to **scholarly-agent-skills-only** commits when they support a paper project.

### §5 Session Log (exceptions only)

Use `docs/<paper-id>/design/test-cases.md` §5 **only** for:

- **Non-commit work** (external review, author oral reports, dialogue-only design review)
- **Retroactive backfill** (pre-protocol sessions without Agent/Model in commit history)
- **Optional session summaries** (narrative spanning multiple commits)

> v2.3.0 "Commit → append §5 row" is **retired in v2.4.0** to avoid hash backfill commit chains.

## Trigger Conditions
- At the end of each working session
- When the AI Agent context window limit is approaching
- When transitioning to a different chapter or research sub-topic
- When interrupting extended continuous work (hyperfocus interruption)

## Workflow

### Step 0: Hyperfocus Context Detection (S3 Principle)
When the agent detects any of the following, it must immediately propose: "Shall I save your current thought context?"

- The user explicitly requests to end or pause the session
- Extended continuous work has been taking place
- The topic shifts significantly (e.g., switching to a different paper or chapter)

### Step 1: Target File Routing (Multi-Paper Context-Aware Routing)
When managing multiple papers in a single repository, determine the target file based on the work context:

| Case | Target File | Example |
|---|---|---|
| **Single-paper focus** | `docs/<paper-id>/session-handoff.md` | Deep in Chapter 3 hypothesis testing of ADHD paper |
| **Cross-paper work** | `docs/session-handoff.md` (root) | Exploring whether Philippines paper methodology applies to ADHD paper |
| **Parallel multi-paper** | Root summary + each `docs/<paper-id>/session-handoff.md` for details | ADHD literature survey + Philippines revision simultaneously |

- **Pointer rule**: The root `docs/session-handoff.md` must **always** contain pointers to paper-specific handoff files when they exist.

### Step 2: Execution Environment Identity Verification (Pre-Recording Checklist)

Before writing `Agent:` / `Model:` lines in a **commit message**, or before logging an exception row in `test-cases.md` §5, complete the checklist below. **Do not copy the previous log row or prior commit message** — model switches can occur within the same chat.

| # | Check | Procedure |
| :-: | :--- | :--- |
| 1 | **Self-identification** | Confirm the model name from conversation context (e.g., Composer) |
| 2 | **UI verification** | If uncertain, transcribe the name exactly as shown in the tool's model selector UI |
| 3 | **User confirmation** | If still unknown, ask the user one question before recording (do not guess) |
| 4 | **Row separation** | After a model switch, always add a **new row** (no appending or overwriting existing rows) |
| 5 | **Prohibition** | Do not infer the model from a prior session log row or handoff §7 entry |

> **Typical failure (Phase 3)**: Under multi-model use, an agent copies the previous row (e.g., Kimi K3) while the actual session ran on Composer. This checklist prevents that "ungrounded recording subject" failure mode.

### Step 3: Generate Handoff Report

> **Friction log check (v2.7.0)**: before generating the handoff, check whether the friction log of [`friction-driven-skill-improvement`](../friction-driven-skill-improvement/SKILL.md) exists and how many entries it has for the current session. If missing or zero, run that skill's Step 2 retroactive reconstruction first.

#### Paper-Specific Handoff Template (`docs/<paper-id>/session-handoff.md`)

```markdown
# Research Session Handoff Report — [Paper Title / paper-id]

## 1. Current Status
- **Completed Work**: First draft of Chapter 2 "Source A Analysis and Argumentation"
- **Active File**: `docs/<paper-id>/chapters/chapter2.md`

## 2. Applied Domain Concepts
- 'Agency' definition: Applied 18th-century Enlightenment model (see `docs/<paper-id>/design/domain-concepts.md`)

## 3. Pending Issues
- [ ] Resolve conflict between Smith (2018) and Jones (2021) on the dating of Source B
- [ ] Polish transition language into Chapter 3

## 4. Resume Protocol
1. Load this file.
2. Resume from Pending Issue #1: Smith/Jones dating conflict.

## 5. Active Thought Context
- "If we interpret Source B's date using Smith's theory (1680s), it contradicts Chapter 4's argument, but Jones's theory (1710s) would be consistent" → verification not yet complete.
- Undecided: scope of "economic transition" definition for Chapter 3 opening.

## 6. Warm-Up Questions
- "Last time you were comparing Smith's and Jones's theories on Source B dating. Do you want to proceed with the Jones interpretation?"
- "Shall we finalize the scope of 'economic transition' for the Chapter 3 opening based on our previous discussion?"

## 7. Execution Environment
Always record the session's execution environment to ensure reproducibility and auditability.

- **Agent (runtime environment)**: e.g., Cursor, Claude Code, Antigravity
- **Model**: record at the granularity of "Provider / Model name / Version"
  - e.g., Cursor / Composer / 2.5, Anthropic / Claude Opus / 4.x, Google / Gemini / Flash, Moonshot AI / Kimi / K3
  - Note: agents and models are not fixed 1:1 (e.g., Antigravity can run Claude Opus or Gemini Flash). Always record them as separate fields.
  - If the exact version is unknown, record the name exactly as shown in the tool's model selector UI.
- **Date**: YYYY-MM-DD (providers may update a model under the same name — model drift — so the date serves as de facto version information)
- **Main Prompts / Instructions**: e.g., "Help me test the Chapter 3 hypothesis"
- **Related Commits**: e.g., `abc1234` (audit trail linking dialogue to artifacts)
```

#### Root Cross-Paper Handoff Template (`docs/session-handoff.md`)

```markdown
# Research Session Handoff Report — Repository Overview

## Active Papers
| Paper (paper-id) | Status | Detail File |
|---|---|---|
| `adhd-ai` | Drafting Chapter 3 | → `docs/adhd-ai/session-handoff.md` |
| `philippines-poverty` | Awaiting revision | → `docs/philippines-poverty/session-handoff.md` |

## Cross-Paper Open Items
- [ ] Whether to reference Philippines paper's "cognitive offloading" concept in ADHD paper Chapter 2
- [ ] Check for duplicate references across both papers

## Recommended Starting Point
→ Resume with `adhd-ai` Chapter 3 (closer deadline)
```

### Step 4: Resume from Handoff
At the start of a new session, the agent restores context in this order:

1. Read `docs/session-handoff.md` (root) if it exists to identify active papers.
2. Load the relevant `docs/<paper-id>/session-handoff.md`.
3. Present **Warm-Up Questions** (Section 6) to the user to facilitate thought context restoration.

## Cognitive Scaffolding
All interactions in this skill must follow the [Cognitive Scaffolding Rule](../../../rules/en/cognitive-scaffolding-rule.md) (S1–S4). S3 (Context Saving) is the core principle of this skill, prioritizing safe hyperfocus interruption and minimal context switch cost.

## Outputs
- `docs/session-handoff.md` (Root cross-paper summary)
- `docs/<paper-id>/session-handoff.md` (Paper-specific detailed handoff)

### Updating the Artifact Index (INDEX.md)
When new artifacts are created under `docs/<paper-id>/design/` during a session, update `design/INDEX.md` alongside the handoff. See the [Artifact Index & Naming Rule](../../../rules/en/artifact-index-rule.md) for categories, naming patterns, and status headers. The goal is to make "location and structure" mechanically decidable without relying on human memory; rule compliance is the agent's responsibility.
