---
name: xarm
description: Reference for xArm robot setup and motion using the xarm-python-sdk. Use when debugging xArm connection or motion issues, starting a new project with xArm, or verifying that initialization and movement follow a known-working pattern.
argument-hint: [optional: describe the issue or what you're setting up]
---

# xArm — Known-Working Reference

Ground truth patterns extracted from working pipelines (`xarm_setup/goto_capture.py`, `xarm_setup/datagen.py`). When debugging arm issues in a new project, compare against these minimal sequences.

## Connection

```python
from xarm.wrapper import XArmAPI
import atexit

arm = XArmAPI('192.168.1.241')
atexit.register(arm.disconnect)
```

The `atexit` pattern ensures the socket is released even on crash. Without `disconnect()`, the arm's TCP server may reject subsequent connections.

## Enable Sequence

The arm must be enabled before any motion command. This is the minimum:

```python
import time

arm.clean_error()
arm.clean_warn()
arm.motion_enable(enable=True)
arm.set_mode(0)       # 0 = position control mode
arm.set_state(state=0) # 0 = ready/sport state
time.sleep(0.5)
```

### Mode Reference

- **Mode 0**: Position control — arm executes `set_position` commands. Used for programmatic motion.
- **Mode 2**: Manual/teach mode — arm is compliant, user can physically move it. Used for kinesthetic teaching.

### Recovery from Error/Stop State

If the arm enters state 4 (STOP) or 5 (ERROR), the full enable sequence must be re-run:

```python
code, state = arm.get_state()
if state in (4, 5):
    arm.clean_error()
    arm.clean_warn()
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    time.sleep(0.5)
```

After recovery, verify: `arm.get_state()` should return state 1, 2, or 3.

## TCP Offset

If a tool is mounted, set the TCP offset **before** enabling:

```python
arm.set_tcp_offset([x, y, z, roll, pitch, yaw], is_radian=False)
```

This was called before `enable_arm()` in the working datagen pipeline. The offset shifts the tool-center-point relative to the flange.

## Motion — Go To Pose

Cartesian position control (mode 0):

```python
code = arm.set_position(
    x=x, y=y, z=z,            # mm
    roll=roll, pitch=pitch, yaw=yaw,  # degrees (unless is_radian=True)
    wait=True,
    radius=-1.0                # -1.0 = move in straight line, no blending
)
assert code == 0, f"set_position failed: code={code}"
```

### Verifying Position After Move

```python
code, pose = arm.get_position()
assert code == 0, f"get_position failed: code={code}"
# pose = [x, y, z, roll, pitch, yaw]
```

### Error Inspection on Failure

```python
code, state = arm.get_state()
code, err = arm.get_err_warn_code()
# err = [error_code, warning_code]
```

## Ordering Invariants

1. `XArmAPI(ip)` — connection must be established first
2. `set_tcp_offset(...)` — if needed, set before enabling
3. `clean_error()` → `clean_warn()` → `motion_enable()` → `set_mode()` → `set_state()` — this exact sequence enables the arm
4. `time.sleep(0.5)` — the arm needs a moment after `set_state` before it's truly ready
5. `set_position(...)` — only valid after enable sequence, only in mode 0
6. `arm.disconnect()` — must be called to release the TCP socket

## Common Failure Modes

- **Connection refused**: Prior session didn't call `disconnect()`. Power-cycle the controller or wait for the TCP timeout.
- **set_position returns non-zero**: Arm may be in error state. Run the full recovery sequence above.
- **Arm doesn't move after enable**: Forgot `set_state(state=0)` or didn't wait long enough after it. The `time.sleep(0.5)` matters.
- **Wrong positions with tool mounted**: TCP offset not set, or set after enabling. Set it before the enable sequence.
- **State 4/5 after motion**: Arm hit a joint limit, singularity, or collision threshold. `clean_error()` + full re-enable required.
- **Euler angle confusion**: `set_position` takes `roll, pitch, yaw` in that order. The SDK default is degrees. The working pipeline converts from rotation matrices using `R.from_matrix(...).as_euler('ZYX', degrees=True)` which returns `[yaw, pitch, roll]` — note the reversal when passing to `set_position`.

## Euler Convention Detail

The scipy-to-xarm bridge from the working pipeline:

```python
from scipy.spatial.transform import Rotation as R

# From rotation matrix to xarm args:
yaw, pitch, roll = R.from_matrix(pose[:3, :3]).as_euler('ZYX', degrees=True)
goto_pose(arm, *pose[:3, -1], roll, pitch, yaw)
#                               ^^^^^^^^^^^^^ reversed from euler output
```

`as_euler('ZYX')` returns `[Z, Y, X]` = `[yaw, pitch, roll]`. The xarm API expects `roll, pitch, yaw` positionally.

## Reference Functions (from `xarm_setup/goto_capture.py`)

These are the functions that `datagen.py` imports and uses in its working pipeline. They wrap the raw SDK calls above into reusable units.

### `connect_arm(ip: str) -> XArmAPI`

Connects and registers cleanup. This is the single entry point for getting an arm handle.

```python
def connect_arm(ip: str):
    arm = XArmAPI(ip)
    atexit.register(arm.disconnect)
    return arm
```

Source: `goto_capture.py:24-33`

### `enable_arm(arm: XArmAPI) -> bool`

Runs the full enable sequence with error-state recovery. Returns whether the arm is ready.

```python
def enable_arm(arm: XArmAPI):
    arm.clean_error()
    arm.clean_warn()
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    time.sleep(0.5)

    code, state = arm.get_state()
    if state in (4, 5):
        # retry the full sequence
        arm.clean_error()
        arm.clean_warn()
        arm.motion_enable(enable=True)
        arm.set_mode(0)
        arm.set_state(state=0)
        time.sleep(0.5)
        code, state = arm.get_state()

    return state in (1, 2, 3)
```

Source: `goto_capture.py:36-62`

### `goto_pose(arm, x, y, z, roll, pitch, yaw, wait=True) -> bool`

Moves arm to a Cartesian pose. Logs current/target/final positions and distance. Returns success.

```python
def goto_pose(arm, x, y, z, roll, pitch, yaw, wait=True):
    code = arm.set_position(
        x=x, y=y, z=z,
        roll=roll, pitch=pitch, yaw=yaw,
        wait=wait,
        radius=-1.0
    )
    return code == 0
```

Source: `goto_capture.py:154-205`. The actual function also reads current position for logging and inspects error codes on failure — useful diagnostics but not essential to the motion.

### `fallback(xarm)`

Emergency disconnect and crash. Used as a hard stop in generator pipelines:

```python
def fallback(xarm):
    xarm.disconnect()
    assert False, "Crash!"
```

Source: `goto_capture.py:207-209`. Called in `datagen.py:74` when `get_position` fails mid-sequence — a blunt but effective guard against continuing with bad state.

### Calling Order in `datagen.py`

```
connect_arm(ip)          # 1. connect + register cleanup
arm.set_tcp_offset(...)  # 2. configure tool (if needed)
enable_arm(arm)          # 3. enable for motion
goto_pose(arm, ...)      # 4. move (repeatable)
fallback(arm)            # on error: disconnect + crash
```

## When Applying This Skill

1. Compare the user's enable sequence against the one above — look for missing steps or wrong ordering
2. Check that `set_tcp_offset` is called before enabling if a tool is mounted
3. Verify return codes are being checked on `set_position` and `get_position`
4. If the arm won't move, check `get_state()` and run recovery if in state 4/5
5. For orientation bugs, trace the euler convention carefully — the ZYX/roll-pitch-yaw reversal is a common source of error
