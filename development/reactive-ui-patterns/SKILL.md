---
name: "reactive-ui-patterns"
description: "Build reactive user interfaces by orchestrating FixiPlug state management and DOM manipulation. Use when creating dynamic interfaces that respond to application state changes, coordinate async operations, or implement event-driven UI updates."
tags:
  - "ui"
  - "reactive"
  - "patterns"
  - "state-management"
  - "dom-manipulation"
  - "workflow"
  - "ajax"
  - "best-practices"
version: "1.0.0"
level: "intermediate"
author: "FixiPlug Team"
references:
  - "stateTrackerPlugin"
  - "fixiAgentPlugin"
  - "introspectionPlugin"
---

# Reactive UI Patterns with FixiPlug

## Overview

This skill teaches you to build reactive user interfaces by combining two FixiPlug plugins:

1. **State Tracker Plugin** - Manages application state transitions
2. **Fixi-Agent Plugin** - Provides declarative DOM manipulation with fx- attributes

The key pattern: **state drives UI updates**, creating a unidirectional data flow similar to modern reactive frameworks.

## Core Concepts

### State-Driven UI

Instead of directly manipulating the DOM, you:
1. Update application state via `api:setState`
2. Listen for state transitions via `state:transition` events
3. Inject/update UI in response to state changes via `api:injectFxHtml`

This separates business logic (state) from presentation (DOM).

### Declarative AJAX with fx- Attributes

The fixi-agent plugin allows you to inject HTML with special `fx-` attributes that handle AJAX requests declaratively:

- `fx-action` - The URL to fetch
- `fx-method` - HTTP method (GET, POST, etc.)
- `fx-target` - Where to put the response
- `fx-swap` - How to swap (innerHTML, outerHTML, etc.)
- `fx-trigger` - What event triggers the request

## Pattern 1: State-Driven Loading Indicator

**Use Case:** Show/hide loading indicator based on async operation state

```javascript
// Step 1: Define state machine
await api:registerStateSchema({
  states: ['idle', 'loading', 'success', 'error'],
  transitions: {
    idle: ['loading'],
    loading: ['success', 'error'],
    success: ['idle'],
    error: ['idle']
  },
  initial: 'idle'
})

// Step 2: Create UI container
await api:injectFxHtml({
  html: '<div id="status-container"></div>',
  selector: '#app',
  position: 'beforeend'
})

// Step 3: Listen for state changes (in a plugin)
ctx.on('state:entered:loading', () => {
  api:injectFxHtml({
    html: '<div class="spinner">Loading...</div>',
    selector: '#status-container',
    position: 'innerHTML'
  })
})

ctx.on('state:entered:success', (event) => {
  api:injectFxHtml({
    html: `<div class="success">${event.data.message}</div>`,
    selector: '#status-container',
    position: 'innerHTML'
  })
})

// Step 4: Trigger async operation
await api:setState({ state: 'loading' })
// ... perform async work ...
await api:setState({
  state: 'success',
  data: { message: 'Data loaded!' }
})
```

## Pattern 2: Progressive Enhancement with fx-action

**Use Case:** Start with a basic button, enhance it with reactive behavior

```javascript
// Step 1: Inject basic interactive element
await api:injectFxHtml({
  html: `
    <button
      fx-action="/api/data"
      fx-target="#result"
      fx-swap="innerHTML"
      fx-trigger="click">
      Load Data
    </button>
    <div id="result"></div>
  `,
  selector: '#app',
  position: 'beforeend'
})

// The button now:
// 1. Listens for 'click' events automatically
// 2. Fetches /api/data when clicked
// 3. Swaps the response into #result
// 4. All without writing any JavaScript event handlers!
```

## Pattern 3: Multi-Step Workflow with State Coordination

**Use Case:** Coordinate multiple async steps with state tracking

```javascript
// Step 1: Define workflow states
await api:registerStateSchema({
  states: ['start', 'fetching-users', 'selecting-user', 'loading-details', 'complete'],
  transitions: {
    start: ['fetching-users'],
    'fetching-users': ['selecting-user', 'error'],
    'selecting-user': ['loading-details'],
    'loading-details': ['complete', 'error'],
    complete: ['start'],
    error: ['start']
  }
})

// Step 2: Start workflow
await api:setState({ state: 'fetching-users' })

// Step 3: Inject user list (server returns HTML with fx-action buttons)
await api:injectFxHtml({
  html: `
    <div fx-action="/api/users" fx-target="#user-list" fx-trigger="load">
      <!-- Server returns: -->
      <!-- <button fx-action="/api/user/1" fx-target="#details">User 1</button> -->
      <!-- <button fx-action="/api/user/2" fx-target="#details">User 2</button> -->
    </div>
    <div id="user-list"></div>
    <div id="details"></div>
  `,
  selector: '#app'
})

// Step 4: Listen for fx:after to advance state
ctx.on('fx:after', async (event) => {
  const currentState = await api:getCurrentState()

  if (event.cfg.action.includes('/api/users')) {
    await api:setState({ state: 'selecting-user' })
  } else if (event.cfg.action.includes('/api/user/')) {
    await api:setState({ state: 'loading-details' })
  }
})

// Step 5: Wait for completion
const result = await api:waitForState({
  state: 'complete',
  timeout: 30000
})
```

## Pattern 4: Optimistic Updates

**Use Case:** Update UI immediately, roll back on error

```javascript
// Step 1: Read current state
const currentData = await api:readDom({
  selector: '#item-count',
  property: 'textContent'
})

// Step 2: Optimistically update UI
await api:injectFxHtml({
  html: `<span id="item-count">${parseInt(currentData.value) + 1}</span>`,
  selector: '#item-count',
  position: 'outerHTML'
})

// Step 3: Track state for rollback
await api:setState({
  state: 'pending-save',
  data: { previousValue: currentData.value }
})

// Step 4: Trigger actual save
await api:triggerFxElement({ selector: '#save-button' })

// Step 5: Roll back on error
ctx.on('state:entered:error', async (event) => {
  if (event.data.previousValue) {
    await api:injectFxHtml({
      html: `<span id="item-count">${event.data.previousValue}</span>`,
      selector: '#item-count',
      position: 'outerHTML'
    })
  }
})
```

## Pattern 5: Form Validation with State

**Use Case:** Coordinate client-side validation with server submission

```javascript
// Step 1: Inject form with validation
await api:injectFxHtml({
  html: `
    <form id="user-form" fx-action="/api/users" fx-method="POST" fx-swap="none">
      <input name="email" type="email" required />
      <button type="submit">Submit</button>
    </form>
    <div id="validation-errors"></div>
  `,
  selector: '#app'
})

// Step 2: Validate before submission
ctx.on('fx:before', async (event) => {
  if (event.cfg.action === '/api/users') {
    const form = event.trigger.target.closest('form')
    if (!form.checkValidity()) {
      event.preventDefault() // Cancel request
      await api:setState({ state: 'validation-error' })
      await api:injectFxHtml({
        html: '<div class="error">Please fix form errors</div>',
        selector: '#validation-errors',
        position: 'innerHTML'
      })
    }
  }
})

// Step 3: Handle server response
ctx.on('fx:after', async (event) => {
  if (event.cfg.action === '/api/users') {
    await api:setState({ state: 'submitted' })
    await api:injectFxHtml({
      html: '<div class="success">Form submitted!</div>',
      selector: '#validation-errors',
      position: 'innerHTML'
    })
  }
})
```

## Best Practices

### 1. Separation of Concerns
- **State Logic**: Use state-tracker for business logic and workflow
- **UI Logic**: Use fixi-agent for presentation and user interaction
- **Never mix**: Don't put business logic in fx- attributes

### 2. Unidirectional Data Flow
- State changes → UI updates (never UI changes → state changes directly)
- Listen to state transitions, not DOM events
- Use fx:events to coordinate with state

### 3. Error Handling
- Always handle 'error' state in your state machine
- Use fx:error event to catch AJAX failures
- Provide user feedback for all error states

### 4. Performance
- Use `fx-swap="innerHTML"` when updating container contents
- Use `fx-swap="beforeend"` for appending (lists, infinite scroll)
- Avoid unnecessary state transitions
- Batch state updates when possible

### 5. Accessibility
- Inject semantic HTML
- Provide loading indicators for async states
- Use ARIA attributes in injected content
- Test keyboard navigation

## Common Pitfalls

### ❌ Don't: Update state from UI callbacks directly
```javascript
button.addEventListener('click', () => {
  api:setState({ state: 'loading' }) // NO! Creates tight coupling
})
```

### ✅ Do: Use fx- attributes and listen to fx:events
```javascript
// HTML
<button fx-action="/api/data" fx-target="#result">Load</button>

// Plugin
ctx.on('fx:before', (event) => {
  if (event.cfg.action === '/api/data') {
    api:setState({ state: 'loading' })
  }
})
```

### ❌ Don't: Inject HTML with inline event handlers
```javascript
api:injectFxHtml({
  html: '<button onclick="doSomething()">Click</button>' // NO!
})
```

### ✅ Do: Use fx-action for behavior
```javascript
api:injectFxHtml({
  html: '<button fx-action="/api/action">Click</button>' // YES!
})
```

### ❌ Don't: Create circular state dependencies
```javascript
ctx.on('state:entered:loading', () => {
  api:setState({ state: 'loaded' }) // Might trigger again!
})
```

### ✅ Do: Use conditional state transitions
```javascript
ctx.on('state:entered:loading', async () => {
  const data = await fetchData()
  api:setState({ state: 'loaded', data }) // Only transition once
})
```

## Example: Complete Todo App

Putting it all together:

```javascript
// 1. Register state machine
await api:registerStateSchema({
  states: ['idle', 'loading-todos', 'ready', 'adding-todo', 'deleting-todo'],
  transitions: {
    idle: ['loading-todos'],
    'loading-todos': ['ready', 'error'],
    ready: ['adding-todo', 'deleting-todo'],
    'adding-todo': ['ready', 'error'],
    'deleting-todo': ['ready', 'error'],
    error: ['idle']
  }
})

// 2. Create app structure
await api:injectFxHtml({
  html: `
    <div id="todo-app">
      <form fx-action="/api/todos" fx-method="POST" fx-swap="none">
        <input name="title" required />
        <button type="submit">Add Todo</button>
      </form>
      <div fx-action="/api/todos" fx-target="#todo-list" fx-trigger="load"></div>
      <ul id="todo-list"></ul>
    </div>
  `,
  selector: 'body'
})

// 3. Listen for state transitions
ctx.on('state:entered:loading-todos', () => {
  api:injectFxHtml({
    html: '<li>Loading...</li>',
    selector: '#todo-list',
    position: 'innerHTML'
  })
})

ctx.on('state:entered:ready', () => {
  // List is automatically populated by fx-trigger="load"
})

// 4. Handle form submission
ctx.on('fx:after', async (event) => {
  if (event.cfg.action === '/api/todos' && event.cfg.method === 'POST') {
    // Reload list after adding
    await api:triggerFxElement({ selector: '[fx-action="/api/todos"]' })
  }
})

// 5. Start app
await api:setState({ state: 'loading-todos' })
```

## Tools You'll Use

### State Tracker Tools
- `api:getCurrentState` - Check current state
- `api:setState` - Transition to new state
- `api:waitForState` - Wait for specific state
- `api:registerStateSchema` - Define state machine
- `api:getStateHistory` - Debug state transitions

### Fixi-Agent Tools
- `api:injectFxHtml` - Inject HTML with fx- attributes
- `api:readDom` - Read current DOM state
- `api:triggerFxElement` - Activate fx-action elements
- `api:getFxDocumentation` - Learn fx- attribute system

### Events to Listen For
- `state:transition` - Any state change
- `state:entered:{stateName}` - Entering specific state
- `fx:before` - Before AJAX request
- `fx:after` - After successful AJAX
- `fx:error` - AJAX request failed

## When to Use This Pattern

✅ **Good For:**
- Multi-step workflows
- Form-heavy applications
- CRUD operations with loading states
- Real-time data updates
- Progressive enhancement
- Event-driven UIs

❌ **Not Ideal For:**
- Simple static pages
- Performance-critical animations
- Complex DOM manipulations
- Large-scale SPAs (consider a full framework)

## Debugging Tips

1. **Track state history**:
   ```javascript
   const history = await api:getStateHistory({ limit: 20 })
   console.log('Recent transitions:', history)
   ```

2. **Listen to all state transitions**:
   ```javascript
   ctx.on('state:transition', (event) => {
     console.log(`State: ${event.from} → ${event.to}`, event.data)
   })
   ```

3. **Debug fx- events**:
   ```javascript
   ctx.on('fx:before', (e) => console.log('Request:', e.cfg.action))
   ctx.on('fx:after', (e) => console.log('Response:', e.cfg.text))
   ctx.on('fx:error', (e) => console.error('Error:', e.error))
   ```

4. **Read current DOM**:
   ```javascript
   const dom = await api:readDom({ selector: '#app', property: 'outerHTML' })
   console.log('Current HTML:', dom.value)
   ```

## Summary

Reactive UI with FixiPlug = **State + Declarative DOM**

1. Define your state machine
2. Inject HTML with fx- attributes
3. Listen to state transitions
4. Update UI in response to state
5. Let fx- attributes handle user interaction

This creates a clean separation between:
- **What** the UI should show (state)
- **How** to show it (fx- attributes)
- **When** to update (state transitions)

