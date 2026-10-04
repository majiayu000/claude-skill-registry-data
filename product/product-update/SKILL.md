---
name: product-update
description: >
  Drafts a Teams product update announcing a shipped feature to the whole
  business, and gathers the before/after screenshots that go with it. Use when
  asked to write a product update, announce or write up a feature that has
  shipped or merged, tell the business about a release, or collect before/after
  media for one. Calls `write-in-my-voice` for the prose and `humanizer` to
  strip AI tells.
---

# Product update

A message pasted into Teams, read by sales, support, ops and engineering. Not a
doc, not a changelog, not a PR description.

## Gather the facts first

The commit bodies are the richest source, better than the PR description. Then
`gh pr view --json body,reviews,comments`, `storefrontFeatureRegistry.ts` for
the test key, and demo-site's `humanizeFeatureName` for the label the feature
carries in the config UI.

None of that carries the *why now*. Ask the user, in one question, before
drafting:

- what the surface was like before this, and why it was like that
- what earlier attempt this replaces, if any, and what went wrong with it
- what the pass was actually for

A draft that explains the mechanism accurately and skips this reads as a
changelog. Answer it first, then write.

## Get the destination right

**It is a chat message.** Plain text, pasted straight in, with images attached
underneath. Publishing an artifact or an HTML page instead is the single most
common way to get this wrong: nobody attaches a document to a Teams post.

**Length is the middle setting.** A three-line summary is too thin, a full
write-up is too much. Aim for a title, a short "what was wrong", a bulleted
"what's changed", the experiment, and how to try it. Professionally
copywritten, digestible by the whole business, still in Isaac's voice.

Write the prose with `write-in-my-voice`, then pass it through `humanizer`.

## The shape

A full annotated example, and why each part earns its place: see [EXAMPLE.md](EXAMPLE.md).

```
[Product Update] <Feature area>

<One line: what is live, and where>

<Two or three sentences: what was wrong before, and what this pass was for.
Say it plainly — "it worked, it just didn't feel great to use".>

What's changed:
<bullets — one per user-visible change, concrete, in the user's terms>

<The experiment: what is being tested, the test name, any caveat.>

<How to try it themselves.>

<Credit by name.>

<screenshots attached in order>
```

## Rules that come from being read by non-engineers

- **Name the product, not the ticket.** "Storefront v3", not "the storefront
  shell (HOL-616)". Drop branch names, commit SHAs and package paths entirely.
- **One clause on the mechanism, at most.** How it was built is the least
  interesting thing in the room. "The panel picks up the colour of the photo
  above it" is the whole explanation; blur radii and seam handling are not.
- **Describe behaviour, not implementation.** "A proper range calendar" beats
  "a `DateRangePicker` bound to the URL state". Mention internals only where
  they explain reach: "that's new all the way through the API".
- **Always name the A/B test key** if there is one — `productDiscoveryInput_20260824`.
  Someone will need to find it in the dashboard. Include the arms if they are
  not obvious.
- **Say how to self-serve.** The demo site, and the feature's name in the
  config UI, so people can look without asking. Better than offering to send a
  link.
- **Own the trade-offs out loud.** Restarting an experiment throws away the old
  data; say so, say why it was right, and address the person it costs by name
  ("sorry Helio"). Owning it lands better than burying it.
- **Credit people by name**, when there is someone to credit. Check the PR
  reviews and the ticket comments first. If both are empty, ask once, and take
  "no credit line" for an answer rather than inventing a plausible name.
- **One personal opinion is welcome.** "Very happy with how mobile feels" reads
  as a human wrote it. Don't stack several.

## Screenshots

Pairs, before first. See [MEDIA.md](MEDIA.md) for capture technique — matched
viewports, forcing each arm, catching a loading skeleton.

- Number filenames in paste order (`3-before-dates-popover.png`), so a
  drag-and-drop or a multi-file paste lands in the right sequence
- Label every frame on brand before handing them over, don't wait to be asked.
  Recipe in [MEDIA.md](MEDIA.md)
- Cover the headline change first, then each sub-change, then mobile
- Offer which ones are skippable if the set runs long — nine is a lot
- Say "before on the left" in the message

## Before sending

- [ ] Would someone in sales understand every line?
- [ ] Ticket IDs, branch names and file paths all gone?
- [ ] A/B test key present?
- [ ] Someone credited, or asked about and declined?
- [ ] Screenshots labelled, text on the clipboard, folder open?
- [ ] Images numbered in paste order, before first?
