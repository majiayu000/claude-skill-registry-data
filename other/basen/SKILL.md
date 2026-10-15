---
name: basen
description: BaseN-tier multi-variant operator catalog. Lookup / search / apply / recommend across registered variants (Base120 LIVE + Krineia/BKI staged). Wraps the basen-mcp server with fallback to canonical JSON registry.
version: 0.1.0
execution-mode: advisory
argument-hint: "<variant>:<code|keyword|problem> or <code> (defaults to base120)"
category: cognitive
status: candidate
---
# BaseN Tier — Multi-Variant Operator Catalog

BaseN is the umbrella tier for HUMMBL's typed-operator registries. Base120 is the first variant, fully canonicalized. Other variants are staged at varying maturity.

## Variant status table (verified 2026-06-13)

| Variant | Status | Operators | Families | Canonical source |
|---|---|---|---|---|
| **base120** | LIVE v1.0.0 (4-surface frozen-hash) | 120 | 6 (P/IN/CO/DE/RE/SY × 20) | `PROJECTS/base120/Base120_Canonical_Model_Registry.yaml` |
| **krineia** | PARTIAL — receipt-chain format, daemon consolidation pending | N/A (receipt-chain) | N/A | `PROJECTS/krineia/RECEIPT_SCHEMA.md` v0.1 + `INVARIANTS.md` v1.0-rc2 |
| **bki** | PARTIAL — measurement framework, no registry artifact | N/A (measurement) | 3 dimensions, 4 baselines | `PROJECTS/hummbl-bki/theory/THEORY_MASTER.md` v1.0 |

> **Retired from BaseN catalog** (2026-06-13): HUAOMP and MTSMU are methodologies, not operator registries. HUAOMP survives as standalone skill `/huaomp`. MTSMU survives as methodology pattern referenced by `mtsmu-review`, `mtsmu-debug`, etc. Neither has or needs a YAML registry.

Q7 verification source: `_internal/governance/basen-architecture/V1-q7-canonicalization-verification.md`.

## Usage

```bash
[basen] P1                                 # Base120 lookup (default variant)
[basen] base120:P1                         # Explicit variant prefix
[basen] "root cause"                       # Keyword search (defaults base120)
[basen] apply "feature velocity dropping"  # Apply Base120 lenses to problem
[basen] recommend "Q2 prioritization"      # Recommend operators for question
[basen] variants                           # Show variant status table
[basen] families base120                   # List families for a variant
```

## Task

$ARGUMENTS

## Pre-flight (6-question invoker discipline)

**Before any `[basen] apply` or `[basen] recommend` on a non-trivial problem, run the 6Q pre-flight (~2 minutes).** Skip for low-stakes lookups (`[basen] P1`).

The canonical Base120 registry is FROZEN (governance: GOVERNED_VERSION_BUMP_ONLY) and has NO auto-detect operator for dishonest prompts. The invoker carries the detection burden.

0. **Epistemic stance** — name the truth-relation this chain will serve BEFORE selecting operators. Each stance permits / forbids different operator families:
   - **descriptive** (what IS): facts, status, current-state recon. Permitted: P-family (anchor perspective), DE-family (decompose existing). Forbidden: RE-family as conclusion-driver (you don't recurse a fact), IN-family inversion to flip a description.
   - **prescriptive** (what SHOULD): recommendations, design, planning. All families permitted; IN-family encouraged for second-order effects; CO-family encouraged for composing recommendations.
   - **strategic** (what WINS): competitive positioning, negotiation prep. All families permitted BUT chain stays operator-local (per axiom 4e Adversarial-leak); only the Primary recommendation publishes to shared trace. Reasoning trace stays in `_internal/` or in-session memory.
   - **negotiative** (what HOLDS the table): bilateral framing where both sides need to keep talking. P-family + CO-family permitted; IN-family private only (don't enumerate the counterparty's failure modes in shared trace); SY-family limited (don't map the negotiation game-tree publicly).

   If stance is hybrid, name the hybrid explicitly and the dominant. **Anti-pattern**: stance-shopping — picking the stance that justifies the chain you already want. The stance MUST be picked from the prompt's truth-relation, not from the desired conclusion.

1. **Tier honesty** — does the prompt's claimed tier (framework name-drops, complexity signals) match its actual decision structure? Flag Trojan-Down (Tier-5 wrapper on Tier-2 decision) and Trojan-Up (Tier-2 wrapper on Tier-5 substrate, e.g. naming, irreversibility).
2. **Trust-root on observables** — does any falsifiability anchor satisfy receipt-writer ≠ observed-agent (Krineia §3.2)? Self-reported state (HRSI, cogstate, "did the chain work for me") fails this check.
3. **Temporal freshness vs. memory** — does the prompt reference pricing / scope / named entities / dates / framings that have documented pivots in memory pins? Pre-pivot framing is auto-disqualifying per `claim-honesty-protocol.md` §4.
4. **Domain fit** — is Base120 the right framework, or is this a surface where reasoning-operator chains do not produce defensible outputs? Apply the 5 domain-fit axioms; if ANY answers YES, route out instead of chaining operators:
   - **4a. Licensure-required**: would the output require professional licensure to produce defensibly? (legal-drafting / medical-advice / financial-advice / accounting-attestation → route to `[legal-counsel]`, `[healthcare-ai-watch]`, `[cfo-advisor]`, or human professional)
   - **4b. Embodied-access-required**: does the answer require felt-sense / nervous-system / somatic data not in text? (trauma response, regulation, BKI territory → route to `[bki-reframe]`, `[fitness-assessment]`, or human practitioner)
   - **4c. Privileged-surface**: would the reasoning trace itself breach confidentiality if logged to bus or ledger? (attorney-client, NDA-bound, secrets, security-incident detail → halt or redact; do not reason in shared audit-trail)
   - **4d. Empirical-probe-suffices**: is there a direct measurement that would replace ALL reasoning? (status checks, file contents, API state, version strings → run the probe instead of reasoning about it)
   - **4e. Adversarial-leak**: does revealing the reasoning structure weaken the position it would optimize? (negotiation strategy, red-team posture, security-by-obscurity → keep opaque; do not chain operators in shared trace)

   Full catalog with observed exemplars: `_internal/governance/2026-05-15-base120-negative-surface.md`.
5. **Falsifiability-at-right-layer** — does the observable measure the actual goal, or a Goodhartable proxy? "Sign without redline in 7 days" measures drafting speed, not legal sufficiency.

If any check flags, refuse the framing as stated. Reconstruct the prompt or route to the correct framework/skill BEFORE invoking apply/recommend.

**Falsifiability triple** (any falsifiable observable in a HUMMBL receipt must satisfy ALL three):
- (a) observable within bounded time
- (b) trust-root-separated (external writer ≠ observed agent)
- (c) measures the right thing (Goodhart-checked at correct layer)

Origin: AAR_2026-05-15 [basen] wickedness stress test (C1' + P1-P5 probes). Memory: `feedback_basen_preflight.md`.

## Execution

### Step 1: parse the argument
- If matches `<variant>:<rest>` → split variant + rest
- Else → variant = `base120` (default; the only LIVE variant)
- If `<rest>` matches operator code regex (e.g., `P1`, `IN7`, `CO3`) → Lookup mode
- If `<rest>` is keyword string → Search mode
- If `<rest>` starts with `apply ` → Apply mode
- If `<rest>` starts with `recommend ` → Recommend mode
- If `<rest>` == `variants` → Variants mode
- If `<rest>` matches `families <variant>` → Families mode

### Step 2: route to MCP server first

Preferred path: call basen-mcp tools

| Mode | Tool call |
|---|---|
| Lookup | `basen_operator_lookup(operator_id, variant)` |
| Search | `basen_family_browse(family, variant)` if keyword matches family; else fallback substring scan |
| Apply | `basen_apply(operator_id, input, mode="advisory")` |
| Recommend | `basen_recommend(problem_description, variant, top_k=3)` |
| Variants | read `basen://manifest` resource |
| Families | read `basen://{variant}/family/*` resources |

If basen-mcp is NOT registered in `.mcp.json` (current state as of 2026-05-14):
- Fallback A: try base120-mcp (external TS server, when wired) — `mcp__base120__*` tools
- Fallback B: read canonical JSON registry directly: `skills/base120-infrastructure/registry/base120_registry.json` (repo-root-relative in `hummbl-io/agents`; that root is `~/.agents` on agent-node and Delta). The previously documented `PROJECTS/.agents/cognition/data/base120_registry.json` does not resolve — verified missing 2026-09-20 — which silently pushed callers to the 22-model Fallback C.
- Fallback C: built-in reference table (see `[base120]` skill's quick reference)

Tag results explicitly:
- `[verified via basen-mcp]` — primary path
- `[verified via base120-mcp fallback]` — TS server fallback
- `[verified via canonical JSON]` — direct registry read
- `[UNVERIFIED — all MCP paths unavailable]` — no canonical lookup

### Step 3: render output

For Lookup mode:
```
BaseN | <variant>:<code> <Name>
═══════════════════════════════
Family: <family-name>
Definition: <text>
Priority: <N>
Related: <list>
Source: [verified via basen-mcp]
```

For Apply mode (Alignment report — MTSMU-wrapped):
```
BaseN Alignment | <variant> | <situation summary>
═════════════════════════════════════════════════
Problem: <1-2 sentence description>
Variant: <variant> (status: LIVE / PARTIAL / NOT canonicalized)

Operators applied:
  1. <variant>:<CODE> <Name> (Priority <N>)
     Why: <why this operator applies>
     Reveals: <the insight>
     Action: <concrete next step>
     Verify-method: [verify-after | cross-check | empirical | unverified]
     Uncertainty: [low | medium | high | unknown] — <one-line basis>
  2. ...

Transformation pattern: <dominant families>
Primary recommendation: <single most important action>

──── MTSMU Receipt ────
Reasoned-by: <invoker identity + session-id-or-tag>
Observed-agent: <who/what will run the Action(s)> — MUST ≠ reasoned-by for trust-root separation per Krineia §3.2
Registry hash: <Base120 v1.0.0 frozen-hash from PROJECTS/base120/Base120_Canonical_Model_Registry.yaml OR "[UNVERIFIED — registry not looked up]">
Falsifiability anchor: <ONE observable that would invalidate Primary recommendation> within <bounded time>
Stance (if stance-gate ran): <descriptive | prescriptive | strategic | negotiative>
Source: [verified via basen-mcp]
```

**MTSMU-wrap rationale** (per brainstorm 2026-05-15 Option A): the per-operator verify-method + uncertainty fields make each link in the chain audit-trail-shaped, not just the final recommendation. The MTSMU Receipt footer closes Krineia §3.2 trust-root separation (the agent who reasons must not be the agent whose state is observed). If `Observed-agent = Reasoned-by`, the chain is self-validating and fails the falsifiability triple's (b) leg — refuse to publish until separation is established or downgrade to operator-local memory only.

**Tag definitions**:
- `verify-after`: the Action produces an observable that will be checked against the Reveal claim within bounded time
- `cross-check`: the Reveal is verified by an independent reasoner (sibling session, peer agent) before the Action ships
- `empirical`: the Reveal cites a direct measurement (file content, API state, log line) — not inferred
- `unverified`: the Reveal is inference-only with no verification path; high-uncertainty by default

For Variants mode: emit the variant status table above + advisory: "Only LIVE variants support [basen] apply. PARTIAL variants may support read-only lookup if their registry has frozen-hash."

## Constraints

- **Default variant = `base120`** (the only LIVE variant as of 2026-05-14)
- **NEVER invent operators or families** — use only canonical registry data. Per `claim-honesty-protocol.md` §3 failure mode #1 (bracketed placeholders) and failure mode #5 (phantom references)
- **NON-canonicalized variants** — RETIRED from BaseN catalog (2026-06-13). HUAOMP and MTSMU are methodologies, not operator registries. Use their standalone skills (`/huaomp`, `mtsmu-*`) directly.
- **PARTIAL variants** (krineia/bki) support read-only lookup of their schemas. Krineia has receipt-chain format; BKI has measurement framework. Neither has a YAML operator registry. Tag results `[PARTIAL — variant is a different kernel type, not an operator catalog]`.
- **SY = Systems** (NOT Synthesis). Known hallucination pattern; always verify against registry.
- **Composition grammar deferred** per Q3 ratification — chains of operators are operator-discretion, not registry-enforced.
- **Tier-S verify-method tagging** (per M02 / M04 doctrine) — when used in Krineia receipts: prefix the Source line with `verify-after | cross-check | empirical | unverified`.

## Cross-variant queries

When a search spans multiple variants:
- `[basen] "feedback loop"` — default base120 first; surface PARTIAL variants as "also see krineia (receipt-chain format)" or "also see bki (measurement framework)"
- Cross-variant search is not yet supported by basen-mcp v0.1. Will be added in v0.2.
- HUAOMP and MTSMU are no longer in the BaseN variant table. Use `/huaomp` for epistemic breadth, `mtsmu-*` skills for rigor wrapping.

## Integration

- **/base120** continues working unchanged. Base120 is the first variant of BaseN; the `[base120]` skill is the variant-specific surface. `[basen] base120:P1` and `[base120] P1` are equivalent.
- **/aar** — when citing operators in AAR sections, prefix with variant if not base120 (`krineia:CRR3` once Krineia v1.0 ships).
- **/huaomp** — epistemic-breadth methodology. Standalone skill, not a BaseN variant.

## Related

- `_internal/governance/basen-architecture/SYNTHESIS.md` — full architecture
- `_internal/governance/basen-architecture/OPERATOR-DECISIONS-2026-05-14.md` — Q1-Q9 ratification record (BaseN promoted to first-class tier per Q1)
- `_internal/governance/basen-architecture/V1-q7-canonicalization-verification.md` — variant canonicalization status (substrate for variant table above)
- `_internal/scratch/basen-mcp/server.py` — basen-mcp server v0.1 draft (smoke-tested; awaiting operator approval for staging move + .mcp.json registration)
- `~/.agents/skills/base120/SKILL.md` — the canonical first-variant skill
- `$RUNTIME_MEM/feedback_base120_accuracy.md` (resolve via `~/.agents/scripts/resolve-memory.sh`) — Base120 canonicalization reference
- `$RUNTIME_MEM/project_basen_tier.md` — BaseN first-class ratification memory pin

## Open questions (passing through)

- Krineia v1.0 freeze target Mon 2026-05-18 — if ships, advance Krineia from PARTIAL to LIVE
- HUAOMP / MTSMU canonicalization path — currently no roadmap; operator may strategically defer indefinitely (the methodologies work fine as advisory frameworks without registries)
- BKI registry artifact — theory is rich but no schema; operator could commission a BKI registry build separately
