---
name: xstate
description: Use this skill when working with XState v5 - a state management and orchestration library using state machines, statecharts, and the actor model for complex logic in JavaScript/TypeScript applications.
---

# XState v5 Skill

Comprehensive assistance with XState v5 development, generated from official Stately.ai documentation.

> **IMPORTANT: XState v5 ONLY**
>
> This skill covers XState v5 exclusively. DO NOT use XState v4 APIs, documentation, or examples.
> - Always verify documentation URLs contain "xstate" (current docs), not "xstate-v4"
> - When researching, explicitly search for "XState v5" to avoid v4 results
> - XState v5 uses `setup()` and requires TypeScript 5.0+ - if you see older patterns, it's v4
> - If migrating from v4, consult the v5 migration guide but implement using v5 APIs only

## When to Use This Skill

This skill should be triggered when:
- **State machine design**: Creating or modeling application logic with state machines/statecharts
- **Actor systems**: Implementing the actor model for orchestration and communication
- **XState v5 implementation**: Writing code using XState v5 APIs (`createMachine`, `createActor`, `setup`)
- **TypeScript typing**: Configuring strong types for state machines with XState v5
- **Actor types**: Working with promise, callback, observable, or transition actors
- **Debugging state machines**: Troubleshooting state transitions, actions, guards, or actor behavior
- **Migration to v5**: Understanding v5 API changes when upgrading from v4 (output will use v5 APIs only)
- **Integration**: Connecting XState with React, Vue, Svelte, or other frameworks

## Key Concepts

### State Machines & Actors
- **State machine**: A mathematical model of computation that can be in exactly one state at a time
- **Actor model**: A computational model where actors are independent entities that communicate by sending messages
- **Statechart**: Enhanced state machine with hierarchy, parallelism, and orthogonality
- **XState v5**: Requires TypeScript 5.0+, uses `setup()` function for type-safe machines

### Actor Types in XState
- **State machine actors**: Logic represented by finite state machines
- **Promise actors**: Actors that represent a single promise
- **Callback actors**: Logic defined by callback functions that can send events
- **Observable actors**: Actors that represent observable streams (e.g., RxJS)
- **Transition actors**: Simple reducer-like actors (similar to Redux reducers)

## Quick Reference

### 1. Simple Counter Machine (Beginner)

Basic state machine with context and actions:

```typescript
import { createMachine, assign, createActor } from 'xstate';

const countMachine = createMachine({
  context: {
    count: 0,
  },
  on: {
    INC: {
      actions: assign({
        count: ({ context }) => context.count + 1,
      }),
    },
    DEC: {
      actions: assign({
        count: ({ context }) => context.count - 1,
      }),
    },
    SET: {
      actions: assign({
        count: ({ event }) => event.value,
      }),
    },
  },
});

const countActor = createActor(countMachine).start();
countActor.subscribe((state) => {
  console.log(state.context.count);
});

countActor.send({ type: 'INC' }); // logs 1
countActor.send({ type: 'DEC' }); // logs 0
```

### 2. Toggle Machine with States (Beginner)

Machine with multiple states and transitions:

```typescript
import { setup, createActor, assign } from 'xstate';

const machine = setup({
  /* ... */
}).createMachine({
  id: 'toggle',
  initial: 'active',
  context: { count: 0 },
  states: {
    active: {
      entry: assign({
        count: ({ context }) => context.count + 1,
      }),
      on: {
        toggle: { target: 'inactive' },
      },
    },
    inactive: {
      on: {
        toggle: { target: 'active' },
      },
    },
  },
});

const actor = createActor(machine);
actor.subscribe((snapshot) => {
  console.log(snapshot.value);
});

actor.start(); // logs 'active' with context { count: 1 }
actor.send({ type: 'toggle' }); // transitions to 'inactive'
```

### 3. Type-Safe Machine with setup() (Intermediate)

Using `setup()` for strong TypeScript typing:

```typescript
import { setup } from 'xstate';

const feedbackMachine = setup({
  types: {
    context: {} as { feedback: string },
    events: {} as
      | { type: 'feedback.good' }
      | { type: 'feedback.bad' },
  },
  actions: {
    logTelemetry: () => {
      // Implement telemetry logging
    },
  },
}).createMachine({
  // Machine config with full type inference
  initial: 'idle',
  context: { feedback: '' },
  states: {
    idle: {
      on: {
        'feedback.good': {
          actions: 'logTelemetry',
          target: 'success'
        },
        'feedback.bad': {
          actions: 'logTelemetry',
          target: 'failure'
        }
      }
    },
    success: {},
    failure: {}
  }
});
```

### 4. Callback Actor for Event Listeners (Intermediate)

Using callback actors to interface with external systems:

```typescript
import { createActor, fromCallback, sendTo, setup } from 'xstate';

const resizeLogic = fromCallback(({ sendBack, receive }) => {
  const resizeHandler = (event) => {
    sendBack(event);
  };

  window.addEventListener('resize', resizeHandler);

  const removeListener = () => {
    window.removeEventListener('resize', resizeHandler);
  };

  receive((event) => {
    if (event.type === 'stopListening') {
      console.log('Stopping listening');
      removeListener();
    }
  });

  // Cleanup function
  return () => {
    console.log('Cleaning up');
    removeListener();
  };
});

const machine = setup({
  actors: { resizeLogic }
}).createMachine({
  invoke: {
    src: 'resizeLogic',
  },
});
```

### 5. Callback Actor with Input (Intermediate)

Passing input to callback actors:

```typescript
import { fromCallback, createActor, setup, type EventObject } from 'xstate';

const resizeLogic = fromCallback<EventObject, { defaultSize: number }>(
  ({
    sendBack,
    receive,
    input, // Typed as { defaultSize: number }
  }) => {
    console.log(input.defaultSize); // 100

    // Use input.defaultSize in your logic
    return () => {
      // Cleanup
    };
  }
);

const machine = setup({
  actors: {
    resizeLogic,
  },
}).createMachine({
  invoke: {
    src: 'resizeLogic',
    input: {
      defaultSize: 100,
    },
  },
});
```

### 6. Observable Actor with RxJS (Advanced)

Creating observable actors for stream processing:

```typescript
import { fromObservable, createActor } from 'xstate';
import { interval } from 'rxjs';

const intervalLogic = fromObservable(({ input }) =>
  interval(input.interval)
);

const intervalActor = createActor(intervalLogic, {
  input: { interval: 10_000 },
});

intervalActor.subscribe((snapshot) => {
  console.log(snapshot.context);
});

intervalActor.start();
// logs 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...
// every 10 seconds
```

### 7. Inspection API for Debugging (Advanced)

Using the Inspect API to observe state transitions:

```typescript
const actor = createActor(machine, {
  inspect: (inspectionEvent) => {
    // type: '@xstate.actor' - when actor is created
    // type: '@xstate.snapshot' - when state updates
    // type: '@xstate.event' - when event is sent
    // type: '@xstate.microstep' - for each transition step
    console.log(inspectionEvent);
  },
});

actor.start();
```

### 8. TypeScript Configuration

Required TypeScript setup for XState v5:

```json
{
  "compilerOptions": {
    "strictNullChecks": true,
    "skipLibCheck": true
  }
}
```

### 9. Installation Commands

```bash
# npm
npm install xstate

# pnpm
pnpm install xstate

# yarn
yarn add xstate

# TypeScript (required: v5.0+)
npm install typescript@latest --save-dev
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **state.md** - Complete documentation covering:
  - Observable actors and RxJS integration
  - TypeScript setup and type safety
  - Installation and getting started
  - Callback actors for event handling
  - Cheatsheet with syntax examples
  - Inspection API for debugging
  - State machine actors and capabilities
  - Actor input/output patterns

Use the reference file to access:
- Detailed API documentation with complete examples
- TypeScript type helpers (`ActorRefFrom`, `SnapshotFrom`, `EventFrom`)
- Event assertion patterns for type safety
- Complete inspection event schemas
- Actor system architecture patterns

## Working with This Skill

### For Beginners

**Start here:**
1. Review the "Simple Counter Machine" example above
2. Understand the basic concepts: states, events, transitions, context
3. Learn the core APIs: `createMachine`, `createActor`, `assign`
4. Check the cheatsheet section in `references/state.md`

**Key learning path:**
- States and transitions (toggle machine example)
- Context and actions (counter machine example)
- Event handling with `send()`
- Subscribing to state changes

### For Intermediate Users

**Focus areas:**
1. Type safety with the `setup()` function
2. Actor invocation and communication patterns
3. Callback actors for external system integration
4. Input/output patterns for actor data flow

**Common tasks:**
- Creating reusable actor logic
- Implementing guards and actions
- Passing typed input to actors
- Managing actor lifecycle (cleanup)

### For Advanced Users

**Advanced topics:**
1. Observable actors with RxJS integration
2. Actor system orchestration (parent-child relationships)
3. Inspection API for comprehensive debugging
4. Microstep analysis for complex transitions
5. Custom actor logic creators

**Integration patterns:**
- Framework integration (React, Vue, Svelte)
- Backend state orchestration
- Event-driven architecture
- Testing state machines

### Navigation Tips

- **Need type safety?** → See "Type-Safe Machine with setup()" example and TypeScript section
- **External events?** → Check callback actor examples
- **Debugging issues?** → Use Inspection API example and review inspection events
- **Stream data?** → See Observable actor with RxJS
- **Quick syntax lookup?** → Reference the cheatsheet examples in `state.md`

## TypeScript Support

XState v5 requires TypeScript 5.0 or higher. Key features:

- **`setup()` function**: Strongly types machines, context, events, and actions
- **`.types` property**: Alternative typing method in machine config
- **Type helpers**: `ActorRefFrom<T>`, `SnapshotFrom<T>`, `EventFrom<T>`
- **`assertEvent()`**: Type assertion helper for narrowing event types
- **Dynamic parameters**: Preferred over direct event access for type safety

## Common Patterns

### Actor Communication
```typescript
// Send events between actors
sendTo('childActor', { type: 'message' })

// Receive events in callback actor
receive((event) => {
  if (event.type === 'message') {
    // Handle message
  }
})
```

### Cleanup & Lifecycle
```typescript
// Return cleanup function from callback actor
return () => {
  // Cleanup resources
  removeEventListeners();
  clearTimers();
};
```

### Type-Safe Event Handling
```typescript
// Use assertEvent for type narrowing
import { assertEvent } from 'xstate';

actions: {
  handleEvent: ({ event }) => {
    assertEvent(event, 'specificEventType');
    // TypeScript now knows event.type is 'specificEventType'
    console.log(event.specificProperty);
  }
}
```

## Resources

### Official Links
- **Documentation**: https://stately.ai/docs/xstate (v5 docs - avoid /xstate-v4/ URLs)
- **Stately Studio**: Visual editor and debugging tool for state machines
- **VS Code Extension**: XState extension for visual editing and autocomplete

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill covers **XState v5** specifically (requires TypeScript 5.0+)
- All actors in XState are observable
- The `setup()` function is the recommended way to create type-safe machines
- Typegen is not yet available for v5; use `setup()` or `.types` instead
- Use the Inspection API for comprehensive debugging
- Reference files contain links to original documentation

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
