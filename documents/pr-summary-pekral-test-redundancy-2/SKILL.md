---
name: pr-summary
description: "Use when summarizing current PR changes for the development and product team. Analyzes all commits in the current branch, explains what broke and what the fix changes, and produces a human-readable report that can be posted as a GitHub PR comment (Markdown), a JIRA comment (ADF), or a Bugsnag comment (plain text)."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## TL;DR

Read the branch's commits and its linked tracker. Write one non-technical comment. Publish it.

- **GitHub and Bugsnag render the same two sections** → `What changed`, then `How to test`.
- **`What changed`** → `Problem`, `Cause`, `Result`, `What I fixed`, plus two conditional fields.
- **JIRA renders one shape on every run** → a status line, `Acceptance criteria`, `Review findings`, `What changed`, `Impact after deployment`. An open question closes the bullet it belongs to. Its reader is a product manager, so the verdict comes first, the review is retold in plain language, `What changed` carries observable behaviour instead of a mechanism, and `Impact after deployment` names what to watch after the release. JIRA renders no `How to test`.
- **`How to test`** (GitHub and Bugsnag) → a scenario a human follows: every step names a concrete input and a must-hold outcome.
- **A closing line** links the PR and the source issue.
- Only the delivery format differs per target: GitHub Markdown, JIRA ADF, Bugsnag plain text.
- Prose is terse. Business "why" first, enough technical context to locate the change, nothing more.
- No code snippets, file paths, line numbers, diff fragments.
- Length follows the facts the report carries. There is no word budget on GitHub and Bugsnag; JIRA caps the comment at 3 000 characters.
- Publish through `upsert-comment.sh` — on GitHub and JIRA it updates this actor's existing comment in place, so one destination carries one permanent summary rather than a chain of them.

---

## Constraints

### Rules to apply

Each line states what the rule actually decides here, so its relevance is clear without opening it.

- Apply @rules/php/core-standards.md — the package-wide prose and code standards every skill is held to.
- Apply @rules/git/general.md — how the base branch is resolved and what the commit history this skill reads is expected to look like.
- Apply @rules/writing/general.md — the sentence shape of every line this skill authors, and the rule that decides how long the report is: one idea per sentence, active voice, one term per concept, no marketing register.
- Apply @rules/jira/general.md when the target is a JIRA issue. The template uses a constrained Wiki Markup source format. The canonical helper converts that source to ADF and publishes it through `--body-adf`.
- Apply @rules/reports/general.md — the published comment is written in the language of the source assignment (Czech assignment → Czech comment; English assignment → English comment). Code identifiers stay verbatim per the rule's *Scope clarifications*.
- If the current project uses Laravel, also apply `@rules/laravel/laravel.md`, `@rules/laravel/architecture.md`, `@rules/laravel/filament.md`, and `@rules/laravel/livewire.md` — they tell the summary what a change to an Action, a Livewire component, or a Filament resource means in business terms.

### What renders where

GitHub and Bugsnag carry the **same** structure and differ only in markup — no target gets a reduced shape, because the report carries nothing a tracker would need to omit. JIRA carries its own section order, for the reason *The JIRA shape* below states.

| Element | GitHub PR comment | JIRA comment | Bugsnag comment |
|---|---|---|---|
| Status line | no | yes — one to three sentences above the first heading | no |
| `Acceptance criteria` | no | yes — first section | no |
| `Review findings` | review-only run only, in place of `How to test` | yes — every run, second section | review-only run only, in place of `How to test` |
| `What changed` | yes — four fields, two conditional | yes — three to five behaviour bullets, third section | yes — four fields, two conditional |
| `Impact after deployment` | no | yes — at most five feature bullets, fourth section | no |
| `How to test` | yes, except a review-only run | no | yes, except a review-only run |
| `{embedded_blocks}` | conditional — exactly as the wrapper passed them | no — each question closes its criterion or finding bullet | conditional — exactly as the wrapper passed them |
| Closing links line | yes | yes | yes |
| Footer | no | yes — the comment is generated, for the ticket owner | no |
| Length cap | none | 3 000 characters | none |
| Markup | GitHub Markdown | ADF at the API boundary; the template's Wiki Markup is intermediate input only | plain text; no markup at all |
| Template | `templates/pr-summary-github.md` | `templates/pr-summary-jira.md` | `templates/pr-summary-bugsnag.md` |

### The JIRA shape — verdict first, behaviour before deployment impact, no mechanism

A JIRA ticket is read by the person who asked for the work, so that comment answers one question before any other: is the assignment satisfied. Every run renders the same shape — a review-only run, a code-review mirror, the post-convergence report, and the merge-readiness TL;DR alike — and `templates/pr-summary-jira.md` is where it is rendered:

1. **A status line opens the comment** — one to three short sentences above the first heading: the state of the work, whether the change is ready to merge or what blocks it, and whether anything was merged or deployed.
2. **`Acceptance criteria` is the first section**, carrying one verdict sentence plus a bullet only for a criterion that is unmet, partially met, or awaiting a human's confirmation. Satisfied criteria are never enumerated one by one. On JIRA the assignment verdict reaches the reader here rather than through `{embedded_blocks}`.
3. **`Review findings` is the second section** — the newest GitHub pull-request review, retold in plain language. One bullet per finding: what can go wrong for the user or the business, and what the fix would change. A point that blocks the merge comes first and says so in words, never with a severity label. **A finding outside the assignment** — a pre-existing defect, or behaviour the assignment does not ask for — **appears only when it is Critical**; every other one stays on the pull request. When the review found nothing to report, or no review has run yet, the section is one sentence that says so.
4. **`What changed` is the third section and carries observable behaviour, not mechanism** — three to five bullets of observable behaviour, in before → after form where a before exists. The `Problem` / `Cause` / `Result` / `What I fixed` fields are not rendered on JIRA: `Cause` asks for a mechanism, and a mechanism is what puts method names in a product manager's ticket.
5. **`Impact after deployment` is the fourth section** — the parts of the application a production deployment can affect, so the ticket owner knows what to watch after the release.
   - One bullet per feature, at most five: the feature in plain language and what a user there may notice, or that nothing visible should change.
   - Source: the features the diff changes, plus the newest review's `## Affected behaviour outside the diff` (`@rules/code-review/core-analysis.md`), retold as features, never as files or methods.
   - When no code-review comment exists for the current head yet, derive the parts from the diff and say in the first bullet that the review has not confirmed them.
   - When the review comment carries no `## Affected behaviour outside the diff`, the review found no affected part outside the diff: list only the features the diff changes, with no caveat.
6. **No `Clarifying questions` section on JIRA.** Each open question is the closing sentence of the bullet it belongs to. A question about an acceptance criterion closes that criterion's bullet in `Acceptance criteria`, and the criterion is then reported as unmet, partially met, or awaiting a human's confirmation. A question that concerns no criterion — a documentation mismatch, a blocking documentation request, a Critical decision outside the assignment — closes its `Review findings` bullet. A question may carry one recommendation sentence after it.
7. **No `How to test` on JIRA.** The steps a tester follows live on the GitHub pull request, whose description carries them (`@rules/git/pull-requests.md` *Testing*). The footer under the closing links line states that the comment is generated automatically and is written for the ticket owner.

`@rules/reports/general.md` *A JIRA comment is written for a non-technical reader* is binding on this comment. It lists the content that never appears in it, its exceptions, and the 3 000-character cap. Do not restate that list here — apply it.

### The section names are translated, the concepts are not

The headings and field labels above are this skill's canonical **concepts**, written in English because the skill itself is. The rendered comment follows the assignment language per `@rules/reports/general.md`, headings and field labels included — a Czech assignment renders `Co se změnilo` / `Problém` / `Příčina` / `Výsledek` / `Co jsem opravil` / `Vedlejší přínos` / `Na jiný ticket` / `Jak otestovat`, and a Czech JIRA ticket renders `Akceptační kritéria` / `Nálezy z kontroly kódu` / `Co se změnilo` / `Co může změna ovlivnit po nasazení`. Never publish an English heading above assignment-language prose; that is the bilingual mixing the rule bans.

### What changed — four required fields, two conditional ones (GitHub and Bugsnag)

Required, always rendered, in this order. On JIRA this section renders as behaviour bullets instead — see *The JIRA shape* above:

- **Problem** — what the reader's own world looked like when it was broken: who hit it, on what, what they saw instead. Name the scale when it is known (how many attempts, over how long, how many accounts).
- **Cause** — why it happened. One mechanism, stated so a non-developer follows it. This is where a missing or partially met acceptance criterion is named in prose, never as a verdict field.
- **Result** — what the cause actually cost: the number, the runtime, the silent failure it produced. When a failure was silent, say why it was silent.
- **What I fixed** — a bullet list, one bullet per change the reader can observe. Each bullet states the new behaviour and, where a number exists, the before-and-after.

Conditional — render only when it has content, never as an empty field:

- **Side benefit** — an improvement the fix produces that the assignment never asked for (load removed from a shared system, a class of failure that can no longer happen).
- **Filed separately** — a genuinely unrelated defect found during the work and filed on its own ticket. Name the ticket and state that it is linked.

### How to test — a scenario, not a checklist of tests

`How to test` is what a human does, in the application's own domain. It is never a list of automated tests and never a code-level instruction. It renders on GitHub and Bugsnag; a JIRA comment carries none (*The JIRA shape* above).

- Every step names **concrete inputs**: the account, the URL, the entity name, the value typed in.
- Every step states an explicit **must-hold outcome** — what the tester must see for the step to pass.
- Order the steps by what matters. When one step is the important one, say so in that step.
- When the change is reachable only behind a test parameter — a feature flag, an ENV switch, a query-string parameter, a request header, an A/B variant, a beta toggle, or an allow-listed account — the **first** step enables it, naming the exact toggle and the value required. There is no separate metadata line for it on any target; the toggle lives inside the step that enables it.
- Cover the regression too: name the neighbouring flows the tester should exercise to confirm nothing else moved.
- **A review-only run replaces the section.** See *Review-only run* below.
- **Caller-supplied steps win.** When the caller (for example `april` in post-convergence reporting mode) passes pre-authored steps derived from designed test scenarios, use those steps as passed — never compressed, never rewritten. The caller's scenarios are the source of truth for this section.

### An unmet criterion addresses the author

When the assignment verdict names a criterion that is not met or partially met, the comment states why and mentions the author of the changes (`@rules/code-review/general.md` *The author of the changes is the account that pushed the pull request*).

- **State why.** Each unmet criterion names what the change does not do and what the review observed that shows it, in plain prose.
- **Mention the author once, after the unmet criteria.** One sentence asks the author to confirm the claim and fix the gap, or to refute it in a reply. On JIRA it sits at the end of `Acceptance criteria`; on GitHub and Bugsnag it follows the embedded blocks.
- **The mention syntax is the tracker's own.**
  1. GitHub: `@<login>` of the pull request's `author.login`.
  2. JIRA: `[~accountid:<id>]`, which the JIRA publish helper converts to an ADF mention. Resolve `<id>` from the JIRA accounts the loader returns (`assigneeAccountId`, a comment's `authorAccountId`) whose name or e-mail matches the pull request's author or commit author, or through the JIRA MCP server's user lookup.
  3. Bugsnag: the author's name as plain text, because the helper carries no mention.
- **Never guess an account.** When no JIRA account resolves, write the author's name as plain text and state the unresolved mention in the handoff.
- **Every criterion met: no mention.** The author stays internal information.

### Review-only run — `Review findings` in place of `How to test`

A review-only run (`/report-code-review`) passes `review-only` together with the findings of the published GitHub pull-request comment. Then:

- **Skip step 7.** Render no `How to test` section on any target. A test-parameter toggle has no step to live in, so it is not rendered either.
- **Render `Review findings` in the position of `How to test`.** The section retells the technical GitHub report so a non-technical reader understands what the review reported and can respond to it. A JIRA comment carries the section on every run already, in the shape *The JIRA shape* above defines; the bullets below apply to all three targets.
  - Write one bullet per finding: what can go wrong for the user or the business, and what the fix would change. Plain prose only.
  - Put the points that block the release first, and say in words that they block it. Never write a severity label.
  - The list in `@rules/reports/general.md` *Never in a JIRA comment* binds this section on every target: no severity labels, finding counts, code names, file paths, or rule references.
  - On GitHub and Bugsnag, end with one sentence that asks the reader to reply in a comment when they disagree with a point or know something that changes it. On JIRA the footer carries that role, so no closing sentence is added.
  - On JIRA, a finding outside the assignment appears only when it is Critical (*The JIRA shape* above).
  - End the bullet that retells a missing-test or a DRY finding with the author mention, and retell `## Missing tests added` as one bullet that names what the added tests protect and ends with the same mention. The syntax is the one *An unmet criterion addresses the author* above defines (`@rules/code-review/general.md` *The author of the changes is the account that pushed the pull request* → *Second exception*).
  - When the review found nothing and the missing-tests commit added no test, render one sentence that says so, and no bullets.
- **Always a new comment.** Pass `--create` as the first argument of the GitHub and JIRA publish helpers, so every review-only run leaves its own comment and never updates an earlier one. The Bugsnag helper creates a new comment on every run already.
- **Length on JIRA.** When the comment overflows the 3 000-character cap, shorten `What changed` first, then merge `Impact after deployment` bullets. Never drop a `Review findings` bullet.

### An issue with several pull requests

When the issue links more than one pull request, render the issue-level verdict once and group everything that retells one pull request under its own heading, per `references/several-pull-requests.md`. A run that reviewed one of them rewrites only that group and carries the others over.

### Closing line — the PR and the source issue

The comment ends with one line linking the pull request and the source tracker item, separated by ` · ` — a `PR #123` link, then an `ECOMAIL-6974` link, each written in the target's own link syntax (see the three templates). Render whichever of the two links exists; when neither exists, omit the line. It is a navigation aid, never prose, and it is never compressed or translated.

### Length follows the facts

On GitHub and Bugsnag there is no word budget and no "fits on one screen" rule. The report is as long as the facts it carries, and no longer. `@rules/writing/general.md` decides the shape of every sentence in it.

- **Never pad.** Do not restate the process, do not narrate what the run did, do not add a closing summary of what was already said.
- **Never truncate a fact** to hit a length. A dropped number, boundary, or must-hold outcome costs the reader the decision the report exists to support. On GitHub and Bugsnag there is no length to hit, so nothing ever forces the choice; on JIRA the cap below is met by carrying fewer facts, never by cutting one in half.
- A one-line fix produces a short report. A change with a measured cause, a measured result, and four things to retest produces a long one. Both are correct.

**JIRA is the one exception, and its cap is real.** That comment carries a 3 000-character limit, because its reader is a product manager rather than a developer (`@rules/reports/general.md` *A JIRA comment is written for a non-technical reader*). Meet the cap by carrying fewer facts, never by truncating one. When the body overflows, shorten `What changed` and drop its least consequential behaviour bullet whole, then merge `Impact after deployment` bullets; never drop an `Acceptance criteria` bullet or a `Review findings` bullet, because those are what the reader decides on. A JIRA body that cannot fit within 3 000 characters without cutting one of them is carrying content the banned list already forbids.

### What the comment carries

- Focus on the "why" and business impact, not on implementation details — but keep enough technical context (which integration, payload, table, endpoint, etc.) that a developer can still follow what changed.
- Do not include code snippets, file paths, line numbers, or diff fragments. The summary is for humans, not for static analysis.
- Do not restate the acceptance criteria as a checklist and do not publish a coverage verdict. `@skills/assignment-compliance-check/SKILL.md` owns the assignment verdict. On GitHub and Bugsnag it reaches this comment through the `{embedded_blocks}` slot, and this skill authors no verdict sentence of its own there: it renders the block it was passed. On JIRA that same verdict renders into the `Acceptance criteria` section, so the section carries it rather than the slot. Either way it reaches the reader on every CR run with a linked tracker — met, not met, or no criteria stated (`@rules/code-review/general.md` *Two-Part CR Output* → *The tracker comment carries the same verdict — in all three cases*). A checklist of satisfied criteria is never rendered on any target.

### Terse output style (issue #51)

Every authored sentence carries a fact and nothing else. Apply `references/terse-output-style.md` in full before you write: what to drop, what stays verbatim, and the auto-clarity carve-outs (`Cause`, `Result`, security warnings, must-hold outcomes).

### Output shape per target

- GitHub and Bugsnag output the **two sections plus the closing line**: `What changed` (four required fields, two conditional), `How to test`, then the PR / issue links. JIRA outputs the status line, `Acceptance criteria`, `Review findings`, `What changed`, `Impact after deployment`, the PR / issue links, and the footer.
- No target renders an `Authors` line, an `Available behind` line, a `Summary of changes` section, a categories list, a breaking-changes section, or a testing-notes section. This skill resolves no authorship — a caller that needs an author set resolves it itself.
- Between GitHub and Bugsnag the only difference is markup and template. JIRA differs in section order and content too, per *The JIRA shape* above.

### No leaked markup on JIRA

The JIRA body uses only the helper's supported Wiki Markup subset, and the reader never sees a raw `**` or `#`. Before publishing, convert or reject every leaked Markdown construct per `references/markup-per-target.md` and `@rules/jira/general.md`.

### No markup at all on Bugsnag

Bugsnag renders plain text: no headings, bold, inline code, or bracket links. `references/markup-per-target.md` defines the shape.

### Embedded blocks (consolidation contract — issue #498)

When the calling CR wrapper passes extra markdown blocks (the `Clarifying questions` block and/or the `Assignment Compliance` block returned by `@skills/assignment-compliance-check/SKILL.md`), append them **verbatim** after `How to test` and **before** the closing links line.

- **On JIRA there is no slot.** The `Assignment Compliance` verdict renders into the `Acceptance criteria` section, and each `Clarifying questions` entry becomes the closing sentence of the criterion or finding bullet it belongs to (*The JIRA shape* above). The caller passes each question together with the criterion or the finding it concerns. A merge-preparation run passes its JIRA questions the same way (`@skills/verify-merge-readiness/SKILL.md` step 4). The `Assignment Compliance` verdict renders into the `Acceptance criteria` section instead of travelling through the slot, per *The JIRA shape* above.
- Each embedded block must already use the target tracker's source format (GitHub Markdown for GitHub, the supported intermediate Wiki Markup subset for JIRA, plain text for Bugsnag).
- The resulting comment is published once per linked tracker target — that single consolidated comment is the only non-technical artifact a CR run posts on each linked issue, JIRA ticket, or Bugsnag error.
- When no embedded blocks are passed, the template renders without that slot. This is the shape of a non-CR invocation (for example `april` in post-convergence reporting mode), never of a clean CR result.
- On GitHub and Bugsnag this slot is how the assignment verdict reaches the reader, and on a CR run it carries that verdict on **every** run with a linked tracker — the affirmative one included; on JIRA the `Acceptance criteria` section carries the same verdict under the same rule. Silence is never the clean signal, because a tracker comment in which "every criterion is met" and "nobody checked" look identical is a defect (`@rules/code-review/general.md` *Two-Part CR Output* → *The tracker comment carries the same verdict — in all three cases*). This skill authors no verdict, no banner, and no "satisfies the assignment" sentence of its own — it renders the passed block verbatim, and the block is the verdict.

---

## Steps

Eight numbered steps, three independent jobs. The headings below are the jobs; the numbering runs continuously so a step can still be cited by number.

### Load context (1–4)

1. Identify the current branch and its base branch (usually `master` or `main`).
2. Load all commits in the current branch since it diverged from the base branch (`git log base..HEAD`).
3. For each commit, read the commit message and the diff to understand what changed and why.
4. If a PR already exists for this branch, load the PR description and linked issue(s) for additional context (business motivation, acceptance criteria, reporter's expectations):
   - **GitHub:** `skills/code-review-github/scripts/load-issue.sh <URL>` — always the full GitHub URL, never a bare number (the loader rejects it); read `body`, `comments[]`, and `closingIssues[]` off the resulting JSON document.
   - **JIRA:** `skills/code-review-jira/scripts/load-issue.sh <KEY|URL>` — read `descriptionText`, `comments[]`, and linked PRs. Also load the pull request through `skills/code-review-github/scripts/load-issue.sh <PR_URL>` and read the newest code-review comment (`cr-comment` marker): it is the source of the JIRA `Review findings` section, and its `## Affected behaviour outside the diff` section feeds `Impact after deployment`.
   - **Bugsnag:** `skills/code-review-bugsnag/scripts/load-issue.sh <URL|TRIPLE>` — read the error context, its `comments[]`, and its linked issues / PRs.
   - Never call `gh pr view`, `gh issue view`, or `acli` directly; fall back to the GitHub / JIRA / Bugsnag MCP server only when the loader is unavailable (exit code 2/3).

### Decide the target (5)

5. Detect the **target tracker** for the comment by following the table in `@skills/resolve-issue/references/source-detection.md` (branch name / PR description / linked issue trail):
   - **JIRA** — the branch or PR description matches a JIRA issue-key regex (e.g. `^[A-Z][A-Z0-9_]+-\d+$`), or the JIRA loader from step 4 returns a non-empty document. Use `templates/pr-summary-jira.md` as intermediate source for the ADF publisher.
   - **Bugsnag** — the caller named a Bugsnag error URL or `organization/project/error` triple, or the Bugsnag loader from step 4 returns a non-empty document. Use `templates/pr-summary-bugsnag.md` (plain text).
   - **GitHub** — otherwise, or when the user explicitly asks for a PR comment. Use `templates/pr-summary-github.md` (GitHub Markdown).
   - If several signals match (a cross-tracker PR), prefer the tracker named in the user's invocation. Absent that, prefer the tracker the assignment itself came from, so the reporter reads the answer where they asked the question.

### Write and publish (6–8)

6. **Write the body sections.** On GitHub and Bugsnag, write `What changed` — the four required fields in order (`Problem`, `Cause`, `Result`, `What I fixed`), then the two conditional ones (`Side benefit`, `Filed separately`) only when each has content. On JIRA, write the status line, then `Acceptance criteria` from the assignment verdict, then `Review findings` from the newest pull-request review per *The JIRA shape*, then `What changed` as three to five observable-behaviour bullets, then `Impact after deployment`. Derive every field from the commits, the diff, and the tracker context loaded in steps 1–4. State numbers where the run measured them; never invent one.
7. **Write `How to test`** (GitHub and Bugsnag; never on JIRA) — an ordered scenario per *How to test* above: concrete inputs, an explicit must-hold outcome per step, the gating toggle enabled in step 1 when the change is gated, and the regression flows named at the end. Use caller-supplied steps as passed when the caller provided them.
8. **Assemble and render.** On GitHub and Bugsnag, place the embedded blocks, when the caller passed any, directly above the closing links line, separated by a single blank line — each rendered exactly as received, with no re-formatting, no language conversion, and no re-ordering. On JIRA, write each open question as the closing sentence of the criterion or finding bullet it belongs to. Close with the PR / issue links line. Translate the headings and field labels into the assignment language, then convert the whole body to the target's markup and verify nothing leaked. On JIRA, close with the footer, measure the published body against the 3 000-character cap, and shorten it per *Length follows the facts* when it overflows, never an `Acceptance criteria` or a `Review findings` bullet.

---

## Output format

- **GitHub PR comments** — `templates/pr-summary-github.md`, in GitHub Markdown.
- **JIRA issue comments** — `templates/pr-summary-jira.md`, converted to ADF by the JIRA helper. Never pass the intermediate Wiki Markup directly to `acli` or the JIRA MCP server.
- **Bugsnag error comments** — `templates/pr-summary-bugsnag.md`, in plain text.

GitHub and Bugsnag carry the same two sections and the same closing line, differing only in markup. JIRA carries its own sections, its own order, and its own length cap, per *The JIRA shape* above.

---

## Publishing

Post the summary as a comment to the related PR or issue if available, using the template that matches the target tracker. Publish through the shared helpers so each tracker receives its tracker-native markup — never via raw `gh issue comment` / `gh pr comment` / `acli jira workitem comment add` calls.

- **GitHub target** (PR comment or linked-GitHub-issue mirror): pipe the rendered body into `skills/code-review-github/scripts/upsert-comment.sh <NUMBER|URL> -`. The helper detects the current GitHub actor (`gh api user --jq .login`), appends the marker `<!-- cr-comment:actor=<gh-login> -->`, and **PATCHes the newest comment already carrying that marker**, POSTing a new one only when none exists. Fall back to the GitHub MCP server only when the helper exits with code 2 (missing tool) or 3 (API failure): `updateIssueComment` on the marker-carrying comment when you can resolve its ID, `addIssueComment` otherwise.
  Append the same `<!-- cr-comment:actor=<gh-login> -->` marker to the body on either fallback call, per `@rules/compound-engineering/tracker.md` *Every comment an agent publishes on GitHub or JIRA carries a marker*.
- **JIRA target**: pipe the rendered source into `skills/code-review-jira/scripts/upsert-comment.sh <KEY|URL> -`. The helper appends the visible marker line `_cr-comment:actor=<actor-digest>_` (a digest of the account e-mail, never the address), converts the source to ADF, and updates the newest comment already carrying that marker through `--body-adf`; only when none exists does it create a new comment and then apply the ADF to it. Fall back to the JIRA MCP server only when the helper exits with code 2 (missing tool) or 3 (API failure), passing an ADF document rather than Wiki Markup — append the same `_cr-comment:actor=<actor-digest>_` marker line to that ADF, per the same rule.
- **Bugsnag target**: pipe the rendered body into `skills/code-review-bugsnag/scripts/upsert-comment.sh <URL|TRIPLE> -`. The helper POSTs a new comment on every run. Fall back to the Bugsnag MCP server only when the helper exits with code 2 (missing tool) or 3 (API failure) — also as a fresh post.
- Pre-existing comments published before these conventions were introduced are left untouched.
- Log the action (`created` or `updated`) plus the resulting comment URL in the CR wrapper's summary line.

---

## Principles

- Explain what broke, why it broke, and what the reader can now observe instead
- Focus on business impact, not technical detail — but keep enough "what" that a developer can locate the change without reading the diff
- Every sentence carries a fact; the report is as long as its facts and no longer
- Make the test scenario reproducible by a non-developer tester, with concrete inputs and explicit must-hold outcomes
- Match the formatting to the target tracker (Markdown for GitHub, ADF for JIRA, plain text for Bugsnag)

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
