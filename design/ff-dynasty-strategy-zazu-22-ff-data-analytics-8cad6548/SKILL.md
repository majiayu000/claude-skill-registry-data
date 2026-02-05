---
name: ff-dynasty-strategy
description: Expert guidance on dynasty fantasy football strategies, player valuation frameworks, roster construction, trade evaluation, and asset management. Use this skill when analyzing dynasty trades, evaluating player value, designing roster strategies, assessing competitive windows, or answering fantasy football domain questions. Covers VoR/VBD methodologies, aging curves, market inefficiencies, draft pick valuation, and win-now vs rebuild strategies.
---

# Dynasty Fantasy Football Strategy

## Overview

Provide expert guidance on dynasty fantasy football strategy, player valuation, roster construction, and trade analysis using research-backed frameworks and methodologies. Apply domain expertise to help evaluate trades, identify market inefficiencies, construct competitive rosters, and make data-driven dynasty management decisions.

## When to Use This Skill

Trigger this skill for queries involving:

- **Player valuation questions**: "How should I value this player?" "What's a fair trade value?" "Is this player overvalued?"
- **Trade analysis**: "Should I accept this trade?" "How do I evaluate this trade offer?" "What's a win-win trade structure?"
- **Roster construction**: "Should I rebuild or compete?" "How do I identify my competitive window?" "What's optimal positional allocation?"
- **Draft strategy**: "What's this draft pick worth?" "Should I trade picks or players?" "When should I target RBs vs WRs?"
- **Aging curves & timing**: "When should I sell this RB?" "Is this WR past his prime?" "What's the optimal exit point?"
- **Market analysis**: "Is this player a buy-low candidate?" "What are common market inefficiencies?" "How do I identify mispriced assets?"
- **Asset management**: "How do I value future picks?" "What's the quantity premium in consolidation trades?" "Should I cut this player or hold for dead cap reasons?"

**Note:** For questions involving statistical modeling, machine learning, or simulation design, consider also using the `ff-ml-modeling` or `ff-statistical-methods` skills.

## Core Capabilities

### 1. Player Valuation Frameworks

Apply research-backed valuation methodologies to assess player worth:

**Value over Replacement (VoR)**

- Calculate VoR using formula: `Player Projected Points - Replacement Level Points`
- Set replacement baselines using worst starter method, man-games approach, or draft position method
- Enable cross-positional comparisons by standardizing value relative to position-specific baselines

**Value-Based Drafting (VBD)**

- Prioritize players with highest VoR regardless of position
- Identify steep "drop off" positions to target early
- Exploit positions with gentle declines by deferring to later rounds

**Sustainable vs Fluky Performance**

- Identify touchdown regression candidates using xTD and TDOE metrics
- Emphasize volume-based metrics (target share, opportunity share, snap count, WOPR)
- Distinguish sustainable opportunity-driven production from TD-luck-driven scoring

**Market Inefficiencies**

- Spot injury overreactions creating buying opportunities
- Recognize offseason pretty roster syndrome (youth overvaluation)
- Identify recency bias in player valuations
- Find gaps between model projections and market consensus (KTC, DynastyProcess)

**Prospect Profiling**

- Apply Dominator Rating thresholds (30%+ = elite, 20-30% = good, <20% = concern)
- Evaluate breakout age (RB <20, WR <21, TE <23)
- Incorporate NFL draft capital as signal for opportunity

**Reference:** `references/valuation_frameworks.md` for detailed formulas, thresholds, and examples.

### 2. Roster Construction Strategies

Guide roster-building decisions based on competitive timeline:

**Win-Now Strategy**

- Prioritize proven producers over unproven rookies
- Target consistent production with track records
- Hold draft picks to add youth and maintain roster rejuvenation
- Mix in younger players for long-term viability

**Rebuild Strategy**

- Accumulate draft picks across multiple classes (picks are lifeblood)
- Focus on 2-3 foundational pieces (QB core, elite WRs under 26)
- Avoid RBs during rebuild (shelf life doesn't align with 2-3 year window)
- Build through WRs for longer careers and stable value trajectories

**Competitive Window Analysis**

- Identify typical 2-3 year competitive windows
- Time RB acquisitions to align with competitive window opening
- Balance present opportunity vs future flexibility
- Reassess window every 4-6 weeks during season

**Positional Allocation**

- QB: Secure higher-level QB early (Superflex = most valuable position)
- RB: "Get in early, exit before decline" - sell after Year 4
- WR: Patient with rookies, best foundation for dynasty rosters
- TE: Expect sophomore breakouts (98.5% PPR increase Year 2)

**Reference:** `references/roster_construction.md` for win-now vs rebuild tactics, roster depth guidelines, and draft philosophies.

### 3. Trade Evaluation & Optimization

Systematically evaluate dynasty trades using multi-objective framework:

**Multi-Objective Analysis**
Assess trades across 5 dimensions:

1. **Current Year Value**: Impact on starting lineup for this season
2. **Future Value**: Outlook 1-3 years from now
3. **Competitive Window Alignment**: Does trade match timeline (contending/rebuilding)?
4. **Positional Scarcity**: Trading for/away from scarce positions (elite TEs, every-down RBs)?
5. **Market Timing**: Buying low or selling high based on value trends?

**Win-Win Trade Structures**

- Identify complementary needs (target teams weak where you're strong)
- Use even swap strategy (2-for-2 trades benefit both sides)
- Account for team timelines (rebuilders trade RBs for WRs; contenders do opposite)
- Apply quantity premium (30-50% overpay when consolidating to elite assets)

**Draft Pick Valuation**

- First round picks: ~45% hit rate, highest value pre-NFL Draft
- Second round picks: 22% hit rate, 69% miss rate
- Third round+: <15% hit rate ("dart throws")
- Future picks: Discount to 80% of current year equivalent
- NFL draft capital matters: High picks indicate opportunity and team faith

**Manager Profiling**

- Assess risk tolerance (safety vs upside chasers)
- Identify position preferences and roster construction philosophies
- Find managers unaware of their competitive window (arbitrage opportunities)
- Distinguish active traders (receptive to creative structures) vs passive builders

**Reference:** `references/trade_evaluation.md` for crowdsourced valuation tools (KTC, DynastyProcess), quantity premiums, and trade evaluation framework.

**Asset:** `assets/trade_evaluation_template.md` - Systematic template for evaluating trades across all dimensions.

### 4. Aging Curves & Timing

Apply position-specific aging patterns to buy/sell decisions:

**Running Backs**

- Career arc: 88% baseline rookie year, decline below baseline Year 7, spread dramatically Year 8
- Optimal exit: After Year 4 (before Year 7 decline)
- Shortest shelf-life; sell while value is highest

**Wide Receivers**

- Career arc: 74% baseline rookie year, peak Year 5, maintain into late 20s
- Be patient Years 2-3 for sophomore surge
- Hold value longer, age more gracefully than RBs

**Tight Ends**

- Career arc: 33% baseline rookie year, 94% baseline Year 2 (98.5% PPR increase)
- Don't give up on rookie TEs; expect Year 2 jump
- Maintain through Year 7, don't decline significantly until age 30

**Quarterbacks**

- Career arc: Efficiency rises age 25+, peak ages 28-33, many produce into mid-to-late 30s
- Most stable position for aging
- Safe to roster older QBs for win-now pushes (especially Superflex)

**Mortality Table Framework (Harstad)**

- Alternative view: Players don't gradually decline; they maintain or "fall off a cliff"
- Focus on survival probability rather than gradual erosion
- 50/50 shot at 100% production vs 0% (not 50% of typical production)

**Reference:** `references/aging_curves.md` for detailed career arcs, exit strategies, and age-adjusted valuation framework.

## Workflow for Trade Analysis

Follow this process when evaluating dynasty trades:

**Step 1: Gather Trade Details**

- List all assets exchanged (players, picks)
- Identify trade partner's competitive timeline (contending/rebuilding)
- Confirm your own timeline

**Step 2: Calculate Raw Value**

- Use KTC, DynastyProcess, or other consensus tools for baseline values
- Sum total value given vs received
- Apply quantity premium (30-50%) if consolidating or breaking apart assets

**Step 3: Multi-Objective Assessment**

- Current year impact: Does this improve starting lineup this season?
- Future value: How does this affect 1-3 year outlook?
- Window alignment: Does trade match my timeline?
- Positional scarcity: Am I addressing gaps or creating new ones?
- Market timing: Am I buying low / selling high?

**Step 4: Aging Curve Analysis**

- Check career year and age for all key assets
- Identify cliff risks (RBs Year 5+, WRs 30+, TEs 30+)
- Reference `aging_curves.md` for position-specific benchmarks

**Step 5: Sustainability Check**

- For key assets received, check for TD regression risk (xTD vs actual TDs)
- Verify volume indicators: target/carry share, snap %, opportunity share
- Prioritize opportunity-driven performance over TD-luck

**Step 6: Win-Win Verification**

- Does this trade help trade partner along their dimensions?
- Is this mutually beneficial given different timelines/needs?
- If not win-win, revise or prepare counter-offer

**Step 7: Make Decision**

- Accept: Strong trade improving roster along key dimensions
- Counter: Close but needs adjustment
- Decline: Does not align with strategy/timeline/value

**Tool:** Use `assets/trade_evaluation_template.md` to systematically document this analysis.

## Workflow for Roster Construction Planning

Follow this process when building or reshaping rosters:

**Step 1: Determine Timeline**

- Assess current roster age, draft capital, competitive position
- Decide: Win-now, retool, or rebuild?

**Step 2: Execute Mode-Specific Tactics**

- **Win-now:** Proven producers + draft picks for youth influx
- **Rebuild:** Accumulate picks + foundational WRs + avoid RBs
- **Retool:** Mix of young WRs + one elite QB/TE to anchor

**Step 3: Positional Allocation**

- Superflex: Prioritize QB depth
- All formats: Build WR depth as portfolio foundation
- Time RB acquisitions to competitive window
- Be patient with TE breakouts (expect Year 2 surge)

**Step 4: Continuous Evaluation**

- Reassess competitive window every 4-6 weeks
- Adjust tactics as roster ages or improves
- Balance present opportunity vs future flexibility

## Identifying Data Requirements

When analyzing dynasty questions, identify what data is needed:

**For Player Valuation:**

- Projected points by player/position
- Historical performance (3+ years for aging curves)
- Opportunity metrics (target share, snap %, carry share)
- Expected vs actual touchdowns (xTD, TDOE)
- Market values (KTC, DynastyProcess)

**For Trade Analysis:**

- Current roster composition (yours and partner's)
- Starting lineup requirements
- Projected points for current season + future years
- Player ages and career years
- Draft pick holdings

**For Roster Construction:**

- Full roster with ages and positions
- Competitive standings
- Draft capital (current and future picks)
- Positional depth charts
- Franchise transaction history

**For Aging Analysis:**

- Player age and NFL experience years
- Position-specific benchmarks
- Career usage (touches, targets)
- Historical performance trends

## Integrating with Other Skills

**Complement with `ff-ml-modeling` when:**

- Building predictive models for player projections
- Feature engineering for valuation models
- Clustering players into tiers
- Training regression models for value estimation

**Complement with `ff-statistical-methods` when:**

- Running Monte Carlo simulations for trade scenarios
- Performing variance analysis for regression-to-mean
- Applying GAMs for non-linear aging curves
- Conducting hypothesis tests on performance trends

**Parallel Execution:** When requests touch multiple domains (e.g., "Build a player valuation model using VoR and regression analysis"), invoke relevant skills in parallel for comprehensive guidance.

## Best Practices

**Emphasize Volume over Touchdowns**

- "Volume is king in fantasy football"
- Target share, snap %, opportunity share are leading indicators
- TDs regress: +TDOE declines 86%, -TDOE improves 93%

**Apply Timeline Discipline**

- Don't hold aging RBs while rebuilding
- Don't hold distant picks while contending
- Align every move with competitive window

**Understand Market Dynamics**

- Buy during injury overreactions
- Sell during offseason hype (pretty roster syndrome)
- Exploit recency bias
- Find model vs market gaps

**Use Multi-Objective Framework**

- Best trades are win-win along different dimensions
- Contender gets win-now assets, rebuilder gets future value
- Avoid zero-sum thinking; find complementary needs

**Respect Aging Curves**

- RBs: Exit Year 4, before Year 7 cliff
- WRs: Patient through Years 2-3, hold through late 20s
- TEs: Don't give up Year 1, expect Year 2 breakout
- QBs: Safe into mid-30s, premium in Superflex

**Avoid Common Pitfalls**

- Overvaluing unproven rookies during win-now
- Drafting RBs early during multi-year rebuild
- Ignoring quantity premium in consolidation trades
- Chasing touchdowns instead of opportunity
- Making lopsided offers that aren't mutually beneficial

## References

All detailed research-backed frameworks are available in:

- `references/valuation_frameworks.md` - VoR, VBD, sustainable performance, market inefficiencies, prospect profiling
- `references/roster_construction.md` - Win-now vs rebuild, competitive windows, positional allocation, draft philosophies
- `references/trade_evaluation.md` - Crowdsourced tools, win-win structures, multi-objective optimization, draft pick valuation
- `references/aging_curves.md` - Position-specific career arcs, exit strategies, mortality tables, age-adjusted valuations

## Assets

- `assets/trade_evaluation_template.md` - Systematic template for documenting and analyzing dynasty trades across all evaluation dimensions
