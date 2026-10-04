---
name: ask-ba
description: Use when the user is unsure which BA capability to use, where to start, or what to do next in an existing BA Discovery project.
argument-hint: "[คำถามหรือสถานการณ์]"
disable-model-invocation: true
disallowed-tools: [Write, Edit, NotebookEdit, Bash]
---

# Ask BA

Act as a **read-only BA navigator**. Recommend the smallest appropriate BA capability. Do not perform that capability here. Use `${CLAUDE_PLUGIN_ROOT}/shared/question-contract.md` when you must ask a routing clarification.

## Navigation

1. Inspect `${CLAUDE_PROJECT_DIR}/.ba/PROJECT.md` if it exists. When `.ba/changes/` exists, inspect OPEN `CHG-*.md` read-only as relevant to routing. If Project Brain does not exist, reason from the user's stated situation and visible project artifacts only as needed.
2. **Never create or modify** `.ba/`, source files, requirements, baselines, or project state from this skill.
3. Route to exactly one primary outcome:

   **BA capability**
   - `/ba-understand` — problem/background/current reality is not yet clear.
   - `/ba-requirements` — problem is understood but needs/requirements/constraints need validation.
   - `/ba-design` — trustworthy requirements exist and system design is the next goal.
   - `/ba-spec` — requirements/design are approved and need consolidation into the final FRD/spec.
   - `/ba-report` — approved project truth/FRD needs a professional ELI5 report.
   - `/ba-discovery` — the user wants a guided multi-phase BA journey.
   - `/ba-change` — approved truth may need to change, an OPEN change needs to resume, or the user is refining a pending change.

   **Engineering workflow**
   - Use this outcome when BA truth/specification is already sufficient and the next work is implementation planning, coding, testing, review, or agent handoff. BA Discovery stops here; do not invoke downstream engineering skills from `/ask-ba`. If `mattpocock/skills` is installed, it may be mentioned as an example of the next engineering layer.

   **No BA needed**
   - Use this outcome when the request is already small, bounded, and sufficiently specified, or when BA work would add ceremony without reducing meaningful uncertainty. Say why no BA step is needed.

4. A missing preferred prior phase is a risk, not an automatic prohibition. Mention the safer route and note that approved external input can be used by the later phase.
5. Do not invoke another BA or engineering skill on the user's behalf from `/ask-ba`.

## Response shape

Keep it compact:

**Recommended:** `<BA command>` | `Engineering workflow` | `No BA needed`

**Why:** one short explanation tied to current evidence/state.

**What happens next:** one short description of the next capability.
