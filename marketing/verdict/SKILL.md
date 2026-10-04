---
name: verdict
description: >-
  Architect-grade technology decision briefs — "which option should we pick, and
  why?" Takes a decision question (X vs Y vs Z for a stated context: library,
  database, framework, platform, buy-vs-build) plus your constraints, fans out
  parallel sub-agents to research each option's project health, community
  sentiment, technical claims, and operational story, then scores options across
  weighted criteria and emits an ADR-style recommendation with a full scorecard
  and cited evidence. Keyless; the recommendation is advisory — you decide. Use
  when the user must choose between technologies or approaches — e.g.
  "/verdict postgres vs mongodb for <use case>", "should we use Kafka or NATS",
  "compare X and Y", "buy vs build", "which framework for this". Also supports
  "/verdict revisit <brief>" to cheaply re-check a past verdict's revisit-when
  triggers. For community buzz on a single topic use pulse; for exhaustive
  fact-checked research use deep-research.
---

# verdict — technology decision briefs

`/verdict <option A> vs <option B> [vs <option C>] for <context> [constraints]`
`/verdict revisit <path-to-previous-brief>` — re-check an old verdict (see Revisit mode)

Answer one question: **given this context, which option should we pick, and what
evidence supports that?** You research every option the same way, score against
explicit weighted criteria, and write the decision up so it can be defended in a
design review — or revisited later when the facts change.

## Step 0 — Frame the decision

Extract from the request (ask **1–2 questions only if** genuinely blocking):

- **Options** (2–4). If the user names only one ("should we use X?"), add the
  status-quo/do-nothing option and the 1–2 strongest alternatives — say you did.
- **Decision context:** what is being built, scale (users/QPS/data volume), team
  size and existing skills, current stack, timeline.
- **Constraints & dealbreakers:** licensing limits, budget, compliance,
  must-run-on-prem, language lock-in, etc.
- **Criteria weights** — defaults below; honor plain-language overrides
  ("ops burden matters most", "we optimize for hiring").

State every assumption you make in the brief header. A verdict against the wrong
context is worse than no verdict.

## Step 1 — Fan out: parallel research sub-agents (per option)

Spawn one research sub-agent **per option**, concurrently (one message, multiple
`Agent` calls, `subagent_type: "Explore"`). Each covers five angles and returns
structured findings — every claim with a `url` + 1-line evidence, anything
unverified marked as such:

1. **Project health** (for OSS/tools; skip for pure approaches): GitHub keyless
   REST — stars trend, commit/release cadence, open-vs-closed issue velocity, bus
   factor, age, backing org/funding. A beautiful README with a dead repo behind
   it is a trap; this angle catches it. **Note:** keyless GitHub REST allows
   60 req/hr shared across all sub-agents — budget calls, and on a 403
   rate-limit mark the angle **unknown** rather than retrying in a loop.
2. **Community sentiment:** HN Algolia (`hn.algolia.com/api/v1/search?query=...`)
   + web search + Reddit fallback — what practitioners report *after adopting*:
   praise, recurring pain points, migration-away stories. Weight experience
   reports over launch-day hype — and over SEO comparison content ("X vs Y in
   2026" listicle farms are marketing surface, not adoption evidence; a real
   practitioner thread outweighs ten of them).
3. **Technical claims:** official docs + independent benchmarks/comparisons for
   the capabilities the context actually needs. **Label every claim vendor-made
   vs independently verified.** Note version/date — a 2022 benchmark may be void.
4. **Operational story:** licensing (and any recent license *changes*), managed
   vs self-hosted options, pricing shape, upgrade pain, hiring pool / learning
   curve for the stated team.
5. **Security posture:** CVE history and severity pattern, GitHub security
   advisories, how fast past vulnerabilities were patched, safety of the default
   configuration, and any compliance certifications the context requires. This
   evidence feeds the *Maturity & health* and *Operational burden* scores (no
   separate criterion) — but an unpatched-critical-CVE pattern can be a
   dealbreaker in its own right.

If an angle returns nothing usable, record it as **unknown** — never fabricate.

**Lossless hand-off:** each sub-agent writes its full findings to
`out/verdicts/.work/<option>.md` and returns a compact summary; score in Step 2
from the files, not the summaries — the evidence that decides a verdict must
not be flattened by the relay.

## Step 2 — Score

Score each option **0–10 per criterion**, weighted. Defaults (overridable in
Step 0):

| Criterion               | Weight | What it measures                                       |
| ----------------------- | ------ | ------------------------------------------------------ |
| Fit for requirements    | 30%    | Does it actually do what this context needs, natively? |
| Maturity & health       | 20%    | Project vitality, stability, ecosystem, longevity risk |
| Team & stack fit        | 20%    | Learning curve vs existing skills; integration cost    |
| Operational burden      | 15%    | Run/upgrade/monitor cost at the stated scale           |
| Cost & licensing        | 15%    | License risk, pricing shape, lock-in                   |

If a criterion doesn't apply, mark it N/A and renormalize the rest — say so.
**Dealbreakers** (license incompatible, can't meet a hard constraint, project
effectively abandoned) disqualify the option outright regardless of score —
called out explicitly, not averaged away.

Compute a weighted total /10 per option. **Close calls (≤0.5 apart) are ties** —
say so honestly and let the tiebreaker be a context factor, not false precision.

## Step 3 — Emit the brief (ADR-style)

Render the brief **in chat** per `references/adr-template.md` (read it when
you reach this step), then save as `.md` + a self-contained `.html` (see Output
files). Cite inline with linked URLs; label vendor claims.

## Revisit mode

`/verdict revisit <path>` (or "revisit the postgres verdict") turns the
**Revisit when** section from a wish into a mechanism. Much cheaper than a full
re-run:

1. Read the previous brief (find it in `out/verdicts/` by slug if only a topic is
   given). Extract the recommendation, scores, dealbreakers, and the **Revisit
   when** triggers.
2. Research **only the triggers** plus two standing checks: any license change
   and any major-release/abandonment signal since the brief's run date. One
   Explore sub-agent per option, narrow scope — not the full five angles.
3. Emit a short **addendum**, not a new brief: per trigger — fired / not fired /
   unknown, with citation — and an overall call: **verdict stands / weakened
   (why) / overturned → recommend a full re-run**. Never silently flip a
   recommendation from a partial check; an overturn verdict recommends the
   re-run, the human decides.
4. Save as `out/verdicts/<slug>-revisit-<YYYY-MM-DD>.md` (markdown only — no HTML
   for addenda) and link the original brief in its header.

## Output files

Save to `./out/verdicts/` in the current working directory:

- `out/verdicts/<slug>-<YYYY-MM-DD>.md` — the brief verbatim.
- `out/verdicts/<slug>-<YYYY-MM-DD>.html` — a **bespoke, distinctively designed**
  version. Self-contained: inline `<style>`, **no JavaScript, no external
  requests** (system fonts), links preserved, the scorecard and recommendation
  as first-class visual elements, responsive, print-friendly.

`<slug>` = options joined by `-vs-`, lowercased. Compute the date with a shell
command (`date +%F`) — do not guess. Create `out/verdicts/` if needed. Briefs
make good shared history, but they may contain internal project context —
committing them is the user's call, not the skill's.

Design the HTML via the **`frontend-design`** skill: subject is *an engineering
decision record*; the page's one job is to make the recommendation, scorecard,
and dealbreakers scannable in ten seconds, with the full evidence beneath.
Design changes presentation only — never scores, evidence, or citations. Fall
back to a clean self-contained no-JS layout if the skill is unavailable.

Tell the user the two saved paths at the end.

## Guardrails

- **Advisory, not authoritative.** Recommend with evidence; the human decides.
  Never present a close call as decisive.
- **Symmetric research.** Every option gets the same five angles — no
  strawmanning the option you suspect will lose.
- **Vendor claims labeled.** Marketing pages are evidence of intent, not of
  performance. Independent verification or it's marked "vendor claim."
- **No fabrication.** Every score traces to cited findings; unknowns stay
  unknown and are listed in the brief.
- **Keyless.** Never ask for API keys; degrade gracefully.
- **Context is king.** The same two options can produce opposite verdicts for
  different contexts — restate the context prominently so the brief can't be
  misapplied later.
