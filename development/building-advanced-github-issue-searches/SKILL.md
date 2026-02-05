---
name: Building Advanced GitHub Issue Searches
description: Builds and executes complex issue queries using GitHub's advanced search syntax with AND/OR boolean operators and nested queries up to 5 levels deep. Use when finding specific issue sets with complex criteria, searching across states/labels/assignees/dates/issue-types, building custom reports, or exporting results to CSV/JSON/markdown.
---

# GitHub Advanced Issue Search

Build and execute complex issue queries using GitHub's advanced search syntax with AND/OR operators and nested queries.

## What you should do

When invoked, help the user build and execute advanced issue searches by:

1. **Understanding the search request** - Determine what the user wants to find:
   - Specific issue states, labels, assignees, authors
   - Date ranges and time-based filters
   - Issue types, milestones, projects
   - Complex combinations with AND/OR logic
   - Nested queries with parentheses

2. **Build the query** - Construct the search using:
   - Boolean operators: AND, OR
   - Nested queries: up to 5 levels of parentheses
   - All available issue fields
   - Proper escaping and syntax

3. **Execute and format results** - Run the query and present results:
   - Via GraphQL API with `advanced_search: true`
   - Via REST API with `advanced_search` parameter
   - Via web UI search
   - Format output (table, JSON, CSV, markdown)

4. **Refine if needed** - Help iterate on queries to get desired results

## Advanced search syntax

### Boolean operators

**AND (implicit):**
```
is:issue state:open author:alice
# All conditions must match (AND is implicit with space)
```

**AND (explicit):**
```
is:issue AND state:open AND author:alice
# Same as above, but explicit
```

**OR:**
```
is:issue (label:bug OR label:security)
# Matches issues with bug OR security label
```

**Complex combinations:**
```
is:issue state:open (label:bug OR label:security) assignee:alice
# Open issues with (bug OR security) label AND assigned to alice
```

### Nested queries

**Up to 5 levels deep:**
```
is:issue state:open (
  (type:Bug OR type:Security) AND
  (assignee:alice OR assignee:bob)
)
```

**Real-world example:**
```
is:issue state:open (
  (label:P0 OR label:P1) AND
  (assignee:@me OR no:assignee) AND
  (milestone:"Q1 2025" OR no:milestone)
)
# High-priority issues that are either assigned to me or unassigned,
# in Q1 milestone or no milestone
```

## Available search qualifiers

### Basic filters
- `is:issue` - Issues only
- `is:pr` - Pull requests only
- `is:open` / `is:closed` - State
- `state:open` / `state:closed` - Alternative state syntax

### People
- `author:USERNAME` - Issue creator
- `assignee:USERNAME` - Assigned user
- `assignee:@me` - Assigned to you
- `mentions:USERNAME` - Mentioned user
- `commenter:USERNAME` - Commented on issue
- `involves:USERNAME` - Any involvement
- `no:assignee` - Unassigned

### Labels
- `label:bug` - Has bug label
- `-label:wontfix` - Does NOT have wontfix label
- `no:label` - No labels

### Milestones and projects
- `milestone:"v2.0"` - In milestone
- `milestone:v2.0` - Alternative (no quotes if no spaces)
- `no:milestone` - No milestone
- `project:BOARD_NAME` - In project

### Issue types (new in 2025)
- `type:Bug` - Bug type
- `type:Epic` - Epic type
- `type:Feature` - Feature type
- `type:Task` - Task type

### Dates
- `created:>2025-01-01` - Created after date
- `created:<2025-12-31` - Created before date
- `created:2025-01-01..2025-12-31` - Date range
- `updated:>2025-10-01` - Updated after date
- `closed:2025-10-01..2025-10-15` - Closed in range

### Text search
- `in:title` - Search in title only
- `in:body` - Search in body only
- `in:comments` - Search in comments
- `security in:title` - Title contains "security"

### Counts and limits
- `comments:>10` - More than 10 comments
- `comments:<5` - Fewer than 5 comments
- `comments:0` - No comments

### Repository and organization
- `repo:owner/name` - Specific repository
- `org:organization` - Organization
- `user:username` - User's repositories

## Execution methods

### Method 1: GraphQL API (recommended)

```bash
gh api graphql -f query='
query {
  search(
    query: "is:issue state:open (type:Bug OR type:Security) assignee:@me"
    type: ISSUE
    first: 100
  ) {
    issueCount
    edges {
      node {
        ... on Issue {
          number
          title
          state
          labels(first: 10) {
            nodes {
              name
            }
          }
          assignees(first: 5) {
            nodes {
              login
            }
          }
        }
      }
    }
  }
}'
```

**Note:** Advanced search is enabled by default in GraphQL search queries.

### Method 2: REST API

```bash
# Will become default on September 4, 2025
gh api "search/issues?q=is:issue+state:open+(type:Bug+OR+type:Security)" \
  --jq '.items[] | {number, title, state}'

# Explicit advanced search (before Sept 2025)
gh api "search/issues?q=is:issue+state:open+(type:Bug+OR+type:Security)&advanced_search=true" \
  --jq '.items[] | {number, title, state}'
```

**URL encoding:**
- Spaces → `+` or `%20`
- Parentheses → `(` and `)` (usually don't need encoding)
- Quotes → `%22`
- Colons → `:` (don't encode)

### Method 3: Web UI

```bash
# Open search in browser
gh issue list --web --search "is:issue state:open (type:Bug OR type:Security)"
```

## Query templates

### Template 1: My open high-priority work
```
is:issue state:open assignee:@me (label:P0 OR label:P1 OR label:critical)
```

### Template 2: Stale issues needing triage
```
is:issue state:open no:assignee no:milestone updated:<2025-09-01
```

### Template 3: Recent bugs and security issues
```
is:issue state:open (type:Bug OR type:Security) created:>2025-10-01
```

### Template 4: Release blockers
```
is:issue state:open (
  (label:blocker OR label:critical) AND
  (milestone:"v2.0" OR milestone:"v2.1")
)
```

### Template 5: Unassigned work ready to pick up
```
is:issue state:open label:ready no:assignee (
  label:good-first-issue OR label:help-wanted
)
```

### Template 6: Issues blocked or blocking others
```
is:issue state:open (has:blocked-issues OR has:blocking-issues)
```

### Template 7: Parent issues with incomplete sub-issues
```
is:issue state:open has:sub-issues -label:all-sub-issues-complete
```

### Template 8: Epic/Feature breakdown
```
is:issue (type:Epic OR type:Feature) (
  state:open OR
  (state:closed AND closed:>2025-10-01)
)
```

## Complete workflow examples

### Example 1: Find my work for the week

```bash
QUERY="is:issue state:open assignee:@me (
  (label:P0 OR label:P1) OR
  (milestone:\"Sprint 42\" AND -label:blocked)
)"

gh api graphql -f query='
query {
  search(query: "'"$QUERY"'", type: ISSUE, first: 50) {
    issueCount
    edges {
      node {
        ... on Issue {
          number
          title
          labels(first: 5) {
            nodes {
              name
            }
          }
        }
      }
    }
  }
}' --jq '.data.search |
  "Found \(.issueCount) issues:\n" +
  (.edges | map(.node | "  #\(.number): \(.title)") | join("\n"))'
```

### Example 2: Export stale issues to CSV

```bash
QUERY="is:issue state:open no:assignee updated:<2025-09-01"

gh api graphql -f query='
query {
  search(query: "'"$QUERY"'", type: ISSUE, first: 100) {
    edges {
      node {
        ... on Issue {
          number
          title
          createdAt
          updatedAt
          author {
            login
          }
        }
      }
    }
  }
}' --jq -r '
["Number","Title","Author","Created","Updated"],
(.data.search.edges[] | [
  .node.number,
  .node.title,
  .node.author.login,
  .node.createdAt,
  .node.updatedAt
]) | @csv' > stale-issues.csv

echo "✅ Exported to stale-issues.csv"
```

### Example 3: Count issues by type

```bash
for type in Bug Epic Feature Task; do
  COUNT=$(gh api "search/issues?q=is:issue+state:open+type:$type" \
    --jq '.total_count')
  echo "$type: $COUNT"
done
```

### Example 4: Interactive query builder

```bash
# Prompt user for filters
echo "Build your issue search:"
read -p "State (open/closed/all): " state
read -p "Labels (comma-separated, or empty): " labels
read -p "Assignee (username or @me, or empty): " assignee
read -p "Issue type (Bug/Epic/Feature/Task, or empty): " type

# Build query
QUERY="is:issue"
[[ "$state" != "all" ]] && QUERY="$QUERY state:$state"

if [[ -n "$labels" ]]; then
  IFS=',' read -ra LABEL_ARRAY <<< "$labels"
  LABEL_QUERY=$(printf "label:%s OR " "${LABEL_ARRAY[@]}")
  LABEL_QUERY=${LABEL_QUERY% OR }
  QUERY="$QUERY ($LABEL_QUERY)"
fi

[[ -n "$assignee" ]] && QUERY="$QUERY assignee:$assignee"
[[ -n "$type" ]] && QUERY="$QUERY type:$type"

echo "Query: $QUERY"
echo ""

# Execute
gh api "search/issues?q=$(echo "$QUERY" | sed 's/ /+/g')" \
  --jq '.items[] | "#\(.number): \(.title)"'
```

### Example 5: Save common searches

```bash
# Create search library
mkdir -p ~/.gh-searches

cat > ~/.gh-searches/my-work.sh <<'EOF'
#!/bin/bash
gh api graphql -f query='
query {
  search(
    query: "is:issue state:open assignee:@me (label:P0 OR label:P1)"
    type: ISSUE
    first: 50
  ) {
    edges {
      node {
        ... on Issue {
          number
          title
        }
      }
    }
  }
}' --jq '.data.search.edges[] | "#\(.node.number): \(.node.title)"'
EOF

chmod +x ~/.gh-searches/my-work.sh

# Use saved search
~/.gh-searches/my-work.sh
```

## Output formatting

### Table format

```bash
gh api graphql -f query='...' --jq -r '
["Number","Title","State","Labels"],
["------","-----","-----","------"],
(.data.search.edges[] | [
  .node.number,
  .node.title,
  .node.state,
  (.node.labels.nodes | map(.name) | join(", "))
]) | @tsv' | column -t -s $'\t'
```

### JSON export

```bash
gh api graphql -f query='...' --jq '.data.search.edges[] | .node' > results.json
```

### Markdown checklist

```bash
gh api graphql -f query='...' --jq -r '
.data.search.edges[] |
"- [ ] #\(.node.number): \(.node.title)"
' > checklist.md
```

## Important notes

### Limitations

1. **Repo/org/user fields** - Currently work as OR filters when space-separated (not AND)
2. **Not in nested queries** - repo, org, user cannot be used in nested parentheses yet
3. **Default date** - Sept 4, 2025: Advanced search becomes default (no parameter needed)
4. **Rate limits** - Search API has lower rate limits than other endpoints

### Performance tips

- Use specific qualifiers to narrow results (repo, milestone, etc.)
- Limit results with `first: N` in GraphQL
- Cache common query results
- Use pagination for large result sets

## Error handling

**Common issues:**

1. **"Syntax error in query"**
   - Check parentheses are balanced
   - Verify operator spelling (AND, OR in caps)
   - Check for invalid qualifiers

2. **"Too many parentheses"**
   - Max 5 levels of nesting
   - Simplify query or break into multiple searches

3. **"Invalid qualifier"**
   - Ensure qualifier is supported (check docs)
   - Some fields only work outside nested queries

4. **"Rate limit exceeded"**
   - Search API has stricter limits
   - Add delays between requests
   - Use authentication to increase limits

## Integration with workflows

**Works well with:**
- `gh-issue-hierarchy` skill - Find parent issues with sub-issues
- `gh-issue-dependencies` skill - Search for blocked/blocking issues
- `gh-issue-types` skill - Filter by issue types
- `gh-project-manage` skill - Find issues to add to projects

**Automation ideas:**
- Daily digest of priority work
- Stale issue cleanup scripts
- Release blocker reports
- Team workload analysis
- Automated triage based on search results

## Example usage patterns

### Common project searches

**High-value work to prioritize:**
```
is:issue state:open label:essential (label:enhancement OR label:bug)
```

**Blocked work needing attention:**
```
is:issue state:open has:blocked-issues
```

**Ready to work (unassigned and ready):**
```
is:issue state:open no:assignee label:ready
```

**Stale backlog items:**
```
is:issue state:open label:backlog updated:<2025-09-01
```

**Recently completed work:**
```
is:issue state:closed closed:>2025-10-01 (label:config OR label:pipeline)
```