---
name: faq-schema-generator
description: Generate FAQ sections with proper FAQPage schema markup for therapy pages. Creates 10-12 therapy-specific questions, 50-100 word answers, and valid JSON-LD schema. Optimized for Google rich snippets (health websites still eligible). Includes CRPO-compliant language and Ontario-specific content. Use when user says "add FAQ", "FAQ schema", "improve rich snippets", or when creating/updating therapy pages.
---

# FAQ Schema Generator

## Purpose
Generate high-quality FAQ sections with valid FAQPage schema markup that help therapy pages appear in Google's rich results while maintaining CRPO compliance.

## When to Use This Skill
- User says "add FAQ section" or "add FAQ"
- User mentions "FAQ schema" or "FAQPage"
- User wants to "improve rich snippets"
- Creating new therapy pages (FAQ is mandatory)
- Updating existing pages that lack FAQ sections

## Research Foundation

### 2024 FAQ Schema Status

**Important Update:**
As of August 2023, Google restricted FAQ rich results to well-known, authoritative websites in government and health sectors. This means:

✅ **Health websites (like therapy practices) ARE eligible** for FAQ rich results
✅ FAQPage schema still provides SEO value beyond rich snippets
✅ Other search engines (Bing, DuckDuckGo) may still display FAQ rich results
✅ Schema helps Google understand content structure

**Sources:**
- [Google FAQPage Documentation](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [FAQ Schema 2024 Guide](https://neilpatel.com/blog/faq-schema/)
- [FAQ Schema for Healthcare](https://www.epicnotion.com/blog/faq-schema-in-2025/)

---

## Quick Start Workflow

### Step 1: Gather Input

**Required from user:**
```
1. Page topic: [condition/service/location]
2. Target audience: [students/professionals/general]
3. Page URL or content
4. Any specific questions to include
```

**Request from user:**
```
Do you have:
- GSC data showing "People Also Ask" questions you rank for?
- Ahrefs questions report for your target keyword?
- Common client questions you receive?
```

### Step 2: Generate Questions

**Question Categories for Therapy Pages:**

| Category | # Questions | Purpose |
|----------|-------------|---------|
| **Treatment & Approach** | 2-3 | Explain therapy process |
| **Logistics & Scheduling** | 2-3 | Booking, availability, format |
| **Cost & Insurance** | 2 | Payment, receipts, coverage |
| **Credentials & Safety** | 1-2 | Build trust, CRPO registration |
| **Condition-Specific** | 2-3 | Address specific concerns |
| **First Session** | 1-2 | Reduce anxiety about starting |

**Total:** 10-12 questions per page

### Step 3: Write Answers

**Answer Guidelines:**

- **Length:** 50-100 words per answer (optimal for schema)
- **Format:** Direct answer first, then elaboration
- **Tone:** Empathetic, professional, accessible
- **CRPO Compliance:** Factual statements only, no guarantees

**Answer Structure:**
```
[Direct answer to question]. [Supporting detail or context].
[Practical information or next step if relevant].
```

### Step 4: Generate Schema Markup

**FAQPage Schema Template:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text here. Keep to 50-100 words for optimal display."
      }
    }
  ]
}
```

### Step 5: Validate Schema

**Before deployment:**
1. Validate syntax at [Google Rich Results Test](https://search.google.com/test/rich-results)
2. Check all questions match visible page content
3. Verify no duplicate FAQ schema on site for same questions

---

## Question Templates by Page Type

### Anxiety Therapy Pages

```markdown
## Frequently Asked Questions About Anxiety Therapy

### What is anxiety therapy?
Anxiety therapy is a form of psychotherapy that helps you understand
and manage anxiety symptoms. Working with a registered psychotherapist,
you'll learn evidence-based techniques like Acceptance and Commitment
Therapy (ACT) to reduce anxiety's impact on your daily life.

### How long does anxiety therapy take?
The duration varies based on individual needs, but many clients begin
noticing improvements within 6-12 sessions. Some people benefit from
short-term focused work, while others prefer longer-term support.
We'll discuss your goals and progress regularly.

### Can anxiety be treated without medication?
Yes, psychotherapy is an effective treatment for anxiety without
medication. Many clients find relief through therapy alone, while
others combine therapy with medication prescribed by their doctor.
As a psychotherapist, I provide therapy; medication is managed by
your physician.

### How much does anxiety therapy cost in Ontario?
Session fees vary by practitioner. NextStep Therapy provides insurance
receipts that you can submit to your extended health benefits for
reimbursement. Many insurance plans cover registered psychotherapist
services. Contact your provider to confirm coverage.

### Is virtual therapy effective for anxiety?
Research shows virtual therapy is as effective as in-person therapy
for anxiety treatment. Virtual sessions offer convenience, privacy,
and accessibility, especially for those with anxiety about traveling
or busy schedules. All sessions are conducted through secure, encrypted
video platforms.

### What happens in the first anxiety therapy session?
Your first session focuses on understanding your experience with
anxiety and what you hope to achieve. We'll discuss your history,
current symptoms, and goals. This is also a chance to ask questions
and ensure we're a good fit. There's no pressure to share more than
you're comfortable with.

### How do I know if I need therapy for anxiety?
Consider therapy if anxiety interferes with work, relationships, or
daily activities, if you experience persistent worry, physical symptoms
like racing heart, or if you're avoiding situations due to fear.
Even if you're unsure, a consultation can help clarify whether therapy
would benefit you.

### What is ACT therapy for anxiety?
Acceptance and Commitment Therapy (ACT) is an evidence-based approach
that helps you accept difficult thoughts and feelings rather than
fighting them, while committing to actions aligned with your values.
It's particularly effective for anxiety because it reduces the struggle
that often intensifies anxious feelings.

### Can I do anxiety therapy online in Ontario?
Yes, licensed psychotherapists in Ontario can provide therapy virtually
to clients anywhere in the province. NextStep Therapy offers same-week
virtual appointments with flexible evening and weekend scheduling.
You'll need a private space and reliable internet connection.

### What credentials should an anxiety therapist have?
In Ontario, look for a Registered Psychotherapist (RP) licensed by
the College of Registered Psychotherapists of Ontario (CRPO). This
ensures your therapist has met education, training, and ethical
standards. You can verify registration at crpo.ca. I am registered
as RP #10979.
```

### Location Pages (City-Specific)

```markdown
## FAQs About Therapy in [City]

### Is there virtual therapy available for [City] residents?
Yes, NextStep Therapy provides virtual psychotherapy services to
residents throughout [City] and all of Ontario. Virtual sessions
offer the same quality care as in-person therapy, with added
convenience of accessing support from home.

### How do I find a therapist in [City]?
You can search the CRPO register (crpo.ca) for registered
psychotherapists serving [City]. NextStep Therapy offers virtual
services to [City] residents with same-week appointments and
flexible scheduling options including evenings and weekends.

### What mental health services are available in [City]?
[City] residents have access to various mental health services
including psychotherapy, counseling, psychiatry, and community
mental health programs. For private psychotherapy, registered
psychotherapists like those at NextStep Therapy offer evidence-based
treatment for anxiety, depression, and other concerns.

### Is therapy covered by OHIP in [City]?
Psychotherapy provided by registered psychotherapists is not covered
by OHIP. However, many employer benefit plans cover psychotherapy
services. NextStep Therapy provides insurance receipts that you can
submit to your extended health benefits for reimbursement.

### Can I see a therapist virtually from [City]?
Yes, Ontario-licensed psychotherapists can provide virtual therapy
to clients anywhere in the province. This means [City] residents
can access specialized services without geographic limitations.
Virtual sessions are conducted through secure, encrypted video
platforms.
```

### Student Pages

```markdown
## FAQs for University Students Seeking Therapy

### Is therapy confidential for university students?
Yes, therapy with a private practitioner like NextStep Therapy is
completely confidential and separate from your university. Your
sessions are protected by professional confidentiality standards,
and nothing is shared with your school without your written consent.

### How do I pay for therapy as a student?
Many university student health plans cover psychotherapy services.
Check your student association benefits or contact your school's
health services office. NextStep Therapy provides insurance receipts
for reimbursement from student plans.

### Can I do therapy around my class schedule?
Yes, NextStep Therapy offers flexible scheduling including evening
and weekend appointments that work around classes and study schedules.
Virtual sessions mean you can access therapy from your dorm, apartment,
or anywhere with privacy.

### What if I'm in crisis and need immediate help?
If you're in crisis, contact your university's crisis services,
call 911, or go to your nearest emergency room. Therapy is best
suited for ongoing support rather than emergency situations.
Resources like Good2Talk (1-866-925-5454) provide 24/7 support for
Ontario students.

### Is it normal to need therapy in university?
Absolutely. University presents unique stressors including academic
pressure, transitions, relationship changes, and identity development.
Seeking therapy is a sign of self-awareness and proactive mental
health care, not weakness.
```

---

## CRPO Compliance for FAQs

### Allowed in Answers:
✅ Factual information about therapy process
✅ General timeframes ("many clients notice improvement in 6-12 sessions")
✅ Descriptions of therapeutic approaches
✅ Insurance and payment information
✅ Credential information (RP, CRPO #10979)
✅ References to evidence-based practices

### Prohibited in Answers:
❌ "Therapy will cure your [condition]"
❌ "Most clients see results in X weeks" (without research citation)
❌ "Best therapist in Ontario"
❌ "Guaranteed improvement"
❌ Any testimonial language
❌ Success rates without citation

### Safe Language Patterns:

| Instead of... | Use... |
|---------------|--------|
| "Therapy will help you" | "Therapy can help with..." |
| "You will feel better" | "Many people find relief through..." |
| "I guarantee results" | "Evidence shows that..." |
| "The best approach" | "An evidence-based approach" |
| "Cure your anxiety" | "Manage anxiety symptoms" |

---

## Schema Validation

### Common Errors to Avoid:

1. **Duplicate FAQ schema** - Only one FAQPage per page
2. **Hidden content** - Questions must be visible on page
3. **Mismatched content** - Schema must match visible FAQ
4. **Advertising in answers** - Avoid promotional language
5. **Syntax errors** - Validate JSON before deployment

### Validation Steps:

```
1. Copy JSON-LD schema
2. Go to: https://search.google.com/test/rich-results
3. Paste schema in "Code" tab
4. Run test
5. Fix any errors before deploying
```

---

## Complete Schema Example

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is anxiety therapy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Anxiety therapy is a form of psychotherapy that helps you understand and manage anxiety symptoms. Working with a registered psychotherapist, you'll learn evidence-based techniques like Acceptance and Commitment Therapy (ACT) to reduce anxiety's impact on your daily life."
      }
    },
    {
      "@type": "Question",
      "name": "How long does anxiety therapy take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The duration varies based on individual needs, but many clients begin noticing improvements within 6-12 sessions. Some people benefit from short-term focused work, while others prefer longer-term support. We'll discuss your goals and progress regularly."
      }
    },
    {
      "@type": "Question",
      "name": "Is virtual therapy effective for anxiety?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Research shows virtual therapy is as effective as in-person therapy for anxiety treatment. Virtual sessions offer convenience, privacy, and accessibility, especially for those with anxiety about traveling or busy schedules. All sessions are conducted through secure, encrypted video platforms."
      }
    },
    {
      "@type": "Question",
      "name": "How much does therapy cost in Ontario?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Session fees vary by practitioner. NextStep Therapy provides insurance receipts that you can submit to your extended health benefits for reimbursement. Many insurance plans cover registered psychotherapist services. Contact your provider to confirm coverage."
      }
    },
    {
      "@type": "Question",
      "name": "What credentials should a therapist have in Ontario?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "In Ontario, look for a Registered Psychotherapist (RP) licensed by the College of Registered Psychotherapists of Ontario (CRPO). This ensures your therapist has met education, training, and ethical standards. You can verify registration at crpo.ca."
      }
    },
    {
      "@type": "Question",
      "name": "What happens in the first therapy session?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Your first session focuses on understanding your experience and what you hope to achieve. We'll discuss your history, current concerns, and goals. This is also a chance to ask questions and ensure we're a good fit. There's no pressure to share more than you're comfortable with."
      }
    },
    {
      "@type": "Question",
      "name": "Is therapy covered by OHIP?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Psychotherapy provided by registered psychotherapists is not covered by OHIP. However, many employer benefit plans cover psychotherapy services. NextStep Therapy provides insurance receipts that you can submit to your extended health benefits for reimbursement."
      }
    },
    {
      "@type": "Question",
      "name": "Can I do therapy online in Ontario?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, licensed psychotherapists in Ontario can provide therapy virtually to clients anywhere in the province. NextStep Therapy offers same-week virtual appointments with flexible evening and weekend scheduling. You'll need a private space and reliable internet connection."
      }
    },
    {
      "@type": "Question",
      "name": "How do I know if I need therapy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Consider therapy if concerns interfere with work, relationships, or daily activities, if you experience persistent distress, or if you're avoiding situations due to anxiety or fear. Even if you're unsure, a consultation can help clarify whether therapy would benefit you."
      }
    },
    {
      "@type": "Question",
      "name": "What is ACT therapy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Acceptance and Commitment Therapy (ACT) is an evidence-based approach that helps you accept difficult thoughts and feelings rather than fighting them, while committing to actions aligned with your values. It's particularly effective for anxiety, depression, and stress-related concerns."
      }
    }
  ]
}
```

---

## Integration Checklist

### Before Adding FAQ to Page:

- [ ] 10-12 questions generated
- [ ] All answers 50-100 words
- [ ] CRPO compliance verified
- [ ] Schema syntax validated
- [ ] Questions visible on page (not hidden)
- [ ] No duplicate FAQ schema on site for same questions
- [ ] Questions match search intent for page
- [ ] Condition-specific questions included
- [ ] Logistics questions included (cost, scheduling)
- [ ] Local/Ontario context included

---

## Sources

**Schema Documentation:**
- [Google FAQPage Structured Data](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Schema.org FAQPage](https://schema.org/FAQPage)

**Best Practices:**
- [FAQ Schema Guide (Neil Patel)](https://neilpatel.com/blog/faq-schema/)
- [FAQ Schema 2025 Value](https://www.epicnotion.com/blog/faq-schema-in-2025/)
- [FAQ Schema Generators Compared](https://nestify.io/blog/top-faq-schema-generators/)

**CRPO Compliance:**
- [CRPO Advertising Standards](https://crpo.ca/practice-standards/business-practices/advertising/)
