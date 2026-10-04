---
name: blog-hypothesis
description: Use when a blog post starts as an idea, hunch, opinion, or irritation and no evidence has been gathered yet. Trigger on "I want to write about X", "I have a theory that", "I've been thinking that", "I hate the term", or any post idea arriving without sources.
---

# State the hypothesis

The first stage. It exists because **research without a falsifiable claim only finds
confirmation** — you gather what fits and never notice what doesn't.

A hypothesis is not a topic. "Spec-driven development" is a topic. "SDD should be called
Spec-Driven Delivery because the practice extends past development" is a hypothesis: it can
be checked, and it can turn out to be wrong.

## Prerequisite

None. This is the entry point.

## Write it to the working doc

One file per post: `docs/research/<slug>.md`, snake_case slug matching the eventual post.
Create it with the stage block and the hypothesis section:

```markdown
# <Working title>

## Stage

- [x] Hypothesis
- [ ] Research
- [ ] Thesis _(gate — human approval)_
- [ ] Outline
- [ ] Draft

## Hypothesis

**Claim.** One sentence, falsifiable.

**Who it's for.** Who changes their mind or their practice if this lands.

**What would falsify it.** The specific finding that would kill or badly wound the claim.

**Why I might be wrong.** The strongest version of the opposing case, written honestly.
```

## The four fields, and why each is required

| Field     | Purpose                          | Failure if skipped                             |
| --------- | -------------------------------- | ---------------------------------------------- |
| Claim     | Gives research something to test | Research becomes topic-browsing                |
| Audience  | Sets register and depth          | Piece argues with nobody in particular         |
| Falsifier | Makes the claim honest           | You cannot tell success from confirmation bias |
| Why wrong | Surfaces the rival case early    | The objection arrives from a reader instead    |

**The falsifier is the one people skip and the one that matters most.** If you cannot name
a finding that would change your mind, you are not writing an argument — you are writing an
opinion with citations attached.

## Do not

- **Do not research first and back-fill the hypothesis.** A hypothesis written after the
  evidence is a summary, and it will quietly match whatever you happened to find.
- **Do not soften the claim to make it safer.** A hedged claim cannot be falsified, so
  research cannot inform it. Overstate slightly; the thesis stage will correct it.
- **Do not skip "why I might be wrong"** because the case seems obvious. On this site's
  own SDD post, the rival framing (goal-driven development) already existed in public and
  was found during research, not before it.

## Expect the claim to change

It usually does, and that is the process working rather than failing. The `blog-thesis`
stage exists specifically to reconcile this hypothesis against what the evidence supported.
Recording the claim now is what makes that comparison possible later.

## Next step

→ `blog-research` to gather and verify sources against this claim.
