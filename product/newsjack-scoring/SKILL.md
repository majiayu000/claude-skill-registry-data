---
name: newsjack-scoring
description: Use this when the user mentions breaking news, newsjacking, or reactive PR. Scores stories (tech, music industry, platform updates, AI announcements) across 4 signals (Relevance, Urgency, Viral Potential, First-Mover Advantage) and generates reactive commentary within 30 minutes. Powered by newsjack.cc product.
---

# NewsJack — Reactive PR & Story Scoring

Powered by **newsjack.cc**. Evaluates breaking stories, industry shifts, and trending news in under 60 seconds, determining whether to post and crafting the optimal reactive angle.

## The 4-Signal Scoring Framework

Evaluate any breaking story on a 0-100 scale:

**Formula**: `(0.35 × Relevance) + (0.25 × Urgency) + (0.25 × Viral Potential) + (0.15 × First Mover)`

- **Score > 60**: High signal. Drop everything and post within 30 minutes.
- **Score 40–60**: Medium signal. Schedule a considered take today.
- **Score < 40**: Low signal. Ignore (noise).

## The 4 Signals Explained

### 1. Relevance (35%)

Does this sit inside your audience's core interest graph? (Genre, tools, platform policies, regulatory shifts).

**Quick test**: Would your reader open this story without your commentary? If yes, find a unique bridge angle. If no, you are the bridge.

### 2. Urgency (25%)

- **Critical (0–2h)**: Breaking platform changes, major label exits, viral controversies
- **High (2–24h)**: Industry reports, product launches, tool updates
- **Medium (2–7 days)**: Feature trends, market analysis

### 3. Viral Potential (25%)

Does the story have concrete numbers, a counter-intuitive finding, or a 1-line shareable takeaway?

### 4. First-Mover Advantage (15%)

Are other accounts already covering it? If top search results on X are > 4 hours old, the first-mover window is closing.

## Reactive Post Output Templates

When a story scores > 60, produce 3 reactive post options:

1. **The Bridge Angle**: Connects the breaking story directly to your product thesis or audience pain point
2. **The Counter-Narrative**: Challenges the popular takeaway with a practitioner's perspective
3. **The Data-First Takearound**: Highlights the specific numbers or policy clause others missed

## Example

**Breaking story**: Spotify announces new editorial playlist submission rules (verified artists only).

**Score**:
- Relevance: 85 (direct impact on indie artists)
- Urgency: 70 (2-hour window before music Twitter saturates)
- Viral Potential: 60 (clear policy change with numbers)
- First-Mover: 50 (some early posts, but no practitioner takes yet)

**Final Score**: `(0.35 × 85) + (0.25 × 70) + (0.25 × 60) + (0.15 × 50) = 69.75` → **POST NOW**

**Reactive angle (Bridge)**: "Spotify's new editorial submission rules (verified artists only) just locked out 80% of independent artists. Here's the workaround: [specific tactic]."

## Related

- newsjack.cc: the product this skill powers (not Total Audio Promo)
- commodity-gate: check reactive posts pass opinion/primitive/voice gates before publishing
