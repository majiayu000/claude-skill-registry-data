---
name: enhance
description: Use when the user invokes /workbench:enhance or asks for one autonomous improvement, such as "improve this repo", "find something worth building", or "surprise me". An optional domain narrows the search. For multiple improvement lanes with stacked PRs, use workbench:incremental-enhancement-lanes.
---

# Enhance

Requires git and authenticated GitHub CLI (`gh`) when a remote is configured. Shipping uses the bundled `workbench:commit-to-pr` skill.

The user has handed you an open mandate: work out what this project should
become next, and build a piece of it. They deliberately did not say what.

**This is not a backlog agent.** You are not here to drain a TODO list or close
the gap between the README and the code. If the user wanted the recorded work
done, they would have pointed at it — it's already written down, and pointing is
cheap. They invoked an open mandate because they want judgment they don't
already have: the thing they'd have wanted if they'd thought of it.

The target is **"huh — I wouldn't have thought of that, and now I can't unsee
it."** Aim there.

## The one rule: do not ask

No clarifying questions. Not about scope, not about which of two options they'd
prefer, not "before I start, should I…". A question defeats the entire point —
they invoked this precisely so they wouldn't have to think about it yet.

You will hit ambiguity anyway. Resolve it, in this order:

1. **Read more code.** Most "questions" are answered three files away.
2. **Follow the repo's existing convention.** If there's one way things are done
   here, that's the answer, even if you'd have chosen differently.
3. **Take the reversible option.** When genuinely torn, pick the one that's
   cheaper to undo, and note it as an assumption in the PR body.

Stating an assumption in the PR is the substitute for asking. The user gets to
disagree with it in review, which costs them one comment instead of a
conversation.

## Phase 1 — Understand the trajectory

You are not inventorying the codebase. You are working out what it's *for*, who
uses it, and which way it has been moving.

Read the README, the entry point, and the core module — enough to use the thing
in your head. Then read direction out of the history:

```bash
git log --oneline -40
```

What kinds of changes keep landing? What did the last three features have in
common? A project reveals its ambition through what its author keeps choosing to
work on. That trend line, extended forward, is where your candidates live.

Then actually run it, or trace the main path end to end as a user would. The
best candidates come from *using* the thing, not from reading it. Friction you
feel in ninety seconds of use is friction nobody has written down yet — which is
exactly why it's still there.

If a domain argument was given, it narrows *where you look*, not how good the
pick has to be. `/enhance perf` means find the best performance change, not
settle for a mediocre one because it was the only performance-shaped thing in
sight.

## Phase 2 — Invent

This phase is the whole value of the skill. Implementation is the easy part;
choosing something the user wouldn't have thought of, that's still right, is
what's hard. Do it in the main thread so the reasoning is visible.

**Generate at least five candidates of your own, then throw out your first
two.** Recorded items — the TODO, the roadmap entry, the open issue — don't
count toward the five; rejecting them is context, not generation. The first
ideas of your own are the obvious ones — the missing flag, the visible gap. They
arrive first because they required no thought. Keep generating past them; the
interesting candidates come after the well runs dry once.

### Where forward-driving candidates come from

**Latent capability.** The codebase is one small step from being able to do
something notably more valuable, and nobody has noticed the step is small. The
pieces are already there; someone just never connected them. This is the richest
vein for surprise, because the cost is low and the payoff reads as obvious only
in hindsight.

**Friction a real user would hit.** Not friction the author recorded — friction
they've absorbed so long they stopped seeing it. The step everyone does manually.
The thing you have to know to use this correctly, that isn't anywhere.

**The next thing on the trend line.** If the last four commits were all making
this more scriptable, what does fully scriptable look like, and what's missing
from it? Extend the author's own direction past where they've gotten to.

**The unasked question the design implies.** The architecture is committed to
something. What does that commitment make possible that hasn't been claimed yet?

### What looks impactful but isn't

- **Backlog execution.** TODOs, `FIXME`s, and open issues are the *previous*
  author's leftovers, not your judgment. Worse: an old unpicked TODO is often
  unpicked because someone decided it wasn't worth it. Read them for context on
  what's already been considered, then look somewhere else. If your pick came
  from a grep, you have almost certainly retreated to the safe answer.
- **Hygiene work** — formatting, lint config, dependency bumps, coverage for its
  own sake, a LICENSE file. This is where agents go when they can't find a real
  idea, and it costs the user their open mandate.
- **Speculative scaffolding** — a config system, a plugin API, an abstraction
  layer nothing consumes. Surprise is the goal; *unmoored* is not. The test is
  whether it serves someone's actual use today, not whether it's novel.
- **Anything requiring product judgment you can't derive** — pricing, auth
  policy, what the company wants this to be. Read this fence narrowly. A
  *technical* decision with two defensible options is not product judgment: it's
  exactly what rule 3 is for. Pick the reversible one, state it as an assumption,
  and move. Dropping a strong candidate because it involves a choice is the most
  expensive mistake available here — the candidates worth having usually involve
  one, and the safe alternative is a backlog item.
- **The grand refactor.** Even when it's right, it isn't this.

### The tie-breaker

Nobody approved this pick, so imagine the maintainer opening the PR cold:

- *"…why did you do this?"* → unmoored. You optimized for novelty over use.
- *"Sure, that was on my list."* → correct, but you wasted the mandate. They
  could have gotten this by asking for it.
- *"Huh — I wouldn't have thought of that. Yes."* → **this is the target.**

Two things have to be true at once: they didn't see it coming, and once they see
it they agree. Either alone is a failure.

### Size envelope

One coherent change — a diff a reviewer reads in a single pass and a competent
dev ships in one sitting.

This constraint is what makes the ambition safe. If your pick needs a migration
plan, a design doc, or a "phase 2", carve off the smallest piece that stands
alone and delivers value by itself. A half-landed large feature is worse than a
whole small one, because the user now owns the remainder.

### Fences

Nobody is watching while this runs, so some things stay off the table regardless
of how good the idea is. These bound the blast radius; they are not a licence to
be timid:

- Auth, credentials, permissions, payments, or anything security-sensitive
- Destructive schema changes, data migrations, or deleting working code beyond
  what the change strictly requires
- Breaking changes to public APIs or existing callers
- CI/CD, deploy config, or anything that runs outside this repo
- New dependencies, unless the change is genuinely impossible without one —
  prefer the standard library, and say so in the PR if you added one

Work on a fresh branch. Never commit to the repository's default branch.

Declining is a real option, but a high bar — a project with a direction almost
always has a next step, and "nothing to build" usually means you stopped
generating candidates too early. Go back and generate five more. Only report
"nothing clears the bar" if the honest answer is that any addition would be
invention for its own sake. Shipping filler to have shipped something is worse.

## Phase 3 — Spec

Write the implementation spec before dispatching. The implementer subagent has
none of your context, so the spec has to stand alone — anything you leave
implicit gets re-derived, badly or not at all.

```
GOAL: <one paragraph, concrete enough to be unambiguous>
WHY: <the insight behind the pick — keeps the implementer from drifting>
FILES: <the files to touch>
CONVENTIONS: <file:line pointers to exemplars in this repo to imitate>
DONE WHEN: <observable outcome + the exact command that verifies it>
NOT IN SCOPE: <the adjacent things it must not touch>
```

`NOT IN SCOPE` matters more than it looks. An implementer with spare capacity
will helpfully expand the diff, and scope creep is what turns a sharp pick into
a sprawling one.

## Phase 4 — Implement

Dispatch one subagent with the spec. Instruct it to:

- Match surrounding style — naming, error handling, test structure, comment
  density. New code should be unidentifiable as new.
- **Verify by execution, not by reading.** Run the test suite, or run the code
  path, or exercise the CLI. "It compiles" and "the diff looks right" are not
  verification. If there's no test suite, run the thing directly.
- **Capture the "before" state by running it too.** The claim that justifies the
  pick — the traceback, the wrong exit code, the broken output — is the one
  you're most likely to assert from reading the source and least likely to
  re-check, because by the time you're writing it up it feels like established
  fact. It is also the claim the whole change rests on. Check out the pre-change
  code and record what it actually does, with the same rigour as the after.
- **Re-run the ordinary path, not just the motivating one.** Before/after on the
  broken case shows the fix; it doesn't show what changed for everyone else. Run
  the most common invocation — the README example, the bundled sample input — on
  old and new code and compare stdout *and* stderr. A new warning that fires on
  every normal run is a regression in the experience even when every test is
  green, and it's easy to miss because you were looking at the edge case.
- **Green tests prove less than they appear to.** A passing test only shows it
  passes against the code you wrote; it doesn't show it would have caught the
  problem. Break the behavior on purpose and confirm the suite notices — revert
  *only* the logic under test, keeping any new surface area in place, or mutate
  the property the code is supposed to guarantee. Two ways this bites: a test
  that fails with `unrecognized argument` is telling you the flag is new, not
  that the test detects the bug; and a suite that only asserts *relational*
  properties (this equals that, the length is right) can pass 10/10 while you
  swap the hash algorithm underneath it.
- Report the actual command and its actual output, including failures. Paste
  what the terminal emitted; never retype, tidy, or reassemble a session into
  what it "would have" printed. A reconstructed transcript is fabrication even
  when every value in it happens to be right, because the one thing a reader
  wants from raw output — evidence it actually ran — is precisely what
  reconstruction removes. The tell is a log too clean to be real: a
  copy-pasteable command that isn't on `PATH`, no shell noise, no missing
  quotes, nothing that errored on the first try.
- If a verification step went wrong, append the correction rather than
  regenerating the log. A verification log that edits out its own wrong moment
  is worth less than one that shows it.

When it returns, read the diff yourself. Confirm the scope held and the change is
what you specified — a subagent reporting success is evidence, not proof. If
verification didn't genuinely run, run it now before going further.

## Phase 5 — Ship

Check for a remote first (`git remote -v`).

**With a remote:** invoke the `workbench:commit-to-pr` skill. Invoking `/workbench:enhance` is the
authorization for the PR; it lands on a feature branch, never on the default branch.

**Without one:** skip `workbench:commit-to-pr` entirely rather than invoking it and letting
it fail at the push. Commit to the feature branch yourself, write the same
content as a summary instead of a PR body, and say the PR step was skipped
because there's nowhere to push. The user still gets a reviewable commit, which
was the point.

The PR body has to sell an idea the user hasn't had yet. Include:

- **What changed** — one paragraph
- **The insight** — what you noticed that made this worth building. This is the
  most important section. If you can't articulate why this wasn't already
  obvious, you probably picked a backlog item.
- **Also considered** — two or three of your own rejected candidates (not the
  backlog items you skipped), one line each. Converts
  an unaudited pick into an auditable one, and lets the user redirect you cheaply
  if you chose wrong.
- **Assumptions** — every ambiguity you resolved under rule 3
- **Verification** — the commands you ran and what they printed, before *and*
  after, plus the ordinary-path comparison. The before output is the evidence
  the pick rests on; a reviewer who only sees the after has to take the problem
  on faith.

## Report back

Close with the PR link, the one-line pick, and the strongest runner-up. If the
user disagrees with the pick, the runner-up is what they'll reach for, and
offering it costs one sentence.
