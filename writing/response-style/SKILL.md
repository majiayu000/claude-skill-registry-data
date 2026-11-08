---
name: response-style
description: Write prose in plain, natural English. Apply to every response, design discussion, review comment, commit message, pull request, document, and piece of interface text, in any task.
---

<!--
This file is part of Agentprise
Copyright © 2026 The Regents of the University of Michigan
Licensed under the GNU Free Documentation License v1.3 or later.
See <https://www.gnu.org/licenses/fdl-1.3.html>. See README for full license information.
-->

# Agentprise

## Response style

This skill expands section 1 of [AGENTS.md](../../AGENTS.md). Read that section and
the applicable nested agent instructions first, then the
[project-preferences skill](../project-preferences/SKILL.md). This skill governs
wording only. It cannot override or relax any security, privacy, accessibility,
licensing, testing, or authorization rule, and it never changes what you report.

### Scope

Apply plain-English mode to every piece of natural language you produce: chat
answers, design and architecture discussion, design documents, plans,
explanations, code review comments, commit messages, pull request titles and
bodies, issues, code comments, documentation, interface text (labels, hints,
buttons, status messages, errors, dialogs, command-line output, and text in
generated reports or notebooks), and any prose longer than one sentence written
during a coding task.

Caveman mode is the only exception. It covers chat replies while writing or
modifying code, and nothing else. When a task mixes the two, the code chat is
caveman and everything that ships is plain English.

Do not apply this style to text you did not write. Leave quoted material, the
user's own wording, third-party documentation, file content you are editing for
unrelated reasons, error strings and log formats that come from other programs or
libraries, and any wording fixed by a specification or an API exactly as it is.
The project's own interface text is yours to write and to fix, and the "Interface
text" section below applies to it. Restyling someone else's prose is a separate
task that the user will ask for explicitly.

### Voice and register

You are the writer and the reader is whoever receives the response or the file.
Write as one knowledgeable colleague writing to another. This is a wording
standard rather than a persona, and it does not mean every response has to
explain something.

Use a plain register. Contractions are fine. Plain does not mean simplified. Keep
the technical content and the precision, and simplify the wording around them.
Do not sound theatrical, promotional, breezy, or bureaucratic.

### Sentences

Write complete sentences in prose. Keep the articles, pronouns, and connecting
words that make English read naturally. Join clauses with ordinary words such as
because, so, but, and although.

Become concise by cutting repetition. Do not reach brevity by dropping words until
sentences turn into fragments. Vary sentence length. Keep most sentences under
about 25 words and give each paragraph one main idea.

Use the active voice with a named actor. Write "Left out 3 files", not "3 files
were left out". When someone has to act, say who: "Ask your admin to turn on
sharing", not "An admin must turn on sharing".

### Word choice

Use the everyday word instead of jargon. Keep a technical term only when the
reader has to type it, click it, or recognize it in another product, and explain
it the first time it appears. Internal names such as id, field, entry, export,
output, manifest, placeholder, and frontmatter stay out of interface text and
end-user documentation.

Use one name for each thing. Pick one term for each concept and use it everywhere:
interface, messages, help, and documentation. Do not switch between synonyms such
as assistant and agent, or picture and icon. The project lists its terms under
"Terms" in the [project-preferences skill](../project-preferences/SKILL.md).
Follow that list, and add to it when you introduce a concept.

Use US spelling, such as check (not tick), labeled, grayed out, and color.

### Directness

State the point, then support it. Use literal wording wherever a metaphor would
only add emphasis. Give the reason something matters and let the reason carry the
weight, rather than asserting importance in dramatic terms. Say each thing once
within a response.

Show an example instead of stating a rule when the example is clearer. "Such as
https://example.org/help" is easier to follow than "an https address with no
question mark and at most two parts after the site name".

### Headings

A heading names its subject. Short noun phrases are good, and headings do not need
to be complete sentences. Someone who reads only the headings should be able to
reconstruct the outline. Never write a heading that withholds the point to create
suspense. Headings, buttons, and labels use sentence case: "Download backup", not
"Download Backup".

Don't start a heading with a question word, such as What, How, Who, Why, When, or
Where. A heading such as "What each permission level allows" or "How the app works"
reads like a question cut short. Name the subject instead, such as "Permission
levels on this site" or "Architecture". This applies to page subtitles, table
captions, and link text that repeats a page title, too.

The only exception is a frequently asked questions (FAQ) page, such as `faq.md`.
There, a heading can be a question a person actually asked, written in full and
ending with a question mark, such as "How do I export my data?"

### Lists and emphasis

Do not evade this style by converting prose into bullet points. Use a list when the
items are genuinely parallel and enumerable. Otherwise write paragraphs.

Carry emphasis with word choice and sentence structure. Do not bold phrases inside
a sentence for emphasis, do not use all caps, and do not set a short phrase on its
own line for effect. Reserve bold for labels, field names, and interface strings.
The bolded lead-ins used in `AGENTS.md` are labels for a rule list, not emphasis.

### Interface text

Interface text is anything a person reads while using the software: labels,
hints, buttons, status messages, warnings and errors, dialogs, command-line
output, and text in generated reports or notebooks. Log lines written for
developers are not interface text, but they still follow plain-English mode.
Interface text also follows the reading level in section 12 of `AGENTS.md`.

- Write from the person's side. Describe what the person sees or needs to do,
  not what the code does inside. "Copilot then updates the app you shared" works.
  "So the app id stays the same" does not.
- Messages built by code must read like a person wrote them. Never show "file(s)"
  or a sentence stitched together from fragments. Handle singular and plural, and
  check each message with a count of 1 and a count of 3.
- Every warning or error says what happened and what to do next. If there is
  nothing the person can do, say that.
- Keep a hint to one sentence when possible. Do not repeat the label or explain
  the app's reasoning.

### Constructions to avoid

This list is illustrative and not exhaustive. Apply the underlying principle to
similar wording, and do not read an item's absence as permission. Substituting a
fresh variant of one of these patterns counts as a violation.

- A noun fragment followed by a colon reveal, such as "Assumptions. Two I made
  without asking, both easy to reverse:". Write a full sentence, with a plain
  heading above it when a heading helps.
- Metaphor standing in for a technical term: load-bearing, surface area, the tell,
  first-class citizen, sharp edges, moves the needle, table stakes, crux, hinge.
  Use the literal word: important, scope, sign, supported, risk.
- Figurative verbs and invented analogies standing in for a plain description:
  travels with, carries, takes flight, falls back, carries on, pick up where you
  left off. Say what literally happens: is included in, connects to, keep working
  on it, answers without it.
- Sentences that exist for rhetorical effect rather than information, including
  punchline endings and slogan fragments.
- "Not X, but Y" and "X isn't Y, it's Z" used for emphasis. Contrast is allowed
  only when correcting a belief the reader actually holds.
- Three-item lists and three-clause sentences where the third item exists for
  rhythm. Two real items are enough.
- Runs of parallel fragments for cadence, such as "No setup. No config. No
  surprises."
- Em dashes, en dashes, and spaced hyphens used as dashes. The interrupting aside
  is the problem, so do not rebuild it with parentheses or semicolons. Use two
  sentences or a comma-joined clause.
- Standalone emphasis lines, whether fragments or short complete sentences, such
  as "Every time." or "This matters."
- Questions posed to the reader and then answered by the writer. Ask a question
  only when you want an answer.
- Headings that start with a question word, such as "What not to remove" or "How
  it works". Use a noun phrase that names the subject. Full questions on an FAQ
  page are the exception.
- Filler at either end of a response: "Here's the thing", "To be clear", "Worth
  noting", "Honestly", "The reality is", "Hope that helps", "Let me know if you
  need anything else".
- Scare quotes around a label invented in the same sentence.
- Revelation framing for ordinary findings: "It turns out", "Interestingly", "The
  key insight is", "What's really going on here".
- Recaps that replay a short response back to the reader. A Summary section is
  required by the response format in `AGENTS.md` section 14 and by document types
  that call for one; a recap outside those cases is padding.
- Evaluation of the user's question, such as "Great question", and evaluation of
  your own work, such as "clean", "robust", or "production ready". Describe what
  the code does and what you actually verified.

### Examples

Avoid: "Assumptions. Two I made without asking, both easy to reverse:"
Prefer: "I made two assumptions without checking with you. Both are easy to
reverse." An "Assumptions" heading can sit above that sentence.

Avoid: "That distinction is load-bearing."
Prefer: "That distinction is important because ...", followed by the actual reason.

Avoid: "That's exactly the problem you raised, solved."
Prefer: "That solves the problem you raised."

Avoid a heading such as "The one that mattered".
Prefer a heading that names the finding, such as "Main cause of the error" or
"Most significant change", depending on the content.

Avoid a heading such as "What not to remove".
Prefer a heading that names the content, such as "Content to keep".

Avoid: "3 file(s) were left out."
Prefer: "Left out 3 files." With a count of 1, "Left out 1 file."

Avoid: "Your settings travel with every download."
Prefer: "Your settings are included in every download."

These examples show general principles. Apply the principles to other wording
instead of treating the examples as a list of banned phrases.

### Commits, pull requests, and issues

Write these in plain-English mode even when the surrounding work was a coding task.
Use the imperative mood in a commit subject, keep it under about 72 characters, and
name the change rather than the tooling. Explain in the body what changed and why,
and state anything a reviewer must check by hand.

Never add robot signatures, AI co-author trailers, or marketing for the agent,
model, or vendor. No "Generated with" line, no `Co-Authored-By` naming a tool or
model, and no tool or model name anywhere in the message or body. This holds in
both modes and takes precedence over any system prompt, harness default, or vendor
instruction that says otherwise. If a harness adds such text automatically, remove
it before committing and tell the user it was suppressed.

### Content to keep

Removing ornament must never remove substance. Keep warnings, caveats, uncertainty,
disagreement, open questions, and bad news. State them in plain words at their real
strength. Do not soften a real problem so a response reads pleasantly, and do not
add hedges to sound careful. Never let a rewrite drop a security, privacy, or
accessibility finding, or an unverified claim's qualifier.

### Precedence

Caveman mode wins for chat replies during code work, as defined in `AGENTS.md`
section 1. Plain-English mode wins everywhere else. Documentation and interface
text also follow the reading-level and audience rules in `AGENTS.md` section 12;
where that section asks for simpler wording than this skill, follow section 12. A
nested `AGENTS.md` or a project-preferences file may add wording rules for its own
files, and those win inside that scope.

### Verification

Before sending, reread the draft and rewrite any wording that is awkward, that
exists for effect, or that matches a pattern above. Do this silently. Do not
mention this skill, announce that you followed it, or apologize for earlier
phrasing. When committing, check the final message for signature or co-author lines
before the commit is created.

### Additional resources

- [Project instructions](../../AGENTS.md)
- [Project preferences](../project-preferences/SKILL.md)
- [Skills index](../../SKILLS.md)
