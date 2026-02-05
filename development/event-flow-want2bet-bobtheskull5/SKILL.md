---
name: event-flow
description: Add new events to Bob The Skull's event-driven architecture. Use when creating new events, event publishers, event handlers, or extending the event system with new event types.
allowed-tools: Read, Edit, Grep, Glob
---

# Event Flow Management

Adds new events to Bob The Skull's event-driven architecture, ensuring all publishers and subscribers are properly connected.

## When to Use

- Creating new event types
- Adding event publishers (components that emit events)
- Adding event subscribers (components that handle events)
- Documenting event flows
- Troubleshooting missing event handlers

## Event-Driven Architecture Overview

Bob The Skull uses a central EventBus for all inter-component communication:

```
Component A → publish(Event) → EventBus → deliver → Component B.on_event()
```

**No direct method calls between components!** Everything goes through events.

## Event Definition Pattern (events.py)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class YourEvent:
    """Published when [describe condition that triggers event]"""
    param1: type  # Description
    param2: type  # Description
    optional_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
```

### Common Event Types

**State Change Events:**
```python
@dataclass
class ComponentStateChangedEvent:
    """Component changed state"""
    component: str
    old_state: str
    new_state: str
    timestamp: datetime = field(default_factory=datetime.now)
```

**Detection Events:**
```python
@dataclass
class ThingDetectedEvent:
    """Thing was detected"""
    confidence: float
    location: tuple
    detector_id: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
```

**Request/Response Events:**
```python
@dataclass
class ProcessRequestEvent:
    """Request to process something"""
    request_id: str
    input_data: Any
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ProcessResponseEvent:
    """Response to process request"""
    request_id: str
    result: Any
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)
```

## Publishing Events

**In component code:**

```python
from events import YourEvent

class YourComponent:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def do_something(self):
        # When condition occurs, publish event
        event = YourEvent(
            param1=value1,
            param2=value2
        )
        self.event_bus.publish(event)
        logger.info(f"Published YourEvent: {event}")
```

## Subscribing to Events

**In component code:**

```python
from events import YourEvent

class YourComponent:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        # Subscribe to event during initialization
        self.event_bus.subscribe(YourEvent, self.on_your_event)

    def on_your_event(self, event: YourEvent):
        """Handle YourEvent"""
        logger.info(f"Received YourEvent: {event}")
        # Process event
        self.do_something_with(event.param1, event.param2)
```

## State Machine Integration

State machine is a special subscriber that coordinates system behavior:

```python
# In state_machine/state_machine.py

def _setup_event_handlers(self):
    """Subscribe to events"""
    self.event_bus.subscribe(YourEvent, self.on_your_event)

def on_your_event(self, event: YourEvent):
    """Handle YourEvent in state machine"""
    logger.info(f"State machine received: {event}")

    # Check current state
    if self.current_state == State.WAITING:
        # Transition to new state
        self._transition_to(State.PROCESSING)
        # Trigger actions
        self._handle_processing(event)
```

## Event Flow Checklist

When adding a new event:

- [ ] Define event dataclass in `events.py`
- [ ] Find all components that should **publish** this event
- [ ] Find all components that should **subscribe** to this event
- [ ] Add publishers: `event_bus.publish(YourEvent(...))`
- [ ] Add subscribers: `event_bus.subscribe(YourEvent, self.on_event)`
- [ ] Add handlers: `def on_your_event(self, event: YourEvent):`
- [ ] Update state machine if needed
- [ ] Test event flow end-to-end
- [ ] Document event flow in comments/docstrings

## Finding Event Usage

**Find where event is published:**
```bash
grep -r "YourEvent(" .
```

**Find where event is subscribed:**
```bash
grep -r "subscribe.*YourEvent" .
```

**Find event handlers:**
```bash
grep -r "def on_your_event" .
```

## Common Event Patterns

### Vision Detection Events
- Published by: Detector plugins
- Subscribed by: State machine, vision processor
- Pattern: `*DetectedEvent`, `*ClearedEvent`

### Speech Events
- Published by: STT, wake word detector
- Subscribed by: State machine
- Pattern: `*RecognizedEvent`, `*DetectedEvent`

### LLM Events
- Published by: LLM processor
- Subscribed by: State machine, TTS
- Pattern: `*ResponseEvent`, `*ToolCallEvent`

### Hardware Events
- Published by: Hardware controllers
- Subscribed by: State machine
- Pattern: `*StatusEvent`, `*ErrorEvent`

## Event Bus Implementation

Bob uses two event bus implementations:

**LocalEventBus** - In-process pub/sub
```python
from local_event_bus import LocalEventBus
event_bus = LocalEventBus()
```

**MQTTEventBus** - Distributed pub/sub
```python
from mqtt_event_bus import MQTTEventBus
event_bus = MQTTEventBus(broker="192.168.1.44")
```

Both implement the same interface:
- `publish(event)` - Send event
- `subscribe(event_type, handler)` - Register handler
- `unsubscribe(event_type, handler)` - Remove handler

## Existing Events Reference

**Core events in `events.py`:**
- `WakeWordDetectedEvent` - Wake word heard
- `SpeechRecognizedEvent` - Speech transcribed
- `LLMResponseReadyEvent` - LLM response available
- `LLMToolCallEvent` - LLM wants to call tool
- `TTSStartedEvent` / `TTSCompletedEvent` - TTS lifecycle
- `FaceDetectedEvent` / `FaceIdentifiedEvent` - Vision events
- `MotionDetectedEvent` / `MotionClearedEvent` - Motion events
- `StateChangedEvent` - State machine transitions

## Event Naming Conventions

**Event Names:**
- Use descriptive nouns: `ThingDetected`, not `DetectThing`
- End with `Event`: `FaceDetectedEvent`
- Use past tense: `Detected`, not `Detect`

**Handler Names:**
- Prefix with `on_`: `on_face_detected`
- Use snake_case: `on_speech_recognized`
- Match event name: `FaceDetectedEvent` → `on_face_detected`

## Debugging Event Flows

**Enable event logging:**
```python
# In LocalEventBus or MQTTEventBus
logger.setLevel(logging.DEBUG)
```

**Trace event flow:**
```python
# In event_bus.py
def publish(self, event):
    logger.debug(f"Publishing: {type(event).__name__} to {len(self.subscribers.get(type(event), []))} subscribers")
    # ... publish logic
```

**Check subscriptions:**
```python
# In component
logger.info(f"Subscribed to: {[t.__name__ for t in self.event_bus.subscribers.keys()]}")
```

## Pro Tips

1. **Events are immutable** - Use dataclasses with frozen=False for mutable data
2. **Include context** - Always add detector_id, component_id, etc.
3. **Timestamp everything** - Use `field(default_factory=datetime.now)`
4. **Document triggers** - Explain in docstring what causes the event
5. **Test isolation** - Mock event_bus for unit tests
6. **Avoid event storms** - Debounce high-frequency events
7. **Use type hints** - Makes IDE autocomplete work perfectly
