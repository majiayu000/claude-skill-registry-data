---
name: wishful-thinking-programming
description: Use when building features with unknowns or uncertainties - start from well-understood parts (business logic, UX, pure functions), write code as if ideal collaborators exist, use mocks to define APIs through usage, preventing analysis paralysis from trying to understand everything upfront
---

# Wishful-Thinking Programming

## Overview

**Write code as if the perfect utilities, libraries, and APIs already exist. Let your tests define what they should be.**

Don't let unknowns block you. Start from what you understand (business logic, UX design, pure functions) and work outward, imagining the ideal collaborators into existence.

**Core principle:** Code first, research later. Mocks collected across tests define what the real collaborator must do.

## When to Use

**Use wishful-thinking when:**
- Building feature with unknowns (which library? what API?)
- Multiple uncertainties block traditional bottom-up approach
- Business logic is clear but infrastructure isn't
- You have UX design but not implementation details
- Facing analysis paralysis from too many unknowns

**Don't use when:**
- All pieces are well-known and documented
- Working with existing, familiar APIs
- Doing pure refactoring (no new collaborators)

## The Anti-Pattern (Baseline Behavior)

**❌ "Understand Everything First" approach:**
1. Research all unknowns upfront
2. Choose libraries before writing code
3. Bottom-up: start from what exists
4. Block on uncertainties
5. Analysis paralysis

**Result:** Stuck researching, never coding.

## The Wishful-Thinking Pattern

**✓ "Code As If It Works" approach:**
1. Identify well-understood part (logic/UX/domain)
2. Start there, write ONE test assuming ideal API (use incremental-tdd skill)
3. Mock collaborators you wish existed
4. Green? Move to next test (ONE at a time)
5. Mocks accumulate → define real collaborator

**Result:** Forward progress, discover APIs through usage.

**CRITICAL:** Use the incremental-tdd skill. Write ONE failing test, make it pass, then write the NEXT test. Never write multiple failing tests at once.

## The Workflow

### 1. Find Your Center

**Start from most well-understood part - WHERE it's USED, not WHAT it is:**
- Have view/UI? Start from handler/controller that CALLS the view
- Have business logic? Start from test that USES the logic
- Know the requirements? Start from test describing WHAT should happen
- Work outward from understanding toward unknowns

**Common mistake:** Starting from infrastructure (config loader, database client, API client). These are EDGES - unknowns that should be mocked.

**Key insight:** Don't write tests for collaborators nobody uses yet. Start from the integration point (handler, controller, service) that USES the collaborators.

**Don't start from edges (infrastructure, config, database, APIs).**

### 2. Write ONE Test with Wishful Thinking

**IMPORTANT:** Write ONE failing test at a time (incremental-tdd skill). Don't write multiple tests before implementing.

Write ONE test as if perfect collaborators exist:

```typescript
test("fetch user profile and cache it", async () => {
  // Wishful thinking: imagine ideal API
  const profile = await userService.fetchProfile("user123");

  expect(profile.name).toBe("Alice");
  expect(profile.email).toBe("alice@example.com");

  // Wishful thinking: imagine caching works perfectly
  const cached = await userService.fetchProfile("user123");
  expect(cached).toBe(profile); // Same instance = cached
});
```

**You don't know:**
- Which HTTP library?
- What's the real API shape?
- How to implement caching?

**You DO know:**
- You want `userService.fetchProfile(id)`
- It should return structured data
- It should cache automatically

### 3. Mock the Collaborators (Use Dependency Injection)

**CRITICAL:** Always use dependency injection, never import collaborators directly.

❌ **Wrong - Direct import:**
```typescript
// userService.ts
import { apiClient } from './apiClient'; // Can't mock!

class UserService {
  async fetchProfile(id: string) {
    return await apiClient.get(`/users/${id}`);
  }
}
```

✓ **Right - Dependency injection:**
```typescript
// Test: Mock what you wish existed
const mockApiClient = {
  get: jest.fn().mockResolvedValue({
    data: { name: "Alice", email: "alice@example.com" }
  })
};

const userService = new UserService(mockApiClient);

// Implementation: Accept injected dependency
class UserService {
  constructor(private apiClient: ApiClient) {}
  async fetchProfile(id: string) {
    return await this.apiClient.get(`/users/${id}`);
  }
}
```

**The mock defines the API** - you've designed what the HTTP client should look like through usage.

### 4. Implement Minimal Code

```typescript
class UserService {
  constructor(private apiClient: ApiClient) {}

  async fetchProfile(userId: string) {
    const response = await this.apiClient.get(`/users/${userId}`);
    return response.data;
  }
}
```

**Still no real HTTP library chosen.** You're coding against your imagined ideal.

### 5. Accumulate Mocks → Define Collaborator

After full test suite, your mocks show you need:

```typescript
interface ApiClient {
  get(url: string): Promise<{ data: any }>;
  post(url: string, body: any): Promise<{ data: any }>;
  // ... discovered through usage
}
```

**NOW research which library fits this interface** - Axios? Fetch? Custom wrapper?

## Quick Reference

| Situation | Wishful-Thinking Action |
|-----------|-------------------------|
| Don't know which library | Write code as if ideal library exists, mock it |
| API shape unclear | Write test with ideal shape, mock returns it |
| Multiple unknowns | Start from logic/UX, mock all edges |
| Bottom-up blocked | Go middle-out or outside-in with mocks |
| Analysis paralysis | Write ONE test with wishful API, run it |

## Integration with TDD

Wishful-thinking IS test-driven development with permission to imagine:

**RED:** Write ONE test with imagined perfect API
**GREEN:** Implement against mocks
**REFACTOR:** Replace mocks with real collaborators (when needed)

The cycle continues. Each test adds to mock behavior, defining the real API.

**CRITICAL:** Use the incremental-tdd skill alongside this one. Write ONE failing test at a time, not multiple tests at once.

**Why they work together:**

The REFACTOR step is where you evaluate the emerging design:

1. **RED**: Write ONE test with wishful thinking (imagine ideal API)
2. **GREEN**: Implement with mocks
3. **REFACTOR**: Look at what emerged. Is the API actually good? Do the mocks make sense?
4. **Learn**: Now you know what works → informs NEXT test

Writing ONE test at a time lets you see and refine the design as it emerges. You can't evaluate design quality until you see it. Each test-implement-refactor cycle reveals what the API should actually be.

**Writing multiple tests at once breaks this:** You commit to an imagined API before seeing if it works. No refactor step between tests means no learning, no refinement, no design discovery.

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Need to research libraries first" | No. Mock first, research when API defined through usage. |
| "Can't write code without knowing API shape" | YES YOU CAN. Imagine ideal shape, code to that. |
| "Let me design the API before using it" | API emerges from usage. Write test first. |
| "Need to plan data structures upfront" | Data shapes emerge from what tests need. Code first. |
| "Mocking is just pretending" | Mocks ARE the spec. They define what real thing must do. |
| "Bottom-up is more reliable" | Bottom-up blocks on unknowns. Outside-in with mocks proceeds. |
| "Start from infrastructure/config/database" | Start from what you KNOW (view, business logic), not edges. |
| "Import collaborators directly for simplicity" | Use dependency injection. Enables mocking and wishful APIs. |
| "This is just prototyping" | This IS production code design. Mocks become interfaces. |
| "Need complete understanding first" | Understanding emerges through coding, not before it. |

**Seeing yourself in this table? STOP. Write one wishful test NOW.**

## Example: Payment Processing

**Blocked:** Which gateway? How do webhooks work? What email service?

**Wishful approach:** Test defines ideal API:
```typescript
test("process payment sends email", async () => {
  const result = await paymentProcessor.process(payment);
  expect(mockEmailService.send).toHaveBeenCalled();
});

// Implement with DI and mocks
class PaymentProcessor {
  constructor(private gateway, private emailService) {}
  async process(payment) {
    const charge = await this.gateway.charge(payment);
    await this.emailService.send({...});
    return { success: true, transactionId: charge.id };
  }
}
```

**Result:** Working code, defined APIs. Still don't know which gateway - but mocks show what it must do.

## Red Flags - You're Doing It Wrong

**STOP if you catch yourself:**
- Researching libraries before writing tests
- "I need to understand X first"
- Designing/planning APIs before writing tests that use them
- Starting from infrastructure (config, database, API client)
- Writing tests for collaborators nobody uses yet
- Choosing tools before knowing requirements
- Using `import { collaborator }` instead of dependency injection
- Analysis paralysis from unknowns
- **Writing multiple failing tests before implementing** (violates incremental-tdd)
- **Creating full test file structure before writing first test** (batch testing)

**All of these mean: Write ONE wishful test NOW from where the feature is USED, make it pass, then write the NEXT test.**

## The Bottom Line

**Wishful-thinking = permission to imagine ideal APIs and code to them.**

You're never ready to code. Code anyway with mocks. Understanding emerges from usage, not before it.

**Start from where it's USED. Work outward with imagination.**
