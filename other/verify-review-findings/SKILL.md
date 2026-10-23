---
name: verify-review-findings
description: 'Use when a pull request has review comments or bot findings to check or address. Also use it for "are these comments right?", "triage the review", "address the review comments", "check the PR comments", or "check what the bot found". Checks each finding against the code at the head of the pull request, and confirms the file, the line, and the claim. Fixes each confirmed finding without waiting, replies by fixed rules, and reports each verdict. Asks the user before it declines a human comment. Not for writing a fix from a bug report (use `scope-confirmed-changes`).'
metadata:
  shadowclone-category: review
  shadowclone-section: workflow
  shadowclone-applies-when: when a pull request has review comments or bot findings
  shadowclone-voice: "true"
---
# Verify Review Findings

## Use when

A pull request has review comments, bot findings, or a list of issues from another agent. A finding is a claim, not a fact. Check each one before you change code or reply.

This skill follows `shadowclone-work` for fixes, commits, pushes, and fix replies. It differs from `shadowclone-work` only in how it declines a finding. A wrong AI finding gets a one-line reply. A human comment is declined only after the user decides.

## Gates

1. Did you read each finding at the head commit of the pull request? A finding about an older commit can be stale.
2. For each finding, do the file and the line exist, and does the code around them do what the finding says? A finding can be right about the problem and wrong about the place.
3. Can you show the claim with a test, a command, or the code itself? If not, label it as not verified.
4. Did you ask what each suggested fix would break, such as a caller, a test, or a documented behavior?
5. Does each finding have a verdict: confirmed, partly right, pre-existing, wrong, stale, or not verified?
6. Did you fix each confirmed finding, reply on its thread with the commit SHA only, and ask the user before you declined a human comment?

## Process

Write in the user's voice. Before you write, read `~/.agents/voice.md`. If it does not exist, build it once from the user's merged pull requests, review comments, and commit messages. Use only text that the user wrote, and name those sources in your handoff. Never overwrite an existing or linked `voice.md`.

1. Fetch the head of the pull request from `origin`, because the local tree can be on another branch. Write down the commit hash.
2. Read the comments without their analysis blocks. Bot comments hold long `<details>` blocks. Remove them with `perl -0pe 's{<details>.*?</details>}{[analysis omitted]}gs'`. Inline comments come from `gh api repos/<owner>/<repo>/pulls/<number>/comments` and carry `path` and `line`.
3. List each finding in one table, with its source (a human or an AI reviewer), its `file:line`, and its claim.
4. For each finding, read the code at that location and its callers. Compare the claim with the real behavior.
5. When the claim is about behavior, run a focused test or a command that shows it.
6. For each suggested fix, list what it changes for callers, tests, and users. A fix that is right in one place can break another place.
7. If a finding is true but the same problem existed before this change, give it the verdict pre-existing. Leave it out of the fix, and say so in the report.
8. Give each finding a verdict, with the evidence that supports it.
9. If a finding is confirmed or partly right, fix the confirmed part without waiting for the user. Use `scope-confirmed-changes` to keep the fix small. Follow `shadowclone-work` to commit in the pull request that owns the code, restack if needed, and push.
10. After the final push, reply to each fixed thread with only the full 40-character SHA of the commit that fixed it. Write nothing else. This applies to human and AI threads.
11. Resolve each fixed AI thread with the `resolveReviewThread` mutation in `gh api graphql`. Leave each fixed human thread open for its reviewer.
12. If an AI finding is wrong or stale, reply with one line that declines it and gives the reason. Leave the thread open.
13. If you would decline a human comment, do not reply. Report the comment and your reason to the user, and wait for the user's decision.
14. Report to the user: each fix with its SHA, each declined AI finding with its reason, and each human comment that waits on a decision. Count the open threads again, and list them. An open thread blocks the merge when the repository requires resolved conversations.

## Example

**Situation:** A review bot says that a function can return null and crash its caller. It suggests a null check.
**Easy route:** Add the null check, and reply "Fixed".
**Hidden cost:** The function never returns null, because a type guard on the line above handles that case. The extra check hides the real contract, and the reply tells the reviewer something false.
**Best route:** Read the function at the head commit, and run its test with an empty input. Give the finding the verdict "wrong", and reply with one line that names the guard.
**Evidence:** The test with the empty input passed at the head commit. The reply read "Declining: the type guard at `parse.ts:41` returns before the value can be null."

## Guardrails

- Never decline a human comment before the user decides.
- A fix reply is the commit SHA only. A declined AI finding gets one line with the reason. Write no other words on the pull request.
- Do not accept a finding because a bot or a senior reviewer wrote it. Do not reject it for that reason either.
- Quote the code that proves each verdict. Do not paraphrase it.
- Keep each finding separate. Do not merge two findings into one verdict.
- A finding that you cannot check stays "not verified" in the report, and gets no reply.
- A resolved or addressed marker is not proof. A bot can mark a finding as addressed because the commit was in the range it reviewed. Check the head.
- If the reason to decline is a claim about behavior, run a command that tests the claim before you reply.

## Completion

- The head commit hash that you checked.
- A table row for each finding: the source, the `file:line`, the claim, the verdict, and the evidence.
- Each command or test that you ran, with its result line.
- For each fix, its commit SHA and what it changes for callers and tests.
- For each thread, the reply and its resolved state. Each thread that stays open, with the reason.
- Each human comment that waits on the user's decision, with the reason to decline it.
