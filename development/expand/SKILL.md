---
name: expand
description: Enrich the user's profile from the public sources they already link to (GitHub repositories, a portfolio site, published projects). Use when the user says /expand, "add my GitHub projects to my profile", or after /setup when the profile is thin. Proposes each discovered fact with its source; nothing is added without the user's yes.
model: claude-sonnet-5-5
effort: high
---

# /expand: what the public web says you have done

The writer may use only what `data/profile.json` holds. This skill finds
what is missing from it, from places the user already points to, and asks
before adding anything.

## Steps

1. Read `data/profile.json`: `links` (GitHub, portfolio, LinkedIn), the
   `projects`, the `experience` bullets, the `skills` and the `facts`.
2. For each public link, fetch what is there. For GitHub, the user's public
   repositories: name, description, languages, README highlights, stars,
   last activity. For a portfolio site, the project pages. LinkedIn is not
   fetched; the user can export it as a PDF into `documents/` instead.
3. Compare with the profile. List, as a table, each candidate addition:
   a project not in `projects`, a language or framework not in `skills`, a
   concrete, checkable fact not in `facts`. Each row names its source.
   Leave out anything vague, anything older than the profile's own
   timeline, and anything the user did not build themselves.
4. Ask the user which rows to add. Then write them with `/profile`'s rules:
   projects as `{name, role, start, end, link, bullets}`, skills into the
   right list, facts as one sentence each. Every added bullet is plain, has
   one fact, and uses only what the source said.
5. Say that the answer memory starts over, because the profile changed,
   and offer `npx jev apply --dry --count 2` to see the effect.

Never invent a number, a date or a credential. If a source and the profile
disagree, ask; do not pick.
