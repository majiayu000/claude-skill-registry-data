---
name: corgi
description: Use this skill when working with any UI code
---

Corgi is a custom React-like UI framework with JSX support, server-side rendering, hydration,
and a controller-based architecture for managing state and handling events.

## Core Concepts

### Virtual DOM and JSX

Corgi uses JSX with a custom factory function:

```tsx
import * as corgi from 'external/dev_april_corgi+/js/corgi';

// JSX compiles to corgi.createVirtualElement calls
function MyComponent() {
  return <div className="container">Hello World</div>;
}
```

Configure your tsconfig.json:
```json
{
  "compilerOptions": {
    "jsx": "react",
    "jsxFactory": "corgi.createVirtualElement",
    "jsxFragmentFactory": "corgi.Fragment"
  }
}
```

### Component Functions

Components are functions that receive props, state, and an updateState callback:

```tsx
interface State {
  count: number;
}

function Counter(
  props: { initialValue?: number },
  state: State | undefined,
  updateState: (newState: State) => void
) {
  // Initialize state on first render
  if (!state) {
    state = { count: props.initialValue ?? 0 };
  }

  return (
    <div>
      <span>Count: {state.count}</span>
    </div>
  );
}
```

### Fragments

Use `<></>` or `corgi.Fragment` to group elements without a wrapper:

```tsx
function List() {
  return <>
    <li>Item 1</li>
    <li>Item 2</li>
  </>;
}
```

## Controllers

Controllers are classes that manage component behavior, handle events, and maintain state.
They extend `Controller` and are attached to elements via the `js` prop.

### Basic Controller

```tsx
import { Controller, Response } from 'external/dev_april_corgi+/js/corgi/controller';
import { EmptyDeps } from 'external/dev_april_corgi+/js/corgi/deps';

interface Args {
  multiplier: number;
}

interface State {
  count: number;
}

class CounterController extends Controller<Args, EmptyDeps, HTMLDivElement, State> {
  constructor(response: Response<CounterController>) {
    super(response);
    // Access args via response.args
    // Access initial state via this.state
    // Access root element via this.root
  }

  increment(): void {
    this.updateState({
      count: this.state.count + 1,
    });
  }
}
```

### Controller Type Parameters

Controllers have four type parameters:
1. `A` - Args type: Props passed from the component
2. `D` - Deps method type: Dependencies (services and child controllers)
3. `E` - Element type: The DOM element type (HTMLDivElement, HTMLInputElement, etc.)
4. `S` - State type: Component state

### Binding Controllers with `js=` Prop

Use `corgi.bind()` to attach a controller to an element:

```tsx
function Counter(
  props: {},
  state: State | undefined,
  updateState: (newState: State) => void
) {
  if (!state) {
    state = { count: 0 };
  }

  return (
    <div
      js={corgi.bind({
        controller: CounterController,
        args: { multiplier: 2 },
        state: [state, updateState],
        events: {
          click: 'increment',
          render: 'wakeup',
        },
        ref: 'counter',  // Optional: for dependency injection
        key: 'unique-id', // Optional: for controller reuse during patches
      })}
    >
      Count: {state.count}
    </div>
  );
}
```

### Bind Options

- `controller`: The controller class constructor
- `args`: Props to pass to the controller (accessible via `response.args`)
- `state`: Tuple of [currentState, updateStateFn]
- `events`: Map of DOM events to controller method names
- `ref`: String identifier for dependency injection (see `ref=` section below)
- `key`: Unique key for controller instance identity during patching. When a component re-renders and patches an element with a controller, Corgi decides whether to reuse the existing controller or create a new one. If the controller type and key both match, the existing controller instance is reused and only `updateArgs()` is called. If the key differs (or one binding has a key and the other doesn't), the old controller is disposed and a new one is created. This is useful when rendering lists where each item has the same controller type - without keys, reordering items would cause controllers to receive args for different items rather than being recreated. With unique keys (e.g., item IDs), each controller stays paired with its logical item.

## Event Handling

### Standard DOM Events via `events=`

Map DOM events to controller methods:

```tsx
js={corgi.bind({
  controller: MyController,
  events: {
    click: 'handleClick',
    keydown: 'handleKeyDown',
    focus: 'handleFocus',
    blur: 'handleBlur',
    input: 'handleInput',
    change: 'handleChange',
    mousedown: 'handleMouseDown',
    mouseover: 'handleMouseOver',
    pointerdown: 'handlePointerDown',
    dragstart: 'handleDragStart',
    drop: 'handleDrop',
    render: 'wakeup', // Special: called when controller is instantiated
  },
})}
```

Available events:
- Mouse: `click`, `mousedown`, `mouseup`, `mouseover`, `mouseout`
- Pointer: `pointerdown`, `pointerup`, `pointermove`, `pointerenter`, `pointerleave`, `pointerover`, `pointerout`
- Keyboard: `keydown`, `keypress`, `keyup`
- Focus: `focus`, `blur`, `focusin`, `focusout`
- Form: `input`, `change`
- Drag: `drag`, `dragstart`, `dragend`, `dragenter`, `dragleave`, `dragover`, `drop`
- Context: `contextmenu`
- Special: `render` (called on controller instantiation)

### Custom Corgi Events

Declare and handle custom events that bubble up through the component tree:

```tsx
// Declare events in a shared file
import { declareEvent } from 'external/dev_april_corgi+/js/corgi/events';

export const ACTION = declareEvent<{}>('myapp.action');
export const VALUE_CHANGED = declareEvent<{ value: string }>('myapp.valueChanged');
export const ITEM_SELECTED = declareEvent<{ id: number; label: string }>('myapp.itemSelected');
```

Listen for custom events via the `corgi` key in events:

```tsx
js={corgi.bind({
  controller: ParentController,
  events: {
    corgi: [
      [ACTION, 'handleAction'],
      [VALUE_CHANGED, 'handleValueChanged'],
    ],
  },
})}
```

Trigger custom events from a controller:

```tsx
class ChildController extends Controller<...> {
  buttonClicked(): void {
    // Trigger a custom event that bubbles up to parent controllers
    this.trigger(ACTION, {});
    this.trigger(VALUE_CHANGED, { value: this.root.value });
  }
}
```

### CorgiEvent Type

Event handlers receive a CorgiEvent with actionElement, targetElement, and detail:

```tsx
import { CorgiEvent, DOM_KEYBOARD, DOM_MOUSE } from 'external/dev_april_corgi+/js/corgi/events';

class MyController extends Controller<...> {
  // For custom events
  handleValueChanged(e: CorgiEvent<typeof VALUE_CHANGED>): void {
    console.log(e.detail.value);
    console.log(e.actionElement);  // QueryOne for element that bound the event
    console.log(e.targetElement);  // QueryOne for element that triggered it
  }

  // For DOM events, detail contains the native event
  handleKeyUp(e: CorgiEvent<typeof DOM_KEYBOARD>): void {
    if (e.detail.key === 'Enter') {
      this.trigger(ACTION, {});
    }
  }

  handleClick(e: CorgiEvent<typeof DOM_MOUSE>): void {
    if (e.detail.ctrlKey) {
      // Ctrl+click handling
    }
  }
}
```

## Unbound Events with `unboundEvents=`

For elements that don't have their own controller but need to trigger events on a parent
controller, use `unboundEvents`. The handler names are strings that reference methods on
the nearest ancestor controller.

```tsx
function MyComponent(props: {}, state: State | undefined, updateState: (s: State) => void) {
  return (
    <div
      js={corgi.bind({
        controller: ParentController,
        state: [state, updateState],
        events: {
          corgi: [[SAVE, 'handleSave']],
        },
      })}
    >
      {/* These buttons don't have their own controller */}
      <button unboundEvents={{ click: 'handleSave' }}>Save</button>
      <button unboundEvents={{ click: 'handleCancel' }}>Cancel</button>

      {/* Unbound events can also listen for custom corgi events */}
      <Input unboundEvents={{ corgi: [[CHANGED, 'handleInputChanged']] }} />
    </div>
  );
}

class ParentController extends Controller<...> {
  handleSave(): void {
    // Called when the Save button is clicked
  }

  handleCancel(): void {
    // Called when the Cancel button is clicked
  }

  handleInputChanged(e: CorgiEvent<typeof CHANGED>): void {
    console.log('Input changed:', e.detail.value);
  }
}
```

Key differences from `events`:
- `unboundEvents` is a prop on any element, not just controller-bound elements
- Handler names are strings (the method name on the parent controller)
- Events bubble up to find the nearest ancestor with a controller
- Custom events use the same `corgi: [[EVENT, 'handler']]` syntax

## The `ref=` Prop and Dependency Injection

The `ref` prop enables parent controllers to access child controllers via dependency injection.

### Setting a Ref

```tsx
<div
  js={corgi.bind({
    controller: ChildController,
    ref: 'childWidget', // This ref name is used for dependency lookup
    state: [state, updateState],
  })}
/>
```

This also adds `data-js-ref="childWidget"` attribute to the element.

### Declaring Dependencies

Controllers declare dependencies via a static `deps()` method:

```tsx
class ParentController extends Controller<Args, Deps, HTMLElement, State> {
  static deps() {
    return {
      controllers: {
        // Single controller dependency (must find exactly one matching ref)
        childWidget: ChildController,
      },
      controllerss: {
        // Multiple controllers with the same ref (finds all matching refs)
        listItems: ListItemController,
      },
      services: {
        dialog: DialogService,
        history: HistoryService,
      },
    };
  }

  private readonly child: ChildController;
  private readonly items: ListItemController[];
  private readonly dialog: DialogService;

  constructor(response: Response<ParentController>) {
    super(response);
    this.child = response.deps.controllers.childWidget;
    this.items = response.deps.controllerss.listItems;
    this.dialog = response.deps.services.dialog;
  }
}
```

### Dependency Resolution

- `controllers`: Maps ref names to single controller instances
- `controllerss`: Maps ref names to arrays of controller instances (note the double 's')
- `services`: Maps names to singleton service instances

The dependency system searches within the element's subtree for elements with matching
`data-js-ref` attributes, stopping at elements that have their own `data-js` (controller boundary).

## Services

Services are singletons that provide shared functionality across the application.

### Creating a Service

```tsx
import { Service, ServiceResponse } from 'external/dev_april_corgi+/js/corgi/service';
import { EmptyDeps } from 'external/dev_april_corgi+/js/corgi/deps';

export class NotificationService extends Service<EmptyDeps> {
  constructor(response: ServiceResponse<EmptyDeps>) {
    super(response);
  }

  show(message: string): void {
    // Implementation
  }
}
```

### Service with Dependencies

Services can depend on other services:

```tsx
type Deps = typeof ApiService.deps;

export class ApiService extends Service<Deps> {
  static deps() {
    return {
      services: {
        auth: AuthService,
      },
    };
  }

  private readonly auth: AuthService;

  constructor(response: ServiceResponse<Deps>) {
    super(response);
    this.auth = response.deps.services.auth;
  }
}
```

### Built-in Services

**HistoryService**: Browser history management

```tsx
import { HistoryService } from 'external/dev_april_corgi+/js/corgi/history/history_service';

class MyController extends Controller<...> {
  static deps() {
    return { services: { history: HistoryService } };
  }

  navigateHome(): void {
    this.history.goTo('/');  // Push new URL
    this.history.replaceTo('/new');  // Replace current URL
    this.history.back();  // Go back
    this.history.reload();  // Notify listeners of current URL
  }
}
```

**ViewsService**: Route matching and navigation

```tsx
import { ViewsService, DiscriminatedRoute, matchPath } from 'external/dev_april_corgi+/js/corgi/history/views_service';

interface Routes {
  home: {};
  user: { id: string };
}

const routes: { [k in keyof Routes]: RegExp } = {
  home: /^\/$/,
  detail: /^\/items\/(?<id>[^/]+)$/,
};

class RouteController extends Controller<{}, Deps, HTMLDivElement, State> {
  static getInitialState(): State {
    const url = currentUrl();
    const match = matchPath<Routes>(url.pathname, routes);
    if (!match) throw new NotFoundError();
    return { active: match };
  }

  static deps() {
    return {
      services: { views: ViewsService<Routes> },
    };
  }

  constructor(response: Response<RouteController>) {
    super(response);
    const views = response.deps.services.views;
    views.addListener(this);
    views.addRoutes(routes);
    this.registerDisposer(() => views.removeListener(this));
  }

  routeChanged(active: DiscriminatedRoute<Routes>, parameters: Record<string, string>): Promise<void> {
    return this.updateState({ active, parameters });
  }
}
```

**DialogService**: Modal dialog management

```tsx
import { DialogService } from 'external/dev_april_corgi+/js/emu/dialog';

class MyController extends Controller<...> {
  static deps() {
    return { services: { dialog: DialogService } };
  }

  async showConfirmation(): Promise<void> {
    try {
      await this.dialog.display(<ConfirmDialog message="Are you sure?" />);
      // User confirmed
    } catch {
      // User cancelled (clicked outside)
    }
  }
}
```

```
// In dialog content, trigger close
this.trigger(CLOSE, { kind: 'resolve' }); // or 'reject'
```

## Controller Lifecycle

### Instantiation

Controllers are lazily instantiated when an event is first triggered on their element.
Use the special `render` event to force immediate instantiation:

```tsx
events: {
  render: 'wakeup',
}
```

### Disposal

Controllers extend `Disposable` and are automatically disposed when their element is removed
from the DOM. Use lifecycle hooks:

```tsx
class MyController extends Controller<...> {
  constructor(response: Response<MyController>) {
    super(response);

    // Register cleanup functions
    this.registerDisposer(() => {
      console.log('Controller being disposed');
    });

    // Register event listeners that auto-cleanup
    this.registerListener(window, 'resize', this.handleResize);

    // Register child disposables
    this.registerDisposable(someOtherDisposable);
  }
}
```

### State Updates

Call `updateState()` to update state and trigger a re-render:

```tsx
class CounterController extends Controller<...> {
  async increment(): Promise<void> {
    await this.updateState({
      ...this.state,
      count: this.state.count + 1,
    });
    // State is now updated and component has re-rendered
  }
}
```

State updates are debounced to batch rapid changes.

### Updating Args

Override `updateArgs` to respond to prop changes:

```tsx
class MyController extends Controller<...> {
  updateArgs(newArgs: Args): void {
    // Called when parent re-renders with new args
    if (newArgs.value !== this.currentValue) {
      this.handleValueChange(newArgs.value);
    }
  }
}
```

## DOM Queries

Controllers have access to DOM query utilities:

```tsx
class MyController extends Controller<...> {
  findChild(): void {
    // Query from root element
    const query = this.query();

    // Find descendants
    const buttons = query.descendants('button');  // Returns Query
    const firstButton = buttons.one();  // Returns QueryOne (throws if not exactly 1)
    const allButtons = buttons.all();  // Returns QueryOne[]
  }
}
```

There are many helper functions on queries:

```typescript
// In controller
const element = this.query()
  .descendants('.my-class')  // Find all descendants matching selector
  .one()                     // Expect exactly one match
  .element();                // Get the DOM element

// Query methods
query.children(selector?)      // Direct children
query.descendants(selector)    // All descendants matching selector
query.parent(selector?)        // Find parent(s)
query.refs(refName)           // Find elements with data-ref or data-js-ref
query.filter(fn)              // Filter elements
query.map(fn)                 // Map over elements
query.one()                   // Get single QueryOne (throws if not exactly one)
query.all()                   // Get array of QueryOne

// QueryOne methods
queryOne.attr(key)            // Get attribute as DataValue
queryOne.data(key)            // Get data-* attribute as DataValue
queryOne.element()            // Get DOM element

// DataValue methods
dataValue.string()            // Get as string
dataValue.number()            // Get as number (throws if NaN)
```

## Rendering and Hydration

### Client-Side Rendering

```tsx
import * as corgi from 'external/dev_april_corgi+/js/corgi';

// Append element to DOM
corgi.appendElement(document.body, <App />);
```

### Server-Side Rendering with Hydration

```tsx
// On the server: render to HTML string
const html = renderToString(<App />);

// On the client: hydrate existing HTML
if (process.env.CORGI_FOR_BROWSER) {
  corgi.hydrateElement(checkExists(document.getElementById('root')), <App />);
}
```

## Emu Component Library

Corgi includes the Emu component library with pre-built components:

### Button

```tsx
import { Button } from 'external/dev_april_corgi+/js/emu/button';
import { ACTION } from 'external/dev_april_corgi+/js/emu/events';

<Button
  ref="submitBtn"
  className="primary"
  unboundEvents={{ corgi: [[ACTION, 'handleSubmit']] }}
>
  Submit
</Button>
```

### Input

```tsx
import { Input } from 'external/dev_april_corgi+/js/emu/input';
import { CHANGED, ACTION } from 'external/dev_april_corgi+/js/emu/events';

<Input
  ref="nameInput"
  placeholder="Enter name"
  value={state.name}
  unboundEvents={{
    corgi: [
      [CHANGED, 'handleNameChange'],  // Fired on input change
      [ACTION, 'handleSubmit'],       // Fired on Enter key
    ],
  }}
/>
```

### Checkbox

```tsx
import { Checkbox } from 'external/dev_april_corgi+/js/emu/checkbox';
import { ACTION } from 'external/dev_april_corgi+/js/emu/events';

<Checkbox
  ref="agreeCheckbox"
  checked={state.agreed}
  unboundEvents={{ corgi: [[ACTION, 'handleAgreeToggle']] }}
>
  I agree to the terms
</Checkbox>
```

### Select

```tsx
import { Select } from 'external/dev_april_corgi+/js/emu/select';
import { CHANGED } from 'external/dev_april_corgi+/js/emu/events';

<Select
  ref="colorSelect"
  options={[
    { label: 'Red', value: 'red' },
    { label: 'Blue', value: 'blue', selected: true },
  ]}
  unboundEvents={{ corgi: [[CHANGED, 'handleColorChange']] }}
/>
```

### Emu Events

```tsx
import { ACTION, CHANGED, FOCUSED, UNFOCUSED, PRESSED, CLOSE } from 'external/dev_april_corgi+/js/emu/events';

// ACTION: Button clicks, checkbox toggles, Enter key in inputs
// CHANGED: Input value changes, select changes
// FOCUSED/UNFOCUSED: Focus events
// PRESSED: Special keys (Arrow keys, Escape) in inputs
// CLOSE: Dialog close events
```

## Data Attributes

Use the `data` prop to set data attributes:

```tsx
<div data={{ id: '123', enabled: true, count: 42 }}>
  ...
</div>
// Renders: <div data-id="123" data-enabled="true" data-count="42">
```

## Style and Class Names

```tsx
// className for CSS classes
<div className="container flex items-center">...</div>

// style for inline styles (as a string)
<div style="left: 10px; top: 20px; transform: scale(2)">...</div>
```

## Assertions (`asserts.ts`)

```typescript
import { checkArgument, checkExists, checkState, checkExhaustive, exists } from 'external/dev_april_corgi+/js/common/asserts';

// Throw if condition is false
checkArgument(value > 0, 'Value must be positive');
checkState(this.initialized, 'Not initialized');

// Throw if null/undefined, otherwise return value
const item = checkExists(maybeItem, 'Item not found');

// Exhaustiveness check for switch/if-else (compile-time check)
switch (value.kind) {
  case 'a': return handleA();
  case 'b': return handleB();
  default: checkExhaustive(value); // Compile error if cases missed
}

// Type guard for null/undefined
if (exists(maybeValue)) {
  // maybeValue is now non-null
}
```

## Futures (`futures.ts`)

Enhanced promises with synchronous completion checking:

```typescript
import { Future, asFuture, resolvedFuture, rejectedFuture, unsettledFuture } from 'external/dev_april_corgi+/js/common/futures';

// Wrap a promise
const future = asFuture(somePromise);

// Create pre-resolved/rejected futures
const resolved = resolvedFuture(value);
const rejected = rejectedFuture(error);

// Check completion synchronously
if (future.finished) {
  if (future.ok) {
    const value = future.value();
  } else {
    const error = future.error();
  }
}
```

## Debouncer (`debouncer.ts`)

```typescript
import { Debouncer } from 'external/dev_april_corgi+/js/common/debouncer';

const debouncer = new Debouncer(300, () => {
  // Called after 300ms of no triggers
});

// Trigger (resets timer if called again within delay)
await debouncer.trigger();
```

## Timer (`timer.ts`)

Repeating timer that can be started/stopped:

```typescript
import { Timer } from 'external/dev_april_corgi+/js/common/timer';

const timer = new Timer(1000, () => {
  // Called every 1000ms
});

timer.start();  // Start repeating
timer.stop();   // Stop
timer.dispose(); // Cleanup
```

## Collections (`collections.ts`)

```typescript
import { DefaultMap, HashMap, HashSet, IdentitySetMultiMap, getOnlyElement, getFirstElement } from 'external/dev_april_corgi+/js/common/collections';

// Map with auto-initialization
const map = new DefaultMap<string, number[]>(() => []);
map.get('key').push(1); // No need to check if key exists

// Map/Set with custom hash function
const hashMap = new HashMap<MyKey, MyValue>(key => key.id);
const hashSet = new HashSet<MyValue>(val => val.id);

// Multi-value map with identity comparison
const multiMap = new IdentitySetMultiMap<string, object>();
multiMap.put('key', obj1);
multiMap.put('key', obj2);

// Get single element from iterable (throws if not exactly one)
const only = getOnlyElement(iterable);
const first = getFirstElement(iterable);
```

## Comparisons (`comparisons.ts`)

```typescript
import { deepEqual, approxEqual, approxGtOrEqual, approxLtOrEqual } from 'external/dev_april_corgi+/js/common/comparisons';

// Deep equality (handles objects, arrays, Maps, Sets, Dates, RegExp)
if (deepEqual(obj1, obj2)) { }

// Approximate numeric comparisons
if (approxEqual(a, b, 0.001)) { }
if (approxGtOrEqual(a, b, 0.001)) { }
```

## Arrays (`arrays.ts`)

```typescript
import { compare, equals, pushInto } from 'external/dev_april_corgi+/js/common/arrays';

// Lexicographic comparison (-1, 0, 1)
const cmp = compare(arr1, arr2);

// Shallow equality
if (equals(arr1, arr2)) { }

// Efficient push without stack issues
pushInto(destination, source);
```

## Promises (`promises.ts`)

```typescript
import { waitMs, waitSettled, waitTicks } from 'external/dev_april_corgi+/js/common/promises';

await waitMs(1000);        // Wait 1 second
await waitSettled();       // Wait for microtask queue to settle
await waitTicks(10);       // Wait N promise ticks
```

## Math (`math.ts`)

```typescript
import { clamp, floatCoalesce } from 'external/dev_april_corgi+/js/common/math';

const clamped = clamp(value, 0, 100);  // Clamp between min/max

// Get first valid number from list
const num = floatCoalesce(maybeNum1, maybeNum2, defaultNum);
```

## Memoized (`memoized.ts`)

```typescript
import { Memoized, maybeMemoized } from 'external/dev_april_corgi+/js/common/memoized';

// Lazy-initialized value
const lazy = new Memoized(() => expensiveComputation());
console.log(lazy.value); // Computed once, cached

// SSR-aware memoization (doesn't cache on server)
const ssrSafe = maybeMemoized(() => computation());
```

## Complete Example

```tsx
import * as corgi from 'external/dev_april_corgi+/js/corgi';
import { Controller, Response } from 'external/dev_april_corgi+/js/corgi/controller';
import { declareEvent, CorgiEvent } from 'external/dev_april_corgi+/js/corgi/events';
import { EmptyDeps } from 'external/dev_april_corgi+/js/corgi/deps';
import { Button } from 'external/dev_april_corgi+/js/emu/button';
import { Input } from 'external/dev_april_corgi+/js/emu/input';
import { ACTION, CHANGED } from 'external/dev_april_corgi+/js/emu/events';

// Declare custom event
const TODO_ADDED = declareEvent<{ text: string }>('app.todoAdded');

// State interface
interface State {
  todos: string[];
  inputValue: string;
}

// Controller
class TodoController extends Controller<{}, EmptyDeps, HTMLDivElement, State> {
  handleInputChange(e: CorgiEvent<typeof CHANGED>): void {
    this.updateState({
      ...this.state,
      inputValue: e.detail.value,
    });
  }

  handleAddTodo(): void {
    if (this.state.inputValue.trim()) {
      this.updateState({
        todos: [...this.state.todos, this.state.inputValue],
        inputValue: '',
      });
      this.trigger(TODO_ADDED, { text: this.state.inputValue });
    }
  }
}

// Component
function TodoApp(props: {}, state: State | undefined, updateState: (s: State) => void) {
  if (!state) {
    state = { todos: [], inputValue: '' };
  }

  return (
    <div
      js={corgi.bind({
        controller: TodoController,
        state: [state, updateState],
        events: {
          corgi: [[CHANGED, 'handleInputChange']],
        },
      })}
    >
      <h1>Todo List</h1>
      <div>
        <Input
          value={state.inputValue}
          placeholder="Add a todo..."
          unboundEvents={{
            corgi: [
              [CHANGED, 'handleInputChange'],
              [ACTION, 'handleAddTodo'],
            ],
          }}
        />
        <Button unboundEvents={{ corgi: [[ACTION, 'handleAddTodo']] }}>
          Add
        </Button>
      </div>
      <ul>
        {state.todos.map(todo => <li>{todo}</li>)}
      </ul>
    </div>
  );
}

// Bootstrap
if (process.env.CORGI_FOR_BROWSER) {
  corgi.hydrateElement(checkExists(document.getElementById('root')), <TodoApp />);
}
```

## Best Practices

1. **Initialize state in components**: Always check `if (!state)` and initialize
2. **Use `checkExists`**: Instead of `!` assertions for null checks
3. **Use refs for controller dependencies**: Name child controllers with `ref` for injection
4. **Prefer unboundEvents for simple handlers**: When a child doesn't need its own controller
5. **Trigger custom events for component communication**: Use `declareEvent` and `this.trigger()`
6. **Use custom events for child-to-parent communication**: Don't pass callbacks as props
7. **Register cleanup with registerDisposer**: Prevent memory leaks
8. **Use registerListener for window/document events**: Auto-cleanup on disposal
9. **Debounce state updates**: `updateState` is already debounced, but batch related changes
10. **Type your state and args**: Use TypeScript interfaces for type safety
11. **Type your controllers**: Use all four generic parameters `Controller<Args, Deps, Element, State>`
12. **Use `render: 'wakeup'` event**: To run initialization code after DOM is ready
