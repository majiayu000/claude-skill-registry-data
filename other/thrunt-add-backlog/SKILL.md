---
name: thrunt-add-backlog
description: Add an idea to the backlog parking lot (999.x numbering)
argument-hint: "<description>"
allowed-tools: Read, Write, Bash
---


<objective>
Add a backlog item to the huntmap using 999.x numbering. Backlog items are
unsequenced ideas that aren't ready for active planning — they live outside
the normal phase sequence and accumulate context over time.
</objective>

<process>

1. **Read HUNTMAP.md** to find existing backlog entries:
   ```bash
   cat .planning/HUNTMAP.md
   ```

2. **Find next backlog number:**
   ```bash
   NEXT=$(node ".github/thrunt-god/bin/thrunt-tools.cjs" phase next-decimal 999 --raw)
   ```
   If no 999.x phases exist, start at 999.1.

3. **Create the phase directory:**
   ```bash
   SLUG=$(node ".github/thrunt-god/bin/thrunt-tools.cjs" generate-slug "$ARGUMENTS")
   mkdir -p ".planning/phases/${NEXT}-${SLUG}"
   touch ".planning/phases/${NEXT}-${SLUG}/.gitkeep"
   ```

4. **Add to HUNTMAP.md** under a `## Backlog` section. If the section doesn't exist, create it at the end:

   ```markdown
   ## Backlog

   ### Phase {NEXT}: {description} (BACKLOG)

   **Goal:** [Captured for future planning]
   **Hypotheses:** TBD
   **Plans:** 0 plans

   Plans:
   - [ ] TBD (promote with /thrunt-review-backlog when ready)
   ```

5. **Commit:**
   ```bash
   node ".github/thrunt-god/bin/thrunt-tools.cjs" commit "docs: add backlog item ${NEXT} — ${ARGUMENTS}" --files .planning/HUNTMAP.md ".planning/phases/${NEXT}-${SLUG}/.gitkeep"
   ```

6. **Report:**
   ```
   ## 📋 Backlog Item Added

   Phase {NEXT}: {description}
   Directory: .planning/phases/{NEXT}-{slug}/

   This item lives in the backlog parking lot.
   Use /hunt-shape-hypothesis {NEXT} to explore it further.
   Use /thrunt-review-backlog to promote items to active milestone.
   ```

</process>

<notes>
- 999.x numbering keeps backlog items out of the active phase sequence
- Phase directories are created immediately, so /hunt-shape-hypothesis and /hunt-plan work on them
- No `Depends on:` field — backlog items are unsequenced by definition
- Sparse numbering is fine (999.1, 999.3) — always uses next-decimal
</notes>
