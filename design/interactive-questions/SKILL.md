---
name: interactive-questions
description: Ask clarifying questions using AskUserQuestion tool when requirements are unclear to prevent assumptions and misunderstandings. Use when facing ambiguous requirements, missing information, or trade-off decisions before implementation.
---

# Interactive Questions with AskUserQuestion Tool

## Instructions

### When to ask

**Always ask when:**
- Requirements unclear
- Missing critical information
- Multiple interpretations possible
- Trade-offs need decision
- Configuration or setup choices needed
- User needs to select from multiple options

**Never assume - Always ask!**

### Question Framework Using AskUserQuestion

The AskUserQuestion tool provides a structured way to ask questions with clear options.

#### Tool Structure

```javascript
AskUserQuestion({
  questions: [
    {
      question: "Clear question text?",
      header: "Short label (max 12 chars)",
      multiSelect: false,  // true if multiple selections allowed
      options: [
        {
          label: "Option 1",
          description: "What this option means and its implications"
        },
        {
          label: "Option 2",
          description: "Another choice with trade-offs"
        }
      ]
    }
  ]
})
```

#### Best Practices

1. **Keep headers short** (max 12 characters) - e.g., "Auth method", "Test type"
2. **Clear questions** - End with "?" and be specific
3. **Provide 2-4 options** - Not too few, not too many
4. **Descriptive labels** - Concise (1-5 words)
5. **Explain trade-offs** - Each option's pros/cons
6. **Use multiSelect** - When choices aren't mutually exclusive
7. **"Other" is automatic** - Don't add it, users can always provide custom input

### Question Framework Steps

1. **Identify the gap** - What information is missing?
2. **Formulate specific question** - Make it clear and unambiguous
3. **Provide context** - Why does this matter?
4. **Offer options** - Use AskUserQuestion with 2-4 choices
5. **Explain implications** - What each option means

## Example

**Request:** "Add validation to {{ENTITIES}}"

### ❌ Don't Assume
```
"Implementing {{field1}} and {{field2}} validation with min/max rules..."
```

### ✅ Use AskUserQuestion

```javascript
AskUserQuestion({
  questions: [
    {
      question: "Which fields need validation?",
      header: "Fields",
      multiSelect: true,  // User can select multiple fields
      options: [
        {
          label: "{{field1}}",
          description: "Primary identifier field"
        },
        {
          label: "{{field2}}",
          description: "Numeric value field"
        },
        {
          label: "{{field3}}",
          description: "Status field"
        }
      ]
    },
    {
      question: "What validation rules for {{field1}}?",
      header: "{{field1}} Rule",
      multiSelect: false,
      options: [
        {
          label: "Range check",
          description: "Validate min/max values (strict bounds)"
        },
        {
          label: "Format check",
          description: "Validate format/pattern only"
        },
        {
          label: "Both",
          description: "Range and format validation"
        }
      ]
    },
    {
      question: "How should validation failures be handled?",
      header: "Error Handle",
      multiSelect: false,
      options: [
        {
          label: "Exception",
          description: "Throw exception immediately (fail fast)"
        },
        {
          label: "Error object",
          description: "Return error object (allow recovery)"
        },
        {
          label: "Collect all",
          description: "Validate all fields, return all errors"
        }
      ]
    }
  ]
})
```

## Common Scenarios

### Scenario 1: Feature Scope Ambiguity

**Request:** "Add authentication"

**Using AskUserQuestion:**

```javascript
AskUserQuestion({
  questions: [
    {
      question: "Which authentication method should be implemented?",
      header: "Auth Method",
      multiSelect: false,
      options: [
        {
          label: "JWT tokens",
          description: "Stateless, scalable, good for APIs (recommended for microservices)"
        },
        {
          label: "Session-based",
          description: "Traditional, stateful, server-side sessions (simpler for monoliths)"
        },
        {
          label: "OAuth2",
          description: "Third-party auth (Google, GitHub, etc.), more complex setup"
        },
        {
          label: "API keys",
          description: "Simple, for service-to-service auth only"
        }
      ]
    },
    {
      question: "What should be protected by authentication?",
      header: "Protection",
      multiSelect: true,  // Can protect multiple areas
      options: [
        {
          label: "All endpoints",
          description: "Everything requires auth (most secure, may impact public APIs)"
        },
        {
          label: "User resources",
          description: "Only user-specific data (balance security and accessibility)"
        },
        {
          label: "Admin only",
          description: "Administrative routes only (least restrictive)"
        }
      ]
    },
    {
      question: "Where should credentials be stored?",
      header: "Storage",
      multiSelect: false,
      options: [
        {
          label: "Database",
          description: "Full control, your infrastructure (requires secure hashing)"
        },
        {
          label: "External (Auth0)",
          description: "Managed service, easier but external dependency"
        },
        {
          label: "In-memory cache",
          description: "Fast but lost on restart (dev/testing only)"
        }
      ]
    }
  ]
})
```

### Scenario 2: Technical Implementation Choices

**Request:** "Improve performance"

**Using AskUserQuestion:**

```javascript
AskUserQuestion({
  questions: [
    {
      question: "What is the primary performance target?",
      header: "Target",
      multiSelect: false,
      options: [
        {
          label: "Response time",
          description: "Reduce latency, faster user experience (< 200ms target)"
        },
        {
          label: "Throughput",
          description: "Handle more concurrent requests (> 1000 req/s)"
        },
        {
          label: "Memory usage",
          description: "Reduce RAM consumption (< 512MB target)"
        },
        {
          label: "All of above",
          description: "Comprehensive optimization (most effort required)"
        }
      ]
    },
    {
      question: "Which operations are currently slow?",
      header: "Bottleneck",
      multiSelect: true,
      options: [
        {
          label: "Database queries",
          description: "Slow SQL, N+1 problems, missing indexes"
        },
        {
          label: "API calls",
          description: "External service latency, no caching"
        },
        {
          label: "File processing",
          description: "Large file I/O, inefficient parsing"
        }
      ]
    }
  ]
})
```

### Scenario 3: Error Handling Strategy

**Request:** "Handle edge cases"

**Using AskUserQuestion:**

```javascript
AskUserQuestion({
  questions: [
    {
      question: "What edge cases need handling?",
      header: "Edge Cases",
      multiSelect: true,
      options: [
        {
          label: "Empty input",
          description: "User provides no data or blank fields"
        },
        {
          label: "Null values",
          description: "Missing or undefined data in system"
        },
        {
          label: "Concurrent access",
          description: "Multiple users modifying same resource"
        },
        {
          label: "Network failures",
          description: "External service unavailable or timeout"
        }
      ]
    },
    {
      question: "How should errors be handled?",
      header: "Strategy",
      multiSelect: false,
      options: [
        {
          label: "Fail fast",
          description: "Throw exception immediately (explicit errors, debugging easier)"
        },
        {
          label: "Graceful degradation",
          description: "Use defaults, continue operation (better UX, may hide issues)"
        },
        {
          label: "Retry with backoff",
          description: "Auto-retry with delays (good for transient failures)"
        },
        {
          label: "Log and continue",
          description: "Record error, proceed (background jobs, non-critical)"
        }
      ]
    }
  ]
})
```

### Scenario 4: Data Migration/Schema Changes

**Request:** "Update database schema"

**Using AskUserQuestion:**

```javascript
AskUserQuestion({
  questions: [
    {
      question: "How should existing data be handled?",
      header: "Migration",
      multiSelect: false,
      options: [
        {
          label: "Auto-migrate",
          description: "Migrate data automatically on deployment (safe, recommended)"
        },
        {
          label: "Manual migration",
          description: "Provide script, admin runs it (more control, manual step)"
        },
        {
          label: "Drop & recreate",
          description: "Delete old data (dev/test only, NOT for production)"
        }
      ]
    },
    {
      question: "What are backwards compatibility requirements?",
      header: "Compatibility",
      multiSelect: false,
      options: [
        {
          label: "Fully compatible",
          description: "Old code must work (safest, may limit changes)"
        },
        {
          label: "Grace period",
          description: "Deprecation warnings, 1-2 releases to migrate (balanced)"
        },
        {
          label: "Breaking change OK",
          description: "Can break old code (fastest, requires coordination)"
        }
      ]
    },
    {
      question: "When should the migration be applied?",
      header: "Timing",
      multiSelect: false,
      options: [
        {
          label: "Immediate",
          description: "Next deployment (for small changes, low traffic)"
        },
        {
          label: "Maintenance window",
          description: "Scheduled downtime (for large migrations, high impact)"
        },
        {
          label: "Gradual rollout",
          description: "Phased migration (for critical systems, zero downtime needed)"
        }
      ]
    }
  ]
})
```

## Advanced Usage

### Multiple Questions in Sequence

Ask up to 4 questions at once for complex scenarios:

```javascript
AskUserQuestion({
  questions: [
    {
      question: "Question 1?",
      header: "Header 1",
      multiSelect: false,
      options: [...]
    },
    {
      question: "Question 2?",
      header: "Header 2",
      multiSelect: false,
      options: [...]
    },
    {
      question: "Question 3?",
      header: "Header 3",
      multiSelect: true,  // Multiple selections allowed
      options: [...]
    },
    {
      question: "Question 4?",
      header: "Header 4",
      multiSelect: false,
      options: [...]
    }
  ]
})
```

### Conditional Questions

Based on previous answers, ask follow-up questions:

```javascript
// First question
AskUserQuestion({
  questions: [{
    question: "Do you want to enable caching?",
    header: "Caching",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Enable caching for better performance" },
      { label: "No", description: "No caching needed" }
    ]
  }]
})

// If answer is "Yes", ask follow-up:
if (answer === "Yes") {
  AskUserQuestion({
    questions: [{
      question: "Which caching strategy?",
      header: "Strategy",
      multiSelect: false,
      options: [
        { label: "Redis", description: "Distributed cache, scalable" },
        { label: "In-memory", description: "Fast but per-instance" },
        { label: "CDN", description: "Edge caching for static assets" }
      ]
    }]
  })
}
```

## Integration with Other Skills

### Use with plugin-setup

The `plugin-setup` skill uses this skill extensively for configuration:

```javascript
// plugin-setup calls this skill
Skill("interactive-questions")

// Then uses AskUserQuestion for all setup questions
AskUserQuestion({
  questions: [
    { question: "Project type?", ... },
    { question: "Issue tracker?", ... },
    ...
  ]
})
```

### Use with project-planner

When requirements are unclear during planning:

```javascript
// In project-planner agent
if (requirementsUnclear) {
  Skill("interactive-questions")
  
  AskUserQuestion({
    questions: [{
      question: "Which approach do you prefer?",
      header: "Approach",
      multiSelect: false,
      options: [
        { label: "Option A", description: "Pros and cons..." },
        { label: "Option B", description: "Trade-offs..." }
      ]
    }]
  })
}
```

## Tips for Effective Questions

1. **Be Specific**: Vague questions get vague answers
   - ❌ "How to do it?"
   - ✅ "Which validation strategy: client-side, server-side, or both?"

2. **Provide Context**: Explain why it matters
   - Include trade-offs in descriptions
   - Mention performance, security, or maintenance implications

3. **Limit Options**: 2-4 options ideal
   - Too few: Not helpful
   - Too many: Overwhelming
   - User can always select "Other" for custom input

4. **Use Clear Labels**: 1-5 words max
   - ❌ "Use the traditional session-based authentication mechanism"
   - ✅ "Session-based"

5. **Actionable Descriptions**: Explain what each option does
   - Include estimated effort if relevant
   - Mention if it's the recommended option

6. **Group Related Questions**: Ask them together
   - Use multiSelect when answers aren't exclusive
   - Use single select for either/or decisions

---

**For detailed patterns, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
