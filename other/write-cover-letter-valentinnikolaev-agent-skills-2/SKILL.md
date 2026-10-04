---
name: write-cover-letter
description: "Create, tailor, revise, or critique truthful cover letters, covering letters, motivation letters, and job-application letters from a job description plus verified candidate evidence. Use when Codex should analyze role requirements, map a resume, CV, portfolio, or brag document to them, research company-specific motivation, or produce an application-ready letter. Do not use for resume-only work, recommendation letters, or generic business correspondence."
---

# Write Cover Letter

Treat the letter as a targeted marketing document grounded in evidence, not as an autobiography.

## Protect truth and scope

- Support every candidate claim with a supplied resume, CV, portfolio, brag document, existing draft, or explicit user statement.
- Treat only explicitly pasted, attached, or named candidate materials as supplied evidence. Do not search neighboring files, guess which file belongs to the candidate, or reuse evidence from another application without explicit user direction.
- Never invent employers, titles, tenure, credentials, tools, metrics, leadership scope, product use, enthusiasm, or personal connections.
- Reuse the employer's terminology only when it accurately describes the candidate's experience. Do not turn a generic tool category into a named product without evidence.
- Treat preferred qualifications, degree preferences, and approximate years of experience as context rather than automatic disqualifiers. Surface hard eligibility constraints such as licensure, work authorization, clearance, mandatory language, or required location without minimizing or misrepresenting them.
- Protect confidential employer, client, and project information. Generalize sensitive details while preserving the verified impact.
- Return prose in chat by default. Create or edit a file only when the user asks for an artifact. Use the appropriate document or PDF workflow when the requested output format requires it.

## Choose the operation

- **Analyze**: Rank the job requirements and build a requirement-to-evidence map without drafting.
- **Draft**: Produce a new tailored letter. Use this by default when the job description and candidate evidence are available.
- **Tailor or revise**: Adapt an existing letter to a role while preserving the candidate's supported facts and recognizable voice.
- **Critique**: Identify weak targeting, unsupported claims, missing evidence, generic company motivation, and structural problems. Do not rewrite unless requested.
- **Template**: Produce a reusable letter with visible placeholders only when the user explicitly requests a generic template.

## Resolve the inputs

Require these inputs for a genuinely tailored letter:

1. The full job description or an accessible official posting.
2. Candidate evidence such as a resume, CV, brag document, portfolio, or structured facts supplied by the user.

Also capture the candidate's name, locale, preferred tone, word limit, existing draft, genuine company connection, and confirmed product use when provided. Infer the company and role from the posting when unambiguous.

If either required input is missing, ask for all missing essentials in one compact question. If the user wants progress without them, provide an outline or placeholder template and label every gap. Never fill a gap with a plausible-sounding claim. Match the language of the job posting unless the user requests another language.

## Build the evidence strategy

Read [references/cover-letter-workbench.md](references/cover-letter-workbench.md) before analyzing, drafting, tailoring, or critiquing a letter.

1. Separate core responsibilities, required qualifications, preferred or soft qualifications, and hard eligibility constraints.
2. Rank requirements by explicit business outcome, repetition, must-have wording, specificity, and placement. Give the first responsibilities extra attention without assuming order is absolute.
3. Map each important requirement to exact candidate evidence and its source. Mark the match as direct, transferable, or a gap.
4. Select the two strongest non-duplicative matches to high-priority responsibilities. Prefer verified results and concrete actions over broad claims.
5. Choose a natural story theme only when it clarifies the evidence. Do not force a theme or make the story more dramatic than the facts support.

Keep the full matrix internal unless the user asks for analysis, rationale, or a workbench view.

## Research company motivation

Research current company facts when the letter needs a company-specific motivation and the user has not prohibited browsing.

- Prefer the official job posting, About, mission, values, product, newsroom, investor-relations, and company-blog pages. Use a credible executive interview only when it adds a relevant fact unavailable from official pages.
- Select two concrete hooks: normally one mission or value and one product, industry, or current initiative. Put genuine product use first only when the candidate confirms it.
- Connect each company fact to a candidate-supplied goal, value, interest, or experience. Do not manufacture enthusiasm or claim that the candidate has followed or used the company without evidence.
- Record source links and access dates in research notes. Do not place citations inside the letter unless the user asks.
- If current research is unavailable, use only facts supplied by the user or posting and flag the limitation outside the letter.

## Draft the letter

Default to 300-450 words, one page, four to six short paragraphs, and plain ATS-friendly formatting unless the user or application form specifies otherwise.

1. Use a verified recipient name or `Dear Hiring Team`.
2. Open with one or two sentences stating who the candidate is, the target role, and a credible strength, goal, or belief. Add a company-specific detail when it reads naturally.
3. Transition with the strongest recent relevant achievement and a concise connection to the opportunity. Use numbers only when verified.
4. Write two complementary evidence paragraphs using: theme or proposition, context, specific action, outcome or learning, and relevance to the role.
5. Explain why this company by weaving together the researched hooks and the candidate's authentic connection to them.
6. Close with a concise statement of fit and interest, then the candidate's name.

Use specific verbs and evidence rather than jargon. Avoid unsupported superlatives, `perfect fit`, keyword stuffing, copied job-posting sentences, generic flattery, and a chronological replay of the resume. Do not include section labels in the finished letter unless requested.

## Validate before delivery

Run a final grounding pass:

1. Trace every candidate claim to supplied evidence.
2. Trace every company claim to a current source or the supplied posting.
3. Recheck names, role, company, dates, tenure, metrics, technologies, credentials, product use, and leadership scope.
4. Confirm that missing preferred qualifications are framed honestly and hard eligibility constraints are not concealed.
5. Remove confidential details, unsupported enthusiasm, stale company facts, repetition, and resume-like lists.
6. Check the requested language, tone, length, salutation, spelling, and plain-text readability.

If the user asks for fabricated credentials or impact, decline that alteration and offer the strongest truthful framing.

## Deliver the result

For a normal creation or tailoring request, return:

1. **Tailored cover letter**
2. **Confirm before sending** only when facts, placeholders, or eligibility details remain unresolved
3. **Research sources** only when external research was used

For analysis, show the prioritized evidence map and recommended story choices. For critique, lead with actionable findings and provide a revision only when requested. Do not expose hidden reasoning or include research notes in the letter itself.

## Method source

This workflow adapts the job-analysis, evidence-mapping, and narrative framework from [My Guide To Writing A Killer Cover Letter](https://www.reddit.com/r/datascience/comments/tag8l5/my_guide_to_writing_a_killer_cover_letter/). Paraphrase the method; do not copy its example language.
