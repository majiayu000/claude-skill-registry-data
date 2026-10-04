---
name: op
description: Strategy orchestration — 17 strategies including refine, tournament, chain, review, debate, red-team, brainstorm, distribute, council, socratic, persona, scaffold, compose, decompose, hypothesis, investigate, monitor
allowed-tools:
  - AskUserQuestion
---

# x-op — Strategy Orchestration (Claude Code Native)

Direct structured strategies to an agent team.
The leader Claude (you) serves as both orchestrator and synthesizer, controlling agents via the **Claude Code native Agent tool**.
No external dependencies (no term-mesh or tmux required).

## Arguments

User provided: $ARGUMENTS

## Mode Detection

Read mode from `.xm/config.json` (`mode` field). Default: `developer`.

**Developer mode**: Use technical terms (strategy, verdict, premise, assumption, consensus). Concise.

**Normal mode**: 쉬운 한국어로 안내합니다.
- "strategy" → "전략", "verdict" → "판정", "premise" → "가정", "self-score" → "자체 점수"
- "consensus" → "합의", "refinement" → "다듬기", "tournament" → "대결", "debate" → "토론"
- "compose" → "조합", "decompose" → "분해"
- Use "~하세요" form; lead with key information first

### Korean output style (avoid AI-slop)

Universal (both modes) — these read as machine-generated in any register:
- Drop empty intensifiers ("매우 / 완벽하게 / 강력한 / 원활하게 / 혁신적인") unless they carry a specific, real claim.
- No forced rule-of-three or "~뿐만 아니라 ~까지" balance that adds no fact.
- No hedged non-conclusions ("결국 상황에 따라 다르다 / 균형이 필요하다"). End on a concrete fact, number, or next action.

Developer mode: terse and direct — lead with the result; state findings/actions without a 권고형 결말 pile-up ("~해야 한다" sentence after sentence).
Easy/normal mode: accessible Korean is the goal — polite guidance ("~해 보세요"), one line of context for non-experts. Keep commands, flags, paths, and proper nouns in English; on first use write a domain term as Korean(original), e.g. 결론(verdict). Still apply the universal rules; accessible ≠ padded or vague.

## Model Routing

| Subcommand | Model | Reason |
|------------|-------|--------|
| `list` | **haiku** (Agent tool) | Catalog display, no reasoning |
| Auto-route (strategy detection) | **session** (leader) | Requires AskUserQuestion — leader-only |
| Strategy execution | **session** (leader) | Judgment work runs on the model the user picked via /model — never downgrade |

For haiku-eligible commands, delegate via: `Agent tool: { model: "haiku", prompt: "Run: [command]" }`

## Wiring

```
suggests: x-eval
suggests: x-humble
```

## Post-Strategy Eval Gate

After every strategy completes (Self-Score appended), check for auto-eval:

1. Read `.xm/config.json` → check `eval.auto` field
2. If `eval.auto: true` OR `--verify` flag was used:
   - Automatically invoke x-eval score with the strategy output
   - Rubric: use the strategy's default rubric from Self-Score Protocol mapping
   - Mode: use `--grounded` if the strategy involved code (review, red-team, monitor)
   - Linkage: pass `--run-id`, `--source-plugin x-op`, `--source-strategy`, and `--source-result`
   - Store result in `.xm/eval/results/`
3. If `eval.auto` is not set and `--verify` is not used:
   - Show suggestion: `"💡 x-eval로 품질 평가를 할 수 있습니다. /xm:eval score로 실행하세요."`

This replaces the previous --verify inline judge panel with x-eval delegation, ensuring a single evaluation path.

> **Self-Score rule (applies to all strategies)**: Every strategy's final output MUST include a `## Self-Score` block per `references/self-score-protocol.md`.

## AskUserQuestion Dark-Theme Rule

See `references/ask-user-question-rule.md` — the `question` field is invisible on dark terminals; put context in markdown, use `header`/`label`/`description` for user-facing text.

## Interaction Protocol

x-op strategies with multiple phases use AskUserQuestion at phase boundaries: after completing a phase, show its results, then call AskUserQuestion to confirm before starting the next one. It is the one mechanism that ends the turn and waits for the user; a question written as plain text ("진행할까요?") does not. When auto-detecting a strategy, confirm the recommendation the same way before executing.

Shape:
- ❌ Complete Phase 1, output results, then immediately start Phase 2
- ❌ Ask "다음 단계로 넘어갈까요?" as text output
- ✅ Complete Phase 1, output results, call AskUserQuestion("Phase 1 완료. Phase 2를 진행할까요?")

### Phase Checkpoint (before any phase transition)

Before calling AskUserQuestion for a phase boundary, the leader outputs a `**PHASE_N_CHECKPOINT:**` block listing the exit conditions for the phase just completed. This forces self-verification and gives the user something concrete to approve.

Template:
```
**PHASE_{N}_CHECKPOINT:**
- [x] {required output produced}
- [x] {evidence collected}
- [x] {dimensions covered or agents completed}
```

Rules:
- Every unchecked (`- [ ]`) item means the phase is NOT complete — fix it before asking
- For fan-out phases, include agent count (e.g., `- [x] 4/4 agents completed`)
- For compose sub-strategies, emit a checkpoint at each sub-strategy boundary, not only at the outer level
- Checkpoint precedes AskUserQuestion; AskUserQuestion still carries phase-transition authority

### Phase Boundary Exceptions

Some strategies contain internal loops or sub-strategy calls. Apply the phase boundary rule at user-meaningful boundaries:
- `chain`: checkpoint after each declared step; ask before moving to the next step unless the user selected `--dry-run`
- `compose`: each sub-strategy follows its own phase rules; ask before starting the next sub-strategy in the pipeline
- `socratic`: ask after the seed phase and after each synthesized question round
- `investigate`: Phase 2.5 cross-validation is part of Phase 2 for `deep|exhaustive`; ask before Phase 3

## Routing

Determine strategy from the first word of `$ARGUMENTS`:
- `list` → [Subcommand: list]
- `direct` → [Strategy: direct]
- `refine` → [Strategy: refine]
- `tournament` → [Strategy: tournament]
- `chain` → [Strategy: chain]
- `review` → [Strategy: review]
- `debate` → [Strategy: debate]
- `red-team` → [Strategy: red-team]
- `brainstorm` → [Strategy: brainstorm]
- `distribute` → [Strategy: distribute]
- `council` → [Strategy: council]
- `socratic` → [Strategy: socratic]
- `persona` → [Strategy: persona]
- `scaffold` → [Strategy: scaffold]
- `compose` → [Strategy: compose]
- `decompose` → [Strategy: decompose]
- `hypothesis` → [Strategy: hypothesis]
- `investigate` → [Strategy: investigate]
- `monitor` → [Strategy: monitor]
- Empty input → [Subcommand: interactive-pick] — show catalog, then AskUserQuestion to select strategy
- Other text (no strategy keyword match) → [Auto-Route] — detect intent and recommend strategy

> **Empty-input anti-pattern** (NEVER do this): output a plain-text question like "어떤 작업을 도와드릴까요?" and wait. Empty input has a deterministic spec — follow it. Plain-text questions don't create a real turn boundary, so the skill keeps re-firing against no arguments.

### Auto-Route (Natural Language → Strategy)

When input matches no strategy keyword, detect intent from the signal table below, then **confirm with AskUserQuestion before executing** (see Interaction Protocol).

| Signal (ko / en) | Strategy | Conf |
|---|---|---|
| 리뷰, 검토 / review, check | review | high |
| 보안, 취약점 / security, vulnerability, XSS, injection | red-team | high |
| vs, 비교 / compare, which is better | debate | high |
| 아이디어, 브레인스토밍 / idea, brainstorm | brainstorm | high |
| 왜, 원인 / why, root cause — explanation only, no fix expected | hypothesis | high |
| 버그, 디버그, 고쳐줘, 안 돼 / debug, fix this bug, failing test | → x-solver iterate | high |
| 조사, 분석 / investigate, analyze | investigate | high |
| 개선, 다듬 / improve, refine | refine | high |
| 합의, 의견 모아 / consensus, stakeholders | council | high |
| 설계, 아키텍처 (whole-system) / design, architecture | council | medium |
| 분해, 나눠, 쪼개 (dependency tree) / break down | decompose | high |
| 조합, 파이프라인 / combine, multi-strategy pipeline | compose | medium |
| 모니터, 감시 / watch, monitor | monitor | high |
| 관점, 입장 / perspective, persona | persona | high |
| 질문, 명확하게 / clarify, socratic | socratic | medium |
| 경쟁, 제일 나은 거 골라, 후보 채택 / compete, best of N | tournament | high |
| 단계별, 순차, 차례대로 / step by step, sequential A→B | chain | high |
| 병렬로 나눠, 동시에 처리 / parallel split, independent subtasks | distribute | high |
| 모듈 구조 잡고 구현 / scaffold, build with module spec | scaffold | medium |
| file/dir path (`src/`, `*.ts`) | review (red-team if security) | medium |
| 그냥, 간단히, 한 줄로 / just, quickly, one-liner — ≤ ~15 words, one target, no other signal | direct | medium |

Priority when multiple match: (1) security → red-team; (2) explicit vs/비교 → debate; (3) code/file target → review unless a security signal is present; (4) why/원인 with no fix expected → hypothesis, an observed failure the user wants fixed → hand off to x-solver iterate; (5) still multiple → pick the highest-confidence row, tie → ask. Compound boost: 2+ signals raise confidence (e.g. "보안 리뷰" = security+review → red-team). `direct` is a recommendation leaf, never a bypass: it goes through the same AskUserQuestion confirmation as every other strategy (`1) direct (Recommended) 2) refine 3) …`). **Use `x-solver iterate` when the run must end in an applied, execution-proven fix — or may need more than one round of state carried across turns; use `x-op hypothesis` when a single pass that names and refutes causes is the whole deliverable.** `hypothesis` stops at a recommended verification method and never applies or proves a fix; offer the hand-off through the same confirmation as any strategy.

See `references/x-op-auto-route.md` for execution flow and worked examples.

## Options

- `--rounds N` — Number of rounds (default 4)
- `--preset quick|thorough|deep` — quick: rounds=2, thorough: rounds=4, deep: rounds=6
- `--preset analysis-deep` — compose preset: `investigate | hypothesis | refine`
- `--preset security-audit` — compose preset: `review | red-team`
- `--preset consensus` — compose preset: `persona | council`
- `--agents N` — Number of participating agents (default: shared config's agent_max_count (default 4). Overrides when specified)
- `--model sonnet|opus|haiku` — Agent model (default sonnet)
- `--cross-vendor` — debate/council/persona (roles→vendors) + brainstorm/red-team/tournament/hypothesis (generation phase→vendors): fan out across different model vendors (claude+codex+cursor…) via `xm panel cross`. **The vendor fan-out MUST go through `xm panel cross` (with `--source op:<strategy>`) — never fan out cross-vendor roles/generations with the Agent tool. Only `xm panel cross` writes `.xm/cross/<run>/status.json`; that file is the ONLY thing that makes the run observable to `xm panel status --all` / `--watch` / dashboard. This holds even for the single-vendor fallback — run it as `xm panel cross --models <one>`, not the Agent tool, or status goes silently blind.** Opt-in; single-vendor fallback when <2 ready. Default without the flag: `.xm/config.json` `cross_vendor.op` ?? `cross_vendor.default`; `--no-cross-vendor` forces single. See `references/cross-vendor.md`.
- `--steps "role:task,role:task"` — Manually specify chain steps
- `--target <file|dir>` — review/red-team target
- `--vote` — Enable dot voting for brainstorm
- `--analogical` — Brainstorm: cross-domain structural mapping mode
- `--lateral` — Brainstorm: de Bono lateral thinking operators mode (4 agents)
- `--context` — Inject conversation context to agents
- `--no-context` — Disable context injection
- `--personas "role1,role2,..."` — Manually specify roles for persona strategy
- `--bracket single|double` — Tournament bracket type (default single)
- `--weights "role:N,role:N"` — Council weighted voting (default equal)
- `--dry-run` — Output execution plan only (no agent execution)
- `--resume` — Resume from previous checkpoint
- `--explain` — Output decision trace
- `--pipe <strategy>` — Strategy pipelining (compose)
- `--start haiku|sonnet` — Escalate starting level (default haiku)
- `--threshold N` — Quality threshold for escalation and x-eval verification (default 7)
- `--max-level haiku|sonnet|opus` — Escalate maximum level (default opus)
- `--angles "a,b,c"` — Manually specify investigation angles
- `--depth shallow|deep|exhaustive` — Investigation depth (default shallow)
- `--verify` — Delegate final quality verification to x-eval after strategy completion

## Shared Config Integration

x-op references shared config from `.xm/config.json`:

| Setting | Key | Default | Effect |
|---------|-----|---------|--------|
| Agent count | `agent_max_count` | `4` | Determines fan-out/broadcast agent count when `--agents` is not specified |
| Mode | `mode` | `developer` | Output style (technical terms vs plain language) |

Change settings: `xm config set agent_max_count 10`

When the skill layer creates agents, if no `--agents` flag is present, it reads agent_max_count from shared config to determine the number of agents.

## Pre-Execution Confidence Gate

Before dispatching agents for any strategy, the leader self-assesses readiness. This is a lightweight pre-check (~50 tokens), not a post-execution quality gate.

### Checklist (answer each before proceeding)

1. **Topic clarity** — Is the task unambiguous? Can agents act on it without guessing?
2. **Sufficient context** — Does the leader have enough information (files read, prior results) to orchestrate?
3. **Strategy fit** — Is the selected strategy appropriate for this task type?
4. **Scope boundedness** — Can agents produce a result within their token/round budget?

### Decision

| Yes count | Confidence | Action |
|:---------:|:----------:|--------|
| 4/4 | HIGH | Proceed silently — no user interruption |
| 3/4 | MEDIUM | State which item is uncertain, proceed with caveat noted in trace |
| ≤ 2/4 | LOW | **STOP.** Show the uncertain items. Use AskUserQuestion: "Confidence is low. Clarify or proceed anyway?" |

### Rules
- The gate fires AFTER strategy selection but BEFORE the first agent dispatch
- For `compose` pipelines, the gate fires ONCE at the top level, not per sub-strategy
- The gate does NOT fire for `list`, `--dry-run`, or `--resume` (no agent dispatch)
- When `--context` is active, context injection counts toward "sufficient context"
- Record the confidence level in the trace entry (session_start args)

## Agent Primitives

This skill uses only Claude Code built-in tools:

### fan-out (same question to all)
Invoke N Agent tools **simultaneously** in a single message:
```
Agent tool call 1: { description: "agent-1", prompt: "...", run_in_background: true, model: "sonnet" } <!-- managed-model: executor -->
Agent tool call 2: { description: "agent-2", prompt: "...", run_in_background: true, model: "sonnet" } <!-- managed-model: executor -->
Agent tool call 3: { description: "agent-3", prompt: "...", run_in_background: true, model: "sonnet" } <!-- managed-model: executor -->
```
All agents receive the same prompt but respond independently.

Agent count is determined by the `--agents N` flag or shared config's `agent_max_count`.

### delegate (assign to a specific agent)
Invoke 1 Agent tool:
```
Agent tool: { description: "role name", prompt: "...", run_in_background: false }
```
Receive the result immediately and use it in the next step.

### broadcast (different context to each)
Same as fan-out, but sends a **different** prompt to each agent (e.g., including other agents' results).

### Result collection
- Agents with `run_in_background: true` auto-notify on completion
- When notified, read results and use them in the next round

## Subcommand: list

Output the catalog in `references/x-op-list.md` verbatim (strategies, options, examples).

---

## Subcommand: interactive-pick

Entry: empty `$ARGUMENTS`. See `references/x-op-interactive-pick.md` — render catalog (same block as `## Subcommand: list`), then TWO AskUserQuestion calls: (1) strategy (4 common options; `AskUserQuestion` auto-appends `Other`, do NOT add it yourself), (2) topic. Plain-text questions are forbidden — they don't create a turn boundary and cause the skill to re-fire against empty args.

> **Strategy block execution rule:** the `## Strategy:` blocks below are routing SUMMARIES. Before executing any strategy, use the Read tool to open `strategies/<name>.md` and follow it verbatim — the exact agent prompts, word limits, phase gates, and persist schema live there, not in the summary. (Repo probe: passive "see X.md" pointers go unread 0/5, so this Read step is mandatory, not optional.)

## Strategy: direct

See `strategies/direct.md` — one agent, one call, no orchestration. The single-agent baseline every other strategy must beat (`/xm:eval bench` includes it as the control arm); persists `.xm/op/direct-*.json` with the canonical keys so `--verify` / dashboard work unchanged.

## Strategy: refine

See `strategies/refine.md` — round-based Diverge → Converge → Verify refinement. Round 1 DIVERGE fan-out produces N independent proposals (run_in_background parallel); Round 2 CONVERGE leader synthesizes and runs a vote fan-out to adopt the best; Round 3+ VERIFY fan-out checks the adopted proposal — all OK triggers early termination, issues raised loop back until max_rounds.

## Strategy: tournament

See `strategies/tournament.md` — Compete → anonymous vote → adopt winner. Phase 1 COMPETE fan-out collects solutions; Phase 2 ANONYMIZE removes agent names and shuffles order; Phase 3 VOTE fan-out ranks anonymized solutions; Phase 4 TALLY applies Borda count. Supports `--bracket double` for seed ranking with losers' bracket. With `--cross-vendor`, the COMPETE phase fans out across vendors (one solution per vendor into the bracket); ANONYMIZE/VOTE/TALLY stay single-vendor — see `references/cross-vendor.md`.

## Strategy: chain

See `strategies/chain.md` — A→B→C sequential pipeline with conditional branching. Each step delegates to one agent passing prior step result as context. Enhanced mode supports `if:condition->step` DAG branching syntax and auto-inserts supplementary steps when confidence is low.

## Strategy: review

See `strategies/review.md` — Multi-perspective code review fan-out. Phase 1 TARGET reads `--target` file or `git diff HEAD`; Phase 2 ASSIGN distributes Security/Logic/Performance perspectives (scales with `--agents N`); Phase 3 REVIEW fan-out with per-perspective prompts; Phase 4 SYNTHESIZE deduplicates and sorts by severity.

## Strategy: debate

See `strategies/debate.md` — Pro vs Con debate followed by verdict. Phase 1 POSITION distributes agents into PRO/CON/JUDGE; Phase 2 OPENING runs simultaneous fan-out for arguments; Phase 3 REBUTTAL cross-sends openings; Phase 4 VERDICT delegate scores all arguments and delivers a final recommendation. With `--cross-vendor`, PRO/CON/JUDGE map to different model vendors — see `references/cross-vendor.md`.

## Strategy: red-team

See `strategies/red-team.md` — Adversarial attack/defend cycle. Phase 1 TARGET collects via `--target` or `git diff HEAD`; Phase 2 ATTACK fan-out finds vulnerabilities tagged by dimension; Phase 3 DEFEND fan-out provides fixes or counter-evidence; Phase 4 REPORT synthesizes Fixed(🟢)/Partial(🟡)/Open(🔴). With `--cross-vendor`, the ATTACK phase fans out across vendors (each model attacks from its own blind spots); DEFEND/REPORT stay single-vendor — see `references/cross-vendor.md`.

## Strategy: brainstorm

See `strategies/brainstorm.md` — free ideation → cluster → vote. Phase 1 GENERATE fan-out produces minimum 5 tagged ideas per agent; two optional modes: `--analogical` (cross-domain structural mapping) and `--lateral` (de Bono operators: Reversal, Provocation, Random Entry, Fractionation). Phase 2 CLUSTER deduplicates and groups by theme; Phase 3 VOTE (when `--vote` is set) fan-out selects top 3. With `--cross-vendor`, the GENERATE phase fans out across model vendors (each vendor's idea set) instead of same-model agents; CLUSTER/VOTE stay single-vendor — see `references/cross-vendor.md`.

## Strategy: distribute

See `strategies/distribute.md` — Split a large task into independent subtasks → parallel fan-out → merge. Phase 1 SPLIT auto-splits or uses `--splits`; Phase 2 DISPATCH fan-out with scoped subtask prompts; Phase 3 MERGE leader resolves conflicts and synthesizes by theme.

## Strategy: council

See `strategies/council.md` — N-party free discussion → cross-examination → deep dive → consensus. Round 1 OPENING fan-out collects positions; Round 2 CROSS-EXAMINE broadcasts each agent's view to others (excluding their own); Round 3~N-1 DEEP DIVE targets key points of contention; Final CONVERGE drafts a consensus proposal for vote. Supports `--weights` for role-based weighted voting. With `--cross-vendor`, opening positions come from different model vendors — see `references/cross-vendor.md`.

## Strategy: socratic

See `strategies/socratic.md` — Socratic questioning across N rounds: Phase 1 SEED collects an initial position via delegate; Phase 2 QUESTION ROUNDS fan-out agents as questioners targeting logical gaps and implicit premises, then leader synthesizes and sends to a responding agent. Early termination when questions become trivial; max_rounds cap for best-effort output.

## Strategy: persona

See `strategies/persona.md` — Role-based multi-perspective analysis. Phase 1 ASSIGN distributes fixed personas (default: senior engineer, security expert, PM, junior developer); Phase 2 ANALYZE broadcast with per-persona prompts; Phase 3 SYNTHESIZE unifies across perspectives; optional Phase 4 CROSS-CHECK verifies unified proposal from each persona's view. With `--cross-vendor`, ASSIGN maps each persona to a different vendor and Phase 2 ANALYZE runs per-vendor (a genuinely different model per perspective, not one model role-playing); SYNTHESIZE/CROSS-CHECK stay single-vendor — see `references/cross-vendor.md`.

## Strategy: scaffold

See `strategies/scaffold.md` — Structure design → module distribution → parallel implementation → integration. Phase 1 DESIGN delegates to opus for module/interface spec; Phase 2 DISPATCH fan-out per module; Phase 3 INTEGRATE resolves interface compatibility and assembles final result.

## Options Reference

See `references/x-op-options.md` — detailed behavior for `--dry-run`, `--resume`, `--explain`, `--verify`, `--vote` (Self-Consistency).

## Strategy: compose

See `strategies/compose.md` — Chain multiple strategies into a sequential pipeline. Supports `compose "A | B | C"` syntax and `--pipe` flag. Leader constructs `pipe_payload` between each step using per-strategy extraction rules; includes a full transformation table for common strategy pairings.

## Strategy: decompose

See `strategies/decompose.md` — Recursive decomposition → leaf parallel execution → bottom-up assembly. Phase 1 DECOMPOSE delegates to an opus agent to build a dependency tree; Phase 2 EXECUTE LEAVES fan-out in dependency order; Phase 3 ASSEMBLE integrates results bottom-up.

## Strategy: hypothesis

See `strategies/hypothesis.md` — Generate hypotheses → falsify → adopt survivors. Phase 1 GENERATE fan-out produces 2-3 tagged hypotheses per agent with falsifiable predictions; Phase 2 FALSIFY fan-out attempts to disprove each (FALSIFIED or SURVIVED); Phase 3 SYNTHESIZE selects strongest survivor, re-runs if none survive (up to max_rounds). With `--cross-vendor`, the GENERATE phase fans out across vendors (diverse root-cause priors); FALSIFY/SYNTHESIZE stay single-vendor — see `references/cross-vendor.md`.

## Strategy: investigate

See `strategies/investigate.md` — Multi-angle investigation → synthesis → gap analysis. Phase 1 SCOPE auto-selects angles from topic pattern (codebase/comparison/security/performance/general); Phase 2 EXPLORE broadcast with depth-aware prompts (shallow/deep/exhaustive); Phase 2.5 CROSS-VALIDATE for deep/exhaustive; Phase 3 SYNTHESIZE with conflict resolution and confidence aggregation; Phase 4 GAP ANALYSIS delegate suggests follow-up strategies.

## Strategy: monitor

See `strategies/monitor.md` — one-shot OODA (observe → orient → decide → act). Default observation targets: `--target` or recent git changes. Phase 2 ORIENT broadcasts to N agents across code-quality/security/dependency/test-coverage angles; Phase 3 DECIDE applies wait/escalate/act; Phase 4 ACT auto-dispatches red-team/review/chain/investigate/hypothesis per alert type.

---

## Strategy Selection Guide

When the user does not know which strategy to use, recommend one using the decision tree below:

```
What kind of task is this?
│
├─ Single well-specified task, one acceptable answer → direct (one agent — measure before adding orchestration)
│
├─ Code writing/implementation → What scale?
│   ├─ Single module → scaffold
│   ├─ Multiple independent tasks → distribute
│   └─ Dependency tree → decompose
│
├─ Code review/security → What purpose?
│   ├─ Quality inspection → review
│   ├─ Vulnerability hunting → red-team
│   └─ Both → compose "review | red-team"
│
├─ Decision-making/design → Are there options?
│   ├─ 2 opposing choices → debate
│   ├─ 3+ candidates → tournament
│   ├─ Multiple stakeholders → council
│   └─ Per-perspective analysis needed → persona
│
├─ Problem solving/debugging → Is a fix expected?
│   ├─ Yes — must end fixed and proven → hand off to x-solver iterate
│   ├─ No, name the cause only → hypothesis (or investigate when there is no symptom yet)
│   └─ Want to verify assumptions → socratic
│
├─ Ideation/planning → What stage?
│   ├─ Divergence → brainstorm
│   ├─ Diverge→select→refine → compose "brainstorm | tournament | refine"
│   └─ Improve existing proposal → refine
│
├─ Sequential workflow → chain
│
└─ Change monitoring/anomaly detection → monitor
```

## Agent Output Quality Contract

Every agent output must be **evidence-based** (cites a fact/example/mechanism — "it's better" FAILs), **falsifiable**, and **dimension-tagged**. The leader enforces this at synthesis: **a finding whose only support is Invalid evidence is dropped, or returned to the agent for evidence before it counts.**

| Valid evidence | Invalid evidence |
|---|---|
| `file.ts:123` with the code quoted | "likely…", "probably…", "may be" |
| Output of a command actually run (grep/test/diff) | Logical deduction with no code proof |
| A test executed whose result proves the behavior | General explanation of how a tech works |
| Cited URL + quoted passage | Bare URL, no quote |
| Another agent's output referenced by ID/phase | "It is well known that…" |

See `references/agent-output-contract.md` for per-category Dimension Anchors and good/bad examples.

---

## Self-Score Protocol

Every strategy appends a `## Self-Score` block before persisting. Scale: **1=fail, 5=baseline, 7=good, 10=excellent.** Overall = weighted average of the rubric criteria.

Rubric by category (override with `--rubric`; the rubric NAME is recorded in the persisted eval object):
| Category | Strategies | Rubric | Criteria (weight) |
|---|---|---|---|
| Code | review, red-team, monitor | code-quality | correctness .30, readability .20, maintainability .20, security .20, test-coverage .10 |
| Argument | refine, tournament, debate, council, socratic, hypothesis, investigate | general | accuracy .25, completeness .25, consistency .20, clarity .20, hallucination-risk .10 |
| Decomposition | scaffold, decompose, distribute, chain | plan-quality | completeness .30, actionability .30, scope-fit .20, risk-coverage .20 |
| Ideation | brainstorm, persona | general | accuracy .25, completeness .25, consistency .20, clarity .20, hallucination-risk .10 |
| Pipeline | compose | (inherits last sub-strategy's) | — |

**4Q hallucination check (mandatory, every strategy)** — answer before presenting the final output:
1. **Evidence?** every factual claim cites a source (file:line / URL / tool output / agent quote); else flag UNVERIFIED.
2. **Requirements?** each element of the task: covered / partial / not covered.
3. **Assumptions?** list each; cite evidence or mark ASSUMED.
4. **Consistency?** findings don't contradict; the verdict follows from the evidence.

If 2+ are ⚠️, append: `"⚠ 2+ items flagged. Consider /xm:eval score --grounded."`

See `references/self-score-protocol.md` for the output-table format and full rationale.

## Result Persistence (REQUIRED — every strategy)

Every strategy MUST save its result to `.xm/op/{strategy}-{YYYY-MM-DD}-{slug}.json` as the final step, after the Self-Score block.

**Canonical top-level keys the saved JSON MUST carry** — a strategy's internal vocabulary (debate→question, persona→subject, …) may be added alongside but cannot REPLACE these. Omitting any is the documented root cause of `—` placeholders in the dashboard Ops list:

| Key | Why |
|---|---|
| `topic` | what the user asked — dashboard Topic column |
| `created_at`, `completed_at` | ISO8601 — sort order + duration |
| `options.agents` | agent count used — Agents column |
| `self_score` | `{overall, criteria}` — Score column |
| `status` | `completed` \| `failed` |
| `cross_vendor` (cross-vendor runs ONLY) | provenance: `{requested, effective, failed[], run_ref, per_vendor_raw[]}` + timing from the cross run's status.json, never the summary-write moment — without it vendor attribution is unauditable (author-attribution hallucination) |

See `references/x-op-result-persistence.md` for the full schema and per-strategy outcome mapping.

### Termination Checkpoint (required before declaring any strategy complete)

Before treating a strategy as done, emit this block as the last thing. Any unchecked item = strategy NOT complete — return to the missing step, do not end the turn.

```
**TERMINATION_CHECKPOINT:**
- [x] Final Output emitted (strategy-specific format)
- [x] Self-Score block emitted (1-10 scale + rubric)
- [x] 4Q hallucination check emitted (⚠ flagged when 2+ items uncertain)
- [x] Result file written with canonical keys (topic, created_at, completed_at, options.agents, self_score, status; + cross_vendor provenance when cross-vendor)
- [x] Save path surfaced to user: `💾 Saved: .xm/op/{filename}`
```

Rules:
- Run this checkpoint BEFORE the Post-Strategy Eval Gate
- `--dry-run` skips the checkpoint (no strategy execution occurred)
- `compose` emits one checkpoint per sub-strategy AND one for the outer pipeline
- Skipping the save step because "the result is in chat" is wrong: the next session cannot resume or cross-reference without the file

---

## Trace Recording

Tracing is automatic: the trace-session hook writes `session_start` when the skill is invoked, one `agent_step` per Agent tool call made before the assistant turn ends, and `session_end` at the turn's Stop hook. Do not hand-write those three row types; `fan_out`/`synthesize` stay LLM-written, metadata only, as x-trace describes.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll just use refine, it always works" | refine is convergence, not exploration. Use it *after* you have candidates, not before. Problems that need divergent thinking (brainstorm, tournament) starve on refine alone. |
| "This result looks good, `--verify` is overkill" | `--verify` exists precisely because "looks good" is where shared bias hides. Skipping it means you're trusting one model's confidence instead of checking its work. |
| "Debate is expensive, I'll skip it" | Debate is expensive *because* it surfaces disagreements that single-strategy runs hide. The cost is the value — if it didn't disagree, you didn't need it. |
| "Any strategy works for this" | "Any strategy" is the tell that you haven't classified the problem. Use auto-route or interactive-pick first — "any strategy" is functionally the same as no strategy. |
| "17 strategies is too many, I'll stick with 3" | Sticking with 3 means you're using them outside their fit zone. Auto-route narrows the 17 to the right 1-2 in seconds. |
| "The strategy matters less than the prompt" | The strategy *is* the control loop around the prompt. Wrong strategy = wrong loop = wasted agents even with a perfect prompt. |
| "Compose is for complex problems, mine is simple" | Compose chains strategies that address different failure modes. Even simple problems benefit when divergence-then-convergence is cheaper than any single strategy solving both. |
| "It's cross-vendor, but a plain Agent-tool fan-out is simpler than `xm panel cross`." | The Agent tool leaves no run record: no `.xm/cross/<run>/status.json`, so the run is invisible to `xm panel status --all`, `--watch`, and the dashboard. Cross-vendor roles/generations fan out through `xm panel cross` every time — including the single-vendor fallback (`--models <one>`). "Simpler" here means "unobservable." |
