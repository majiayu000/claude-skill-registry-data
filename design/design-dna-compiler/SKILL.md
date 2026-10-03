---
name: design-dna-compiler
description: Use when a user needs to preserve an existing product or brand's interface identity across new or modified UI using one to five authorized project, URL, or screenshot sources.
---

# Design DNA Compiler

Compile authorized, same-brand UI evidence into a traceable design system, an installable brand Skill, and an implemented proof page. Work from this Skill directory so every command resolves `scripts/design-dna.mjs`. Deterministic scripts collect, normalize, compile, and verify artifacts; deterministic scripts do not call a model or API. Apply agent judgment only to evidence review, semantic decisions, exclusions, and original proof authorship.

## Non-negotiable boundaries

- Accept one to five `project`, `URL`, or `screenshot` sources for the same brand. Count independent support by canonical page key, not by modality.
- Require an explicit brand/project name and explicit authorization for every URL. Public visibility is not authorization. Stop and request missing authorization before accessing a URL. Stop and request brand mismatch resolution when strong identifiers conflict; ask the user to remove or relabel sources. Otherwise, continue autonomously through delivery.
- Keep every source immutable. Do not modify an input project, screenshot, or other local source. Write to a separate output directory that is neither inside nor an ancestor of a local source. Preserve and compare source hashes.
- Do not use an unauthorized URL. Do not copy source code, logos, proprietary icons, imagery, video, fonts, or source copy. Do not invent brand claims, capabilities, metrics, testimonials, or product facts.
- A screenshot shows visible appearance only: a screenshot does not prove DOM semantics, exact fonts, breakpoints, computed contrast, interactions, states, or other hidden behavior.
- Never average conflicts. Use only emitted `global`, `viewport:<name>`, `page:<pageKey>`, or `component:<context>` scopes. Exclude evidence that cannot fit those scopes, record why, and request resolution.
- Report-only completion is not allowed. Do not stop at an audit: actually implement the selected proof surface in the generated scaffold, verify it, and repair hard failures.

`pipeline-state.json` binds every stage to artifact digests. Brief resets downstream state; collect clears inference, compilation, and verification; infer clears compilation and verification; compile atomically regenerates core artifacts, brand Skill, specimen, and neutral proof scaffold and clears prior verification; verify publishes one report and capture generation. Never edit `pipeline-state.json` or generated artifacts to bypass stale-lineage rejection.

## Ordered workflow

Follow all seven stages in order. Do not skip a stage because an earlier artifact looks plausible.

### 1. Intake and brief

Read [references/input-contract.md](references/input-contract.md) before accepting inputs. Collect the explicit brand name, purpose, users, one to five sources, canonical page keys, authorization, proof surface, and constraints. Resolve missing URL authorization or same-brand ambiguity before continuing. Choose a separate output directory, create `brief.json` exactly as specified, and run:

```text
node scripts/design-dna.mjs brief --input <brief.json> --output <output-directory>
```

Review `source-manifest.json`; record inferred proof-surface assumptions rather than silently accepting them. Use only `marketing`, `application`, `settings`, or `specimen`; an unknown value currently behaves as omitted and is inferred, not rejected.

### 2. Immutable evidence collection

Read [references/evidence-model.md](references/evidence-model.md) for collector limits and exact records. Record the manifest checksums before collection and never mutate a source. Visually inspect every screenshot input. Put only provable visible observations in a JSON object; `collect` labels them `visible-only`. Do not treat a visual-reference checksum as design evidence.

Collect once for all manifest sources. Repeat `--project-url` for each runnable project page in the same invocation. `--visual-evidence` accepts raw JSON, not a filename. If observations are stored in a file, read its contents first, then pass the serialized object to `--visual-evidence` as one argument. Runnable pages are captured at 375 × 812, 768 × 1024, and 1440 × 1000.

```text
node scripts/design-dna.mjs collect --output <output-directory> [--project-url <source-id>=<loopback-url> ...] [--visual-evidence '<JSON object>']
```

Inspect both `raw-evidence.json` and `evidence.json`: collector limitations live only in the raw file. Confirm source hashes separately after collection; the verifier does not re-hash inputs.

### 3. Evidence review and inference

Visibly label screenshot limits. Identify defects, noise, ambiguity, and page-specific styling. Create `exclusion-reasons.json` beside the brief as a coarse evidence-ID-to-reason map with no paths, source copy, or secrets. It is a working/delivery sidecar, not a generated pipeline artifact and not lineage-bound. Pass only its IDs to `--exclude`; the CLI does not ingest reasons. Never exclude inconvenient evidence merely to raise confidence. Read [references/rule-inference.md](references/rule-inference.md), then run:

```text
node scripts/design-dna.mjs infer --output <output-directory> [--exclude <evidence-id,...>]
```

Inspect `candidates.json` and `rule-report.md`. Every accepted rule must cite valid evidence IDs; keep `exclusion-reasons.json` separately because ordinary CLI exclusions retain IDs/flags, not reasons.

### 4. Confidence, conflict, and compilation

Apply the confidence thresholds exactly. Narrow conflicts only to an implemented scope. If a conflict cannot be represented, exclude its affected evidence, record the reason/limitation, and seek resolution; never hand-edit `candidates.json`, because lineage validation rejects it. Ask for brand resolution if the same-brand boundary remains unresolved. Then run:

```text
node scripts/design-dna.mjs compile --output <output-directory>
```

Treat this as the final compile before proof authorship. A later compile replaces `DESIGN.md`, `design-tokens.json`, `tokens.css`, the brand Skill, specimen, neutral proof scaffold, and prior verification. Do not author the proof until final `compile`; before an intentional recompile, back up user-owned proof changes outside the managed output and reapply them afterward. Review synchronized outputs and read [references/brand-skill-contract.md](references/brand-skill-contract.md) for behavior and portability.

### 5. Proof implementation

Actually replace the proof body with a substantive original implementation inside `<output-directory>/proof/`; use only neutral or user-owned content. Preserve the `design-dna-compiler:proof-brief-sha256` comment/digest, every required `data-token`, and the `../tokens.css` link. In the proof meta, change `design-dna-proof-content` from `neutral-scaffold` to `authored-content` while preserving `data-neutral-sha256` exactly. Do not mark content authored before substantive body replacement exists; missing or unchanged provenance remains a conditional limitation.

Exercise real page states and keyboard behavior. Preserve accessible names, visible focus, reduced-motion behavior, and at least 44 × 44 targets except native inline prose links.

### 6. Verification and repair

Read [references/verification.md](references/verification.md). Resolve the official validator via explicit `SKILL_VALIDATOR` or derive it from `CODEX_SKILLS_ROOT`; the verifier runs it with `PYTHON` or `python3`. Confirm the selected runtime has YAML and set `PYTHON` when needed:

```text
if [ -z "${SKILL_VALIDATOR:-}" ]; then
  : "${CODEX_SKILLS_ROOT:?Set SKILL_VALIDATOR or CODEX_SKILLS_ROOT}"
  export SKILL_VALIDATOR="$CODEX_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py"
fi
"${PYTHON:-python3}" -c 'import yaml'
```

Then run:

```text
node scripts/design-dna.mjs verify --output <output-directory>
```

Inspect `verification-report.md` and all six 375, 768, and 1440 specimen/proof captures. Repair every hard failure in the proof implementation or evidence-backed artifacts, then rerun verification. Repeat until `pass` or an honest `conditional pass`. Never rename a failure, suppress a check, remove provenance, or weaken a rule to obtain a better status.

### 7. Delivery

Deliver the complete output plus separate `exclusion-reasons.json`. State status, exact derived limitations, scopes/conflicts, exclusions/reasons, unresolved facts, and the independently compared pre/post source checksums. The report contains one current core artifact hash set; it does not prove deterministic reruns. Test determinism only by running two clean pipelines in separate outputs and comparing their reported hashes. State that the sidecar is not lineage-bound.

Include these exact rerun commands, replacing placeholders with the delivered paths and retaining only options that were used:

```text
node scripts/design-dna.mjs brief --input <brief.json> --output <output-directory>
node scripts/design-dna.mjs collect --output <output-directory> [--project-url <source-id>=<loopback-url> ...] [--visual-evidence '<JSON object>']
node scripts/design-dna.mjs infer --output <output-directory> [--exclude <evidence-id,...>]
node scripts/design-dna.mjs compile --output <output-directory>
node scripts/design-dna.mjs verify --output <output-directory>
```
