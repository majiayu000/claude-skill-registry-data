---
name: feature-review
description: Review a completed feature against its requirements + design + acceptance criteria — verifies the assembled feature actually delivers what was specified, surfaces gaps, and authorizes status=done. Loads when a task is at test→done transition awaiting human sign-off, or when the operator says "review feature X" / "is X actually done" / "verify X meets the spec".
allowed-tools: Read, Bash, Glob, Grep
effort: high
---

# feature-review

The closing gate of the feature-development chain. Test stage produced
green tests; review verifies the FEATURE (not just the tests) meets the
spec authored at document stage. Per Methodology Standards: "99→100 is
human-only on both dimensions — adversarial review required." This skill
runs the adversarial review the operator confirms or rejects.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **End-of-chain checkpoint**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: test` AND `readiness: 95-99` AND test-stage Done When all checked
- **Direct verb**: operator says "review feature X", "is X done", "verify X meets spec", "did we actually build what was specified", "ready to mark X as done?"
- **Pre-merge gate**: feature is on a branch, about to merge to main; reviewer wants an adversarial pass before merge
- **Post-incident review**: a feature shipped, a problem surfaced; review traces back to confirm what the spec said vs what shipped (different from `ops-incident` — that's about resolving the live issue)

Do NOT load when:

- Task `current_stage` is upstream of test (review needs test-stage artifacts to review against)
- The "review" is a code review at a tactical level (load `pr-review-toolkit:review-pr` for line-by-line review)
- The review is of the architecture, not a specific feature (load `architecture-review`)

## Operations

This skill has 4 named operations. Execute in order; the review either authorizes status=done or sends the task BACK to an earlier stage with documented reasons.

### Operation 1: Reconstruct the spec contract

**Trigger**: skill loaded; current_stage is test-complete confirmed.

**Process**:

1. Read the task file. Capture: title, type, Done When list, all artifacts produced across the 5 stages.
2. Read the document-stage artifacts: requirements doc + gap analysis. Capture every functional + non-functional requirement and every acceptance criterion.
3. Read the design-stage artifact: capture the decisions made (and the alternatives explicitly rejected — these are still relevant; if the implementation accidentally drifted toward a rejected alternative, flag it).
4. Read the scaffold artifacts: capture the API surface (types, configs) — the implementation should NOT have expanded the API beyond what scaffold defined.
5. Read the implement + test artifacts: capture which files exist + which tests claim to verify which Done When.

**Quality bar (Operation 1 done when)**:

- [ ] Every Done When item enumerated with the test that supposedly proves it
- [ ] Every functional requirement enumerated with the implementation file that satisfies it
- [ ] Design decisions enumerated with the implementation behavior that honors them
- [ ] Rejected alternatives enumerated (to detect drift)
- [ ] API surface from scaffold enumerated (to detect scope creep)

### Operation 2: Verify spec vs implementation (adversarial pass)

**Trigger**: Operation 1 spec contract reconstructed.

**Process**:

1. For each Done When item: RUN the verification (the test, the CLI command, the file existence check). Don't trust prior runs — re-run now. Capture stdout/stderr.
2. For each functional requirement: trace from requirement → implementation file → test → passing run. If any step is missing, the requirement isn't actually delivered.
3. For each design decision: read the relevant implementation code and verify the implementation HONORS the decision. Examples:
   - Decision said "use `extends:` for profile inheritance" → grep for extends in profiles
   - Decision said "circuit breaker threshold is per-profile" → confirm threshold is read from profile, not hardcoded
4. For each rejected alternative: scan the implementation for telltale signs the rejected approach crept in. Examples:
   - Rejected "hardcode tier order" → grep for hardcoded backend lists in router
   - Rejected "single-tier" → confirm router actually has the 4 tiers, not just 2
5. Run the FULL test suite (not just `-x`): `pytest tests/ --tb=short`. Capture the test count + result.
6. Run lint: `ruff check aicp/ tests/`. Capture any new violations.
7. Run wiki lint: `python3 -m tools.lint`. The new wiki content (decisions, etc.) must validate.

**Quality bar (Operation 2 done when)**:

- [ ] Each Done When item produced fresh evidence in this review (re-run, not memoized)
- [ ] Each functional requirement traces requirement → file → test → pass
- [ ] Each design decision honored by implementation (specific evidence)
- [ ] No rejected alternative crept into implementation (specific evidence absent)
- [ ] Full test suite passes (not just `-x`)
- [ ] Lint clean
- [ ] Wiki lint clean

### Operation 3: Surface gaps + write the review verdict

**Trigger**: Operation 2 verifications complete.

**Process**:

1. Author a Review Verdict — short note appended to the task body OR a separate file at `wiki/decisions/00_inbox/T<id>-review-<date>.md`. Required structure:
   - **Verdict**: APPROVED / APPROVED WITH FOLLOW-UPS / SEND BACK TO <stage>
   - **Verification log**: each Done When + evidence (command + output snippet)
   - **Spec drift detected**: any divergence between spec and implementation, with file references
   - **Follow-up tasks**: any gaps that warrant a NEW task (not part of this feature's scope)
   - **Reviewer notes**: judgment calls (e.g., "scope expansion in X is acceptable because Y")
2. **Be honest about partial wins**. If 9/10 Done When pass and 1 fails, the verdict is APPROVED WITH FOLLOW-UPS, not APPROVED. The failing item becomes a follow-up task.
3. **Send back if architecture drifted**. If the implementation honors the requirements but violates the design (e.g., picked a rejected alternative), the verdict is SEND BACK TO design — the design needs updating to reflect reality, OR the implementation needs reverting to honor the design.

**Quality bar (Operation 3 done when)**:

- [ ] Verdict is one of the three valid values (APPROVED / APPROVED WITH FOLLOW-UPS / SEND BACK)
- [ ] Verification log has evidence for every Done When
- [ ] Spec drift section exists (even if "none observed")
- [ ] Follow-up tasks listed (or "none required")
- [ ] Reviewer notes capture judgment calls explicitly

### Operation 4: Apply the verdict (operator confirms 99→100)

**Trigger**: Operation 3 verdict written.

**Process**:

1. Present the review verdict to the operator. Point them at the file path; don't summarize away the details.
2. Operator decides:
   - **APPROVED**: operator says "approved, mark done." → set task `status: done`, `readiness: 100` (per Methodology Standards: human-only). Commit `chore(backlog): T<id> review approved → done`.
   - **APPROVED WITH FOLLOW-UPS**: operator agrees + you create the follow-up tasks first. Create one task file per follow-up. THEN set the original task `status: done`. Commit follow-ups separately, then the status update.
   - **SEND BACK TO <stage>**: operator confirms send-back OR pushes back. If confirmed, set task `current_stage: <stage>`, `readiness: <range floor>`. Commit `chore(backlog): T<id> review sent back to <stage>`.
3. After verdict applied: re-run wiki lint to confirm task files validate.
4. If APPROVED: contribute insights from this feature back to second brain via `gateway contribute --type lesson` if any reusable principle was learned.

**Quality bar (Operation 4 done when)**:

- [ ] Operator EXPLICITLY confirmed the verdict (not implicit)
- [ ] Task state updated per the verdict
- [ ] Follow-up tasks created (if APPROVED WITH FOLLOW-UPS)
- [ ] Wiki lint passes
- [ ] If APPROVED + reusable insight: contribution submitted to second brain

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Approving without re-running verifications (memoized acceptance)

The temptation: tests passed at the test stage. Implementation file exists. Surely the feature works. NO — review's job is ADVERSARIAL re-verification. Memoized acceptance ("it passed before, it must still pass") misses regressions introduced by other changes since test stage ran.

**Detection**: did Operation 2 RE-RUN every Done When verification fresh? Or did it cite test results from a prior session?

**The rule**: every Done When verification runs fresh during review. Capture fresh stdout. The cost is minutes; the value is catching regressions before status flips to done.

### Gotcha 2: Approving when 9/10 Done When pass (false-binary thinking)

A feature has 10 Done When items. 9 pass cleanly, 1 has a flaky failure. Tempting to approve and "fix the flaky one later." NO — that's how technical debt accumulates silently. The verdict for 9/10 is APPROVED WITH FOLLOW-UPS, not APPROVED.

**Detection**: any Done When item has output that's not a clean pass.

**The rule**: every imperfect Done When yields a follow-up task. Follow-ups land first; status flips after. The bookkeeping discipline prevents drift.

### Gotcha 3: Missing the rejected-alternative drift

The design rejected "hardcode tier order." The implementation has a hardcoded list of tiers in `aicp/core/router.py`. The implementation passes tests because the tests don't assert on configurability. The implementation honored the requirement (router routes) but violated the design decision (configurable per profile). This is "spec drift" and review's specific job is to catch it.

**Detection**: did Operation 2 check for telltale signs of EACH rejected alternative? Or only verify the chosen alternative was implemented?

**The rule**: rejected alternatives are part of the spec. Verify their absence with the same rigor as you verify the chosen approach's presence.

### Gotcha 4: Operator approval as rubber-stamp (review theater)

The operator says "approved" without reading the verdict file. You set status=done. Two weeks later they discover something they would have flagged. This is the symmetric problem to Gotcha 4 in `feature-plan` — approval theater.

**Detection**: did you point the operator at the verdict FILE PATH and confirm they READ it? Or did you summarize and accept "approved" based on the summary?

**The rule**: reviews that authorize status=done require operator to consume the actual verdict, not your summary of it. Reviews are the LAST gate before the feature ships; rubber-stamping defeats the purpose.

### Gotcha 5: Skipping spec drift section (because "looks fine")

Operation 3 requires a Spec Drift section even if "none observed." Tempting to omit when nothing drifted. NO — the explicit "none observed" is itself the artifact that proves the check was performed. Empty section means "I didn't check"; "none observed" means "I checked and found nothing."

**Detection**: the Spec Drift section is missing from the verdict file.

**The rule**: every verdict has a Spec Drift section. The content is "none observed" or a list. Never absent.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact this skill produces:

- **Review verdict structure**: Operations Plan template at `~/devops-solutions-research-wiki/wiki/spine/standards/operations-plan-page-standards.md` (verdict is structurally a 4-step operations plan: re-verify → trace spec → write verdict → apply)
- **Adversarial review pattern**: see `superpowers:requesting-code-review` and `pr-review-toolkit:review-pr` skills for related (but tactical) review approaches; this skill operates at the FEATURE level, those operate at the line/PR level.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). Review is a read-only operation against the codebase + wiki; the only writes are the verdict file (in `wiki/decisions/` or task body) and the task state update.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-test | test stage (preceding) | Authors + runs tests; this skill reviews the assembled feature against the spec |
| feature-iterate | post-shipping refinement | Iterate is for changes; review is for sign-off on the original |
| pr-review-toolkit:review-pr | line-by-line PR review | Tactical code review; this skill is feature-level review against the spec |
| architecture-review | architecture quality | System-wide; this skill is per-feature |
| ops-incident | live problem investigation | Incident is reactive; review is proactive (catches issues before incident) |
