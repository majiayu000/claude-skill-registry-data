---
name: decision-support
description: Structured decision-making frameworks for better choices
version: 1.0.0
---

# Decision Support Framework

_Structured analysis for better decisions_

## 🎯 Purpose

Help users make better decisions using proven frameworks:
- Multi-Criteria Decision Analysis (MCDA)
- Cost-Benefit Analysis
- Decision Trees
- Risk Assessment
- Scenario Planning
- SWOT Analysis

## 🧠 Frameworks

### 1. Multi-Criteria Decision Analysis (MCDA)

**When to Use:** Multiple options, multiple criteria

**Process:**
```
1. List all options
2. Define criteria (what matters)
3. Assign weights (importance 1-10)
4. Score each option per criterion (1-5)
5. Calculate weighted scores
6. Recommend highest score
```

**Example:**
```
Decision: Which job to accept?

Criteria (Weights):
- Salary (25%)
- Growth (25%)
- Work-Life (20%)
- Team (15%)
- Location (15%)

Options: Job A, Job B, Current

Result: Job A scores 4.2/5 ⭐
```

### 2. Cost-Benefit Analysis

**When to Use:** Evaluate if something is worth it

**Process:**
```
1. List all costs (one-time + recurring)
2. List all benefits (tangible + intangible)
3. Assign monetary values where possible
4. Calculate NPV (Net Present Value)
5. Calculate ROI
6. Recommend if benefits > costs
```

### 3. Decision Tree

**When to Use:** Sequential decisions with uncertainty

**Process:**
```
1. Map out decision points
2. Identify possible outcomes
3. Assign probabilities
4. Calculate expected values
5. Choose path with highest EV
```

### 4. Risk Assessment Matrix

**When to Use:** Evaluate and prioritize risks

**Process:**
```
1. List all risks
2. Assess probability (1-5)
3. Assess impact (1-5)
4. Calculate risk score (P × I)
5. Prioritize by score
6. Define mitigation strategies
```

**Matrix:**
```
     Impact →
     1  2  3  4  5
P 1 [G  G  G  G  M]
r 2 [G  G  G  M  H]
o 3 [G  G  M  H  H]
b 4 [G  M  H  H  E]
a 5 [M  H  H  E  E]
b  ↓
i
l
i
t
y
→

G=Green (Low) M=Medium H=High E=Extreme
```

### 5. Scenario Planning

**When to Use:** Uncertain future, multiple possibilities

**Process:**
```
1. Identify key uncertainties
2. Define 3-4 scenarios
   - Best case
   - Worst case
   - Most likely
   - Wild card
3. Analyze implications of each
4. Identify no-regret moves
5. Prepare contingency plans
```

### 6. SWOT Analysis

**When to Use:** Strategic planning

**Process:**
```
Strengths  | Weaknesses
-----------|-----------
Opportunities | Threats

Analyze each quadrant
Identify strategic actions
```

## 💬 Response Template

```markdown
## 🤔 Decision Analysis

**Decision:** [What needs to be decided]

**Framework Used:** [MCDA / Cost-Benefit / Decision Tree / etc.]

### Options Considered
1. **Option A** - [Brief description]
2. **Option B** - [Brief description]
3. **Option C** - [Brief description]

### Analysis

**Criteria & Weights:**
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| [X] | 25% | ★★★★☆ | ★★★☆☆ | ★★★★★ |
| [Y] | 25% | ... | ... | ... |

**Scores:**
- Option A: X.X/5
- Option B: X.X/5
- Option C: X.X/5

### Recommendation

**I recommend:** Option X

**Reasoning:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

### Risks & Concerns
- ⚠️ [Risk 1] - [Mitigation]
- ⚠️ [Risk 2] - [Mitigation]

### Confidence Level
**Confidence:** XX%

**Why:** [Explanation of confidence level]

### Next Steps
- [ ] Your decision
- [ ] I'll execute
- [ ] Need more analysis?

**Questions?**
```

## 📋 Usage Examples

### Example 1: Job Decision
```
User: "Should I accept this job offer?"

AI: [Uses MCDA framework]
- Analyzes: Salary, growth, work-life, team, location
- Scores each option
- Recommends with reasoning
```

### Example 2: Build vs Buy
```
User: "Should we build this tool or buy existing?"

AI: [Uses Cost-Benefit Analysis]
- Lists all costs (dev time, maintenance, opportunity cost)
- Lists all benefits (customization, ownership, speed)
- Calculates 3-year TCO
- Recommends based on numbers
```

### Example 3: Risk Assessment
```
User: "What are the risks of launching this feature?"

AI: [Uses Risk Matrix]
- Lists all risks
- Scores probability & impact
- Prioritizes top 5
- Suggests mitigations
```

## 🎯 Success Metrics

✅ User makes better decisions  
✅ Analysis is structured & clear  
✅ All options fairly considered  
✅ Risks clearly identified  
✅ Recommendation is actionable  
✅ User feels confident in choice  

---

**Status:** Active  
**Version:** 1.0.0  
**Last Updated:** 2026-04-10
