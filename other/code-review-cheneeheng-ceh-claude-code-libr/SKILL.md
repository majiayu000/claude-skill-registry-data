---
name: code-review
description: >-
  Load this skill when reviewing a pull request or someone else's diff: what to review first,
  blocking versus advisory comments, and how to structure the feedback. Trigger on "review this
  PR", "code review", "is this ready to approve".
disable-model-invocation: false
user-invocable: true
disallowed-tools: Edit Write
license: Apache-2.0
---

# Code review

Every comment must be clearly marked as **blocking** or **advisory**, and every review ends with
an explicit verdict.

Claude Code's built-in `/code-review` and `/security-review` hunt for defects in a diff. Use them
for the finding. This skill adds what they do not carry: the comment prefixes, the review order,
and the verdict, so the author knows exactly what blocks the merge.

## Procedure

1. Check scope drift before judging the code. Compare what the PR says it does (title, body,
   linked issue) with what the diff changes. A file or behavior the description does not account
   for is the first comment: `[blocking]` when it changes behavior, `[question]` otherwise.
2. Fan out to stack reviewers when the diff is large. If more than about 200 changed lines fall in
   files a stack reviewer covers, or the user asks for a deep review, and that reviewer agent is
   installed, write the diff with `git diff <base>...<head> > <scratch>/review.diff` and dispatch
   each matching agent in the background, in parallel, with the diff path, the PR's stated intent,
   and both commits: `ceh-python-service:python-service-reviewer` for Python service code,
   `ceh-web-frontend:web-frontend-reviewer` for frontend code. Review the rest yourself meanwhile.
   When they return, merge: one comment per problem at the same `path:line`, at the higher
   severity, and re-read every quoted line against the file before it becomes a comment. The
   five-`[blocking]` cap applies after the merge. Smaller diffs skip this step, since the fan-out
   costs more than it finds.
3. Check the spec on its own axis. When the PR links a spec (an issue with acceptance criteria, a
   spec or plan file), list each requirement in it and mark it met, missing, or diverging, quoting
   the diff line that meets it or the spec line nothing meets. When step 2 fans out, give this to
   one more background subagent with the spec path and the diff path, and keep it apart from the
   stack reviewers. Spec findings are never merged into or re-ranked against the standards
   findings: they answer "is it the right change", the rest answer "is the change written well",
   and a merge lets a style nit outrank a missing requirement. A missing requirement is
   `[blocking]`. To check the whole codebase against a build plan rather than one diff,
   `ceh-check-build-against-plan:check-build-against-plan` is the fuller check.
4. Review in priority order:
   1. **Correctness** — does it do what it claims? Are edge cases handled? Are errors swallowed:
      an empty `catch`, a log-and-continue, a fallback default that hides a failure?
   2. **Security** — injection risks, secrets exposure, input validation gaps
   3. **Test coverage** — is new behavior tested? Are tests testing behavior?
   4. **Design** — right abstraction? Fits existing patterns? Does a comment the diff left alone
      now describe code that no longer does that? Is a type weaker than the data: `any`, a bare
      `dict` or `str` where a domain type exists, optional where the value is always present?
      Where the repo writes down no standards, the baseline is Fowler's smells: duplicated code,
      long function, long parameter list, feature envy, data clumps, primitive obsession,
      shotgun surgery, speculative generality, middle man.
   5. **Style** — only flag if linting tools don't catch it
5. Leave a **summary** comment — one or two sentences: what the PR does and your overall read.
   Lead with anything that blocks. Give the step 3 spec findings their own **Against the spec**
   list. Close it with a **Dismissed** list: each finding you considered and dropped, one line
   with the reason, so the author can overrule the call.
6. Leave **line comments** — each prefixed `[blocking]` / `[advisory]` / `[question]`, anchored to
   the exact line, stating the problem and (for blocking) what would resolve it. Leave at most
   five `[blocking]` comments. With more, leave the five that matter most and say in the summary
   that the PR needs rework before the rest are worth reviewing.
7. End with an explicit verdict (see Output).

### Panel mode

Opt-in only, on "panel review", "review with several models", or "second opinion from another
model", because it costs several times a single review. Dispatch the same brief to two or three
background subagents in parallel, each on a different model through the Agent tool's `model`
parameter (for example `opus` and `sonnet`): the diff path, the PR's stated intent, and this
skill's priority order, prefixes, and quote-or-suppress rule, word for word. The brief is
identical so that a difference in findings comes from the model, not the prompt. Merge their
findings by `path:line` and rank by agreement: a problem every model raised comes first, then
those two raised, then single-model findings. Agreement orders the list and never changes a
severity, and a single-model finding still stands if its quoted line holds when you re-read it.
State in the summary which models sat on the panel and how many findings each raised.

### Gate mode

Opt-in only, on "gate this PR", "two reviewers must approve", or "dual review", because every
round costs two reviews. Use it when no human will review the change before it lands. Dispatch two
background subagents in parallel on the most capable model, with the identical brief Panel mode
uses. Neither sees this session or the other's report, so one reviewer's miss is not the other's.
The verdict is **Approve** only when both approve. Otherwise it is **Request changes** with every
`[blocking]` finding either one raised, each re-read against the file first. After the author
fixes them (`ceh-git-workflow:address-review-comments`), gate again with two fresh reviewers given
the same brief plus the list of findings to confirm resolved. Stop after three rounds and hand the
findings still open to a human, with what each round changed.

### Comment prefixes

| Prefix       | Meaning                                     | Author must                       |
| ------------ | ------------------------------------------- | --------------------------------- |
| `[blocking]` | Must be resolved before merge               | Fix or discuss with reviewer      |
| `[advisory]` | Suggestion, optional improvement            | Address or explicitly acknowledge |
| `[question]` | Seeking understanding, not a change request | Answer the question               |

Examples:

```
[blocking] This query is not parameterized — SQL injection risk on line 47.

[advisory] This helper could be extracted to a utility function for reuse.

[question] Why is this retry limit set to 3?
```

## Rules

- Do not comment on style a linter would catch.
- Do not re-litigate decisions already recorded in the repo's decision records unless new risk
  is identified.
- Do not review from memory — verify against current file contents.
- **Quote or suppress.** Every finding quotes the code it is about, as `path:line` plus the line
  itself. A finding you cannot anchor to quoted code goes in the Dismissed list as unverified,
  never in a line comment.
- **Judge from the code, not the brief.** A request that says "don't flag X" or "minor issues
  only" narrows where to look, never how severe a finding is. Report every finding at its real
  severity, and say where the brief asked for less.
- Approve with non-blocking nits rather than withholding approval to force trivial changes:
  withholding stalls the author and blurs what `[blocking]` is for.

### Responding as the author

- `[blocking]`: fix it, or reply with the reasoning and reach agreement before merge.
- `[advisory]`: address it or acknowledge why you're not ("good idea, out of scope for this PR").
- `[question]`: answer in-thread; if the code was unclear enough to prompt the question, that's
  often a signal to clarify the code or a comment.

Resolve a thread only once it's actually addressed. Don't merge over unresolved `[blocking]`
threads.

## Output

| Verdict             | When                                                                               |
| ------------------- | ---------------------------------------------------------------------------------- |
| **Approve**         | No `[blocking]` comments. Advisory items can be left to the author's judgment.     |
| **Request changes** | One or more `[blocking]` comments. Say what must change to flip to approve.        |
| **Comment**         | Questions outstanding, or not your call to approve — no verdict yet.               |
| **Cannot verify**   | Correctness rests on code, config, or data outside the diff. Name what settles it. |

When the comments are posted on a PR, the PR is the record. Otherwise (a local diff, or comments
not posted) save the summary, the line comments, and the verdict to
`.agents_workspace/code-reviews/<branch>-<YYYY-MM-DD>.md`, so the author can work through them in a
later session, and name the path in the reply.
