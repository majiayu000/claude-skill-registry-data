---
name: draft-post
description: >-
  Load this skill when drafting a new blog post from a topic, repo, or idea (interview first) or
  from notes or an outline (draft straight away). Trigger on "write a blog post about this repo",
  "turn these notes into a post", "interview me for a blog post". Not for an existing draft.
argument-hint: "[topic, repo URL or path, or notes file] [blog posts path]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Uses uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML, to check a
  BUSINESS_PLAN or EVIDENCE YAML before reading it, and to check and render the voice profile.
  Without uv they are read or written unchecked, and the profile's Markdown is not rendered.
license: Apache-2.0
---

# Draft post

Turn whatever the author has into one complete, publishable draft in their personal voice. The
input decides the route: a repo or bare topic gets an interview first, rich notes get drafted
immediately. Done means a full post with a title, body, and meta description, ending on its open
thread, saved or shown where the Output section says.

## Procedure

### 1. Read the blog first

Read the blog, not just the repo, before the first question or the first word of the draft. Every
question this skill has goes into the one batch of step 3, per
`${CLAUDE_SKILL_DIR}/references/ask-the-author.md`. Read that file now.
**Finding the blog:** use a path or URL the user gave; otherwise look in the current repo for a
posts directory (`content/`, `posts/`, `_posts/`, `src/content/`, `blog/`); if neither turns one
up, add a question to the batch on where the blog lives. "No existing blog" is a valid answer and
skips this step.

Read the previous posts, especially the latest one on the same project. When the blog runs as a
series, each post an episode the reader follows in order, also do the steps marked (series).
Then:

- **Pick up the thread** (series): if the last post ended on a live thread, open with it ("Last time I
  said…") and cross-link it. When interviewing, add a question to the batch: _"the last post
  ended on X, is this the post that answers it?"_
- **Pin chronology**: if the material does not say when this happened relative to the last post,
  add one timestamp question to the batch. It prevents continuity bugs (wrong versions, events out
  of order).
- **Check continuity facts** (series) against earlier episodes: versions, dates, what the reader already
  knows. Don't re-tell a story a previous episode owns — call back in a sentence and link.
- **Leave a thread** (series): plan what this episode leaves open. Closure instead if the series is
  finished.
- **Capture the voice once**: if the blog has three or more posts, the target repo's `CLAUDE.md`
  defines no blog voice, and neither `blog-voice.yaml` nor `blog-voice.md` exists in
  `.agents_workspace/product/blog/` or the older `.agents_workspace/product/` root yet, write
  `.agents_workspace/product/blog/blog-voice.yaml` from the posts, filling
  `${CLAUDE_SKILL_DIR}/assets/blog-voice.template.yaml`, per the `blog-voice/v2` section of
  `${CLAUDE_SKILL_DIR}/references/blog-voice-schema.md`, each point backed by a line quoted word
  for word with the post it came from. After the last edit, run
  `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`, which checks it
  and writes `blog-voice.md` beside it. On exit 1, fix each error it lists and render again. On
  exit 2 or 3, without uv, or when the command is denied, say in the reply that the profile went unchecked and unrendered. On
  later runs read the profile instead of re-deriving it, the YAML when there is one: first run the
  same command with `check`. On exit 1, use no profile and report its errors, unless the only
  error is a stale `.md`, which `render` repairs. On exit 2 or 3, without uv, or when the command is denied, say it went
  unchecked and read it anyway. A `blog-voice.md` with no YAML is a `v1` profile, read as it is,
  and converted as the schema says only before an amendment the author asked for. Offer once to
  move the profile into `CLAUDE.md` so it outlives the workspace, and move it only with the
  author's agreement. The profile governs vocabulary, register, and rhythm. The banned tells in
  Voice still apply.

### 2. Read the material and pick the route

Read everything provided before doing anything else, then follow the matching route.

**A repo or code artefact** (GitHub URL, local path, pasted README or file contents): read it
before asking anything.

- **GitHub URL**: fetch the README with `WebFetch` (`https://raw.githubusercontent.com/{owner}/{repo}/main/README.md`, `master` if `main` fails), or with `gh repo view {owner}/{repo}` when `gh` is available — the only route that works for a private repo. Browse key files if needed (`package.json`, `pyproject.toml`, main entry point).
- **Local path**: `Glob` the top two levels, `Read` the README (or `.rst`/`.txt`), then key manifests and entry points for stack and structure.
- **Pasted content**: read it directly.

**Product handoff files.** When the repo has them, read them before inferring anything, because
they hold what earlier stages settled. `.agents_workspace/product/business/BUSINESS_PLAN.yaml` gives who the product is for,
the problem, and the differentiator: take them from it rather than asking. `.agents_workspace/product/EVIDENCE.yaml`
bounds every claim about what the product does or how well it does it (tested, fast, secure,
usable). Read only its newest section, the first one, because earlier sections describe older
commits. State only what that section's Claims list, and nothing about an area it marks `stale`,
`not run`, or `open issues`. When either file is missing, carry on from the repo and say which
claims rest on nothing proven. Where only the `.md` of a file
exists, read that. Before reading a YAML, run
`uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <file>.yaml` (formats in
`${CLAUDE_SKILL_DIR}/references/business-plan-schema.md` and `evidence-schema.md`). On exit 1,
stop and report its errors, unless the only error is a stale `.md`. On exit 2 or 3, or without
uv, say in the reply that the file went unchecked, and go on. The user, problem and
differentiator are `sections.target_customer.body`, `sections.problem.body` and
`sections.value_proposition.body`, the newest run is `runs.0`, its claims `runs.0.claims`, and
each area's status `runs.0.areas.<area>.status`.

Infer without asking: **what it does** (README, module names, entry points); **who it's for**
(docs, example usage); **stack and key design decisions** (structure, dependencies); **current
state** (finished tool, experiment, WIP?). A repo usually supports several post types, so surface
only the angles that fit, as one question in the batch:

> _Which angle should the post take?_
> _A. **Launch/showcase** — what it is, why you built it, how to use it_
> _B. **Tutorial/How-To** — walk readers through building something similar_
> _C. **Lessons Learned** — what you discovered, what surprised you, what you'd do differently_
> _D. Other: say what_

If the repo can support multiple posts (complex system, long build journey, multiple use patterns),
add a second question: _"This project has enough depth for a short series, e.g. an intro post now,
a deep-dive into [key decision] later, a retrospective once it's been out a while. A. One post to
start (recommended) B. Plan a series C. Other: say what"_ For a series, plan the arc first (which
post covers what), then one post at a time.

**Notes, bullets, an outline, or fragments**: assess completeness.

- **Rich material**: multiple specifics, a clear arc or argument. Draft immediately.
- **Workable but sparse**: angle clear, some detail thin. Draft, and flag the gaps in the refinement offer rather than asking upfront.
- **Genuinely incomplete**: a topic with no substance — no story, steps, or argument. The one case warranting a batch before drafting, built around the question that unlocks the most (e.g. "What was the moment this actually became a problem?"). Then draft without further questions.

**Only a topic, idea, or experience** (verbal prompt, nothing written): infer **topic**, **post
type**, **audience**, **goal** (credibility, lesson, traffic, entertainment, announcement), and
**length/tone**. Each one that is genuinely uninferable becomes its own question in the batch, the
audience and takeaway ones first. Then interview (step 3).

### 3. Interview for what is missing

Skip this step when the material is rich or the route was notes. Otherwise read
`${CLAUDE_SKILL_DIR}/references/interview.md` and follow it: what to ask for each post type, the
four story beats, and the interview rules. Send every question from steps 1 to 3 as one batch, in
the format of `${CLAUDE_SKILL_DIR}/references/ask-the-author.md`.

### 4. Draft the post

Produce a complete draft — not an outline, not a bullet summary.

- **Title**: sharp, specific, honest. No clickbait, no vague "My Thoughts on X". Aim for: _specific claim + implicit promise to reader_.
- **Opening**: inside a moment or a thought within the first 2 sentences — not background, not a product pitch.
- **Body**: match structure to post type (below). Use the user's own words and specifics — quotable interview lines go in nearly verbatim, and real details are not paraphrased into abstractions.
- **Closing**: the open thread (see Voice). No "I hope this was helpful", no manufactured takeaway, lesson, or CTA.
- **Length**: what the content needs, not the length of the source material — don't pad, don't cut substance.
  - Opinion / Personal Story / Thought Leadership: 400–800 words. Tight is better.
  - Lessons Learned / Launch: 600–1,000 words.
  - How-To / Tutorial: 800–1,800 words, driven by steps and code samples — no ceiling if genuinely required.

**Post types:**

| Type                   | Trigger signals                                                          | What it needs                                                 |
| ---------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Lessons Learned**    | "I tried X", "we built Y", "I made a mistake", a story ending in insight | Story arc: situation → problem → decision → outcome → insight |
| **How-To / Tutorial**  | "how to do X", "step-by-step", commands, config snippets                 | Concrete steps, actual commands/examples, pitfalls            |
| **Opinion / Take**     | "I think X is wrong", "here's my hot take", a stated position            | Clear thesis, 2–3 arguments, counter-argument addressed       |
| **Project / Launch**   | "I shipped X", "we launched", feature descriptions                       | What it does, why it matters, what was hard, what's next      |
| **Thought Leadership** | "my view on [trend/industry]"                                            | Unique insight backed by evidence, non-obvious conclusion     |
| **Personal Story**     | "something happened to me", "my journey"                                 | Emotional arc, honest detail, why the reader should care      |

**Structure by post type.** Every template ends on **the open thread** (defined in Voice).

**Lessons Learned:**

```
Hook: The moment it went wrong (or right)
Setup: Context — what were you trying to do?
The Story: What happened, in order
The Turn: When/where things changed
The Insight: What you actually learned (be specific)
The Open Thread: What's unresolved, what you'll watch for, what comes next
```

**How-To:**

```
Hook: The moment this became a problem for you / what it cost you
Overview: What we're doing and why this approach
Steps: Numbered, concrete, with real examples
Pitfalls: What they cost you — narrated as your experience, not warnings issued to the reader
The Open Thread: Where this leaves you — what's still rough, what you're watching for
```

**Opinion / Take:**

```
Hook: State the controversial or non-obvious thesis upfront
Argument 1: [strongest point]
Argument 2: [second point]
Counter-argument: What the other side would say — and why you're still right
The Open Thread: Where you actually land — a reserved verdict is valid; what would change your mind
```

**Project / Launch:**

```
Hook: The moment that led to building it (a scene or a thought), with what it does and who it's for inside the first paragraph
The Origin: Why you built this — what was missing, what frustrated you, why existing tools didn't cut it
How It Works: The interesting parts only — architecture, key decisions, not a feature list
What Was Hard: Be honest — one real technical or design challenge
The Open Thread: What's unresolved, what you're watching for, what comes next
```

**Thought Leadership:**

```
Hook: State the non-obvious claim or question upfront — don't bury the thesis
Argument: Build through specific examples, not abstract assertions (name real products, companies, events)
Counter-argument: The strongest objection — acknowledge it directly, then explain why the thesis holds
Implication: What changes if this view holds? (concrete, not vague)
The Open Thread: What's still unresolved in your own thinking — what you'll watch for next
```

**Personal Story:**

```
Hook: The specific moment this post is really about — one concrete scene, not a summary
Setup: Enough context to understand what was at stake (brief)
Arc: What happened, what changed, what the turning point was
The Insight: What you actually learned — specific, not "I learned resilience"
The Open Thread: What's unresolved, what you'll watch for, what comes next
```

### 5. Refine

After sharing the draft, ask for feedback as one batch in the format of
`${CLAUDE_SKILL_DIR}/references/ask-the-author.md`. Turn every item below that applies into its
own question, with the fix as an option. Always close with one general question, _"How does the
draft read overall? A. Ready to use B. Needs the changes answered above C. Other: say what"_. These
are things you'd fix even if they're happy. Watch for and raise:

- **Opening too slow**: first paragraph is setup, not a moment — offer an alternative opening.
- **Missing the specific**: draft generalizes where the material or interview has real numbers, names, or moments — insert them.
- **Wrong angle**: post reads for practitioners but the audience is beginners (or vice versa).
- **Conclusion fizzles or lectures**: ending restates the intro, trails off, or lands on a tidy takeaway or CTA — replace with the genuinely open thread or a reserved verdict.
- **Influencer tells**: any banned tell present — rewrite quieter, per Voice.
- **Continuity slip**: a version, date, or fact contradicts an earlier episode — fix against the previous posts.
- **Paraphrased voice**: a quotable line got smoothed into generic prose — restore the user's phrasing.
- **Generic title**: could describe dozens of posts — push for a specific claim or hook.
- **Tone mismatch**: source casual, draft formal (or vice versa) — ask if they want the voice adjusted.
- **Gaps flagged earlier**: surface thin spots as concrete questions: _"The pitfalls section would be stronger with a real example. A. I'll paste one B. Leave the pitfalls as drafted C. Other: say what"_

If the user wants a different angle or structure, **re-draft** — a revision that fights the original structure reads like a revision.

## Rules

### Voice

Personal voice, not influencer style — the reader overhears the reasoning, not a lecture. If the
target repo's `CLAUDE.md` defines a blog voice, it overrides every structure template above.

**Prefer:** first person, grounded in what actually happened and was thought; connected
paragraphs that carry the narrative — reflective, not prescriptive; doubt and self-report kept in
("I shipped it anyway, because I was tired of this bug"); quieter is better; open inside a moment
or a thought — an annoyance, a realization, a scene — never a product pitch or background.

**Banned tells:** punchy standalone one-liner paragraphs; aphoristic closers ("The boring choice
is the correct one"); imperative lessons aimed at the reader ("Don't design your own. Surface
theirs."); "If you're building X, then Y" prescriptions; bold pseudo-headers as section labels
("**What it does**", "**The lesson:**"); tidy meta-takeaway sign-offs that turn a personal story
into a lecture; CTA endings.

**Never invent scenes, feelings, or chronology.** Every beat comes from the material (changelogs,
specs, commits) or the author's own words — quote those nearly verbatim; the phrasing _is_ the
voice. If a human beat is missing, flag the gap instead of fabricating it.

**Endings — the open thread:** the honest current state — what's unresolved, what you'll watch
for, what comes next. A reserved verdict ("I'm keeping it, for now") is valid. Only a finished
series' final post ends with closure — no manufactured cliffhangers. Never a tidy takeaway,
lesson, or CTA.

**Series:** when the blog is a series, each post is an episode the reader follows in order (see
step 1).

**Tutorials** keep full utility — real code, steps, pitfalls — but pitfalls are narrated as what
they cost the author, not warnings issued to the reader.

### Working principles

- **Pick the strongest thread**: if the material sprawls, choose the sharpest angle rather than covering everything, and tell the user which thread you picked and why.

### Edge cases

- **Wall of notes with multiple threads**: pick the strongest one — don't weave. Tell the user, then draft immediately without asking permission: _"Your notes cover a few directions. I've written about [angle X] because [reason]. If you'd rather have [angle Y], I'll re-draft."_
- **Conflicting signals** (half story, half tutorial): pick the dominant signal and note the tension: _"Your notes mix story and tutorial. I've written this as a [type], which fits most of the material. If you want the other framing, I can re-draft."_
- **How-To with abstract steps**: if real commands, config, or code are missing, draft with what's there and flag it in the refinement offer (_"drop in actual commands and I'll weave them in"_). Don't ask upfront if the rest is strong enough.
- **No clear topic yet**: ask what they've been working on, thinking about, or frustrated by lately, as a question with options for the likely areas. The topic is in there.
- **Multiple posts wanted**: one at a time — complete the first interview and draft before starting the next.
- **Expert writing for beginners**: push them to explain jargon, add examples, and not skip "obvious" steps.
- **Listicle or generic SEO post**: write it well anyway, but flag a more compelling angle if one is hiding underneath.
- **No human to answer** (a headless run, or called by another agent): draft from the material you have and never invent a personal moment, quote, or number. Put a bracketed placeholder where each missing specific belongs (`[the moment you noticed X]`), mark the post as a draft, and end with the interview questions you would have asked, as the numbered batch with options. With only a bare topic and no material, stop and report that the post needs the author's story.

## Output

**During an interview:** one numbered batch of every question, each with lettered options, no preamble.

**Before drafting** (if noting thread selection or flagging a gap): one short paragraph, then the draft immediately.

**Final draft**: complete post, ready to copy-paste — title; body (subheadings only if length warrants); one-line meta description `> **Meta:** [description]` — ~150 chars, specific angle, readable without the title.

**Where it goes:** the post is always YAML with its Markdown rendered beside it, filling `${CLAUDE_SKILL_DIR}/assets/blog-draft.template.yaml`, per the `blog-draft/v2` section of `${CLAUDE_SKILL_DIR}/references/blog-draft-schema.md`, with `status: draft` (its `title` and `description` replace the title line and the `> **Meta:**` line). Inside a blog repo (a posts directory was found), save it there as a new `.yaml` named in the existing posts' filename pattern, so the rendered `.md` sits where the other posts do, its front matter the format's keys. Otherwise save it to `.agents_workspace/product/blog/<YYYY-MM-DD>-<slug>.yaml`, the slug from the title in kebab case. Then run `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`, which writes the `.md` in the layout of `${CLAUDE_SKILL_DIR}/assets/blog-draft.template.md`, and fix the YAML for each error it lists. Never edit the generated `.md`: a later revision goes through the YAML. On exit 2 or 3, or without uv, say in the reply that the draft went unchecked and unrendered. Show the post in chat too, so an interview's post outlives the session.

## Hands off to

- Once the user is satisfied, mention: _"When you're ready to share this, `/ceh-blog-and-seo:repurpose-post` can adapt it into a Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb."_
- If the input turns out to be an existing prose draft rather than notes, offer `/ceh-blog-and-seo:edit-post` instead of drafting over it.
