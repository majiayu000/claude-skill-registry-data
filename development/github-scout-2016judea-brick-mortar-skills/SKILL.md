---
name: github-scout
description: Evaluate GitHub before building or picking tooling, and read what's trending. Use whenever you're looking for or thinking about a tool, library, framework, MCP server, agent harness or skill pack to solve something — "is there a tool for X", "what should we use for Y", "before we build this", "is this already solved" — and when you ask "what's trending on GitHub", "anything new on GitHub", "check trending repos". Includes a no-auth trending scraper that writes a weekly digest.
---

# github-scout

Two jobs: a fit search for one specific need, and a broad sweep of what's trending.

## 1. Fit search: a specific need

Before building a tool, or choosing one, search GitHub for the need, not the name of a
tool you already know.

```bash
gh search repos "<the need in plain words>" --sort stars --limit 20 \
  --json fullName,description,stargazersCount,pushedAt,license,language
gh search repos "<need>" --sort updated --limit 20 ...   # catches new work stars haven't found yet
gh search code "<distinctive API or file name>" --limit 20  # who already wired the thing we'd wire
```

Run 2-4 phrasings of the need. Then read the latest trending digest (job 2) for anything adjacent.

Judge each candidate on these facts. Read them; never guess.
- **Alive:** `pushedAt` within ~90 days, and issues get answered (`gh issue list -R o/r --limit 10`).
- **Licence:** `gh repo view o/r --json licenseInfo`. No licence means you can't ship it. AGPL inside a hosted product is a problem.
- **Fit:** read the README and one real source file. Does it do *your* step, or something nearby?
- **Weight:** what it pulls in, and whether it needs an account or key you don't have.

**Output: the decision first**: *use X* / *fork X* / *build it, nearest was X because Y*.
One line per candidate under that. Stars measure attention, not fit. Never pick on stars alone.

A good existing repo rarely kills a build. It changes **what** you build: wire it in,
don't rewrite it.

## 2. Trending: the broad sweep

`trending.py` scrapes github.com/trending. No auth needed. It writes
`~/.claude/github-trending/YYYY-MM-DD-<since>[-lang].md`.

```bash
python3 trending.py weekly            # or daily / monthly
python3 trending.py weekly --lang python
```

To run it on a schedule on macOS, add a launchd agent (e.g. Mondays 07:00) that calls the
script with an absolute path. Keep its output under `~/.claude`, not `~/Desktop` or
`~/Documents`: launchd jobs are denied access to those folders by macOS privacy controls.
To read it: `ls -t ~/.claude/github-trending | head`.

When you read a digest, name the 1-3 repos that touch **your** live work, say what each
would change, and skip the rest. An adjacent idea goes on a backlog as one line; don't
start new work for it.

## Traps
- If the script prints "0 repos parsed", GitHub has changed the trending markup. Fix the regexes in `trending.py`; don't fall back to guessing.
- Trending ranks by stars gained in the period. A spike can come from a launch, a Hacker News post or a bot ring. Check the repo's age and its commit history before you trust the spike.
- `gh search` is rate-limited to 30 requests/min when authenticated. Spread the phrasings out.
- **Impostor repos ride every trending name.** A popular repo's name returns the real project and also low-star clones that copy its description and offer an "Official free download... Local zip" for Windows. Those clones are malware bait. Install only from the canonical repo's own package (the npm/pip name in *its* README), and never run a zip from a clone.
- **Reverse-engineering agents don't get through bot walls.** Headless capture tools tend to hit rate-limit pages and PerimeterX/Kasada walls on big consumer sites, and a JS analyser can report 0 network endpoints in a Next.js bundle where a plain `grep /graphql/` finds the route. Curl probing is often the faster path. Set a timeout on every step, or a missing selector hangs the run forever.
