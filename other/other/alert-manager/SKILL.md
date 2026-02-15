---
name: alert-manager
description: 'Use when the user asks to "set up SEO alerts", "monitor rankings", "notify me when rankings drop", "traffic alerts", "watch competitor changes", "alert me if rankings drop", "notify me of traffic changes", or "watch my keywords for changes". Sets up and manages alerts for critical SEO and GEO metrics including ranking drops, traffic changes, technical issues, and competitor movements. Enables proactive monitoring and quick response to issues. For detailed rank analysis, see rank-tracker. For comprehensive reporting, see performance-reporter.'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - alerts
    - monitoring
    - ranking alerts
    - traffic monitoring
    - competitor alerts
    - seo notifications
    - proactive monitoring
  triggers:
    - "set up SEO alerts"
    - "monitor rankings"
    - "notify me when rankings drop"
    - "traffic alerts"
    - "watch competitor changes"
    - "alert me"
    - "ranking notifications"
    - "alert me if rankings drop"
    - "notify me of traffic changes"
    - "watch my keywords for changes"
---

# Alert Manager


> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · Install all: `npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) · [technical-seo-checker](../../optimize/technical-seo-checker/) · [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) · [content-refresher](../../optimize/content-refresher/)

**Monitor** · [rank-tracker](../rank-tracker/) · [backlink-analyzer](../backlink-analyzer/) · [performance-reporter](../performance-reporter/) · **alert-manager**

**Cross-cutting** · [content-quality-auditor](../../cross-cutting/content-quality-auditor/) · [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) · [entity-optimizer](../../cross-cutting/entity-optimizer/) · [memory-management](../../cross-cutting/memory-management/)

</details>

This skill helps you set up proactive monitoring alerts for critical SEO and GEO metrics. Get notified when rankings drop, traffic changes significantly, technical issues occur, or competitors make moves.

## When to Use This Skill

- Setting up SEO monitoring systems
- Creating ranking drop alerts
- Monitoring technical SEO health
- Tracking competitor movements
- Alerting on content performance changes
- Monitoring GEO/AI visibility changes
- Setting up brand mention alerts

## What This Skill Does

1. **Alert Configuration**: Sets up custom alert thresholds
2. **Multi-Metric Monitoring**: Tracks rankings, traffic, technical issues
3. **Threshold Management**: Defines when alerts trigger
4. **Priority Classification**: Categorizes alerts by severity
5. **Notification Setup**: Configures how alerts are delivered
6. **Alert Response Plans**: Creates action plans for each alert type
7. **Alert History**: Tracks alert patterns over time

## How to Use

### Set Up Alerts

```
Set up SEO monitoring alerts for [domain]
```

```
Create ranking drop alerts for my top 20 keywords
```

### Configure Specific Alerts

```
Alert me when [specific condition]
```

```
Set up competitor monitoring for [competitor domains]
```

### Review Alert System

```
Review and optimize my current SEO alerts
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~search console + ~~web crawler connected:**
Automatically monitor real-time metric feeds for ranking changes via ~~SEO tool API, indexing and coverage alerts from ~~search console, and technical health alerts from ~~web crawler. Set up automated threshold-based alerts with notification delivery.

**With manual data only:**
Ask the user to provide:
1. Current baseline metrics for alert thresholds (rankings, traffic, backlinks)
2. Critical keywords or pages to monitor
3. Alert priority levels and notification preferences
4. Historical data to understand normal fluctuation ranges
5. Manual reporting on metric changes when they check their tools

Proceed with the alert configuration using provided parameters. User will need to manually check metrics and report changes for alert triggers.

## Instructions

When a user requests alert setup:

1. **Define Alert Categories**

   ```markdown
   ## SEO Alert System Configuration
   
   **Domain**: [domain]
   **Configured Date**: [date]
   
   ### Alert Categories
   
   | Category | Description | Typical Urgency |
   |----------|-------------|-----------------|
   | Ranking Alerts | Keyword position changes | Medium-High |
   | Traffic Alerts | Organic traffic fluctuations | High |
   | Technical Alerts | Site health issues | Critical |
   | Backlink Alerts | Link profile changes | Medium |
   | Competitor Alerts | Competitor movements | Low-Medium |
   | GEO Alerts | AI visibility changes | Medium |
   | Brand Alerts | Brand mentions and reputation | Medium |
   ```

2. **Configure Ranking Alerts**

   ```markdown
   ## Ranking Alerts
   
   ### Position Drop Alerts
   
   | Alert Name | Condition | Threshold | Priority | Action |
   |------------|-----------|-----------|----------|--------|
   | Critical Drop | Any top 3 keyword drops 5+ positions | Position change ≥5 | 🔴 Critical | Immediate investigation |
   | Major Drop | Top 10 keyword drops out of top 10 | Position >10 | 🔴 High | Same-day review |
   | Moderate Drop | Any keyword drops 10+ positions | Position change ≥10 | 🟡 Medium | Weekly review |
   | Competitor Overtake | Competitor passes you for key term | Comp position < yours | 🟡 Medium | Analysis needed |
   
   ### Position Improvement Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | New Top 3 | Keyword enters top 3 | Position ≤3 | 🟢 Positive |
   | Page 1 Entry | Keyword enters top 10 | Position ≤10 | 🟢 Positive |
   | Significant Climb | Keyword improves 10+ positions | Change ≥+10 | 🟢 Positive |
   
   ### SERP Feature Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Snippet Lost | Lost featured snippet ownership | 🔴 High |
   | Snippet Won | Won new featured snippet | 🟢 Positive |
   | AI Overview Change | Appeared/disappeared in AI Overview | 🟡 Medium |
   
   ### Keywords to Monitor
   
   | Keyword | Current Rank | Alert Threshold | Priority |
   |---------|--------------|-----------------|----------|
   | [keyword 1] | [X] | Drop ≥3 | 🔴 Critical |
   | [keyword 2] | [X] | Drop ≥5 | 🔴 High |
   | [keyword 3] | [X] | Drop ≥10 | 🟡 Medium |
   ```

3. **Configure Traffic Alerts**

   ```markdown
   ## Traffic Alerts
   
   ### Traffic Decline Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | Traffic Crash | Day-over-day decline | ≥50% drop | 🔴 Critical |
   | Significant Drop | Week-over-week decline | ≥30% drop | 🔴 High |
   | Moderate Decline | Month-over-month decline | ≥20% drop | 🟡 Medium |
   | Trend Warning | 3 consecutive weeks decline | Any decline | 🟡 Medium |
   
   ### Traffic Anomaly Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Traffic Spike | Unusual increase | 🟢 Investigate |
   | Zero Traffic | Page receiving 0 visits | 🔴 High |
   | Bot Traffic | Unusual traffic pattern | 🟡 Medium |
   
   ### Page-Level Alerts
   
   | Page Type | Alert Condition | Priority |
   |-----------|-----------------|----------|
   | Homepage | Any 20%+ decline | 🔴 Critical |
   | Top 10 pages | Any 30%+ decline | 🔴 High |
   | Conversion pages | Any 25%+ decline | 🔴 High |
   | Blog posts | Any 40%+ decline | 🟡 Medium |
   
   ### Conversion Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Conversion Drop | Organic conversions down 30%+ | 🔴 Critical |
   | CVR Decline | Conversion rate drops 20%+ | 🔴 High |
   ```

4. **Configure Technical SEO Alerts**

   ```markdown
   ## Technical SEO Alerts
   
   ### Critical Technical Alerts
   
   | Alert Name | Condition | Priority | Response Time |
   |------------|-----------|----------|---------------|
   | Site Down | HTTP 5xx errors | 🔴 Critical | Immediate |
   | SSL Expiry | Certificate expiring in 14 days | 🔴 Critical | Same day |
   | Robots.txt Block | Important pages blocked | 🔴 Critical | Same day |
   | Index Dropped | Pages dropping from index | 🔴 Critical | Same day |
   
   ### Crawl & Index Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Crawl Errors Spike | Errors increase 50%+ | 🔴 High |
   | New 404 Pages | 404 errors on important pages | 🟡 Medium |
   | Redirect Chains | 3+ redirect hops detected | 🟡 Medium |
   | Duplicate Content | New duplicates detected | 🟡 Medium |
   | Index Coverage Drop | Indexed pages decline 10%+ | 🔴 High |
   
   ### Performance Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Core Web Vitals Fail | CWV drops to "Poor" | 🔴 High |
   | Page Speed Drop | Load time increases 50%+ | 🟡 Medium |
   | Mobile Issues | Mobile usability errors | 🔴 High |
   
   ### Security Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Security Issue | GSC security warning | 🔴 Critical |
   | Manual Action | Google manual action | 🔴 Critical |
   | Malware Detected | Site flagged for malware | 🔴 Critical |
   ```

5. **Configure Backlink Alerts**

   ```markdown
   ## Backlink Alerts
   
   ### Link Loss Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link Lost | DA 70+ link removed | 🔴 High |
   | Multiple Links Lost | 10+ links lost in a day | 🟡 Medium |
   | Referring Domain Lost | Lost entire domain's links | 🟡 Medium |
   
   ### Link Gain Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link | New DA 70+ link | 🟢 Positive |
   | Suspicious Links | Many low-quality links | 🟡 Review |
   | Negative SEO | Spam link attack pattern | 🔴 High |
   
   ### Link Profile Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Toxic Score Increase | Toxic score up 20%+ | 🔴 High |
   | Anchor Over-Optimization | Exact match anchors >30% | 🟡 Medium |
   ```

6. **Configure Competitor Alerts**

   ```markdown
   ## Competitor Monitoring Alerts
   
   ### Ranking Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Competitor Overtake | Competitor passes you | 🟡 Medium |
   | Competitor Top 3 | Competitor enters top 3 on key term | 🟡 Medium |
   | Competitor Content | Competitor publishes on your topic | 🟢 Info |
   
   ### Activity Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | New Backlinks | Competitor gains high-DA link | 🟢 Info |
   | Content Update | Competitor updates ranking content | 🟢 Info |
   | New Content | Competitor publishes new content | 🟢 Info |
   
   ### Competitors to Monitor
   
   | Competitor | Domain | Monitor Keywords | Alert Priority |
   |------------|--------|------------------|----------------|
   | [Competitor 1] | [domain] | [X] keywords | High |
   | [Competitor 2] | [domain] | [X] keywords | Medium |
   | [Competitor 3] | [domain] | [X] keywords | Low |
   ```

7. **Configure GEO/AI Alerts**

   ```markdown
   ## GEO (AI Visibility) Alerts
   
   ### AI Citation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Lost | Lost AI Overview citation | 🟡 Medium |
   | Citation Won | New AI Overview citation | 🟢 Positive |
   | Citation Position Drop | Dropped from 1st to 3rd+ source | 🟡 Medium |
   | New AI Overview | AI Overview appears for tracked keyword | 🟢 Info |
   
   ### GEO Trend Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Rate Drop | AI citation rate drops 20%+ | 🔴 High |
   | GEO Competitor | Competitor cited where you're not | 🟡 Medium |
   ```

8. **Configure Brand Alerts**

   ```markdown
   ## Brand Monitoring Alerts
   
   ### Mention Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Brand Mention | New brand mention online | 🟢 Info |
   | Negative Mention | Negative sentiment mention | 🔴 High |
   | Review Alert | New review on key platforms | 🟡 Medium |
   | Unlinked Mention | Brand mention without link | 🟢 Opportunity |
   
   ### Reputation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Review Rating Drop | Average rating drops | 🔴 High |
   | Negative Press | Negative news article | 🔴 High |
   | Competitor Comparison | Named in competitor comparison | 🟡 Medium |
   ```

9. **Define Alert Response Plans**

   ```markdown
   ## Alert Response Plans
   
   ### Critical Alert Response (🔴)
   
   **Response Time**: Immediate (within 1 hour)
   
   | Alert Type | Immediate Actions |
   |------------|-------------------|
   | Site Down | 1. Check server status 2. Contact hosting 3. Check DNS |
   | Traffic Crash | 1. Check for algorithm update 2. Review GSC errors 3. Check competitors |
   | Manual Action | 1. Review GSC message 2. Identify issue 3. Begin remediation |
   | Critical Rank Drop | 1. Check if page indexed 2. Review SERP 3. Analyze competitors |
   
   ### High Priority Response (🔴/🟡)
   
   **Response Time**: Same day
   
   | Alert Type | Actions |
   |------------|---------|
   | Major Rank Drops | Analyze cause, create recovery plan |
   | Traffic Decline | Investigate source, check technical issues |
   | Backlink Loss | Attempt recovery outreach |
   | CWV Failure | Diagnose and fix performance issues |
   
   ### Medium Priority Response (🟡)
   
   **Response Time**: Within 48 hours
   
   | Alert Type | Actions |
   |------------|---------|
   | Moderate Rank Changes | Monitor trend, plan content updates |
   | Competitor Movement | Analyze competitor changes |
   | New 404s | Set up redirects, update internal links |
   
   ### Low Priority (🟢)
   
   **Response Time**: Weekly review
   
   | Alert Type | Actions |
   |------------|---------|
   | Positive Changes | Document wins, understand cause |
   | Info Alerts | Log for trend analysis |
   ```

10. **Set Up Alert Delivery**

    ```markdown
    ## Alert Notification Setup
    
    ### Notification Channels
    
    | Priority | Channels | Frequency |
    |----------|----------|-----------|
    | 🔴 Critical | Email + SMS + Slack | Immediate |
    | 🔴 High | Email + Slack | Immediate |
    | 🟡 Medium | Email + Slack | Daily digest |
    | 🟢 Low | Email | Weekly digest |
    
    ### Alert Recipients
    
    | Role | Critical | High | Medium | Low |
    |------|----------|------|--------|-----|
    | SEO Manager | ✅ | ✅ | ✅ | ✅ |
    | Dev Team | ✅ | ✅ (tech only) | ❌ | ❌ |
    | Marketing Lead | ✅ | ✅ | ❌ | ❌ |
    | Executive | ✅ | ❌ | ❌ | ❌ |
    
    ### Alert Suppression
    
    - Suppress duplicate alerts for 24 hours
    - Don't alert on known issues (maintenance windows)
    - Batch low-priority alerts into digests
    
    ### Alert Escalation
    
    | If No Response In | Escalate To |
    |-------------------|-------------|
    | 1 hour (Critical) | SEO Manager → Director |
    | 4 hours (High) | Team Lead → Manager |
    | 24 hours (Medium) | Team → Lead |
    ```

11. **Create Alert Summary**

    ```markdown
    # SEO Alert System Summary
    
    **Domain**: [domain]
    **Configured**: [date]
    **Total Active Alerts**: [X]
    
    ## Alert Count by Category
    
    | Category | Critical | High | Medium | Low | Total |
    |----------|----------|------|--------|-----|-------|
    | Rankings | [X] | [X] | [X] | [X] | [X] |
    | Traffic | [X] | [X] | [X] | [X] | [X] |
    | Technical | [X] | [X] | [X] | [X] | [X] |
    | Backlinks | [X] | [X] | [X] | [X] | [X] |
    | Competitors | [X] | [X] | [X] | [X] | [X] |
    | GEO | [X] | [X] | [X] | [X] | [X] |
    | **Total** | **[X]** | **[X]** | **[X]** | **[X]** | **[X]** |
    
    ## Quick Reference
    
    ### If You Get a Critical Alert
    
    1. Don't panic
    2. Check alert details
    3. Follow response plan
    4. Document actions taken
    5. Update stakeholders
    
    ### Weekly Alert Review Checklist
    
    - [ ] Review all alerts triggered
    - [ ] Identify patterns
    - [ ] Adjust thresholds if needed
    - [ ] Update response plans
    - [ ] Clean up false positives
    ```

## Validation Checkpoints

### Input Validation
- [ ] Alert thresholds are based on realistic baseline data
- [ ] Critical keywords and pages clearly identified
- [ ] Response plans defined for each alert priority level
- [ ] Notification channels configured with appropriate recipients

### Output Validation
- [ ] Every metric cites its data source and collection date
- [ ] Alert thresholds account for normal metric fluctuations
- [ ] Response plans are specific and time-bound
- [ ] Source of each alert trigger clearly stated (~~SEO tool API alert, ~~search console notification, ~~web crawler alert, or manual user check)

## Example

**User**: "Set up ranking drop alerts for my top keywords"

**Output**:

```markdown
## Ranking Alert Configuration

### Critical Keywords (Immediate Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| best project management software | 2 | Drops to 5+ | 🔴 Critical |
| project management tools | 4 | Drops to 8+ | 🔴 Critical |
| team collaboration software | 1 | Any drop | 🔴 Critical |

### Important Keywords (Same-Day Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| agile project management | 7 | Drops out of top 10 | 🔴 High |
| kanban software | 9 | Drops out of top 10 | 🔴 High |

### Alert Response Plan

**If Critical Keyword Drops**:
1. Check if page is still indexed (site:url)
2. Look for algorithm update announcements
3. Analyze what changed in SERP
4. Review competitor ranking changes
5. Check for technical issues on page
6. Create recovery action plan within 24 hours

**Notification**: Email + Slack to SEO team immediately
```

## Tips for Success

1. **Start simple** - Don't create too many alerts initially
2. **Tune thresholds** - Adjust based on normal fluctuations
3. **Avoid alert fatigue** - Too many alerts = ignored alerts
4. **Document response plans** - Know what to do when alerts fire
5. **Review regularly** - Alerts need maintenance as your SEO matures
6. **Include positive alerts** - Track wins, not just problems

## Alert Threshold Recommendations

### Recommended Alert Thresholds by Metric

| Metric | Warning Threshold | Critical Threshold | Check Frequency |
|--------|------------------|-------------------|-----------------|
| Organic traffic | -15% WoW | -30% WoW | Daily |
| Average position (tracked KWs) | >3 position drop | >5 position drop | Daily |
| Pages indexed | -5% change | -20% change | Weekly |
| Crawl errors | >10 new errors | >50 new errors | Daily |
| Core Web Vitals | Any metric moves to "Needs Improvement" | Any metric moves to "Poor" | Weekly |
| Backlinks lost | >5% of total in 1 week | >15% in 1 week | Weekly |
| AI citation loss | Any key query loses citation | >20% queries lose citation | Weekly |
| Server errors (5xx) | >1% of pages | >5% of pages | Daily |
| Security issues | Any detected | Any detected | Daily |
| Manual penalty | N/A | Any notification | Daily |

## Alert Fatigue Prevention

### Alert Management Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Tiered severity** | Not all alerts need immediate action | Critical: Immediate; Warning: Review daily; Info: Weekly digest |
| **Threshold tuning** | Reduce false positives | Start conservative, tighten after 1 month of baseline data |
| **Grouping** | Prevent alert storms | Group related alerts (e.g., multiple rank drops = "ranking alert") |
| **Cooldown periods** | Avoid repeated alerts for same issue | Do not re-alert on same metric for 24-48 hours |
| **Scheduled digests** | Reduce notification volume | Batch non-urgent alerts into daily or weekly email |
| **Auto-resolution** | Close alerts when metric recovers | Track recovery and auto-close if threshold restored |

### Alert Priority Classification

| Priority | Response Time | Notification Channel | Example |
|----------|-------------|---------------------|---------|
| P0 — Emergency | Within 1 hour | SMS + Slack + Email | Site down, manual penalty, security breach |
| P1 — Urgent | Same day | Slack + Email | Major traffic drop, crawl blocked, indexing issues |
| P2 — Important | Within 48 hours | Email + Weekly digest | Rank drops, CWV degradation, backlink loss |
| P3 — Monitor | Next weekly review | Weekly digest only | Minor fluctuations, new competitor content |

## Escalation Path Templates

### Standard Escalation Flow

```
Alert Triggers -> Automated Classification -> Route by Priority

P0: Notify SEO Lead + Dev Team immediately
    -> If not acknowledged in 30 min -> Notify Engineering Manager
        -> If not resolved in 2 hours -> Notify VP/Director

P1: Notify SEO Lead
    -> If not acknowledged in 4 hours -> Notify Marketing Manager
        -> Add to next standup agenda

P2: Add to daily digest
    -> If persists >1 week -> Escalate to P1

P3: Add to weekly digest
    -> If persists >1 month -> Escalate to P2
```

## Alert Response Playbooks

### Traffic Drop Alert

| Step | Action | If True | If False |
|------|--------|---------|----------|
| 1 | Check if site-wide or page-specific | Go to Step 2a | Go to Step 2b |
| 2a | Check Google Search Status Dashboard for algorithm update | Document and wait | Go to Step 3 |
| 2b | Check specific page for technical issues (404, noindex, slow) | Fix technical issue | Go to Step 3 |
| 3 | Check Search Console for crawl errors or index drops | Fix crawl/index issues | Go to Step 4 |
| 4 | Check if competitors published new content | Analyze and plan content response | Go to Step 5 |
| 5 | Check backlink profile for lost links | Outreach for link recovery | Escalate for deeper analysis |

### Ranking Drop Alert

| Step | Action | If True | If False |
|------|--------|---------|----------|
| 1 | Verify the drop is real (check multiple tools, wait 24-48h) | Confirmed drop, go to Step 2 | False alarm, close alert |
| 2 | Check if algorithm update occurred | Document, monitor, improve content quality | Go to Step 3 |
| 3 | Check if your page changed recently | Revert or fix the change | Go to Step 4 |
| 4 | Analyze the SERP — did a new competitor appear? | Study competitor, plan response | Go to Step 5 |
| 5 | Check for lost backlinks to the ranking page | Recover links or build new ones | Escalate for full audit |

### Technical Alert (Site Down / 5xx Errors)

| Step | Action | If True | If False |
|------|--------|---------|----------|
| 1 | Confirm site is actually down (check from multiple locations) | Go to Step 2 | Close alert as false positive |
| 2 | Check server/hosting status page | Provider issue — contact support, wait | Go to Step 3 |
| 3 | Check recent deployments or configuration changes | Rollback the change | Go to Step 4 |
| 4 | Check server resource usage (CPU, memory, disk) | Scale resources or optimize | Escalate to engineering |

## Reference Materials

- [Alert Threshold Guide](./references/alert-threshold-guide.md) — Recommended thresholds by metric, fatigue prevention strategies, and escalation path templates

## Related Skills

- [rank-tracker](../rank-tracker/) — Ranking data for alerts
- [backlink-analyzer](../backlink-analyzer/) — Backlink monitoring
- [technical-seo-checker](../../optimize/technical-seo-checker/) — Technical monitoring
- [performance-reporter](../performance-reporter/) — Alert summaries in reports
- [memory-management](../../cross-cutting/memory-management/) — Store alert history and thresholds in project memory
- [content-refresher](../../optimize/content-refresher/) — Content decay alerts trigger refresh workflows

