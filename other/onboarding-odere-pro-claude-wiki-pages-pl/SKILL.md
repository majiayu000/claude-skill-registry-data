---
name: onboarding
description: >
  First-run guided tour for a brand-new user. Walks from a fresh project to a
  working wiki: health check → scaffold the vault → drop a first source →
  ingest (with automatic git-checkpointed self-heal) → ask a first question.
  Trigger when the user says "get started", "onboard me", "set this up",
  "what now", "how do I use this", "first time", or invokes
  /claude-wiki-pages:onboarding directly. Idempotent — safe to re-run; it
  resumes from wherever the vault already is.
allowed-tools: Read Bash Glob Grep
---

# Onboarding — guided first run

Take someone from "just installed the plugin" to "I have a cited answer from my
own wiki" in five short steps. Each step verifies before moving on and explains
what just happened, so the user learns the model by doing it once.

## Principles

- **One step at a time.** Do a step, show the result, say what is next. Never dump the whole pipeline.
- **Resume, don't restart.** Probe state first; skip steps already done. Re-running is always safe.
- **Self-healing.** Ingest runs the git-checkpointed auto-heal; never ask the user to fix structure by hand.
- **Plain language.** The user does not need to know the words "MOC" or "frontmatter" to finish onboarding.

## Steps

1. **Health check.** Run `/claude-wiki-pages:doctor` (or `bash scripts/doctor.sh`). If anything is red, run it with `--fix` and explain what was repaired. Confirm Bun is present (the engine) — if not, note that hooks still work and point to <https://bun.sh>.
2. **Scaffold the vault.** If no vault exists, run the `init` skill to create `vault/` (immutable `raw/`, maintained `wiki/`, schema in `vault/CLAUDE.md`). Tell the user where it is and that `raw/` is for _their_ sources.
3. **Add a first source.** Check whether `vault/raw/` already contains the bundled sample source (`sample-source.md`) — it is seeded there by the scaffold so first-time users can ingest immediately without providing their own material. Tell the user it is there. Ask whether they want to add their own file instead or alongside it; if so, ask them to drop it into `vault/raw/` and confirm it landed.
4. **Ingest.** Run the ingest flow (`/claude-wiki-pages:wiki "ingest the new source"`). Explain that the plugin reads the source, writes cited wiki pages, and **auto-heals the wiki under a git checkpoint** (so it is always reversible with `git revert`). Show the new pages.
5. **Ask a question.** Run `/claude-wiki-pages:query "<a question the source can answer>"`. Show the answer with its `[[wikilink]]` citations — this is the payoff: answers grounded in the user's own material.

## Close

End with a short "what you can do next" map:

- Ingest more sources: drop files into `raw/` and run `/claude-wiki-pages:wiki` — that is the one verb for everything.
- Ask questions: `/claude-wiki-pages:query`.
- Rollback: `git log` inside the vault.
- Something feels wrong: `/claude-wiki-pages:doctor`.
- Power users: `/claude-wiki-pages:engine-api` to drive the deterministic engine directly.
- **Optional — work offline with a local model (Ollama).** If the user mentions
  privacy, offline use, or Ollama: ingestion and querying also run with zero
  Claude through a gate-approved local model (`qwen3-coder:30b` today). Point
  them at `docs/local-models.md` for the two-line `localModel` config and the
  `scripts/offline-draft.sh` / `scripts/offline-query.sh` commands. Mention the
  safety net plainly: an unapproved model or tier is refused, and a query answer
  is shown only after every citation verifies against their wiki — otherwise it
  is denied with a warning. Do not set this up unprompted; it is an opt-in.

## Specification anchor

Contracts: [`docs/architecture.md`](../../docs/architecture.md) (commands & `claude-wiki-pages-onboarding-agent`).
