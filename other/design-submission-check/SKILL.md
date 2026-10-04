---
name: design-submission-check
description: "Audit a design-award submission package against the current official rules for a specific award cycle. Check required materials and technical constraints, cross-material facts and claims, rights and disclosure risks, and final submission readiness. Use when a user asks for a pre-submission check, compliance review, missing-material audit, consistency check, or final go/no-go decision. Do not use this skill to choose an award, retrieve winners, judge the design itself, rewrite the whole entry, or give a legal clearance opinion."
---

# Design Submission Check

## Purpose

Determine whether a concrete design-award submission package is complete, internally consistent, and ready to submit under the current official rules for one exact award, track, category, and cycle.

Return one of three decisions:

- `Ready`: no Blocker or Important findings remain.
- `Conditionally ready`: no Blocker remains, but one or more Important findings require attention.
- `Not ready`: at least one Blocker remains.

## Scope Boundary

- Convert current official submission rules into a project-specific checklist.
- Check required files, fields, declarations, and technical constraints.
- Compare names, facts, claims, credits, metrics, and versions across materials.
- Screen rights, permissions, confidentiality, personal-data, and disclosure risks.
- Perform a final package-level audit and prioritize fixes.
- Stop after the audit. Do not select the award, score design quality, redesign the project, or perform comprehensive copy-editing.

Use `$design-award-match` before this skill when the award, track, or category has not been selected. Route design-quality questions to `design-evaluation` and substantive redesign or rewriting to `design-optimization` when those skills are available.

## Severity Model

Read [references/checking-framework.md](references/checking-framework.md). Classify every finding:

- `Blocker`: likely prevents submission, violates an explicit hard rule, invalidates eligibility, or leaves a mandatory item absent.
- `Important`: materially weakens clarity, credibility, consistency, or rights readiness but is not a confirmed hard-rule failure.
- `Optimization`: optional improvement that does not affect basic submission readiness.

Never hide an unresolved rule or unreadable file inside an overall percentage. The highest unresolved severity controls the final decision.

## User Interaction Contract

Accept:

- the exact award, track, category, and submission cycle;
- official rule page, entry guide, or terms when supplied;
- the submission files or a manifest describing them;
- applicant, team, project, release, authorship, and rights facts relevant to the entry.

If the award, track/category, or cycle is missing, ask one concise question containing only the missing identifiers. If materials are incomplete, audit what is available and list everything that could not be checked; do not invent a pass.

Offer this template when the user asks how to use the skill:

```text
Award / cycle: {exact award and year}
Track / category: {exact official names}
Official rules: {URL or attached guide, optional}
Applicant / team: {names, roles, organization, country or student status}
Submission materials: {attach files or provide paths}
Known third-party content: {images, fonts, music, data, trademarks, AI-generated content}
Requested mode: {full audit / technical check / consistency check / final check}
```

## Audit Workflow

### 1. Lock the submission target

Record the exact award program, cycle, track, category, applicant type, submission stage, deadline, and official timezone. Do not combine requirements from different cycles, categories, or judging stages.

If the selected target appears inconsistent with the package, report it and refer category selection back to `$design-award-match`; do not silently change the target.

### 2. Verify and extract current rules

Read [references/rule-evidence-policy.md](references/rule-evidence-policy.md). At request time, verify current official sources and create a requirement ledger containing:

- mandatory and optional materials;
- form fields and declarations;
- accepted file types, counts, sizes, dimensions, aspect ratios, duration, word or character limits, and languages;
- filename, anonymity, branding, caption, and credit rules;
- applicant, authorship, release-window, prototype, and publication restrictions relevant to final submission;
- rights, consent, AI-use, confidentiality, and disclosure requirements;
- deadline with an absolute date and official timezone.

Attach an official URL and `checked on` date to each rule group. Search snippets and third-party summaries are discovery evidence only. When official sources conflict, the most specific current official terms control; report unresolved conflicts as Blockers.

### 3. Inventory the package

List every supplied file and form field. Assign each item to exactly one requirement ID and record its version, file type, size, technical metadata, language, and readable/openable status.

Use `scripts/check_submission_manifest.py` for deterministic checks when a local package or structured manifest is available. Prepare inputs using the schemas in [examples/rules.example.json](examples/rules.example.json) and [examples/manifest.example.json](examples/manifest.example.json).

```powershell
python scripts/check_submission_manifest.py `
  --rules examples/rules.example.json `
  --manifest examples/manifest.example.json `
  --pretty
```

The script checks declared metadata and available filesystem facts. It does not replace opening documents, inspecting images, playing videos, or verifying portal behavior.

### 4. Check completeness and technical compliance

For each requirement, check:

- presence and required count;
- readable/openable state;
- extension and actual format when detectable;
- file size, dimensions, aspect ratio, resolution, duration, word or character count;
- naming, language, anonymity, credits, and other explicit restrictions;
- form fields, checkboxes, declarations, and signatures;
- deadline and upload-stage compatibility.

Mark an unverified mandatory constraint `Not checked`, never `Pass`. Treat a required missing item or confirmed hard-limit failure as a Blocker.

### 5. Check cross-material consistency and evidence integrity

Read [references/consistency-rights-checklist.md](references/consistency-rights-checklist.md). Establish a canonical fact sheet, then compare every material against it:

- project title, category, applicant, team, roles, organization, dates, and version;
- problem, target user, primary function, workflow, technology, materials, and sustainability claims;
- quantities, dimensions, performance, research results, impact metrics, and commercial status;
- captions, labels, subtitles, voice-over, charts, citations, and credits.

Flag contradictions, unsupported superlatives, missing units, inconsistent denominators, obsolete versions, and claims that exceed the supplied evidence. Do not independently validate scientific or commercial truth unless authoritative evidence is supplied; state the verification limit.

Evaluate narrative only for submission integrity: required content coverage, logical continuity, comprehensibility, and agreement with evidence. Do not perform general stylistic polishing or rewrite the entire entry unless separately requested through the appropriate skill.

### 6. Screen rights and disclosure risks

Check the provenance and declared permission status of photographs, illustrations, video, music, sound, fonts, icons, maps, datasets, research, code, trademarks, product imagery, personal information, and AI-generated or AI-assisted content.

Use only these statuses:

- `Cleared`: the user supplies a credible ownership, license, consent, or permitted-use basis.
- `Pending`: permission or required disclosure is being obtained.
- `Unknown`: provenance or permission is not established.
- `Restricted`: supplied terms appear incompatible with the intended submission use.

This is risk screening, not legal advice or a guarantee of non-infringement. Never mark content legally cleared from appearance alone. Escalate ambiguity in official terms or third-party licenses for qualified review.

### 7. Run the final gate

Follow [references/output-template.md](references/output-template.md). Before declaring `Ready`, confirm:

- all mandatory requirements have been mapped and checked;
- every Blocker and Important finding has a disposition;
- final versions are identifiable and no stale duplicate is in the upload set;
- the portal-entry values match the final files when portal information is available;
- the deadline and timezone are explicit;
- a final archive or manifest can reproduce the intended upload set.

If portal behavior, payment, account permissions, or an upload preview cannot be accessed, state that this portion remains a user-executed check.

## Decision Rules

- Current official rules outrank templates, past-cycle guides, organizer emails without context, and third-party summaries.
- Explicit hard-rule failures are Blockers even when the material is otherwise strong.
- Missing evidence never becomes a pass by inference.
- One issue receives one primary severity; cross-reference affected materials instead of duplicating it.
- Do not use an average score to cancel a Blocker.
- Rights `Pending`, `Unknown`, or `Restricted` cannot be reported as cleared.
- A completed offline audit does not prove that the award portal accepted the upload.

## Fallback Rules

- If live official rules cannot be verified, use user-supplied official documents, label rule freshness, and do not return `Ready` for time-sensitive requirements.
- If a file cannot be opened, report exactly which checks were impossible and classify mandatory unreadability as a Blocker.
- If technical metadata cannot be measured, request the metadata or mark the constraint `Not checked`.
- If only a partial package is supplied, return a partial audit and a missing-material list, not a final pass.
- If official rights or AI-disclosure wording is ambiguous, quote minimally, link the rule, and label the issue for qualified review.

## Compliance and Safety

- Inspect only user-authorized files and public official pages.
- Do not upload materials to an award portal, accept legal declarations, pay fees, or submit on the user's behalf without explicit authorization and an available approved workflow.
- Do not expose confidential project content in external search queries.
- Avoid reproducing or redistributing copyrighted submission content beyond what is necessary for the audit.
- Treat personal data, unpublished designs, credentials, and application identifiers as sensitive.

## Example Invocations

- `使用 $design-submission-check，按照附件中的 iF 当届规则，对这个提交包进行完整终检。`
- `使用 $design-submission-check，只检查所有图片、PDF和视频的数量、格式、大小及命名是否合规。`
- `使用 $design-submission-check，核对表单、展板、说明文档和视频中的项目数据是否一致，并筛查授权风险。`

