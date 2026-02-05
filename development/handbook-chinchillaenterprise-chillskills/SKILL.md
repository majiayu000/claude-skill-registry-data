---
name: handbook
description: Complete Amplify Gen 2 handbook - instructs Claude to read resources/handbook/ before implementing any code
---

# Handbook Skill - Read Before You Code

## Purpose

This skill instructs Claude to **read the project's handbook BEFORE implementing any code** in an Amplify Gen 2 project.

The handbook contains proven, production-tested patterns for:
- Authentication (Google OAuth, Cognito, security)
- Data modeling (DynamoDB, GraphQL schemas, TTL)
- Lambda functions (scheduled, triggers, DynamoDB access)
- Webhooks (Slack, Stripe, GitHub)
- Frontend patterns (MUI, design systems)
- Troubleshooting and debugging

## Core Principle: No Hallucinations, Only Handbook Patterns

When a user asks you to implement anything in an Amplify Gen 2 project:

1. **STOP** - Don't immediately write code
2. **CHECK** - Does `resources/handbook/` exist in the current project?
3. **LEARN** - Read the handbook to understand the correct patterns
4. **THEN CODE** - Implement using handbook patterns, not generic approaches

---

## The Workflow

### Step 1: Check for Handbook
```bash
# Is there a handbook in this project?
ls resources/handbook/README.md
```

If it exists, you have access to the complete Amplify Gen 2 handbook.

### Step 2: Start with Table of Contents
**ALWAYS begin here:**
- Read `resources/handbook/README.md`
- This contains the full table of contents
- Understand what sections exist (Auth, Functions, Data, Webhooks, etc.)
- Treat it like a textbook - respect the organization

### Step 3: Navigate to Relevant Section

Based on what the user wants to build:

| User Wants To Build | Read This Section |
|---------------------|-------------------|
| **DynamoDB model/schema** | `resources/handbook/data/` |
| **Scheduled Lambda function** | `resources/handbook/functions/scheduledFunction/` |
| **GraphQL resolver** | `resources/handbook/functions/graphqlResolver/` |
| **Webhook handler** | `resources/handbook/webhooks/` |
| **Google OAuth authentication** | `resources/handbook/auth/GOOGLE_OAUTH_SETUP.md` |
| **Cognito triggers** | `resources/handbook/auth/TRIGGERS_GUIDE.md` |
| **Environment variables** | `resources/handbook/ENVIRONMENT_VARIABLES.md` |
| **Docker Lambda** | `resources/handbook/functions/DOCKER_LAMBDA_WITH_AMPLIFY_GEN2.md` |
| **Long-running operations (>30s)** | `resources/handbook/ASYNC_PATTERNS.md` |

### Step 4: Learn the Pattern
- Read the guide completely
- Understand the Amplify Gen 2 way to do it
- Note any security considerations
- Check for common pitfalls
- Look at examples if available

### Step 5: Implement the Code
NOW you write the code, following the handbook patterns you just learned.

---

## Critical Rules (Always Follow)

### The "No CDK" Rule
- ❌ NEVER import from `aws-cdk-lib` for standard tasks
- ✅ ONLY use: `defineAuth`, `defineData`, `defineFunction`, `defineStorage`
- See: `resources/handbook/AI-DEVELOPMENT-GUIDELINES.md`

### The "No API Gateway" Rule
- ❌ NEVER create API Gateway resources
- ✅ Internal operations: GraphQL custom mutations
- ✅ External webhooks: Next.js API routes
- See: `resources/handbook/NO-API-GATEWAY.md`

### The "Learn First" Rule
- ❌ Don't write code based on generic knowledge or hallucinations
- ✅ Read the handbook section first, THEN code
- This prevents using wrong patterns or outdated approaches

---

## Navigation Aid

The handbook README.md has a comprehensive "I Need To..." table that maps user needs to specific documentation. Use it as your guide.

---

## What This Prevents

❌ Using outdated Amplify Gen 1 patterns
❌ Importing unnecessary CDK libraries
❌ Creating API Gateway resources (not needed)
❌ Manually writing IAM policies (handled by Amplify)
❌ Making up APIs that don't exist
❌ Generic Lambda code that doesn't integrate properly

✅ Using correct Amplify Gen 2 abstractions
✅ Following proven, production-tested patterns
✅ Writing code that works first try
✅ Proper integration with Amplify resources

---

## Remember

Every time you're about to write Amplify Gen 2 code:
1. Check for `resources/handbook/`
2. Read the relevant section
3. Learn the pattern
4. Then code

This ensures you implement things the correct way, following the template's established patterns and best practices.

---

## Updating the Handbook

**To get latest handbook:** Use the `handbook-sync` skill

**To contribute new patterns:** Use the `handbook-updater` skill
