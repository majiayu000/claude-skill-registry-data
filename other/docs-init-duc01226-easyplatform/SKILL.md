---
name: docs-init
version: 2.0.0
description: '[Documentation] Use when you need to initialize project reference docs via hook + scan skills.'
disable-model-invocation: false
---

## Quick Summary

**Goal:** Initialize project reference documentation by verifying the `session-init-docs.cjs` hook has created placeholder files, then running scan skills to populate them.

**Workflow:**

1. **Verify** -- Check that `session-init-docs.cjs` hook has created placeholder docs in `docs/`
2. **List** -- Show which reference docs exist and which are still placeholders
3. **Populate** -- Ask user which scan skills to run (or run all)

**Key Rules:**

- Let the hook create placeholders automatically -- do not create docs manually
- Each reference doc has a corresponding `/scan-*` skill that populates it
- Scan skills do deep codebase scanning; expect 5-15 min per skill

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Step 1: Verify Reference Doc Stubs

Check that `session-init-docs.cjs` has created the project reference docs declared for the project:

1. Read `docs/project-config.json` and use `referenceDocs[*].filename` as the source of truth.
2. If `referenceDocs` is empty or missing, use `DEFAULT_REFERENCE_DOCS` from `.claude/hooks/lib/session-init-helpers.cjs`.
3. Do not manually add missing `docs/project-reference/` files. Add or correct the project config/template entry first, then rerun the session-init/docs-init path.

Common mappings when configured:

```
docs/project-reference/project-structure-reference.md     -> /scan --target=project-structure
docs/project-reference/backend-patterns-reference.md      -> /scan --target=backend-patterns
docs/project-reference/seed-test-data-reference.md       -> /scan --target=seed-test-data
docs/project-reference/frontend-patterns-reference.md     -> /scan --target=frontend-patterns
docs/project-reference/integration-test-reference.md      -> /scan --target=integration-tests
docs/project-reference/feature-spec-reference.md          -> /scan --target=feature-spec
docs/project-reference/spec-system-reference.md           -> static template (no scan skill)
docs/project-reference/spec-principles.md                -> static template (no scan skill)
docs/project-reference/workflow-spec-test-code-cycle-reference.md -> static template (no scan skill)
docs/project-reference/code-review-rules.md              -> /scan --target=code-review-rules
docs/project-reference/scss-styling-guide.md             -> /scan --target=scss-styling
docs/project-reference/design-system/README.md           -> /scan --target=design-system
docs/project-reference/e2e-test-reference.md             -> /scan --target=e2e-tests
docs/project-reference/domain-entities-reference.md      -> /scan --target=domain-entities
docs/project-reference/docs-index-reference.md           -> /scan --target=docs-index
docs/project-reference/lessons.md                        -> /learn (managed separately)
```

If configured files are missing, the hook should create them on next prompt/session start. Verify by checking `docs/project-reference/` against the configured filenames.

## Step 2: Detect Placeholder vs Populated

Read the first 512 bytes of each file. If it contains `<!-- Fill in your project's details below. -->`, it is still a placeholder and needs scanning.

## Step 3: Offer Scan Options

Use `AskUserQuestion` to present:

1. **"Run /claude-md-init + all configured scan skills" (Recommended for first-time init)** -- Generates CLAUDE.md from config, then runs scan skills for configured docs
2. **"Run configured scan skills only"** -- Runs scan skills without CLAUDE.md generation
3. **"Select specific skills"** -- Let user choose which ones to run
4. **"Skip -- docs are already populated"** -- Exit if all docs have content

For each selected scan target, invoke it via the Skill tool (e.g., `/scan --target=backend-patterns`).

## Step 4: M1-M5/M7 Compliance Gate (BLOCKING)

See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria. After the scan skills generate/populate the reference docs, gate the generated output:

- **M1/M2 — tech-agnostic prose:** Spec/feature-facing docs (and any populated `spec-principles.md` extension) keep narrative and headings free of framework/product/language/design-pattern names and source identifiers; those appear only in evidence carriers (`[Source: namespace/service/id]`, `**Evidence**`), frontmatter, and Mermaid. Authority: `docs/project-reference/spec-principles.md` §3.
- **M3 — logical-IDs-first:** Where docs carry requirements/rules/TCs, the logical IDs (`FR-`/`BR-`/`OP-`/`TC-`) are the primary spine and `[Source: namespace/service/id]` (a stack-portable abstract anchor — never physical code coordinates or repository-root paths; physical coords live only in the provenance sidecar) is the secondary carrier.
- **M4/M5 — implementability:** Generated content is testable, observable, one-interpretation, and sufficient to rebuild the described behavior on any stack.
- **M7 — business-visibility:** Where generated docs carry business-tree cases or TCs, apply the demo test to each case's BODY: _"what would a stakeholder SEE change?"_ — no answer → FAIL as TECHNICAL-ONLY. Every `Given` = a state a user could arrange; every `When` = an action a user could take; every `Then` = an outcome a user could see. FAIL a `When` that is an invocation (a handler runs, a consumer receives, a job fires, data syncs) or a `Then` asserting schema/type/nullability/call-count, and FAIL any TC count derived from an architecture inventory. Judge the BODY, never the title or ID.

> **M1 vs M7 — distinct gates.** M1 governs **vocabulary**; M7 governs **subject matter**. A technical case in impeccably tech-free prose satisfies M1 while violating M7 — that gap is the most common way business specs rot. Ask what a user could SEE, not which words were used.

**Verification step (run after generation):** Run the exact SDD compliance verifier documented by the project and resolve any failures before declaring init complete. Do not invent a verifier command; if the verifier or project config is not yet initialized, record that and re-run once available.

## Configuration

Reference doc definitions are in `docs/project-config.json` under `referenceDocs`. The hook reads this config to determine which files to create. Static local-extension docs use `.claude/templates/reference-docs/` templates. See `.claude/hooks/session-init-docs.cjs` for the full implementation.

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Critical Thinking:** Apply critical + sequential thinking; cite proof, confidence >80% to act.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
