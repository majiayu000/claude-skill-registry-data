---
name: payprobe-external-positioning
description: >
  Load when writing or reviewing ANYTHING that leaves the repo: README edits,
  release notes, blog posts, papers, conference talks, the GitHub profile page,
  the presentation deck, website copy, comparison tables, or answers to "can we
  say X publicly?". Covers: PolyForm Noncommercial licensing rules (source-available,
  NOT open source), the employer-independence disclaimer and what it forbids,
  the audit of quantitative claims (50K connections / 10K ops/sec / 20K TPS —
  which are measured vs targets), the novel-vs-known map against jPOS / chaos
  tools / commercial scheme simulators, what must be PROVEN before each SOTA
  claim, reproducibility standards for external artifacts, and the release
  checklist. Keywords: license, open source, OSS, PolyForm, noncommercial,
  disclaimer, employer, positioning, claim, benchmark, publish, release, paper,
  blog, announcement, marketing, competitor.
---

# PayProbe External Positioning — license, claims, and proof discipline

Everything PayProbe says to the outside world must survive two tests:
**is it legally clean?** and **can we prove it?** This skill is the rulebook
for both. It is grounded in the repo as of 2026-07-03; re-verification
commands are at the end.

**Prime directive:** a number, capability, or comparison may be claimed in an
external artifact ONLY if a reproducible measurement or a runnable
demonstration in this repo backs it. Everything else is labeled a *target*,
*design goal*, or *planned* — or it is cut.

---

## 1. Licensing discipline — PolyForm Noncommercial 1.0.0

**The license** (root `LICENSE`, verbatim PolyForm Noncommercial 1.0.0,
`https://polyformproject.org/licenses/noncommercial/1.0.0`, Required Notice:
"Copyright 2025 David Sakhelashvili (https://github.com/pay-probe)").

| It permits | It forbids / requires |
|---|---|
| Any **noncommercial** use: personal study, research, experiment, hobby projects | **Commercial use** — not permitted; commercial licensing is by separate contact with the author |
| Use by charitable, educational, public-research, public-safety/health, environmental, or **government** organizations, regardless of funding source | Sublicensing or transferring your licenses |
| Distributing copies, with or without changes | Distribution **must** pass along the license terms (or their URL) and every `Required Notice:` line |
| Changes and new works for any permitted purpose | Patent license terminates if you claim the software infringes a patent |
| Fair-use rights (not limited by the terms) | Violations: 32-day cure window after written notice, else all licenses end |

**Vocabulary rules — non-negotiable:**

1. **Never call PayProbe "open source."** It is **source-available**. The
   README's License section says this explicitly: the OSI open-source
   definition does not allow restrictions on commercial use, and PolyForm
   Noncommercial restricts exactly that. Saying "open source" in a talk, post,
   or README edit is a positioning bug — file it and fix it like one.
2. Approved one-liner (matches README title line): *"Source-available
   integration testing & simulation framework for distributed backend systems."*
3. **Why this license:** it creates deliberate legal distance — the project is
   shareable for study/research/nonprofit/government use while its author
   retains commercial rights, and the noncommercial restriction removes any
   suggestion that the project competes commercially with, or belongs to, an
   employer. This pairs with the independence disclaimer (next section);
   license choice and disclaimer are two halves of one posture.
4. Any distribution (zip, fork, package, demo bundle) must carry `LICENSE`
   including the `Required Notice:` line. There are **no per-file license
   headers** in the codebase (verified: no `Required Notice` in `packages/`
   source) — the file-level LICENSE is the single carrier, so never drop it.
5. The license badge in `README.md` and `.github/profile/README.md` must say
   *PolyForm Noncommercial 1.0.0* and link to `LICENSE`.

---

## 2. Independence discipline — the employer disclaimer

`README.md` carries this disclaimer near the top. Quote it exactly; do not
paraphrase it in external materials:

> This project is an independent, source-available infrastructure testing and
> simulation framework. It is not affiliated with my employer and does not
> include employer code, confidential information, internal specifications,
> production data, customer data, credentials, configurations, or proprietary
> business logic. All development is performed outside working hours using
> personal equipment.

The README License section reinforces it: *"It is not affiliated with,
endorsed by, or built from the proprietary materials of any employer."*

**Rules that follow (apply to every external artifact and every commit):**

| Rule | Practical meaning |
|---|---|
| No employer references | Never name, imply, or "as used at…" any employer in docs, talks, commit messages, or examples |
| No proprietary specs | Member-only scheme documents (e.g. VISA V.I.P. field-level specs, BASE I/II edit tables) are neither committed nor encoded from memory. `docs/simulators/visa-scheme.md` is the model: it states DE 62/63 are treated as opaque **because** the sub-field layouts are member-only |
| Generic positioning | The product is framed as testing "distributed backend systems" — payments is a domain it serves, not an employer system it mirrors. Keep diagrams generic (App Server, Message Switch, External Host) |
| Test data only | No production data, customer data, credentials, or live PANs — ever. Example PANs are test numbers (e.g. `4111111111111111`); keys are test keys (payShield sim uses a test LMK) |
| Disclaimer travels | Any substantial external artifact (deck, paper, profile page) repeats the independence + source-available framing. `presentation/payprobe-deck.html` and `.github/profile/README.md` already exist — check them when the README posture changes |

---

## 3. Claims audit — every public number, classified

Classification key: **measured-in-repo** (a reproducible measurement artifact
exists in the repo) · **design-target** (the number sized the design; honest
as a *target*) · **aspiration** (marketing shorthand; no evidence either way).

Audit result as of 2026-07-03: **the repo contains NO benchmark artifacts** —
no committed load-run results, no benchmark docs, no perf-test outputs. Every
quantitative claim below is therefore a design-target or aspiration until a
measurement lands.

| Claim | Where it appears | Class | Evidence status |
|---|---|---|---|
| "50K concurrent connections" | `README.md` (Key Features + architecture diagram), `packages/worker/README.md`, `docs/architecture/overview.md`, `.github/profile/README.md`, `presentation/payprobe-deck.html` | **design-target** | The engine docstring (`packages/worker/engine/engine.py`) says the concurrency semaphores are *sized to* "the spec's 50K/10K ceilings." That is capacity sizing, not a measurement. No artifact shows 50K sockets held. |
| "10,000 operations/sec — sustained throughput against real backend infrastructure" | same places | **design-target**, and the "sustained… against real backend infrastructure" phrasing **overstates** — no sustained-run artifact exists in the repo. Soften to "designed for" until measured. |
| 20K TPS / 100K connections | `docs/architecture/overview.md` ("**Targets**: 20K TPS, 100K concurrent connections (distributed across worker fleet)"), `docs/history/TEST-CONSOLE-BUILD-SPEC.md`, `packages/worker/load_worker.py` docstring | **design-target** — and honestly labeled as such at the source. Keep the word "targets" attached wherever these numbers travel. |
| "Adding a new adapter takes ~2 hours" | `README.md` (Adapters section) | **aspiration** | No timing evidence. Fine as internal folklore; do not put in a paper. |
| "~30 users" (portal) | `README.md` architecture diagram | **design-target** (sizing assumption) | Not a measured user count. |
| "Up and running in 10 minutes" | `README.md` docs table (quick-start) | **aspiration** — but cheaply testable; time a clean `docker compose up` before quoting it externally. |

**The repo's own review agrees:** `docs/history/project-review.md` warns that the
in-process load fallback "can starve the orchestrator… at the advertised
20K TPS" and concludes the load subsystem "should graduate from in-process
fallback to a real, persisted, externally-scaled fleet **before it's leaned
on at 20K TPS**." Quoting the big numbers externally while that caveat stands
unresolved is oversell.

**Rules:**

1. External artifacts may state a number only with a reproducible measurement
   behind it (Section 6 format). Until then, write "designed for" /
   "targets" — never bare "does."
2. When a measurement DOES land, commit the artifact (config, environment
   spec, raw output, commit hash) under `docs/` so the claim is auditable,
   then update this table's classification.
3. Existing README/profile/deck numbers are grandfathered *inside the repo*
   but are the first thing to re-verify at any release (Section 7). Do not
   propagate them into new external artifacts without measurement.

---

## 4. Novel-vs-known map — the four SOTA ambitions

For each ambition: what already exists in the ecosystem (**general knowledge**,
from training data, not repo-verified — label it as such in any paper and
re-check versions/status before citing), what PayProbe's specific angle is
(repo-verified), and the proof bar before any public claim.

### 4.1 Full-fidelity scheme simulation

- **Known ecosystem:** jPOS (mature Java ISO 8583 framework with binary/BCD/
  EBCDIC packagers and channel machinery), j8583 and Python iso8583 libraries,
  Kaitai Struct for declarative binary parsing, Wireshark dissectors; on the
  commercial side, certification-grade scheme simulators and brand test tools
  (e.g. Paragon FASTest-class products, Visa/Mastercard certification
  environments). *(general knowledge)*
- **PayProbe's angle:** simulators are integrated into one platform — the same
  responder machinery (`TcpResponder`) feeds the saved-simulator registry,
  live metrics, chaos injection, and load testing; VISA Base I-style,
  payShield 10K HSM, and CyberSource REST simulators exist with optional real
  card cryptography (CVV2/PVV/ARQC, DUKPT). *(repo-verified: `docs/simulators/`,
  `packages/worker/tests/test_visa_simulator.py`, `test_payshield_sim.py`,
  `test_dukpt_pvv.py`)*
- **Proof bar before claiming publicly:**
  - "Spec-exact VISA" requires the follow-on phase described in
    `docs/simulators/visa-scheme.md` — today it is a **functional Base I**
    simulator built from *public* ISO 8583:1987 structure; DE 62/63 are
    opaque echo fields because the V.I.P. field-level specs are member-only.
    The claimable sentence today is exactly the doc's own framing: a
    functional Base I-style simulator, **not** byte-exact V.I.P.
  - Binary ISO 8583 (binary bitmaps, BCD/EBCDIC, binary length prefixes) was
    scored the highest-impact gap in `docs/standards-gap-analysis.md`
    (2026-06-20) — verify current codec status before claiming binary
    interop (see Provenance).
  - Fidelity claims need conformance evidence: a published test-vector suite
    or a real-host interop trace, committed.

### 4.2 Time-travel observability (Chronoscope)

- **Known ecosystem:** record/replay debuggers (rr, UDB), distributed tracing
  (OpenTelemetry, Jaeger, Zipkin), deterministic-simulation testing
  (FoundationDB-style, Antithesis). *(general knowledge)*
- **PayProbe's angle:** a live topology map with an 8-minute replay buffer,
  time scrubber, and replay JSON export/import for offline review
  (`packages/portal/src/app/topologies/chronoscope/` — recorder service,
  time-scrubber, chronicle panel, node inspector), plus wire-level execution
  traces on step outcomes. Replay of a *simulated payment network's* state,
  integrated with the test engine, is the differentiator.
- **Proof bar:** publish only with (a) a stated fidelity contract — what is
  recorded vs sampled vs dropped, buffer limits; (b) at least one
  reproducible debugging case study where replay found a fault that live
  observation missed, with the exported replay JSON as the artifact.

### 4.3 AI-operated test platform

- **Known ecosystem:** MCP servers over dev tools are now common; LLM test
  generation and agentic QA tools exist broadly. *(general knowledge)*
- **PayProbe's angle:** the platform is operable end-to-end by an agent —
  MCP server (`packages/mcp-server`) proxying scenario-service and
  orchestrator, an NL→flow scenario assistant, and a tool registry with
  change-journal/guardrails in scenario-service (`agent_tools.py`).
- **Proof bar:** "AI-operated safely end-to-end" needs a demonstrated,
  repeatable agent session (create → run → diagnose → report) with the
  guardrail/change-journal evidence attached, plus a stated safety envelope
  (what the agent may not do). Until then say "AI-operable via MCP," not
  "AI-operated."

### 4.4 Chaos-certified payment resilience

- **Known ecosystem:** Chaos Monkey lineage, Gremlin, Chaos Toolkit,
  LitmusChaos, AWS FIS; the Principles of Chaos Engineering. *(general
  knowledge)* None of these emit a *payments-specific resilience
  certificate*.
- **PayProbe's angle:** chaos injection on protocol simulators (fault dial +
  timed storms; `packages/worker/tests/test_chaos.py`) scored against a
  concurrent load run into a pass/fail certificate
  (`packages/orchestrator/api/resilience.py`: availability, absorption,
  recovery, latency gates and a grade).
- **Proof bar:** "certification methodology" is a strong word. Before using
  it publicly: publish the scoring rubric and gate thresholds with rationale,
  show score stability across repeated identical runs (inter-run variance),
  and show the score discriminates (a deliberately weakened system fails).
  Until then: "resilience scoring," not "certification standard."

---

## 5. The honesty precedent — keep the genre alive

`docs/standards-gap-analysis.md` is the house model for external honesty:
a claimed capability area, what actually exists (with file references), the
gaps stated plainly ("ASCII representation only… will not interoperate with a
binary-encoded host", "❌ missing"), a scorecard, and priorities. Note its
discipline: *"Grounded in the codebase as of 2026-06-20, not aspiration."*

Two lessons:

1. **Write gap analyses, not brochures.** Any paper or long-form post gets a
   "Limitations" section written in this register, or it does not ship.
2. **Date-stamped honesty goes stale in both directions.** That document
   marks DUKPT "❌ missing" — but DUKPT has since been built
   (`packages/worker/tests/test_dukpt_pvv.py`, `engine/crypto_tools.py`).
   Stale *understatement* is also a claims bug: re-verify gap documents
   before quoting them externally, in either direction.

`docs/history/project-review.md` is the same genre applied to engineering quality —
cite it internally, and let its unresolved High items veto related external
claims (e.g. the 20K TPS caveat in Section 3).

---

## 6. Reproducibility standard for external artifacts

Any paper, blog post, release note, or talk that states a number or
demonstrates a behavior must include (or link to a committed doc containing):

| Element | Requirement |
|---|---|
| **Pinned commit** | Full SHA of the exact tree measured (`git rev-parse HEAD`). Not a branch name. |
| **Exact commands** | Copy-pasteable, repo-root-relative, from clean checkout to result — e.g. `docker compose -f infra/docker/docker-compose.yml up --build`, then the specific run/load-run invocation with its full config JSON. |
| **Environment spec** | Hardware (CPU model, cores, RAM), OS, Python version, Docker version, network topology (loopback vs LAN — decisive for TPS/connection numbers), and whether targets were mock or real. |
| **Expected numbers with tolerance** | "20,150 TPS ± 5% over 10 min" — a point estimate with run duration and variance, never a bare peak. State how many repetitions. |
| **Artifacts** | Raw output committed or attached: load-run summary JSON, JUnit XML (`GET /runs/{id}/junit`), resilience certificate JSON, replay export — whatever the claim rests on. |
| **Limitations** | The Section 5 register: what was NOT measured, known caveats (e.g. in-process fallback vs external worker fleet). |

A reader with comparable hardware must be able to reproduce the headline
number from the pinned commit using only the artifact's instructions.

---

## 7. Release checklist

Run top to bottom before any tag, announcement, or artifact publication:

- [ ] **Suite green:** `make test` passes at the release commit (the CI gate;
      also `.github/workflows/ci.yml` portal build + `security-scan.yml`
      Syft SBOM / Trivy are green).
- [ ] **Version:** there is no single canonical version today — versions are
      scattered (orchestrator FastAPI `version="0.1.0"` in
      `packages/orchestrator/api/main.py`, scenario-service `0.2.0` in
      `packages/scenario-service/api/main.py`, portal `0.1.0` in
      `packages/portal/package.json`). Pick the release version and update
      all three consistently; note the divergence until unified.
- [ ] **Changelog:** no `CHANGELOG.md` exists (verified 2026-07-03). Create or
      update one for the release; derive entries from `git log` and
      `docs/history/PROGRESS.md`, written in the Section 5 register.
- [ ] **Claims re-verified:** walk the Section 3 table. Any number in
      README / `.github/profile/README.md` / `presentation/` that is still a
      design-target either carries the word "target/designed for" or ships
      with a fresh Section 6 measurement.
- [ ] **License intact:** `LICENSE` present and unmodified, `Required Notice:`
      line preserved, README License section still says source-available /
      not OSI open source, badges correct.
- [ ] **Disclaimer intact:** the employer-independence disclaimer (Section 2)
      is verbatim in `README.md`, and any new external artifact repeats the
      independence + source-available framing.
- [ ] **No proprietary content:** grep the diff since last release for scheme
      member-only material, employer references, live-looking PANs or real
      credentials.
- [ ] **Docs of record updated:** `docs/history/PROGRESS.md`, `ROADMAP.md` (unchecked items
      stay unchecked — Grafana, Helm chart, Python SDK, AMQP adapter, scenario
      versioning are open roadmap items, not features), and gap analyses
      refreshed if quoted.

---

## When NOT to use this skill

- **Internal docs, ADRs, Diátaxis structure, house style, PROGRESS/spec
  templates** → `payprobe-docs-and-writing`.
- **How to run experiments, evidence bars, hypothesis discipline, idea
  lifecycle** → `payprobe-research-methodology`.
- **The substance of the four SOTA ambitions (why SOTA fails, first steps,
  falsifiable milestones)** → `payprobe-research-frontier`; this skill only
  governs what may be *said publicly* about them.
- **What counts as test evidence inside the repo** → `payprobe-validation-and-qa`.
- **Change gating and the non-negotiables** → `payprobe-change-control`.

---

## Provenance and maintenance

Authored 2026-07-03 against the live repo (HEAD at commit `1b377c8`). Every
file path, quote, and classification above was verified by direct read or
grep on that date. Ecosystem tool references in Section 4 are general
knowledge (training data), not repo-verified. Re-verify before relying:

- License text + notice: `head -5 LICENSE && grep -n "Required Notice" LICENSE`
- Disclaimer + license section wording: `grep -n -A5 "Disclaimer" README.md && grep -n "source-available" README.md`
- Quantitative claims inventory: `grep -rn "50K\|50,000\|10,000 op\|20K TPS\|100K conn" README.md docs/ packages/*/README.md .github/profile/ docs/history/TEST-CONSOLE-BUILD-SPEC.md`
- Benchmark evidence (expect nothing until one lands): `grep -rli "benchmark" docs/ examples/ && ls docs/*bench* 2>/dev/null`
- VISA fidelity wording: `sed -n '14,30p' docs/simulators/visa-scheme.md`
- Binary ISO 8583 codec status (gap-analysis staleness check): `grep -rn -i "binary bitmap\|BCD\|EBCDIC" packages/worker/engine/ packages/worker/adapters/ | grep -v tests`
- DUKPT-now-exists staleness example: `ls packages/worker/tests/test_dukpt_pvv.py`
- Version scatter + changelog: `grep -rn "version=" packages/orchestrator/api/main.py packages/scenario-service/api/main.py; grep -n '"version"' packages/portal/package.json; ls CHANGELOG* 2>/dev/null`
- Chronoscope module: `ls packages/portal/src/app/topologies/chronoscope/`
- Resilience scorer: `ls packages/orchestrator/api/resilience.py`
