---
name: stack-sync
description: Point it at a repository. It reads the dependency manifests, updates your daily.dev tech stack and follows the matching tags, so your feed matches what you actually build. Shows the plan before changing anything.
---

# Stack Sync

Your daily.dev feed is only as good as the tags you follow and the stack on your profile. Stack Sync derives both from the code you work on.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected with the `write` scope, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Read the manifests** in the current repository: `package.json` (dependencies and devDependencies), `go.mod`, `Cargo.toml`, `pyproject.toml` or `requirements.txt`, `Gemfile`, `pom.xml`/`build.gradle`, `composer.json`, plus Dockerfiles and CI config for infrastructure (Postgres, Redis, Kubernetes, Terraform). Collect the technology names, not every package: `@fastify/cors` means Fastify, `@types/*` means nothing.
2. **Look at what's already there.** `getProfileStack` (`GET /profile/stack?limit=100`) and `getFeedsFilters` (`GET /feeds/filters`). Don't propose anything already on the stack or already followed.
3. **Resolve each technology twice.** Tags and stack tools are separate vocabularies:
   - Tag: `getSearchTags` with `q` set to the name (`GET /search/tags?q=<name>`). Tags are lowercase hyphenated slugs; `typeorm` has no tag while `fastify`, `graphql`, `redis`, `postgresql` do. Spaces in the query are treated as hyphens.
   - Stack tool: `getProfileStackSearch` with `query` (`GET /profile/stack/search?query=<name>`). Use the returned `title` exactly; the add call must match an existing tool.
4. **Show the plan.** One table: technology, tag found (or none), stack tool found (or none), action. Ask the user to confirm, and let them strike lines. Report the technologies that matched neither so they can add them by hand.
5. **Apply.**
   - Tags: `postFeedsFiltersTagsFollow` with the list (`POST /feeds/filters/tags/follow`, body `{ "tags": [...] }`). One call for all tags.
   - Stack: `postProfileStack` per tool (`POST /profile/stack`, body `{ "title": "Fastify", "section": "primary" }`). Use `primary` for the main stack, `learning` or `hobby` if the user says so.
6. **Optional: a feed for this repo.** If the user wants it, create a custom feed named after the repository with `postFeedsCustom` (letters, numbers and spaces only, max 50 characters) and follow the same tags on it with `postFeedsFiltersByFeedIdTagsFollow` (`POST /feeds/filters/{feedId}/tags/follow`).
7. **Confirm** with `getProfileStack` and `getFeedsFilters` and summarize what changed.

## Output

The plan table before, a short "done" list after: tags followed, tools added, anything skipped and why.

## Guardrails

- Never unfollow, block or remove anything. This skill only adds.
- Always show the plan and wait for confirmation before step 5.
- A typical sync is 2 lookups per technology plus 2 to 4 writes, so 20 to 30 requests for a medium repo. Say so if the user is on a free account.
