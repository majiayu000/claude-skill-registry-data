---
summary: "AI-powered Ad Creative Generation"
description: "Generate AI-powered ad creatives including headlines, body copy, calls-to-action (CTAs), and A/B test variations tailored for platforms like Facebook, Instagram, Google Ads, and in-app promotions. Focuses on performance marketing for Tecno Mobile and agency clients."
---

# 🎨 Ad Creative Generation Skill

This skill leverages AI to rapidly generate high-performing ad creatives. It's designed for performance marketers at Tecno Mobile and agency environments, aiming to streamline the ad creation process, increase conversion rates, and optimize ad spend.

## 🚀 Use Cases for Tecno Mobile & Agency Work

### Tecno Mobile:
-   **New Product Launches:** Quickly generate diverse ad copy and visual concepts for new Tecno smartphone or accessory launches (e.g., "Tecno Pova 6 Pro 5G - Unleash Infinite Power").
-   **Campaign Optimization:** Create multiple A/B test variants for existing ad campaigns to improve CTR and CVR (e.g., testing different headlines for a sales campaign).
-   **Localized Campaigns:** Generate culturally relevant ad creatives for specific regions or Festive periods in India (e.g., Diwali, Eid, Baisakhi).
-   **Performance Marketing:** Produce data-driven ad copy for Facebook, Instagram, and Google Ads focusing on key product features and benefits (e.g., camera, battery life, processor).
-   **In-App Promotion:** Develop engaging creatives for app store listings and in-app advertisements for pre-installed Tecno apps or partnerships.

### Agency Work:
-   **Client Onboarding:** Rapidly prototype ad creative ideas for new clients across various industries (e.g., e-commerce, real estate, SaaS).
-   **Campaign Scaling:** Generate a high volume of diverse ad copy and CTA options to scale successful campaigns across multiple platforms and audiences.
-   **Creative Block Breaker:** Overcome creative stagnation by exploring novel angles and messaging strategies suggested by the AI.
-   **Personalized Ads:** Produce dynamic ad content tailored to specific audience segments based on demographics, interests, and behavior.
-   **Competitive Analysis:** Generate ad copy that counter-positions competitors' messaging by highlighting unique selling propositions.

## ✨ Features

-   **Headline Generation:** Craft compelling and attention-grabbing headlines.
-   **Body Copy (Primary Text) Generation:** Develop persuasive ad descriptions.
-   **Call-to-Action (CTA) Suggestions:** Propose effective CTAs (e.g., "Shop Now," "Learn More," "Pre-order Today").
-   **Visual Concept Prompts:** Generate textual prompts for image/video creation, suggesting themes, elements, and styles.
-   **A/B Test Variant Generation:** Automatically create multiple versions of headlines, body copy, and CTAs for testing.
-   **Platform-Specific Optimization:** Tailor output for character limits and best practices of Facebook, Instagram, Google Ads, etc.

## 🛠️ `agent.py` Implementation Overview

The `agent.py` will expose functions to:
-   `generate_ad_creative(product_name, key_features, target_audience, platform, tone, num_variants)`: Generates a full ad creative set.
-   `generate_headlines(product_name, key_features, tone, num_headlines)`: Focus specifically on headlines.
-   `generate_ctas(product_name, tone, num_ctas)`: Generate CTA options.
-   `generate_visual_prompts(product_name, key_features, tone, num_prompts)`: Create prompts for visual assets.

## 📝 Tested Workflows

### Workflow 1: New Tecno Product Launch Ad Set
1.  **Input:** `product_name="Tecno Pova 6 Pro 5G"`, `key_features=["108MP Camera", "6000mAh Battery", "Dimensity 8300-Ultra"]`, `target_audience="Young tech enthusiasts, mobile gamers"`, `platform="Facebook, Instagram"`, `tone="Excited, powerful"`, `num_variants=3`
2.  **Output:** 3 distinct ad creative variants, each with headline, body copy, CTA, and visual concept prompts, ready for Facebook/Instagram Ads Manager.
    -   Variant A: Focus on Camera + Gaming.
    -   Variant B: Focus on Battery + Performance.
    -   Variant C: Focus on overall power + innovation.

### Workflow 2: A/B Testing Existing Campaign - Headline Optimization
1.  **Input:** `product_name="Tecno Spark 10C"`, `current_body_copy="Experience blazing-fast performance and stunning visuals. Get your Tecno Spark 10C today!"`, `key_features=["90Hz Display", "5000mAh Battery"]`, `tone="Direct, Benefit-driven"`, `num_headlines=5`
2.  **Output:** 5 different headlines that can be rotated into the existing ad copy for A/B testing on Google Ads.
    -   "Spark Your Day: Tecno Spark 10C!"
    -   "Smooth Scrolls, Long Lasting Power."
    -   "Experience the 90Hz Spark 10C."
    -   "Affordable Power: Get Spark 10C."
    -   "Your Next Upgrade: Spark 10C."

## 💡 Real Examples (Simulated Outputs)

**Input:**
`generate_ad_creative(product_name="Tecno Pova 6 Pro 5G", key_features=["6000mAh Battery", "108MP Ultra Clarity Camera", "Slim Design"], target_audience="Gamers, tech enthusiasts who prioritize battery and camera", platform="Facebook", tone="Bold, Innovative", num_variants=1)`

**Output (Example Variant 1):**

---
**Platform:** Facebook Ad

**Headline:**
**🔥 UNLEASH INFINITE POWER: Tecno Pova 6 Pro 5G is HERE!**

**Primary Text:**
Dominate every game, capture every detail! The new Tecno Pova 6 Pro 5G packs a massive 6000mAh battery for endless action and an unprecedented 108MP Ultra Clarity Camera to bring your world to life. All in a stunningly slim design that fits your style. Ready to experience the future?

**Call to Action:**
Shop Now | Learn More

**Visual Concept Prompt:**
Dynamic shot of the Tecno Pova 6 Pro 5G in action: a hand holding the phone mid-game with vibrant graphics, transitioning to a high-res photo captured by the phone, with a subtle focus on the slim profile. Energetic, futuristic feel. Colors: Electric blue/green accents.
---
