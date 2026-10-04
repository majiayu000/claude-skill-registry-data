---
name: auto-research
description: Improve any existing Claude Code skill, CLAUDE.md, subagent definition, slash-command, or prompt markdown file by combining web-researched best-practice rewrites with autonomous Karpathy-style binary eval loops. Use when the user wants to "auto-research", "self-improve", "auto-improve", "optimize", "modernize", or "research-improve" any existing SKILL.md, CLAUDE.md, agent file under .claude/agents/, slash-command file under .claude/commands/, or any prompt markdown file. Triggers on phrases like "use auto-research to improve skill X", "auto-improve this CLAUDE.md", "research best practices and rewrite Y", or "self-research and optimize this agent". Researches authoritative sources (Anthropic docs, anthropic.com engineering blog, anthropics/skills GitHub) in parallel sub-agents, proposes a cited rewrite, runs an autonomous binary-assertion eval loop with git commit and reset bookkeeping for testable artifacts, and asks the user to confirm only at the end with a before-and-after score and full source list.
---

# Auto-Research

Improve a target prompt artifact (SKILL.md, CLAUDE.md, subagent definition, slash-command, or generic prompt markdown) by:

1. **Detecting** the artifact type and the rules that apply to it
2. **Researching** current authoritative best practices in parallel — every claim cited
3. **Proposing** a rewrite with per-change rationale and source URLs
4. **Validating** the rewrite — for testable artifacts, an autonomous Karpathy-style binary-assertion eval loop with git commit/reset bookkeeping; for non-testable artifacts, deterministic format validation
5. **Confirming** once at the very end with a before/after score table, the diff, and the cited sources — only the user's explicit "yes" causes the final write

Run autonomously between steps 1 and 4. Stop only at step 5.

---

## Phase 0 — Read Inputs and Set Up Workspace

The user will name a target artifact (a path, or a phrase like "my copywriting skill" — resolve it). Resolution rules:

- If a path is given, use it.
- If a skill name is given, search `.claude/skills/<name>/SKILL.md` (project) then `~/.claude/skills/<name>/SKILL.md` (user).
- If "this CLAUDE.md" or similar, use the most-specific one in the current working directory tree (project > user).

Then:

1. **Read** the target artifact in full.
2. **Classify** it via [references/artifact-types.md](references/artifact-types.md): SKILL.md / CLAUDE.md / subagent / slash-command / generic-prompt.
3. **Set up the workspace** — a sibling directory `.auto-research/<target-name>/` next to the target. If the target's parent directory is not under `git`, run `git init` there so commit/reset bookkeeping works locally. (If the user's project root has its own git repo and the target lives inside it, use the existing repo — do NOT init a sub-repo.)
4. **Capture baseline** — copy the original artifact to `.auto-research/<target-name>/iteration-0/baseline.md` and record git rev (`git rev-parse HEAD` if available, else "untracked").
5. **Create `iterations.tsv`** with columns: `iter | hypothesis | score_before | score_after | decision | git_rev | timestamp | notes`.

The whole workspace structure is documented in [references/eval-loop.md](references/eval-loop.md). Read that file when about to run the eval loop in Phase 4.

---

## Phase 1 — Extract Research Topics

Read the artifact and produce a list of **research topics** — concrete questions whose answers would let you rewrite the artifact better. Each topic must be (a) likely to have an authoritative answer on the web in 2026 and (b) directly applicable to a section, claim, or convention in the target.

Examples of well-formed topics:

- "What is the current Anthropic-recommended structure for the SKILL.md `description` field, and what are the current character limits?"
- "What are 2026 best practices for CLAUDE.md length and content selection?"
- "What `.claude/agents/*.md` frontmatter fields are currently supported, and how should `tools` be specified?"
- "What does the official skill-creator skill recommend for progressive disclosure between SKILL.md body and reference files?"
- "Which `<tool>` frontmatter field has replaced `<old-tool>` in 2026?" (only ask this if the target uses something that may be deprecated)

Anti-patterns:

- "Is this skill good?" — too vague, not researchable
- "What does Karpathy say about autoresearch?" — not directly applicable to the target rewrite

Read [references/research-strategies.md](references/research-strategies.md) for the per-artifact-type topic checklist and source authority ranking.

Output of this phase: a `research_topics` list (5–12 topics) saved to `.auto-research/<target-name>/research_topics.md`.

---

## Phase 2 — Parallel Research

For each topic, spawn a parallel sub-agent (general-purpose, model: sonnet) using the `Agent` tool. Each sub-agent must:

1. Run `WebSearch` queries (current year 2026) on the topic.
2. `WebFetch` the most authoritative results — see source authority ranking in [references/research-strategies.md](references/research-strategies.md).
3. Return a structured findings block:

```markdown
### Topic: <topic>
**Verdict:** <1–3 sentence answer>
**Evidence:**
- Quote: "..." — <URL>
- Quote: "..." — <URL>
**Confidence:** high | medium | low
**Implications for rewrite:** <1–2 sentences>
```

Spawn **all topic agents in parallel** in one message (multiple `Agent` tool calls in a single response). Wait for all to complete. If any returns "low confidence" or no source, mark that topic as **uncertain** and either drop it from the rewrite or ask one targeted clarifying research question.

Save aggregated findings to `.auto-research/<target-name>/findings.md`.

---

## Phase 3 — Propose Rewrite (Draft)

Apply the findings to produce a rewritten artifact at `.auto-research/<target-name>/iteration-1/proposal.md`.

Rules:

- Every substantive change must trace to at least one citation in `findings.md`.
- Preserve any project-specific content (German prose, custom workflows, examples) unless a cited best-practice says otherwise.
- Respect format constraints from [references/artifact-types.md](references/artifact-types.md) (line caps, frontmatter rules, etc.).
- Do **not** silently invent new sections that have no evidence backing.

Then produce a **rationale block** at `.auto-research/<target-name>/iteration-1/rationale.md`. Format per change:

```markdown
### Change: <one-line summary>
**Old:** <quoted excerpt>
**New:** <quoted excerpt>
**Why:** <1–2 sentences>
**Source:** <URL>
```

---

## Phase 4 — Validate / Eval Loop

Decide the validation strategy by artifact type. Look up the rules in [references/artifact-types.md](references/artifact-types.md) — the table there says, per type, whether the **autonomous Karpathy eval loop** is run or **only format validation**.

### 4a. Format validation (always run)

Deterministic checks before any eval loop:

- **SKILL.md**: frontmatter has `name` and `description`; description ≤ 1024 chars; body ≤ 500 lines; references one level deep only.
- **CLAUDE.md**: total ≤ 200 lines (warn, not fail, if 200–250); no nested imports beyond one level; no Windows backslash paths.
- **Subagent (.claude/agents/*.md)**: valid frontmatter (`name`, `description`, optional `tools`, `model`); description third-person, "use when …" pattern.
- **Slash-command (.claude/commands/*.md)**: optional frontmatter; reasonable length (< 200 lines); clear single purpose.
- **Generic prompt MD**: only line-count + heading-structure sanity.

If format validation fails, **fix the rewrite proposal** and re-validate before continuing. Do not advance with a malformed proposal.

### 4b. Autonomous eval loop (only for eligible types)

Eligible types per [references/artifact-types.md](references/artifact-types.md): SKILL.md (always), generic-prompt with measurable output (if user supplied test inputs).

Run the loop documented in [references/eval-loop.md](references/eval-loop.md). The reference file owns the full operational manual:

- How to generate `evals.json` with binary assertions
- The autonomous instruction block ("Be aspy, do not stop, keep looping…")
- Per-iteration: hypothesise → modify → run skill on N test prompts → score → keep (git commit) or revert (git reset) → log
- Iteration cap: 10 by default, hard-stop at 15 (quality typically degrades past that — see eval-loop.md)
- The deterministic scorer is `scripts/score_evals.py`

The loop runs **autonomously** — do **not** pause to ask the user inside the loop. Push notifications are fine; questions are not.

### 4c. Skip-eval branch

If the artifact type is in the skip-eval set (CLAUDE.md, subagent, slash-command, generic-prompt without test inputs), the score is "format-validation-only: PASS/FAIL". Do not invent eval scores.

---

## Phase 5 — Final Confirmation Gate (the only stop)

This is the **only** point at which the skill stops and asks the user. Read [references/confirmation-gate.md](references/confirmation-gate.md) for the exact report format.

Produce a single confirmation report containing:

1. **Artifact** — path, type, total lines before/after
2. **Score** — eval pass-rate before/after if eval loop ran, otherwise "format-validation only"
3. **Iterations** — table from `iterations.tsv`
4. **Sources** — every URL cited in `findings.md`, deduped
5. **Diff** — unified diff between baseline and final proposal (truncated to ~150 lines if huge; full diff in `.auto-research/<target-name>/final.diff`)

Then ask **exactly one question**: "Apply these changes to <path>? (yes / no / iterate-with-feedback)".

- **yes** → overwrite the target file with the final proposal. The git history in the workspace already has the iteration trail; copy the final commit info into `.auto-research/<target-name>/RESULT.md`.
- **no** → leave the target untouched. The workspace stays for inspection.
- **iterate-with-feedback** → take the user's free-text feedback as a new constraint, return to Phase 3 with the constraint added, run another single iteration, then re-enter Phase 5.

Do not loop indefinitely — if the user says "iterate" three times in a row without "yes", surface that explicitly and ask whether to abort.

---

## Tool & Model Guidance

- **Phase 2 (research)**: `general-purpose` sub-agents, model `sonnet`, run in parallel.
- **Phase 3 (rewrite)**: main agent (Opus). One serial pass — synthesis benefits from full context.
- **Phase 4 (eval loop)**: main agent drives the loop; spawn `general-purpose` sonnet sub-agents to *execute* the target skill on each test prompt (parallelisable per prompt within an iteration). The scorer is deterministic Python.
- **Never** allow the eval loop to modify the scoring script (`scripts/score_evals.py`) or `evals.json` — those are the locked ground truth, equivalent to Karpathy's `prepare.py`.

---

## What This Skill Deliberately Does NOT Do

- It does **not** create new skills from scratch. Use the `skill-creator` skill for that. This skill is for **improving** existing artifacts.
- It does **not** run Anthropic's full eval/benchmark/packaging pipeline. `skill-creator` already does that and is composable with this skill.
- It does **not** silently overwrite the target file. Phase 5 is mandatory.
- It does **not** rewrite a target whose research topics all came back "low confidence" — surface this and ask whether to proceed without strong evidence.
