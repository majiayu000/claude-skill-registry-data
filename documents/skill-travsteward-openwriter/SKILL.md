---
name: authors-voice
description: |
  Author's Voice — constructed-voice skill. Anchors writing to a training-data
  author blend, progressively layers NEVER rules, presentation fingerprints,
  sentence stats, coined terms, and curated examples from a growing local
  corpus. Pure markdown, opus sub-agent (the minion) writes prose.

  Use when: "/authors-voice", "/writers-voice", "set up my voice", "anchor
  my voice", "voice match", "use my voice", "write in my voice", "add to my
  voice profile", "voice profile status", "voice status", "authors voice",
  "writer's voice".

  API path (plugin / programmatic flows): see `docs/api/` for the rewrite +
  generate endpoints, MCP tools, setup, and troubleshooting. The local skill
  body below is the default; the API is one access point among others.
metadata:
  author: travsteward
  version: "0.19.1"
license: MIT
---

# Author's Voice

_This skill is the free, any-agent manifestation of the larger Author's Voice ecosystem — the same anchor + NEVER-rules + anti-AI engine that powers the paid API, the OpenWriter plugin, and the dashboard. Free here, productized there; one voice DNA across all surfaces._

## FIRM RULES

### 1. Editor NEVER writes prose. Every writing task fires a minion.

The editor scopes briefs, cuts, reorders, and patches NEVER violations. Editor does NOT write new prose — every word ENTERING the document is minion-written. Applies to: initial drafts, revisions, bridges, closers, openers, transitions, single-line aphorisms, one-paragraph corrections, gap-fillers, idea-extensions — any new prose, full stop.

Two carve-outs: (1) **violation patch** at Apply step 6 — 1-3 sentence local fix to NEVER violation or brief-error in otherwise-acceptable minion output; constructive rephrase preferred. (2) **co-write mode** — editor writes directly when ALL THREE hold: continuous real-time collaboration (user steering each move), explicit per-piece authorization for THIS piece, small scope (sentence to short paragraph; max one). Blanket authorizations ("you handle it") do NOT trigger co-write — those are delegations and go to the minion.

Editor territory (no minion): cuts, reorders, accept/reject decorations, resolve agent marks, version restores. Cuts that leave holes needing new connective tissue — the connector is minion work.

Rationale: editor context is polluted by the live conversation; voice anchors lose to active context; minion in clean context with voice files loaded outperforms editor-with-intent.

If the editor catches itself drafting prose mid-conversation, **STOP** and spawn a minion — even for one sentence.

### 2. After anchor critique, discuss before revising.

Anchor critique returns scores + convergent diagnostic. First move after aggregation: surface to user, discuss what to act on / disagree with / defer, align scope. Then spawn revision minions. Critics are advisory; user owns the prose.

Anchor critique result protocol:
1. Aggregate panel scores + convergent diagnostic.
2. Surface to user: scores, themes raised by 3+ critics, proposed CUTS (subtraction) and REWRITES / ADDITIONS (new prose).
3. Discuss. User decides act / disagree / defer. No revision begins until this happens.
4. Editor executes agreed CUTS directly (Rule 1 carve-out).
5. Editor scopes briefs for agreed REWRITES / ADDITIONS, spawns revision minions per brief.
6. Patch micro-violations on returned prose.
7. Re-fire panel only if user wants another pass.

### 3. Revisions must be tighter than the original. If a revision is additive, the editor wrote it.

Critique-driven revision produces a smaller word count, not larger. If post-revision is longer than pre-revision, the editor was inventing rather than executing the diagnostic. Revision minion brief specifies a WORD-COUNT TARGET (often "this paragraph in 60% of the original"). Minion compresses. Editor verifies the count dropped.

## Architecture

Skeleton prompt template (`prompts/skeleton.md`) assembled from per-user `voice/*.md` files at write time. Editor loads skeleton, substitutes `{INCLUDE: ...}` markers, fills `{TASK}`, spawns a fresh opus sub-agent (the minion) with the assembled prompt (Claude Code) or dispatches via `task({ subagent_type: "general", prompt: <assembled skeleton> })` (OpenCode). Minion has no session pollution, returns prose, dies. Editor integrates.

```
writers-voice/
├── SKILL.md            (this file — router + firm rules + Apply Protocol)
├── docs/               (on-demand: setup, analysis, apply-deep, anchor-iteration, context-hygiene, tiers)
├── catalog/            (read-only reference: ai-tells, fingerprints, hurdle, anchor-prompt, author-hints, post-write-audit)
├── prompts/skeleton.md (template + injection points)
└── voice/              (user-specific — anchor blend, NEVER rules, stats, fingerprints, coined-terms, examples, corpus/)
```

Lean / rich split: `voice/*-analysis.md` is human-facing only — never injected into the minion prompt.

## Routing

| User intent | Action |
| --- | --- |
| "set up my voice" / "/writers-voice" / first run | **Setup Flow** — `docs/setup.md` |
| "add this essay to my voice profile" / "save this writing" | Append to `voice/corpus/`, run **Analysis Protocol** — `docs/analysis.md` |
| "voice status" / "what's locked" / "tier" | Read `voice/status.md`; tier reference at `docs/tiers.md` |
| (User asks the agent to write anything) | Run **Apply Protocol** (below) after **Context Hygiene** check — `docs/context-hygiene.md` |
| "show me my anchor" / "show me my fingerprints" | Read the relevant `voice/*.md` and report |
| "regenerate my profile" / "re-analyze my corpus" | **Analysis Protocol** — `docs/analysis.md` |
| "make a book / business / [context] voice anchor" | **Anchor Protocol** for that register — `docs/setup.md` |
| "split my anchor by register" | **Multi-Register Split** — `docs/setup.md` |
| Book-scale project (multi-chapter book) | Load `/book-writer` skill — that's the orchestration layer (chapter architecture, beats methodology, workspace management, book mode, long-form orchestration). This skill provides the Apply Protocol that `/book-writer` delegates to for every prose pass. |
| "polish this" / "iterate to 90" / final-polish ready prose | **Anchor Iteration** — `docs/anchor-iteration.md` |
| "use the API" / "call author's voice from a workflow" / plugin / programmatic | API path — `docs/api/protocol.md` (rewrite, generate, MCP tools, setup, troubleshooting) |

## Apply Protocol (Apply Minion — generative writing from commitments)

Four minion types (full taxonomy: `docs/apply-protocol-deep.md`): **Apply** (generative, no source prose) · **Rewrite** (Apply + context awareness, updated commitments) · **Blinder Audit** (critic — paragraph-level substance duplication only) · **Anchor Iteration** (polish — channels voice anchors as panel, iterates critique → rewrite → re-score until 90/100).

Pick the wrong minion → weak output. Substance problem → Rewrite, not Apply. Rough draft → not Anchor Iteration.

When the user asks for a voice-matched write:

1. **Context Hygiene check.** Reset if polluted — `docs/context-hygiene.md`.
2. **Pick the anchor.** List `voice/anchor*.md`. If only `voice/anchor.md`, use it. If context-specific, infer from request or ask. Fallback: `voice/anchor.md`.
3. **Assemble the minion prompt.** Read `prompts/skeleton.md`. For each `{INCLUDE: <path>}`, substitute file contents. If a referenced file is missing (e.g., user hasn't curated examples), drop the entire `{INCLUDE: ...}` line AND its section header. Swap `voice/anchor.md` → `voice/anchor-<context>.md` if a context-specific anchor applies.
4. **Fill `{TASK}`.**

   **Required: COMMITMENTS** — what must be true of the output (concepts, claims, sequence, register, avoidances, length).

   **DEFAULT MODE: pure generation (regenerate).** SEMANTIC commitments only — what claims must land, not how to phrase them. No structural beats. No paragraph patterns. No device prescription. No sentence-rhythm prescription. The shape of any prescription becomes a ceiling on what the model produces. Let the minion bring its own moves. Always.

   ### Never write meta-references into commitments

   Anything the prose reader cannot see — chapter labels, beat numbers, "as discussed earlier", "the previous beat established" — does NOT belong in commitments. The minion reproduces them literally and breaks the fourth wall. Commitments describe what must be COMMUNICATED, never how the editor is thinking about structural position. If continuity from a prior section matters, capture it as the SUBSTANTIVE thread the new section must pick up (the content, not the structural pointer).

   ### COMMITMENTS function as quasi-verbatim instructions

   When the editor writes a commitment with literal phrasing in parentheses (*"Define sleep debt (lost sleep compounds like unpaid interest)"*), the model treats the parenthetical as exact phrasing to reproduce — every section gets that line. For multi-section work where phrasing should vary, write commitments abstractly (*"Define sleep debt"*) and let the model phrase. Use literal commitments only when a specific phrasing MUST land.

   ### Read prior integrated sections first (multi-section work)

   Read prior integrated sections before writing this one's brief. Cadence shapes already used, substantive threads to pick up, and heavy-use coined terms are only visible by reading what's on the page. Set the new section's commitments and cadence prescription against that context.

   ### Preservation scope (load-bearing call on a gradient)

   | Mode | Source prose in TASK? | Commitments shape | Use when |
   |---|---|---|---|
   | **Full preservation (rewrite mode)** | YES | "preserve every load-bearing claim; refine voice while preserving structure and phrasing" | source is already strong; author has specific phrasing that must land; polishing voice-applied work |
   | **Pure generation with selective lifts** | NO | OMIT source. Identify 1-3 specific moves worth keeping. Lift them pre-emptively (MUST-APPEAR-VERBATIM in brief) OR post-edit (patch in after minion returns) | source is mostly weak with 1-3 lines worth keeping. Pre-emptive when known in advance; post-edit when the strong move is only obvious after seeing the minion's output |
   | **Pure generation (regenerate)** | NO | SEMANTIC commitments only — what claims must land, not how to phrase them | source is "good but not great"; want dramatic improvement; existing shape would constrain output; high-stakes piece. The shape of the source becomes a ceiling on what the model produces |

   ### Cadence prescription (optional, recommended for high-stakes writing)

   Lifts voice fidelity ~0.5 points over baseline. Explicit rhythm scaffolding doesn't constrain content; it frees capacity by removing "what shape should this take?" overhead.

   Example: *"Para 1: open with 3 short declaratives, stack medium with concrete examples, close with one analytical long. Para 2: alternate short claim with longer explanatory, end with sharp short. Para 3: build with longer analytical, end with single-line aphoristic close."*

   **Vary cadence prescriptions across sections.** Same prescription per section produces document-scale rhythm repetition (every section opens with 3 shorts, closes with aphorism) — invisible at section scale, mechanical at document scale.

   Edge-case guidance (Rewrite Minion brief template, Blinder Audit brief shape, multi-section context-loading layers, writing minion taxonomy): `docs/apply-protocol-deep.md`.
5. **Spawn the minion.** Claude Code: `model: "opus"`, `subagent_type: "general-purpose"`. OpenCode: `subagent_type: "general"` with no model parameter (subagent inherits parent model; encourage using the session's strongest model). Both: `prompt: <assembled skeleton>`.
6. **Patch NEVER violations + brief-error meta-references.** Smallest local span. Constructive rephrase preferred (contrastive negation → direct statement; banned word → plain equivalent; meta-reference → substantive thread it pointed at). Don't regenerate; minion voice IS the result. Detail: `docs/apply-protocol-deep.md`.
7. **Post-write audit.** Read `catalog/post-write-audit.md` and apply distribution-level checks (opener repetition, sentence-initial "The", function-word over-use, sentence-length variance, lexical watch list). For each failing check, surgically rewrite the smallest local span — 5-10 light substitutions across a typical draft; heavier rewrites mean misuse. Load-bearing prose wins ties.
8. **Integrate via openwriter.** `write_to_pad` for edits, `populate_document` for new docs.
9. **Cross-section coherence review** (multi-section only). (a) Editor self-review — cut test: could you delete this paragraph and lose only redundancy? (b) **Mandatory Blinder Audit Minion** — fresh-context critic, paragraph-level substance duplication only. Most well-written beats produce zero findings. Brief template + exclusions: `docs/apply-protocol-deep.md`.
10. **Polish (optional, two patterns).** (a) **Parallel pick-best** — N (3-6) Apply minions in parallel, same brief; editor picks best whole, mixes variants, or hands all to user. (b) **Anchor Iteration** — `docs/anchor-iteration.md`. Polish-class only; not for rough drafts.
11. **`/anti-ai` pass.** MANDATORY after Anchor Iteration (which runs no-context and introduces AI tells). OPTIONAL otherwise. Global surface fingerprints (em-dashes, semicolons, contrastive negation, banned diction, register monotony) vs `voice/never-rules.md` + `voice/fingerprints.md`. Complements step 7.

**Use opus (Claude Code).** Sonnet leaks 3+ NEVER violations where opus leaks 0-1. Haiku loses voice. **OpenCode:** subagents inherit the parent model — use the strongest model available in the session for prose generation.
**Send full editing scope.** If 6 of 8 paragraphs need fixes, send all 8 for flow continuity.
**One minion per natural editing unit** — beat, section, blog post, tweet thread.

## Tiers + Companion Skills

Voice profile tiers (Empty / Anchor / Preliminary / Full Coverage / AV-Grade) gate features by corpus word count. Table: `docs/tiers.md`.

Companions: `/anti-ai` (final fingerprint scrub) · `/voice-presets` (generic frames, no profile — if installed) · Author's Voice plugin (paid — full RAG, inline edits, deterministic extraction).
