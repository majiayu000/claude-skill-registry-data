---
name: curate-a-team-library
description: Use when building a managed team skills library for a real stack. Map work to shelves, browse before curating, write meaningful `whyHere` notes, and create a starter pack once the first pass is solid.
category: workflow
version: 4.1.0
---

# Curate A Team Library

## Goal

Build a managed skills library that another teammate or agent can actually browse, trust, and install.

Do not hand-edit `skills.json`, `README.md`, or `WORK_AREAS.md` when the CLI already has the mutation you need.

## First Move

Start with a managed workspace.

```bash
npx ai-agent-skills init-library <name>
cd <name>
```

Ask at most 3 short questions before acting:

- what kinds of work the library needs to support
- whether the first pass should stay small and opinionated or aim broader
- whether the output should stay local or end as a shareable GitHub repo

## Shelf System

Use these 5 work areas as the shelf system:

- `frontend`: web UI, browser work, design systems, visual polish
- `backend`: APIs, data, security, infrastructure, runtime systems
- `mobile`: iOS, Android, React Native, Expo, device testing, app delivery
- `workflow`: docs, testing, release work, files, research, planning
- `agent-engineering`: prompts, evals, tools, orchestration, agent runtime design

Map the user's stack to shelves before adding anything.

- Example: `React Native + Node backend` maps to `mobile` + `backend`.
- Add `workflow` only when testing, release, docs, or research are real parts of the job.
- Add `agent-engineering` only when the team is doing AI features, prompts, evals, or tooling.
- Make sure the first pass covers every primary shelf the user explicitly named.

## Discovery Loop

Browse before curating.

```bash
npx ai-agent-skills list --area <work-area>
npx ai-agent-skills search <query>
npx ai-agent-skills collections
```

If the user named multiple primary shelves, inspect each one before choosing skills.

## Mutation Rules

Keep the first pass small: around 3 to 8 skills.

- Use `add` first for bundled picks and simple GitHub imports.
- Use `catalog` when you want an upstream entry without copying files into `skills/`.
- Use `vendor` only for true house copies the team wants to edit or own locally.

Every mutation must include explicit curator metadata like `--area`, `--branch`, and `--why`.

Good branch names:

- `React Native / UI`
- `React Native / QA`
- `Node / APIs`
- `Node / Data`
- `Docs / Release`

Bad branch names:

- `stuff`
- `misc`
- `notes`

## Writing Good `whyHere`

`whyHere` is curator judgment, not filler.

- Mention the stack or workflow it supports.
- Mention the gap it fills in this library.
- Be honest about why it belongs here.

Good:

`Covers React Native testing so the mobile shelf has a real device-validation option.`

Bad:

`I want this on my shelf.`

## Featured Picks

Use `--featured` sparingly.

- keep it to about 2 to 3 featured skills per shelf
- reserve it for skills you would tell a new teammate to install first

## Collections

After the library has about 5 to 8 solid picks, create a `starter-pack` collection.

- Use `--collection starter-pack` while adding new skills.
- Or use `npx ai-agent-skills curate <skill> --collection starter-pack` for existing entries.
- Keep the collection small and onboarding-friendly.

## Sanity Check

Before finishing:

```bash
npx ai-agent-skills list --area <work-area>
npx ai-agent-skills collections
npx ai-agent-skills build-docs
```

- Run `list --area` for each primary shelf you touched.
- If you created `starter-pack`, confirm the install command looks right.
- Make sure the final shelf mix still matches the user's actual stack.

## Finish

Return:

- what you added
- which shelves you used and why
- which skills are featured
- what `starter-pack` contains, if you created one
- whether the library is local-only or ready to share
