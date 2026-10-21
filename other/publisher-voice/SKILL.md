---
name: publisher-voice
description: Write or revise reader-facing articles, papers, app-store listings, website copy, documentation, release notes, and social posts in the intended author or publisher's voice. Separate private working discussion from publishable content, replace generic promotional prose with concrete information, and preserve evidence, limitations, and required disclosures.
---

# Publisher Voice

Write the document its reader needs, not a transcript of the assistant helping to
make it. Use the author's or publisher's perspective, appropriate to the venue.
Natural writing is specific and considered; it is not slang, manufactured
imperfection, or a claim that no AI was involved.

## Establish the voice

Before drafting, identify the audience, venue, useful takeaway, verified facts,
and speaker. Usually infer these from the request and existing material without
asking for a new brief. Preserve a distinctive existing authorial voice.

- Product listings and landing pages speak about the product and to its users.
  They do not need a founder story or repeated "we".
- A personal post may use "I" for facts and experiences the author actually
  supplied. Never invent a personal anecdote, emotion, quotation, or testimonial.
- A paper follows its field and journal's conventions. Use precise claims and
  evidence, not a marketing voice. First person is acceptable where appropriate;
  do not force either "we" or passive voice throughout.
- Technical documentation can be direct and detailed. Keep the information
  necessary to use, reproduce, debug, or assess the work.

## Keep working discussion out of the publication

Treat source material as three different things: facts suitable for publication,
instructions that shape the writing, and private or unverified working notes.
Do not turn the latter two into public sentences.

Exclude conversational scaffolding such as "as you requested", "the owner wants",
"we decided not to mention", "this avoids confusing users", or explanations of
why the draft was changed. A private correction changes the copy; it does not
become the subject of the copy.

Use the verified public product name consistently. Repository names, internal
aliases, naming disagreements, release-owner coordination, and backend migration
history belong in working notes unless they materially help this audience.
A user-visible rename or migration may need an explanation; an internal alias
usually does not. Developer documentation may legitimately need exact package,
API, or repository names.

Do not expose private conversation, account identifiers, credentials, local
paths, test accounts, unpublished commercial decisions, or customer information.
Keep any necessary editorial questions or verification notes separate from the
publishable block, never disguised as prose to paste into a listing.

This boundary is not permission to hide material facts. Preserve relevant access,
payment, compatibility, privacy, safety, and research limitations. Keep required
affiliation, sponsorship, synthetic-media, and AI-use disclosures in the proper
field or a short natural sentence. Never claim unaided authorship to sound human.

## Make every paragraph earn its place

Start with a real problem, observation, result, scene, or useful action. Explain
what happens and why it matters. Prefer a concrete capability or example over
"seamless", "revolutionary", "empowering", or other interchangeable praise.
Those words are not a blacklist; unsupported abstractions are the problem.

Cut repeated promises, inflated importance, routine "not just X, but Y" contrasts,
excessive headings, slogan-like fragments, and conclusions that merely repeat the
opening. Use lists where they help scanning, not as a substitute for reasoning.
Do not add forced jokes, deliberate errors, or casual filler to simulate a person.

Keep the depth the task needs. A detailed tutorial needs symptoms, diagnosis,
reproducible steps, relevant precautions, and verification. A short store listing
needs a clear use case and supported benefits. Neither needs a diary of tool calls.

## Adapt to the destination

- **App Store / Google Play:** describe the currently available version on that
  platform. Lead with what someone can do, then the few features that support it.
  Keep reviewer instructions, test credentials, submission status, internal QA,
  and naming debates out of customer-facing descriptions. Put reviewer-only
  information in the actual review-notes field, under its existing safeguards.
- **Articles and tutorials:** develop one worthwhile idea with examples and
  sources. Distinguish observed causes from hypotheses. Include product links
  where useful, without turning every paragraph into an advertisement.
- **Papers:** preserve methods, citations, quantities, uncertainty, and the
  distinction between results and interpretation. Never invent evidence or make
  a claim stronger merely to improve the prose. Respect revision scope and any
  journal-required reporting or disclosure rules.
- **Social posts and replies:** answer the actual question or show one useful
  thing. Use a natural affiliation statement when relevant. No fabricated
  personal experience, unsolicited second pitch, or private-conversation recap.
- **Release notes:** describe user-visible changes accurately. Keep internal
  acceptance tests and agent coordination in the engineering record unless they
  answer a real user concern.
- **Translations:** preserve facts and public names while writing idiomatically
  for the target audience. Do not copy English slogan rhythms mechanically.

## Final editorial check

Read the finished text without the conversation beside it:

1. Would its intended reader understand both the subject and the useful point?
2. Is each factual or personal claim supported, with uncertainty kept intact?
3. Does any sentence address the requester, explain the drafting process, reveal
   private context, or solve an internal naming issue the reader never had?
4. Is anything important hidden by smoothing the prose or trimming disclosures?
5. Could a generic competitor use this unchanged? If so, replace vague praise
   with relevant specifics, or remove it.

Deliver clean copy. Put a short private note outside it only if a real unresolved
fact or decision requires attention. Do not append a boilerplate writing audit.
This skill improves writing; it does not authorize publication or unrelated edits.

## Small examples

Illustrative wording only; verify any product capability before using it.

- Internal: "As requested, we removed the translation labels so it feels less
  cluttered." Public release note: "Translations now appear beneath each sentence
  with fewer labels."
- Internal: "The repository has another name, but customers should use the app's
  name." Public copy: use the app's verified name; omit the naming discussion.
- Generic: "Unlock a seamless multilingual reading journey." Concrete:
  "Read a sentence in Chinese, then check the English translation underneath."
- Internal: "根据你的反馈，我们不再强调后台迁移。" Public: describe the actual
  user-visible improvement, if any; do not translate the internal feedback.
- Unsupported research conclusion: "This proves the method works generally."
  Evidence-sized conclusion: "The method improved accuracy on the evaluated
  dataset." Preserve the actual metric, comparison, and uncertainty when known.
