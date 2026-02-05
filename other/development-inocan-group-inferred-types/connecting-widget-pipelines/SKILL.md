---
name: connecting-widget-pipelines
description: Connecting StickerNest widgets via pipelines and ports. Use when the user asks about widget communication, connecting widgets, ports, inputs, outputs, pipelines, event routing, widget I/O, or making widgets talk to each other. Covers port definitions, type compatibility, event emission, and pipeline configuration.
---

# Connecting Widget Pipelines

This skill covers how widgets communicate in StickerNest v2 through the port and pipeline system. Widgets expose typed input/output ports that can be connected to create data flows.

## Core Concepts

### Ports
Typed connection points on widgets. Inputs receive data, outputs emit data.

### Pipelines
Named collections of connections between widget ports on a canvas.

### Events
The actual data flowing through connections. Each event has a type and payload.

---

## Defining Ports in Manifest

### Input Ports

```typescript
inputs: {
  trigger: {
    type: 'trigger',
    description: 'Activates the widget',
  },
  data: {
    type: 'any',
    description: 'Receives data from other widgets',
    default: null,
  },
  count: {
    type: 'number',
    description: 'Numeric input value',
    default: 0,
    required: false,
  },
}
```

### Output Ports

```typescript
outputs: {
  result: {
    type: 'any',
    description: 'Processed output data',
  },
  clicked: {
    type: 'trigger',
    description: 'Emitted when widget is clicked',
  },
  valueChanged: {
    type: 'number',
    description: 'Current value after change',
  },
}
```

---

## Port Types

| Type | Description | Compatible With |
|------|-------------|-----------------|
| `trigger` | Signal with no data (void) | `trigger`, `any` |
| `string` | Text data | `string`, `any` |
| `number` | Numeric data | `number`, `any` |
| `boolean` | True/false | `boolean`, `any` |
| `object` | JSON object | `object`, `any` |
| `array` | JSON array | `array`, `any` |
| `any` | Accepts anything | All types |

### Type Compatibility Rules

1. **Exact match**: Same types always connect
2. **Any accepts all**: `any` input accepts any output type
3. **Any outputs to all**: `any` output connects to any input
4. **Trigger is special**: Only connects to `trigger` or `any`

---

## I/O Capability Declarations

The `io` field provides AI-friendly hints for automatic wiring:

```typescript
io: {
  inputs: [
    'trigger.activate',      // Trigger to activate widget
    'data.set',              // Set widget data
    'ui.show',               // Show the widget
    'ui.hide',               // Hide the widget
  ],
  outputs: [
    'data.result',           // Output result data
    'ui.clicked',            // User clicked
    'state.changed',         // State changed
  ],
}
```

### Common I/O Patterns

| Pattern | Description |
|---------|-------------|
| `trigger.*` | Activation signals |
| `data.*` | Data transfer |
| `ui.*` | User interaction events |
| `state.*` | State changes |
| `text.*` | Text-specific operations |
| `media.*` | Media events (play, pause, etc.) |

---

## Receiving Input Events

### Using WidgetAPI

```javascript
const API = window.WidgetAPI;

// Single input handler
API.onInput('data.set', function(value) {
  console.log('Received data:', value);
  // Process the input
  updateDisplay(value);
});

// Multiple inputs
API.onInput('trigger.activate', function() {
  performAction();
});

API.onInput('text.set', function(text) {
  if (typeof text === 'string') {
    state.text = text;
  } else if (text?.content) {
    state.text = text.content;
  }
  updateDisplay();
});
```

### Using postMessage (Protocol v3.0)

```javascript
window.addEventListener('message', (event) => {
  if (event.data.type === 'widget:event') {
    const { type, payload } = event.data.payload || {};

    switch (type) {
      case 'trigger.activate':
        performAction();
        break;
      case 'data.set':
        handleData(payload);
        break;
    }
  }

  // Alternative pipeline input format
  if (event.data.type === 'pipeline:input') {
    const { portName, value } = event.data;
    handleInput(portName, value);
  }
});
```

---

## Emitting Output Events

### Using WidgetAPI

```javascript
const API = window.WidgetAPI;

// Emit to specific output port
API.emitOutput('data.result', {
  value: 42,
  processed: true
});

// Emit trigger (no payload needed)
API.emitOutput('ui.clicked', {});

// Emit with state update
function handleClick() {
  state.clickCount++;
  API.setState({ clickCount: state.clickCount });
  API.emitOutput('state.changed', {
    clickCount: state.clickCount
  });
}
```

### Using postMessage (Protocol v3.0)

```javascript
function emit(portId, data) {
  window.parent.postMessage({
    type: 'widget:emit',
    payload: {
      type: portId,      // MUST match io.outputs[].id
      payload: data
    }
  }, '*');
}

// Usage
emit('data.result', { value: 42 });
emit('ui.clicked', {});
```

---

## Broadcast Events (Canvas-Wide)

For events that should reach all widgets on the canvas:

### Emitting Broadcasts

```javascript
// Using WidgetAPI
API.emit('weather.update', {
  sunny: true,
  temperature: 72
});

// These go to ALL widgets, not just connected ones
API.emit('theme.changed', { dark: true });
```

### Listening to Broadcasts

```javascript
API.on('weather.update', function(payload) {
  // Handle weather update from any widget
  updateWeatherDisplay(payload);
});
```

### Declaring Broadcast Events in Manifest

```typescript
events: {
  emits: ['weather.update', 'game.tick'],
  listens: ['theme.changed', 'canvas.resize'],
}
```

---

## Pipeline Structure

Pipelines are stored in the canvas state:

```typescript
interface Pipeline {
  id: string;
  canvasId: string;
  name: string;
  enabled: boolean;
  nodes: PipelineNode[];
  connections: PipelineConnection[];
}

interface PipelineNode {
  id: string;
  widgetId: string;           // Widget instance ID
  config?: Record<string, any>;
}

interface PipelineConnection {
  id: string;
  sourceNodeId: string;       // Source widget node
  sourcePortId: string;       // Output port ID
  targetNodeId: string;       // Target widget node
  targetPortId: string;       // Input port ID
  transformFn?: string;       // Optional transform code
}
```

---

## Common Connection Patterns

### Button -> Action

```
[Button Widget]          [Action Widget]
  ui.clicked ---------> trigger.activate
```

### Data Producer -> Consumer

```
[API Widget]            [Display Widget]
  data.result --------> data.set
```

### Counter -> Multiple Displays

```
[Counter Widget]        [Display A]
  valueChanged -------> data.set
        |
        +-------------> [Display B]
                        data.set
```

### Chained Processing

```
[Input] -> [Transform A] -> [Transform B] -> [Output]
result     data.set         data.set         data.set
           result           result
```

---

## Transform Functions

Connections can include transform functions to modify data:

```typescript
// In pipeline connection
{
  sourceNodeId: 'widget-a',
  sourcePortId: 'data.result',
  targetNodeId: 'widget-b',
  targetPortId: 'data.set',
  transformFn: `
    // 'value' is the incoming data
    return {
      ...value,
      transformed: true,
      timestamp: Date.now()
    };
  `
}
```

---

## Debugging Connections

### Using Debug Panel

1. Open Debug tab in StickerNest
2. Watch "Events" section for real-time event flow
3. Check "Pipeline" section for connection status

### Console Logging

```javascript
API.onInput('data.set', function(value) {
  API.log('Received on data.set: ' + JSON.stringify(value));
  // Process...
});
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Events not received | Port ID mismatch | Ensure port IDs in code match manifest exactly |
| Wrong data format | Type incompatibility | Check type compatibility or use `any` |
| No events flowing | Missing connection | Verify pipeline connection exists in canvas |
| Events to wrong widget | Wrong targetNodeId | Check pipeline configuration |

---

## Example: Complete Connected Widget

### Manifest

```typescript
export const DataProcessorManifest: WidgetManifest = {
  id: 'stickernest.data-processor',
  name: 'Data Processor',
  version: '1.0.0',
  kind: 'interactive',
  entry: 'index.html',
  description: 'Transforms incoming data and outputs result',
  inputs: {
    rawData: {
      type: 'any',
      description: 'Raw data to process',
    },
    trigger: {
      type: 'trigger',
      description: 'Process immediately',
    },
  },
  outputs: {
    processed: {
      type: 'object',
      description: 'Processed data output',
    },
    error: {
      type: 'string',
      description: 'Error message if processing fails',
    },
  },
  capabilities: { draggable: true, resizable: true, rotatable: true },
  io: {
    inputs: ['data.raw', 'trigger.process'],
    outputs: ['data.processed', 'error.message'],
  },
  size: { width: 180, height: 120 },
};
```

### HTML Implementation

```html
<script>
(function() {
  const API = window.WidgetAPI;
  let pendingData = null;

  function process() {
    if (!pendingData) return;

    try {
      const result = {
        original: pendingData,
        processed: true,
        timestamp: Date.now(),
      };
      API.emitOutput('data.processed', result);
      API.log('Processing complete');
    } catch (err) {
      API.emitOutput('error.message', err.message);
    }
  }

  API.onInput('data.raw', function(data) {
    pendingData = data;
    // Auto-process on data receive
    process();
  });

  API.onInput('trigger.process', function() {
    process();
  });

  API.onMount(function(context) {
    pendingData = context.state?.pendingData || null;
  });
})();
</script>
```

---

## Reference Files

- **Port types**: `src/types/manifest.ts` (WidgetInputSchema, WidgetOutputSchema)
- **Pipeline runtime**: `src/runtime/PipelineRuntime.ts`
- **Port compatibility**: `src/runtime/PortCompatibility.ts`
- **Event bus**: `src/runtime/EventBus.ts`
- **Protocol spec**: `Docs/WIDGET-PROTOCOL-SPEC.md`
