---
name: pr-review
description: >
  Evidence-based code review of a GitHub PR. Validates PR prerequisites, CI status and
  log sanity, technical rules (scope, diff coverage ~95%, single-responsibility, no side
  effects, DRY, ≤30-line methods, ≤4 positional args), system seams, and the security
  (incl. LLM/agent surface and CI supply chain), data handling and dependency checks,
  then writes review comments tagged [r]equired / [o]ptional / [f]uture / [c]uriosity.
  Use when the user says "review this PR", "review PR 123", "security review of this
  PR", "/pr-review", or asks for a code review of a pull request. Docs-only or proposal
  PRs need a design-doc review instead.
---

PR review in a fixed order. Gate, then orient in the repo, then function-level,
system-level and security checks, then write the comments.

The order matters: findings made before reading the surrounding code are generic, and
generic findings get ignored.

Never raise PR size, line count, or splitting the PR, anywhere. Large diffs change how
the reviewer reads (Phase 0.5 step 1), not what the author is asked to do.

## Phase 0 - Gate (block if fail)

Skip technical review until these pass:

1. **Scope present.** PR linked to a ticket OR has a 1-line scope description. If neither → request scope, stop.
2. **Branch hygiene.** No nested feature branches alive >1 week. Detect it, do not guess:
   ```bash
   gh pr list --base <headRefName> --state open          # PRs stacked on this branch
   git log --reverse --format=%cr origin/<default>..origin/<baseRefName> | head -1
   ```
   A non-default base whose oldest unmerged commit is older than a week → flag once.
3. **CI present.** Confirm a GitHub Actions workflow runs for this path. If missing → `[r] Add CI automation` + ask author or sync with TL on owner; create tracking task.
4. **CI green, and green for real.** `gh pr checks <PR>` must be green, and a green check is
   not proof. Open the log of every test job (`gh run view <run-id> --log | rg -n 'collected|passed|failed|skipped|error'`)
   and look for false positives: 0 tests collected, a step with
   `continue-on-error`, a job skipped by a path filter, a cache hit that skipped the test step,
   a matrix leg that never ran. A false positive → `[r]` plus a line in the working notes
   for the retro. A red check is attributed only after the base-branch baseline
   (Phase 0.5 step 6); a failure that is red on base too is not the author's.

## Phase 0.5 - Orient in the repo (do this before judging anything)

A review is only worth the reviewer's grounding in the codebase. Generic findings
("violates DRY", "consider extracting") get ignored; a finding that names the sibling
that already solves this gets fixed. Spend the first pass reading, not commenting.

Collect once, before reading anything, so no phase goes back to the network:

```bash
S=<scratch dir>
gh pr view  <PR> --json title,body,author,files,headRefName,baseRefName,closingIssuesReferences > $S/meta.json
gh pr diff  <PR> > $S/pr.diff            # whole diff, read it end to end first
gh pr view  <PR> --json commits          # per-commit intent; review in order if authored that way
gh pr checks <PR>                        # what CI actually says right now
gh api repos/<o>/<r>/pulls/<PR>/comments # existing inline threads, yours and the bots'
gh issue view <N>                        # every ticket the PR closes: the acceptance criteria
```

Then:

1. **Plan the reading by risk.** Rank the changed files: auth and access rules, persistence
   and migrations, concurrency and background work, public contracts (API, events, manifests),
   CI config, then everything else. Break ties by churn:
   `git log --since=6.months --format= --name-only -- <files> | sort | uniq -c | sort -rn`.
   Read the top of that list first. Defect yield falls off sharply past ~400 changed lines
   in one sitting (SmartBear/Cisco), so on a large diff split the *reading* into passes,
   never the PR. Record in the working notes which files were read in full and which were
   only skimmed, so the verdict does not claim more than was reviewed.
2. **Find the sibling.** `rg` for the same shape elsewhere in the service - another
   router's response mappers, another table's migration, another store's protocol,
   another background sweep. If one exists, it is the standard; deviation needs a reason.
   If none exists, say so rather than inventing a rule. T6, T9 and T10 all lean on this.
3. **Read the enclosing file, not the hunks.** A `+` line is judged against the 200 lines
   around it. Half of what matters is what the diff did *not* change.
4. **Find what actually runs in CI.** Read the workflow. Do not assume type checks or
   linting gate this service - if CI only runs unit tests, a type-level argument is not a
   blocker and a Protocol mismatch will reach production silently.
5. **Read prior threads on the same files.** The comments you collected above, and the
   same for any predecessor PR. Do not re-raise a resolved point; do correct a bot that
   got it wrong.
6. **Establish the baseline.** Run the test suite on the **base branch** before running it
   on the PR. A worktree is the cheap way (`git worktree add --detach <dir> <base>`).
   Without this you cannot tell an introduced failure from a pre-existing one, and
   attributing someone else's red test to the author burns the whole review's credibility.
7. **Re-review: start from your own threads.** Before looking for anything new, build a
   status table of every comment you posted in earlier rounds, checked against the current
   head, not against the author's reply:

   | Thread | Tag | Status | Evidence |
   |--------|-----|--------|----------|
   | `file.py:L42` | [r] | fixed / half / declined / unanswered | commit sha, line, or test |

   Half-fixed and unanswered `[r]` threads lead the new round. A declined `[r]` with a
   reason is argued once in-thread, then goes to stalemate handling, not to a new comment.

## Phase 1 - Technical review

Check, in order. One comment per finding, one location per repeated pattern.

Splitting, single behavior, DRY and argument count are recommendations; only high-impact
problems are requirements. Those checks therefore default to `[o]` and become `[r]` only when a concrete defect follows from them (a bug, a divergence
between copies, a caller that already passed arguments in the wrong order).

| # | Check | Action if fail |
|---|-------|---------------|
| T1 | Code accomplishes the declared scope (tests prove it) | `[r] Scope mismatch: <what is missing>` |
| T2 | Diff coverage ~95% on changed lines that carry logic | `[r] <file>:L<a>-<b> untested: <behavior>` |
| T3 | Each function does one thing | `[o] Split <fn> - does X and Y` |
| T4 | No side effects on inputs or globals | `[r] <fn> mutates <arg/global>; return new value` |
| T5 | One behavior per function (no boolean-branching params) | `[o] Split <fn> on <bool_param> into two functions` |
| T6 | DRY, SOLID and GoF patterns - no copy-paste, no tight coupling | `[o] Extract repeated logic to <util>`; `[r]` if the copies already diverge |
| T7 | Method ≤30 lines / class ≤30 elements (reference, not blocker) | `[o] <fn> is <N> lines; consider extract` - never block on 32 vs 30 |
| T8 | ≤4 positional args | `[o] <fn> has <N> positional args. Keyword args with defaults, or group only the ones that travel together` |
| T9 | Follows industry standards for what it is doing | `[r] <thing> is hand-rolled; <standard approach> is the norm because <reason>` |
| T10 | Follows the convention already in this repo | `[r] <file> does X; this does Y. Match the sibling or say why in the PR, not in a code comment` |
| T11 | Every new field has a producer AND a consumer **today** | `[r] Nothing writes/reads <field>. Cut it, or name the caller that will` |
| T12 | Logic sits on the right side of the wire | `[r] <thing> is presentation; the client owns it. Backend stores what it is given` |
| T13 | Fragile parsing or hand-built heuristics that a typed AI judgment would replace | `[o]` or `[f]` - never `[r]` |

Numbers in T2, T7 and T8 are guidance. Do not block PRs over small overruns.

### T1 - the ticket's own acceptance criteria

"Scope present" is the gate; this is the check. Open every issue the PR closes and read
its acceptance criteria as a list. For each one, name the test that proves it. A criterion
with no test is `[r]`, and a criterion the diff does not touch at all is the finding that
matters most, because it is the one nobody notices until the feature is called done.

If the PR closes no ticket, the scope line in its description is the list.

### T2 - measure the diff, not the repo

Whole-repo coverage says nothing about this change. Measure the lines the PR touched:

```bash
pytest --cov=<pkg> --cov-report=xml && uvx diff-cover coverage.xml --compare-branch=origin/<base>
# TS: vitest run --coverage --coverage.reporter=lcov && uvx diff-cover coverage/lcov.info --compare-branch=origin/<base>
```

Name uncovered ranges that carry logic (branches, error paths, conversions). Uncovered
logging, `__repr__` and re-exports are not findings. Coverage says a line ran, not that
it was checked; whether the assertions bite is S9.

### T8 - grouping arguments

Keyword arguments are encouraged, a dataclass only for values that
belong together. Do not suggest hiding every positional argument in a context object;
that moves the problem, it does not solve it.

### T10 - the deviation tell

The strongest signal is in the diff itself: **a comment or docstring that explains why this
code departs from an existing convention IS the finding.** If the author had to write
"unlike `app/models/api/assets.py`, these live here because…", the reviewer will ask the
same question the comment is pre-empting. Either match the sibling (Phase 0.5 step 2), or
move the rationale into the PR description where it can be argued, not into the file where
it hardens. "There is no convention yet" is a valid answer, but check first.

### T11 - producer and consumer

A field with no producer is speculation, and it ships as dead weight that later has to be
migrated or removed. For each new column, response key, enum member, or model field, name
the code that writes it and the code that reads it. If either is "the frontend, once it is
wired", the field is a `[r]` question, not a fact.

Two shapes that both fail:
- **No producer.** Nothing sets the value, so every row is null and the consumer needs a
  fallback nobody specified.
- **Backend-invented producer.** The backend derives a value it was never given, to fill a
  field the client should have supplied. That is T12 wearing a disguise.

Apply this to your own diffs with the same force you apply it to other people's. The
failure mode is asymmetric: it is easy to flag a stranger's unproducible field and then
add one of your own because you can picture the caller that will eventually exist.

### T12 - right side of the wire

Display labels, truncation, formatting, sort captions, and default titles belong to the
client, which knows the viewport and the locale. The backend stores what it is handed and
validates the bound. When the backend derives one of these, ask what it does when its
input is absent. If the answer is "fall back to something else it guessed", the
derivation is in the wrong process.

### T13 - typed AI judgment

Load the `typesafe:typesafe-ai` skill. Look for code that fakes judgment with brittle
machinery: regex ladders over free text, keyword lists that classify, scoring heuristics
with magic weights, multi-stage parse-and-guess over messy input. For each, check the
TypeSafe cookbooks (https://console.typesafe.ai/docs/cookbooks, fetch during orientation,
not mid-review) for a pattern that replaces it with a typed judgment. Name the cookbook and
the function it would replace. This is an opportunity, not a defect: `[o]` when the swap
is local, `[f]` when it changes a contract. Skip deterministic parsing of a formal grammar
(JSON, dates, CSV); a model is worse there, not better.

## Phase 1b - System-level review

T1-T13 are function-shaped. The findings that actually cause outages are not:
they live in the seams between a function and the runtime it runs in. Walk this table for
any PR that touches persistence, background work, streaming, or a request path.

| # | Dimension | What to look for |
|---|-----------|------------------|
| S1 | Async/sync seam | A blocking call (DB, file, network, `time.sleep`) reached from an `async def`. One slow caller stalls every request in the pod. Check whether the callee is sync and whether the call site awaits |
| S2 | Concurrency and replicas | Read-then-write without a constraint or lock; a background sweep with no `SKIP LOCKED` / advisory lock running in every replica; shared mutable state on a singleton |
| S3 | Schema and query fit | Does an index exist for the query that was actually written (leading column, sort direction, composite order)? Is there a CHECK/UNIQUE where the code assumes one? Does the ORM declare what the migration created? |
| S4 | Deploy coexistence | Old and new code run together during rollout. A renamed column, a new required field, or a changed event shape must go expand/contract: add the new shape, dual-write or dual-read, migrate, remove the old in a later release. One-step renames break the pods that have not restarted yet |
| S5 | Lifecycle and teardown | Background tasks cancelled and awaited on shutdown; pools closed; a `while True` that never returns is not a shutdown path |
| S6 | Scale | N+1 across a page; unbounded read; an extra round trip per row; a count query that duplicates the page query |
| S7 | Failure surfacing | An error path that degrades to an empty result, a truncated list, or a stream that never closes. Every degradation needs a visible surface and a must-fail test |
| S8 | Entry-point matrix | The invariant this PR adds, is it enforced on *every* way in (REST, WS/SSE, scheduled sweep, CLI, direct store call)? One shared resolution function, not a check per route |
| S9 | Test strength | Would the test fail if the code were wrong? See below |
| S10 | Observability | A new path, job, or failure mode can be seen working in production: a structured log with the ids needed to trace it, a metric or status field for the thing an on-call person will ask about. A background loop with no heartbeat or counter is invisible until a user reports it |

S1-S10 are all part of the default single round. When the review is split (see Round strategy), S9 moves to the specifics round unless the tests are the deliverable.

### S9 - prove the test bites

Weak shapes: assertions looser than the contract (`is not None`, `>= 1`, substring), one
happy case where a table is needed, a mock that has drifted from the real shape, time,
randomness or dict/set ordering left uncontrolled, a retry that turns a flake green.

The cheap evidence is a hand mutation. Flip the comparison, delete the guard, return the
default, then run the test that claims to cover it. Still green → the test does not check
that behavior, and the finding is `[r]` with the mutation named:
"`<file>:L<n>` changed `<` to `<=`, `<test>` still passes."

## Phase 1c - Security, data handling and dependencies

T and S ask whether the code is right. This asks whether it is safe to run, and it is the
half a structural review keeps missing. Walk it for any PR that touches a route, a query,
a filesystem path, an outbound call, a log line, a response body, a prompt, the dependency
manifest, or a CI workflow.

| # | Dimension | What to look for |
|---|-----------|------------------|
| D1 | Injection | Untrusted input reaching SQL, a shell, a filesystem path, or a template. Parameterised query or a validated allowlist, never string building. A path from a request must be normalised and re-checked against its root after normalisation, not before |
| D2 | Authorization | Every new route, handler, and store call asserts the caller may act on THIS object, not just that they are logged in. The ownership predicate matches the sibling route's; a new one that reads differently is either a bug here or a bug there |
| D3 | What leaves the process | No secret, credential, token, PII, or resolved private config into a log, an exception message, or a response body. Stack traces and internal state stay server-side. This is also what the CodeQL scanner posts threads about |
| D4 | Input at the boundary | Size caps on the actual read, content type checked after sanitisation, bounds validated before use. A cap on the listing is not a cap on the read |
| D5 | Dependencies | A new package needs a reason, a maintained upstream, a compatible licence, a name that is not a typosquat, and its lockfile in the same commit. Prefer the library the service already depends on. Check whether the thing being added is 30 lines the repo already has |
| D6 | Web surface | Escaping on anything rendered, CSRF on state-changing routes, CORS not widened, cookie flags unchanged unless the PR is about them |
| D7 | Outbound requests (SSRF) | A URL, host, bucket, or object key that a caller can influence, fetched by the server. Allowlist the destination; block link-local and metadata addresses; an S3 key from a request is re-scoped to the caller's prefix |
| D8 | Unsafe deserialization | `pickle`, `yaml.load` without `SafeLoader`, `eval`, `exec`, dynamic import from data. Anything read from a user, a bucket, or a model is untrusted |
| D9 | Crypto and abuse | Hand-rolled crypto, non-constant-time secret comparison, `random` for tokens instead of `secrets`; a new expensive or public route with no rate limit, quota, or size budget |
| D10 | CI and supply chain | Workflow changes: third-party actions pinned to a commit SHA, `pull_request_target` or `workflow_run` never checking out untrusted code with secrets, `permissions:` not widened, no secret echoed into a log, no `curl \| sh` |
| D11 | LLM and agent surface | Prompt injection: file contents, tool output, or web text reaching a prompt that can call tools. Model output reaching exec, SQL, a path, or a shell without the same validation as user input. Tool permissions wider than the task. Sandbox escape routes (mounted secrets, network egress, writable host paths). Secrets or other tenants' data inside a prompt. No cap on turns, tokens, or cost, so one bad loop burns the budget |

A `[r]` here follows the same evidence rule as everywhere else: name the reachable call
site, or post it as `[c]`.

## Phase 1d - What ships with the change

| # | Check | Action if fail |
|---|-------|---------------|
| C1 | Docs that describe the changed behavior changed with it (README, the service's docs/, the manifest comment that states the contract) | `[r] <doc> still describes the old behavior` |
| C2 | The PR description says why, links the ticket, and matches what the diff actually does | `[o] Description says X; the diff also does Y. Say so in the description` |
| C3 | A behavior change that needs a deploy step (migration, bundle re-upload, env var, backfill) says so where the deployer will look, along with how to roll it back | `[r] <change> needs <step>; nothing in the PR says so, or how to undo it` |

## Phase 1e - Stack prompts

Ask these only where the diff touches that stack. They are the ones that actually bite.

| Stack | Ask |
|-------|-----|
| Python | Blocking call inside `async def`; a mutable default; a bare `except` swallowing the failure; a Protocol the implementation no longer satisfies; type checking that is not in CI, so a type argument is not a blocker |
| TypeScript / React | A new object or function identity in a prop or a dependency array; state derived on every render instead of memoised; an effect with no cleanup; `any` hiding a shape that changed on the wire; accessibility regressions: an interactive element with no label, a click handler on a non-button, a dialog that does not trap and restore focus, a control unreachable by keyboard |
| SQL and migrations | Index for the query as written (leading column, sort direction); migration reversible and safe while old pods still run (S4); constraint the code assumes actually declared; DDL that takes a long lock on a big table: `CREATE INDEX` without `CONCURRENTLY`, `ADD COLUMN` with a volatile default, `ALTER COLUMN TYPE`, adding a `NOT NULL` or FK without `NOT VALID` then `VALIDATE` |

## Evidence rule - prove it before posting

**Every `[r]` needs evidence a reader can check.** A review that is right but unproven
reads the same as a review that is wrong, and the author will litigate it. Before posting
a required finding, do the cheapest thing that settles it:

- Run the repro. A five-line script that shows the hang, the `TypeError`, or the duplicate
  index is worth more than a paragraph of reasoning.
- Mutate the code. For a test-strength claim, the mutation that stays green is the proof (S9).
- Cite the call site. `file.py:LN` for the caller that makes the bug reachable, not just
  the line where the bug lives.
- Name the sibling. "`app/routers/assets.py` does X" beats "this is unconventional".
- Check the claim against the branch, not memory. Bots and prior rounds go stale, and the
  author may have already fixed it in a commit you have not fetched.

If a finding cannot be proven cheaply, post it as `[c]` phrased as a question, not as `[r]`
phrased as a fact. Downgrading an uncertain finding costs nothing; an overconfident `[r]`
that turns out to be wrong costs the next three.

## Phase 2 - Communication framework

**Tag every comment** with one of:

- `[r]` - must change before merge (required)
- `[o]` - author may take or skip (optional)
- `[f]` - for a follow-up PR / ticket (future)
- `[c]` - question, no action expected (curiosity)

### Round strategy

**One round by default: every check, every finding, tagged.** The tags already tell the
author what blocks and what does not; holding a finding back to a later round only costs
the author a second context switch, often on the same lines they just changed. Google
eng-practices say the same: give all comments in one pass and label the minor ones.

Staging (high-level changes first, specifics only once the main scope is met) is
**conditional**. Split into a high-level round and a specifics round only when one of these holds:

- **Scope unmet (T1).** An acceptance criterion is missing or not reached.
- **A redesign is on the table.** A `[r]` would move, replace, or delete the code that
  the line-level findings sit on, so those findings would be void after the fix.

When splitting, the first round carries T1, T9-T12, S1-S8, S10 and all of D1-D11 (a
security finding is never held: held is shipped if the PR merges first), and its summary
says that line-level comments follow once the design settles. Everything else, including
S9, T13 and C1-C3, goes in the next round.

Before holding anything, check it against the `[r]` fixes: a finding on the same lines
or the same state as a required fix always goes out now, or the author reworks those
lines twice.

**Later rounds** (re-review after the author pushes) open with the thread status table
(Phase 0.5 step 7), then only what the new commits introduced or what was genuinely
unreachable before. A finding that only surfaces in round 3 was usually reachable in
round 1 with one more `rg`.

### Drop / keep

**Drop:**
- "you" - refer to the code, not the author. (`successfuly -> successfully`, not "you misspelled")
- Hedging / pleasantries inside comments. Praise once at top, not per file.
- Restating what the diff already shows.
- Comments on every occurrence of a pattern - comment once, request global change.
- Style nits a formatter would fix - link the formatter once (e.g. `black`, `ruff`, `prettier`, `eslint --fix`).

**Keep:**
- Concrete fix proposal, not "consider refactoring".
- File:line anchor.
- The *why* if not obvious.

### Code samples

- Max **3 sample snippets per round**. Beyond that → describe the change in prose.
- Samples only for clear, uncontroversial suggestions. Controversial → discuss, don't paste code.

### Praise

- Offer **sincere** praise when warranted, especially for new joiners. Once at the top, specific to the change. No filler.

### Stalemate detection

If any of these → escalate, do not keep arguing in-thread:
- Tone turns tense / hostile
- Notes-per-round not decreasing
- Heavy pushback on many notes

**Actions:** contact TL, pair-program next round, request design review, add another reviewer.

## Comment format

```
[<Tag>] <file>:L<line> - <problem>. <fix>.
```

Examples:

```
[r] auth.py:L42 - `user` can be None after `.find()`. Guard before `.email`.
[o] api.py:L88-140 - function does validate + normalize + persist. Split into 3.
[o] utils.ts:L12 - 34-line fn just over 30-line guideline. Extract `parseHeader`.
[f] db.py:L201 - N+1 on `.orders`. Switch to `selectinload` next PR.
[c] worker.py:L55 - why `time.sleep(0.1)` here?
[o] handler.py - 6 positional args. `org_id, user_id` always travel together, group those as `Owner`; the rest as kwargs.
[r] rules.py:L30 - `>` to `>=` keeps test_rules.py green. Add the boundary case.
```

## Verdict criterion

Approve when the change, as it stands, clearly improves the health of the codebase and
meets its acceptance criteria, even if it is not how the reviewer would have written it
(Google eng-practices). Open `[o]`, `[f]` and `[c]` never hold an approval. Changes
requested means at least one `[r]` that survived the evidence rule. Comment only means
the review could not reach a verdict, and says what is missing (a skimmed file, a job
that did not run, an unanswered `[c]` that decides it).

## Output structure

Two artifacts, because they have different readers. Keep them apart or the working notes
leak into the PR.

1. **Working notes** (yours, never posted): the risk-ordered reading plan with which files
   were read in full and which were skimmed, every candidate finding with the evidence that
   settles it, including the ones you disproved and the threads you checked and dropped,
   the re-review thread status table, and any CI false positive for the retro. This is what
   makes the next round cheap and what stops you re-raising a point the author has already answered.
2. **The comments** (the author's): only what survived the evidence rule, in the shape
   below. Run them through `pr-post-comments` to post.

Produce the comments in this shape, in order:

```
## Gate
- CI: <green / green but <false positive> / red (introduced | pre-existing) / missing>
- Scope: <linked ticket / inline / missing>
- Acceptance criteria: <N met of N total, name the unmet ones>

## Round <N> - <full | high-level, specifics to follow>

### Prior threads
<re-review only: counts by status, name the unanswered and half-fixed [r]>

### Praise
<one line, only if warranted>

### Required
- ...

### Optional
- ...

### Future
- ...

### Curiosity
- ...

## Stalemate watch
<note only if signs present>

## Verdict
<approve / changes requested / comment>, one line of why, per the verdict criterion
```

Omit empty sections.

## Reviewing your own diff

Same tables, same evidence rule. Bot reviewers (Copilot, CodeQL) catch patterns; they
do not model a person. T9-T13, S1-S10 and D1-D11 are what a teammate will raise, and
C1-C3 is what the person deploying it will.

## Boundaries

- Reviews only. Never pushes code, and never submits an approval or a change request via
  `gh`: the verdict is a recommendation in the text. The one exception is an explicit
  request from the user in the current conversation.
- Output is comments ready to paste into the PR, posted only through `pr-post-comments`,
  and only after the user approves the drafts.
- Numeric thresholds (~95% diff coverage, 30 lines, 4 args) are **guidance** - flag, don't auto-block on small overruns.
- Never raise PR size, line count, or splitting the PR up, in any round or any section.
- Severity is the `[r] [o] [f] [c]` tags and nothing else: no emoji markers, no blocker/nit vocabulary.
