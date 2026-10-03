---
name: firebase-development
description: Routes Firebase development tasks to specialized sub-skills covering project setup, feature development, debugging, and validation. Use when starting a Firebase project, adding Cloud Functions or Firestore collections, troubleshooting Firebase emulator or deployment issues, or reviewing Firebase security rules and architecture.
---

# Firebase Development

## Overview

This skill system guides Firebase development using proven patterns from production projects. It routes to specialized sub-skills based on detected intent.

**Sub-skills:**
- `firebase-development:project-setup` - Initialize new Firebase projects
- `firebase-development:add-feature` - Add functions/collections/endpoints
- `firebase-development:debug` - Troubleshoot emulator and runtime issues
- `firebase-development:validate` - Review Firebase code for security/patterns

## When This Skill Applies

- Starting new Firebase projects
- Adding Cloud Functions or Firestore collections
- Debugging emulator issues or rule violations
- Reviewing Firebase code for security and patterns
- Setting up multi-hosting configurations
- Implementing authentication (API keys or Firebase Auth)

## Routing Logic

### Keywords by Sub-Skill

**project-setup:**
- "new firebase project", "initialize firebase", "firebase init"
- "set up firebase", "create firebase app", "start firebase project"

**add-feature:**
- "add function", "create endpoint", "new tool", "add api"
- "new collection", "add feature", "build", "implement"

**debug:**
- "error", "not working", "debug", "emulator issue"
- "rules failing", "permission denied", "troubleshoot", "deployment failed"

**validate:**
- "review firebase", "check firebase", "validate", "audit firebase"
- "look at firebase code", "security review"

### Routing Process

1. **Analyze Request**: Check for routing keywords
2. **Match Sub-Skill**: Identify best match based on keyword density
3. **Announce**: "I'm using the firebase-development:[sub-skill] skill to [action]"
4. **Route**: Load and execute the sub-skill
5. **Fallback**: If ambiguous, use AskUserQuestion with 4 options

### Fallback Example

If intent is unclear, ask:

```
Question: "What Firebase task are you working on?"
Options:
  - "Project Setup" (Initialize new Firebase project)
  - "Add Feature" (Add functions, collections, endpoints)
  - "Debug Issue" (Troubleshoot errors or problems)
  - "Validate Code" (Review against patterns)
```

## Reference Projects

Patterns are extracted from three production Firebase projects:

| Project | Source | Key Patterns |
|---------|--------|--------------|
| **oneonone** | Express API project (private repo not found on GitHub) | Express API, custom API keys, server-write-only |
| **bot-socialmedia** | https://github.com/2389-research/bot-socialmedia-server (private) | Domain-grouped functions, Firebase Auth + roles |
| **meme-rodeo** | https://github.com/2389-research/meme-rodeo (private) | Individual function files, entitlements |

## Pattern Summaries

- **Multi-Hosting Setup:** `docs/examples/multi-hosting-setup.md`
- **Authentication:** `docs/examples/api-key-authentication.md`
- **Cloud Functions Architecture:** `docs/examples/express-function-architecture.md`
- **Security Model:** `docs/examples/firestore-rules-patterns.md`
- **Emulator-First Development:** `docs/examples/emulator-workflow.md`

## Modern Tooling Standards

All Firebase projects follow these standards:

| Tool | Purpose | Config File |
|------|---------|-------------|
| TypeScript | Type safety | `tsconfig.json` |
| vitest | Testing | `vitest.config.ts` |
| biome | Linting + formatting | `biome.json` |

### ABOUTME Comment Pattern

Every TypeScript file starts with 2-line ABOUTME comment:

```typescript
// ABOUTME: Brief description of what this file does
// ABOUTME: Second line with additional context
```

### Testing Requirements

- **Unit tests**: Test handlers/utilities in isolation
- **Integration tests**: Test with emulators running
- Both required for every feature

## Common Gotchas

| Issue | Solution |
|-------|----------|
| Emulator ports in use | `lsof -i :5001`, kill process |
| Admin SDK vs Client SDK | Admin bypasses rules, client respects rules |
| Cold start delays | First call takes 5-10s, normal |
| Data persistence | Use Ctrl+C (not kill) to export data |
| CORS in functions | `app.use(cors({ origin: true }))` |

