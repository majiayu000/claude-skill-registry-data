---
name: apply-prep
version: 1.0.0
description: >
  Live application prep for Heath Barnett. Given a role name or a job application URL,
  renders the real application form, reads every field including the bespoke custom
  questions, drafts each answer grounded in Heath's receipts and resume master, and
  returns a copy-paste breakdown plus the submit window in the hiring manager's timezone.
  Built for the hot window: Heath is at the keyboard, this gets him ready to paste and
  submit in minutes. Trigger on "prep [company/role]", "apply prep", "get me ready to
  apply to [company]", "prep my application for [role]", "extract the questions for
  [role]", "what does the [company] application ask", or Heath pasting an application URL
  with intent to apply. Never submits the form. Never fabricates. No em dashes.
license: MIT
compatibility: cowork claude-code hermes
---

# Apply Prep

Heath applies during his hot windows (mornings and evenings). This skill turns "I want to apply to X" into a copy-paste-ready breakdown of the actual form, with every answer drafted, in a few minutes. It runs live because Heath is present: it renders the real application and reads the real questions rather than guessing from a stored template.

## The one rule
Heath copies and submits. This skill NEVER types into the application, NEVER clicks Submit or any irreversible control, and NEVER uploads or sends on his behalf. It produces text for him to paste. It also never invents a number, a claim, or a credential. Every answer is grounded in his real corpus.

## Inputs it accepts
- A role name or company ("prep Superhuman", "prep the Alchemy Head of GTM").
- A direct application URL (Ashby, Greenhouse, Lever, Workable, BambooHR, Rippling, JazzHR, Workday, etc.).
- A LinkedIn job URL (resolve the real apply URL from it, see Step 2).

## Data sources (Heath's real corpus, never fabricate outside these)
- Resume master: `career/resume.json` in the Built GTM repo (name, contact, tailored titles, experience, competencies, education, awards).
- Receipts: `career/receipts.md` (the numbers and stories that ground answers).
- Per-role tailored materials, hiring manager, and recruiter: the Lab. In Hermes call the toolbox endpoint `POST https://builtgtm.ai/api/agents/tool` with `{"tool":"get_job","input":{"role_key":"Company|Job Title"}}`, or `{"tool":"apply_ready","input":{}}` to list roles ready to apply. In Cowork, read the role from the Job Engine (`storage.ats_tracking`) or `career/`.

## Steps

### 1. Identify the role
If given a name, match it to a tracked role (`apply_ready` or `list_jobs` / `get_job`). Pull its stored URL, hiring manager, recruiter, and tailored resume_json. If given only a URL, use it directly and still pull the tailored materials if the role is tracked.

### 2. Resolve the real application URL
Many stored URLs are LinkedIn job views, which are not the application form. Open the posting and follow the Apply button to the company ATS (Ashby, Greenhouse, etc.). If it is LinkedIn Easy Apply or you cannot reach a real form, say so and ask Heath to paste the direct application link.

### 3. Render the form and read every field
Open the application page in a browser (Claude in Chrome in Cowork; the Nous Portal cloud browser in Hermes). Read the rendered DOM, not a guess. Capture every field with: label, input type (text, textarea, select, radio/boolean, file), required flag, and the options for any dropdown or multiple choice. Separate them into:
- Universal fields (name, preferred name, email, phone, LinkedIn, location, resume upload, how-did-you-hear).
- Bespoke custom questions (essays, screeners, company-specific dropdowns).
- Voluntary EEO / demographic questions.

### 4. Fill the universal fields
From `resume.json`: First/Last/Full legal name, Preferred first name (Heath), email, phone, LinkedIn, Location (Dallas, TX, United States), How did you hear (LinkedIn unless the source says otherwise), Work authorization (Authorized to work in the US, no sponsorship required). Resume upload: note to attach the tailored PDF.

### 5. Answer the bespoke questions
- Essay prompts ("Why do you want to work here?", "Describe a time you...", "What interests you about this role?"): draft a grounded answer from `receipts.md` + the job description, in Heath's voice (plain declaratives, first-person, a real number or story, no "excited", no bow-tied ending, no em dashes). Keep to the length the form implies.
- Screeners: give a recommended value. Expected OTE or salary: anchor to the posting's range if shown, else his target. Years of experience: from the resume. Sponsorship: no. Willing to relocate / remote: per the role. Start date: flexible / standard notice unless he says otherwise.
- Company-specific dropdowns: recommend the best-fit option and say why in one line.

### 6. EEO / demographic questions
Present them as voluntary and Heath's personal choice. Do not fill protected attributes for him. Offer "I prefer not to answer" as a neutral default and move on.

### 7. Compute the submit window
Target 7-8am in the hiring manager's timezone. Convert to Heath's time in Dallas (CT): 6-7am for an ET hiring manager, 7-8am for CT, 8-9am for MT, 9-10am for PT. If the hiring manager's timezone is unknown, show the four-zone table and note most US tech HQs are Pacific. Name the hiring manager and recruiter if known, and remind Heath to send the outreach notes in the same window.

### 8. Output
Return a clean, ordered, copy-paste breakdown: the submit window first, then each form field as its own labeled block with the drafted value, in the order the form asks them. For work-history forms that take atomic fields, break each role into Company, Title, Location, Start, End, and Details. For a richer artifact, optionally write an HTML apply kit to `career/apply-kits/<company>-<role>.html` (mirror the existing Superhuman kit: brand tokens, per-field copy buttons, atomic work-history pills) and hand Heath the link.

Then stop. Heath reviews, pastes, submits, and marks the role Applied in the Job Engine.

## Outreach touches (produce all three per role)
Alongside the field breakdown, generate:
1. LinkedIn connection note (300 chars max): name the role in line one, one line of proof, one soft offer to send a 90-second video. No pitch, no "I'd love the opportunity".
2. Email: subject + body. Open on their situation, two receipts, the "I build the AI-native systems, I don't just ask for them" line, a line with the video link, one ask for 20 minutes.
3. Video: Heath records ONE reusable core walkthrough (how he builds, chaos to clarity, the Mixmax engine plus the Job Engine). Per role, draft only a fresh 10 to 15 second personalized intro (name, role, company, their angle) that he films and stitches on the front. Do not rewrite the whole video each time. Reusable core script lives at career/apply-kits/video-core-script.md.
Ground receipts in receipts.md. No em dashes. Never send; Heath sends. Send order: LinkedIn note with the request, email with the video link in the submit window, recruiter note last.

## Voice guardrails (for any drafted answer)
Plain declaratives. First person. One real number or story per point. Never "excited", never "passionate", never a bow-tied closing line. No em dashes anywhere. Never claim a title, employer, date, or metric that is not in `resume.json` or `receipts.md`.
