---
name: internal-comms
description: |
  "Expert routing and synthesis for internal company communications, status updates, newsletters, and FAQ documents. Trigger this skill when asked to write, edit, format, or draft any internal workplace communications, leadership updates, or team reports. Keywords: 3P updates, company newsletter, status reports, leadership updates, project updates, incident reports, FAQ responses, internal communication, staff announcement, examples/."

  "Expert routing and synthesis for internal company communications, status updates, newsletters, and FAQ documents. Trigger this skill when asked to write, edit, format, or draft any internal workplace communications, leadership updates, or team reports. Keywords: 3P updates, company newsletter, status reports, leadership updates, project updates, incident reports, FAQ responses, internal communication, staff announcement, examples/."
---

# Internal Communications Router

This is a **navigation skill**. You MUST load the corresponding detailed markdown guidelines from the `examples/` directory based on the specific type of communication requested.

---

## Mindset & Thinking Framework

Before writing any communication, ask yourself:

1. **Who is the Audience?** (Executive leadership, direct team, cross-functional partners, or company-wide?)
2. **What is the Core Message?** (What is the single most important takeaway? Put it in the first sentence or headline.)
3. **What is the Action Required?** (Is this FYA - For Your Action, or FYI - For Your Information?)
4. **What is the Tone?** (Transparent, concise, data-driven, or celebratory?)

---

## Scenario Detection & Loading Triggers

You **MUST** identify the communication type and immediately load the corresponding file from the `examples/` directory before drafting:

| Requested Comms Type | Target Guideline File (MANDATORY - Load via `view_file`) | What it covers |
| :--- | :--- | :--- |
| **Progress, Plans, Problems** | [`examples/3p-updates.md`](file:///home/jsoehner/yuv-skills-backup/internal-comms/examples/3p-updates.md) | Weekly/bi-weekly updates for teams or cross-functional stakeholders. |
| **Newsletters / Staff Announcements** | [`examples/company-newsletter.md`](file:///home/jsoehner/yuv-skills-backup/internal-comms/examples/company-newsletter.md) | All-hands digests, department milestones, monthly summaries. |
| **Q&A / FAQs** | [`examples/faq-answers.md`](file:///home/jsoehner/yuv-skills-backup/internal-comms/examples/faq-answers.md) | Answering employee or customer questions directly and constructively. |
| **Other / General Comms** | [`examples/general-comms.md`](file:///home/jsoehner/yuv-skills-backup/internal-comms/examples/general-comms.md) | Incident updates, ad-hoc leadership messages, project milestones. |

---

## Procedural Sequence

1. **Classify:** Identify which of the 4 buckets the user's request falls into.
2. **Load Reference:** Execute `view_file` on the corresponding file in `examples/`. **Do NOT guess the format.**
3. **Extract Context:** Gather the raw facts, data points, or bullet points provided by the user.
4. **Draft:** Apply the specific structure, constraints, and style constraints defined in the loaded reference file.
5. **Refine against NEVER list:** Verify the draft doesn't violate the anti-patterns below.

---

## NEVER Anti-Patterns

| Action | Why | Consequences | Correct Alternative |
| :--- | :--- | :--- | :--- |
| **NEVER** write a status report or 3P update without loading the reference file first. | Different companies/teams have rigid structural preferences that must be adhered to. | Unprofessional formatting, missing critical sections. | Run `view_file` on the exact guideline path. |
| **NEVER** bury the lead or put critical context at the bottom of the message. | Executives and busy team members scan internal comms and rarely read full paragraphs. | Key decisions missed, delayed action items, poor visibility. | Put the summary/TL;DR and primary action items in the first 2 sentences. |
| **NEVER** use jargon or vague timeline references ("soon", "next week"). | Ambiguity breeds confusion and misaligned expectations. | Missed deadlines, lack of accountability. | Use concrete dates (e.g., "by EOD Friday, Oct 24") and define acronyms. |
| **NEVER** hide bad news, setbacks, or blockers in a status update. | Hiding problems prevents leadership and peers from offering support/resources. | Delayed escalation, loss of trust when issues eventually surface. | List them clearly in "Problems" or "Blockers" with mitigation plans. |

---

## Usability & Fallback Logic

* **No direct match:** If the request doesn't match one of the template files (e.g., a post-mortem incident report), load [`examples/general-comms.md`](file:///home/jsoehner/yuv-skills-backup/internal-comms/examples/general-comms.md) as the default baseline.
* **Missing Details:** If the user asks for an update but provides no data, do not invent achievements. Prompt the user:
  > "To draft this update, please provide: (1) Key achievements/launches this period, (2) Critical milestones for next period, and (3) Any blockers/problems you are facing."

## 6) Capture Knowledge

After a company-wide announcement or complex internal communication is finalized, automatically trigger the `capture_knowledge.py` script.
The script will analyze the communication to identify:
- New company-wide policies or project-wide rules.
- Key stakeholder names and contact points.
- Recurring communication patterns or feedback loops.
The script will then route this information to the appropriate storage:
- **OKF**: High-level communication standards, brand voice rules, and announcement templates.
- **ChromaDB**: Specific communication logs, stakeholder summaries, and feedback-driven improvements.
",path: