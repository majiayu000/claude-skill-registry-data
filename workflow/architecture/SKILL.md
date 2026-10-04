---
name: architecture
description: Turn an approved spec into an architecture document and workspace cards by running the level-aware architecture pipeline inside Codex. Use when the user wants boundaries, card slices, or board-ready implementation cards from a finished spec.
---

# Architecture

Use this skill after `foundation` and before `orchestrate`.

This is a Codex-native translation of the Claude plugin's architecture pipeline redesign:

1. Research measures eight fields and computes a level.
2. Audit independently re-measures and verifies the level.
3. Compose runs the L1, L2, or L3 architecture process.
4. Approved card slices become workspace cards.

Classification is deterministic. The user sees the bundle and verified level for transparency, but approves the architecture document, not the level.

Reference worker prompts live in:

- `references/research-worker.md`
- `references/classification-auditor-worker.md`
- `references/compose-l1-worker.md`
- `references/compose-l2-worker.md`
- `references/compose-l3-worker.md`

## Workflow

1. Load the `agentboard` skill first.
2. Apply the `expert-standard` frame for architecture judgment.
3. Locate the approved spec in `docs/specs/`.
4. Select or create the target app and board.
5. Create one scaffold workspace card to hold architecture artifacts.
6. Spawn a worker using `references/research-worker.md` with:
   - `spec_path`
   - `scaffold_card_id`
   - `agent_id`
7. Wait for the `ARCH_FACTS_BUNDLE_V1` artifact.
8. Spawn a worker using `references/classification-auditor-worker.md` with:
   - `spec_path`
   - `audited_bundle_artifact_id`
   - `scaffold_card_id`
   - `agent_id`
9. Wait for the `ARCH_BUNDLE_AUDIT_V1` artifact and read `verified_level`.
10. Show the bundle, audit verdicts, and verified level to the user as transparency only.
11. Spawn exactly one compose worker based on `verified_level`:
   - `references/compose-l1-worker.md`
   - `references/compose-l2-worker.md`
   - `references/compose-l3-worker.md`
12. Pass the compose worker:
   - `spec_path`
   - `verified_level`
   - `scaffold_card_id`
   - `agent_id`
   - the verified bundle inline as `arch_facts_bundle`
13. Wait for the `architecture_document` artifact and verify the written file in `docs/arch/`.
14. Show the architecture document to the user and iterate until explicitly approved.
15. Commit the approved architecture document.
16. Read the `Card Slices` section from the approved document.
17. Create one workspace card per slice, then resolve `Depends on` edges in a second pass.
18. Move the scaffold card to `finished`.
19. Summarize the architecture path, level, board, and created cards.

## Rules

- Do not let `foundation` create implementation cards. Cards come from approved architecture slices.
- Do not let the user override the computed level at runtime. If the classification looks wrong, fix the rules in a future version instead of bypassing them.
- Use `spawn_agent` for research, audit, and compose workers. Keep the scaffold card as the artifact trail.
- L1 and L2 do not require Context7. L3 does.
- Clear Thought is required only for L3.
- If a required tool surface is unavailable, stop and surface the blocker instead of improvising around it.
- The architecture document is the approval surface. The level is not.
