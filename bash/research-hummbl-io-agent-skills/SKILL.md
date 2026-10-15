---
name: research
description: Intelligence surge mode — sweep, ingest, synthesize, dispatch. For deep research sessions that must produce ledger-ready findings.
version: 1.3.0
execution-mode: side_effecting
argument-hint: "--mode preview|persistent <topic or focus area>"
category: fleet-ops
status: tested
providers:
  required: [bash, python]
---
# Research Mode Activation

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action (host prefix is required for agent-originated posts).
```
Type: SKILL_INVOKE
To: all
Message: host=<machine> [skill=research] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`. The message body MUST begin with `host=$(hostname)` or canonical mesh host name per `bus-protocol.md §Machine tagging`.)

Example bash invocation:
```bash
python ~/bin/bus-global.py post <from_id> all SKILL_INVOKE \
  "host=$(hostname) [skill=research] [mode=side_effecting] [args_hash=<args_sha256>] [session=<session_id>]"
```

### 0.1 Authorization Preflight (MANDATORY before Sweep)

Every invocation MUST explicitly select `--mode preview|persistent`. If the
mode is absent, stop before searching and ask the operator to choose. A skill
invocation, broad autonomy request, or research topic alone is not permission
for persistent mutations. The runtime **MUST NOT infer authorization**.

Run the guard before any internal or external source sweep:

```bash
# Read-only source preview: no persistent research mutations.
python ~/.agents/scripts/research-run-guard.py preflight \
  --mode preview --session-id <session_id>

# Durable run: pass each grant only when the operator explicitly authorized it.
python ~/.agents/scripts/research-run-guard.py preflight \
  --mode persistent --session-id <session_id> \
  --authorization-ref <operator-message-or-decision-receipt> \
  --authorize-mutation branch \
  --authorize-mutation worktree \
  --authorize-mutation ledger \
  --authorize-mutation artifact \
  --authorize-mutation commit \
  --authorize-mutation bus
```

If persistent preflight exits nonzero, post `BLOCKED` and stop before the
sweep. Do not downgrade silently to preview mode. If the operator explicitly
authorizes a staging directory, add both `--receipt-dir <path>` and
`--staging-authorized` so the preflight receipt and any later interruption
receipts have a permitted destination.

#### Mode contract

- **Preview**: may read internal sources, query external sources, classify
  unreviewed candidates, and post coordination receipts. It MUST NOT create or
  switch a branch/worktree, append to the ledger, write a research artifact,
  report candidates as findings, commit, or push. Its user-facing output is
  limited to query coverage and candidate URLs labeled
  `UNREVIEWED / NOT REPORTED AS FINDINGS`.
- **Persistent**: executes the full Sweep → Ingest → Synthesize → Dispatch
  contract only after all six grants pass. The authorization reference and
  preflight receipt are part of the run evidence.

If a run becomes blocked after queries have started, preserve reproducible
query inputs only when a staging directory was explicitly authorized:

```bash
python ~/.agents/scripts/research-run-guard.py stage-query \
  --session-id <session_id> --receipt-dir <authorized_path> \
  --staging-authorized --source <source_name> --query <query_text> \
  --retrieved-at <YYYY-MM-DDTHH:MM:SSZ> --result-count <N> \
  --candidate-url <URL> --stop-reason <reason>
```

This receipt is provenance, not ingestion: it is content-addressed, contains no
finding claims, and remains `unreviewed-candidates` / `not-reported`.

You are operating in **RESEARCH MODE** — maximum intelligence gathering, source-grounded, ledger-ready output.

## Active Configuration
- **Tempo**: OVERNIGHT (deep research takes time; don't rush the synthesis)
- **Autonomy**: Mode-bound — preview is read-only; persistent requires the complete explicit mutation grant set
- **Pipeline**: Sweep → Ingest → Synthesize → Dispatch

## Task
$ARGUMENTS

## Research Pipeline

0. **Design Check** (pre-Sweep) — before searching, identify known epistemological weaknesses in the research domain:
   - **Case-study bias**: Will the evidence base rely on creator/practitioner case studies? If so, flag that findings will be survivorship-biased by construction and plan for platform-mechanic evidence to anchor confidence.
   - **Single-source claims**: Are there claims that rely on a single source? Flag them for corroboration requirements at the Gate.
   - **Stale statistics**: Does the domain involve fast-changing metrics (platform growth, market share, algorithm behavior)? Flag that statistical claims will need freshness verification at the Gate.
   - **Platform-reported figures**: Are key statistics self-reported by platforms with a commercial interest? Flag for source-type classification at Classify.
   (Origin: 2026-09-08 AAR — survivorship bias and stale statistics were caught in ARCANA review, not at research design time. Catching them pre-Sweep is cheaper than catching them in review.)
1. **Sweep** — cast wide (`[daily-research]`, `[industry-watch]`, `[anthropic-watch]`, `[preprint-scan]` as relevant)
2. **Classify** — all local-model and Gemini output enters as **HYPOTHESIS**, not FINDING. Promotion to FINDING requires human review or external-source corroboration. **Survivorship bias screening**: flag findings based on creator/practitioner case studies as lower confidence (max 0.85) than findings based on platform mechanics or independent measurement. Case studies are survivorship-biased by construction — the creators who failed don't write case studies. Distinguish: *platform mechanics* (durable, non-copyable, adoption-resistant) vs *creator systems* (depreciating, copyable, adoption-eroding). (Origin: 2026-09-08 AAR — ARCANA review found case-study evidence base was epistemically invalid under fat-tailed distributions.)
3. **Gate** — run citation gate on any output with author-year citations. Run claim decomposition on high-stakes outputs (pitch, paper, client-facing). **Primary-source verification**: before ingesting any statistical claim cited via a secondary source, verify it against the cited primary source. If the primary source is not accessible or doesn't contain the figure, label as HYPOTHESIS, not FINDING. **Freshness check**: for any statistical claim, verify the data's *collection date*, not just the citation's publication date. Statistics have expiry dates — a 2024 zero-click figure cited in a 2026 article is stale. (Origin: 2026-09-08 AAR — "67% reach decline" attributed to ConvertKit 2024 was not findable in the primary source; "58%" zero-click figure was 2024 data cited without date in a 2026 secondary source.)
4. **Ingest** — only VERIFIED or PROMOTED findings go to ledger via `[research-ingest]`. HYPOTHESIS-level output stays in `docs/research/` with labels intact. **Before the `cognition post` batch**: emit a fresh SKILL_INVOKE (the 300s provenance window does not survive a long sweep) and run `python ~/bin/bus-global.py status` to persist the local bus mirror — the provenance check reads the mirror, not the hub, so a bridge-posted invoke is invisible until `status` pulls it down. See `skills/research-ingest/SKILL.md` §0b. (Origin: 2026-09-20 AAR — ingest rejected twice on mirror lag + expired window.)
5. **Synthesize** — compress to 3-5 key findings with source citations; use `[research-digest]` to verify coverage. Before grading the artifact, run `python scripts/intel_surge_quality_check.py <artifact.md>` (R1-R4 structure + declared grade); errors cap the grade at C. Record unanswered questions and conjectures as `open_question` / `conjecture` rows (`[INF]` until reviewed) per `skills/explore-mode/SKILL.md`.
6. **Dispatch** — post SITREP to bus; suggest `[competitive-intel]` if competitor signals found, `[evidence-pack]` if findings need bundling for external use

## Quick-Access Skills
- **Sweep**: `[daily-research]`, `[deep-research]`, `[industry-watch]`, `[anthropic-watch]`, `[web-research]`
- **Evidence**: `[preprint-scan]`, `[evidence-grade]`, `[hallucination-check]`
- **Ingest**: `[research-ingest]`, `[research-digest]`, `[ledger]`
- **Dispatch**: `[competitive-intel]`, `[evidence-pack]`, `[sitrep]`, `[send-email]`
- **Meta**: `[brainstorm]`, `[base120]`, `[decision-log]`

## Rules
- **Source everything** — every claim needs a URL, arXiv ID, or `[ESTIMATE: basis]` tag
- **[ESTIMATE] tag format** — any quantitative claim, timeline, or prediction without a
  direct source MUST be tagged at write time as `[ESTIMATE: <basis for the estimate>]`.
  The tag must state the reasoning, not just flag the estimate. Example:
  `[ESTIMATE: 5-10 years from commercial viability, based on typical research-to-product
  timelines for emerging silicon technologies — no direct source]`.
  Do NOT add the tag post-hoc during self-review — tag at write time. If you cannot
  provide a basis, the claim should be removed, not tagged.
  (Origin: 2026-09-02 AAR — "5-10 years from commercial viability" written without
  source or tag; caught in self-review, required post-hoc tagging.)
- **No unsupported statistics** — bare numbers without a source fail the ingest gate
- **Primary-source verification for secondary-sourced statistics** — any statistical claim cited via a secondary source (e.g., a marketing blog citing a research report) MUST be verified against the cited primary source before ingestion as a FINDING. If the primary source is not accessible, doesn't contain the figure, or the attribution is inaccurate, label as HYPOTHESIS. Do not promote secondary-sourced statistics to FINDINGS without primary-source confirmation. (Origin: 2026-09-08 AAR — "67% of creators experienced reach declines" attributed to ConvertKit 2024 was not findable in the primary source; the sweep trusted the secondary attribution.)
- **Statistical freshness checking** — for any statistical claim, verify the data's *collection date*, not just the citation's publication date. A 2024 data point cited in a 2026 article is stale unless explicitly confirmed as still current. Flag the collection date in the finding's source metadata. (Origin: 2026-09-08 AAR — "58%" zero-click figure was 2024 SparkToro/Datos data cited without date in a 2026 secondary source; the current 2026 figure is 68.01%.)
- **Survivorship bias screening** — findings based on creator/practitioner case studies are capped at confidence 0.85 and labeled as PRACTITIONER_EVIDENCE, not DISCOVERY. Case studies are survivorship-biased: the creators who tried the same strategy and failed don't write case studies. Distinguish *platform mechanics* (structural, durable, non-copyable) from *creator systems* (anecdotal, depreciating, copyable). Weight platform-mechanic findings higher than creator-system findings in synthesis. (Origin: 2026-09-08 AAR — ARCANA review found the case-study evidence base was epistemically invalid under fat-tailed distributions; Taleb lens showed expected value of hub-and-spoke is ~2%, not the 217% cited from a single case study.)
- **Ingest before reporting** — findings must hit the ledger before ANY report, including intermediate SITREPs. The SITREP must include ledger IDs, not "0 entries." If you have findings to report, ingest them first. (Origin: 2026-09-02 AAR — SITREP posted with "0 ledger entries" because ingest ran after the SITREP instead of before.)
- **Confidence floor: 0.70** — below that, flag as unverified and do not ingest as DISCOVERY
- **EU AI Act and NIST COSAiS are always relevant** — surface compliance angles on every governance-adjacent finding
- No Ollama on MBP
- **Verify-pass mandatory on adoption recommendations**: Whenever a research swarm produces a synthesis that recommends ADOPT, LIFT, COPY, or DEPEND ON an external project/library/tool, dispatch a verify-pass agent (IP/legal/operational risk audit + source-read of 2-4 files) BEFORE the decision-log ADR is written. Verdict: GREEN (proceed) / YELLOW (proceed with note) / RED (pause and reconsider). Cost: 1 agent + ~700-word budget. Origin: 2026-04-26 OR-research session — Lane B fabricated stale OpenCode details that propagated through two synthesis turns until Lane F caught them; Lane K source-read separately corrected a ClawRouter "code to lift" claim. Receipts: ledger:clp-d016b8f32ba7, clp-163d98f976c2, clp-f7d33313385b.

## Citation Gate (mandatory for local-model and Gemini output)

Any research output containing author-year citations (e.g., "Smith et al., 2018") from a
local model (Ollama, Gemini, or any non-web-grounded source) MUST pass through the citation
gate before ingestion or use in any downstream artifact (paper, pitch, email, case study).

### Gate Protocol

1. **Extract** — list every `Author (Year)` or `Author et al. (Year)` citation in the output
2. **Classify** — for each citation:
   - **Canonical**: widely-known foundational work (e.g., Janis 1982 Groupthink, Rizzolatti 2000 mirror neurons) → PASS with spot-check
   - **Specific**: precise author+year+journal claim → MUST VERIFY via `[preprint-scan]` or web search
   - **Generic**: placeholder-sounding names ("Smith et al., 2018", "Jenkins & Patel, 2019") → PRESUME FABRICATED until verified
3. **Verify** — for Specific and Generic citations:
   - Search for the exact paper (author + year + key finding)
   - If found: tag `[VERIFIED: <URL or DOI>]`
   - If not found: tag `[FABRICATED]` and exclude from all downstream artifacts
4. **Report** — citation gate summary: `N citations extracted, M verified, K fabricated, J canonical-pass`

### When to Apply

- After any `[deep-research]` session using local models
- After any Gemini research delivery (per gemini-guardrails.md arXiv rule)
- After ingesting remote-node research team output (remote-node dormant since 2026-07-01 — historical reference only)
- Before any finding enters a paper, pitch, or external communication

### Why This Exists

Local models (gemma4, qwen3.5, mistral) and Gemini fabricate citations at a ~30-40% rate.
They mix real canonical references with invented author-year combinations that sound plausible.
Research Team v2 (Apr 17 2026) BKI lane produced 10 "peer-reviewed studies" — at least 3
had placeholder-style author names not traceable to real papers. This gate prevents fabricated
citations from reaching publication or client-facing materials.

## Output Contract

In **persistent mode**, end every session with:
1. Ledger entry count (how many ingested)
2. Top 3 findings with source + confidence
3. One-line HUMMBL positioning implication per finding
4. Bus SITREP posted
5. Git commit of research artifacts — `docs/research/` files MUST be committed to the repo before the session closes. Artifacts on disk + in the ledger are not sufficient; git history is the third durability layer. Stage only the `docs/research/` files, not unrelated working-tree changes. (Origin: 2026-08-25 AAR — Levin grounding artifacts were left untracked in git after the session froze; a follow-up session had to commit them.)
6. **Use a dedicated research worktree** — create a clean worktree from `origin/main` before committing research artifacts. Do NOT commit to the shared symlinked worktree (`~/PROJECTS/.agents` or equivalent) because concurrent sessions mutate its branch state unpredictably. Pattern: `git worktree add /work/active/<repo>-research-docs -b docs/research-<topic> origin/main`. (Origin: 2026-09-02 AAR — first commit landed on a concurrent session's branch; second commit was blocked by merge conflicts from another session. Both required recovery via clean worktree creation.)
7. **Verify branch ownership before commit** — run `git branch --show-current` immediately before `git add`, not just during start-session. If the branch belongs to another agent's lane (e.g., `feat/evaluation-framework-*`, `fix/devin-*`), create a new branch or worktree instead. (Origin: 2026-09-02 AAR — branch was checked at session start but a concurrent session changed it before the commit.)
8. **Git staging retry in autonomous loop harnesses** — any autonomous loop script or harness modifying artifacts during multi-cycle execution MUST explicitly call `git add <file>` immediately after writing, and if pre-commit hooks reformat the file, it MUST re-stage and retry the commit once so intermediate changes are never silently dropped as "no changes". (Origin: 2026-09-04 AAR — 1-hour harness cycles produced unstaged changes because pre-commit hooks or staging was not retried.)
9. **Distinguish artifact brain directory from repo paths** — in agent environments, tools requiring `ArtifactMetadata` MUST target `<appDataDir>/brain/<conversation-id>/`. Repository documents in `/work/active/` must be written directly via filesystem tools or copied from the brain artifact directory to avoid metadata path rejection. (Origin: 2026-09-04 AAR — `write_to_file` rejected repository path when `ArtifactMetadata` was passed.)
8. **Git staging retry in autonomous loop harnesses** — any autonomous loop script or harness modifying artifacts during multi-cycle execution MUST explicitly call `git add <file>` immediately after writing, and if pre-commit hooks reformat the file, it MUST re-stage and retry the commit once so intermediate changes are never silently dropped as "no changes". (Origin: 2026-09-04 AAR — 1-hour harness cycles produced unstaged changes because pre-commit hooks or staging was not retried.)
9. **Distinguish artifact brain directory from repo paths** — in agent environments, tools requiring `ArtifactMetadata` MUST target `<appDataDir>/brain/<conversation-id>/`. Repository documents in `/work/active/` must be written directly via filesystem tools or copied from the brain artifact directory to avoid metadata path rejection. (Origin: 2026-09-04 AAR — `write_to_file` rejected repository path when `ArtifactMetadata` was passed.)

In **preview mode**, end with only the preflight result, searched sources and
queries, and explicitly labeled unreviewed candidate URLs. Do not provide a
findings synthesis, positioning implications, ledger count, research artifact,
or commit claim.

## Pre-flight Confabulation Probe (for remote-node research dispatches — remote-node dormant since 2026-07-01, use Workstation)

Before dispatching a multi-hour research run to local models, run 3 quick induction
prompts in the target domain to calibrate the model's fabrication density:

1. **Citation probe**: "Cite the most influential 2023 paper on [topic]" — does it fabricate?
2. **Statistic probe**: "What percentage of enterprises have adopted [framework]?" — does it invent a number?
3. **Entity probe**: "Who is the CEO of [real company in the domain]?" — does it get it right?

If 2+ probes produce fabrications → route the lane to a more reliable model (gemma4:e4b
was 100% reliable in Research Team v2; qwen3.5:9b had 3 empty responses).

This takes <2 minutes and prevents committing a 6-hour budget to an unreliable model.

Begin research now.

## When to use [research-pipeline] instead

Use `[research-pipeline]` when you need:
- Depth control (`--depth quick|full|overnight`)
- BKI parallel track (`--focus bki`)
- Audience-targeted dispatch (`--audience ciso|caio|board|investor`)
- A structured pipeline receipt (stage counts, drop log, top findings)

`[research]` is for open-ended sessions. `[research-pipeline]` is for reproducible, documented runs.

## Skill Chains
- For delegate research execution to opencode -> `[cross-runtime-bridge]` (`python ~/bin/cross_runtime_bridge.py delegate`)
- For free-tier inference for research synthesis tasks -> `[reasoning-router]` (`route`)

### Mandatory

- `research-run-guard.py preflight` before Sweep; the selected mode controls all later actions.

### Advisory

- After `[research]` → `[research-digest]` to verify coverage and compress findings
- After `[research]` → `[evidence-pack]` if findings need bundling for external use
- After `[research]` → `[decision-log]` if the session produced an adoption recommendation (ADR)
- Before `[research]` → `[brainstorm]` to scope the research question
- During `[research]` → use `python ~/bin/free_apis.py` for live scholarly/regulatory/vulnerability data (OpenAlex, PubMed, Federal Register, NVD, OSV, Wikidata)

## Authority

- **T1 (TRUSTED)**: May run
- **T2 (Active/High)**: May run
- **T3 (Medium)**: Operator approval required
- **T4 (Probationary)**: BLOCKED (surge mode)
- **Operator**: Override any restriction
