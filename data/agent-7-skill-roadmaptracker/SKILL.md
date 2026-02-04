# Skill: Roadmap Tracker

## Name
**Roadmap Tracker** - Automated 1M€ 18-Month Business KPI Tracking

## Description
This skill automates the tracking and visualization of business metrics for the 18-month journey to 1M€ ARR as defined in `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`. It updates the live dashboard `/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md` with current MRR, customer counts, feature progress, and KPI trends, calculating variance against targets and generating progress visualizations.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Update roadmap tracker"
- "Track business KPIs"
- "Show progress toward 1M€"
- "Update MRR dashboard"
- "Calculate roadmap variance"
- "Generate business metrics report"
- "Track revenue milestones"

### Context Indicators
- User mentions MRR, ARR, revenue, or customers
- User discusses roadmap phases or milestones
- User asks about progress toward business goals
- User wants to update metrics dashboards

## Process Steps

### Phase 1: Gather Current Metrics (5 minutes)

1. **Collect Revenue Metrics**
   Ask user for (or retrieve from CRM/database):
   - **Current MRR (Monthly Recurring Revenue)**: €X,XXX
   - **Current ARR (Annual Recurring Revenue)**: MRR × 12
   - **Total Customers**: XX (Fitnaai SaaS subscribers)
   - **Beta Users**: XX (free trial users)
   - **Churn Rate**: X.X% (monthly customer loss)

2. **Collect Product Metrics**
   - **Features Shipped**: X out of Y planned
   - **WAU (Weekly Active Users)**: XXX
   - **MAU (Monthly Active Users)**: XXX
   - **Feature Adoption Rate**: XX% (users using new features)
   - **NPS Score**: XX (Net Promoter Score)

3. **Collect Content & Marketing Metrics**
   - **YouTube Subscribers**: XXX
   - **Newsletter Subscribers**: XXX
   - **Newsletter Open Rate**: XX%
   - **Blog Traffic**: XXX visitors/month
   - **Social Media Followers**: XXX (LinkedIn, Twitter, etc.)

4. **Collect Consulting & Products Metrics**
   - **Consulting Revenue (Monthly)**: €X,XXX
   - **Course Sales (Monthly)**: €XXX
   - **Content Revenue (Monthly)**: €XXX (sponsorships, affiliates)

### Phase 2: Calculate Target Variance (5 minutes)

5. **Determine Current Phase**
   Reference: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`

   **Phase Timeline:**
   - **Q1 (M1-3)**: Foundation → MVP Launch + 10 Beta (0€ → 1.5K€ MRR)
   - **Q2 (M4-6)**: Validation → PMF + 50 Customers (1.5K€ → 9.5K€ MRR)
   - **Q3 (M7-9)**: Scale → 500 Customers (9.5K€ → 25K€ MRR)
   - **Q4-Q6 (M10-18)**: Acceleration → Dominance (25K€ → 103K€ MRR)

   **Calculate Month Number:**
   ```
   Start Date: [ROADMAP_START_DATE]
   Current Date: [TODAY]
   Month Number: (Current - Start) / 30 days
   Current Phase: [Q1/Q2/Q3/Q4-Q6]
   ```

6. **Calculate MRR Variance**
   ```
   Target MRR (from phase): €X,XXX
   Actual MRR: €Y,YYY
   Variance: €(Y,YYY - X,XXX)
   Variance %: ((Actual - Target) / Target) × 100
   Status: 🟢 On Track (±10%) / 🟡 Behind (-10% to -25%) / 🔴 Critical (>-25%)
   ```

7. **Calculate Customer Variance**
   ```
   Target Customers: XX
   Actual Customers: YY
   Variance: YY - XX
   Variance %: ((Actual - Target) / Target) × 100
   ```

8. **Calculate Revenue Stream Breakdown**
   Reference roadmap revenue model:

   | Stream | Target@M[X] | Actual | Variance | % of Total |
   |--------|-------------|--------|----------|------------|
   | SaaS (Fitnaai) | €X,XXX | €Y,YYY | €Z,ZZZ | XX% |
   | Consulting | €X,XXX | €Y,YYY | €Z,ZZZ | XX% |
   | Content | €XXX | €YYY | €ZZZ | X% |
   | Courses/Products | €X,XXX | €Y,YYY | €Z,ZZZ | XX% |
   | **TOTAL MRR** | €X,XXX | €Y,YYY | €Z,ZZZ | 100% |

### Phase 3: Generate Progress Visualizations (5 minutes)

9. **Create MRR Progress Bar**
   ```markdown
   ## MRR Progress Toward 103K€

   [████████████░░░░░░░░░░░░░░░░░░░░] 40% (€41K / €103K)
   ```

   **Calculation:**
   - Each █ = 3.33% (100% / 30 bars)
   - Bars = (Actual MRR / Target MRR) × 30

10. **Create Customer Acquisition Progress**
    ```markdown
    ## Customer Acquisition Progress

    Phase: Q2 - Validation (Target: 50 customers)
    Current: 32 customers
    [████████████████████░░░░░░░░░░░░] 64% (32/50)

    Remaining: 18 customers
    Days Left in Phase: 45
    Required Rate: 0.4 customers/day
    Current Rate: 0.5 customers/day ✅
    ```

11. **Create Feature Completion Tracker**
    ```markdown
    ## Feature Roadmap Progress

    ### Must-Have Features (M1-3)
    - [x] User authentication & onboarding
    - [x] Workout plan generator (AI-powered)
    - [x] Client progress tracking
    - [x] Basic reporting dashboard
    - [ ] Mobile app MVP (2 weeks delayed)

    Progress: [████████████████░░░░░░░░] 80% (4/5 features)

    ### Nice-to-Have Features (M4-6)
    - [x] Advanced AI workout customization
    - [ ] Nutrition planning integration
    - [ ] WhatsApp/SMS notifications
    - [ ] Video exercise library

    Progress: [█████░░░░░░░░░░░░░░░░░░░░] 25% (1/4 features)
    ```

12. **Create KPI Dashboard**
    ```markdown
    ## Key Performance Indicators (KPIs)

    | KPI | Target | Actual | Status |
    |-----|--------|--------|--------|
    | MRR | €9.5K | €7.2K | 🟡 -24% |
    | Customers | 50 | 32 | 🟡 -36% |
    | Churn Rate | <5% | 3.8% | 🟢 |
    | CAC (Cost per Acquisition) | <€50 | €42 | 🟢 |
    | LTV/CAC Ratio | >3x | 4.2x | 🟢 |
    | WAU/MAU | >40% | 52% | 🟢 |
    | NPS Score | >50 | 58 | 🟢 |
    | Feature Adoption | >60% | 65% | 🟢 |
    ```

### Phase 4: Update Live Dashboard (5 minutes)

13. **Update 1M Roadmap Tracker File**
    Reference: `/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md`

    ```bash
    # Read current tracker
    TRACKER_FILE="/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md"

    # Update with new metrics (use Edit tool)
    # Replace MRR section with calculated values
    # Update progress bars
    # Refresh variance calculations
    # Update last updated timestamp
    ```

14. **Add Trend Analysis**
    ```markdown
    ## Trend Analysis (Last 30 Days)

    ### MRR Growth
    30 days ago: €6.1K
    Today: €7.2K
    Growth: +€1.1K (+18%)
    Monthly Growth Rate: 18%
    **Projection to M6 Target:** €9.5K (reachable if growth sustained)

    ### Customer Acquisition
    30 days ago: 24 customers
    Today: 32 customers
    Net New: +8 customers (+33%)
    Churn: -2 customers
    Gross New: +10 customers
    **Projection:** 50 customers by end of Q2 ✅ On track
    ```

15. **Generate Insights & Recommendations**
    ```markdown
    ## Insights & Recommendations

    ### 🟢 What's Working
    - Feature adoption rate (65%) exceeds target → users love the product
    - Churn rate (3.8%) well below target → strong retention
    - LTV/CAC ratio (4.2x) indicates healthy unit economics

    ### 🟡 Areas to Improve
    - MRR growth (-24% vs target) needs acceleration
      → **Action**: Launch Q2 pricing tier (€79/mo for 20-50 clients)
    - Customer acquisition (-36% vs target) behind pace
      → **Action**: Increase content marketing (2 blogs/week + YouTube shorts)

    ### 🔴 Risks
    - Mobile app MVP delayed by 2 weeks
      → **Impact**: May miss Q2 beta launch window
      → **Mitigation**: Re-scope MVP, focus on core features only
    ```

### Phase 5: Sprint & Weekly Sync (Continuous)

16. **Link to Sprint Progress**
    Reference: `/home/fitna/homelab/sprints/sprint-{NUMBER}/SPRINT_BOARD.md`

    ```markdown
    ## Current Sprint Contribution to Roadmap

    **Sprint 26 Goals:**
    - Landing page → Impacts: Customer acquisition (+10 signups/week projected)
    - Beta launch email → Impacts: Onboarding (10 beta users)
    - Monitoring setup → Impacts: Reliability (reduce downtime to <1%)

    **Sprint Impact on MRR:** +€500 (5 new customers @ €99/mo)
    ```

17. **Weekly Update Cadence**
    - **Every Monday**: Update MRR, customers, churn from CRM
    - **Every Friday**: Update feature progress, KPIs, trend analysis
    - **End of Month**: Full variance analysis, quarterly projections

## Rules and Constraints

### Hard Rules (Must Follow)
1. **Update MRR and customers WEEKLY** (minimum)
2. **Variance MUST be calculated against roadmap targets**
3. **Progress bars MUST be accurate** (don't fake progress)
4. **KPIs MUST use objective data** (no guessing)
5. **Churn rate MUST be tracked monthly** (critical metric)
6. **All revenue streams MUST be broken down** (SaaS, consulting, content, products)

### Soft Rules (Best Practices)
- Update dashboard every Monday morning
- Include trend analysis (30-day, 90-day)
- Document assumptions in projections
- Link roadmap to sprint deliverables
- Celebrate wins (milestones reached)

### Quality Gates
Before finalizing roadmap update:
- [ ] All KPIs populated with current data
- [ ] Variance calculated correctly (Actual - Target)
- [ ] Progress bars match percentages
- [ ] Trend analysis includes 30-day comparison
- [ ] Insights backed by data (not opinions)
- [ ] Recommendations are actionable

## Expected Outputs

### Deliverables
1. **1M Roadmap Tracker (updated)** - Live dashboard with current metrics
2. **Variance Report** - Target vs. actual analysis
3. **Trend Analysis** - 30/90-day growth trends
4. **Insights & Recommendations** - Data-driven action items

### File Structure
```
/home/fitna/homelab/shared/dashboards/
├── 1m-roadmap-tracker.md (updated weekly)
├── monthly-reports/
│   ├── 2025-01-mrr-report.md
│   ├── 2025-02-mrr-report.md
│   └── ...
└── historical/
    ├── 2025-01-snapshot.md
    └── 2025-02-snapshot.md
```

### Success Metrics
- ✅ MRR updated weekly
- ✅ Variance within ±10% (on track)
- ✅ All 8 KPIs tracked and visualized
- ✅ Trends show upward trajectory
- ✅ Recommendations implemented within 2 weeks

## Error Handling

### Common Issues & Solutions

**Issue: Missing MRR data**
- **Solution**: Query CRM/Stripe for subscription revenue
- **Fallback**: Estimate from customer count × average plan price

**Issue: Churn rate unknown**
- **Solution**: Calculate: (Customers Lost / Total Customers) × 100
- **Data Source**: CRM cancellation records

**Issue: Feature progress unclear**
- **Solution**: Review sprint boards and Git commits
- **Metric**: Features marked "Done" / Total planned features

**Issue: Variance too large (>25%)**
- **Action**: Trigger urgent review, adjust roadmap or strategy
- **Escalate**: Discuss with stakeholders, revise targets if needed

**Issue: Progress bars don't match percentages**
- **Solution**: Recalculate: (Actual / Target) × 30 bars
- **Validation**: Percentage = (Number of █ symbols / 30) × 100

## Example Usage

### User Request
"Update the roadmap tracker with current MRR of €7.2K and 32 customers."

### Agent Response
```markdown
I'll update the roadmap tracker with your current metrics.

**Current Phase:** Q2 - Validation (Month 5 of 18)
**Target MRR:** €9.5K
**Actual MRR:** €7.2K
**Variance:** -€2.3K (-24%) 🟡

**MRR Progress Toward 103K€:**
[██████░░░░░░░░░░░░░░░░░░░░░░░░] 7% (€7.2K / €103K)

**Customer Acquisition:**
Target: 50 customers
Actual: 32 customers
Variance: -18 customers (-36%) 🟡

**Revenue Breakdown:**
- SaaS (Fitnaai): €5.8K (81%)
- Consulting: €1.0K (14%)
- Content: €0.3K (4%)
- Courses: €0.1K (1%)

**Trend Analysis (30 days):**
MRR: €6.1K → €7.2K (+€1.1K, +18%) 📈
Customers: 24 → 32 (+8, +33%) 📈
Churn: 3.8% (target: <5%) 🟢

**Recommendations:**
1. Launch €79/mo pricing tier to accelerate MRR growth
2. Increase content output (2 blogs/week) to boost customer acquisition
3. Focus on retention (churn excellent, maintain current quality)

**Status:** 🟡 Behind pace but trending positively. Sustaining 18% monthly growth will reach Q2 target.

**Updated:** `/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md`
```

## Integration Points

### Related Skills
- **Agent 1 - SprintManager**: Link sprint deliverables to roadmap KPIs
- **Agent 4 - DailyProgressReporter**: Weekly velocity feeds into roadmap projections
- **Agent 6 - MonitoringSetup**: Track infrastructure KPIs (uptime, performance)

### External Tools
- CRM/Stripe: Revenue and customer data
- Google Analytics: Traffic and content metrics
- GitHub: Feature completion tracking

### Data Sources
- Roadmap: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`
- Tracker: `/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md`
- Sprint boards: `/home/fitna/homelab/sprints/sprint-{NUMBER}/SPRINT_BOARD.md`

## Version
v1.0 - Initial skill definition based on 1M€ roadmap analysis
