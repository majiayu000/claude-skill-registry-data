---
name: docgen
description: >-
  Generates and validates project documentation: READMEs, ADRs, changelogs,
  ARCHITECTURE.md, and code documentation. Use when creating, updating, or
  reviewing any non-code markdown artifact, README file, architecture decision
  record, ARCHITECTURE document, CHANGELOG entry, or code documentation
  (docstrings, XML docs, TSDoc). Activates for: (1) scaffolding README,
  CHANGELOG, ADR, CONTRIBUTING, ARCHITECTURE, or SECURITY files; (2) writing
  or reviewing doc comments on exported APIs; (3) auditing documentation
  coverage or staleness; (4) generating release notes from commit history.
metadata:
  token_estimates:
    entry_point: 2800
    full_load: 12000
    max_load: 24000
---

# [H1][DOCGEN]
>**Dictum:** *Documentation is a typed contract between author and reader.*

<br>

Single authority on documentation structure, content requirements, and generation workflow. Routes to task-specific references by document type. Code examples in references align with csharp-standards, python-standards, and ts-standards — those skills remain authority on code discipline; this skill governs documentation discipline.

---
## [1][LOAD_SEQUENCE]
>**Dictum:** *Foundation references apply to every documentation task.*

<br>

**Step 1 — Foundation (always load first)**

| [INDEX] | [REFERENCE]     | [FOCUS]                          |
| :-----: | :-------------- | -------------------------------- |
|   [1]   | `validation.md` | Compliance checklists per type   |
|   [2]   | `patterns.md`   | Documentation anti-pattern codex |

**Step 2 — Task-specific (load per routing table)**

| [INDEX] | [REFERENCE]           | [LOAD_WHEN]                        |
| :-----: | :-------------------- | ---------------------------------- |
|   [3]   | `readme-gen.md`       | README creation or update          |
|   [4]   | `adr.md`              | Architecture decision recording    |
|   [5]   | `code-docs.md`        | Code documentation (any language)  |
|   [6]   | `changelog-gen.md`    | Changelog or release notes         |
|   [7]   | `contributing-gen.md` | CONTRIBUTING.md creation           |
|   [8]   | `architecture-gen.md` | ARCHITECTURE.md creation or update |

**Step 3 — Template (scaffolding only)**

| [INDEX] | [TEMPLATE]                 | [ARCHETYPE]  |
| :-----: | :------------------------- | :----------: |
|   [9]   | `readme.template.md`       |    README    |
|  [10]   | `adr.template.md`          |     ADR      |
|  [11]   | `architecture.template.md` | ARCHITECTURE |

---
## [2][CONTRACTS]
>**Dictum:** *Structural invariants constrain all documentation.*

<br>

**Content discipline**
- **Documentation completes type signature** — encode intent, constraints, failure semantics, domain invariants. Never restate what types and names already communicate.
- **Every document targets one Diátaxis quadrant:** Tutorial (learning), How-To (task), Reference (information), Explanation (understanding). Mixing quadrants produces documents that serve no audience well.

**Generation discipline**
- **Exploration before generation:** Read project structure, dependencies, existing documentation before producing new content. Generated documentation contradicting existing artifacts is worse than no documentation.
- **Code examples are compilable/runnable** — never pseudocode, never truncated. For libraries: importable. For services: `curl` with expected response. For CLIs: exact invocation with output.
- **Audience-first structure:** Organize content by reader need, not by implementation topology.

**Density discipline**
- **Standards docs** (`docs/standards/*.md`): canonical truth about document types. 125-200 LOC.
- **Skill references** (`references/*.md`): generation-specific instructions. <250 LOC each.
- **Templates** (`templates/*.md`): structural skeletons with placeholders, guidance, and checklists. <125 LOC each.

---
## [3][ROUTING]
>**Dictum:** *Task type determines reference loading.*

<br>

| [INDEX] | [TASK]                    | [REFERENCES]        | [TEMPLATE]               | [STANDARDS_DOC]                 |
| :-----: | ------------------------- | ------------------- | ------------------------ | ------------------------------- |
|   [1]   | **README creation**       | readme-gen.md       | readme.template.md       | readme-standards.md             |
|   [2]   | **README update**         | readme-gen.md       | —                        | readme-standards.md             |
|   [3]   | **ADR creation**          | adr.md              | adr.template.md          | adr-standards.md                |
|   [4]   | **ADR review**            | adr.md              | —                        | adr-standards.md                |
|   [5]   | **Code documentation**    | code-docs.md        | —                        | code-documentation-standards.md |
|   [6]   | **CONTRIBUTING creation** | contributing-gen.md | —                        | —                               |
|   [7]   | **ARCHITECTURE creation** | architecture-gen.md | architecture.template.md | architecture-standards.md       |
|   [8]   | **ARCHITECTURE update**   | architecture-gen.md | —                        | architecture-standards.md       |
|   [9]   | **Changelog entry**       | changelog-gen.md    | —                        | changelog-standards.md          |
|  [10]   | **Release notes**         | changelog-gen.md    | —                        | changelog-standards.md          |
|  [11]   | **Doc validation/audit**  | validation.md       | —                        | (all applicable)                |

---
## [4][DECISION_TREES]
>**Dictum:** *Branching tables route ambiguous tasks.*

<br>

**Document type selection:**

| [INDEX] | [SIGNAL]                                     | [DOCUMENT_TYPE]  |
| :-----: | -------------------------------------------- | :--------------: |
|   [1]   | New project, no README exists                |      README      |
|   [2]   | New directory with 2+ docs, no index         |   README (hub)   |
|   [3]   | Monorepo package missing documentation       | README (package) |
|   [4]   | Architectural choice with alternatives       |       ADR        |
|   [5]   | Version release, feature completion          |    Changelog     |
|   [6]   | New/modified exported API surface            |     Code-Doc     |
|   [7]   | New project accepting external contributions |   CONTRIBUTING   |
|   [8]   | System with 10k+ LOC needing structural docs |   ARCHITECTURE   |
|   [9]   | Existing documentation accuracy concern      |    Validation    |

**README scope routing:**

| [INDEX] | [CONTEXT]                                   |      [SCOPE]      | [REFERENCE_SECTION]      |
| :-----: | ------------------------------------------- | :---------------: | ------------------------ |
|   [1]   | Project root, full project documentation    |   Project root    | readme-gen.md §3.1 row 1 |
|   [2]   | `packages/*` or `apps/*` in monorepo        | Package/workspace | readme-gen.md §3.4       |
|   [3]   | `src/modules/*` or bounded context boundary |  Module/feature   | readme-gen.md §3.1 row 3 |
|   [4]   | `docs/` or directory with child `.md` files |   Directory hub   | readme-gen.md §3.3       |

**README audience routing:**

| [INDEX] | [AUDIENCE]      | [SECTION_DEPTH]              | [EMPHASIS]           |
| :-----: | --------------- | ---------------------------- | -------------------- |
|   [1]   | **Evaluator**   | Title, Description, Badges   | Problem/solution fit |
|   [2]   | **Adopter**     | + Install, Usage, License    | Time to first value  |
|   [3]   | **Contributor** | + Architecture, Contributing | Orientation velocity |

**Code doc language routing:**

| [INDEX] | [LANGUAGE]     | [FORMAT]          | [EFFECT_TYPE_DOCS]                      |
| :-----: | -------------- | ----------------- | --------------------------------------- |
|   [1]   | **C#**         | XML Documentation | `Fin<T>` success/failure in `<returns>` |
|   [2]   | **Python**     | Google Style      | `Result[T,E]` in Returns section        |
|   [3]   | **TypeScript** | TSDoc             | `Effect<A,E>` in `@returns` tag         |

---
## [5][ANTI_PATTERNS]
>**Dictum:** *Named violations enable precise correction.*

<br>

Summary table — full examples in `patterns.md`.

| [INDEX] | [PATTERN]          | [SYMPTOM]                                        | [CORRECTION]                                |
| :-----: | ------------------ | ------------------------------------------------ | ------------------------------------------- |
|   [1]   | TROPHY_README      | Lists every file; no architecture explanation    | Audience-tiered progressive disclosure      |
|   [2]   | COMMIT_CHANGELOG   | Git log dumped as changelog entries              | User-facing language grouped by category    |
|   [3]   | WALL_OF_TEXT_ADR   | Context section narrates history                 | Bullet-point facts with explicit unknowns   |
|   [4]   | PARAMETER_NOISE    | `@param name` repeats "the name"                 | State constraint, range, or semantic origin |
|   [5]   | STALE_DOCS         | Documents removed/changed functionality          | Couple doc updates to code change workflow  |
|   [6]   | PSEUDOCODE_EXAMPLE | Code examples that won't compile/run             | Extractable, testable examples only         |
|   [7]   | AUDIENCE_MIXING    | Single doc targeting evaluators and contributors | One Diátaxis quadrant per document          |
|   [8]   | TYPE_RESTATING     | Comment says "Returns string" on `-> str`        | Document what types cannot express          |

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent documentation debt.*

<br>

[VERIFY]: Per-task completion — select checklist from `validation.md` matching document type.

[IMPORTANT]:
1. [ALWAYS] Load `validation.md` before marking any documentation task complete.
2. [ALWAYS] Verify code examples compile/run in the target language.

[CRITICAL]:
- [NEVER] Skip negative consequence documentation in ADRs.
- [NEVER] Ship a README without a runnable Usage example.
- [NEVER] Document code by restating type signatures.
