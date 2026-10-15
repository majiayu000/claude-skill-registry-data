---
name: intent-derived-ui-state
description: Model responsive or context-dependent UI by storing only durable user intent and deriving the rendered selection from that intent plus route, viewport, capability, and open-state inputs. Use when resize, media-query, orientation, device capability, or route synchronization is mutating selected tabs, panes, modes, or other redundant React state.
---

# Intent-Derived UI State

## Principle

Store the smallest durable fact: what the user explicitly chose. Derive the
current UI result from that intent plus live context.

```ts
const selectedTab = deriveSelectedTab({
  intent,
  routeTab,
  isNarrow,
  isOpen,
});
```

Treat viewport width, orientation, pointer capability, route synchronization,
and open state as inputs to the derivation—not as events that rewrite intent.
Only semantic actions such as the user selecting a tab may update the intent.

This is a single-source-of-truth pattern: **intent state + derived UI state**.

## Avoid Effect-Based Synchronization

Do not mirror the derived result into state:

```ts
useEffect(() => {
  setSelectedTab(resolveTab(width, routeTab));
}, [width, routeTab]);
```

That makes resize and route synchronization accidental state transitions. It
also creates ordering problems because intent and presentation can overwrite
each other.

Instead, update intent in explicit event handlers and calculate the selected
result during render:

```ts
const [panelIntent, setPanelIntent] = useState<"overview" | "details">("overview");

const selectedTab = resolveSelectedTab({
  panelIntent,
  routeTab,
  isNarrow,
  isOpen,
});

const handleTabSelect = (tab: Tab) => {
  if (tab === "details") {
    setPanelIntent(isNarrow ? "details" : "overview");
  }

  navigateToTab(tab);
};
```

## Design Checklist

- Separate durable user intent from transient environment and navigation inputs.
- Define one pure function for the final selected or visible state.
- Mutate intent only from explicit semantic events.
- Let resize and capability changes recompute the output without writing state.
- Avoid storing any value that can be derived unambiguously.
- Test resize round trips: the rendered result may change while the underlying
  intent remains unchanged.

The invariant is: **context changes presentation; user actions change intent**.
