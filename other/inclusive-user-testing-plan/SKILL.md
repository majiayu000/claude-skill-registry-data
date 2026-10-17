---
name: inclusive-user-testing-plan
description: Creates an inclusive participant user-testing plan for websites, applications, components, and critical task flows. Use when the user asks to plan usability research with disabled and non-disabled participants, define recruitment and accommodations, prepare accessible sessions, measure task outcomes, protect consent and privacy, record issues, or synthesize lived-experience evidence without conflating it with WCAG conformance.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to product, research, and accessibility context. No specialist skill or research platform is required.
metadata:
  category: research-synthesis
  task_type: research
  audience: user-researchers-accessibility-specialists-designers-and-product-teams
  tags:
    - user-research
    - usability-testing
    - accessibility
    - inclusive-design
    - disabled-participants
    - research-ethics
    - accommodations
    - research-synthesis
  status: draft
  side_effects: none
---

# Inclusive User Testing Plan

## Purpose

Create an ethical, accessible, and decision-ready plan for participant usability research across websites, applications, components, and critical task flows. Define who to recruit, what to learn, how to remove participation barriers, how to run sessions, and how to synthesize evidence without treating any participant as representative of an entire disability category.

This skill plans research only. It does not recruit participants, collect consent, run sessions, claim statistical representativeness, or determine WCAG conformance.

## When to use this skill

Use this skill when:

- A product team needs a moderated or unmoderated usability study that includes disabled participants and varied access methods.
- A website, application, component, prototype, or critical flow needs participant evidence about task performance, comprehension, confidence, barriers, or recovery.
- Recruitment, accommodations, accessible materials, session setup, moderation, compensation, privacy, issue recording, and synthesis need one coherent plan.
- An inclusive interface audit needs a participant-research work package.
- Existing user-testing evidence needs a predefined synthesis method and reporting boundary.

Do not use this skill when:

- The request is only for an expert accessibility audit, automated scan, assistive-technology compatibility check, or WCAG conformance evaluation.
- The user wants findings synthesized from completed specialist audits; use `cross-framework-audit-synthesis`.
- The task is clinical, diagnostic, therapeutic, or intended to make claims about a disability population.
- The target is too unstable, unsafe, or incomplete for participants and the research question cannot be answered with a lower-fidelity artifact.

## Research principles

- Treat disability as diverse and intersecting, not as one participant segment. Consider access needs, assistive technologies, strategies, experience, context, language, age, and other relevant characteristics without assuming they are interchangeable.
- Never ask one participant to represent blind people, Deaf people, neurodivergent people, mobility-disabled people, or any other category.
- Recruit for relevant variation across participants. Describe each participant's evidence as individual and contextual before identifying patterns across sessions.
- Ask participants what access and accommodation setup works for them. Do not infer needs from a diagnosis or require unnecessary medical disclosure.
- Test meaningful user goals, not whether participants can reproduce a prescribed interaction.
- Separate participant usability evidence, expert accessibility evidence, assistive-technology compatibility evidence, and WCAG criterion results.
- Do not infer WCAG pass or failure from participant success, difficulty, preference, or absence of an observed barrier.
- Do not present expert review as lived-experience evidence or participant observations as universal truth.
- Minimize personal and disability-related data. Collect only what the research question and accommodation process require.

## Inputs to inspect

Inspect the smallest available set that establishes the study:

- Product decision, research goal, known risks, assumptions, and unanswered questions.
- Target URL, build, prototype, component, route, flow, version, and release stage.
- Critical tasks, user stories, roles, locales, devices, supported platforms, and real-world contexts.
- Existing analytics, support themes, prior research, known accessibility issues, expert audits, and WCAG results.
- Recruitment constraints, participant relationships, timeline, budget, compensation policy, and ethics or legal-review requirements.
- Available remote platforms, research locations, recording tools, test devices, assistive technologies, test accounts, and safe sample data.
- Existing consent forms, privacy notices, retention rules, accessibility statements, and incident procedures.
- Any scope, target IDs, evidence rules, or finding contract supplied by `inclusive-interface-audit-orchestrator`.

Label assumptions and missing inputs. Do not delay a useful draft for every unknown; add unresolved decisions and recruitment or session gates.

## Workflow

### 1. Frame the study

1. Identify the product decision the research must inform.
2. Define the target, version, scope, release stage, and critical flows.
3. State what participant research can establish: observed behavior, strategies, comprehension, barriers, preferences, confidence, and recovery in tested contexts.
4. State what it cannot establish: population prevalence, universal usability, technical compatibility across all environments, legal compliance, or WCAG conformance.
5. Preserve orchestrator-provided scope, target IDs, criticality, exclusions, and evidence labels when supplied. When absent, define them locally so the plan remains independently usable.

### 2. Define research questions

Write a short set of neutral, decision-linked questions. Cover only questions the study design can answer, such as:

- Can participants recognize how to begin and complete each critical task using their usual access method?
- Where do participants encounter barriers, uncertainty, excessive effort, loss of context, or unrecoverable states?
- What information, feedback, labels, structure, or controls support or hinder understanding and action?
- How do access method, familiarity, environment, role, or task complexity change strategies and outcomes?
- Can participants detect errors, understand consequences, and recover without unsafe or unwanted results?
- Which observed problems recur, which are context-specific, and what evidence would distinguish them?

For every question, record the decision it informs, participants and tasks needed, observable evidence, and limitation. Avoid questions that presume a cause, ask participants to validate a proposed solution, or frame disability as the problem.

### 3. Build the participant plan

Create a recruitment matrix from the research risks rather than a single disability quota.

Consider relevant variation across:

- Functional experiences and access needs involving vision, hearing, speech, mobility, dexterity, cognition, learning, attention, memory, fatigue, pain, or sensory processing.
- Primary and secondary access methods, such as screen readers, magnification, text resizing, high contrast, captions, transcripts, switches, voice input, keyboard-only use, alternative pointers, reading support, or reduced motion.
- Familiarity with the product domain, relevant assistive technology, devices, operating systems, and task.
- Role, permission level, language, literacy, age range, socioeconomic context, geography, and environmental constraints when they affect the research question.
- Temporary, episodic, situational, and multiple disabilities where relevant.

For each characteristic, record why it matters, the variation sought, recruitment source, screening method, target range rather than token count, and remaining gap.

Apply these safeguards:

- Do not combine disabled participants into one comparison group.
- Do not assume people sharing a diagnosis, impairment, or assistive technology will behave alike.
- Do not use a single participant as the voice of a category.
- Do not screen for diagnoses when access needs, strategies, or task context are the relevant variables.
- Do not promise demographic representativeness from a small qualitative sample.
- If the sample is constrained, narrow the claims and identify follow-up cohorts instead of overstating coverage.

### 4. Plan accommodations and participation access

Ask each participant privately what they need before the session. Offer examples without making the list exhaustive:

- Preferred communication channel and format.
- Captions, sign-language interpretation, transcripts, audio description, plain language, Easy Read, large print, Braille, or advance materials.
- Use of personal assistive technology, device, browser, settings, input method, or support person.
- Extra setup time, flexible pacing, breaks, shorter sessions, split sessions, rescheduling, or asynchronous options.
- Quiet or low-stimulation space, lighting control, scent reduction, seating, physical access, accessible transport, parking, restrooms, and service-animal access.
- Camera-off participation, alternatives to speech, and alternatives to timed or written responses.

Record who will arrange each accommodation, confirmation deadline, backup, cost owner, and privacy treatment. Accommodation time must not reduce task time or compensation. Never require a participant to justify a need with medical evidence unless a binding policy explicitly requires it and has been reviewed.

### 5. Select representative tasks

Choose tasks from criticality, frequency, uncertainty, and exclusion risk. Include:

- Entry and orientation.
- The primary success path.
- Validation, error, cancellation, timeout, interruption, and recovery where relevant.
- Destructive, financial, health, identity, privacy, or legal-commitment steps when safe to test.
- Relevant roles, permissions, devices, locales, and content variations.
- Component states and compositions when testing a component rather than a complete flow.

Write goal-based scenarios in participants' language. Avoid naming controls, revealing the intended path, requiring a specific input method, or turning the session into training. Define safe data, starting state, success state, reset procedure, stopping rule, and expansion trigger for each task.

### 6. Define success measures

Use a mixed evidence set and interpret it within each task and access context:

- Outcome: completed independently, completed with participant-requested assistance, partially completed, abandoned, or blocked.
- Critical and non-critical errors, unsafe outcomes, and unintended actions.
- Assistance requested, moderator intervention, and reason.
- Recovery success, recovery route, and residual uncertainty.
- Observable effort, repeated actions, navigation loops, loss of context, and workaround use.
- Comprehension of labels, instructions, feedback, status, errors, and consequences.
- Participant-reported ease, confidence, control, trust, and fit with their usual strategy.
- Time on task only when timing is meaningful and accommodation or technology setup is excluded.

Define success thresholds before sessions, but do not average unlike access contexts into a misleading benchmark. Report counts with denominators and context. Qualitative studies support pattern and mechanism discovery, not population-rate estimates.

### 7. Prepare observation and follow-up prompts

Use neutral prompts and allow silence:

- “What are you looking for or expecting here?”
- “What, if anything, is making this step difficult?”
- “What did that change or message mean to you?”
- “What would you do next?”
- “How does this compare with the way you usually do this?”
- “What helped you know the action worked?”
- “Would you normally continue, seek help, choose another route, or stop?”
- “Is there anything about your setup or this session that affected what happened?”

Ask participants to describe their experience, not diagnose code or propose a WCAG criterion. Do not require continuous think-aloud when it adds cognitive, speech, fatigue, or access burden; use retrospective probing or observation instead.

### 8. Establish consent, privacy, and compensation

Create accessible, plain-language consent materials that state:

- Study purpose, activities, duration, voluntary nature, foreseeable discomfort, and right to pause, skip, or withdraw without penalty.
- What is recorded, who can access it, how it will be used, retention period, deletion process, and limits on confidentiality.
- Whether observers, vendors, artificial intelligence tools, transcription, or cross-border data processing are involved.
- Separate, granular choices for session participation, audio, video, screen, assistive-technology output, quotes, and future contact.
- How to revoke optional permissions and whom to contact with questions or concerns.

Use pseudonymous participant and session IDs. Avoid collecting diagnosis, medical details, personal account data, or assistive-technology output unless necessary. Prevent test data from exposing real financial, health, identity, employment, or authentication information. Define redaction, secure transfer, access control, incident handling, retention, and destruction.

Set compensation that:

- Reflects total participant time, preparation, technology checks, and burden at a fair local or organizational rate.
- Does not reduce payment for withdrawal, access-related pauses, slower task completion, or technical failure outside the participant's control.
- Covers agreed access costs such as interpreters, support workers, transport, or data use separately from the participant honorarium.
- Offers an accessible payment method and clearly communicates timing, tax implications when applicable, and alternatives.
- Avoids coercion, exploitative recruitment, or asking community organizations to provide unpaid accessibility labor.

Route organization-specific consent, privacy, ethics, safeguarding, tax, or compensation decisions to qualified owners. Do not provide legal or institutional approval.

### 9. Design accessible session materials

Prepare screeners, invitations, consent forms, schedules, instructions, tasks, questionnaires, moderator guides, and debriefs in accessible formats:

- Use semantic headings, meaningful links, clear labels, logical reading order, keyboard access, visible focus, sufficient contrast, resizable text, and plain language.
- Provide requested alternative formats early enough to review.
- Avoid inaccessible CAPTCHA, drag-only ranking, forced video, strict timeouts, and response widgets that do not work with the participant's input method.
- Make rating scales understandable, optional when appropriate, and operable with assistive technology.
- Include contact and accommodation-request channels in more than one mode.
- Pilot materials with the actual platform and relevant access methods.

### 10. Specify remote or in-person setup

For remote sessions, define:

- Platform accessibility and known limitations; browser, device, account, and assistive-technology compatibility.
- An optional paid technology check that does not rehearse study tasks.
- Join instructions, accessible authentication, dial-in or text backup, captioning or interpreting setup, and a reconnect plan.
- Whether the participant shares a screen, camera, audio, or assistive-technology output, with separate consent and a non-sharing alternative.
- Test-account provisioning, safe data, recording indicators, observer behavior, and technical-support ownership.

For in-person sessions, define:

- Step-free route, entrances, elevators, room dimensions, adjustable furniture, accessible restroom, transport, parking, signage, emergency egress, lighting, acoustics, temperature, and sensory conditions.
- Device and assistive-technology choice, permission to use personal equipment, sanitized loan equipment, power, connectivity, and setup time.
- Reception procedure, support-person and interpreter access, service animals, observer placement, recording visibility, breaks, and private waiting space.

For either mode, run a dry run, document fallbacks, and specify when to stop or reschedule rather than forcing a compromised session.

### 11. Guide the moderator

The moderator must:

- Confirm communication preferences, consent choices, accommodations, recording state, and the right to stop before beginning.
- Distinguish participant-requested assistance from moderator intervention and log both.
- Avoid leading, teaching, defending the design, completing actions for the participant, or touching their device or assistive technology without explicit permission.
- Use the participant's preferred language for disability, identity, technology, and assistance.
- Allow the participant to choose their access method and pace.
- Watch for fatigue, distress, privacy exposure, unsafe actions, and access breakdowns; pause, skip, or stop according to the protocol.
- Ask about observed behavior without attributing it to disability.
- Debrief, explain any deception if ethically approved, confirm compensation, and restate data-withdrawal contacts.

### 12. Record issues and evidence

Use one record per distinct observed barrier or enabling behavior:

| Field | Requirement |
|---|---|
| `research_id` | Stable identifier |
| `session_id` | Pseudonymous ID; never use participant name |
| `target` | Product version, route, component, task, step, and state |
| `environment` | Mode, device, platform, browser, input and assistive technology when relevant |
| `observation` | What happened, in behavioral language |
| `participant_perspective` | Participant explanation or a short consented quote, clearly attributed |
| `task_outcome` | Outcome, errors, assistance, recovery, and consequence |
| `access_context` | Relevant access method or context without unnecessary diagnosis |
| `evidence_reference` | Notes, timestamp, recording, screenshot, or artifact under the consent rules |
| `moderator_influence` | Prompt, intervention, technical problem, or setup effect |
| `interpretation` | Supported usability meaning, alternative explanations, and confidence |
| `status` | `observed`, `hypothesis`, `needs-validation`, or `positive-pattern` |
| `related_ids` | Similar observations, expert findings, or technical results without merging them prematurely |

Record product barriers separately from research-platform, accommodation, moderator, or environment failures. Preserve positive patterns that explain what worked. Do not include sensitive participant profiles in product issue trackers; publish the minimum evidence needed for action.

When an orchestrator contract is present, preserve its target and evidence identifiers and provide an explicit mapping rather than replacing the research record. A participant observation may be linked to a canonical audit finding, but it remains participant evidence.

### 13. Synthesize without overgeneralizing

1. Review notes against recordings only within consent and retention limits.
2. Separate observed behavior, participant interpretation, moderator influence, and researcher inference.
3. Cluster by task, barrier or enabling mechanism, consequence, and likely remediation locus.
4. Analyze patterns within relevant access contexts before comparing across them.
5. Look for variation, contradictions, successful strategies, negative cases, and research-setup effects.
6. Count participants, sessions, and occurrences separately. Always show denominators and avoid statistical language unsupported by the design.
7. Rate confidence from evidence quality, recurrence, contextual consistency, moderator influence, and alternative explanations.
8. Prioritize by task criticality, consequence, recurrence in the studied sample, workaround quality, reach of the affected surface, and confidence.
9. Keep single-participant severe barriers visible as contextual findings; do not dismiss them for low frequency or generalize them to a category.
10. State tested and untested participants, access methods, tasks, states, environments, and product versions.
11. Convert unresolved explanations into follow-up research or technical validation questions.

Maintain two explicit result tracks:

- **Usability research findings:** Participant behavior, perspective, strategies, barriers, enabling patterns, task outcomes, context, recurrence, confidence, and design implications.
- **Accessibility conformance results:** Criterion-level WCAG results produced by a separately scoped technical evaluation with version, level, target, method, and evidence.

Cross-reference the tracks only when evidence supports a relationship. Never relabel a participant difficulty as a WCAG failure, a participant success as a WCAG pass, or a WCAG result as proof of a good or bad experience for all users.

## Output format

Return:

```md
# Inclusive User Testing Plan

## Study brief
- Product decision:
- Target, version, and release stage:
- In scope:
- Out of scope:
- Research limitations:

## Research questions
| ID | Question | Decision informed | Participants and tasks | Observable evidence | Limitation |
|---|---|---|---|---|---|

## Participant and recruitment matrix
| Relevant characteristic or context | Variation sought | Why it matters | Screening and source | Target range | Coverage gap |
|---|---|---|---|---|---|

## Accommodation plan
| Need or preference | How it will be requested | Arrangement and owner | Confirmation | Backup | Privacy treatment |
|---|---|---|---|---|---|

## Task protocol
| Task ID | Goal-based scenario | Start and success state | Variations and recovery | Measures | Safety and reset | Expansion trigger |
|---|---|---|---|---|---|---|

## Success measures
- Outcome definitions:
- Assistance and intervention rules:
- Qualitative measures:
- Timing rules:
- Interpretation boundaries:

## Observation prompts
- ...

## Consent, privacy, and compensation
- Consent choices:
- Data collected and excluded:
- Recording, access, retention, and deletion:
- Compensation and access-cost treatment:
- Required organizational review:

## Accessible materials checklist
- [ ] ...

## Session setup
### Remote
- ...
### In person
- ...
### Fallback and stop rules
- ...

## Moderator guide
- Opening:
- During tasks:
- Safety, fatigue, and access checks:
- Closing:

## Issue record
[Repeat the research issue fields and allowed status values.]

## Synthesis plan
- Coding and clustering:
- Within-context and cross-context analysis:
- Contradictions and negative cases:
- Confidence and prioritization:
- Claim boundaries:
- WCAG separation and cross-reference method:

## Coverage and limitations
| Participants or contexts | Tasks and states | Environments | Covered | Not covered | Follow-up trigger |
|---|---|---|---|---|---|

## Open decisions and readiness gates
- ...
```

Keep the plan proportional. A component study may use a compact matrix; a consequential multi-flow study needs the full protocol and explicit ethics, safety, and evidence gates.

## Quality bar

The task is complete only when:

- Every research question informs a named decision and has observable evidence.
- Recruitment covers relevant variation without treating disabled participants as one group or a participant as a category representative.
- Individual accommodations, accessible materials, compensation, consent, privacy, and withdrawal are operationally defined.
- Tasks are realistic, goal-based, safe, and representative of critical success and recovery paths.
- Measures distinguish task outcome, assistance, recovery, comprehension, effort, and participant perspective.
- Remote or in-person setup, fallbacks, moderator behavior, and stop rules are executable.
- The issue record preserves context, evidence, participant perspective, moderator influence, and uncertainty without unnecessary personal data.
- Synthesis includes within-context variation, contradictions, negative cases, positive patterns, confidence, denominators, coverage gaps, and bounded claims.
- Usability research findings and WCAG conformance results are reported in separate tracks.
- The plan can accept an orchestrator scope and feed a synthesis workflow but remains usable with neither skill available.
- No claim of universal usability, population prevalence, legal compliance, certification, or WCAG conformance is made.

## Edge cases

- **One available disabled participant:** Include the participant when ethical and relevant, report individual contextual evidence, and do not use it to characterize a disability group. Recommend follow-up variation.
- **Very small sample:** Focus on mechanisms, severe barriers, strategies, and hypotheses. Avoid percentages or saturation claims.
- **Mixed disabilities or access methods:** Let participants describe their combination and strategy. Do not force observations into one impairment category.
- **Unknown accommodation needs:** Ask privately, offer flexible examples and contact modes, budget contingencies, and confirm before the session.
- **Inaccessible research platform:** Change the platform, provide an equivalent channel, or reschedule. Record platform failure separately from product usability.
- **Prototype limitations:** Mark unavailable semantics, input methods, states, or assistive-technology behavior and narrow the questions accordingly.
- **Unmoderated study:** Validate platform and materials with relevant access methods, provide accessible support and withdrawal routes, and avoid tasks requiring safety monitoring.
- **Safety-sensitive flow:** Use sandboxed accounts and reversible data, define stop rules, and involve the appropriate ethics, safety, or domain owner.
- **Participant and WCAG evidence disagree:** Preserve both evidence tracks, examine scope and context, and plan criterion-specific technical validation or further research.
- **Community partner recruitment:** Define respectful engagement, data stewardship, compensation for organizational labor, and feedback to the community.
- **International study:** Localize language, consent, payment, privacy handling, cultural assumptions, time zones, and accommodation sourcing.

## Related skills

- `inclusive-interface-audit-orchestrator` — provide study scope, critical flows, target IDs, and evidence boundaries.
- `cross-framework-audit-synthesis` — synthesize technical audit findings while preserving participant evidence as a distinct source type.
- `inclusive-task-flow-review` — identify task and recovery risks that may become research questions.
- `wcag-audit-scope-planner` — plan criterion-based conformance evaluation separately from participant research.
- `accessibility-validation-planner` — plan technical validation for hypotheses raised during sessions.
