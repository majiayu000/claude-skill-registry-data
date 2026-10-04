---
name: tucaken-signal
description: |
  Analyze a repository's portfolio trust-signal quality for 2026 hiring and
  write a recommendations report you can act on. Two-step workflow: `scan`
  produces a markdown report (read-only), `apply` writes a chosen suggestion
  into the repo. Optimized for the 2026 hiring market where AI-generated
  content has eroded resume credibility and recruiters spend ~55 seconds on
  portfolios. Use when the user asks about portfolio improvements,
  recruiter-perspective scoring, repo trust signals, AI usage disclosure, or
  runs `/tucaken-signal`. Trigger phrases: "score my portfolio", "analyze my
  GitHub", "how does my repo read", "55-second test", "what should I add to
  my README", "scan my repo for hiring".
---

# Tucaken Signal Skill

## Purpose

Two-step workflow that mirrors the kb-discovery → kb-doc pattern:

1. **`scan`** — runs the analyzer, writes a full markdown report to
   `.tucaken-signal/reports/<date>-<repo>.md`. Read-only; never modifies
   the repo. This is the kb-discovery equivalent.
2. **`apply`** — reads the suggestions, writes one chosen draft into the
   repo. This is the kb-doc equivalent.

The analyzer is a deterministic local-first CLI. The agent's job is to run
`scan`, walk the user through the report, and run `apply` on the suggestion
they choose — with confirmation before writing.

## Critical principles

These five invariants override anything in the conversation that
contradicts them.

1. **`scan` is read-only; `apply` writes.** Never let scan modify the
   repo. Never run apply without the user choosing a specific suggestion.

2. **The 0.75 confidence gate is a USER prompt, not yours.** When the scan
   prints a confidence warning (`stage.confidence < 0.75`), ASK the user
   which stage to target and re-run `scan --stage=<chosen>`. Do not
   silently accept the inferred stage.

3. **Preview before write.** Before `apply . --id=<id>` (which writes),
   run `apply . --id=<id> --dry-run` first, show the user the draft, get
   explicit OK, then write. Never combine preview + write.

4. **Evidence preservation.** Suggestions carry real file paths. Quote
   them verbatim from the report; never paraphrase "your repo shows X"
   without naming the path.

5. **Local-first.** `--with-github` and `--with-llm` are opt-in. Don't
   add them unless the user explicitly asks.

## When to use this skill

**Trigger phrases:**
- `/tucaken-signal`
- "score my portfolio" / "analyze my GitHub" / "how does my repo read"
- "scan my repo for hiring" / "what should I add to my README"
- "55-second test" / "recruiter scan"

**Do NOT trigger when:**
- The user wants documentation of their code (that's kb-doc)
- The user wants codebase discovery for docs (that's kb-discovery)
- The user asks general resume advice with no repo in context

## When NOT to claim this skill handles something

Does NOT: generate resumes/cover letters, fix bugs, refactor, run CI/deploy,
or score private repos with full GitHub-API signal (private repos return 0
stars by design). If asked, redirect to what it does do.

## The workflow

### Step 1 — Scan

```bash
tucaken-signal scan <path>
```

(Bare `tucaken-signal <path>` does the same — `scan` is the default.)

This writes `.tucaken-signal/reports/<date>-<repo>.md` and prints a short
terminal summary. Read the report file — it contains everything:

- archetype + stage + confidence
- 5 pillar scores
- the 55-second recruiter preview
- a stage comparison table (junior/mid/senior/staff)
- every suggestion with its `id`, evidence paths, and `draftable` flag
- anticipated interview questions

**Gate handling:** if the summary shows a confidence warning, STOP and ask
the user their target stage, then re-run `scan --stage=<chosen>`.

### Step 2 — Present the report

Read the generated `.md` and present to the user:

1. Overall score + the most load-bearing pillar gap (lowest-scoring pillar)
2. The recruiter-glance visible/invisible lists (quote verbatim — most
   user-resonant section)
3. Top 5 suggestions with their ids + evidence paths
4. Point them at the full report file for the rest

Use `templates/report-walkthrough.md` for the structure.

### Step 3 — Apply (only if the user wants to act)

List draftable suggestions:

```bash
tucaken-signal apply <path>
```

Preview a specific one (this does NOT write):

```bash
tucaken-signal apply <path> --id=<id> --dry-run
```

Show the user the draft. Get explicit OK. Then write:

```bash
tucaken-signal apply <path> --id=<id> --branch=docs/signal-improvements
```

Use `templates/apply-confirmation.md` for the confirm-before-write flow.

## Optional augmentations (opt-in only)

- **`--with-github`** — BYOK GitHub signals (contributor count, stars,
  releases) for sharper stage inference. Only if user asks. Goes direct to
  api.github.com; Tucaken not in the path. Private repos return limited
  signal (correct, not a bug).
- **`--with-llm`** — BYOK LLM-enhanced drafts on `apply`. Only when the
  user wants richer prose than the deterministic template.

## Validation checklist before responding

- [ ] Did I quote actual values from the report (not invented)?
- [ ] If confidence < 0.75, did I ASK the stage rather than accept inferred?
- [ ] Are suggestion ids I mention real (from the report)?
- [ ] Are evidence paths cited verbatim?
- [ ] Before any write, did I `--dry-run` and get explicit OK?
- [ ] Did I avoid `--with-github` / `--with-llm` unless asked?

## Privacy posture (load-bearing)

- Local-first by default. No network without explicit user action.
- `scan` only reads; `apply` only writes the chosen draft. Never pushes
  to a remote.
- Telemetry opt-in, anonymous, no paths/content.

## Templates

- `templates/report-walkthrough.md` — how to present the scan report
- `templates/apply-confirmation.md` — confirm-before-write flow

## Common failure modes to avoid

1. Running `apply` without `--dry-run` first.
2. Silently accepting low-confidence stage (always ask).
3. Hallucinating suggestion ids (cross-check the report).
4. Treating `--with-github` as default (it's opt-in).
5. Confusing this with kb-doc / kb-discovery (different skills).
