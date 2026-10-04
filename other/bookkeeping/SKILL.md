---
name: bookkeeping
tier: D
category: knowledge
version: 1.5.0
primitive: P6
description: Universal knowledge engine — scores, promotes, and compounds knowledge across all sources into a permanent, query-able entity graph
author: broomva
tags:
  - knowledge-graph
  - knowledge-extraction
  - scoring
  - entity-graph
  - bstack
  - p6
compounding:
  - social-intelligence
  - knowledge-graph-memory
  - content-creation
  - deep-dive-research
---

# bookkeeping — Universal Knowledge Engine

The bookkeeping skill is **bstack primitive P6**: the universal knowledge bookkeeping layer that sits beneath every knowledge-producing workflow in the Broomva stack. It implements the LLM Wiki pattern (Karpathy): raw sources flow in, get scored, scatter into entity pages, deduplicate against the existing graph, and compound into synthesis notes. Every other skill that produces knowledge delegates its extraction and promotion phases here.

---

## When to Invoke

- After any knowledge-gathering session: social engagement runs, research experiments, deep-dive sessions, conversation transcripts
- When prompted with `/bookkeeping` or `bookkeeping run`
- Automatically after the `social-intelligence` loop runs (Phase 2 — Knowledge Extraction — is fully delegated here)
- Before creating synthesis notes or flagging blog post candidates
- When asked to "extract knowledge from", "distill", "index", or "promote" any content
- When entity pages are stale or lint errors are detected in the entity graph

## Reflexive Trigger Rule (binding on every agent in this workspace)

Bookkeeping — and knowledge capture generally — is a reflex, not a request, **and never a question**. Agents must invoke `bookkeeping.py` and file graph-worthy material without being prompted in any of these situations:

1. **Before committing a feature/page that reads from the graph** — anything consuming `~/.config/bookkeeping/status.json`, `research/entities/`, or a snapshot at `apps/*/public/data/bookkeeping.json`. The data must be fresh at commit time.
2. **Before committing a synced snapshot to a public surface** — e.g., `apps/*/public/data/bookkeeping.json`. The committed copy must reflect a freshly-run pipeline.
3. **At the close of any substantial work session that produced graph-relevant material** — new names, decisions, concepts, partnerships, threads, design debates. The pipeline ingests/scores/promotes so the next session starts indexed.
4. **Before a substantial promotion run, prefer `bookkeeping replay` over `bookkeeping run`** — `run` reads from the live graph it writes to (the *shadow-dream* corruption mode). `replay` runs against a frozen snapshot first; review the diff; then `--commit` if the changes look right. Use `run` for small, well-scoped extractions; use `replay` for cross-source consolidation passes or any time the graph has grown materially since the last run.
5. **The moment a session surfaces a discrete graph-worthy item** — a decision, a name, a discovered tool/person/paper, a recurring pattern, or a typed relation inferred between entities. File it proactively (entity page, `related:` edge, or synthesis note) **as part of the work** and report what you filed in one line. Do **not** ask the user whether to record it.

**Never a question.** The interrogative form — *"do you want me to create an entry / file this into the knowledge graph?"* — is forbidden. Capture is the default action, not an opt-in the user approves; the agent files first and reports after, so the user vetoes *after* (cheap: `git revert` / delete the entity), never gates *before*. Surfacing graph-worthy material and then deferring its capture to a user yes/no is the **permission-to-document anti-pattern**: knowledge that waits for permission is knowledge lost. Two bounds keep this safe rather than spammy: (a) capture is gated by the **Nous score** (proactive ≠ indiscriminate — a low-confidence inference goes to a synthesis note, not a committed entity); (b) an **explicit standing instruction not to record** something, or material the agent has reason to treat as sensitive/private, overrides the default — those are the *only* cases where the agent withholds capture, and it does so silently, not by asking permission to document. See `research/entities/pattern/proactive-documentation.md`.

Mental checklist before declaring graph-dependent work done: *Did this session produce material that belongs in the graph? Does my feature read graph state? Am I about to commit a snapshot? Should I be using `replay --commit` instead of `run` here?* — yes to any → invoke bookkeeping / file it before committing, **without asking**.

---

## Pipeline — 7 Stages

Each stage is idempotent. Stages can be run individually or as a full pipeline via `bookkeeping run`.

### Stage 1 — INGEST

Load raw sources from any of: JSONL run logs, conversation transcripts (Markdown), web clips, manual notes, social engagement logs. Normalize every item to the canonical source record:

```json
{
  "source_id": "sha256-prefix-8chars",
  "type": "social_comment | transcript | web_clip | note | experiment_log",
  "content": "...",
  "timestamp": "ISO-8601",
  "metadata": {
    "origin": "moltbook | x | conversation | web | manual",
    "author": "...",
    "url": "...",
    "session_id": "..."
  }
}
```

All ingested records are appended to the Layer 2 raw extract file at `research/notes/YYYY-MM-DD-{source}-raw.md` and to `~/.config/bookkeeping/run-log.jsonl`.

### Stage 2 — SCORE

Two-pass scoring against the Nous gate rubric (full spec in `references/scoring-rubric.md`):

**Dimensions** (each 0–3):
- `novelty` — Is this genuinely new to the knowledge graph?
- `specificity` — Is this concrete and actionable, not generic?
- `relevance` — Does this connect to active projects, research threads, or strategic concerns?

**Heuristic fast-path** (no LLM call needed):
- Score ≤ 2 → discard immediately (clearly low-signal)
- Score ≥ 7 → promote immediately (clearly high-signal)

**LLM-as-judge** for ambiguous band (score 3–6) — **opt-in, off by default**:
- Pass item + existing entity graph context to judge (see LLM Judge Spec below)
- Output: per-item score tuple `(novelty, specificity, relevance)` + total + promote flag + candidate entity slugs
- Enable with `run --judge` or `BOOKKEEPING_JUDGE=1`. With the flag unset the
  heuristic score stands for in-band items.

> **The judge had never run once before BRO-2506.** Both original transports
> require a paid API credential absent from this workspace, so `scoring_breakdown`
> recorded 1,051,042 heuristic / 0 llm_judge across 7,765 runs. Since ~54% of
> intake lands in the 3–6 band, the heuristic decided nearly the whole corpus
> while the docs described a two-pass gate. Enabling the judge by default now
> would re-gate most of a million items in one step, which the L3 stability
> budget in CLAUDE.md forbids — hence opt-in, and hence `judge-check` below.

**Transports**, tried in this order (by billing, not by age):

| Order | Transport | Billing | Requirement |
|---|---|---|---|
| 1 | `claude -p` | **subscription-preferred** | `claude` on PATH **+** all three scorer specs **+** PyYAML |
| 2 | authored agents (Anthropic SDK) | API key | `anthropic` + `ANTHROPIC_API_KEY` **+** all three scorer specs **+** PyYAML |
| 3 | Gemini (legacy) | API key | `google-generativeai` + `GEMINI_API_KEY` |

**"subscription-preferred", not "subscription"** — and the distinction is
deliberate, because an earlier version of this table asserted a guarantee the
code had explicitly withdrawn. What the transport *enforces* is: the
API-billing environment variables it knows of are stripped, user/project/local
settings are not loaded (`--setting-sources ""`, where `apiKeyHelper` would
redirect auth), and customizations are disabled (`--safe-mode`). What it does
**not** do is probe the effective auth source at runtime — and note that
`--safe-mode`'s own help states "Admin-managed (policy) settings still apply",
so a managed `apiKeyHelper` survives both flags. It reports a preference, not
a proof, and that is why the label is hedged rather than hardened. `ANTHROPIC_API_KEY` is not the recommended carrier:
setting it routes to API billing.

The scorer is also isolated from ambient context — `--safe-mode` (no CLAUDE.md,
skills, plugins, hooks, MCP servers), `--tools ""`, `--strict-mcp-config`. A
scorer grading untrusted text must not be reachable by a hook that edits what
it sees, and must not be able to read files or run commands on the strength of
that text.

When the judge is requested and every transport fails, the fallback is announced
on stderr unconditionally and counted in the run log (`judge_failures`). It is
never a silent default — silence is what hid the dead judge.

**Inspect and calibrate — `judge-check`:**

```bash
bookkeeping judge-check                    # which transports are CONFIGURED + blocker for each that is not
bookkeeping judge-check --verify           # actually round-trip the transport with a probe item
bookkeeping judge-check --sample 20        # shadow-score 20 in-band items: heuristic vs judge
bookkeeping judge-check --sample 20 --labels sheet.json   # + blinded labeling sheet (+ sheet.key.json)
```

`CONFIGURED` means prerequisites are present — a binary on PATH, a spec file, a
credential. It does **not** mean judging works; an expired token satisfies every
static check. `--verify` is the round trip, and it is the only output that
proves the judge functions.

`--labels` writes TWO files: a blinded sheet with no machine scores, and a
`.key.json` holding them. Label the sheet fully before opening the key — an
instruction not to look at an anchor printed in the same row is prose standing
in for a control.

`--sample` reports exact agreement, decision flips (items that cross the
promote boundary), and mean delta. It is a **head sample** — the first in-band
items of the earliest source file, so typically one source and one day, not a
random draw from the corpus. It measures the two scorers against **each
other** — it does not say which is right. `--labels` emits the sheet a human
settles that with; label without reading the machine scores first, or the label
is anchored rather than independent.

Cost note: **highly variable, and the two figures below do not divide into each
other** — say so rather than pick one. Single dimension calls were measured at
5.5s and at 31.6s on the same machine, which puts an authored-transport item
(three calls) somewhere between ~16s and ~95s. Separately, a 6-item
`judge-check --sample` took 11m41s wall = 117s/item, *above* that range.

Per-call latency is the largest known term, and the figure below is an
ESTIMATE, not a full attribution: 6 items x 3 dimension calls = 18 calls, which
at the 31.6s end would be 569s — about 81% of the 701s observed. It applies one
observed call latency to all 18 calls, which is why it is an estimate; the
remaining ~19% is unattributed and nobody has instrumented the phases
separately. Ingest is **not** the explanation. An
earlier version of this note asserted that sampling "ingests and heuristically
scores every discovered extract before it judges anything"; that is false
(`cmd_judge_check` stops at the first files that fill the band) and full ingest
was measured at 3.67s for the entire corpus regardless. It was a mechanism
invented to explain a number instead of dividing it.

So the figure to distrust is the 5.5s call, not the 117s item. Treat this as
tens of seconds to ~2 minutes per item, dominated by per-call latency, and
re-measure before relying on it. The spread alone rules the judge out of the
always-on ingest loop.

Scoring output is written to the raw extract file as a YAML front-matter annotation per item.

### Stage 3 — SCATTER

From each high-scoring source item, extract N candidate entity concepts (0–5 per source). Each candidate becomes a potential entity page in the graph. Scatter means one source can produce multiple entities — a single research thread might yield a tool entity, a person entity, a technique entity, and a project entity.

Candidates are output as slug strings (lowercase, hyphen-separated): `e.g. "bitnet-ternary-weights", "karpathy-llm-wiki-pattern"`.

### Stage 4 — RESOLVE

Deduplicate candidates against the existing entity graph:

1. **Exact wikilink slug match** — check `research/entities/{type}/{slug}.md` directly
2. **Fuzzy title match** — compare candidate title against all existing entity titles (cutoff: 0.80 similarity). If match found → update existing entity. If no match → create new entity.

Resolution prevents graph fragmentation. A single concept must not appear under multiple slugs.

### Stage 5 — PROMOTE

Apply promotion decision based on total score:

| Score | Action | Destination |
|-------|--------|-------------|
| ≥ 5   | Promote | `research/entities/{type}/{slug}.md` (Layer 3) |
| 3–4   | Hold    | Stays in `research/notes/YYYY-MM-DD-{source}-raw.md` (Layer 2) |
| ≤ 2   | Discard | Dropped, not written |

Entity page type is inferred from the candidate context; the live list is `ENTITY_TYPES` in `scripts/bookkeeping.py` (`concept`, `pattern`, `tool`, `person`, `project`, `discovery`, `question`, `framework-refinement`, `industry-pattern`, `persona`, `org`). Use the template at `templates/entity-page.md` when creating new pages.

### Grounding floor (promotion stage, runs first)

The per-axis floor the Nous axes cannot supply. On workspace#789 (2026-09-27) 13 of 14 new pages were auto-promoted and all 13 were junk as written (review dropped 12 and rewrote the 13th; the 14th was hand-authored), and the (n, s, r) scores could not have told them apart: they are **note-level**, so the kept `person/beata-halassy` and the junk `pattern/insane-method` carry an identical `6/9 (n=3 s=3 r=0)`; a `relevance >= 1 ∧ specificity >= 1` floor refuses the kept page and admits three junk ones. That is why `AXIS_FLOOR` stays 0 (a test pins it against the fixture). The junk is an *attribution* failure — `core_claim` is derived per item, the slug per candidate — so the floor is on a per-item axis instead:

- **Grounding** of the would-be page: **2** if the item's section heading *is* the entity (the slug covers at least half the heading's content tokens, or the heading begins with the entity's name); **1** if the derived claim, with that heading stripped, **names** the entity — a `person` by surname, a one- or two-word name by every word (`jev-judge` needs "jev" *and* "judge"; `design-review` is not named by "we review …"), a longer claim-shaped slug by its head noun plus at least half its content words; **0** otherwise. Tokens are whole words, plural- and accent-folded. `GROUNDING_FLOOR = 1`. The floor is necessary, not sufficient — a grounded page still goes on to the coherence gate.
- Format-2 ingest records the heading as `metadata.section_heading`; items without one (paragraph, Moltbook formats) are never stripped. The key is **reserved**: `_make_item` drops it from source-supplied metadata, so frontmatter or a JSONL object cannot forge a heading (and with it grounding 2).
- **Deterministic and local**, so unlike the coherence gate it cannot fail open; it runs before the coherence call, so a refused page costs no call. A refusal prints `SKIP (grounding < 1 …)` and is counted as `grounding.refused` in every run-log entry. Nothing is quarantined — the verdict is a pure function of the raw note, which stays in Layer 2.
- Measured with this code on the door's real input (60 raw notes → 134 would-be new pages): refuses 124 — 107 of the 114 the coherence gate rejects and 17 of its 20 accepts, of which a hand read finds ~3 arguably legitimate (`system-initiative`, `freepik-company`, `long-proof`). **Not a page-quality rule** — hand-written claims omit the title legitimately (668 of 1,074 hand-authored pages, 62.2%, would fail it); it applies only to claims *derived* from an item, i.e. the new-page path of `promote_item`.
- Fixture: `tests/fixtures/pr789/entities.json` (13 junk refused, 2 kept pass).

### Entity coherence gate (promotion stage)

The sum gate's false positives are **identity** failures, not score failures: a section heading, a person's name, or a phrase lifted from a source document, filed as a `concept` with a claim that is not about its own title. Measured 2026-09-18 (jev-1.13.0) on the 9 human-quarantined junk pages (`~/.config/bookkeeping/quarantine/2026-09-16-nous-sum-gate/`) vs 30 accepted pages: specificity AUC **0.60**, relevance AUC **0.81**, and a Noul question — *is the title a coherent knowledge-graph node that the core_claim is genuinely about, vs a heading / name / lifted phrase?* — AUC **0.98**. The three Nous axes do not measure entity identity; this gate does, once, at the single door every new page passes through (`promote_item`, new-page path only — the existing-page update branch is never gated).

- **Transport:** one stdlib POST to `https://api.typesafe.ai/v1/systemone` (`model: jev-latest`, one `noul` question), 10 s timeout, no SDK. Key from `TYPESAFE_API_KEY`, else `~/.config/typesafe/api_key`; the key must be a single printable token (no spaces, no line breaks) or it is refused unsent.
- **Type-aware criteria** (`COHERENCE_CRITERIA` in `scripts/bookkeeping.py`): for `tool` / `person` / `project` / `org` a product or personal NAME as the title is legitimate — the question is whether the claim is about that named thing; for every other type in `ENTITY_TYPES` (`concept`, `pattern`, `question`, `discovery`, `framework-refinement`, `industry-pattern`, `persona` — persona pages are preference claims, not identity names) the title must name the concept the claim asserts, and a heading, a name, or a lifted phrase is `false`. The two sets partition `ENTITY_TYPES` and a test enforces it, so a new type forces a criteria decision.
- **Verdict:** `p < COHERENCE_THRESHOLD` (0.5) ⇒ the page is **not** written to `research/entities/`; it goes to `~/.config/bookkeeping/quarantine/<YYYY-MM-DD>-coherence/<type>_<slug>.md` with `coherence: <p>` and `coherence_gate: rejected` added to its frontmatter, and one line is printed. Quarantine, never delete — recovery is `mv` + deleting those two lines.
- **Memory** (two doors, both counted as `remembered`): within a run, a `(type, slug)` refused earlier is skipped without a call — this is the only door a `--dry-run` has, since it writes no file; across runs, while `<type>_<slug>.md` sits in *any* dated quarantine dir the item is skipped and the quarantined copy is never overwritten. A permanently junk item is charged once, not once per run. Moving the file out (recovery) or deleting it (re-judge) re-opens the question on the next run.
- **Unavailable** (no key, malformed key, HTTP error, timeout, malformed response) ⇒ pass-through (the page is written, status quo) but LOUD: one stderr line per distinct cause per run, and counted. The key is refused before a request is built if it is not a single printable token, and is redacted from any cause line. A failed quarantine *write* is also loud; the page is then written nowhere and the item is re-judged next run.
- **Counters:** `coherence.{enabled,checked,rejected,remembered,unavailable}` in every run-log entry and in the `run` summary line `Coherence gate: on | checked: N | rejected: N | remembered: N | unavailable: N`.
- **`--dry-run` still asks the classifier** — the verdict *is* the preview (`dry-run: would QUARANTINE …`) — but writes neither the page nor the quarantine file. A dry run is therefore not free or offline.
- **Knobs:** `BOOKKEEPING_COHERENCE_GATE=0` disables explicitly (transport never called, memory ignored). Default ON when a key is present. That default was *not* acceptable for the scoring judge, which runs on every in-band item, costs seconds per call and changes scores; this gate runs only on new promotions (a handful per run), takes ~300 ms and ~$0.00005 per call, and quarantines rather than deletes. What default-on *does* change: the slug, title, derived `core_claim` and first 1500 chars of every **new** page leave the machine to a third-party API — opt out with the knob if that is not acceptable for a corpus.

### Graph root resolution

Every command resolves `(root, entities_dir, catalog)` once, at import. Precedence: a top-level `knowledge:` block in the nearest `.control/policy.yaml` > `KG_ROOT` / `KG_ENTITIES_DIR` / `KG_CATALOG` / legacy `BROOMVA_ROOT` (explicit overrides; `KG_NO_POLICY=1` skips the policy layer) > **the nearest enclosing git toplevel that holds `research/entities`** (a `.git` dir, or a worktree's `.git` file — so a worktree resolves to itself; a nested repo without a graph is walked past) > `~/broomva`, only when CWD is inside no such checkout. Before 1.5.0 the last layer applied from anywhere, so `index` run from a worktree overwrote the main checkout's catalog. `kg` carries the same resolver.

### Stage 6 — SYNTHESIZE

After promotion, scan the entity graph for clusters: groups of 3 or more entities that share tags or reference each other via `[[wikilinks]]`. For each cluster:

1. Check if a synthesis note already exists in `research/notes/` covering that cluster
2. If not → flag the cluster as a synthesis candidate with a suggested filename: `YYYY-MM-DD-{cluster-topic}-synthesis.md`
3. Synthesis candidates are written to `~/.config/bookkeeping/status.json` under `pending_synthesis`

Synthesis notes are not auto-generated — they are flagged for human or agent authorship. The bookkeeping skill creates the scaffold, not the prose.

### Stage 7 — LINT

Validate all entity pages in `research/entities/` against the schema (full spec in `references/entity-schema.md`):

Errors (block-worthy, surfaced as `error`):

- `core_claim` field present and ≤ 140 characters
- `sources` field present and non-empty
- `related` field uses `[[wikilink]]` format (not bare URLs or plain text)

Warnings (non-breaking nudges, surfaced as `warning`):

- No broken wikilinks (all `[[slug]]` references resolve to existing entity files)
- `status` field is one of: `raw`, `candidate`, `entity`, `synthesis`, `archived`
- `type` field is one of: `concept`, `pattern`, `tool`, `person`, `project`, `discovery`, `question`, `framework-refinement`, `industry-pattern`, `persona`, `org`
- **Frontmatter dates are quoted** — an unquoted `created: 2026-05-30` re-serializes to a full timestamp on edit and breaks `YYYY-MM-DD` queries; mechanically auto-fixable via `lint --fix`
- **Tags are controlled-vocabulary** — every tag ∈ `research/entities/_tags.md` (81 canonical tags); no missing tags, no type-redundant tags (a tag equal to `type:`); the check no-ops if `_tags.md` is absent
- **`contradicts:` carries a resolution** — a non-empty `contradicts:` list must have a body `## Contradiction`/`## Resolution` section
- `## Timeline` entries (when present) carry a leading ISO date

Opt-in temporal audit (`lint --all --temporal`; warning-only):

- **`updated` is not older than dated evidence** — warns when valid ISO dates
  in `sources` or the body are later than frontmatter `updated`; invalid dates
  and dates after the audit date are ignored
- **Mutable state is dated where it is detached from context** — warns on
  catalog-visible current-state claims, mutable headings, and explicit state
  labels without an inline `YYYY-MM-DD` as-of marker
- **The typed revision envelope is well-formed** — `recorded_at` parses and is
  not in the future; `valid_from` parses (a *future* `valid_from` is fine — a
  scheduled change is not a defect); `supersedes` entries are `[[wikilink]]`s
  that resolve, are not self-references, and are not newer than the record that
  supersedes them; `supersedes` carries a `revision_link` and vice versa. All
  four fields stay **optional** — a page without them produces no finding
- **Semantic reconciliation remains outside lint** — the audit does not decide
  whether claims contradict or supersede one another, nor whether a
  supersession is correct; it only checks what the write path is supposed to
  guarantee

> Enum values defer to `references/entity-schema.md` (the schema is authoritative for `type`/`status` membership); SKILL.md remains authoritative for thresholds, stages, and layers.

Lint report is written to stdout and to `~/.config/bookkeeping/status.json` under `lint_errors`. A non-zero lint error count does NOT block the pipeline — it surfaces warnings only. `lint --fix` mechanically repairs the auto-fixable classes (`related:` format, unquoted dates).

---

## Self-Maintenance Rules (CRITICAL)

These rules govern any agent that modifies files in this skill. They are enforced by reasoning, not by hooks. When you touch any file under `skills/bookkeeping/`, you MUST apply these rules before completing the task.

**Rule 1 — Stage count consistency**
When adding, removing, or renaming a pipeline stage: update the stage count and stage list in BOTH this file AND `README.md`. The stage count in both files must always match.

**Rule 2 — Scoring threshold consistency**
When changing the promote threshold (currently ≥5), the discard threshold (currently ≤2), or the heuristic fast-path boundaries (currently ≤2 / ≥7): update BOTH this file AND `references/scoring-rubric.md`. The two files must always agree on all threshold values.

**Rule 3 — Entity schema consistency**
When adding a new entity `type` value or a new `status` value: update BOTH `references/entity-schema.md` AND `templates/entity-page.md`. The template must always reflect all valid field values defined in the schema.

**Rule 4 — Layer definition consistency**
When changing the layer count (currently 4) or redefining layer boundaries: update BOTH this file AND `references/promotion-workflow.md`. All destination path patterns must be consistent across both files.

**Rule 5 — Post-modification verification**
After any modification to any file in this skill, run:
```bash
python3 scripts/bookkeeping.py lint --all
python3 scripts/bookkeeping.py status
```
Fix all lint errors before considering the task complete.

**Rule 6 — SKILL.md is authoritative**
This SKILL.md is the single source of truth for all thresholds, stage definitions, and layer boundaries. All other files in this skill (references/, templates/, README.md) defer to it. If a conflict exists between this file and any other file, this file wins and the other file must be updated.

---

## CLI Reference

```bash
python3 scripts/bookkeeping.py run                    # Full 7-stage pipeline
python3 scripts/bookkeeping.py replay                 # Score against frozen snapshot (no writes)
python3 scripts/bookkeeping.py replay --commit        # Apply replay's proposed promotions
python3 scripts/bookkeeping.py ingest --source FILE   # Ingest single file
python3 scripts/bookkeeping.py score --file FILE      # Score items in raw extract
python3 scripts/bookkeeping.py promote --file FILE    # Promote pending items
python3 scripts/bookkeeping.py synthesize             # Detect clusters, flag candidates
python3 scripts/bookkeeping.py synthesize --gaps      # + ranked ## Gaps report (goal-formation)
python3 scripts/bookkeeping.py synthesize --gaps --backlog  # JSON Backlog ticket candidates → file via Linear MCP
python3 scripts/bookkeeping.py lint --all             # Validate all entity pages
python3 scripts/bookkeeping.py lint --all --health    # + 0-100 health score + remediation plan
python3 scripts/bookkeeping.py lint --all --temporal  # + warning-only temporal-drift audit
python3 scripts/bookkeeping.py bench                  # Retrieval benchmark (P@5/R@5/MRR)
python3 scripts/bookkeeping.py status                 # Show knowledge graph stats
python3 scripts/bookkeeping.py query "concept-slug"   # Find and display entity page
python3 scripts/bookkeeping.py merge dupe canonical   # Fold a dup into a canonical (tombstone)
python3 scripts/bookkeeping.py revise --entity new --supersedes old \
        --revision-link REF                           # Record an explicit correction
python3 scripts/bookkeeping.py backfill-revisions     # Replay recorded merges into the envelope
```

The pipeline remains **7 stages** (Ingest → Score → Scatter → Resolve → Promote → Synthesize → Lint). `bench`, `synthesize --gaps`, `lint --health`, `lint --temporal`, `merge`, `revise`, and `backfill-revisions` are *subcommands/flags*, not new pipeline stages.

All commands accept `--dry-run` to preview changes without writing. All commands write structured output to `~/.config/bookkeeping/run-log.jsonl`.

### `bench` — retrieval benchmark (P@k / R@k / MRR)

Measures the **same two-tier retrieval the `kg` load skill performs** (tier-1 catalog scoring over `docs/knowledge-index.md`; tier-2 body-grep fallback) against a labeled fixture, so the numbers describe real retrieval quality, not a mock.

```bash
python3 scripts/bookkeeping.py bench                            # default fixture, k=5
python3 scripts/bookkeeping.py bench --k 10 --json              # widen cutoff, JSON out
python3 scripts/bookkeeping.py bench --fixture path/to.jsonl    # custom fixture
```

- Fixture: `fixtures/brainbench.jsonl` — one `{"query","expected":["type/slug",...],"notes"}` per line. Every `expected` id is a real `research/entities/{type}/{slug}` page.
- Metrics are macro-averaged (mean of per-query P@k / R@k / reciprocal-rank). Single-gold queries cap P@k at `1/k` by construction — read P@k alongside R@k and MRR.
- Machine-readable results are written to `~/.config/bookkeeping/bench-latest.json` (for trend tracking across catalog regenerations).
- Unit tests for the metric math + gaps→backlog export: `scripts/test_bench.py` (stdlib `unittest`, 46 cases). **CI-gated** on every push/PR via `.github/workflows/test.yml` (test suite + a CLI smoke) so retrieval metrics and the export can't silently regress.

### `synthesize --gaps` — gap analysis (goal-formation)

A **gap** is where the graph is incomplete in a way that blocks retrieval or signals an unanswered research question: (a) unresolved `[[wikilink]]` targets, (b) missing/over-long `core_claim`, (c) highly-referenced **stubs** (short body but ≥3 inbound refs). Each gap is scored by inbound-reference frequency and emitted as a ranked `## Gaps` markdown section. High-leverage gaps (≥3 inbound refs, or broken links with ≥2 referrers) are written to `~/.config/bookkeeping/status.json` under `pending_gaps` — candidate **Backlog** research questions (the script never calls Linear). `pending_gaps` is recomputed on every `synthesize` run regardless of the `--gaps` flag.

**`--backlog` — Pillar-2 goal-formation close.** `synthesize --gaps --backlog [--backlog-cap N]` emits the high-leverage gaps as JSON **ticket candidates** (`title`, `body`, stable `dedup_key`, `leverage`), ranked by leverage and **deduped** (the same slug across type dirs — e.g. `concept|pattern|tool/bstack` — collapses to one candidate). The engine **never files tickets**: filing is **agent-mediated through the Linear MCP** after a **P20 reasoning-enforced quality pass** ("is this a real, actionable research question?"). This honors the workspace's *Linear-via-MCP, never CLI/API* rule (the CLI defaults to the wrong workspace) and keeps the knowledge engine free of network side-effects. The `dedup_key` (`kg-gap:<kind>:<slug>`) lets the filer skip gaps already promoted, so the loop is idempotent across runs. Flow: `synthesize --gaps --backlog` → agent reads candidates → quality-filters → files top-N into Linear Backlog via MCP.

### `lint --health` — health score + remediation plan

Computes a `0-100` health score — `100 * (1 - weighted_issues / total_entities)`, errors weighted `1.0`, warnings `0.3`, capped at `[0,100]` — and prints a **dependency-ordered remediation plan**: broken-wikilink TARGETS first (creating one missing page unblocks every referrer), then missing/over-long `core_claim`, then enum non-conformance. Implied by `lint --all`.

### `lint --temporal` — calibrated temporal-drift warnings

Adds an explicit, non-blocking audit for temporal bookkeeping defects that can
be detected mechanically without pretending to understand claim semantics:

```bash
python3 scripts/bookkeeping.py lint --all --temporal
python3 scripts/bookkeeping.py lint --file path/to/entity.md --temporal
```

The audit checks two conditions: frontmatter `updated` predates newer dated
source/body evidence, and mutable state appears in a catalog-visible
`core_claim`, state-labelled heading, or explicit label line without an inline
ISO as-of date. It deliberately excludes arbitrary present-tense prose and
generic `Open Questions` sections. Findings are `warning` severity, so they do
not fail the command when no ordinary lint errors exist. Default `lint` output
is unchanged unless `--temporal` is passed.

This is an emitter-first maintenance signal, not a revision-graph validator.
Semantic contradiction and temporal authority remain Dream (P13) review work.
Calibration and known limitations are recorded in
`references/temporal-drift-audit.md`.

### `revise` — record an explicit correction

The write side of the typed temporal revision envelope. Four frontmatter fields
carry different clocks and different provenance rules; the governing constraint
is that **none of them may be produced by reading prose**.

| Field | Meaning | Who writes it |
|---|---|---|
| `recorded_at` | System time — when the graph recorded this state | `promote`, mechanically |
| `valid_from` | Claim-effective time — when the claim became true | Only a source or revision that *supplies* it |
| `supersedes` | Records this page replaces | `revise` / `merge` only |
| `revision_link` | The record that authorized the supersession | `revise` / `merge` only |

```bash
python3 scripts/bookkeeping.py revise \
  --entity new-belief --supersedes old-belief \
  --revision-link "https://linear.app/broomva/issue/BRO-1234" \
  [--valid-from 2026-04-15] [--dry-run]
```

`promote` stamps `recorded_at` from system time and writes `valid_from` only
when the raw item carries an explicit `metadata.valid_from`; it never emits
`supersedes` or `revision_link`, whatever the content asserts. `merge` records
the canonical as superseding the dup, with the tombstone as its authorizing
record. `revise` refuses (non-zero exit) on a missing entity, an unresolvable
superseded slug, a self-supersession, or a non-ISO `--valid-from`, and is
byte-identical on replay — repeated revisions union rather than overwrite.

`backfill-revisions` replays supersessions the graph already recorded — a
`status: merged` tombstone names the canonical, dates the merge, and is itself
the authorizing record — stamping `recorded_at` with the HISTORICAL merge date.
It is the sanctioned way a pre-envelope page acquires the fields, and it built
the corpus the audit was calibrated on. It never derives supersessions from
`aliases:` (those are `aka` search synonyms) or from prose.

Envelope findings are warning-only and appear only under `--temporal`.
Calibrated 2026-08-10 against that corpus: **zero envelope findings on every
migrated page, 13/13 audit branches reachable** (no false-positive rate is
quoted — the corpus has no coherent sampling unit for one). There is still **no hard gate**, for a measured reason — 10
of the 13 checks are DEFINITIONAL (the predicate *is* the property, so its
false-positive rate asks whether `x == x`) and only 3 are proxies with a gap a
rate could measure; none of those 3 is measured by this corpus; the 1 genuine
heuristic is unmeasurable on real data because tombstones carry no
`recorded_at`; and 5 of 943 pages carrying the envelope is not enough
operational history to gate on. Receipts:
`references/supersession-calibration-2026-08-10.json`. Full contract:
`references/temporal-revision-envelope.md`.

### `replay` — closes the shadow-dream corruption mode

`bookkeeping run` reads from the same graph it writes to. The local research entity at `research/entities/concept/multi-tier-dreaming.md` (scored 9/9) explicitly identifies this as a *"shadow dream"* — gather + consolidate without the **replay** phase. The corruption mode hasn't fired yet only because the graph is small.

`replay` adds the missing replay phase:

1. **Gather** — read the source files (or auto-discover all `*-raw.md`)
2. **Replay** — copy `research/entities/` into a tempdir; score+promote against the *frozen* copy
3. **Prune** — items below threshold or failing lint are flagged; replay reports counts
4. **Consolidate** — pass `--commit` to apply the proposed promotions to the live graph (re-runs the scoring against the live state to ensure idempotence)
5. **Index** — `git diff research/entities/` is the audit trail; the agent or human inspects before merging

Without `--commit`, replay is **read-only** — pure diagnostic. With `--commit`, replay re-runs the pipeline against the live graph (so the diff applies cleanly to the same starting state the human approved).

Smoke-tested against the live workspace: 3 raw extracts gathered, 178 entities frozen in tmpdir, 96 items scored (15 below threshold, 81 would-promote, mean 5.4/9). No writes without `--commit`.

### `render` — Category B projection (MD → single-file HTML)

```bash
bookkeeping render <path>             # render a single .md file
bookkeeping render <dir>/             # glob *-synthesis.md in directory
bookkeeping render --layer 4          # all Layer-4 synthesis notes
bookkeeping render --link-html        # rewrite [[slug]] → .html targets
bookkeeping render --verbose          # log each rendered file
```

Produces a deterministic single-file HTML projection alongside the source MD.
The HTML carries `canonical:` frontmatter pointing back to the source MD; it
is gitignored by default and regenerable. See the **Format Discernment (P18 ·
Audience)** section below for when to use this vs keep MD-only.

`render` is the **lossless floor**, not the rich ceiling: it can only express
what CommonMark expresses (no diagrams, SVG, charts, or interactivity — by
design, "avoids client-side dependencies"). When the artifact's *presentation*
carries knowledge, do **not** reach for `render` — generatively author a
**Category C** rich HTML document (see below).

---

## Format Discernment (P18 · Audience)

Before emitting any artifact, classify into one of three categories. Choose
format from the category, not the other way around.

### Category A — Substrate (MD, always)

Any artifact another agent, governance system, or `bookkeeping` will re-read,
lint, score, or grep:

- `research/entities/**/*.md` — graph nodes
- `research/notes/*-raw.md` — Layer 2 extracts
- `research/notes/*-synthesis.md` — Layer 4 canonical (HTML is a *projection*, see B)
- `CLAUDE.md`, `AGENTS.md`, `METALAYER.md` — governance, L3
- `skills/*/SKILL.md` — skill packages, agent-consumed
- `docs/superpowers/specs/*.md`, `plans/*.md` — superpowers consumed
- `docs/conversations/*.md` — conversation bridge output
- `.control/policy.yaml`, `schemas/*.json` — already non-MD, same category

**Invariant:** HTML breaks substrate. MD-only. Frontmatter at top.

### Category B — Projection (MD canonical + HTML on demand)

Artifacts authored and re-edited as text but consumed by a human as a rendered
document:

- Layer 4 synthesis notes (blog-post candidates)
- Weekly retros, status updates, post-mortems
- Architecture explainers (large reviews)

**Behavior:** MD is source-of-truth (lintable, scored, agent-readable).
`bookkeeping render <path>` projects to HTML for human-read events. HTML is
`.gitignored`, regenerable, carries `canonical:` frontmatter pointing back
to MD.

### Category C — Native (generatively authored; the medium IS the value)

Artifacts where the **presentation itself carries knowledge** — diagrams,
interactive views, or multiple data-representation modalities convey what
prose-in-markdown cannot. No useful MD source exists (an MD version would lose
the thing that makes the artifact valuable). Examples: architecture and
decision documents, system explainers, dashboards, interactive demos, drag-drop
boards, animation sandboxes; future `.ipynb` analyses, `.tldr` canvases,
`.svg` packs.

**This is NOT a `render` projection and NOT a template fill.** The agent
**generatively authors** the artifact — bespoke for *this* content, in *this*
session, informed by the actual data + relevant `research/entities/` + session
research. There is deliberately **no component/template library to assemble
from**: a fixed kit ossifies and under-fits the content. Generative authoring
adapts to each context. This skill *directs* the generation (below); the
agent's generative capacity is the engine.

**Generation menu** — pick the modalities the content needs, author them fresh:

| When the content is… | Generate… |
|---|---|
| A system / architecture | inline **SVG** diagram, hand-authored for that system |
| A process / workflow / state machine / sequence | inlined **Mermaid** or SVG |
| Tradeoffs / options / criteria | sortable/filterable **tables**, interactive **decision matrices** |
| A layered system | **tier-stack** diagram |
| Time / evolution / roadmap | **timeline** |
| A hierarchy / taxonomy | **tree / nested** view |
| Quantitative data | **charts** (inline SVG or inlined lib), **metric/stat cards** |
| Dense reference | **collapsible** sections, **tabs**, sticky **table-of-contents** nav |
| Relationships | **node-link graph** |
| Code / config | annotated, syntax-highlighted blocks |

**Constraints (the how — binding):**

1. **Self-contained single file.** Inline all CSS/JS/SVG; system-font stack;
   **no external CDN or network dependency** (deterministic, offline, portable,
   archival — the same value `render` enforces). If a library is genuinely
   needed (e.g., Mermaid), inline it; don't CDN-link it.
2. **Accessible & responsive.** Semantic HTML, light/dark, keyboard-navigable,
   legible at any width; degrades to readable static content with JS disabled.
3. **Graph-integrated.** Carry frontmatter in the format's idiomatic carrier
   (HTML-comment YAML for `.html`, notebook `metadata` for `.ipynb`, sidecar
   `.meta.yaml` for binaries) with at least `type` + `slug`; render wikilinks as
   `<a data-relation="…">` anchors; include `canonical:` when an MD source
   exists. Category-C artifacts still pass `bookkeeping lint` and rejoin the
   graph.
4. **Rich by default.** Once an artifact qualifies as C, author it *to the
   ceiling*, not to the minimum that clears the predicate. Default to the full
   expressive range the content can carry: diagrams + flows + the right
   data-representation modalities from the menu, purposeful motion and
   interaction (transitions, hover/focus affordances, expand/collapse, filter,
   sort, step-through), and the depth the subject actually warrants. **Length
   and structure follow the content, not a cap** — a dense architecture or
   decision doc may be long, sectioned, tabbed, or **multiple linked HTML
   pages** (an `index.html` + sibling pages under one `docs/<arc>/` dir, linked
   with relative `<a href>`); a small explainer stays one tight page. "As
   complex as needed" is the rule; gratuitous complexity for its own sake is
   still the anti-pattern. The floor (`render`) is for B; C does not settle for
   floor-grade output.

**Design-craft composition (the polish layer).** The constraints above are the
*correctness* floor (portable, accessible, graph-integrated). They are not a
*visual-craft* bar — and craft is deliberately **not** machine-checked
(the workspace declined to promote "premium/best-in-class" to an invariant
because it has no lint gate; see the Ritual-vs-Substance table in `CLAUDE.md`).
Craft therefore stays a **convention**, but a *named, discoverable* one: when
generatively authoring a Category-C artifact, **compose with the design layer**
for visual quality rather than relying on raw generative instinct —

| Skill | Use for |
|---|---|
| `ui-ux-pro-max` (plugin) | layout systems, 50+ styles, color palettes, font pairings, chart types — the broad UI/UX intelligence menu |
| `impeccable` | visual hierarchy, information architecture, cognitive-load reduction, spacing/typography/alignment audit, ambitious-but-tasteful visual effects |
| `make-interfaces-feel-better` / `emil-design-eng` | interaction & motion polish — the invisible details (easing, timing, affordance, state transitions) that make a doc feel crafted |
| `arcan-glass` | Broomva brand tokens (Arcan Glass design language) when the artifact is brand-facing |

Pull from these at authoring time the same way you pull modalities from the
generation menu. They set the *craft* bar; the four binding constraints set the
*correctness* floor. Both apply — neither substitutes for the other. Because
craft is a convention not a gate, a C artifact never *fails lint* for being
plain; but the standing instruction is to author rich, not plain.

**Floor vs ceiling.** `bookkeeping render` (Category B) is the deterministic
*floor* — a lossless MD→HTML projection of text-expressible content. Category C
is the *ceiling* — generatively authored rich HTML where the medium is the
value. Never force `render` to be rich; never settle for `render` when the
content deserves C.

### Predicate Test

The agent applies these in order at artifact-creation time:

1. Will any agent or substrate re-read this as text? → **A**
2. Does an MD source-of-truth exist (or should exist), with content fully
   expressible as text? → **B** (`render` projects it on demand)
3. Does the artifact's **presentation carry knowledge** — diagrams, interaction,
   or multiple data-representation modalities markdown can't hold? → **C**
   (generatively author rich self-contained HTML; not a `render` projection,
   not a template)

**Tiebreaker:** when ambiguous between B and C, default to **B** (reversible,
lower disruption). But do not let the tiebreaker downgrade a genuinely visual /
interactive artifact to a flat projection — if the modalities in the generation
menu would materially help the reader, it is **C**.

### Enforcement

Four lint checks via `bookkeeping lint --all`:

| Check | Severity | Trigger |
|-------|----------|---------|
| `stale_projection` | warning | `<note>.md` mtime > `<note>.html` mtime |
| `broken_canonical` | error | `<note>.html`'s `canonical:` field doesn't resolve to existing sibling MD |
| `substrate_violation` | error | Non-`.md` file under `research/entities/` (hidden dirs like `.lago-blobs/` excluded) |
| `unregistered_c` | warning | `.html` under `research/notes/` with no frontmatter AND no sibling MD |

Full reference and worked examples: `references/format-discernment.md`.

---

## 4-Layer Knowledge Lifecycle

```
Layer 1 — Ephemeral (never stored)
  Social threads, passing ideas, unprocessed conversation fragments.
  Lives only in context windows. Discarded after session.

Layer 2 — Raw Extracts  research/notes/YYYY-MM-DD-{source}-raw.md
  Ingested + scored items. Score 3-4 items rest here.
  Reviewed manually or swept by next bookkeeping run.

Layer 3 — Entity Pages  research/entities/{type}/{slug}.md
  Promoted items (score ≥5). Structured, query-able, wikilinked.
  The permanent knowledge graph. Source of truth for the vault.

Layer 4 — Synthesis Notes  research/notes/YYYY-MM-DD-{topic}-synthesis.md
  Cluster-level understanding. Written when ≥3 entities share a theme.
  Blog candidates and architectural decisions live here.
```

---

## Output Locations

| Output | Path |
|--------|------|
| Layer 2 raw extracts | `research/notes/YYYY-MM-DD-{source}-raw.md` |
| Layer 3 entity pages | `research/entities/{type}/{slug}.md` |
| Layer 4 synthesis notes | `research/notes/YYYY-MM-DD-{topic}-synthesis.md` |
| Run log (JSONL) | `~/.config/bookkeeping/run-log.jsonl` |
| Status + lint report | `~/.config/bookkeeping/status.json` |

---

## Integration Points

| Skill | Integration |
|-------|-------------|
| `social-intelligence` | Delegates Phase 2 (Knowledge Extraction Loop) entirely to bookkeeping. After each engagement run, calls `bookkeeping run` on the loop-log.jsonl. |
| `knowledge-graph-memory` | Receives entity page paths after promotion. Indexes them into the Obsidian vault via the symlink layer. |
| `content-creation` | Receives blog candidate flags from `status.json` → `pending_synthesis`. Picks up entity wikilinks as source material. |
| `deep-dive-research` | Outputs raw research logs that bookkeeping ingests. Ensures research sessions feed the permanent entity graph, not just the conversation transcript. |
| `CLAUDE.md P6` | This skill is bstack primitive P6. Listed alongside P1–P20 in the Bstack Core Automation Primitives table. All sessions that produce knowledge are expected to run bookkeeping before closing. |

---

## LLM Judge Spec

Used in Stage 2 for the ambiguous band (score 3–6). The judge is called with the item text and a snapshot of relevant existing entities.

**System prompt:**
```
You are a knowledge quality evaluator for a personal knowledge OS (the Broomva bstack).
Your job is to score extracted knowledge items on three dimensions and decide whether to
promote them into the permanent entity graph.

Scoring dimensions (each 0–3):
  novelty      — 0: already well-represented in graph. 3: genuinely new concept or framing.
  specificity  — 0: vague, generic, or obvious. 3: concrete, named, actionable.
  relevance    — 0: unrelated to active projects or research threads. 3: directly applicable.

Promotion threshold: total ≥ 5 → promote = true.

Output ONLY valid JSON. No markdown fences, no explanation outside the JSON object.
```

**User prompt template:**
```
ITEM TEXT:
{item_content}

EXISTING ENTITY GRAPH CONTEXT (relevant excerpts):
{entity_context}

ACTIVE PROJECT TAGS FOR RELEVANCE SCORING:
{active_tags}

Score this item and identify candidate entity slugs it could produce.

Output format:
{
  "novelty": <0-3>,
  "novelty_reason": "<one sentence>",
  "specificity": <0-3>,
  "specificity_reason": "<one sentence>",
  "relevance": <0-3>,
  "relevance_reason": "<one sentence>",
  "total": <0-9>,
  "promote": <true|false>,
  "candidate_entities": ["slug-one", "slug-two"]
}
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/scoring-rubric.md` | Full Nous gate rubric with examples for each score level |
| `references/entity-schema.md` | Complete entity page schema with all valid field values |
| `references/promotion-workflow.md` | Layer definitions, promotion decision tree, status transitions |
| `references/temporal-drift-audit.md` | `lint --temporal` drift detector: contract, precision boundary, calibration |
| `references/temporal-revision-envelope.md` | Typed revision envelope: producer contract, provenance rules, `revise`, `backfill-revisions`, calibration + the no-hard-gate decision |
| `templates/entity-page.md` | Canonical template for new entity pages |
| `scripts/bookkeeping.py` | Main CLI implementation |
