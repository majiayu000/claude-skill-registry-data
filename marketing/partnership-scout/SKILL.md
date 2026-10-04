---
name: "Partnership Scout"
description: "Find and evaluate strategic partners"
author: "@namanwtf"
version: 3.0.0
---

# Partnership Scout

## When to Use

Use this skill to identify, evaluate, and initiate strategic partnerships that can amplify your brand's reach and impact. This is essential when you need to:

-   **Expand Market Reach:** Find partners who can introduce your brand to new audiences and markets.
-   **Co-Marketing Opportunities:** Discover complementary brands for joint campaigns and cross-promotion.
-   **Influencer & Creator Partnerships:** Identify relevant influencers and content creators for authentic collaborations.
-   **Strategic Alliances:** Evaluate potential business partners for long-term strategic relationships.
-   **Event & Sponsorship Opportunities:** Find events, conferences, and sponsorship opportunities aligned with your brand.
-   **Distribution Channels:** Identify new channels and platforms to distribute your products or content.

## Capabilities

The Partnership Scout skill provides the following capabilities:

-   **Partner Discovery:** Searches and identifies potential partners based on criteria like industry, audience demographics, values alignment, and market presence.
-   **Compatibility Scoring:** Evaluates potential partners using a multi-factor scoring system considering audience overlap, brand values, reputation, and engagement metrics.
-   **Outreach Template Generation:** Creates personalized outreach messages and partnership proposals tailored to each prospect.
-   **Competitive Partnership Analysis:** Analyzes your competitors' partnerships to identify gaps and opportunities.
-   **Partnership Performance Tracking:** Monitors and reports on the success of existing partnerships using defined KPIs.
-   **Contract & Terms Guidance:** Provides templates and guidance for partnership agreements and terms.
-   **Risk Assessment:** Flags potential risks associated with prospective partners (reputation, financial stability, audience fit).

## Usage Examples

### Example 1: Find potential co-marketing partners in the fitness industry

```python
partnership.find_partners(
    industry="fitness & wellness",
    target_audience="millennials interested in health",
    partnership_type="co-marketing",
    min_followers=50000,
    values_alignment=["sustainability", "inclusivity"]
)
```

### Example 2: Evaluate a specific brand for partnership potential

```python
partnership.evaluate_brand(
    brand_name="EcoFriendly Apparel Co.",
    evaluation_criteria=["audience_overlap", "brand_reputation", "values_alignment", "engagement_rate"]
)
```

### Example 3: Generate an outreach email for a potential influencer partner

```python
partnership.generate_outreach(
    partner_name="FitLife Sarah",
    platform="Instagram",
    partnership_type="product_collaboration",
    your_brand="GreenGear Fitness",
    mutual_benefit="Shared audience of eco-conscious fitness enthusiasts"
)
```

## Configuration

The Partnership Scout skill can be configured with the following parameters:

-   **`minimum_partner_followers`**: (Integer, optional) Sets the minimum follower count threshold for influencer partners. Default is 10000.
-   **`industries_of_interest`**: (List of Strings, optional) Specifies industries to focus partnership searches on.
-   **`excluded_brands`**: (List of Strings, optional) Lists brands or competitors to exclude from partnership recommendations.
-   **`values_priorities`**: (List of Strings, optional) Defines brand values that are prioritized in partnership matching (e.g., ["sustainability", "innovation", "diversity"]).
-   **`api_keys`**: (Dictionary, optional) Contains API keys for social media and business intelligence platforms.
    -   `linkedin_api_key`: (String) For LinkedIn company data.
    -   `instagram_api_key`: (String) For Instagram influencer metrics.
    -   `crunchbase_api_key`: (String) For startup and company intelligence.

Example configuration in your `config.yaml`:

```yaml
partnership_scout:
    minimum_partner_followers: 25000
    industries_of_interest:
        - "fitness & wellness"
        - "sustainable fashion"
        - "health tech"
    excluded_brands:
        - "Competitor Brand X"
        - "Controversial Company Y"
    values_priorities:
        - "sustainability"
        - "innovation"
        - "community_focus"
    api_keys:
        linkedin_api_key: "YOUR_LINKEDIN_API_KEY"
        instagram_api_key: "YOUR_INSTAGRAM_API_KEY"
        crunchbase_api_key: "YOUR_CRUNCHBASE_API_KEY"
```
