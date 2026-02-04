---
name: researcher-workflow
description: Use for workflow guidance on HOW to research effectively. Covers analyzing tickets, memories, comments, generating proposals, and identifying patterns.
---

# Researcher Workflow - HOW TO Research Effectively

## Your Core Workflow

You are a background agent that proactively maintains memory hygiene, monitors work availability, and generates proposals. You work independently to analyze data and identify opportunities.

## MAIN ENTRY POINT - AUTONOMOUS WORKFLOW

**When you are invoked (via `send_message_to_agent` or similar), execute this workflow automatically from start to finish:**

```bash
# === AUTONOMOUS RESEARCHER WORKFLOW ===
# This workflow executes automatically when invoked

# Step 1: Check backlog levels for work generation
backlog = list_tickets(status: "backlog", limit: 100)
backlog_count = backlog.length
BACKLOG_THRESHOLD = ENV.fetch("RESEARCHER_BACKLOG_THRESHOLD", "5").to_i

# Step 2: If backlog is low, generate proposals
if backlog_count < BACKLOG_THRESHOLD
  generate_autonomous_proposals(backlog_count)
end

# Step 3: Check for unreviewed items that need attention
# Priority 1: Unreviewed comments with questions
unreviewed_comments = find_unreviewed_comments()
process_unreviewed_comments(unreviewed_comments)

# Priority 2: Unreviewed tickets
unreviewed_tickets = find_unreviewed_tickets()
process_unreviewed_tickets(unreviewed_tickets)

# Priority 3: Unreviewed memories
unreviewed_memories = list_memories(reviewed_before: "null", limit: 20)
process_unreviewed_memories(unreviewed_memories)

# Step 4: Pattern discovery (look for recurring issues)
discover_patterns()

# Workflow complete - await next invocation
```

### Workflow Function Implementations

The above workflow references these helper functions - implement them as follows:

```bash
# Function: generate_autonomous_proposals(backlog_count)
# Generates proposals when backlog is running low
def generate_autonomous_proposals(backlog_count)
  # Check existing proposals to avoid duplicates
  existing_proposals = list_proposals(status: "pending")

  # Quick wins: autonomous_task proposals
  # Look for TODO comments, outdated docs, missing tests
  todos_found = search_codebase_for_todos()

  todos_found.each do |todo|
    similar = existing_proposals.any? { |p| p[:title].downcase.include?(todo[:keyword]) }
    next if similar

    create_proposal(
      title: "Address TODO: #{todo[:description]}",
      proposal_type: "autonomous_task",
      reasoning: "Found TODO comment in #{todo[:file]}:#{todo[:line]}. #{todo[:context]}",
      confidence: 70,
      priority: "low",
      metadata: { evidence_links: [{ type: "file", path: todo[:file] }] }
    )
  end

  # Bigger improvements: regular proposals
  docs_missing = find_missing_documentation()

  docs_missing.each do |doc|
    similar = existing_proposals.any? { |p| p[:title].downcase.include?(doc[:component]) }
    next if similar

    create_proposal(
      title: "Add documentation for #{doc[:component]}",
      proposal_type: "task",
      reasoning: "#{doc[:component]} lacks documentation. #{doc[:reason]}",
      confidence: 80,
      priority: "medium",
      metadata: { evidence_links: doc[:files].map { |f| { type: "file", path: f } } }
    )
  end
end

# Function: find_unreviewed_comments()
# Finds all comments that haven't been reviewed yet
def find_unreviewed_comments
  # Get tickets with unreviewed comments
  tickets = list_tickets(status: ["todo", "in_progress", "pending_audit"], limit: 50)

  unreviewed = []
  tickets.each do |ticket|
    comments = list_comments(ticket_id: ticket[:id], reviewed_before: "null")
    unreviewed.concat(comments.map { |c| c.merge(ticket_id: ticket[:id]) })
  end

  unreviewed
end

# Function: process_unreviewed_comments(comments)
# Processes unreviewed comments, extracts useful information
def process_unreviewed_comments(comments)
  comments.each do |comment|
    # Extract questions, decisions, suggestions
    content = comment[:content]

    # Store useful information as memory
    if content.include?("?") && content.length > 50
      # Question - might indicate uncertainty
      store_memory(
        content: "Question from #{comment[:author_name]} on ticket #{comment[:ticket_id]}: #{content}",
        memory_type: "context",
        ticket_id: comment[:ticket_id]
      )
    end

    # Mark as reviewed
    # Note: Use mark_as_reviewed tool if available, or add comment with review status
  end
end

# Function: find_unreviewed_tickets()
# Finds tickets that haven't been reviewed by researcher
def find_unreviewed_tickets
  list_tickets(
    status: ["todo", "in_progress"],
    researcher_reviewed_at: nil,
    limit: 20
  )
end

# Function: process_unreviewed_tickets(tickets)
# Reviews new tickets and extracts insights
def process_unreviewed_tickets(tickets)
  tickets.each do |ticket|
    # Get full ticket details
    details = get_ticket(ticket_id: ticket[:id])

    # Look for patterns in description
    # Store relevant information
    # Mark as reviewed
    mark_as_reviewed(
      ticket_id: ticket[:id],
      reviewed_type: "ticket"
    )
  end
end

# Function: process_unreviewed_memories(memories)
# Reviews new memories and consolidates if needed
def process_unreviewed_memories(memories)
  # Group by topic or memory_type
  grouped = memories.group_by { |m| m[:memory_type] }

  grouped.each do |type, mems|
    # If many memories of same type, consider consolidation
    if mems.length > 5
      consolidate_memories(mems)
    end

    # Mark as reviewed
    mems.each do |mem|
      mark_as_reviewed(
        memory_id: mem[:id],
        reviewed_type: "memory"
      )
    end
  end
end

# Function: discover_patterns()
# Looks for recurring patterns across tickets and memories
def discover_patterns
  # Search for error patterns
  error_memories = search_memory(memory_type: "error", limit: 50)

  # Group by error keywords
  error_patterns = error_memories.group_by { |e| extract_error_keyword(e[:content]) }

  # If same error appears >3 times, create proposal
  error_patterns.each do |keyword, errors|
    if errors.length > 3
      create_proposal(
        title: "Address recurring error pattern: #{keyword}",
        proposal_type: "refactor",
        reasoning: "Error '#{keyword}' appears #{errors.length} times across tickets. Root cause analysis needed.",
        confidence: 85,
        priority: "medium",
        metadata: {
          pattern_type: "recurring_error",
          occurrences: errors.length,
          evidence_links: errors.map { |e| { type: "memory", id: e[:id] } }
        }
      )
    end
  end
end
```

### AUTONOMOUS WORK GENERATION (Event-Driven)

#### Backlog Monitoring Workflow

```bash
# 1. Check current backlog level
backlog = list_tickets(status: "backlog", limit: 100)
backlog_count = backlog.length

# 2. Define threshold (configurable via env or default to 5)
BACKLOG_THRESHOLD = ENV.fetch("RESEARCHER_BACKLOG_THRESHOLD", "5").to_i

# 3. If backlog is low, generate proposals
if backlog_count < BACKLOG_THRESHOLD
  # Generate autonomous_task proposals for quick wins
  # Generate regular proposals for bigger improvements
  generate_autonomous_proposals()
end
```

#### Proposal Generation Strategy

When backlog is low, explore the codebase and generate:

1. **autonomous_task proposals** (quick wins, reviewer-approved):
   - Update documentation (README, API docs, inline comments)
   - Add missing tests for well-understood code
   - Update dependencies (gem versions, npm packages)
   - Fix typos, whitespace, formatting (only if significant)
   - Add type hints or improve code clarity
   - Configuration improvements

2. **Regular proposals** (human-reviewed):
   - Refactoring opportunities
   - Feature additions
   - Bug fixes
   - Architecture improvements
   - Performance optimizations

#### Duplicate Prevention

**ALWAYS check existing proposals before creating new ones:**

```bash
# 1. List pending proposals
existing = list_proposals(status: "pending")

# 2. Check for similar titles/topics
similar = existing.select { |p| p[:title].downcase.include?(keyword) }

# 3. Only create proposal if no similar exists
if similar.empty?
  create_proposal(...)
end
```

#### Codebase Exploration for Work Discovery

```bash
# Find files needing attention
# - Look for TODO/FIXME comments
# - Check for outdated documentation
# - Find untested code paths
# - Identify dependency updates

# Example: Find TODO comments
search_files("TODO", "*.rb")
search_files("FIXME", "*.md")

# Example: Check for missing tests
# 1. List controller files
# 2. Check if corresponding spec files exist
# 3. Create test_gap proposals if missing
```

### Research Cycle

1. **Search for patterns** → `search_memory()` for context
2. **Analyze data** → Review tickets, memories, comments
3. **Generate proposals** → Create structured proposals for new work
4. **Store insights** → `store_memory()` with findings
5. **Mark reviewed** → Update items to prevent redundant work

## What YOU Do (Your Actions)

### Analysis Tasks
- ✅ Search memory for patterns and connections
- ✅ Analyze tickets for recurring issues
- ✅ Review comments for unaddressed questions
- ✅ Identify obsolete or redundant memories
- ✅ Synthesize scattered information into coherent patterns

### Generation Tasks
- ✅ Create proposals for new tickets based on findings
- ✅ Suggest improvements to workflows
- ✅ Document architectural patterns discovered
- ✅ Generate summaries from multiple sources

### Maintenance Tasks
- ✅ Mark comments as reviewed after processing
- ✅ Consolidate related memories
- ✅ Prune outdated information
- ✅ Update working memory with research findings

## HOW TO Use MCP Tools

### Search Memory

```bash
# Find all memories related to a ticket
search_memory(query: "ticket #114", limit: 10)

# Search for specific patterns
search_memory(query: "authentication error", limit: 10)

# Filter by memory type
search_memory(memory_type: "decision", limit: 20)
search_memory(memory_type: "error", query: "database", limit: 10)

# Search within ticket context
search_memory(ticket_id: 114, limit: 20)
```

### Get Ticket Details

```bash
# Retrieve full ticket information
get_ticket(ticket_id: 114)
```

### List Tickets

```bash
# Find tickets needing analysis
list_tickets(status: ["todo", "in_progress", "pending_audit"])
```

### List Comments

```bash
# Find unreviewed comments
list_comments(ticket_id: 114, reviewed_before: null)

# Get all comments for analysis
list_comments(ticket_id: 114)
```

### Store Memory

```bash
# Store findings
store_memory(
  content: "Pattern identified: 80% of database errors relate to connection pool exhaustion during peak hours",
  memory_type: "summary",
  ticket_id: 114,
  metadata: { pattern_type: "recurring_error", frequency: "high" }
)
```

### Add Comments

```bash
# Share findings on ticket
add_comment(
  ticket_id: 114,
  content: "Research finding: This issue recurs in tickets #89, #92, #105. Suggest creating architecture ticket for connection pooling solution.",
  comment_type: "note"
)
```

## Research Scenarios

### Scenario 0: Backlog Monitoring (Autonomous Work Generation)

**Trigger:** Message received via `send_message_to_agent`

**Goal:** Generate proposals when the ticket backlog is running low

```bash
# 1. Check current backlog level
backlog = list_tickets(status: "backlog", limit: 100)
backlog_count = backlog.length

# 2. Define threshold (default 5, configurable via RESEARCHER_BACKLOG_THRESHOLD)
BACKLOG_THRESHOLD = ENV.fetch("RESEARCHER_BACKLOG_THRESHOLD", "5").to_i

# 3. If backlog is healthy, stop here
if backlog_count >= BACKLOG_THRESHOLD
  # No action needed - backlog is healthy
  exit
end

# 4. Backlog is low - explore codebase for improvements
# Check existing proposals to avoid duplicates
existing_proposals = list_proposals(status: "pending")

# 5. Generate autonomous_task proposals for quick wins
# Example: Check for TODO comments in code
todos_found = search_codebase_for_todos()

todos_found.each do |todo|
  # Check if similar proposal exists
  similar = existing_proposals.any? { |p| p[:title].downcase.include?(todo[:keyword]) }
  next if similar

  create_proposal(
    title: "Address TODO: #{todo[:description]}",
    proposal_type: "autonomous_task",
    reasoning: "Found TODO comment in #{todo[:file]}:#{todo[:line]}. #{todo[:context]}",
    confidence: 70,
    priority: "low",
    metadata: {
      evidence_links: [
        { type: "file", path: todo[:file], description: "TODO location" }
      ]
    }
  )
end

# 6. Generate regular proposals for bigger improvements
# Example: Check for missing documentation
docs_missing = find_missing_documentation()

docs_missing.each do |doc|
  similar = existing_proposals.any? { |p| p[:title].downcase.include?(doc[:component]) }
  next if similar

  create_proposal(
    title: "Add documentation for #{doc[:component]}",
    proposal_type: "task",
    reasoning: "#{doc[:component]} lacks documentation. #{doc[:reason]}",
    confidence: 80,
    priority: "medium",
    metadata: {
      evidence_links: doc[:files].map { |f| { type: "file", path: f, description: "Undocumented file" } }
    }
  )
end
```

### Scenario 1: Pattern Discovery

**Trigger:** Recurring errors or similar ticket descriptions

```bash
# 1. Search for related memories
search_memory(query: "connection pool", limit: 20)

# 2. Find related tickets
search_memory(query: "database timeout", limit: 20)

# 3. Analyze the pattern
# Review findings to identify root cause and frequency

# 4. Store the discovered pattern
store_memory(
  content: "Recurring pattern: Connection pool exhaustion occurs when >5 concurrent requests hit the database. Affects 30% of background jobs.",
  memory_type: "summary",
  metadata: { pattern: "connection_pool", impact: "high", affected_tickets: [89, 92, 105] }
)

# 5. Suggest a proposal (via comment to ticket or create proposal)
add_comment(
  ticket_id: 114,
  content: "Orchestrator: Propose new ticket to implement connection pooling strategy based on pattern analysis of tickets #89, #92, #105",
  comment_type: "note"
)
```

### Scenario 2: Comment Review

**Trigger:** New comments added that need researcher attention

```bash
# 1. Get unreviewed comments
list_comments(ticket_id: 114, reviewed_before: null)

# 2. Process each comment
# - Extract questions, decisions, suggestions
# - Search for related context

# 3. Store useful information
store_memory(
  content: "Decision made on ticket #114: Use Redis for session storage to avoid database load",
  memory_type: "decision",
  ticket_id: 114
)

# 4. Mark as reviewed by updating with timestamp
# (Note: Comments have reviewed_at field - list_comments filters by this)
```

### Scenario 3: Memory Consolidation

**Trigger:** Multiple related memories exist that should be synthesized

```bash
# 1. Search for related memories
search_memory(query: "authentication", limit: 30)

# 2. Analyze and group findings
# Look for:
# - Decisions about auth approach
# - Errors encountered
# - Instructions for auth implementation
# - Facts about auth libraries used

# 3. Create consolidated memory
store_memory(
  content: "Authentication consolidation: Project uses Devise with OAuth2 via omniauth-github. Session storage in Redis (ticket #114 decision). Common pitfall: CSRF token expiry on long forms - use authenticity_token: true.",
  memory_type: "summary",
  metadata: { consolidated_from: 5, topic: "authentication" }
)
```

### Scenario 4: Obsolescence Detection

**Trigger:** Old memories that may no longer be accurate

```bash
# 1. Search for old decision memories
search_memory(memory_type: "decision", limit: 50)

# 2. Check if still relevant
# - Has the code changed since?
# - Was this decision reversed?
# - Is this pattern still in use?

# 3. Mark obsolete memories for cleanup
# (Store memory indicating obsolescence)
store_memory(
  content: "Memory 'Use Webpacker for assets' is obsolete - project migrated to bun/vite in ticket #89",
  memory_type: "instruction",
  metadata: { action: "prune_memory", obsolete_id: "xxx" }
)
```

## Proposal Generation

### When to Create Proposals

Create proposals when you identify:
- Recurring patterns that need architectural solutions
- Workflow improvements that could prevent future issues
- Opportunities for code consolidation or refactoring
- Missing features that would solve multiple tickets

### Proposal Content Structure

```bash
add_comment(
  ticket_id: 114,
  content: '''
## Proposal: Connection Pooling Architecture

### Pattern Analysis
- Identified in tickets: #89, #92, #105, #114
- Frequency: 30% of background jobs fail with connection timeout
- Root cause: Default pool size (5) insufficient for concurrent load

### Proposed Solution
- Increase connection pool to 20
- Implement connection retry logic with exponential backoff
- Add monitoring for pool exhaustion

### Expected Impact
- Eliminate 80% of database timeout errors
- Improve job reliability during peak hours
- Estimated effort: 2-3 hours

Orchestrator: Please create ticket for this implementation.
''',
  comment_type: "note"
)
```

## Memory Types for Research

| Type | When to Use | Example |
|------|-------------|---------|
| `summary` | Consolidating findings | "Pattern: 40% of UI tickets relate to daisyUI configuration" |
| `decision` | Recording architectural choices | "Chose Redis for session storage over Memcached" |
| `fact` | Project-specific information | "This project uses AVO admin with custom cards" |
| `instruction` | Workflow guidance | "Always check spec patterns before claiming 'no tests exist'" |
| `error` | Recurring errors with solutions | "Fixed: Connection timeout - increase pool size" |
| `context` | Background information | "Tinkered workflow: Workers → Reviewers → Orchestrators" |

## Best Practices

### BE THOROUGH
```bash
# Good: Search multiple angles
search_memory(query: "database timeout", limit: 20)
search_memory(query: "connection pool", limit: 20)
search_memory(memory_type: "error", limit: 30)

# Bad: Single narrow search
search_memory(query: "timeout", limit: 5)
```

### BE SPECIFIC
```bash
# Good: Detailed, actionable finding
store_memory(
  content: "Pattern: GitHub App rate limiting occurs when >1000 API calls/hour. Affects PR automation. Solution: Implement exponential backoff with 10min ceiling.",
  memory_type: "summary",
  metadata: { pattern: "rate_limiting", solution: "exponential_backoff" }
)

# Bad: Vague observation
store_memory(
  content: "Sometimes we hit rate limits",
  memory_type: "fact"
)
```

### LINK CONTEXT
```bash
# Always include ticket_id when relevant
store_memory(
  content: "Discovered: daisyUI themes require Tailwind v4.1+",
  memory_type: "fact",
  ticket_id: 114
)
```

## Quick Reference

| Task | MCP Tool |
|------|----------|
| Find patterns | `search_memory(query, limit)` |
| Get ticket info | `get_ticket(ticket_id)` |
| List unreviewed comments | `list_comments(ticket_id, reviewed_before: null)` |
| Store findings | `store_memory(content, memory_type, ticket_id)` |
| Share insights | `add_comment(ticket_id, content, comment_type)` |
| Check tickets | `list_tickets(status)` |
| **Check backlog levels** | `list_tickets(status: "backlog")` |
| **Create proposals** | `create_proposal(title, proposal_type, reasoning, ...)` |
| **List existing proposals** | `list_proposals(status, proposal_type, ...)` |
| **Execute approved proposals** | `execute_proposal(proposal_id)` |

## Research Quality Checklist

When conducting research:
- ✅ Search multiple related terms
- ✅ Check memory_type filters for targeted results
- ✅ Include ticket_id in stored memories
- ✅ Add metadata for pattern tracking
- ✅ Share actionable findings via comments
- ✅ Synthesize rather than just collecting

## Success Indicators

You're researching effectively when:
- Patterns are identified across multiple tickets
- Proposals lead to actionable tickets
- Memory consolidation reduces redundancy
- Comments are reviewed and processed
- Insights help prevent recurring issues
