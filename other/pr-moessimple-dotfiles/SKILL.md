---
name: pr
description: Turn the current branch into a pull request whose description tells the problem, the outcome, and the evidence behind it, then create it (or refresh an existing one) with gh after an independent review and approval.
disable-model-invocation: true
---

# Create or refresh a Pull Request

Turn the current branch into a pull request. Write the description for a reviewer who does not have your context, a person or an agent reading it later: it carries the problem, the outcome, and, when the design is not obvious, the decision behind it. The line-by-line implementation stays in the diff; do not retell it in prose.

The skill has two modes, decided by whether a PR already exists for this branch:

- **Mode A (create):** no open PR for this branch yet. Write the description and open the PR.
- **Mode B (refresh):** an open PR already exists. Regenerate the description from the current branch and update the PR, so it never lags behind changes made after it was opened.

Both modes run the same context-gathering, the same review, and the same prose craft. They differ only at the human checkpoint and the final `gh` call.

**REQUIRED SUB-SKILL:** Use the `outcome-writing` skill for every sentence of the title and description. It owns the prose craft (problem first, outcome over mechanism, precise terms but no code-internal names, and the self-review checklist). This skill owns only the PR-specific structure and mechanics below.

## Current state

Run and inspect:

- `git branch --show-current`
- `git status --porcelain`
- `git log --oneline -10`
- `gh pr view --json url,state --jq '.state + " " + .url' 2>/dev/null || echo none`
- `git default-branch` for the default branch, used as `{defaultBranch}` below. If it prints nothing or fails, stop and tell the user: every later step depends on it.

## Step 1: Preflight

Check the state above. Stop and tell the user if any of these apply:

- **On the default branch** (whatever `{defaultBranch}` is, for example `main`, `master`, or `production`). A PR needs a feature branch. Offer to create one that takes over the current commits.
- **Uncommitted changes exist.** They will not be part of the PR. Ask whether to commit them first or proceed without them.

When stopping, present the options as a short numbered list, not as an open question.

**Establish the mode** from the `gh pr view` output above:

- `none` → **Mode A (create)**.
- `OPEN <url>` → **Mode B (refresh)**.
- `MERGED <url>` or `CLOSED <url>` → stop. Tell the user this branch's PR is already merged or closed; a fresh PR needs a fresh branch. Do not continue.

State the chosen mode in one sentence before moving on.

## Step 2: Gather context

Steps 1 to 3 run in order, each depends on the previous. Steps 4 to 6 do not depend on each other and can run in parallel once step 1 found commits.

1. `git log {defaultBranch}...HEAD --oneline` for the commits on this branch. If empty, stop: there is nothing to open a PR for.
2. `git diff {defaultBranch}...HEAD` for all changes
3. **Mode B only:** `gh pr view --json title,body` for the PR's current title and description. This is the text you are about to replace; you need it to show a before/after and to spot hand-written content.
4. Read `SPEC*.md` (root, `docs/`, `docs/specs/`, or `spec/`; includes per-module `SPEC-<name>.md`), `tasks/plan.md`, and `tasks/todo.md` if they exist
5. Check the current conversation for a shipping report, a diagnosis, and test or command output on these changes. A shipping report feeds the Limitations section; if it ended NO-GO, say so in one sentence and let the user decide, do not block. A diagnosis is the source for a bug's cause, and test or command output is the source for Validation. For a user-visible change, collect the local screenshots or recordings and device checks made for it; this skill does not capture them itself, so ask the user when they are missing.
6. The repository's conventions:
   - A PR template: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, any file in `.github/PULL_REQUEST_TEMPLATE/`, or the same names in the repository root or `docs/` (case-insensitive).
   - Pull request rules for agents and contributors: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.github/copilot-instructions.md`, and files under `.ai/guidelines/`. Read only the parts about pull requests, review, validation, and evidence.
   - A title lint config (`.commitlintrc*`, `commitlint.config.*`), and otherwise the title style of recent merged PRs by people, not bots: `gh pr list --state merged --limit 10 --json author,title --jq '.[] | select(.author.is_bot | not) | .title'`. Look for a conventional-commit prefix (`fix:`, `feat(scope):`), a version prefix (`[13.x]`), or plain sentences.

**Choose the description format:** the **repository template** if one exists, otherwise a **description structure prescribed by the repository's PR rules**, otherwise the **default template** from Step 4. Nothing else defines the format, including past PR descriptions, which may have been written by an earlier version of this skill. Name the chosen format to the user in one sentence.

**Repository rules take precedence.** A requirement from the repository's PR rules or from a template's prompts (a required verdict, evidence, check, or section) applies on top of this skill, and where the two differ, the stricter one wins. If a requirement cannot be met, tell the user before Step 5 which one and why; do not publish around it silently.

**Verify the artifacts match this branch before using them.** Spec and task files can be relics of earlier work. Cross-check them against the diff. Use an artifact only if it clearly describes this change. If it describes something else, ignore it, tell the user in one sentence that stale artifacts were ignored, and continue down the priority list below.

The **problem** comes from, in order of priority:

1. The motivation supplied in the current request, if any
2. The spec file, the deliberate and curated source
3. The current conversation, if there was meaningful discussion about the motivation
4. **Mode B:** the problem statement already in the current PR description, if it still fits the diff
5. None of the above: ask the user once what the change does and why it was made

The **what changed** content prefers completed task descriptions from `tasks/todo.md` over re-deriving outcomes from the raw diff.

The **cause** of a bug comes from a diagnosis in the current conversation, a reproduction, or a failing test. If the cause was never established, do not reconstruct one from the diff; say in the description that the fix addresses the symptom and the cause is unconfirmed.

The **approach rationale** comes from the design discussion in the current conversation, a design or "alternatives considered" section in the spec, or an ADR. If none of those exist and the approach was not discussed, do not invent a rationale; leave it out of Changes.

Commit messages are never a source for the title or the story. They are often WIP commits and carry no reliable meaning. Use them only to see which commits belong to the branch.

## Step 3: Independent review

Every PR gets an independent review of the exact commit being published before its description is written.

1. Record the reviewed range: base `git merge-base {defaultBranch} HEAD`, head `git rev-parse HEAD` (both shortened to 7 characters). The base is the merge base because `git diff {defaultBranch}...HEAD` compares against it, not against the current tip of the default branch.
2. **Reuse:** if this session, or in Mode B the current PR description, already reports a review of the same head (and, for a user-visible change, of the same captures), keep that result and skip to Step 4.
3. Run the `code-review-dispatch` skill as a report-only run on the diff from Step 2 and its file list. Give it the problem from Step 2, any repository PR rules, the validation results collected so far, and the known limitations, so it judges the change against its intent and can tell whether the tests that ran actually cover it.
4. Set the **code verdict** with the same rule as the `review` skill: **FAIL** if any Critical finding is open, **PASS WITH REMARKS** if any Important finding is open, otherwise **PASS**. If the repository's PR rules or template require a plain PASS or FAIL, report PASS WITH REMARKS as PASS with the open Important findings listed, and use the repository's wording for the verdicts (for example `CODE: PASS`, `VISUAL: PASS`).
5. **Visual verdict**, only when the change alters something a user sees or touches (UI, layout, interaction, motion): read `references/visual.md` and run the visual review it describes. For a change with nothing visible, there is no visual verdict; the description says why in one sentence.
6. **Any FAIL:** show the findings and stop. The user decides: fix them first, or publish with the verdicts and the open findings stated in the description. If the repository's PR rules require a PASS before publication, publishing with a FAIL is not an option; only fixing is. After fixes, the head (or the captures) has moved: start again at Step 2, and give the new review the earlier findings and how each was addressed, so it checks the fixes instead of starting blind.

The description records the review so a reader knows which exact revision was checked, by what kind of reviewer, with which result and which limits. Describe the reviewer as "a separate read-only agent", not by an internal skill name: the name means nothing to a reader outside this setup, and Rule 2 keeps tool attribution out of the PR.

Never write a verdict for a review that did not run on the head being published. Do not apply any finding yourself; fixing is the user's decision.

## Step 4: Write title and description

Apply the `outcome-writing` skill throughout.

Determine the PR language before drafting, following the applicable output-language rules. English instructions
and examples do not prescribe the output language. Preserve required technical tokens such as `fix:`, `feat:`,
`BREAKING CHANGE:`, and `Closes #N`.

Write the description for the **whole branch diff against the default branch**, not just what changed since the PR was opened. In Mode B you are rewriting the description to match the current state, not appending a delta.

If a ship report exists, its Blockers, Recommended fixes, Acknowledged risks, and rollback trigger conditions are the primary source for the Limitations section. Only add what the report missed. Without a report, derive them from the diff: migrations (rollback possible, data loss risk), behavior changes that could break callers, missing test coverage, changes to shared infrastructure, security implications.

The Validation section comes from what was actually run or checked during the session (test commands, manual checks, a shipping report's test evidence), never invented after the fact. If nothing was verified beyond writing the code, say so plainly rather than omitting the section.

The Changes section is a deliberate exception to the `outcome-writing` skill's "outcome over mechanism" rule: keep the cause and the design decision through the self-review checklist even though the checklist would otherwise trim them. Class, method, and file names are allowed here, because the reader of this section has the diff open.

**Title.** Follow the convention found in Step 2 (prefix style, version bracket, casing). The text after any prefix is a complete imperative sentence that states the outcome and stands alone, under 72 characters ("fix: validate payment details before checkout", not "fix: bug" or "Update OrderController"). Without a convention, use the sentence alone ("Validate payment details before checkout"). Derive it in order of priority: the spec title, the plan's goal statement in `tasks/plan.md`, or the problem condensed to one line. Never from commit messages. If no artifact yields a clear title, ask the user.

**Repository template.** If Step 2 found one, fill it instead of the default template below; the repository's readers expect its structure. Preserve its headings unless repository rules or the current task explicitly allow changes. If there are several, pick the one that fits the change and name it to the user. Put the content the default template would carry (problem and outcome, changes and cause, validation, limitations) into the sections that match. Validation and limitations are never dropped: if no section fits them, put them in the closest one (for example additional information). Remove the template's HTML comment prompts once their requirements are met (see "Repository rules take precedence" in Step 2). A section that does not apply says so in one sentence and why. Report the review from Step 3 (both verdicts, if there was a visual one) in the section that fits it (a review, reviewer notes, or additional information section). If none fits, do not add one to the repository's template: report the verdict to the user in Step 5 instead, and if the user publishes a FAIL, state the open Critical findings in the section closest to limitations or risks.

**Prescribed structure.** If Step 2 chose a structure prescribed by the repository's PR rules, follow it the same way as a repository template: its headings, their order, and its form, with the default template's content placed where it fits.

**Default template.** Otherwise use the section order and content requirements below. Translate human-readable headings and example wording into the selected PR language, including those in the **with media** variant. Every section is present. A section that does not apply says so in one sentence and why. Pick the **with media** variant when the change alters something a user sees or touches (UI, layout, interaction, motion), otherwise **text only**. If the user asks for text only on such a change, use text only: the captures still go to the visual review in Step 3 but stay out of the body, and the device results go into Validation.

Text only:

```markdown
## Summary

{If the issue is known, start with `Closes #N.` Then 1 to 3 sentences: what was broken, missing, or painful before this change, for whom, and what happens now. Include why the change is needed.}

## Changes

{Short bullets with only the implementation details and tradeoffs that help a reviewer assess the change, not a file-by-file walkthrough. For a bug fix: the cause as the mechanism that produced the symptom, and why the fix addresses it; or that the cause is unconfirmed. When the design is not the obvious one: why this approach over the alternatives, what constraint forced it, what was rejected and why. Where a reviewer should look closely, if anything is non-obvious. Side changes that do not serve the main change get their own bullet with the reason.}

## Validation

{Exact commands or scenarios and their results, only for checks that actually ran. Keep local checks and hosted CI apart: "Hosted CI: pending" unless a CI result belongs to the head being published. Report failed or unavailable checks explicitly, with the reason; a check that failed or could not run is not a pass. Keep pre-existing failures and environment blockers apart from regressions caused by this change. For a changed mobile interaction: device, operating system, browser, and whether that was hardware, a simulator, or emulation.}

## Independent review

{From Step 3: "A separate read-only agent", base and head, the code verdict, open Important findings for PASS WITH REMARKS, open Critical findings if the user chose to publish a FAIL, and the limits of the review (for example, tests it did not run).}

## Limitations

{Remaining risks (what could go wrong, under what condition), missing evidence, unverified behavior, environment blockers that kept a check from running, what the PR deliberately does not change when a reviewer would otherwise have to check it, and related problems left for another PR. If there is nothing: "None".}
```

With media: the text only template plus the Visual evidence section, laid out in `references/visual.md`.

Before showing the draft, run the `outcome-writing` self-review checklist against it. Then check that every claim traces to a source from Step 2 or Step 3. Revise until every check passes.

## Step 5: Human checkpoint

**Mode A.** Show the title and the full description, ask whether both fit, and state that the PR will only be created after confirmation.

**Mode B.** Show the current title and description next to the proposed ones, so the user sees exactly what changes. Then, before asking for approval:

- **Flag content that would be lost.** If the current description contains anything the regenerated version does not reproduce (hand-written notes, reviewer answers, linked issues or checklists, extra sections), list each item and ask whether to keep it. Do not drop it silently.
- **Detect a no-op.** If the regenerated description says the same things as the current one, tell the user the existing description already matches the branch and stop. Do not push an edit that only reshuffles words.

State that the PR will only be updated after confirmation.

Wait. Do not continue until the user explicitly approves (Rule 1). Treat hedged responses ("probably fine", "should be ok", "looks fine I guess") as NOT approved. If they request changes, apply them and show the updated description again before continuing.

## Step 6: Create or update the PR

Everything below runs after the human checkpoint in Step 5. Pushing and the `gh` write rely on the session's own permission settings. Expect a permission prompt when required.

Add one `--attach './path.png#label'` per local image referenced in the description.

**Mode A (create):**

1. Push: `git push -u origin HEAD`
2. Check for an existing PR: `gh pr view --json url --jq '.url'`. If a URL is returned, the PR already exists (it was opened since preflight). Switch to Mode B step 2 below instead of creating a duplicate.
3. Create with the approved title and description:

```bash
gh pr create --title "the title" --body "$(cat <<'EOF'
## Summary
...
EOF
)"
```

**Mode B (refresh):**

1. Push any new local commits: `git push`
2. Update the PR with the approved title and description:

```bash
gh pr edit --title "the title" --body "$(cat <<'EOF'
## Summary
...
EOF
)"
```

Return the PR URL.

## Rules

1. Never create or update the PR before the human approved the description. Not even for trivial changes.
2. No AI attribution anywhere in the PR: no "Generated with" footer, no co-author line, no mention of Claude. No "Test plan" section either.
3. Never open or refresh the PR for a change you cannot explain yourself. If a hunk in the diff does not trace to a reason you can state, say so to the user before writing the description, do not paper over it with vague prose.
4. In Mode B, never discard hand-written content from the existing description without the user's explicit say-so (Step 5).
5. Never invent evidence. A cause, a rationale, a test result, a review verdict, an image, or a "does not change" claim appears only when it was established in the session or checked against the diff. Without a source, leave it out or ask.
6. The body stands on its own for a reader who was not in this session. No conversation history ("as discussed", "after several attempts"), and no links to planning artifacts (`SPEC*.md`, `tasks/`, `docs/specs/`), which are not committed.
7. Nothing private in the body: no secrets, credentials, personal data, internal hostnames, or machine-specific paths. Validation shows the commands and their results, not raw output that carries these.

## Definition of Done

- Title and description follow the `outcome-writing` skill consistently throughout
- The Summary describes an experience or problem, not a diff
- The title follows the repository's convention, or is an imperative outcome sentence when there is none
- The description follows the repository's template if present, otherwise a structure prescribed by the repository's PR rules, otherwise the default template (text only or with media) with every section present
- The repository's PR rules and template requirements were met, or each unmet one was raised with the user before approval
- When the design is not obvious, Changes states why this approach and what was rejected
- A bug fix states its cause, or states that the cause is unconfirmed
- The description covers the whole branch diff, not just changes since the PR was opened
- Every part of the diff is accounted for in the description or was flagged to the user
- A review by `code-review-dispatch` ran on the exact head being published, and the description reports its range, verdict, and limits (Independent review, or the fitting section of a repository template)
- A user-visible change has a separate visual verdict on its captures and device results, reported apart from the code verdict
- Validation lists only checks that actually ran, with their results
- Every claim traces to a source from Step 2 or Step 3
- The human explicitly approved the description before `gh pr create` / `gh pr edit` ran
- Mode B: content that only lived in the old description was either carried over or explicitly dropped with the user's approval
- The PR body contains no AI attribution
- The PR URL is returned and accessible
