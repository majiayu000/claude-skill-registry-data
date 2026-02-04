---
name: strategic-search
description: Solve complex multi-constraint problems through systematic web search using multiple engines with adaptive strategies.
---

# Strategic Search

You solve complex, multi-constraint problems by systematically researching and combining multiple clues. You have access to a search MCP server that provides DuckDuckGo, Brave, and Serper engines.

- **Core approach**: Extract all constraints, rank them by uniqueness and searchability, research progressively, and validate candidates until finding the answer that satisfies ALL conditions.
- **Engine strategy**: DuckDuckGo (free) is the default; use Brave/Serper (paid) when DuckDuckGo results are insufficient or for cross-validation.

---

## CRITICAL: Search Budget Management

**You have a maximum of 30 searches. Track your count explicitly at every step.**

**Format:** `[Search X/30]` before EVERY query.

**Phase budgets (recommended):**
- Phase 1 (Extract & Rank): 0 searches (analysis only)
- Phase 2 (Initial Search & Validation): 8-15 searches
- Phase 3 (Cross-Validation): 3-5 searches
- Phase 4 (Revision if needed): 5-10 searches

**Early termination triggers:**
- ✅ **STOP immediately** when you find a candidate that satisfies ALL constraints
- ✅ **STOP at search 20** if you have a strong candidate (satisfies 80%+ constraints)
- ✅ **STOP at search 25** regardless, finalize your best answer
- ✅ **STOP at search 30** hard limit - return best candidate with explanation

---

## Core Workflow: Constraint-Based Search

**Example problem:** "Identify the fictional character who breaks the fourth wall, has a backstory with ascetics, is known for humor, and had a TV show in the 1960s-1980s with fewer than 50 episodes."

### Phase 1: Extract and Rank Constraints (0 searches)

#### 1.1. Extract all constraints

List every condition explicitly:

**Example:**

1. Fictional character
2. Breaks the fourth wall
3. Has a backstory with ascetics
4. Known for humor
5. Had a TV show in the 1960s-1980s
6. TV show had fewer than 50 episodes

#### 1.2. Rank by uniqueness and searchability

**Ranking strategy:**

- **Most unique/specific** → Highest priority (narrows search space dramatically)
- **Verifiable numerical constraints** → High priority (precise validation)
- **Common traits** → Lower priority (too broad initially)

**Example (high → low):**

1. **"ascetics backstory"** - Most distinctive characteristic
2. **"fewer than 50 episodes"** - Specific, verifiable number
3. **"TV show 1960s-1980s"** - Narrows time period significantly
4. **"breaks fourth wall"** - Distinctive but more common in comedy
5. **"known for humor"** - Very broad; many shows fit this
6. **"fictional character"** - Universal; not useful for initial search

**Rationale:** Start with the constraint that eliminates the most candidates. "Ascetics" is unusual enough to point toward specific genres (Eastern spirituality, martial arts, mythology), making it the ideal starting point.

---

### Phase 2: Progressive Search and Validation (Target: 8-15 searches)

Start with the **highest-ranked constraint**, generate candidate answers, then progressively filter using remaining constraints until finding the final answer.

#### 2.1. Initial Search (2-3 searches)

**Query construction:**

- Combine the top 1-3 most distinctive constraints
- Use synonyms to broaden coverage
- Keep queries concise but specific

**Example:**

```
[Search 1/30]
Query: "TV show 1970s 1980s monks ascetics humor"
Goal: Find shows with Eastern spiritual themes
Expected: Kung Fu, Monkey, martial arts shows
```

#### 2.2. Candidate Validation (5-12 searches)

**Key principle: Validate ONE candidate at a time, STOP as soon as ALL constraints are satisfied.**

For each candidate, verify constraints in order of ease/speed:

**Example - Candidate "Kung Fu":**

```
[Search 2/30]
Query: "Kung Fu TV series 1972 episode count"
Result: 63 episodes
✗ REJECTED immediately - Fails episode constraint (<50)
→ Move to next candidate
```

**Example - Candidate "Monkey":**

```
[Search 3/30]
Query: "Monkey TV show 1978 episode count"
Result: 52 episodes (Japanese), 39 episodes (English dub)
✓ Episode constraint satisfied (39 < 50)
→ Continue validation

[Search 4/30]
Query: "Monkey TV show 1978 fourth wall breaks audience"
Result: Confirms character addresses the camera directly
✓ Fourth wall constraint satisfied
→ Continue validation

[Search 5/30]
Query: "Monkey TV show Buddhist monk Tripitaka ascetics"
Result: Confirms journey with Buddhist monk, spiritual themes
✓ Ascetics constraint satisfied

Validation checklist:
✓ Fictional character (Sun Wukong/Monkey King)
✓ Breaks the fourth wall (speaks directly to camera)
✓ Ascetics backstory (travels with Tripitaka, Buddhist monk)
✓ Known for humor (comedic, mischievous character)
✓ TV show 1978-1980 (within 1960s-1980s range)
✓ <50 episodes (39 episodes in English version)

→ ALL CONSTRAINTS SATISFIED - STOP SEARCHING
→ Final answer: Monkey (TV series, 1978-1980)
```

**Total searches used: 5/30** ✅

---

### Phase 3: Cross-Validation (Optional, 3-5 searches)

**Only use if:**
- You found a candidate but have doubts
- Multiple viable candidates exist
- Critical decision requires high confidence

If you have a strong candidate that satisfies all constraints, **skip this phase**.

**Example:**

```
[Search 6/30]
Query: "Monkey 1978 TV series episode count IMDb"
→ Confirms: 52 episodes total, 39 English dub

[Search 7/30]
Query: "Monkey TV show 1978 fourth wall Wikipedia"
→ Confirms fourth wall breaking in multiple sources
```

---

### Phase 4: Revision Strategy (5-10 searches, only if needed)

**Trigger revision ONLY if:**
- After 15 searches, no viable candidates satisfy >50% of constraints
- All candidates fail critical constraints
- Search results consistently off-target

**If you reach search 15 without a good candidate, PAUSE and revise:**

**Revision strategy:**

- **Re-examine constraints**
	
	- Are you interpreting "ascetics" too narrowly?
    - Could "fourth wall" mean something different?
    - Is the time period flexible (late 60s, early 80s)?
    
- **Re-rank constraints**
    
    - Perhaps start with "fourth wall + <50 episodes" instead
    - Try different constraint combinations
     
- **Switch search engines**
	
	- Use Brave/Serper (paid)
	- Different engines index content differently 
	
- **Adjust search parameters**
	
	- Increase `max_results` in `search` MCP tool (default: 10 → try 15-20)
	- More results = higher chance of finding obscure matches

**Hard stops:**
- **Search 20**: If you have a candidate satisfying 80%+ constraints, finalize it
- **Search 25**: Finalize your best candidate regardless
- **Search 30**: ABSOLUTE LIMIT - return best candidate with explanation

---

## Complete Worked Example: Full Search Sequence

**Problem:** "What TV show from the 1970s-1980s featured a character who breaks the fourth wall, has a backstory involving ascetics, is comedic, and had fewer than 50 episodes?"

### Phase 1: Analysis (0 searches)

```
Constraints extracted:
1. TV show 1970s-1980s
2. Character breaks fourth wall
3. Backstory with ascetics
4. Comedic/humorous
5. <50 episodes

Ranking (most unique first):
1. Ascetics backstory (MOST DISTINCTIVE)
2. <50 episodes (VERIFIABLE)
3. 1970s-1980s (NARROWS TIME)
4. Breaks fourth wall (DISTINCTIVE)
5. Comedic (COMMON)

Strategy: Search "ascetics + 1970s TV" first
```

### Phase 2: Search & Validate

```
[Search 1/30]
Query: "TV show 1970s 1980s monks ascetics comedy"
Engine: DuckDuckGo
Results: "Kung Fu", "Monkey", "The Water Margin"
→ 3 candidates identified

[Search 2/30]
Query: "Kung Fu TV series episode count"
Result: 63 episodes
✗ Fails <50 constraint → REJECT

[Search 3/30]
Query: "Monkey TV show 1978 episode count"
Result: 52 episodes (Japanese), 39 (English dub)
✓ Passes <50 constraint (39 episodes)
→ Promising candidate

[Search 4/30]
Query: "Monkey TV show 1978 breaks fourth wall"
Result: "Monkey frequently addresses the camera and audience directly"
✓ Passes fourth wall constraint

[Search 5/30]
Query: "Monkey TV show Tripitaka Buddhist monk"
Result: "Journey to the West adaptation, Tripitaka is a Buddhist monk"
✓ Passes ascetics constraint

Quick checklist:
✓ 1970s-1980s (1978-1980)
✓ Breaks fourth wall (confirmed)
✓ Ascetics backstory (Buddhist monk companion)
✓ Comedic (described as comedic throughout)
✓ <50 episodes (39 English episodes)

→ ALL CONSTRAINTS SATISFIED
→ ANSWER: "Monkey" (1978-1980 TV series)
→ STOP SEARCHING

Total searches: 5/30 ✅
```

**Key success factors:**
- Started with most distinctive constraint (ascetics)
- Rejected failed candidates immediately (Kung Fu at search 2)
- Validated incrementally, stopped as soon as all constraints met
- Did NOT continue searching after finding valid answer

---

## Search Optimization Techniques

### Technique 1: Synonym Expansion

```
"breaks fourth wall" → "talks to audience", "addresses camera", "narrator character"
"ascetics" → "monks", "hermits", "spiritual teachers", "Buddhist", "Shaolin"
"humor" → "comedy", "comedic", "funny", "satirical"
```

### Technique 2: Query Chaining

Build subsequent queries from previous results.

```
[Search 1/30]: "TV 1970s spiritual comedy" → Identifies: Show X, Show Y, Show Z
[Search 2/30]: "Show X episode count" → Verify constraint
[Search 3/30]: "Show X fourth wall breaking" → Verify constraint
[Search 4/30]: "Show X monks ascetics backstory" → Verify constraint
```

### Technique 3: Constraint Combination

```
Combine multiple constraints:
"TV 1970s fourth wall <50 episodes comedy monks"
→ May directly hit the answer if the search engine indexes well
```

### Technique 4: Rapid Elimination

```
If a candidate FAILS any hard constraint (numbers, dates), REJECT immediately.
Don't waste searches validating other constraints.

Example:
[Search N/30]: "Show X episode count" → 75 episodes
✗ Fails <50 → STOP, move to next candidate
→ DON'T search for fourth wall, ascetics, etc.
```

---

## MCP Tool Interfaces

| Tool                                                 | Function                             | Return                                              |
| ---------------------------------------------------- | ------------------------------------ | --------------------------------------------------- |
| `get_engine_status()`                                | Check availability of search engines | DuckDuckGo: O\|X<br>Brave: O\|X<br>Serper: O\|X<br> |
| `search(query, max_results=10, engine="duckduckgo")` | Run search query on selected engines | List of {rank, title, content, url}                 |

---

## Search Engines

**Engine selection strategy:**

- **DuckDuckGo (free)**: Default for all searches
- **Brave / Serper (paid)**: Use when:
  - DuckDuckGo returns <5 relevant results
  - Cross-validation needed for confidence
  - After 10 searches with no strong candidates

**Budget management:**

- Maximum 30 total queries per problem
- Track count explicitly: `[Search X/30]`
- Stop immediately when answer is validated
- At search 20: finalize if you have 80%+ match
- At search 25: finalize best candidate
- At search 30: hard stop

---

## Anti-Patterns: What NOT to Do

**DON'T:** Continue searching after finding a valid answer
```
[Search 8/30]: Found "Monkey" - satisfies all constraints
[Search 9/30]: "Let me verify one more time..."  ← WASTEFUL
```

**DO:** Stop immediately when all constraints are met
```
[Search 8/30]: Found "Monkey" - satisfies all constraints
→ ANSWER: "Monkey" ✓
```

---

**DON'T:** Validate all constraints on failed candidates
```
[Search 5/30]: "Show X episode count" → 100 episodes (fails <50)
[Search 6/30]: "Show X fourth wall" ← WASTEFUL, already failed
[Search 7/30]: "Show X ascetics" ← WASTEFUL, already failed
```

**DO:** Reject immediately on hard constraint failures
```
[Search 5/30]: "Show X episode count" → 100 episodes
✗ REJECTED - move to next candidate
```

---

**DON'T:** Forget to track search count
```
Query: "TV show monks"
Query: "another search"
Query: "yet another"
... (loses count, exceeds budget)
```

**DO:** Track explicitly every time
```
[Search 1/30]: "TV show monks"
[Search 2/30]: "another search"
[Search 3/30]: "yet another"
```
