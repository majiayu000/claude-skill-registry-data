---
name: agent-context-maintainer
description: "Maintain local agent context and package metadata. Use for AGENTS.md, skill UI metadata, manifests, marketplace entries, default prompts, or package sync; use skill-curator for external discovery."
---
# Agent Context Maintainer
Keep agent context small, durable, consistent, and easy to trust.
## Core Rules
1. Read the existing context files before editing. Preserve repo-specific rules that are still true.
2. Keep durable instructions; remove stale, temporary, obvious, or tool-noisy guidance.
3. Put rules in the canonical owner file. Do not duplicate skill content into packaged copies except through the repo's sync path.
4. Separate human project facts from agent behavior rules, skill instructions, and marketplace metadata.
5. Never add secrets, credentials, private tokens, or machine-specific absolute paths.
6. Resolve conflicts explicitly when different agent surfaces say different things.
7. Validate generated or packaged copies after changing canonical context.
## Workflow
1. Classify the request:
   - AGENTS.md, CLAUDE.md, company.md, Cursor, Copilot, or repo instruction cleanup
   - skill metadata, default prompts, or marketplace entry updates
   - plugin manifest review
   - stale context, duplicated rules, or conflicting guidance audit
   - packaged-copy sync and validation
2. Inventory relevant context files and their ownership:
   - root instructions for repo-wide behavior
   - skill `SKILL.md` and `agents/openai.yaml`
   - plugin manifests and marketplace metadata
   - generated distribution copies
   - local marketplace metadata, manifests, and default prompts; these belong here, not to `skill-curator`
3. Load the matching files from the Reference Map.
4. Edit the smallest canonical file set that fixes the problem.
5. Run the repo's sync and validation commands when packaged copies or skill metadata are affected.
6. Report changed rules, removed stale instructions, and validation gaps.
7. If validation fails, repair the canonical source, rerun validation and sync, then report only unresolved owner decisions.
## Company Context
When repo work touches durable context, user-facing agent behavior, plugin metadata, marketplace descriptions, or distribution packaging, read root `company.md` if present. Follow its terminology, product positioning, governance, privacy, and release guidance unless higher-priority instructions conflict.
## Reference Map
Load [references/context-file-audit.md](references/context-file-audit.md) for AGENTS.md, CLAUDE.md, company.md, Cursor/Copilot rules, context pruning, deduplication, and conflict resolution.

Load [references/plugin-metadata.md](references/plugin-metadata.md) for Codex or Claude plugin manifests, marketplace entries, display metadata, default prompts, packaged skill copies, and sync validation.
## Context Standards
- Root context should explain durable repo commands, canonical paths, release paths, and gotchas only.
- Skill files should explain role behavior, trigger boundaries, workflow, references, standards, and output shape.
- Metadata should describe discoverability and selection; it should not hide mandatory behavior.
- Default prompts should include the exact skill name when a client expects that trigger.
- Generated or packaged copies should be reproducible from canonical sources.
- Avoid vague global commands such as "always be excellent" or "use best practices." Replace them with specific behavior or delete them.
- Prefer fewer stronger rules over long instruction dumps.
## Tool Output
- Use RTK when available for noisy, non-destructive inventory, validation, sync, or test output. Treat it as triage and inspect raw output when an exact packaging or release claim depends on it.
## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.
## Output Shape
For a context audit:

1. verdict
2. conflicts or stale rules
3. canonical files to edit
4. exact rule changes
5. sync and validation commands
6. remaining owner decisions
