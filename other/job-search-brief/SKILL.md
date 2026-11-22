---
name: job-search-brief
description: Turn a CV, experience summary and stated preferences into an evidence-based job-search brief. Use when the user wants to choose target roles, focus a job hunt or revise search criteria; it does not perform a vacancy search.
---
# Job Search Brief

Build the brief in the conversation. Read an attached CV with the host's available attachment tools; when the user has no CV, use their experience summary. Do not require a document merely to start planning. Ask only for missing information that materially changes the search, together where practical.

Separate three things: facts the user supplied, role suggestions derived from that evidence, and unresolved preferences. Preserve the user's chosen direction even when proposing adjacent roles. Choose role level from demonstrated scope, responsibilities and relevant experience rather than a rigid years-to-title ladder. Never infer work authorization, nationality, protected characteristics or a salary floor from the CV.

Return a compact brief containing:

- Candidate strengths supported by CV lines or the user's statements.
- Primary and adjacent target titles with the evidence for each; label untested title suggestions.
- Stated geography, remote preferences, work-authorization or sponsorship constraints, salary floor/currency/period if supplied, and deal-breakers.
- Search keywords and exclusions that follow from those choices.
- Unknowns that would change the search, without presenting them as failed requirements.

Do not claim that a title has abundant current vacancies unless a live search established that. Do not invent employers, achievements, years of experience or target companies. If the user says to proceed without more questions, use labeled assumptions for ordinary search choices and leave sensitive/legal eligibility unknown.

If Scout is connected, translate the brief into two minimal objects. Search parameters are role titles, locations, workplace, recency and result/spending caps. Local ranking uses stated skills, target titles and logistics; newer contracts accept explicit `experience_years`, `target_seniority`, `remote_from_country` and `domains`. Scout v0.3 additionally accepts `is_student`, `degree_completed`, `graduation_year`, `fields_of_study`, `placement_year_available`, `completed_study_years` and `grade_classification`. Distinguish actual experience from desired role level and search location from the country the candidate will work remotely from. Leave unstated facts unset and inspect discovered schemas before using newer fields. Do not put CV text, names, email, phone, past employers or credentials into an Apify search request. No separate model API key is needed.

For student/intern searches, pass enrollment, degree completion, graduation year and subject only when the CV or user statements establish them. A future expected graduation year does not prove how many study years are completed, permit a placement year, establish a grade classification or rule out an earlier degree. Leave those facts unknown unless explicitly supported. Academic projects and competitions demonstrate skills and scope; they are not commercial employment at a sponsor or partner organization. A junior target may include internships when the stated target titles include them.

Show the brief and continue with the user's requested next action in the same chat. This skill does not authorize a paid search, application, message or background monitoring beyond the user's request. Never ask for an API token in conversation; initial secrets belong in the host's protected configuration.
