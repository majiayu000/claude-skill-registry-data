---
name: skill-catalog-curator
description: Audit installed and source-controlled Codex skill catalogs for duplicates, drift, stale metadata, placeholder text, risky overlap, frontmatter quality, routing triggers, no-op candidates, and local metadata leaks. Use when the user asks to clean up skills, compare local skills with TheAngrySkills remote, evaluate a skill like Sensei, find duplicates, or make skill updates safer before commit/update.
---

# Skill Catalog Curator

Use this skill for read-only skill catalog hygiene. It reports problems; it does not remove, rename, install, update, or overwrite skills.

## Default Workflow

1. Inspect the requested roots. If none are specified, include existing roots from:
   - `~/.agents/skills`
   - `~/.codex/skills`
   - `~/TheAngrySkills/skills`
2. Run the scanner:

```bash
python3 <this-skill>/scripts/scan_skill_catalog.py
```

3. For Sensei-style frontmatter/routing quality on one skill or a repo:

```bash
python3 <this-skill>/scripts/audit_skill_frontmatter.py <skill-or-root>
python3 <this-skill>/scripts/audit_skill_frontmatter.py <skill-or-root> --profile shared
python3 <this-skill>/scripts/audit_skill_frontmatter.py <skill-or-root> --profile codex
python3 <this-skill>/scripts/audit_skill_frontmatter.py <skill-or-root> --profile agentskills
python3 <this-skill>/scripts/audit_skill_frontmatter.py <skill-or-root> --json
```

4. For Waza-style trigger fixtures, generate prompts from explicit `WHEN:` or
   `USE FOR:` phrases:

```bash
python3 <this-skill>/scripts/generate_trigger_tests.py <skill-dir>
python3 <this-skill>/scripts/generate_trigger_tests.py <skill-dir> --write tests
```

These fixtures test expected trigger intent. They do not prove that Codex chose
the skill in a live session.

5. Review findings by severity:
   - `error`: likely broken skill discovery or real local-vs-remote drift.
   - `warning`: likely stale metadata, placeholder text, or duplicated catalog entry.
   - `info`: useful inventory or optional cleanup candidate.
6. Before destructive cleanup, ask the user to approve exact paths and actions.

## Scanner

Use `scripts/scan_skill_catalog.py` for deterministic checks.

Common commands:

```bash
python3 scripts/scan_skill_catalog.py
python3 scripts/scan_skill_catalog.py --root ~/.agents/skills --root ~/TheAngrySkills/skills
python3 scripts/scan_skill_catalog.py --json
```

The scanner checks:

- duplicate frontmatter `name` values across roots
- duplicate folder names across roots
- folder name versus frontmatter name mismatch
- installed/local copy drift for same folder names by directory hash
- missing `agents/openai.yaml`
- `agents/openai.yaml` default prompt that does not mention `$skill-name`
- placeholder/TODO template residue
- short or generic descriptions

## Frontmatter Auditor

Use `scripts/audit_skill_frontmatter.py` when the question is whether a skill
will route well, trigger clearly, stay compact, avoid publishing local machine
metadata, and avoid no-op instruction text. The default profile is `shared`,
for the mixed team/session environment rather than only Codex Desktop.

It checks:

- frontmatter parseability as real YAML, not loose key/value text
- `name` validity and folder-name match
- description length, word count, and trigger language
- extra frontmatter fields
- oversized `SKILL.md`
- missing `agents/openai.yaml`
- local filesystem paths in `SKILL.md` and references
- possible no-op instruction lines such as "be thorough", "make it easy to
  read", or "follow best practices" when they are not tied to an observable
  constraint

No-op findings are informational. They identify cleanup candidates, not proven
bugs. Keep a line if it changes behavior through a concrete constraint, exact
output requirement, path, command, threshold, or routing rule.

This is a Codex/TheAngryPit-specific audit. Do not automatically copy external
spec recommendations such as `license` or `metadata.version` into Codex skills
unless the repo intentionally adopts those fields.

Profiles:

- `shared`: default. Allows metadata used across team sessions while still
  warning on weak routing and local path leaks.
- `codex`: stricter Codex-style frontmatter posture.
- `agentskills`: adds Sensei/agentskills-style hints such as license/version
  recommendations and explicit `WHEN:`/`USE FOR:` trigger checks.

For the policy on what to adopt from Sensei and what to reject, read
`references/sensei-compatibility.md`.

## Trigger Test Fixtures

Use `scripts/generate_trigger_tests.py` to create Waza-compatible
`trigger_tests.yaml` fixtures from a skill's frontmatter. It prefers explicit
quoted phrases in `WHEN:` or `USE FOR:` and falls back to description clauses
when needed.

Common commands:

```bash
python3 scripts/generate_trigger_tests.py skills/core/skill-catalog-curator
python3 scripts/generate_trigger_tests.py skills/core/skill-catalog-curator --write tests
```

This is stronger than static score alone because it creates concrete
should-trigger and should-not-trigger prompts. It is still not live Codex
routing proof.

## Security Admission

Use `scripts/security_scan_skill.py` when the question is whether a skill is
safe enough to admit, install, or update. This is a security lane, not a quality
lane.

Common commands:

```bash
python3 scripts/security_scan_skill.py skills/example-skill
python3 scripts/security_scan_skill.py skills/example-skill --json
python3 scripts/security_scan_skill.py scan-root skills --json
python3 scripts/security_scan_skill.py diff /tmp/old-skill /tmp/new-skill --json
python3 scripts/security_admission_pipeline.py update-plan --candidate-root skills --installed-root ~/.agents/skills --json
python3 scripts/security_admission_pipeline.py update-apply --plan /tmp/skill-update-plan.json --only-safe --confirm
python3 scripts/security_admission_pipeline.py quarantine suspicious-skill --root ~/.agents/skills --quarantine-root ~/.agents/quarantine --reason "blocked scan" --confirm
python3 scripts/security_admission_pipeline.py skillspector skills/example-skill --report-dir /tmp/skillspector-report --json
```

The security scanner is deterministic, offline, and read-only. It does not
execute candidate skill code, install dependencies, mutate active roots, or
replace human approval.

Use `scan-root` to audit every immediate skill directory under a root before a
bulk update or release. Use `diff` to compare an old installed skill with a new
candidate before deciding whether an update is safe enough to apply.

Use `update-plan` before updating installed roots. It is read-only and compares
candidate skills against an installed root. Use `update-apply` only with an
accepted plan, `--only-safe`, and `--confirm`; it skips review and blocked
entries. Use `quarantine` only with `--confirm`; it moves a skill into an
explicit quarantine directory and writes metadata. Use `skillspector` only as an
external evidence adapter when the binary is already available or explicitly
provided; SkillSpector evidence does not override local hard-deny verdicts.

Generated documentation skills may include high-risk commands, credential paths,
privileged install snippets, or active agent instructions as upstream reference
text. Treat a blocking verdict on generated docs as a hard promotion gate, not
as automatic proof of malicious intent. Classify whether the finding is inert
reference material, active skill behavior, or real supply-chain risk before
installing, updating, or publishing the skill.

It checks for:

- remote download execution such as `curl | sh`
- inline shell/runtime execution
- credential-path reads
- persistence and global mutation surfaces
- privilege escalation instructions
- network exfiltration patterns
- policy-bypass or concealment instructions
- global package installs
- MCP, plugin, hook, and Codex config mutation surfaces
- broad filesystem scans
- bundled scripts, executable files, dependency manifests, workflows, Docker
  files, nested agent instruction files, symlinks, and path escapes

Security verdicts are separate from quality scores:

- `safe_to_install`
- `safe_docs_only`
- `needs_human_review`
- `quarantine`
- `blocked_malicious`
- `blocked_unscannable`

SkillSpector or other external scanners may be used later as evidence adapters,
but they do not replace local deterministic deny rules.

To manually check whether the external Sensei comparator changed:

```bash
python3 scripts/check_external_auditors.py
```

Run that monthly or before major skillset releases. It checks versions only; it
does not install Sensei or mutate skills.

## Repo CLI

When working inside the TheAngrySkills repo, prefer the repo CLI wrapper:

```bash
scripts/theangry-skills.mjs score skills/core/skill-catalog-curator
scripts/theangry-skills.mjs audit skills/core/skill-catalog-curator
scripts/theangry-skills.mjs check --root skills --profile shared
scripts/theangry-skills.mjs trigger-tests skills/core/skill-catalog-curator --write tests
scripts/theangry-skills.mjs security scan skills/core/skill-catalog-curator --json
scripts/theangry-skills.mjs security scan-root skills --json
scripts/theangry-skills.mjs security diff /tmp/old-skill /tmp/new-skill --json
scripts/theangry-skills.mjs security skillspector skills/core/skill-catalog-curator --report-dir /tmp/skillspector-report --json
scripts/theangry-skills.mjs update-plan --candidate-root skills --installed-root ~/.agents/skills --json
scripts/theangry-skills.mjs update-apply --plan /tmp/skill-update-plan.json --only-safe --confirm
scripts/theangry-skills.mjs quarantine suspicious-skill --root ~/.agents/skills --quarantine-root ~/.agents/quarantine --reason "blocked scan" --confirm
scripts/theangry-skills.mjs check --root skills --strict --emit-proof reports/skill-audit-shared.md
scripts/theangry-skills.mjs sensei-version
```

Install the wrapper into `~/.local/bin` only when the operator wants a PATH
command:

```bash
scripts/install-theangry-skills-cli.sh
```

## Reporting

Use this output shape:

```text
Scope: <roots scanned>
Summary: <skills count, issue count by severity>
Critical findings:
<error/warning bullets with exact paths>
Recommended actions:
<ordered, non-destructive next steps>
Not done:
<anything requiring user approval>
```

Do not treat duplicate names as automatically wrong. Some duplicates are expected during repo-versus-installed comparison; real risk is unexplained drift, stale metadata, or conflicting frontmatter.
