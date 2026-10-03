---
name: pr-reviewer
description: "Review pull requests with full context. Fetches linked Jira tickets, Figma designs, and Notion docs via MCP, spawns parallel subagents for systematic code review (correctness, security, tests, SOLID, clean code), then drafts friendly, humanized GitHub-ready comments. Use when reviewing PRs, examining code changes, or when the user asks for a code review."
---

# PR Reviewer

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

Reviews pull requests systematically with full context awareness and humanized feedback.

This skill fetches linked resources via MCP, spawns parallel review subagents for systematic analysis, then synthesises findings into friendly, GitHub-ready comment drafts.

---

## When to Use

- User asks to review a PR, code changes, or diff
- User shares a PR link or number
- User asks "review this", "what do you think of these changes", "check this PR"
- User provides a GitHub PR URL

---

## Workflow

### Step 1: Identify the PR

Parse the PR from user input:
- GitHub URL: extract owner, repo, PR number
- PR number: use current repo context
- Branch name: find associated PR via `gh pr list`

Fetch the PR details:
```bash
gh pr view <number> --json title,body,files,commits,labels,baseRefName,headRefName
gh pr diff <number>
```

### Step 2: Extract and Fetch Linked Resources via MCP

Scan the PR title, description, branch name, and commit messages for linked resources.

**Jira/Atlassian tickets:**

Extract ticket IDs matching `[A-Z]+-[0-9]+` (e.g. `SKU-123`, `CORE-3211`).

1. Call `getAccessibleAtlassianResources` to obtain `cloudId`
2. For each ticket key, call `getJiraIssue` with `cloudId` and `issueIdOrKey`
3. Use the ticket's summary, description, and acceptance criteria to verify alignment

**Figma links:**

Extract URLs matching `figma.com/design/:fileKey/:fileName?node-id=...`

1. Parse `fileKey` and `nodeId` (convert `-` to `:` in node-id)
2. Call `get_design_context` with `fileKey` and `nodeId`
3. Optionally call `get_screenshot` for visual reference

**Notion docs:**

Extract URLs matching `*.notion.so/...` or `*.notion.site/...`

1. Call the Notion MCP to fetch page content
2. Use for requirements, API specs, or architecture decisions

**If MCP fails:**

Note it in the review: "Could not fetch Jira ticket CORE-3211 (Atlassian MCP unavailable). Review based on PR description only." Proceed with available context.

### Step 3: Systematic Code Review (parallel subagents)

Spawn **five review subagents in parallel** using `model: "sonnet"`. Each receives the full PR diff and returns findings.

Do not run these checks sequentially. Spawn all five simultaneously, collect results, then synthesise.

**Rules every brief below inherits.** Paste these into each subagent's prompt ahead of its brief. The coverage, scope and evidence rules here, and the evidenced-drop rule in Step 5, are adapted from the review prompts in alibaba/open-code-review; the teardown is at [`docs/research/2026-09-14-open-code-review-teardown.md`](../../../../docs/research/2026-09-14-open-code-review-teardown.md).

- **Report your coverage.** Open your report with one line: files seen, files reviewed, files skipped with a one-phrase reason each. A file whose hunks you did not read is skipped, not reviewed. Reviewing an implementation file does not cover its interface, its config, its type declarations, or its barrel export; the secondary file is where contract drift hides, and it is the one most often skipped.
- **Reading is unbounded, findings are not.** Read whatever you need to understand the change, including files outside the diff. File findings only against code inside the diff. A problem on a line the author did not touch is context you gathered, not a finding.
- **Spend your calls on evidence, not on certainty.** Budget roughly two or three tool calls per finding. Once you can cite the construct and say what is wrong with it, write the finding and move on; the main agent verifies every finding after you report it. Never call the same tool twice with the same arguments.
- **Finding nothing is a result.** If a sweep turns up nothing real, say so and finish. Do not keep probing for marginal findings, and do not manufacture one to prove you read the diff; your coverage line is that proof. An invented finding costs more than a missed one, because it trains the reader to skim the whole report.
- **Every finding cites its construct.** File, line, and the code you are talking about. A finding without a citation is a hunch, and hunches do not leave the subagent.

---

#### Subagent 1: Correctness & Logic

**Inputs:** full PR diff, PR description, linked ticket acceptance criteria.

For every changed function/method:
- Does the logic match the stated intent (from PR description and ticket)?
- Are there off-by-one errors, missing null checks, unhandled branches?
- Are edge cases covered: empty input, boundary values, error paths?
- Are there race conditions or ordering assumptions?
- Does the change break any existing callers?

---

#### Subagent 2: Security

**Inputs:** full PR diff, file list.

Scan for OWASP Top 10 patterns:
- Injection (SQL, command, XSS, template)
- Broken authentication / authorization checks
- Sensitive data exposure (logging secrets, hardcoded keys)
- Missing input validation at system boundaries
- Insecure deserialization
- Overly permissive CORS or CSP
- Dependencies with known vulnerabilities (if lockfile changed)

Only flag issues with concrete exploit paths, not theoretical risks.

---

#### Subagent 3: Test Coverage & Quality

**Inputs:** full PR diff (test files and non-test files).

For every behavior introduced or changed:
- Is there at least one test that exercises it through the public API?
- Do tests assert on observable behavior or implementation internals?
- Are test names descriptive of the behavior being tested?
- Missing scenarios: happy path, empty/nil, boundary, error path, idempotency?
- Do tests mock only at genuine external boundaries (network, clock, OS)?
- Testing Trophy shape: more integration tests than unit tests for cross-unit behavior?

---

#### Subagent 4: SOLID & Architecture

**Inputs:** non-test source files from the PR diff.

- **S**: Does any new class/module have more than one reason to change?
- **O**: Does adding a new variant require modifying existing code?
- **L**: Does any subtype violate its base type's contract?
- **I**: Are there fat interfaces forcing unused method implementations?
- **D**: Are concrete dependencies hardcoded where abstractions would be natural?

Also check: does the change follow the repository's existing architectural patterns, or does it introduce a novel pattern without justification?

---

#### Subagent 5: Clean Code & Conventions

**Inputs:** full PR diff, project CLAUDE.md / DEVELOPMENT_GUIDELINES.md (if they exist).

- Magic values without named constants
- Functions doing more than one thing
- Generic unqualified names (`data`, `info`, `handler`, `manager`)
- Comments that restate the code (keep only "why" comments)
- Half-finished surfaces (TODOs, stub bodies, "implement later")
- Long parameter lists (>3-4 positional params)
- Style violations against project guidelines (if documented)
- Inconsistency with patterns used elsewhere in the same codebase

---

### Step 4: Contextual Review (from MCP-fetched resources)

Layer additional review based on the fetched context:

**Ticket alignment:**
- Do the changes implement what the ticket describes?
- Are all acceptance criteria met?
- Is there scope creep (changes beyond ticket scope)?

**Design alignment (if Figma fetched):**
- Does the implementation match the design?
- Are spacing, colors, states, and interactions correct?
- Are all design states handled (empty, loading, error, success)?

**Doc alignment (if Notion/Confluence fetched):**
- Does the implementation match documented specs?
- Are API contracts followed?
- Are architectural decisions respected?

### Step 5: Verify Every Finding Before Drafting

**Subagent output is a lead, not a finding.** Do not draft a comment from a subagent report you have not confirmed yourself. Agents overstate severity, mistake convention for defect, and occasionally invent a line number. A wrong finding posted on a colleague's PR costs more than a missed one. The rule is the same at both stages: no finding is reported without the construct it cites (Step 3), and no finding is dropped without the fact that disproved it (this step).

For each reported finding, before it earns a comment draft:

1. **Read the actual code** at the cited file and line. Confirm the construct is really there and really does what the report says.
2. **Check the claim's load-bearing premise.** If a report says "this branch is untested", grep for the test. If it says "this violates the module rule", read the rule. If it says "this breaks callers", find the callers.
3. **Check for a sibling precedent.** Does the pre-existing equivalent do the same thing? If yes, it is `(pre-existing)` and the severity usually drops. A "CRITICAL: no tests for this adapter" collapses when the adapter it was modelled on has no tests either.
4. **Reproduce the reasoning for anything security or concurrency related.** Walk the interleaving yourself. State the ordering that produces the bad outcome. If you cannot construct it, the finding does not ship as an assertion. When the downside-if-true is critical (a race, a security hole, data loss), it may ship as a genuine question that states the specific mechanism you suspect and why you could not confirm it. At most one or two of these per review; more than that and they become the faux-questions Step 6 forbids.
5. **Kill it if it does not survive, and say what killed it.** A drop cites the specific fact that disproved it: the test it claimed was missing, by file and line; the caller it claimed would break, unbroken; the sibling that does the same thing. "Could not confirm" is not a reason to drop, it is a reason to soften (rule 4) or to state the uncertainty in the draft. Report every drop to the user in Step 7 rather than silently padding the review.

Also verify the author's own claims where a finding depends on them. PR descriptions that argue a design decision at length are usually right, and checking beats assuming in both directions: a claim that checks out is worth one clause of confirmation, and a claim that doesn't is often the most valuable thing in the review.

Findings that survive this step carry their evidence into the draft: the file and line of the rule broken, the name of the pattern to copy, the interleaving that triggers the race.

### Step 6: Draft Humanized GitHub Comments

For every finding that survived Step 5, produce a GitHub-ready comment draft.

**Severity scale:**

| Severity | Symbol | Meaning |
|----------|--------|---------|
| Critical | CRITICAL | Likely bug, security hole, or broken behavior |
| Suggestion | SUGGESTION | Quality, clarity, maintainability |
| Nice to have | NICE | Optional improvement |

The severity labels are for the user's chat summary only. They never leak into the comment text as conditions ("before merge", "blocker", "must"): the reviewer is a peer sharing what they noticed, not a gatekeeper deciding what the author has to do (see "You're a peer, not a gatekeeper" below).

**Comment requirements:**
- 1-2 sentences for inline comments. Budget roughly 100-300 characters. If a draft runs past 350, cut a whole sentence, never a subject (see below).
- Copy-paste ready for GitHub
- No AI-isms: avoid "consider", "it would be beneficial", "enhance", "leverage", "crucial", "pivotal"
- Use "you" when it fits
- Frame suggestions as options: "One option:", "It might be worth adding...", "It might be cleaner to..."
- No firm language, even for a real bug: say what you think happens and ask what they think

**Never drop the subject of a sentence.** Brevity comes out of whole sentences, never out of grammar. Telegraphic prose reads as a machine writing minutes, not a colleague talking.

| Write | Not |
|---|---|
| I checked the transaction boundaries | Checked the transaction boundaries |
| I didn't find any correctness bugs | No correctness bugs found |
| I don't see a spec for this one | No spec for this one |
| I think this could use a note on X | Worth a note on X |
| It looks like the union is stale | Looks like the union is stale |

**Brevity yields to comprehensibility.** The 1-2 sentence budget assumes the finding is self-evident once the reader sees the line it sits on. When the defect is a causal chain (a value import pulling in a runtime dependency, a race across two requests, a lock that doesn't cover what it appears to), state each link. A comment the author cannot follow has failed no matter how short it is. Spend the extra sentences on the mechanism, not on preamble or on restating their PR description back at them.

**Every reference has to be resolvable by the author alone.** This is the other way comments turn cryptic, and the existing brevity rule does not catch it: the mechanism is stated fine, but the comment points at something the author cannot reach from where they are standing. You have the other PR's diff, the design file, and the ticket open in tabs. They have this line of code. A reference they would have to come back and ask you about has failed, however precise it is.

| Unresolvable as written | What it needs |
|---|---|
| a bare design node id (`4051:28381`) | a full clickable link, plus what the frame shows |
| another PR by number or ticket key | one clause saying what that PR changes, so its relevance is legible without opening it |
| a symbol you added on a different branch | the file it lives in, and what it does |
| "AC #2", "the third bullet", "the rule in CLAUDE.md" | the criterion or rule restated in a few words |
| "the sibling does this too" | which sibling, by path |

Before and after, from a review that pointed at a design frame the author had no way to open:

- Cryptic: `The read-only Figma section already specs it (4051:28381: single full-width Close instead of Cancel/Save).`
- Clear: `Design already has the read-only version of it: [node 4051-28381](https://figma.com/design/<key>?node-id=4051-28381) shows the same modal with one full-width Close button in place of Cancel/Save.`

Same sentence, same length budget. The difference is whether the author can act on it without a round trip.

**Read each draft back as the author before it ships.** They have not seen your other tabs, your subagent reports, or the branch you were on ten minutes ago. Every proper noun in the comment (a PR, a ticket, a file, a symbol, a design frame, a person) either resolves from what is in front of them or gets one clause of context attached. This is the last check before Step 6 output, and it is cheap: reread, and for each name ask "could they follow this from this page alone?"

**Voice and examples:**

Voice setup. Think of the author as a teammate you respect, someone who's going to read this tomorrow morning before they've had coffee. They already shipped a draft, which took real effort. Write the way you'd actually talk to them at lunch. Usually that means starting from what we noticed rather than what we want done, and asking instead of telling when we're not sure. Use "we" where it fits, since the code is something we share.

Concrete before-and-after pairs. The envelope around each comment (severity, file, line) stays the same; only the comment text shifts. Eight pairs, ordered by severity, then by finding type. **Every friendly version below is inside the length budget. They are the target, not a floor to build on.**

**1. Null check (Critical, correctness)**
- Cold: `` `venue` can be null here. Add a safe call or null check. ``
- Friendly: `` I think `venue` can come back as null here when the search doesn't match. Should we add a guard? ``
- *What changed: opens with the observation rather than the instruction, asks instead of commanding.*

**2. SQL injection (Critical, security)**
- Cold: `SQL injection risk. Use parameterized queries.`
- Friendly: `` Heads up, it looks like `userId` is going straight into the query string here. Should we switch this over to a parameterized version? It's an easy thing to miss in review. ``
- *What changed: warmer opener, asks rather than commands, "easy to miss" removes blame.*

**3. Test coverage (Suggestion, tests)**
- Cold: `Missing test for the cancelled path.`
- Friendly: `It looks like we're already covering the success and reschedule paths, but not cancel. It would be good to lock that one down too if we get a chance.`
- *What changed: credits existing work first, uses "we" throughout, "if we get a chance" softens the suggestion.*

**4. Single responsibility (Suggestion, SOLID)**
- Cold: `This method has too many responsibilities. Extract validation.`
- Friendly: `I noticed this one's doing both validation and persistence. Pulling validation out into its own function might make the tests easier for us down the line. Totally up to you, though.`
- *What changed: names the two responsibilities specifically, explains why with "us", explicit "up to you" defuses authority.*

**5. Missing edge case (Suggestion, correctness)**
- Cold: `` What happens when `items` is empty? Add handling. ``
- Friendly: `` I was wondering what happens here if `items` comes through empty. Does the total just zero out, or do we want to throw? ``
- *What changed: poses as a genuine question, offers both options so the author isn't cornered, "we want to" instead of "you should".*

**6. Generic naming (Suggestion, clean code)**
- Cold: `` `data` is too generic. Rename. ``
- Friendly: `` I think this `data` could use a more specific name, maybe `customerLoyaltyRecord`. Future-us would thank us when we're grepping for it. ``
- *What changed: "Future-us" is the small but real win. Concrete alternative offered, future-pain rationale frames it as shared.*

**7. Magic number (Nice, clean code)**
- Cold: `` Replace magic number `86400` with a named constant. ``
- Friendly: `` Small thing, but `86400` would probably read more clearly as `SECONDS_PER_DAY`. It took me a beat to recognize it. Do you think it's worth pulling out into a constant? ``
- *What changed: "small thing" calibrates severity, admits the inference ("takes a beat"), asks instead of instructs.*

**8. Convention match (Nice, clean code)**
- Cold: `Use early return.`
- Friendly: `` I noticed the rest of `BookingService` goes with early-returns on validation failures. It might be worth doing the same here, just for consistency, but totally up to you. ``
- *What changed: references the local convention without claiming authority, "might be worth" hedges.*

What the pairs are showing:
- Open with what we noticed, not what we want done.
- First-person voice when we're guessing ("I think", "it looks like", "I was wondering if").
- "We" instead of "you" when the codebase is the subject.
- One short clause of "why" attached to suggestions, not a paragraph.
- Hedges: "probably", "it might be worth", "totally up to you", "if we get a chance".
- Severity in the opener: "Heads up" for a likely bug, "small thing" or "it would be good" for nice-to-haves.

**You're a peer, not a gatekeeper.** The reviewer is rarely in a position to set conditions on someone else's PR, and even when they are, phrasing it that way reads as cocky. Every comment and the review body share what you noticed and ask what the author thinks. Never write what you want, need, or require, and never grade their work.

| Avoid | Because | Instead |
|---|---|---|
| "The one I'd want sorted before merge is X" | sets a condition on their merge | "I left a question inline about X, I might be missing something there" |
| "That's the blocker" / "needs to be fixed before merge" | a verdict you aren't positioned to give | "I think this one could bite us, what do you think?" |
| "The per-row isolation looks solid to me" / "The rest looks right to me" | grades their work from above | drop it, or a personal reaction: "I really liked how the tests read" |
| "We'd get the same result here without `SKIP LOCKED`" | gotcha framing, stated as settled fact | "I could be wrong, but I think this test would still pass without `SKIP LOCKED`" |
| "Could you also add X to the description?" stacked after findings | reads as an assignment list | "It might be nice to mention X in the description too" |

Read the review body and every comment once more as the author would: if any sentence sounds like a manager signing off, a teacher grading, or someone who already knows they're right, rewrite it as a teammate thinking out loud.

**Vary the openers across one review.** The phrases above are examples, not a template. Reuse one on every comment of the same severity and a review of three nits reads "Small thing: ... Small thing: ... Small thing: ...", which is the tell of a form being filled in, not a person reading code. Before Step 7, read the drafts' first words side by side: no two comments in one review open with the same phrase, and at most one opens with a severity label at all. The rest open straight on the observation ("We cover X, but not Y", "`SkuOrderReportsPage.js` already has a `SummaryTile` that..."), letting a hedge later in the sentence ("might be worth", "totally up to you", "if we get a chance") carry the severity. Other openers to rotate in when a label is warranted: "Minor one:", "Nit:", "Optional, but", "One more thought:".

**Humanization rules (apply to every comment):**
- No em dashes. Use commas, periods, or parentheses.
- No rule of three.
- No "Additionally", "Furthermore", "Moreover".
- No sycophancy ("Great approach!", "Excellent work!").
- Be specific, but keep the subject. "I think this needs a null check" beats "It might be worth considering adding a null check to improve robustness." Cutting to a bare imperative ("Add a null check here") overshoots into the clipped voice.

**Don't score points.** A well-argued PR description means most findings will contradict something the author claimed. That is exactly when the framing goes wrong. Each of these reads as passive aggressive:

| Avoid | Because | Instead |
|---|---|---|
| "reintroduces the flaw this PR set out to avoid" | quotes their own goal back as a scoreboard | describe the defect on its own terms |
| "the rationale doesn't hold" | a verdict on their thinking | "the rationale might need a tweak" |
| "To be fair, the legacy code does this too" | concessive opener, implies you're granting them something | "The legacy routes are in the same spot" |
| "this passes for a different reason than its name suggests" | gotcha framing | "I think this might be passing for a different reason" |
| "am I reading this right that this is unused?" | a faux-question that is really an assertion | assert it plainly, with the evidence |

Attach the point of agreement to the criticism rather than parking it after a "though". Offer fixes as proposals ("if you agree", "would that cover it?"). Never open a comment or a review body by summarizing what the PR does: the author wrote it.

**Format per finding:**

```
CRITICAL - `path/to/File.kt` L45 (introduced)
GitHub comment: I think `venue` can come back as null here when the search doesn't match. Should we add a guard?

SUGGESTION - `reservations/BookingService.kt` L32 (introduced)
GitHub comment: I noticed this one's doing both validation and persistence. Pulling validation out might make the tests easier for us.

NICE - `reservations/BookingServiceTest.kt` (file-level, pre-existing pattern)
GitHub comment: I don't see a test for the cancelled path. The sibling suites skip it too, so it's not a convention break, but it'd be good to lock down.
```

**Mark every finding `(introduced)` or `(pre-existing)`.** Determine which by checking whether the surrounding code, or the nearest sibling implementation, already does the same thing. A finding the PR did not cause needs different framing: say so in the comment, so the author isn't asked to answer for something they inherited. This changes the comment text, not the severity: an inherited security hole is still a security hole, but "the sibling adapter does this too" is information the author needs.

### Step 7: Present the Review

**There are two separate artifacts and they have different rules. Do not let one leak into the other.**

| Artifact | Audience | Contains |
|---|---|---|
| **A. The chat summary** | the user, deciding whether to post | context fetched, verdict, every finding with its draft, checklist, findings dropped in Step 5 |
| **B. The GitHub review body** | the PR author | one paragraph, opening on the main thing you noticed |

**A. Present to the user in chat:**

```
## PR Review: <PR title>

### Context Fetched
- Jira: <ticket key> - <summary> (or "not linked" / "MCP unavailable")
- Figma: <file/frame> (or "not linked")
- Notion: <page> (or "not linked")

### Coverage
- N files in the diff. Per subagent: correctness N/N, security N/N, tests N/N, SOLID N/N, clean code N/N. Skipped: <file> (<which subagent>, <reason>). Omit the skipped clause if none.

### Overall Assessment
[One paragraph: what the PR does, whether it aligns with the ticket/design, and the verdict: approve / approve with feedback / needs work]

### Findings

[Each finding: severity, file, line, (introduced|pre-existing), and its GitHub comment draft]

### Dropped in verification
[Each: the finding, and the specific fact that disproved it. Omit the section if none.]

### Checklist
- [ ] Logic correct and edge cases handled
- [ ] No security issues
- [ ] Tests cover new/changed behavior
- [ ] Code follows project conventions
- [ ] PR description explains what and why
- [ ] Ticket acceptance criteria met
- [ ] Design alignment verified (if applicable)
```

The "what the PR does" clause in the Overall Assessment is orientation **for the user**. It does not go on GitHub.

If any subagent skipped a file without a reason, the verdict says so in its first sentence. A review with unexplained partial coverage does not get to read as a clean review.

**B. The GitHub review body is one paragraph.** It opens on the main thing you noticed, said as something you noticed or a question, never as a condition ("I'd want", "before merge"). It doesn't grade the rest of the PR. A second short paragraph is allowed only for findings that have no line to anchor to (a wrong claim in the PR description, a stale response shape).

One paragraph is a shape, not a compression license. When the main finding is a causal chain, the opening states the mechanism link by link in plain words and the paragraph grows to fit it, same as Step 6's comprehensibility rule. "Details inline" supplements a mechanism the reader already grasped; it never substitutes for one.

Never put these in the review body:
- A summary of what the PR does. The author wrote it.
- A recap of what you verified or which of their claims checked out.
- A list of things you looked at and chose not to flag.
- Praise beyond a clause, or any verdict on the rest of their work ("the rest looks right to me").

```
Good: I think the race in `verifyMfaOtp.controller.ts` could activate a factor for a
number we never verified, I left the details inline. I might be missing something
there, so let me know what you think!

Bad:  Adds the two `/v2/registration/mfa/*` endpoints over the aggregate from #7421.
The layering is clean. Adapters are only constructed in `index.ts` and injected,
neither controller reaches into `infrastructure/`, and the responder maps are
genuinely exhaustive. I also went through the CLAUDE.md edits and I think they're
documenting what shipped. A few things I looked at and decided not to flag: ...
```

The bad version opens with a subjectless fragment, narrates the PR back at its author, grades their work ("The layering is clean"), recaps the verification, and appends a not-flagged inventory. Every one of those is padding that buries the main point.

The Good example above works because its defect fits in a clause ("could activate a factor for a number we never verified"). Do not imitate its compression when yours doesn't:

```
Cryptic: I think the formKey change can remount the edit form under the partner
mid-edit once the groups query resolves, details inline.

Clear:   I think I found something in the edit flyout: the modifier groups fetch
feeds into the form's `key`, and when the fetch resolves the key changes and
React remounts the form. So a partner who starts typing while that fetch is still
in flight could get their edits wiped. I left the details inline, let me know if
I'm missing something!
```

The cryptic version gestures at the mechanism in a clause and leans on "details inline" to carry it. It reads fine to the reviewer who just traced the chain, and to nobody else.

### Step 8: Post It

Only after the user approves. Create the review as **pending** so the user submits it themselves, which keeps the judgment call on severity with them:

```bash
# one call, body + all inline comments, no `event` field => PENDING
gh api --method POST /repos/{owner}/{repo}/pulls/{n}/reviews --input review.json
```

`review.json` is `{"body": "...", "comments": [{"path", "line", "side": "RIGHT", "body"}, ...]}`.

- Anchor every comment on a line that is **added in the diff**. Verify before posting: parse the diff's `@@` hunks for added-line numbers, or check `position` and `diff_hunk` on the created comments.
- **When a comment will not anchor, do not drop it.** Re-derive the target by copying the lines verbatim from the diff and stripping the leading markers, then find that range in the hunks. If it still will not anchor (the finding is about an absence, or the file has no added lines), fold it into the review body. Do not post it as a standalone file-level comment: that endpoint posts immediately and bypasses the pending-review gate. A finding that survived Step 5 never disappears for a mechanical reason.
- Report the review ID and the anchored lines back, then let the user submit.
- To submit on request: `POST .../reviews/{id}/events -f event=COMMENT|REQUEST_CHANGES|APPROVE`. Recommend an event, but the user chooses.
- To revise after posting: `PATCH /repos/{owner}/{repo}/pulls/comments/{comment_id}` for a comment, `PUT .../pulls/{n}/reviews/{id}` for the body. Both work after submission.

---

## Anti-patterns

- Don't review without fetching linked resources. The ticket and design ARE the spec.
- Don't give vague feedback. "This could be better" is useless. Say what to change.
- Don't nitpick formatting if tooling handles it.
- Don't sound like a checklist or a formal audit.
- Don't post comments to the PR without explicit user approval. Always draft first.
- Don't run subagents sequentially. The whole point is parallel dispatch.
- Don't trust a subagent finding you haven't confirmed in the code yourself (Step 5).
- Don't drop a finding without naming the fact that disproved it. "Could not confirm" softens a finding; it does not kill one.
- Don't present a review as clean when a subagent skipped files without saying why.
- Don't shorten a comment by dropping its subject. Cut sentences, not grammar.
- Don't open the review body by describing the PR to the person who wrote it.
- Don't set conditions or grade the work ("the one I'd want sorted before merge", "looks solid to me"). Share what you noticed and ask.
- Don't quote the author's stated goal back at them as evidence they missed it.
- Don't cite anything the author cannot resolve from the page they are on: a bare design node id, another PR by number with no gloss, a symbol that only exists on your branch, an acceptance criterion by number. Precise and unreachable is still cryptic.

---

## Flow position

```
[PR created or shared]
     |
     v
/flagrare:pr-reviewer
     |--- Step 1-2: fetch PR + linked resources (Jira, Figma, Notion)
     |--- Step 3: 5 parallel subagents (correctness, security, tests, SOLID, clean code)
     |--- Step 4: contextual review (ticket/design/doc alignment)
     |--- Step 5: verify every finding in the code; drop what doesn't survive
     |--- Step 6: humanize survivors into GitHub comment drafts
     |--- Step 7: present to the user (full) vs GitHub body (one paragraph)
     |--- Step 8: post as a pending review; the user submits
     |
     v
[user approves posting or adjusts]
```
