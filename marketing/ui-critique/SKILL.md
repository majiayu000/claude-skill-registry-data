---
name: ui-critique
description: Use when structured UI review — visual hierarchy, consistency, accessibility,
  and actionable improvement feedback. Use when working with ui critique.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- critique
- digital-content
- media
version: 1.0.0
category: content
---




## Overview

Structured framework for reviewing UI designs. Evaluates visual hierarchy, consistency, accessibility, spacing, typography, color usage, and provides actionable improvement recommendations.

## Capabilities

- Analyze visual hierarchy and information architecture
- Check consistency across components and pages
- Evaluate accessibility (contrast, focus states, semantic HTML)
- Review responsive behavior across breakpoints
- Provide specific, actionable improvement recommendations

## When to Use
**Trigger phrases:**
- "ui critique"
- "Structured UI review — visual hierarchy, consistency, accessibility, and actiona"


- Before launching a new UI or redesign
- Onboarding a new team member to design standards
- User complaints about usability or confusion
- Pre-launch design review checklist

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The ui-critique workflow follows a standard pipeline pattern.

Core flow:
```
# ui-critique primary flow
input = prepare(raw_data)
result = process(input, config={accessibility, actionable, consistency, critique, feedback})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# ui-critique primary flow
input = prepare(raw_data)
result = process(input, config={accessibility, actionable, consistency, critique, feedback})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Critique Framework
```python
def critique_ui(screenshot, url):
    checks = {
        "visual_hierarchy": check_hierarchy(screenshot),  # Can user find CTA in 3s?
        "consistency": check_spacing_and_colors(screenshot),  # Same patterns everywhere?
        "contrast": check_color_contrast(screenshot),  # WCAG AA compliant?
        "responsive": check_mobile_view(url),  # Works on 320px?
        "loading": check_performance(url),  # LCP < 2.5s?
        "accessibility": check_aria_and_semantics(url)  # Screen reader friendly?
    }
    return generate_report(checks)
```

## Common Patterns

- **3-second test**: Can user identify the primary action in 3 seconds?
- **Squint test**: Blur the UI — does the hierarchy still work?
- **Contrast check**: All text meets WCAG AA (4.5:1 for normal text)
- **Spacing audit**: Consistent spacing between similar elements

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |