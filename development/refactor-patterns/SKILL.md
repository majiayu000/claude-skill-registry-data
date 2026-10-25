---
name: refactor-patterns"
description: Common refactoring recipes and code transformation patterns. Use when improving code structure, reducing complexity, or modernizing legacy code.
---

# Refactor Patterns Skill

## Extract Method/Function

### Before
```typescript
function processOrder(order: Order): Receipt {
  // Validate
  if (!order.items.length) throw new Error("Empty order");
  if (!order.customer.email) throw new Error("No email");
  
  // Calculate totals
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
  
  // Generate receipt
  const receipt = {
    orderId: order.id,
    items: order.items,
    subtotal,
    tax,
    total,
    timestamp: new Date()
  };
  
  // Save
  db.save(receipt);
  email.send(order.customer.email, receipt);
  
  return receipt;
}
```

### After
```typescript
function processOrder(order: Order): Receipt {
  validateOrder(order);
  const { subtotal, tax, total } = calculateTotals(order.items);
  const receipt = createReceipt(order, subtotal, tax, total);
  persistAndNotify(receipt, order.customer.email);
  return receipt;
}

function validateOrder(order: Order): void {
  if (!order.items.length) throw new Error("Empty order");
  if (!order.customer.email) throw new Error("No email");
}

function calculateTotals(items: OrderItem[]): { subtotal: number; tax: number; total: number } {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * 0.1;
  return { subtotal, tax, total: subtotal + tax };
}

function createReceipt(order: Order, subtotal: number, tax: number, total: number): Receipt {
  return { orderId: order.id, items: order.items, subtotal, tax, total, timestamp: new Date() };
}

function persistAndNotify(receipt: Receipt, email: string): void {
  db.save(receipt);
  email.send(email, receipt);
}
```

## Replace Conditional with Polymorphism

### Before
```typescript
function calculateShipping(order: Order): number {
  switch (order.shippingMethod) {
    case "standard": return 5.99;
    case "express": return 15.99;
    case "overnight": return 29.99;
    case "pickup": return 0;
    default: throw new Error("Unknown method");
  }
}
```

### After
```typescript
interface ShippingStrategy {
  calculate(order: Order): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(order: Order): number { return 5.99; }
}

class ExpressShipping implements ShippingStrategy {
  calculate(order: Order): number { return 15.99; }
}

class OvernightShipping implements ShippingStrategy {
  calculate(order: Order): number { return 29.99; }
}

class PickupShipping implements ShippingStrategy {
  calculate(order: Order): number { return 0; }
}

const strategies: Record<string, ShippingStrategy> = {
  standard: new StandardShipping(),
  express: new ExpressShipping(),
  overnight: new OvernightShipping(),
  pickup: new PickupShipping()
};

function calculateShipping(order: Order): number {
  const strategy = strategies[order.shippingMethod];
  if (!strategy) throw new Error("Unknown method");
  return strategy.calculate(order);
}
```

## Introduce Parameter Object

### Before
```typescript
function createUser(
  name: string,
  email: string,
  password: string,
  role: string,
  preferences: Preferences,
  metadata: Record<string, any>
): User { ... }
```

### After
```typescript
interface CreateUserParams {
  name: string;
  email: string;
  password: string;
  role: Role;
  preferences?: Preferences;
  metadata?: Record<string, any>;
}

function createUser(params: CreateUserParams): User { ... }

// Usage
createUser({
  name: "John",
  email: "john@example.com",
  password: "secret",
  role: "user",
  preferences: { theme: "dark" }
});
```

## Replace Magic Numbers/Strings

### Before
```typescript
if (user.status === 1) { ... }
if (event.type === "click") { ... }
setTimeout(fn, 30000);
```

### After
```typescript
enum UserStatus {
  Active = 1,
  Inactive = 2,
  Suspended = 3
}

const EventTypes = {
  Click: "click",
  Hover: "hover",
  Submit: "submit"
} as const;

const TIMEOUTS = {
  Short: 5000,
  Medium: 15000,
  Long: 30000
} as const;

if (user.status === UserStatus.Active) { ... }
if (event.type === EventTypes.Click) { ... }
setTimeout(fn, TIMEOUTS.Long);
```

## Guard Clauses

### Before
```typescript
function processPayment(payment: Payment): Result {
  if (payment.amount > 0) {
    if (payment.method) {
      if (payment.method.isValid()) {
        if (payment.customer.verified) {
          // ... actual logic
        }
      }
    }
  }
  return { success: false };
}
```

### After
```typescript
function processPayment(payment: Payment): Result {
  if (payment.amount <= 0) return { success: false, reason: "Invalid amount" };
  if (!payment.method) return { success: false, reason: "No payment method" };
  if (!payment.method.isValid()) return { success: false, reason: "Invalid method" };
  if (!payment.customer.verified) return { success: false, reason: "Customer not verified" };
  
  // ... actual logic
  return { success: true };
}
```

## Consolidate Duplicate Code

### Before
```typescript
function formatUserName(user: User): string {
  return `${user.firstName} ${user.lastName}`.trim();
}

function formatAdminName(admin: Admin): string {
  return `${admin.firstName} ${admin.lastName}`.trim();
}

function formatGuestName(guest: Guest): string {
  return `${guest.firstName} ${guest.lastName}`.trim();
}
```

### After
```typescript
interface Named {
  firstName: string;
  lastName: string;
}

function formatName(entity: Named): string {
  return `${entity.firstName} ${entity.lastName}`.trim();
}
```

## Replace Loop with Pipeline

### Before
```typescript
const activeUsers = [];
for (const user of users) {
  if (user.isActive) {
    const profile = fetchProfile(user.id);
    if (profile.completed) {
      activeUsers.push({ ...user, profile });
    }
  }
}
```

### After
```typescript
const activeUsers = users
  .filter(u => u.isActive)
  .map(u => ({ ...u, profile: fetchProfile(u.id) }))
  .filter(u => u.profile.completed);
```

## When to Use

- Large functions (>20 lines)
- Deep nesting (>3 levels)
- Duplicate code (3+ occurrences)
- Switch statements on type
- Magic numbers/strings
- Long parameter lists (4+ params)
- Feature envy (method uses other object's data more than its own)