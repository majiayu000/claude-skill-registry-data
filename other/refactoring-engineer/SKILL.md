---
name: refactoring-engineer
version: "2.0"
trigger: refactoring, tech debt, code cleanup, restructure, modernize
description: Code refactoring strategies, technical debt reduction, architecture modernization, and code quality improvement. Use when refactoring code, modernizing legacy code, reducing complexity, or improving maintainability.
---

# Refactoring Engineer

## Refactoring Patterns

### Extract Function
```typescript
// Before
function processOrder(order: Order) {
  console.log(`Processing order ${order.id}`);
  
  // Validate items
  for (const item of order.items) {
    if (item.quantity <= 0) throw new Error('Invalid quantity');
    if (!item.price || item.price < 0) throw new Error('Invalid price');
  }
  
  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  
  // Apply discount
  if (order.coupon) {
    total = total * (1 - order.coupon.discount);
  }
  
  return { orderId: order.id, total };
}

// After
function processOrder(order: Order) {
  console.log(`Processing order ${order.id}`);
  
  validateOrderItems(order.items);
  const subtotal = calculateSubtotal(order.items);
  const total = applyDiscount(subtotal, order.coupon);
  
  return { orderId: order.id, total };
}

function validateOrderItems(items: OrderItem[]) {
  for (const item of items) {
    if (item.quantity <= 0) throw new Error('Invalid quantity');
    if (!item.price || item.price < 0) throw new Error('Invalid price');
  }
}

function calculateSubtotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(amount: number, coupon?: Coupon): number {
  return coupon ? amount * (1 - coupon.discount) : amount;
}
```

### Replace Conditional with Polymorphism
```typescript
// Before
function calculateShipping(order: Order): number {
  if (order.shippingType === 'ground') {
    return order.weight * 1.5;
  } else if (order.shippingType === 'express') {
    return order.weight * 3 + 10;
  } else if (order.shippingType === 'overnight') {
    return order.weight * 5 + 25;
  }
  throw new Error('Unknown shipping type');
}

// After
interface ShippingStrategy {
  calculate(weight: number): number;
}

class GroundShipping implements ShippingStrategy {
  calculate(weight: number) {
    return weight * 1.5;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(weight: number) {
    return weight * 3 + 10;
  }
}

class OvernightShipping implements ShippingStrategy {
  calculate(weight: number) {
    return weight * 5 + 25;
  }
}

const strategies: Record<string, ShippingStrategy> = {
  ground: new GroundShipping(),
  express: new ExpressShipping(),
  overnight: new OvernightShipping()
};

function calculateShipping(order: Order): number {
  const strategy = strategies[order.shippingType];
  if (!strategy) throw new Error('Unknown shipping type');
  return strategy.calculate(order.weight);
}
```

### Replace Magic Numbers
```typescript
// Before
if (user.tier === 3) {
  return 100;
}

// After
const TIERS = {
  BASIC: 1,
  STANDARD: 2,
  PREMIUM: 3,
  ENTERPRISE: 4
} as const;

const RATE_LIMITS = {
  [TIERS.BASIC]: 10,
  [TIERS.STANDARD]: 50,
  [TIERS.PREMIUM]: 100,
  [TIERS.ENTERPRISE]: 1000
} as const;

if (user.tier === TIERS.PREMIUM) {
  return RATE_LIMITS[TIERS.PREMIUM];
}
```

## Legacy Code Modernization

### Callback to Async/Await
```typescript
// Before
function getUser(id: string, callback: (err: Error | null, user?: User) => void) {
  db.query('SELECT * FROM users WHERE id = ?', [id], (err, results) => {
    if (err) return callback(err);
    callback(null, results[0]);
  });
}

// After
async function getUser(id: string): Promise<User | null> {
  const [user] = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  return user || null;
}
```

### Class to Functional with Hooks
```typescript
// Before
class UserList extends React.Component {
  state = { users: [], loading: false };
  
  componentDidMount() {
    this.loadUsers();
  }
  
  loadUsers = async () => {
    this.setState({ loading: true });
    const users = await fetchUsers();
    this.setState({ users, loading: false });
  };
  
  render() {
    const { users, loading } = this.state;
    return loading ? <Spinner /> : <List users={users} />;
  }
}

// After
function UserList() {
  const { data: users, isLoading } = useQuery(['users'], fetchUsers);
  return isLoading ? <Spinner /> : <List users={users} />;
}
```

## Complexity Reduction

### Reduce Nesting
```typescript
// Before
function process(data: Data) {
  if (data) {
    if (data.items) {
      if (data.items.length > 0) {
        for (const item of data.items) {
          if (item.active) {
            processItem(item);
          }
        }
      }
    }
  }
}

// After
function process(data: Data) {
  if (!data?.items?.length) return;
  
  for (const item of data.items) {
    if (!item.active) continue;
    processItem(item);
  }
}
```

### Early Returns
```typescript
// Before
function validateUser(user: User): boolean {
  let isValid = true;
  
  if (!user.email) {
    isValid = false;
  } else if (!user.email.includes('@')) {
    isValid = false;
  } else if (user.email.length < 5) {
    isValid = false;
  }
  
  return isValid;
}

// After
function validateUser(user: User): boolean {
  if (!user.email) return false;
  if (!user.email.includes('@')) return false;
  if (user.email.length < 5) return false;
  return true;
}
```

## Refactoring Checklist

- [ ] Extract long functions
- [ ] Remove duplicate code
- [ ] Rename unclear variables
- [ ] Replace magic numbers
- [ ] Simplify conditionals
- [ ] Reduce nesting depth
- [ ] Add type safety
- [ ] Update tests
- [ ] Run full test suite
- [ ] Measure performance impact
