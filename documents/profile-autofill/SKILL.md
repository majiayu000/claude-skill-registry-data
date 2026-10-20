---
name: profile-autofill
description: Paste your CV, LinkedIn export or a short career summary and your agent fills in your daily.dev work history, education, projects and tech stack, so recruiters and feed personalization have something to work with.
---

# Profile Autofill

Your daily.dev profile powers Career Mode matching and feed personalization, and most profiles are empty. Profile Autofill fills them from something you already have.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected with the `write` scope, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Read the source** the user provides: a CV (PDF, Markdown, text), a LinkedIn data export, a résumé website, or a few sentences. Extract experiences with `type` (`work`, `education`, `project`, `certification`, `volunteering`, `opensource`), `title`, organization, `startedAt` and `endedAt` (ISO dates; use the first of the month when only a month is known; omit `endedAt` for current roles), a one-paragraph `description`, and for work entries `employmentType` (`FULL_TIME`, `PART_TIME`, `CONTRACT`, `INTERNSHIP`) and `locationType` (`REMOTE`, `OFFICE`, `HYBRID`) when stated. Collect technologies as `skills` per role and as a flat list for the stack.
2. **Check what exists.** `getProfileExperiences` with `limit` 50 (`GET /profile/experiences?limit=50`) and `getProfileStack` (`GET /profile/stack?limit=100`). Skip anything that matches an existing entry by title and organization; propose updates with `putProfileExperiencesById` (`PUT /profile/experiences/{id}`) only if the user asks to overwrite.
3. **Show the plan** as a table (type, title, organization, dates) plus the stack additions, and ask the user to confirm or edit. Never guess dates or employers that aren't in the source.
4. **Create experiences.** `postProfileExperiences` per entry (`POST /profile/experiences`). Required: `type`, `title`, `startedAt`. Use `customCompanyName` for the organization (and `customDomain` for its favicon); `companyId` only when the user supplies one. For `opensource`, pass `repository: { name, url, owner }`. Unknown enum names are rejected with a 400, so send only the values listed in step 1.
5. **Update the stack.** For each technology, `getProfileStackSearch` with `query` (`GET /profile/stack/search?query=<name>`); if a tool matches, `postProfileStack` with its exact `title` and `section` `primary` (`POST /profile/stack`). Report technologies with no matching tool.
6. **Confirm** with `getProfileExperiences` and summarize what was created.

## Output

The plan table before, then a short list of created entries with their ids, and the technologies that couldn't be matched.

## Guardrails

- Never invent or embellish. If the source says "2019 to 2021", don't add months.
- Never delete or overwrite existing entries without an explicit instruction.
- Don't send personal data beyond what the profile fields hold; leave out addresses, phone numbers and references.
- One request per experience and per stack tool, typically 15 to 30 for a full CV.
