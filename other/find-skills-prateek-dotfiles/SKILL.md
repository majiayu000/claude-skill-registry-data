---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

Use the open agent skills ecosystem to find reusable workflows, tools, and templates. The `npx skills` CLI searches and installs skill packages; [skills.sh](https://skills.sh/) is its public directory.

## Find a skill

1. **Translate the request into search terms.** Identify the user's domain and task, then choose specific keywords. For example, search for `react performance` rather than `testing` when the user wants to speed up a React app.
2. **Check the leaderboard.** Look at [skills.sh](https://skills.sh/) for popular skills in that domain before running a CLI search. Common sources include `vercel-labs/agent-skills` for web development and `anthropics/skills` for frontend design and document processing.
3. **Search when the leaderboard does not answer the request.** Run `npx skills find <query>`, such as:

   ```bash
   npx skills find react performance
   npx skills find pr review
   npx skills find changelog
   ```

   Results include an install target and a skills.sh page, for example:

   ```text
   Install with npx skills add <owner/repo@skill>

   vercel-labs/agent-skills@vercel-react-best-practices
   └ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
   ```

4. **Check each candidate before recommending it.** Review its install count, source author, and GitHub repository. Prefer skills with at least 1K installs; treat fewer than 100 as a caution. Official sources such as `vercel-labs`, `anthropics`, and `microsoft` have stronger provenance. Treat repositories with fewer than 100 stars cautiously. Base claims on the current listing and repository details.
5. **Present useful options.** For each match, give the skill name and purpose, install count and source, exact install command, and skills.sh link. For example:

   ```text
   I found a skill that might help: "vercel-react-best-practices" provides React and Next.js performance guidance from Vercel Engineering (185K installs).

   Install it with:
   npx skills add vercel-labs/agent-skills@vercel-react-best-practices

   Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
   ```

6. **Install only after the user chooses to proceed.** For a user-approved global install, run:

   ```bash
   npx skills add <owner/repo@skill> -g -y
   ```

## Search categories

Use these examples as starting points, then narrow the query to the user's task.

| Category | Example queries |
| --- | --- |
| Web development | `react`, `nextjs`, `typescript`, `css`, `tailwind` |
| Testing | `testing`, `jest`, `playwright`, `e2e` |
| DevOps | `deploy`, `docker`, `kubernetes`, `ci-cd` |
| Documentation | `docs`, `readme`, `changelog`, `api-docs` |
| Code quality | `review`, `lint`, `refactor`, `best-practices` |
| Design | `ui`, `ux`, `design-system`, `accessibility` |
| Productivity | `workflow`, `automation`, `git` |

Try related terms when a query returns no useful results. For example, replace `deploy` with `deployment` or `ci-cd`. Popular skill sources also include `ComposioHQ/awesome-claude-skills`.

For installed skill maintenance, use `npx skills check` to look for updates and `npx skills update` to update installed skills.

## If no skill fits

Tell the user that the search found no suitable match, offer to help with the task directly, and mention `npx skills init <name>` if they want to create a reusable skill. For example:

```text
I searched for skills related to "xyz" but did not find a match. I can still help with the task directly. Would you like me to proceed?

If you expect to repeat this work, you could create a skill with:
npx skills init my-xyz-skill
```
