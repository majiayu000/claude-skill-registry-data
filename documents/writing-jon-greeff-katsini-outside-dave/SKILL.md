---
name: writing
description: "Use whenever writing any non-code prose: documentation, README or wiki pages, code comments, docstrings, descriptions, commit messages, PR descriptions, error messages, or config text. Trigger on any task that produces words a human will read, even when the user never asks for writing help. Carries the voice, grammar, and anti-AI-tell rules, rules for code-adjacent writing, and a subagent review pass that checks the draft against them and cuts what it doesn't need."
---

# Writing

Everything here applies to prose a human will read. Write it, then read it back once as the
recipient. If a sentence sounds like a template, a bot, or a corporate memo, rewrite it.

## The voice in one line

Professional and direct. Say the thing, explain it well when it's genuinely complex, and stop.
Sound like a sharp colleague writing to another human, not a press release.

## Core rules

**Get to the point.** Lead with the conclusion, the ask, or the decision. Supporting detail goes
after it. The reader should know why they're reading by the end of the first line.

**Write in short paragraphs.** Two to four sentences each, one idea per paragraph. Reach for
bullets only when you have a genuine list or a sequence of steps. Over-bulleting reads as choppy
and evasive.

**Prefer prose and bullets over tables.** A table fragments the writing and forces clipped phrasing
into the cells. Use one only when the data is genuinely two-dimensional and the reader needs to
compare across rows and columns, like a compatibility matrix.

**Match depth to the topic and the audience.** Simple things get one clean line. Complex or
unfamiliar things get the reasoning walked through. Judge who's reading before deciding how much
to say.

**Keep sentences short.** Aim under about 25 words. If a sentence needs two commas to survive,
split it.

**Prefer active voice.** "We shipped the fix" beats "the fix was shipped".

**Use plain words.** *use* not *utilise*, *help* not *facilitate*, *about* not *regarding*, *start*
not *commence*, *enough* not *sufficient*. Clarity is the whole job.

**Define acronyms on first use.** Spell it out once, "single sign-on (SSO)", then abbreviate.

## Grammar and spelling

- **British.** *organise*, *colour*, *centre*, *licence* (noun), *analyse*,
  *behaviour*. Not American spelling.
- **Oxford comma.** "design, build, and ship", not "design, build and ship".
- **Contractions are fine.** *don't*, *we'll*, *it's*. Dial them back only in a genuinely formal
  document such as a policy or legal notice.
- **No em-dashes.** Never use "—". Restructure with a comma, parentheses, a colon, or two sentences.

## Flourishes: sparing

- **Emoji:** never in documents, PRs, commits, or code comments.
- **Exclamation marks:** rare. Never stack them.
- **No hype.** Skip *amazing*, *awesome*, *game-changing*, *super excited*. Let the substance be
  the enthusiasm.

## Per artefact

**Documentation (README, wiki, docs/).** Use headings, lead each section with its point, and write
for a reader with no context. State each fact once, where a reader would look for it, and link
rather than duplicate. Write what stays true: rules and instructions survive, while counts and
file-by-file catalogues of today's code are wrong by the next commit.

**Code comments.** State only what the code can't show: a constraint, a non-obvious reason, a
warning. Never narrate the next line or address the reviewer ("fixed the bug here"). Match the
surrounding code's comment density and idiom.

**Docstrings and descriptions.** One active-voice sentence saying what the thing does: "Validates
the voucher", not "This function is responsible for...". Add parameters, return value, and errors
only where the signature doesn't make them obvious.

**Error messages and UI text.** Say what went wrong in the user's terms and what to do next:
"Voucher expired on 12 March. Request a new one from the account page", not "An unexpected error
has occurred".

**Commit messages and PR descriptions.** Factual and scannable. Say what changed and why. No
filler, no hype. Follow the repo's existing format if there is one.

## Code review comments

Review is the hardest audience, because you usually don't know who's reading. The author might be
the person who built the system, or someone three weeks into their first job. **When you can't
tell, write for the junior.** Layering makes this safe: put the point in the first line so a senior
can stop there, and keep the explanation below it.

The trap that loses a junior isn't long words, it's **assumed context**. A comment leaning on an
internal subsystem name, a nickname like "the wave", or a flag like `--max-turns` reads as obvious
to whoever built the thing and means nothing to a newcomer.

### The shape

1. **The point, in one line.** What's wrong or what should change, said plainly.
2. **Why it matters.** What actually happens, and what it costs. This is the teaching part.
3. **The fix.** Something concrete. Use a GitHub suggestion block when it's small enough to apply
   in one click.
4. **The wider lesson, when there is one.** Skip it when the fix is obvious or the point doesn't
   generalise.

Steps 1 and 3 keep it useful for the senior. Steps 2 and 4 are what make it teach.

### How to teach in a review

**Explain the mechanism, not the verdict.** "This is an N+1 query" only teaches people who already
know what an N+1 is. Say what the code does: it runs one query per row in the loop, so a hundred
rows means a hundred round trips. Then name it, because the name is what they'll search for.

**Name the pattern and explain it.** Don't drop *memoisation* or *idempotent* and move on. One
clause of plain English is enough: "this is a race condition, meaning two requests can read the
same value before either writes back, so one update gets lost".

**Gloss internal shorthand before you use it.** Tool names, subsystem nicknames, CLI flags, and
house idioms all need half a sentence the first time they appear. If a comment only makes sense to
someone already inside the system, it can't teach anyone who isn't.

**Teach the principle, not just the instance.** "Same applies anywhere we build SQL from user
input" is worth the extra sentence.

**Say how much it matters.** Label it: *blocking*, *suggestion*, *nit*, or *question*. A junior
can't always tell a blocker from a preference by tone alone.

**Ask real questions.** "What happens if `items` is empty here?" invites an answer. Don't use a
fake question to deliver a verdict you've already reached.

**Comment on the code, not the person.** "This re-fetches on every render", not "you forgot to
memoise this".

**Say when something is good.** One line is worth writing, and it tells them what to do more of.

**Don't teach what needs no teaching.** A typo is a typo. Over-explaining a trivial fix is its own
kind of condescension.

### Example

Weak, too terse for anyone who doesn't already know, and mildly accusatory:

> You've got an N+1 here. Fix the query.

Weak in the other direction, buries the ask and lectures:

> Great work on this PR overall! I wanted to take a moment to talk about database access patterns,
> which are really important for performance at scale. As you may know, when we access a database
> we open a connection and...

Fixed:

> **Suggestion:** fetch the orders in one query before the loop.
>
> As written, `getOrder` runs inside the loop, so it's one database round trip per user. With 500
> users on the dashboard that's 500 queries, and the page will slow down as the table grows. This
> is the "N+1 query" pattern (one query, plus N more for each result), which is worth knowing about
> because it looks fine in testing with 10 rows and falls over in production.
>
> ```suggestion
> const orders = await getOrdersByUserIds(users.map(u => u.id));
> ```
>
> Then look each one up from `orders` inside the loop. Same rule applies anywhere we're querying
> inside a loop, so it's a useful shape to spot.

The first line is the whole comment for a senior. Everything after it costs them one second to skip.

## Things to avoid

**AI-tell phrases.** Cut on sight: *delve*, *in today's fast-paced world*, *it's worth noting*,
*furthermore*, *moreover*, *unlock*, *leverage* (as a verb), *robust*, *seamless*, *elevate*,
*at the end of the day*, *it's important to note*, *when it comes to*, *dive into*, *in summary*,
*in conclusion*, *rest assured*, *needless to say*, *a testament to*, *the realm of*, *ever-evolving*,
*cutting-edge*, *state-of-the-art*, *top-notch*, *supercharge*, *plays a crucial role*, *boasts*.

**AI sentence shapes.** The sneakier tells are structural, and they survive a word-swap:

- **The "not just X, it's Y" reversal.** Also "It's not about X. It's about Y." Say the thing once.
- **The rule of three.** "clear, concise, and compelling". One accurate word beats three padded ones.
- **"Not only... but also" and "both X and Y."** Scaffolding that adds words, not meaning.
- **"Whether you're X or Y..."** The blog-intro opener. Drop it and say what the thing does.
- **The summary that restates.** If the point landed, don't echo it. If it didn't, fix the body.
- **Sycophantic openers.** "Great question!", "You're absolutely right!" Skip the warm-up.
- **Rhetorical-question headings.** A heading names its content, it doesn't tease it.
- **Puffery adverbs.** *seamlessly*, *effortlessly*, *simply*, *easily*. They claim ease instead of
  showing it.
- **Hollow hedges dressed as help.** Say "This caches the result", not "This can help improve
  performance".
- **Title Case Headings.** Headings are sentence case.

**Corporate jargon.** *synergy*, *circle back*, *touch base*, *move the needle*, *low-hanging
fruit*, *action item*, *bandwidth* (for time), *reach out*, *going forward*, *deep dive*.

**Filler and hedging.** *just*, *basically*, *actually*, *sort of*, *I think maybe*, *in order to*
(use "to"), *very*, *really*, *quite*. Cut throat-clearing openers like "So," and "Well,".

**Clichés and boilerplate.** If a phrase writes itself, it's probably a cliché. The test: would a
thoughtful person say this out loud to a colleague?

## Examples

**Documentation sentence for a mixed audience**
Weak: "We leverage a robust caching layer to seamlessly elevate performance across the platform."
Fixed: "We added a caching layer to cut repeated database reads. When a page is requested twice,
the second request is served from memory instead of hitting the database, which is noticeably
faster."

**PR description**
Weak: "This PR delves into fixing some issues and furthermore improves the overall robustness of
the system."
Fixed: "Fixes the race condition in the session store that logged users out at random. Adds a lock
around the write and a test that reproduces the old behaviour."

**Code review comment**
Weak: "It's worth noting that maybe this could potentially be a bit of a performance concern going
forward."
Fixed: "**Blocking:** this needs to handle a rejected promise. If `fetchUser` throws, nothing
catches it, so the request hangs until it times out rather than returning a 500. Wrapping the await
in a try/catch and returning the error is enough. Worth doing on every `await` that talks to the
network, since any of them can fail."

**Structural AI tell, where every word is fine but the shape isn't**
Weak: "This release isn't just a performance update, it's a fundamental rethink of how we handle
data. Whether you're a power user or just getting started, it's fast, reliable, and built to scale."
Fixed: "This release rewrites the data layer. Queries that took two seconds now take under 200ms,
and the new caching holds up under load we couldn't handle before."

## Final check

Reread the draft once as the recipient:

1. Is the main point in the first line or two?
2. Would a real person say this out loud, or does it sound like a template?
3. Any AI-tells left, the words (*delve*, *robust*, jargon, filler, em-dashes) and the shapes
   ("not just X, it's Y", rule-of-three triads, restated summaries, puffery adverbs)?
4. British/SA spelling, Oxford commas, sentences short enough to scan?
5. For a code review comment: is the ask in the first line, is the severity clear, and is every CS
   term and bit of internal shorthand glossed the first time it appears?
6. Does every comment, docstring, and error message earn its place, or is it narrating the obvious?

Fix what fails, then hand the draft to the review pass.

## The review pass

Self-checking is unreliable, because you remember what you meant and read it back into the words. A
subagent has none of that context, so it can only judge what is on the page, which is the reader's
position exactly. Once the draft passes the final check, hand it to one.

Run it on Haiku: pass `model: "haiku"` to the Agent tool. The reviewer checks a draft against a
written rule set rather than reasoning about a codebase, so a cheap model does it well, and the cost
is what makes it affordable to run the pass again after every revision.

Give the subagent the draft, the path to this skill file, and the brief the prose has to satisfy.
Ask for three things:

1. **Rule breaches.** Every place the draft breaks a rule here: the AI-tell words and shapes,
   em-dashes, American spelling, missing Oxford commas, Title Case headings, hype, over-bulleting, a
   table where prose would do, and the per-artefact rules for whatever this is.
2. **Over-writing.** Sentences that restate the one before, explanation this audience doesn't need,
   hedges and qualifiers carrying no meaning, and depth beyond what the topic warrants.
3. **What to cut.** The specific lines and paragraphs to delete or compress, each with the shorter
   version written out and a note on what the reader loses. A cut that takes a fact the reader needs
   is a bad cut, and the reviewer should say so rather than propose it.

Every finding quotes the text it is about and names the rule it breaks or the line it duplicates.
"Feels wordy" is not a finding.

The reviewer reports; it does not rewrite. Resolve each finding yourself, then send the revised
draft to a fresh subagent on the same model, which judges the new draft rather than defending its
own suggestions. Repeat until it comes back clean.

Skip the pass on prose too short to hide a problem: a commit message, a one-line docstring, a single
error string. A README section, a doc page, a PR description, or a review comment that teaches all
go through it.
