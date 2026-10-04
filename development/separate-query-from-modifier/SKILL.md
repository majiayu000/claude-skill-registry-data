---
name: separate-query-from-modifier
description: Split a method that both returns a value and changes state into two separate methods.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Separate Query from Modifier

A method that returns a value AND has side effects is unpredictable and hard to test. Separate it into a pure query and a dedicated command (Command-Query Separation principle).

## When to Use

- A method returns a value but also mutates state
- Callers cannot call the method safely just to read a value
- The method is difficult to test in isolation
- Applying CQRS or functional-style patterns

## How to Apply

1. Create a query method that returns the value (no side effects)
2. Modify the original method to return `void` (it becomes the command)
3. Update all callers: call the query first, then the command
4. Run tests

## Example

```ts
// Before — returns name AND sends alert
function checkSecurity(people: string[]): string {
  let found = '';
  for (const p of people) {
    if (p === 'Don') { sendAlert(); found = 'Don'; }
    if (p === 'John') { sendAlert(); found = 'John'; }
  }
  return found;
}

// After
function findMiscreant(people: string[]): string {
  if (people.includes('Don')) return 'Don';
  if (people.includes('John')) return 'John';
  return '';
}
function sendAlerts(people: string[]): void {
  if (people.some(p => p === 'Don' || p === 'John')) sendAlert();
}
// Caller:
const found = findMiscreant(people);
sendAlerts(people);
```

## References

- [refactoring.guru/separate-query-from-modifier](https://refactoring.guru/separate-query-from-modifier)
