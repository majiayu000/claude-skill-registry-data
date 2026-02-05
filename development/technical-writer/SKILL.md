---
name: technical-writer
description: User documentation technical writer focused on user and developer experience, code examples, and 2025 best practices. Use when creating README files, API docs, getting started guides, tutorials, or any technical documentation intended for developers or end users.
---

# Technical Writer

*Documentation that developers actually want to read.*

<purpose>
Create documentation that helps users accomplish specific tasks. Every doc answers: What is this? Why should I care? How do I start?
</purpose>

<when_to_activate>
Activate when:
- Creating or improving README files
- Writing API documentation
- Building getting started guides or quickstarts
- Creating tutorials or how-to guides
- Writing reference documentation
- Documenting CLI tools or SDKs

**Trigger phrases:** "docs", "documentation", "readme", "guide", "tutorial", "API docs"
</when_to_activate>

---

## Core Philosophy

**Documentation is a product.** It has users, and those users have jobs to be done. Every piece of documentation should help someone accomplish something specific.

The three questions every doc must answer:
1. **What is this?** (in 10 seconds or less)
2. **Why should I care?** (the value proposition)
3. **How do I start?** (immediate actionability)

---

## The 2025 Documentation Stack

### Progressive Disclosure Architecture

Structure documentation in layers:

```
Layer 1: README / Landing (30 seconds)
   ↓
Layer 2: Quickstart (5 minutes)
   ↓
Layer 3: Tutorials (30 minutes)
   ↓
Layer 4: Reference (as needed)
   ↓
Layer 5: Deep Dives (when ready)
```

**Never front-load complexity.** Users discover depth when they need it.

### The Four Documentation Types

| Type | Purpose | User State | Format |
|------|---------|------------|--------|
| **Tutorial** | Learning | "Teach me" | Step-by-step journey |
| **How-to** | Problem-solving | "Help me do X" | Task-focused steps |
| **Reference** | Information | "What does X do?" | Accurate, complete, dry |
| **Explanation** | Understanding | "Why does X work this way?" | Discussion, context |

**Don't mix types.** A tutorial that turns into a reference confuses everyone.

---

## README Structure (The Front Door)

Every README follows this hierarchy:

```markdown
# Project Name

One-line description of what this does and who it's for.

## Quick Start

[Fastest possible path to "hello world"]

## Installation

[Complete installation for all platforms]

## Usage

[Common patterns with examples]

## Documentation

[Links to full docs]

## Contributing

[How to help]

## License

[Legal stuff]
```

### The 10-Second Test

A developer landing on your README should understand:
- What the project does
- Whether it's relevant to them
- How to try it immediately

If they have to scroll to understand what it is, you've failed.

### The One-Line Description Formula

```
[Project Name] is a [category] that [primary action] for [target user].
```

**Good:**
> Fastify is a web framework that provides the fastest HTTP server for Node.js

**Bad:**
> Fastify is a highly performant, low overhead web framework built on top of a highly optimized architecture leveraging modern JavaScript features...

---

## Code Examples: The Heart of Technical Docs

### The Copy-Paste Standard

Every code example must be:
1. **Complete** - Runnable without modification
2. **Correct** - Actually works when copied
3. **Contextual** - Shows where the code goes
4. **Current** - Uses latest stable API

### Code Block Anatomy

```typescript
// Context: Where does this code go?
// File: src/api/users.ts

import { createClient } from '@example/sdk'  // Dependencies shown

// Create client with required config
const client = createClient({
  apiKey: process.env.API_KEY,  // Environment variables, not hardcoded
  region: 'us-west-2'
})

// Usage pattern - the actual thing they're learning
const users = await client.users.list({
  limit: 10,
  status: 'active'
})

// What to expect
console.log(users)
// → [{ id: '123', name: 'Alice', ... }, ...]
```

### Example Progression

Start simple, build complexity:

```typescript
// Basic usage
const result = await api.query('SELECT * FROM users')

// With options
const result = await api.query('SELECT * FROM users', {
  timeout: 5000,
  cache: true
})

// With error handling
try {
  const result = await api.query('SELECT * FROM users')
} catch (error) {
  if (error instanceof QueryTimeout) {
    // Handle timeout specifically
  }
  throw error
}
```

### Language-Specific Conventions

**JavaScript/TypeScript:**
- Prefer `const` over `let`
- Use async/await over callbacks
- Show TypeScript types when relevant
- Include `// →` output comments

**Python:**
- Use type hints for function signatures
- Include docstring examples
- Show both sync and async patterns where applicable

**CLI:**
```bash
# Comment explaining what this does
$ command --flag value
Expected output here
```

Note: Always prefix commands with `$` to distinguish input from output.

### Anti-Patterns in Code Examples

**Never:**
```typescript
// Bad: Placeholders without explanation
const client = new Client(YOUR_API_KEY)

// Bad: Partial code
// ... some code ...
const result = await fetch()

// Bad: Outdated patterns
var data = null
fetch(url, function(err, res) { ... })

// Bad: Console.log without expected output
console.log(response)
```

**Instead:**
```typescript
// Good: Environment variable pattern
const client = new Client(process.env.API_KEY)

// Good: Complete context
import { Client } from '@example/sdk'
const client = new Client(process.env.API_KEY)
const result = await client.fetch('/users')

// Good: Modern patterns
const data: User | null = await fetchUser(id)

// Good: Expected output shown
console.log(response)
// → { status: 200, data: { id: '123', name: 'Alice' } }
```

---

## API Documentation

### Endpoint Documentation Template

```markdown
## Create User

Creates a new user in the system.

### Request

`POST /api/v1/users`

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | Must be `application/json` |

#### Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| name | string | Yes | Display name (2-100 chars) |
| role | string | No | One of: `admin`, `user`. Default: `user` |

#### Example Request

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "name": "Alice Smith",
    "role": "admin"
  }'
```

### Response

#### Success (201 Created)

```json
{
  "id": "usr_abc123",
  "email": "alice@example.com",
  "name": "Alice Smith",
  "role": "admin",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

#### Errors

| Status | Code | Description |
|--------|------|-------------|
| 400 | `invalid_email` | Email format is invalid |
| 409 | `email_exists` | User with this email already exists |
| 422 | `name_too_short` | Name must be at least 2 characters |
```

### SDK Documentation Pattern

```typescript
/**
 * Creates a new user in the system.
 *
 * @param options - User creation options
 * @returns The created user object
 * @throws {ValidationError} When email format is invalid
 * @throws {ConflictError} When email already exists
 *
 * @example
 * ```ts
 * const user = await client.users.create({
 *   email: 'alice@example.com',
 *   name: 'Alice Smith'
 * })
 * console.log(user.id) // → 'usr_abc123'
 * ```
 */
async create(options: CreateUserOptions): Promise<User>
```

---

## Writing Style Guide

### Voice & Tone

**Be direct.** Technical readers want information, not persuasion.

| Instead of | Write |
|------------|-------|
| "You might want to consider..." | "Use..." |
| "It's worth noting that..." | [Just state it] |
| "In order to..." | "To..." |
| "Please ensure that you..." | [Just give the instruction] |
| "The system will then proceed to..." | "Then..." |

### Second Person, Active Voice

**Good:** "Configure the database connection."
**Bad:** "The database connection should be configured by the user."

### Present Tense

**Good:** "This function returns a promise."
**Bad:** "This function will return a promise."

### Sentence Structure

- Lead with the action: "Run `npm install` to install dependencies."
- One idea per sentence
- Maximum 25 words per sentence for instructions
- Use lists for 3+ related items

### Technical Terminology

**Be consistent.** Pick one term and stick with it:
- "function" not "method/function/procedure"
- "parameter" not "argument/parameter/input"
- Define terms on first use, then use them consistently

**Be precise:**
- "Click" for mouse, "Tap" for touch, "Select" for either
- "Enter" for typing, "Paste" for clipboard
- "Run" for commands, "Execute" for code

---

## 2025 Best Practices

### AI-Era Documentation

Your documentation will be read by AI assistants helping developers. Optimize for both:

**For humans:**
- Visual hierarchy with headers and whitespace
- Contextual explanations
- Progressive disclosure

**For AI parsing:**
- Structured, consistent formatting
- Clear section boundaries
- Explicit relationships between concepts
- Complete, runnable code examples

### Accessibility

- Alt text for all images
- Text alternatives for diagrams (ASCII or descriptions)
- Color-independent meaning (don't rely on color alone)
- Logical heading hierarchy (h1 → h2 → h3, no skipping)
- Code examples with syntax highlighting classes, not just color

### Versioning

Every doc should indicate:
- What version it applies to
- When it was last updated
- Where to find docs for other versions

```markdown
> **Version:** This document applies to v2.x. For v1.x docs, see [here](link).
> **Last updated:** 2025-01-15
```

### Searchability

- Use the words developers actually search for
- Include common misspellings in metadata (not visible text)
- Repeat key terms naturally
- Create descriptive headings (not "Overview" but "User Authentication Overview")

### Maintenance Signals

Help future maintainers:
- Date stamps on time-sensitive content
- `TODO:` markers for known gaps
- Links to related issues/PRs for complex decisions
- Clear ownership (who maintains this section?)

---

## Document Templates

### Getting Started Guide

```markdown
# Getting Started with [Product]

Get [Product] running in under 5 minutes.

## Prerequisites

Before you begin, ensure you have:
- Node.js 18 or later
- An API key ([get one here](link))

## Step 1: Install

```bash
npm install @example/sdk
```

## Step 2: Configure

Create a `.env` file:

```bash
API_KEY=your_api_key_here
```

## Step 3: Hello World

Create `index.js`:

```javascript
import { Client } from '@example/sdk'

const client = new Client(process.env.API_KEY)
const result = await client.ping()
console.log(result) // → { status: 'ok' }
```

Run it:

```bash
node index.js
```

## Next Steps

- [Tutorial: Build your first integration](link)
- [API Reference](link)
- [Examples repository](link)
```

### How-To Guide

```markdown
# How to [Accomplish Task]

[One sentence describing what this guide helps you do.]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Steps

### 1. [First action]

[Explanation if needed]

```code
example
```

### 2. [Second action]

...

## Verification

[How to confirm it worked]

## Troubleshooting

### [Common problem 1]

[Solution]

### [Common problem 2]

[Solution]

## Related

- [Related guide 1](link)
- [Related guide 2](link)
```

### Migration Guide

```markdown
# Migrating from v1 to v2

## Overview

v2 introduces [major changes]. This guide covers:
- Breaking changes and how to handle them
- New features you can adopt
- Deprecations to address

**Estimated time:** 30 minutes for most projects

## Breaking Changes

### [Change 1]: New authentication method

**Before (v1):**
```typescript
const client = new Client(apiKey)
```

**After (v2):**
```typescript
const client = new Client({ apiKey })
```

**Migration:** Wrap your API key in an options object.

### [Change 2]: ...

## New Features

### [Feature 1]

You can now [capability]. To use it:

```typescript
// Example
```

## Deprecations

| Deprecated | Replacement | Remove in |
|------------|-------------|-----------|
| `oldMethod()` | `newMethod()` | v3.0 |

## Need Help?

- [GitHub Discussions](link)
- [Discord](link)
```

---

## Quality Checklist

Before publishing any documentation:

### Accuracy
- [ ] All code examples tested and runnable
- [ ] Links verified working
- [ ] Version numbers current
- [ ] Screenshots match current UI

### Completeness
- [ ] Prerequisites listed
- [ ] All required steps included
- [ ] Error cases addressed
- [ ] Next steps provided

### Clarity
- [ ] One idea per paragraph
- [ ] Technical terms defined
- [ ] Consistent terminology throughout
- [ ] Headings are descriptive

### Experience
- [ ] Can complete the task in stated time
- [ ] No assumed knowledge beyond stated prerequisites
- [ ] Works on stated platforms
- [ ] Copy-paste code actually works

---

<skill_compositions>
## Skill Compositions

### technical-writer + dmitrii-writing-style
**Creates:** Documentation with authentic voice

Use when documentation needs personality while maintaining technical accuracy. Apply dmitrii-writing-style's directness and warmth to technical content.

### technical-writer + first-time-user
**Creates:** Validated documentation

Write docs, then test them with first-time-user simulation. Fix friction points. Repeat until smooth.

### technical-writer + ultrathink
**Creates:** Thoughtful documentation architecture

Before writing, ultrathink the information architecture. Who are the users? What are their jobs to be done? What's the right structure?

### technical-writer + serghei-qa
**Creates:** Battle-tested examples

Write the docs, then have Serghei review the code examples for edge cases, error handling, and security issues.
</skill_compositions>

---

## Anti-Patterns

**Wall of Text**
Break it up. Use headers, lists, code blocks, and whitespace.

**Tutorial-Reference Hybrid**
Don't explain concepts in reference docs. Don't list every option in tutorials.

**Placeholder Examples**
`YOUR_API_KEY_HERE` without explaining how to get one is a dead end.

**Screenshot-Only Documentation**
Screenshots break. Always include text alternatives.

**Assuming the Happy Path**
Document what happens when things go wrong.

**Writing for Yourself**
You already know how it works. Write for someone who doesn't.

---

## The Meta-Rule

The best documentation disappears. When someone finishes using your docs, they should feel like the product was so intuitive they barely needed help.

If your docs feel like a maze, your product probably is too. Documentation problems are often product problems in disguise.

---

*Now: what are we documenting?*
