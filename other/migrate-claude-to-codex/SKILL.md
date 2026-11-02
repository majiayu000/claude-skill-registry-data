---
name: migrate-claude-to-codex
description: Adapt Claude harness assets for Codex while preserving shared AGENTS.md policy and canonical skills.
disable-model-invocation: true
---

# Migrate Claude to Codex

Adapt runtime integration while preserving shared policy and skill ownership.
Inspect target AGENTS.md, canonical skills and existing integration first. The
bundled helper is a scaffold; structural success does not prove semantic parity.

1. Run the dry-run inventory:
   `python3 <skill-dir>/scripts/migrate_claude_to_codex.py migrate --repo <target>`.
2. Review planned links, command conversions, agent scaffolds and hook mappings.
   Shared project/docs paths stay canonical. Claude Markdown rules need a manual
   decision: always-on policy in AGENTS.md or conditional shared references.
3. Apply when migration is authorized and the plan fits that authority, adding
   `--apply`. Existing skill destinations are preserved even with `--force`;
   reconcile them separately. Force applies to generated scaffolds and needs
   explicit overwrite authority for any existing work it would replace.
4. Review runtime model/tool assumptions, invocation metadata and hook payloads.
   Validate hooks with fixtures before treating them as enforcement. The script
   does not edit AGENTS.md, consolidate rule content, or generate execution policy.
5. Run `verify --repo <target> --skip-codex` for structure, then use permitted
   current Codex discovery tooling if runtime verification is in scope. Inspect
   the expected skill names and invocation modes; a catalog path alone proves
   neither correct routing nor actual execution. Report missing runtime checks.

Read `references/mapping.md` for exact mappings and caveats. Run
`python3 <skill-dir>/scripts/test_migration.py` after changing helper behavior.
The helper does not delete Claude sources, stage or commit. Preserve unrelated
changes and test in a disposable target before applying a changed migrator.
