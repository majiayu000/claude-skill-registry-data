---
name: state-machine-transition
description: Add new states or transitions to Bob The Skull's state machine. Use when adding new states, defining transitions, implementing state behavior, or modifying state machine logic.
allowed-tools: Read, Edit, Grep
---

# State Machine Transitions

Adds new states or transitions to Bob The Skull's finite state machine that coordinates system behavior.

## When to Use

- Adding new states to the state machine
- Defining valid state transitions
- Implementing state entry/exit actions
- Adding timeout handling for states
- Documenting state behavior

## State Machine Overview

Bob uses a finite state machine (FSM) to coordinate all system behavior:

```
State Machine receives events → Decides transitions → Coordinates responses
```

**Current States:**
- `IDLE` - Waiting for wake word
- `WAKE_LISTENING` - Brief pause after wake word
- `GREETING` - Playing greeting audio
- `LISTENING` - Recording user speech
- `PROCESSING` - LLM thinking
- `SPEAKING` - Bob responding (TTS)
- `OBSERVING` - Vision-only mode
- `ERROR` - Error state with recovery

## State Machine Files

**Primary file:** `state_machine/state_machine.py`

Key components:
- `State` enum - Define all states
- `BobStateMachine` class - Core logic
- `_setup_event_handlers()` - Event subscriptions
- `_transition_to()` - State transition logic
- `on_<event>()` methods - Event handlers
- `_enter_<state>()` methods - State entry actions
- `_exit_<state>()` methods - State exit actions

## Adding a New State

### 1. Define State in Enum

```python
class State(Enum):
    """Bob's finite state machine states"""
    IDLE = "idle"
    WAKE_LISTENING = "wake_listening"
    GREETING = "greeting"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    OBSERVING = "observing"
    YOUR_NEW_STATE = "your_new_state"  # Add here
    ERROR = "error"
```

### 2. Define Valid Transitions

```python
# Valid state transitions
VALID_TRANSITIONS = {
    State.IDLE: [State.WAKE_LISTENING, State.OBSERVING, State.ERROR],
    State.WAKE_LISTENING: [State.GREETING, State.LISTENING, State.IDLE, State.ERROR],
    State.GREETING: [State.LISTENING, State.IDLE, State.ERROR],
    State.LISTENING: [State.PROCESSING, State.IDLE, State.ERROR],
    State.PROCESSING: [State.SPEAKING, State.IDLE, State.ERROR],
    State.SPEAKING: [State.IDLE, State.OBSERVING, State.ERROR],
    State.OBSERVING: [State.IDLE, State.WAKE_LISTENING, State.ERROR],
    State.YOUR_NEW_STATE: [State.IDLE, State.ERROR],  # Add here
    State.ERROR: [State.IDLE]
}
```

### 3. Define State Timeouts

```python
# State timeout configuration (seconds)
STATE_TIMEOUTS = {
    State.WAKE_LISTENING: 1.0,   # Brief pause
    State.GREETING: 10.0,         # Max greeting time
    State.LISTENING: 30.0,        # Max listening time
    State.PROCESSING: 60.0,       # Max LLM time
    State.SPEAKING: 120.0,        # Max TTS time
    State.OBSERVING: None,        # No timeout (continuous)
    State.YOUR_NEW_STATE: 15.0,   # Add appropriate timeout
    State.IDLE: None,             # No timeout
    State.ERROR: 5.0              # Error recovery time
}
```

### 4. Implement Entry Action

```python
def _enter_your_new_state(self):
    """Entry action for YOUR_NEW_STATE"""
    logger.info("Entering YOUR_NEW_STATE")

    # Start operations for this state
    # Example: Start a component, publish event, etc.

    # Publish state change event
    self.event_bus.publish(StateChangedEvent(
        old_state=self.previous_state.value if self.previous_state else None,
        new_state=State.YOUR_NEW_STATE.value,
        timestamp=datetime.now()
    ))
```

### 5. Implement Exit Action (Optional)

```python
def _exit_your_new_state(self):
    """Exit action for YOUR_NEW_STATE"""
    logger.info("Exiting YOUR_NEW_STATE")

    # Cleanup operations
    # Example: Stop component, clear state, etc.
```

### 6. Add Event Handlers

```python
def _setup_event_handlers(self):
    """Subscribe to events"""
    # ... existing subscriptions ...
    self.event_bus.subscribe(YourTriggerEvent, self.on_your_trigger_event)

def on_your_trigger_event(self, event: YourTriggerEvent):
    """Handle event that triggers transition to YOUR_NEW_STATE"""
    logger.info(f"Received YourTriggerEvent: {event}")

    if self.current_state == State.IDLE:
        # Transition to new state
        self._transition_to(State.YOUR_NEW_STATE)
```

### 7. Add Timeout Handler (If Needed)

```python
def _on_timeout(self, state: State):
    """Handle state timeout"""
    logger.warning(f"Timeout in state: {state.value}")

    if state == State.YOUR_NEW_STATE:
        # Handle timeout for your state
        logger.error("YOUR_NEW_STATE timed out")
        self._transition_to(State.IDLE)  # Or appropriate fallback
    # ... handle other states ...
```

## State Transition Pattern

```python
def _transition_to(self, new_state: State):
    """
    Transition to a new state

    Args:
        new_state: Target state
    """
    # Validate transition
    if new_state not in VALID_TRANSITIONS.get(self.current_state, []):
        logger.error(f"Invalid transition: {self.current_state.value} -> {new_state.value}")
        return False

    # Exit current state
    exit_method = getattr(self, f'_exit_{self.current_state.value}', None)
    if exit_method:
        try:
            exit_method()
        except Exception as e:
            logger.error(f"Error in exit action: {e}", exc_info=True)

    # Update state
    self.previous_state = self.current_state
    self.current_state = new_state
    self.state_start_time = time.time()

    # Enter new state
    entry_method = getattr(self, f'_enter_{new_state.value}', None)
    if entry_method:
        try:
            entry_method()
        except Exception as e:
            logger.error(f"Error in entry action: {e}", exc_info=True)
            self._transition_to(State.ERROR)
            return False

    # Start timeout timer if configured
    timeout = STATE_TIMEOUTS.get(new_state)
    if timeout:
        self._start_timeout_timer(timeout)

    logger.info(f"State transition: {self.previous_state.value} -> {new_state.value}")
    return True
```

## Common State Patterns

### Transient States (Brief, automatic exit)
```python
State.WAKE_LISTENING  # 1 second pause, then auto-transition
State.GREETING        # Play audio, then transition
```

Characteristics:
- Short timeout
- Entry action starts operation
- Auto-transition when operation completes

### Active States (Wait for events)
```python
State.LISTENING       # Wait for speech or silence
State.PROCESSING      # Wait for LLM response
```

Characteristics:
- Moderate timeout
- Entry action starts component
- Exit on component completion event

### Continuous States (No timeout)
```python
State.IDLE            # Wait indefinitely for wake word
State.OBSERVING       # Vision-only mode, no timeout
```

Characteristics:
- No timeout (None)
- Only exit on specific events
- May have periodic actions

### Error State (Recovery)
```python
State.ERROR           # Brief error state, then return to IDLE
```

Characteristics:
- Short timeout (5s)
- Entry logs error details
- Auto-transition to IDLE on timeout

## Event-Driven Transitions

Most transitions are triggered by events:

```python
# Wake word detected → WAKE_LISTENING
def on_wake_word_detected(self, event: WakeWordDetectedEvent):
    if self.current_state == State.IDLE:
        self._transition_to(State.WAKE_LISTENING)

# Speech recognized → PROCESSING
def on_speech_recognized(self, event: SpeechRecognizedEvent):
    if self.current_state == State.LISTENING:
        self.user_input = event.transcript
        self._transition_to(State.PROCESSING)

# LLM response → SPEAKING
def on_llm_response_ready(self, event: LLMResponseReadyEvent):
    if self.current_state == State.PROCESSING:
        self._transition_to(State.SPEAKING)
```

## Configuration Integration

States can be configured via BobConfig.py:

```python
# State machine configuration
STATE_MACHINE_WAKE_LISTENING_DURATION: float = 1.0
STATE_MACHINE_LISTENING_TIMEOUT: int = 30
STATE_MACHINE_PROCESSING_TIMEOUT: int = 60
STATE_MACHINE_SPEAKING_TIMEOUT: int = 120
STATE_MACHINE_ERROR_RECOVERY_TIME: int = 5
STATE_MACHINE_YOUR_NEW_STATE_TIMEOUT: int = 15  # Add config
```

Reference in state machine:

```python
STATE_TIMEOUTS = {
    State.YOUR_NEW_STATE: getattr(config, 'STATE_MACHINE_YOUR_NEW_STATE_TIMEOUT', 15.0)
}
```

## State Diagram Documentation

Update state diagram in documentation:

```
[IDLE] --wake word--> [WAKE_LISTENING] --pause complete--> [GREETING]
[GREETING] --greeting done--> [LISTENING]
[LISTENING] --speech recognized--> [PROCESSING]
[PROCESSING] --LLM response--> [SPEAKING]
[SPEAKING] --speech done--> [IDLE]

[YOUR_NEW_STATE] --trigger--> [IDLE]  # Document new transitions
```

## Testing State Transitions

```python
# test_state_machine.py
def test_your_new_state_transition():
    """Test transition to YOUR_NEW_STATE"""
    state_machine = BobStateMachine(event_bus, config)

    # Start in IDLE
    assert state_machine.current_state == State.IDLE

    # Trigger transition
    event_bus.publish(YourTriggerEvent(...))

    # Verify transition
    assert state_machine.current_state == State.YOUR_NEW_STATE

    # Verify timeout
    time.sleep(16)  # Wait for timeout
    assert state_machine.current_state == State.IDLE
```

## Checklist

- [ ] Add state to State enum
- [ ] Add valid transitions to VALID_TRANSITIONS
- [ ] Add timeout to STATE_TIMEOUTS
- [ ] Implement `_enter_<state>()` method
- [ ] Implement `_exit_<state>()` method (if needed)
- [ ] Add event handlers for transitions
- [ ] Add timeout handler in `_on_timeout()`
- [ ] Add configuration parameters (if needed)
- [ ] Update state diagram documentation
- [ ] Write unit tests for state
- [ ] Test transitions from all valid states
- [ ] Test timeout behavior
- [ ] Test error recovery

## Pro Tips

1. **Keep states focused** - Each state should have one clear purpose
2. **Define all transitions** - Explicitly list valid from→to pairs
3. **Add timeouts** - Every active state should have a timeout for recovery
4. **Log everything** - State transitions are critical for debugging
5. **Test edge cases** - What if event arrives in wrong state?
6. **Document intent** - Explain why state exists in docstring
7. **Handle errors** - All entry/exit actions should handle exceptions
