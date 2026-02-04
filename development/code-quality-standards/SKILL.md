---
name: code-quality-standards
description: Use when writing any code - enforces clean architecture with descriptive names, real implementations, no backward compatibility concerns, and no lint suppressions
---

# Code Quality Standards

**Core principle:** Write clean, maintainable code that speaks for itself.

## When to Use This Skill

**Always use when:**
- Writing any new code
- Refactoring existing code
- Reviewing code before committing
- Creating functions, variables, or classes

**This is mandatory - not optional.**

## Five Non-Negotiable Rules

### 1. Variable Names Must Be Descriptive, Not IDs

**WRONG:**
```typescript
const id = getUserId();
const val = calculateTotal();
const tmp = data.filter(x => x.active);
const i = items[0];
const user1 = getUser();
const data2 = processData();
const result3 = calculate();
```

**RIGHT:**
```typescript
const currentUserId = getUserId();
const orderTotal = calculateTotal();
const activeCustomers = data.filter(customer => customer.active);
const firstItem = items[0];
const primaryUser = getUser();
const processedCustomerData = processData();
const finalCalculationResult = calculate();
```

**Key principles:**
- Use full, descriptive names that reveal intent
- Avoid abbreviations (except universally understood ones like `url`, `id` in compound names)
- Variables should read like English sentences
- Never use single letters except in tiny scopes (map/filter callbacks)
- Never use numbers in variable names (e.g., `user1`, `data2`, `temp3`)
- Be verbose - clarity > brevity

### 2. Actual Implementation, Not Placeholders

**WRONG:**
```typescript
function processOrder(order: Order) {
  // TODO: Implement validation
  // Validate order here
  /* Implementation goes here */
  return true;
}

const handleSubmit = () => {
  // To be implemented
};
```

**RIGHT:**
```typescript
function processOrder(order: Order): ProcessedOrder {
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must contain at least one item');
  }

  if (order.total <= 0) {
    throw new Error('Order total must be greater than zero');
  }

  const validatedOrder = {
    ...order,
    validatedAt: new Date(),
    status: 'validated',
  };

  return validatedOrder;
}

const handleSubmit = async (formData: FormData) => {
  const validatedData = validateFormData(formData);
  await saveToDatabase(validatedData);
  navigateToSuccessPage();
};
```

**Key principles:**
- Write complete, working implementations
- No TODO comments for core functionality
- No placeholder functions
- No "to be implemented" comments
- If you write a function, implement it fully

### 3. Never Care About Backward Compatibility

**WRONG:**
```typescript
// Keep old function for backward compatibility
function getUser(id: string) {
  return getUserById(id);
}

function getUserById(userId: string) {
  // New implementation
}

// Support both old and new parameter names
function createOrder(params: { id?: string; orderId?: string }) {
  const actualOrderId = params.orderId || params.id;
}
```

**RIGHT:**
```typescript
// Just use the better name
function getUserById(userId: string) {
  // Implementation
}

function createOrder(orderId: string) {
  // Implementation
}
```

**Key principles:**
- Don't keep deprecated functions
- Don't support multiple parameter formats
- Don't add compatibility shims
- If a name is bad, change it - delete the old one
- Clean breaks > gradual migration

### 4. Never Use Lint Suppressions

**WRONG:**
```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function process(data: any) {
  return data;
}

// biome-ignore lint/suspicious/noExplicitAny: legacy code
function processLegacy(data: any) {
  return data;
}

// @ts-ignore
const result = unsafeOperation();

/* eslint-disable */
function legacyCode() {
  // Bad code here
}
/* eslint-enable */
```

**RIGHT:**
```typescript
function processUserData(userData: UserData): ProcessedUserData {
  return {
    userId: userData.id,
    userName: userData.name,
    processedAt: new Date(),
  };
}

function performSafeOperation(): OperationResult {
  const validatedInput = validateInput();
  return executeOperation(validatedInput);
}

function modernImplementation(customer: Customer): Invoice {
  const invoiceItems = customer.orders.map(createInvoiceItem);
  return generateInvoice(invoiceItems);
}
```

**Key principles:**
- Fix the code instead of suppressing warnings
- Type everything properly - no `any`, no `@ts-ignore`
- If the linter complains, there's usually a good reason
- Write code that passes linting naturally
- Suppressions = technical debt
- No `eslint-disable`, `@ts-ignore`, `biome-ignore`, or any other suppressions

### 5. Code Must Pass Biome and TypeScript Checks

**WRONG:**
```typescript
// Code that has type errors
function processData(data) {  // Missing type annotation
  return data.map(item => item.value);  // No type safety
}

// Code that fails Biome checks
const unused = 'variable';  // Unused variable
let x = 1; x = 2;  // Unnecessary let when const would work

// Committing without running checks
// git commit -m "quick fix"
```

**RIGHT:**
```typescript
// Code with proper types
interface DataItem {
  value: string;
}

function processData(data: DataItem[]): string[] {
  return data.map(item => item.value);
}

// Clean code that passes all checks
const processedResults = calculateResults();
const finalValue = processedResults.total;

// Always verify before committing
// npm run typecheck  ✓
// npm run biome:check  ✓
```

**Key principles:**
- Run `tsc --noEmit` or equivalent before committing
- Run Biome checks before committing
- Fix all type errors - no `any` types
- Fix all Biome warnings - unused variables, incorrect patterns
- Never commit code that doesn't pass checks
- TypeScript strict mode should be enabled
- All code must be properly typed

**Required commands before commit:**
```bash
# TypeScript type check
npm run typecheck
# or
tsc --noEmit

# Biome check (lint + format)
npx biome check .
# or
npm run biome:check
```

## Hardcoded Values - Never Use Them

**WRONG:**
```typescript
if (user.role === 'admin') { }
const timeout = 5000;
const apiUrl = 'https://api.example.com';
const maxRetries = 3;
```

**RIGHT:**
```typescript
const USER_ROLE_ADMIN = 'admin';
const REQUEST_TIMEOUT_MILLISECONDS = 5000;
const API_BASE_URL = process.env.API_BASE_URL;
const MAXIMUM_RETRY_ATTEMPTS = 3;

if (user.role === USER_ROLE_ADMIN) { }
```

**Key principles:**
- Extract all magic numbers and strings to named constants
- Use SCREAMING_SNAKE_CASE for constants
- Constants should have descriptive, verbose names
- Environment-specific values come from env vars
- The constant name should explain what the value means

## Naming Conventions

### Variables

```typescript
// Bad
const d = new Date();
const arr = getData();
const temp = process(data);
const user1 = getUser();
const item2 = getItem();

// Good
const currentTimestamp = new Date();
const userAccounts = getData();
const processedCustomerData = process(data);
const primaryUser = getUser();
const secondaryItem = getItem();
```

### Functions

```typescript
// Bad
function get() { }
function process() { }
function handle() { }

// Good
function getUserById(userId: string) { }
function processPaymentTransaction(transaction: Transaction) { }
function handleFormSubmission(formData: FormData) { }
```

### Constants

```typescript
// Bad
const max = 100;
const url = 'https://...';

// Good
const MAXIMUM_UPLOAD_SIZE_BYTES = 100;
const PAYMENT_GATEWAY_API_URL = process.env.PAYMENT_GATEWAY_API_URL;
```

### Types/Interfaces

```typescript
// Bad
interface Props { }
type Data = { };

// Good
interface UserProfileComponentProps { }
type CustomerOrderData = { };
```

## Red Flags - Stop Immediately If You See

- Single letter variable names (except in tiny map/filter callbacks)
- Numbers in variable names (`user1`, `data2`, `temp3`)
- Abbreviations that aren't universal
- TODO comments for core functionality
- Placeholder implementations
- Commented out code "for reference"
- Functions that support "old and new" parameters
- Any form of `eslint-disable`
- Any form of `@ts-ignore`
- Any form of `biome-ignore`
- Any lint suppression comments
- TypeScript errors or warnings
- Biome check failures
- Unused variables or imports
- Missing type annotations
- Using `any` type
- Hardcoded strings or numbers (magic values)
- Generic names like `data`, `value`, `item`, `temp`

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Long names are verbose" | Descriptive names prevent bugs |
| "We'll implement this later" | Write complete code now or don't write it |
| "Need backward compatibility" | Clean breaks are better than tech debt |
| "Just this one lint suppression" | Fix the code, don't suppress the warning |
| "Everyone knows what this magic number means" | They don't - use a named constant |
| "It's just a temporary variable" | Temporary doesn't mean unclear |
| "I'll run the checks later" | Run checks before committing, always |
| "TypeScript is too strict" | Strict types prevent runtime errors |

## Checklist for Every Code Change

Before committing any code, verify:

- [ ] All variables have descriptive, verbose names
- [ ] No single-letter variables (except tiny scopes)
- [ ] No numbers in variable names (`user1`, `data2`, etc.)
- [ ] All functions are fully implemented (no placeholders)
- [ ] No TODO comments for core functionality
- [ ] No backward compatibility shims
- [ ] No deprecated functions kept around
- [ ] No `eslint-disable`, `@ts-ignore`, or `biome-ignore`
- [ ] No lint suppressions of any kind
- [ ] No hardcoded values - all extracted to named constants
- [ ] **TypeScript check passes (`tsc --noEmit` or `npm run typecheck`)**
- [ ] **Biome check passes (`npx biome check .` or `npm run biome:check`)**
- [ ] No unused variables or imports
- [ ] All types are explicit (no `any`)
- [ ] Code passes all linting without suppressions

## Examples

### Before (Wrong)

```typescript
function getData(id: string) {
  // TODO: Add validation
  const url = 'https://api.example.com/users';
  // @ts-ignore
  const res = fetch(`${url}/${id}`);
  return res;
}

const val = getData('123');
const x = val.map(i => i.name);
```

### After (Right)

```typescript
const USER_API_BASE_URL = process.env.USER_API_BASE_URL;

interface UserApiResponse {
  userId: string;
  userName: string;
  userEmail: string;
}

async function fetchUserById(userId: string): Promise<UserApiResponse> {
  if (!userId || userId.trim().length === 0) {
    throw new Error('User ID is required and cannot be empty');
  }

  const response = await fetch(`${USER_API_BASE_URL}/users/${userId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`);
  }

  const userData = await response.json();
  return userData;
}

const userResponse = await fetchUserById('123');
const userNames = userResponse.map(user => user.userName);
```

## Enforcement

**This skill is MANDATORY for all code changes.**

If you find yourself:
- Using vague variable names → Stop and rename
- Writing TODO comments → Stop and implement
- Adding backward compatibility → Stop and make a clean break
- Adding lint suppressions → Stop and fix the code
- Using magic values → Stop and extract to constants
- Skipping type checks → Stop and run `tsc --noEmit`
- Skipping Biome checks → Stop and run `npx biome check .`
- Committing with type errors → Stop and fix the types

**There are no exceptions.**

## Quick Decision Tree

1. **Writing a variable?** → Use a descriptive, verbose name
2. **Writing a function?** → Implement it completely, no placeholders
3. **Changing an API?** → Make a clean break, no backward compatibility
4. **Linter complaining?** → Fix the code, never suppress
5. **Using a value?** → Extract to a named constant
6. **Before committing?** → Run `tsc --noEmit` and `npx biome check .`

## Final Rule

```
Every line of code must be:
1. Clearly named with verbose, descriptive identifiers
2. Fully implemented with no placeholders
3. Breaking changes are fine - no backward compatibility
4. Passing all linters without suppressions
5. Free of hardcoded values
6. Pass TypeScript type checks
7. Pass Biome checks (lint + format)
```

Write code that reads like documentation.

## Pre-Commit Verification

**ALWAYS run these commands before committing:**

```bash
# 1. TypeScript type check
npm run typecheck
# or
tsc --noEmit

# 2. Biome check (lint + format)
npx biome check .
# or
npm run biome:check

# 3. If any errors, FIX them - never suppress or skip
```

**Only commit when all checks pass.**
