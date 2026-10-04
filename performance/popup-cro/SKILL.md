---
summary: "Optimize modal and overlay timing and content for maximum conversion."
---

# Popup CRO Skill

This skill focuses on optimizing the timing, content, and design of pop-ups, modals, and overlays to improve conversion rates without negatively impacting user experience.

## When to use this skill:
Use this skill when you need to:
- Optimize lead capture pop-ups, promotional modals, or exit-intent overlays.
- A/B test different pop-up triggers, delays, or display rules.
- Improve the conversion rate of pop-ups while minimizing user annoyance.
- Analyze the effectiveness of pop-up content, headlines, and calls-to-action.
- Understand user interaction and dismissal patterns with overlays.

## Capabilities:
- **Timing & Trigger Optimization:** Recommends optimal display timings (e.g., after X seconds, on scroll, on exit-intent) and triggers.
- **Content & Design A/B Testing:** Facilitates experimentation with different headlines, body copy, images, and layout variations for pop-ups.
- **Audience Segmentation:** Helps target specific user segments with tailored pop-up content based on behavior or demographics.
- **Performance Analytics:** Tracks key metrics such as impression rate, conversion rate, click-through rate, and dismissal rate for various pop-ups.
- **User Experience Assessment:** Identifies potential negative impacts on user experience and suggests improvements to maintain a good balance with conversion.

## Examples:

### Example 1: Analyze a specific pop-up's performance
```
/popup-cro analyze --popup-id="newsletter_signup_exit_intent"
```
This command analyzes the effectiveness of the specified exit-intent pop-up.

### Example 2: Suggest A/B tests for a pop-up's trigger timing
```
/popup-cro recommend-ab-test --element="trigger_timing" --current-setting="10_seconds_delay" --proposals="15_seconds_delay;on_scroll_50_percent;exit_intent"
```
This command suggests A/B test variations for the pop-up's display trigger.

### Example 3: Get conversion rate for all pop-ups on a page
```
/popup-cro get-metrics --page-url="https://example.com/pricing" --metric="conversion_rate" --timeframe="last_month"
```
This command retrieves the conversion rate for all pop-ups displayed on the pricing page over the last month.
