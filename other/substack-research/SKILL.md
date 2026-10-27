---
name: substack-research
description: >-
  What are the independent voices actually saying? Extract and analyze long-form
  content from Substack publications. Use when (1) researching independent
  journalist perspectives, (2) analyzing a specific Substack publication,
  (3) building a research corpus from long-form written content,
  (4) cross-referencing Substack analysis with other sources.
---

# Substack Research

**Seed question:** *What are the independent voices actually saying?*

Extract and analyze long-form content from Substack publications. Substacks capture independent journalist analysis, expert commentary, and long-form reasoning that mainstream outlets often compress or omit.

## First-Time Setup

```
IF auth/browser_state.json does NOT exist:

  1. Run: python -m scripts.auth_capture https://yoursubstack.substack.com
  2. Browser opens — log in manually (handles 2FA, CAPTCHA)
  3. IMPORTANT: After login, navigate to ANY OTHER PAGE in the Substack
     (click an article, the homepage, anything)
     → This signals the script to close the browser and save credentials
  4. Credentials cached in auth/browser_state.json (one-time only)
     The auth/ directory is created automatically during first login.

  The "navigate to another page" step is REQUIRED — the script waits for
  a navigation event to know login is complete.
```

**Tooling location:** `tools/substack-scraper/` (relative to plugin root)

## Quick Start

Use the `/substack-extract` command for the full pipeline:
```bash
/substack-extract --url https://example.substack.com --detail 5
```

## Phases

### Phase 1: Setup and Configuration

1. Locate scraper: the plugin includes it at `${CLAUDE_PLUGIN_ROOT}/tools/substack-scraper/`
2. Install dependencies: `pip install -r ${CLAUDE_PLUGIN_ROOT}/tools/substack-scraper/requirements.txt && playwright install chromium`
3. Check `auth/browser_state.json` — if missing, guide first-time setup
4. Configure target Substack URL (copy `config.example.json` to `config.json` and edit, or use `--url` flag)

### Phase 2: Discovery and Extraction

```bash
cd ${CLAUDE_PLUGIN_ROOT}/tools/substack-scraper
python main.py
```

This extracts articles to `data/` directory. Output: `all_articles.md` + individual article files.

### Phase 3: Parsing with Detail Levels

```bash
python scripts/parse_content.py data/ --detail N --prompt "Focus on [topic]"
```

**Detail levels:**

| Level | Mode | Output | When to Use |
|-------|------|--------|-------------|
| 0-3 | Quick | Theme clusters, topic tags | Triage large corpus, initial discovery |
| 4-6 | Balanced | Summaries + key arguments + notable quotes | Standard research |
| 7-10 | Deep | Full analysis, cross-references, argument mapping | High-value publications |

**Adaptive adjustment for bulk corpora:**

| Corpus Size | Max Effective Detail | Mode |
|-------------|---------------------|------|
| 100+ articles | 2 | Theme clustering |
| 50-100 articles | 3 | Theme clustering |
| 20-50 articles | 5 | Standard |
| < 20 articles | Requested | Standard |

### Phase 4: Pattern Analysis and Synthesis

**Per-author analysis:**
- Core arguments and thesis evolution over time
- Recurring themes and intellectual frameworks
- Sources cited (trace upstream influences)
- Blind spots (what topics does this author avoid?)

**Cross-author analysis (multiple Substacks):**
- Where do independent voices converge? (genuine consensus or echo chamber?)
- Where do they diverge? (genuine disagreement or different evidence bases?)
- What do they all omit? (structural blind spot detection)

### Phase 5: Export

**Normal mode:**
```
output/
  HANDOFF.md          — Summary + suggested next actions
  corpus.json         — Machine-readable (auto-generated)
  all_content.md      — Consolidated markdown
  analysis/
    overview.md
    patterns.md
    themes.md
```

**Budget mode:** Skip corpus.json unless user requests.

**Relational memory:** Memorize key findings if relational-memory MCP is configured (skip if not available):
```python
mcp__relational-memory__memorize(
    agent_name="substack-research",
    layer="recent",
    content="[key finding]",
    metadata={"substack": "...", "articles": N}
)
```

## Self-Managing Iteration

Same saturation detection as youtube-research (see youtube-research SKILL.md "Decision Algorithm" section for full implementation):

- Track new patterns vs reinforced patterns per pass
- Stop after 2+ consecutive LOW passes (< 2 total: new + reinforced patterns)
- Adjust detail level dynamically: up if finding gold, down if diminishing returns

## Topic-Based Escalation

Consult `reference/topic-based-escalation.md` when extracted content touches:
- Safety/trust claims → suggest DIP
- Power structures / "who benefits" → suggest cui-bono
- Geopolitical/military → suggest DIP + cui-bono lenses
- Contrarian single-source claims → suggest dialectic-spiral (full) + iterative-verification

Substack content is often contrarian by nature (independent journalists). Apply extra scrutiny via dialectic-spiral when a single Substack is the sole source for a claim.

## Budget Mode

**Activation (any of these):**
1. Explicit flag: `--budget` or `-b`
2. Auto-detect: If `budget-mode` skill is active in session
3. Inherited: If invoked from research hub in budget mode

**When active:**
- Detail levels 0-3 instead of default 4-6
- Cap dialectic at 2 rounds if escalating
- corpus.json is OPT-IN (ask user, default: no)
- Relational-memory memorize still happens

**Note:** After context compaction, auto-detection may fail. Re-invoke `budget-mode` skill or pass `--budget` explicitly.

**Propagation:** When invoking other skills, pass budget:
"Invoking dialectic-spiral --budget"

## Tips

1. **Author credibility:** Check author's credentials, track record, funding sources
2. **Paywall content:** Auth capture handles paid subscriptions if user has access
3. **Publication vs author:** Some Substacks are multi-author — track per-author, not just per-publication
4. **Time dimension:** Sort by date to see how author's position evolved (especially valuable for geopolitical topics)
5. **Cross-corpus value:** Substack + YouTube + mainstream creates triangulation — each source type has different blind spots

## Limitations

- Requires Python + browser for first-time auth
- Paywall content only accessible if user has subscription
- DOM changes in Substack may break extraction (check for selector updates)
- Large corpora (100+ articles) need adaptive detail to prevent token waste

## Cross-References

- **video-transcript-extraction** — for complementary video sources
- **youtube-research** — for practitioner perspective on same topics
- **deep-investigation-protocol** — escalation target for trust/safety topics
- **cui-bono** — escalation target for power analysis topics
- **cui-bono + financial-mcp** — escalation target when financial dimension needed (a dedicated **stonk** agent is in design — issue #61)
- **dialectic-spiral** — stress-testing findings from single-source Substacks
- **reference/topic-based-escalation.md** — shared escalation logic

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
