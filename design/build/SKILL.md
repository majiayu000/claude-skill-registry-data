---
name: build
description: Use this skill during Phase 4 implementation whenever Claude is about to write or modify code. Validates the work item (requirement ID for new builds, issue ticket for fixes, signed CR for change requests), enforces surgical-edit discipline against the plan's in-scope list, validates code against the tech spec and architecture, validates frontend output against UX specs, and generates unit tests ONLY for functions actually modified in the diff. Coordinates with the surgical-edit, minimal-code, and security-review skills. Triggered by any Edit/Write tool call when a plan file exists.
config_requirements:
  - key: formatter.command
    required: false
    on_skip: skip_format_step
  - key: linter.command
    required: false
    on_skip: skip_lint_step
  - key: test_runner.command
    required: false
    on_skip: skip_test_execution
next_suggestions:
  - when: build_gate_signed
    suggest: "run /test to execute tests and record defects"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /test when all roles are covered"
---

# Build (Phase 4)

Implement from approved plans and specs with surgical edits and work-item traceability.

## Prerequisite

`.claude/sdlc/gates/design-<task-slug>.md` must exist and be signed. (For fixes under the `/fix --fast` path, a compressed gate is acceptable — see `commands/fix-fast.md`.)

## Step 1 — Validate the work item

Before any Edit/Write, confirm based on the plan's classification:

- **New build** → the code change must reference at least one `REQ-<n>` ID from `.claude/sdlc/requirements/<task-slug>.md`. If none, halt and ask.
- **Fix** → the change must reference an issue ticket. Detect the ticket system from `.claude/sdlc/env.json`:
  - GitHub/GitLab/Bitbucket Issues → require an issue URL or number
  - Jira/Linear (via MCP) → require an issue key
  - No ticket system detected → require a local ticket file under `.claude/sdlc/tickets/` using `templates/ticket.md`
- **Change request** → the change must reference a CR with a sign-off artifact under `.claude/sdlc/sign-offs/CR-<n>.md`. No sign-off → halt.

The `work-item-validation.sh` hook enforces this at the tool level.

## Step 2 — Implement with surgical-edit discipline

Delegate the *how* of editing to the `surgical-edit` skill, which enforces:

- Smallest diff that satisfies the plan
- Only files in the plan's in-scope list
- Only functions in the plan's in-scope list (no adjacent-function edits)
- No speculative refactoring, renaming, or "while I'm here" cleanups
- Unrelated bugs → `.claude/sdlc/followups/<task-slug>.md`, not fixed in this change

The `diff-scope-check.sh` and `adjacent-function-detector.sh` hooks enforce these post-write.

## Step 3 — Validate against specs

After writing, run a conformance pass:

- Code shape matches the tech spec (API signatures, error modes, side effects)
- NFRs addressed (or explicitly deferred with justification)
- Security controls from the security architecture are in place for the modified surface

If the build touched a frontend surface, run the UX conformance checklist against the rendered UI (screenshots live under `.claude/sdlc/test/ux/`).

## Step 4 — Unit tests for MODIFIED CODE ONLY

Extract the list of functions modified from `git diff`. For each modified function:

- Add or update its unit test(s) under `.claude/sdlc/test-scripts/` (mirroring source tree)
- Tests reference the test cases from Design and, through them, the REQ IDs

Do **not** rewrite tests for unmodified functions. The `modified-code-test-gate.sh` hook verifies the test-to-function mapping.

## Step 5 — Deployment scripts and pipeline

If the change requires:

- New env var → update the deployment script and the pipeline config in the same commit
- New secret → update the secrets management doc and the pipeline; never commit the secret
- New service, queue, bucket → update infra-as-code
- New test gate → update the pipeline

Deployment updates ride with the code change. Never defer.

## Human gate

Summarize: files modified, functions modified, tests added/updated, pipeline changes, UX conformance status. Sign-off goes to `.claude/sdlc/gates/build-<task-slug>.md`.

## References

- `skills/surgical-edit/SKILL.md`
- `skills/minimal-code/SKILL.md`
- `skills/security-review/SKILL.md`
- `hooks/work-item-validation.sh`, `hooks/diff-scope-check.sh`, `hooks/adjacent-function-detector.sh`, `hooks/modified-code-test-gate.sh`
- `templates/ticket.md`, `templates/change-request.md`, `templates/sign-off.md`

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'build_gate_signed|run /test to execute tests and record defects' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /test when all roles are covered' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
