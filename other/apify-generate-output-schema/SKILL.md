---
name: apify-generate-output-schema
description: Deprecated. Output schema generation moved to the apify-actor-development skill; prefer that skill whenever it is available.
metadata:
  deprecated: "true"
---

# Deprecated: use apify-actor-development

This skill is deprecated and will be removed in a future release. Generating and updating Actor output schemas (`dataset_schema.json`, `output_schema.json`, `key_value_store_schema.json`) is now part of the `apify-actor-development` skill.

- If the `apify-actor-development` skill is available, load it and follow its `references/output-schemas.md`.
- If it is not available, tell the user this skill is deprecated and help them install `apify-actor-development` from `https://github.com/apify/agent-skills`, then stop. Do not write the schemas from memory. Use the install method that fits their agent, preferably the same one this skill was installed with:
  - Claude Code plugin: `/plugin install apify-actor-development@apify-agent-skills`
  - Skills CLI, which works with most agents: `npx skills add https://github.com/apify/agent-skills --skill apify-actor-development`
  - Cloned repo: pull the latest changes; the skill is at `skills/apify-actor-development/SKILL.md`
