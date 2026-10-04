---
name: feature-implement
description: Implement the IMPLEMENT stage of a feature-development task — write business logic that wires into runtime, gated by lint + tests + integration check. Loads when a task is at the scaffold→implement transition or when the operator says "implement X" / "wire up X" / "make X work".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# feature-implement

The IMPLEMENT stage skill in the feature-development methodology chain
(`document → design → scaffold → implement → test`). Write the business logic
on top of the scaffold, wire it into the existing runtime, and verify lint +
tests + integration before advancing to the test stage.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Stage transition**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: scaffold` AND `readiness: 50-80` AND scaffold-stage `Done When` items are all checked
- **Direct verb**: operator says "implement X", "code X", "wire up X", "build out X", "make X work", "now write the logic"
- **After a scaffold skill completes**: scaffold artifacts (types, configs, test stubs) exist; next move is implementation
- **Bug-fix model implement step**: bug-fix chain (`document → implement → test`) reaches its implement stage

Do NOT load when:

- Task `current_stage` is `document`, `design`, or `scaffold` (those are different skills)
- Operator says "test X" (load `feature-test` instead)
- The change is a refactor with no behavior change (load `refactor-*` skills)
- The change adds tests only (load `feature-test` or `quality-coverage`)

## Operations

This skill has 4 named operations. Each has its own Process, Quality bar, and Gotchas. Execute in order; you can stop after any operation if the next one is blocked.

### Operation 1: Plan the implementation

**Trigger**: skill loaded; current_stage is scaffold OR scaffold-complete confirmed.

**Process**:

1. Read the task file (`wiki/backlog/tasks/<task-id>.md` or equivalent) — get title, type, current_stage, readiness, Done When list, artifacts produced so far.
2. Read the design artifact (named in the task's `artifacts:` list under design stage). If missing, STOP and load `feature-plan` first — implementing without a design is a stage skip (`Never skip stages — even when told to continue`).
3. Read the scaffold artifacts (types, Protocols, configs, test stubs from scaffold stage). These define the API surface to implement.
4. List the specific files to create or modify. For each file, name **the consumer**: which existing file will import the new code? (No-orphan rule — see Gotcha 1.)
5. Present the plan to the operator and wait for "go" before writing.

**Quality bar (Operation 1 done when)**:

- [ ] Each file to write/modify has a named consumer file in `aicp/`, `tools/`, or `tests/`
- [ ] Each Done When item from the task maps to ≥1 file in the plan
- [ ] No FORBIDDEN paths per the implement stage in [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml)
- [ ] Operator approved the plan (per CLAUDE.md hard rule #6: "One step at a time. Plan → 'go' → execute")

### Operation 2: Wire to runtime

**Trigger**: Operation 1 plan approved.

**Process**:

1. Write each planned file. Maintain Python type hints on all public functions (CLAUDE.md convention). Keep modules small and single-responsibility (CLAUDE.md convention).
2. Immediately after each file: add the import in the named consumer file. **No file lands without a consumer in the same commit.**
3. For each new public class or function: add a one-line docstring explaining WHY (not what — the code shows what). Don't add docstrings just to have them.
4. Run `ruff format aicp/ tests/` after each file — keeps formatting drift out of review noise.
5. Commit one logical unit at a time (per CLAUDE.md conventional commits). Format: `feat(<scope>): <description>`. Don't batch unrelated changes.

**Quality bar (Operation 2 done when)**:

- [ ] All planned files written
- [ ] Each new file imported by ≥1 existing file (verify via `grep -r "from <new_module>" aicp/ tools/ tests/`)
- [ ] Type hints on all public function signatures
- [ ] `ruff format --check aicp/ tests/` exits 0
- [ ] One commit per logical unit (check `git log --oneline -<n>`)

### Operation 3: Verify integration

**Trigger**: Operation 2 commit(s) landed; about to advance stage.

**Process**:

1. Run `ruff check aicp/ tests/` — must exit 0. Fix violations; re-run.
2. Run `pytest tests/ -x --tb=short` — fail-fast. Fix the first failure; re-run. Repeat until exits 0.
3. Verify the integration by exercising the feature: invoke the new code via CLI (`python -m aicp.cli ...`) or via a test (`pytest tests/test_<new>.py -v`). Don't trust "tests pass" alone — confirm the feature WORKS (per OpenArms Bug 6 lesson — 2,073 lines passed tests but feature didn't work because nothing imported it).
4. Check no test files were modified (forbidden during implement; that's test stage). Run `git diff --stat tests/` — should be empty unless you added new tests for the feature.
5. Re-read the task's Done When list. Each item must map to verifiable evidence (a passing test, a CLI command output, a file existing).

**Quality bar (Operation 3 done when)**:

- [ ] `ruff check aicp/ tests/` exits 0
- [ ] `pytest tests/ -x --tb=short` exits 0
- [ ] Feature exercised end-to-end (not just tests pass)
- [ ] No unauthorized test modifications
- [ ] Every Done When item has verifiable evidence

### Operation 4: Update task state

**Trigger**: Operation 3 verifications all pass.

**Process**:

1. Open the task file (`wiki/backlog/tasks/<task-id>.md`).
2. Update frontmatter: `current_stage: test`, `readiness: 95`, append new files to `artifacts:` list.
3. Add a brief note to the task body recording: what was implemented, which files were touched, the verification commands run.
4. Commit the task update separately: `chore(backlog): T<id> implement → test`.
5. Run `python3 -m tools.lint wiki/backlog/tasks/<task-id>.md` to confirm the task page still validates.

**Quality bar (Operation 4 done when)**:

- [ ] Task frontmatter shows `current_stage: test`, `readiness: 95`
- [ ] All produced files listed in `artifacts:`
- [ ] Task lint passes (`tools/lint.py` exits 0 for the task file)
- [ ] Operator informed: "Implement done; test stage is next."

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Orphan code (OpenArms Bug 6 — most common implement failure)

Writing 100s of lines of "production code" that no existing file imports. Tests pass because the new code's own tests pass. Feature doesn't work because the production runtime never reaches the new code.

**Detection**: After writing a new file `aicp/core/<new>.py`, run:

```bash
grep -rn "from aicp.core.<new>\|import aicp.core.<new>" aicp/ tools/ tests/
```

If only the new file's own tests show up, you have an orphan. **Stop**. Either wire it into an existing entry point (router, controller, CLI subcommand, MCP tool registration) OR remove the file — orphan code is worse than no code (it ages, drifts, and confuses future maintainers).

### Gotcha 2: Stage skipping ("just one quick test fix")

You're implementing feature X. You notice an unrelated test that's been broken. Tempting to "just fix it while I'm here." This is the stage gate violation that AGENTS.md rule 10 forbids ("Stay in scope. No refactoring beyond the current task").

**The rule**: implement stage may modify business code, NOT test code (except adding tests for the new feature, in line with the feature's task spec). If you find a broken unrelated test, file it as a bug task. Do not fix it in this commit.

### Gotcha 3: Done When interpreted as suggestions

"Done When: feature works correctly." Vague Done When let the agent claim done without verification. The implement stage MUST treat each Done When as a verifiable gate. If the spec says "Done When: aicp --route returns local for simple Q&A," then the verification is `aicp --route "what is 2+2"` and confirming the response shows local backend.

**The rule**: every Done When item produces evidence (a command + its output, a file path, a test). If you cannot produce evidence, the item is not done — go back to Operation 3.

### Gotcha 4: Implementing without a design artifact

The feature-development chain is `document → design → scaffold → implement → test`. Implement assumes design + scaffold both produced their artifacts. If the design doc is missing or incomplete, you're implementing the wrong thing or implementing without alignment.

**The rule**: if the design artifact named in the task's `artifacts:` doesn't exist, STOP. Load `feature-plan` (or `architecture-propose` for larger scope) and complete the design stage first. Don't improvise.

### Gotcha 5: "Refactor while implementing" temptation

The new feature touches existing code. The existing code has a quirk you'd like to clean up. Tempting to refactor "while you're here." This conflates implement (add behavior) with refactor (restructure without behavior change), violating CLAUDE.md hard rule 10.

**The rule**: if a refactor would help, file it as a separate refactor task with its own design+scaffold+implement+test. Implement the feature on the existing structure. The new feature lands; the refactor lands later if it earns its place.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. See [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for the implement-stage gate commands (ruff check + ruff format --check + pytest -x), path patterns, and integration requirements.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-plan | document/design stage of a feature | Designs the feature; doesn't write code |
| feature-test | test stage after implement | Adds tests + verifies coverage; implement stage adds tests for the new feature only |
| feature-iterate | already-shipped feature, refining | Behavior changes need design first; iterate is for refinements |
| refactor-* | restructure without behavior change | Implement adds behavior; refactor doesn't |
| ops-deploy | shipping the feature to runtime | Deploy comes after implement+test, and is its own concern |
