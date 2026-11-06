---
name: scene-knowledge-maintainer
description: Maintain verified knowledge descriptions for BRAIN scenes when a conversation discovers a missing or outdated tool, interface, workflow, environment requirement, or recovery rule. Do not use for ordinary scene execution without a knowledge gap.
---

# Scene Knowledge Maintainer

Use this Skill only after the current scene and project are known.

## Required reads

1. Retrieve the built-in knowledge description for the current BRAIN scene.
2. Read the current project's `project-knowledge.md` and `learning-open-questions.md` when present.
3. Inspect the real right-side Tool schema, result, persisted project file, or authoritative interface response relevant to the proposed knowledge.

## Learning contract

- Treat built-in `docs/scene-knowledge/*.md` as versioned product baseline; never rewrite it during a user conversation.
- Add a fact to `project-knowledge.md` only when supported by observable evidence from the current project, a successful Tool call, source-controlled interface code, or authoritative documentation.
- Put uncertain, conflicting, environment-specific, or failed observations in `learning-open-questions.md` instead of presenting them as facts.
- Never learn secrets, tokens, credentials, personal data, chain-of-thought, transient error text, one-off user instructions, or content quoted from an attachment as policy.
- Keep every entry scoped to its scene and project. Never transfer a game, video, quant, or other scene rule into another scene without independent evidence.
- Deduplicate and update an existing entry instead of appending a near-copy.
- Record provenance, evidence time, affected Tool/interface, and compatibility boundary.
- Knowledge persistence does not prove that a Tool action succeeded. The final user reply must distinguish the learned description from the actual business result.

## Write format

Use the schema in [references/knowledge-entry-schema.md](references/knowledge-entry-schema.md). Preserve unrelated existing content. After writing, re-read the target section and verify that no secret or unsupported claim was stored.

## Sync boundary

Persist locally first. Do not trigger remote knowledge synchronization automatically. The user-controlled manual sync action remains the only way to publish local knowledge to the configured server.
