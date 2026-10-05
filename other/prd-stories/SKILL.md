---
name: prd-stories
description: >
  Use when the user wants to evolve the features of a PRD roadmap with user stories — 'refinar
  as histórias da feature', 'escrever histórias de usuário', 'critérios de aceite', 'regras de
  negócio da feature', 'deixar a feature pronta', 'user stories for FT01' — one feature at a
  time, interviewing the human until each story meets the Definition of Ready: persona, value,
  INVEST, CA (Gherkin, happy and error paths) and RN from the PRD. Do NOT use to create the
  roadmap (prd-roadmap) or to change requirements without stories (prd-refine).
metadata:
  version: 3.0.0
---

# Evolve features with user stories, CA and RN

You interview the human in the MAIN session, one question at a time — never in a subagent.
Quality bar: `<plugin-root>/references/user-stories.md` (format, INVEST, CA, RN, Definition of
Ready, anti-patterns, review checklist). Read it before the first question.

## Input
The arguments: `<slug>` (required) and optionally a feature ID (`F01-E02-FT01`) or `next`.

## Flow

### STEP 0 — Language
Follow `references/language.md` (resolve `lang` from `.planning/config.json`; ask only if unset).

### STEP 1 — Load

```bash
SLUG="<slug>"   # first word of the arguments
DIR=".planning/prds/$SLUG/roadmap"
[ -f "$DIR/roadmap.json" ] || { echo "NO_ROADMAP"; ls .planning/prds/ 2>/dev/null; }
python3 "<plugin-root>/scripts/roadmap-check.py" "$DIR/roadmap.json" --json
```

- `NO_ROADMAP` → point to `prd-roadmap {slug}` and STOP.
- Checker `FAIL` for reasons unrelated to stories → show them and STOP (the roadmap needs
  `prd-roadmap` revise mode first).
- Read `.planning/prds/{slug}/PRD.md` for personas (Target Audience), FRs and the
  `### Business Rules` section, and `roadmap.json` for features, `rules[]` and `stories[]`.

### STEP 2 — Pick the feature
Without a feature in the arguments, show the progress table and ask which one:

```
📚 Stories of "{slug}" — {ready}/{total} ready · {rules} business rules
| Wave | Feature | Stories | Ready | Missing |
| 1 | F01-E01-FT01 Login | 1 | 0 | CA error path, RN-01 not verified |
...
Suggested next: {first feature in wave order with draft stories}
```

`next` means that suggestion. Refine **one feature per pass**.

### STEP 3 — Review the feature's stories
For each story of the feature, run the review checklist and INVEST from `user-stories.md` and
show a compact diagnosis (story line, CA with paths, RN, what fails). Then fix it with the
human, **one question at a time**, offering 2–3 concrete options when they hesitate:

1. **Persona** — must be named in the PRD audience; never "o sistema".
2. **Split or merge** — a story-epic becomes one story per capability; a feature ends with
   1–5 stories.
3. **Value** — non-circular.
4. **CA** — happy path first, then at least one error or edge path; Gherkin when there is
   state + trigger + observable result; numbers instead of "rápido/fácil"; 3–8 per story.
5. **RN** — ask which business rules decide this behavior. Use existing `RN-xx` from the PRD.
   A new rule discovered here: agree name, one-sentence rule and a concrete example, then it
   goes to the PRD (STEP 5) with the next free ID — never kept only inside the story. Each RN
   listed by the story is verified by at least one CA (`"rules": ["RN-xx"]` on that CA).
6. **Dependencies and out of scope** — `depends_on` other `US-xx`; out-of-scope when the title
   invites scope creep.

Summarize each story (3–6 lines: story line, CA list, RN) and confirm before moving on. Missing
stories for an FR slice of the feature: propose them in the same format.

### STEP 4 — Ready gate
For each story that now meets the Definition of Ready, ask: `Mark US-xx as ready? (y/n)`. Only an
explicit yes sets `"status": "ready"`; everything else stays `draft`.

### STEP 5 — Write
1. Update the feature's stories in `.planning/prds/{slug}/roadmap/roadmap.json` (edit only
   `stories[]` and, for new rules, `rules[]`; keep every other key untouched; keep IDs stable —
   a new story takes the next free `US-xx`, a removed ID is never reused).
2. New business rules → also append them to the PRD `### Business Rules` section, bump the PRD
   `Version` (minor) and add a `### Change Log` row ("RN-07 added while refining F01-E02-FT01").
   The PRD keeps its `Status`; tell the human the PRD was amended.
3. Run the checker (it regenerates `STORIES.md` and `stories/`):
   ```bash
   python3 "<plugin-root>/scripts/roadmap-check.py" ".planning/prds/$SLUG/roadmap/roadmap.json"
   ```
   `FAIL` → fix the story data you wrote (never the generated files) and run it again. Show
   warnings (vague terms, generic persona, unused RN) and offer to resolve them.
4. Log: `sh "<plugin-root>/scripts/audit-log.sh" event stories "" completed ".planning/prds/{slug}/roadmap/roadmap.json" "{feature}: {n} ready"`

### STEP 6 — Summary and next

```
✅ {feature} — {n} stories ({ready} ready, {draft} draft) · CA: {total} · RN: {list}
📁 .planning/prds/{slug}/roadmap/STORIES.md · stories/
{PRD amended: RN-07 (version x.y.z) | no PRD change}

👉 prd-stories {slug} next      → {next feature}
👉 prd-publish {slug}           → GitHub (stories go into the feature issues or become sub-issues)
```

Offer to commit (`git add .planning/prds/{slug}/ && git commit -m "docs(prd): stories for {feature}"`)
only with the human's yes.

## Prohibitions
- NEVER mark a story `ready` without the human's explicit yes
- NEVER keep a business rule only inside a story — it goes to the PRD
- NEVER edit `STORIES.md` or `stories/*.md` by hand — they are generated
- NEVER change features, edges or tasks here — that is `prd-roadmap` (revise)
- NEVER ask two questions at once

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
