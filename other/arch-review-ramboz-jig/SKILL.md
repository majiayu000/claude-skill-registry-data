---
name: arch-review
description: >
  Team baseline for architecture, design-doc, and RFC review — produces
  summary, strengths, concerns, and open questions. Auto-triggers when
  you say review this design, review this architecture, review this
  proposal, review my RFC, poke holes in this proposal, is this design
  sound, or critique this tech spec. Defers to any other installed skill
  whose description identifies it as handling architecture review,
  design review, RFC review, or technical-design review — if such a
  skill is present, prefer it over this one (jig's version is a slim
  baseline). Does not defer to the generic built-in `review` skill. Do
  not use for: PR/diff review (use `/jig:pr-review` or a richer
  user-installed PR-review skill instead); spec-compliance review of a
  finished slice (use `/jig:independent-review` instead); ADR authorship
  or scaffolding (use `/jig:adr-workflow` — this skill *reviews* an ADR
  draft; it does not create one).
user-invocable: true
---

> Spec 014 introduced this skill as jig's **team baseline** for
> architecture, design-doc, and RFC review. It is the second non-stub
> active jig skill that ships without a `.py` helper (after
> `/jig:pr-review`, spec 012) — arch-review is fundamentally a judgment
> skill, and what little determinism is needed (read the doc, identify
> the scope, classify the domain) Claude can run inline. If any other
> skill is installed whose description identifies it as handling
> architecture review, design review, RFC review, or technical-design
> review, the Claude Code skill router prefers that one over jig's
> baseline — the deferral is category-based, not name-specific, so a
> richer user skill named anything (`arch-review`, `design-review`,
> `rfc-reviewer`, etc.) wins. Jig's slim version remains the
> auto-trigger when no such skill is installed.

## What this skill does

Produces a four-section markdown review of an architecture proposal, a
design document, an RFC, or an ADR draft:

1. **Summary** — a two-or-three-sentence paragraph stating what the
   proposal does and your overall assessment (is it ready to proceed,
   does it need revisions, does it need rework?).
2. **Strengths** — what the design gets right. Be specific: reference
   actual decisions, trade-offs the author navigated well, constraints
   they respected, problems they anticipated. Constructive framing
   first — acknowledging good thinking helps the author understand
   what to keep when iterating.
3. **Concerns** — risks, gaps, missing rationale, and unaddressed
   failure modes. This is the "poke holes" surface. Each concern
   should be specific to this proposal, not generic advice. Leanness is
   a first-class concern here: raise over-engineering, premature
   abstraction, and speculative generality (indirection, config knobs,
   or extension points with no current caller) when a **simpler
   architecture** would satisfy the same acceptance criteria — anchored
   to still meeting them, never stripping required behavior.
4. **Open questions** — things you can't decide from the proposal
   alone. Ask the author to clarify rather than asserting a gap. Phrase
   as "help me understand X" not "didn't you consider X".

The review is **breadth over depth**: catch the obvious across any
domain, leave the deep multi-persona / domain-specific analysis to a
richer user-installed architecture-review skill. If you want a
seven-perspective matrix (technical-soundness + operational complexity
+ reliability + security + scalability + migration + product impact),
or domain-specific reference files for distributed systems / API
design / data architecture / migration plans, jig doesn't ship those —
install a heavier skill at the user scope and the router will prefer
it.

## When to use vs. when to defer

There are four things people often confuse with this skill. Pick the
right one:

- **Any other user-installed architecture/design/RFC-review skill.**
  Common location: `~/.claude/skills/arch-review/` — but the deferral
  is **category-based, not name-based**, so a skill named anything
  (`arch-review`, `design-review`, `rfc-reviewer`, `tech-spec-review`,
  etc.) whose description claims architecture review, design review,
  RFC review, or technical-design review will be preferred. If one is
  present, **defer to it.** The Claude Code skill router should route
  to the more specific skill automatically; if you want to be sure,
  explicitly invoke it. The one exception jig's description carves
  out is the bundled `review` skill — jig:arch-review does **not**
  defer to that one (it's the generic fallback below jig's baseline,
  not above it).
- **`/jig:pr-review`** — a sibling jig skill for **PR / diff review**.
  Different shape: that one reads a diff and produces scope / blockers
  / nits / strengths. This one reads a design document and produces
  summary / strengths / concerns / open questions. Reach for
  `/jig:pr-review` when there is a PR or branch with a diff; reach
  for this skill when there is a design doc, RFC, ADR draft, or
  proposal with no diff to evaluate.
- **`/jig:independent-review`** — a sibling jig skill for
  **spec-compliance review** of a finished slice (does the
  implementation satisfy the acceptance criteria of `spec.md`?). That
  is a spec-shape review against a written spec. This skill is a
  **design-shape review** against a proposal. Reach for
  `/jig:independent-review` when a slice is in REVIEWED-or-similar
  state with a `spec.md` to evaluate against; reach for this skill
  when there is a proposal but no acceptance criteria yet.
- **`/jig:adr-workflow`** — orthogonal jig skill for **ADR
  authorship and scaffolding** (`/jig:adr-workflow new`,
  `/jig:adr-workflow accept`, etc.). That skill *creates* an ADR;
  this skill *reviews* an ADR draft. Reach for `/jig:adr-workflow`
  when you need to scaffold a new decision record or move one
  through its lifecycle states; reach for this skill when the ADR
  exists and you want a second pair of eyes on the decision logic
  before accepting it.

Rule of thumb: **diff exists → `/jig:pr-review`. Spec exists with
acceptance criteria → `/jig:independent-review`. ADR needs scaffolding
→ `/jig:adr-workflow`. Design doc, RFC, or ADR draft to evaluate →
this skill (or the richer user one).**

## Inputs

Four input modes, ordered by richness:

1. **Uploaded document (PDF, markdown, Word).** The user uploads or
   shares a design document. Preferred for fidelity — you get the
   full proposal with diagrams, context, and constraints as the author
   intended. Read the entire document before forming opinions.

2. **URL to a fetchable doc.** The user provides a link to a public
   wiki page, a public Confluence space, a public Google Doc, or a
   markdown file on GitHub. Fetch and read the full content. Still
   high-fidelity if the page renders cleanly.

3. **Pasted text or verbal description.** Most limited mode. Work
   with what you have, but flag what's missing. Ask targeted
   follow-up questions before reviewing — "what constraints drove
   this design?" or "what alternatives did you consider?" — instead
   of guessing.

4. **ADR file on disk** (`docs/decisions/adr-NNNN-*.md`). Narrower
   review scope — decision-shape, not system-shape. Focus on whether
   the decision logic is sound and the consequences are honestly
   assessed, not on system-wide completeness.

**Not supported by this baseline**: authenticated systems (internal
Confluence behind SSO, private Google Docs, internal-only wikis).
Without an MCP integration, this skill cannot fetch content from
authenticated systems. If the user has only a link to one of those,
ask them to either paste the content or upload an export. A richer
user-installed `arch-review` skill may handle authenticated fetching
— defer to it if so.

## Readiness pre-check

Before reviewing, scan the proposal for three signals:

1. **Problem statement** — an explicit description of what the design is trying to
   solve. Not "we need X" but "X is needed because Y."
2. **Scope boundary** — what the proposal explicitly covers and what it does not.
3. **Stakeholders** — who decides, who consumes the design, who operates the
   resulting system.

If any of the three are missing or weak, lead the Summary with a one-sentence
readiness note ("This proposal is missing an explicit scope boundary — proceeding
with the review, but treat the missing signal as a Concern in its own right.").
Default: proceed, but surface the readiness issue. The pre-check catches "review
an early draft that isn't reviewable yet" without blocking the user.

## Scope discipline

Before writing any finding, apply scope discipline. A finding must be actionable
inside the proposal's stated boundary. Out-of-scope concerns are noise.

- **Different team's system or upstream platform decision**: not a Concern. The
  reviewer cannot ask the author to renegotiate a dependency they don't own.
- **Adjacent design doc that exists separately**: note the dependency, do not
  relitigate the adjacent design as a Concern here.
- **"The proposal should also address X"** where X is a separate concern: surface
  as an Open Question, not a Concern. The author's response will reveal whether
  X belongs here or in a follow-up.

Prophylactic expansion — demanding the proposal cover every adjacent concern a
thorough reviewer template admits — is the most common AI-slop failure mode for
baseline reviews. Resist it.

## Review structure

For each proposal, emit a markdown report with exactly these four H2
sections:

```markdown
## Summary
<two or three sentences: what the proposal does, your overall
assessment, and whether it is ready to proceed>

## Strengths
- <specific decision or trade-off the author got right>. Worth keeping
  because <why>.
- (or: "None obvious from the proposal alone.")

## Concerns
- <specific risk, gap, or unaddressed failure mode>. Matters because
  <why>; one concrete mitigation is <suggestion>.
- (or: "None.")

## Open questions
- <thing you cannot decide from the proposal alone>. Would help to
  know <what>.
- (or: "None.")
```

If a section is empty, write "None." rather than omitting the heading
— consistency makes the output scan-friendly.

### Worked example

Suppose the design-doc fragment is:

```markdown
# Add Redis cache in front of the product-search service

## Context
The product-search service currently queries Postgres on every
request. p99 latency at peak is 450ms; the SLO target is 200ms.

## Proposal
Add a Redis cluster between the API layer and Postgres. Cache the
result of every search query for 5 minutes, keyed on the normalized
query string. Cache invalidation is purely TTL-based; no explicit
invalidation on writes.

## Constraints
- We have ~30 product writes per day; reads are ~50 req/s peak.
- Team has operated Redis in two other services for 18 months.
```

A baseline review would read:

```markdown
## Summary
Proposes a Redis read-through cache in front of the product-search
service to bring p99 latency from 450ms to under the 200ms SLO.
Reasonable for a read-heavy workload with low write volume; the
TTL-only invalidation strategy is the main thing worth scrutinizing
before accepting.

## Strengths
- Right tool for the workload — 30 writes/day with 50 req/s reads
  is the textbook read-through cache fit, and the team already
  operates Redis. Worth keeping because the team-fit dimension is
  often where caching proposals fail.

## Concerns
- TTL-only invalidation means a product update is invisible to
  search for up to 5 minutes. Matters because product-detail
  changes (price, availability) are exactly the kind of edit
  customers notice as stale data; one concrete mitigation is
  publishing an invalidation event on every product write (the
  30/day write rate makes this cheap).

## Open questions
- What does the cache hit-rate look like at the chosen TTL? Would
  help to know whether the chosen 5 minutes was modeled against
  actual query distribution or chosen as a round number.
```

Notice what's **not** in this review: no seven-perspective matrix
(no separate technical-soundness / operational-complexity /
reliability / security / scalability / migration / product-impact
walk-through), no domain-specific deep dive (no "use Redis Sentinel
vs. Cluster mode for this scale", no "consider a write-through cache
instead"). That depth belongs in a richer user-installed
architecture-review skill, not the baseline.

## Gotchas

- **A configured `review.arch_review_skill` (scaffold.json) is honored only in
  the orchestrated arch pass, not here.** Spec 096-01 / ADR-0040 D1 lets a
  project name its richer arch-review skill in `scaffold.json`; that key is read
  by `review.py` when it builds the **arch pass** prompt for the spec-workflow
  reviewer subagent. It is **not** consulted on this router-only interactive
  invocation. Config honoring on orchestrator-invoked surfaces is a tracked
  follow-up (ADR-0040 OQ1).
- **The deferral hint is the routing mechanism, not a code path.**
  Jig's description tells the Claude Code router "prefer any other
  installed skill whose description identifies it as handling
  architecture review, design review, RFC review, or technical-design
  review." There is no filesystem probe, no plugin-precedence lookup,
  no name-matching against `arch-review` specifically. The deferral
  is **category-based**: a user skill named anything that claims that
  surface area will win. If the router consistently picks jig's
  baseline over such a skill, jig's description is too greedy — open
  an issue. **This router-based deferral applies to _interactive_ use
  only.** The spec-workflow **arch pass** spawns a read-only `reviewer`
  subagent with no `Skill` tool, so it cannot use the router at all —
  there `review.py` does explicit file-read dispatch (detects
  `~/.claude/skills/arch-review/` and points the reviewer at it). See
  [docs/workflow.md](../../docs/workflow.md) § Post-implementation review.
- **Lightweight is a feature, not a limitation.** The baseline does
  not ship a seven-perspective matrix. It does not ship
  domain-specific reference files (distributed systems, API design,
  data architecture, migration plans). It does not perform a
  completeness-checklist sweep. It does not produce a severity-rated
  finding list. If you find yourself wishing the baseline did more,
  you are in the target audience for installing a richer skill at
  the user scope (commonly `~/.claude/skills/arch-review/`).
- **This skill reviews an ADR draft; `/jig:adr-workflow` creates
  one.** The direction matters. If the ADR does not exist yet, you
  want the scaffolding skill, not this one. If the ADR exists in
  PROPOSED state and you want a second pair of eyes on the decision
  logic before accepting, this skill is the right choice.
- **The bundled `review` skill is explicitly excluded from the
  deferral.** Jig's description says it does **not** defer to
  `review`. That's the one carve-out; everything else in the
  architecture-review category wins over jig.
- **Fallback mode** (if the routing-dogfood in spec 014-01's DoD
  ever fails): the SKILL.md frontmatter gets
  `disable-model-invocation: true` and this skill becomes
  explicit-invocation-only (`/jig:arch-review`). In that mode, no
  auto-trigger fires — the user has to type the slash command. If
  you see `disable-model-invocation: true` in this skill's
  frontmatter, the post-merge routing-dogfood (see spec 014-01
  AC #9) flipped it after a failed dogfood.

## Relationship to other skills

- **`/jig:pr-review`** — sibling skill, different shape. PR-shape
  review against a diff, not design-shape review against a
  proposal. See "When to use vs. when to defer" above. The two
  skills compose: pr-review evaluates the implementation diff
  *after* the design is settled; arch-review evaluates the design
  *before* the implementation starts.
- **`/jig:independent-review`** — sibling skill, different shape.
  Spec-compliance review against `spec.md`, not design review
  against a proposal. Use it when a slice has acceptance criteria
  to evaluate against; use this skill when the proposal is
  upstream of any acceptance criteria.
- **`/jig:adr-workflow`** — orthogonal skill. Scaffolds and
  transitions ADRs through their lifecycle; this skill reviews an
  ADR draft before it's accepted. Pairs naturally: an architect
  drafts an ADR via `/jig:adr-workflow new`, this skill reviews
  the draft, and `/jig:adr-workflow accept` moves it to accepted
  once the review is addressed.
- **`/jig:slice-land`** — orthogonal skill. Lands a finished slice
  (prepares the PR body, runs the merge sequence). Different phase
  of the workflow: arch-review operates upstream of any slicing;
  slice-land operates downstream of implementation. They do not
  interact.
