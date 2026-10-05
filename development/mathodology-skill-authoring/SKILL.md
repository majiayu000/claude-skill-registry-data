---
name: mathodology-skill-authoring
description: Use when adding, editing or reviewing skills, role prompts or skill metadata.
---

# Mathodology Skill Authoring

Write reusable guidance around decisions, evidence and useful outputs. Explain
when a method helps, how to recognize failure and when a simpler approach is
better. Avoid mandatory phases, handoff schemas, arbitrary scores and prose
that merely repeats another skill. Link the owning skill instead.

Every skill has SKILL.md frontmatter with a `name` equal to its directory and
a trigger-focused `description` starting with `Use when`. Its agents/openai.yaml
contains display_name, short_description and a default_prompt mentioning the
matching `$skill-name`. These metadata files are discovery interfaces, not a
workflow engine. Use concise role definitions; inherit the host's model choice.

Put detailed figure recipes, source provenance and examples in references or
examples directories within the owning skill. Keep the entry point short and
load only the references relevant to the task. Preserve third-party licensing;
never execute downloaded source snapshots as an installation step.

Small scripts are appropriate when they perform concrete work such as plotting,
backup or rendering. Keep them optional, declare dependencies, and verify the
behavior they actually promise. Do not create a framework to enforce prompts.

Update all affected entry points, role skill lists, metadata and English/Chinese
documentation. Keep each language natural; heading or code-block counts need
not match. Check that commands, capabilities and links agree. Use
[maintenance](../mathodology-dev-test-release/SKILL.md) for mechanical checks.
