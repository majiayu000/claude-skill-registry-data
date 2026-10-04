---
name: "Case Study Generator"
description: "Auto-create customer success stories"
author: "@namanwtf"
version: 3.0.0
---

# Case Study Generator

## When to Use

Utilize this skill to rapidly generate compelling customer success stories and case studies. This is invaluable when you need to:

-   **Showcase Success:** Highlight customer achievements and the value your product/service delivers.
-   **Accelerate Sales:** Provide sales teams with powerful evidence of ROI and impact.
-   **Streamline Content Creation:** Automate the writing process for marketing materials.
-   **Build Thought Leadership:** Establish your brand as an expert in your industry.
-   **Support Marketing Campaigns:** Integrate success stories into various marketing channels like websites, social media, and email campaigns.
-   **Pitch Investors/Partners:** Present clear, data-driven narratives of positive outcomes.

## Capabilities

The Case Study Generator skill provides the following capabilities:

-   **Automated Content Drafting:** Generates initial drafts of case studies based on provided data points and templates.
-   **Data Integration:** Pulls relevant customer data, metrics, and testimonials from integrated CRMs or data sources.
-   **Problem-Solution-Impact Framework:** Structures case studies using a proven narrative arc: Customer's Challenge, Your Solution, Achieved Results, and Future Outlook.
-   **Customizable Templates:** Offers a variety of templates for different industries, use cases, and content lengths.
-   **Tone & Style Adjustment:** Allows for customization of the case study's tone (e.g., formal, innovative, empathetic) and writing style.
-   **SEO Optimization:** Suggests keywords and phrasing to improve the case study's search engine visibility.
-   **Call-to-Action (CTA) Generation:** Crafts effective CTAs tailored to the case study's objective.
-   **Multi-format Output:** Generates content in various formats suitable for web, PDF, or presentation slides.

## Usage Examples

### Example 1: Generate a B2B case study about a software implementation

```python
case_study.generate(
    customer_name="Global Innovations Inc.",
    industry="Software & Tech",
    challenge="Inefficient data processing",
    solution="Implemented AI-powered automation platform",
    results=["Reduced processing time by 40%", "Improved data accuracy by 99%", "Saved $50,000 annually"],
    testimonial="Their platform transformed our operations!",
    template="B2B_software_template",
    tone="professional"
)
```

### Example 2: Create a concise success story for a marketing campaign

```python
case_study.generate_short_story(
    customer_name="Local Bakery",
    product_service="Social Media Marketing",
    outcome="Increased online orders by 150% in 3 months",
    quote="Our cakes are flying off the digital shelves!",
    cta="Learn how to bake up your own success with our marketing"
)
```

### Example 3: Revise an existing case study for a different audience

```python
case_study.revise(
    case_study_id="cs_001",
    target_audience="small business owners",
    focus_metrics=["cost savings", "ease of use"]
)
```

## Configuration

The Case Study Generator skill can be configured with the following parameters:

-   **`default_template`**: (String, optional) Sets the default template to use for case study generation. Default is "standard_template".
-   **`default_tone`**: (String, optional) Defines the default tone for generated content (e.g., "professional", "conversational", "empathetic"). Default is "professional".
-   **`crm_integration_enabled`**: (Boolean, optional) If true, enables integration with CRM systems (e.g., Salesforce, HubSpot) to pull customer data. Default is false.
-   **`data_sources`**: (List of Strings, optional) Specifies additional data sources for metrics and testimonials (e.g., ["Google Analytics", "SurveyMonkey"]).
-   **`seo_keyword_suggestions_enabled`**: (Boolean, optional) If true, includes SEO keyword suggestions in the generated drafts. Default is true.

Example configuration in your `config.yaml`:

```yaml
case_study_generator:
    default_template: "B2B_software_template"
    default_tone: "innovative"
    crm_integration_enabled: true
    data_sources:
        - "Salesforce"
        - "Zendesk"
    seo_keyword_suggestions_enabled: true
```
