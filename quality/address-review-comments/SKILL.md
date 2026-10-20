---
name: address-review-comments
description: >-
  Load this skill when acting on review feedback left on your change: verify each comment, fix what
  holds, push back with evidence on what does not, reply to every thread. Trigger on "address these
  review comments", "fix the review feedback", "the reviewer said".
argument-hint: "[PR number or URL]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Reading and replying to PR threads needs the GitHub CLI (`gh`) authenticated against the repo.
  Without it, work from comments pasted into the session and report replies as text.
license: Apache-2.0
---

# Address review comments

Treat each review comment as a claim to check, not an order to follow. Done means every comment
has a verdict (fixed, pushed back, or answered), each fix is proven by a check run after it, and
every thread has a reply.

## Procedure

1. **Collect every comment** with its file, line, and prefix. For a PR:
   `gh pr view <n> --comments` and `gh api repos/{owner}/{repo}/pulls/<n>/comments`. Number them.
2. **Verify each one against the current code** before deciding. Open the line, read enough
   around it to know whether the claim is true, and run the code or a test when reading cannot
   settle it. A comment about a line that has since changed may already be resolved.
3. **Give each comment a verdict:**
   - **Holds** → fix it. The fix is the smallest change that resolves the stated problem.
   - **Does not hold** → push back. Quote the code or output that shows why, in the reply.
   - **Unclear** → ask one specific question in the thread. Do not guess the reviewer's intent
     and change code on the guess.
4. **Fix the holding comments one at a time**, running the change's own checks after each.
   `[blocking]` comments come first.
5. **Reply in every thread** with the verdict and its evidence: the commit that fixes it, the
   output that shows the claim is wrong, or the question. Resolve a thread only when it is fixed
   or the reviewer agreed.

## Rules

- Agree only with evidence. "Good catch", "you're right" and "great point" before checking the
  code are performative: a reviewer reads them as a fix promised and stops looking.
- A pushback cites code or output, never preference. "I'd rather keep it" is not a reason. "The
  caller at `api.py:88` already validates this, see the test at `test_api.py:40`" is.
- A comment that asks for more than the PR's scope gets a reply naming the follow-up, not a
  drive-by change in this PR.
- Never resolve a `[blocking]` thread you pushed back on. The reviewer resolves it, or the
  disagreement goes to the person who owns the merge.

## Output

One line per comment, in order:

```
1  src/api.py:47   [blocking]  fixed in a1b2c3d, test_api.py::test_rejects_empty added
2  src/api.py:90   [advisory]  pushed back: caller validates at api.py:88 (quoted in thread)
3  src/db.py:12    [question]  answered: retry limit matches the provider's documented cap
```
