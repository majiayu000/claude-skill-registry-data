---
name: github-for-gtm
description: Understand GitHub well enough to run a GTM context repo, no CS degree required. The mental model (repo, commit, branch, push, pull, clone), the operator's GUI-first workflow (GitHub Desktop, or let Claude Code handle the git), how to organize the repo, and the hard rules on what to never commit (CRM data, API keys, transcripts, pricing). The prerequisite to building a context repo. Fire on "what is a repo", "how does GitHub work", "learn git", "GitHub for GTM", "do I need to know GitHub", "clone the starter kit", "commit and push", "how do I organize my repo", or the start of building a GTM context repo.
---

# GitHub for GTM: run a repo without a CS degree

## What this does
Gives a GTM operator the exact GitHub knowledge needed to build and run a context repo, and nothing more. The mental model, the workflow, how to organize it, and what to never put in it. This is the 20% of git you actually use, so the repo stops being the scary part and GTM can own it in the AI era.

## What you'll need (reads)
A free GitHub account, and GitHub Desktop installed if you want to skip the terminal entirely. Your context repo, or the starter kit you plan to clone. No coding, ever.

## The mental model, in plain English
- Repository ("repo"). A project folder that also keeps its full history, like a Time Machine for the folder. Your GTM brain lives in one repo.
- git vs GitHub. git is the tool that tracks changes on your computer. GitHub is the cloud that stores the repo, backs it up, and shares it with your team and with Claude.
- Commit. A saved snapshot with a short note, for example "Add ICP tiers". Commit small and often so you can always look back or roll back.
- Push and pull. Push uploads your commits to GitHub. Pull downloads the latest. This is how every device, teammate, and agent stays in sync.
- Clone. Download a copy of a repo (like the starter kit) to your machine.
- Branch. A safe copy where you try a change without touching the main version, then merge it back when it works. Working solo, you can mostly live on the main branch.
- Private vs public. Anything with your company context should be a private repo.

## The method: the operator workflow, GUI first
1. Set up once. Create a free GitHub account. Install GitHub Desktop (or Tower) so you never need the terminal. Sign in so it is linked to your account.
2. Get a repo. Either clone an existing one (in GitHub Desktop: File, Clone repository, e.g. the GTM starter kit) or create a new one (File, New repository). Choose Private for anything with company context.
3. Open it where you work. Open the repo folder in Claude Code or your editor. This is where CLAUDE.md and the context files live.
4. Make a change, then commit it. Edit a file, or let Claude write one. GitHub Desktop shows exactly what changed. Type a short message ("Add signal library v1") and click Commit.
5. Push so it is saved and shared. Click Push. Now it is on GitHub, backed up, and any teammate or agent can pull it.
6. Pull before you start next time. Open the repo, click Pull, and you have the latest before you touch anything.
7. Or let Claude Code do the git. Claude can stage, commit, and push for you with clean messages while you just review. Either path is fine, pick the one you will actually use.

## How to organize the repo
- Follow the five layers: CLAUDE.md at the root (the brain), context/ (knowledge), skills/, workflows/, outputs/ (the archive).
- Plain, descriptive file names in lowercase-with-dashes. A README that says what lives where.
- Name outputs by date and type so they sort themselves: YYYY-MM-DD-type-name.md.

## Never commit this (the guardrail that saves you)
- CRM data or contact lists. Customer and prospect data never goes in git.
- API keys or passwords. Put them in a .env file and add it to .gitignore. Never hardcode a key.
- Raw meeting transcripts. Summarize the substance into the right context file instead.
- Pricing and commercial terms. Keep them out of the repo.
A .gitignore file simply lists what git should ignore, like .env. A good starter kit ships one already.

## Failure points
- Committing a secret or CRM data. It is hard to fully erase from history, so treat a leaked key as burned and rotate it.
- Leaving a company repo public when it should be private.
- Letting fear of the terminal stop you. Use GitHub Desktop, or let Claude commit.
- Hoarding weeks of uncommitted changes. Commit small and often.

## The receipt (writes)
[your context repo, private, cloned or created, with your first commit pushed and a .gitignore protecting your keys]

## Example chat
**You:** I want Claude to manage my context repo git for me, I don't want to touch the terminal or GitHub Desktop.

**Claude:** That works. I'll edit a file, then stage, commit, and push it for you.
```
$ git add context/icp.md
$ git commit -m "Add ICP tiers v2"
$ git push
```
You just review the diff before I commit, same as you'd review anything else I write. The one thing that would burn you here: if a CRM export or an API key ever lands in a context file, it's in git history the moment I commit it, and that's hard to undo.
One sharpener: add a .gitignore now, before the first real commit, so a stray .env file never gets the chance.

## Go further
Knowing the mental model is the prerequisite. Here is what running the repo looks like once it's second nature.

- **Let Claude Code own the git dance entirely.** Skip GitHub Desktop altogether, have Claude stage, commit, and push on every session while you just glance at the diff.
- **Guard the repo automatically.** Add a pre-commit check that blocks a commit containing anything that looks like an API key or a CRM export, so the rule isn't just something you have to remember.
- **Sync teammates without a git lesson.** Point teammates at GitHub Desktop's Pull button only, so they get the latest context before a call without ever touching a terminal.

The repo runs itself. You just review what changed.

## Next move
Now build the brain. Hand off to the Context Pack to write CLAUDE.md. Built GTM. Receipts only.
