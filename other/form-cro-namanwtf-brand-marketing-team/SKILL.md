---
summary: "Optimize lead capture forms through A/B testing and best practices."
---

# Form CRO Skill

This skill focuses on optimizing lead capture forms to maximize conversion rates. It helps in designing, testing, and analyzing forms to improve their effectiveness.

## When to use this skill:
Use this skill when you need to:
- Optimize lead generation forms, contact forms, or survey forms.
- A/B test different form layouts, field types, or calls-to-action.
- Reduce form abandonment rates.
- Improve the quality and quantity of leads captured.
- Understand user interaction with form elements.

## Capabilities:
- **Form Analysis:** Identifies potential issues and friction points in existing forms.
- **A/B Testing Framework:** Provides tools to set up and manage A/B tests for form variations.
- **Field Optimization:** Suggests improvements for individual form fields (e.g., number of fields, field labels, input types).
- **Validation & Error Handling:** Helps in optimizing error messages and real-time validation to improve user experience.
- **Performance Tracking:** Monitors key metrics such as form completion rate, time to complete, and field-level interactions.

## Examples:

### Example 1: Analyze a specific lead capture form
```
/form-cro analyze --form-id="lead_gen_form_Q2"
```
This command analyzes the lead capture form with the specified ID, highlighting areas for improvement.

### Example 2: Suggest A/B tests for a call-to-action button
```
/form-cro recommend-ab-test --element="submit_button" --current-text="Submit" --proposals="Get a Free Quote;Download Now"
```
This command suggests A/B test variations for the submit button text.

### Example 3: Get completion rate for a form over a period
```
/form-cro get-metrics --form-id="contact_us_form" --metric="completion_rate" --timeframe="last_quarter"
```
This command retrieves the completion rate for the 'contact_us_form' over the last quarter.
