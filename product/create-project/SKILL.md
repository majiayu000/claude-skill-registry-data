---
name: create-project
description: Start a new project in the user's brain after a short interview (what it is, the goal, where it stands, what exists, the next steps), placed in the right hub with its About.md and Roadmap.md. Use when the user types /create-project, says "nouveau projet", "crée un projet pour X", "I want to start X" or brings work that fits no project.
argument-hint: "[what the project is, in a few words]"
metadata:
  internal: true
---

Turn an idea or a new piece of work into a project folder any future session can pick up from one file. The brain is the folder named in the `## Brain` section of `~/.claude/CLAUDE.md` (default `~/brain`). Talk to the user in their language, one short question at a time, with no jargon (never say "slug", "frontmatter" or "repo" to them). Write every file in English; only names (products, people, tools) stay as they wrote them.

1. **Read.** Read the brain `AGENTS.md` (its hubs and rules) and every `projects/**/About.md` title and status. When an existing project or hub already covers this work, say so in one line and propose to continue it or add a sub-project inside it rather than a new folder.
2. **Interview.** Ask only what the argument and the conversation did not already answer, one question per message, each with an example or choices. Accept short answers and move on when they skip one.
   1. What is it, in one or two sentences, and what does "done" look like? (for example "a landing page for my coaching offer, online with a payment button")
   2. Where does it stand? "Just an idea", "started", or "already well along".
   3. What already exists? Links, files, a folder with code, accounts, people involved, tools it uses. "Nothing yet" is fine.
   4. Is there a date or a rhythm? (a launch date, every week, no rush)
   5. What are the next 2 or 3 steps, or the first thing you want me to do on it?
3. **Place.** Pick the hub from `AGENTS.md` that fits (a business, `perso/`...), or the `projects/` root when none does, and a short folder name in lowercase with dashes (`coaching-landing`). Propose a new hub only for a new business or a big new area. Confirm place and name in one line, for example "I'll put it in `projects/my-coaching/landing-page/`, OK?".
4. **Create.** Write `About.md` from [references/about-md.md](references/about-md.md) with only what they told you: "To fill" rather than a guessed fact, number or link. Put the date or rhythm and what exists under Key info (a code folder outside the brain stays where it is: write its path). Write `Roadmap.md` with the next steps as checkboxes, the first thing to do on top. Create `files/`, `assets/` or `output/` only with their first file, never empty. A new hub gets its own short `About.md` and a line in the Hubs list of `AGENTS.md`.
5. **Save.** Commit in the brain with `git add -A` and `project: create <name>`, and push when the brain has a GitHub copy.
6. **Report.** Tell the user in 3 lines where the project is, the first step, and that next time they just say "load project <name>". Offer to start that first step right now.
