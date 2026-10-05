---
name: job-search-agent-cn
description: Optimize Chinese technical resumes, screen and apply to matching jobs, write tailored recruiter greetings, monitor recruiting messages, and prepare or send safe routine replies. Use for BOSS Zhipin and similar China job-search workflows involving AI Agent, AI application, full-stack, backend, career transitions, application tracking, interview funnel improvement, or recurring recruiting-message automation.
---

# AI Job Search Agent (China)

Run a truthful, selective job-search workflow. Optimize for interview conversion and role fit, not raw message volume.

## Select a mode

1. **Audit**: inspect the resume, target roles, profile consistency, and application funnel without changing external state.
2. **Resume**: rewrite a role-specific resume and verify the exported artifact.
3. **Search**: rank suitable positions without contacting recruiters.
4. **Apply**: send job-specific greetings only after the user authorizes outbound contact.
5. **Reply**: read new messages and send routine factual replies within the authorization boundary.
6. **Monitor**: check status periodically, reply when safe, and resume targeted applications after a configured quiet period.

Create a fact profile from [references/profile-template.md](references/profile-template.md) before applying or replying. Read [references/reply-playbook.md](references/reply-playbook.md) before handling recruiter messages.

## Establish truth first

- Separate formal employment, independent products, open-source work, and interests.
- Verify unstable facts such as repository Stars, merged PRs, salary ranges, company information, and job status before using them.
- Do not invent production users, revenue, team size, tenure, degrees, business metrics, or availability.
- If the resume conflicts with the user's latest statement, pause and reconcile the fact.

## Optimize the resume

1. Read the source resume and target job description.
2. Diagnose first-screen positioning: target title, experience narrative, strongest proof, keywords, dates, and compensation expectations.
3. Create separate variants when the candidate spans distinct tracks.
4. Put concrete evidence near the top: shipped scope, personal ownership, test/release work, public contributions, and demo links.
5. Render and inspect the PDF or HTML when layout matters. Check dates, links, page breaks, and text extraction.

## Screen jobs

Score each role using visible evidence:

- target-role, experience, stack, compensation, and location fit;
- hard education, tenure, industry, language, and technology requirements;
- demonstrable transferable skills;
- duplicate or previously rejected applications.

Always read the full job description. A search result marked “经验不限” may still require several years or a graduate degree in the description.

## Apply selectively

- Confirm outbound authorization for the current platform and session.
- Prefer a small batch of strongly matched jobs per run.
- Write each greeting from the actual job description in roughly 80–180 Chinese characters.
- Lead with the strongest match, add one or two verified proofs, and end with an invitation to review a demo, code, or resume.
- If the platform sends a generic greeting automatically, add one tailored follow-up.
- Do not send the same template in bulk or contact mismatched positions to inflate counts.
- Verify delivery and record the application with `scripts/application_log.py`.

## Reply safely

Routine factual replies may cover verified projects, stack, graduation, availability, links, demos, open-source work, and an authorized resume.

Stop for user confirmation before sending messages about:

- current or expected salary and negotiation;
- exact interview times or start-date commitments;
- phone, identity, address, certificates, banking, or other sensitive data;
- relocation, work hours, probation, non-compete, equity, offers, or contracts;
- facts not supported by the profile, resume, repository, or user confirmation.

Do not reply to rejection-only notifications. Mark them viewed when safe.

## Monitor without spamming

- Track the last meaningful recruiter reply and last outbound application separately.
- Treat “read” and “resume viewed” as progress, not an invitation to send another message.
- Follow up on a read conversation at most once, normally after 24 hours.
- Resume a small batch of high-fit applications only after the configured quiet period.
- Restore the user's previously active browser tab when possible.
- Use the host's supported recurring automation mechanism when the user requests monitoring.

## Maintain a deduplicated log

```bash
python3 scripts/application_log.py add \
  --path /absolute/path/applications.csv \
  --company "Example AI" \
  --role "AI Agent 工程师" \
  --url "https://example.com/job/123" \
  --status sent
```

Run `list` before applying. Update status after replies, resume views, interviews, rejections, closure, or offers.

## Report outcomes

Report new replies, sent messages, contacted roles, resume views, rejections, interview requests, and decisions requiring the user. Never claim an external action without verifying it on the platform.
