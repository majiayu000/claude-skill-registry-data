---
name: youtube-research
description: >-
  What do practitioners actually DO (not just document)? Methodology for
  extracting practitioner knowledge from YouTube video transcripts. Use when
  (1) researching how people actually use a technology, (2) seeking practitioner
  insights beyond documentation, (3) looking for tips, patterns, or workflows
  from creators, (4) building a research corpus from video content.
---

# YouTube Research

**Seed question:** *What do practitioners actually DO (not just document)?*

Extract structured knowledge from YouTube video transcripts. Videos capture practitioner insights, tips, and patterns that don't appear in formal documentation.

## Phases

### Phase 1: Discovery

**Method A: Web Search**
```
WebSearch: "[topic] tutorial 2025 youtube"
WebSearch: "[topic] best practices youtube"
WebSearch: "[topic] tips advanced youtube"
```

**Method B: Playwright Discovery (Better for Recommendations)**
1. Navigate to YouTube search
2. Search for `[topic] tutorial [year]`
3. Capture video titles and URLs from results
4. Click into a relevant video to get recommendations
5. Capture recommended videos (YouTube's algorithm surfaces related content)

**Method C: Known Creator Channels**
- Official company channels (Anthropic, Google, Microsoft)
- Tech educators (Fireship, NetworkChuck, Traversy Media)
- Conference channels (AI Engineer, React Conf)

### Phase 2: Transcript Acquisition

**Delegates to `video-transcript-extraction` skill.**

For each discovered video:
1. Invoke video-transcript-extraction
2. If transcripts disabled, skip and note in research log
3. Save transcript to working directory

### Phase 3: Pattern Extraction

For each transcript, extract:

**Structural Elements:**
- Concepts defined (new terms, mental models)
- Workflows described (step-by-step processes)
- Anti-patterns mentioned (what NOT to do)
- Tips and tricks (practitioner shortcuts)
- Tools/libraries mentioned (ecosystem components)

**Quality Signals:**
- Confidence markers: "Always do X" vs "I prefer X"
- Source authority: official channel vs creator opinion
- Recency: check video date, concepts may be outdated
- Triangulation: same pattern from 3+ sources = high confidence

### Phase 4: Synthesis

**Cross-Video Analysis:**
1. Group similar concepts across transcripts
2. Identify consensus patterns (3+ sources agree)
3. Flag contradictions for human review
4. Note unique insights from single sources (lower confidence)

**Output Structure:**
```markdown
# [Topic] YouTube Research Analysis

**Date:** YYYY-MM-DD
**Videos Analyzed:** N

## Videos Analyzed
| Video | Creator | Focus | Key Value |

## New Patterns Discovered
## Reinforced Patterns
## Contradictions Found
## Methodology Notes
```

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

**Budget mode:** Skip corpus.json unless user requests. HANDOFF.md and all_content.md always generated.

**Relational memory:** Memorize key findings if relational-memory MCP is configured (skip if not available):
```python
mcp__relational-memory__memorize(
    agent_name="youtube-research",
    layer="recent",
    content="[key finding]",
    metadata={"topic": "...", "videos": N}
)
```

## Detail Levels

Choose detail level BEFORE starting extraction:

| Level | Mode | Per-Video Output | When to Use |
|-------|------|------------------|-------------|
| 0-3 | Quick | 1-2 sentences, topic tags | Triage many videos, initial discovery |
| 4-6 | Balanced | Summary + key points + notable quotes | Standard research, known-good sources |
| 7-10 | Deep | Full extraction, timestamps, cross-references | High-value topics, building corpus |

**Adjusting mid-research:** Start at 4-6 by default. Increase to 7-10 if finding gold. Decrease to 0-3 if hitting diminishing returns.

## Self-Managing Iteration

**This skill is SELF-MANAGING. No user input needed for iteration decisions.**

### Budget-Aware Self-Review (After Each Pass)

```markdown
## SELF-REVIEW - Pass N

### Value Assessment
1. Patterns found this pass: [count]
2. Novel insights (not seen before): [count]
3. Reinforced patterns: [count]

### Budget Check
4. Detail level used: [N]
5. Token investment: HIGH/MEDIUM/LOW
6. Value delivered: HIGH/MEDIUM/LOW
7. Value/Token ratio: GOOD/ACCEPTABLE/POOR

### Decisions
8. Continue? [YES/NO]
9. Adjust detail level? [UP/DOWN/SAME]
```

### Decision Algorithm

```python
def should_continue():
    consecutive_low = count_trailing_lows(pass_history)
    if consecutive_low >= 2:
        return STOP, "Data exhausted"
    if saturation == "YES":
        return STOP, "Saturation confirmed"
    if value_token_ratio == "POOR" and consecutive_low >= 1:
        return STOP, "Diminishing returns"
    return CONTINUE, "Proceed to next pass"
```

### Saturation Detection
- **NO**: New concepts, diverse sources
- **BEGINNING**: Meta-themes repeating, still finding techniques
- **YES**: Multiple videos saying same things, no novel patterns

## Topic-Based Escalation

Consult `reference/topic-based-escalation.md` when extracted content touches:
- Safety/trust claims → suggest DIP
- Power structures / "who benefits" → suggest cui-bono
- Geopolitical/military → suggest DIP + cui-bono lenses
- Contrarian single-source → suggest dialectic-spiral (full) + iterative-verification

Mid-research escalation is a suggestion, not automatic. Note it and let the user decide.

## Budget Mode

**Activation (any of these):**
1. Explicit flag: `--budget` or `-b`
2. Auto-detect: If `budget-mode` skill is active in session
3. Inherited: If invoked from research hub in budget mode

**When active:**
- Detail levels 3-5 instead of default 4-6
- Cap dialectic at 2 rounds if escalating
- corpus.json is OPT-IN (ask user, default: no)
- Relational-memory memorize still happens (cheap, always valuable)

**Note:** After context compaction, auto-detection may fail. Re-invoke `budget-mode` skill or pass `--budget` explicitly.

**Propagation:** When invoking other skills, pass budget:
"Invoking video-transcript-extraction --budget"

## Tips

1. **Timestamps matter:** Note timestamps for verification of specific claims
2. **Creator bias:** Sponsored content may promote specific tools
3. **Recency decay:** Tech videos older than 18 months may have outdated info
4. **Comment gold:** Video comments sometimes have better tips than the video (not accessible via transcript)
5. **Playlist structure:** Tutorial series may build concepts progressively

## Limitations

- Cannot access videos with disabled transcripts (fallback to Whisper via video-transcript-extraction)
- Auto-generated transcripts may have errors
- Cannot see visual demonstrations (code on screen, diagrams)
- Comments and community notes not accessible
- Live streams may have transcript issues

## Cross-References

- **video-transcript-extraction** — called for Phase 2 (transcript acquisition)
- **deep-investigation-protocol** — escalation target for trust/safety topics
- **cui-bono** — escalation target for power analysis topics
- **cui-bono + financial-mcp** — escalation target when financial dimension needed (a dedicated **stonk** agent is in design — issue #61)
- **dialectic-spiral** — used when findings need stress-testing
- **reference/topic-based-escalation.md** — shared escalation logic

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
