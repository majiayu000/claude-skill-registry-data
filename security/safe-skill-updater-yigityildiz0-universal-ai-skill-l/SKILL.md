---
name: safe-skill-updater
description: Audit, compare, merge, repair, or improve Codex and ChatGPT Desktop skills without degrading proven behavior. Use for skill health checks, duplicate cleanup, stale tool/model review, broken references, trigger tuning, cross-version comparison, or conservative skill updates with backups and regression validation. Keep available to Codex/ChatGPT; deny it in OpenCode.
---

# Safe Skill Updater

Improve a skill only when evidence shows a measurable benefit. "No change" is a successful result when a proposed rewrite would add length, remove useful behavior, weaken safety, or merely restyle working instructions.

## Scope Boundary

- Target user-owned Codex/ChatGPT Desktop skills only; ChatGPT web has no local skill tree, so produce an import package instead of claiming a local edit.
- Do not install or mirror this updater into OpenCode.
- Do not edit managed plugin caches, system skills, marketplace checkouts, or generated runtime caches. Update their source package or leave a report.
- Do not change Claude/OpenCode variants unless the user names those targets separately.

## Preservation-First Workflow

1. Snapshot the baseline.
   - Record source path, full tree hash, frontmatter, sidecars, referenced files, platform scope, and current validation result.
   - Back up the complete skill folder before any write.

2. Recover the behavioral contract.
   - List trigger phrases, supported tasks, required tools, outputs, fallbacks, safety rules, and verification steps.
   - Read every same-name variant as a separate implementation; newer or longer is not automatically better.
   - Identify user-authored constraints that must survive.

3. Classify evidence.
   - `DETERMINISTIC_BREAK`: reproducible missing file, invalid metadata, broken command, encoding damage, or validator failure.
   - `TRIGGER_ERROR`: confirmed over-trigger or under-trigger.
   - `STALE_INTEGRATION`: official current documentation contradicts a tool, API, path, or config.
   - `MODEL_POLICY`: prescriptive model/provider choice is stale or incorrectly placed.
   - `PORTABILITY_ERROR`: host-specific behavior was copied into a shared core.
   - `DUPLICATE`: exact or semantic duplicate with no unique contract.
   - `REGRESSION_RISK`: a proposed simplification drops capabilities, sidecars, safeguards, or user preferences.
   - `UNSUPPORTED_CLAIM`: the concern has no reproducible or authoritative evidence.

4. Produce a semantic diff before editing.

```markdown
| Contract item | Current | Proposed | Evidence | Risk |
|---|---|---|---|---|
| Trigger | ... | ... | ... | low/medium/high |
| Workflow | ... | ... | ... | ... |
| Tools/sidecars | ... | ... | ... | ... |
| Verification | ... | ... | ... | ... |
| Platform/model policy | ... | ... | ... | ... |
```

   - Mark each operation `ADD`, `REMOVE`, `MODIFY`, `REORDER`, `MERGE`, `SPLIT`, or `NO_CHANGE`.
   - Prefer the smallest change that resolves the confirmed issue.

5. Apply only an authorized, evidence-backed diff.
   - Preserve the folder/name unless a collision or invalid ID requires a migration.
   - Keep frontmatter to `name` and a concise trigger-focused `description`.
   - Keep `SKILL.md` under 500 lines when practical; move deep detail to directly linked references.
   - Preserve scripts/assets unless the replacement is verified and all references are updated.

6. Validate at three levels.
   - Structural: frontmatter, name/folder match, links, encoding, metadata, and package layout.
   - Behavioral: replay representative trigger, non-trigger, edge, and failure prompts; run harmless script tests.
   - Comparative: prove the updated variant preserves every accepted baseline contract item and improves the targeted issue.

7. Use independent review for high-risk changes.
   - Required for deletion, merge, split, platform migration, security logic, model/tool rewrites, or changes above roughly 20% of the body.
   - Give reviewers the raw before/after artifacts and test prompts, not the desired verdict.

8. Commit or roll back.
   - Keep the update only if validation passes and no accepted behavior regresses.
   - Restore the backup when results are ambiguous or worse.
   - Report evidence, diff, tests, residual risk, and rollback path.

## Optional cross-skill rule extraction

Use this mode only when the user explicitly asks to extract, consolidate, or promote rules across a named skill scope. Read [references/evaluation-and-rule-promotion.md](references/evaluation-and-rule-promotion.md). It may propose a rule with evidence and a semantic diff; it must not auto-write global instructions or silently replace a local/host-specific contract.

## Merge and Delete Rules

Merge only when trigger domains, dependencies, safety constraints, and output contracts substantially overlap. Preserve distinct platform integrations as namespaced variants or overlays.

Archive before permanent deletion. High-confidence removal candidates include exact physical duplicates, aliases loaded twice, test fixtures, example packages already represented by production skills, broken pointer stubs, managed-plugin copies without their runtime, and instructions whose primary purpose is bypassing safety or policy.

Do not delete based only on file age, length, a heuristic score, popularity, or a newer version number.

## Model and Provider Rules

Read [references/model-provider-policy.md](references/model-provider-policy.md) before changing any provider or model language. Shared skills should use the active host's available capabilities and must not select a provider/model automatically. Keep a fixed model name only when the skill explicitly configures or documents that runtime and the name is verified from an official current source.

## Audit Tools

Run the read-only scanner before broad work:

```powershell
python scripts/analyze_skill_corpus.py --output <audit-dir> --root "codex=<path>" --root "agents=<path>"
```

Review `all_skills.csv`, `exact_duplicate_groups.csv`, `same_name_conflicts.csv`, `vendor_model_review.csv`, and `quality_and_format_review.csv`. Heuristic flags are evidence prompts, never automatic edit decisions.

Use [references/quality-preservation-rubric.md](references/quality-preservation-rubric.md) for the final go/no-go decision.

## Stop Conditions

Stop without editing when the source is managed, the target platform is unclear, required tools cannot be verified, the change is cosmetic, tests cannot distinguish better from worse, or the proposed benefit does not exceed regression risk.
