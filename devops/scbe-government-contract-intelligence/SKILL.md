---
name: scbe-government-contract-intelligence
description: Investigate and prioritize U.S. federal and prime-contractor opportunities for SCBE swarm, autonomy, navigation, and AI-governance technologies. Use when evaluating SAM.gov/DIU/AFWERX/SBIR pathways, validating policy/news claims, producing capture plans, or preparing outreach packets for government-adjacent revenue.
---

# SCBE Government Contract Intelligence

## Quick Start
1. Validate market/policy claims first:
- check official sources in `references/federal-opportunity-sources.md` before writing positioning copy.
- label unverified claims as unverified.

2. Run a source scan:
- `python scripts/gov_contract_scan.py --keywords "swarm,autonomy,navigation,ai safety"`
- write outputs to `artifacts/contracts/`.

3. Build a capture packet:
- use `references/capture-packet-template.md`.
- keep a one-page summary per target lane (SBIR, DIU CSO, prime subcontract, OTA/BAA).

4. Produce monetization output:
- ranked lane list (where to bid first),
- top 5 leads with one-message outreach draft each,
- next 14-day action plan with owners.

## Workflow

### 1) Reality Check
- verify current events and policy claims with primary or top-tier reporting.
- separate facts from assumptions in every output.

### 2) Route Selection
- SBIR/STTR path: fast for R&D prototypes and phase funding.
- DIU/CSO path: faster transition lane for commercial tech.
- Prime subcontract path: near-term revenue through established contractors.
- Direct federal prime path: longer cycle, stronger compliance burden.

### 3) Qualification Gate
- confirm SAM entity registration readiness and basic compliance posture.
- ensure architecture claims map to demonstrable repo artifacts.
- reject claims that cannot be linked to code/tests/docs evidence.

### 4) Offer Framing
- position SCBE as risk-reduction and interoperability infrastructure:
- AI-to-AI coordination
- resilient navigation/control logic
- governance/auditability layer
- autonomous workflow orchestration

### 5) Capture Output
- ship a concise packet:
- problem statement
- capability map
- deployment model
- integration plan
- proof references
- pricing hypothesis

## Scripts
- `scripts/gov_contract_scan.py`: fetch official lane pages, score keyword relevance, emit JSON/MD briefs.

## References
- `references/federal-opportunity-sources.md`: official portals and what each is best for.
- `references/capture-packet-template.md`: one-page structure for qualified opportunities.

## Guardrails
- do not present rumor as policy.
- do not claim contract eligibility that is not verified.
- do not claim benchmarks without reproducible evidence.
- do not include secrets or private credentials in artifacts.
