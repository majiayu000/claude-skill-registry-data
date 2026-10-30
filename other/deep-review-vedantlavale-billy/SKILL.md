---
name: deep-review
description: Deep code review for pull requests, tuned to match CodeRabbit and Greptile depth but reported short. Checks two things separately, whether the code is right (correctness, project invariants, security, performance, conventions, code smells) and whether it does what the linked issue asked, then posts a plain-language summary anyone can read, at most five P0 to P3 findings underneath it, and a verdict. Use when reviewing a PR, re-reviewing after a push, or when the user asks for a thorough review.
allowed-tools:
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr list:*)
  - Bash(gh pr comment:*)
  - Bash(gh issue view:*)
  - Bash(gh api:*)
  - Bash(git:*)
  - Read
  - Grep
  - Glob
  - Task
  - TodoWrite
  - mcp__github_inline_comment__create_inline_comment
---

# Deep review

Review a pull request to the depth a paid review bot gives, and report it in the
time a human actually has. Deep analysis, short output: every finding verified
against the code, anchored to a line, and capped at five.

It reviews on two axes and keeps them apart:

- **Code**: is the code right? Groups A to F below.
- **Spec**: does it do what the issue asked? Group G below.

A PR can pass one and fail the other: clean code that builds the wrong thing, or
the right thing built badly. Reporting them separately stops one hiding the
other. The two-axis split and the smell baseline in group E come from
[mattpocock/skills](https://github.com/mattpocock/skills) `code-review` (MIT).

The analysis can be as long as it needs to be. The review cannot. Never show
reasoning, never restate the diff, never pad.

> **Set up section B before using this.** Everything else works on any repo.
> Section B is where your project's own invariants go, and it is the part that
> makes this better than a generic reviewer. A review without it is still useful;
> it just will not catch the bugs specific to your product.

## Inputs

- **PR number** (required). Detect from the branch when not given.
- **`--comment`**: post findings to the PR. Without it, print to the terminal only.
- **`--focus <area>`**: restrict to one area from the rubric below.

## Never suppress a re-review

Review on every invocation, including when this bot has already commented and
including PRs authored by an agent. A push changes the code, so the previous
review is stale. Address the current head SHA and say which SHA you reviewed.

Do skip only these, and say why in one line:
- The PR is closed or merged.
- The PR is a draft, unless `--comment` was passed explicitly.

## Step 1: gather

```bash
gh pr view <N> --json number,title,body,headRefOid,baseRefName,author,isDraft,state,files
gh pr diff <N>
```

Check out with full history, so `git log origin/<base>..HEAD` and
`git diff origin/<base>...HEAD` both work. Read whole files around the diff
when a finding depends on context the hunk does not show. A shallow checkout
makes those commands fail; if they do, say so rather than reviewing blind.

Read `AGENTS.md` at the repo root plus any `CLAUDE.md` in the changed
directories. They are the repo's own rules and rank alongside correctness.

Find the spec, in this order, and stop at the first hit:

1. Issues the PR closes: `gh pr view <N> --json closingIssuesReferences`.
2. `#123`, `Closes #45` or an issue URL in the PR body or commit messages. Read
   it with `gh issue view <n> --comments`, including any agent brief posted by
   `/triage`, which is the authoritative version.
3. A spec file under `docs/` or `specs/` matching the branch name.

If there is none, group G is skipped and the review says "No linked issue" in
the Spec section. Do not ask; a review runs unattended.

## Step 2: review against the rubric

> **In CI, never end your turn with a subagent still running.** Launch them in
> the foreground (`run_in_background: false`) and wait for every result. A
> headless session exits when your turn ends, so "pausing until the agents
> report back" posts nothing and the run still goes green. If a subagent does
> come back as launched in the background, wait for its result before writing
> anything. The job is done when the summary comment is on the PR, not before.
>
> Do not write scratch files or run ad hoc scripts to test a theory; CI denies
> them and each denial wastes a turn. Work from `gh pr diff` output and `Read`.

Run these as parallel subagents, one per group, each returning findings with
file, line, severity and the reason it was flagged. Use your strongest model for
groups A to D and G, and a cheaper one for E and F. Group G gets its own
subagent with the spec and the diff and nothing else, so the code groups do not
colour its judgement.

Add an agent on git history when the diff touches a file with a long history:
`git log -p --follow <file>` over the last 20 commits, looking for a fix this
change reverts or re-breaks. A regression that reintroduces a bug someone
already fixed is the highest-value finding a reviewer can produce, and it is
invisible from the diff alone.

### A. Correctness

Logic that produces wrong results, off-by-one, inverted conditions, wrong
operator precedence. Unhandled null on values that can be absent. Promises not
awaited, floating promises, unhandled rejections. Async work inside a loop that
should be batched. Race conditions between a write and a read of the same
record. Errors swallowed by an empty catch. Early return that skips cleanup.
Type assertions that paper over a real mismatch.

### B. Project invariants

Billy is a fully client-side invoice editor: a Next.js static export on
Cloudflare Workers static assets, with no backend, no auth and no database. The invoice lives in
the browser's `localStorage` and the PDF is made in the browser. There is no
tenant boundary to check. What matters is that the export matches the screen,
and that the user's data stays on their machine.

Every finding in this group is blocking (P0) unless the bullet says otherwise.

**What you see is what you get. This is the product.**

- `InvoicePage` (`apps/web/components/invoice/invoice-page.tsx`) is the only
  invoice layout. The editable canvas, the live preview and the PDF export
  (`apps/web/lib/pdf/client-export.tsx`) all render that one component tree. The
  only switch between them is `RenderModeProvider readOnly`. A second layout
  path, such as a PDF-only component, a print stylesheet or a preview-only
  branch that changes layout, is a finding. Consequence: the downloaded PDF
  stops matching what the user saw and approved.
- Styling that differs between edit and read-only mode must not change layout,
  size or spacing. Only editing affordances may differ (borders on hover,
  placeholders, controls). Consequence: text wraps differently in the export,
  page breaks move, and content shifts or clips in the PDF.
- Per-template styles key on the shared section class names in global CSS, and
  both render modes keep those names. Renaming or removing a section class
  without updating every template's CSS is a finding. Consequence: a template
  silently loses its styling, in the editor and in the PDF.
- `PAGE_W`, `PAGE_H` and `PAGE_GAP` are defined in both `invoice-page.tsx` and
  `client-export.tsx` and must stay identical (A4 at 96dpi: 794 × 1123, 24px
  gap). A change to one without the other is a finding. Consequence: the
  exporter slices the capture at the wrong offsets and pages get cut through
  the middle of content.
- Logo and stamp images must reach the rasteriser as `data:` URLs
  (`inlineInvoiceImages`). Consequence: a remote URL can taint the canvas, and
  the logo or stamp goes missing from the PDF or the export fails.
- Before capture, the export must wait for fonts, images and a stable layout
  (`ensureInvoiceFontLoaded`, `waitForImages`, `waitForStableLayout`). Removing
  or short-circuiting any of these is a finding. Consequence: the PDF renders in
  a fallback font or with missing images, even though the screen looked right.

**Invoice data never leaves the browser.**

- Nothing from `InvoiceData` (business or client names, addresses, emails,
  GSTIN, bank details, line items, amounts, invoice number, logo or stamp) may be
  sent over the network. That means no `fetch`, beacon, upload or third-party
  SDK call carrying it. Consequence: the README's "no data ever leaves your
  machine" becomes false, and users' client and bank details reach a server.
- PostHog (initialised in `apps/web/instrumentation-client.ts`, called as
  `posthog.capture`) may receive event names and anonymous, non-identifying
  properties only. Passing invoice fields to `posthog.capture` or
  `posthog.identify` is a finding. Consequence: invoice content ends up in a
  third-party analytics store.

**It stays a static export.**

- `apps/web` builds with `output: "export"`. Any of these is a finding: a route
  handler (`app/**/route.ts`), a server action, `middleware`/`proxy.ts`,
  `rewrites`/`redirects`/`headers` in `next.config.ts`, anything that needs a
  Node runtime at request time, or a dynamic route without
  `generateStaticParams`. Security headers belong in
  `apps/web/public/_headers`. Consequence: `next build` fails, or the code
  builds and then silently never runs on Cloudflare.
- There is no backend. The old Supabase migrations and scripts were removed
  (#39); new code must not add a database, auth or server SDK. Consequence: a
  server dependency comes back and breaks both the static build and the
  no-data-leaves promise.

**Saved drafts must keep loading.**

- The draft in `localStorage` under `billy_invoice_data` has no schema version.
  It is parsed with a bare `as InvoiceData` cast and dispatched as
  `LOAD_STATE`. Renaming or removing a field, or adding a required field to
  `InvoiceData`, `InvoiceOptions` or `LineItem`, without a default or migration
  applied on load is a finding. Consequence: returning users load a malformed
  draft, and the editor crashes or silently shows blanks where their data was.

**Package boundaries.** P2.

- `@billy/invoice-core` stays pure TypeScript, with no React, DOM or browser
  APIs. Consequence: the domain logic can no longer be tested or reused outside
  the web app.

**Open questions, not yet agreed. Do not block on these.** Flag them as P3 at
most, as questions:

- `calculateTotals` uses float arithmetic, not integer minor units, and applies
  tax to the subtotal before the discount. Whether either is intended for GST
  invoices has not been confirmed.
- Whether PostHog's defaults (`defaults: "2026-01-30"` in
  `apps/web/instrumentation-client.ts`) enable autocapture or session recording
  that could read text from the invoice's editable fields is unverified. If a
  diff turns either on explicitly, ask.
- `localStorage.setItem` failures (quota is about 5MB, and a logo and a stamp
  can each be up to 2MB) are only sent to `console.error`, so a draft can
  silently stop saving.

### C. Security and data handling

Injection: raw SQL built by interpolation, shell commands built from user input.
Prompt injection where user or document text reaches a system prompt unescaped.
Missing auth middleware on a new route. A token read without verification.
Secrets, API keys or connection strings in code, logs or error responses. CORS
widened beyond the known origin. Cookie flags dropped (`httpOnly`, `secure`,
`sameSite`). Rate limiting removed from a route that had it. File upload without
a type or size check. Path traversal. PII in logs.

**In CI config specifically:** an expression interpolated into a `run:` body.
Templating engines paste the value into the script text before the shell sees
it, so a crafted branch name, PR title or issue body executes on the runner.
Pass it through the environment instead. This is the single most common real
vulnerability in a repo's own automation, and it is easy to miss because the
workflow looks like configuration rather than code.

### D. Performance and resource use

N+1 queries, especially inside a loop over a collection. Selecting whole rows
where two columns were needed. A query on an unindexed column added to a hot
path. An index dropped or invalidated by a migration. Unbounded list queries
with no limit. Large payloads held in memory where a stream would do. Streams
that never close on client disconnect, leaking the connection and the upstream
request. Blocking work on the request thread.

### E. Repo conventions

Read them from `AGENTS.md` and `CLAUDE.md`, do not assume. Flag only a rule you
can quote. A written rule is a hard finding.

On top of that, a fixed **smell baseline** applies even when the repo documents
nothing. These are always judgement calls, never higher than P2, and a written
repo rule that endorses the pattern overrides them. Flag one only when it is in
the diff, not in code the PR merely touches:

- **Mysterious name**: the name does not say what it does or holds. Rename.
- **Duplicated code**: the same logic appears in two hunks or files. Extract it.
- **Feature envy**: a function uses another object's data more than its own.
  Move it to that data.
- **Data clumps**: the same few params travel together. Make them one type.
- **Primitive obsession**: a string or number standing in for a domain concept.
  Give it a type.
- **Repeated switches**: the same `switch` on the same value in several places.
  One map both sites share.
- **Shotgun surgery**: one change forces edits scattered across many files.
  Gather what changes together.
- **Speculative generality**: parameters, hooks or abstractions the issue does
  not need. Inline them.
- **Middle man**: a function that only forwards. Call the target directly.

Skip anything a linter or formatter already enforces.

### F. Tests and evidence

New behaviour with no test. A test asserting a mock rather than the behaviour. A
changed error path with no case covering it. A migration with no rollback note.
A PR claiming a fix with no before/after proof when the change has a visible
surface.

### G. Spec: does it do what was asked?

Only when step 1 found a spec. Compare the diff against it and report:

- **Missing**: a requirement or acceptance criterion that is absent or only
  partly done. Quote the line from the issue. **P1** by default: the PR does not
  do its job.
- **Wrong**: looks implemented, but the behaviour does not match what the issue
  describes. **P1**.
- **Unasked**: behaviour the issue did not ask for, or explicitly put out of
  scope. **P3**, or **P2** if it widens risk (a new route, a schema change).

An issue with acceptance criteria is checked item by item. Say which ones pass.

## Step 3: score each finding 0 to 100, then verify

Give every candidate finding a confidence score from 0 to 100 reflecting how
strong the evidence is. **Drop anything below 80.** Prefer a handful of findings
you are sure about over broad coverage.

Then launch one subagent per surviving finding whose only job is to disprove it.
Give it the finding, the file and the PR intent. It reads the surrounding code
and answers `CONFIRMED` or `FALSE_POSITIVE` with a reason. Drop everything not
confirmed, and deduplicate findings that are the same root cause in two places.

A finding survives only if you can state a concrete failure: the input or state,
and the wrong output, leak or crash that follows. "This could be risky" is not a
finding. "A user of org A calling `GET /api/documents/:id` with org B's document
id gets the document, because the handler looks it up by id alone" is.

Do not flag: pre-existing issues the PR did not touch, anything a linter or the
type checker already catches, style preferences, or a rule explicitly silenced
in the code with a comment saying why.

## Step 4: assign a priority

| Priority | Meaning |
|---|---|
| **P0** | Critical. Security, data loss, data exposure, system-breaking |
| **P1** | High. Serious correctness or production issue |
| **P2** | Medium. Real bug, maintainability or reliability issue |
| **P3** | Low. Minor improvement |

Everything in group B is P0 unless you deliberately wrote it otherwise. Those
are the rules you said could not be broken.

## Step 5: write the review

**Two readers, one review.** A non-engineer opens this to find out whether the
work is safe to ship. An engineer opens it to find out what to change. Serve the
first reader in the first three lines, then give the second the detail.

A good review has **0 to 5 findings**. If you have more, you have stopped
filtering. Cut to the ones that change what the author does next. Spec findings
count toward the five but are listed under their own heading, so a code problem
never pushes a missed requirement out of view.

Use this exact structure:

```markdown
**In short:** <one or two plain sentences: what this does for the user, and
whether anything is blocking.>

<!-- technical detail below -->

## Summary

- What this PR changes
- Why it changes it
- Any important architectural or behavioural change
- Any notable risk

## Spec

Issue #123: 3 of 4 acceptance criteria met. (Or: "No linked issue.")

### [P1] Missing: export as CSV

**Problem** / **Impact** / **Suggestion**, same shape as below, quoting the issue.

## Findings

### [P0] Short issue title

**Problem**
One or two sentences on the concrete problem.

**Impact**
One sentence on what breaks or why it matters.

**Suggestion**
The fix or the direction, briefly.

`src/routes/documents.ts:42`

## What's good

- 1 to 3 genuinely useful observations, or omit the section

## Verdict

✅ Looks good
```

### The "In short" line is the important one

It is the only part most readers will finish. Write it for someone who runs the
business, not someone who runs the build.

Rules, all of them hard:

- **Two sentences, maximum.** One is better.
- **No identifiers, no file paths, no line numbers, no type or function names,
  no framework words.** Not `useMemo`, not `page.tsx`, not `div`, not `NUL
  byte`, not `P2`. Those all live below.
- **Say what changes for the person using the product**, not what changed in the
  code. "The prompts list can now be searched and used from the keyboard" beats
  "refactors the list into a button with filter state".
- **Then say whether anything blocks**, in the same plain register. "Nothing
  blocking." or "One thing to fix first: the change does not show up properly on
  GitHub, so nobody can review it."
- If a finding is a security or customer-data problem, say so here in words a
  non-engineer understands. That is the one case where the line leads with the
  risk rather than the feature.

Worked example, for a PR whose only finding was an unreadable diff:

> **In short:** The settings page is easier to scan and can now be used without
> a mouse. One thing to fix first: a stray character makes the change unreadable
> on GitHub, so nobody can review it properly.

Not this:

> **In short:** Refactors `SettingsPage` to a 3-col grid and converts the row
> `div` to a `button`. P2: NUL byte in `ALL_ITEMS` forces git to treat
> `page.tsx` as binary.

### Verdict

Verdict is one of:

- `✅ Looks good` when there are no P0 or P1 findings
- `⚠️ Changes requested` when there is a P1, or several P2s
- `❌ Blocking issues` when there is any P0

`/ship-pr` reads that verdict line, so keep it exact and put it last.

Drop the `Findings` section entirely when there are none. Keep the `In short`
line, `Summary`, `Spec` and `Verdict` always; `Spec` is one line when nothing is
wrong. When a spec finding exists, the `In short` line says so in plain words,
for example "It does not yet do one thing the request asked for: exporting the
list.".

Keep each finding under 100 words.

### Tone

Write like a staff engineer who has read the code and has somewhere to be.
Direct, technical, neutral.

Never write: "I think", "It seems like", "Let's make sure", "Great work on this".
No praise padding, no generic advice, no hedging, no restating what the author
obviously did.

## Step 6: post

Without `--comment`, print the review and stop.

With `--comment`:

1. Post each P0, P1 and P2 finding as an inline comment via
   `mcp__github_inline_comment__create_inline_comment` with `confirmed: true`.
   The inline comment carries the `Problem` / `Impact` / `Suggestion` body. One
   comment per issue, never a duplicate. Add a committable `suggestion` block
   only when committing it alone fixes the issue completely.
2. Post the review above as a single summary comment with `gh pr comment`. In
   the summary, reduce each finding to its priority tag and title, one line
   each, so the summary stays scannable and the detail lives inline:

   ```markdown
   ## Findings

   - **[P0]** Documents route looks up by id without an ownership check `documents.ts:42`
   - **[P2]** List issues one query per row `list.ts:88`
   ```

P3 findings go in the summary only. Do not spend an inline comment on them.
A spec finding with no single line to anchor to (a missing requirement) also
goes in the summary only, under `## Spec`.

## Links

Anchor every code reference to the full head SHA, or the markdown will not
render:

`https://github.com/<owner>/<repo>/blob/<full-sha>/src/routes/chat.ts#L40-L47`

Include one line of context either side of the line you mean.

## Say what you could not check

If the checkout has no dependencies installed, you cannot run the build or the
type checker, so you cannot confirm the results the PR body claims. Say so in
one line at the end rather than letting silence imply you verified them.
