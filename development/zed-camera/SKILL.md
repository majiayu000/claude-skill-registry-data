---
name: zed-camera
description: Reference for ZED stereo camera setup and capture using the pyzed/sl SDK. Use when debugging ZED camera issues, starting a new project with ZED, or verifying that camera initialization and image retrieval follow a known-working pattern.
argument-hint: [optional: describe the issue or what you're setting up]
---

# ZED Camera — Known-Working Reference

Ground truth patterns extracted from a working data-collection pipeline (`xarm_setup/goto_capture.py`). When debugging camera issues in a new project, compare against these minimal sequences to identify what extra overhead may be causing problems.

## Initialization

The minimum viable init sequence:

```python
import pyzed.sl as sl

zed = sl.Camera()

init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.camera_fps = 30
init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
init_params.coordinate_units = sl.UNIT.METER

err = zed.open(init_params)
assert err == sl.ERROR_CODE.SUCCESS, f"Failed to open ZED: {err}"
```

### Cleanup

The camera **must** be closed or the USB device stays locked:

```python
import atexit
atexit.register(zed.close)
```

Or explicitly: `zed.close()`. The `atexit` pattern guarantees cleanup even on unhandled exceptions (as long as the interpreter shuts down normally).

## Capture — Single Frame

Each grab/retrieve cycle produces one synchronized stereo pair + depth:

```python
import numpy as np

runtime_params = sl.RuntimeParameters()

image_left = sl.Mat()
image_right = sl.Mat()
depth_map = sl.Mat()

err = zed.grab(runtime_params)
assert err == sl.ERROR_CODE.SUCCESS, f"Grab failed: {err}"

zed.retrieve_image(image_left, sl.VIEW.LEFT)
zed.retrieve_image(image_right, sl.VIEW.RIGHT)
zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH)

# IMPORTANT: copy the data out of the sl.Mat — the SDK reuses the buffer
left_np = np.array(image_left.get_data(), copy=True)
right_np = np.array(image_right.get_data(), copy=True)
depth_np = np.array(depth_map.get_data(), copy=True)
```

### Critical Detail: `copy=True`

The `sl.Mat` objects are SDK-owned buffers that get overwritten on the next `grab()`. Always `copy=True` when converting to numpy if you intend to keep the data.

## Intrinsics

```python
info = zed.get_camera_information()
left_calib = info.camera_configuration.calibration_parameters.left_cam
right_calib = info.camera_configuration.calibration_parameters.right_cam

# Build 3x3 intrinsic matrices
left_K = np.diag([left_calib.fx, left_calib.fy, 1.0])
left_K[:2, -1] = [left_calib.cx, left_calib.cy]

right_K = np.diag([right_calib.fx, right_calib.fy, 1.0])
right_K[:2, -1] = [right_calib.cx, right_calib.cy]
```

Intrinsics are stable after `open()` — call once and reuse.

## Ordering Invariants

1. `sl.Camera()` → `zed.open(init_params)` — must open before anything else
2. `zed.grab(runtime_params)` — must succeed before any `retrieve_*` call
3. `retrieve_image` / `retrieve_measure` — only valid after a successful `grab()`
4. `get_camera_information()` — valid any time after `open()`
5. `zed.close()` — must be called to release USB device

## Common Failure Modes

- **Camera not detected**: Another process holds the USB device. Check `zed.close()` was called in prior runs. `lsusb` to verify hardware presence.
- **Grab returns non-SUCCESS**: Camera may have disconnected or USB bandwidth saturated (especially with multiple cameras or high resolution).
- **Stale/corrupted images**: Forgot `copy=True` on `get_data()` — the SDK buffer was overwritten by the next grab.
- **Depth is all NaN**: Object too close or too far. Check `coordinate_units` matches your scene scale.

## File-Descriptor Pattern: SafeZed + grabbed_frame

The ZED SDK has an implicit precondition: `zed.grab()` must precede any `retrieve_*` call. This is the same shape as UNIX `open()`/`read()`. We enforce it with a context manager that yields a proxy object — like how `open()` returns an fd that `read()`/`write()` require.

`SafeZed` (`datastructs.py`) is a transparent `__getattr__` proxy over `sl.Camera`. `grabbed_frame` (`goto_capture.py`) is the only factory — it calls `grab()`, yields a `SafeZed`, and invalidates it on exit.

```python
with grabbed_frame(zed) as frame:
    left, right = retrieve_stereo_images(frame)  # image-only
    depth = retrieve_depth(frame)                 # depth-only
    frame.retrieve_image(mat, sl.VIEW.LEFT)       # raw SDK calls work too
```

Key properties:
1. **Created by grab** — no `SafeZed` exists until `grab()` succeeds
2. **Is the retrieve interface** — callers use `frame`, not raw `zed`
3. **Exit invalidates** — post-`with` access raises `RuntimeError`
4. **Raises on failure** — makes caller-side retry/backoff a simple loop around the `with`

Image and depth retrieval are separate primitives (`retrieve_stereo_images`, `retrieve_depth`) that assert they receive a `SafeZed`. Callers compose whichever subset they need. `capture_zed_images` is the convenience function that grabs everything.

## Reference Functions (from `xarm_setup/goto_capture.py`)

These are the functions that `datagen.py` imports and uses in its working pipeline.

### `init_zed_camera() -> sl.Camera`

Single entry point for getting a camera handle. Configures resolution, FPS, depth mode, and registers cleanup.

```python
def init_zed_camera():
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.camera_fps = 30
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        return None

    atexit.register(zed.close)
    return zed
```

Source: `goto_capture.py:77-99`

### `capture_zed_images(zed) -> Zedpack | None`

Grabs one synchronized frame and returns all data as numpy arrays (with `copy=True`). Returns `None` on grab failure.

```python
def capture_zed_images(zed) -> Zedpack | None:
    runtime_params = sl.RuntimeParameters()

    image_left = sl.Mat()
    image_right = sl.Mat()
    depth_map = sl.Mat()

    if zed.grab(runtime_params) != sl.ERROR_CODE.SUCCESS:
        return None

    zed.retrieve_image(image_left, sl.VIEW.LEFT)
    zed.retrieve_image(image_right, sl.VIEW.RIGHT)
    zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH)
    left_K, right_K = get_intrinsics(zed)

    return Zedpack(
        left_image=np.array(image_left.get_data(), copy=True),
        left_depth=np.array(depth_map.get_data(), copy=True),
        right_image=np.array(image_right.get_data(), copy=True),
        left_K=left_K,
        right_K=right_K,
    )
```

Source: `goto_capture.py:117-138`

### `Zedpack` — the return type

```python
@dataclass
class Zedpack:
    left_image: np.ndarray
    left_depth: np.ndarray
    right_image: np.ndarray
    left_K: np.ndarray    # 3x3 intrinsic matrix
    right_K: np.ndarray   # 3x3 intrinsic matrix
```

Source: `xarm_setup/datastructs.py:7-12`

### Calling Order in `datagen.py`

```
camera = init_zed_camera()       # 1. open + register cleanup
zed_pack = capture_zed_images(camera)  # 2. grab frame (repeatable)
zed_pack.left_image              # 3. access numpy arrays
```

## When Applying This Skill

1. Compare the user's init sequence against the one above — look for missing params or wrong ordering
2. Check that `grab()` return codes are being checked before `retrieve_*`
3. Verify `copy=True` on numpy conversion
4. Confirm cleanup path exists (`atexit.register` or explicit `close()`)
5. If images look wrong, check resolution/fps settings and whether depth_mode is appropriate
