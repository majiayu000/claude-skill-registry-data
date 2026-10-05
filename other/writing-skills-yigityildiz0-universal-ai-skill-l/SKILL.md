---
name: writing-skills
description: Create, edit, split, merge, port, or validate agent skills and SKILL.md packages. Use for skill architecture, trigger descriptions, supporting references/scripts, host variants, regression checks, or Turkish intents such as “skill yaz/geliştir”, “becerileri birleştir/böl”, “tetikleyicileri düzelt”, “ChatGPT-Claude-OpenCode skill paketi”. Do not use for ordinary project documentation that is not an agent skill.
---

# Writing Skills

Build skills as small, testable behavior contracts. Optimize discovery separately from the full procedure: the description routes; the body instructs; references hold conditional detail; scripts make repeated deterministic work verifiable.

Read [anthropic-best-practices.md](anthropic-best-practices.md) only when Claude-specific behavior or a deep authoring review is needed. Read [testing-skills-with-subagents.md](testing-skills-with-subagents.md) only when the current host and instructions permit isolated agent evaluations. Never spawn agents solely because this reference mentions them.

## 1. Recover the contract

Before editing, record:

- Trigger intents and explicit non-triggers
- User outcome and output shape
- Required inputs, tools and supporting files
- Side effects, authorization and safety boundaries
- Verification and failure behavior
- Target hosts and discovery roots

Inspect every existing variant before deciding which is canonical. Preserve useful behavior unless evidence supports removal.

## 2. Decide add, modify, split, merge or remove

- **Add** only for a recurring need with no adequate owner.
- **Modify** when the owner is correct but routing, procedure, safety or verification is weak.
- **Split** when trigger domains, permissions, dependencies or outputs differ materially.
- **Merge** only when triggers, dependencies, safety and output contract substantially overlap.
- **Remove** only for exact duplicates, broken stubs, superseded copies or unsafe behavior after backup and evidence.

Do not merge by topic name alone. Do not keep duplicate IDs across discovery roots unless a host override is intentional and documented.

## 3. Write portable frontmatter

Use a lowercase kebab-case directory and matching `name`. Keep `description` within the target host's limit and front-load:

1. Exact capability/domain
2. Natural use cases and symptoms
3. High-value English and Turkish intents when the audience needs both
4. A concise false-positive boundary for overlapping skills

Descriptions should make selection discriminating, not reproduce the workflow. Provider-specific invocation controls belong only in host variants:

- OpenAI: `agents/openai.yaml`
- Claude Code manual-only: `disable-model-invocation: true`
- OpenCode V2 manual-only: `metadata.opencode/autoinvoke: false`

## 4. Structure the body

Keep the entrypoint focused and use progressive disclosure:

- Scope and owner boundary
- Inputs and routing
- Ordered workflow
- Hard rules and authorization limits
- Output contract
- Links to one-hop references/scripts/templates

Move long, conditional material to `references/`. Put repeatable deterministic calculations or validation in `scripts/`. Do not hide a critical safety or trigger rule only in a reference.

## 5. Build safe supporting files

- Prefer standard-library, read-only scripts when sufficient.
- Validate paths, encodings, schemas, units and invalid inputs.
- Never execute imported/community code during review merely to see what it does.
- Never bundle credentials, personal identifiers, machine-specific paths or undocumented network calls.
- State model limits; a script's precise output is not precise confidence.

## 6. Evaluate

Every changed skill needs, at minimum:

- Structural validation: frontmatter, name/folder, description length, encoding and links
- Positive trigger cases in natural English and Turkish when bilingual
- Negative cases for the nearest competing skill
- Boundary/failure cases for missing inputs, unsafe actions and stale evidence
- Deterministic script fixtures where scripts exist
- Host-specific invocation-policy checks
- Regression comparison against the previous accepted contract

For a new discipline-enforcing skill, use a no-skill baseline and skill-enabled test when an allowed fresh-context harness exists. If the host or current instructions forbid subagents, use static cases and deterministic checks; do not violate higher-level rules to satisfy a testing technique. For a batch corpus, every skill still receives structural and trigger checks, while full pressure tests focus on new or high-risk behavior owners.

## 7. Package and verify

1. Build all host variants from one validated common source.
2. Back up every destination before sync.
3. Generate manifests and SHA-256 hashes.
4. Re-enumerate each local/cloud/repository destination separately.
5. Never claim account/cloud installation, a push, or an upload without read-back evidence.

## Acceptance result

Return `PASS`, `CONDITIONAL`, or `FAIL` with changed skills, preserved behavior, trigger collisions, host differences, tests, unresolved limits and rollback location.
