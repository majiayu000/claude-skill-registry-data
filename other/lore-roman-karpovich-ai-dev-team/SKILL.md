---
name: lore
description: "Reframe a session, spec, investigation, or retrospective as a short Warhammer 40K vignette using the plugin's agent cast. Pure flavor, no side effects."
argument-hint: "[session|--spec <slug>|--investigation <path>|--retro] [--save]"
---

# /lore — WH40K vignettes from real sessions

Pure flavor skill. Turns a finished thread of work into a 200-400 word
imperial-grim-but-cheeky vignette using the cast defined in
`docs/wh40k-cast.md`. Never gates anything, never invokes other agents, never
modifies code. The single allowed write is the optional `--save` to KB.

## When to use

- After a finished spec, completed investigation, or hairy refactor — when the
  story is over and worth a one-paragraph retelling.
- As a session recap when wrapping up.
- For fun. This is the easter egg of the plugin; it earns its keep through tone,
  not utility.

Skip when:
- Mid-task, mid-step, or with an open spec checklist. Vignettes need a finished
  arc — narrate the dragon's death, not the third sword strike.
- The source material is empty or one message long.

## Argument parsing

`$ARGUMENTS` selects what to narrate. First positional argument:

- empty / `session` — the current conversation transcript.
- `--spec <slug>` — read the spec matching `<slug>` under
  `<kb>/repos/<project>/design/` (canonical `YYYY-MM-DD-<slug>.md`; glob by slug
  since the date prefix is unknown) and the matching execution workdoc at
  `<kb>/repos/<project>/design/workdocs/<slug>/exec.md`.
- `--investigation <path>` — read an investigation transcript file (typically
  `<kb>/repos/<project>/research/<slug>.md` or a paste).
- `--retro` — current session, framed as a retrospective scene rather than a
  realtime narrative.

Flags (any position):

- `--save` — additionally write the vignette to
  `<kb>/repos/<project>/lore/<YYYY-MM-DD>-<slug>.md`. Slug derived from the
  source material (spec slug, investigation slug, or `session-<topic>`).
  Print inline anyway.

If `$ARGUMENTS` is malformed or names a missing path, print one line of
guidance and stop. Do not invent source material.

## Workflow

1. **Load the cast.** Read `docs/wh40k-cast.md` in the plugin source. This is
   the single source of truth for cast definitions and voice/tone. If the file
   is missing, refuse with a one-line nudge to restore it.

2. **Read the source material.** Based on `$ARGUMENTS`:
   - For `session` / `--retro` / empty: use the current conversation as source.
   - For `--spec <slug>`: read the spec and workdoc(s); skim git log for matching
     commits if useful.
   - For `--investigation <path>`: read the file at the path.

3. **Identify featured agents.** Scan the source for which roles actually fired:
   - Did a developer step run? (Codex / Senior)
   - Did `cross-auditor` run? Probes E/F?
   - Did `spec-compliance-checker` block or pass?
   - Did `investigator` debate? `librarian` create a KB doc? `verifier` run tests?
   - Was this a pure orchestrator-only thread?

   **Be faithful.** Do not introduce a Комиссар scene if compliance never fired.
   Do not invent an Inquisitor tribunal for a one-step refactor. The cast list is
   a vocabulary, not a checklist.

4. **Write the vignette.** ~200-400 words. Present tense. English narration with
   Russian WH40K proper nouns (Капитан, Комиссар, Конклав, Техножрец, ауспекс,
   ересь, устав). Reference real events from the source — commit messages, file
   paths, spec slugs, actual finding names — recast as imperial drama. Print
   inline as the skill's response.

5. **(Optional) Save to KB.** If `--save` was passed:
   - Resolve the project KB root (typically `<kb>/repos/ai-dev-team/`; for other
     projects, follow `docs/kb-discovery.md`).
   - Ensure `<kb>/repos/<project>/lore/` exists; create if needed.
   - Write the vignette to `<kb>/repos/<project>/lore/<YYYY-MM-DD>-<slug>.md`
     with frontmatter:
     ```yaml
     ---
     date: YYYY-MM-DD
     source: session | spec:<slug> | investigation:<path>
     featured: [list of agent roles that featured]
     ---
     ```
   - Body is the vignette text.
   - Confirm the save in one line of output after the inline vignette.

## Constraints

- **Read-only on plugin source.** Never modify `agents/*.md`, `skills/`, `docs/`,
  or any plugin file as part of `/lore`.
- **Read-only on the project repo.** Don't touch source files, specs, or
  workdocs. The single allowed write is the `--save` target in the KB.
- **No subagent invocation.** Don't spawn cross-auditor, investigator, librarian,
  or any other agent. The whole skill runs in the orchestrator session.
- **No state changes.** Don't update spec checklists, MISSION.md, MOC indexes,
  memory, or anything else. Vignettes are flavor; they don't carry decisions.
- **Faithful to source.** No invented agents, no invented events, no invented
  commit hashes. If the source doesn't mention something, the vignette doesn't
  either.

## Examples

```
/lore                                   # current session, default voice
/lore session                           # same as above
/lore --retro                           # current session, retrospective frame
/lore --spec 2026-04-30-shared-absence-helper-extraction --save
/lore --investigation <kb>/repos/ai-dev-team/research/2026-04-26-cuts-investigation/round-3.md
```

The cast and tone live in `docs/wh40k-cast.md`. Read that first.
