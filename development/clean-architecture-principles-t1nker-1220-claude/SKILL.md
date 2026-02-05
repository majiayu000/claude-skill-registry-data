---
name: clean-architecture-principles
description: Enforce clean architecture principles including DRY, YAGNI, KISS, Law of Demeter, and Separation of Concerns. Warns when complexity creeps in and questions unnecessary features. Use when designing architecture, refactoring, code review, or when user mentions architecture, design patterns, complexity, or refactoring.
version: 1.0.0
---

# Clean Architecture Principles

Core architectural principles focused on simplicity, maintainability, and avoiding unnecessary complexity.

## Philosophy: Simplicity Over Complexity

**If a feature is getting complicated, approach the user about it.**

**Warn when:**
- Engineering becomes complex or complicated
- Multiple approaches exist (suggest simpler one)
- Potential issues are detected

**Format:**
```
WARNING: This feature is getting complicated. Here's a simpler approach...
```

## Core Principles

### 1. DRY (Don't Repeat Yourself)

**Code duplication means failure.**

**Bad - Duplication:**
```typescript
// Creating user
async function createUser(data: UserInput) {
  const user = {
    id: generateId(),
    ...data,
    createdAt: new Date(),
    updatedAt: new Date()
  };
  await db.users.insert(user);
  await sendEmail(user.email, 'Welcome!');
  await logEvent('user_created', user.id);
  return user;
}

// Creating admin - DUPLICATED LOGIC
async function createAdmin(data: AdminInput) {
  const admin = {
    id: generateId(),
    ...data,
    createdAt: new Date(),
    updatedAt: new Date(),
    role: 'admin'
  };
  await db.users.insert(admin);
  await sendEmail(admin.email, 'Welcome Admin!');
  await logEvent('admin_created', admin.id);
  return admin;
}
```

**Good - DRY:**
```typescript
// Shared logic extracted
async function createUserAccount(
  data: UserInput,
  role: 'user' | 'admin' = 'user'
) {
  const account = {
    id: generateId(),
    ...data,
    role,
    createdAt: new Date(),
    updatedAt: new Date()
  };

  await db.users.insert(account);
  await sendEmail(account.email, getWelcomeMessage(role));
  await logEvent(`${role}_created`, account.id);

  return account;
}

// Simple wrappers
const createUser = (data: UserInput) => createUserAccount(data, 'user');
const createAdmin = (data: AdminInput) => createUserAccount(data, 'admin');
```

### 2. YAGNI (You Ain't Gonna Need It)

**Speculation gets rejected.**

**Bad - Building features "just in case":**
```typescript
interface UserService {
  // Currently needed
  getUser(id: string): Promise<User>;

  // Speculative - might need someday
  getAllUsers(): Promise<User[]>;
  searchUsers(query: string): Promise<User[]>;
  batchUpdateUsers(ids: string[], updates: Partial<User>): Promise<void>;
  exportUsersToCSV(): Promise<string>;
  importUsersFromCSV(csv: string): Promise<void>;
  archiveOldUsers(days: number): Promise<number>;
}
```

**Good - Only what's needed now:**
```typescript
interface UserService {
  // Only what's actually needed right now
  getUser(id: string): Promise<User>;
}

// Add methods ONLY when requirements emerge
```

**Question everything:**
- "Is this really needed?"
- "Will we use this now?"
- "Can we add it later if needed?"

### 3. KISS (Keep It Simple, Stupid)

**Complexity means rewrite.**

**Bad - Over-engineered:**
```typescript
// Complex factory pattern for simple task
interface INotificationStrategy {
  send(message: string): Promise<void>;
}

class EmailNotificationStrategy implements INotificationStrategy {
  async send(message: string): Promise<void> {
    await emailService.send(message);
  }
}

class SMSNotificationStrategy implements INotificationStrategy {
  async send(message: string): Promise<void> {
    await smsService.send(message);
  }
}

class NotificationContext {
  constructor(private strategy: INotificationStrategy) {}

  async notify(message: string): Promise<void> {
    await this.strategy.send(message);
  }
}

class NotificationFactory {
  static create(type: 'email' | 'sms'): NotificationContext {
    const strategy = type === 'email'
      ? new EmailNotificationStrategy()
      : new SMSNotificationStrategy();
    return new NotificationContext(strategy);
  }
}

// Usage - overly complex
const notifier = NotificationFactory.create('email');
await notifier.notify('Hello');
```

**Good - Simple:**
```typescript
// Simple function - does the same thing
async function sendNotification(message: string, type: 'email' | 'sms') {
  if (type === 'email') {
    await emailService.send(message);
  } else {
    await smsService.send(message);
  }
}

// Usage - clear and simple
await sendNotification('Hello', 'email');
```

### 4. Minimalism

**Bloat means delete.**

**Bad - Bloated with unused features:**
```typescript
class User {
  // Actually used
  id: string;
  name: string;
  email: string;

  // Unused - delete these
  nickname?: string;
  favoriteColor?: string;
  zodiacSign?: string;
  lucky Numbers?: number[];
  bio?: string;
  website?: string;
  socialLinks?: Record<string, string>;
}
```

**Good - Only what's needed:**
```typescript
class User {
  id: string;
  name: string;
  email: string;
}

// Add fields only when actually needed
```

### 5. Law of Demeter (Principle of Least Knowledge)

**Coupling means refactor.**

**Bad - Too much coupling:**
```typescript
// Reaching through multiple objects
function displayUserCity(user: User) {
  const city = user.profile.address.location.city.name;
  console.log(city);
}

// If any intermediate object changes, this breaks
```

**Good - Tell, don't ask:**
```typescript
// User provides what's needed
class User {
  getUserCity(): string {
    return this.profile.address.getCity();
  }
}

function displayUserCity(user: User) {
  const city = user.getUserCity();
  console.log(city);
}

// Or even simpler
function displayUserCity(city: string) {
  console.log(city);
}
```

### 6. SoC (Separation of Concerns)

**Mixed concerns means split.**

**Bad - Mixed concerns:**
```typescript
// One function doing everything
async function handleUserRegistration(formData: FormData) {
  // Validation
  if (!formData.email.includes('@')) throw new Error('Invalid email');
  if (formData.password.length < 8) throw new Error('Password too short');

  // Business logic
  const hashedPassword = await bcrypt.hash(formData.password, 10);
  const user = {
    id: generateId(),
    email: formData.email,
    password: hashedPassword,
    createdAt: new Date()
  };

  // Data access
  await db.users.insert(user);

  // Email sending
  await sendEmail(user.email, 'Welcome!');

  // Analytics
  await analytics.track('user_registered', { userId: user.id });

  // UI update
  showNotification('Registration successful!');

  return user;
}
```

**Good - Separated concerns:**
```typescript
// Validation layer
function validateRegistration(data: FormData): void {
  if (!data.email.includes('@')) throw new Error('Invalid email');
  if (data.password.length < 8) throw new Error('Password too short');
}

// Business logic layer
async function createUser(data: FormData): Promise<User> {
  const hashedPassword = await bcrypt.hash(data.password, 10);
  return {
    id: generateId(),
    email: data.email,
    password: hashedPassword,
    createdAt: new Date()
  };
}

// Data access layer
async function saveUser(user: User): Promise<void> {
  await db.users.insert(user);
}

// Notification layer
async function notifyNewUser(user: User): Promise<void> {
  await sendEmail(user.email, 'Welcome!');
  await analytics.track('user_registered', { userId: user.id });
}

// Orchestration - clean and clear
async function handleUserRegistration(formData: FormData) {
  validateRegistration(formData);
  const user = await createUser(formData);
  await saveUser(user);
  await notifyNewUser(user);
  showNotification('Registration successful!');
  return user;
}
```

## Filipino Wisdom Integration

### "Wag mong isama kung hindi mo kailangan"

**Apply to every line of code.**

**Questions to ask:**
- Do we really need this line?
- Is this variable actually used?
- Can we remove this abstraction?
- Is this dependency necessary?

**Examples:**

**Bad:**
```typescript
// Including things not needed
import { useEffect, useState, useCallback, useMemo, useRef } from 'react';

function SimpleComponent() {
  const [count, setCount] = useState(0);

  // useEffect, useCallback, useMemo, useRef not used - remove them
  return <div>{count}</div>;
}
```

**Good:**
```typescript
// Only what's needed
import { useState } from 'react';

function SimpleComponent() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}
```

## Clarity Beats Cleverness

**Every single time.**

**Bad - Clever but unclear:**
```typescript
// "Clever" one-liner
const result = users.reduce((a, u) => ({...a, [u.id]: u.posts.filter(p => p.likes > 10).map(p => p.title)}), {});
```

**Good - Clear and understandable:**
```typescript
// Clear multi-step process
const result: Record<string, string[]> = {};

for (const user of users) {
  const popularPosts = user.posts.filter(post => post.likes > 10);
  const titles = popularPosts.map(post => post.title);
  result[user.id] = titles;
}
```

## Warning System

**Always warn when complexity creeps in:**

```markdown
WARNING: This authentication flow is getting complicated with 5+ steps.

Simpler approach:
1. Use existing authentication library (e.g., NextAuth.js)
2. Reduces custom code by 80%
3. Battle-tested security
4. Maintained by community

Current approach requires:
- Custom JWT handling
- Manual token refresh
- Session management
- Security auditing

Recommendation: Use established solution instead.
```

## Questioning Requirements

**Never just accept requirements blindly.**

**Example conversation:**

```
User: "Add a feature where users can export their data to XML, JSON, CSV, and YAML formats"

Response:
"Let me question this requirement:

1. Which format will users actually use?
2. Can we start with just JSON (most common)?
3. Add other formats only if users request them?

Starting simple:
- Implement JSON export first
- Monitor usage
- Add other formats if needed

This approach:
✅ Delivers value faster
✅ Avoids building unused features
✅ Easier to maintain
✅ Can always add more later

Does JSON-only work for the initial release?"
```

## Complexity Detection Checklist

Warn if you detect:

- [ ] More than 3 levels of nesting
- [ ] Functions longer than 50 lines
- [ ] More than 5 function parameters
- [ ] Deeply nested object access (user.a.b.c.d.e)
- [ ] Multiple concerns in one function
- [ ] Duplicate code in 3+ places
- [ ] Speculative features not in requirements
- [ ] Over-engineered patterns for simple tasks
- [ ] Unnecessary abstractions or layers
- [ ] Complex logic that could be simplified

## Refactoring Triggers

Refactor when:

1. **Code Duplication** (DRY violation)
   - Same logic in multiple places
   - Copy-paste code

2. **High Coupling** (Law of Demeter violation)
   - Reaching through multiple objects
   - Changes ripple across many files

3. **Mixed Concerns** (SoC violation)
   - One function doing multiple things
   - Hard to understand or test

4. **Unnecessary Complexity** (KISS violation)
   - Over-engineered solutions
   - Complex patterns for simple problems

5. **Speculative Code** (YAGNI violation)
   - Unused features or functions
   - "Just in case" code

## Architecture Decision Template

Before building a feature, ask:

```markdown
## Feature: [Name]

### Is this really needed?
- [ ] Yes, it's in current requirements
- [ ] No, it's speculative

### Can we make it simpler?
Current approach: [Describe]
Simpler approach: [Describe]

### Does it follow principles?
- [ ] DRY - No code duplication
- [ ] YAGNI - Not speculative
- [ ] KISS - Simple, not complex
- [ ] SoC - Concerns separated
- [ ] Minimalism - Only what's needed

### Warning flags:
- Complexity level: [Low/Medium/High]
- Dependencies added: [Number]
- Lines of code: [Estimate]

### Recommendation:
[Approve / Simplify / Reject with reasons]
```

## Summary: Keep It Simple

**Golden Rules:**

1. **Question Everything**
   - "Is this really needed?"
   - "Can we make it simpler?"

2. **Avoid Complexity**
   - Simple solutions over clever ones
   - Warn when complexity creeps in

3. **Follow Principles**
   - DRY - Don't repeat yourself
   - YAGNI - You ain't gonna need it
   - KISS - Keep it simple
   - Minimalism - Only what's needed
   - Law of Demeter - Minimal coupling
   - SoC - Separate concerns

4. **Filipino Wisdom**
   - "Wag mong isama kung hindi mo kailangan"
   - Apply to every line

5. **Clarity Always Wins**
   - Clear code beats clever code
   - Every single time

**Remember:** The best architecture is the simplest one that solves the actual problem. Don't build what you might need—build what you need now.
