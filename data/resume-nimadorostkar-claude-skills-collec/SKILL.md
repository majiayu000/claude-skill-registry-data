---
name: resume
description: Use when writing or tailoring a CV or resume. Covers evidence over adjectives, tailoring to a specific role without lying, structure, and the specific patterns that get a resume discarded.
metadata:
  category: business
  version: 1.0.0
  tags: [resume, cv, career, tailoring, writing]
---

# Resume

## Purpose

Write a resume that survives a six-second scan and a hiring manager's skepticism. Most resumes fail on the same thing: they list responsibilities rather than demonstrating outcomes.

## When to Use

- Writing or rewriting a resume.
- Tailoring a resume to a specific role.
- A resume that generates no responses.
- Reviewing someone else's resume.

## Capabilities

- Structure and prioritization.
- Turning responsibilities into evidence.
- Tailoring without dishonesty.
- Handling gaps, career changes, and short tenures.
- Applicant-tracking-system considerations.

## Inputs

- The person's actual experience, in detail.
- The specific role, and its posting.
- What is genuinely relevant to it.

## Outputs

- A resume where each bullet is evidence.
- A version tailored to the role, drawing on real experience.
- No adjectives doing the work that numbers should do.

## Workflow

1. **Extract the outcomes** — For each role: what changed because you were there? Not what you were responsible for. What was different afterwards.
2. **Quantify** — Numbers survive a six-second scan; adjectives do not. If a number is not available, use a comparison, a scale, or a before-and-after.
3. **Lead with the strongest evidence** — The top third of the first page is nearly all that is read on the first pass. Put the best thing there.
4. **Tailor to the posting, honestly** — Reorder, re-emphasize, and use the posting's vocabulary where it genuinely describes what you did. Never invent.
5. **Cut everything irrelevant** — A resume is an argument for one role, not a complete autobiography.
6. **Check it survives a keyword scan** — Most applications pass through automated filtering. If the posting says "Kubernetes" and your resume says "container orchestration", you may be filtered out for a skill you have.

## Best Practices

- "Responsible for the deployment pipeline" says nothing. "Cut deploy time from 45 to 6 minutes; deploy frequency tripled" says everything. The first describes a job description; the second describes a person.
- Adjectives are what you write when you do not have evidence. "Highly motivated", "results-driven", "passionate" — cut all of them, always. They are free to write, so they carry no information.
- Numbers do not have to be impressive to be useful. "Reduced the on-call page volume from ~30 to ~8 per week" is a small number and a compelling one.
- Tailoring is reordering and re-emphasizing what is true. It is not inventing. The interview will find the invention.
- Two pages maximum, and one page for under ten years of experience. Length is not evidence of substance.
- If a hiring manager can substitute anyone else's name at the top and the resume still reads correctly, it is not a resume — it is a job description.

## Examples

**The single most important transformation:**

```text
BEFORE — a job description. Anyone in the role could have written this.

  Senior Software Engineer, Acme Corp (2022-2026)
  - Responsible for backend services and API development
  - Worked with cross-functional teams to deliver features
  - Participated in code reviews and mentored junior developers
  - Utilized Python, PostgreSQL, and AWS in a microservices architecture

AFTER — evidence. Only this person could have written this.

  Senior Software Engineer, Acme Corp (2022-2026)
  - Cut checkout p99 latency from 3.2s to 340ms by replacing an N+1 query
    pattern in the pricing service. Checkout abandonment fell 4 points.
  - Led the migration of 12 services off a shared database, eliminating the
    incident class that caused 3 of the year's 6 SEV-1s.
  - Built the deploy gate that made integration tests mandatory. Production
    incidents caused by deploys fell from ~2/month to 0 over 8 months.
  - Mentored 3 engineers; 2 promoted to senior within 18 months.

  Python, PostgreSQL, AWS (ECS, RDS, SQS), Terraform
```

Same job. The first version could describe ten thousand people. The second describes one, and every line is checkable.

**Tailoring honestly:**

```text
The posting emphasizes: reliability, incident response, Kubernetes.

The candidate has all three, but their resume leads with feature work, because
that is what they spent the most time on.

Tailor by reordering — not by inventing:
  - Move the incident-reduction bullet to the top of the most recent role.
  - Move the database migration bullet (which eliminated an incident class)
    to second.
  - The feature work moves down. It is still true, still there, and no longer
    the first thing read.
  - The posting says "Kubernetes"; the resume said "container orchestration".
    The candidate used Kubernetes. Say "Kubernetes" — an automated filter does
    not do synonyms.

Nothing was invented. The same experience is presented in the order that
answers the question the reader is actually asking.
```

## Notes

- The six-second scan is real, and it lands on the top third of page one. Whatever is there is your resume; the rest is read only if that part worked.
- Automated keyword filtering is imperfect and literal. Using the posting's exact terminology for skills you genuinely have is not gaming the system; it is not being filtered out for a synonym.
- If a bullet does not contain a number, a scale, or a specific outcome, ask what it is doing there. Usually the answer is that it is padding a role that had one real achievement, and it would be stronger alone.
