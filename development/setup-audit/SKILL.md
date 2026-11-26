---
name: setup-audit
description: Audit the repo to extract architecture principles, or with --merge unify audits from multiple repos into a single team-wide document
type: skill
user-invocable: false
---

# MTK Setup Audit — Extract or Unify Architecture Principles

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

**Companion files:** several steps below defer detail to `.claude/references/audit-*.md` companions, resolved via the block above. If a companion cannot be resolved at read time, stop the affected step and report the missing file path — do not reconstruct its content from memory.

---

This skill has two modes:

- **Default (single-repo audit):** Audit the current repository and produce `.claude/references/architecture-principles.md` describing how this team builds software.
- **`--merge` (multi-repo unification):** Combine architecture audits from multiple repos placed under `.claude/references/audits/` into a single unified document.

Pick based on the argument. If the engineer passed `--merge`, jump to **MERGE MODE** below. Otherwise, run **AUDIT MODE**.

---

# AUDIT MODE (default)

You are a senior architect performing an architectural audit of this repository. Document what the codebase ACTUALLY does, not what it should do. If you find inconsistencies, flag them as "⚠️ Inconsistency" — let the team decide which pattern to standardize on.

## STEP -1: Versioned Re-Run Detection

Before regenerating anything, resolve whether this is a re-run and whether a previous template cache exists.

1. **Read current manifest version.** The full manifest lives at the plugin root (marketplace installs have no project-local `.claude/manifest.json`); target repos carry the slim `.claude/mtk-version.json` written by `setup-bootstrap`:
   ```bash
   PM="${CLAUDE_PLUGIN_ROOT}/.claude/manifest.json"
   [ -f "$PM" ] || PM=".claude/mtk-version.json"
   CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$PM'))['version'])")
   ```

2. **Read previous version from the existing constitution footer.** Bootstrap stamps the footer on `AGENTS.md`; `CLAUDE.md` is only the import shim, so read `AGENTS.md` first and fall back to `CLAUDE.md` for legacy (pre-inversion) repos:
   ```bash
   PREVIOUS_VERSION=""
   for CONST_DOC in AGENTS.md CLAUDE.md; do
     PREVIOUS_VERSION=$(grep -oE 'mtk-setup: v[0-9.]+' "$CONST_DOC" 2>/dev/null | head -1 | awk '{print $2}' | sed 's/^v//')
     [ -n "$PREVIOUS_VERSION" ] && break
   done
   ```
   If neither file exists or neither has a footer, `PREVIOUS_VERSION` is empty.

3. **Locate previous template cache:**
   ```bash
   PREV_CACHE=".claude/.mtk-cache/v${PREVIOUS_VERSION}"
   ```

4. **Classify:**

   | Case | Condition | Action |
   |---|---|---|
   | **First v7+ run on an existing repo** | `AGENTS.md` or `CLAUDE.md` exists but neither has a footer, OR cache missing | Go to **Migration Path** below |
   | **Clean re-run** | Footer present and `$PREV_CACHE` exists | Go to **Re-Run Merge Logic** below |
   | **Fresh bootstrap** | `AGENTS.md` and `CLAUDE.md` both absent | Proceed directly to STEP 0 — no merge needed |

The **Migration Path** and **Re-Run Merge Logic** procedures (including the re-run summary table) live in `.claude/references/audit-rerun-migration.md`. When the classification above is a migration or a clean re-run, read that file now (path per `## MTK File Resolution`) and follow it; do not paraphrase it from memory. On a fresh bootstrap (`AGENTS.md` and `CLAUDE.md` both absent), skip it and proceed to STEP 0.

## STEP 0: Determine The Tech Stack

Read `.claude/tech-stack` to determine the active stack. If missing, detect it:

```bash
bash scripts/setup-detect.sh --json
```
Read `stacks` (array) and `primary_candidate` from the output.

If multiple stacks detected (`stacks` has more than one entry), ask the engineer which to audit first. Multi-stack repos may need multiple audits.

If no supported stack detected (`stacks` is empty), stop and tell the engineer to run `/mtk-setup` first or add a tech stack skill.

Then load `.claude/skills/tech-stack-{stack}/SKILL.md`. The `## Scan Recipes` section provides the bash commands for that stack.

## STEP 0.5: Build the Ranked Symbol Graph (repomap)

Before running ad-hoc scan recipes, produce a deterministic symbol graph. This is the **primary input** to the audit — scan recipes remain a supplement, not the source of truth.

```bash
bash scripts/repomap.sh <stack> --budget=4000 --out=.claude/.mtk-cache/repomap.json
```

Read the resulting JSON. The `fit` field tells you the quality tier:

| `fit` value | Meaning | Audit behavior |
|---|---|---|
| `full` | All symbols fit within budget | Cite freely — full graph available |
| `ranked` | Top-N by in-edge count (PageRank-ish) | Cite top symbols; acknowledge truncation in provenance section |
| `defer-to-mcp` | .NET only — attempt csharp-lsp enrichment for the top files found by scan recipes (the tool is per-file — no solution-wide ranked graph exists); if the MCP server is unreachable or the workspace fails to load, treat exactly as `fallback` and disclose in Provenance | Use MCP tool for the ranked pass, then cite |
| `fallback` | No tree-sitter / no LSP available | Audit degrades to scan-recipes-only; **provenance section must state this** |

When `fit != "fallback"`, the audit prompt changes character — instead of "read the codebase and extract principles", become:

> "The following ranked symbols are the structural backbone of this codebase (top by incoming-reference count). For each architectural principle you propose, cite at least one symbol from this list that evidences it. Do not claim a principle you cannot evidence."

Pass the ranked JSON into the prompt context. Keep the symbol list visible while writing principles.

## STEP 0.9: Scan Ledger (resumable)

Long audits on large repos must survive crash, compaction, or session handoff. Use the existing `scripts/workflow-artifact.sh` to record progress as a resumable ledger.

1. **Resume check.** Before starting, run `scripts/workflow-artifact.sh list`. If an incomplete (`status` not `completed`/`abandoned`) artifact of type `setup-audit` exists:
   - If its `updated` timestamp is **less than 24h old**, ask via `AskUserQuestion`:
     ```
     question: "Found an in-progress setup-audit from <updated>. How do you want to proceed?"
     header: "Resume audit"
     options:
       - label: "Resume from <current_step>"
         description: "Skip completed steps, reload their outputs summaries instead of re-scanning."
       - label: "Start fresh (abandon)"
         description: "Abandon the previous run and start a new audit from STEP 0."
       - label: "Cancel"
         description: "Stop — don't touch anything."
     ```
     On "Resume from <current_step>", skip every STEP already marked `step_completed` in the artifact's event log and reload its recorded `outputs`/`summary` instead of re-running the scan. On "Start fresh (abandon)", run `scripts/workflow-artifact.sh abandon <uuid> --reason "engineer requested restart"`, then continue to step 2. On "Cancel", stop without modifying anything.
   - If its `updated` timestamp is **24h or older**, auto-abandon it — `scripts/workflow-artifact.sh abandon <uuid> --reason stale-24h` — print a one-line notice, and continue to step 2 without asking.

2. **Start (fresh run).** `bash scripts/workflow-artifact.sh init setup-audit --goal "<one-line audit goal>"` and record the returned UUID for the rest of the run.

3. **After each numbered STEP.** Once a STEP completes, record it on the ledger:
   ```bash
   scripts/workflow-artifact.sh event <uuid> step_completed --data '{"step":"STEP 2","outputs":["<files written>"],"summary":"<one concrete sentence>"}'
   scripts/workflow-artifact.sh set <uuid> current_step="STEP 2"
   ```
   Summaries must be concrete — "scanned 214 files, 3 inconsistencies", never "made progress" or other vague phrasing. A vague summary is useless on resume: the next session has nothing to reload.

4. **On completion.** `scripts/workflow-artifact.sh set <uuid> status=completed`.

**Context economy (large repos).** For repos with more than 1000 tracked source files, process each scan category (STEP 1 and STEP 2.5) in turn — write its findings into the ledger event immediately after that category finishes, keep only a 1-2 sentence summary in working context, then move to the next category. The ledger, not the conversation, is the working memory; don't hold the full scan output in context waiting to write the doc at the end.

## STEP 1: Run The Scan Recipes

Execute each scan recipe block from the active tech stack skill in order. The standard categories are:

1. **Project Structure** — solutions, projects/modules, dependencies, framework version, key packages
2. **Patterns In Use** — frameworks, design patterns (CQRS, repository, validation, mapping)
3. **Data Layer** — ORM configuration, query patterns, migrations, raw SQL usage
4. **Infrastructure** — cloud services, IaC, containers, networking, secrets, messaging
5. **Naming Conventions** — file/folder layout, controller/handler/service patterns
6. **Testing Patterns** — frameworks, providers, fixture patterns, integration test bases
7. **Configuration** — config files, options patterns, logging

For each block, sample 2-3 representative files in detail to understand intent — not just file counts.

**Verbatim version extraction.** Framework and runtime versions in `architecture-principles.md`, `CLAUDE.md`, and `detected-tools.json` are quoted verbatim from the manifest file — not paraphrased, rounded, or restated from training-data knowledge, because `verify-claims.sh` re-checks them against the manifest. Read and cite:

- TypeScript / Node: `cat package.json | jq '.dependencies.next, .dependencies.react, .devDependencies.typescript, .engines.node'` (or `grep -E '"(next|react|typescript|node)"'` if `jq` unavailable). Quote the actual range string (e.g., `next: ^15.0.3` → write "Next.js 15", not "Next.js 16").
- Python: `grep -E '^\s*(python|django|fastapi|flask|sqlalchemy)\s*=' pyproject.toml` (or the `[project] dependencies` block).
- .NET: `grep -hE '<TargetFramework[s]?>|<PackageReference Include=' **/*.csproj` — quote both `TargetFramework(s)` (e.g., `net9.0`) and the explicit `Version=` on each `PackageReference`.

If the manifest file is missing or unparseable, write `unknown` — never guess. Hallucinated versions ("Next.js 16" when `package.json` says `^15.0.3`) are a recurring audit failure; this rule exists to block them.

## STEP 2: Run Stack-Agnostic Cross-Cutting Scans

These apply to any tech stack:

```bash
# Git conventions
git log --oneline -20
git branch -a | head -20
find . -name "pull_request_template*"

# CI/CD
find . \( -name "*.yml" -o -name "*.yaml" \) | grep -i "github\|pipeline\|ci\|cd\|workflow\|azure\|jenkins"

# Docker
find . \( -name "Dockerfile" -o -name "docker-compose*" -o -name ".dockerignore" \)
```

## STEP 2.5: Extract Codebase Conventions

Beyond architecture principles, extract the specific conventions this codebase follows. These are more granular than architecture — they're the patterns a new developer (or AI) needs to match when writing code in this repo.

The five convention-extraction scan blocks (Naming, Folder Structure, DI Registration, Response/Error, Test Patterns) and the `conventions.md` output template live in `.claude/references/audit-convention-scans.md`. Read that file now (path per `## MTK File Resolution`) and follow it; the `conventions.md` template is machine-relevant output — copy it verbatim and do not paraphrase it from memory.

**Majority-verify conventions, never cherry-pick.** A convention is what the codebase does *predominantly*, not what one example happens to do. In the eval, a handler-naming convention was prescribed from a single example while the prescribed form was actually the 32% minority. For every convention claim ("handlers are named X", "money is `decimal`(18,4)"):
- Count BOTH (all) competing forms with a concrete command run from the repo root, e.g. `grep -rEc` or `find … | sed … | sort | uniq -c`.
- Report the DOMINANT form with its proportion (e.g. "`{Verb}{Entity}Handler` — 21/31 handlers, 68%"). If no form exceeds ~60%, call it `[AMBIGUOUS]`/split rather than prescribing one.
- Run counts from the repo root and against the correct directory — verify the path holds the files you think it does before counting (an eval money-precision count came from the wrong directory).

## STEP 2.6: Emit Detected Tools Manifest

Before writing prose architecture documents, emit a machine-readable manifest of the tools and frameworks actually present in this repo. `setup-bootstrap` reads this file to **prune stack reference files that don't apply** (e.g., don't ship a Drizzle data-layer checklist when the repo uses Prismic).

The `.claude/detected-tools.json` schema and its emit rules (empty-array policy, `secondary_stacks` derivation, lowercase hyphenated ids, detection sources, and the STEP 3.6 consumer note) live in `.claude/references/audit-convention-scans.md`. This file is parsed by `setup-bootstrap`, so read that companion now (path per `## MTK File Resolution`) and copy the schema verbatim; do not paraphrase it from memory.

## STEP 3: Generate Architecture Principles Document

Based on everything you found, create `.claude/references/architecture-principles.md`. Every verbatim output template this step and STEP 3.5 / STEP 4 emit — the `architecture-principles.md` skeleton (sections 1-10), the confidence line-format example, the confidence legend block, the `ambiguities.json` schema, the `## Provenance` template, and the STEP 4 results block — lives in `.claude/references/audit-output-templates.md`. These outputs are consumed by `verify-claims.sh` and machine parsers, so read that file now (path per `## MTK File Resolution`) and copy each template verbatim; do not paraphrase them from memory.

### Rules for Generation:
- Document what IS, not what should be. This is a descriptive document.
- Include actual code paths as examples (e.g., "See `src/handlers/user_handler.py`")
- Flag inconsistencies — where the same thing is done differently in different places
- If a pattern is only used in some places, note its adoption percentage
- Be specific about file locations so engineers can find examples
- Don't skip sections — if you found nothing for a section, say "Not found in this codebase"
- **Counter-example gate before absolute language.** Before writing any principle using `NEVER`, `ALWAYS`, `all`, `every`, or `must`, grep for counter-examples. A pattern seen *somewhere* is not a law. Real failures: "all API handlers validate with Yup" (only 1 of 9); "never use `DateTime.UtcNow`" (used in 2 files). If ANY counter-example exists, do not state it as absolute — soften to "most"/"prefer", report the dominant form with its proportion, and tag `[INFERRED:N]` or `[AMBIGUOUS]` (never `[EXTRACTED]`). Reserve absolute language + `[EXTRACTED]` for genuinely zero-counter-example facts.
- **Reproducible numeric claims.** Every numeric claim (project counts, file censuses, "N of M" proportions) must carry the exact shell command that produced it, runnable from the repo root, so `verify-claims` can re-run it. Real failures: "18 projects" (actual 17, propagated to 4 lines); grep counts that don't reproduce. If you cannot produce a reproducible command, drop the number and state the fact qualitatively ("several projects") instead of guessing one.
- **Capability requires a usage site, not just an import.** Do not assert a capability or integration exists from an import/using/package-reference alone. Real failures: "CDK provisions EC2/VPC" inferred from a dead `using Amazon.CDK.AWS.EC2;` (zero VPC/Subnet/SG in code); a dead `AWSSQSResource` (0 references) presented as active "SQS access". Require a USAGE SITE — instantiation, call, or DI registration — before claiming the capability. If only an import exists with no usage, omit it or explicitly mark it `dead/unused reference`.
- **Security-claim grounding.** Never assert that a sanitization / validation / audit / secret-handling path exists unless a usage site is found (imported and called). Real failures: "use the existing dompurify/sanitize-html path" while dompurify is imported nowhere; "never log raw event XML" framed as an existing invariant while code logs raw XML + MQ creds. If the protection is ABSENT, state it as a GAP ("no input sanitization found on X — add it"), not as an existing convention to follow.
- **Interview answers are authoritative.** When `.claude/setup-answers.json` exists, its contents are authoritative human input, not a scan hypothesis. Principles or rules sourced from it cite it as their evidence anchor (e.g. `Evidence: engineer interview — .claude/setup-answers.json (hard_nevers)`) and are never dropped or reworded by regeneration. If a fresh scan contradicts an interview answer, do not silently pick a side — emit a "Needs review" item describing the conflict instead.

### Confidence Tagging (S1.15)

Every principle (or sub-bullet) the audit emits must carry a **confidence tag** so downstream tools (drift detection, code review) know how strict to be. Three tags:

- `[EXTRACTED]` — directly observed in the code. High trust. Drift detection blocks on contradictions.
- `[INFERRED:0.0–1.0]` — pattern inference with explicit confidence (`0.9` strong, `0.7–0.89` reasonable, `<0.7` weak). Drift detection flags rather than blocks.
- `[AMBIGUOUS]` — sources disagree, or the pattern is split. Drift detection notes without verdict.

**Every tagged line must cite evidence** — file:line, a path glob with a hit count, or a commit SHA. No tag without evidence.

**Grade tags by evidence, not vibes (eval fix):** a directly-observable fact with a file:line citation is `[EXTRACTED]` — do not under-tag it `[INFERRED:0.5]` (e.g. EF Core at `Program.cs:61 UseSqlServer` is EXTRACTED). An **absence** claim ("no raw SQL", "no test project") is `[EXTRACTED]` only when you cite the zero-result command that proves it; otherwise tag it `[INFERRED]`.

Format each principle line per the line-format example in `.claude/references/audit-output-templates.md`, and prepend that file's confidence legend block to the top of `architecture-principles.md` (right after the header).

Aim for `[EXTRACTED]` whenever you can; downgrade to `[INFERRED]` only when fewer than 100% of cases match. Use `[AMBIGUOUS]` sparingly — it's an explicit "team decision needed" marker, not a way to dodge analysis.

### Emit Ambiguities Manifest

Every `[AMBIGUOUS]` line the audit writes ALSO lands as an entry in `.claude/.mtk-cache/ambiguities.json`, regenerated wholesale on every audit run (stale file replaced, never appended to):

The `ambiguities.json` schema is in `.claude/references/audit-output-templates.md` (loaded at STEP 3 start).

- One entry per `[AMBIGUOUS]` line emitted this run: `claim` is the line's text, `evidence` its citation, `doc` the file it lives in, `anchor` the section heading (or file:line) it cites.
- `competing_forms` counts come from the majority-verify counting this audit already performs (§ Confidence Tagging above) — never invented.
- No `[AMBIGUOUS]` lines this run → file absent, or `"ambiguities": []`, both read by consumers as "nothing ambiguous."
- Consumed by `setup-bootstrap` STEP 2.5's adaptive interview.

## STEP 3.5: Provenance Section (mandatory)

Add the `## Provenance` section to `architecture-principles.md` using the provenance template (and its `fit == "fallback"` variant) in `.claude/references/audit-output-templates.md` (loaded at STEP 3 start) — copy it verbatim; do not paraphrase it from memory.

The provenance section is not optional. If you produced principles without evidence from the repomap, you either hallucinated or the repomap fell back — either way, disclosure is required.

## STEP 3.6: PR review mining (optional, with --mine-prs)

When `--mine-prs` is passed (or the engineer asks to seed principles from PR feedback), run:

```bash
bash scripts/pr-review-mine.sh --prs 10
```

Each candidate phrase is presented to the engineer for per-line approval. Approved phrases are appended to `.claude/references/architecture-principles.md` with the tag `[MINED:feedback]` and the PR numbers cited as evidence. Untagged or auto-promoted mining is forbidden — see `.claude/references/pr-mining-patterns.md`. Fails soft when `gh` is missing or unauthenticated.

## STEP 3.7: Stamp + verify generated docs

Before reporting completion, every generated doc (`architecture-principles.md`, `conventions.md`) must be (a) stamped with the audit SHA and (b) verified against the codebase. See `.claude/references/audit-grounding.md` for the full ruleset.

### Stamp

The stamp-block format — including the re-run-only `previous-stamp` / `sections-changed` / `claims-delta` delta fields and the constitution (`AGENTS.md`) footer variant — lives in `.claude/references/audit-rerun-migration.md`. Read it now (path per `## MTK File Resolution`) and copy the block verbatim; do not paraphrase it from memory.

**Rule tags:** every prescriptive rule line in `architecture-principles.md` carries `[ENFORCED]` / `[CONVENTION]` / `[ASPIRATIONAL]` with an evidence anchor; untagged rules are quarantined into a `## Untagged (review)` section — full ruleset in `.claude/references/audit-grounding.md` §1.

### Verify-claims pass

Run after writing each generated doc:

```bash
bash scripts/verify-claims.sh .claude/references/architecture-principles.md
bash scripts/verify-claims.sh .claude/references/conventions.md
```

This script:
- parses tagged claim lines,
- grep/AST-checks every backticked evidence anchor against the working tree,
- downgrades zero-hit `[EXTRACTED] → [INFERRED:0.5 unverified]` and `[ENFORCED] → [ASPIRATIONAL unverified]` **in place**,
- writes per-doc reports `.claude/.mtk-cache/weak-claims-<doc>.json` (full) and `.claude/.mtk-cache/weak-claims-<doc>.md` (top-5 paste-ready).

The audit is not complete until verify-claims has run. A passing audit surfaces weak claims; it does not pretend they don't exist.

### Retry loop (one pass)

After the first `verify-claims.sh` run on a doc, read `.claude/.mtk-cache/weak-claims-<doc>.json`. For each downgraded claim, make **one** re-derivation attempt:
- Fix the evidence anchor — the right path, glob, or symbol — so the claim resolves under its original tag, OR
- If no anchor resolves the claim, delete the claim line — **but only if this run generated that line** (byte-identical to the freshly generated template's version). A line the engineer authored or modified is never deleted here: leave the downgraded tag in place for the engineer to resolve. Every deleted line must be itemized in the STEP 4 report.

Rewrite the doc, then run `verify-claims.sh` once more. Downgrades that survive this second pass are accepted and reported as-is. Never re-upgrade a tag (`[INFERRED:0.5 unverified] → [EXTRACTED]`, `[ASPIRATIONAL unverified] → [ENFORCED]`) without a resolving anchor found during the retry. Never loop more than once per doc.

### Seed template cache

After verify-claims (and the retry loop) completes on a fresh audit, snapshot the final stock outputs to `.claude/.mtk-cache/v<MANIFEST_VERSION>/references/` (`architecture-principles.md`, `conventions.md`) and `.claude/.mtk-cache/v<MANIFEST_VERSION>/detected-tools.json` — same layout and retention rules as `setup-bootstrap` STEP 4.8. Without this seed, the next re-run or refresh has no ancestor and must classify these files conservatively as engineer-edited (regen-diff-contract §2), losing the stock fast-path.

**Transient-state lint:** the verify pass drops lines carrying branch names, PR numbers, non-audit dates, and author emails — see `.claude/references/audit-grounding.md` §2.

**Terminology denylist:** the verify pass flags denylisted terminology (recorded in `weak-claims.json` with `reason: terminology-needs-review`, never auto-rewritten) — see `.claude/references/audit-grounding.md` §4.

## STEP 4: Present Results

The verbatim results block to print is in `.claude/references/audit-output-templates.md` (loaded at STEP 3 start; path per `## MTK File Resolution`) — copy it verbatim; do not paraphrase it from memory.

---

## Audit mode invariants
- This mode is read-only except for writing the output document
- Never modify source code during an audit
- If `.claude/references/architecture-principles.md` already exists, use AskUserQuestion before overwriting
- Create `.claude/references/` directory if it doesn't exist
- The actual scan commands live in the tech stack skill — do not duplicate them here. If they need updating, update the tech stack skill.
- **Ignore patterns (S1.14):** Tree walks honor `.mtkignore` at the repo root. Patterns are loaded automatically by `scripts/repomap-tree-sitter.py` (which `scripts/repomap.sh` invokes). Engineers control what the audit "sees" by editing `.mtkignore` — same syntax as `.gitignore`. Missing file is non-fatal; falls back to built-in defaults. Do **not** invent ad-hoc exclude logic in this skill.
- **Shrink-guarded write (S3.16):** When writing or regenerating `architecture-principles.md`, write to a temp file first then promote it via `mtk_guarded_write`. This refuses silent truncation if a partial regenerate would shrink the file > 50% bytes or > 20% lines. Override with `MTK_SHRINK_GUARD_OVERRIDE=1` for intentional rewrites.
  ```bash
  . hooks/lib/shrink-guard.sh
  mtk_guarded_write .claude/references/architecture-principles.md "$tmp"
  ```

---

# MERGE MODE (--merge)

Unify architecture audits from multiple repos (placed under `.claude/references/audits/`) into a single team-wide document. The entire merge flow — locating inputs, cross-audit analysis, the Confidence Tag Merge Rules, the unified-document template, presenting results, and the merge-mode read-only invariants — lives in `.claude/references/audit-merge-mode.md`. Read it now (path per `## MTK File Resolution`) and follow it; do not paraphrase it from memory. The `## STEP` headings below are retained as anchors for cross-skill references; each defers to that companion.

## STEP 0: Locate Inputs

See `.claude/references/audit-merge-mode.md`.

## STEP 1: Analyze Across Audits

See `.claude/references/audit-merge-mode.md`.

## STEP 2: Generate Unified Document

See `.claude/references/audit-merge-mode.md`.

## STEP 3: Present Results

See `.claude/references/audit-merge-mode.md`.
