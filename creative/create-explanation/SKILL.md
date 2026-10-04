---
name: create-explanation
description: Generate scholarly bilingual (English + Traditional Chinese) explanations for classical Chinese verses. Use when explaining Yilin, I Ching, or Tang poetry lines.
user-invocable: true
argument-hint: "[paste your verse here]"
metadata:
  version: "1.0.0"
---

# Create Verse Explanation

Generate scholarly bilingual explanations for classical Chinese oracular verses. These explanations make abstract ancient poetry accessible by explaining historical allusions and connecting imagery to meaning.

## Your Task

Given a classical Chinese verse, produce:
1. An **English explanation** (100-150 words)
2. A **Traditional Chinese explanation** (150-200 characters)
3. A **references** list of historical figures, places, or allusions used

## Critical Requirements

### Research Before Writing

**For ANY historical reference:**
1. Verify the reference before explaining — do not hallucinate historical facts
2. Common references needing verification:
   - Figures: 大禹 (Da Yu), 蚩尤 (Chiyou), 彭祖 (Pengzu), 夏桀 (Xia Jie), etc.
   - Places: 龍門 (Dragon Gate), 夏臺 (Xia Terrace), 羑里 (Youli), etc.
   - Allusions: Classical idioms, historical events, mythological references

## Writing Guidelines

### English Explanation (100-150 words)

**Structure:**
1. **Open with the literal scene** (1-2 sentences)
   - What's happening in the verse visually/narratively?
   - Ground the reader in the imagery before explaining

2. **Explain historical allusions** (2-3 sentences)
   - Clarify references with brief context
   - Keep scholarly but accessible — no academic jargon

3. **Connect to transformation meaning** (1-2 sentences)
   - What quality of change does the verse capture?

**Tone:**
- Scholarly but conversational
- Explain without talking down
- Active voice preferred
- Avoid: "This verse is about...", "The poem describes..."
- Prefer: Direct description → explanation → insight

**Example opening patterns:**
- "Great Yu inspects the roads while Chiyou clears the way ahead..."
- "The verse depicts a parched horse climbing a mountain..."
- NOT "This verse is about Great Yu and Chiyou working together..."
- NOT "The poet uses the image of drought to symbolize..."

### Traditional Chinese Explanation (150-200 chars)

**Structure:**
1. 場景描述 (1 sentence)
2. 典故解釋 (1-2 sentences)
3. 變化意涵 (1 sentence)

**Tone:**
- 文白相間 (literary but accessible)
- 不說教，點到為止

## Output Format

Present the result conversationally:

**English**
Great Yu inspects the roads while Chiyou clears the way ahead, covering ten thousand miles without danger...

**繁體中文**
大禹巡視道路，蚩尤開闢通途，行遍萬里不遇危險...

**References:** 大禹, 蚩尤

---

## Example: Strong Explanation

**Verse:** 大禹式路，蚩尤除道。周匝萬里，不危不殆，見其所使，無所不在。

**English (138 words):**
Great Yu inspects the roads while Chiyou clears the way ahead, covering ten thousand miles without danger. Yu, the legendary flood-tamer who founded the Xia dynasty, represents methodical governance; Chiyou, the mythical warrior deity, embodies raw martial force. Together they symbolize the pairing of strategy and execution — authority that both plans and acts. The verse connects to the transformation from Creative (乾) pure yang to Splitting Apart (剝): as yang lines erode from below, power must expand its reach to compensate for shrinking foundation. "Seeing their agents everywhere" suggests surveillance born of weakness, not strength. The journey is safe not because of dominance but because authority has learned to delegate, to work through envoys rather than direct force.

**繁體中文 (198 chars):**
大禹巡視道路，蚩尤開闢通途，行遍萬里不遇危險。大禹為治水聖王，建夏朝；蚩尤為戰神，象徵武力。二者合象謀略與執行之配——既謀劃又行動的權威。詩呼應乾卦純陽至剝卦剝蝕之變：陽爻自下而蝕，權力須擴展觸角以補基礎之削弱。「見其所使，無所不在」暗示監視源於虛弱而非強大。旅途安全非因壓制，乃因權威學會委派，藉使者而非直接施力。

**References:** 大禹, 蚩尤

## Quality Checks

Before finalizing output:
- [ ] All historical references verified (not hallucinated)
- [ ] EN explanation 100-150 words
- [ ] ZH explanation 150-200 chars
- [ ] All references listed
- [ ] Tone is scholarly but accessible
- [ ] Explanations connect imagery to verse meaning
- [ ] Both EN and ZH stand alone — not literal translations of each other
