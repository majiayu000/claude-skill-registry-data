---
name: repo-audit
description: "Audit repositories or PRs for bugs, security, code quality, and docs: quick review or exhaustive domain coverage."
license: MIT
compatibility: "Requires git and bash (exhaustive detector); worker dispatch is optional"
metadata:
  source: iuliandita/skills
  date_added: "2026-09-20"
  effort: high
  argument_hint: "[quick|exhaustive] [scope]"
---

# Repo Audit

Choose the audit depth explicitly. **Quick** is a bounded pre-merge sweep. **Exhaustive** is a wave-based repository health audit. Never turn a quick request into exhaustive coverage without saying so.

## When to use

- Review a repository or PR across bugs, security, code quality, and documentation.
- Run a predictable quick merge check.
- Run a deliberate exhaustive audit that detects and covers applicable technical domains.

## When NOT to use

- Review one concern only: invoke its owning skill.
- Review a product, business, or implementation decision: use **plan-review**.
- Audit the skill collection itself: use **skill-creator**.
- Diagnose a live incident or administer a live system: use the matching operational skill.

## Workflow

1. **Preflight:** require a git repository; collect commit, branch, integration base, scope, changed files, languages, manifests, file count, instructions, and whether `docs/local/` is ignored before artifacts are written.
2. **Choose mode:** use explicit user wording; default to **quick** for a PR, diff, merge, release, or handoff check, and to **exhaustive** only for a repo-wide health check, onboarding, or a request for comprehensive coverage. State the choice and scope before dispatch.
3. **Quick mode:** read `references/quick-workflow.md`, then run independent, scoped lanes: code review, code simplification, security audit, and documentation sweep. Preserve each lane's native report; disclose failed, substituted, or skipped lanes. Do not add domain lanes or task-planning artifacts.
4. **Exhaustive reconnaissance:** read `references/exhaustive-workflow.md` and copy its progress checklist, then invoke the shipped `references/detect.sh` against the scoped repository and interpret its output with `references/detection-patterns.md`; show the 31-worker budget, matched, root-manifest-only, and skipped candidates before work starts. If the detector cannot run, disclose that failure and perform the documented manual equivalent. Confirm ambiguous matches against the scoped tree.
5. **Exhaustive waves:** follow the guide to run code quality once (code review, code simplification, prose); then detected domain lanes; then security before vulnerability research; then docs, roadmap, and git hygiene. Show each wave before the next. Never dispatch an undetected lane.
6. **Persist:** quick mode retains one wrapper report containing the four unedited lane reports, but creates no exhaustive artifacts. Exhaustive mode preserves lane reports in `DEEP-AUDIT.md`, derives `DEEP-AUDIT-TASKS.md`, states residual risk, and chooses direct execution only for a small task list. Larger task lists need an explicitly selected planning workflow.
7. **Report:** prioritize security, correctness, test gaps, code quality, domain findings, then docs and hygiene. Keep evidence, scope limits, and unrun checks visible.

## AI Self-Check

- [ ] Mode, scope, integration base, and git context were stated before dispatch.
- [ ] Quick coverage stayed at four lanes; exhaustive coverage ran code-quality lanes once and only confirmed domain lanes.
- [ ] Every skipped, failed, timed-out, or fallback lane is disclosed.
- [ ] Security precedes vulnerability research, which receives only a concise nonduplicating finding summary.
- [ ] Findings cite files, commands, outputs, or source documentation; residual risk is explicit.
- [ ] Artifacts are protected by `docs/local/` ignore coverage.
- [ ] Cross-cutting hygiene is applied from `references/agent-hygiene.md`.

## References

- `references/detection-patterns.md` - domain-lane signals and scoped detection rules.
- `references/quick-workflow.md` - bounded four-lane merge-review procedure.
- `references/exhaustive-workflow.md` - wave order, persistence, and task-list limits.
- `references/exclusions.md` - skills that are operational, meta, or otherwise not audit lanes.
- `references/report-templates.md` - exhaustive report and task list shapes.
- `references/output-contract.md` - required reporting format.

## Output Contract

Use `references/output-contract.md`.

- **Skill name:** REPO-AUDIT
- **Deliverable:** quick: `docs/local/audits/repo-audit/<YYYY-MM-DD>-<slug>.md`; exhaustive: `docs/local/audits/DEEP-AUDIT.md` and `DEEP-AUDIT-TASKS.md`.
- **Mode:** always-on for audit invocations.
- **Priority:** P0-P3 and info; retain the source lane and evidence for every finding.

## Rules

- Quick means exactly four lanes; exhaustive means every lane listed in Step 5, nothing undetected. Do not duplicate code-simplification as separate slop and slimming passes.
- Workers need independent context, read access, target-skill instructions, and the right tools. Sequential fallback is allowed and must be disclosed.
- Do not normalize, merge, or silently discard lane reports. Synthesis is a separate final priority view.
- Audit is read-only unless the user separately authorizes fixes. Do not write artifacts until ignore protection is verified.
- Scope constraints apply to every lane. Root manifests in a monorepo are candidates, not proof that a scoped service uses a dependency.
