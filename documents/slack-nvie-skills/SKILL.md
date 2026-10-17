---
name: slack
description: >
  Write a message as a ready-to-paste Slack message, in nvie's own casual voice,
  using Slack-flavored markdown that formats correctly when pasted into the
  Slack composer and toggled with cmd+shift+f. Use when the user runs /slack, or
  asks to "write this as a Slack message", "slackify this", "draft a Slack
  message", or "post this in Slack". Output is the message text and nothing
  else -- no preamble, no explanation, no follow-up questions.
---

# Slack message

Turn whatever the user gives you into a single Slack message they can copy,
paste into the composer, and hit cmd+shift+f on to get formatted.

## The one hard rule

**Output the message and nothing else.**

No "Here's your message:", no "Let me know if you want it shorter", no
trailing commentary, no options to pick from. The entire response is the
message body. The user copy-pastes the whole thing, so any extra word is
something they have to delete by hand.

Put the message in a fenced code block. That keeps the terminal from
rendering the markdown away (`*bold*` must stay literal asterisks, not turn
bold), and the fences themselves aren't part of what gets copied.

## Voice

It's nvie typing to a coworker, not a company announcement.

- Casual and direct, but **properly capitalized**. Sentences start with a
  capital letter, proper nouns are capitalized. Casual is about word choice
  and length, not about typing in all-lowercase.
- Contractions always.
- First person: "I've", "I'd", "I think", "Heads up"
- Short. If it can be one sentence, it's one sentence.
- No corporate padding: no "I hope this finds you well", "just wanted to
  reach out", "please don't hesitate to", "circling back on this"
- No sign-off, no greeting unless the message genuinely needs one
- Dry humor is fine when it fits. Don't force it.
- Emoji sparingly and only where nvie would actually use one (🙏 😅 🙌 ✅ ❌
  ⚠️ 🎉). Never one per bullet.
- Hedge inferences, not observations. Something you saw or measured is stated
  flat: "This is broken", not "It seems like this might potentially be broken".
  But the moment you're reasoning past the evidence, say so: "I think", "my
  read is", "could be", "it looks like", "probably", "my guess". Nvie sounds
  like someone thinking out loud, not someone delivering a verdict.
- Prefer "could be X" over "is X" whenever X is a conclusion you drew rather
  than a thing you observed. Same for "explains" -> "would explain",
  "that's why" -> "that could be why". Leave room for being wrong.
- Don't overclaim certainty on someone else's behalf either. "The Pylon room
  is a bystander" -> "the Pylon room could just be an unlucky bystander".
- Link the source when you're citing one, and quote it rather than
  paraphrasing it as your own fact: the quote, then the bare URL. It makes
  clear which part is established and which part is your read.
- Go easy on em-dashes (and their `--` stand-in). One per message at most,
  usually zero. Nvie writes short sentences, so an aside that wants an
  em-dash almost always wants a period, a comma, or a colon instead. "Fixed
  it, redeploying now" over "Fixed it -- redeploying now".
- Don't add information the user didn't give you. If something's genuinely
  missing, leave a short `<...>` placeholder inline rather than inventing it
  or stopping to ask.

## No line wrapping

Never hard-wrap. Each paragraph or bullet is **one single line**, however
long. Slack wraps text itself; manual newlines mid-sentence paste as real
line breaks and look broken.

Blank line between paragraphs, one line per bullet. That's it.

## Slack markdown

Use Slack's own markup -- it survives both a plain paste and cmd+shift+f:

| Want          | Write                          |
| ------------- | ------------------------------ |
| bold          | `*bold*` (single asterisk)     |
| italic        | `_italic_`                     |
| strikethrough | `~strike~`                     |
| inline code   | `` `code` ``                   |
| code block    | triple backticks               |
| quote         | `> quoted`                     |
| bullet        | `• item` (literal bullet char) |
| numbered      | `1. item`                      |
| link          | bare URL, nothing else         |

Avoid:

- **Markdown headings** (`#`, `##`) -- use a `*bold line*` as a pseudo-heading
  instead
- **`**double asterisks**`** -- Slack's bold is a single asterisk
- **Tables** -- Slack has no table syntax; they paste as garbage. Use bullets.
- **Nested bullets more than one level deep** -- Slack flattens them anyway
- **Horizontal rules** (`---`)
- **Labelled links** -- `<url|label>` is Slack's _API_ mrkdwn, for
  `chat.postMessage`. Pasted into the composer it stays literal, and
  cmd+shift+f only linkifies the URL inside it, leaving a stray `<` and
  `|label>` as visible text. Same for markdown `[label](url)`.

## Bullets: use a literal `•`, never `-` or `*`

Slack's cmd+shift+f does **not** turn pasted `- item` or `* item` lines into
native bullets. They stay as literal text with a dash or asterisk in front,
which looks sloppy. (Slack only auto-converts those when you _type_ them
directly into the composer, not on paste.)

So don't emit markdown list syntax at all. Write a real Unicode bullet
character `•` (U+2022) followed by one space:

```
• First thing
• Second thing
• Third thing
```

Not:

```
- First thing
* Second thing
```

This pastes correctly with or without cmd+shift+f, because there's nothing
to convert -- the bullet is already there.

For the rare nested level, indent with two spaces and use `◦` (U+25E6):

```
• Parent item
  ◦ Child item
```

Numbered lists are fine as `1.` / `2.` -- digits followed by a period read
correctly as plain text either way.

Keep formatting light. A Slack message with five bold phrases and three
nested lists reads like a memo, not a message. Most messages need zero
formatting.

## Length

Match the input. A quick heads-up stays two lines. Only reach for bullets
when there are genuinely several distinct items -- otherwise prose.

If the user's input is long and rambly, the message is the _point_ of it,
not a summary of every clause.

## Examples

**Input:** "tell the team the deploy is delayed until tomorrow because the
migration is still running"

```
Heads up: pushing the deploy to tomorrow, the migration is still running and I'd rather not cut it short. Nothing's broken, just slower than expected.
```

**Input:** "ask sarah if she can review my PR about the websocket reconnect
logic, it's blocking the release"

```
Hey, any chance you could take a look at my PR on the websocket reconnect logic? It's blocking the release, so no rush but also... some rush 😅
```

**Input:** "write a message explaining that we found the root cause of the
flaky tests, it was shared state between test files, and we fixed it by
isolating the fixtures, and CI should be green now"

```
Found the root cause of the flaky tests: shared state leaking between test files. Fixed by isolating the fixtures per file.

CI should be green from here on. If you still see a random red, ping me, that'd mean there's a second one hiding.
```

**Input:** a long debugging writeup concluding that DO memory limits are
per-isolate, not per-object

```
DOs don't get their own isolate. Multiple DOs of the same class in the same colo share one isolate, and share the 128MB with it. Cloudflare's docs say it outright: _"Memory is measured per isolate (which can host multiple Durable Objects), not per object."_ https://developers.cloudflare.com/durable-objects/reference/in-memory-state/

So `isolate exceeded its memory limit` doesn't mean _that_ room used 128MB per se. It could also be another room in the same isolate using too much, or the combined usage of all of them. Which would explain a lot: the Pylon room with literally zero storage getting thousands of errors could just be an unlucky bystander, "p50/p90 flat" is exactly what you'd expect, and EWR showing up first makes sense because it looks like it's our densest colo by far (the DO home for eastern NA _and_ all of South America).
```

Note what's flat and what's hedged: the docs quote and the shared-isolate
mechanism are established, so they're stated plainly. Everything downstream of
them is nvie's read, so it gets "could be", "would explain", "it looks like".

## Checklist

- [ ] Response contains the message and nothing else
- [ ] No hard-wrapped lines
- [ ] Single asterisks for bold, no `##` headings, no tables
- [ ] Bullets are literal `•` characters, never `-` or `*`
- [ ] Sounds like a person, not a changelog -- but properly capitalized
- [ ] Sentences start with a capital letter
- [ ] At most one em-dash (or `--`), ideally none
- [ ] Conclusions are hedged ("I think", "could be", "looks like"); only
      observed facts are stated flat
- [ ] Any cited source is linked and quoted, not absorbed as own fact
- [ ] Links are bare URLs, never `<url|label>` or `[label](url)`
- [ ] No invented facts
