---
name: project-explorer
description: Heuristics + operating manual for the project-explorer runtime agent that bootstraps a DDD domain wiki under docs/domain/ from a fresh repository.
version: 1
consumed_by: project-explorer agent
---

## Purpose

This skill is the operating manual the `project-explorer` runtime agent reloads at the start of every run. It is the auditable source for the heuristics that drive `docs/domain/` generation — DDD code signals, ubiquitous-language extraction, known failure modes, conflict resolution, and the Evans-canonical output schema. The agent treats this file as authoritative for the run; co-located `research.md` carries the long-form citations and per-category enumerations that this file cites by reference.

## Inputs

- `<path>` (required) — local filesystem path to the target repository. No remote URLs; no cloning; no git invocation. The agent reads the path read-only.
- `[branch-name]` (optional) — recording-only string. Written to the `branch_name` field in each generated file's frontmatter. The user is responsible for actually checking out the branch they want recorded before invoking the command — the agent does not switch branches.

## Idempotency guard

Before reloading this skill (operating procedure step 2), the agent checks `docs/domain/` of the **current working directory** (not `<path>`).

**Refuse condition.** `docs/domain/` exists AND contains at least one non-hidden file when searched recursively. "Hidden" means the filename starts with `.` — the POSIX convention; the Windows filesystem hidden attribute is not consulted. Examples of hidden files that do NOT trigger refusal: `.git`, `.DS_Store`, `.gitkeep`.

**Proceed condition.** `docs/domain/` is missing, OR `docs/domain/` exists but contains no non-hidden files (recursive). Empty subtrees alone do not trigger refusal — only at least one non-hidden file (recursive) triggers.

**Refusal message.** When the refuse condition is met, the agent prints the literal message:

```
docs/domain/ is not empty. project-explorer is a one-shot bootstrapper. Use project-update for updates.
```

and exits before the skill-load step (step 2 of `## Operating procedure`) continues. No repo walk, no candidate surfacing, no writes.

## Operating procedure

Numbered steps 1-7. Mirror the Core Behaviour list in the feature's overview plan. The agent must execute these in order; later sections fill in the precise contract for each step.

1. **Idempotency guard.** Resolve `<path>`; check the current working directory's `docs/domain/`. If it exists and is non-empty, refuse with a canonical message pointing the user at the sibling `project-update` and exit before any further step runs. See `## Idempotency guard` above.
2. **Skill load.** The agent reloads this `SKILL.md` and treats it as the operating manual for the rest of the run. The agent must not proceed past this step if the skill file is missing or malformed.
3. **Repo walk.** The agent scans `<path>` for the code signals enumerated in `## Code signals` below — aggregates, repositories, events, services, value objects, and ubiquitous-language tokens. .NET signals are first-class; other stacks are best-effort. Excludes test projects, generated files, `bin/`, `obj/`, `node_modules/`, `dist/`.
4. **BC candidate surfacing.** The agent groups the signals into bounded-context candidates using repo namespacing / top-level project boundaries / folder structure. Names must trace to a real namespace or folder path; no invented taxonomy. See `## BC candidate surfacing` below.
5. **Print candidate report (non-blocking).** The agent prints the candidate BC list (with rationale, detected aggregates, and the small-repo-fallback flag if triggered) to the user for the audit trail, then proceeds directly to output generation. No human approval is required; the agent does not halt. See `## BC candidate surfacing` below.
6. **Output generation.** After printing the candidate report, the agent writes the full Evans-canonical tree under `docs/domain/`. _The full per-file content contract (which fields each file carries, the `file:line` invariant back-reference rule, the small-repo-fallback variant, the write order) is specified in `### Per-file content contract` below._
7. **Frontmatter recording.** Every generated file under `docs/domain/` carries a four-field YAML frontmatter block (`source_repo`, `branch_name`, `generated_at`, `skill_version`) as the very first content in the file, before any heading. See `## Frontmatter contract` below.

## BC candidate surfacing

This section is the full contract for steps 4 and 5 of the `## Operating procedure`. The runtime agent must consult this section verbatim — the spec lives here, not in the agent's body.

### Grouping rule

BC candidates MUST be derived from observable repo namespacing, top-level project boundaries, or folder structure observed during step 3 (repo walk). Each candidate name MUST trace to a real namespace token or folder path. Names that do not trace to source MUST be rejected before the candidate report is printed — the agent does not invent taxonomy.

When namespace and folder structure disagree, the agent prefers the namespace as the canonical name and records the folder path in the candidate's rationale.

### Reverse mapping (BC -> source paths)

**What it inverts.** This is the strict inverse of `### Grouping rule`. The forward rule maps a source namespace token / folder path **into** a BC candidate name; this rule maps a `docs/domain/<bounded-context>/` folder name **back out** to the set of source paths that currently map into it. It is the single source of truth's inverse and is cited-by-reference (never forked) wherever it is consumed — mirror the cite pattern the `## Path -> BC classifier` `### Namespace -> BC mapping` already uses for the forward `### Grouping rule`. This rule does NOT restate the forward rule's namespace/folder mechanics; for those it points at `### Grouping rule`.

**The deterministic inversion mechanism.** Given a `docs/domain/<bc>/` (a.k.a. `docs/domain/<bounded-context>/`) folder name, the agent re-applies the `## BC candidate surfacing` `### Grouping rule` namespace/folder correspondence **against the current `<path>` working tree** the explorer already reads read-only: it resolves the set of source directories/files whose namespace token or folder path maps to that BC name under the forward rule. This is a deterministic re-application of a defined mechanism, not a free-text guess. It honours the forward rule's existing tie-break clause by reference — `### Grouping rule`'s "when namespace and folder structure disagree, the agent prefers the namespace as the canonical name and records the folder path in the candidate's rationale" — so name -> path resolution traces through either a namespace token OR a folder path exactly as the bootstrap recorded it. The tie-break is attributed to `### Grouping rule`, not re-decided here.

**Output shape.** The result is the set of source paths (directories and/or files) for that one BC, expressed as the `<bc-source-paths>` argument list: space-separated, repo-root-relative POSIX pathspecs (forward slashes, matching the `source_repo` slash-normalization in `## Frontmatter contract`), passed after `--` to `git diff <base>..HEAD -- <bc-source-paths>` — the command the per-BC pre-check consumes. Because the inversion is taken against the working tree and the resulting pathspecs are handed to a commit-range diff, a pathspec that no longer exists at HEAD simply contributes no diff for that path (git resolves it against the range; an absent path yields an empty diff for that pathspec, never an error).

**The conservative empty/unresolvable rule (the false-SKIP safety valve).** If the inversion resolves to an **empty or unresolvable path set** — the folder name does not trace back to any current namespace/folder; the BC was renamed, merged, or split since bootstrap; or the name is ambiguously spread across multiple folders — the result is treated as **"cannot determine slice" -> no skip -> full regen**, the same conservative posture a missing SHA forces in the per-BC pre-check. As a named special case, the `module-map` fallback token (the small-repo single-BC name from `### Small-repo fallback detection`) is **always** treated as unresolvable -> no skip -> full regen: `module-map` is an explicit fallback-mode token, not a discovered BC, so it has no clean source-path inversion and there is nothing to optimize in single-BC fallback mode. Ambiguity therefore degrades to **over-regen, never to under-skip**; a false SKIP is **impossible by construction**.

**No-cache note.** The path set is **re-derived every run** from the working tree and is **never** persisted to frontmatter — caching it would add a new frontmatter field (the requirement freezes the frontmatter surface beyond `last_generated_sha`) and the cached field would itself drift from the forward `### Grouping rule`.

### Candidate report format

The candidate report is a markdown block the agent prints to the user for the audit trail before writing. Format:

1. `### BC candidates` — numbered list. One numbered item per candidate BC. Per-candidate nested bullets:
   - **Rationale** — one line naming the folders / namespaces that contributed (e.g., `folder: src/Ordering`, `namespace: eShop.Ordering`).
   - **Aggregates detected** — bulleted list; each entry names the aggregate root and cites `file:line` as an inline-code span (e.g., `` `src/Ordering/Order.cs:42` ``).
2. `### Fallback flag` — single line with the boolean and explanation (see `### Small-repo fallback detection` below).
3. `### Conflicts detected` — bulleted list of every divergent definition the walker found, per the conflict-resolution rule (see `./research.md#what-to-do-when-code-as-source-of-truth-conflicts-with-itself`). Each entry cites both divergent definitions by `file:line`. Empty list is rendered as `(none)`. The agent never silently picks a side without listing the conflict here. The format includes a `### Conflicts detected` subsection at the bottom of the report; entries cite both divergent definitions by `file:line` per the conflict-resolution rule.

### Small-repo fallback detection

The fallback fires when at least one of these three triggers holds. Triggers are independent — any one match flips the flag to `true`.

1. Total first-class source files in `<path>` are `< 20`. First-class source files are files matched by the language whitelist `*.cs`, `*.fs`, `*.vb`, `*.ts`, `*.js`, `*.py`, `*.java`, `*.go` minus paths matching the exclusion globs `**/bin/**`, `**/obj/**`, `**/node_modules/**`, `**/dist/**`, `**/*Tests/**`, `**/*.Tests/**`, `**/*.generated.*`, `**/*Designer.cs`. Files are matched against the language whitelist after the exclusion globs (so markdown / config / generated files do not count; `.py` files anywhere under `<path>` that survive the exclusion globs do count).
2. Only one top-level namespace or project exists across the walked source set. Zero namespaces is treated as `<= 1` and fires this trigger naturally.
3. BC candidate count after grouping is `<= 1`.

The fallback flag is reported as a single boolean (`true` / `false`) accompanied by an explanation that enumerates which of the three triggers fired. Example explanation when triggers (i) and (iii) both fire: `triggers fired: (i) total source files = 7 < 20; (iii) BC candidate count = 1`.

When the flag is `true`, the candidate report includes the literal token `FALLBACK: single-BC module-map` on its own line. The fallback path writes automatically like any other run — no human approval is required.

### Auto-write contract

This agent is **fully agent-driven**: after printing the candidate report (`### Candidate report format`), the agent proceeds directly to output generation under `docs/domain/`. There is **no APPROVE gate, no halt, and no edit-revision loop** — the agent surfaces its BC decisions in the printed report for the audit trail, then writes immediately. The only thing that stops a run is the `## Idempotency guard` (refuses when `docs/domain/` is already non-empty); that guard is a re-run safety check, not an approval gate.

## Code signals

Concrete observable code patterns per DDD category. See `./research.md#ddd-code-signals` for the full enumeration (5 categories, >=3 signals each, .NET first-class, other stacks best-effort).

## Ubiquitous-language heuristic

Heuristic for extracting candidate glossary terms from code. See `./research.md#ubiquitous-language-extraction-heuristic` for the named heuristic and step-by-step recipe.

## Soft input: docs/narrative/

### When narrative is read

After the repo walk completes (operating procedure step 3) and before BC candidate surfacing begins (operating procedure step 5), the agent checks the working directory's `docs/narrative/` for two file kinds: `docs/narrative/architecture.md` and any `docs/narrative/<bc>/walkthrough.md` files. The check is filesystem-only — no git, no remote, no cloning. If neither path exists, the agent skips the entire `## Soft input: docs/narrative/` section and proceeds to BC candidate surfacing with no narrative input — this is the backward-compat no-op path.

### Backward-compat invariant

When `docs/narrative/` is absent or empty, the agent's behaviour is **byte-identical** to runs before this section was added. The output schema, frontmatter contract, write order, hallucination guard, and auto-write contract all run unchanged. Specifically: a downstream repo that has never invoked `/project:overview` MUST produce the same `docs/domain/` tree (modulo `generated_at` timestamp and `last_generated_sha` when HEAD has moved) as it produced before this hook landed. Any divergence is a regression.

### How narrative augments BC candidate surfacing

- **(a) BC candidate ordering.** When `docs/narrative/architecture.md` contains a `## Logic overview` section listing BCs in narrative order, the agent uses that order as the **display order** for the BC candidate report in step 5. The underlying candidate list (which BCs surface) is unchanged — only the order in which they appear in the report changes.
- **(b) Per-aggregate description seeds.** When `docs/narrative/<bc>/walkthrough.md` contains drill-down sections for a detected endpoint or handler, the agent may use the plain-language description from that drill-down as a seed for the BC's per-aggregate description in the candidate report's rationale line. The seed is a **suggestion only** — the agent must still cite `file:line` for the aggregate detection itself. Plain-language text without a `file:line` citation is never elevated to the canonical aggregate doc.
- **(b-marker) Rationale-line narrative marker.** When narrative augmented a BC's surfacing (one or both of (a) ordering / (b) description seed applied for THIS candidate), the candidate report's `Rationale` line gains a third comma-separated entry of the literal form `narrative: docs/narrative/<bc>/walkthrough.md` (relative path, lowercase, trailing-slash on the bc folder name only). Existing entries (`folder: ...`, `namespace: ...`) remain byte-identical and appear before the narrative entry in source-of-truth order (folder, namespace, narrative). When the narrative did NOT augment this candidate (e.g., narrative absent, narrative malformed, or narrative present but no rule (a)/(b) applied to THIS bc), the `narrative:` entry is omitted entirely. This is the grep-able marker for narrative augmentation.
- **(c) BC name preference (advisory).** When `docs/narrative/<bc>/` exists as a folder, the agent may prefer the folder name as the candidate BC's display name (over the namespace token) IF the namespace token and folder name disagree. The fallback to the namespace token still applies when no narrative folder exists. This rule is advisory — the underlying grouping rule (`### Grouping rule`) is not changed.

### Hallucination guard (narrative variant)

Soft input is *input*, not *source of truth*. Code remains the source of truth for every `file:line` citation, every aggregate detection, every event/command/repository/service row in the output schema. The agent MUST NOT invent a `file:line` citation, an aggregate, an event, or a BC because the narrative says so. The narrative shifts BC display order and seeds plain-language descriptions; it never adds rows to the output schema. If the narrative claims a BC the code walk does not detect, the agent logs the divergence in `context-map.md`'s `## Skipped candidates` H2 section as `<narrative-claimed-bc>: not detected by code walk (narrative said exists; no namespace / folder match)`. The narrative-claimed BC is NOT promoted to a `<bounded-context>/` folder.

### Malformed narrative degraded path

If `docs/narrative/architecture.md` or any `docs/narrative/<bc>/walkthrough.md` file exists but its YAML frontmatter does NOT parse (missing block, malformed YAML, or fewer than the four sibling-parity fields `source_repo` / `branch_name` / `generated_at` / `skill_version` present), the agent logs the literal line `narrative file at <absolute-path>: malformed (frontmatter does not parse); skipping soft-input augmentation` (substituting the actual absolute path of the offending file) and proceeds as if that file did not exist — the narrative-absent backward-compat no-op path. No stop condition fires. `last_generated_sha` is tolerate-missing and does NOT count toward the four required fields.

## Output schema

The agent emits an Evans-canonical tree under `docs/domain/` of the working directory. The five subsections below define exactly which files are written, what content each file carries, how the small-repo fallback degrades, the write order, and the hallucination guard. Frontmatter contract for every emitted file is defined in `## Frontmatter contract`; every file under `docs/domain/` carries the four-field YAML block as its first content.

### Files written

```
docs/
  domain/                           # OUTPUT TARGET (written at runtime, not at scaffold-author time)
    context-map.md
    glossary.md
    <bounded-context>/
      glossary.md
      aggregates/<aggregate>.md
      events.md
      commands.md
      repositories.md
      services.md
```

### Per-file content contract

All `file:line` citations in the output tree use paths relative to the `<path>` root the agent was invoked against. Empty sections are rendered as `(none)` rather than omitted, preserving the locked file shape for downstream `project-update`. Frontmatter contract is defined in `## Frontmatter contract`; every file under `docs/domain/` carries the four-field YAML block as its first content.

| File | Required content |
|---|---|
| `context-map.md` | Numbered list of confirmed BCs (one per `<bounded-context>/` folder); one short paragraph per BC describing relationships to other BCs (upstream / downstream / shared kernel / partnership / customer-supplier / open-host service / anti-corruption layer). Ends with a `## Conflicts detected` H2 section (bulleted list of `<conflict-description>: <file:line>, <file:line>`; `(none)` when empty) and a `## Skipped candidates` H2 section (bulleted list of `<candidate-name>: <reason for omission>`; `(none)` when empty). |
| `glossary.md` (repo-wide) | Term -> definition markdown table built from the ubiquitous-language extraction heuristic (`research.md#ubiquitous-language-extraction-heuristic`). Header row: `\| Term \| Definition \|`. Terms appearing across `>= 2` BCs go here; BC-local terms go in the per-BC glossary. `(none)` when the heuristic finds no cross-BC terms. |
| `<bounded-context>/glossary.md` | Term -> definition markdown table scoped to that BC. Same header row as the repo-wide glossary. `(none)` when no BC-local terms. |
| `<bounded-context>/aggregates/<aggregate>.md` | Aggregate name as `# <AggregateName>` H1 + bulleted invariants list. At least one invariant per aggregate file, each invariant carrying a `file:line` citation as an inline-code span (e.g., `` `src/Ordering/Order.cs:42` ``). If no behavioural invariants are detected the file is still emitted with a single bullet `(no invariants detected; see <ServiceName> at \`file:line\` for likely behaviour)` per the anemic-domain-model failure mode (`research.md#known-failure-modes`). The per-BC `aggregates/` directory is emitted as a directory even when empty (no placeholder file inside). |
| `<bounded-context>/events.md` | Markdown table: `\| Name \| Emitting aggregate \| file:line \|`. One row per detected domain event. `(none)` body when no events detected. |
| `<bounded-context>/commands.md` | Markdown table: `\| Name \| Target aggregate \| file:line \|`. One row per detected command. `(none)` body when no commands detected. |
| `<bounded-context>/repositories.md` | Markdown table: `\| Name \| Target aggregate \| file:line \|`. One row per detected repository interface. `(none)` body when no repositories detected. |
| `<bounded-context>/services.md` | Markdown table: `\| Name \| Behavior summary \| file:line \|`. One row per detected domain service. `(none)` body when no services detected. |

### Small-repo fallback variant

When the small-repo fallback flag is `true`, the writer emits the same file shape with exactly **one** `<bounded-context>/` folder named `module-map`. All other rules in `### Per-file content contract` still apply inside `module-map`. The `context-map.md` body begins with the single line `Fallback active: single-BC module-map. See \`module-map/\` for module-by-module breakdown.` (replacing the numbered BC list that multi-BC mode would emit). The `## Conflicts detected` and `## Skipped candidates` H2 sections at the bottom of `context-map.md` are emitted as in multi-BC mode.

### Write order

The agent writes top-level files first, then each `<bounded-context>/` folder. Within a BC folder, files are written in this order:

1. `docs/domain/context-map.md`
2. `docs/domain/glossary.md`
3. For each `<bounded-context>/` (alphabetical by folder name): write the BC folder in this order:
   1. `<bounded-context>/glossary.md`
   2. `<bounded-context>/aggregates/<aggregate>.md` files (one per detected aggregate, alphabetical by aggregate name)
   3. `<bounded-context>/events.md`
   4. `<bounded-context>/commands.md`
   5. `<bounded-context>/repositories.md`
   6. `<bounded-context>/services.md`

In small-repo fallback mode the single `module-map/` folder follows the same per-BC ordering.

### Hallucination guard

Every multi-BC `<bounded-context>/` folder name MUST match a real namespace token or folder path observed during the repo walk (per `## BC candidate surfacing` `### Grouping rule`). Names with no source MUST NOT be emitted; the writer logs each omission in `context-map.md` under the `## Skipped candidates` H2 section as `<candidate-name>: <reason for omission>`. The `## Skipped candidates` section renders as `(none)` when the writer rejected nothing.

The guard rule applies in multi-BC mode only. In small-repo fallback mode the single folder is emitted with the literal name `module-map` regardless of whether the target repo has a namespace or folder by that name — `module-map` is an explicit fallback-mode token, not a discovered BC, and is exempt from the trace-to-source rule.

## Frontmatter contract

Every file the agent emits under `docs/domain/` carries a four-field YAML frontmatter block as its **first content**, before any heading. The contract:

- **`source_repo`** — the `<path>` argument resolved to an absolute path, normalized to POSIX-style forward slashes (the agent normalizes Windows backslashes to forward slashes). Trailing slashes are stripped. UNC paths and symlinks are passed through as the OS resolves them; this contract does not enforce a specific transformation beyond slash normalization.
- **`branch_name`** — the `[branch-name]` argument as a YAML scalar when supplied (e.g., `branch_name: main`). When the argument is omitted, the value is the bare YAML `null` token (which parses as the YAML null value), NOT the quoted string `"null"`.
- **`generated_at`** — ISO-8601 UTC timestamp with second precision and the literal `Z` suffix, e.g., `2026-05-18T10:30:00Z`. Sub-second precision is not used. The timezone is always UTC.
- **`skill_version`** — integer matching the `version` field of this SKILL.md's YAML frontmatter (currently `1`). If a future revision of this skill bumps the `version` field, the writer stamps the new integer; the contract has no auto-track magic.

Example frontmatter block emitted at the top of every file under `docs/domain/`:

```yaml
---
source_repo: C:/repos/eShopOnContainers
branch_name: main
generated_at: 2026-05-18T10:30:00Z
skill_version: 1
---
```

The frontmatter block is the **first content** in every file under `docs/domain/`, before any heading or paragraph. If a heading appears before the frontmatter block, the file is malformed.

## Failure modes

Known DDD modeling failure modes the agent must watch for during the walk. See `./research.md#known-failure-modes`.

## Conflict resolution

What to do when two parts of the codebase disagree on the same invariant. See `./research.md#what-to-do-when-code-as-source-of-truth-conflicts-with-itself`.
