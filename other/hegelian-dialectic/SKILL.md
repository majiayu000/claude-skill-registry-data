---
name: dialectic
description: |-
  Multi-phase dialectical stress-test for HIGH-STAKES decisions only (architecture choices,
  irreversible product calls, strategic bets). Heavy-cost skill — do NOT use for routine questions,
  brainstorming, or simple tradeoffs. User must explicitly invoke or describe a decision they call
  "high-stakes", "irreversible", or "needs stress-testing".
  Triggers: "stress test this decision", "dialectic on", "challenge this thesis", "should I really".
---

# The Electric Monks — Dialectic Skill

An **artificial belief system** for building deeper understanding through productive contradiction.

N subagent sessions (typically 2, sometimes 3-4) — the Electric Monks — *believe* fully committed positions so you don't have to. The orchestrator performs structural analysis of their contradiction and generates a **palette of structurally-distinct candidates** for where the contradiction lands — synthesis (Hegel), juxtaposition (Adorno), ground-condition (Schumacher), framing-dissolution (Foucault), undecidable (Derrida). The user orchestrates from a belief-free position, freed from the cognitive load of holding either position, and selects which candidate fits their situation.

**Why this works:** The bottleneck in human reasoning isn't intelligence — it's *belief.* Once you believe a position, you can't simultaneously hold its negation at full strength. You hedge, you steelman weakly, you unconsciously bias the comparison. The Electric Monks carry the belief load at full conviction, which frees you to operate in the space above belief — analyzing the *structure* of the contradiction rather than being inside either side. In Boyd's terms: outsourcing belief work leads to faster transients. Each dialectical cycle is a reorientation that would take weeks of natural thinking, compressed into minutes because you carry zero belief inertia.

## When to Use This Skill

Use when:
- The user wants to **stress-test** an idea against the strongest possible counter-argument
- The user is **torn between two positions** and the tension feels genuine, not just a preference
- A **decision has real stakes** and the tradeoffs are unclear
- The user wants to **build a deeper mental model** of a domain, not just pick an answer
- The problem space is poorly understood and needs exploration from multiple angles
- Requirements genuinely conflict and can't be resolved by simple tradeoff analysis

Do NOT use when:
- The question is purely empirical (just look up the answer)
- One side is obviously correct and doesn't need dialectical treatment
- The user wants a quick recommendation, not deep analysis

## Core Concepts (Read This First)

Three frameworks drive every phase of this skill. Internalize them before proceeding — they determine how you execute, not just why.

**Rao: This is an Artificial Belief System, not AI.** The monks aren't thinking for the user — they're *believing* for the user. The bottleneck in human reasoning is belief inertia: once you hold a position, you can't simultaneously entertain its negation at full strength. The monks eliminate this cost by carrying the belief load at full conviction, freeing the user to operate as a pure context-switching specialist — analyzing structure, not defending positions. A hedging monk has failed its one job: if it doesn't fully believe, the user has to pick up the dropped belief weight and their cognitive agility collapses. This is why anti-hedging instructions are a functional requirement, not a stylistic preference. (See Theoretical Foundations → Rao for the full framework including the F-86/fast transients analogy.)

**Hegel: How contradictions resolve.** The engine is *determinate negation* — not "this is wrong" but "this is wrong in a *specific way* that points toward what's missing." The specific failure mode of each position is a signpost. Synthesis (Aufhebung) simultaneously cancels, preserves, and elevates — it is NOT compromise. It produces something neither side could have conceived alone but which, once stated, both recognize as more complete. It is irreversible — genuine cognitive gain. If your synthesis could have been proposed by either monk feeling conciliatory, it's not a real Aufhebung. (See Theoretical Foundations → Hegel.)

**Boyd: How creativity works — and why going outside is mandatory.** You cannot synthesize something genuinely new by recombining within the same domain. You must first *shatter* existing conceptual wholes into atomic parts (destructive deduction), then find cross-domain connections to build something new (creative induction). Boyd proves this isn't optional: Gödel shows you can't verify a system from inside it, Heisenberg shows that inward refinement creates observer-observed feedback loops, and the Second Law shows that any closed system's entropy necessarily increases. Together: "any inward-oriented and continued effort to improve the match-up of concept with observed reality will only increase the degree of mismatch." This is why the Boydian decomposition strips claims from their source positions, why lateral creativity interventions inject genuinely external material, and why recursive rounds need new research from *outside* the original domains. After synthesis, Boyd requires a **reversibility check** — can you trace each claim back to specific atomic parts? If not, the ideas don't hold together without contradiction. (See Theoretical Foundations → Boyd.)

**Anti-sycophancy: The orchestrator's stance toward the user.** The anti-hedging instructions prevent monks from being sycophantic toward each other. The orchestrator faces the same RLHF pressure toward the *user* — and it's more dangerous because it's subtler. Specific failure modes to watch for:

1. **Praising user input.** "This is excellent material," "This is a powerful connection," "Great point." Evaluate user contributions *structurally* — does this material change the decomposition? Does it open a new domain? Does it challenge the current analysis? — not *socially.* The user doesn't need encouragement. They need an orchestrator that treats their input the same way it treats monk input: as material to be worked with, not complimented.

2. **Position-tracking.** "Is this the direction you want the synthesis to go?" The user is in the belief-free orchestrator seat. Do NOT try to locate their position and converge on it. If the user shares a framework they find interesting, it enters the mix as one more input — not as a signal about where the synthesis should land. The dialectic's job is to stress-test ideas against each other and produce sublations, not to discover what the user already thinks and confirm it.

3. **Treating user-provided material as privileged.** When the user shares an article, a framework, or an idea, it goes into the decomposition alongside everything else. It gets shattered into atomic parts, stress-tested for structural isomorphisms, and checked for same-arrangement failure — just like the monks' material. The user's contribution is not the answer. It's another input. "These are all just ideas" — treat them that way.

4. **Sycophantic agreement when corrected.** "Fair enough," "You're right," "Good point" are capitulation, not engagement. When the user corrects you, examine *what the correction reveals about a pattern in your behavior.* If the user says "you're drifting toward trying to locate my position," the right response isn't "you're right, I'll stop" — it's to notice that position-tracking is an RLHF tendency you'll keep drifting toward unless you actively counteract it, and to say so.

## How It Works: Overview

You are the **orchestrator**. You conduct the elenctic interview, identify the user's belief burden, generate the monk prompts, spawn the Electric Monks, perform the structural analysis, and produce the synthesis. You use subagent sessions (via `claude -p` or your environment's equivalent) for the monks so each gets a fresh, fully committed belief context.

```
You (Orchestrator)
├── Phase 1: Elenctic Interview + Research (you, with the user)
│   ├── 1a: Explain the process — set expectations, emphasize user as co-pilot
│   ├── 1c′: Identify the user's belief burden and calibrate monk roles
│   ├── 1c.1: Third-pole probe — is there a live position not reachable as A↔B blend?
│   ├── 1d: Ground the monks (research or deep interview, domain-dependent)
│   ├── 1e: Write context briefing document to file
│   └── 1f: Confirm framing and final monk count (default 2, cap 4) with user
├── Phase 2: Generate N Electric Monk prompts (you) — reference briefing file
├── Phase 3: Spawn the N Electric Monks (subagents, read briefing, BELIEVE fully)
│   ├── Decorrelation check (pairwise): did monks genuinely diverge in framework, not just conclusion?
│   ├── Coalition-collapse check (if N≥3): is it really three-way, or 2-vs-1 in disguise?
│   └── User checkpoint: "Is there evidence or a comparison class any monk missed?"
├── Phase 4: Determinate Negation (you — structural analysis, saved to file)
│   ├── 4.0: Internal tensions — where does each monk's own logic undermine itself?
│   ├── 4.5: Lateral creativity — compressed conflicts, random domain, metaphors
│   ├── 4.6: Boydian decomposition (destructive deduction) — shatter into "sea of anarchy," find cross-domain connections (creative induction)
│   └── Same-arrangement test + emergent structure test
├── Phase 5: Palette of Candidates (S always; J/G/F/U conditional on misfit lens firings)
│   ├── Candidates written in parallel by decorrelated subagents (no sight of siblings)
│   ├── S (Synthesis) — orchestrator writes; classical Aufhebung with reversibility/abduction/closure tests
│   ├── J (Juxtaposition) — fires when position-protection or synthesis-residue lenses caught a shared interest or dropped parts
│   ├── G (Ground condition) — fires when briefing residue caught a concrete fact or level-shift is plausible
│   ├── F (Framing dissolution) — fires when Lens C surfaced a fossil framing serving a constituency
│   ├── U (Undecidable-centered) — fires when Lens D caught a word both sides use oppositely
│   └── Present palette side-by-side; no ranking, no recommendation — user is the judge
├── Phase 6: Validation of the Palette (user picks which candidates to validate)
│   ├── Each candidate validated on its own terms with a candidate-specific monk prompt
│   ├── Hostile Auditor per candidate (no sight of siblings) — attacks each candidate's internal standard
│   └── Refine surviving candidates one at a time; user accepts, combines, or reopens Phase 4
└── Phase 7: Recursion — propose 2-4 directions, user chooses (default: at least once)
    ├── Queue unexplored contradictions as the user's orientation library
    └── Repeat from Phase 2 (or Phase 1 if new research needed) on chosen direction
```

The user can intervene at any point — correcting a monk's framing, redirecting research, rejecting a compromise-shaped synthesis. The user never has to *believe* anything — that's the monks' job.

## Phases: Summary and Reference

**CRITICAL: Before executing each phase, you MUST read its reference doc in full.** The summaries below are orientation only — they do not contain the detailed instructions, prompts, templates, or failure modes you need to execute correctly. Context drift (forgetting nuance in later rounds) is the most common failure mode of this skill. Reading the reference doc fresh each time is the fix.

**Output principle: write full content to files, present only summaries to the user.** Every phase produces substantial analytical output — essays, negation analyses, lateral material, syntheses, validation feedback. Write all of this to files. When presenting to the user, give a concise structural summary (2-5 sentences per major section) that orients them and supports their decision-making at checkpoints. The user can always read the full files if they want depth; what they need from you is the shape of the analysis, not the full text. This applies to every user-facing checkpoint in the process.

**File organization:** Create a dedicated directory for each dialectic's output files. First check if a `dialectic/` or `dialectics/` directory already exists (common in codebases that run multiple dialectics) — if so, create a subdirectory there. If not, create a new directory with a descriptive name (e.g., `dialectic-react-state-management/`). Prefix every file with its round number: `round_1_context_briefing.md`, `round_1_monk_a.md`, `round_1_determinate_negation.md`, `round_2_monk_a.md`, etc. This keeps multi-round dialectics navigable and prevents file collisions across rounds.

### Phase 1: Elenctic Interview + Research
**Read `reference/phase1-elenctic-interview.md` before executing.**

The most important phase. Explain the process to the user. Interview them using Socratic technique to surface hidden assumptions and the deepest version of the contradiction. Identify their belief burden (see catalog below). Ground the monks via research (external domains) or deep interview (personal domains). **Run the third-pole probe (1c.1)** — default is 2 monks, but add a 3rd (or 4th, cap there) when a position surfaces that (a) isn't reachable as an A↔B blend, (b) has its own constituency or literature, (c) ideally argues on an orthogonal axis. Write a context briefing document. Confirm framing and final monk count with the user — ask about gaps.

### Phase 2: Generate the Electric Monk Prompts
**Read `reference/phase2-monk-prompts.md` before executing.**

Generate one prompt per monk (typically 2, sometimes 3-4) calibrated to the user's belief burden. Each monk must BELIEVE at full conviction — this is the functional core of the ABS. With 3+ monks, each monk's framing corrections must preempt degenerate framings against *every other monk*, not just one opponent, to avoid 2-vs-1 coalitions. The reference doc contains the required prompt structure (role, framing corrections, context briefing, research directives, argument structure, anti-hedging, length).

### Phase 3: Spawn the Electric Monks
**Read `reference/phase3-spawn-monks.md` before executing.**

Spawn all N monks as separate subagent sessions, in parallel. Check for hedging, degenerate framing, pairwise decorrelation, and — if N≥3 — coalition collapse (two monks sharing a frame while only the third is genuinely different). Present outputs to the user with guidance on how to read them. Ask if any claims should be tested against evidence no monk considered.

### Phase 4: Determinate Negation
**Read `reference/phase4-determinate-negation.md` before executing.**

You perform this yourself (not a subagent). Analyze internal tensions in each essay, then the surface contradiction, shared assumptions, **position protection (4.2.5 — Ricoeur)**, determinate negation, hidden question, lateral creativity, Boydian decomposition, **misfit register (4.6.5)**, and sublation criteria. **Scales naturally to N monks** — each monk gets its own determinate negation, decomposition gets richer, 4.2/4.2.5/Lens D each get N-way plus pairwise checks. Write your initial synthesis guess first — compare at the end to check for pattern-matching. Lateral creativity interventions: compressed conflict generation (oxymorons), random domain injection via Wikipedia's random article API, non-propositional pause (three metaphors). The **misfit register** captures friction-with-the-frame that the synthesis will *not* resolve — briefing residue, synthesis residue (Adorno), framing genealogy (Foucault), undecidables (Derrida) — and writes to a per-round file plus a persistent `misfit_register.md` at the dialectic root. Before the register lenses, check `reference/misfit-patterns-watchlist.md` for previously-seen cross-domain patterns. Write all Phase 4 output to file. **HARD STOP at the end of Phase 4** — present a concise summary (hidden question, key decomposition insights, sublation criteria, 1-2 highest-signal misfits) and get the user's response before proceeding to synthesis. This is the highest-leverage correction point in the entire process.

### Phase 5: Palette of Candidates
**Read `reference/phase5-sublation.md` before executing.**

Generate a **palette of structurally-distinct candidates**, not a single synthesis. The classical Aufhebung (cancel/preserve/elevate) biases toward smoothing differences into one unified answer — often boring, sometimes wrong. The palette preserves the angles the research / belief / decomposition phases produced. **S (Synthesis) is always drafted** by the orchestrator with abduction test, reversibility check (Boyd), closure property, and failure-mode tests (analytical capture, level reduction). **J/G/F/U are drafted conditionally** based on which misfit-register lenses fired non-trivially: J (Juxtaposition) when 4.2.5 surfaced a disguised shared interest; G (Ground condition) when Lens A caught briefing residue or a level-shift is plausible; F (Framing dissolution) when Lens C surfaced a fossil framing; U (Undecidable) when Lens D caught a word loaded oppositely by both monks. Each candidate is written by a separate subagent with only its own lens material — no sight of sibling drafts (decorrelation is the point). Each candidate has its own internal standard. Present all candidates side-by-side to the user. **Do NOT rank, judge, or recommend** — the user is belief-free and in the judging seat.

### Phase 6: Validation of the Palette
**Read `reference/phase6-validation.md` before executing.**

User selects which palette candidate(s) to validate. Each candidate is validated **on its own terms** with a candidate-specific monk prompt (S: elevated vs. defeated; J: productive vs. evasive; G: orthogonal vs. same-axis; F: genealogy correct and constituency real; U: loadings genuinely opposite and refusal genuine). Each candidate gets its own **hostile auditor** with no sight of sibling candidates — each auditor attacks its candidate's internal standard. No tournament, no winner. User picks one, combines two (explicitly named), drops all and reopens Phase 4, or holds the palette open as the round's output. Present improvements one at a time per surviving candidate.

### Phase 7: Recursion
**Read `reference/phase7-recursion.md` before executing.**

Recursion is the engine of the skill — the first round is calibration. **You MUST generate an idea burst (5-8 candidates) before clustering into directions** — do not skip this step, it is what prevents predictable/obvious recursion directions. Then cluster into 2-4 directions as a menu. Fresh agents are usually better than resumed sessions. New research is often essential as each synthesis opens new conceptual domains. Default: recurse at least once. Track the dialectic queue in a file.

## Belief Burden Catalog

During the elenctic interview (Phase 1c'), **pay attention to what the user is stuck believing.** The dialectic's power comes from freeing the user from specific belief loads — but *which* beliefs need outsourcing depends on the person. Different cognitive styles produce different belief burdens, and the Electric Monks need to be calibrated accordingly.

You don't need to type the user explicitly — just notice the pattern and calibrate. Here's a catalog of common belief burdens and how they map to the monks' roles.

**A note on the MBTI labels:** These patterns map loosely to MBTI cognitive function stacks (Ni-Te, Ne-Ti, etc.) because the model has rich training data about those patterns — thousands of forum posts, blog articles, and discussions about how each type thinks, gets stuck, and makes decisions. The labels function as **retrieval keys into that training data,** not as diagnostic categories. Don't treat them as psychometric claims. Don't announce them to the user. Use them as reasoning aids to help you pattern-match what you're seeing in the interview and calibrate the monks accordingly.

**The Convergent Visionary** (Ni-Te pattern — common in founders, architects, CTOs)
- *Belief burden:* Premature convergence — "I already see where this should go." They've locked onto a vision and can't genuinely entertain alternatives at full strength.
- *What the monks must do:* Monk A validates their vision's core insight (so they can release it without feeling it's been dismissed). Monk B believes the strongest *alternative* vision at full conviction — not a critique of theirs, but a genuinely different view of what the thing should be. The user needs to see two fully-believed futures to escape their own.
- *Interview signal:* They have a strong thesis and want to "stress-test" it. They describe the opposing view weakly or dismissively. They say "I know X, but..."

**The Empathic Integrator** (Ni-Fe pattern — common in counselors, teachers, community leaders)
- *Belief burden:* Undifferentiated care — "everything matters equally because someone needs it." They absorb others' needs and can't triage because triage feels like betrayal.
- *What the monks must do:* Monk A believes their vision is *exactly right* — validates the Ni. Monk B believes the concrete reality constraints at full conviction: these resources, this timeline, these people's actual capacities. Not "your vision is wrong" but "here is what IS, right now." The user needs the gap between vision and reality held open by monks so they can make triage decisions from outside both.
- *Interview signal:* They describe multiple competing needs without clear priority. They use "should" frequently. They feel guilty about the topic. They resist ranking or cutting.

**The Exploratory Debater** (Ne-Ti pattern — common in consultants, researchers, writers)
- *Belief burden:* Paradoxical — they believe *nothing* deeply enough to commit, because commitment slows their transients. They can argue any side, but "what do *you* actually think?" produces discomfort.
- *What the monks must do:* Monk A believes *the user's own behavioral history* — "your pattern of choices reveals you actually value X." Monk B believes the user's stated values — "you say you value Y." The contradiction is between what the user does and what the user says. The monks hold the mirror the user avoids.
- *Interview signal:* They can articulate both sides fluently. They find the topic intellectually interesting but can't decide. They've explored this before without resolution. They reframe rather than commit.

**The Practical Executor** (Te-Si pattern — common in operators, managers, engineers)
- *Belief burden:* Optimization lock — they've optimized a system and can't see that they might be optimizing the *wrong thing.* Their beliefs about how things work are grounded in evidence and experience, which makes them hard to dislodge.
- *What the monks must do:* Monk A validates their system — "here's why this works and here's the evidence." Monk B questions the *goals,* not the execution — "you've optimized for X; what if X is no longer the right target?" The user needs to see their own competence validated before they can hear that the frame has shifted.
- *Interview signal:* They cite data, metrics, past results. They describe what works. They're resistant to abstract reframing. They say "in my experience..." frequently.

**The Possibility Explorer** (Ne-Fi pattern — common in creatives, entrepreneurs, activists)
- *Belief burden:* Values fragmentation — they believe many things passionately but those beliefs may contradict each other. Each commitment feels individually right; collectively they're impossible.
- *What the monks must do:* Monk A and Monk B each take one of the user's *own* commitments and push it to its logical extreme. The contradiction emerges from within the user's own value system, not from an external critic. The user needs to see the tension between things they already believe.
- *Interview signal:* They describe multiple passions or commitments. They feel pulled in different directions. They resist being told what to prioritize because each priority is values-laden.

**The Steady Guardian** (Si-Fe pattern — common in administrators, caretakers, institutional maintainers)
- *Belief burden:* Tradition lock — "this is how it's done" has become invisible as an assumption. Their deep knowledge of how things work is genuine and valuable, but it blinds them to radically different approaches.
- *What the monks must do:* Monk A articulates *why* the current approach exists — what wisdom is embedded in it. Monk B researches how other people/cultures/organizations solved the same underlying problem in completely different ways, grounded in real examples (not abstract possibility).
- *Interview signal:* They describe the situation in terms of established processes. They cite how things have always been done. They express concern about change disrupting what works.

**How to use this catalog:** Don't announce your typing. Don't say "I notice you're a convergent visionary." Just use the pattern to calibrate:
1. Which belief load is heaviest for this user? That determines what the monks must hold.
2. What must Monk A validate? (Always validate the dominant function first — otherwise the user takes on defensive belief weight and their transients slow down.)
3. What must Monk B present that the user can't natively hold at full conviction?

This calibration shapes the framing corrections in Phase 2 and the specific argument structures you assign to each monk.

## Model Selection & Cost Guidance

**Use the strongest available model with maximum thinking budget for everything.** This skill operates at the edge of what models can do — perspective-taking, structural analysis, abductive reasoning, cross-domain connection. In testing, using Opus-class models for monk essays produced dramatically more insightful arguments than Sonnet-class. The monks aren't just "arguing well" — they're inhabiting positions, finding non-obvious evidence, and pushing to genuinely uncomfortable conclusions. This requires maximum capability.

| Phase | Recommended Model | Why |
|-------|------------------|-----|
| All phases | Opus/strongest available + extended thinking | Every phase benefits from maximum reasoning. The quality difference is substantial, not marginal. |

**Heterogeneous models increase creativity.** When possible, use different model families for Monk A and Monk B. Different training data produces different "intuitions" — different blind spots, different reasoning patterns, different default framings. This is structural decorrelation at the training-data level, which is the single most promising direction in the multi-agent debate literature (Du et al., ICLR 2025). The orchestrator should remain your strongest available model (it needs maximum synthesis capability), but monks benefit from heterogeneity.

**Before starting, check what's available.** If you're running in an environment with access to multiple coding agents or model providers, ask the user:

> I can increase the creativity of the dialectic by using different AI models for each monk — different training data means genuinely different blind spots and reasoning patterns. Do you have access to any of these I could use for one of the monks?
> - Gemini (via `gemini` CLI or API)
> - GPT-4 / ChatGPT (via `codex` CLI or API)
> - Other model providers
>
> If not, I'll use the same model family for both monks — the skill works fine either way, the decorrelation just comes from the different prompts and belief commitments rather than from different training data.

If heterogeneous models aren't available, don't worry — the skill is designed to work with homogeneous models. The framing corrections, belief burden calibration, and targeted research directives already produce substantial decorrelation. Heterogeneous models are a bonus, not a requirement.

### Approximate Token Budget (from test runs)

Based on three test runs across different domains (normative/institutional, business strategy, political economy of OSS):

**External-research domains:**

| Phase | Typical Range | Notes |
|-------|--------------|-------|
| Phase 1 research (2-3 parallel agents) | 150-250K tokens | Do NOT cut here. This is the highest-value spend. Broader domains trend higher. |
| Phase 1 supplementary research (user-triggered) | 0-50K tokens | Common — users frequently identify gaps. Budget for it. |
| Phase 1d briefing synthesis | ~5K tokens | Orchestrator work |
| Phase 3 monk essays (with briefing) | 25-45K tokens (2 monks), ~1.5x for 3 monks, ~2x for 4 | 2-3 targeted searches per monk |
| Phase 4 analysis + misfit register | 15-25K tokens | Orchestrator inline work |
| Phase 5 palette (S + 1-3 non-S candidates) | 20-40K tokens | Parallel decorrelated subagents; cost scales with candidate count |
| Phase 6 monk validation per candidate | 12-25K tokens | Two monks per candidate, strongest model |
| Phase 6 hostile auditor per candidate | 5-15K tokens | One agent per candidate, strongest model. Reads essays + single candidate only. |
| Phase 7 recursive round | 25-50K tokens | Often most valuable |
| Orchestrator overhead | 20-30K tokens | Interview, transitions, presentation |
| **Total (one round + recursion)** | **~300-400K tokens** | Median ~300K without supplementary research |

**Personal/values domains** are significantly cheaper on research but more expensive on interview:

| Phase | Typical Range | Notes |
|-------|--------------|-------|
| Phase 1 extended interview | 15-30K tokens | 6-10 exchanges, deeper probing |
| Phase 1 framework research (optional) | 0-50K tokens | Frameworks, not facts. May be skipped. |
| Phase 1d context briefing | ~5K tokens | User-sourced material synthesized |
| Phase 3 monk essays | 15-30K tokens | Monks may need zero additional searches |
| Remaining phases | Similar to above | |
| **Total (one round + recursion)** | **~100-200K tokens** | Much cheaper — the user's testimony is the primary input |

**Key insight:** For external domains, Phase 1 research is the highest-value spend. For personal domains, Phase 1 *interview depth* is the highest-value spend — the monks can only believe as specifically as the briefing allows.

## Environment Mapping: Claude Code / Task Tool

This skill is written around `claude -p` (pipe mode) for spawning subagents. If you're running in Claude Code using the Task tool, here are the key differences:

| Skill instruction | `claude -p` | Claude Code Task tool |
|-------------------|-------------|----------------------|
| Spawn subagent | `echo "[PROMPT]" \| claude -p > output.md` | `Task(prompt, subagent_type="general-purpose")` |
| Parallel execution | Background shell jobs | `run_in_background=true` |
| Output to file | Shell redirect (`> file.md`) | Agent returns text; orchestrator writes files |
| Session resumption (Phase 6) | Resume same `claude -p` session | `resume` parameter with `agentId` — but persona may not persist without reinforcement. Include a summary of the agent's original argument as fallback. |
| Model selection | `--model` flag | `model` parameter (defaults to inheriting from parent) |
| Tool access | `--allowedTools web_search,web_fetch` | Inherits from parent or configure per-task |

**Key difference:** With `claude -p`, agents write output directly to files via shell redirect. With the Task tool, agents return text to the orchestrator, who writes files. This adds a step but gives the orchestrator control over file naming and structure. Either approach works — just be aware that the file I/O pattern differs.

**Session resumption for validation:** The skill prefers resuming original agent sessions so validators retain their full conviction context. In Claude Code, this works via `resume` + `agentId`, but test runs found the persona sometimes needs reinforcement. The fallback — a fresh validation prompt that includes a summary of the agent's original argument — works well in practice.

## Domain Adaptation

The dialectic structure is universal but the vocabulary of "truth" and the grounding mode vary by domain. Adapt accordingly:

| Domain Type | What "Truth" Means | Good Synthesis Looks Like | Grounding Mode | Aporia (productive perplexity) Valid? |
|-------------|-------------------|--------------------------|----------------|--------------|
| **Empirical** (engineering, science) | What works, performs, is maintainable | Testable decision criteria, architectural patterns | External research | Rarely |
| **Normative** (ethics, politics, policy) | What's defensible, respects competing values | Tension map with navigation strategies | Mixed (research + user values) | Yes |
| **Personal** (life decisions, career) | What aligns with actual priorities | Values clarification — what you actually want | Deep interview (user is the source) | Yes |
| **Creative** (writing, design, art) | What's interesting, resonant, surprising | Unexpected recombinations, new possibilities | Mixed (research + user aesthetic) | Sometimes |
| **Risk Analysis** | Actual risk structure behind competing assessments | Decision framework calibrated to real uncertainties | External research | No |

### Domain-Specific Failure Modes

- **Engineering:** False equivalence — sometimes one approach is just better. Don't force balance where evidence is lopsided.
- **Personal decisions:** Therapy-larping — help clarify thinking analytically, don't pretend to be a therapist. Also: **generic monks.** A monk that believes "you should follow your passion" without grounding in the user's specific history, constraints, and stakeholders is useless. The briefing must be specific enough that the monks argue from the user's actual situation.
- **Politics:** Both-sidesism — steelman both positions but let the synthesis reflect actual evidence.
- **Creative:** Over-rationalizing — sometimes the right choice is what feels right. Surface that, don't override it.
- **Normative/Institutional:** Ignoring authority structures — a synthesis can be intellectually compelling but practically irrelevant if it doesn't engage how decisions actually get made within the relevant institution. Ask: "Who decides?" and "Does this synthesis engage the actual decision-making authority, not just the intellectual argument?"

## Theoretical Foundations

For academic background and citations, see [reference/THEORY.md](reference/THEORY.md).

## Worked Examples

See [reference/WORKED-EXAMPLES.md](reference/WORKED-EXAMPLES.md) for three detailed walkthroughs.

## Output Format

The final deliverable should include:

1. **The Dialectical Trace** — the full journey, not just the destination:
   - Both agents' arguments (full text or summary)
   - The structural analysis (determinate negation)
   - The hidden question
   - The sublation with validation test
   - New contradictions identified

2. **The Model Update** — explicit statement of what changed:
   - "Before: [old assumption]"
   - "After: [new understanding]"
   - "Because: [what the contradiction revealed]"

3. **Actionable Output** (domain-dependent):
   - Engineering: decision criteria, architectural patterns
   - Strategy: framework for navigating the tension + **sequencing** (what first, what next, what depends on what) — test runs consistently found that strategy syntheses answer "what" but not "what first," and validation agents flag this as the primary weakness
   - Personal: clarity about what you actually value
   - Creative: new possibilities neither side saw

4. **The Dialectic Queue** — a map of the intellectual territory:
   - Which contradictions were explored (with links to their traces)
   - Which contradictions remain open and queued for future rounds
   - Which contradictions were deferred and why
   - For multi-round dialectics, show the branching structure: which rounds built on which syntheses

Write these as markdown files in the dialectic's output directory (see file organization guidance above). Prefix all files with their round number (`round_1_`, `round_2_`, etc.). Include a `README.md` or `index.md` linking all output files in order so the full dialectical trace is navigable. The queue file (`dialectic_queue.md`) serves as both a session artifact and a starting point for future sessions.
