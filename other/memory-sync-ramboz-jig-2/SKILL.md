---
name: memory-sync
description: >
  Persist new context, terms, learnings, and settled lightweight decisions. Use when
  the user says remember this, save this for later, add to glossary, note this down,
  or at session end to consolidate what was learned — that goes to the memory layer
  (AGENTS.md hot cache, docs/memory/, docs/inbox.md). Also use to record a decision
  or remember this decision when the call is a lightweight one shipped outside a
  spec slice: UI strings, visual and CSS choices, copy, or translation fixes. Those
  go to docs/decisions/lightweight-decisions.md via decisions.py. Also use when
  revising, updating, or re-pricing an already-recorded decision: judge whether it
  now warrants an ADR and promote it if so, rather than editing it in place. Also
  auto-fires at session end. Do not use for updating specs or code comments. For a
  NEW load-bearing decision, one with rejected alternatives, or any the user wants
  written up as an ADR, use `/jig:adr-workflow`; an already-recorded entry that
  outgrew this home is promoted from here.
user-invocable: true
---

> Spec 002 (memory layer) is fully closed — all four slices DONE: 002-01
> (explicit-sync), 002-02 (lookup-pattern), 002-03 (auto-detect-hooks),
> 002-04 (reconciliation-integration). 002-04's reconciliation integration
> is now the Memory-sync gate in the spec-workflow reconciliation checklist.

## What this skill does

Persists session-derived context to the memory layer via a deterministic helper.
Codex makes the *what / where* decisions; `memory.py` does the file I/O,
idempotency, and self-healing of missing memory structure.

## When to invoke

- User says "remember this", "save this for later", "add this to the glossary",
  "note this down", or similar (→ persist flow below).
- User explicitly invokes `/jig:memory-sync`.
- An unknown capitalized reference appears in the conversation (→ lookup-pattern flow below).
- Session-end consolidation (after slice 002-03 auto-trigger ships).
- **The session settled a non-spec shipped decision** — a UI string, visual/CSS
  choice, translation correction, or scoped brand/icon call made *outside* a spec
  slice (→ lightweight-decision flow below). This is the forcing function for
  out-of-spec work, which has no reconciliation phase to catch it.

## Lookup-pattern flow

When you see a capitalized reference, acronym, or project-specific term you
don't recognize, follow this flow **before asking the user**:

```
seen unknown reference X
  ↓
python3 memory.py lookup "X" .
  ↓ exit 0 → use the printed definition; do not ask
  ↓ exit 2 → ask the user once: "I don't recognize X — what is it?"
  ↓ user answers
  ↓
python3 memory.py add-term "X" "<definition>" .   (or promote if high-frequency)
  ↓ next time X appears, lookup hits
```

Concretely, the commands are:

```bash
python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" lookup "<term>" "<target>"
# exit 0 = hit (definition + source on stdout)
# exit 2 = miss (proceed to ask the user)
```

The lookup is case-insensitive and checks hot cache first, then glossary. Hot
cache hits win when a term exists in both (the user has explicitly elevated it).

**Do not ask twice.** Once a term is persisted (via `add-term` or `promote`),
future lookups in the same or later sessions resolve without re-asking. If the
user says "I told you this already," check whether you forgot to persist last
time, then persist now.

## How to use

1. **Identify candidate items** from the recent session:
   - **New domain terms** — anything the user defined or that needed explaining.
   - **Learnings** — failed approaches, dead ends, "we tried X" gotchas.
   - **Parked ideas** — things mentioned but not yet decided on.
   - **Frequently-referenced terms** — anything used ≥3 times this session.
   - **Non-spec shipped decisions** (spec 083) — UI strings, visual/CSS choices,
     translation corrections, scoped brand/icon calls settled *outside* a spec
     slice. **Conditional, to avoid noise:** only surface this when the session
     actually touched such product/UI/out-of-spec work — skip it entirely for
     pure backend/refactor/spec sessions.
   - **Load-bearing decision escape hatch** (spec 083-06 / ADR-0031) — the
     enumerated surface list above is **not** a closed gate. This session-end
     prompt is the **only** judgment owner for *out-of-spec* load-bearing
     decisions (which have no reconciliation phase), so also surface — regardless
     of which surface was touched — any decision the canonical ADR trigger
     covers. Canonical wording — single-sourced from ADR-0031, drift-tested
     verbatim across all four surfaces:
     A load-bearing design choice with rejected alternatives — one a future agent would need to know about to avoid undoing it — warrants an ADR even when it changes no module boundary or public contract.
2. **Decide per item** which file it belongs in:
   - Niche/domain term → glossary
   - Failed approach / gotcha → learnings
   - Unresolved/unfinished thought → inbox
   - High-frequency term → hot cache (in AGENTS.md)
   - Non-spec shipped decision → `docs/decisions/lightweight-decisions.md`
3. **Invoke `memory.py` once per item** with the right command. **Always quote
   the term/definition/body arguments** — terms may contain spaces, definitions
   often contain punctuation:
   ```bash
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" add-term "<name>" "<definition>" "<target>"
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" add-learning "<title>" --body "<text>" "<target>"
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" add-inbox "<text>" "<target>"
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" add-refinement-todo "<raw-markdown-chunk>" "<target>"
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" promote "<term>" "<definition>" "<target>"
   ```
   `add-refinement-todo` appends raw text (caller composes the markdown chunk —
   H2 category, deferred-/resolution-trigger structure, etc.) to
   `docs/refinement-todo.md` under the parallel-session file lock (slice 028-02).
   Where `<target>` is the project root (usually `.`).

   **Non-spec shipped decisions use `decisions.py`, not `memory.py`** (spec
   083-05): the file lives in `docs/decisions/`, not `docs/memory/`. Record one
   with the idempotent helper (it appends in the file's `### [Date] — [Title]` /
   Decision / Context / Scope / Commit template; re-running with the same title
   is a no-op):
   ```bash
   python3 "${PLUGIN_ROOT}/skills/memory-sync/decisions.py" add-lightweight \
     --title "<short title>" --decision "<what>" --context "<why>" \
     --scope "<which screen / component / string / asset>" [--commit "<SHA/PR>"]
   ```
   The helper seeds `lightweight-decisions.md` from jig's template when the
   project has none (bug 012) and says so — a project that adopted jig before
   the feature landed never received the file. **Never hand-write the file
   yourself:** if the helper refuses because an existing file is not in jig's
   format, it names both remedies — follow one, don't invent a third.

   Confirm with the user before writing — it's their decision to record, not
   yours to infer. If the decision clears the ADR trigger above, route it to an
   ADR (`adr.py new`) instead of here.

   **Revising an already-recorded entry — re-ask the routing question first**
   (spec 100-01 / [ADR-0042](../../docs/decisions/adr-0042-decision-routing-gate.md)).
   A decision's weight can change *after* it was filed: [#121](https://github.com/ramboz/jig/issues/121)
   reports one recorded as bounded, later re-priced by review into a
   module-boundary change with rejected alternatives, edited in place, and never
   re-routed. Routing is asked once at first write and never again — so **you**
   ask it again here. Before revising, judge the entry **as it will read after
   the change** against the canonical ADR trigger quoted above:

   - **Clears the trigger** → promote it; do not revise it in place:
     ```bash
     python3 "${PLUGIN_ROOT}/skills/memory-sync/decisions.py" promote \
       --title "<existing title>" --no-push [--slug "<adr-slug>"]
     ```
     This creates the ADR via `adr.py new`, seeds it from the entry's own
     fields, and leaves a forward-linking stub so old references still land on
     a record.

     **`--no-push` is shown because you are almost always on a feature
     branch.** Push mode reserves the ADR number on `origin/main` from an
     ephemeral worktree, so the file never lands in your working copy and
     there is nothing to seed — `promote` refuses up-front rather than
     stranding a reserved ADR on the trunk. Drop `--no-push` (or use `--pr`)
     only when promoting from `main` itself; the local ADR lands with the rest
     of your branch's work.
   - **Still settled, local, and bounded** (one screen / component / string /
     asset, no *real* rejected alternatives) → revise it in place. Omitted
     fields keep their recorded values:
     ```bash
     python3 "${PLUGIN_ROOT}/skills/memory-sync/decisions.py" update \
       --title "<existing title>" [--decision "<what>"] [--context "<why>"] \
       [--scope "<where>"] [--commit "<SHA/PR>"]
     ```

   Judge meaning, not vocabulary. A UI-copy or translation decision saying "X
   instead of Y" is naming a *wording* preference, not a rejected architectural
   alternative — it belongs here. The trigger is about a **load-bearing** choice
   a future agent could undo by accident. As with recording, confirm a promotion
   with the user before running it.

   To sweep records written before this guidance existed, `decisions.py lint`
   reports entries whose text reads as ADR-worthy. It is **advisory** — it
   matches wording, not meaning, so treat a finding as a prompt to judge, never
   as a verdict.
4. **Report a summary** at the end:
   ```bash
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" summary <target>
   ```
5. **Re-check the team signal** as the final step (spec 050-01). This
   re-runs scaffold-init's exact team detection (≥2 distinct mailmap git
   authors, monorepo-guarded). When the project has grown past solo and
   `docs/memory/people.md` is absent (and no `.jig/no-people-md` opt-out
   marker is present), the helper surfaces a structured nudge:
   ```bash
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" team-check <target>
   ```
   The advisory offers three options — `[y]` bootstrap people.md now,
   `[n]` skip this run, `[never]` suppress future nudges. In an
   **interactive terminal** the helper prompts and acts. In **agent
   (non-TTY) context** it prints the advisory and exits 0 *without
   blocking* — **you must surface the advisory to the user, ask which
   option they want, and relay their choice** by re-running with the
   matching flag:
   ```bash
   # user chose [y] — create docs/memory/people.md from the template:
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" team-check --bootstrap <target>
   # user chose [never] — write the opt-out marker, never ask again:
   python3 "${PLUGIN_ROOT}/skills/memory-sync/memory.py" team-check --never <target>
   # user chose [n] — do nothing this run (they'll be asked next memory-sync).
   ```
   `team-check` is a no-op when `people.md` already exists, when
   `.jig/no-people-md` is present, or when the project is still solo —
   so it is safe to run unconditionally at the end of every memory-sync.

## Judgment guidance

- **Don't over-persist.** Persisting trivia bloats memory files. If you wouldn't
  want to read it back in a future session, don't write it.
- **"≥3 references" is your judgment.** The helper does not track session counts —
  you decide when a term has been used enough to deserve hot-cache promotion.
- **Inbox > glossary** when in doubt. An inbox entry can be promoted later; a
  premature glossary entry pollutes the searchable terminology.
- **The reviewer subagent cannot run this skill.** Reviewers read from memory but
  must not write — defining the glossary is not the reviewer's job (see
  `agents/reviewer.md`).

## Self-healing

If `docs/memory/` or `docs/inbox.md` don't exist (pre-scaffold-init project),
the helper creates them. If `AGENTS.md` is absent, `promote` falls back to
`add-term` (writes to glossary) and warns on stderr. The skill works on
unscaffolded projects, though scaffold-init is the recommended setup.

## Gotchas

- `add-term` and `add-learning` are idempotent on the exact heading text. Re-running
  with the same `term`/`title` is a no-op. To genuinely update an existing entry,
  edit the file by hand or use Edit.
- `add-inbox` is NOT idempotent — it always appends. The inbox is a stream; near-
  duplicates are tolerated and triaged later.
- `promote` is idempotent on a line-anchored `- **<term>**` match. If a term is
  in the Key terms list with a slightly different label or hyphenation, it counts
  as new.
- `promote` inserts new bullets immediately after the `### Key terms` heading
  (LIFO — newest first). This is intentional: the most recently promoted term is
  the most likely to be referenced in the next session. If alphabetical or
  chronological order is preferred later, this is a design point worth revisiting.
- Definitions are stored as-is; markdown is allowed but be conservative — these
  files are scanned by humans more often than parsed.
