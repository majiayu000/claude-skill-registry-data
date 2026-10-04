---
name: typescript-master
description: Advanced TypeScript expertise for building type-safe applications at scale. Use when designing complex type systems, creating generic utilities, implementing discriminated unions, fixing type errors, configuring tsconfig.json, working with conditional types/mapped types/template literals, or enforcing strict type safety across large codebases. Triggers on TypeScript types, generics, type inference, tsconfig, type errors, advanced types, or TypeScript best practices.
---

# TypeScript Master - Type Safety at Scale

**Purpose**: Master TypeScript for building type-safe, maintainable applications at scale

**Agent**: All FAANG Engineers
**Use When**: Building any TypeScript project, ensuring type safety, or refactoring JavaScript to TypeScript

---

## Overview

TypeScript is JavaScript with syntax for types, providing static type checking, better IDE support, and improved code quality.

**Core Philosophy**:
- Type safety prevents runtime errors
- Better developer experience (autocomplete, refactoring)
- Self-documenting code
- Gradual adoption (JavaScript is valid TypeScript)
- Scales to large codebases

---

## Core Concepts

### 1. Basic Types

```typescript
// Primitives
let name: string = "John"
let age: number = 30
let isActive: boolean = true
let nothing: null = null
let notDefined: undefined = undefined

// Arrays
let numbers: number[] = [1, 2, 3]
let strings: Array<string> = ["a", "b", "c"]

// Tuples
let tuple: [string, number] = ["hello", 10]

// Enums
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Pending = "PENDING"
}

// Any (avoid when possible)
let anything: any = "could be anything"

// Unknown (safer than any)
let value: unknown = "something"
if (typeof value === "string") {
  value.toUpperCase() // Type narrowing
}

// Never (for functions that never return)
function throwError(message: string): never {
  throw new Error(message)
}
```

### 2. Interfaces vs Types

```typescript
// Interface (extensible)
interface User {
  id: number
  name: string
  email: string
}

interface Admin extends User {
  role: string
}

// Type (flexible)
type Point = {
  x: number
  y: number
}

type ID = string | number // Union
type Callback = (data: string) => void // Function type

// Use Interface for objects, Type for unions/intersections
```

### 3. Generics

```typescript
// Generic function
function identity<T>(arg: T): T {
  return arg
}

const num = identity<number>(42)
const str = identity("hello") // Type inference

// Generic interface
interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

const userResponse: ApiResponse<User> = {
  data: { id: 1, name: "John", email: "john@example.com" },
  status: 200,
  message: "Success"
}

// Generic constraints
interface HasLength {
  length: number
}

function logLength<T extends HasLength>(arg: T): T {
  console.log(arg.length)
  return arg
}

logLength("hello") // ✓
logLength([1, 2, 3]) // ✓
// logLength(42) // ✗ number doesn't have length
```

### 4. Advanced Types

```typescript
// Union Types
type Status = "pending" | "approved" | "rejected"

function handleStatus(status: Status) {
  if (status === "pending") {
    // TypeScript knows status is "pending"
  }
}

// Intersection Types
type Timestamped = {
  createdAt: Date
  updatedAt: Date
}

type Post = {
  title: string
  content: string
} & Timestamped

// Utility Types
type User = {
  id: number
  name: string
  email: string
  password: string
}

type UserProfile = Omit<User, "password"> // Remove password
type PartialUser = Partial<User> // All fields optional
type RequiredUser = Required<PartialUser> // All fields required
type ReadonlyUser = Readonly<User> // All fields readonly
type UserKeys = keyof User // "id" | "name" | "email" | "password"

// Pick specific fields
type UserCredentials = Pick<User, "email" | "password">

// Record type
type Roles = "admin" | "user" | "guest"
type Permissions = Record<Roles, string[]>

const permissions: Permissions = {
  admin: ["read", "write", "delete"],
  user: ["read", "write"],
  guest: ["read"]
}
```

### 5. Type Guards & Narrowing

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase()
  } else {
    return value.toFixed(2)
  }
}

// instanceof guard
class Dog {
  bark() { console.log("Woof!") }
}

class Cat {
  meow() { console.log("Meow!") }
}

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark()
  } else {
    animal.meow()
  }
}

// Custom type guard
interface Fish {
  swim: () => void
}

interface Bird {
  fly: () => void
}

function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined
}

function move(pet: Fish | Bird) {
  if (isFish(pet)) {
    pet.swim()
  } else {
    pet.fly()
  }
}

// Discriminated unions
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; size: number }
  | { kind: "rectangle"; width: number; height: number }

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2
    case "square":
      return shape.size ** 2
    case "rectangle":
      return shape.width * shape.height
  }
}
```

---

## Best Practices

### 1. Avoid `any`, Use `unknown`

```typescript
// ❌ Bad: any disables type checking
function process(data: any) {
  return data.value.toUpperCase() // No error, but could crash
}

// ✅ Good: unknown requires type checking
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    const value = (data as { value: string }).value
    if (typeof value === "string") {
      return value.toUpperCase()
    }
  }
  throw new Error("Invalid data")
}
```

### 2. Prefer Interfaces for Objects

```typescript
// ✅ Good: Interface for object shapes
interface User {
  id: number
  name: string
}

// ✅ Good: Type for unions, primitives
type ID = string | number
type Status = "active" | "inactive"
```

### 3. Use Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitThis": true
  }
}
```

### 4. Type Function Parameters & Returns

```typescript
// ✅ Good: Explicit types
function add(a: number, b: number): number {
  return a + b
}

// ❌ Avoid: Implicit returns (less clear)
function add(a: number, b: number) {
  return a + b // Inferred, but not explicit
}
```

### 5. Use Const Assertions

```typescript
// Without const assertion
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000
}
// Type: { apiUrl: string, timeout: number }

// With const assertion
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000
} as const
// Type: { readonly apiUrl: "https://api.example.com", readonly timeout: 5000 }
```

---

## Common Patterns

### API Response Typing

```typescript
interface ApiResponse<T> {
  data: T
  error?: string
  status: number
}

interface User {
  id: number
  name: string
  email: string
}

async function fetchUser(id: number): Promise<ApiResponse<User>> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}

// Usage
const result = await fetchUser(1)
if (result.error) {
  console.error(result.error)
} else {
  console.log(result.data.name) // TypeScript knows data is User
}
```

### Event Handlers

```typescript
// React event handlers
import { ChangeEvent, FormEvent } from 'react'

function Form() {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    // handle submit
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
    </form>
  )
}
```

### Async/Await with Types

```typescript
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  return await response.json()
}

// Usage
interface Todo {
  id: number
  title: string
  completed: boolean
}

const todo = await fetchData<Todo>("/api/todos/1")
console.log(todo.title) // TypeScript knows todo is Todo
```

---

## React + TypeScript

### Component Props

```typescript
import { FC, ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick: () => void
  variant?: "primary" | "secondary"
  disabled?: boolean
}

const Button: FC<ButtonProps> = ({
  children,
  onClick,
  variant = "primary",
  disabled = false
}) => {
  return (
    <button onClick={onClick} disabled={disabled} className={variant}>
      {children}
    </button>
  )
}

// Usage
<Button onClick={() => console.log("Clicked")} variant="primary">
  Click Me
</Button>
```

### Hooks with Types

```typescript
import { useState, useEffect } from 'react'

// useState with explicit type
const [user, setUser] = useState<User | null>(null)

// useState with initial value (inferred)
const [count, setCount] = useState(0) // Type: number

// useEffect
useEffect(() => {
  async function loadUser() {
    const data = await fetchUser(1)
    setUser(data.data)
  }
  loadUser()
}, [])
```

---

## Node.js + TypeScript

### Express Server

```typescript
import express, { Request, Response, NextFunction } from 'express'

const app = express()

interface User {
  id: number
  name: string
}

// Typed route handler
app.get('/users/:id', async (req: Request, res: Response) => {
  const id = parseInt(req.params.id)
  const user: User = await db.findUser(id)
  res.json(user)
})

// Custom middleware with types
interface AuthRequest extends Request {
  user?: User
}

const authMiddleware = (
  req: AuthRequest,
  res: Response,
  next: NextFunction
) => {
  const token = req.headers.authorization
  if (!token) {
    return res.status(401).json({ error: "Unauthorized" })
  }
  req.user = verifyToken(token)
  next()
}
```

---

## Configuration

### tsconfig.json (Recommended)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## When to Use TypeScript

✅ **Always use TypeScript for**:
- Production applications
- Team projects (multiple developers)
- Long-lived codebases
- Libraries/packages (for better DX)
- Large-scale applications

❌ **May skip TypeScript for**:
- Quick prototypes/experiments
- Very small scripts
- Learning basic JavaScript

---

**Remember**: TypeScript is JavaScript with types. Start with basic types, use `strict` mode, and let the compiler help you write better code.

**Created**: 2026-02-04
**Maintained By**: All FAANG Engineers
**Version**: TypeScript 5+
