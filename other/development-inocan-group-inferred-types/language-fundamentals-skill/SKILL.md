---
name: language-fundamentals-skill
description: Master programming languages from Python to Rust. Learn core concepts like variables, OOP, functional programming, algorithms, data structures, and competitive programming techniques. Use when exploring programming languages, learning CS fundamentals, or preparing for technical interviews.
---

# Language & Fundamentals Skill

Complete guide to programming languages and computer science fundamentals from absolute beginner to expert level.

## Quick Start

### Choose Your Learning Path

```
Beginner → Intermediate → Advanced → Expert
   ↓           ↓            ↓         ↓
 Syntax    Paradigms   Patterns  Optimization
```

### Get Started in 5 Steps

1. **Pick a Language**:
   - Start: Python, JavaScript, or Go
   - Choose based on your goals

2. **Learn Fundamentals**:
   - Variables and data types
   - Control flow (if, loops, functions)
   - Basic data structures

3. **Understand OOP/FP**:
   - Choose paradigm (OOP preferred for beginners)
   - Classes, inheritance, polymorphism
   - Or: Functions, immutability, higher-order functions

4. **Master Algorithms & DS**:
   - Arrays, linked lists, trees, graphs
   - Sorting, searching, dynamic programming

5. **Practice & Specialize**:
   - LeetCode or CodeWars (50+ problems)
   - Build projects in your chosen language

---

## Programming Languages Overview

### **Tier 1: Best for Beginners**

#### Python
- **Why**: Readability, versatility, massive ecosystem
- **Use Cases**: Data science, web, automation, teaching
- **Roadmap**: https://roadmap.sh/python
- **Key Concepts**:
  ```python
  # Variables and types
  name = "Alice"  # Dynamic typing
  age = 30

  # Functions
  def greet(name):
      return f"Hello, {name}!"

  # List comprehension
  squares = [x**2 for x in range(10)]

  # OOP
  class Person:
      def __init__(self, name):
          self.name = name
  ```
- **Learning Time**: 3-6 months to intermediate
- **Job Market**: 🟢 Excellent (data science, web, ML)

#### JavaScript
- **Why**: Runs everywhere (browser, Node.js, mobile)
- **Use Cases**: Web frontend, backend (Node), full-stack
- **Roadmap**: https://roadmap.sh/javascript
- **Key Concepts**:
  ```javascript
  // Variables (let, const)
  const name = "Alice";
  let count = 0;

  // Functions (arrow functions)
  const greet = (name) => `Hello, ${name}!`;

  // Objects and arrays
  const user = { name: "Alice", age: 30 };
  const numbers = [1, 2, 3, 4, 5];

  // Async/await
  async function fetchData() {
      const data = await fetch('/api/data');
      return data.json();
  }
  ```
- **Learning Time**: 3-6 months to intermediate
- **Job Market**: 🟢 Excellent (web development dominant)

### **Tier 2: Popular & Powerful**

#### Go (Golang)
- **Why**: Fast, simple, excellent for concurrency
- **Use Cases**: Cloud infrastructure, microservices, DevOps tools
- **Roadmap**: https://roadmap.sh/golang
- **Key Concepts**:
  ```go
  package main
  import "fmt"

  // Simple syntax
  func greet(name string) string {
      return fmt.Sprintf("Hello, %s!", name)
  }

  // Goroutines for concurrency
  go func() {
      fmt.Println("Running concurrently")
  }()

  // Interfaces (duck typing)
  type Reader interface {
      Read(p []byte) (n int, err error)
  }
  ```
- **Learning Time**: 4-8 months to intermediate
- **Job Market**: 🟢 Growing (DevOps, cloud, microservices)

#### Java
- **Why**: Enterprise standard, strong typing, JVM ecosystem
- **Use Cases**: Enterprise apps, Android, large systems
- **Roadmap**: https://roadmap.sh/java
- **Key Concepts**:
  ```java
  public class Person {
      private String name;
      private int age;

      public Person(String name, int age) {
          this.name = name;
          this.age = age;
      }

      // Streams API
      List<Person> adults = people.stream()
          .filter(p -> p.getAge() >= 18)
          .collect(Collectors.toList());
  }
  ```
- **Learning Time**: 6-12 months to intermediate
- **Job Market**: 🟢 Excellent (enterprise, Android)

#### TypeScript
- **Why**: JavaScript with types (better than plain JS)
- **Use Cases**: Full-stack web, large JavaScript projects
- **Roadmap**: https://roadmap.sh/typescript
- **Key Concepts**:
  ```typescript
  // Type annotations
  interface User {
      name: string;
      age: number;
  }

  // Generic functions
  function getValue<T>(arr: T[], index: number): T {
      return arr[index];
  }

  // Union types
  type Response = Success | Error;
  ```
- **Learning Time**: 1-2 months after JavaScript
- **Job Market**: 🟢 Excellent (web development)

#### Rust
- **Why**: Memory safety, performance, no garbage collector
- **Use Cases**: System programs, embedded, performance-critical
- **Roadmap**: https://roadmap.sh/rust
- **Key Concepts**:
  ```rust
  // Ownership system (unique selling point)
  let s1 = String::from("hello");
  let s2 = s1; // s1 is moved, can't use it anymore

  // Borrowing
  let s3 = &s1;  // Immutable borrow
  let s4 = &mut s1;  // Mutable borrow

  // Pattern matching
  match value {
      Some(x) => println!("Value: {}", x),
      None => println!("No value"),
  }
  ```
- **Learning Time**: 8-16 months to intermediate
- **Job Market**: 🟡 Growing (systems programming, Web3)

### **Tier 3: Specialized**

#### C++
- **Why**: Maximum performance, used in games, systems
- **Use Cases**: Game engines, high-performance computing
- **Roadmap**: https://roadmap.sh/cpp
- **Job Market**: 🟢 Solid (games, systems, performance)

#### PHP
- **Why**: Web server scripting language (legacy but still common)
- **Use Cases**: Web development, server-side rendering
- **Roadmap**: https://roadmap.sh/php
- **Job Market**: 🟡 Declining (but still many jobs)

#### Kotlin
- **Why**: Modern JVM language, official Android language
- **Use Cases**: Android development, JVM applications
- **Roadmap**: https://roadmap.sh/kotlin
- **Job Market**: 🟡 Growing in Android ecosystem

#### Swift
- **Why**: Modern iOS/macOS language
- **Use Cases**: iOS, macOS, watchOS development
- **Roadmap**: https://roadmap.sh/swift
- **Job Market**: 🟢 Solid (iOS development)

---

## Computer Science Fundamentals

### **Data Structures**

**Essential DS Cheat Sheet:**

| Structure | Insert | Search | Delete | Use Case |
|-----------|--------|--------|--------|----------|
| Array | O(n) | O(n) | O(n) | Random access |
| Linked List | O(1) | O(n) | O(1) | Sequential access |
| Hash Table | O(1)* | O(1)* | O(1)* | Key-value storage |
| Binary Tree | O(log n)* | O(log n)* | O(log n)* | Hierarchical data |
| Graph | - | O(V+E) | - | Networks, relationships |

*Average case, depends on implementation

### **Essential Algorithms**

**1. Sorting Algorithms**
```
Quick Sort:   O(n log n) average, in-place, most common
Merge Sort:   O(n log n) guaranteed, stable, parallel-friendly
Heap Sort:    O(n log n), in-place
Bubble Sort:  O(n²) - avoid, only for learning
```

**2. Searching**
```
Binary Search:  O(log n) on sorted arrays
Linear Search:  O(n) on unsorted
Hash Lookup:    O(1) average
```

**3. Dynamic Programming**
```
Common patterns:
- Fibonacci (overlapping subproblems)
- Longest Common Subsequence (optimal substructure)
- Knapsack Problem (decision trees)
```

### **Big O Complexity Analysis**

```
O(1)      → Constant    (best)
O(log n)  → Logarithmic
O(n)      → Linear
O(n log n)→ Linearithmic
O(n²)     → Quadratic
O(n³)     → Cubic
O(2ⁿ)     → Exponential
O(n!)     → Factorial   (worst)
```

**Space Complexity**: Same analysis applies to memory usage

---

## Programming Paradigms

### **Object-Oriented Programming (OOP)**

The dominant paradigm. Four pillars:

```
1. Encapsulation   - Hide internal state, expose interface
2. Inheritance     - Reuse code through class hierarchies
3. Polymorphism    - Same interface, different implementations
4. Abstraction     - Deal with essential features only
```

**Example in Python:**
```python
# Encapsulation + Abstraction
class Animal:
    def __init__(self, name):
        self.__name = name  # Private

    # Polymorphism - override in subclasses
    def speak(self):
        pass

# Inheritance
class Dog(Animal):
    def speak(self):
        return f"{self.__name} says Woof!"
```

### **Functional Programming (FP)**

Alternative paradigm gaining popularity.

```
Core concepts:
- Pure functions    - No side effects
- Immutability     - Don't modify data
- First-class functions - Functions as values
- Higher-order functions - Functions that operate on functions
```

**Example in JavaScript:**
```javascript
// Pure function
const add = (a, b) => a + b;

// Higher-order function
const map = (fn, arr) => arr.map(fn);

// Immutability
const newList = [...oldList, newItem];
```

---

## Interview Preparation

### **LeetCode Problem Categories**

Target these in order of importance:

1. **Arrays & Hashing** (25% of interviews)
   - Two Sum, Contains Duplicate
   - Valid Anagram, Group Anagrams

2. **Two Pointers** (15%)
   - Valid Palindrome
   - Max Water Container

3. **Sliding Window** (15%)
   - Best Time to Buy Stock
   - Longest Substring Without Repeating

4. **Stack** (10%)
   - Valid Parentheses
   - Daily Temperatures

5. **Binary Search** (10%)
   - Binary Search, Search in Rotated Array

6. **Linked List** (10%)
   - Reverse Linked List
   - Merge k Sorted Lists

7. **Trees & Graphs** (10%)
   - Inorder/Preorder/Postorder Traversal
   - Lowest Common Ancestor

8. **Greedy & DP** (5%)
   - Jump Game, Coin Change

### **Study Plan**

```
Week 1-2: Arrays, Hashing, Two Pointers (Master basics)
Week 3-4: Strings, Sliding Window (Pattern recognition)
Week 5-6: Linked Lists, Stack (Data structure manipulation)
Week 7-8: Trees, Graphs (Traversals and patterns)
Week 9-10: Dynamic Programming (Complex problems)
Week 11-12: Mock interviews (Practice under pressure)
```

---

## Competitive Programming

**For algorithm competitions and contests:**

### **Key Concepts**
- Time limits: Usually 1-2 seconds
- Memory limits: Usually 256MB
- Input/Output optimization critical
- Mathematical insight often needed

### **Common Techniques**
- **Brute Force**: Solve correctly first
- **Optimization**: Reduce time complexity
- **Math**: Number theory, combinatorics
- **Graph Theory**: DFS, BFS, shortest paths
- **DP**: Overlapping subproblems

### **Platforms**
- Codeforces: Most popular, weekly contests
- AtCoder: High-quality, Japanese contests
- TopCoder: Longer format competitions
- HackerRank: Good for learning

---

## Learning Resources

### **By Language**
- **Python**: Real Python, Codecademy
- **JavaScript**: Eloquent JavaScript, freeCodeCamp
- **Go**: Official tour, Go by Example
- **Rust**: The Rust Book, Rust by Example

### **Algorithms & Data Structures**
- Introduction to Algorithms (MIT)
- Data Structures Easy to Advanced Course
- LeetCode Solutions: Community explanations

### **Practice Platforms**
- LeetCode: 3000+ problems, mock interviews
- CodeWars: Gamified learning
- HackerRank: Structured problem sets
- Project Euler: Math-heavy problems

---

## Skill Progression Checklist

- [ ] Chosen a language to focus on
- [ ] Completed basic syntax tutorial (1-2 weeks)
- [ ] Solved 10-20 easy LeetCode problems
- [ ] Understand variables, functions, control flow
- [ ] Know basic data structures (array, list, dict, set)
- [ ] Completed 1-2 small projects (calculator, todo app)
- [ ] Understand OOP or FP concepts
- [ ] Solved 30-50 medium LeetCode problems
- [ ] Know algorithms (sorting, searching, recursion)
- [ ] Understand Big O notation
- [ ] Ready to interview or build real projects!

---

**Source**: https://roadmap.sh/python, https://roadmap.sh/javascript, https://roadmap.sh/java, and more
