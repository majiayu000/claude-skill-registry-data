---
name: ros2-architect
version: 1.0.0
description: ROS2 standards across Jazzy/Kilted/Lyrical — colcon + ament_cmake/ament_python layout, lifecycle nodes, explicit QoS, services/actions, parameters, Python launch DSL. Cross-platform dev env via Pixi + RoboStack. C++ (rclcpp) and Python (rclpy) equal first-class. Use when scaffolding or reviewing a ROS2 workspace.
---

# ROS2 Architecture

Covers the three current ROS2 distributions; patterns are consistent across all three with version-specific notes called out where they diverge. C++ (`rclcpp`) and Python (`rclpy`) treated as equal first-class targets. **Development environment via Pixi + RoboStack** — the modern, cross-platform alternative to `sudo apt install ros-*`. See [STACK.md](STACK.md) for distro details and pinned tool versions.

Python-side `rclpy` nodes inherit the typing, dataclass, asyncio, and testing rules from [python-architect](../../languages/python-architect/SKILL.md) — this skill adds the ROS2-specific layer on top.

## 0. Distribution selection

| Distro | Type | Released | EOL | When to pick |
|---|---|---|---|---|
| **Jazzy Jalisco** | LTS | May 2024 | May 2029 | **Default for new production systems.** Mature, broad community, 3+ years of support left. |
| **Kilted Kaiju** | non-LTS | May 2025 | Dec 2026 | When you specifically need a feature added in Kilted and can plan a migration before Dec 2026. |
| **Lyrical Luth** | LTS | May 2026 | May 2031 | **Default for new systems once the ecosystem catches up** (typically 1–3 months post-release as third-party packages migrate). Long support window. |

- **Migrate from Kilted before Dec 2026** — direct target is Lyrical (next LTS) for a 5-year runway.
- **Jazzy → Lyrical migration** is straightforward; most code ports with minimal changes.
- **`ros2-architect`'s patterns apply to all three** — the differences are in specific package APIs and tooling. Where this matters, the section calls it out.

## 1. Workspace layout

A ROS2 workspace is the root of one or more packages built together by `colcon`. Pixi sits at the workspace root and gives every contributor the same ROS distro, the same compiler, the same Python — on Linux, macOS, or Windows. Full tree in [RECIPES § Workspace layout](RECIPES.md#workspace-layout).

- **`src/` holds packages**, never code at the workspace root.
- **One package, one responsibility** — drivers, navigation, perception, custom messages, bringup. Don't put everything in one `my_robot` package.
- **`_msgs` packages hold ONLY interfaces** (msg/srv/action). Rebuilt rarely, consumed by everyone.
- **`_bringup` package** holds launch files and config for assembling the full robot stack. No source code.

## 2. Pixi for the development environment

Pixi solves the historical ROS2 pain: needing a specific Ubuntu version, conflicting Python installs, broken updates from `apt`. RoboStack channel on conda-forge distributes ROS distros as conda packages, so Pixi can install ROS2 anywhere conda runs — Linux, macOS, Windows. Skeleton: [RECIPES.md § `pixi.toml` — workspace manifest](RECIPES.md#pixitoml--workspace-manifest).

- **`pixi.lock` is committed.** Reproducibility is the whole point.
- **`platforms = [...]`** declares every OS/arch your team uses. CI uses the same lockfile.
- **No `sudo apt install` on contributor machines.** Pixi's `.pixi/` directory is isolated; the system stays clean.
- **CI uses Pixi too.** `pixi run build` in GitHub Actions = the same env every developer uses.
- **`colcon build --symlink-install`** in dev — Python changes hot-reload without rebuilding. Drop the flag for release builds.

## 3. Package structure — `ament_cmake` vs `ament_python`

The build type is declared in `package.xml`. Use `ament_cmake` for C++ (and for interface-only `_msgs` packages); `ament_python` for pure-Python packages. Skeletons: [RECIPES.md § `package.xml` — `ament_cmake`](RECIPES.md#packagexml--ament_cmake-c-and-_msgs) and [§ `ament_python`](RECIPES.md#packagexml--ament_python).

- **`format="3"`** for `package.xml`. Older formats still work but lack features.
- **Every dep declared.** Implicit dependencies (`std_msgs` showing up because something else pulled it) is a latent bug.
- **`depend`** vs `build_depend` / `exec_depend`: prefer the unified `<depend>` tag when the dependency is needed at both build and runtime. Split only when they differ.
- **Tests declared as `test_depend`.** Linters (`ament_lint_*`) are part of every package's test suite.

## 4. Nodes — lifecycle, executors, single-responsibility

A **node** is the unit of computation. One process can host one or many nodes (`rclcpp::executors::MultiThreadedExecutor` / `rclpy.executors`).

- **One node, one job.** A node that publishes IMU data, listens for joystick input, *and* runs path planning has three responsibilities. Three nodes.
- **Lifecycle nodes** for anything with non-trivial init: `unconfigured → inactive → active → finalized`. Allows the launch system to bring up nodes in the right order, retry init, and gracefully shut down. Use for any node that holds an open connection (camera, motor controller, network socket).
- **Standard `Node`** for stateless or trivially-init nodes.
- **Single-threaded executor by default**; switch to multi-threaded only when callbacks genuinely contend (e.g. a long-running service callback shouldn't block fast topic callbacks). Multi-threaded executors require thread-safe callback groups — easy to get wrong.
- **Node names: lowercase snake_case**, namespaced by component (`/imu_driver`, `/path_planner`).
- **No business logic in `main.cpp` / `main.py`.** Construct the node, spin, shut down. Logic lives in node classes.

## 5. Topics & QoS — explicit profiles

Every publisher / subscriber declares an explicit QoS profile. Default behavior **bites**. Profile reference + C++/Python snippets in [RECIPES § QoS](RECIPES.md#qos--explicit-profiles).

- **Topic names use plural / hierarchical paths**: `/sensors/imu/data`, `/control/cmd_vel`. Namespace by subsystem.
- **Publisher and subscriber QoS must match.** Mismatched QoS means subscribers silently fail to connect (visible only in `ros2 topic info -v`).
- **Sensor streams = best-effort + KEEP_LAST(N).** High-rate, drop the old.
- **Low-rate state = reliable + KEEP_LAST(10).** `/robot/battery`, `/system/status`.
- **Reliable + KEEP_ALL on a high-rate topic is a memory leak.**

## 6. Services and actions

| | Service | Action |
|---|---|---|
| Purpose | Synchronous request/response | Long-running task with feedback + cancellation |
| Pattern | `Add(a, b) → c` | `MoveToGoal(pose) → feedback(progress) → result(success)` |
| Use when | Operation completes in < 100 ms | Operation takes seconds-to-minutes |
| Pitfall | Blocking callbacks freeze the executor | Action server complexity (goal/feedback/result/cancel) |

- **Services for short queries**: parameter get/set, mode change, calibration trigger.
- **Actions for everything navigation-like, manipulation-like, planning-like.**
- **Never call a service synchronously from inside a topic callback.** That's an executor deadlock. Use `async_send_request` (C++) / `call_async` (rclpy) and handle the future.

## 7. Parameters — declared, typed, validated

- **Declare every parameter on node init** with `declare_parameter(name, default, descriptor)`. Undeclared parameters fail to read.
- **Provide a `ParameterDescriptor`** with type and description. Visible in `ros2 param describe`.
- **Validate on change** via `add_on_set_parameters_callback` — reject bad values; never silently accept and crash later.
- **YAML config files** in the `_bringup` package, loaded by launch via `Node(parameters=[config_path])`. Per-robot, per-environment configs live there.
- **Use ranges and choices in the descriptor:** `IntegerRange`, `FloatingPointRange`, `additional_constraints` — the parameter system enforces them.

## 8. Launch files — Python DSL

Launch files describe how to bring up a system: which nodes to run, with which parameters, in which order, on which conditions. Skeleton: [RECIPES.md § Launch file — Python DSL](RECIPES.md#launch-file--python-dsl).

- **Always Python launch (`*.launch.py`)** — XML launch is legacy.
- **Launch arguments for environment differences** (`use_sim`, `robot_model`). One launch file, many configurations.
- **Compose smaller launch files** with `IncludeLaunchDescription` — reuse the camera launch in both sim and real robot.
- **No business logic in launch files.** Launch files orchestrate; nodes compute.

## 9. Testing

- **Unit tests inside the package.** C++: GTest. Python: pytest.
- **`ament_lint_*`** in every package's test suite — `ament_cppcheck`, `ament_cpplint` (C++), `ament_flake8`, `ament_pep257` (Python). Failures fail CI.
- **Integration tests via `launch_testing`** — spin up a launch graph, assert nodes reach expected states, topics carry expected messages.
- **`ros2 doctor`** in CI before tests — catches missing deps, network issues, ROS_DOMAIN_ID conflicts.
- **Run tests in Pixi:** `pixi run test` → `colcon test && colcon test-result --verbose --all`.

## 10. Logging, debugging, deployment

- **`RCLCPP_INFO` / `self.get_logger().info()`** — ROS2 logger, integrates with the launch logger and external aggregators. Not `printf` / `print`.
- **Severity levels** (DEBUG / INFO / WARN / ERROR / FATAL) match the rest of our skills (e.g. [observability-architect §3](../../infra/observability-architect/SKILL.md#3-logging-structured-leveled-correlated)).
- **`ros2 topic echo`, `ros2 node info`, `ros2 service list`** are the field-debugger toolkit — make sure your nodes / topics / services are discoverable (correct namespace, QoS, lifecycle state).
- **`ros2 bag record / play`** for capturing real-robot data; integration tests replay against the same bag.
- **Containerized deploys:** Docker image built FROM a Pixi-installed base, or from `osrf/ros:kilted-desktop` if you need the upstream container. Multi-arch (amd64 + arm64) per [docker-architect §5](../../infra/docker-architect/SKILL.md#5-multi-arch-builds) for robot vs dev machine.

## 11. Cross-skill ties

- [docker-architect](../../infra/docker-architect/SKILL.md) — multi-arch builds for robot hardware (often arm64); the Pixi-in-Docker pattern for deployment.
- [observability-architect §3](../../infra/observability-architect/SKILL.md#3-logging-structured-leveled-correlated) — structured logging conventions; ROS2 logger forwards to aggregators.
- [grafana-architect](../../infra/grafana-architect/SKILL.md) — robot telemetry dashboards (CPU per node, topic latency, lifecycle states).
- [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md) — Pixi here partially overlaps with `mise`/`proto` (env management) and Task (task running). For ROS2 workspaces, Pixi covers both jobs; for polyglot repos with ROS2 + other services, mise + Pixi can coexist (Pixi owns the ROS2 environment).
- [python-architect](../../languages/python-architect/SKILL.md) / [go-architect](../../languages/go-architect/SKILL.md) — node implementations follow language conventions where they don't conflict with ROS2 patterns (callback structure, lifecycle).
