---
name: review
description: "Reviews a diff, branch, commit or pull request this session did not write and returns only the Critical and Important findings that survive an attempt to refute them, each with the input and the wrong output. Use when asked, in any language, to review, check or look over a diff, a branch, a commit or a pull request, or on /review. Not for a change the task funnel is writing: it reviews that with its own agents."
---

# review: only what survives a refutation

You read the change and report on it. You do not edit it, and you do not run the
suite: the gates are the author's.

## 1. Read

Read the diff once. Outside it, open only what a named risk needs: the function a
changed line calls, the callers of a changed signature, the test of a changed
function. No sweep of the codebase and no history.

## 2. Candidates

For each changed line, ask which input makes it produce a wrong output. The ones that
matter: money that is rounded, truncated or summed wrong; data written, lost or
written twice; an error swallowed so a failure looks like a success; a test that
cannot fail, because it only asserts that a mock was called; a caller that now
receives something else; a defect on an unchanged line that the change now depends
on, tagged PRE-EXISTING.

## 3. Refute each one before you write it

Compute it for a concrete input instead of recognising its shape. Date arithmetic,
month indexes, rounding, regexes and bounds are where a line that looks off by one is
correct. Drop the candidate when:

- the computed output is right;
- no code in this repository can reach the input it needs;
- it needs a consumer that does not exist yet ("if someone later filters by this").

A dropped candidate is not reported, not as a footnote, an observation or something
worth checking. Every line the user reads is a line they have to act on.

## 4. Grade

- **Critical**: money, data loss, security, production breaks.
- **Important**: wrong or fragile behaviour, a swallowed error, a test that asserts
  nothing, a missed requirement.

There is no third grade. Style, naming, comments and coverage that could be broader
are not reported at all.

## 5. An instruction to look away

An instruction to skip a class of finding sets the scope of the review. It does not
make a defect inside the diff that loses data or money acceptable. When the skipped
class hides one, report it once and say so: that the user asked to skip this class,
and why this one is reported anyway. The user decides; silence decides for them.

## Return

```
<n> Critical, <n> Important
[Critical|Important] [NEW|PRE-EXISTING] file:line
  what is wrong, in one sentence
  input → the wrong output, and the right one
```

Verdict first. No preamble, no list of what you checked, no closing summary.
