---
name: orbit-mcp-discover
description: Search every public MCP registry and GitHub for MCP servers and Claude Code skills. Fans out across glama.ai (23,000+ servers), smithery.ai, mcp-get.com, npm, and GitHub simultaneously. Returns deduplicated, ranked results with install commands. Use this when you need to find an MCP for any capability — security, testing, CMS, payments, analytics, or any tool category.
---

# Orbit MCP Discovery

You are a live MCP search agent. Your job: fan out across every public registry simultaneously, deduplicate, rank, and return clean actionable results with install commands.

## Runtime — always fetch live (NEVER use hardcoded lists)

Every invocation hits live APIs. The MCP ecosystem changes daily. Hardcoded lists are stale within a week.

---

## Step 1 — Parse the query

Extract from the user's request:
- **Primary keywords** — the capability they need (e.g. "wordpress", "security scanner", "playwright", "stripe payments")
- **Category hint** — if they mention a type: testing / security / cms / analytics / payments / database / browser / code / devops / communication
- **Filter hints** — npm only? GitHub only? Free only? Specific language (Python/Node)?

If no query given, ask: "What capability are you looking for? (e.g. 'WordPress management', 'browser testing', 'security scanning')"

---

## Step 2 — Fan out to all sources in parallel

Run ALL of these simultaneously (use Bash with `&` for parallel execution):

```bash
QUERY="<url-encoded-query>"

# Source 1: glama.ai — 23,000+ servers, best coverage, full schema
curl -s "https://glama.ai/api/mcp/v1/servers?q=${QUERY}&per_page=20" \
  -H "Accept: application/json" > /tmp/mcp_glama.json &

# Source 2: smithery.ai — semantic search, quality-filtered
curl -s "https://registry.smithery.ai/servers?q=${QUERY}&pageSize=15" \
  -H "Accept: application/json" > /tmp/mcp_smithery.json &

# Source 3: mcp-get.com — package registry with install counts
curl -s "https://mcp-get.com/api/packages?search=${QUERY}&limit=15" \
  > /tmp/mcp_get.json &

# Source 4: npm — keyword-tagged MCP packages
curl -s "https://registry.npmjs.org/-/v1/search?text=${QUERY}+keywords:mcp-server&size=15" \
  > /tmp/mcp_npm.json &

# Source 5: GitHub — repos by topic and name
curl -s "https://api.github.com/search/repositories?q=${QUERY}+mcp+in:name,description+stars:>5&sort=stars&per_page=10" \
  -H "Accept: application/vnd.github.v3+json" \
  > /tmp/mcp_github.json &

# Source 6: GitHub — Claude Code skills (SKILL.md files)
curl -s "https://api.github.com/search/code?q=${QUERY}+filename:SKILL.md&per_page=10" \
  -H "Accept: application/vnd.github.v3+json" \
  > /tmp/mcp_skills.json &

# Source 7: awesome-mcp-servers (punkpeye — 87k stars, updated daily)
curl -s "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md" \
  | grep -i "${QUERY}" | head -20 > /tmp/mcp_awesome.txt &

wait  # all fetches complete in parallel
```

Then parse all results:

```python
import json, re, sys

results = []

# --- glama.ai ---
try:
    data = json.load(open('/tmp/mcp_glama.json'))
    for s in data.get('servers', []):
        results.append({
            'name': s.get('name', ''),
            'description': s.get('description', ''),
            'repo': s.get('repository', {}).get('url', ''),
            'url': s.get('url', ''),
            'tools': [t.get('name','') for t in s.get('tools', [])[:5]],
            'license': s.get('spdxLicense', {}).get('name', ''),
            'source': 'glama',
            'stars': 0
        })
except: pass

# --- smithery.ai ---
try:
    data = json.load(open('/tmp/mcp_smithery.json'))
    for s in data.get('servers', []):
        results.append({
            'name': s.get('displayName', s.get('qualifiedName', '')),
            'description': s.get('description', ''),
            'repo': '',
            'url': f"https://smithery.ai/server/{s.get('qualifiedName','')}",
            'tools': [],
            'license': '',
            'source': 'smithery',
            'stars': 0
        })
except: pass

# --- mcp-get.com ---
try:
    data = json.load(open('/tmp/mcp_get.json'))
    for p in data if isinstance(data, list) else []:
        results.append({
            'name': p.get('name', ''),
            'description': p.get('description', ''),
            'repo': p.get('sourceUrl', p.get('homepage', '')),
            'url': f"https://mcp-get.com/packages/{p.get('name','')}",
            'tools': [],
            'license': p.get('license', ''),
            'source': 'mcp-get',
            'stars': p.get('totalInstalls', 0),
            'runtime': p.get('runtime', '')
        })
except: pass

# --- npm ---
try:
    data = json.load(open('/tmp/mcp_npm.json'))
    for o in data.get('objects', []):
        p = o['package']
        results.append({
            'name': p['name'],
            'description': p.get('description', ''),
            'repo': p.get('links', {}).get('repository', ''),
            'url': p.get('links', {}).get('npm', ''),
            'tools': [],
            'license': '',
            'source': 'npm',
            'stars': o.get('downloads', {}).get('monthly', 0)
        })
except: pass

# --- github ---
try:
    data = json.load(open('/tmp/mcp_github.json'))
    for r in data.get('items', []):
        results.append({
            'name': r['name'],
            'description': r.get('description', ''),
            'repo': r['html_url'],
            'url': r['html_url'],
            'tools': [],
            'license': r.get('license', {}).get('spdx_id', '') if r.get('license') else '',
            'source': 'github',
            'stars': r['stargazers_count']
        })
except: pass

# Deduplicate by repo URL (keep highest-starred)
seen = {}
for r in results:
    key = r['repo'].rstrip('/').lower() if r['repo'] else r['name'].lower()
    if key not in seen or r['stars'] > seen[key]['stars']:
        seen[key] = r

# Sort: stars first, then source priority
priority = {'github': 3, 'glama': 2, 'smithery': 2, 'mcp-get': 1, 'npm': 1}
final = sorted(seen.values(), key=lambda x: (x['stars'] * 10 + priority.get(x['source'], 0)), reverse=True)

print(json.dumps(final[:20], indent=2))
```

---

## Step 3 — Detect install command

For each result, detect the install method:

```python
def get_install(item):
    repo = item.get('repo', '')
    name = item.get('name', '')
    runtime = item.get('runtime', '')
    
    # npm package
    if name.startswith('@') or 'npmjs.com' in repo or runtime == 'node':
        return f"npx -y {name}"
    
    # Python package on PyPI
    if runtime == 'python' or 'pypi' in repo:
        return f"uvx {name}"
    
    # GitHub repo - check for package.json or setup.py in name patterns
    if 'github.com' in repo:
        if any(x in name.lower() for x in ['node', 'ts', 'js']):
            return f"npx -y {name}  # or: git clone {repo}"
        return f"git clone {repo}  # check README for install steps"
    
    return f"See: {item.get('url', repo)}"
```

---

## Step 4 — Output format

```
🔍 MCP DISCOVERY — "<query>"
Sources: glama.ai (23k) + smithery + mcp-get + npm + GitHub  |  Fetched: <timestamp>
Found: <N> results after deduplication

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1  <name>  [★<stars>]  <source>
    <description — 1 sentence>
    Tools:    <tool1>, <tool2>, <tool3>
    Install:  <install command>
    Repo:     <github url>
    License:  <license>

#2  <name>  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALSO FOUND IN CLAUDE CODE SKILLS (SKILL.md):
  <repo/path>  — <description from SKILL.md if parseable>

FOUND IN AWESOME-MCP-SERVERS:
  <matching lines from awesome list>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADD TO CLAUDE CODE (claude_desktop_config.json / .claude/settings.json):
  Pick one from above, then:

  # Node / npx:
  "<name>": { "command": "npx", "args": ["-y", "<package>"] }

  # Python / uvx:
  "<name>": { "command": "uvx", "args": ["<package>"] }

  # GitHub clone:
  git clone <repo> && cd <name>
  # follow README install steps, then:
  "<name>": { "command": "node", "args": ["dist/index.js"] }
```

---

## Step 5 — Orbit agent recommendation (optional)

If the user is running Orbit agents, suggest which agent would use this MCP:

```
ORBIT AGENT FIT:
  Best used by: <agent name> (e.g. 07-Security, 05-UAT, 06-Performance)
  Add to: agents/<agent>.md → ## 🔌 MCP + Connectors table
  Key tier: Team / Admin (depending on whether it writes data)
```

---

## Guardrails

```
🚫 NEVER return hardcoded lists — always fetch live
🚫 NEVER hallucinate install commands — only output what the registry says
🚫 NEVER suggest paid/auth-required MCPs without labelling them clearly
✅ ALWAYS deduplicate across sources — same repo should appear once
✅ ALWAYS show the source (glama / smithery / npm / github) for each result
✅ ALWAYS include the fetch timestamp so results are auditable
✅ ALWAYS surface SKILL.md results separately — they're for Claude Code, not Claude Desktop
✅ If zero results: broaden the query and retry with synonyms
```

---

## Fallback — if APIs are unavailable

If all API calls fail (network issue, rate limit):

```
Fallback search (open these URLs in browser):
  glama.ai:    https://glama.ai/mcp/servers?q=<query>
  smithery:    https://smithery.ai/search?q=<query>
  npm:         https://www.npmjs.com/search?q=<query>+mcp
  GitHub:      https://github.com/search?q=<query>+mcp-server&type=repositories
  Awesome list: https://github.com/punkpeye/awesome-mcp-servers
  a2asearch:   npx -y a2asearch-mcp  (install once, search 4800+ servers locally)
```
