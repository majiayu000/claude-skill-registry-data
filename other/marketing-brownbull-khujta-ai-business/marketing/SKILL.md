---
name: marketing
description: Frameworks, strategies, and templates for planning and executing marketing campaigns. Use this skill for market research, crafting messages, segmentation, and analyzing results.
license: MIT
metadata:
  category: business
---
# Marketing Playbook

## Overview

This skill provides marketing frameworks, analysis techniques, and creative guidance to help you plan, execute, and evaluate campaigns.

## Strategic Frameworks

- **STP (Segmentation, Targeting, Positioning)**: Identify market segments, choose your target audiences, and position your product or service to meet their needs.
- **4Ps (Product, Price, Place, Promotion)**: Define your product, set pricing strategy, select distribution channels, and plan promotional tactics.
- **AIDA (Attention, Interest, Desire, Action)**: Structure messaging to capture attention, generate interest, create desire, and drive action.

## Creating a Marketing Plan

1. **Define objectives**: SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound).
2. **Conduct market research**:
   - Analyze competitors.
   - Survey customer needs.
   - Identify trends.
3. **Segment and target**:
   - Group potential customers based on demographics, behavior, or psychographics.
   - Prioritize segments with high potential.
4. **Positioning statement**:
   - Concise description of how your product meets the needs of the target segment and stands out from alternatives.
5. **Develop messaging**:
   - Use the AIDA model to craft compelling copy.
   - Emphasize benefits and address pain points.
6. **Choose channels**:
   - Email, social media, SEO content, paid advertising, events.
7. **Execute and optimize**:
   - Launch campaigns.
   - Measure performance using key metrics (CTR, conversion rate, ROI).
   - Iterate based on data.

## Copywriting Tips

- Focus on benefits, not just features.
- Use clear, concise language.
- Include a strong call-to-action (CTA).
- Personalize messages using customer data.
- Test headlines and subject lines (A/B testing).

## Digital Marketing Tools

- **SEO**: Research keywords, optimize on-page content, and build backlinks.
- **Email marketing**: Segment lists, design visually appealing newsletters, and automate sequences.
- **Social media**: Schedule posts, engage with followers, and use analytics to refine content.
- **Analytics**: Track metrics with Google Analytics, social insights, or built-in platform analytics.

## Data Analysis in Python

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load campaign data
df = pd.read_csv('campaign_results.csv')

# Calculate conversion rate
df['conversion_rate'] = df['conversions'] / df['clicks']

# Plot conversion rate by channel
df.groupby('channel')['conversion_rate'].mean().plot(kind='bar')
plt.xlabel('Channel')
plt.ylabel('Conversion Rate')
plt.title('Average Conversion Rate by Channel')
plt.show()
```

Use this code to analyze marketing performance and identify high-performing channels.

## Additional Resources

- Kotler & Keller, *Marketing Management*.
- HubSpot marketing blog.
- Seth Godin’s books on permission marketing.
