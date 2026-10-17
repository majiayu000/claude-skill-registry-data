---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: tommy-x-posts
description: >
  Write and publish X posts for Tommy (@__morse) in his voice. Use when asked to
  draft, plan, or post a tweet or long-form X post, especially product/launch
  posts for his projects. Covers voice rules, structure, fact gathering from
  real code, and publishing via the akarso CLI.
---

# Writing X posts for Tommy

## Workflow

1. **Gather real facts first.** Read the actual project code before drafting.
   Get concrete numbers: file line counts, feature names, limits, as they exist
   in code. Never use numbers from memory or from the user's rough notes
   without verifying against the source. If a note is wrong, use the real
   number and tell the user you corrected it.
2. **Study his recent tweets** with the `searching-x` skill
   (`from:__morse -filter:replies`) to calibrate the voice against what he
   actually posts, not against these rules alone.
3. **Draft in chat, never post immediately.** Show a long post draft + a short
   tweet draft + 2-3 alternative hooks. Iterate until he explicitly says post.
4. **Publish with akarso** from `~/.kimaki/projects/akarso/cli`:

   ```bash
   pnpm akarso posts create --text "$(cat /tmp/post.txt)" --platforms x --publish-now
   ```

   Write the text to a temp file first (heredoc), never inline multiline text
   in the flag. After posting, poll `posts get <id>` until `status: POSTED`
   and share the permalink.

## Voice rules

- lowercase everywhere, except **"I" stays capitalized** and proper nouns keep
  their casing; product names he mocks or compares against can stay lowercase
- write the way he talks: full sentences that carry a thought, often with a
  clause after the comma. look at his real posts, not telegram fragments.
  "the benefit of gpuix is that you can compile the bindings in release mode
  when developing the app" is the length. "no node. no npm. no fetch." is not
- **no mic drops.** every paragraph having a clever closer reads as AI
- do not chop a list into one-word sentences. if three things belong together,
  keep them in one sentence
- no "→" arrow chains, no em dashes, no rhetorical questions, no "here's the
  thing", no listicles with bold labels
- no hashtags, no emojis
- occasional mild swearing is fine when genuinely excited, don't force it
- commands in monospace unicode, e.g. 𝚗𝚙𝚡 𝚜𝚘𝚖𝚎𝚝𝚑𝚒𝚗𝚐
- launch posts open with "introducing <name>" then one line saying what it is,
  often "for agents & humans"

## Structure (long post)

- **open with an attention-catching phrase that explains what the post is
  about.** it works when it answers a question the reader might already have:
  "how do I get agents to write good animations", "how do I get good design
  with AI", tips and tricks, valuable tools or how to use them. the reader
  should immediately see there is value in reading on. keep it plain, not
  clickbait
- **empty line between every paragraph**, no exceptions
- each paragraph is one idea, written in normal sentences that connect. 1-3
  sentences is fine if they are real sentences, not three fragments
- agent-related angles come first — agents as users of tools is his recurring
  thesis
- end with the install command in monospace unicode, then the github/site link
  as the last line, plain url

## Themes he cares about

- agents are the real users of frameworks and tools now; tools need feedback
  loops (type checking, tests) so agents fix their own mistakes without a human
- lightweight over magic: small codebases, few dependencies, tools you can read
  in one sitting, running many instances in parallel worktrees
- no hidden framework magic or implicit caching; you own your code
- deploy anywhere, no platform lock-in
- self-service software, anti enterprise bloat

## Inspiration accounts

Before drafting, read recent posts from these accounts with the `searching-x`
skill and borrow what fits:

- **@emilkowalski** (`from:emilkowalski -filter:replies`, no trailing
  underscore) — long posts about design, animations, and frontend engineering.
  Study him for: openings that promise value ("New skill: /apple-design",
  "The people getting great UI results with AI aren't using a secret model"),
  posts built around a concrete useful artifact (a skill, a fix, a technique),
  explaining one idea plainly across short paragraphs, and following up a
  launch post with example prompts / usage posts that extend its life.
- **@thdxr** — opinion pieces and formatting. He is a low-effort poster on
  purpose: humor, controversial takes stated flat with zero hedging ("the
  agent you're building into your product is most likely not going to work"),
  fake-dialogue formatting for jokes, real numbers as flexes. Study him for
  how short an opinion post can be while still landing.

## What kills a draft

If he says "sounds like AI bs", the fix is always the same: remove punchlines,
remove parallel rhetorical structure, remove manufactured hooks, and write like
someone explaining the thing to a friend.

If he says the sentences are too short, join the fragments. the voice is
casual and complete, not staccato.
