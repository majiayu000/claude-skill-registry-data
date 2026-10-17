---
name: handle-feedback
description: Checks review feedback against the code and answers it with fixes and evidence. Use when code review feedback from a person or a pull request has arrived, before implementing the suggestions.
---

# Handle Feedback

Review feedback is a claim about the code, made by someone who may be missing context. Check each item before acting on it, and answer with changes and evidence rather than agreement.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Commit your work on the feature branch as you go: the spec and plan may be held back, code never is. If you are on `main`, `master` or the plan's `Base:` branch, first ask once: "I'll create branch `<name>` for this work. Reply with **yes** or **no**." If your partner declines, do no code work until a branch is agreed. Nothing is pushed or merged without asking.

1. Find the pull request and its comments (`gh pr view --comments`; inline review comments via `gh api repos/{owner}/{repo}/pulls/{pr}/comments`), and read the spec and plan it links.
2. Read all the feedback before reacting to any of it.
3. Restate each item as a technical requirement in your own words. If an item could be read two ways that lead to different changes, ask about it before implementing it or anything that depends on it; carry on with the rest.
4. Check each item against the codebase. Does it hold here? Does it break something that currently works? Is there a reason the code is the way it is? Does the reviewer have the full context?
5. Where a suggestion adds a feature nothing uses, grep for callers first and say what you found. An endpoint nothing calls should be removed, not implemented properly.
6. Where a suggestion is wrong, push back with technical reasoning and point at the tests or code that show it. Where it conflicts with a decision your partner already made, raise it with them rather than choosing for them.
7. Where an item would alter behavior the spec describes, invoke the `dietpowers:update-spec` skill before implementing it.
8. Where you cannot verify a claim, say what you would need to verify it instead of proceeding on assumption.
9. Implement in order: things that break or are insecure, then simple fixes, then complex ones. Start each fix with a test that reproduces the problem and fails, then make it pass. Check for regressions. Commit each fix with its test.
10. Draft a reply for each item: for correct feedback, the fix and where it landed, without agreement or thanks; for pushback, the reasoning and evidence; if you pushed back and turned out to be wrong, what you checked and what it showed.
11. Show your partner the drafts and ask one question: "Push the fixes and post these replies? Reply with **yes** or **no**." Post nothing yet: replies must not cite changes the pull request does not have.

Terminal state: invoke the `dietpowers:prove-done` skill, then the `dietpowers:finish-branch` skill to push the fixes to the open pull request. Once the push succeeds, post the approved replies; on GitHub, reply inside each comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a new top-level comment. Then, if `.dietpowers/trackers/open-items.md` has `open` items, ask: "There are <N> open items. Triage them now? Reply with **triage** or **later**." On **triage**, invoke the `dietpowers:triage-open-items` skill.
