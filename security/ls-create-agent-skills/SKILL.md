---
name: ls-create-agent-skills
description: "Use when creating a new Agent Skills-compliant skill, adapting a document into a skill, importing an existing skill for LocalSetup, or exporting framework skills to other spec-compliant hosts."
metadata:
  version: "1.4"
---

# Skill creator (framework)

**Purpose:** Create Agent Skills format-compliant skills for this framework, adapt documents into skills, route external-skill imports through the framework's safety pipeline, and prepare skills for other hosts. Format compatibility does not guarantee behavioral portability: scripts, links, dependencies, tools, coordination references, and deployment assumptions may require host-specific adaptation.

## When to use this skill

- User wants to "create a new skill," "capture this as a skill," or "turn this into a skill."
- User wants to **import** an existing skill, such as one from Anthropic's repo, through LocalSetup's vetting, normalization, sandbox, and registration pipeline.
- User provides a skill or document from elsewhere and wants it adapted for this framework.
- User asks about preparing a framework skill for another host or auditing its behavioral portability.

## Interoperability (design for interchange)

- **Format compatibility:** Skills created or adapted here conform to the [Agent Skills](https://agentskills.io/specification) format (required `name`, `description`; optional `metadata.version`, `scripts/`, `references/`, `assets/`). No framework-only frontmatter is required.
- **Behavioral portability requires evidence:** A format-compliant skill may still depend on repository-relative links, sibling skills, platform tools, runtime dependencies, coordination protocols, or LocalSetup deployment semantics. Never promise unchanged operation in another host without the export audit below.
- **External-skill imports:** Do not copy an external candidate into `ls/skills/` from this skill. Hand the source to `ls-import-external-skills`, which owns discovery, duplicate handling, safety screening, and the gated path through `ls-skill-security-vetting`, `ls-normalize-skill-format`, and `ls-skill-sandbox-tester` before canonical copy, registration, or success confirmation.
- **Design guidance:** For structure and progressive disclosure, follow the [Agent Skills spec](https://agentskills.io/specification) and [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator). This skill adds LocalSetup authoring and export checks; it does not make framework behavior universally portable. See [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md).

## Rule ownership

This skill owns framework skill-authoring, import handoff, and export-audit behavior. Public docs such as `AGENT_SKILLS_COMPLIANCE.md`, `SKILL_INTEROPERABILITY.md`, and `SKILLS_AND_RULES.md` are reference surfaces; where their direct-copy or unchanged-operation guidance conflicts with this skill's safety pipeline or export audit, this skill is authoritative. Do not add new required `SKILL.md` fields in those docs without also updating this skill, validation tests, and generated catalogs.

- Keep Agent Skills portability: `name` and `description` remain the only required skill frontmatter fields.
- Keep LocalSetup-only classification in `ls/config/pack.yaml` under `extensions.skill_taxonomy`; do not require taxonomy fields in every `SKILL.md`.
- For imports, hand off to `ls-import-external-skills` as the sole operational import owner. It coordinates `ls-skill-security-vetting`, `ls-normalize-skill-format`, and `ls-skill-sandbox-tester`; do not embed or bypass those workflows here.

## Capturing completed work

When the user requests capture of a completed setup, configuration, repair, or
operational procedure, use `ls-skill-capture-handoff` for the completion offer,
standalone package, and optional full-source contribution handoff. This skill
continues to own authoring and export checks; the importer continues to own
incoming skills. Capturing or installing a skill does not authorize publication
or adoption of global completion policy. Reuse existing explicit authorization
for each requested stage instead of asking twice.

## Inputs you can accept

1. **Free-form description**  - User describes the workflow or behavior. Infer purpose, steps, and trigger scenarios; ask one or two clarifying questions if needed. Draft a spec-compliant skill using concise instructions, appropriate degrees of freedom, and progressive disclosure.
2. **Existing document**  - A local Markdown path or content to adapt into a newly authored skill. For pasted content or a remote single-document URL, follow [SKILL_IMPORTING.md](../../docs/SKILL_IMPORTING.md#adding-a-skill-from-paste-or-url): preserve the exact bytes in a temporary path and pass `skill_importer_scan` before adapting the screened path here. Content represented as an existing external skill instead belongs entirely to `ls-import-external-skills` through canonical copy and registration.
3. **Existing skill (import)**  - Directory or URL of a skill from any source. Load `ls-import-external-skills` and hand it the source and user intent. The importer must complete its collision decision and return passing vetting, normalization, and sandbox evidence before any canonical copy, registration, deployment, or success claim.

## Framework skill requirements (spec-compliant)

- **Spec:** Every skill must satisfy the [Agent Skills](https://agentskills.io/specification) format contract. Required: `name` (matches directory, 1-64 chars, lowercase, hyphens), `description` (1-1024 chars, what + when to use). Optional: `metadata.version`, `license`, `compatibility`; optional dirs: `scripts/`, `references/`, `assets/`. Behavioral support still depends on the target host.
- **Name (framework convention):** `ls-<trigger-keywords>` for a capability skill and `ls-wf-<trigger-keywords>` for a workflow. Choose the three to five most useful keywords from the circumstances or requests that should activate it, such as sudo, merge conflict, failing tests, or dependency advisory. Prefer concrete task language to abstract outcomes; omit redundant type words and filler. The directory name must equal `name` per spec.
- **Location (source):** `ls/skills/<name>/SKILL.md`. This is the canonical skill; deploy maps to each platform's configured adapter skills root per [ls/docs/PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md) and `ls/config/platforms.yaml`.
- **Frontmatter:** `name`, `description` (required). Include `metadata.version: "1.0"` so our hook can auto-bump. Lead the description with natural requests, symptoms, commands, file types, or error conditions that should activate the package, then state its behavior and scope limits. Put related phrases and exclusions in the description rather than stuffing the name. Use third person; keyword relevance is a LocalSetup discovery policy, not a guarantee that every host will select the package.
- **Body:** Start with a **Purpose** line; clear sections (##). Keep under ~500 lines; use progressive disclosure; link to `references/` or `ls/docs/` as needed. Follow [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) for structure and what to put in scripts/references/assets; keep host-specific dependencies explicit.

## Registration (required for discoverability)

After creating the skill, **register it** in its owning metadata and regenerate the shared catalogs so clients can discover it when the task matches.

**Canonical registration contract:** Read [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md), section **"Skill registration (new skills)"**, and complete its metadata, smoke-matrix, generation, and validation requirements. Do not maintain a separate registration list in this skill.

Keep the current task description in package frontmatter. Platform templates route to that metadata and the generated catalogs; do not add duplicate per-skill lists to each template.

## Workflow (agent steps)

**If importing an existing skill:**

1. **Hand off to the import owner**  - Load `ls-import-external-skills` and provide the candidate directory or URL plus the user's intended LocalSetup name and purpose. Do not duplicate its acquisition, collision, copy, or registration procedure here.
2. **Require the complete safety pipeline**  - Keep `ls-import-external-skills` as the active coordinator. Its completion result must include passing evidence from `ls-skill-security-vetting`, `ls-normalize-skill-format`, and `ls-skill-sandbox-tester`, in that order, under the repository's onboarding contract. If the importer cannot produce all three results, stop: no candidate may enter `ls/skills/`, registration, deployment, or a success claim.
3. **Accept only verified completion**  - Confirm import success only after the importer reports the canonical copy and registration plus passing vetting, normalization, and sandbox evidence. Deployment remains a separate action.

**If creating from scratch or from a doc:**

1. **Gather input**  - Use a user-authored description or a local document path. For pasted content or a remote single-document URL, first preserve its exact bytes in a temporary path and pass the path-based `skill_importer_scan` required by `SKILL_IMPORTING.md`; adapt only the screened path. Existing external skills remain entirely in the import workflow.
2. **Decide name and triggers**  - Derive `ls-<trigger-keywords>` from representative user requests and activation circumstances before drafting the procedure. Use `ls-wf-<trigger-keywords>` for a workflow under the workflow standard. Check that a matching request can recognize the name and description, and that nearby unrelated requests are excluded. Preserve published selectors through the owning alias mechanism when intentionally renaming a package; keep source, registration, callers and generated provenance aligned.
3. **Public skill discovery (recommended)**  - Load `ls-find-public-skills` with the proposed purpose and description. Consume its returned candidates and user choice without refreshing or re-ranking its index or reproducing its interaction procedure here. If the user chooses a public skill or adaptation, hand that candidate to `ls-import-external-skills`; otherwise continue authoring.
4. **Duplicate, overlap, and namespace check**  - For this newly authored skill only, list existing `ls/skills/` names and descriptions. If the proposed name already exists or its purpose and triggers strongly overlap, warn and offer **Keep existing**, **Replace existing**, **Merge**, or **Create as new**. Get explicit user choice. Imported candidates never use this step; their decision belongs exclusively to `ls-import-external-skills`.
5. **Draft SKILL.md**  - Use spec-compliant frontmatter and body. Follow the Agent Skills specification and Anthropic's skill-creator for structure; avoid unnecessary framework-only behavior and document every required host capability.
6. **Create file**  - Write `ls/skills/<name>/SKILL.md` or the user-approved alternative. Deploy maps it to each platform's configured adapter skills root; manual adapter copy is optional when needed.
7. **Register**  - Complete the registration and generated-catalog checks in [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md) under "Skill registration (new skills)."
8. **Confirm**  - Confirm the skill is created, spec-compliant, and registered. Before claiming it works in another Agent Skills host, complete the export audit below and adapt any host-specific behavior.

## Duplicate and overlap for new authoring

- The creation workflow owns collision and overlap choices only for newly authored skills. Every imported candidate's collision and overlap decision belongs exclusively to `ls-import-external-skills`; do not pre-check or repeat it here.

## Quality checks

- Skill is [Agent Skills](https://agentskills.io/specification)-compliant: `name` matches directory, `description` is present and under 1024 characters, and optional directories follow the specification.
- For framework use: name follows the `ls-*` convention, `metadata.version` is present, and registration is complete per `PLATFORM_REGISTRY.md`.
- Description includes what the skill does and when to apply it. Body has clear sections; committed content contains no personal data or machine-specific paths.
- Registration metadata and generated catalogs satisfy [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md). Imports additionally require passing vetting, normalization, and sandbox evidence before canonical copy or registration.

## Using our skills in another host (export)

Agent Skills format compliance permits another compliant host to parse the skill; it does not prove unchanged behavior. Before export:

1. Audit every `SKILL.md`, `references/`, `scripts/`, and asset reference for repository-local or absolute paths, sibling-skill handoffs, LocalSetup-specific commands, adapter paths, and deployment assumptions.
2. Inventory runtime and package dependencies, required executables, environment or secret providers, MCP/platform tools, network capabilities, and coordination protocols. Confirm the target host provides compatible equivalents.
3. Replace or document unsupported references and host-specific semantics, then validate links and execute the skill's real smoke scenario in the actual target host.
4. Copy the reviewed skill directory and rename its directory and `name` only when the target host requires it. Report any retained host assumptions; never describe format compatibility alone as behavioral portability.

See [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md) for the broader interchange contract.

## Reference

- [Agent Skills specification](https://agentskills.io/specification)  - Format and interchange.
- [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)  - Design, anatomy (scripts/references/assets), progressive disclosure.
- [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md)  - Import external skills; export our skills; full interchange steps.
- [SKILL_DISCOVERY.md](../../docs/SKILL_DISCOVERY.md)  - Public registries and discovery; use ls-find-public-skills when creating to recommend similar public skills.
- [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md)  - Registration file list.
- [SKILLS_AND_RULES.md](../../docs/SKILLS_AND_RULES.md)  - How skills are loaded and platform paths.
