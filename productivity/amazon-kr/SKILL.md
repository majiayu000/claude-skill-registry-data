---
name: amazon-kr
description: Create, reference-replicate, revise, resize, or audit Amazon main images, secondary listing images, and A+ modules for physical products. Use for product fidelity, listing graphics, lifestyle/use scenes, and image export QA. Excludes PPC, inventory, and account operations.
---

# Amazon KR

Produce useful image assets constrained by the actual product. Geometry, parts, branding, material, color, use, and supported claims take priority over a richer scene or closer style match. For an explicitly requested concept, record the authorized transformations as the visual target and preserve all other product facts; identify the result as a concept rather than evidence of an existing sale variant.

## Execution contract

Identify the requested deliverable first. Creation, replication, and revision end in actual image files. Planning, copy, prompts, and audit end in those deliverables when requested; audit alone is read-only. Follow the relevant branch in [production-modes.md](references/production-modes.md), not every production step for every task.

Within the user's authorized scope, continue through production, verification, and defect correction. Reuse prior facts, decisions, and approvals while their scope remains valid. Ask only when a consequential unresolved fact or an explicit approval gate blocks the next dependent action. A question blocks only the affected output or step; continue independent authorized work. Silence is neither an answer nor approval.

Use `qa_passed` for an asset the Agent has checked against all applicable requirements. Use `user_approved` only for an explicit user approval and record what it covers. A QA-passed master can be reused without a new approval request. If the user asks to review a master or layout first, wait at that named gate before dependent production; the user's explicit correction authorizes that correction. Seek renewed approval only when proposing a material departure from an explicitly approved decision that the current instructions do not already authorize.

Producing and delivering files does not authorize store publication, additional purchases, or new service access. Use only tools permitted and available in the current environment. Preserve source files and masters; write revisions as new versions. Follow the user's requested scope and approval conditions over this skill's default workflow.

## Production workflow

Apply these steps to new production or substantial product editing. For local revisions, resize, audit, or intermediate deliverables, use the branch-specific scope and completion criteria.

1. **Inventory sources and outputs.** Record each requested output's purpose, authoritative product source, and target marketplace/module when relevant. Track dimensions as confirmed, provisional, or pending. Pending dimensions permit independent master/copy preparation; ratio-dependent layout needs a usable aspect ratio, and final export needs a confirmed or user-authorized target. Never present an assumed size as a verified upload requirement.
2. **Resolve only relevant product facts.** Use [product-intake.md](references/product-intake.md). Separate confirmed evidence, visual inference, requested changes, and blocking unknowns. Required source images must be requested when their absence would force invention of the real product; preserve source pixels or omit an unsupported nonessential view when that satisfies the task.
3. **Load relevant detail.** Read [reference-replication.md](references/reference-replication.md) for reference matching; [material-fidelity.md](references/material-fidelity.md) when generating or changing material appearance; [resizing.md](references/resizing.md) for canvas adaptation. [suction-hook-profile.md](references/suction-hook-profile.md) is an optional historical example only for matching geometry; current evidence controls.
4. **Build only the needed assets.** Choose the page set through the production branch. Reuse existing suitable masters; create a QA-passed master for each required angle, variant, finish, or use state that needs one. Compare it with authoritative product evidence before reuse.
5. **Compose and export.** Prefer isolating and editing the real product to regenerating it. Use generation for scenes and narrowly scoped reconstruction. Prefer deterministic tools for type, logos, arrows, layout, crops, and export: code or an available precise design editor may be used within the environment's tool rules. If only generated text is feasible, inspect it character by character and correct errors; unverified text, logos, or values cannot pass QA. Preserve physical proportions and perspective through crop, contain, re-layout, or matched extension.
6. **Inspect and correct.** Apply [visual-qa.md](references/visual-qa.md) to each final file. For local files, run `scripts/validate_images.py` with explicit target specifications, individually, in homogeneous groups, or through a per-file manifest. A script success covers only reported checks. If a check cannot be executed, use an available equivalent or record it as unverified; do not claim it passed.
7. **Deliver against the requested scope.** Return the actual files and a concise audit record with sources, target specifications, checks performed, corrections, and per-file disposition. A production task is complete only when every requested output exists, has passed applicable visual and technical checks, and has no unsupported factual claim. Respect any user-defined delivery approval gate.

## Correction and completion

Fix defects within scope without asking whether to continue. Repair the affected layer: copy/layout, scene, master, or export. Recheck the changed requirements and any affected cross-image consistency; a title correction does not require rebuilding a sound product master.

Each retry must address an identified defect using a meaningful change in method or input. When the same defect persists without improvement, switch to a more reliable edit, source, or simpler truthful composition within the requested scope. If no viable method remains, retain successful work and report the affected files, blocker, attempts, and smallest required input or capability. If no suitable image capability is available, provide the most useful production-ready fallback possible and explicitly leave the image-production task incomplete; do not claim that a plan or prompt is a generated image. Do not repeat an unchanged failing operation indefinitely or silently reduce the requested deliverables.

Track per-output status as `pending`, `reworking`, `waiting_for_input`, `waiting_for_approval`, `blocked`, `unverified`, or `qa_passed`. Use `blocked` when a required capability is unavailable or no viable production method remains; include the reason and recovery requirement. User approval is a separate record, not a substitute for QA. Deliver passed files when useful, keep incomplete/rejected files outside final folders, and state that the overall task remains incomplete when any requested output is blocked or unverified. For audit-only work, a complete report may correctly find that assets fail QA.

## Product and claim rules

- User-product evidence controls goods; reference designs control presentation. Preserve product identity and adapt incompatible reference elements.
- Keep geometry, parts, branding, colorway, finish, and mechanically plausible use consistent across repeated and sequential views. Preserve legitimate perspective changes rather than forcing every projected round surface into a circle.
- Match material response to the actual reference and brief; generic finish cues are aids, not grounds to override evidence.
- Include performance and compatibility claims only when supported by product evidence. Omit an unsupported nonessential claim and continue, noting the omission. If it is essential to the requested page, request substantiation and pause that page's dependent content.
- Distinguish real alpha transparency from a baked background pattern. A heuristic warning requires visual review, not automatic approval or rejection.
- When current Amazon compliance is asserted or required for delivery, verify relevant official Amazon/Seller Central rules and identify marketplace, category/module, and check date. If inaccessible, report compliance as unverified while continuing independent work. A mechanical resize does not automatically request a fresh policy audit.
- Use confirmed module/upload targets when a generic label conflicts with dimensions. Explain the conflict; incompatible aspect ratios require separate layouts. Historical dimensions are project examples, not platform-wide rules.
