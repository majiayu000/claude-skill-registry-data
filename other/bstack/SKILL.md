---
name: bstack
category: governance
latent_only: true
description: "bstack primer — the Broomva Stack: twenty irreducible automation primitives (P1–P20) that turn an agent-driven workspace into a self-operating system. This is the AGENT-READABLE PRIMER (primitive contract + short-name index + when each fires), NOT the CLI. The bstack CLI + governance substrate (bin/, doctor, templates, hooks) is a separate product installed by clone + bootstrap (git clone https://github.com/broomva/bstack && ./bin/bstack bootstrap) — do NOT `npx skills add broomva/bstack` (it drops bin/scripts, the repo-root SKILL.md case of vercel-labs/skills#1523). Use this primer to reason with the primitives: Bridge (P1), Gate (P2), Tickets (P3), Pipeline (P4), Fanout (P5), Bookkeeping (P6), Freshness (P7), Janitor (P8), Wait (P9), Hygiene (P10), Empirical (P11), Persist (P12), Dream (P13), Dep-Chain (P14), Snapshot (P15), Crystallize (P16), Lens (P17), Audience (P18), Orchestrate (P19), Cross-Review (P20). Triggers on 'bstack', 'Broomva Stack', 'the primitives', 'P1'..'P20', 'primitive contract', 'bstack bootstrap', 'governance metalayer', 'self-operating workspace', 'how do I install bstack', 'what does Pn mean'."
---

# bstack — the Broomva Stack (primitives primer)

**A portable harness metalayer for AI-native development.** Twenty irreducible
primitives that turn any agent-driven workspace into a self-operating system. Each
primitive closes one failure mode that otherwise drifts into entropy in unsupervised
agent sessions.

> **This file is the agent-readable *primer*, not the CLI.** It teaches you the
> primitive contract so you can reason with it. The bstack CLI + governance substrate
> (the `bstack` binary, `doctor`, templates, hooks, schemas) is a **separate product**:
>
> ```bash
> git clone https://github.com/broomva/bstack.git
> cd bstack && ./bin/bstack bootstrap
> ```
>
> Do **not** `npx skills add broomva/bstack` — bstack has a repo-root `SKILL.md`
> beside `bin/`, so skills.sh copies only that file and drops the CLI
> ([vercel-labs/skills#1523](https://github.com/vercel-labs/skills/issues/1523)).
> `bstack bootstrap` installs the companion-skill roster from **this monorepo**:
> `npx skills add broomva/skills --skill <name>` per entry.

## Referencing primitives

Use the `Name (Pn)` form in prose — *"applying Snapshot (P15)"*, *"via Dep-Chain
(P14)"*, *"running Bookkeeping (P6)"*. The number is the canonical id; the name is
the human handle.

**Short-name index:** Bridge (P1) · Gate (P2) · Tickets (P3) · Pipeline (P4) ·
Fanout (P5) · Bookkeeping (P6) · Freshness (P7) · Janitor (P8) · Wait (P9) ·
Hygiene (P10) · Empirical (P11) · Persist (P12) · Dream (P13) · Dep-Chain (P14) ·
Snapshot (P15) · Crystallize (P16) · Lens (P17) · Audience (P18) · Orchestrate (P19) ·
Cross-Review (P20).

## The twenty primitives

| # | Primitive | Closes / does |
|---|-----------|---------------|
| **P1** | **Bridge** — Conversation Bridge | Session amnesia. Stop hook → JSONL → docs → vault; capture is automatic. |
| **P2** | **Gate** — Control Gate | Destructive ops the model didn't authorize. PreToolUse hook → `.control/policy.yaml`; G1–G4 never bypassed. |
| **P3** | **Tickets** — Linear Tickets | Invisible work. Every unit tracked Backlog → Done; no significant work without a ticket. |
| **P4** | **Pipeline** — PR Pipeline | Merging unreviewed code. Branch → PR → CI → merge → deploy; never merge on red. |
| **P5** | **Fanout** — Parallel Agents | Serial bottlenecks. Concurrent isolated agents via worktrees; no shared mutable file writes. |
| **P6** | **Bookkeeping** — Knowledge Bookkeeping | Lost knowledge. Score → promote → entity pages → synthesize. Capture is a reflex, **never a question** — file it, report after. |
| **P7** | **Freshness** — Skill Freshness Check | Silent skill rot. SessionStart nudge when installed skills are ≥7d stale. Never blocks. |
| **P8** | **Janitor** — Branch + Worktree Janitor | Dead branches/worktrees. `make janitor` removes squash-merged + orphaned safely; default dry-run. |
| **P9** | **Wait** — Productive Wait | Sleeping on CI. `gh pr checks --watch` via background; drain a work-queue while blocked. Never `sleep`. |
| **P10** | **Hygiene** — Worktree Hygiene | Dirty trees. Decide worktree-or-not before the first file; a clean `git status` is the only reliable reset point. |
| **P11** | **Empirical** — Empirical Feedback | Reasoning mistaken for validation. Validate by *interacting* — log-tails, E2E, screenshots, deploy verification. |
| **P12** | **Persist** — Persistent Loop | Work that must outlive one session losing its state. State lives in the filesystem; each iteration spawns a fresh context. |
| **P13** | **Dream** — Dream Cycle | Dense low-tier signal corrupting sparse high-tier rules. Cross-tier consolidation replays against a frozen substrate (stop-gradient). |
| **P14** | **Dep-Chain** — Dependency-Chain Reasoning | "Think deeply" as ritual. Enumerate upstream + downstream (concrete file paths, function names) in the response — not in your head. |
| **P15** | **Snapshot** — State-Snapshot Before Action | Plans built on stale state. Surface `git status` + branch + ahead/behind + open PRs + CI/deploy state *before* planning. |
| **P16** | **Crystallize** — Crystallization (the engine) | Patterns staying in the operator's head. Recurs ≥3× → promote to skill / rule / gate. The meta-primitive that produces the others. |
| **P17** | **Lens** — Lens-Routed Articulation | `act as X` persona theater. Route input through a lens registry that loads *substantive* context, not a persona rewrite. |
| **P18** | **Audience** — Format-Follows-Audience | Wrong format by habit. Agent-read → markdown; human-read (specs, reports) → rich HTML. Format follows audience. |
| **P19** | **Orchestrate** — Mechanism Selection | "Continue please" handoffs. Pick the autonomous-continuation mechanism by the 2×2×2 cube before substantive work. |
| **P20** | **Cross-Review** — Cross-Model Adversarial Gate | Single-model echo chambers. The writer cannot be the final judge; fire a cross-model gate (≥7/10) before merging substantive PRs. |

## When to use this primer

- You're operating in a bstack-governed workspace and need the primitive contract to reason with.
- Someone references `Pn` / a primitive short-name and you need its meaning + invariant.
- You're deciding **how** to install bstack (answer: clone + `bstack bootstrap`, not skills.sh).
- You want the discipline without the CLI (this primer is enough to *apply* the primitives by hand).

The full mechanism specs, the `bstack doctor` primitive-contract linter, the RCS
control-loop math, and the governance templates all live in the CLI repo
(`github.com/broomva/bstack`). This primer is the entry point; the substrate is the product.
