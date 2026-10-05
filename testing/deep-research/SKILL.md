---
name: deep-research
description: 'Automatically plan and execute deep, evidence-backed, multi-source research when the user says "derin/çok detaylı araştır", "bütün siteleri/kaynakları tara", "yüzeysel olma", "güzel analiz et", asks for due diligence, a broad literature/market scan, a consequential comparison, fact-check, or a decision that cannot be supported by a quick lookup. If a research request says "gerekli/alakalı becerileri kullan", "bütün gerekli skilleri kullan", or similar, do not stop at this umbrella: select the smallest complete set of research-depth, owning-domain, evidence-verification, and independent-challenge skills while excluding unrelated or duplicate skills. Route one ordinary low-stakes lookup to quick-research and supplied long-form analysis to deep-reading-analyst.'
---

# Deep Research

Produce a current, traceable answer that is useful for a decision. Use the tools and model already available in the active host. Do not switch providers or require a named model unless the user explicitly asks.

## Compose the research team

Deep research owns the research plan; it is not automatically the only skill
needed. When the user asks for the necessary, related, compatible, or all
relevant skills, read
[domain-routing.md](references/domain-routing.md) and select the smallest
complete combination:

1. one research-depth owner;
2. the specialist that owns each distinct decision domain;
3. the appropriate evidence-integrity layer;
4. an independent challenger only when stakes, uncertainty, or the user's
   request justify it.

“Use all relevant skills” never means load every installed skill. Do not add
another umbrella or specialist that contributes no distinct work, and do not
let a broad research skill displace a narrower medical, financial, clinical,
technical, product, pricing, legal, or route specialist.

## 1. Frame the decision

1. Restate the deliverable and the decision it must support.
2. Infer safe defaults from the request. Ask only when a missing answer changes scope, cost, safety, or the conclusion.
3. Separate stable background facts from claims that require live verification.
4. Define a stopping rule: enough evidence to answer, material disagreements resolved or exposed, and important gaps named.

## 2. Build a research map

Create 3-7 non-overlapping questions. Mark each as:

- independent: can be researched without another result;
- dependent: must wait for earlier evidence;
- verification: attempts to disprove or stress-test a likely conclusion.

Set source preferences before searching:

1. primary or official sources;
2. peer-reviewed papers, standards, filings, or authoritative datasets;
3. strong independent analysis;
4. community evidence for lived experience and failure modes.

Treat popularity, search rank, and repetition as weak evidence by themselves.

## 3. Choose the fastest honest execution mode

Use the strongest mode actually exposed by the host:

1. Parallel workers: assign one bounded independent question per worker.
2. Concurrent tool calls: run independent searches, file reads, or lookups together.
3. Batched retrieval: place several independent queries or URLs in one supported tool call. This is the normal fallback for hosts without subagents.
4. Sequential workstreams: preserve the same map and evidence separation when no parallel or batch mechanism exists.

Never claim workers, browsing, or concurrency that did not occur. Use the dispatching-parallel-agents skill when work needs explicit ownership, shared-workspace rules, or multi-worker integration.

Each delegated workstream must return: findings, exact evidence links or paths, relevant dates, confidence, contradictions, and unresolved gaps.

## 4. Retrieve and record evidence

- Open the supporting page, paper, dataset, or document; do not rely on snippets.
- For changing facts, record both publication date and event or effective date.
- Prefer first-party documentation for product behavior and technical claims.
- Seek at least two independent sources for consequential disputed claims when feasible.
- Record negative evidence and failed searches when they affect confidence.
- Distinguish source-backed facts, calculations, and inference.

Maintain a compact ledger:

~~~markdown
| Claim | Evidence | Date | Source quality | Confidence | Contradiction or gap |
|---|---|---|---|---|---|
~~~

Do not average contradictory sources. Explain why they differ: scope, date, method, population, incentives, or definitions.

## 5. Synthesize around the user's goal

1. Lead with the answer, verdict, or ranked options.
2. Explain the few findings that drive the conclusion.
3. Separate facts from inference and recommendation.
4. State tradeoffs, uncertainty, and what would change the conclusion.
5. Put citations beside the claims they support and link to the exact page when possible.
6. Prefer a concise decision memo unless the user requests a full report.

For a multi-document report or literature compilation, read references/compilation-method.md only for the needed sections.

## 6. Adversarial verification

Before delivery:

- re-open the strongest sources and confirm each citation supports the nearby claim;
- check names, dates, units, versions, sample sizes, and arithmetic;
- search for credible counterevidence to the leading conclusion;
- confirm recommendations reflect the user's constraints rather than generic popularity;
- remove unsupported attractive claims;
- state what could not be verified.

Use `$evidence-integrity-guard` for a separate claim/source/citation audit when it is available, especially for consequential, disputed, commercial, scientific, medical, legal, financial, or time-sensitive conclusions. Do not claim the guard ran when it was unavailable; apply the same checks directly.

## Guardrails

- Do not hardcode a vendor, model family, reasoning level, or proprietary tool.
- Do not fabricate citations, browsing, workers, access, or consensus.
- Do not treat model memory as current evidence when live verification is needed.
- Minimize quotation; paraphrase and cite.
- For medical, legal, financial, security, or other high-stakes topics, use current authoritative sources and make decision boundaries explicit.
