---
name: managing-chef
description: |
  Use when working with Chef — chef infrastructure automation and configuration
  management. Covers cookbook management, node configuration, compliance
  profiles, data bag management, role/environment administration, and Chef
  InSpec auditing. Use when managing Chef infrastructure, debugging convergence
  failures, inspecting node run lists, or auditing compliance.
connection_type: chef
preload: false
---

# Chef Management Skill

Manage and inspect Chef cookbooks, nodes, roles, environments, and compliance profiles.

## MANDATORY: Discovery-First Pattern

**Always check node status and server connectivity before modifying configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Chef Versions ==="
chef-client --version 2>/dev/null
knife --version 2>/dev/null

echo ""
echo "=== Chef Server Status ==="
knife status 2>/dev/null | head -15 || \
echo "Chef Server not configured or not reachable"

echo ""
echo "=== Node Summary ==="
knife node list 2>/dev/null | wc -l | xargs -I{} echo "{} nodes registered"

echo ""
echo "=== Environments ==="
knife environment list 2>/dev/null

echo ""
echo "=== Cookbooks ==="
knife cookbook list 2>/dev/null | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

# Knife wrapper with JSON output
knife_cmd() {
    knife "$@" --format json 2>/dev/null
}

# Chef Server API call
chef_api() {
    local endpoint="$1"
    knife raw "$endpoint" 2>/dev/null
}

# Node search
chef_search() {
    local query="$1"
    knife search node "$query" --format json 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--format json` with jq for structured output
- Use `knife search` for querying nodes by attributes
- Never dump full node objects -- extract run lists and key attributes

## Common Operations

### Node Inspection

```bash
#!/bin/bash
NODE="${1:-}"

if [ -n "$NODE" ]; then
    echo "=== Node Details: $NODE ==="
    knife node show "$NODE" --format json 2>/dev/null | jq '{
        name: .name,
        environment: .chef_environment,
        run_list: .run_list,
        platform: .automatic.platform,
        platform_version: .automatic.platform_version,
        ip: .automatic.ipaddress,
        fqdn: .automatic.fqdn,
        uptime: .automatic.uptime,
        last_run: .automatic.ohai_time
    }'
else
    echo "=== All Nodes ==="
    knife status --format json 2>/dev/null | jq -r '
        .[] | "\(.name)\t\(.environment)\t\(.ipaddress)\t\(.run_list | join(","))"
    ' | column -t | head -25
fi
```

### Cookbook Management

```bash
#!/bin/bash
echo "=== Server Cookbooks ==="
knife cookbook list 2>/dev/null

echo ""
COOKBOOK="${1:-}"
if [ -n "$COOKBOOK" ]; then
    echo "=== Cookbook Details: $COOKBOOK ==="
    knife cookbook show "$COOKBOOK" 2>/dev/null | head -20

    echo ""
    echo "=== Cookbook Dependencies ==="
    knife cookbook show "$COOKBOOK" --format json 2>/dev/null | jq '.metadata.dependencies'

    echo ""
    echo "=== Recipe List ==="
    knife cookbook show "$COOKBOOK" --format json 2>/dev/null | jq '.metadata.providing | keys'
fi
```

### Role and Environment Management

```bash
#!/bin/bash
echo "=== Roles ==="
knife role list 2>/dev/null

echo ""
ROLE="${1:-}"
if [ -n "$ROLE" ]; then
    echo "=== Role Details: $ROLE ==="
    knife role show "$ROLE" --format json 2>/dev/null | jq '{
        name: .name,
        run_list: .run_list,
        default_attributes: (.default_attributes | keys),
        override_attributes: (.override_attributes | keys)
    }'
fi

echo ""
echo "=== Environments ==="
knife environment list 2>/dev/null
ENV="${2:-}"
if [ -n "$ENV" ]; then
    echo "=== Environment: $ENV ==="
    knife environment show "$ENV" --format json 2>/dev/null | jq '{
        name: .name,
        cookbook_versions: .cookbook_versions,
        default_attributes: (.default_attributes | keys)
    }'
fi
```

### Compliance and InSpec Profiles

```bash
#!/bin/bash
echo "=== InSpec Version ==="
inspec version 2>/dev/null

echo ""
echo "=== Available Profiles ==="
inspec supermarket profiles --format json 2>/dev/null | jq '.[0:10]' || \
ls compliance/profiles/ 2>/dev/null

echo ""
PROFILE="${1:-}"
if [ -n "$PROFILE" ]; then
    echo "=== Profile Execution ==="
    inspec exec "$PROFILE" --reporter json 2>/dev/null | jq '{
        version: .version,
        statistics: .statistics,
        controls: [.profiles[].controls[] | {
            id: .id,
            title: .title,
            status: .results[0].status
        }] | .[0:10]
    }'
fi
```

### Data Bag Management

```bash
#!/bin/bash
echo "=== Data Bags ==="
knife data bag list 2>/dev/null

echo ""
BAG="${1:-}"
if [ -n "$BAG" ]; then
    echo "=== Items in $BAG ==="
    knife data bag show "$BAG" 2>/dev/null

    ITEM="${2:-}"
    if [ -n "$ITEM" ]; then
        echo ""
        echo "=== Item: $BAG/$ITEM ==="
        knife data bag show "$BAG" "$ITEM" --format json 2>/dev/null | jq 'del(.id)' | head -30
    fi
fi
```

## Safety Rules

- **NEVER upload cookbooks to production without testing** -- use Test Kitchen or ChefSpec first
- **Use environment cookbook version constraints** to prevent untested versions in production
- **Data bag secrets must be distributed securely** -- never commit encryption keys to source control
- **Node run list changes take effect on next chef-client run** -- be aware of convergence timing
- **Force-removing nodes** orphans their client keys -- clean up both node and client objects

## Output Format

Present results as a structured report:
```
Managing Chef Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Attribute precedence**: Chef has 15 levels of attribute precedence -- `override` beats `default` beats `automatic`
- **Cookbook dependency conflicts**: Version constraints across cookbooks can create unsolvable dependency graphs
- **Chef client interval**: Nodes converge periodically (default 30min) -- changes are not instant
- **Search index lag**: Chef Server search index updates asynchronously -- recently added nodes may not appear immediately
- **Encrypted data bags**: Require the shared secret on every node -- key rotation requires re-encrypting all items
- **Recipe ordering**: Recipes in run list execute in order -- resource conflicts between recipes are common
- **Berkshelf vs Policyfile**: Two dependency management approaches -- mixing them causes confusion
- **Test Kitchen overhead**: Each test creates a full VM -- can be slow and resource-intensive
