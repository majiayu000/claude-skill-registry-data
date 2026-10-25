---
name: gem0-agent
description: Work in Gem0 (gem0.dev headless CMS) as the signed-in user through an agent token (gem_pat_...) - list and create projects, tables (schemes), rows, project API keys. Use whenever GEM0_TOKEN is set, the user hands you a gem_pat_ token, or asks Claude to manage their Gem0 content or setup. The live API reference is served by Gem0 itself; always fetch it first. Prefer this over gem0-api, which needs session headers.
---

# Gem0 agent API

This skill is a stub. The contract lives on the server and changes with each deploy.

1. Check `GEM0_TOKEN` (`gem_pat_...`) is set; if not, ask the user. They mint one in the Gem
   admin under Settings, Agent tokens. `GEM0_URL` defaults to `https://apist.gem0.dev`.
2. Fetch the current reference and follow it over anything you remember:
   `curl -fsS "${GEM0_URL:-https://apist.gem0.dev}/en/v3/agent/skill"`
3. Find out what this token may do before doing anything:
   `curl -fsS "${GEM0_URL:-https://apist.gem0.dev}/en/v3/agent/me" -H "Authorization: Bearer $GEM0_TOKEN"`
   Stay inside `modules` and `projects` from that response.

Rules that hold whatever the live doc says:

- Never echo, log, commit or paste the token anywhere. Reference it as `$GEM0_TOKEN`.
- Any `remove`, disabling a user, revoking a key or publishing needs the user's explicit yes in this session.
- On `success:false`, show the `data` field verbatim; Gem0 messages name the exact cause.
- A 403 means the token is read-only or the route is human-only (login, minting tokens). Tell the user; do not look for a way around it.
