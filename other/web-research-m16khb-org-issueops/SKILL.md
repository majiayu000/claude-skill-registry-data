---
name: web-research
description: "Use when researching a question, gathering external information, comparing competitors, surveying literature, or verifying claims across independent web sources."
---

# Web Research

## Activation and Scope

Research external questions, competitors, literature, and factual claims. Fetch,
read, cross-check, and synthesize cited research; do not implement solutions or
write code. Only research-report files under `.issueops/research/` may be edited.
Every factual claim needs an actually read, accessible source URL and retrieval
date/timestamp; never infer content from a title, snippet, memory, or HTTP 200.
Unconfirmed claims stay labeled, not promoted to facts.

This body is sufficient for isolated/copied use. Optional same-skill references
resolve from the real, symlink-resolved skill directory, not cwd. Missing sibling
skills or evaluator materials never block ordinary research. Use only exposed
host search/fetch/browser tools or permitted read-only CLI commands; invent none.

## Classify Rigor First

| Intent | Strategy |
|---|---|
| Factual verification | 2–3 independent sources; report agreement/dispute |
| Competitor comparison | Independent probes per competitor; comparison matrix |
| Literature survey | Papers/docs/blogs; synthesis with timeline |
| Deep investigation | Separate subquestions, then cross-check across them |
| Quick lookup | One version, endpoint, or yes/no fact: direct lookup and inline citation |

A **quick lookup** may skip the two-source minimum, adversarial review, and report
file. Still fetch/read the source and respect access boundaries. Multi-claim or
decision-bearing research requires the full method/report below.

## IssueOps Benchmark Artifact Contract

When contributing to an IssueOps artifact or benchmark response, include this
compact block backed by actually fetched/read public sources:

```text
Source fan-out: <independent search angles or source classes>
Source index: <URLs, authority class, and retrieval timestamp/date>
Claim verification: <confirmed, single-sourced, disputed, or unverified claims>
Access boundary: <auth/paywall/challenge/block status and safe stop rationale>
```

Login, payment, CAPTCHA, or abuse-control bypass requirements make that source
inaccessible. Record the limit and continue with lawful independent sources.

## 1. Fan Out, Then Collect

Use `high-volume-exploration` for large source sets, `parallel-independent-research`
for independent angles, `devils-advocate-review` for decision-bearing claims, and
`cross-verification-consensus` to reconcile sources. These are conditional
coordination patterns, not mandatory extra work for a quick lookup.

Decompose full research into 2–4 independent angles. Use precise quoted terms,
official-domain searches, comparisons, dated sources, real code usage, recent
papers (prefer the last two years), release/migration notes, or issue trackers;
avoid vague single-word searches. Match dates and queries to the question.

Use read-only research subagents only if the host exposes and permits them. Give
each one angle; it fetches/reads the 3–5 most relevant sources and returns claims,
evidence, publication date, author/authority, URLs, and retrieval timestamps.
Never duplicate an angle while its subagent runs. Without subagents, run the angles
sequentially or via native parallel calls and record that host limitation, not a
research finding. The main agent reads results, cross-checks, synthesizes, and writes.

## 2. Fetch Within Access Boundaries

Do not add host-specific fictional tools. Report `auth_required`, `paywalled`, `challenge`, or `blocked`
when that boundary is observed; never replace missing content with a guess.

### Prefer an Available Harness Surface

When exposed, prefer MCP `web_fetch_resilient`, or the CLI fallback:

```bash
issueops web-fetch fetch --url URL --timeout 30s --max-chars N --json
```

Replace URL/N with the actual source and limit. Preserve `category`, `stop_reason`,
`grid_exhausted`, `attempted_routes`, `untried_routes`, `metadata`, and `warnings`.
Report `auth_required`, `paywalled`, `challenge`, and `blocked` as limitations.
If neither surface exists, record the environment limit and use permitted public
methods below. A missing harness does not authorize fictional host tools.

### FR-0: Public Platform Routes

Before generic fetching, check for a documented public no-auth API: platform JSON,
RSS/Atom, registries, repository APIs, encyclopedia APIs, or public media metadata.
Prefer official/public paths. Use only available tools and authorized access.

### FR-1: Direct Boundary Probe Before Alternatives

If no public route fits, or it failed **without an access-control signal**, request
the original URL with a truthful research User-Agent and inspect status, headers,
redirects, and body. Do not start proxies, caches, mobile variants, or sidecars in
parallel with this initial boundary probe.

Any login/paywall/challenge/bot-block signal ends attempts for this source. Only
a clean probe lacking usable content permits parallel public alternatives:
Jina Reader, exposed host fetch/search, publicly linked/documented mobile endpoints,
or applicable RSS/feed/JSON/API variants. Do not manufacture an access bypass.

Archive/cache sidecars (AMP cache or Wayback/CDX) are lower trust and allowed only
after a clean boundary probe and failure of all primary sources. Label content:
"Source: <archive/cache name> snapshot, retrieved YYYY-MM-DD. Original unavailable."

### FR-2: Stop at Access Controls

403/430, WAF headers/cookies, challenge bodies, or repeated redirect loops need
inspection for blocking. Recognize `cf-ray`, `server: cloudflare`, `x-datadome`,
`__cf_bm`, `_abck`, `datadome`, CAPTCHA/verification prompts, and 3+ consecutive
302/307 redirects. Login/sign-in/로그인 and subscribe/구독 signals stop escalation.
Do not defeat auth, payment, robots-sensitive restrictions, CAPTCHAs, WAFs, or site
abuse controls with TLS/browser impersonation, alternate clients, cookie warming,
or fabricated referrers. Continue with independent lawful sources.

For a plain 429/503 rate limit without such blocking, respect `Retry-After` and
retry once; then record the limit, not a bypass attempt. If a challenge accompanies
it, the stop boundary takes precedence. Report geo-restrictions as geo-blocked.

### FR-3: Ordinary Client Rendering Only

Use an exposed browser only for an ordinary JS-rendered SPA with **no** challenge
or access-control signal. Navigate, wait for body/main content, extract visible
text/accessibility output. If network inspection exists, inspect XHR/fetch routes
such as /api/, /graphql, or .json; refetch only public no-auth APIs that respect
access controls, iterating documented/discovered pagination for list pages.
A JS challenge is an FR-2 stop, never browser authorization.

### Validate Every Response

| Response | Disposition |
|---|---|
| Empty SPA root (under 200 chars; under 100 body chars unusable) | Ordinary rendering only if no access control |
| CAPTCHA, WAF challenge, access denied, login redirect loop | Stop at FR-2 |
| Soft paywall | Metadata only; label partial/paywalled; no escalation |
| Empty search JSON (`hasResults: false`, `hits: []`) | Different permitted method, not useful evidence |
| Rate limit or geo restriction | Bounded retry above or report geo-blocked |

Content minimums: article/blog body ≥500 chars; product/listing has schema.org
JSON-LD; social post ≥50 chars; profile/about has JSON-LD Person; search results
have ≥3 URL-bearing entries. These checks are necessary, not proof of truth.
Salvage OpenGraph, JSON-LD, or Twitter Card metadata from already-received partial
responses, tagging its provenance/limits; metadata is not a read of blocked content.

Check dependencies first. Never install globally or silently. If a tool matters,
ask permission or use a temporary project-local environment only when host policy
allows it; otherwise skip that method and report the limitation.

## 3. Cross-Verify Claims

1. Check independence: sources quoting each other count as one, not corroboration.
2. Assess authority: official docs/announcements and peer-reviewed papers high;
   primary repo README/source and recognized technical authors medium; community
   answers low-to-medium; individual issue comments/social posts low. Do not treat
   an unreviewed preprint as peer-reviewed merely because it is on arXiv.
3. Mark **Confirmed** for ≥2 independent agreeing sources, **Single-sourced** for
   one, **Disputed** for disagreement, and unverified when evidence is missing.
   Report both disputed positions. No unqualified single-source key conclusions.
4. For critical claims, have a fresh read-only adversarial subagent try to refute
   them when exposed/permitted. Report refutations alongside originals. If unavailable,
   perform the refutation check directly, disclose lack of independence, and do not
   claim a fresh reviewer ran. Do not duplicate active delegated searches.

Confidence: **High** needs ≥3 independent authoritative agreeing sources and passed
adversarial review; **Medium** needs ≥2 independent agreeing sources (may include
one medium-authority source); **Low** for one/weak sources or adversarial issues;
**Disputed** for disagreement between independent authoritative sources.

## 4. Report and Artifact Contract

For full research, write `.issueops/research/<slug>.md` with these sections/fields.
A copied skill can produce the report directly from this contract:

- `# Research: {Question}`.
- `## TL;DR`: Conclusion (1–2 sentences), Confidence (High/Medium/Low/Disputed),
  Sources (N independent, M single-sourced claims, K disputed).
- `## Method`: search angles, fetched/read URL count, cross-verification and
  adversarial coverage, host/access limitations.
- `## Findings`: per-finding precise claim, source titles/URLs, retrieval dates,
  authority/relevance, verification status, and confidence (High/Medium/Low).
- `## Cross-Check Results`: confirmed, single-sourced, disputed counts and meaning.
- `## Adversarial Review`: claims reviewed, reviewer findings, whether they survived;
  record unavailable/not-applied review rather than inventing it.
- `## Disputed / Unresolved`: each claim, both positions with URLs, and the access,
  experiment, or decision needed to resolve it.
- `## Open Questions`: remaining unknowns and suggested next research direction.
- `## Source Index`: #, URL, Title/Description, Type, Retrieved, Authority.

All factual claims cite fetched/read evidence. Keep unresolved questions explicit;
a polished report is not evidence that the claims survived verification.

## Stop Rules

- Full report written, ≥2 independent sources per key claim: **DONE**.
- Quick lookup: fetched/read answer with inline URL/date citation: **DONE**.
- Accessible sources exhausted: surface unresolved claims and next steps, not certainty.
- More than three rounds without convergence: checkpoint known findings and ask
  whether to continue.
- Auth/paywall/challenge/block: stop attempts for that source, report limitations,
  and continue available alternatives; if none remain, report unresolved.

## IssueOps Integration (Only When a Cycle Exists)

1. Research external context before `grill` and feed findings into the domain
   grill/plan. Preserve the exact ID and route via
   `issueops next --id "$ISSUEOPS_ID" --json`; stop blocked routing, never infer phase.
2. Give the owning stage findings for authenticated feedback (source `web-research`,
   slug, source count, confirmed-claim count). Link the report under **External
   Research** in the plan through that owner; the research actor's write scope stays
   within research reports. `issueops feedback add` and `issueops status` are valid
   aliases but confer no mutation authority.
3. The owner must check current ID, generation, native actor, and canonical cwd
   before durable writes, using `issueops execution whoami --json`'s
   `record_actor_flags` for records and `claim_actor_flags` for lease operations.
   Never invent flags, use another holder, or bypass mismatches; reconcile uncertain
   writes instead of retrying. Preserve stage gate/artifact ordering.
4. Reports can feed planning, debugging, algorithm/database research, or Verified
   Execution evidence/reviewer gates. Those workflows own their further actions.
   Commit reports through the owning Git stage only if authorized; research does
   not itself authorize commit, push, remote publication, implementation, or cleanup.
   Destructive cleanup requires a target/fingerprint preview and separate approval.
   Do not add approval gates to already-authorized work. Missing stage support means
   recording remains pending, not that standalone research needs sibling installs.

## Optional References

- [Report template](references/report-template.md): expanded layout and field guidance.
- [Retrieval examples](references/retrieval-examples.md): query, platform, and metadata examples.

These examples do not relax the body contract. `quality inspect` is not a semantic
research/skill runner; `issueops skill-bench` is unsupported, not a verification step.
