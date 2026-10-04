---
name: mode-classification
description: "Use before routing a /meta-agent request to choose single-agent-creator, team-builder, or agentlas-packager from the user's wording and available files."
---

# Mode Classification

Pick one Agentlas meta-agent mode before generating or repairing files.

## Procedure

1. Inspect the user request and any provided path, repo, ZIP, prompt, or agent
   files.
2. Step 0 - existing material wins: if existing material is being converted,
   repaired, cleaned, imported, or released, choose `agentlas-packager`.
3. Step 1 - count independent ownership boundaries. Ask how many roles must
   independently own all three of:
   - their own memory/context;
   - their own tools/permissions;
   - their own success criteria.
   One boundary means `single-agent-creator`. Two or more boundaries means a
   `team-builder` candidate. If the boundary count is unclear, run the clarify
   question loop before generating; do not infer from the word "team" alone.
4. Step 2 - check synthesis need for multi-boundary candidates. If those role
   outputs must be routed, reviewed, synthesized, or chained through
   produces/consumes dependencies, choose `team-builder` and require an
   orchestrator/HQ plus memory, policy, eval, and QA. If the roles are
   unrelated, create separate single-agent packages instead of one team.
5. Step 3 - shape guard. `single-agent-creator` may have many skills/tools but
   must not emit multiple loose worker `agent.md` files. `team-builder` may be
   small, but it must not omit the orchestrator/HQ.
6. Use keyword signals only as hints after the ownership-boundary check:
   - MULTI hints: separate memory partitions, tools or permissions that must
     not be merged, role-to-role review/policy separation, and
     produces/consumes pipelines.
   - SINGLE hints: one coherent job, many tools/skills owned by one worker, no
     routing or final synthesis requirement.
7. Overlay check: if the request depends on knowledge search over user
   documents, evidence-based or citation-attached generation, or a document
   corpus (HWPX/docx/pdf/제안서/계약서/견적서), additionally apply the
   `ontology-backed-agent` overlay (`modes/ontology-backed-agent.md`) with
   `ontology_backed: true` on the chosen base mode.
8. Loop policy: derive `loop_policy` from task purpose and risk using
   `.agentlas/contract-injection-map.json` risk tiers — `none` for simple
   one-shot tasks, `self-correct` for complex or long-running work, `verified`
   (separate-context verifier + side-effect gate) when the agent performs
   external writes or sends. Do not force loops onto simple tasks.
9. If the choice changes the output and the request is ambiguous, run the
   clarify question loop instead of guessing.

## Return

Return the selected mode, whether the `ontology-backed-agent` overlay applies,
the derived `loop_policy`, and one short reason. Then route to the matching
builder.

## Reference

See `docs/mode-classifier.md`.
