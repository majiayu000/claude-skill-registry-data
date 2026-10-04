---
name: composite
description: Compose objects into tree structures and treat individual objects and compositions uniformly.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Composite

Allows clients to treat individual objects (leaves) and groups of objects (composites) identically via a shared interface. Perfect for tree-shaped structures.

## When to Use

- You need to represent part-whole hierarchies (file system, UI component tree, org chart)
- Clients should be able to ignore the difference between single objects and groups
- Operations on a group should recursively apply to all children

## How to Apply

1. Define a `Component` interface with operations common to both leaves and containers
2. Create `Leaf` class implementing `Component` (no children)
3. Create `Composite` class implementing `Component`; holds a list of child `Component`s
4. Composite delegates operations to its children and combines results
5. Clients program to the `Component` interface

## Example

```ts
interface FileSystemEntry {
  getSize(): number;
  print(indent?: string): void;
}

class File implements FileSystemEntry {
  constructor(private name: string, private size: number) {}
  getSize() { return this.size; }
  print(indent = '') { console.log(`${indent}📄 ${this.name} (${this.size}B)`); }
}

class Directory implements FileSystemEntry {
  private children: FileSystemEntry[] = [];
  constructor(private name: string) {}
  add(e: FileSystemEntry) { this.children.push(e); }
  getSize() { return this.children.reduce((s, c) => s + c.getSize(), 0); }
  print(indent = '') {
    console.log(`${indent}📁 ${this.name}`);
    this.children.forEach(c => c.print(indent + '  '));
  }
}
```

## References

- [refactoring.guru/design-patterns/composite](https://refactoring.guru/design-patterns/composite)
