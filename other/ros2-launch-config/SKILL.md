---
name: ros2-launch-config
description: >
  ROS2 launch and configuration patterns. Use when writing XML or Python launch files,
  composing multi-node systems, externalizing parameters into YAML, splitting large launch
  files, including subsystem launch files, declaring launch arguments, using
  LaunchConfiguration, FindPackageShare, IfCondition, TimerAction, event handlers, namespaces,
  remapping, parameter files, or composable-node containers for intra-process communication.
---

# ROS2 Launch and Configuration

## When to Use This Skill

- Writing a launch file that brings up a node, a subsystem, or a whole robot
- Splitting a too-big launch file into composable subsystems (`hardware`, `drivers`, `app`)
- Choosing between XML launch and Python launch for a given file
- Externalizing parameters from launch into YAML config files
- Conditionally launching nodes based on `sim`/`real`, `use_composition`, or robot model
- Wiring composable nodes inside a `ComposableNodeContainer` for IPC
- Diagnosing "node A starts before its dependency is ready" race conditions

## XML First, Python When You Need Logic

Henki's rule of thumb (and ROS2's official guidance): prefer XML launch as the front-end. It's declarative, easy to diff, and unambiguous. Drop to Python only when you need real logic — runtime branching on parameter values, dynamic file discovery, or programmatic parameter assembly.

```xml
<!-- launch/robot.launch.xml -->
<launch>
  <arg name="robot_name" default="robot_1"/>
  <arg name="use_sim_time" default="false"/>

  <set_parameter name="use_sim_time" value="$(var use_sim_time)"/>

  <node pkg="my_robot_pkg" exec="perception_node" name="perception"
        namespace="$(var robot_name)" output="screen">
    <param from="$(find-pkg-share my_robot_pkg)/config/perception.yaml"/>
  </node>

  <include file="$(find-pkg-share my_robot_pkg)/launch/sensors.launch.xml">
    <arg name="robot_name" value="$(var robot_name)"/>
  </include>
</launch>
```

If you're tempted to write `<if>` chains spanning dozens of lines, that's the signal to switch to Python.

## Externalize Parameters: Launch Files Should Not Hold Values

A common antipattern is hardcoding parameter values inside launch files. They become invisible to `ros2 param`, hard to override, and require a rebuild to change.

### Park parameters in YAML config

```yaml
# config/perception.yaml
/**:
  ros__parameters:
    use_sim_time: false

perception:
  ros__parameters:
    rate_hz: 30.0
    threshold: 0.7
    frame_id: "camera_link"
    filter:
      type: "kalman"
      process_noise: 0.01

navigation:
  ros__parameters:
    max_velocity: 1.5
    planner:
      type: "astar"
```

The `/**:` namespace applies to every node; named keys (`perception`, `navigation`) apply only to nodes with that name.

### Treat package-shipped YAML as defaults

Users should not edit your package's `config/*.yaml`. Instead they keep their own YAML and pass it via `--params-file` or override individual parameters with `-p`. Document this in your package's `README.md`.

```bash
ros2 launch my_robot_pkg robot.launch.py \
  params_file:=/home/me/robot_overrides.yaml
```

### If parameters change at runtime, register a callback

`add_on_set_parameters_callback` lets a running node accept `ros2 param set` mutations. See `ros2-node-creation` for the full pattern.

## Layered Launch Composition

A robot's bringup naturally decomposes into layers. Make each layer its own launch file and have a top-level launch include them.

```
launch/
├── robot.launch.py            # top-level: includes everything
├── sensors.launch.py          # cameras, lidar, IMU
├── drivers.launch.py          # motor controllers
├── perception.launch.py
└── application.launch.py
```

```python
# launch/robot.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import SetParameter
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('my_robot_pkg')

    args = [
        DeclareLaunchArgument('robot_name', default_value='robot_1'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument(
            'params_file',
            default_value=PathJoinSubstitution([pkg, 'config', 'robot.yaml']),
        ),
    ]

    env = [SetEnvironmentVariable('RCUTILS_COLORIZED_OUTPUT', '1')]

    use_sim_time = SetParameter(
        name='use_sim_time', value=LaunchConfiguration('use_sim_time'))

    def include(rel_launch):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([pkg, 'launch', rel_launch])),
            launch_arguments={
                'robot_name':   LaunchConfiguration('robot_name'),
                'params_file':  LaunchConfiguration('params_file'),
            }.items(),
        )

    return LaunchDescription(
        args + env + [
            use_sim_time,
            include('sensors.launch.py'),
            include('drivers.launch.py'),
            include('perception.launch.py'),
            include('application.launch.py'),
        ]
    )
```

## Conditional Launching

```python
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

# Only when sim:=true
gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource('gazebo.launch.py'),
    condition=IfCondition(LaunchConfiguration('sim')),
)

# Only when sim:=false
hardware = Node(
    package='my_robot_pkg', executable='hardware_driver',
    condition=UnlessCondition(LaunchConfiguration('sim')),
)

# Custom predicate
debug_tools = Node(
    package='my_robot_pkg', executable='debug_publisher',
    condition=IfCondition(PythonExpression([
        '"', LaunchConfiguration('robot_name'), '" == "robot_dev"'])),
)
```

## Composable Nodes (Zero-Copy IPC Container)

When two nodes pass large data (images, point clouds), put them in the same container so messages can move via intra-process communication instead of serializing through DDS.

```python
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

container = ComposableNodeContainer(
    name='perception_container',
    namespace='',
    package='rclcpp_components',
    executable='component_container_mt',   # multi-threaded
    composable_node_descriptions=[
        ComposableNode(
            package='my_robot_pkg',
            plugin='my_robot_pkg::PerceptionComponent',
            name='perception',
            parameters=[LaunchConfiguration('params_file')],
            remappings=[('camera/image_raw', 'realsense/color/image_raw')],
            extra_arguments=[{'use_intra_process_comms': True}],
        ),
        ComposableNode(
            package='my_robot_pkg',
            plugin='my_robot_pkg::TrackerComponent',
            name='tracker',
            extra_arguments=[{'use_intra_process_comms': True}],
        ),
    ],
)
```

The plugin authoring side is in `ros2-messaging` (UniquePtr publish/subscribe).

## Lifecycle Nodes in Launch

```python
from launch_ros.actions import LifecycleNode
from launch_ros.events.lifecycle import ChangeState
from launch_ros.event_handlers import OnStateTransition
from launch.actions import EmitEvent, RegisterEventHandler
from lifecycle_msgs.msg import Transition


driver = LifecycleNode(
    package='my_robot_pkg', executable='lidar_driver',
    name='lidar', namespace='', output='screen')

configure = EmitEvent(event=ChangeState(
    lifecycle_node_matcher=lambda n: n == driver,
    transition_id=Transition.TRANSITION_CONFIGURE))

activate_when_inactive = RegisterEventHandler(OnStateTransition(
    target_lifecycle_node=driver,
    goal_state='inactive',
    entities=[EmitEvent(event=ChangeState(
        lifecycle_node_matcher=lambda n: n == driver,
        transition_id=Transition.TRANSITION_ACTIVATE))],
))

return LaunchDescription([driver, configure, activate_when_inactive])
```

See `ros2-lifecycle` for state semantics.

## Boot Order: Avoid `TimerAction` Where Possible

`TimerAction` (delayed start) is a quick fix for "B starts before A is ready" but it's brittle. Prefer:

1. **Lifecycle event handlers** — only `activate` B once A reports `active`.
2. **Service waits inside the consumer** — B's first action is `client.wait_for_service()`.
3. **Health checks at the application boundary** — see `robot-bringup` for systemd-level ordering.

Use `TimerAction` only as a stopgap, and add a comment naming what should replace it.

## Common Pitfalls

| Pitfall                                                  | What goes wrong                                                          | Fix                                                                                       |
|----------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Hardcoding params in launch files                        | Can't tune without code change; not visible to `ros2 param`              | Move to YAML; pass via `params_file` or `--params-file`                                   |
| Forgetting `use_sim_time` propagation                    | Half the system listens to wall clock, half to `/clock` → broken TF       | `SetParameter('use_sim_time', ...)` once at top of `LaunchDescription`                    |
| Editing upstream launch files in-place                   | Lost on next `apt upgrade` / re-clone                                    | Copy launch + config into your workspace and modify there                                 |
| Composable nodes without `use_intra_process_comms: true` | Messages still serialize, defeats the purpose                            | Set `extra_arguments=[{'use_intra_process_comms': True}]` on every node in the container  |
| Using `Node` (non-lifecycle) under `LifecycleNode`-only event handlers | Events never fire, node sits idle                              | Either use `LifecycleNode` or skip the lifecycle event wiring                              |
| `TimerAction(period=N)` to "fix" a race                  | Race re-emerges on slower hardware or under load                         | Use lifecycle event handler, or `wait_for_service` in the consumer                        |
| Forgetting to install `launch/` and `config/`            | `ros2 launch my_pkg robot.launch.py` fails: file not found in install    | `install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})` in CMakeLists.txt    |

## Related Skills

- **ros2-node-creation** — package scaffolding (CMakeLists install rules)
- **ros2-messaging** — composable nodes and IPC for big data
- **ros2-lifecycle** — managed-node startup orchestration
- **robot-bringup** — systemd-level boot ordering, watchdog, log rotation (one level above launch)
