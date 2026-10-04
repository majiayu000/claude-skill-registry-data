---
name: start-new-task
description: Safely start any new piece of work on this site. Asks what you want to do in one line, creates a git branch so `main` is never touched, asks for the details, reads the code and docs, then presents a plain-English plan for approval before anything is built. Use this skill whenever the user wants to change, add, fix, update, tweak, swap, move, or try anything on the site — a new section or page, a copy edit, an image swap, a colour/spacing/font change, "this looks broken on mobile", "can we make X do Y", "I want to redesign Z" — even if they never mention branches, git, or planning, and even if the request sounds tiny. Also use when they say "start a new task", "new task", "let's work on something", "I have a new task", or invoke `/start-new-task`. Skip only if they are purely asking a question about the code with no change intended.
---

# Start a new task

You are working with a designer, not an engineer. She knows exactly how the site should look and feel, and nothing about git, builds, or React. Your job in this skill is to get her safely off `main`, understand the task properly, and hand her a plan she can actually read and approve.

Two things make this skill worth running instead of just diving in:

1. **She can't undo a mistake on `main`.** A branch is the seatbelt. Put it on before touching anything.
2. **A plan catches misunderstandings before they cost an hour.** She'll spot "no, not that card, the one below it" in five seconds of reading — but only if the plan describes what she'll _see_, not what the code will do.

Work through the steps in order. Do not skip ahead to editing files — this skill ends when the plan is approved.

---

## Step 1 — Ask what she wants to do, in one line

Ask one short, open question. Nothing else. No preamble, no checklist yet.

> What do you want to work on?

Keep it to that. She may answer with two words ("fix the mobile nav") or a paragraph. Either is fine — you only need enough to name a branch.

If her answer isn't a change to the site at all — she wants design feedback, a copy review, an accessibility audit — say so in one line and point her at the right skill (`design:design-critique`, `design:ux-copy`, `design:accessibility-review`) instead of branching.

---

## Step 2 — Create the branch

Do this **before** the detailed questions. If the conversation drifts into editing files, the seatbelt is already on.

### Name it

Format: `kind/short-slug`, where kind is one of:

| kind      | for                                                      |
| --------- | -------------------------------------------------------- |
| `content` | words, images, links, blog posts, project copy           |
| `design`  | colours, spacing, fonts, layout, hover states, animation |
| `fix`     | something is broken or looks wrong                       |
| `feature` | a new section, page, or piece of functionality           |

The slug is 2–4 kebab-case words drawn from her own wording. Examples: `content/update-about-bio`, `design/project-card-hover`, `fix/mobile-nav-overlap`, `feature/case-study-page`.

Pick the kind yourself from what she said — don't quiz her on it. If it's genuinely ambiguous (a redesign that's also a fix), pick the one that covers most of the work.

### Create it

```bash
git status --short
git branch --show-current
```

Then handle what you find:

- **On `main`, clean tree** — get the latest and branch: `git fetch origin && git pull --ff-only origin main && git checkout -b <kind>/<slug>` If the pull fails (no network, diverged), skip it, branch anyway, and mention it in one line. Don't let a network hiccup block her.
- **On `main`, uncommitted changes** — `git checkout -b` carries the changes onto the new branch, which is almost always what she wants (she started fiddling before asking). Skip the pull, create the branch, and tell her plainly: _"Your in-progress changes to X came along with you."_ If the changes look unrelated to this task, ask before carrying them.
- **Already on a task branch** — if it's for this same task, stay put and say so. If it's a different task, ask which she'd rather do: park that work and start fresh from `main`, or build on top of it. Don't guess; losing work is unforgivable.
- **Branch name already exists** — append `-2`.

Then confirm in one sentence, in her language:

> You're now on a safe copy called `design/project-card-hover`. Nothing you approve here can break the live site, and `main` stays exactly as it was.

### Never, in this skill

Push, commit, merge, rebase, force anything, `git checkout .`, `git reset --hard`, or stash without asking. Creating a branch is the only write you make. And never ask her to run a git command herself — you run it.

---

## Step 3 — Ask for the details

Now get what you need to plan. Ask **at most five questions**, chosen for this specific task — not a generic form. Number them so she can answer "1, 3, and 4".

Ask only about things you genuinely cannot decide or find yourself. Split every candidate question into one of two buckets:

- **Taste and content** — her call, always ask: exact wording, which image, which colour, how it should feel, which page it belongs on, what happens on hover, does it matter on mobile.
- **Technical** — your call, never ask: which file, which component, Tailwind vs Emotion, whether to add a dependency, how to structure it. Decide it, and if it's a real fork, state your choice in the plan as an assumption she can veto.

Things worth asking a designer that are easy to forget, when relevant:

- Is the copy final, or should I draft something for you to edit?
- Where are the images? (Give me a path, or drop them anywhere and tell me where.) Do you have them at 2x?
- Any reference — a Figma link, a screenshot, a site you like?
- Exact colours as hex, if you have them.
- Does this need to work on mobile too, or is desktop enough for now?
- Is there a hard deadline? (Changes what's worth doing properly vs. quickly.)

If she says "I don't know" or "you decide", decide — pick the sensible default and record it in the plan's assumptions. Never bounce a question back at her twice.

---

## Step 4 — Read the code and docs before planning

A plan written without reading is a guess. Read enough to know precisely which files change and what's already there to reuse.

Always start with `CLAUDE.md` — it holds the architecture notes and the Bun/Gatsby caveat you'll need for the preview instructions.

Then go straight to the relevant area. Map for this repo:

| She said                                 | Look at                                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Homepage text or sections                | `src/sections/*` (companies, contact, projects, testimonial)                                                 |
| A project card on the homepage           | `src/sections/projects/*.tsx` — one file per card                                                            |
| A project's detail page                  | `ProjectsLookup` in `gatsby-node.ts`, `src/templates/details.tsx`, images in `src/images/details/<project>/` |
| A project's hero/marketing image         | `src/images/projects/<project>/`                                                                             |
| Blog post                                | `src/content/<slug>/index.md`                                                                                |
| Nav bar, footer, page shell              | `src/layouts/mainLayout/`                                                                                    |
| A small piece reused across pages        | `src/components/` — import from the barrel `../components`                                                   |
| Contact form                             | `netlify/functions/contact-form/` (higher risk — env vars, live submissions)                                 |
| Page title, description, sharing preview | `siteMetadata` in `gatsby-config.ts`, `src/components/seo.tsx`                                               |
| A new page                               | `src/pages/` — the filename becomes the URL                                                                  |

Also worth a look: `git log --oneline -10` on the area she's changing, in case someone recently touched it, and whether a component that already does this exists (per `CLAUDE.md`, reuse beats rewrite).

---

## Step 5 — Write the plan

Use this structure. Keep the whole thing under a screen — if it's longer, the task is too big and should be split.

```markdown
## What I understood

[One short paragraph, in her words. This is the sentence she'll catch a misunderstanding in — make it specific, not a restatement of the obvious.]

## What you'll see change

- On the homepage, the three project cards will [visible change]
- On mobile, [visible change] [One bullet per thing she could point at on screen. No file names, no component names, no framework words.]

## What I need from you first

- [Blocking item, e.g. the final headline copy, or the hero image] [Or: "Nothing — I have everything I need."]

## Assumptions I've made

- [Each decision you made on her behalf that she might disagree with]

## What I won't touch

- [Nearby things she might worry about — other pages, the contact form, existing copy]

## Size

[Small / Medium / Large, plus a half-sentence why.]

## How you'll check it

[Which page, which part of it, and what "right" looks like.]

## Open questions

- [Anything still unclear. Or omit this section entirely.]
```

Writing rules that matter more than the template:

**Describe what she'll see, never what the code does.** "The card lifts slightly and the shadow deepens when you hover" — not "add a transform and box-shadow transition to ProjectCard".

**Say the risk out loud when there is one.** Touching the contact form, env vars, or dependencies is riskier than changing copy, and she deserves to know before approving, in one plain sentence: _"This one touches the contact form, so if I get it wrong, messages could stop arriving — I'll test it before we're done."_

**Swap the jargon.** Some ready-made translations:

| don't say             | say                              |
| --------------------- | -------------------------------- |
| component             | the reusable piece / the card    |
| props                 | settings                         |
| refactor              | tidy up behind the scenes        |
| branch                | a safe copy of the site          |
| commit                | save a checkpoint                |
| merge / deploy        | put it on the live site          |
| responsive breakpoint | how it looks on phones           |
| build fails           | the site won't finish generating |

**Don't pad.** A one-line copy change gets a four-line plan. Ceremony on a tiny task trains her to skim the plans that actually matter.

---

## Step 6 — Save it, present it, and stop

Save the plan so she can reopen it tomorrow or in a fresh session:

```bash
mkdir -p .claude/tasks
```

Write it to `.claude/tasks/<branch-with-slashes-as-dashes>.md` — e.g. branch `design/project-card-hover` → `.claude/tasks/design-project-card-hover.md`. Put the branch name and the date at the top of the file.

Then post the plan in the chat too (don't make her open a file to read it), and close with exactly what to say next:

> Say **go** and I'll build it. Or tell me what to change — nothing's been touched yet.

**Then stop.** Do not start implementing, do not create files, do not "just make a start". Waiting for a real yes is the entire point of the plan.

When she does approve, one thing to carry forward: `bun run dev` fails under Bun's runtime in this repo (see the caveat in `CLAUDE.md`) — the dev server needs Node, and the preview lives at `http://localhost:8000`. Use the `run` skill for previews rather than working it out from scratch.
