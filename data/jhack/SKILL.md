---
name: jhack
description: Expert assistant for Juju charm development using jhack utilities. Use when debugging charms, inspecting relations, syncing code, replaying events, testing scenarios, or performing rapid development iterations. Keywords include jhack, Juju debugging, charm testing, relation inspection, event replay, sync, tail, fire, show-relation, show-stored.
license: Apache-2.0
compatibility: Requires jhack and juju installed locally. Network access needed for model operations.
allowed-tools: Bash(jhack:*) Bash(juju:*) Read
---

# Jhack Development Assistant

Expert guidance for using jhack utilities to streamline Juju charm development, debugging, and testing.

## What is Jhack?

Jhack is a collection of developer utilities that make charm development faster and easier by:
- Providing shortcuts for common operations
- Enabling rapid code iteration without redeployment
- Visualising charm state and relations
- Capturing and replaying real events
- Simplifying debugging workflows

## Core Workflows

### Inspecting Charm State

```bash
# View relation databags
jhack show-relation myapp postgresql
jhack show-relation myapp:database postgresql:database  # Specific endpoints

# View charm stored state
jhack show-stored myapp/0
jhack show-stored myapp/leader  # Leader unit

# List integration endpoints
jhack list-endpoints myapp

# Get charm version info
jhack charm-info myapp/0
```

**`show-relation`** displays what data charms are sharing in a relation as a formatted table, making debugging integration issues much easier.

**`show-stored`** shows the persistent state stored by the charm (via `StoredState` in Ops framework).

### Live Development with Sync

```bash
# Sync local source to running unit (watch mode)
jhack sync src/ myapp/0

# Sync specific directories
jhack sync --src=./src --src=./lib myapp/0

# One-time sync (no watching)
jhack sync --no-watch src/ myapp/0
```

**Use case:** Edit code locally, jhack automatically pushes changes to the running unit. Combined with `jhack utils fire`, you can test changes in seconds without repacking and redeploying.

**For packed charm sync:** Use `jhack charm sync-packed`

### Monitoring Events

```bash
# Watch all events in real-time
jhack tail

# Watch specific unit
jhack tail myapp/0

# Watch with debug output
jhack tail -d myapp/0

# Filter by event type
jhack tail --filter=config-changed
```

**`tail`** provides a colour-coded, hierarchical view of charm events as they fire, showing:
- Event names
- Handler execution
- Nested events (e.g., relation-changed triggering config-changed)
- Timing information

### Firing Events Manually

```bash
# Fire a specific event
jhack utils fire myapp/0 config-changed
jhack utils fire myapp/0 database-relation-changed

# Fire with specific relation
jhack fire myapp/0 upgrade-charm

# Speed up update-status for testing
jhack ffwd myapp --interval=10s  # Every 10 seconds
jhack ffwd myapp --stop          # Reset to normal
```

**Use case:** Test specific event handlers without waiting for natural triggers or performing manual operations.

### Event Replay (Advanced)

```bash
# Install recorder on unit
jhack replay install myapp/0

# List captured events
jhack replay list myapp/0

# Replay a specific event
jhack replay emit myapp/0 5  # Replay event #5

# Dump event data
jhack replay dump myapp/0 5

# Purge recorded events
jhack replay purge myapp/0
```

**Use case:** Capture real production events (with all their context and data) and replay them for debugging or testing.

### Scenario Testing

```bash
# Capture current state as scenario
jhack scenario snapshot myapp/0 > state.json

# Apply a state to a unit
jhack scenario state-apply myapp/0 state.json
```

**Integration with ops-scenario:** Use `snapshot` to capture real charm state, then use it in unit tests with the Ops state-transition (unit) testing framework.

### Charm Manipulation

```bash
# Update packed charm with local files
jhack charm update myapp.charm src/

# Sync packed charm continuously
jhack charm sync-packed --src=./src --charm=myapp.charm

# Lobotomize charm (prevent event processing)
jhack charm lobotomy myapp/0  # Enable
jhack charm lobotomy myapp/0 --undo  # Disable

# Force unit to become leader
jhack utils elect myapp/1  # Make unit 1 the leader
```

**`lobotomy`** is useful for freezing a charm's behavior during debugging - it prevents the charm from processing any events.

### Pebble Commands (K8s Charms)

```bash
# Run pebble commands on remote units
jhack pebble -c mycontainer myapp/0 plan
jhack pebble -c mycontainer myapp/0 services
jhack pebble -c mycontainer myapp/0 logs myservice
jhack pebble -c mycontainer myapp/0 exec "ls -la /"
```

**Shortcut for:** `juju ssh --container=mycontainer myapp/0 -- pebble <command>`

### Debugging and Logs

```bash
# Unified log view (charm + containers)
jhack debug-log myapp/0

# Execute Python in charm context
jhack script myapp/0 myscript.py

# Evaluate expression
jhack eval myapp/0 "self.unit.status"
```

**`script`** and **`eval`** let you run arbitrary Python code in the context of a live charm, with access to the charm instance.

### Destructive Operations

```bash
# Safe removal with pattern matching
jhack nuke myapp          # Remove application
jhack nuke "test-*"       # Remove all apps matching pattern
jhack nuke --model=mymodel --all  # Nuke entire model

# Kill stuck hook execution
jhack kill myapp/0

# Auto-resolve all error states (use carefully!)
jhack utils this-is-fine
```

**Safety:** All destructive commands require confirmation unless you enable devmode: `jhack conf set devmode=true`

### Chaos Testing

```bash
# Stress test charm through rapid changes
jhack chaos mancioppi myapp --duration=300  # 5 minutes
jhack chaos flicker myapp  # Rapid scaling up/down
```

**Use case:** Identify race conditions and state management issues by rapidly scaling, relating, and modifying charms.

## Common Workflows

### Rapid Development Iteration

1. Deploy charm: `juju deploy ./myapp.charm`
2. Start sync: `jhack sync src/ myapp/0`
3. Edit code locally
4. Fire event to test: `jhack utils fire myapp/0 config-changed`
5. Watch events: `jhack tail myapp/0 -d`
6. Inspect state: `jhack show-stored myapp/0`

**Result:** Test changes in seconds instead of minutes.

### Debugging Integration Issues

1. Check relation data: `jhack show-relation myapp postgresql`
2. Fire relation event: `jhack utils fire myapp/0 database-relation-changed`
3. Watch handler execution: `jhack tail myapp/0 -d`
4. Inspect stored state: `jhack show-stored myapp/0`

### Capturing Production Issues

1. Install recorder: `jhack replay install myapp/0`
2. Wait for issue to occur
3. List events: `jhack replay list myapp/0`
4. Dump problematic event: `jhack replay dump myapp/0 <id>`
5. Replay locally: `jhack replay emit myapp/0 <id>`

### Testing Leadership Changes

1. Check current leader: `juju status`
2. Force different unit to lead: `jhack utils elect myapp/1`
3. Test leader-specific behavior
4. Watch events: `jhack tail myapp`

## Command Quick Reference

```bash
# Inspection
jhack show-relation <app> <app>      # View relation data
jhack show-stored <unit>              # View stored state
jhack tail [unit]                     # Watch events
jhack charm-info <unit>               # Charm version info

# Development
jhack sync <src> <unit>               # Sync code to unit
jhack utils fire <unit> <event>       # Fire event manually
jhack ffwd <app> --interval=10s       # Speed up update-status

# Replay
jhack replay install <unit>           # Install recorder
jhack replay list <unit>              # List events
jhack replay emit <unit> <id>         # Replay event

# Scenario
jhack scenario snapshot <unit>        # Capture state
jhack scenario state-apply <unit> <file>  # Apply state

# Pebble (K8s)
jhack pebble -c <container> <unit> <command>

# Debugging
jhack debug-log <unit>                # Unified logs
jhack eval <unit> <expression>        # Evaluate in charm context
jhack script <unit> <script>          # Execute Python script

# Manipulation
jhack charm lobotomy <unit>           # Freeze charm
jhack utils elect <unit>              # Force leadership
jhack kill <unit>                     # Kill hook

# Cleanup
jhack nuke <pattern>                  # Safe removal
jhack utils this-is-fine              # Auto-resolve errors

# Chaos
jhack chaos mancioppi <app>           # Stress test
```

## Integration with Development Tools

### With Tox
```bash
# Edit charm code
vim src/charm.py

# Format and lint
tox -e format
tox -e lint

# Sync to unit
jhack sync src/ myapp/0

# Test specific handler
jhack utils fire myapp/0 config-changed
```

### With Ops-Scenario
```python
# Capture real state
# $ jhack scenario snapshot myapp/0 > tests/state.json

# Use in tests
import json

from ops import testing

with open('tests/state.json') as f:
    state = testing.State.from_dict(json.load(f))

# Test with real production state
ctx = testing.Context(MyCharm)
ctx.run(event, state)
```

### With Charmcraft
```bash
# Pack charm
charmcraft pack

# Update running charm without redeploying
jhack charm update myapp.charm src/

# Or continuously sync packed charm
jhack charm sync-packed --charm=myapp.charm --src=./src
```

## Best Practices

### Development
1. **Use sync for rapid iteration** - Don't repack/redeploy for every change
2. **Watch events with tail -d** - Understand what's happening
3. **Fire events manually** - Test specific scenarios quickly
4. **Capture real states** - Use scenario snapshot for realistic test data

### Debugging
1. **Start with show-relation** - Most integration issues are data problems
2. **Check show-stored** - Verify state persistence
3. **Use replay for production issues** - Capture and replay real events
4. **Enable debug logging** - `jhack tail -d` shows detailed output

### Testing
1. **Use scenario snapshots** - Test against real charm states
2. **Test leadership changes** - Use `elect` to simulate failover
3. **Stress test with chaos** - Find race conditions early
4. **Lobotomize for state inspection** - Freeze charm to inspect state

### Safety
1. **Enable devmode only in dev** - `jhack conf set devmode=false` for production
2. **Use --dry-run** - Many commands support dry-run mode
3. **Verify nuke targets** - Double-check pattern matching before confirming
4. **Be careful with this-is-fine** - Only use when you understand why units errored

## Configuration

```bash
# View configuration
jhack conf show

# Set devmode (skip confirmations)
jhack conf set devmode=true

# Set log level
jhack --loglevel=DEBUG <command>

# Log to file
jhack --log-to-file=jhack.log <command>
```

## Troubleshooting

**Sync not working:**
- Ensure SSH access: `juju ssh myapp/0`
- Check source path exists locally
- Verify unit is active: `juju status`

**Events not appearing in tail:**
- Check you're watching the right model: `juju models`
- Switch model: `juju switch <model>`
- Verify unit name: `juju status`

**Replay fails:**
- Ensure recorder installed: `jhack replay install myapp/0`
- Check database exists: `jhack replay list myapp/0`
- Verify event ID: Use list output

**Pebble commands fail:**
- Verify container name: `juju ssh myapp/0 -- pebble version`
- Check K8s charm: Machine charms don't use Pebble
- Ensure container is ready: `juju status`

**For comprehensive troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md)**

## Resources

- **Jhack GitHub**: https://github.com/canonical/jhack
- **Juju docs**: https://documentation.ubuntu.com/juju/3.6/
- **Ops-scenario**: https://documentation.ubuntu.com/ops/latest/reference/ops-testing/
- **Ops framework**: https://documentation.ubuntu.com/ops/

## Additional References

When you need detailed information:
- **Complete command reference**: See [references/command-reference.md](references/command-reference.md)
- **Troubleshooting guide**: See [references/troubleshooting.md](references/troubleshooting.md)
- **Workflow examples**: See [references/workflows.md](references/workflows.md)

---

**Key reminders:**
- Use `jhack sync` for rapid development iteration
- `tail -d` is your friend for debugging
- Capture production issues with `replay`
- Test with real state using `scenario snapshot`
- Enable devmode only in development environments
