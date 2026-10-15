---
name: programming-essay
description: |
  Write a programming essay or blog post in the voice of the canon —
  Spolsky, Yegge, Graham, Mickens, Dijkstra, Brooks, Nystrom, Kleppmann,
  patio11. Invoke when the user wants to argue an idea about software,
  architecture, languages, or the craft — not a debugging war story
  (use debugging-story for that), not a tutorial, not a release note.
  The audience is working developers worldwide with taste and strong
  opinions of their own.
---

# Writing essays that outlive their stack

The great programming essays do one thing: they give the reader a handle
they didn't have before. *Leaky abstractions.* *Innovation tokens.* *The
kingdom of nouns.* *Worse is better.* *No silver bullet.* Ten years later
the language is gone but the phrase is still in your head. That is the
job. Everything else in this file serves it.

If you find yourself writing "in this post we will explore…" you are not
yet writing an essay. You are warming up. Cut the warm-up.

## The six moves

**1. Name the thing.** Coin a handle readers can reuse. Spolsky didn't
invent leaky abstractions, he named them. McKinley didn't invent "don't
add tech for fun," he called it an innovation token. The name is the
durable export. Before you start, ask: what am I naming? If nothing, the
essay isn't ready.

**2. Commit to a thesis inside the first three paragraphs.** Not teased.
Not hedged. The reader should know what you believe and be able to argue
with you by the time they're scrolling. Essays that survey the landscape
before taking a side are read once and cited never.

**3. If you pick a metaphor, ride it.** Yegge's medieval kingdom is not
decoration — it is the argument. Nystrom sustains *what color is your
function* for 4,000 words and never breaks. Half-committed metaphor is
worse than none. Either your whole essay lives in the metaphor's world or
the metaphor doesn't belong.

**4. Specifics, always.** Not "a common pattern in enterprise Java" —
name the class. Not "a popular framework" — name it, version it, link
the commit. Concrete detail is the smell of someone who has actually been
there. It cannot be faked and AI cannot fake it.

**5. Pull from outside the field.** Graham pulls from painting. Brooks
from theology. Norvig's *Teach Yourself Programming in Ten Years* works
because it's built on music pedagogy, not software. The outside reference
is how an essay escapes its era — React will not exist in 2040, but the
analogy will still read.

**6. Write toward one tattooable sentence.** *"All non-trivial
abstractions, to some degree, are leaky."* *"Organizations ship their org
chart."* *"Worse is better."* Every essay that's still cited has a line
you could put on a shirt. Know which sentence of yours that is before you
publish. If you can't find it, the essay hasn't earned the draft yet.

## Voice

**Do:**

- First person, confident, specific.
- Strong opinions stated strongly — then defended, not softened.
- Pull your examples from code that actually exists. Link it.
- Admit when you're arguing against a position you respect. Steelman once,
  then cut.
- Use real numbers. "47× slowdown," not "significantly slower." "2019,"
  not "a few years ago."
- Length that matches the idea. Dijkstra on `goto` is three pages. Yegge's
  *Kingdom* is twenty. Both correct. Both sized to the claim.

**Don't:**

- "In today's fast-paced world of software…"
- "Let's dive in" / "Let's explore" / "Let's take a look at"
- "On the one hand… on the other hand…" as a structural crutch.
- End with "What do you think? Let me know in the comments!"
- Pad with three-item lists where the third item is filler.
- Explain things the reader obviously knows. Motivated developers stopped
  reading when you defined `malloc`.
- Open with a dictionary definition of anything. Ever.

## The anti-AI purge list

Grep these out before shipping. Each one is a tell.

- `delve`, `dive into`, `unpack`, `walk through`, `explore`
- `leverage`, `robust`, `seamless`, `comprehensive`, `cutting-edge`,
  `powerful`, `innovative`, `scalable solution`
- `in conclusion`, `to summarize`, `in this blog post`
- `it's worth noting that`, `it's important to remember`
- `in the ever-evolving landscape of`
- `the intersection of X and Y`
- `game-changer`, `revolutionize`, `unlock`
- Parallel sentence padding: *"Not just X, but Y. Not just Y, but Z."*
- Any paragraph whose first sentence previews what the paragraph is about.
- Any section that exists only because the draft "needed a section there."

## Before and after

**AI-voiced:**

> In this post, we'll explore some common pitfalls that developers
> encounter when working with distributed systems. As applications scale,
> it becomes increasingly important to understand the tradeoffs involved
> in various architectural decisions, and microservices are no exception.

**Human-voiced:**

> Every year or so I watch a team discover, painfully, that their
> "microservices" are a distributed monolith with worse latency and a
> harder deploy story. This post is about why that keeps happening and
> three questions that catch it in the design review.

The second one names the pattern, takes a side, and puts a person in the
room. That is the whole trick. It is not a secret. It is just work.

## Three skeletons

Pick one. Don't try to combine them.

**A. Name-the-thing essay** *(Spolsky, McKinley, Brooks)*

```
[Concrete situation where the thing bites. One paragraph, in scene.]
[Name it. Bold it. Define it in one sentence.]
[Three examples of it in the wild. Specific projects, versions, links.]
[Why it exists. Root cause, not symptom.]
[What to do about it. Honest — often "nothing, just see it coming."]
[Close on the name, reframed. The sentence readers will steal.]
```

**B. Extended-metaphor essay** *(Yegge, Nystrom, Gabriel)*

```
[Open in the metaphor's world. Programming not mentioned yet.]
[Establish the metaphor's rules. Have fun with it.]
[Map to the programming situation. The reader should feel the click.]
[Push past cute. The metaphor has to earn its length by doing actual
 explanatory work. If it stops paying, the essay ends.]
[Step out of the metaphor for one clean line. Exit.]
```

**C. Contrarian take** *(Graham, Norvig, patio11)*

```
[State the consensus. Fairly. In one paragraph.]
[State your counter-claim. One sentence. Unhedged.]
[Evidence: personal experience, historical pattern, or actual data.
 Pick one and go deep. Don't try all three.]
[Concede what the consensus gets right. This is where trust is earned.]
[Sharpen the claim past where you started and close.]
```

## Length discipline

| Essay type          | Sweet spot      | Failure mode              |
|---------------------|-----------------|---------------------------|
| Name-the-thing      | 800–1,500 words | Overexplaining the name   |
| Extended metaphor   | 2,000–4,000     | Metaphor breaks, you pad  |
| Contrarian take     | 1,200–2,500     | Relitigating the obvious  |
| Technical explainer | 3,000–6,000     | No thesis, just a survey  |

If your draft is longer than the sweet spot, the idea isn't bigger — the
prose is looser. Cut 20%. The essay will be better. It always is.

## Reference cuts

When stuck, open one of these and steal the move:

- **Joel Spolsky, *The Law of Leaky Abstractions*** — how to name a
  phenomenon in 1,200 words and have it still quoted 20 years later.
- **Steve Yegge, *Execution in the Kingdom of Nouns*** — sustained
  metaphor, comic timing, mean in the way that lands.
- **Paul Graham, *Beating the Averages*** — essayistic voice, the
  Blub Paradox, how to pull in an outside-field reference.
- **Bob Nystrom, *What Color Is Your Function?*** — one idea, sustained,
  never lets go. A masterclass in not diluting a claim.
- **Martin Kleppmann, *Turning the Database Inside-Out*** — deep
  technical content in clean prose, with taste.
- **Patrick McKenzie, *Don't Call Yourself a Programmer*** — direct,
  specific career advice without motivational-poster energy.
- **James Mickens, *The Night Watch*** — humor as load-bearing structure.
- **Edsger Dijkstra, *Go To Considered Harmful*** — short and mean. The
  proof that an essay can fit on two pages.
- **Fred Brooks, *No Silver Bullet*** — how to distinguish concepts
  (essential vs. accidental) in a way readers keep using.
- **Richard Gabriel, *The Rise of Worse is Better*** — the three-word
  title that became a whole worldview.

## Final check

Read it aloud. Two tests:

1. **The Slack test.** Is there a sentence you'd paste into a group chat
   to end an argument? If not, the essay doesn't have its line yet.
2. **The 2040 test.** Strip out every library, language, and product
   name. Does the essay still have a point? If yes, ship. If no, the
   point was the stack, not the idea — and the essay will rot with it.

If both pass, you're done. Post it.
