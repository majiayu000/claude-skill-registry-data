---
name: woostack-init
description: Create or maintain root README.md, AGENTS.md, DESIGN.md, PRODUCT.md, and ARCHITECTURE.md; also initialize or repair local .woostack/ support when explicitly requested.
---

# woostack-init

Help the user create or improve the root README and project guidance: accurate, repository-specific,
useful for decisions, concise, and maintainable. Inspect before asking, consult before writing,
preserve what works, and apply only changes the request authorizes. A rerun may make no changes.

## Command and scope

```text
/woostack-init [path]
```

The default intent is guided document authoring, including root `ARCHITECTURE.md`. Honor a request
limited to one document or to review, planning, or drafts; architecture-only requests do not edit
other root documents. An explicit local-support setup/repair request, including Doctor's
missing-support referral, goes directly to [Local support](#local-support) without a document
consultation. When both intents are requested, keep their authorization and verification separate.

Document work requires no `.woostack/`, GitHub policy validation, Doctor, GitHub access, or
dependency installation. Missing support or an unrelated malformed setting must not block drafting.
Load support helpers and contracts only for relevant support work.

## Guided authoring

1. **Inspect the evidence.** Resolve the target and requested scope without changing it. Read relevant
   conversation decisions, existing root and scoped agent instructions, README/contributor guidance,
   product/design/architecture documents and their canonical sources, representative source,
   entrypoints, manifests, configuration, scripts, and CI.
   Prepare a brief opening summary of the current understanding, which in-scope documents need
   creating, updating, or preserving, and what should stay. Distinguish observed implementation,
   documented intent, and proposed direction; surface contradictions rather than silently choosing
   one. Preserve the authority and scope of existing instructions.
   When verification guidance is relevant to scope, inspect the repository's actual tools, commands,
   instructions, CI, test suites, and available timing evidence, distinguishing demonstrated bottlenecks
   from unmeasured concerns. An adequate verification setup is a valid no-op.
2. **Consult before drafting.** Open the discussion with the opening summary, then ask
   repository-informed questions and wait for the user's response before drafting or writing any
   document, even when the existing repository appears comprehensive. A general request to
   initialize or update documents is not permission to skip this consultation, and ordinary edit
   authorization never silently waives it. For a general run, discuss the areas relevant to the
   requested documents: intention (why the repository exists, whom it serves, the problem it
   should solve, desired outcomes, and non-goals), general structure (the intended organization
   and responsibilities of its major apps, packages, modules, and documents; which existing
   arrangements are deliberate and worth preserving), direction (near-term priorities, longer-term
   ambitions, product and design principles, constraints, and tradeoffs), and architecture
   (intended boundaries, dependencies, important interactions and data flows, and rationale that
   source code alone cannot establish). These are discussion areas, not a fixed question bank:
   read factual details from the repository rather than asking the user to inventory it, and ask
   about the intention and rationale behind those facts. A scoped update consults only its
   relevant decisions and never becomes an unrelated whole-repository interview.
   When `AGENTS.md` is in scope, establish project stage and actual consumers, compatibility
   commitments (including an explicit "none" when confirmed), and which data/environments must
   survive changes or are explicitly disposable. These are separate decisions: an unreleased
   label or `0.x` version alone establishes neither an absence of consumers nor disposable data.
   Preserve existing commitments unless the user explicitly changes them; unresolved answers
   stay unresolved. Use the [AGENTS.md guidance](references/document-schemas.md#agentsmd) to
   translate confirmed decisions into operational instructions.
   Ask a manageable initial set, then wait. Use each response to revise the understanding and
   choose follow-ups that respond to earlier answers, including answers that contradict
   assumptions inferred from existing code; clarify implications, contradictions, and meaningful
   unresolved choices instead of mechanically advancing through a fixed checklist. Reuse answers
   already supplied: when prior answers establish the relevant decisions, present the resulting
   understanding and ask what, if anything, should change rather than re-running the interview.
   Offer recommendations and tradeoffs when useful, and keep material decisions explicitly
   deferred rather than inventing certainty. Never create or modify documents in the same turn as
   unanswered interview questions. Honor an explicit request to proceed without questions; the
   agent's confidence alone is not an exception. Without answers, draft only from observed
   evidence and mark remaining decisions unresolved instead of inventing missing facts.
   For verification recommendations, use the [testing principles](references/tdd.md): prefer
   removing redundant work and configuring native capabilities before adding or replacing tools.
   Investigate only warranted options against current authoritative ecosystem sources; preserve
   settled viable choices and compare compatibility, correctness, execution cost, migration effort,
   and maintenance. Keep current setup, agreed direction, and unimplemented recommendations
   distinct, with tradeoffs and verification rather than unmeasured speedup claims.
3. **Draft focused guidance.** Draft from the agreed understanding, keeping current implementation,
   agreed future direction, and deferred decisions distinct, and never representing proposed or
   deferred architecture as already implemented. Product → design → agent instructions is a useful
   draft order, not a required sequence. Use the
   [document responsibilities](#document-responsibilities) and
   applicable [document schemas](references/document-schemas.md). Create missing guidance, replace
   empty or placeholder content with supported guidance, or make targeted revisions, preserving
   useful project-specific content.
   Identify stale, contradictory, and duplicated material for removal rather than appending another
   generated layer. Link to canonical specifications, architecture decisions, design systems, and
   contributor guidance instead of copying them; propose consolidation before replacing established
   documents. Never invent commands, metrics, architectural rationale, or settled decisions.
   Repository manifests and CI configuration remain authoritative for adopted tooling. Record verified
   command existence, working directory, and conditions; keep current commands distinct from proposals
   under the [document schemas](references/document-schemas.md). Preserve scoped instructions.
4. **Review meaningful changes and apply authorized edits.** Present the proposed result, calling out
   changes to product direction, design or architectural constraints, and agent permissions.
   Reuse authorization already given; do not add approval ceremonies for individual headings or
   paragraphs. Review-only, draft-only, or planning requests write nothing. Unapproved scope expansion
   remains a proposal.
   Tooling and verification recommendations are advisory under [Boundaries](#boundaries).
   Preserve unrelated work, file ownership, and existing file/symlink relationships: verify a linked
   target's identity and authorization before editing it, never replace the link or write through an
   unsafe or ambiguous path. A blocked write does not prevent presenting a draft.
5. **Verify within scope.** Check the applicable schema, consistency across affected documents,
   referenced paths/links, and technical claims against current repository evidence. Verify a format
   before adding its version marker; report applicability limits and unresolved conversions. Use
   relevant safe checks authorized by the request and project rules; distinguish commands inspected
   from commands actually executed.
   Do not run unrelated setup, network operations, or side-effectful commands to validate prose.
6. **Report the result.** State what was created, updated, intentionally preserved, or blocked, the
   verification evidence, and unresolved decisions. Report any unimplemented recommendations,
   tradeoffs, and verification approaches separately from current setup and agreed direction. Leave
   good guidance unchanged rather than rewriting it for stylistic novelty.

## Document responsibilities

Use the current applicable [document formats](references/document-schemas.md), not an exhaustive
template or the same questionnaire for every project. Omit irrelevant sections. Preserve an
established architecture-focused meaning of `DESIGN.md`; the visual schema does not replace it.

| Document | Purpose | Useful content |
| --- | --- | --- |
| `README.md` | What is this project, and how do I start using it? | The [README contract](references/document-schemas.md#readmemd): evidence-backed identity, shortest verified first-use path, representative usage, and navigation to canonical docs and policies. |
| `PRODUCT.md` | What are we building, for whom, and why? | The [product record](references/document-schemas.md#productmd): users, purpose, operating context, capabilities, constraints, and confirmed principles. Separate current scope from future direction. |
| `DESIGN.md` | How should the product work and feel? | The [visual format](references/document-schemas.md#designmd) where applicable: observed or agreed identity, tokens, components, and usage. Preserve canonical system-design decisions where the document already owns them. |
| `ARCHITECTURE.md` | Where should a change live, how do the parts interact, and what boundaries must it preserve? | [Technical orientation](references/document-schemas.md#architecturemd): major responsibilities and paths, important relationships and flows, constraints, and supported decision links. |
| `AGENTS.md` | How should an agent work effectively in this repository? | [Unversioned operational Markdown](references/document-schemas.md#agentsmd): actual commands and working directories, conditional verification, boundaries, pitfalls, and links to deeper documentation. |

Keep `AGENTS.md` operational: no copied product specification, exhaustive file inventory, generic
coding advice, or duplicated Woostack workflows. When `AGENTS.md` is also in the authorized scope,
include or refine short conditional pointers to `PRODUCT.md`, `DESIGN.md`, and `ARCHITECTURE.md`
where applicable. Explain when to read architecture guidance, such as before changing component
boundaries or cross-component flows; link rather than copying content or assuming automatic loading.
When creating or updating `AGENTS.md` during Woostack adoption, write a concise,
availability-aware routing paragraph locally from this wording, replacing unconditional Woostack
usage or installation requirements:

```markdown
Use woostack skills when available. At the start of work, `using-woostack` may load
project rules and route `/woostack-*` requests to the matching installed skill when it
is installed; it is an optional navigation aid, not a conduit. Each installed skill
carries its own activation, authority, approval, and completion behavior, so a missing
router or sibling skill must not block ordinary repository work. If woostack skills
are unavailable, follow this file and continue ordinary work with the host's available
capabilities; installation is not required. For an explicit `/woostack-*` command whose
skill is unavailable, name the missing skill and ask whether to install it or proceed
without it before continuing.

Follow this file first when it conflicts with generic agent defaults.
```

Adoption output must not require another skill, the source checkout, or a shared runtime.
Do not copy the workflow catalog or flatten scoped instructions.

## Local support

Use this secondary path only for explicit support initialization/repair. It stays local-only and
provider-free and does not require product/design decisions or document edits.

1. Resolve the canonical target repository without changing it. Verify repository root, branch,
   working state, existing `.woostack/` files, and collision/symlink/path safety.
2. Resolve effective local policy with
   [`scripts/config/resolve-config.sh`](scripts/config/resolve-config.sh). It merges tracked
   `.woostack/config.json` with the optional primary-checkout `.woostack/config.local.json`,
   validates the optional canonical `github` object, and preserves unrelated user-owned settings.
   The [artifact contract](references/artifact-backends.md#canonical-github-configuration) owns
   configuration fields, precedence, validation, and retained legacy-setting protections.
3. Create only missing support paths within the selected support scope:
   - `.woostack/config.json` from [`templates/config.json`](templates/config.json);
   - local diagnostic report roots for Doctor, audit, and QA; and
   - worktree/recovery support declared by the [worktree contract](references/worktrees.md).

   Propose repairs to existing support only within the authorized changeset; do not overwrite
   user-owned settings. Delegation uses agents the host exposes; Init never creates, validates, or
   repairs project agent definitions. The bundled [OMP host notes](references/hosts/omp.md)
   own optional cleanup guidance for unchanged definitions generated by older releases.
4. Run the bundled non-mutating [support checker](scripts/doctor.sh) with `--check <target>`
   after support creation or repair. This is a local procedure, not the Doctor workflow. Also
   validate permissions, report roots, and cross-links for paths this run created or repaired.
   Fail closed on unsafe paths, permissions, collisions, malformed canonical configuration,
   incomplete checks, or incomplete recovery evidence for the affected support operation, not
   unrelated document drafting.
5. Report created, repaired, preserved, skipped, and blocked support paths with exact validation
   results. Never infer a GitHub owner, Project, Status field, issue, or publication destination,
   contact a provider, or select remote persistence.

Existing `.woostack/tmp/runs/`, legacy drafts, manifests, locks, reports, and remote records are
historical user data. Do not import, rewrite, delete, or recreate wrappers from them. The
[artifact contract](references/artifact-backends.md#retained-data-and-retirement) owns these
protections and the optional read-only historical reader; unknown or partial outcomes stop at the
last independently read boundary.

## Boundaries

Init authors authorized project guidance and explicit local support, not application source or a
scaffold. Tooling recommendations are advisory: Init installs no packages, writes or updates no
package manifests, lockfiles, or CI workflows, and schedules no implementation handoff; implementing
them remains separately authorized. It creates no issue, Project, branch, commit, pull request, or
lifecycle state; it never pushes, merges, reads/writes credentials, migrates retained data, or performs
destructive cleanup. It never creates host extensions or `.omp/` for session naming. User-owned files,
legacy settings, retained records, dirty worktrees, and reports remain preserved.
