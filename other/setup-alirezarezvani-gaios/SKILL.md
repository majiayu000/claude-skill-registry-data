---
name: setup
description: First-run guided setup for a fresh gAIOS clone. Interviews the user (identity, role, priorities, voice, connections, team, pain, guardrails) and fills the templates — CLAUDE.md, context/, references/voice.md, connections.md — then introduces the WAT / wiki / workflows / experiments features. Trigger on "/setup", "set me up", "get started", "onboard me", or a fresh clone where CLAUDE.md still has {{placeholders}}.
---

# Setup — make this AIOS yours

A guided interview that turns the blueprint into a personalized AIOS. Read `aios-intake.md` first; if it's filled, confirm and scaffold; if not, run the interview conversationally, **one question at a time, with a recommended answer** so the user can confirm/correct.

## Interview (capture each answer into `aios-intake.md` as you go)
1. **Who are you** — role, company, what you own. (→ `context/about-me.md`, `CLAUDE.md` header)
2. **Voice samples** — ask the user to **paste 1–2 real, unedited** things they've written. *Refuse typed-fresh prose* (it contaminates the sample). (→ `references/voice.md`)
3. **90-day priorities** — dated, concrete. Push back on vague. (→ `context/priorities.md`)
4. **Business** — what it sells, to whom, the model. (→ `context/about-business.md`, Knowledge base)
5. **The stack** — where revenue/customers/comms/docs/tasks live. (→ `connections.md`)
6. **The team** — roster + who can absorb delegated work. (→ `context/about-team.md`)
7. **The constraint / pain** — what eats the week; what to hand off first.
8. **Guardrails** — the hard rules + sensitive-data line + any compliance regime (GDPR/HIPAA/SOC2/...); what may be sent/acted-on vs only drafted. (→ `CLAUDE.md` Guardrails)

## Scaffold (after the interview)
Fill every `{{placeholder}}` in `CLAUDE.md` (name, persona, knowledge base, voice summary, connections, **guardrails — customize rule #1 and #8 to the domain**). Write `context/*`, `references/voice.md`, and the `connections.md` rows. Back up any existing versions to `archives/` first.

## Introduce the engine (one screen)
Point the user at: `/structure` (frame fuzzy asks) · `/triage` · `/daily` · `/weekly` (Cadence) · `/wiki` (second brain: `raw/` → `wiki/`) · `/graph` · `/graph-query` · `/graph-ingest` (knowledge graph) · `/workflow` (dynamic workflows) · `/experiment` (autoresearch loop) · `/audit` + `/level-up` (weekly). Then suggest the first prompt: *"what should I focus on this week?"*

## Optional: knowledge graph (graphify)
Offer to set up the knowledge graph so the user can *see* and query their code + second brain: run `python tools/graphify_setup.py install` (installs graphify and wires the Claude Code & Codex skills). Then `/graph` builds it. Skippable and additive — graphs **code + the committed `wiki/` only**, never `raw/`.

## Rules
- Voice paste cannot be skipped or typed fresh.
- One-shot scaffold after the interview; the user iterates by editing `aios-intake.md` and re-running.
- Customize the Guardrails block to the user's domain — don't ship the generic defaults unchanged for a regulated business.
