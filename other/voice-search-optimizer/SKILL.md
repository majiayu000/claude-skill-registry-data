---
name: "Voice Search Optimizer"
description: "Alexa/Siri/voice SEO optimization"
author: "@namanwtf"
version: 3.0.0
---

# Voice Search Optimizer

## When to Use

Use this skill when you need to optimize your brand's content and online presence for voice search platforms like Alexa, Siri, Google Assistant, and other voice-activated devices. This is crucial for improving visibility in spoken queries, capturing zero-click answers, and engaging with customers through a conversational interface. Deploy this skill for:

-   **SEO Strategy:** Integrating voice search optimization into your overall SEO strategy.
-   **Content Creation:** Developing content that is structured to answer common voice queries directly and concisely.
-   **Local SEO:** Enhancing local business listings for "near me" voice searches.
-   **FAQ Development:** Creating comprehensive FAQ sections tailored to spoken questions.
-   **Product Discovery:** Optimizing product descriptions and features for voice-activated shopping.
-   **Brand Presence:** Ensuring your brand consistently appears in relevant voice search results.

## Capabilities

The Voice Search Optimizer skill provides the following capabilities:

-   **Keyword Analysis for Voice:** Identifies long-tail keywords, natural language phrases, and question-based queries frequently used in voice search.
-   **Conversational Content Structuring:** Guides content creation to be more conversational, direct, and answer-focused for voice assistants.
-   **Featured Snippet Optimization:** Highlights opportunities to rank for featured snippets (Position Zero) which are often read aloud by voice assistants.
-   **Local Business Optimization:** Audits and suggests improvements for Google My Business listings and other local directories to capture "near me" voice searches.
-   **Schema Markup Generation:** Helps generate appropriate schema markup (e.g., FAQPage, LocalBusiness) to provide structured data for voice assistants.
-   **Question Formulation Analysis:** Analyzes current content for how well it answers direct questions and suggests rephrasing for better voice compatibility.
-   **Competitive Voice Search Analysis:** Provides insights into how competitors are performing in voice search and identifies gaps.

## Usage Examples

### Example 1: Analyze a webpage for voice search potential

```python
voice.analyze_page(url="https://www.example.com/blog/voice-seo-guide")
```

### Example 2: Generate optimal schema markup for an FAQ page

```python
voice.generate_schema_markup(page_type="FAQPage", content="{'question1': 'answer1', 'question2': 'answer2'}")
```

### Example 3: Identify long-tail voice keywords for a product category

```python
voice.suggest_voice_keywords(product_category="smart home devices", target_audience="tech enthusiasts")
```

### Example 4: Audit a local business listing for voice search readiness

```python
voice.audit_local_listing(business_name="Acme Coffee Shop", location="New York, NY")
```

## Configuration

The Voice Search Optimizer skill can be configured with the following parameters:

-   **`default_language`**: (String, optional) Sets the default language for keyword analysis and content suggestions (e.g., "en-US", "en-GB", "hi-IN"). Default is "en-US".
-   **`api_key_google_knowledge_graph`**: (String, optional) API key for accessing Google Knowledge Graph for enhanced entity recognition and context.
-   **`api_key_serpapi`**: (String, optional) SERP API key for more comprehensive voice search result analysis.
-   **`enable_realtime_serp_check`**: (Boolean, optional) If true, performs real-time SERP checks during analysis (can increase latency and API usage). Default is false.

Example configuration in your `config.yaml`:

```yaml
voice_search_optimizer:
    default_language: "en-US"
    api_key_google_knowledge_graph: "YOUR_GOOGLE_KNOWLEDGE_GRAPH_API_KEY"
    api_key_serpapi: "YOUR_SERPM_API_KEY"
    enable_realtime_serp_check: false
```
