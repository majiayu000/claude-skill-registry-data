---
name: ord-ship
description: Publish to npm, create README, set up repo, and log the shipment
type: ops
version: v0.4
context_intake: artifact_only
---

# ORD Ship

Invoke as `/ord-ship`.

Rapid shipping for ORD packages. Publishes to npm, creates a developer-friendly README, sets up the GitHub repo, and appends to the running ship log.

## Process

1. **Pre-flight:** Confirm the package is ready to publish.
   - Read the ord-align doc for scope, package name, and API surface.
   - Run the build and tests. Fix blockers.
   - Verify the core API works as documented.
   - Check `package.json` has correct name, version, description, keywords, license, and repository fields.
   - Ensure `files` or `.npmignore` is configured to publish only intended files.
2. **README:** Create or verify `README.md` with:
   - Package name and one-line description
   - Install command (`npm install <name>`)
   - Quick start (3-10 lines showing the primary use case)
   - API reference (brief — each exported function/command with signature and one-line description)
   - License
3. **Publish to npm:**
   - Run `npm publish` (or `npm publish --access public` for scoped packages).
   - Verify the package appears on npmjs.com.
   - If publish fails due to auth, report the blocker and provide the manual command.
4. **GitHub repo setup:**
   - Ensure the repo has a description, topics/tags, and the homepage URL set.
   - Add a `.github/FUNDING.yml` if the user has sponsorship configured.
5. **Ship log:** Append entry to `research/ord-ship-log.md`:
   - Date, package name, npm URL, GitHub URL
   - Tech stack used
   - Build time (estimated hours)
   - v1 API surface summary
   - Success metric from alignment doc
   - Status: `published`
6. **Distribution:** Execute launch-day distribution:
   - Identify relevant channels: dev Twitter, Reddit r/node or r/javascript, HN Show, relevant Discord servers
   - Draft a launch post (the user posts it manually)

## Output

End with:

```md
**Shipped:** <package name> — <npm URL>
**Next work:** monitor adoption for 1-2 weeks, then run the ORD traction gate before any Devtool AFPS graduation decision
**Recommended next command:** /ord-traction (after monitoring) or /ord-scan (next experiment)
```

## Constraints

- Do not gold-plate. Ship the minimum useful version.
- Do not run `npm publish` without user confirmation if this is the first publish for this package.
- Do not modify unrelated packages or repositories.
- If npm auth is not configured, provide the manual publish command and stop.
- Create `research/ord-ship-log.md` with a header if it doesn't exist.

## Default Shipping Contract

Follow the shared shipping contract convention.
