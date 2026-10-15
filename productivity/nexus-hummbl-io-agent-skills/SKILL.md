---
name: nexus
description: Canonical-surface scanner for governance and operator context before `/apex` plans.
version: 0.2.5
execution-mode: advisory
argument-hint: "<topic, task, agent name, rule name, or question>"
category: governance-compliance
status: candidate
---
<!-- SoT: profile (~/.agents/skills/nexus/SKILL.md). Repo mirror: PROJECTS/apex-nexus/skills/nexus/SKILL.md. -->

# Nexus Activation

You are operating in **NEXUS MODE** — the canonical-governance-hub scan that pairs with `[apex]`.

**Concept**: APEX-NEXUS is the compound governance surface. Apex is the strategic-assessor role (task-scoped: "what should I do?"). Nexus is the canonical-source-of-truth hub (`~/.agents/`) it operates from. While apex assesses the task, nexus assesses **the governance landscape the task lives inside**: which rules govern, which agents have jurisdiction, which skills compose, which memory is relevant, what's canonical vs candidate vs superseded, where SoT lives.

Distinction:
- `[apex]` — task-scoped assessment ("what should I do about X?")
- `[nexus]` — surface-scoped scan ("what does the fleet PSOT already know about X?")
- `[memory-registry]` + `[bus]` — full cross-session state load when needed; nexus is narrower + PSOT-only
- `[find-work]` — operator-facing what-next; nexus is agent-facing context-fill

## Active Configuration
- **Mode**: Advisory read-only skill. Does not commit, does not push, does not write to PROJECTS/. Writes nothing except (optionally) a scratch summary under `_internal/nexus/`.
- **Tempo**: RECON — bounded scan of canonical surfaces (~2 minutes wall-clock)
- **Bus identity in skill-mode**: injected by the skill invocation runtime. This skill is a fallback workflow. It does not authorize the caller to post as `nexus`.
- **Resident distinction**: when the actual named resident Nexus agent is launched, bus identity is `nexus` per `~/.agents/rules/nexus-guardrails.md`.
- **Output**: Structured connection map suitable as input to `[apex]` planning OR direct operator consumption

## Receipt

On scan completion, post a STATUS receipt through the host-canonical bus wrapper when it is available:

Unix (bash/zsh):

```bash
python "$HOME/bin/bus-global.py" post <caller-identity> all STATUS "host=<host> nexus-scan-complete: mode=<topic|inventory>, surfaces=<N>, hits=<N>, drift-flags=<N>, promotion-ripe=<N>"
```

Windows (PowerShell):

```powershell
$busWrapper = Join-Path $HOME "bin\bus-global.py"
python $busWrapper post <caller-identity> all STATUS "host=<host> nexus-scan-complete: mode=<topic|inventory>, surfaces=<N>, hits=<N>, drift-flags=<N>, promotion-ripe=<N>"
```

Skill-mode callers keep their own canonical identity; they never post as `nexus`. If the canonical bus wrapper is unavailable, report `receipt=SKIPPED bus-unavailable` in the final response rather than writing directly to a TSV or fabricating a receipt. A structured scan summary may optionally be written to `_internal/nexus/<YYYY-MM-DD>-<topic-slug>.md`.

## Task
$ARGUMENTS

## Mode variants

- **Topic mode** (default): `$ARGUMENTS = <topic>`. Relevance-filter and cap at 5-10 hits per surface with 3-5 graph edges.
- **Inventory mode**: `$ARGUMENTS` empty or `--inventory`. Sweep all surfaces and cap at 15-20 hits per surface with 10-15 graph edges.

## Execution

Run independent surface scans in parallel when the runtime and context budget permit. If inherited context exceeds the active runtime's dispatch limit or background agents are unavailable, scan inline with parallel read-only calls. Each scan remains bounded to the mode-specific cap.

remote-node is DORMANT/OFFLINE_INDEFINITE since 2026-07-13. Skip remote-node-targeted surfaces and flag active-host or active-sync references to it as `STALE-remote-node-REF`.

### 1. Rule surface scan
- Grep `~/.agents/rules/` for the topic + cite each match: rule name + 1-line relevance
- Grep `~/.agents/rules/_candidates/` for proposed-rule matches; surface each with its **codification_tier + maturity_tier** (C1/C2/C3 × M0/M1/M2/M3). If a local candidate policy README is absent, read the candidate's frontmatter and flag missing two-axis metadata.
- Surface SoT discipline: a rule twin is the same filename under `PROJECTS/apex-nexus/rules/`; name the profile canonical, repo mirror, and any divergence.

### 2. Agent surface scan
- Grep `~/.agents/ROSTER.md` for agents with topic-relevant scope (role, default model, bus identity, guardrail file)
- Grep `~/.agents/rules/<agent>-guardrails.md` for any agent whose scope/prohibited-actions intersect the topic
- Surface trust tier + whether DECISION authority applies

### 3. Skill surface scan
- Grep `~/.agents/skills/` directory names + nearby SKILL.md headers for topic match
- Check `~/.agents/rules/skill-routing.md` for any trigger pattern matching the topic — name the routed skill
- Check `~/.agents/rules/skill-chains.md` for what to suggest BEFORE and AFTER the candidate skill

### 4. Memory surface scan
- Prefer the active caller's `~/.agents/agents/<agent>/memory/MEMORY.md`. If it is absent, resolve shared/runtime memory via `~/.agents/scripts/resolve-memory.sh` and scan `$FLEET_MEM` plus `$RUNTIME_MEM/*.md`.
- Do not hardcode one runtime's private memory path as the shared default.
- Pull 1-line summary from any matched memory pin file
- Surface freshness: when was the pin last updated? Stale (>30d) gets flagged

### 5. Candidate / superseded surface scan
- Grep `~/.agents/rules/_candidates/` for in-flight candidates
- Grep `~/.agents/rules/_archived/` (and any `SUPERSEDED` markers) for retired rules
- Surface: "this topic has a candidate at C2/M0 — observe-only" or "this rule was superseded YYYY-MM-DD by X"
- For each candidate with a dated observation target, compute whether the budget elapsed and flag it `PROMOTION-RIPE`; C1 candidates past budget are highest priority.
- Before reporting a candidate as missing tier metadata, check whether it is a `SUPERSEDED` stub (it points to a promoted canonical rule) or intentionally legacy-format (a `SEMANTIC_REVIEW` note explains why). Neither is drift.
- Before reporting a lifecycle decision as pending (promote/demote/extend, "awaiting ratification"), check the rule's status in `~/.agents/rules/rules-index.md` and its history (`git log -- rules/<name>.md`). A rule body can lag its own ratification; report the stale body, not a pending decision.

### 6. SoT vs mirror reconciliation
- For each surfaced rule/doc: name the canonical location vs mirror locations (per `~/.agents/README.md` § SoT and mirror convention)
- Measure mirror drift with the mirror repo's own checker when it has one, not a byte comparison. `PROJECTS/apex-nexus` is a redacted mirror (placeholders such as `<HOME_DIR>`, `<FLEET_HOST_1>`), so raw diffs report nearly every file as divergent. Use `python scripts/mirror_drift_check.py --root . --canonical-root ~/.agents --canonical-ref origin/main --surface rules --baseline ci/mirror-drift-baseline.json` from an `apex-nexus` checkout of `origin/main`, and report its `divergent` and `missing-mirror` counts.
- Flag any surfaced file lacking the `<!-- SoT: -->` annotation when a repo twin exists (hygiene-debt, low-priority)

### 7. Cross-references
- For each surfaced surface, list its named cross-references (the "Related" / "Cross-references" / "Companion" sections in canonical rules)
- Build a small connection-graph: which rules cite which agents, which skills chain to which, which memory pins reference which projects

## Output shape

Emit a structured block apex can consume directly. Default template:

```
## NEXUS scan: <topic>

Scope: <which surfaces scanned, which skipped + why>
Scan time: <wall-clock>
Canonical host: Workstation (primary) / Delta and remote-node (active execution hosts) / Huxley (retired) / remote-node (OFF-FLEET 2026-09-17)

### Rules in scope
- <rule-name>.md — <1-line relevance> [SoT: profile|repo]
- ...

### Candidate rules (observe-zone)
- _candidates/<name>.md — <tier C?/M?> — <relevance> — [PROMOTION-RIPE if past observation budget]

### Agents with jurisdiction
- <agent> — <trust tier> — <scope intersection>

### Skills in scope (composable)
- /<skill> — <when to use> — <chains before: X, chains after: Y>

### Memory pins relevant
- <pin-file>.md — <1-line> — <freshness flag>

### Superseded / archived (avoid)
- <retired>.md — superseded YYYY-MM-DD by <X> — <why noted>

### Connection graph (top 3-5 edges)
- <node> → <node>: <relation>
- ...

### Drift / gaps detected
- <missing SoT marker | stale memory | PROMOTION-RIPE candidate | STALE-remote-node-REF | rule with no consumers>

### Recommended apex consumption
- For task assessment, [apex] should load: <ordered list of 3-5 most relevant artifacts>
```

## When to invoke nexus

- **Before [apex] on a topic the agent doesn't have full context on** — fills the assessment surface before planning
- **After [apex] when the task touches multiple canonical surfaces** — verify nothing was missed
- **On rule-drift suspicion** — surface candidate vs canonical vs superseded for a topic
- **On agent onboarding/promotion review** — surface every artifact that governs an agent
- **On skill creation** — surface adjacent skills, chain candidates, routing-trigger collisions
- **On memory-pin cleanup** — surface what's stale vs current vs missing

## When NOT to invoke nexus

- Pure code review (no governance surface involved) — use [mtsmu-review] or direct read
- Single-file local edits with no fleet relevance — overkill
- Cross-session state load needed — use `[memory-registry]` + `[bus]` first; nexus is PSOT-only
- Operator-facing what-next — use [find-work]

## Pairing with [apex] (canonical pattern)

```
operator → [apex] <task>
  ↓
  [apex] Step 1 (Assess) calls [nexus] <topic-extracted-from-task> inline
  ↓
  [nexus] scans canonical surfaces, emits structured block
  ↓
  [apex] Step 2-4 (Map/Plan/Gate) consume nexus output
  ↓
  [apex] Step 5 (Delegate) dispatches to [build] [ship] [ops] [research] [govern]
```

Or invoked sequentially:

```
operator → [nexus] <topic>            (surface scan)
operator → [apex] <task in topic>     (task assessment with nexus context already on screen)
```

Or as a sub-step inside an apex assessment when apex's own checklist surfaces governance-context gaps.

## Composition patterns with [apex] (MTSMU x HUAOMP)

Three documented composition patterns. Pick by task class; none require new wrapper skills.

### Pattern A -- Rigor-stack (MTSMU outer, HUAOMP-Omni between)

For: P0/P1 governance changes, security-class edits, irreversible decisions, cross-machine coordination.

```
[mtsmu-orchestrator]  <-  outer evidence/uncertainty/action/verification contract
   |- Evidence       :  [nexus] <topic> output (canonical-surface scan)
   |- [HUAOMP-O]     :  explicit stakeholder/timescale/failure-mode rotation
   |- Uncertainties  :  apex's plan gaps + nexus drift findings
   |- Action         :  [apex] <task> plan
   |- Verification   :  post-execution receipts vs nexus canonical context
   |_ Next lanes     :  drift remediation, gap-fills
```

MTSMU's confidence-scoring (0-1 with evidence ties) prevents apex over-confidence. HUAOMP-Omni's all-perspective rotation catches stakeholders nexus surfaces implicitly but doesn't enumerate. Token cost: ~3-4x plain `[apex] + [nexus]`. Worth it when reversibility is low.

### Pattern B -- Breadth-stack (HUAOMP outer 6-lens sweep, [nexus] per-lens)

For: new-domain entry, novel architecture, paradigm-uncertain work, UTF tier-3+ (Complex/Wicked).

```
[huaomp] full <topic>                        <-  generates 6 lens-questions
   |- H (system feedback loops)   ->  [nexus] -> surface-map-H
   |- U (cross-domain invariants) ->  [nexus] -> surface-map-U
   |- A (hard constraints)        ->  [nexus] -> surface-map-A
   |- O (all stakeholders)        ->  [nexus] -> surface-map-O
   |- M (problem-of-problem)      ->  [nexus] -> surface-map-M
   |_ P (paradigm assumptions)    ->  [nexus] -> surface-map-P
[apex] synthesizes 6 maps with MTSMU per-lens output-contract
      -> plan with explicit lens-attribution on each decision
```

Forces problem-reframing before solution-search. Paradigmatic + Meta are the under-exercised lenses that catch "we're solving the wrong problem." Token cost: ~6x baseline. Run nexus scans in parallel to compress wall-clock.

### Pattern C -- Adversarial-pair (HUAOMP-Absolute set ops + MTSMU verification)

For: cross-check Stage 3 PR review, adversarial audit, gap-detection on shipped plans, post-hoc review.

```
[apex] <task>      ->  plan A (intended-future)
[nexus] <topic>    ->  canonical context C (current-canonical)
[huaomp] absolute  ->  3 set ops:
                     A intersect C : constraint-checks (each MUST pass)
                     A minus     C : assumption-flags  (each MUST be verified)
                     C minus     A : coverage-gaps     (each MUST be addressed or waived)
[mtsmu] Verification gate  :  post-execution receipt-match
```

Set-op language maps directly to the severity ladder:
- `A - C` unflagged -> P1 (unverified assumption)
- `C - A` ignored -> P2 (coverage gap)
- `A intersect C` unverified -> P3 (constraint not asserted)

Naturally bidirectional -- works as cross-check between Principal AI Agent and Engineer (codex plan vs nexus canonical vs claude-code review).

Validated 2026-05-21: this pattern's discipline would have flagged kai-guardrails criterion #6 (a `C - A` gap apex missed) at plan-time, not post-hoc.

### Pattern selection rubric

| Task class | Pattern | Why |
|---|---|---|
| High-frequency consequential (PRs, ADRs, releases) | **A** | Cheap insurance against apex over-confidence at scale |
| Novel ground (new agent class, new primitive, paradigm-uncertain) | **B** | Paradigmatic lens catches misframed problems |
| Review / audit / cross-check Stage 3 | **C** | Set-op language ↔ severity ladder, bidirectional |

Patterns are additive, not exclusive -- a session may use A on Monday, C on Tuesday, B for the next quarter's new initiative.

## Anti-patterns

- **Caller skill-mode posting as `nexus`** — using this skill does not make the caller resident Nexus. Skill-mode bus posts use the runtime-injected identity. Only the actual named resident Nexus runtime posts as `nexus`.
- **Nexus writing canonical rules** — read-only. Promotions go through `_candidates/` triage and operator review, not via nexus.
- **Nexus skipping the candidate/superseded scan** — those are the highest-signal surfaces for "is this topic already governed". Skipping them defeats the purpose.
- **Nexus replacing [apex] assessment** — nexus surfaces context; apex makes the call. Nexus alone produces no plan.
- **Unbounded scan** — cap each surface at the mode-appropriate limit (5-10 in topic mode; 15-20 in inventory mode). If a wider scan is needed, the operator scopes it explicitly.

## Cross-references

- `~/.agents/README.md` — APEX-NEXUS topology (PSOT, junction views, SoT convention)
- `~/.agents/IDENTITY.md` — APEX-NEXUS physical host (Workstation) + sync policy
- `~/.agents/skills/apex/SKILL.md` — paired skill; nexus is the canonical-surface companion
- `~/.agents/rules/apex-nexus-composition.md` — canonical A/B/C composition pattern bodies
- `~/.agents/rules/apex-guardrails.md` — apex agent's guardrails (resident-apex constraints; nexus the skill operates under the caller's guardrails)
- `~/.agents/rules/nexus-guardrails.md` — resident Nexus identity, authority, and bus contract
- `~/.agents/agents/nexus.md` — named resident Nexus prompt
- `~/.agents/rules/nexus-query-scoping-pre-check.md` — specificity filter before scans
- `~/.agents/rules/_candidates/README.md` — T1/T2/T3 + two-axis candidate triage (nexus surfaces candidates with explicit tier marks)
- `~/.agents/skill-routing.md` — where [nexus] trigger phrases live (generated data file; moved out of `rules/` 2026-08-31)
- `~/.agents/rules/skill-chains.md` — where [nexus] chain suggestions live
- `~/.agents/skills/memory-registry/SKILL.md` and `~/.agents/skills/bus/SKILL.md` — broader cross-session state load; nexus is narrower

## Origin

Codified 2026-05-21 per operator request: "we dont have a skill for nexus yet but we know what nexus is. review it. build the skill. use it in conjunction with apex."

The concept of NEXUS was implicit across multiple canonical surfaces (`~/.agents/README.md` header "HUMMBL APEX-NEXUS", `IDENTITY.md` "APEX-NEXUS physical host", `crab-protocol-workstation.md` "`.agents/` tree is canonical (APEX-NEXUS)") but had no skill surface. This skill makes the canonical-hub scan invocable directly and composable with [apex].

v0.1.0 was the first cut. v0.2.0 added inventory mode, bounded parallel scanning, receipts, promotion-ripe checks, remote-node dormancy handling, agent-specific memory, and explicit mirror matching. v0.2.1 added resident-agent and scoping-rule cross-references. v0.2.2 reconciles the profile as SoT, replaces dead `hummbl-governance` paths, makes receipts bus-availability-aware, and makes the execution model runtime/context-aware.

v0.2.3 corrects the inventory output template after Huxley retired: Workstation is
canonical, Delta and remote-node are active execution hosts, Huxley is retired, and
remote-node remains offline indefinitely. The scan contract is unchanged.

v0.2.4 (2026-09-18) adds verification steps after an inventory scan overreported
drift: steps 5 and 6 now require checking superseded stubs, `rules-index.md`,
and git history before calling a candidate untiered or a decision pending, and
measuring mirror drift with the mirror's own redaction-aware checker instead of
byte comparison (the scan reported 143 diverged files; the real figure was 48).

v0.2.5 (2026-09-24) corrects remote-node status line to OFF-FLEET 2026-09-17 per machine-roster.md.

Promote to v1.0 after:
- ≥3 sessions cite the skill as load-bearing in AAR or peer review
- At least one cycle of [apex] + [nexus] composition produces a measurably better plan than [apex] alone
- Routing entry in `skill-routing.md` proves discoverable (operator invokes by trigger phrase, not by skill name)
