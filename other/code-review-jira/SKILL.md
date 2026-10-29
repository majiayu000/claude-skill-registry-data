---
name: code-review-jira
description: Use when run code review for JIRA issues and publish results to
  GitHub PR and JIRA
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Apply the shared CR tracker-wrapper contract in `@skills/code-review-github/references/cr-wrapper-contract.md` — Constraints, Load Context gates, Run Reviews, Publish Results, and Output Rules all live there and are not restated here. This file carries only what a JIRA-sourced review decides for itself.
- Apply @rules/jira/general.md
- Publishing is limited to PR / linked-issue comments via `gh` and to JIRA ticket comments via `acli`.
- Apply @rules/reports/general.md *A JIRA comment is written for a non-technical reader* — the banned-content list, its exceptions, and the 3 000-character cap bind every comment this skill puts on a JIRA ticket, the embedded blocks included. The publisher converts the constrained template source to ADF and applies it through `--body-adf`.
- **The split is the point of this wrapper: technical findings go to the GitHub pull request, and the JIRA ticket receives the non-technical summary alone.** Never publish severity labels, finding counts, code references, a head SHA, a diff fingerprint, a gate result, a CI status, or a coverage figure to JIRA. None of it is lost — the GitHub PR comment carries it, and that is the comment `@skills/merge-github-pr/SKILL.md` reads.

---

## Scope
Perform code review for JIRA issues by analyzing related pull requests and publishing results to:
- GitHub (technical findings)
- JIRA (human-readable summary)

---

## Execution

### 1. Load Context
- Load JIRA context by running `skills/code-review-jira/scripts/load-issue.sh <KEY|URL>`. The script accepts a bare key (`ACME-1234`), a `/browse/<KEY>` URL, or any URL containing `?selectedIssue=<KEY>`. Read issue header, description, comments, attachments, subtasks, issue links, custom fields, `devSummary`, and `pullRequests` off the resulting JSON document.
- The context-brief and comment-array helpers are `skills/code-review-jira/scripts/gather-issue-context.sh <KEY|URL>` and `skills/code-review-jira/scripts/parse-comments.sh <KEY|URL>`. The brief renders the issue plus its comments, attachments, recursively-loaded linked issues, and an inventory of external URLs. `acli` cannot download attachments, so their content is read with your own tools.
- Prefer the JIRA MCP fallback for the data the scripts cannot cover: changelog (`expand=changelog`), available next transitions, and friendly custom-field names (`expand=names`).
- Identify all open PRs linked to the issue from the script's `pullRequests` array.
- **Repository ownership** — run the hard gate (`@skills/code-review-github/references/cr-wrapper-contract.md` *Repository ownership*) **per linked PR, after the `pullRequests` array is known and before that PR is checked out**. A JIRA project can carry links to PRs across several repositories, so this is where a cross-repo review silently starts — and it is why this wrapper skips a mismatching PR and continues with the rest instead of stopping the run.

#### Issue Context Analysis
The assignment is the **JIRA issue**. Fetch it complete — description, all comments, and all attachments (screenshots, files, embedded data) — and run the four analysis steps in `@skills/code-review-github/references/cr-wrapper-contract.md` *Issue Context Analysis* against it.

#### Incremental review scope — where the round history lives
The baseline still resolves from the **GitHub PR's** CR comments (`@skills/code-review-github/references/cr-wrapper-contract.md` *Incremental review scope*) — JIRA carries no reviewed revision. The round markers this wrapper reads as a pointer to that history are the `kolo N` / `round N` markers in the **JIRA description and comments**, and they are resolved **per linked PR**: each PR keeps its own baseline, so a ticket linking several PRs never crosses one PR's revision into another's delta.

### 2. Pre-checks
- `statusCheckRollup[]` for the CI check map comes off the GitHub PR JSON, loaded via `skills/code-review-github/scripts/load-issue.sh <PR-URL>` if it is not already loaded.

### 3. Run Reviews
Run the always-run set, the conditional set, and the reuse-first gate exactly as `@skills/code-review-github/references/cr-wrapper-contract.md` *3. Run Reviews* defines them, for **each** linked PR. Two JIRA-specific riders apply:

- Convert the `## Assignment Compliance` block `@skills/assignment-compliance-check/SKILL.md` returns to the supported JIRA intermediate source before passing it to `pr-summary`, and keep the GitHub-Markdown original for the linked-GitHub-issue mirror. The JIRA helper converts that source to ADF. The block travels on every run with a linked ticket, its affirmative verdict included — a JIRA comment that stays silent when every criterion is met tells the ticket owner nothing (`@rules/code-review/general.md` *Two-Part CR Output* → *The tracker comment carries the same verdict — in all three cases*).
- Every blocking documentation request from the Third-Party API & Service Analysis also becomes a plain-language question in the JIRA comment, so whichever tracker the answerer reads carries the ask. On JIRA it closes the `Review findings` bullet it belongs to.

### 4. Publish Results

#### JIRA (consolidated non-technical comment — one comment per issue, updated in place)
- Delegate the JIRA comment to `@skills/pr-summary/SKILL.md`: invoke it with the **JIRA** tracker target so it renders `@skills/pr-summary/templates/pr-summary-jira.md` as the intermediate source and publishes real ADF via `skills/code-review-jira/scripts/upsert-comment.sh` (JIRA MCP server fallback on exit code 2/3). No direct JIRA comment write may bypass the helper.
- The JIRA comment carries the shape `pr-summary` renders for **this** target — a status line, `Acceptance criteria`, `Review findings` retold from the GitHub PR comment this run just published, `What changed`, `Impact after deployment` retold from that comment's `## Affected behaviour outside the diff`, then the closing links line and the footer — as rendered ADF (`@skills/pr-summary/SKILL.md` *The JIRA shape*). On JIRA, a finding outside the assignment reaches `Review findings` only when it is Critical. There is **no reduced JIRA shape**: this is not a cut-down GitHub comment but its own order, written for the person who owns the ticket, who needs the verdict before anything else.
- **Several linked pull requests — one group per pull request.** Pass every reviewed pull request's findings to `pr-summary` with the pull request they belong to. The comment keeps the verdict once and groups the findings, the questions that close them, and the per-PR sections under one heading per pull request (`@rules/code-review/general.md` *An issue with several pull requests — remarks and findings split per pull request*).
- Pass both together in one invocation — the *Clarifying questions* (conditional: only when a question survives the gate below) and *Assignment Compliance* (always, on every run with a linked ticket). On JIRA `pr-summary` renders the compliance verdict into the `Acceptance criteria` section, and each clarifying question becomes the closing sentence of the criterion bullet or the `Review findings` bullet it concerns; there is no separate questions section and no `{embedded_blocks}` slot. The verdict still reaches the reader exactly once, and first. Still no severity counts and no file paths: the JIRA comment stays non-technical.
- The JIRA comment carries no `How to test`, so test-parameter gating is not rendered there. The pull request's own description carries the testing steps (`@rules/git/pull-requests.md` *Testing*).
- **Clarifying questions block (conditional).** While running the sub-reviews, collect every **genuine open question** the reviewer needs answered before the work can be accepted — an ambiguity in the assignment that the issue description, comments, and code could not resolve (a missing acceptance criterion, an undefined edge case, a value the assignment never specified, a contradiction between the ticket and a comment). Then put every candidate through the **severity gate**, the **already-answered walk**, and the **scope gate** below, in that order, and assemble the block only from what survives all three. When at least one question survives,
pass each one to `pr-summary` as a single plain-language sentence, together with the acceptance criterion it concerns or, when it concerns no criterion, the finding it belongs to. `pr-summary` writes it as the closing sentence of that bullet. When none survives, pass nothing — never emit an empty "no questions" block, and never a "previously answered" note. Do not invent questions to fill the section; ask only what genuinely blocks acceptance. **Every blocking documentation request** produced by the Third-Party API & Service Analysis step 7 is such a question and must appear here as one question, phrased so a non-developer can forward it:
the vendor / service name, the version in use (or that it could not be determined), and the ask for a documentation link covering the reviewed operations. Keep the endpoint / SDK-method list itself on the GitHub PR comment — JIRA carries no technical detail per the constraint above.
- **Severity gate and already-answered walk (issue #208).** Emit only **Critical** questions (without the answer the change cannot be accepted) and **Moderate** ones (the change ships either way, but the answer decides whether the implemented behaviour is the intended one); every other question is dropped, never asked. Then walk every comment step 1 already loaded and drop each question the tracker has already answered **and** the diff already implements.
  Last, drop each question that no longer holds on the current head or falls outside the ticket's scope. Severity is never rendered — the questions are plain sentences, passed in Critical-before-Moderate order. The full gate, the sources walked, the answered-but-not-implemented case, the ambiguous-answer rule, and the scope gate live in `references/clarifying-questions.md`.
- **ADF source conversion.** Convert an embedded Markdown block to the supported source per @rules/jira/general.md (`## ` → `h2. `, `**bold**` → `*bold*`, `` `code` `` → `{{code}}`, `- ` → `* `, Markdown link `[label]` + `(url)` → `[label|url]`) before passing it. Verify the source contains no leaked Markdown. The canonical helper performs the only conversion to ADF and the only `acli` write; never post the source directly.

#### Linked GitHub issues (consolidated mirror — one comment per issue, updated in place)
- The JIRA-side summary is the **primary** tracker comment; the linked-GitHub-issue comment is a courtesy mirror so reviewers reading the GitHub issue see the same report without opening JIRA. Both come from `pr-summary` and carry the same facts, but **not the same shape**: the mirror renders the GitHub structure (*What changed*, *How to test*, and the *Assignment Compliance* block through `{embedded_blocks}`), while the ticket renders the JIRA one (*Acceptance criteria*, *Review findings*, *What changed*, *Impact after deployment*, with the verdict inside the first section and each question inside the bullet it concerns).
  Do not copy one body onto the other target — render each from its own template, or the mirror publishes a shape that target's contract does not define. Publish it per `@skills/code-review-github/references/cr-wrapper-contract.md` *Linked GitHub issues*, passing the GitHub-Markdown version of any embedded block.
- If `closingIssues[]` is empty, note `no linked GitHub issue — mirror skipped` in the PR comment summary line.

---

## Output Rules

### GitHub (technical report — only here)

Apply `@skills/code-review-github/references/cr-wrapper-contract.md` *Output Rules — GitHub PR comment*, and use the template defined in `templates/github-output.md`. The JIRA-specific slots it leaves open:

- The header block's tracker-mirror field is `Linked-tracker mirror`.
- The summary line's tracker-mirror status is `posted JIRA summary on <KEY> (+ mirrored to GitHub issue #N)`, `JIRA only — no linked GitHub issue`, or `failed: <reason>`.

### JIRA (non-technical summary — only here)
- The non-technical JIRA comment is **produced and posted by `@skills/pr-summary/SKILL.md`**, not by this skill. Do not author or embed a custom template here.
- It carries no severity counts, no file paths, no line numbers, no code snippets — plain language understandable by non-developers, per @rules/reports/general.md *A JIRA comment is written for a non-technical reader*. Its sections are `Acceptance criteria`, `Review findings`, `What changed`, and `Impact after deployment`, under one status line and above a footer, with each open question inside the bullet it belongs to; `pr-summary` owns them, and this skill neither authors nor reorders them.
- The intermediate source constructs (`h2.` / `h3.` headings, `*bold*`, `_italic_`, `{{inline}}`, `{code:php} ... {code}`, `*` / `#` bullets, `[label|url]`, `{quote}`) come from `@skills/pr-summary/templates/pr-summary-jira.md`. The helper converts them to ADF nodes and marks per @rules/jira/general.md.

### The split, verified per run

Before the run ends, confirm both halves actually landed where they belong. The split is a property of what was published, not of what was intended.

1. The **GitHub PR comment** carries the technical report — findings, severities, counts, the reviewed revision, the diff fingerprint, coverage, and the quality-gate result.
2. The **JIRA comment** carries the non-technical summary alone, and nothing on the banned list survives in it. Walk the rendered body against that list before the publish; `agents/april.md` runs the same walk when it is the publisher.

A path that would put technical content on the ticket is a defect in that path, never an exception to grant here.

## References

- @skills/code-review-github/references/cr-wrapper-contract.md
- references/clarifying-questions.md

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
