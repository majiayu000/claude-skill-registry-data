---
name: onboard-session
description: Begin a bracketed onboarding session over an existing artifact you didn't author — a codebase, a document corpus, a body of papers — inside a agentic-study-environment sub-project. The agent surveys the artifact, walks it part by part with comprehension checks, then has the user reproduce a recent change from its history. Use whenever the user signals they want to get up to speed on something someone else made — phrases like "onboard me on this codebase", "walk me through this repo", "help me get up to speed on X", "I just joined this project", "drop me into this codebase", or "get familiar with this corpus" should trigger this skill. `onboarding` is the fourth core session type; unlike `theory`/`practice`/`role-play` it has its own dedicated entry point rather than being proposed inside `start-session`. A session ends with the `stop-session` skill.
---

# Begin an onboarding session

This skill begins a bracketed **onboarding** session: getting up to speed on an existing artifact — a codebase, a document corpus, a body of papers — that the user did **not** author. The artifact *is* the source material; the goal is a working mental model and the confidence to make changes, not learning a topic from first principles.

Onboarding is one of the harness's four core session types, alongside `theory`, `practice`, and `role-play`. The other three are proposed and run through `start-session`; onboarding gets its own skill because its shape differs enough to warrant it — a read-only pass over an artifact outside the usual source-materials flow, its own three-phase protocol, and its own artifact tree under `work/onboarding/`.

## When to use

The user wants to get familiar with something someone else built or wrote — a new job's codebase, an open-source project, a teammate's service, an inherited body of papers, a legal corpus. Phrases like "onboard me on this codebase", "walk me through this repo", "help me get up to speed on X", or "I just joined this project" should match.

If the user has not bootstrapped a sub-project yet, redirect them to the `bootstrap` skill first.

If the user instead wants `theory`, `practice`, or `role-play`, redirect to `start-session` — this skill only runs `onboarding`.

## What to read before doing anything else

Before proposing or conducting anything, load context — the same up-front reads as `start-session`:

1. The harness's optional `.studyenv/AGENTS.md` if present, otherwise `.studyenv/CLAUDE.md` if present (for cross-project conventions and any global `Language:`), and `.studyenv/PROGRESS.md`. Both are optional context; if either is missing, continue without it.
2. The sub-project's `.studyenv/<name>/AGENTS.md`, falling back to `.studyenv/<name>/CLAUDE.md` for older projects (for `Domain:`, `Language:`, goals, Tools & Materials), and `.studyenv/<name>/PROGRESS.md` (for what's been covered and at what status).
3. The sub-project's `.studyenv/<name>/ai-agent-materials/` — especially `curriculum.md`, which may already name an `onboarding` topic entry — and `work/onboarding/map.md` if a prior onboarding session left one (so you resume where the last one left off, rather than re-surveying from scratch).
4. If the sub-project declares `Domain:`, load the matching overlay at `../../domains/<domain>.md` (relative to this SKILL.md). The overlay supplies the four onboarding parameters below; if no `Domain:` is set, the generic protocol applies over a flat corpus.

## The onboarding protocol

Run the **generic onboarding protocol** defined in `../../reference/conventions.md` → *Onboarding session protocol (generic)*: Phase 0 (identify the target artifact, read it read-only, build `work/onboarding/map.md`, propose an ordering), Phase 1 (teach one part at a time — explain, send the user to the real artifact, ask comprehension/prediction questions), Phase 2 (pick a few small recent changes from the artifact's history, let the user pick and reproduce one, then review against what actually happened), Phase 3 (wrap-up — see *Ending the session* below).

The active domain overlay fixes the protocol's four parameters — **what the corpus is**, **what "send the user to read" points at**, **what "a recent change" means**, and the **`work/onboarding/` artifact layout**. `coding` (`../../domains/coding.md`) ships the canonical worked flavor for codebases; `academic-research`, `legal-documents`, and `speech-therapy` inherit the generic protocol unchanged for papers, legal corpora, and clinical material respectively. With no `Domain:` set, the generic protocol applies as-is.

This is the **one case** the agent may read outside `.studyenv/` — the designated onboarding target — and only read-only; the user's reproduction work happens under `work/onboarding/` like everything else the harness generates.

## Language

Reply in the conversational language declared by the active `Language:` field (BCP 47 tag), per `../../reference/conventions.md`. File names, symbols, code identifiers, and verbatim excerpts from the target artifact stay in their original language regardless of the setting.

## Ending the session

Onboarding is not in-character, so there is no role-play debrief. When the user signals they're done — "stop session", "wrap up", or similar — invoke the `stop-session` skill. It records which parts were walked and at what comprehension, which change was reproduced and how it compared, and the next part to onboard onto (see `../stop-session/SKILL.md` → *Onboarding sessions*).

## Related skills

- `bootstrap` — mint a new sub-project.
- `start-session` — the other three core session types (`theory` / `practice` / `role-play`).
- `stop-session` — record progress and summarize at session end.
