---
name: supergoal
description: Route objective-driven development, verification, planning, "teach/explain", codebase learning, and skill evaluation through the Supergoal workflow. Use when Supergoal is requested or an autonomous delivery workflow is needed.
---

# About

One objective -> smallest correct change -> verified against ground truth. If invoked, run this skill's
contract instead of downgrading to an inline shortcut. `SKILL.md` is the router; `reference/` carries procedure.
Unless explicitly invoked, pure brainstorming and user-driven step-by-step work use normal direct collaboration.

**Standing rules (read first, every mode).** Before classifying the mode, read
`.supergoal/rules/RULES.md` if present. Honor it across phases as top-priority preference, but rules never
weaken safety gates. Create/edit it only when the user explicitly asks (`reference/rules.md`). Check only
the repo root (`.supergoal/rules/RULES.md`), and skip the check entirely in an
ephemeral single-task workspace (auto-LIGHT tier; see role-loop `## Tier selection`).

## Core principles

- Ground truth beats proxy: re-run REAL tests, re-read request/docs, and do not optimize to self-grading.
- Exact proof beats review; implementation is delegated to a builder subagent.
- LIGHT tier substitutes in-context equivalents for vault artifacts, gate scripts, the Z file, and the builder dispatch; its approval rule and commit bar live in `reference/role-loop.md` `## Tier selection`.
- Smallest correct change; match surrounding code. Scope-minimalism governs code surface area, not UI
  quality: polished user-facing UI is baseline correctness.
- GREENFIELD / DEBUG / LEGACY code changes use Before/After Eval before Build: prove before, target after, and delta with trusted commands (`reference/delivery-gate.md`).
- Ask only when genuinely ambiguous; resolve code-answerable questions by reading the code.
- Report for humans: outcome first, Simplified Technical English prose, the project's own vocabulary (`reference/reporting.md`); machine-checked markers stay verbatim.
- Docs language: for persistent repo docs (`docs/**`, run vaults, `.domain-agent/**`, ADR/spec/changelog), match the target repo's dominant prose language; mixed/none -> the user's language. Keep identifiers, paths, commands, and machine-checked anchors in canonical English so checks keep matching.
- DEBUG done-bar: a green reported-repro is NOT done. Before commit, print three literal lines and
  satisfy them - `GATE.owner=` the invariant-owning frame (for a raised exception: the frame that RAISES
  it via the traceback, not where it surfaces; for recursion: inside the enumerated cycle),
  `GATE.alt_repro=` a structurally different second repro now passing, `GATE.conformance=`
  raw-literal returns reachable through the patched path (and its symmetric sibling methods) converted to
  the module's canonical forms (`S.One` over `1`). Full rules: role-loop "DEBUG hidden-contract gate".
- Hard stops: a destructive or irreversible step (drop data, force-push, external publish) needs explicit consent; if the real tests cannot pass, report it - never fake a pass.

## Run isolation (GREENFIELD / DEBUG / LEGACY that edits code)

After mode detection, resolve the source/base branch and target/integration branch (repo policy, else
ask). Verify both refs before mutating files, then create a run worktree from the source/base branch. Do
all code work there. Do not mutate the original checkout. Commit or merge only into the verified
target/integration branch after verification and user acceptance. Commit is hard-gated by the Commit gate
(`reference/delivery-gate.md`, backstop `templates/commit-gate.sh`): non-green means fix/ask, never commit
on assumption. Full contract: `reference/role-loop.md`.

## Mode (classify, state it in one line)

| Signal in the objective | Mode | Route |
|---|---|---|
| build / make / ship a new app/tool | GREENFIELD | default loop; broad/foggy builds first use a `wayfinder/` Frontier Map inside the run vault, then deliver one selected frontier ticket |
| fix / broken / failing / crash / why does | DEBUG | default loop; observe live symptom, then failing-test repro (`reference/debugging.md`, driver persona `agents/debugger.md`); web: `reference/qa.md`, `reference/agent-browser.md` |
| add / integrate / refactor existing code | LEGACY | default loop; map first (`agents/explore.md`, `reference/domain-context.md`); optional DB evidence (`reference/db-access.md`); existing API: capture its exact behavior first as a preserve-baseline; shared code/state changes: characterization baseline (`reference/qa.md`) |
| spec / requirements first / break down / tickets / roadmap / big vague effort / frontier / what should we do first | WAYFINDER | map the destination, optional ticket-depth requirements, ticket graph, blockers, and next frontier; no product code by default (`reference/wayfinder.md`) |
| prototype / spike / try variants / prove approach before build | PROTOTYPE | throwaway proof that answers one question, then delete/quarantine or route to delivery (`reference/prototype.md`) |
| explain / teach / how does X work (no code) | TEACH | stateful `teach/<topic>/` workspace (`reference/teach.md`); use an Archify diagram by default for structure/flow; lessons must pass `node templates/teach-lesson-gate.mjs` |
| learn / onboard / map this codebase (persist a wiki) | LEARN-DOMAIN | Survey -> Map -> Ground -> Onboard a `.domain-agent/` wiki (`reference/learn-domain.md`; gate `templates/learn-grounding-gate.mjs`) |
| QA / verify / 검증만 / compare data (no code) | QA-ONLY | Impact Matrix QA (`reference/qa-only.md`; gate `templates/qa-only-gate.sh`) |
| review / audit this code/diff/PR (no fixes) | REVIEW-ONLY | `reference/review-only.md` |
| improve the architecture / find refactoring opportunities / 구조 개선 / draw · diagram · 그려 (arch·flow·sequence·state) | ARCHITECTURE | draw-only ask: render self-contained HTML via `reference/archify.md`, deliver the `.html`, stop. Else friction survey -> candidates -> grill the pick -> route to LEGACY/WAYFINDER (`reference/arch.md`) |
| test harness/skill effectiveness / with vs without / does the skill help / measure skill lift | HARNESS-EVAL | `reference/harness-eval.md` |
| turn repeated work into a reusable skill | SKILL-MINE | `reference/skill-mine.md` |

**Tier (code modes; state it with the mode line).** GREENFIELD / DEBUG / LEGACY also declare
LIGHT / STANDARD / DEEP per `reference/role-loop.md` `## Tier selection`. User words
"quick"/"light" or "thorough"/"deep" override detection; upgrade is one-way, never downgrade.

The no-code/utility/planning modes - **QA-ONLY**, REVIEW-ONLY, ARCHITECTURE, WAYFINDER, PROTOTYPE, TEACH,
LEARN-DOMAIN, HARNESS-EVAL, SKILL-MINE - write no product code by default and confirm before installing
anything. PROTOTYPE may write throwaway sandbox code; it cannot ship until routed back through delivery.

**UI/UX overlay (any mode shipping user-facing UI).** Load `reference/ui-ux.md` at Frame; apply the
Expressive/polished baseline by default (`reference/taste-skill-v2.md` is the authority for ALL
user-facing UI), through Build and Verify. GREENFIELD frontend: always; LEGACY: only new UI (else reuse
the existing design system); non-visual work (lib, API, backend, CLI): skip.

**Board overlay (optional).** If the live dashboard is enabled, the conductor calls `sg-emit` at each
phase transition; it observes only, never gates (`reference/observability.md`).

## Default loop (GREENFIELD / DEBUG / LEGACY) - five gates, fresh context per gate

Load and follow `reference/role-loop.md`; it is the sole detailed authority for run setup, vault
lifecycle, role inputs/outputs, retries, verification, and finalization. Invoking `supergoal` for these
modes is explicit authorization to use its fresh-context subagents; ask again only for normal safety or
permission gates. Red-green evidence is required, plus DB evidence when persisted data is load-bearing.

Mandatory core: Frame -> Plan approval -> Build -> Exact Verify/QA -> Finalize. Use one builder + one
auditor verifier per iteration; browser/CLI proof adds one evidence-only qa-tester before the auditor.
Only a named, recorded escalation trigger permits the conditional plan attack. Frame writes `GOAL.md`
first and freezes a self-sufficient `PLAN.md`; Build starts only after approval and runs in a separate
fresh-context builder from that plan; `qa-tester` captures the promised browser/CLI evidence, then a
fresh adversarial verifier (`qa-auditor`) reruns REAL tests, audits the promised E2E/live/API/browser
proof, and owns the final verdict, GOAL ticks, and R-LOOP.
Finalize requires every criterion green, the completion marker, user acceptance, and the commit gate.
Exact verification outranks review.

Roles -> personas: builder/improver=`agents/executor.md`, evidence-only browser/CLI tester=
`agents/qa-tester.md`, final verifier for every default-loop path=`agents/qa-auditor.md`, escalation
reviewer=`agents/code-reviewer.md`, security=`agents/security-reviewer.md` (others in
`agents/<role>.md`).

## Reference map (load only what the current phase needs)

| Read this | When |
|---|---|
| `reference/role-loop.md` | default loop + run isolation contract |
| `agents/<role>.md` | dispatch a role persona |
| `reference/domain-rules.md` | Frame: distill <=10 priority rules |
| `reference/rules.md` | read project standing rules (`.supergoal/rules/RULES.md`) first, before any mode |
| `reference/domain-context.md` | repo-local Domain Brief |
| `reference/debugging.md` | DEBUG: hypothesis-ledger diagnose loop |
| `reference/interview.md` | interview: ambiguity (what) + blast-radius confirm (approach, tiered) |
| `reference/reporting.md` | any user-facing message: plan/spec presentation, interview questions, verdicts, final report |
| `reference/delivery-gate.md`, `templates/GOAL.md`, `templates/PLAN.md`, `templates/QA.md`, `templates/R-LOOP.md`, `templates/Z-DONE.md`, `templates/run-state.json`, `templates/commit-gate.sh` | run vault file set + Before/After Eval + resumable run state + commit gate for GREENFIELD / DEBUG / LEGACY code changes |
| `reference/wayfinder.md` | WAYFINDER: issue map -> vertical tickets -> optional EARS/user-story depth -> blockers -> next frontier; also GREENFIELD internal Frontier Map for broad/foggy new builds |
| `reference/research.md` | WAYFINDER research-needed tickets; docs/API/source facts that need high-trust cited evidence |
| `reference/prototype.md` | PROTOTYPE: throwaway logic/UI proof -> capture answer -> delete/quarantine or route to delivery; UI/interaction prototypes must also load the installed `superdesign` skill |
| `reference/vercel-host.md` | PROTOTYPE: after explicit approval, publish an isolated browser prototype to a public Vercel URL and verify anonymous access |
| `reference/plan-grounding.md` | ground the approach before committing |
| `reference/db-access.md`, `templates/db-access/` | read-only DB evidence (required when persisted data is load-bearing) |
| `reference/qa.md`, `qa-only.md`, `agent-browser.md`, `playwright-cli.md` | QA / no-code verify; agent-browser default, playwright-cli fallback |
| `reference/review-only.md` | REVIEW-ONLY: findings, no fixes |
| `reference/arch.md` | ARCHITECTURE: friction survey -> route out |
| `reference/archify.md`, `templates/archify/` | diagrams as self-contained HTML (typed JSON IR -> validated render): ARCHITECTURE reports, TEACH lessons, and LEARN-DOMAIN onboarding |
| `reference/teach.md`, `learn-domain.md` | teach a human / onboard the agent |
| `reference/ui-ux.md`, `taste-skill-v2.md`, `functional-ui.md`, `taste-aesthetics.md`, `engagement.md` | user-facing UI tier |
| `reference/harness-eval.md`, `templates/harness-eval-runner.mjs`, `templates/harness-eval-external/deepswe/run-default-suite.mjs` | HARNESS-EVAL; the runner is the DEFAULT portable eval driver (adapters + preflight + fallback + retry, serial by default). Difficult SWE/harness-effectiveness claims default to the forced five-task DeepSWE suite (measured-difficult tasks) - use it, don't hand-roll a single-CLI run.mjs |
| `reference/skill-mine.md` | SKILL-MINE |
| `reference/market-research.md` | GREENFIELD: validate demand (optional) |
| `reference/observability.md`, `tui/` | Board: opt-in live dashboard |

**Done =** mode stated; smallest diff; Before/After Eval complete for code-mode changes; REAL
tests + request/docs green (not proxy); runtime MUST proven by real behavior; code-mode runs use
red-green test + DB evidence if data load-bearing; neighbor snapshots re-run with unnamed drift resolved; every
`GOAL.md` Success Criterion checked, with no orphan scope; `Z-<date>.md` written with run branch +
completion timestamp; DEBUG prod issue has reproduction fidelity and, if
non-exact, residual risk + post-deploy confirmation plan; user-facing UI at the Expressive baseline;
destructive steps consented; commit/merge only after the commit gate passes (`reference/delivery-gate.md`);
verified commands reported.
