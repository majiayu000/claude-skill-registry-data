---
name: feishu-issue-debugger
description: Read and investigate Feishu Project work items that report bugs or performance issues against local repositories, exact versions, screenshots, attachments, logs, and runtime evidence. Use when the user asks to analyze, reproduce, diagnose, or prepare a local fix for a bug work item in Feishu Project. Feishu access is always read-only; do not use for ordinary Feishu documents, non-bug work items, issue administration, issue mutation, or publishing.
---

# Feishu Issue Debugger

Build an evidence-backed account of the reported issue before proposing or making a change. Keep issue-page evidence, repository state, runtime evidence, and validation claims distinct.

## Start Minimally

Read only the instructions needed to establish scope and permissions:

1. Read the `AGENTS.md` files that govern the current directory.
2. Follow any explicit pointer those instructions make mandatory for this task.
3. Do not load every local context file at startup and do not create missing context files during a read-only task.

Treat names such as `.manifest/AGENTS.md`, `context.md`, `knowledge.md`, `validation.md`, `pr.md`, and Feishu rule files as repository-specific candidates, not universal contracts. Discover files by their role: local rules, project orientation, durable knowledge, validation guidance, and delivery conventions.

## Enforce the Browser Gate

After the minimal instruction read, open the exact Feishu Project bug work-item URL supplied by the user. Prefer the Codex in-app Browser and select it explicitly when the browser control surface supports a stable in-app selector such as `iab`; do not use URL-based automatic browser selection for the first attempt.

The in-app Browser is a preference, not an absolute prohibition on native external browsers. Fall back to a connected native external browser only when the in-app Browser is unavailable, disconnected after bounded recovery, cannot render the issue, or lacks an operation required to collect the evidence. Do not choose the external browser merely because it is more convenient or already open. Record the reason for fallback and the actual browser surface used.

Confirm that the target bug work item itself is visible, including its title or name and the relevant rendered detail fields or narrative. Do not require a literal `Description` label. A cookie, Feishu homepage, loading shell, login page, SSO page, or permission error does not prove access.

If the selected browser reaches a login, SSO, or permission barrier, stop. State the precise blocker and ask the user to log in or restore access in that browser; do not switch browser surfaces merely to bypass authentication. Do not silently fall back to public search, an API summary, copied browser credentials, local history, or a guessed issue description.

Feishu issue access is a hard read-only boundary for this skill. Never edit fields, status, assignees, comments, attachments, relations, work progress, or any other issue state. Do not invoke mutating Feishu tools, submit forms, upload files, or publish evidence. If the user asks for issue administration or mutation, stop this skill's Feishu workflow and route that request to a separate explicitly authorized workflow; do not reinterpret it as permission for this debugger to write.

This read-only boundary applies to Feishu remote state, not to the local evidence workspace. Within the verified ignored or external issue evidence root, this skill may create, update, organize, deduplicate, hash, validate, and sanitize local evidence files as part of the investigation. Local evidence writes never imply permission to change the Feishu work item.

Downloaded staging artifacts created by the current run are temporary. After a final artifact is copied into the verified issue evidence root and passes the required validation, delete the exact staging file by default. This standing cleanup rule does not authorize deleting pre-existing downloads, user-provided files, final evidence, or anything whose ownership cannot be proven. Follow the guarded cleanup procedure in [references/evidence-and-validation.md](references/evidence-and-validation.md).

Local evidence persistence is the default for an investigation. Unless the user explicitly requests an access-only or download-capability check, or explicitly says not to download, create a verified ignored or external issue evidence root and retain a sanitized issue brief, all captured comments, every non-sensitive issue-owned Description or comment image, every diagnostically relevant non-sensitive image-valued custom field, the attachment inventory and relevant downloaded attachments, lifecycle evidence that was inspected, and a validation/acquisition index. Keep final evidence; clean only proven task-created staging artifacts. If any required evidence cannot be saved, report the exact coverage and blocker rather than silently continuing with a browser-only summary.

## Establish the Authoritative Issue Brief

Before deep repository exploration, record a compact brief from the rendered page:

- exact work-item URL and identifier;
- work-item type or template when visible, and the work-item title or name as the primary statement of scope and symptom;
- version and environment baseline, including relevant version/build/commit fields and readable screenshots, separated by owning component when multiple components participate;
- trigger conditions and the reported reproduction or execution path;
- observed outcome or failure signal;
- expected outcome or exact acceptance signal, kept distinct from the observed outcome and marked missing when the work item does not state it;
- the original rendered field label or narrative source for each mapped baseline, trigger, observed-outcome, and expected-outcome value;
- comments or remarks, including their authors, timestamps, reply context, links, and embedded evidence;
- relevant activity-log state changes and the current work-progress state;
- identifiers and names of linked work items, without recursively expanding them unless the user asks or their contents are necessary for the reported symptom;
- relevant screenshots, attachments, logs, branches, and environment notes;
- missing or unreadable evidence.

Feishu field names are template-specific. Map rendered evidence to the semantic slots above instead of requiring fixed keys. Labels such as `测试版本：`, `复现步骤：`, and `结果：` are one valid existing pattern, not a contract; another bug template may expose equivalent evidence through fields such as software version, version screenshot, problem description, job or scene, key logs, or key files. Preserve the actual source label and do not treat an absent candidate label as missing evidence until the relevant visible narrative and fields have been checked.

Classify every diagnostically relevant rendered field as a scalar value, explicit empty state, resolved media value, unresolved media value, or sensitive exclusion. A field label with no flattened text value is not proof that the field is empty when its rendered value area contains or may contain an image, file, preview, or other media. Do not select a code baseline while a baseline-related media field remains unresolved; open and inspect it, or record the exact access or readability blocker.

Open screenshots, including screenshots stored in custom fields, at a readable size. Do not infer their contents from thumbnails, filenames, URLs, flattened API text, or generic version fields.

Inspect the rendered comments surface when it exists. Feishu Project localizes the same tab as `评论/备注` in Chinese and `Comments` in English. Locate it by its visible semantic label for the active locale, not by a single fixed string or URL parameter. After selecting it, verify that the comment list or empty-comment state is actually rendered; a comment-shaped URL does not prove that the tab is active.

When the user asks for complete issue evidence, or when lifecycle changes matter, also inspect the localized `操作记录` / `Activity Log` and `工作进展` / `Work Progress` surfaces when present. Record their actual rendered coverage and empty states rather than assuming a tab contains data.

When comments, activity, screenshots, attachments, logs, customer projects, or runtime validation matter, read [references/evidence-and-validation.md](references/evidence-and-validation.md).

## Load Local Context Progressively

Use the issue brief to choose the next evidence source. Search first, then read only the relevant section or the one or two most relevant records.

- Load project orientation when ownership, runtime entrypoints, or adjacent repositories are unclear.
- Search durable knowledge when the issue resembles a known mistake or recurring failure.
- Read issue-specific traces when an issue id, exact log text, symbol, version, or lifecycle matches.
- Read validation guidance when using downloaded projects, logs, private tests, hardware, or external services.
- Read delivery conventions only when the user asks to prepare a commit, push, or merge request.
- Expand to adjacent repositories only when the observed path crosses their boundary.

Before loading another substantial file, identify the unresolved question it should answer. Do not load it if it cannot materially answer that question.

Local summaries orient the investigation; current code, Git history, artifacts, and runtime observations establish proof.

## Select the Correct Code Baseline

Use the tested version evidence before interpreting current code. Check the current branch, commit, worktree state, and any in-progress Git operation before checkout.

Build a component-level baseline matrix before selecting a ref: rendered component/build string, precision (`exact commit`, `tag/version only`, `incomplete`, or `unknown`), owning repository, whether the ref resolves there, and whether the reported entrypoint exists at that ref. Do not substitute a nearby current-workspace symbol for an unavailable client application, middleware, or other component entrypoint.

- A clean worktree may switch directly to the verified target ref by default. Record the original branch and commit first.
- A dirty worktree must remain untouched. Use ref-qualified static inspection when sufficient; create a separate worktree when the target version must run.
- Never stash, commit, reset, discard, overwrite, or force-switch the user's changes merely to reach the tested version.
- If a separate worktree is created, report its path, ref, and remaining changes in the final answer. Creation need not pause the investigation.

Read [references/git-baselines.md](references/git-baselines.md) whenever the tested version differs from the current checkout, the worktree is dirty, a separate worktree may be needed, or branch ancestry affects the conclusion.

## Diagnose the Reported Symptom

Follow the real entrypoint and data/state ownership across every repository that participates in the reported path. Establish ordering, cache and object lifetimes, configuration overlays, background work, and the point where the observed symptom is emitted.

Keep these categories explicit:

- rendered issue evidence;
- current code facts;
- commit-specific code facts;
- runtime or log observations;
- inference;
- competing explanations;
- unknowns.

Do not replace the work-item title or name with a broader theory. Separate workflow correctness from observability defects such as duplicate, absent, delayed, or misleading logs. A failed implementation or experiment invalidates that result, not automatically the underlying proposal.

Use the exact acceptance signal. Do not substitute a nearby warning, duplicate call, successful import, static call path, or syntax check for the behavior the issue reports.

## Delegate When It Adds Independent Evidence

Multiple sub-agents are allowed and recommended for complex issues, but never required. For one issue, the primary agent must complete the browser gate and authoritative issue brief before delegation. For a batch, the primary agent must first complete the shared login/permission gate, establish the batch scope and read-only boundary, and assign one issue per acquisition worker; each worker must then create the authoritative brief for its assigned issue before deeper analysis.

Delegate independent read-only evidence streams such as version ancestry, cross-repository call paths, log timelines, validation design, or adversarial review. Keep Git/worktree selection, scope, synthesis, and all non-local side-effect decisions with the primary agent. For a batch of issues, the primary agent may delegate issue-specific in-app Browser acquisition in parallel only under the isolation rules in [references/delegation.md](references/delegation.md). Any flow that writes to a shared Downloads directory remains serialized.

Read [references/delegation.md](references/delegation.md) before spawning sub-agents for this skill.

## Preserve Authorization Boundaries

Default to read-only diagnosis. Phrases such as “分析即可”, “评估即可”, “验证即可”, or “先找出来” do not authorize business-code edits, remote changes, commits, pushes, or merge requests. Feishu issue state remains read-only under this skill even when the user later authorizes a local code implementation.

When implementation is authorized, make the smallest change that repairs the proven invariant and validate it at the strongest available layer. Keep private fixtures and customer data out of tracked files.

Treat push and merge-request creation as a separate gate. “先不要 push” remains in force until the user explicitly reverses it for the current issue. Never inherit publication authority from another issue or an earlier task.

## Report by Evidence Strength

Lead with the current conclusion, then report:

- issue and tested baseline;
- confirmed cause or leading hypotheses;
- evidence and exact locations;
- validation actually performed;
- what remains unverified and why;
- files, worktrees, or local artifacts created;
- the retained evidence root and comment, image, attachment, failed, unverified, and cleaned counts when local acquisition ran;
- whether any code, remote state, issue, commit, push, or merge request changed.

Distinguish documentation claims, static code proof, focused tests, real-project replay, and full GUI/GPU/customer-runtime validation. Never promote one layer into another or invent `TEST` wording.
