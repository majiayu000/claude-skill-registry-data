---
name: reviewing-a-change
description: Review someone else's change the way a senior reviewer does — read the whole change against its stated intent, verify claims by running rather than reading, give every finding a concrete failure scenario, rank by consequence, separate blocking from optional, and state what you did not check. Use when asked to review a PR, diff, branch, commit, or patch, "what do you think of this change", or before approving or merging. Not for reviewing your own diff before done (see workmanship).
---

# reviewing-a-change

Weak review reads the diff top to bottom, comments on naming and formatting, and ends with "LGTM, a few nits". Strong review starts from what the change claims to do, checks the claim against the code and the tests by running things, and delivers findings the author can act on, in the order that matters.

## 1. Establish what the change claims

Read the PR description, linked issue, and commit messages before the diff. Write one line: "this change claims to X". Every finding either supports or attacks that line. No description? Derive the intent from the diff and put it at the top of the review as an assumption the author can correct.

## 2. Read the whole change, not the hunks

- Check out the branch and open the files, not only the diff view: a hunk is right or wrong in the context of the function around it.
- For every changed function, list its callers (`grep -rn`). A change that is fine locally can break a caller relying on the old behaviour.
- What is missing is a finding too: a new endpoint with no auth check, a new field with no migration, a renamed symbol with a stale doc, config, or fixture reference, a behaviour change with no test.
- Read the tests as carefully as the code. Would each new test fail with the fix reverted? Do assertions check output, or only "no exception"? Does a mock echo the expected value back (see test-design)?

## 3. Verify, don't infer

Every claim in the description that can be checked in under a minute gets checked: run the suite on the branch, run the new test alone, hit the endpoint, run the script. "Tests pass" in a description is a claim; the command you ran and its summary line are evidence. Where you cannot run something, say which claims you took on trust.

## 4. Hunt with the checklists

Walk the diff once per lens that applies and record hits: trust boundaries (security-reflexes), edge cases (edge-case-sweep), races (concurrency-reasoning), numbers (numerical-care), complexity classes (perf-sanity), contract changes (api-surface-care), stored-data shape (data-migration-safety). A finding needs a failure scenario — "input X in state Y produces Z" — or it is a hunch. Hunches are allowed, labelled as hunches.

## 5. Rank and separate

Order by consequence: data loss and security, wrong output, crashes, then maintainability. Tag each finding **blocking** (must change before merge), **should** (fix now or file it), or **nit** (author's call). Style a linter or formatter already enforces is not a finding; the tool will say it. Taste that matches repo precedent is not a finding either.

## 6. Write for the author

- Each finding: `file:line`, what is wrong, the scenario, and the suggested fix or the one question that would resolve it. Suggest, don't rewrite: a review is not a competing implementation.
- Lead with the verdict — approve / approve with changes / request changes — and a one-sentence reason. Then blocking findings, then the rest.
- Name what was good only when it is specific and non-obvious (an edge case handled, a clean deprecation path). Skip generic praise.
- Ask questions you genuinely cannot answer; never ask one a grep would settle.

## 7. State the coverage

Close with what you checked and how (`ran pytest tests/orders: 41 passed`; `exercised POST /orders with an empty body`; `read all 6 callers of parse_row`) and what you did not (UI not rendered, migration not run against data). A review with no stated scope cannot be trusted or built on.
