---
name: Experiment Design
description: Comprehensive guide to A/B testing, multivariate testing, statistical significance, and experiment analysis for data-driven product decisions
---

# Experiment Design

## Types of Experiments

### 1. A/B Test (Two Variants)

**What:** Compare two versions (A vs B)

**Example:**
- **Control (A):** Blue "Buy Now" button
- **Treatment (B):** Green "Buy Now" button

**When to Use:**
- Testing single change
- Clear hypothesis
- Binary decision (ship or don't ship)

**Pros:**
- Simple to implement
- Easy to analyze
- Clear winner

**Cons:**
- Only tests one change
- Can't test interactions

### 2. Multivariate Test (Multiple Changes)

**What:** Test multiple changes simultaneously

**Example:**
- **Variable 1:** Button color (Blue, Green, Red)
- **Variable 2:** Button text ("Buy Now", "Add to Cart", "Get Started")
- **Variants:** 3 × 3 = 9 combinations

**When to Use:**
- Testing multiple elements
- Want to find best combination
- Have enough traffic

**Pros:**
- Test interactions between variables
- Find optimal combination

**Cons:**
- Requires much more traffic
- Complex analysis
- Longer test duration

### 3. Sequential Testing

**What:** Continuously monitor and stop early if clear winner

**Example:**
- Start A/B test
- Check results daily
- Stop when statistical significance reached (could be day 3 or day 14)

**When to Use:**
- Want to ship winners fast
- High traffic
- Using tools that support it (Statsig, GrowthBook)

**Pros:**
- Faster results
- Less opportunity cost

**Cons:**
- Requires special statistical methods
- Can't "peek" with traditional A/B tests

### 4. Holdout Groups (Long-Term Effects)

**What:** Keep small % of users on old experience permanently

**Example:**
- **95% of users:** New feature
- **5% of users:** Old experience (holdout)

**When to Use:**
- Measure long-term effects
- Detect delayed negative impacts
- Validate cumulative changes

**Pros:**
- Detects long-term issues
- Measures true impact

**Cons:**
- Some users get worse experience
- Requires ongoing monitoring

---

## When to Experiment

### ✅ Experiment When:

1. **Significant Features (High Impact)**
   - Major redesign
   - New pricing model
   - Core flow changes

2. **Uncertain Outcomes**
   - Don't know if it will work
   - Conflicting opinions
   - No clear data

3. **Multiple Solution Options**
   - Two different approaches
   - Want to pick the best

4. **Optimization Opportunities**
   - Incremental improvements
   - Conversion optimization
   - Engagement optimization

### ❌ Don't Experiment When:

1. **Obvious Bugs/Fixes**
   - Broken functionality
   - Security issues
   - Legal compliance

2. **Very Low Traffic**
   - Can't reach statistical significance
   - Would take months

3. **Trivial Changes**
   - Copy typo fix
   - Minor styling adjustment

4. **Ethical Issues**
   - Manipulative dark patterns
   - Harmful to users

---

## Experiment Design Process

### Step 1: Define Hypothesis

**Template:**
> "If we [change], then [metric] will [improve by X%], because [reasoning]."

**Example:**
> "If we change the CTA button from blue to green, then click-through rate will increase by 10%, because green is more attention-grabbing."

### Step 2: Choose Metrics

**Primary Metric:** What you're optimizing
- Example: Click-through rate

**Secondary Metrics:** Other important outcomes
- Example: Conversion rate, revenue per user

**Counter Metrics:** Watch for negatives
- Example: Bounce rate, time on page

### Step 3: Determine Sample Size

**Inputs:**
- Baseline conversion rate: 5%
- Expected improvement: 10% relative lift (5% → 5.5%)
- Significance level: 0.05 (95% confidence)
- Power: 0.80 (80% chance of detecting effect)

**Output:**
- Sample size needed: ~31,000 users per variant

**Tools:**
- Evan Miller's calculator: https://www.evanmiller.org/ab-testing/sample-size.html
- Optimizely sample size calculator

### Step 4: Set Test Duration

**Factors:**
- Sample size needed
- Daily traffic
- Weekly patterns (run at least 1-2 weeks)
- Business cycles

**Example:**
- Sample size: 31,000 per variant (62,000 total)
- Daily traffic: 5,000
- Duration: 62,000 / 5,000 = 12.4 days → **Run for 2 weeks**

### Step 5: Design Variants

**Control (A):** Current experience
**Treatment (B):** New experience

**Best Practices:**
- Change only one thing (for A/B test)
- Make change meaningful (not trivial)
- Ensure variants are distinct

### Step 6: Launch Test

**Checklist:**
- [ ] Hypothesis documented
- [ ] Metrics instrumented
- [ ] Sample size calculated
- [ ] Randomization working
- [ ] QA tested both variants
- [ ] Monitoring dashboard ready

### Step 7: Analyze Results

**Check:**
- Statistical significance (p < 0.05)
- Practical significance (is improvement meaningful?)
- Secondary metrics (any red flags?)
- Segment analysis (works for everyone?)

### Step 8: Decide (Ship, Iterate, Kill)

**Ship if:**
- Positive, significant, no red flags

**Iterate if:**
- Mixed results, some segments good

**Kill if:**
- Negative, not significant, opportunity cost too high

---

## Choosing Metrics

### Primary Metric (What We're Optimizing)

**Characteristics:**
- Directly tied to hypothesis
- Sensitive to change
- Measurable in test duration

**Examples:**
- Click-through rate (CTR)
- Conversion rate
- Sign-up completion rate
- Time to first action

**Bad Primary Metrics:**
- Revenue (too noisy, delayed)
- Retention (takes too long to measure)
- NPS (survey-based, low sample)

### Secondary Metrics (Guardrails, Side Effects)

**Purpose:** Ensure we're not breaking other things

**Examples:**
- Revenue per user
- Engagement (sessions per user)
- Feature adoption
- Customer satisfaction

### Counter Metrics (Watch for Negatives)

**Purpose:** Detect unintended negative consequences

**Examples:**
- Bounce rate (users leaving immediately)
- Error rate (technical issues)
- Support tickets (confusion)
- Churn rate (users leaving)

### Example: Checkout Flow Test

**Hypothesis:**
> "If we reduce checkout from 5 steps to 3 steps, conversion will increase by 15%."

**Metrics:**
- **Primary:** Checkout conversion rate
- **Secondary:** Average order value, time to complete checkout
- **Counter:** Cart abandonment rate, error rate, support tickets

---

## Statistical Significance

### P-Value < 0.05 (95% Confidence)

**What it Means:**
- Less than 5% chance result is due to random chance
- 95% confident the effect is real

**Example:**
- Control: 5.0% conversion
- Treatment: 5.5% conversion
- P-value: 0.03 ✅ (< 0.05, statistically significant)

**Interpretation:**
> "We're 95% confident that the treatment is better than control."

### Statistical Power (80%+)

**What it Means:**
- 80% chance of detecting an effect if it exists
- Reduces false negatives

**Example:**
- Power: 80%
- Means: 20% chance of missing a real effect

### Minimum Detectable Effect (MDE)

**What it Means:**
- Smallest effect size you can reliably detect
- Depends on sample size

**Example:**
- Baseline: 5% conversion
- Sample size: 10,000 per variant
- MDE: 0.5% absolute (10% relative)
- Can detect: 5.0% → 5.5% or larger

**Trade-off:**
- Larger sample size → Smaller MDE (detect smaller effects)
- Smaller sample size → Larger MDE (only detect big effects)

---

## Sample Size Calculation

### Formula (Simplified)

```
n = (Z_α/2 + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₁ - p₂)²

Where:
- n = sample size per variant
- Z_α/2 = 1.96 (for 95% confidence)
- Z_β = 0.84 (for 80% power)
- p₁ = baseline conversion rate
- p₂ = expected conversion rate
```

### Example Calculation

**Inputs:**
- Baseline conversion rate (p₁): 5% = 0.05
- Expected improvement: 10% relative lift
- New conversion rate (p₂): 5.5% = 0.055
- Significance level (α): 0.05
- Power (1-β): 0.80

**Calculation:**
```
n = (1.96 + 0.84)² × (0.05×0.95 + 0.055×0.945) / (0.05 - 0.055)²
n = 7.84 × (0.0475 + 0.052) / 0.000025
n = 7.84 × 0.0995 / 0.000025
n ≈ 31,200 per variant
```

**Total sample size:** 62,400 users

### Using Online Calculators

**Evan Miller's Calculator:**
1. Go to https://www.evanmiller.org/ab-testing/sample-size.html
2. Enter baseline conversion rate: 5%
3. Enter minimum detectable effect: 10% (relative)
4. Get sample size: ~31,000 per variant

**Optimizely Calculator:**
1. Go to Optimizely sample size calculator
2. Enter baseline: 5%
3. Enter minimum detectable effect: 0.5% (absolute)
4. Get sample size: ~31,000 per variant

---

## Test Duration

### Minimum Duration: 1-2 Weeks

**Why:**
- Capture weekly patterns (weekday vs weekend)
- Avoid day-of-week bias
- Account for user behavior cycles

**Example:**
- Don't run Monday-Wednesday only
- Run at least Monday-Sunday (1 full week)

### Full Business Cycles

**Examples:**
- **E-commerce:** Include payday (1st and 15th of month)
- **B2B SaaS:** Include full week (avoid Friday-only)
- **Seasonal:** Avoid holidays (unless testing holiday-specific)

### Enough Data for Significance

**Formula:**
```
Duration = Sample Size Needed / Daily Traffic
```

**Example:**
- Sample size: 62,000 total
- Daily traffic: 5,000
- Duration: 62,000 / 5,000 = 12.4 days
- **Run for:** 2 weeks (14 days)

### Not Too Long (Opportunity Cost)

**Trade-off:**
- Longer test = More confidence
- Longer test = Delayed learnings, slower iteration

**Guideline:**
- Most tests: 1-4 weeks
- High-traffic sites: 1-2 weeks
- Low-traffic sites: 2-4 weeks
- Don't run > 1 month (diminishing returns)

---

## Experiment Variants

### Control (Current Experience)

**What:** The existing experience

**Example:**
- Current checkout flow (5 steps)
- Current button color (blue)
- Current pricing page

**Purpose:** Baseline for comparison

### Treatment (New Experience)

**What:** The proposed change

**Example:**
- New checkout flow (3 steps)
- New button color (green)
- New pricing page

**Purpose:** Test hypothesis

### Multiple Treatments (If Testing Different Approaches)

**Example:**
- **Control:** 5-step checkout
- **Treatment A:** 3-step checkout (combine steps)
- **Treatment B:** 1-page checkout (all on one page)

**Traffic Split:**
- Control: 33%
- Treatment A: 33%
- Treatment B: 34%

**Analysis:**
- Compare each treatment to control
- Compare treatments to each other

---

## Randomization

### User-Level Randomization (Consistent Experience)

**What:** Each user always sees same variant

**How:**
```javascript
const variant = hashUserId(userId) % 2 === 0 ? 'control' : 'treatment';
```

**When to Use:**
- Logged-in users
- Want consistent experience
- Testing flows (multi-step)

**Pros:**
- Consistent experience
- No confusion

**Cons:**
- Requires user ID

### Session-Level (For Anonymous Users)

**What:** Each session sees same variant (but different sessions can differ)

**How:**
```javascript
const variant = hashSessionId(sessionId) % 2 === 0 ? 'control' : 'treatment';
```

**When to Use:**
- Anonymous users
- Single-page tests

**Pros:**
- Works for anonymous users

**Cons:**
- Same user can see different variants across sessions

### Stratified Sampling (For Segments)

**What:** Ensure even distribution across segments

**Example:**
- Segment 1: Free users (50% control, 50% treatment)
- Segment 2: Paid users (50% control, 50% treatment)

**Why:**
- Avoid imbalanced segments
- Enable segment analysis

---

## Common Pitfalls

### 1. Peeking (Stopping Test Early When "Winning")

**Problem:**
```
Day 3: Treatment is winning! (p = 0.04) → Ship it!
Day 7: Treatment is losing... (p = 0.12) → Oops.
```

**Why It's Bad:**
- Increases false positive rate
- P-value fluctuates during test

**Solution:**
- Decide sample size upfront
- Don't look until test completes
- Or use sequential testing (proper method)

### 2. Sample Ratio Mismatch (Uneven Splits)

**Problem:**
```
Expected: 50% control, 50% treatment
Actual: 48% control, 52% treatment
```

**Why It's Bad:**
- Indicates randomization bug
- Results may be invalid

**Solution:**
- Check sample ratio before analyzing
- Investigate if mismatch > 1%

### 3. Novelty Effect (Users Trying New Thing)

**Problem:**
```
Week 1: Treatment is winning! (+20%)
Week 4: Treatment is same as control (0%)
```

**Why It's Bad:**
- Users try new thing out of curiosity
- Effect fades over time

**Solution:**
- Run test longer (2-4 weeks)
- Use holdout group for long-term measurement
- Segment by new vs returning users

### 4. Seasonality (Testing During Holidays)

**Problem:**
```
Test during Black Friday: +50% conversion
Test during normal week: +5% conversion
```

**Why It's Bad:**
- Holiday behavior is different
- Results don't generalize

**Solution:**
- Avoid testing during holidays
- Or run test across multiple weeks (include holiday + normal)

---

## Sequential Testing

### What is Sequential Testing?

**Traditional A/B Test:**
- Decide sample size upfront
- Run until sample size reached
- Analyze once at end

**Sequential Testing:**
- Monitor continuously
- Stop early if clear winner
- Adjust significance threshold

### How It Works

**Algorithm:**
- Use adjusted significance threshold (not 0.05)
- Account for multiple looks
- Stop when threshold crossed

**Example (Simplified):**
```
Day 1: p = 0.10 → Continue
Day 3: p = 0.03 → Continue
Day 5: p = 0.001 → Stop! (clear winner)
```

### Tools That Support Sequential Testing

- **Statsig:** Built-in sequential testing
- **GrowthBook:** Bayesian statistics
- **Optimizely:** Stats Engine (sequential)

### Benefits

- Faster results (stop early if clear winner)
- Less opportunity cost
- Detect large effects quickly

### Drawbacks

- Requires special tools
- Can't use traditional p-value
- More complex

---

## Holdout Groups

### What is a Holdout Group?

**Definition:** Small % of users kept on old experience permanently

**Example:**
- 95% of users: New feature
- 5% of users: Old experience (holdout)

### Why Use Holdout Groups?

**Measure Long-Term Effects:**
- A/B test shows +10% conversion in 2 weeks
- Holdout shows +5% conversion after 6 months
- **Learning:** Effect diminishes over time

**Detect Delayed Negative Impacts:**
- A/B test shows +15% signups
- Holdout shows +10% churn after 3 months
- **Learning:** Feature attracts wrong users

### How Long to Keep Holdout?

**Guideline:**
- 1-3 months for most features
- 6-12 months for major changes
- Permanent for critical features

### When to Remove Holdout?

**Remove if:**
- No long-term differences detected
- Opportunity cost too high (5% of users on worse experience)
- Feature is critical (everyone should have it)

---

## Experiment Analysis

### Step 1: Compare Primary Metric

**Example:**
- Control: 5.0% conversion
- Treatment: 5.5% conversion
- Lift: +10% relative
- P-value: 0.03 ✅

**Decision:** Treatment is statistically significantly better.

### Step 2: Check Secondary Metrics

**Example:**
- Revenue per user: $10.50 (control) vs $11.20 (treatment) ✅
- Time to checkout: 3.2 min (control) vs 2.8 min (treatment) ✅

**Decision:** Secondary metrics also improved.

### Step 3: Check Counter Metrics

**Example:**
- Bounce rate: 30% (control) vs 32% (treatment) ⚠️
- Error rate: 0.5% (control) vs 0.5% (treatment) ✅

**Decision:** Slight increase in bounce rate, investigate.

### Step 4: Segment Analysis

**Did it work for everyone?**

| Segment | Control | Treatment | Lift |
|---------|---------|-----------|------|
| Mobile | 4.5% | 5.2% | +15% ✅ |
| Desktop | 5.5% | 5.8% | +5% ✅ |
| Free users | 3.0% | 3.6% | +20% ✅ |
| Paid users | 7.0% | 7.1% | +1% ⚠️ |

**Learning:** Works great for mobile and free users, minimal impact on paid users.

### Step 5: Statistical Significance

**Check:**
- P-value < 0.05 ✅
- Confidence interval doesn't include 0 ✅

**Example:**
- Lift: +10%
- 95% CI: [+5%, +15%]
- Interpretation: We're 95% confident the true lift is between 5% and 15%.

### Step 6: Practical Significance

**Is the improvement meaningful?**

**Example:**
- Statistically significant: Yes (p = 0.04)
- Lift: +0.1% (5.0% → 5.005%)
- **Decision:** Not practically significant (too small to matter)

**Guideline:**
- Small lift but high volume → Ship (e.g., +0.1% on 1M users = 1,000 more conversions)
- Large lift but low volume → Maybe ship (e.g., +50% on 100 users = 50 more conversions)

---

## Decision Framework

### Ship If:

✅ **Positive:** Treatment is better than control
✅ **Significant:** P-value < 0.05
✅ **No Red Flags:** Secondary and counter metrics look good
✅ **Works for Key Segments:** At least works for majority

**Example:**
- Conversion: +10% (p = 0.03) ✅
- Revenue: +8% (p = 0.05) ✅
- Bounce rate: No change ✅
- Works for mobile and desktop ✅
- **Decision: Ship!**

### Iterate If:

⚠️ **Mixed Results:** Some metrics up, some down
⚠️ **Works for Some Segments Only:** E.g., only mobile, not desktop
⚠️ **Close to Significance:** P = 0.06 (just missed)

**Example:**
- Conversion: +10% (p = 0.03) ✅
- Revenue: -5% (p = 0.08) ⚠️
- **Decision: Iterate.** Conversion is up but revenue is down. Investigate why.

### Kill If:

❌ **Negative:** Treatment is worse than control
❌ **Not Significant:** P-value > 0.05
❌ **Opportunity Cost Too High:** Could be working on better ideas

**Example:**
- Conversion: +2% (p = 0.15) ❌
- Took 4 weeks to test
- **Decision: Kill.** Not significant, move on to next idea.

---

## Tools

### Feature Flags

**LaunchDarkly:**
- Feature flag management
- Gradual rollouts
- Kill switches

**Split.io:**
- Feature flags + experimentation
- Real-time metrics

**Unleash:**
- Open-source feature flags
- Self-hosted option

### Experimentation Platforms

**Optimizely:**
- Full-stack experimentation
- Visual editor for web
- Stats Engine (sequential testing)

**VWO (Visual Website Optimizer):**
- A/B testing for web
- Heatmaps, session recordings
- Visual editor

**GrowthBook:**
- Open-source experimentation
- Bayesian statistics
- Feature flags

**Statsig:**
- Modern experimentation platform
- Sequential testing
- Free tier

### Analytics

**Amplitude:**
- Product analytics
- Funnel analysis
- Cohort analysis

**Mixpanel:**
- Event-based analytics
- A/B test analysis
- Retention analysis

**PostHog:**
- Open-source product analytics
- Feature flags
- Session replay

---

## A/B Testing for Engineers

### 1. Feature Flag Implementation

**Node.js (LaunchDarkly):**
```javascript
const LaunchDarkly = require('launchdarkly-node-server-sdk');

const client = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY);

await client.waitForInitialization();

app.get('/checkout', async (req, res) => {
  const user = {
    key: req.user.id,
    email: req.user.email,
    custom: {
      plan: req.user.plan
    }
  };
  
  const showNewCheckout = await client.variation('new-checkout-flow', user, false);
  
  if (showNewCheckout) {
    res.render('checkout-new');
  } else {
    res.render('checkout-old');
  }
});
```

**Python (Statsig):**
```python
from statsig import statsig

statsig.initialize(os.environ['STATSIG_SERVER_KEY'])

@app.route('/checkout')
def checkout():
    user = {
        'userID': current_user.id,
        'email': current_user.email,
        'custom': {
            'plan': current_user.plan
        }
    }
    
    show_new_checkout = statsig.check_gate(user, 'new_checkout_flow')
    
    if show_new_checkout:
        return render_template('checkout_new.html')
    else:
        return render_template('checkout_old.html')
```

### 2. Metric Instrumentation

**Segment (Event Tracking):**
```javascript
const Analytics = require('analytics-node');
const analytics = new Analytics(process.env.SEGMENT_WRITE_KEY);

// Track checkout started
analytics.track({
  userId: user.id,
  event: 'Checkout Started',
  properties: {
    variant: showNewCheckout ? 'treatment' : 'control',
    cart_value: cart.total,
    items_count: cart.items.length
  }
});

// Track checkout completed
analytics.track({
  userId: user.id,
  event: 'Checkout Completed',
  properties: {
    variant: showNewCheckout ? 'treatment' : 'control',
    order_id: order.id,
    revenue: order.total
  }
});
```

### 3. Data Pipeline

**Architecture:**
```
Application
    ↓ (events)
Segment
    ↓ (forwards to)
├── Amplitude (analytics)
├── Mixpanel (analytics)
├── Data Warehouse (BigQuery, Snowflake)
└── Statsig (experimentation)
```

### 4. Results Dashboard

**Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "A/B Test: New Checkout Flow",
    "panels": [
      {
        "title": "Conversion Rate by Variant",
        "targets": [
          {
            "expr": "sum(checkout_completed{variant='control'}) / sum(checkout_started{variant='control'})",
            "legendFormat": "Control"
          },
          {
            "expr": "sum(checkout_completed{variant='treatment'}) / sum(checkout_started{variant='treatment'})",
            "legendFormat": "Treatment"
          }
        ]
      },
      {
        "title": "Sample Size",
        "targets": [
          {
            "expr": "sum(checkout_started{variant='control'})",
            "legendFormat": "Control"
          },
          {
            "expr": "sum(checkout_started{variant='treatment'})",
            "legendFormat": "Treatment"
          }
        ]
      }
    ]
  }
}
```

---

## Real Experiment Examples

### Example 1: Button Color Test (Classic)

**Hypothesis:**
> "If we change the CTA button from blue to orange, click-through rate will increase by 10%, because orange is more attention-grabbing."

**Test:**
- Control: Blue button
- Treatment: Orange button
- Sample size: 10,000 per variant
- Duration: 1 week

**Results:**
- Control: 5.2% CTR
- Treatment: 5.7% CTR
- Lift: +9.6%
- P-value: 0.04 ✅

**Decision:** Ship orange button.

### Example 2: Checkout Flow Optimization

**Hypothesis:**
> "If we reduce checkout from 5 steps to 3 steps, conversion will increase by 15%, because users abandon due to flow length."

**Test:**
- Control: 5-step checkout
- Treatment: 3-step checkout (combined steps)
- Sample size: 50,000 per variant
- Duration: 2 weeks

**Results:**
- Control: 8.5% conversion
- Treatment: 9.8% conversion
- Lift: +15.3%
- P-value: 0.001 ✅

**Secondary Metrics:**
- Time to checkout: 4.2 min → 3.1 min ✅
- Error rate: 2.1% → 1.8% ✅

**Decision:** Ship 3-step checkout.

### Example 3: Pricing Page Variants

**Hypothesis:**
> "If we show annual pricing first (instead of monthly), annual plan adoption will increase by 25%, because anchoring effect."

**Test:**
- Control: Monthly pricing shown first
- Treatment: Annual pricing shown first
- Sample size: 20,000 per variant
- Duration: 3 weeks

**Results:**
- Control: 12% annual adoption
- Treatment: 18% annual adoption
- Lift: +50%
- P-value: 0.001 ✅

**Counter Metrics:**
- Overall conversion: 10.5% → 10.2% ⚠️ (slight drop)

**Decision:** Ship, but monitor overall conversion.

### Example 4: Onboarding Flow

**Hypothesis:**
> "If we add an interactive tutorial in onboarding, activation rate will increase by 30%, because users don't know how to get started."

**Test:**
- Control: No tutorial
- Treatment: Interactive tutorial (5 steps)
- Sample size: 15,000 per variant
- Duration: 2 weeks

**Results:**
- Control: 25% activation rate
- Treatment: 28% activation rate
- Lift: +12%
- P-value: 0.08 ❌ (not significant)

**Segment Analysis:**
- New users: +20% (p = 0.03) ✅
- Returning users: +2% (p = 0.5) ❌

**Decision:** Iterate. Show tutorial only to new users.

---

## Advanced: Bayesian A/B Testing

### Traditional (Frequentist) A/B Testing

**Approach:**
- Null hypothesis: No difference between A and B
- P-value: Probability of seeing this result if null is true
- Reject null if p < 0.05

**Interpretation:**
> "There's a 95% chance the result is not due to random chance."

### Bayesian A/B Testing

**Approach:**
- Prior belief: What we believe before test
- Likelihood: Data from test
- Posterior belief: Updated belief after test

**Interpretation:**
> "There's a 95% probability that B is better than A."

### Benefits of Bayesian

1. **Easier to Interpret:**
   - "95% probability B is better" (intuitive)
   - vs "p = 0.03" (confusing)

2. **Can Stop Early:**
   - No peeking problem
   - Stop when confident enough

3. **Incorporates Prior Knowledge:**
   - Use historical data
   - More accurate with small samples

### Tools That Use Bayesian

- **GrowthBook:** Bayesian by default
- **VWO:** Bayesian engine option
- **Google Optimize:** Bayesian (deprecated)

### Example

**Test:**
- Control: 5.0% conversion (1000 users)
- Treatment: 5.5% conversion (1000 users)

**Frequentist:**
- P-value: 0.15 (not significant)
- Decision: Can't conclude

**Bayesian:**
- Probability B > A: 87%
- Expected lift: +10%
- Decision: Likely better, but not confident enough (need 95%)

---

## Summary

### Quick Reference

**Experiment Types:**
- A/B test: Two variants
- Multivariate: Multiple changes
- Sequential: Stop early
- Holdout: Long-term measurement

**When to Experiment:**
- Significant features
- Uncertain outcomes
- Multiple options
- Optimization

**Process:**
1. Define hypothesis
2. Choose metrics
3. Calculate sample size
4. Set duration
5. Design variants
6. Launch
7. Analyze
8. Decide

**Metrics:**
- Primary: What we're optimizing
- Secondary: Guardrails
- Counter: Watch for negatives

**Statistical Significance:**
- P-value < 0.05
- Power > 80%
- Minimum detectable effect

**Common Pitfalls:**
- Peeking
- Sample ratio mismatch
- Novelty effect
- Seasonality

**Decision Framework:**
- Ship: Positive, significant, no red flags
- Iterate: Mixed results
- Kill: Negative, not significant

**Tools:**
- Feature flags: LaunchDarkly, Split.io
- Experimentation: Optimizely, Statsig, GrowthBook
- Analytics: Amplitude, Mixpanel, PostHog
