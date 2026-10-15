---
name: triage
description: Adopt / Adapt / Avoid evaluation for any external candidate (project, library, tool, model, idea). Returns a graded verdict with explicit risks, evidence, and ledger receipt.
version: 1.0.0
execution-mode: advisory
argument-hint: <candidate-name-or-url>
category: cognitive
status: tested
providers:
  required: [bash, python]
---
# [triage] — Adopt / Adapt / Avoid

Apply HUMMBL's external-candidate triage framework to a specific candidate. Output is a structured verdict that other agents and future sessions can consume as precedent.

## When this skill is right

- Someone (you, an agent, a swarm) recommended ADOPTING, LIFTING, COPYING, or DEPENDING ON an external project / library / tool / model / standard
- Before any decision-log ADR is written
- Before any new dependency lands in `pyproject.toml`
- Before any new agent identity is added to `agent-roster.md`
- Before any external code is vendored into a HUMMBL repo

If the question is "should we use X?", run [triage] on X.

## What this skill is NOT for

- Internal HUMMBL primitives — they're already in the stack
- Trivial decisions (a typo fix, a single-file utility) — overkill
- Operator-authority strategic decisions (those are not adopt/adapt/avoid; they're business decisions)

## Inputs

`[triage] <candidate>`

Candidate can be:
- A package name (e.g., `litellm`, `langfuse`)
- A GitHub URL (e.g., `https://github.com/vellum-ai/vellum-python-sdks`)
- A model name (e.g., `MiniMax-M2.5`, `Pi`)
- A standard/spec (e.g., `OpenTelemetry GenAI semconv`)
- An architectural pattern (e.g., `OpenCode pattern-matching permissions`)

## Steps

### 1. Identify the candidate
- Resolve to a primary URL (GitHub repo, official site, package registry)
- Note the source of the recommendation (which agent/swarm/session surfaced it)

### 2. Verify-pass (mandatory)
Per `~/.agents/rules/adopt-adapt-avoid.md`, dispatch a verify-pass agent OR run primary-source verification yourself. Read 2-4 sources:
- License file
- Install script or package metadata
- Top-level architecture entry points (README, main module)
- Active maintainership signals (recent commits, releases)

Grade GREEN / YELLOW / RED with named risks.

### 3. Apply evaluation dimensions
Per the rule, run through:
1. License compatibility
2. Maintainership signals
3. Provenance + vendor identity
4. ADR-001 admission gate (Tier-1/2/3)
5. Vendor data flow
6. Supply chain
7. IP overlap with HUMMBL primitives
8. Operational risk
9. Strategic alignment

Don't enumerate every dimension in the output — name only the load-bearing ones.

### 4. Compose with existing skills as needed
- License depth → `[license-audit]`
- Maintainership + supply chain → `[dependency-health]`, `[supply-chain-audit]`
- Security/operational risk → `[redteam]`, `[threat-model]`
- Web evidence → `[web-research]`
- For Gemini-authored candidates → `[gemini-audit]`

Don't auto-invoke; mention them in the output as "next-pass deepen if needed."

### 5. Issue verdict
ADOPT / ADAPT / AVOID / DEFER, with confidence HIGH / MED / LOW.

### 6. Write ledger entry
Mandatory. Tags: `triage`, `<verdict-lowercase>`, `<candidate-slug>`.

```bash
python -m hummbl_governance.cognition post-verified \
  --type discovery --scope project \
  --content "Triage <candidate>: <verdict>" \
  --evidence "<URL or file:line>" \
  --confidence <0.0-1.0> \
  --tags triage <verdict-lowercase> <candidate-slug>
# The skill invocation runtime injects the caller's canonical identity as agent.
```

### 7. Output the verdict per the rule's required format

## Output template

```markdown
## Triage: <candidate name>

**Verdict**: ADOPT | ADAPT | AVOID | DEFER
**Confidence**: HIGH | MED | LOW
**Date**: YYYY-MM-DD
**Triaged by**: <agent> (runtime-injected caller identity)
**Verify-pass**: <agent id> | "self-verified via N source reads"

### Why this verdict
<1-3 sentences naming the 2-3 load-bearing dimensions>

### Risks
- <specific risk 1, severity HIGH/MED/LOW>
- <specific risk 2, severity>

### Action
ADOPT → Admission path:
  - ADR-001 entry
  - License check + SBOM
  - Integration plan with timeline
ADAPT → Patterns to lift:
  - <pattern 1>
  - <pattern 2>
  What to replace: <list>
AVOID → Alternative: <internal build / different external / defer>
DEFER → Re-triage trigger: <time-bound or evidence-bound>

### Evidence
- <URL or file:line>
- <ledger entry id from related triage if precedent exists>

### Ledger receipt
clp-<id>
```

## Anti-patterns

- **No verdict without verify-pass.** Synthesis-only verdicts can propagate fabricated claims.
- **No DEFER without trigger.** Open-ended defers become AVOID by default.
- **No verdict without ledger entry.** Cross-session pattern recognition needs persisted decisions.
- **Don't confuse triage with implementation.** Triage produces a recommendation; the operator (or designated agent) decides whether to act.
- **Don't enumerate all 9 dimensions in output.** Name only the 2-3 load-bearing ones; verbose verdicts dilute signal.

## Examples

### Example 1: ADOPT verdict
```markdown
## Triage: OpenTelemetry GenAI semantic conventions

**Verdict**: ADOPT
**Confidence**: HIGH
**Date**: 2026-04-26
**Triaged by**: claude-code
**Verify-pass**: self-verified via opentelemetry.io docs + GitHub repo

### Why this verdict
Active OTel WG with quarterly releases; permissive Apache-2.0 license; established `gen_ai.*` namespace pattern; HUMMBL Krineia receipts can extend to `gen_ai.governance.*` cleanly.

### Risks
- Spec is still evolving (semconv v1.27 → opt-in stability path) — MED
- Custom `governance.*` top-level namespace would face WG resistance — LOW (use extension, not replacement)

### Action
ADOPT → Extend with `gen_ai.governance.*` attributes; file informational SEP concurrent with Krineia P1 ship; no new top-level namespace.

### Evidence
- https://opentelemetry.io/docs/specs/semconv/gen-ai/
- HUMMBL Krineia proposal v2 §10.10

### Ledger receipt
clp-<placeholder>
```

### Example 2: AVOID verdict
```markdown
## Triage: Vellum AI (vellum-ai/vellum-python-sdks)

**Verdict**: AVOID
**Confidence**: HIGH
**Date**: 2026-04-26
**Triaged by**: claude-code
**Verify-pass**: self-verified via gh search + GitHub stars

### Why this verdict
Name conflict — Vellum AI is an active LLM ops startup with multiple repos in adjacent space (81+69 stars). Naming our repo "vellum" collides with their search/SEO surface; using their SDK creates competitive-substrate dependency.

### Risks
- Search-engine confusion — HIGH for any HUMMBL adoption
- Vendor lock-in to their cloud platform — MED

### Action
AVOID → Alternative: HUMMBL primitive Layer 2 was originally named `verum` (Latin, distinctive — verified GitHub availability, dormant org since 2016, no relevant repos). Public-facing name renamed to `Krineia` on 2026-05-04 per namespace audit; `verum` retained in filenames, repo URL (hummbl-io/verum), and OTel attributes as INTENTIONAL_DEBT per the Krineia migration plan in hummbl-governance/docs/ecosystem/PLAN.md.

### Evidence
- https://github.com/vellum-ai/vellum-python-sdks
- https://github.com/vellum-ai/vellum-assistant

### Ledger receipt
clp-<placeholder>
```

## Composition with handoff-packet

A triage verdict can become a handoff packet (`~/.agents/rules/handoff-packet.md`) when delegated to another agent for execution:

```yaml
---
packet-version: 1.0
from: <agent>
to: <agent>
type: DISPATCH
task-id: triage-<candidate-slug>-<verdict>-action
priority: HIGH
execution-mode: side_effecting
---
```

The triage verdict's "Action" section becomes the handoff packet's "Recommended Action."

## Versioning

- v0.1 (2026-04-26) — initial draft. Adopted for immediate use across sessions.
- v1.0 (planned) — after first 5 triage verdicts; adjust based on what's working.

## Related

- `~/.agents/rules/adopt-adapt-avoid.md` — the rule (canonical framework)
- `[gemini-audit]` — adopt/adapt/avoid for Gemini-authored artifacts
- `[repo-init-secured]` — adopt/adapt/avoid baked into redteam-before-ship for new repos
- `[license-audit]` — license dimension deep-dive
- `[dependency-health]` — maintainership + supply-chain dimensions
- `[redteam]` — operational risk dimension
- `~/.agents/rules/stdlib-only.md` — ADR-001 admission gate (Tier 1/2/3)
- `~/.agents/rules/handoff-packet.md` — verdict → execution packet

## Skill Chains
- For delegate verify-pass to opencode -> `[cross-runtime-bridge]` (`python ~/bin/cross_runtime_bridge.py delegate`)

### Mandatory

None — this skill is a read-only evaluation of an external candidate; no upstream chain is required before issuing a verdict.

### Advisory

- License depth → `[license-audit]`
- Maintainership + supply chain → `[dependency-health]`, `[supply-chain-audit]`
- Security/operational risk → `[redteam]`, `[threat-model]`
- Web evidence → `[web-research]`
- Gemini-authored candidates → `[gemini-audit]`

## Authority

- **T1 (TRUSTED)**: Full access — run triage, post ledger entry
- **T2 (Active/High)**: Full access — run triage, post ledger entry
- **T3 (Medium)**: Full access — run triage, post ledger entry
- **T4 (Probationary)**: May run — read-only evaluation only (no ledger entry)
- **Operator**: Override any restriction
