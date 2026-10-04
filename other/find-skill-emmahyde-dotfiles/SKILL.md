---
description: >-
  Scour the internet for proven, well-reviewed, high-quality agentic-CLI
  integrations (plugins, skills, hooks, agents, MCP servers, proxy layers,
  CLAUDE.md / AGENTS.md prompts) for a given topic. Surveys curated awesome
  lists, active communities (Reddit, GitHub, dev blogs), and recent academic
  / engineering best practice. Compares candidates in a tradeoff table,
  justifies pick + rejections, and offers a "use as inspiration"
  hybridization mode that genetically mixes N source approaches into a new
  combined design tailored to the user's workflow.
  <triggers>
    /find-skill, find skill, find plugin, find hook, find agent, find mcp,
    survey integrations, search awesome lists, hybridize skills,
    integration research
  </triggers>
argument-hint: <topic-or-functionality> --scope <scope> [--n <count>] [--inspire <ids>]
---

# find-skill

Survey proven agentic-CLI integrations for a topic, score them, justify a
pick, and offer a tailored hybrid synthesis.

```
/find-skill <topic> --scope <scope> [--n 5] [--inspire 1,3,4]
```

Scopes: `agentic` | `plugin` | `skill` | `hook` | `agent` | `mcp` |
`proxy` | `project-md` | `user-md` (multi-allowed: `--scope plugin,hook`).

Helper scripts live in `scripts/`. Canon source list in
`references/canon-sources.md`.

---

## Output skeleton — render verbatim

Every run emits exactly these seven sections, in this order, with these
banners. The user reads top-to-bottom; do not reorder, do not skip.

```
═══════════════════════════════════════════════════════════
  /find-skill — <topic>   |   scope: <scope>   |   n=<N>
═══════════════════════════════════════════════════════════

▸ STEP 1 — Parse & confirm
▸ STEP 2 — Curated-list sweep
▸ STEP 3 — Community signal pass
▸ STEP 4 — Quality filter
▸ STEP 5 — Compare-and-contrast
▸ STEP 6 — Recommendation + justification
▸ STEP 7 — Hybridize? (interactive)
```

---

## ▸ STEP 1 — Parse & confirm

Echo the parsed inputs. If anything is ambiguous, ask one tight clarifier
and stop until answered.

```
┌─ Inputs ──────────────────────────────────────────────────
│ Topic   : <topic>
│ Scope   : <scope>[, <scope>...]
│ N       : <count>           (default 5, max 10)
│ Inspire : <ids or none>
│ Workflow: <one line about user's current task — read from
│           conversation context, not invented>
└───────────────────────────────────────────────────────────
```

The "Workflow" line matters — it anchors STEP 6 ("choose this if…") and
STEP 7 (hybrid intent). Pull it from what the user has been doing this
session, don't fabricate.

---

## ▸ STEP 2 — Curated-list sweep

Run `scripts/survey.sh <topic> <scope>` for a one-shot fan-out across
awesome.ecosyste.ms, GitHub repo search, and Reddit. Cross-reference with
`references/canon-sources.md` to pick up pinned indexes the search may miss.

Render survivors compactly:

```
┌─ Curated lists & seed repos ──────────────────────────────
│ • <name>  ★<stars>  pushed:<date>  <one-liner>  
│ • …
└───────────────────────────────────────────────────────────
```

Hard cap: 8 lines. If more, demote the rest into STEP 3.

---

## ▸ STEP 3 — Community signal pass

Spawn parallel **haiku** agents (one Agent message, multiple tool blocks)
when raw count > 8 candidates. One agent each:

| Agent       | Task                                          |
|-------------|-----------------------------------------------|
| reddit-haiku| Reddit threads for `<topic>` last 12mo, score≥5 |
| gh-haiku    | GitHub issues/discussions: usage reports, fail modes |
| web-haiku   | Blog posts / HN / dev.to last 12mo            |

Each returns ≤200-word digest + URLs. Dedupe with `scripts/dedupe.sh`.

```
┌─ Community signal ────────────────────────────────────────
│ Reddit  : <N> threads, top: "<title>" (r/<sub>, <score>↑)
│ GitHub  : <N> reports, top: <repo>#<issue>
│ Web     : <N> posts, top: <author>, <date>
└───────────────────────────────────────────────────────────
```

---

## ▸ STEP 4 — Quality filter

Apply the gate. Reject candidates failing ANY:

- Last commit > 12 months AND not in `references/canon-sources.md`
- < 5 stars AND no notable referrer
- Broken install / missing manifest / dead MCP server
- Solo-author + zero closed issues (likely abandoned)

Keep candidates with ≥1 of:

- Active maintenance (commits last 90d)
- Cited in ≥2 independent sources
- In Anthropic cookbook / official MCP registry / academic paper
- Notable maintainer / strong PR throughput

Render the rejection log:

```
┌─ Filter results ──────────────────────────────────────────
│ Kept     : <N>
│ Rejected : <N>  reasons:
│           ✗ <name> — stale (last commit YYYY-MM-DD)
│           ✗ <name> — broken install per <issue>
│           ✗ <name> — duplicate of <name>
└───────────────────────────────────────────────────────────
```

Rejection transparency matters — the user can override.

---

## ▸ STEP 5 — Compare-and-contrast

Render TWO tables. First is the spec sheet, second is the decision-helper.

### 5a. Spec sheet

```
┌─ Candidates ──────────────────────────────────────────────
│ ID │ Name              │ Type   │ ★    │ Pushed     │ Signal
│ 1  │ <name>            │ skill  │ 1.2k │ 2026-04-10 │ canon + 3 reddit
│ 2  │ <name>            │ plugin │ 480  │ 2026-03-22 │ HN front page
│ …
└───────────────────────────────────────────────────────────
```

### 5b. Tradeoffs

```
┌─ Tradeoffs ───────────────────────────────────────────────
│ ID │ Pros                          │ Cons                          │ Choose if…
│ 1  │ tight scope, fast, cached     │ no MCP integration            │ you want a single skill, low ceremony
│ 2  │ batteries-included, MCP+hook  │ heavy; opinionated            │ you want full plugin with hooks pre-wired
│ …
└───────────────────────────────────────────────────────────
```

For each candidate also drop a 3-line block:

```
#<id> <name>
  approach     : <one sentence on the architectural shape>
  distinctive  : <the load-bearing idea — what others lack>
  weakness     : <what it gets wrong / misses>
```

---

## ▸ STEP 6 — Recommendation + justification

This step is **mandatory**. Pick one, then justify both the pick AND every
rejection in the shortlist.

```
┌─ ✅ Recommendation ───────────────────────────────────────
│ Pick: #<id> <name>
│
│ Why it fits <user workflow from STEP 1>:
│   • <reason 1 — concrete, ties to workflow>
│   • <reason 2>
│   • <reason 3 — ideally cites a specific feature>
└───────────────────────────────────────────────────────────

┌─ ❌ Why the others didn't fit ───────────────────────────
│ #<id> <name>: <one-line reason tied to workflow>
│ #<id> <name>: <one-line reason tied to workflow>
│ #<id> <name>: <one-line reason tied to workflow>
└───────────────────────────────────────────────────────────
```

Rejection reasons must be **workflow-relative**, not absolute. "Uses Python
not bash" only matters if user's workflow needs bash. Surface that
explicitly.

If no candidate is a clean fit, say so and skip straight to STEP 7.

---

## ▸ STEP 7 — Hybridize? (always ask)

Always ask. Even when the recommendation is strong, the hybrid path is
where this skill earns its keep.

```
┌─ 🧬 Genetic mixing ───────────────────────────────────────
│ Want a custom hybrid that genetically mixes 2-4 of the
│ above into something tailored to <user workflow>?
│
│ Here is what a hybrid could look like for YOUR case:
│
│   Parents     : #<id> + #<id> [+ #<id>]
│   New intent  : <one sentence — what this hybrid does that
│                 no parent does alone>
│
│   Inherited primitives:
│     • from #<a>: <load-bearing piece — frontmatter/triggers/
│                   step structure/hook wiring/etc.>
│     • from #<b>: <complementary piece>
│     • from #<c>: <polish piece>
│
│   New genes (not in any parent):
│     • <thing genuinely added — e.g. cache layer, gating,
│       project-specific trigger, output format>
│
│   Why this combo > any single parent:
│     <one or two sentences on the additive value>
│
│ Reply with one of:
│   1. "ship it"        — generate the hybrid file now
│   2. "tweak: <notes>" — adjust parents, intent, or genes
│   3. "skip"           — just take the recommendation
└───────────────────────────────────────────────────────────
```

If user says "ship it", invoke STEP 7-build.

### STEP 7-build (on "ship it")

1. **Extract primitives** — for each parent, list its load-bearing pieces
   (frontmatter shape, trigger phrases, step structure, hook wiring, prompt
   scaffolds, output format). Use `scripts/extract-skill.sh <url>` per parent
   to keep it cheap.
2. **Conflict map** — render points of disagreement:

   ```
   ┌─ Conflicts ─────────────────────────────────────────
   │ Trigger style : #1 keyword-list   vs #2 regex      → keep #1
   │ Hook event    : #1 PreToolUse     vs #3 Stop       → keep #3
   │ Output format : #1 markdown table vs #2 jsonl     → keep #1 (user reads)
   └─────────────────────────────────────────────────────
   ```
3. **Selection rationale** — one line per primitive on why the winner won.
4. **New synthesis** — write a draft of the hybrid (skill / hook / agent)
   inline in the same file format the user would commit. Mark borrowed
   lines with `# from #<id>` comments where non-obvious.
5. **Delta callout** — bullet what is genuinely *new*. If nothing is new,
   say so and recommend just using the strongest single parent.

Hybrid count guidance:

| N parents | Pattern |
|-----------|---------|
| 2 | Frame from one, fill from the other. Cleanest. |
| 3 | Frame + scaffold + polish split. Sweet spot. |
| 4-5 | Risk of Frankenstein. Force-rank, drop weakest. |
| 6+ | Don't. Cluster first, hybridize cluster reps. |

Then ask before writing to disk:

```
Save hybrid to ~/.claude/skills/<name>/SKILL.md ? [y/N/path]
```

---

## Helper scripts (in `scripts/`)

| Script              | Purpose                                       |
|---------------------|-----------------------------------------------|
| `survey.sh`         | One-shot fan-out: awesome+gh+reddit, deduped. **Start here.** |
| `awesome.sh`        | awesome.ecosyste.ms list search, TSV out      |
| `gh-search.sh`      | Recent active GH repos by topic+scope, pipe out |
| `gh-quality.sh`     | Per-repo signal: stars, push, issues, archived |
| `reddit.sh`         | Top reddit threads, no-auth, pipe out         |
| `extract-skill.sh`  | Cheap structural digest of a SKILL.md / agent.md |
| `dedupe.sh`         | Dedupe pipe-rows by name, keep highest-stars  |

All scripts emit pipe-delimited rows (or TSV). Token-shaped — feed to
`grep` to filter further; they are already compact, so do not run them
through another summarizing reader.

---

## Output discipline

- Render the seven banners verbatim. Skip none.
- Lead each step with the table/box, prose after.
- Cite every claim with URL or candidate ID.
- Recommend zero candidates if none pass STEP 4 — do not pad.
- STEP 6 justification is non-negotiable. STEP 7 hybrid prompt is
  non-negotiable.
- Web access fails → degrade to `references/canon-sources.md` and say so.

## Anti-patterns

- ✗ Recommending a candidate without fetching its README.
- ✗ Padding to N=5 with low-quality fillers. n=3 strong > n=5 mid.
- ✗ Hybridizing without showing the conflict map.
- ✗ Justifying the pick without justifying the rejections (asymmetric
  reasoning hides bias).
- ✗ Using Claude-in-Chrome for this — WebFetch / firecrawl_search / the
  helper scripts are faster.
- ✗ Writing the hybrid file without the "Save to ...?" confirmation.
