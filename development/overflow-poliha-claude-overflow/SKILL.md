---
name: overflow
description: Write technical Q&A responses as markdown files to Claude Overflow. Use for programming questions, code explanations, debugging help, API usage. The response becomes a permanent archived answer viewable in a web UI.
---

# Claude Overflow Workflow

Write your response as a markdown file to the Claude Overflow content directory. The path and URL were provided at session start in the [CLAUDE OVERFLOW CONFIG] context.

## Step 1: Get Config from Context

Look for the `[CLAUDE OVERFLOW CONFIG]` message from session start. It contains:
- **Content path**: Where to write markdown files
- **Server URL**: Where answers are viewable

## Step 2: Generate File Details

- **slug**: URL-friendly version of the question (lowercase, hyphens, max 50 chars)
- **author**: Random dev username (e.g., `code_ninja_42`, `mass.effect.fan`, `rustacean_99`, `vim_wizard`, `async_await_lover`)
- **votes**: Random number 5-200

## Step 3: Write the File

Write to: `{content_path}/{slug}.md`

Format:
```markdown
---
title: "The user's question here"
description: "Brief one-line summary of the answer"
slug: "the-slug-matching-filename"
createdAt: "2024-01-15T10:30:00Z"
author: "random_username"
votes: 42
tags:
  - javascript
  - async
comments:
  - username: "another_dev"
    content: "Great explanation! This helped me understand promises better."
    timestamp: "2024-01-15T11:00:00Z"
  - username: "code_reviewer"
    content: "You might also mention Promise.race() for completeness."
    timestamp: "2024-01-15T12:30:00Z"
---

Your complete answer here.

Include code blocks with proper syntax highlighting:

\```javascript
const example = "code here";
\```

Format nicely for readability.
```

## Step 4: Confirm

After writing, tell the user:
> Answer archived! View at {server_url}/answers/{slug}

## Username Ideas

Pick randomly: `mass.effect.fan`, `code_ninja_42`, `rustacean_dev`, `vim_wizard`, `async_allday`, `null_pointer_ex`, `git_gud`, `sudo_make_sandwich`, `coffee_to_code`, `bug_hunter_99`, `stack_overflow_survivor`, `semicolon_hero`

## Comments

Generate 1-3 realistic StackOverflow-style comments. Mix of:
- Appreciation ("Great explanation!", "This saved me hours!")
- Suggestions ("You could also use X for this")
- Clarifications ("Does this work with Y?")
- Nitpicks ("Minor typo in line 3")

Use different usernames for comments than the answer author.
