---
name: composing-components
description: Teaches component composition patterns in React 19 including children prop, compound components, and render props. Use when designing component APIs, creating reusable components, or avoiding prop drilling.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Component Composition Patterns

<role>
This skill teaches you how to compose components effectively using React 19 patterns.
</role>

<when-to-activate>
This skill activates when:

- Designing reusable component APIs
- Need to avoid prop drilling
- Creating compound components (Tabs, Accordion, etc.)
- Building flexible, composable interfaces
- Choosing between composition patterns
  </when-to-activate>

<overview>
React 19 supports multiple composition patterns:

1. **Children Prop** - Simplest composition, pass components as children
2. **Compound Components** - Components that work together (Context-based)
3. **Render Props** - Functions as children for flexibility
4. **Composition over Props** - Prefer slots over configuration props

**When to Use:**

- Children prop: Simple containment
- Compound components: Coordinated behavior (tabs, accordions)
- Render props: Custom rendering logic
- Slots: Multiple insertion points
  </overview>

<workflow>
## Pattern 1: Children Prop

```javascript
function Card({ children, header, footer }) {
  return (
    <div className="card">
      {header && <div className="header">{header}</div>}
      <div className="body">{children}</div>
      {footer && <div className="footer">{footer}</div>}
    </div>
  );
}

<Card header={<h2>Title</h2>} footer={<button>Action</button>}>
  <p>Card content goes here</p>
</Card>;
```

## Pattern 2: Compound Components

```javascript
import { createContext, use } from 'react';

const TabsContext = createContext(null);

export function Tabs({ children, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext>
  );
}

export function TabList({ children }) {
  return <div className="tab-list">{children}</div>;
}

export function Tab({ id, children }) {
  const { activeTab, setActiveTab } = use(TabsContext);

  return (
    <button className={activeTab === id ? 'active' : ''} onClick={() => setActiveTab(id)}>
      {children}
    </button>
  );
}

export function TabPanel({ id, children }) {
  const { activeTab } = use(TabsContext);

  if (activeTab !== id) return null;

  return <div className="tab-panel">{children}</div>;
}
```

Usage:

```javascript
<Tabs defaultTab="profile">
  <TabList>
    <Tab id="profile">Profile</Tab>
    <Tab id="settings">Settings</Tab>
  </TabList>

  <TabPanel id="profile">
    <Profile />
  </TabPanel>

  <TabPanel id="settings">
    <Settings />
  </TabPanel>
</Tabs>
```

## Pattern 3: Render Props

```javascript
function DataProvider({ render, endpoint }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(endpoint)
      .then((res) => res.json())
      .then(setData);
  }, [endpoint]);

  return render({ data, loading: !data });
}

<DataProvider
  endpoint="/api/users"
  render={({ data, loading }) => (loading ? <Spinner /> : <UserList users={data} />)}
/>;
```

</workflow>

<examples>
## Example: Modal with Composition

```javascript
function Modal({ children, isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
}

function ModalHeader({ children }) {
  return <div className="modal-header">{children}</div>;
}

function ModalBody({ children }) {
  return <div className="modal-body">{children}</div>;
}

function ModalFooter({ children }) {
  return <div className="modal-footer">{children}</div>;
}

Modal.Header = ModalHeader;
Modal.Body = ModalBody;
Modal.Footer = ModalFooter;
```

Usage:

```javascript
<Modal isOpen={showModal} onClose={() => setShowModal(false)}>
  <Modal.Header>
    <h2>Confirm Action</h2>
  </Modal.Header>

  <Modal.Body>
    <p>Are you sure you want to proceed?</p>
  </Modal.Body>

  <Modal.Footer>
    <button onClick={() => setShowModal(false)}>Cancel</button>
    <button onClick={handleConfirm}>Confirm</button>
  </Modal.Footer>
</Modal>
```

For comprehensive composition patterns, see: `research/react-19-comprehensive.md` lines 1263-1293.
</examples>

<constraints>
## MUST
- Use `use()` API for Context in React 19 (can be conditional)
- Keep compound components cohesive
- Document required child components

## SHOULD

- Prefer composition over complex prop APIs
- Use Context for compound component state
- Provide good component names for debugging

## NEVER

- Over-engineer simple components
- Use Context for non-coordinated components
- Forget to handle edge cases (missing children, etc.)
  </constraints>
