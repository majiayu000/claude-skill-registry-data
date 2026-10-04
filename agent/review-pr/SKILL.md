---
name: review-pr
description: Review a pull request with the user, then draft the review on GitHub for them to submit.
argument-hint: "<PR>"
disable-model-invocation: true
---

A **finding** is one claim about the PR: where it applies, what's wrong, and why it matters. A **note** is a finding the user adds themselves, a `file:line` and a rough remark; it enters as **keep** and skips triage. **Triage** sorts every finding onto a **disposition** before a word of the review is written. The review lands as a **pending review**, visible only to the user until they submit it from GitHub.

## 1. Establish the PR

Take the PR from the invocation; otherwise ask. Read its title, body, base, head SHA, and every existing review thread, from any reviewer. The **range** every pass reviews runs from the head SHA's merge-base with the base branch to the head SHA.

Done when you hold the head SHA, the range, and the existing threads.

## 2. Choose the passes

Detect which passes apply:

- `/code-review` at `high` effort: always.
- `/mattpocock-skills:code-review`: always. It finds the spec itself.
- `/browser-qa`: when the app is browser-driven and the diff touches something a user sees.

Confirm with one multiSelect AskUserQuestion that lists every pass, marking the ones that apply as recommended, each with a one-line reason.

Done when the user has chosen the passes.

## 3. Run the passes

Dispatch each chosen pass as its own sub-agent, all in parallel. Each brief carries the range, names the skill to invoke, and asks for the findings back as a list: file, line (or none), one-line claim, why it matters. A `/browser-qa` brief asks for each failure as a **repro**: steps to reproduce, expected against actual.

While the passes run, tell the user they can add notes at any point before step 6.

Done when every pass has returned its list. A reply without the list means the pass is still working: message it to finish and send the list.

## 4. Collect

Merge the lists into one, collapsing findings that make the same claim. Compare each finding with the existing threads, and tag one that repeats a thread with who raised it.

Done when every finding from every pass is on the list exactly once.

## 5. Triage

Judge each finding on its face, from what it claims and what you already know. Present it as a one-line summary with its location and any thread tag, and offer the four dispositions that fit it best, your recommendation first (AskUserQuestion, one finding per question, four per call). Work through every finding this way, however many there are.

- **keep**: valid; it goes in the review.
- **ask the author**: the user suspects a problem but can't show it; it goes in the review as a question.
- **discard**: invalid, already raised, or not worth the author's time.
- **investigate** _(interim)_: a sub-agent reads the code to confirm whether the finding holds.
- **explain** _(interim)_: a sub-agent reads the code and explains the finding so the user can decide.

Dispatch a sub-agent for each interim finding as soon as the user picks it, and keep triaging while it reads. As each reports, relay what it found and triage that finding again.

Done when every finding is **keep**, **ask the author**, or **discard**.

## 6. Write the comments

Ask the user once whether they have notes still to add. Then load `/humanize`: every word of the review follows it.

Write a comment for each **keep** and **ask the author** finding:

- **Anchor** it on the line that owns it: the line where the cause sits. GitHub accepts anchors only inside the diff's hunks, so when the cause sits outside them, anchor on the changed line that brings it into play. Anchor a range, `start_line` to `line`, when a suggestion replaces several lines.
- A finding with no owning line in the hunks goes in the review body. The body holds those findings and nothing else, so it is empty when everything anchors.
- Write as the user, a teammate talking to the author: first person where it's natural, the problem, why it matters, and what to do about it.
- Phrase an **ask the author** finding as the question the user wants answered.
- Give a `/browser-qa` failure as its repro.
- When prose alone won't make the point, add the smallest **shape** that does, next to the sentence it supports: a one-click `suggestion` for a fix confined to the anchored lines; pseudocode, a tree, a diff, or a diagram for logic, flow, or structure. Read [references/shapes.md](references/shapes.md) before writing one.

Done when every **keep** and **ask the author** finding has a comment or a place in the body.

## 7. Draft the review

GitHub allows each user one pending review per PR. When the user already has one on this PR, ask whether to delete it first.

Create the pending review in one call: write the payload as JSON and send it with `gh api repos/<owner>/<repo>/pulls/<number>/reviews --input <file>`. The payload holds `commit_id` (the head SHA), `body`, and `comments[]` of `{path, line, side, body}`, adding `start_line` for a range. `side` is `"RIGHT"`, or `"LEFT"` on a line the PR deletes. Omit `event`: that is what keeps the review pending.

Done when the pending review exists on the PR.

## 8. Report

Recommend a **mode** by asking whether merging the PR as it stands would do harm:

- **Request changes**: a **keep** finding would do harm on merge: a bug, a missed requirement, a risk to data.
- **Comment**: no **keep** finding would, but an **ask the author** question could reveal one.
- **Approve**: what remains is optional.

On the user's own PR, GitHub offers only Comment, so recommend Comment.

Report the PR's link, the recommended mode, and a one-line reason for it.

Done when the user holds the link and the recommendation.
