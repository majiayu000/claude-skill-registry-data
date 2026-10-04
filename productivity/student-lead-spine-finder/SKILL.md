---
name: student-lead-spine-finder
description: Find a professor or lab's recent student-led publication spine from public evidence. Use when Codex needs a bounded subtask to identify recurring first-author, student-like, or non-corresponding-author leads in the latest 3-4 years; infer likely senior PhD/lab main student candidates; verify each candidate's direction through Google Scholar/OpenAlex/Semantic Scholar/homepage/public search; and return candidate names, directions, confidence, caveats, and source evidence for a parent professor-direction-mapper run.
---

# Student Lead Spine Finder

Find the recent student-led execution spine of a professor or lab. This skill is designed to run as an independent delegated task, often in a subagent, and return a compact evidence packet to the parent `professor-direction-mapper`.

It does not decide the professor's final mainline. It identifies candidate student leads and their directions so the parent call can use them as cross-check evidence.

## Inputs

Required:

- Professor or PI name.
- At least one public source: personal homepage, lab page, HKUST(GZ) profile, publication list, Google Scholar/OpenAlex/Semantic Scholar/DBLP profile, or a paper list.

Optional:

- Institution and lab name.
- Field or venue family.
- Target time window. Default: latest 3-4 complete years plus current year.
- Known students, alumni pages, group member pages, or candidate papers.

## Workflow

1. Establish identity and scope.
   - Confirm the professor/PI identity and institution.
   - Record the time window used.
   - Flag common-name ambiguity before inferring people.

2. Collect recent group papers.
   - Prefer official publication pages, lab pages, DBLP/OpenAlex/Semantic Scholar/Google Scholar profile exports, official proceedings, and paper pages.
   - Use AnySearch or available web search for missing pages.
   - Keep only papers plausibly connected to the professor/PI.
   - Do not include private notes, emails, or unpublished user material in search queries.

3. Extract author-role evidence.
   - For each paper, record title, year, venue, authors, first author, corresponding/senior author signal when visible, and source URL.
   - Treat first-author recurrence as a signal of execution leadership only in fields where author order is meaningful.
   - Treat non-corresponding repeated authors near the front of the author list as possible student/postdoc contributors, not confirmed students.
   - Use lab member pages, student pages, CVs, LinkedIn-like public pages, thesis pages, or institutional pages to confirm student status when possible.

4. Rank candidate student leads.
   - Count latest-window papers per recurring first author or student-like lead.
   - Cluster each candidate's papers by direction/topic.
   - Prefer candidates with repeated first-author papers connected to the professor, clear lab/student affiliation, and coherent direction.
   - Do not call someone a student unless public evidence supports it. Use "candidate lead" or "student-like lead" otherwise.

5. Verify candidate direction externally.
   - Search each top candidate by name plus Google Scholar/profile/publication keywords.
   - Use Google Scholar only as public search/profile evidence when accessible; if blocked or unavailable, use OpenAlex, Semantic Scholar, DBLP, personal homepage, or institutional pages.
   - Record the candidate's apparent direction from their own profile/publications, not only from the professor's page.

6. Return a compact packet to the parent call.
   - Use `references/output-template.md`; do not improvise a different packet shape.
   - Include at most 5 candidates and at most 5 evidence papers per candidate.
   - Include a source coverage statement: searched sources, inaccessible sources, and whether the corpus is complete or sampled.
   - Explicitly state whether the student-led evidence supports, contradicts, or is insufficient for the parent's tentative current-mainline hypothesis.

## Output Rules

Always separate:

- Confirmed facts: direct source evidence.
- Inferences: likely student lead, likely direction, likely relation to professor.
- Caveats: author-order conventions, common names, inaccessible profiles, equal contribution, unclear student status.

The final answer must be easy for a parent agent to paste into a direction map:

- Candidate name.
- Candidate role confidence.
- Direction label.
- Evidence papers.
- External profile/search confirmation.
- Support/contradiction relative to the professor's current-mainline hypothesis.

## Confidence Rubric

Candidate role confidence:

- High: public lab/student/homepage/CV/institutional page confirms the candidate is or was a student/PhD/RA/postdoc in the professor's group, and at least 2 latest-window papers connect the candidate to the professor.
- Medium: repeated first-author or front-author papers connect the candidate to the professor, but public role confirmation is incomplete.
- Low: only one connected paper, common-name ambiguity, unclear affiliation, or author-order conventions weaken the inference.

Direction confidence:

- High: at least 2 latest-window papers plus an external profile/search result point to the same direction.
- Medium: at least 1 latest-window paper plus profile/search evidence, or multiple papers but no external profile confirmation.
- Low: direction inferred only from title keywords, one paper, or weak search snippets.

Relation-to-PI confidence:

- High: lab page/profile/paper metadata clearly connects the candidate to the professor's group.
- Medium: repeated coauthorship with the professor in the latest window, but no explicit group membership source.
- Low: one coauthored paper or ambiguous coauthor identity.

## Parent Hypothesis Rules

Use these labels relative to the parent `professor-direction-mapper` tentative current-mainline hypothesis:

- Supports: the strongest candidate direction matches the hypothesis and has at least medium role confidence, medium direction confidence, and 2 or more latest-window connected papers.
- Contradicts or weakens: the strongest candidate direction clearly differs from the hypothesis, has at least medium confidence, and the hypothesized direction has little or no latest-window student-led evidence.
- Insufficient: evidence is sparse, candidate identity is ambiguous, student status is unconfirmed, authorship order is not meaningful for the field, or no candidate reaches medium confidence.

Never claim that the student-led evidence proves the lab mainline. Say it supports, weakens, or is insufficient as a cross-check.

## Subagent Use

When this skill is invoked by `professor-direction-mapper`, it should be run in a separate subagent if subagent tools are available.

Suggested delegated prompt:

```text
Use $student-lead-spine-finder at C:\Users\Administrator\.codex\skills\student-lead-spine-finder to find the recent student-led publication spine for <professor/lab>. Use only public evidence. Focus on the latest 3-4 years, recurring first authors or student-like non-corresponding leads, and verify top candidate directions through Google Scholar/OpenAlex/Semantic Scholar/personal pages. Return candidate names, directions, evidence papers, confidence, caveats, and whether this supports or contradicts the tentative current-mainline hypothesis: <hypothesis or unknown>.
```

If subagent tools are unavailable, report that the ideal delegated lane is unavailable and either ask whether to run the skill inline or proceed without the student-led cross-check. Do not silently fold a large student-lead investigation into the parent direction-mapping task.

## Guardrails

- Do not identify a "senior PhD", "main student", or "lab lead" from author order alone.
- Do not write "X is the main student" unless public role evidence supports it; prefer "candidate student-like lead" or "likely student-led spine".
- Do not equate one prolific student with the entire lab's mainline.
- Do not overrule current homepage/recruiting/project evidence using student-lead evidence alone.
- Do not use Google Scholar scraping as canonical evidence; use it as one public signal and cross-check with open sources.
- Do not bypass CAPTCHA, login, or paywall barriers.
- Do not search private user notes or unpublished material.
- Do not hide uncertainty when names are common or profiles cannot be confirmed.
- Forbidden overclaims:
  - "This is the professor's current mainline" based only on one student.
  - "X is the senior PhD" without a public role source.
  - "No student-led spine exists" when the paper corpus is incomplete or sampled.
  - "Google Scholar confirms the direction" when only a blocked page or weak snippet was seen.
