---
name: sem
description: Entity-aware code change analysis using the pi-sem tools. Use when the user asks what changed, wants blast radius or affected tests, needs focused context for a function/class, wants review help on a commit/branch/PR, or asks to compare semantic diff with raw git diff. Prefer sem_context and sem_impact; use sem_diff selectively for summaries and reviews.
---

# sem

Use the `pi-sem` tools as a **semantic lens**, not as a universal replacement for raw git diff.

## Default decision tree

Choose the smallest useful tool first:

1. **Focused understanding of one entity** → `sem_context`
   - Best for a single function, method, class, block, or config section
   - Prefer this before reading a whole large file

2. **Blast radius / affected tests / hidden dependents** → `sem_impact`
   - Use when reasoning about what could break
   - Prefer `scope=tests` for test selection
   - Prefer `scope=all` when validating broader impact

3. **Structural inventory of a file** → `sem_entities`
   - Use before drilling into a suspicious file
   - Good for large files and mixed code/config files

4. **What changed across a commit/range/working tree** → `sem_diff`
   - Use for semantic summaries, entity counts, and review overviews
   - Do **not** default to it when you only need exact patch details or a single entity

5. **History / ownership of an entity** → `sem_log`, `sem_blame`
   - Use for regressions, archaeology, and ownership questions

## Review workflow

For commit / branch / PR review:

1. Run `sem_diff` once for a semantic overview
2. Pick the riskiest changed entities
3. Run `sem_impact` on those entities
4. Run `sem_context` on the suspicious ones you need to understand deeply
5. Confirm final findings with raw `git diff`, `read`, or direct file inspection before citing line numbers

For snapshot / folder review:

1. Start with `sem_entities`
2. Use `sem_context` on the most relevant entities
3. Use `sem_impact` only after you identify something suspicious

## Important caveats

- `sem diff --format json` is **not always smaller** than raw `git diff`
- `sem` may under-cover tests, assets, generated files, or non-semantic glue code
- Do not cite `sem` output alone as final evidence for line-level review comments
- If semantic coverage looks incomplete, fall back to raw `git diff`, `read`, `grep`, and file inspection

## Good prompts / tool choices

- “What changed in this commit?” → `sem_diff`
- “What tests are affected by this function?” → `sem_impact` with `scope=tests`
- “Give me focused context for this class without reading the whole file.” → `sem_context`
- “What is in this Terraform file?” → `sem_entities`
- “How did this function evolve?” → `sem_log`

## Anti-patterns

Avoid these habits:

- Running `sem_diff` repeatedly when `sem_context` would answer the question faster
- Using only raw `git diff` for entity counts or blast radius questions
- Treating `sem_impact` as infallible; verify surprising results with file reads and grep
- Writing review findings from semantic summaries without checking the actual changed code
