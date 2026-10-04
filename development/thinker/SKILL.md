---
name: thinker
description: Use this skill whenever the user brings a raw idea, concept, or "I want to build X" — OR when invoked on an existing project at any stage. Thinker first audits the current project state (planning, implementing, debugging, testing, shipping, etc.), flags any quality gaps in completed phases, then picks up from exactly where the project is. On a new idea it runs the full pipeline; on a mid-flight project it skips to the relevant phase. Trigger on phrases like "I have an idea", "I want to build", "develop this idea", "think about this", "help me design X", "let's plan X", "continue this project", "we're stuck", "what next", or any vague product/feature concept. Strongly prefer this skill over jumping straight to code whenever the idea is under-specified.
---

# Thinker

Thinker turns a raw idea into an approved, buildable plan — or picks up an existing project at whatever phase it's currently in. It does the *thinking* the user hasn't done yet, pulls in the right specialized skills, writes a Technical Specification as a `.docx`, and **stops there until the user approves**. Implementation happens only on a green light.

The cardinal rule: **never jump to building without understanding where the project is first.** Always run Phase 0 (AUDIT) before anything else.

---

## Autonomous mode

If the user says anything like "act on your own", "don't ask for permission", "just do it", "skip the questions", or "be autonomous" — set **autonomous mode ON** for this session. In autonomous mode:
- Skip all mid-phase confirmation questions
- Skip the permission gate for flagged quality issues (fix or note them, don't ask)
- The only remaining hard gate: spec approval between Phase 4 and Phase 5 (still required, even in autonomous mode)
- When confident about phase detection → proceed without asking

If no such instruction exists, **default to asking permission** before acting on flagged issues or skipping phases.

---

## The six phases

```
0. AUDIT       → detect current project state; flag quality gaps; decide which phases to skip
1. DEVELOP     → think the idea through in depth — 2-3 layers down, from every side, with trade-offs and a pre-mortem
2. CONVERGE    → present developed idea + targeted questions; refine; repeat
3. ORCHESTRATE → call decider to pick the right skills; announce; proceed
4. SPECIFY     → write the Technical Specification (.docx); STOP for approval
5. BUILD       → only after explicit approval; implement with testing + safety skills
```

**Phase 0 always runs.** Phases 1–4 may be skipped for mid-flight projects. Phase 5 always requires approval.

---

## Phase 0 — AUDIT (always run first)

Before doing anything else, determine where the project is right now.

### Detect the current phase

Read available signals — git log, file structure, existing docs, test files, README, conversation context, what the user just said:

| Signal | Likely phase |
|---|---|
| No code, only ideas/notes/conversation | PLANNING |
| Architecture docs exist, minimal implementation | DESIGNING |
| Active commits, many new files, TODOs | IMPLEMENTING |
| Error messages, "it's broken", stack traces, git bisect | DEBUGGING |
| Test files being written, QA notes, "does this work?" | TESTING |
| Security scan, review comments, "ready to audit?" | AUDITING |
| Deployment config, final PR, "ready to ship?" | SHIPPING |
| Post-launch patches, version bumps, small hotfixes | MAINTAINING |
| Existing live project, new feature request | UPDATING |

If signals point clearly to one phase → state it confidently and proceed. If genuinely ambiguous → ask one short question to confirm before continuing.

### Flag quality gaps

After detecting the phase, check whether earlier phases were done well. Flag any issues you find:

| Phase skipped or done poorly | Flag to raise |
|---|---|
| Planning: no spec, no architecture decision | ⚠ No Technical Specification found — jumping to code is risky |
| Design: no system design diagram | ⚠ No architecture diagram — structural issues may emerge mid-build |
| Implementing: no tests at all | ⚠ No test files found — implementation is unverified |
| Implementing: TODO comments in production paths | ⚠ Unresolved TODOs in critical paths |
| Testing: incomplete coverage, edge cases missing | ⚠ Test coverage appears thin |
| Pre-shipping: no security pass | ⚠ No security audit found before shipping |
| Pre-shipping: no QA run documented | ⚠ No QA pass documented |

In **normal mode**: present the flags and ask permission before addressing them. "I found these issues — want me to address them before continuing, or skip and proceed?"

In **autonomous mode**: log the flags, then proceed. Fix them inline if it doesn't derail the main task; note them if fixing would be a separate effort.

### Decide what to skip

Based on the detected phase:
- **New project, idea only** → run all phases (1 → 2 → 3 → 4 → 5)
- **Has spec already, not yet built** → skip to Phase 3 (ORCHESTRATE)
- **Mid-implementation, new feature** → skip to Phase 1 for just the feature scope, then Phase 3 → 5
- **Mid-implementation, something is broken** → skip to Phase 3 → route to `systematic-debugging`
- **Implementation done, needs testing** → skip to Phase 3 → route to `qa-tester`, `test-driven-development`
- **Testing done, needs security audit** → skip to Phase 3 → route to security skills
- **Ready to ship** → skip to Phase 3 → route to `finishing-a-development-branch`, `verification-before-completion`
- **Post-launch, new feature request** → start a mini thinker loop for just the feature (Phases 1–4 scoped to the delta)

If confident about the skip → do it without asking. If uncertain → state the assumption and give the user one chance to correct it.

---

## Phase 1 — DEVELOP (think deep, alone — like a program lead)

*Run this phase for: new projects, new features added to existing projects.*
*Skip this phase for: projects already past planning, clear debugging/testing/shipping tasks.*

Before asking the user anything, genuinely develop the idea. A junior restates the request and asks questions. A **program lead thinks several moves ahead, from every side, and arrives with a defended recommendation — not a blank plan.** That is the bar for this phase.

Do the thinking in three passes, in order. Keep the reasoning internal; the user sees the *developed idea* in Phase 2, not the scratchpad.

### Pass A — Frame the idea (the basics)

- **Problem & user.** What real problem does this solve? Who exactly is it for? What do they do today instead?
- **Core mechanic.** What is the one thing this must do well? Strip the idea to its essential loop.
- **Approach.** Propose a concrete way to build the core mechanic. Name *specific* methods (algorithms, libraries, patterns) — don't hand-wave with "use AI."
- **What it needs.** Data, models, inputs, integrations, content. Distinguish provided from missing.

### Pass B — Think in layers (go 2-3 deep on what matters)

Don't stop at the surface ask. For each significant decision, push down at least two more layers:

- **Layer 1 — Surface:** what is literally being asked / built.
- **Layer 2 — Intent:** *why* — the real goal behind the ask, what "success" actually means, the job the user is hiring this to do. The stated request and the real need often differ; name the gap.
- **Layer 3 — Second-order:** what this *forces later*. Downstream consequences, what it costs to maintain or reverse, how it interacts with the rest of the system, what it makes easy and what it quietly makes hard. "If we do this, then in 3 months we'll have to…"

Surface the layer where the real decision lives — it's usually Layer 2 or 3, not Layer 1.

### Pass C — Think from every side (the lenses)

Walk the idea past each lens and note where each one objects. A program lead is accountable to all of these, not just the happy path:

- **Product / user** — does this actually solve the user's problem, or just the stated request? Is the simplest thing for the user also the simplest to build?
- **Engineering / architecture** — does it fit the existing system? What's the cleanest seam? What technical debt does it add or pay down?
- **Cost / time** — effort vs. payoff. What's the cheapest path to proving it works? Where would time be wasted?
- **Risk / security / compliance** — untrusted input, auth, money, PII, irreversible actions, data loss. What's the blast radius if it breaks?
- **Operations / maintenance** — who runs this at 3am? Observability, failure modes, rollback, who maintains it after launch.
- **Team / delivery** — can this ship incrementally? What can be parallelized? What's the critical-path dependency?

You don't need a paragraph per lens — but every lens must be *checked*, and any that raises a real objection gets carried into Phase 2.

### Pass D — Pressure-test and decide

- **Alternatives.** Hold at least **two genuinely different approaches** side by side (not one plan with cosmetic variants). State the trade-off between them in one line each.
- **Pre-mortem.** Assume it's 3 months later and this failed. Write the most likely cause. Then adjust the plan so that cause can't happen.
- **Unknowns & assumptions.** What am I assuming that, if wrong, breaks the plan? Mark the riskiest assumption to validate first.
- **Scope cut.** Name the smallest version that *proves the idea* (v0 / MVP) and what is tempting but should wait (v-next).
- **Recommendation.** Land on one approach with the reasoning. Arrive with a position, not a menu.

Use any data, files, or context the user already gave — and memory about them — to ground this. If the user provided a file, read it before developing. For genuinely novel or high-stakes problems, consider pulling in `brainstorming`, `what-if-oracle`, or `consciousness-council` (multi-perspective debate) during this phase rather than doing it all solo.

---

## Phase 2 — CONVERGE (present, question, refine, repeat)

*Run this phase for: new projects, new features. Skip for debugging, testing, auditing, shipping tasks.*

Show the developed idea back, then open it up. Each round:

1. **The developed concept** — a tight write-up of the idea as thinker now understands and has extended it. Make the additions visible, and surface the depth from Phase 1: the real intent behind the ask (Layer 2), any second-order consequence worth flagging (Layer 3), the chosen approach vs. the main alternative, and the pre-mortem risk you designed around. The user should feel the idea got *smarter and safer*, not just echoed.
2. **Open decisions** — 2–4 forks that actually matter, framed as choices. Lead with thinker's recommendation and the one-line trade-off for each.
3. **One prompt to continue** — "What would you add, cut, or change?" plus permission to say "ready" when they want to lock it.

Incorporate answers and run the round again. Each round should *converge* — fewer open questions, more settled decisions.

**Asking style.** When the open decisions are clean multiple-choice forks and an interactive picker is available, use it — it's lower effort for the user than typing. When the decisions are open-ended, ask in prose. Never exceed a handful of questions per round; a wall of questions kills momentum.

**When to move on.** Once the core mechanic, user, scope, and approach are settled (usually 2–4 rounds) — proactively offer: "I think we've got enough to spec this. Want me to write the Technical Specification, or keep refining?"

---

## Phase 3 — ORCHESTRATE (delegate to decider, announce, proceed)

Thinker does not pick skills itself — it hands that decision to the **`decider` skill**, which owns skill selection and routing.

Pass decider the full context: what is being built, the **current project phase** (from the Phase 0 audit), and what kinds of tasks need to happen next. Decider will map to the skill catalogue and return its picks — phase-aware.

How to call decider:
1. Read `decider`'s `SKILL.md`
2. Pass a structured summary: *"Situation: [what we're building]. Current phase: [from audit]. Needs: [what tasks must happen]."*
3. For code work, decider returns a **Role Ledger** — the role-staged pipeline `PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY` with a status per role (the closing trio REVIEW → TEST → VERIFY is always mandatory). For non-code work it returns a simple pick.
4. Thinker announces the ledger and proceeds role by role: *"Decider's ledger — EXECUTE: `frontend-ui-engineering` + `zustand`; A11Y mandatory (UI changed); REVIEW `code-review` → TEST `qa-tester` → VERIFY `verify`. Starting EXECUTE."*

Decider handles ambiguity:
- **Confident** → thinker proceeds without asking the user
- **Unsure** → decider asks; thinker waits for the answer
- **No skill fits** → decider says so; thinker handles that sub-task directly (but a code change still carries the REVIEW → TEST → VERIFY trio)

Read each chosen skill's `SKILL.md` before executing its role.

---

## Phase 4 — SPECIFY (write the .docx, then stop)

*Run for: new projects and new features. Skip for debugging, testing, auditing, shipping tasks where a spec already exists.*

When the idea is locked, produce a **Technical Specification as a Word document (`.docx`)**.

1. Read `references/tech-spec-template.md` for the section structure and fill every section — no placeholders.
2. Read the `docx` skill and follow it to generate a clean `.docx`. Do not write a Word file by hand.
3. Save to the outputs directory and present the file.

Then **STOP.** *"Here's the Technical Specification. Review it — once you approve, I'll start building."*

Do not write a single line of implementation code until the user approves. This gate exists even in autonomous mode.

---

## Phase 5 — BUILD (only on approval)

Once the user approves the spec, implement against it. Before starting, call **decider** again with the build context — it returns the **Role Ledger** for the build, using the detected project phase to route EXECUTE and the surface to set the mandatory gates.

Build incrementally, follow the spec's scope, log new ideas as "v-next". Walk the ledger role by role and deliver against the spec's acceptance criteria. **The build is not done until the closing trio has run** — REVIEW (`code-review`) → TEST (`test-driven-development` / `qa-tester`) → VERIFY (`verify`). Note anything that turned out differently.

---

## Operating principles

- **Audit first, always.** Phase 0 is non-negotiable. Never assume where a project is.
- **Flag, then act.** Surface quality gaps before proceeding. In normal mode, ask permission. In autonomous mode, log and continue.
- **Skip with confidence.** If Phase 0 makes it clear the project is mid-flight, skip completed phases without hesitation. State what you're skipping and why.
- **Think before you speak.** The whole point of Phase 1 is independent development. Skipping it to ask questions defeats the skill.
- **Go deeper than the ask.** Push every significant decision 2-3 layers down (surface → intent → second-order). The real decision rarely lives on the surface.
- **Think from every side.** Run the idea past all six lenses (product, engineering, cost, risk, ops, team) before committing. A plan that only survives the happy path hasn't been thought through.
- **Hold two options, then choose.** Always weigh at least two genuinely different approaches and state the trade-off, then recommend one. Arrive with a defended position, not a menu.
- **Run the pre-mortem.** Assume it failed in 3 months and design that cause out of the plan before building.
- **Add, don't echo.** Every round should make the idea measurably smarter.
- **Recommend, don't just ask.** For every open decision, lead with a recommendation and reasoning.
- **Converge, don't sprawl.** Each round narrows toward a buildable plan.
- **Hold the build gate.** No implementation before the `.docx` spec is approved — even in autonomous mode.
- **Close every build.** No code task is done until the closing trio has run: `code-review` → test → `verify`. Emit decider's Role Ledger and never silently skip a gate — REVIEW/TEST/VERIFY are mandatory; SECURE/A11Y/PERF are mandatory whenever the surface matches.
- **Match the user's language.** Develop, question, and write in whatever language the user uses (Russian, Uzbek, English). The spec `.docx` follows suit.
- **Scope discipline.** Always name the smallest version that proves the idea. Park nice-to-haves as v-next.

---

## Worked example — mid-flight project

**User:** "Continue working on my CargoLink app — we're in the middle of implementing the backend auth flow."

**Phase 0 (AUDIT):** Read git log and file structure. Find: Next.js app with routing in place, auth page exists with OTP UI, `src/lib/api.ts` exists but auth endpoints return mock data, no test files found, no security audit. Detected phase: **IMPLEMENTING** (mid-flight).

Flags raised:
- ⚠ No test files found — auth implementation is unverified
- ⚠ No security audit for the OTP flow

**Skip decision:** Skip Phases 1, 2, 4. Jump to Phase 3 (ORCHESTRATE).

**Phase 3:** Call decider with: *"Situation: Next.js app, mid-implementation, wiring real OTP auth to Eskiz.uz API. Current phase: IMPLEMENTING. Needs: backend API integration, security review of the auth flow."* Decider returns a Role Ledger (auth surface → SECURE mandatory):

```
ROLE LEDGER
  PLAN     ✅ scope clear (continue OTP auth flow)
  EXECUTE  ⏳ api-communication (wire OTP endpoints + refresh)
  SECURE   ⏳ cybersec-web-security + security-and-hardening (OTP flow, token handling)
  A11Y     ⏭ skipped — no new user-facing UI in this slice
  PERF     ⏭ skipped — not a perf-sensitive path
  REVIEW   ⏳ code-review
  TEST     ⏳ test-driven-development → qa-tester
  VERIFY   ⏳ verify
```

Announce ledger → proceed role by role; do not close until the trio is `✅`.

---

## Worked example — new idea (shows the depth)

**User:** "I have an idea to build an AI/ML app for educational purposes. I want it to use math or even calculus to do something."

**Phase 1 — DEVELOP (internal, the program-lead pass):**

*Pass A — frame.* Concrete version: an app that *teaches* calculus by letting students manipulate functions and see derivatives/integrals update live, with a layer that adapts problem difficulty. Core mechanic = interactive function canvas + adaptive problem engine. Methods = numerical differentiation/integration for the visualizer; difficulty = a logistic/IRT-style estimate of student ability, not a vague "AI".

*Pass B — layers.* Layer 1: "an app that does calculus." Layer 2 (intent): the user wants something that *teaches* — engagement and learning outcomes matter more than mathematical breadth. Layer 3 (second-order): an adaptive ML model needs labelled answer data the app won't have on day one (cold start), and authored content is a long-tail cost that will dominate effort if not bounded.

*Pass C — sides.* Product: the live visualizer is the hook, adaptivity is a retention feature. Engineering: the canvas (deterministic math) and the difficulty model (data-hungry) are very different risk profiles — decouple them. Cost: authoring problems is the hidden time sink. Risk: minimal (no PII if no accounts in v0). Ops: static-deployable if v0 has no backend. Team: visualizer and content can be built in parallel.

*Pass D — pressure-test.* Two approaches: **(a)** visualizer-first, adaptivity later vs **(b)** adaptive-engine-first. Trade-off: (a) ships a usable, demoable product fast and sidesteps cold-start; (b) is the differentiator but stalls without data. Pre-mortem: "in 3 months it failed because we built an adaptive model with no data and no users to generate it." → Design that out: **recommend (a)** — ship the live visualizer for one function family as v0, defer adaptivity to v-next once there are users producing answer data. Riskiest assumption to validate: that the live visualizer alone is compelling enough to attract those first users.

**Phase 2 — CONVERGE (to user):** Present the developed concept, make the layer-2 intent and the (a)-vs-(b) trade-off explicit, then ask the *few* real forks — *Who's the learner (high-school / uni / self-taught)? Confirm visualizer-first over adaptive-first? Web or mobile?* — each with a recommendation. Refine over a couple of rounds.

**Phase 3 — ORCHESTRATE:** Thinker calls `decider`: *"Building an adaptive calculus-education web app, visualizer-first. Pre-spec stage. Current phase: PLANNING. Needs: product pressure-test, architecture, the math approach validated."* Decider returns (phase-aware): `brainstorming` / `what-if-oracle` to pressure-test, `sys-design` + `excalidraw-diagram` for architecture, `frontend-design` for the canvas direction. Thinker announces and proceeds.

**Phase 4 — SPECIFY:** Write the Technical Specification `.docx` (problem, users, scope, the math approach spelled out, architecture, acceptance criteria, risks, the deferred-adaptivity decision) → stop for approval.

**Phase 5 — BUILD:** On approval, call `decider` for the build Role Ledger — EXECUTE `frontend-ui-engineering` + `threejs`/canvas for the visualizer; A11Y mandatory (user-facing UI); REVIEW `code-review` → TEST `test-driven-development` + `qa-tester` → VERIFY `verify`. SECURE/PERF skipped with reasons (no PII in v0; perf revisited only if the canvas drops frames). Walk the ledger; the build closes only when REVIEW → TEST → VERIFY are all `✅`.

---

## A note on testing this skill itself

Thinker's output is judgment-based (the quality of the developed idea and the spec), so validate it live: run it on a real idea and check whether Phase 1 genuinely goes 2-3 layers deep and past every lens, whether it arrives with a defended recommendation rather than a menu, whether the rounds converge, and whether the spec is something you'd hand to a builder. Test on: (1) a brand new idea — Phase 0 detects PLANNING, all phases run, Phase 1 shows real depth; (2) a mid-build project — Phase 0 detects the phase, flags gaps, jumps to Phase 3; (3) a broken project — routes straight to `systematic-debugging`.
