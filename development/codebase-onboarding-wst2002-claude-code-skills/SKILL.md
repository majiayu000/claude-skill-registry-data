---
name: codebase-onboarding
description: Use when joining or exploring an unfamiliar codebase, asked to explain how a project works, where something is implemented, how to run it locally, or to create an onboarding guide for new team members.
---

# Codebase Onboarding

## Overview

Give a new developer a working mental model in minutes: what the project does, how it is organized, how a request flows through it, how to run it, and where to make common changes. Every claim points to a file.

## Method

1. **Identify the project:** README, manifests (`package.json`, `pom.xml`, `pyproject.toml`, `go.mod`), languages, frameworks, versions.
2. **Find how it runs:** scripts, `Makefile`, `docker-compose.yml`, `.env.example`, CI workflow (the CI file shows the real build and test steps).
3. **Map the structure:** top-level folders and what each owns. Find the entry points (server start, routes, CLI main, app root).
4. **Trace one real flow end to end:** for example an HTTP request from route → handler → service → database → response, with file paths.
5. **Find the conventions:** state management, data access, error handling, logging, testing style, naming.
6. **List the gotchas:** required services, generated code, environment quirks, slow or flaky parts, areas without tests.
7. **Write the guide** with the format below. Verify the run commands exist.

## Output format

```
# <Project> — onboarding

## What it is
<2-3 sentences: purpose, users, main tech>

## Run it locally
<prerequisites, env setup, install, run, test commands — verified>

## Map
| Path | Responsibility |

## How a request flows
<numbered steps with file paths, or a Mermaid sequence diagram>

## Conventions
<how to add an endpoint / page / table here, with an example file to copy>

## Gotchas
<things that surprise newcomers>

## Where to start
<3 good first areas or files to read, in order>
```

When the user asks a narrower question ("where is checkout implemented?"), answer it directly with paths and a short flow, and skip the full guide.

## Common mistakes

- Describing the folder tree without explaining responsibilities.
- Explaining frameworks in general instead of how this project uses them.
- Listing commands from memory instead of from the scripts that exist.
- Missing the one required service or environment variable that blocks first run.
- Reading only the README, which is often out of date; trust code and CI first.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
