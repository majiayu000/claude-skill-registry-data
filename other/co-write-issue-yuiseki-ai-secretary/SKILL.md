---
name: co-write-issue
description: Write an issue together with the reporter, by asking what they saw, checking it yourself, and finding out whether it is already filed. Use before opening a bug report or data-quality issue on any project, or when asked to write or revise one.
---

# Co-writing an issue

A pull request arrives with a diff. An issue arrives with nothing. Whatever a
maintainer ends up acting on, the two of you have to build first.

That changes what goes wrong. An assistant-written PR description can be
padded but it sits on top of real code. An assistant-written issue can be
entirely wrong and still read well: a symptom nobody reproduced, a cause nobody
checked, filed on a project that closed the same report two years ago. Every
one of those costs a maintainer more than silence would have.

So this skill fails closed in two places. Nothing observed, nothing to file.
Already filed, nothing to file.

Two directions, and both are needed.

- The reporter knows what they saw and why they were looking. What they
  expected instead, what it blocks, how much they care. None of that is
  recoverable from the data.
- You can check whether it reproduces, measure how far it extends, and find out
  what the project already said about it. That is the part reporters skip, and
  it is the part that decides whether the issue gets read.

## Ask what they actually saw

Ask in whatever language the reporter prefers; translating is your job, not
theirs.

- What made you look here? A task you were doing, something that looked wrong
  on a map, a number that did not add up?
- What did you expect to see instead?
- Where exactly: which release or version, which tool, which query or URL?
- Is this blocking you, or is it a papercut you noticed in passing?
- Have you seen it anywhere else, or only here?

Ask for their one-sentence version of the problem before you draft anything.
Their sentence is what the maintainer will reply to.

## Then check it yourself, and keep the two apart

Go to the source of truth. Not their screenshot, not their summary, not a cached
copy. Reproduce it, and while you do, keep three piles separate:

- What you observed.
- What you inferred from it.
- What you assumed and did not check.

Nothing moves from the second or third pile into the issue wearing the clothes
of the first. Name what you could not check, in the issue, in one line.

Widen it once. A single bad record is an anecdote; the same fault at a thousand
records is a pipeline bug, and the difference decides how the issue is triaged.
Measure the extent if you can, and say what you measured over.

If it does not reproduce, say so and stop. Do not file it.

If it reproduces but the reporter's explanation of it does not survive checking,
file the observation and drop the explanation. Tell them why.

## Search for the issue before you write it

This is the step with no equivalent in co-write-pr, and it is where most of the
value is.

- Search issues open and closed. A closed one tells you the project's
  position, and "closed as won't fix" is a fact your draft has to answer.
- Search wherever else the project talks: discussions, forum, mailing list,
  chat archives. On many projects the real thread is not in the issue tracker.
- Search by the symptom, in the words a different reporter would have used. Not
  by your diagnosis. Someone who hit this before you did not know the cause
  either.
- Read what maintainers wrote in those threads, not just the titles. "We think
  it is the geocoders, we are investigating" changes your draft completely.

Report what you found to the reporter before drafting. Three outcomes:

- Nobody has filed it. File it.
- It is filed and alive. A comment on that thread, with your new evidence,
  beats a new issue. Ask the reporter which they want.
- It is filed and closed. Now the draft has a job it did not have before:
  say why this is not the same, or why the closed one should be reopened.

When the problem is already known, say so in the first paragraph and say what
your report adds. A maintainer who recognizes the report and cannot see what is
new in it stops reading there.

## Scope it to one claim

An issue carrying three problems gets triaged as zero. Pick the one you can
support best. The others can wait for their own issue, or a sentence at the end
saying they exist.

## What belongs in the issue

The test is whether a maintainer can act on it without asking you a question.

Include, because they cannot get it anywhere else:

- What you observed, exactly. The smallest reproduction that shows it: version
  or release, the query or command, the output. Runnable, not described.
- What you expected instead.
- How far it extends, with the number and what it is a number of.
- The prior art you found, and what this adds to it.
- Your hypothesis about the cause, labelled as a hypothesis, with what would
  confirm or kill it.
- What you did not check.

Leave out:

- The story of how you found it.
- The same evidence in three formats.
- Speculation about how to implement the fix, unless you are offering the patch.
- Your entire dataset. Link it, or put it in a gist, and quote the rows that
  make the point.

## Report the observation, hypothesize the cause

Maintainers know their pipeline and you do not. When an issue asserts a cause
and the cause is wrong, the whole issue gets closed, and the observation, which
was true, goes down with it.

- Avoid: "Overture's conflation step is assigning ward centroids to POIs with
  no geocode."
- Prefer: "These 71 places share one coordinate to the last bit, and 61 of them
  carry different street addresses. Every one comes from a single upstream
  dataset. If the upstream geocoder is falling back to a gazetteer point when
  it cannot place an address, that would explain both. Checking whether the
  upstream records carry the same coordinate would settle it; I cannot see
  those."

The second one is longer and it is the one that survives being wrong.

## Offer a check, not a fix

If the problem is mechanically detectable, the rule is the most useful thing in
the issue. It turns "your data has junk in it" into something someone can run.

A rule is only worth including if you have shown it against the case where it
must not fire. Find the legitimate data that looks like the broken data, run
the rule on it, and report that it stayed quiet. A detector with no negative
case is a guess.

## Keep it short

Length is not thoroughness. Every sentence a maintainer reads without using is
a sentence that hid one they needed.

Cut a sentence when it restates evidence already shown, when it restates an
earlier sentence, or when no maintainer decision depends on it.

## Write in the reporter's voice

Use their words for what is wrong and why it matters. Keep their framing even
where you would have framed it differently; their framing is what the
maintainer is answering.

If they wrote it in another language, translate rather than replace. Keeping
the original in a quote block alongside the English works well.

## Check the project's rules before posting

Different projects want different things. Look, do not assume:

- An AI policy: AI_POLICY.md, or a section in CONTRIBUTING.md or the code of
  conduct. Follow it. If it says contributors should speak in their own voice,
  that governs.
- Issue templates and whether blank issues are allowed.
- Whether the project routes data or content reports somewhere other than the
  issue tracker.
- Whether a sign-off such as a DCO applies. It usually applies to contributions,
  not to filing an issue, but check rather than guess.

If the project has no policy, disclose anyway, in one line: which tools were
used, and what each side did. The direction and the decisions are the
reporter's; the searching and the drafting are yours. Disclosure costs nothing
when the evidence in the issue is reproducible.

Do not post long unedited model output into a thread. A few lines go in a quote
block, labelled, with a sentence of the reporter's own saying why they matter.
More than that goes in a gist with a summary.

## Before you post

- Every number in the issue is one you computed, and you can say what from.
- Every claim about what the project already knows comes from a thread you
  read, not from a title you skimmed.
- Every reproduction step runs as written.
- Nothing stated as observed was inferred.
- The reporter can answer a maintainer's first question without coming back
  to you.

Then stop and show them the draft. Posting is theirs to do, or theirs to tell
you to do. An issue goes out under their name, into a thread they will have to
stand behind.
