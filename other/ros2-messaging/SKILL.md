---
name: ros2-messaging
description: >
  ROS2 publisher, subscriber, QoS, custom message, synchronization, and zero-copy
  communication patterns. Use when designing topic graphs, choosing QoSProfile policies,
  debugging topics that connect but deliver no data, defining msg interfaces or interface
  packages, using rosidl_generate_interfaces, message_filters, ApproximateTime, ExactTime,
  intra-process comms, rclcpp components, namespaces, remappings, or topic naming.
---

# ROS2 Messaging

## When to Use This Skill

- Designing the topic graph for a robot or feature (what publishes what, with which QoS)
- Choosing the right `QoSProfile` for sensors, commands, state, transforms, or maps
- Debugging "publisher and subscriber both exist but nothing arrives" (almost always QoS)
- Designing a custom `.msg` and standing up a `_msgs` interfaces package
- Synchronizing two or more topics by timestamp (`message_filters`)
- Cutting copy/serialization overhead with intra-process communication and `UniquePtr`
- Naming topics consistently across a fleet

## QoS: The #1 Source of "Topic Doesn't Connect" Bugs

A publisher and subscriber must have **compatible** QoS. Most "silent failure" bugs are QoS mismatches.

```
Publisher        Subscriber       Connect?
RELIABLE         RELIABLE         Yes
RELIABLE         BEST_EFFORT      Yes
BEST_EFFORT      BEST_EFFORT      Yes
BEST_EFFORT      RELIABLE         NO — silent failure (most common bug)
```

Durability matters too: a `VOLATILE` publisher will not deliver to a `TRANSIENT_LOCAL` subscriber that joined late.

### Diagnose a QoS mismatch in 10 seconds

```bash
ros2 topic info /camera/image_raw -v
# Look at "Reliability" and "Durability" for both publishers and subscribers.
# If they don't match per the table above → that's your bug.
```

### Recommended QoS Profiles

```python
from rclpy.qos import (
    QoSProfile, QoSReliabilityPolicy as Rel, QoSHistoryPolicy as Hist,
    QoSDurabilityPolicy as Dur,
)

# Sensors (cameras, LiDAR, IMU): tolerate drops, want latest
SENSOR_QOS = QoSProfile(
    reliability=Rel.BEST_EFFORT,
    history=Hist.KEEP_LAST, depth=1,
    durability=Dur.VOLATILE,
)

# Commands (cmd_vel, joint goals): never miss
COMMAND_QOS = QoSProfile(
    reliability=Rel.RELIABLE,
    history=Hist.KEEP_LAST, depth=10,
    durability=Dur.VOLATILE,
)

# Maps, robot_description, static config: late joiners must receive
LATCHED_QOS = QoSProfile(
    reliability=Rel.RELIABLE,
    history=Hist.KEEP_LAST, depth=1,
    durability=Dur.TRANSIENT_LOCAL,   # the ROS2 replacement for ROS1 latching
)

# Default state/diagnostics
STATE_QOS = QoSProfile(
    reliability=Rel.RELIABLE,
    history=Hist.KEEP_LAST, depth=10,
)
```

```cpp
#include <rclcpp/qos.hpp>

static const rclcpp::QoS SENSOR_QOS  = rclcpp::SensorDataQoS();
static const rclcpp::QoS COMMAND_QOS = rclcpp::QoS(10).reliable();
static const rclcpp::QoS LATCHED_QOS = rclcpp::QoS(1).reliable().transient_local();
```

### Selection Guide

| Data type            | Reliability | Durability       | Depth   | Examples                    |
|----------------------|-------------|------------------|---------|-----------------------------|
| Sensor (high freq)   | BEST_EFFORT | VOLATILE         | 1–5     | LiDAR, camera, IMU          |
| Command              | RELIABLE    | VOLATILE         | 10      | cmd_vel, joint commands     |
| State / config       | RELIABLE    | TRANSIENT_LOCAL  | 1       | robot_description, map      |
| Transforms           | RELIABLE    | VOLATILE         | 100     | /tf                         |

## Publisher / Subscriber Patterns

### Python

```python
class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_publisher')
        self._pub = self.create_publisher(RobotState, 'robot/state', STATE_QOS)
        self.create_timer(0.1, self._tick)

    def _tick(self):
        msg = RobotState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.battery_level = self._read_battery()
        self._pub.publish(msg)
```

```python
class StateSubscriber(Node):
    def __init__(self, on_state):
        super().__init__('state_subscriber')
        self._on_state = on_state
        self.create_subscription(RobotState, 'robot/state',
                                 self._cb, STATE_QOS)
    def _cb(self, msg):
        self._on_state(msg)
```

### C++

```cpp
class StateSubscriber : public rclcpp::Node {
public:
  StateSubscriber() : Node("state_subscriber") {
    sub_ = create_subscription<robot_interfaces::msg::RobotState>(
        "robot/state", STATE_QOS,
        [this] (robot_interfaces::msg::RobotState::ConstSharedPtr msg) {
          on_state(*msg);
        });
  }
private:
  void on_state(const robot_interfaces::msg::RobotState& s) {
    // delegate to application logic; see ros2-clean-architecture
  }
  rclcpp::Subscription<robot_interfaces::msg::RobotState>::SharedPtr sub_;
};
```

## Message Synchronization (`message_filters`)

When two topics describe the same instant (image + camera_info, left + right stereo), align them by timestamp.

```python
import message_filters
from sensor_msgs.msg import Image, CameraInfo

def on_pair(image, info):
    process(image, info)

img_sub = message_filters.Subscriber(node, Image, 'image_raw')
info_sub = message_filters.Subscriber(node, CameraInfo, 'camera_info')

# ApproximateTime tolerates small clock skew between sources
sync = message_filters.ApproximateTimeSynchronizer(
    [img_sub, info_sub], queue_size=10, slop=0.05)
sync.registerCallback(on_pair)
```

```cpp
#include <message_filters/subscriber.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <message_filters/synchronizer.h>

using Image = sensor_msgs::msg::Image;
using Info  = sensor_msgs::msg::CameraInfo;

message_filters::Subscriber<Image> image_sub(node, "image_raw");
message_filters::Subscriber<Info>  info_sub(node, "camera_info");

using Policy = message_filters::sync_policies::ApproximateTime<Image, Info>;
auto sync = std::make_shared<message_filters::Synchronizer<Policy>>(
    Policy(10), image_sub, info_sub);
sync->registerCallback(
    [] (Image::ConstSharedPtr img, Info::ConstSharedPtr info) { ... });
```

## Custom Messages: When and How

### Reuse before you invent

Check `common_interfaces` first. The vast majority of topics map to existing types:

- `geometry_msgs/PoseStamped`, `Twist`, `Transform`
- `sensor_msgs/Image`, `LaserScan`, `Imu`, `PointCloud2`, `JointState`
- `nav_msgs/Odometry`, `Path`, `OccupancyGrid`
- `std_msgs/Header` (and only `Header` — see anti-pattern below)

### Don't publish primitives

`std_msgs/Float32`, `Bool`, `String`, and `example_interfaces/*` are explicitly meant for prototyping and demos. In production, define a custom message that names the quantity:

```
# msgs/BatteryLevel.msg                    # GOOD — semantic meaning
std_msgs/Header header
float32 percentage      # 0.0 .. 100.0
float32 voltage         # volts
uint8 status
uint8 STATUS_OK = 0
uint8 STATUS_LOW = 1
uint8 STATUS_CRITICAL = 2
```

```
# Don't publish std_msgs/Float32 on /battery — the consumer can't tell what unit it is.
```

### Enums via constants

ROS2 `.msg` files don't have native enums. Simulate with constants and a numeric field (see the `STATUS_*` lines above). This pattern is used throughout `common_interfaces` (e.g., `diagnostic_msgs/DiagnosticStatus.level`).

### Custom `_msgs` package

Custom messages **must** live in their own package, suffixed `_msgs`. This decouples consumers from your implementation package.

```
robot_interfaces/
├── CMakeLists.txt
├── package.xml
├── msg/
│   ├── BatteryLevel.msg
│   └── RobotState.msg
├── srv/
│   └── SetMode.srv      # see ros2-service-action
└── action/
    └── NavigateToGoal.action
```

```cmake
cmake_minimum_required(VERSION 3.8)
project(robot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(action_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BatteryLevel.msg"
  "msg/RobotState.msg"
  "srv/SetMode.srv"
  "action/NavigateToGoal.action"
  DEPENDENCIES std_msgs geometry_msgs action_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
```

```xml
<package format="3">
  <name>robot_interfaces</name>
  <version>0.1.0</version>
  <description>Robot interface definitions</description>
  <maintainer email="dev@example.com">Dev</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>action_msgs</depend>

  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <export><build_type>ament_cmake</build_type></export>
</package>
```

After building, **source the install overlay** before running consumer nodes — Python imports of generated message types fail if the overlay isn't sourced.

## Topic Naming

Conventions that scale across a fleet:

| Rule                            | Example                            |
|---------------------------------|------------------------------------|
| Lowercase                       | `/robot/cmd_vel`                   |
| Underscores for multi-word      | `/joint_states`                    |
| Avoid abbreviations             | `/camera/image` not `/cam/img`     |
| Use namespaces                  | `/robot1/cmd_vel`                  |
| Descriptive over short          | `/laser_scan` not `/ls`            |

Group by domain: `/<robot>/<category>/<specific>`

```
/robot/sensors/lidar/scan
/robot/sensors/camera/image_raw
/robot/control/cmd_vel
/robot/state/odometry
/robot/state/battery
/robot/perception/detections
```

## Intra-Process Communication and Zero-Copy

For high-bandwidth data (images, point clouds) flowing between two nodes in the same process, intra-process comms (IPC) avoids serialization. With `UniquePtr` publish and a single subscriber, the message can be moved without copying.

```cpp
#include <rclcpp_components/register_node_macro.hpp>

class PerceptionComponent : public rclcpp::Node {
public:
  explicit PerceptionComponent(const rclcpp::NodeOptions& opts)
      : Node("perception", opts) {  // opts come from container, may enable IPC
    rclcpp::SubscriptionOptions sub_opts;
    sub_opts.use_intra_process_comm = rclcpp::IntraProcessSetting::Enable;

    sub_ = create_subscription<sensor_msgs::msg::Image>(
        "image_raw", rclcpp::SensorDataQoS(),
        [this] (sensor_msgs::msg::Image::UniquePtr msg) {
          // UniquePtr → moved, not copied, when:
          //   • publisher also publishes UniquePtr
          //   • IPC is enabled in both
          //   • this is the only subscriber
          process(std::move(msg));
        },
        sub_opts);
  }
private:
  void process(sensor_msgs::msg::Image::UniquePtr msg);
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_;
};

RCLCPP_COMPONENTS_REGISTER_NODE(PerceptionComponent)
```

Run it inside a `ComposableNodeContainer` to share a process with its publisher (see `ros2-launch-config`).

## Common Pitfalls

| Pitfall                                                     | What goes wrong                                                       | Fix                                                                       |
|-------------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------|
| BEST_EFFORT publisher, RELIABLE subscriber                  | No data delivered, no error                                            | Match QoS; use `SensorDataQoS()` on both ends for sensors                  |
| VOLATILE publisher of `robot_description`                   | Late-joining consumers (RViz, MoveIt) see nothing                     | Use `TRANSIENT_LOCAL` durability                                           |
| Publishing `std_msgs/Float32` on `/battery`                 | Consumers can't infer units; brittle to refactor                      | Define `BatteryLevel.msg` with `percentage`, `voltage`, status            |
| Custom messages in the same package as your nodes           | Consumers must depend on your whole package to use the message        | Put messages in a separate `_msgs` package                                |
| Forgetting to source `install/setup.bash` after rebuilding msgs | Python `from my_msgs.msg import X` fails                          | Re-source the overlay; consider `colcon build --symlink-install` for Python|
| Subscribing twice with different QoS                        | Duplicate processing or accidental drop                                | Pick one QoS per topic-direction; document it                              |
| `ApproximateTimeSynchronizer` with too-tight `slop`         | Pairs never match                                                     | Start at 0.05–0.1s and tighten                                             |

## Related Skills

- **ros2-node-creation** — node skeletons that publish/subscribe
- **ros2-service-action** — request/response and long-running tasks
- **ros2-launch-config** — composing nodes for IPC, parameter files
- **ros2-transforms** — `/tf` and `/tf_static` are messaging on geometry_msgs
- **ros2-bag** — recording the topic graph for replay
