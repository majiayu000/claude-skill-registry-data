---
name: agent-skill-authoring
description: >
  Author, structure, document, and validate compliant, high-quality Agent Skills
  for OWL, Claude Code, and other Agent Skills-compatible systems. Use when creating
  new skills, authoring SKILL.md frontmatter, writing activation-focused trigger
  descriptions, designing progressive disclosure structures with references/ and
  assets/, or preparing skills for inclusion in the OWL registry.
compatibility: >
  Agent Skills-compatible coding agents authoring or evaluating agent skill packages.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "agent-skills, owl, skill-authoring, meta-skill, ai-agents, specifications"
  topics: "ai-agents, devtools, software-development"
---

# Agent Skill Authoring & Quality Engineering

An Agent Skill is a structured, modular package that equips an AI coding agent with domain-specific engineering workflows, non-negotiable conventions, actionable best practices, and executable validation techniques. High-quality skills steer agent behavior reliably, prevent improvisation, and adhere strictly to the [Agent Skills Specification](https://agentskills.io/specification).

Detailed reference guides and starter templates:
- [Agent Skills Specification & Metadata Rules](references/specification.md)
- [Canonical Skill Starter Template](assets/skill-template.md)

---

## Core Rules

1. **Directory name must match skill name exactly**: The folder `skills/<skill-name>/` must match the frontmatter `name:` identifier (lowercase letters, digits, and single hyphens, <= 64 chars).
2. **Descriptions must define WHAT and WHEN**: The `description` field in frontmatter is the primary trigger mechanism. It must describe both what capability the skill provides and the specific user requests or file contexts that activate it.
3. **No author directories in the repository**: Keep the registry layout flat (`skills/<name>/SKILL.md`). Author identity is stored in metadata (`author: michaelweissdev`).
4. **Practice Progressive Disclosure**: Keep `SKILL.md` focused and concise (< 500 lines). Offload in-depth references into `references/` and templates into `assets/`.
5. **Skills are passive data**: Never include executable scripts that run automatically during installation or discovery. Scripts in `scripts/` must be explicit, documented, and run only on demand.
6. **Skills must control agent behavior**: Avoid vague motivational guidance ("Write clean code"). Give unambiguous technical rules ("Validate bounds before write", "Use try-with-resources", "Run mypy --strict").

---

## 1. Canonical Skill Package Structure

```text
skills/my-new-skill/
├── SKILL.md                    # Required: frontmatter + core workflow (< 500 lines)
├── skill.json                  # Optional: metadata overlay
├── references/                 # In-depth technical guides and deep dives
│   ├── specification.md
│   └── common-pitfalls.md
└── assets/                     # Reusable templates, skeletons, or boilerplate
    └── template.py
```

---

## 2. Frontmatter Specification (Agent Skills & OWL Compatible)

```yaml
---
name: my-new-skill
description: >
  Perform actionable task X, apply standard Y, and resolve issue Z.
  Use when the user requests feature A, encounters error B, reviews
  file type C, or needs guidance on domain D.
compatibility: >
  Agent Skills-compatible coding agents operating on Linux, macOS, or Windows
  environments with appropriate language toolchains.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "tag1, tag2, tag3"
  topics: "devtools, software-development"
---
```

Constraints:
- `name`: Lowercase, numbers, single hyphens (`[a-z0-9]+(-[a-z0-9]+)*`), max 64 characters.
- `description`: Plain text or YAML folded string, max 1024 characters.
- `compatibility`: Tooling requirements and agent prerequisites, max 500 characters.
- `metadata.author`: Alphanumeric author handle (e.g. `michaelweissdev`).
- `metadata.version`: SemVer string (`"1.0.0"`).
- `metadata.tags`: Comma-separated search keywords.
- `metadata.topics`: High-level taxonomy topics.

---

## 3. Mandatory SKILL.md Document Sections

Every skill should implement this 11-step structural anatomy:

1. **Title & Mission Statement**: Clear definition of the skill's engineering domain.
2. **Core / Non-Negotiable Rules**: 4-6 strict operational guardrails.
3. **When to Use**: Concrete triggers and user request scenarios.
4. **When NOT to Use**: Clear boundaries and handoffs to other specialized skills.
5. **Prerequisites & Tooling**: Required binaries, compilers, or permissions.
6. **Step-by-Step Workflow**: The sequential mental and operational model for the agent.
7. **Standards & Conventions**: Official style guides, RFCs, and API patterns.
8. **Common Mistakes & Anti-Patterns**: Tabular list of typical mistakes, risks, and fixes.
9. **Real-World Examples**: At least two realistic scenarios with code or command snippets.
10. **Verification Checklist**: Concrete checklist verifying that the task is finished correctly.
11. **References**: Authoritative documentation links and local relative references.

---

## 4. Verification and Registry Compliance

Before committing a newly authored skill to the OWL registry:

```bash
# 1. Validate skill against Agent Skills specification
owl validate ./skills/my-new-skill

# 2. Check complete registry integrity, directory naming, and collisions
owl registry check .

# 3. Test functional searchability in OWL
owl search my-new-skill
```

---

## 5. Verification Checklist

- [ ] Directory name exactly equals frontmatter `name`.
- [ ] Description specifies both functionality and activation conditions (<= 1024 chars).
- [ ] Compatibility field documents environment constraints (<= 500 chars).
- [ ] `author: michaelweissdev` and `version: "1.0.0"` set in `metadata`.
- [ ] All relative file links to `references/` and `assets/` resolve to existing files.
- [ ] `owl validate` and `owl registry check .` pass with 0 errors and 0 warnings.
