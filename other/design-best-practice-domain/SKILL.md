---
name: design-best-practice-domain
description: Use when adding a new domain or sub-domain to grimoire — whether starting a brand-new domain (health, finance, law), adding a new sub-domain to an existing domain, or deciding whether a new sub-domain is needed at all.
source: Apache Software Foundation project governance, npm package organization standards, Library of Congress classification system
tags: [domain-creation, knowledge-architecture, subdomain-design, contributor, maintainer, domain-release]
---

# Design Best Practice Domain

Architect a new grimoire domain or sub-domain: decide structure, create plugin files, write seed skills, and verify quality before release.

## Why This Is Best Practice

**Adopted by:** Explicit domain architecture standards are used across major knowledge systems — Apache Software Foundation requires new top-level projects to meet maturity criteria before graduation from incubation, npm's scoped package organization (`@scope/package`) provides consistent namespacing conventions for domain groupings, and the Library of Congress classification system defines explicit criteria for when a topic warrants its own subject heading vs. being nested under an existing one.
**Impact:** Domains without architecture standards become stubs — single files, no maintainer, no coverage plan — that are never completed and pollute discovery results. Apache's structured incubation model demonstrates that explicit domain criteria prevent project abandonment by establishing minimum viability before release. Consistent naming conventions (applied by npm and Wikipedia's category structure) reduce install and discovery errors by preventing naming collisions and ambiguous paths.
**Why best:** Ad-hoc domain creation — vs. following a defined architecture pattern — produces inconsistent plugin configurations, broken install paths, and stub domains that confuse contributors. A domain architecture checklist ensures every new domain is complete, discoverable, and maintainable before users encounter it.

Sources: Apache Software Foundation incubation policy, npm scoped packages documentation, Library of Congress Classification Outline

## Steps

### 1. Qualify the domain

A new top-level domain qualifies if ALL three are true:

- **Distinct**: not a sub-domain of an existing grimoire domain — run `suggest-best-practice` with your topic first; if it maps to an existing domain, add a sub-domain there instead
- **Broad enough**: covers at least 3 separable sub-domains (e.g., `health/` → `fitness/`, `nutrition/`, `medicine/`)
- **Has majority-adopted best practices**: credentialed professionals in this domain follow structured practices with demonstrated, measurable outcomes

If only 1–2 separable sub-domains exist, add a sub-domain under the closest existing domain instead of creating a new top-level domain.

### 2. Choose architecture: hierarchical vs. flat

| Pattern | When to use | Example |
|---|---|---|
| **Hierarchical** (recommended) | 3+ sub-domains, 10+ eventual skills | `engineering/` → `development/`, `testing/`, `architecture/` |
| **Flat** | Narrow scope, ≤2 sub-domains, <10 skills total | `meta/` with direct skill file references |

Hierarchical `plugin.json` `skills` field: array of `"./subdomain/skills"` paths.
Flat `plugin.json` `skills` field: array of `"./skills/skill-name/SKILL.md"` paths.

### 3. Create directory structure

**Hierarchical:**
```
skills/<domain>/
  .claude-plugin/plugin.json
  <subdomain-1>/
    .claude-plugin/plugin.json
    skills/
      <skill-name>/
        SKILL.md
  <subdomain-2>/
    .claude-plugin/plugin.json
    skills/
```

**Flat:**
```
skills/<domain>/
  .claude-plugin/plugin.json
  skills/
    <skill-name>/
      SKILL.md
```

### 4. Write domain-level plugin.json

```json
{
  "name": "grimoire-<domain>",
  "description": "<Domain> skills: <comma-list of sub-domain topics>.",
  "version": "0.1.0",
  "author": { "name": "Your Name", "email": "your@email.com" },
  "homepage": "https://github.com/jeffreytse/grimoire",
  "repository": "https://github.com/jeffreytse/grimoire",
  "license": "MIT",
  "skills": [
    "./<subdomain-1>/skills",
    "./<subdomain-2>/skills"
  ]
}
```

For flat pattern: `"skills"` is an array of `"./skills/<skill-name>/SKILL.md"` paths instead.

### 5. Write sub-domain plugin.json (hierarchical only)

One file per sub-domain at `<subdomain>/.claude-plugin/plugin.json`:

```json
{
  "name": "grimoire-<domain>-<subdomain>",
  "description": "<Subdomain> skills: <what this sub-domain covers>.",
  "version": "0.1.0",
  "author": { "name": "Your Name", "email": "your@email.com" },
  "homepage": "https://github.com/jeffreytse/grimoire",
  "repository": "https://github.com/jeffreytse/grimoire",
  "license": "MIT",
  "skills": "./skills"
}
```

`"skills"` is a string (directory path) — Claude Code auto-discovers all SKILL.md files under it.

### 6. Write seed skills

Use `write-best-practice-skill` for each seed skill.

One skill per sub-domain for hierarchical; seed skills distributed across sub-domains for flat.

**Minimum seed skills:** A domain must have at least 3 seed skills before being registered. A domain with fewer than 3 skills does not have enough definition to be useful — add more seeds or merge into an existing domain.

A single-skill domain is almost always a misclassified subdomain — verify the new domain genuinely needs its own top-level namespace before proceeding.

### 7. Add marketplace.json entries

For each new installable unit (domain + each sub-domain), add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "grimoire-<domain>",
  "source": { "source": "github", "repo": "jeffreytse/grimoire", "path": "skills/<domain>" },
  "description": "<one-sentence description>"
},
{
  "name": "grimoire-<domain>-<subdomain>",
  "source": { "source": "github", "repo": "jeffreytse/grimoire", "path": "skills/<domain>/<subdomain>" },
  "description": "<one-sentence description>"
}
```

### 8. Update README domains table

Add a row to the domains table in `README.md`:

```markdown
| [Domain](./skills/<domain>/) | Subdomain 1, Subdomain 2, ... | `/plugin install grimoire-<domain>@grimoire` |
```

### 9. Audit the domain design

Invoke `audit-best-practice-domain` on the new domain path. All seed skills must PASS before proceeding to registration or opening a PR. A NEEDS-REVISION or REJECT on any seed skill blocks the domain PR.

**Audit before registration:** Run the quality audit (check against STANDARD.md criteria) before registering the domain in SKILLS.md. Registration is the commitment — audit first to avoid registering a domain that immediately needs correction.

### 10. Open a PR

PR title: `feat(<domain>): add <domain> domain with <N> seed skills`

PR description must include:
- Sub-domains created
- Seed skills written (names + one-line purpose each)
- audit-best-practice-domain output (all PASS)
- Install command for users: `/plugin install grimoire-<domain>@grimoire`

## Rules

- Never release with 0 seed skills — stub domains block contributors who try to install
- Always run audit-best-practice-domain before opening a PR — seed skills must pass review-best-practice-skill
- Sub-domain names: lowercase, hyphen-separated, 1–2 words (`nutrition`, `contract-law`, not `about-nutrition`)
- Domain names: single noun, lowercase (`health`, `finance`, `law`)
- If the topic fits under an existing domain, create a sub-domain — don't create a parallel top-level domain

## Common Mistakes

**Domain for a single skill**: if it's one skill, it belongs in a sub-domain of an existing domain.

**Flat structure for a large domain**: `health/` with 30+ skills needs sub-domains — a flat plugin with dozens of skill paths slows discovery and maintenance.

**Missing marketplace.json entries**: users cannot install sub-domains individually without them.

**Skipping audit-best-practice-domain**: seed skills that don't pass review-best-practice-skill undermine the domain's quality signal from day one.

**Subdomain too granular**: `fitness/running/skills/` is too deep — keep it `fitness/skills/` and scope skills within it.