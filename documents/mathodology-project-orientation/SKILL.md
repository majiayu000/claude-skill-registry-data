---
name: mathodology-project-orientation
description: Use when maintaining the skills-only repository or checking whether a change belongs here.
---

# Mathodology Repository Orientation

The maintained source is `.claude/skills/`, with roles in `.claude/agents/`,
workflow prompts in `.claude/workflows/`, and user documentation in `docs/`.
The root retains AGENTS.md, the two READMEs, LICENSE, .gitignore and .mcp.json.

Skill directories may include reference Markdown, attributed source snapshots,
small licensed images, generated demonstration figures and optional scripts.
A reference figure is teaching material, not contest evidence. Keep synthetic
previews visibly labeled and reproducible. Do not add a dataset collection,
application runtime, CI, package manifest or deployment framework.

`.agents/skills/` is an ignored local mirror, never a second authoring source.
Before replacing this project's installed skills, back up its Mathodology
entries outside the checkout. Leave other skills and global directories alone.

`.mcp.json` is a client configuration for the keyless search MCP. It is retained;
custom user configurations and secrets do not belong in source control.
Contest output can live in ignored `work/` or another working directory.
Historical application implementation is available through Git history.

For maintenance, optionally run the repository checker described in
[maintenance](../mathodology-dev-test-release/SKILL.md). The checker verifies
metadata, references and boundaries; it does not assess mathematical quality.
