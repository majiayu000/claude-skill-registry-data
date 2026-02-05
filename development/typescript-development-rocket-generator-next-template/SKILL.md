---
name: typescript-development
description: Develop typescript frontend and/or backend 
---
# TypeScript Development Guidelines

## Core Requirements
- TypeScript must be used for all code generation
- Never use the `any` type as it will break the build
- Always use Shadcn and Tailwind CSS, but implement without using Card components
- Avoid typing components with React.FC
- Use const for component declarations instead of function
- Follow React's composable patterns

## State Management and Performance
- Minimize use of useState and useEffect hooks
- Prefer computed state where possible
- Use useMemo and useCallback when necessary to prevent unnecessary re-renders
- Prioritize server actions and useActionState
- Fall back to fetch and API route handlers when server actions aren't suitable
- When components need to modify data, they should receive server actions as props

## Component Architecture
- Prioritize server components whenever possible
- Create client components only when necessary
- Utilize Suspense and streaming capabilities where possible
- For components requiring specific functionality not tightly coupled to the component itself, create higher-order components
- Group related components, hooks, and functions in the same file when it makes semantic sense for easier distribution and usage

## Forms and Data Handling
- Implement forms as server-side components
- Only use client components for dynamic operations (e.g., user registration sections)
- Always validate inputs using Zod in server actions and API endpoints
- Always HTML escape text content

## Custom Hooks
- Create custom hooks to encapsulate specific logic when grouping useState and useEffect makes sense
- Custom hooks should be focused and reusable

## Best Practices
- Group related components, hooks, and functions in the same file when it makes semantic sense for easier distribution and usage
- Follow consistent naming conventions
- Maintain clear separation of concerns
- Ensure proper error handling
- Implement proper type safety throughout the codebase