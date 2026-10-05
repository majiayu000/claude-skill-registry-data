---
name: co-write-pr
description: Write a pull request description together with the contributor, by asking until both sides understand the change. Use before opening a pull request on any project, or when asked to write or revise a PR description.
---

# Co-writing a pull request description

A pull request arrives with a diff. Whatever the description adds has to be
the part the diff cannot carry. If what you have is a report rather than a
change, there is no diff to sit on, and that is co-write-issue instead.

Many projects ask contributors to write their own PR descriptions, and the
reason given is usually the same one: it is how the contributor ends up having
reviewed and understood their own work. That reason is the target. Writing it
by hand is one way to reach it.

This skill is another. It reaches the same place by making both sides
understand the change before either writes anything, and it fails closed: with
nothing to draw on, there is nothing to write.

Two directions, and both are needed.

- The contributor knows why the change exists: what prompted it, what was tried
  and rejected, what is still uncertain. None of that is in the diff.
- You know what the diff does, line by line. Some of it the contributor has not
  looked at closely, and that is exactly what review time gets spent on.

So ask in both directions, then write what came out of it.

## Ask about intent first

The motivation is the part no one can reconstruct later. Ask for it in whatever
language the contributor prefers; translating is your job, not theirs.

Useful questions:

- What made you start this? A bug you hit, a review comment, something that
  looked wrong while reading?
- What else did you try? What made you drop it?
- Which part are you least sure about?
- Does this change behaviour anyone outside this repository would notice?

Ask for the summary in their words before drafting. A sentence of theirs is
worth a paragraph of yours.

## Then make the diff mutually understood

Read the diff. Where it makes a decision that is not forced, name it and check
it against the contributor's intent.

- Prefer: "This makes the empty result a success rather than an error. Callers
  can no longer tell 'nothing there' from 'lookup failed'. Is that what you
  want?"
- Avoid: "I've reviewed the changes and they look good."

Name the specific decision. A question the contributor can answer without
opening the diff has not helped them review it.

Ask about anything you changed that they have not seen: a helper you added, a
default you picked, an error path you wrote. Those are the lines a maintainer
will ask about.

When the answer reveals the change is wrong, fix the change. Do not write it up.

## What belongs in the description

The test is whether a reader could get it from the diff.

Include, because the diff does not carry it:

- Why the change exists. The bug, the report, the observation that started it.
- Approaches considered and dropped, when the choice is not obvious.
- Impact on people outside this repository: behaviour changes, new
  requirements, anything that breaks.
- What was verified, and how. Name what actually ran: which platform, which
  version, which backend, which dataset, which hardware. Then name what was
  only reasoned about. Be explicit about whatever in this change is easy to get
  plausibly wrong and hard to catch by reading a diff; concurrency, lifetimes,
  timing, platform differences, and anything depending on a device or service
  you did not run all qualify.
- Open questions and known limits.

Leave out, because the diff carries it:

- A file-by-file walkthrough of the changes.
- Restating a function's body in prose.
- Line counts and file counts.
- Any summary of the code that a reader gets faster from the diff itself.

## Keep it short

Length is not thoroughness. Every sentence a reviewer reads without using is a
sentence that hid a sentence they needed.

Cut a sentence when it restates the diff, when it restates an earlier sentence,
or when no reviewer decision depends on it.

- Avoid: "This PR modifies `src/parser.cpp` and `src/parser.hpp`, adding a new
  method `parse_header()` which takes a `std::string_view` and returns an
  `std::optional<Header>`. The method validates the magic bytes and then reads
  the version field. Tests were added in `tests/parser_test.cpp` covering the
  valid case, the truncated case, and the wrong-magic case."
- Prefer: "Headers were parsed inline in three places and two of them skipped
  the magic-byte check. `parse_header()` is the shared one. Truncated input
  returns nothing rather than a zeroed header, which is what the wrong-magic
  case used to produce."

The second version is shorter and says more, because it says what the diff
cannot.

## Write in the contributor's voice

Use their words for the motivation. Keep their framing of the problem, even
where you would have framed it differently; their framing is what a maintainer
is replying to.

If they wrote the summary in another language, translate it rather than
replacing it. Keeping the original in a quote block alongside the English works
well.

## Check the project's rules before posting

Different projects want different things. Look, do not assume:

- An AI policy: AI_POLICY.md, or a section in CONTRIBUTING.md or the code of
  conduct. Follow it. If it says contributors should write in their own voice,
  that governs, and this skill's job is to get them to the point where they
  can.
- The pull request template. If it has an AI assistance section, fill it in.
  If it asks for a checklist, a linked issue, or a changelog entry, that is
  part of the description too.
- Whether a sign-off such as a DCO applies. It usually does for contributions,
  and it is the contributor's to give, not yours.
- The project's conventions for the title: a prefix, a component name, a
  conventional-commit type. Read recent merged PRs rather than guessing.

If the project has no policy, disclose anyway, in one line: which tools were
used, and what each side did. The direction and the decisions are the
contributor's; the drafting is yours.

Disclosure is not penalized.

Do not post long unedited model output into a thread. A few lines go in a quote
block, labelled, with a sentence of the contributor's own saying why they
matter. More than that goes in a gist with a summary.

## Before you post

- Every claim about what was verified is one you actually observed.
- Nothing in the description is contradicted by the diff.
- Every reproduction or verification step runs as written.
- The contributor can answer a maintainer's question about any part of it.

The last one is the real test. If they cannot, go back and ask.

Then stop and show them the draft. Posting is theirs to do, or theirs to tell
you to do. A pull request goes out under their name.

---

Adapted from the `co-write-pr` skill in maplibre/maplibre-native-slint, with
the project-specific parts generalized. Copyright (c) 2025 MapLibre
contributors, BSD 2-Clause. Sibling skill: co-write-issue.
