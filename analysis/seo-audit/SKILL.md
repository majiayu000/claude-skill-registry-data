---
summary: "Comprehensive SEO Audit"
description: "Conducts comprehensive SEO audits covering technical, on-page, backlink, and competitor gap analysis. Provides actionable recommendations to improve organic search performance for Tecno Mobile and agency clients."
---

# 🔍 Comprehensive SEO Audit Skill

This skill performs a thorough SEO audit to identify critical issues and opportunities for improvement across various aspects of a website. It provides actionable insights for Tecno Mobile properties and agency clients, helping them achieve higher rankings, more organic traffic, and better online visibility.

## 🚀 Use Cases for Tecno Mobile & Agency Work

### Tecno Mobile:
-   **Website Health Check:** Regularly audit the main Tecno Mobile website (e.g., tecno-mobile.in) for technical SEO issues (crawlability, indexability, site speed, mobile-friendliness).
-   **New Product Launch Readiness:** Before launching a new product page, perform an on-page and technical audit to ensure it meets all SEO best practices.
-   **Content Performance Review:** Audit specific content hubs or blog categories to identify underperforming pages, duplicate content issues, or opportunities for content expansion.
-   **Competitor Backlink Analysis:** Analyze backlink profiles of top competitors to identify link-building opportunities and understand their strategies.
-   **International SEO Audit:** Review subdomains/subdirectories for different regions (e.g., Tecno India) for correct hreflang implementation, localized content, and regional search performance.

### Agency Work:
-   **New Client Discovery:** Rapidly conduct initial SEO audits for prospective and new clients to identify quick wins and lay the foundation for a long-term SEO strategy.
-   **Ongoing Client Reporting:** Provide periodic SEO audit summaries to clients, demonstrating value and progress based on identified issues and implemented solutions.
-   **Migration Support:** Audit websites before and after major CMS changes or site redesigns to prevent SEO traffic drops.
-   **Penalty Recovery:** Identify potential causes of Google penalties (e.g., unnatural link profiles, thin content) and recommend recovery strategies.
-   **Market Opportunity Analysis:** Use competitor gap analysis to find niches where clients can outperform competitors with targeted content or technical improvements.

## ✨ Features

-   **Technical SEO Audit:** Checks for crawl errors, indexation issues, site speed (Core Web Vitals), mobile-friendliness, broken links, HTTPS status, XML sitemap, robots.txt optimization, and structured data implementation.
-   **On-Page SEO Audit:** Analyzes title tags, meta descriptions, heading structure (H1-H6), content quality, keyword usage, image alt attributes, internal linking, and content readability.
-   **Backlink Profile Analysis:** Evaluates backlink quantity and quality, identifies toxic links, checks anchor text distribution, and assesses referring domain diversity.
-   **Competitor Gap Analysis:** Compares website performance with key competitors across organic keywords, content topics, and backlink profiles to identify opportunities.
-   **Actionable Recommendations:** Generates a prioritized list of recommendations with estimated impact and effort levels.

## 🛠️ `agent.py` Implementation Overview

The `agent.py` will expose functions to:
-   `run_full_seo_audit(target_url, competitor_urls=None)`: Performs a comprehensive SEO audit.
-   `audit_technical_seo(target_url)`: Focuses on technical aspects.
-   `audit_on_page_seo(page_url, keywords=None)`: Specifically audits on-page elements.
-   `analyze_backlinks(target_domain, competitor_domains=None)`: Evaluates backlink profiles.
-   `perform_competitor_gap_analysis(target_domain, competitor_domains)`: Compares against competitors.

## 📝 Tested Workflows

### Workflow 1: Pre-Launch Technical & On-Page Audit for a New Tecno Product Page
1.  **Input:** `target_url="https://www.tecno-mobile.in/pova-6-pro-5g-launch-page"`, `keywords=["Tecno Pova 6 Pro 5G price", "Pova 6 Pro 5G features"]`
2.  **Output:** An audit report highlighting any technical issues (e.g., page not indexed, slow load time) and on-page recommendations (e.g., missing H1, poor keyword density) before the official launch.

### Workflow 2: Monthly Backlink Health Check for Agency Client
1.  **Input:** `target_domain="client-ecommerce.com"`, `competitor_domains=["competitorA.com", "competitorB.com"]`
2.  **Output:** A report on the client's backlink profile, identifying new backlinks, potentially toxic links, and comparing with competitors to find new link acquisition opportunities.

## 💡 Real Examples (Simulated Outputs)

**Input:**
`run_full_seo_audit(target_url="https://www.tecno-mobile.in/camon-30-premier-5g", competitor_urls=["https://www.xiaomi.in/phone/redmi-note-13-pro-plus-5g", "https://www.samsung.com/in/smartphones/galaxy-a55/"])`

**Output (Example Audit Summary Snippet):**

---
**Summary SEO Audit Report for: https://www.tecno-mobile.in/camon-30-premier-5g**

**Overall Health Score:** 78/100 (Good, with areas for improvement)

**Key Findings & Recommendations:**

**1. Technical SEO:**
-   **Issue:** Some images lack proper `alt` attributes, impacting accessibility and image search SEO.
    -   **Recommendation:** Implement descriptive `alt` tags for all images, especially product shots and feature graphics. **Impact:** High, **Effort:** Low.
-   **Issue:** Mobile Page Speed (LCP) is moderately slow (3.5s) compared to competitors (Xiaomi: 2.8s, Samsung: 3.1s).
    -   **Recommendation:** Optimize image sizes and consider lazy loading for below-the-fold content. Minify CSS/JS. **Impact:** High, **Effort:** Medium.

**2. On-Page SEO:**
-   **Issue:** Meta Description on `/camon-30-premier-5g` is slightly truncated on SERP due to length.
    -   **Recommendation:** Shorten meta description to ~155 characters, ensuring primary keywords like "Camon 30 Premier 5G Camera" are included early. **Impact:** Medium, **Effort:** Low.
-   **Issue:** Content depth under "AI Vision Processor" section could be expanded to include more unique keywords.
    -   **Recommendation:** Add 200-300 words detailing the benefits and specific technologies of the AI Vision Processor, incorporating long-tail keywords. **Impact:** Medium, **Effort:** Medium.

**3. Backlink Analysis:**
-   **Finding:** Strong natural backlink growth from tech review sites. No apparent toxic links identified.
-   **Recommendation:** Focus on acquiring more diverse referring domains, specifically from photography blogs and niche tech forums where competitors have a stronger presence. **Impact:** High, **Effort:** High.

**4. Competitor Gap Analysis (vs. Xiaomi, Samsung):**
-   **Keyword Gap:** Competitors rank for more long-tail keywords related to "low light photography comparison" and "smartphone video recording features".
    -   **Recommendation:** Create dedicated blog content addressing these specific long-tail queries, linking back to the Camon 30 Premier 5G page. **Impact:** High, **Effort:** Medium.
-   **Content Gap:** Competitors feature more user-generated content examples or testimonials directly on product pages.
    -   **Recommendation:** Integrate customer sample photos or short video testimonials on the Tecno product page to enhance user trust and engagement. **Impact:** Medium, **Effort:** Medium.
---
