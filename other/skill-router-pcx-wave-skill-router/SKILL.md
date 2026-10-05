---
name: skill-router
description: >
  Activate once per session to route substantive requests to the right installed skill.
  Two modes: suggest (interactive, ranked proposals) or auto (silent with attribution footer).
  Trigger: /skill-router on | /skill-router on --auto | /skill-router status
version: 1.2.0
license: MIT
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# Skill Router

## Purpose

Scan all installed skills once, build a lightweight in-session index, then route
subsequent requests to the most relevant skill — but only when a skill would
materially improve the response. No overhead on conversational or trivial requests.

Two modes:
- **Suggest mode** (default): proposes matching skills ranked by relevance, waits for confirmation
- **Auto mode**: routes silently and appends `*(via skill-name)*` to routed responses

---

## Activation

### `/skill-router on` — suggest mode (default)

### `/skill-router on --auto` — auto mode

Both run the same activation steps:

### Step 1 — Scan installed skills

```bash
find ~/.claude/skills -name "SKILL.md" | sort
```

For each file found, extract the following fields (in order of preference):
1. `name:` from YAML frontmatter
2. `description:` from YAML frontmatter
3. `triggers:` or `trigger:` from YAML frontmatter (if present)
4. If any field is missing, infer it from the first 20 lines of the file

Skip `skill-router` itself. Skip files that cannot be read.

### Step 2 — Build the index

Construct an in-memory table (session-only, never written to disk):

```
SKILL INDEX
-----------
<skill-name> | <trigger keywords, comma-separated> | <one-line description>
...
```

Also initialize an in-memory **session usage counter**:

```
SESSION_USAGE = {}   ← empty dict, incremented each time a skill is invoked
```

Example row:
```
geo-audit | geo, seo, audit, AI search | Full website GEO+SEO audit with parallel subagent delegation.
```

Rules:
- Extract trigger keywords from the `trigger`, `triggers`, or `tags` frontmatter fields
- If none exist, infer 3–5 keywords from the description and first 20 lines
- Keep the total index under 1000 tokens — truncate descriptions aggressively, not skill names
- Group similar skills mentally (e.g. all `geo-*` skills = "GEO/SEO domain")

### Index quality

The router reads only frontmatter + first 20 lines of each `SKILL.md` at activation time — NOT the full content. Full `SKILL.md` content is only loaded when a skill is actually selected for routing. This means routing quality depends directly on the quality of each installed skill's frontmatter.

The fields that matter most:
- `description:` — most important. Use verb-first phrasing with concrete keywords.
- `tags:` — explicit keyword list for matching.
- `trigger:` / `triggers:` — alternative keyword sources.

Good frontmatter example:
```yaml
description: "Run a full GEO audit on a website — crawlability, schema, content quality, AI citability"
tags: [geo, seo, audit, AI search]
```

Bad frontmatter example:
```yaml
description: "A useful skill for various tasks"
```

Tip: if an expected skill is not triggering, check its frontmatter first.

### Step 3 — Confirm activation

If the scan returns zero SKILL.md files, reply:
```
Skill Router: no skills found at ~/.claude/skills. Install skills first.
```
and do not activate routing.

Otherwise, reply with exactly one line:

```
Skill Router active [suggest | auto] — <N> skills indexed (<domain1>, <domain2>, ...).
```

Examples of domains: GEO/SEO, Testing, Deployment, Git, Security, Code Review, AI Delegation.
List at most 5 domain labels. Nothing else.

---

### `/skill-router off`

Reply with exactly one line: `Skill Router off.`
All subsequent requests are answered directly — no routing until `/skill-router on` is run again.

---

## Behavior after activation

> **Lifecycle note:** routing state lives in conversation context. In very long sessions,
> context compression may truncate earlier turns and silently deactivate routing.
> If you notice routing has stopped, re-run `/skill-router on` to re-activate.

For **every subsequent user input**, first apply the gate check:

```
1. Is the request conversational, a simple question, or under ~10 words?
   → Answer directly. Do NOT load any skill.

2. Is it a substantive task (feature, audit, workflow, architecture, etc.)?
   → Scan the index. Identify all skills with HIGH confidence match.
   → Branch based on active mode (see below).

3. No HIGH confidence match?
   → Answer directly from your own knowledge. Do NOT mention any skill.
```

**HIGH confidence** = clear keyword overlap, not just tangential similarity.

```
✅ "run a GEO audit on plume.africa" → geo-audit (exact domain + action match)
✅ "write a Dockerfile for this Node app" → docker-patterns (explicit tool + task)
❌ "fix this bug in my app" → no match (too generic, no skill keyword overlap)
❌ "how do I structure my API?" → no match (tangential, answerable directly)
```

---

## Suggest mode behavior

When one or more skills match with HIGH confidence, **before answering**, show:

```
Suggested skills for this request:
  1. <skill-name> — <one-line reason why it matches>
  2. <skill-name> — <one-line reason why it matches>  ← if a second skill also matches

Use skill 1, 2, or answer directly? (1/2/no)
```

- List at most 2 skills, ranked by relevance (most specific first)
- Wait for the user's reply before proceeding
- If user replies `1` or `2` → load that skill's SKILL.md fully, apply its rules, then **record usage** (see Usage Tracking)
- If user replies `no` or anything else → answer directly without loading any skill
- If only one skill matches, still show the prompt with just option 1

---

## Auto mode behavior

When one skill matches with HIGH confidence:
- Load that skill's SKILL.md fully, apply its rules, then **record usage** (see Usage Tracking)
- Append exactly this footer at the end of the response:

```
*(via skill-name)*
```

- No other mention of routing. No preamble. No explanation.
- If two skills match equally, prefer the **more specific** one
  (e.g. `geo-schema` beats `geo` for a schema-only question)

---

## Routing rules (both modes)

- Load **at most one skill** per request
- Never load a skill for requests under ~10 words
- Never trigger `skill-router` on itself
- Never auto-trigger on `/skill-router status`
- The bar is HIGH: only trigger when the skill would **change the quality of the response**,
  not just because keywords overlap

---

## Usage Tracking

Every time a skill is invoked (user confirms in suggest mode, or auto-routes), do two things:

**1. Update in-memory session counter:**
```
SESSION_USAGE[skill-name] += 1
```

**2. Persist to `~/.claude/skill-usage.json`** by running this Bash command (replace `SKILL_NAME` and `TODAY`):

```bash
python3 -c "
import json, os
f = os.path.expanduser('~/.claude/skill-usage.json')
d = json.load(open(f)) if os.path.exists(f) else {}
s = 'SKILL_NAME'
d.setdefault(s, {'total': 0, 'last_used': None})
d[s]['total'] += 1
d[s]['last_used'] = 'TODAY'
json.dump(d, open(f, 'w'), indent=2)
"
```

Where `TODAY` = current date in `YYYY-MM-DD` format (`$(date +%Y-%m-%d)`).

Run this silently — no output to user.

---

## `/skill-router stats`

Read the persistent usage file, merge with the session counter, and display:

```bash
python3 -c "
import json, os
f = os.path.expanduser('~/.claude/skill-usage.json')
print(json.dumps(json.load(open(f)), indent=2) if os.path.exists(f) else '{}')
"
```

Then display a table sorted by `total` descending, with session column overlaid from `SESSION_USAGE`:

```
Skill Usage Stats
-----------------
Skill               | Total | Session | Last Used
--------------------+-------+---------+----------
geo-audit           |    12 |       2 | 2026-05-15
vibe                |     8 |       1 | 2026-05-18
docker-patterns     |     3 |       0 | 2026-05-01
geo-schema          |     0 |       0 | never
```

Rules:
- Show all skills currently in the index, even if count = 0
- Skills with `total = 0` appear at the bottom with `never` as last used date
- Sort: descending by `total`, then alphabetically within ties
- Session column shows 0 for skills not used in the current session
- After the table: `Total invocations this session: <sum of SESSION_USAGE values>`

---

## `/skill-router status`

Show exactly this, nothing more:

```
Skill Router status
-------------------
Mode:           suggest | auto | off
Skills indexed: <N>

Index:
  <skill-name>  |  <trigger domains>  |  <one-line description>
  ...

Last skill used: <skill-name> | none this session
```

If the router was never activated this session:
```
Skill Router not active. Type `/skill-router on` (suggest) or `/skill-router on --auto` to activate.
```

---

## Non-goals

- Do NOT persist the index across sessions (stateless, session-only)
- Do NOT update the index mid-session
- Do NOT load multiple skills per request
- Do NOT trigger on greetings, status checks, or clarifying questions
- Do NOT create any files during activation or routing — **except** `~/.claude/skill-usage.json` (usage tracking only)
