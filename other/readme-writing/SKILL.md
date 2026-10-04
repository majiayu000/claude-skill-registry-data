---
name: readme-writing
description: Use when creating, rewriting, or improving README files for public repositories
---

# README Writing

## Overview

Write README files that help a visitor understand the project in the first screen, trust it within one minute, and try it without guessing. A good README is a landing page, setup guide, and trust signal at the same time.

## When To Use

Use this skill when:

- Creating a new `README.md`.
- Rewriting a README for a public repository.
- Improving a README's clarity, structure, visuals, or quickstart.
- Adding badges, screenshots, diagrams, language links, or contribution sections.
- Making a repository more attractive for GitHub readers.

Do not use it for long-form product docs, API references, or internal-only runbooks unless the user specifically wants a README-style entry page.

## Workflow

1. Identify the primary reader.
   Decide whether the README is for users, developers, contributors, evaluators, or agents. Put the most important reader first.

2. Write the first screen.
   Include project name, one-sentence value proposition, optional language links, visual banner or screenshot, and trust badges.

3. Explain the project quickly.
   State what it does, who it is for, and why it is different. Avoid marketing fluff that does not help someone decide whether to continue.

4. Show the fastest path to value.
   Provide a short quickstart with commands that can be copied. Include expected output when it reduces uncertainty.

5. Show structure and capabilities.
   List key directories, features, or modules. Use tables for scanability when comparing multiple items.

6. Add proof.
   Include screenshots, SVG diagrams, badges, test commands, examples, or links to demos. Prefer local assets for long-lived public repos.

7. Cover contribution and license.
   Link to contribution docs, issue templates, validation commands, and license.

8. Verify the README.
   Check links, commands, image paths, and consistency with the actual repository.

## Recommended Structure

```markdown
# Project Name

Language links, badges, and hero image.

One-sentence value proposition.

## Why This Exists
## Features
## Quickstart
## Examples
## Project Structure
## Contributing
## License
```

Adjust the sections to the project. Keep the README useful, not ceremonial.

## Visual Guidelines

- Use a hero image, product screenshot, or architecture diagram when it helps visitors understand the project faster.
- Prefer local assets under `docs/assets/` for stability.
- Use badges sparingly: license, tests, package version, or public readiness are usually enough.
- Add alt text for images.
- Avoid huge images that push all useful text below the fold.

## Multilingual README Pattern

For multilingual repositories:

- Keep `README.md` as the default language most GitHub visitors should see.
- Add language links near the top.
- Use files like `README.zh-CN.md` for full translations.
- Keep shared sections such as features, quickstart, and skill lists consistent across languages.

## Verification

Before claiming completion:

- Confirm every referenced file path exists.
- Confirm links point to the right local files or public URLs.
- Run repository validation or tests if README commands mention them.
- Check that badges and images render from valid URLs or local files.
- Re-read the first screen and verify it answers: what is this, why care, how do I start?

## Common Failures

- Starting with a long backstory instead of a clear value proposition.
- Including installation commands that do not match the repository.
- Adding badges that look impressive but do not communicate useful trust.
- Using screenshots or diagrams without alt text.
- Letting translated READMEs drift from the main README.
- Hiding the quickstart below too much explanation.

## Example

User:

```text
Make this repository README more attractive for GitHub.
```

Agent:

1. Reads the project structure and existing README.
2. Identifies the target reader and primary use case.
3. Adds a strong first screen with badges and a local hero image.
4. Adds a short quickstart and capability table.
5. Verifies image paths, links, and commands before reporting completion.
