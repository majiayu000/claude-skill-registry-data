---
name: exit
description: Exit engine for ID8Labs. Position for and execute successful exits through strategic preparation, valuation optimization, and deal execution.
version: 1.0.0
mcps: [Perplexity, GitHub]
subagents: [strategic-think-tank]
skills: []
---

# ID8EXIT - Exit Engine

## Purpose

Position your product for a successful exit. Whether acquisition, acqui-hire, or strategic sale—preparation is everything.

**Philosophy:** Exits are not events, they're outcomes. Build acquirable from day one. The best exits happen when you're not desperate.

---

## When to Use

- User is considering exit options
- User receives acquisition interest
- User wants to maximize company value
- User needs help with due diligence preparation
- User asks "how do I sell my company?"
- Project is in OPERATING state and mature

---

## Commands

### `/exit <project-slug>`

Run full exit readiness assessment.

**Process:**
1. ASSESS - Evaluate current exit-readiness
2. POSITION - Optimize for acquirer interest
3. VALUE - Understand worth and multiples
4. PREPARE - Build data room and materials
5. NEGOTIATE - Structure optimal deal
6. EXECUTE - Close the transaction

### `/exit assess`

Evaluate exit readiness and identify gaps.

### `/exit value`

Estimate valuation range and comparable exits.

### `/exit dataroom`

Create due diligence documentation checklist.

### `/exit memo`

Draft internal exit strategy memo.

---

## Exit Philosophy

### Solo Builder Exit Reality

| Exit Type | Realistic For | Typical Range |
|-----------|---------------|---------------|
| Acqui-hire | Any stage | $50K-500K |
| Asset sale | With users/revenue | $50K-1M |
| Strategic acquisition | PMF + growth | $500K-10M |
| Financial acquisition | Scale | $5M+ |

### Exit Timing

**Too early signals:**
- No product-market fit
- No sustainable revenue
- Still figuring out the model
- Desperate for cash

**Right time signals:**
- Clear PMF demonstrated
- Sustainable growth
- You want to exit
- Strategic interest exists

**Warning signs to exit:**
- Losing interest/energy
- Market shrinking
- Better opportunities elsewhere
- Burnout incoming

---

## Process Detail

### Phase 1: ASSESS

**Exit readiness scorecard:**

| Factor | Score (1-5) | Notes |
|--------|-------------|-------|
| Product-Market Fit | | Evidence of PMF |
| Revenue/Growth | | MRR, growth rate |
| User Base | | Size, engagement |
| Technology | | Clean, documented |
| Team | | Dependencies |
| Legal | | Clean cap table, IP |
| Operations | | Systematized |
| Market Position | | Competitive moat |

**Scoring:**
- 35-40: Ready for premium exit
- 25-34: Ready with some gaps
- 15-24: Significant prep needed
- <15: Not ready

### Phase 2: POSITION

**Positioning for acquirers:**

| Acquirer Type | What They Want | How to Position |
|---------------|----------------|-----------------|
| Strategic (competitor) | Market share, customers | User base, retention |
| Strategic (adjacent) | New capability | Technology, team |
| Financial (PE/VC) | Returns | Growth, margins |
| Individual buyer | Lifestyle business | Cash flow, low effort |

**Positioning activities:**
- Clean up technical debt
- Document everything
- Show growth trajectory
- Highlight strategic value
- Build relationships early

### Phase 3: VALUE

**Valuation methods:**

| Method | Formula | Best For |
|--------|---------|----------|
| Revenue multiple | ARR × Multiple | SaaS with growth |
| Profit multiple | EBITDA × Multiple | Profitable businesses |
| User-based | Users × Value/User | Pre-revenue, engaged users |
| Asset value | Assets - Liabilities | Distressed/no growth |
| Comparable | What similar sold for | Market validation |

**SaaS multiples (solo builder scale):**

| Growth Rate | Typical Multiple |
|-------------|------------------|
| <10% YoY | 2-3x ARR |
| 10-30% YoY | 3-5x ARR |
| 30-50% YoY | 5-8x ARR |
| >50% YoY | 8-12x ARR |

**Adjustments:**
- +1-2x for strong retention (>90% NRR)
- +1-2x for strategic fit
- -1-2x for high churn
- -1-2x for concentration risk

### Phase 4: PREPARE

**Data room essentials:**

| Category | Documents |
|----------|-----------|
| **Corporate** | Formation docs, cap table, contracts |
| **Financial** | P&L, balance sheet, projections |
| **Product** | Tech docs, architecture, roadmap |
| **Customers** | Metrics, top accounts, churn analysis |
| **Team** | Org chart, key person dependencies |
| **Legal** | IP assignments, material agreements |

**Preparation timeline:**

| Timeframe | Actions |
|-----------|---------|
| 12 months out | Clean up financials, document processes |
| 6 months out | Build data room, fix legal issues |
| 3 months out | Prepare materials, identify buyers |
| 1 month out | Finalize data room, practice pitch |

### Phase 5: NEGOTIATE

**Deal structure components:**

| Component | Description | Typical Range |
|-----------|-------------|---------------|
| Cash at close | Immediate payment | 50-80% |
| Earnout | Performance-based | 10-30% |
| Equity | Stock in acquirer | 0-20% |
| Escrow | Held for indemnity | 10-20% |
| Employment | Retention package | Varies |

**Negotiation priorities:**
1. Total consideration (valuation)
2. Cash vs equity split
3. Earnout terms and achievability
4. Escrow terms and release
5. Employment terms
6. Reps and warranties scope

### Phase 6: EXECUTE

**Closing process:**

```
LOI SIGNED
    ↓
Due diligence (30-60 days)
    ↓
Definitive agreement negotiation
    ↓
Final document execution
    ↓
Closing conditions satisfied
    ↓
CLOSE
```

**Post-close:**
- Transition assistance
- Earnout execution
- Team integration
- Customer communication

---

## Framework References

### Exit Options
`frameworks/exit-options.md` - Types of exits and fit

### Valuation
`frameworks/valuation.md` - Methods and multiples

### Due Diligence
`frameworks/due-diligence.md` - What buyers want

### Deal Structure
`frameworks/deal-structure.md` - Terms and negotiation

### Acquisition Prep
`frameworks/acquisition-prep.md` - 12-month prep plan

---

## Output Templates

### Data Room Checklist
`templates/data-room-checklist.md` - Due diligence documents

### Exit Memo
`templates/exit-memo.md` - Internal exit strategy

### Term Sheet Review
`templates/term-sheet-review.md` - Analyzing offers

---

## Tool Integration

### MCPs

**Perplexity:**
- Research comparable exits
- Find potential acquirers
- Market research

**GitHub:**
- Clean up repository
- Document codebase
- Prepare for technical DD

### Subagents

**strategic-think-tank:**
- Exit strategy analysis
- Negotiation strategy
- Deal structure optimization

---

## Handoff

After completing exit preparation:

1. **Save outputs:**
   - Exit memo → `docs/EXIT_MEMO.md`
   - Data room → `docs/data-room/`

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "EXIT: Preparation complete. Valuation range: ${X}-${Y}. Ready for market."
   ```

3. **Update state:**
   ```
   /tracker update {project-slug} EXITING
   ```

4. **On successful exit:**
   ```
   /tracker update {project-slug} EXITED
   ```

---

## Exit Readiness Quick Check

### Minimum Requirements

- [ ] 12+ months of financial records
- [ ] Clean cap table
- [ ] IP properly assigned
- [ ] No legal issues
- [ ] Customer contracts in order
- [ ] Key metrics documented
- [ ] Code is documented and clean
- [ ] Team dependencies identified

### Red Flags for Buyers

| Red Flag | Impact | Fix |
|----------|--------|-----|
| Messy cap table | Deal complexity | Clean up early |
| No financial records | Trust issues | Start tracking now |
| Single customer >50% | Risk | Diversify |
| Key person dependency | Risk | Document, cross-train |
| IP not assigned | Deal blocker | Fix immediately |
| Material litigation | Deal killer | Resolve before |

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Waiting until desperate | Weak negotiating position | Plan 12+ months ahead |
| Hiding problems | Will surface in DD | Disclose upfront |
| Only one buyer | No leverage | Create competition |
| Focusing only on price | Miss bad terms | Evaluate full package |
| No advisor | Make mistakes | Get help on first exit |
| Neglecting business during sale | Value erodes | Keep running hard |

---

## Quality Checks

Before starting exit process:

- [ ] Exit readiness score >25
- [ ] Financial records clean and current
- [ ] Legal issues resolved
- [ ] Data room 80%+ complete
- [ ] Valuation expectations realistic
- [ ] Exit timeline defined
- [ ] Key decisions documented
