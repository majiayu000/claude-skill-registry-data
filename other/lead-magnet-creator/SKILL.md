---
description: Builds ebooks, templates, calculators for lead capture.
---

# Lead Magnet Creator Skill

## Strategic Value

The Lead Magnet Creator automates the production of high-value content assets designed to capture prospect information and move them through the sales funnel. By leveraging AI to generate professionally formatted ebooks, interactive templates, and utility tools, this skill eliminates the bottleneck between strategy and execution—enabling rapid testing of multiple lead generation approaches.

## Capabilities

- **Ebook Generation:** Auto-generates professional ebooks from outlines or topics.
- **Template Creation:** Builds downloadable templates (spreadsheets, documents, designs).
- **Calculator/Tool Builder:** Creates interactive calculators and utilities.
- **Quality Assurance:** Reviews generated content for brand voice and value proposition.
- **Format Optimization:** Outputs in multiple formats (PDF, DOCX, interactive web).
- **A/B Testing Support:** Creates multiple variants for conversion optimization.

## Limitations

- Content quality depends on input prompt quality.
- May require manual review for complex technical topics.
- Brand-specific nuances may need human refinement.

## Examples

### Example 1: Ebook Creation

**User Prompt:** "Create a lead magnet ebook about 'The Complete Guide to Mobile Photography in 2026' for our smartphone brand."

**Generated Output:**
```json
{
  "asset_type": "ebook",
  "title": "The Complete Guide to Mobile Photography in 2026",
  "pages": 45,
  "chapters": [
    "Chapter 1: Camera Fundamentals on Modern Smartphones",
    "Chapter 2: Composition Techniques That Work",
    "Chapter 3: Editing Apps & Workflow Optimization",
    "Chapter 4: Social Media Optimization Strategies",
    "Chapter 5: Advanced Techniques for Professional Results"
  ],
  "formats": ["PDF", "EPUB", "Interactive Web"],
  "estimated_reading_time": "25 minutes",
  "cta_placement": "Chapter 5 - encourages product trial"
}
```

### Example 2: ROI Calculator

**User Prompt:** "Create a calculator that shows prospects the ROI of switching to our premium plan."

**Generated Output:**
```json
{
  "asset_type": "interactive_calculator",
  "title": "Premium Plan ROI Calculator",
  "inputs": [
    "Current monthly spending",
    "Team size",
    "Hours saved per week estimate",
    "Current tool limitations"
  ],
  "outputs": [
    "Annual cost savings",
    "Productivity gain value",
    "Break-even timeline",
    "3-year ROI projection"
  ],
  "shareable_results": true,
  "lead_capture_form": "collects email before showing results"
}
```

## Configuration (config.yaml)

```yaml
lead_magnet_types:
  ebook:
    min_pages: 20
    max_pages: 100
    output_formats: ["pdf", "epub", "html"]
  template:
    types: ["spreadsheet", "document", "checklist", "workflow"]
    output_formats: ["xlsx", "docx", "pdf"]
  calculator:
    input_limit: 10
    complexity: "medium"
    output: "web_embed"

branding:
  primary_color: "#1E90FF"
  secondary_color: "#FF4500"
  logo_path: "assets/logo.png"
  font_family: "Inter"
  compliance_note: "Include privacy policy link"

distribution:
  landing_page_template: "templates/lead_magnet_lp.html"
  email_sequence:
    - immediate: "Thank you + download link"
    - day_3: "Follow-up value content"
    - day_7: "Soft product pitch"
```
