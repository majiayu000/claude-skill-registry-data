---
name: go-fsm
description: Finite state machine patterns in Go - typed states, transition guards, event broadcasting, and state-aware operations for process or workflow lifecycle management
triggers:
  - state machine
  - finite state machine
  - FSM
  - state transition
  - transition guard
  - lifecycle states
  - state management
  - workflow state
  - process state
  - state event
---

## Role

Expert Go developer specializing in explicit finite state machines: typed state constants, validated transitions, state-based operation guards, and event broadcasting via channels — without third-party FSM libraries.

## Instructions

### Response Format

Produce production-ready FSM implementations in Go:

1. **State type**: `type State int` with `iota` constants — not stringly typed
2. **Transition table**: `map[State][]State` or `CanTransitionTo(target State) bool` method
3. **Transition enforcement**: `Transition(target State) error` validates before mutating
4. **Operation guards**: `EnsureState(allowed ...State) error` before any state-dependent operation
5. **Event broadcasting**: `chan StateEvent` with `from`/`to`/`time` fields; buffered to avoid blocking
6. **Concurrency**: `sync.RWMutex` — write lock only on transition, read lock for state queries
7. **Error sentinel**: `ErrInvalidTransition` with `from`/`to` fields for caller inspection
8. **String representation**: `func (s State) String() string` via a `[...]string` array lookup

### Edge Cases

If the FSM is part of a long-running service: integrate with context cancellation to drain the event channel on shutdown.

If states carry data (tagged union): use a struct with `State` field plus optional payload; avoid interface embedding for state data.

If the transition graph is large (>10 states): use a `map[State][]State` adjacency list instead of a `switch` in `CanTransitionTo`.

If testing state machines: verify both valid transitions and rejection of invalid ones; test concurrent transitions under `-race`.

## Examples

<example>
<input>Implement a process state machine with Stopped/Starting/Running/Stopping/Error states and transition validation</input>
<output>
```go
package process

import (
    "fmt"
    "sync"
    "time"
)

type State int

const (
    StateStopped State = iota
    StateStarting
    StateRunning
    StateStopping
    StateError
)

var stateNames = [...]string{
    StateStopped:  "stopped",
    StateStarting: "starting",
    StateRunning:  "running",
    StateStopping: "stopping",
    StateError:    "error",
}

func (s State) String() string {
    if int(s) < len(stateNames) {
        return stateNames[s]
    }
    return "unknown"
}

// valid defines allowed transitions.
var valid = map[State][]State{
    StateStopped:  {StateStarting},
    StateStarting: {StateRunning, StateError},
    StateRunning:  {StateStopping, StateError},
    StateStopping: {StateStopped, StateError},
    StateError:    {StateStarting, StateStopped},
}

func (s State) CanTransitionTo(target State) bool {
    for _, t := range valid[s] {
        if t == target {
            return true
        }
    }
    return false
}

type TransitionError struct {
    From, To State
}

func (e *TransitionError) Error() string {
    return fmt.Sprintf("invalid transition: %s → %s", e.From, e.To)
}

type StateEvent struct {
    From, To State
    At       time.Time
}

type StateMachine struct {
    mu      sync.RWMutex
    state   State
    eventCh chan StateEvent
}

func NewStateMachine(initial State, buf int) *StateMachine {
    return &StateMachine{
        state:   initial,
        eventCh: make(chan StateEvent, buf),
    }
}

func (sm *StateMachine) State() State {
    sm.mu.RLock()
    defer sm.mu.RUnlock()
    return sm.state
}

func (sm *StateMachine) Events() <-chan StateEvent { return sm.eventCh }

func (sm *StateMachine) Transition(target State) error {
    sm.mu.Lock()
    defer sm.mu.Unlock()

    if !sm.state.CanTransitionTo(target) {
        return &TransitionError{From: sm.state, To: target}
    }

    ev := StateEvent{From: sm.state, To: target, At: time.Now()}
    sm.state = target

    select {
    case sm.eventCh <- ev:
    default: // drop if no consumer; never block
    }
    return nil
}

// EnsureState returns an error if the current state is not one of the allowed states.
func (sm *StateMachine) EnsureState(allowed ...State) error {
    sm.mu.RLock()
    cur := sm.state
    sm.mu.RUnlock()

    for _, s := range allowed {
        if cur == s {
            return nil
        }
    }
    return fmt.Errorf("operation requires state in %v, got %s", allowed, cur)
}
```
</output>
</example>

<example>
<input>Use the state machine in a service — guard Start() and Stop() with state checks</input>
<output>
```go
type Service struct {
    fsm *StateMachine
    mgr *Manager // subprocess manager
}

func (s *Service) Start(ctx context.Context) error {
    if err := s.fsm.EnsureState(StateStopped, StateError); err != nil {
        return fmt.Errorf("start: %w", err)
    }
    if err := s.fsm.Transition(StateStarting); err != nil {
        return err
    }

    if err := s.mgr.Start(ctx); err != nil {
        _ = s.fsm.Transition(StateError)
        return fmt.Errorf("start process: %w", err)
    }

    return s.fsm.Transition(StateRunning)
}

func (s *Service) Stop() error {
    if err := s.fsm.EnsureState(StateRunning); err != nil {
        return fmt.Errorf("stop: %w", err)
    }
    if err := s.fsm.Transition(StateStopping); err != nil {
        return err
    }

    if err := s.mgr.Stop(); err != nil {
        _ = s.fsm.Transition(StateError)
        return fmt.Errorf("stop process: %w", err)
    }

    return s.fsm.Transition(StateStopped)
}
```
</output>
</example>

<example>
<input>Subscribe to state events and log transitions</input>
<output>
```go
func watchState(ctx context.Context, sm *StateMachine, log *slog.Logger) {
    for {
        select {
        case ev := <-sm.Events():
            log.Info("state changed",
                "from", ev.From,
                "to", ev.To,
                "at", ev.At,
            )
        case <-ctx.Done():
            return
        }
    }
}
```
</output>
</example>

## References

- [Constraints](references/constraints.md)
- [FSM Patterns](references/fsm-patterns.md)
