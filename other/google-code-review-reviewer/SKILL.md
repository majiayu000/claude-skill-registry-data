---
name: google-code-review-reviewer
description: >-
  Use when reviewing a code change, deciding what to inspect, applying Google's review standard,
  writing comments, reviewing quickly, navigating a change, or handling pushback. Do not use
  when only preparing your own change for review.
---

# Google's Code Review Guide for Reviewers

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## The Standard of Code Review

The primary purpose of code review is to make sure that the overall
code health of Google's code
base is improving over time. All of the tools and processes of code review are
designed to this end.
First, developers must be able to _make progress_ on their tasks. If you never
submit an improvement to the codebase, then the codebase never improves. Also,
if a reviewer makes it very difficult for _any_ change to go in, then developers
are disincentivized to make improvements in the future.
On the other hand, it is the duty of the reviewer to make sure that each CL is
of such a quality that the overall code health of their codebase is not
decreasing as time goes on. This can be tricky, because often, codebases degrade
through small decreases in code health over time, especially when a team is
under significant time constraints and they feel that they have to take
shortcuts in order to accomplish their goals.
Thus, we get the following rule as the standard we expect in code reviews:
**In general, reviewers should favor approving a CL once it is in a state where
it definitely improves the overall
code health of the system
being worked on, even if the CL isn't perfect.**
A key point here is that there is no such thing as "perfect" code&mdash;there is
only _better_ code. Reviewers should not require the author to polish every tiny
piece of a CL before granting approval. Rather, the reviewer should balance out
the need to make forward progress compared to the importance of the changes they
are suggesting. Instead of seeking perfection, what a reviewer should seek is
_continuous improvement_. A CL that, as a whole, improves the maintainability,
readability, and understandability of the system shouldn't be delayed for days
or weeks because it isn't "perfect."
Reviewers should _always_ feel free to leave comments expressing that something
could be better, but if it's not very important, prefix it with something like
"Nit: " to let the author know that it's just a point of polish that they could
choose to ignore.
Note: Nothing in this document justifies checking in CLs that definitely
_worsen_ the overall code health of the system. The only time you would do that
would be in an emergency.

### Principles

*   Technical facts and data overrule opinions and personal preferences.
*   On matters of style, the [style guide](http://google.github.io/styleguide/)
    is the absolute authority. Any purely style point (whitespace, etc.) that is
    not in the style guide is a matter of personal preference. The style should
    be consistent with what is there. If there is no previous style, accept the
    author's.
*   **Aspects of software design are almost never a pure style issue or just a
    personal preference.** They are based on underlying principles and should be
    weighed on those principles, not simply by personal opinion. Sometimes there
    are a few valid options. If the author can demonstrate (either through data
    or based on solid engineering principles) that several approaches are
    equally valid, then the reviewer should accept the preference of the author.
    Otherwise the choice is dictated by standard principles of software design.
*   If no other rule applies, then the reviewer may ask the author to be
    consistent with what is in the current codebase, as long as that doesn't
    worsen the overall code health of the system.

### Resolving Conflicts

In any conflict on a code review, the first step should always be for the
developer and reviewer to try to come to consensus, based on the contents of
this document and the other documents in
The CL Author's Guide and this
Reviewer Guide.
If that doesn't resolve the situation, the most common way to resolve it would
be to escalate. Often the
escalation path is to a broader team discussion, having a Technical Lead weigh in, asking
for a decision from a maintainer of the code, or asking an Eng Manager to help
out. **Don't let a CL sit around because the author and the reviewer can't come
to an agreement.**


## What to look for in a code review

### Design

The most important thing to cover in a review is the overall design of the CL.
Do the interactions of various pieces of code in the CL make sense? Does this
change belong in your codebase, or in a library? Does it integrate well with the
rest of your system? Is now a good time to add this functionality?

### Functionality

Does this CL do what the developer intended? Is what the developer intended good
for the users of this code? The "users" are usually both end-users (when they
are affected by the change) and developers (who will have to "use" this code in
the future).
Mostly, we expect developers to test CLs well-enough that they work correctly by
the time they get to code review. However, as the reviewer you should still be
thinking about edge cases, looking for concurrency problems, trying to think
like a user, and making sure that there are no bugs that you see just by reading
the code.

### Complexity

Is the CL more complex than it should be? Check this at every level of the
CL—are individual lines too complex? Are functions too complex? Are classes too
complex? "Too complex" usually means **"can't be understood quickly by code
readers."** It can also mean **"developers are likely to introduce bugs when
they try to call or modify this code."**
A particular type of complexity is **over-engineering**, where developers have
made the code more generic than it needs to be, or added functionality that
isn't presently needed by the system. Reviewers should be especially vigilant
about over-engineering. Encourage developers to solve the problem they know
needs to be solved *now*, not the problem that the developer speculates *might*
need to be solved in the future. The future problem should be solved once it
arrives and you can see its actual shape and requirements in the physical
universe.

### Tests

Ask for unit, integration, or end-to-end
tests as appropriate for the change. In general, tests should be added in the
same CL as the production code unless the CL is handling an
emergency.
Make sure that the tests in the CL are correct, sensible, and useful. Tests do
not test themselves, and we rarely write tests for our tests—a human must ensure
that tests are valid.
Will the tests actually fail when the code is broken? If the code changes
beneath them, will they start producing false positives? Does each test make
simple and useful assertions? Are the tests separated appropriately between
different test methods?
Remember that tests are also code that has to be maintained. Don't accept
complexity in tests just because they aren't part of the main binary.

### Naming

Did the developer pick good names for everything? A good name is long enough to
fully communicate what the item is or does, without being so long that it
becomes hard to read.

### Comments

Did the developer write clear comments in understandable English? Are all of the
comments actually necessary? Usually comments are useful when they **explain
why** some code exists, and should not be explaining *what* some code is doing.
If the code isn't clear enough to explain itself, then the code should be made
simpler. There are some exceptions (regular expressions and complex algorithms
often benefit greatly from comments that explain what they're doing, for
example) but mostly comments are for information that the code itself can't
possibly contain, like the reasoning behind a decision.
Note that comments are different from *documentation* of classes, modules, or
functions, which should instead express the purpose of a piece of code, how it
should be used, and how it behaves when used.

### Style

We have [style guides](http://google.github.io/styleguide/) at Google for all
of our major languages, and even for most of the minor languages. Make sure the
CL follows the appropriate style guides.
If you want to improve some style point that isn't in the style guide, prefix
your comment with "Nit:" to let the developer know that it's a nitpick that you
think would improve the code but isn't mandatory. Don't block CLs from being
submitted based only on personal style preferences.

### Consistency

What if the existing code is inconsistent with the style guide? Per our
code review principles, the style guide is the
absolute authority: if something is required by the style guide, the CL should
follow the guidelines.
In some cases, the style guide makes recommendations rather than declaring
requirements. In these cases, it's a judgment call whether the new code should
be consistent with the recommendations or the surrounding code. Bias towards
following the style guide unless the local inconsistency would be too confusing.
If no other rule applies, the author should maintain consistency with the
existing code.

### Documentation

If a CL changes how users build, test, interact with, or release code, check to
see that it also updates associated documentation, including
READMEs, g3doc pages, and any generated
reference docs. If the CL deletes or deprecates code, consider whether the
documentation should also be deleted.
If documentation is
missing, ask for it.

### Every Line

In the general case, look at *every* line of code that you have been assigned to
review. Some things like data files, generated code, or large data structures
you can scan over sometimes, but don't scan over a human-written class,
function, or block of code and assume that what's inside of it is okay.
Obviously some code deserves more careful scrutiny than other code&mdash;that's
a judgment call that you have to make&mdash;but you should at least be sure that
you *understand* what all the code is doing.
If it's too hard for you to read the code and this is slowing down the review,
then you should let the developer know that
and wait for them to clarify it before you try to review it. At Google, we hire
great software engineers, and you are one of them. If you can't understand the
code, it's very likely that other developers won't either. So you're also
helping future developers understand this code, when you ask the developer to
clarify it.
If you understand the code but you don't feel qualified to do some part of the
review, make sure there is a reviewer on the CL who is
qualified, particularly for complex issues such as privacy, security,
concurrency, accessibility, internationalization, etc.

### Context

It is often helpful to look at the CL in a broad context. Usually the code
review tool will only show you a few lines of code around the parts that are
being changed. Sometimes you have to look at the whole file to be sure that the
change actually makes sense. For example, you might see only four new lines
being added, but when you look at the whole file, you see those four lines are
in a 50-line method that now really needs to be broken up into smaller methods.
It's also useful to think about the CL in the context of the system as a whole.
Is this CL improving the code health of the system or is it making the whole
system more complex, less tested, etc.? **Don't accept CLs that degrade the code
health of the system.** Most systems become complex through many small changes
that add up, so it's important to prevent even small complexities in new
changes.

### Good Things

If you see something nice in the CL, tell the developer, especially when they
addressed one of your comments in a great way. Code reviews often just focus on
mistakes, but they should offer encouragement and appreciation for good
practices, as well. It’s sometimes even more valuable, in terms of mentoring, to
tell a developer what they did right than to tell them what they did wrong.


## Navigating a CL in review

### Summary

1.  Does the change make sense? Does it have a good
    description?
2.  Look at the most important part of the change first. Is it well-designed
    overall?
3.  Look at the rest of the CL in an appropriate sequence.

### Step One: Take a broad view of the change

Look at the CL description and what the CL
does in general. Does this change even make sense? If this change shouldn't have
happened in the first place, please respond immediately with an explanation of
why the change should not be happening. When you reject a change like this, it's
also a good idea to suggest to the developer what they should have done instead.

### Step Two: Examine the main parts of the CL

Find the file or files that are the "main" part of this CL. Often, there is one
file that has the largest number of logical changes, and it's the major piece of
the CL. Look at these major parts first. This helps give context to all of the
smaller parts of the CL, and generally accelerates doing the code review. If the
CL is too large for you to figure out which parts are the major parts, ask the
developer what you should look at first, or ask them to
split up the CL into multiple CLs.
If you see some major design problems with this part of the CL, you should send
those comments immediately, even if you don't have time to review the rest of
the CL right now. In fact, reviewing the rest of the CL might be a waste of
time, because if the design problems are significant enough, a lot of the other
code under review is going to disappear and not matter anyway.

### Step Three: Look through the rest of the CL in an appropriate sequence

Once you've confirmed there are no major design problems with the CL as a whole,
try to figure out a logical sequence to look through the files while also making
sure you don't miss reviewing any file. Usually after you've looked through the
major files, it's simplest to just go through each file in the order that
the code review tool presents them to you. Sometimes it's also helpful to read the tests
first before you read the main code, because then you have an idea of what the
change is supposed to be doing.


## How to write code review comments

### Courtesy

In general, it is important to be
[courteous and respectful](https://chromium.googlesource.com/chromium/src/+/master/docs/cr_respect.md)
while also being very clear and helpful to the developer whose code you are
reviewing. One way to do this is to be sure that you are always making comments
about the *code* and never making comments about the *developer*. You don't
always have to follow this practice, but you should definitely use it when
saying something that might otherwise be upsetting or contentious. For example:
Bad: "Why did **you** use threads here when there's obviously no benefit to be
gained from concurrency?"
Good: "The concurrency model here is adding complexity to the system without any
actual performance benefit that I can see. Because there's no performance
benefit, it's best for this code to be single-threaded instead of using multiple
threads."

### Explain Why

One thing you'll notice about the "good" example from above is that it helps the
developer understand *why* you are making your comment. You don't always need to
include this information in your review comments, but sometimes it's appropriate
to give a bit more explanation around your intent, the best practice you're
following, or how your suggestion improves code health.

### Giving Guidance

**In general it is the developer's responsibility to fix a CL, not the
reviewer's.** You are not required to do detailed design of a solution or write
code for the developer.
This doesn't mean the reviewer should be unhelpful, though. In general you
should strike an appropriate balance between pointing out problems and providing
direct guidance. Pointing out problems and letting the developer make a decision
often helps the developer learn, and makes it easier to do code reviews. It also
can result in a better solution, because the developer is closer to the code
than the reviewer is.

### Label comment severity

Consider labeling the severity of your comments, differentiating required
changes from guidelines or suggestions.
> Nit: This is a minor thing. Technically you should do it, but it won’t hugely
> impact things.
>
> Optional (or Consider): I think this may be a good idea, but it’s not strictly
> required.
>
> FYI: I don’t expect you to do this in this CL, but you may find this
> interesting to think about for the future.
This makes review intent explicit and helps authors prioritize the importance of
various comments. It also helps avoid misunderstandings; for example, without
comment labels, authors may interpret all comments as mandatory, even if some
comments are merely intended to be informational or optional.

### Accepting Explanations

If you ask a developer to explain a piece of code that you don't understand,
that should usually result in them **rewriting the code more clearly**.
Occasionally, adding a comment in the code is also an appropriate response, as
long as it's not just explaining overly complex code.
**Explanations written only in the code review tool are not helpful to future
code readers.** They are acceptable only in a few circumstances, such as when
you are reviewing an area you are not very familiar with and the developer
explains something that normal readers of the code would have already known.


## Speed of Code Reviews

### How Fast Should Code Reviews Be?

If you are not in the middle of a focused task, **you should do a code review
shortly after it comes in.**

### Speed vs. Interruption

There is one time where the consideration of personal velocity trumps team
velocity. **If you are in the middle of a focused task, such as writing code,
don't interrupt yourself to do a code review.**
Research has shown that it can
take a long time for a developer to get back into a smooth flow of development
after being interrupted. So interrupting yourself while coding is actually
*more* expensive to the team than making another developer wait a bit for a code
review.

### Fast Responses

When we talk about the speed of code reviews, it is the *response* time that we
are concerned with, as opposed to how long it takes a CL to get through the
whole review and be submitted. The whole process should also be fast, ideally,
but **it's even more important for the *individual responses* to come quickly
than it is for the whole process to happen rapidly.**
If you are too busy to do a full review on a CL when it comes in, you can still
send a quick response that lets the developer know when you will get to it,
suggest other reviewers who might be able to respond more quickly, or
provide some initial broad comments. (Note: none of this means
you should interrupt coding even to send a response like this&mdash;send the
response at a reasonable break point in your work.)

### LGTM With Comments

In order to speed up code reviews, there are certain situations in which a
reviewer should give LGTM/Approval even though they are also leaving unresolved
comments on the CL. This should be done when at least one of the following
applies:
*   The reviewer is confident that the developer will appropriately address all
    the reviewer's remaining comments.
*   The comments don't *have* to be addressed by the developer.
*   The suggestions are minor, e.g. sort imports, fix a nearby typo, apply a
    suggested fix, remove an unused dep, etc.

### Large CLs

If somebody sends you a code review that is so large you're not sure when you
will be able to have time to review it, your typical response should be to ask
the developer to
split the CL into several smaller CLs that build on
each other, instead of one huge CL that has to be reviewed all at once. This is
usually possible and very helpful to reviewers, even if it takes additional work
from the developer.


## Handling pushback in code reviews

### Who is right?

When a developer disagrees with your suggestion, first take a moment to consider
if they are correct. Often, they are closer to the code than you are, and so
they might really have a better insight about certain aspects of it. Does their
argument make sense? Does it make sense from a code health perspective? If so,
let them know that they are right and let the issue drop.
However, developers are not always right. In this case the reviewer should
further explain why they believe that their suggestion is correct. A good
explanation demonstrates both an understanding of the developer's reply, and
additional information about why the change is being requested.

### Cleaning It Up Later

A common source of push back is that developers (understandably) want to get
things done. They don't want to go through another round of review just to get
this CL in. So they say they will clean something up in a later CL, and thus you
should LGTM *this* CL now. Some developers are very good about this, and will
immediately write a follow-up CL that fixes the issue. However, experience shows
that as more time passes after a developer writes the original CL, the less
likely this clean up is to happen. In fact, usually unless the developer does
the clean up *immediately* after the present CL, it never happens. This isn't
because developers are irresponsible, but because they have a lot of work to do
and the cleanup gets lost or forgotten in the press of other work. Thus, it is
usually best to insist that the developer clean up their CL *now*, before the
code is in the codebase and "done." Letting people "clean things up later" is a
common way for codebases to degenerate.
If a CL introduces new complexity, it must be cleaned up before submission
unless it is an emergency. If the CL exposes surrounding
problems and they can't be addressed right now, the developer should file a bug
for the cleanup and assign it to themselves so that it doesn't get lost. They
can optionally also write a TODO comment in the code that references the filed
bug.
