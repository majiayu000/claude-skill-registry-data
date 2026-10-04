---
description: Coordinates multi-channel campaigns across all other skills.
---

# Campaign Orchestrator Skill

## Strategic Value

The Campaign Orchestrator skill provides a centralized control hub for managing complex multi-channel marketing campaigns. It ensures a cohesive brand message and optimized resource allocation across various platforms and agent skills. By integrating with other specialized skills, it automates campaign execution, tracks performance, and adapts strategies in real-time to maximize ROI and achieve marketing objectives. It eliminates manual coordination bottlenecks, allowing for agile and data-driven campaign management.

## Capabilities

- **Multi-channel Integration:** Connects and orchestrates campaigns across social media, email, content marketing, advertising, and other channels.
- **Automated Workflow Management:** Defines and executes campaign workflows, assigning tasks to relevant agent skills (e.g., content creation, ad placement, trend analysis).
- **Real-time Performance Monitoring:** Tracks key campaign metrics (KPIs) and provides a unified dashboard for performance overview.
- **Dynamic Optimization:** Adjusts campaign parameters (e.g., budget allocation, targeting, messaging) based on real-time performance data and predefined rules.
- **Cross-skill Communication:** Facilitates seamless data exchange and collaboration between different agent skills involved in a campaign.
- **Reporting and Analytics:** Generates comprehensive reports on campaign effectiveness, highlighting successes and areas for improvement.

## Limitations

- Requires robust integration with all participating agent skills.
- Initial setup and configuration of campaign workflows can be complex.
- Effectiveness depends on the quality and accuracy of input data from other skills.

## Examples

### Example 1: Launching a New Product Campaign

**User Prompt:** "Orchestrate a new product launch campaign for 'XProduct' targeting young professionals across Instagram, LinkedIn, and email. Allocate 60% of the budget to Instagram, 30% to LinkedIn, and 10% to email. The campaign should run for 4 weeks. Use the 'trend-hijacker' skill for content ideas, 'lead-magnet-creator' for a pre-launch ebook, and 'viral-predictor' to optimize ad creatives."

**Campaign Orchestrator Actions:**

1.  **Define Campaign Structure:** Sets up a 4-week campaign with specified budget allocation per channel.
2.  **Task Assignment (Trend Hijacker):** Requests trending topics relevant to young professionals and XProduct.
3.  **Task Assignment (Lead Magnet Creator):** Initiates creation of a pre-launch ebook lead magnet.
4.  **Task Assignment (Content Creation - via other skills):** Coordinates development of Instagram posts, LinkedIn articles, and email sequences.
5.  **Task Assignment (Viral Predictor):** Submits ad creatives for Instagram and LinkedIn for virality prediction and optimization.
6.  **Scheduled Publishing:** Schedules posts, ads, and emails according to the campaign timeline.
7.  **Performance Monitoring:** Continuously monitors engagement, click-through rates, and conversion rates across all channels.
8.  **Automated Adjustments:** If Instagram ad performance dips, reallocates a small portion of the budget to LinkedIn or suggests new creative based on viral predictor feedback.
9.  **Weekly Reports:** Provides summary reports on campaign progress and ROI.

### Example 2: Seasonal Sales Promotion

**User Prompt:** "Run a 2-week seasonal sales promotion for our summer collection. Focus on Facebook and email retargeting past customers. Use 'pricing-psychology' to craft discount offers and 'competitor-content-monitor' to check similar offers from rivals."

**Campaign Orchestrator Actions:**

1.  **Define Campaign:** Sets up a 2-week sales promotion on Facebook and email targeting.
2.  **Task Assignment (Competitor Content Monitor):** Gathers intelligence on competitor summer sales promotions.
3.  **Task Assignment (Pricing Psychology):** Requests optimized discount strategies (e.g., "buy one get one 50% off" vs. "25% off everything").
4.  **Content Generation:** Creates Facebook ad copies and email newsletters with the chosen offers.
5.  **Targeted Distribution:** Launches retargeting ads on Facebook and sends emails to segmented customer lists.
6.  **Performance Tracking:** Monitors sales conversions attributed to the campaign.
7.  **A/B Testing:** Automatically A/B tests different offer presentations based on pricing psychology recommendations.

## Configuration (config.yaml example)

```yaml
campaigns:
  - id: product_x_launch_2026
    name: "XProduct Launch Campaign"
    duration_weeks: 4
    channels:
      instagram:
        budget_allocation: 0.6
        skills_involved: [trend_hijacker, viral_predictor]
        targets: ["young professionals", "tech enthusiasts"]
      linkedin:
        budget_allocation: 0.3
        skills_involved: [lead_magnet_creator]
        targets: ["marketing managers", "product managers"]
      email:
        budget_allocation: 0.1
        list_segment: "early_adopters"
    objectives:
      - metric: "website_traffic"
        target: 10000
        period: "weekly"
      - metric: "leads_generated"
        target: 500
        period: "campaign"
```
