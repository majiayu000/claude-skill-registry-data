---
name: prompt-builder
description: Generates copy-paste-ready ChefFlow build prompts from raw ideas using repo-grounded context, build-queue rules, domain docs, current workspace state, and Codex readiness data. Use when the user asks to make a prompt, turn a brain dump into a Codex prompt, create a build prompt, prime an agent, or prepare a serious build agent without implementing.
---

# Prompt Builder

## Purpose

Turn a raw ChefFlow idea into a repo-grounded prompt the user can copy and paste into a fresh Codex or build-agent chat.

This skill does not implement app code. It writes the final prompt in chat.

## Required Context

Before writing the prompt, inspect only the context needed for the idea:

1. Read `AGENTS.md`.
2. Run `git status --short`.
3. Read `.claude/skills/omninet/SKILL.md` when present.
4. Read build-queue contracts:
   - `.agents/skills/build-queue/references/QUEUE-FORMAT.md`
   - `.agents/build-queue/context-freshness.md`
   - `.agents/build-queue/run-lifecycle.md`
   - `.agents/build-queue/role-domain-matrix.md`
   - `.agents/build-queue/domain-orchestration.md`
   - `.agents/build-queue/build-observability.md`
5. Refresh the Codex readiness brief when useful:
   - Prefer `npm run codex:brief`.
   - Fallback: `node scripts/codex-readiness.mjs`.
   - Then read `docs/.codex-workspace-brief.md`.
6. Check current queue state:
   - `node .agents/skills/build-queue/scripts/build-queue.mjs status`
   - `node .agents/skills/build-queue/scripts/build-queue.mjs domain-plan --status active`
   - `node .agents/skills/build-queue/scripts/build-queue.mjs workspace`
7. Read only relevant domain docs, queue items, specs, or current code files needed to name real files, routes, modules, or constraints.

## Prompt Modes

Choose one mode:

- **Spec Questions Prompt:** Use when the idea is not build-ready.
- **Queue Item Draft Prompt:** Use when the idea is mostly shaped but should be queued, not built.
- **Fire-Ready Build Prompt:** Use only when the user explicitly authorizes execution with ChefFlow firing language.
- **Prompt QA:** Use when the user asks to review, lint, score, or improve an existing generated prompt.
- **Prompt Repair:** Use when an existing prompt is weak but should be converted into a safe ChefFlow prompt.
- **Context Pack:** Use when a fired run needs one repo-grounded handoff file for build agents.
- **Prompt Archive:** Use when a generated prompt should be saved for reuse or later audit.
- **Prompt Debrief:** Use after a build report to identify prompt gaps that caused misses, assumptions, or weak proof.
- **Prompt Manifest:** Use when a serious run needs a single chain of custody from raw idea through debrief.
- **Collision Preflight:** Use before parallel or fired work to identify dirty-workspace and queue file collisions.
- **Verification Recommender:** Use when a prompt needs focused verification commands based on likely changed files.
- **Security Appendix:** Use when the prompt touches routes, server actions, API routes, database queries, tenant data, admin, or protected surfaces.

When unsure, default to **Spec Questions Prompt**.

Detailed mode templates live in [REFERENCE.md](REFERENCE.md). Concrete examples live in [EXAMPLES.md](EXAMPLES.md).

## Output Rule

The final answer must contain a single fenced block labeled exactly:

```text
COPY-PASTE PROMPT
...
```

Keep any explanation outside the fenced block to at most three bullets. If the user asks for only the prompt, output only the fenced block.

Do not create queue items, fire work, edit app code, or run implementation unless the user explicitly asks for that separate action.

For Prompt QA, use `npm run prompt:lint -- --file <path>` or pipe prompt text with `node scripts/prompt-lint.mjs --stdin`. Use `--strict` when the prompt must fail on missing safeguards.

For Prompt Repair, use:

```powershell
npm run prompt:lint -- --file <path> --repair-template
```

For run context packs, use:

```powershell
npm run prompt:context-pack -- --run <RUN-ID> --ids <BQ-ID-1>,<BQ-ID-2>
```

For prompt archives, use:

```powershell
npm run prompt:archive -- --file <prompt.md> --run <RUN-ID> --slug <short-slug>
```

For prompt debriefs, use:

```powershell
npm run prompt:debrief -- --report <final-report.md> --prompt <prompt.md>
```

For prompt manifests, collision preflight, verification recommendations, and security appendix checks, use:

```powershell
npm run prompt:manifest -- --run <RUN-ID> --prompt <prompt.md> --queue-ids <BQ-ID-1>,<BQ-ID-2>
npm run prompt:preflight -- --prompt <prompt.md> --queue-files <queue-item-1.md>,<queue-item-2.md>
npm run prompt:verify -- --file <prompt.md>
npm run prompt:security -- --file <prompt.md>
```

## Required Prompt Contents

Every generated prompt must include:

- Raw user idea, preserved.
- Objective.
- Canonical context files to read.
- Queue/build rules from `AGENTS.md`.
- Current dirty-workspace warning when `git status --short` is not clean.
- Current active, in-flight, blocked, or related done queue overlap.
- Product domain/module.
- Existing systems/files likely involved, with real paths when verified.
- Scope and out of scope.
- Role/privacy matrix.
- Security, auth, tenant-scoping, server action, API, and route-policy requirements.
- Acceptance criteria.
- Risks, dependencies, and likely file collisions.
- Verification and proof-pack requirements.
- Required final report shape.
- Instruction not to invent files or rely on stale docs without inspecting current code.

For serious or broad builds, require build-queue fire with a run ID, a run context pack, non-overlapping file ownership, wave plan, runtime proof, proof pack, and `build-queue.mjs finish-check`.

## Quality Bar

The generated prompt should be concrete enough that a fresh agent can act without rediscovering the whole repo, but narrow enough to avoid bloated context. Prefer exact paths, queue IDs, route names, test names, and file ownership over generic advice.

If the prompt is serious enough to paste into a fresh build agent, lint it or repair it first. If the prompt is fire-ready, generate or require a context pack, run collision preflight, add the security appendix when relevant, archive the prompt under the run, and create a prompt manifest.
