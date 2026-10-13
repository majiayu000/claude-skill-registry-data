---
name: retro-notes-refactor
description: >-
  Refactor an accumulated `l-lessons-*` skill (created by /retro-notes) when later entries partially
  supersede or extend earlier ones, so future planning agents see the cross-cutting wisdom first
  instead of having to read every dated entry. Use when (1) the user says "lessons refactor", "retro
  refactor", "retro-notes refactor", "refactor lessons", or "synthesize lessons", (2) a
  `/retro-notes` session just added a new dated entry that broadens / narrows / contradicts a claim
  in an earlier entry on the same area, (3) an `l-lessons-*/SKILL.md` has 5+ dated entries on the
  same problem area OR exceeds ~500 lines, (4) the next `/big-plan` run in that area would have to
  scan many entries to find the relevant pattern. Produces a top-of-file "Recurring patterns
  (synthesized)" section in Trigger/Action/See format, adds Caveat notes to entries whose claims
  were later widened, updates the frontmatter description with pattern keywords, and formats with
  mdx-formatter. Does NOT delete historical entries — they remain as terse drill-down postmortems.
  Pair with /retro-notes (which writes new entries) and /big-plan (which reads the synthesized
  section first).
---

# Retro Notes Refactor

Synthesize cross-cutting wisdom across the dated entries in an `l-lessons-*` skill so future planning agents can read patterns first and drill into history second.

The retro-notes skill writes one dated entry per dev session. Over time multiple entries on the same problem area accumulate, and later entries often extend or partially supersede earlier ones (e.g. R6's "structural fix subsumes R3/R5" claim was itself widened by R7's "the bug class survives at a different layer"). Future readers — primarily future `/big-plan` runs and other LLM planning agents — should not have to read every dated entry to find the relevant pattern.

## When to refactor

Run this skill when ANY of these hold:

- The user explicitly asks ("lessons refactor", "retro refactor", "synthesize lessons").
- A `/retro-notes` session just landed and the new entry's claims widen, narrow, or contradict a claim in an earlier entry on the same area.
- The lessons file has 5+ dated entries on overlapping problem areas.
- The lessons file exceeds ~500 lines and the synthesis section hasn't been written yet.

Skip when:

- The file has fewer than 3 dated entries — too few patterns to extract; refactoring is premature.
- The dated entries are on unrelated areas (e.g. one zoom-tool entry and one auth entry, no overlap) — synthesis would be forced and shallow.
- A refactor was done within the last ~3 entries and no new contradictions surfaced.

## Output shape

A refactored lessons file has this structure (top to bottom):

```
---
name: l-lessons-{area}
description: {...includes pattern keywords AND a hint that file starts with a synthesized section...}
last-updated: YYYY-MM-DD
---

# {Area} Lessons

{1-2 sentence intro}

---

## Recurring patterns (synthesized YYYY-MM-DD, post-{latest entry tag})

{1-paragraph note: "Read this first. Dated entries below are the chronological record."}

### P1 — {short pattern name}

**Trigger.** {Observable conditions that mean this pattern applies.}
**Action.** {Remedial action with concrete tool calls / methodology refs.}
**See.** {Dated entries this derives from, with short descriptors.}

### P2 — ...
...

---

## Quick decision rules     ← include only when 5+ patterns

When in doubt, apply these in order:
1. **{condition}?** → P{n} ({short reminder}).
2. ...

---

## YYYY-MM-DD — {original first dated entry title}      ← unchanged

{...original entry body, possibly with a "Caveat (added YYYY-MM-DD by R{n} closeout)" section at end...}

## YYYY-MM-DD — {second dated entry title}             ← unchanged

...

## YYYY-MM-DD R{latest} — {latest entry title}        ← unchanged
```

Dated entries are NEVER deleted. They may receive a `### Caveat (added YYYY-MM-DD by R{n} closeout)` appendix when a later entry widened or narrowed their claim.

## Workflow

### Step 1: Locate and read the lessons file

Lessons files live at `<repo>/.claude/skills/l-lessons-{area}/SKILL.md` (project scope) or `$HOME/.claude/skills/l-lessons-{area}/SKILL.md` (personal scope).

Read the whole file. If it's >25 000 tokens, read in chunks via the Read tool's `offset` + `limit` — but read every byte. Pattern synthesis requires complete coverage.

While reading, capture three lists:

- **Entries list** — date, title, 1-line summary of the lesson's structural cause.
- **Cross-cutting threads** — bug-classes / methodologies / failure-modes that surfaced in 2+ entries.
- **Superseded claims** — places where an earlier entry's "Watch for next time" or "Would-skip-if-redoing" is later widened / narrowed / contradicted by a newer entry.

### Step 2: Pre-flight checks

Before writing, confirm:

1. **File has 3+ dated entries.** Fewer = refactoring is premature.
2. **At least 2 cross-cutting threads found.** A pattern needs 2+ supporting entries — one-off observations are not patterns.
3. **No active dev work on the same area.** Refactoring while a `/retro-notes` session is mid-write risks merge conflict. If a retro was just written, wait for that file change to settle (usually fine immediately after; just confirm `git status` shows the file's recent change is committed or that you'll write on top of it).
4. **User intent matches.** If invoked autonomously (e.g. after /retro-notes), confirm with one short message: "Refactor `{file}` now? It has {N} entries; I see {threads} as patterns." Don't ask permission for every detail — just the go/no-go.

### Step 3: Plan the synthesis

For each cross-cutting thread, draft a pattern with this template:

```
### P{n} — {short pattern name, ≤8 words}

**Trigger.** {1-3 sentences. Use concrete observable conditions: file paths, test outcomes, symptom phrases. Avoid hand-wave like "when something feels off".}

**Action.** {1-3 sentences. Include specific tool calls or methodology refs: "/headless-browser subagent", "ctx.getImageData pixel histogram", "dispatch a 1-hour Node prototype with inlined production math". Avoid vague "investigate carefully".}

**See.** {Comma-separated list of dated-entry refs with 3-6 word descriptors: "R3 (probe-feasibility spike); R4 (probe-surface vs paint-surface); R7 (resize-cycle pixel histogram)."}
```

Rules of thumb for the pattern list:

- **Promote only what recurs.** A pattern needs 2+ entries' worth of evidence. One-offs stay in their dated entry.
- **Name the structural cause, not the symptom.** "Storage-model divergence is a class of bug" beats "watch out for canvas resize blanking."
- **Cap at ~12 patterns.** More than that and the synthesis becomes its own scrolling problem. If you have 15 candidate patterns, group the most-overlapping ones.
- **Order by how often the trigger fires, not by file order.** Patterns the future reader will hit most often go first.

If you end up with 5+ patterns, also draft a "Quick decision rules" section: a numbered list of 5-8 triggers, each pointing at one pattern by number. The triggers are short — they're the index, not the explanation.

### Step 4: Plan the Caveat appendices

For each superseded claim identified in Step 1, draft a Caveat block to append at the END of the relevant dated entry (after its existing "Would-skip-if-redoing" or last sub-section):

```
### Caveat (added YYYY-MM-DD by R{n} closeout)

{1-3 sentences. State which claim of this entry was widened/narrowed, why, and point the reader at the pattern OR the dated entry that subsumes / extends it. Concrete language: "R6's claim '...' was correct for X but R7 surfaced Y at a different layer."}
```

Caveats are surgical. Don't rewrite the entry. Don't delete the original "Watch for next time" bullets. The Caveat is appended; the historical claim stays.

### Step 5: Update the frontmatter description

The frontmatter is what `/big-plan` and other planning agents see first. After refactoring, the description should:

- Include the file's H1 area name and a phrase like "starts with a 'Recurring patterns' synthesis section (P1–P{n}) — scan that first."
- List each pattern by number + name + the dated entries it derives from. Example: "storage-model divergence as a class (P1, R6, R7); probe-the-right-surface (P2, R3, R4); ..."
- Keep the prior keyword list but trim duplicates that the pattern names now cover. The description has a budget; ruthlessly cut keywords already implied by a pattern name.
- Update `last-updated: YYYY-MM-DD` if the field exists. If it doesn't exist, don't add it — that's the existing skill's convention to respect.

### Step 6: Write the changes

Order of edits:

1. **Insert** the "Recurring patterns (synthesized)" section after the H1 intro and before the first dated entry. Use the Edit tool with `old_string` = the H1 intro's last line + immediate `---` + first dated entry's `##` header; `new_string` = same + the new patterns section + `---` + first dated entry's `##` header.
2. **Insert** "Quick decision rules" right after the patterns section if 5+ patterns.
3. **Append** Caveat blocks to each superseded dated entry. Use Edit tool with `old_string` = the last line of the entry's "Would-skip-if-redoing" (or last sub-section).
4. **Replace** the frontmatter `description:` line with the updated version.

Verify after each edit that the file still parses (`head -5 SKILL.md` shows valid YAML).

### Step 7: Format with mdx-formatter

```bash
pnpm dlx @takazudo/mdx-formatter --write <path-to-SKILL.md>
```

This normalises bullet indentation, code-fence language tags, and trailing whitespace. Skips on network failure — proceed without if the formatter fails, the file is still valid markdown.

### Step 8: Verify

Spot-check:

- `wc -l SKILL.md` — note the new line count. Patterns section typically adds 100-200 lines; that's normal.
- `grep -E "^##|^### P" SKILL.md` — should show patterns first, then dated entries in chronological order.
- `head -1 SKILL.md` — should still be `---` (frontmatter intact).
- Pattern count matches the description's pattern-keyword list.

### Step 9: Tell the user

One short message:

- Lines added/removed (`git diff --stat`).
- Number of patterns extracted and their short names.
- Number of Caveat appendices added.
- Whether the file is committed (mention only if state changed).
- Suggest: "Future `/big-plan` runs touching {area} will now load the synthesized patterns first."

Do NOT commit automatically. Per project git policy, commits happen only when the user asks. The file change is left staged-but-uncommitted (or unstaged) so the user can run `/co` themselves.

## What NOT to do

- **Don't delete dated entries.** They're terse postmortems and remain valuable as drill-down. If an entry's claim is wrong, append a Caveat — don't rewrite the body.
- **Don't paraphrase entries into patterns.** Patterns are synthesized — they name the cross-cutting structural cause across 2+ entries. If a "pattern" is just one entry restated, it's not a pattern.
- **Don't change the skill name.** The frontmatter `name:` field is the skill's identity and is referenced by `/big-plan` and other readers.
- **Don't add or remove dated entries.** Adding entries is `/retro-notes`'s job. Removing them is never anyone's job.
- **Don't introduce a `references/` split unless the file exceeds ~800 lines after refactoring.** A split adds discovery overhead for future readers. If the file is 600-700 lines after refactoring, keep it as one file.
- **Don't promote a one-off observation to a pattern.** Patterns require 2+ supporting entries. An isolated lesson belongs in its dated entry's "Watch for next time" bullets, not in the synthesis section.

## Example: the post-R7 refactor of l-lessons-ui-verification

This skill was authored after refactoring `l-lessons-ui-verification` post-R7 (composerOutputSize ↔ fitDim storage-model divergence). The refactor added 12 patterns (P1-P12) and one Caveat (to R6, noting that R7 widened "asymmetric X is subsumed" to "asymmetric X moved up a layer"). File grew from 557 lines to 685 — within budget. Future `/big-plan` runs touching `packages/pattern-gen-viewer` now load the patterns first instead of scanning 10 dated entries.

That refactor is the canonical reference shape. If unsure how the output should look, read `.claude/skills/l-lessons-ui-verification/SKILL.md` in any pgen worktree.
