---
name: ros2-node-creation
description: >
  ROS2 node design and package scaffolding patterns. Use when creating rclpy or rclcpp nodes,
  refactoring oversized nodes, separating ROS communication from business logic, designing
  BaseNode conventions, declaring parameters and descriptors, using parameter callbacks,
  choosing executors, callback groups, timers, publishers, subscribers, QoS, lifecycle
  initialization, workspace layout, or ament Python and CMake package files.
---

# ROS2 Node Creation

## When to Use This Skill

- Creating a brand-new ROS2 node in Python (rclpy) or C++ (rclcpp)
- Refactoring a node whose `__init__`/constructor has become a wall of code
- Designing a workspace-wide `BaseNode` to standardize parameter and QoS conventions
- Choosing between SingleThreadedExecutor, MultiThreadedExecutor, and callback groups
- Wiring parameter declarations, descriptors, ranges, and runtime parameter callbacks
- Deciding whether the node should be C++ or Python (performance budget vs. iteration speed)
- Scaffolding `package.xml`, `CMakeLists.txt`, or `setup.py` for a new ament package
- Setting up dependency injection so business logic is unit-testable without spinning ROS

## The Core Rule: Nodes Are Adapters, Not Application Code

A ROS2 node should be a thin adapter between the middleware and your application logic. Pure logic — kinematics, state machines, planners, filters — lives in plain classes you can import without `rclpy`/`rclcpp`. The node wires those classes to topics, services, parameters, and timers.

This is the single most leveraged decision in a ROS2 codebase: it makes nodes testable, swappable between simulation and hardware, and resistant to ROS2 API churn.

```python
# GOOD — node is an adapter
class PerceptionLogic:
    """Pure Python. No rclpy import. Unit-testable."""
    def __init__(self, threshold: float):
        self.threshold = threshold
    def detect(self, image_array) -> list:
        ...

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception')
        threshold = self.declare_parameter('threshold', 0.7).value
        self._logic = PerceptionLogic(threshold)             # injected
        self.create_subscription(Image, 'image', self._cb, sensor_qos)
    def _cb(self, msg):
        detections = self._logic.detect(msg_to_array(msg))   # delegate
        self._pub.publish(detections_to_msg(detections))
```

```python
# BAD — logic baked into the node, untestable without ROS
class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception')
        self.threshold = 0.7
        self.create_subscription(Image, 'image', self.detect, sensor_qos)
    def detect(self, msg):
        # 200 lines of CV math directly in the callback
        ...
```

## Python Node Template

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import (
    ParameterDescriptor, FloatingPointRange, SetParametersResult
)
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray


class PerceptionNode(Node):
    """ROS2 adapter. Constructs logic, wires comms, delegates work."""

    def __init__(self):
        super().__init__('perception_node')

        # 1. Declare parameters with descriptors and ranges (visible in `ros2 param`)
        self.declare_parameter(
            'rate_hz', 30.0,
            ParameterDescriptor(
                description='Processing rate in Hz',
                floating_point_range=[FloatingPointRange(
                    from_value=1.0, to_value=120.0, step=0.0)],
            ),
        )
        self.declare_parameter('threshold', 0.7)
        self.declare_parameter('frame_id', 'camera_link')

        # 2. Read once into typed locals
        rate_hz = self.get_parameter('rate_hz').value
        self._threshold = self.get_parameter('threshold').value
        self._frame_id = self.get_parameter('frame_id').value

        # 3. Construct application logic with the parameters
        from my_pkg.perception_logic import PerceptionLogic
        self._logic = PerceptionLogic(self._threshold)

        # 4. QoS profiles tuned for the data shape (see ros2-messaging)
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        # 5. Publishers first, then subscribers (subs may fire immediately on spin)
        self._det_pub = self.create_publisher(
            Detection2DArray, 'detections', reliable_qos)
        self._image_sub = self.create_subscription(
            Image, 'camera/image_raw', self._image_cb, sensor_qos)

        # 6. Timers for periodic work
        self._timer = self.create_timer(1.0 / rate_hz, self._timer_cb)

        # 7. Runtime-mutable parameters
        self.add_on_set_parameters_callback(self._on_param_change)

        self.get_logger().info(
            f'Perception started: rate={rate_hz}Hz threshold={self._threshold}')

    def _on_param_change(self, params):
        """Validate and apply parameter updates from `ros2 param set`."""
        for p in params:
            if p.name == 'threshold':
                if not (0.0 <= p.value <= 1.0):
                    return SetParametersResult(
                        successful=False, reason='threshold must be in [0,1]')
                self._threshold = p.value
                self._logic.threshold = p.value
        return SetParametersResult(successful=True)

    def _image_cb(self, msg: Image):
        detections = self._logic.detect(msg)
        self._det_pub.publish(detections)

    def _timer_cb(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## C++ Node Template

```cpp
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <vision_msgs/msg/detection2_d_array.hpp>
#include <memory>

#include "my_pkg/perception_logic.hpp"   // pure C++, no rclcpp

class PerceptionNode : public rclcpp::Node {
public:
  PerceptionNode() : Node("perception_node") {
    declare_parameter<double>("rate_hz", 30.0);
    declare_parameter<double>("threshold", 0.7);
    declare_parameter<std::string>("frame_id", "camera_link");

    const double rate_hz = get_parameter("rate_hz").as_double();
    const double threshold = get_parameter("threshold").as_double();

    logic_ = std::make_unique<my_pkg::PerceptionLogic>(threshold);

    auto sensor_qos = rclcpp::SensorDataQoS();
    auto reliable_qos = rclcpp::QoS(10).reliable();

    det_pub_ = create_publisher<vision_msgs::msg::Detection2DArray>(
        "detections", reliable_qos);

    image_sub_ = create_subscription<sensor_msgs::msg::Image>(
        "camera/image_raw", sensor_qos,
        [this] (sensor_msgs::msg::Image::ConstSharedPtr msg) {
          this->image_cb(std::move(msg));
        });

    timer_ = create_wall_timer(
        std::chrono::milliseconds(static_cast<int>(1000.0 / rate_hz)),
        [this] () { this->timer_cb(); });

    RCLCPP_INFO(get_logger(), "Perception started at %.1fHz", rate_hz);
  }

private:
  void image_cb(sensor_msgs::msg::Image::ConstSharedPtr msg) {
    auto detections = logic_->detect(*msg);
    det_pub_->publish(detections);
  }
  void timer_cb() {}

  std::unique_ptr<my_pkg::PerceptionLogic> logic_;
  rclcpp::Publisher<vision_msgs::msg::Detection2DArray>::SharedPtr det_pub_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr image_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PerceptionNode>());
  rclcpp::shutdown();
  return 0;
}
```

> **Avoid virtual calls in C++ Node constructors.** A common BaseNode pattern that calls `setup_publishers()` in the base ctor will dispatch to the BASE override, not the derived class. Initialize in the derived ctor or use a separate `init()` method called after construction.

## Workspace-Wide BaseNode (Optional)

Useful when many nodes share parameter names or QoS conventions.

```python
# rclpy
class BaseRobotNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.declare_parameter('update_rate', 10.0)
        self._update_rate = self.get_parameter('update_rate').value
        self.get_logger().info(f'{node_name} initialized')

    def create_rate_timer(self, callback):
        return self.create_timer(1.0 / self._update_rate, callback)
```

```cpp
// rclcpp
class BaseRobotNode : public rclcpp::Node {
public:
  BaseRobotNode(const std::string& name,
                const rclcpp::NodeOptions& opts = rclcpp::NodeOptions())
      : Node(name, opts) {
    declare_parameter("update_rate", 10.0);
    update_rate_ = get_parameter("update_rate").as_double();
    RCLCPP_INFO(get_logger(), "%s initialized", name.c_str());
  }
protected:
  rclcpp::TimerBase::SharedPtr create_rate_timer(std::function<void()> cb) {
    auto period = std::chrono::duration<double>(1.0 / update_rate_);
    return create_wall_timer(period, cb);
  }
  double update_rate_;
};
```

## Package Scaffolding

### `package.xml` (C++ with custom messages)

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_robot_pkg</name>
  <version>0.1.0</version>
  <description>Robot perception package</description>
  <maintainer email="dev@example.com">Dev</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>

  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_cmake_pytest</test_depend>
  <test_depend>launch_testing_ament_cmake</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### `CMakeLists.txt` (ament_cmake)

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_pkg)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(vision_msgs REQUIRED)

add_executable(perception_node src/perception_node.cpp)
ament_target_dependencies(perception_node rclcpp sensor_msgs vision_msgs)
install(TARGETS perception_node DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

### `setup.py` (ament_python)

```python
from setuptools import find_packages, setup

package_name = 'my_python_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/robot.launch.py']),
        ('share/' + package_name + '/config', ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dev',
    maintainer_email='dev@example.com',
    description='Pure Python ROS2 package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'perception_node = my_python_pkg.perception_node:main',
        ],
    },
)
```

### Build types: pick one

- `ament_cmake` — C++ packages, mixed C++/Python, packages with custom messages.
- `ament_python` — pure Python packages with no C++ code and no message generation.

### Recommended package layout

```
my_robot_pkg/
├── CMakeLists.txt          # or setup.py for ament_python
├── package.xml
├── my_robot_pkg/           # Python module (same name as package)
│   ├── __init__.py
│   ├── perception_node.py  # ROS2 adapter
│   └── perception_logic.py # pure Python, no rclpy import
├── src/                    # C++ adapters
│   └── perception_node.cpp
├── include/my_robot_pkg/   # C++ headers (pure logic + adapter headers)
├── config/                 # YAML defaults — see ros2-launch-config
│   └── params.yaml
├── launch/                 # XML or Python launch — see ros2-launch-config
│   └── robot.launch.py
├── msg/  srv/  action/     # see ros2-messaging, ros2-service-action
└── test/                   # see ros2-testing
```

## Executor and Callback-Group Choice

Default to `SingleThreadedExecutor`. Reach for multi-threading only when you can name the specific deadlock or throughput problem it solves.

| Situation                                                  | Use                                                |
|------------------------------------------------------------|----------------------------------------------------|
| Most nodes                                                 | `SingleThreadedExecutor` (deterministic, simple)    |
| Service-call-from-callback (would self-deadlock)           | `MultiThreadedExecutor` + `ReentrantCallbackGroup` |
| Heavy CPU work in one callback blocking high-rate sensor   | Two callback groups, separate executor threads     |
| One node, high-frequency sensor + slow planner in same proc| Composition + multi-threaded container             |

```python
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup

# In a node that calls a service from a subscriber callback:
self._sensor_cb_group = MutuallyExclusiveCallbackGroup()
self._service_cb_group = ReentrantCallbackGroup()
self.create_subscription(Image, 'image', self._cb, 10,
                         callback_group=self._sensor_cb_group)
self._client = self.create_client(Trigger, 'trigger',
                                  callback_group=self._service_cb_group)

# In main():
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

## Three Cross-Cutting Rules

- **Single responsibility.** One node, one job. Split a node before its `__init__` exceeds ~50 lines.
- **C++ for hot paths, Python everywhere else.** Use C++ for high-frequency control loops and large-data processing (images, point clouds). Python is fine for tooling, orchestration, and prototyping.
- **Don't fork upstream just to change config.** Copy launch and config files into your workspace and override there. Rebuilding upstream is a maintenance trap.

For logging, see `ros2-diagnostics`. For dependency declaration, see the `package.xml` example above.

## Common Pitfalls

| Pitfall                                                          | What goes wrong                                                                       | Fix                                                                                  |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Subscribing before publishers are created                         | Subscriber callback fires while `self._pub` is still `None`                          | Create publishers before subscriptions in `__init__`                                  |
| Heavy CPU work inside callback                                   | Blocks executor → other callbacks starve → topics appear "dropped"                   | Move work to a timer or a worker thread; consider MultiThreadedExecutor              |
| Calling a service from a subscriber on SingleThreadedExecutor    | Deadlock                                                                              | MultiThreadedExecutor + `ReentrantCallbackGroup` for the client                       |
| Mutating shared state from multiple callbacks without locking    | Data races under MultiThreadedExecutor                                                | Either stay single-threaded, or use locks and `MutuallyExclusiveCallbackGroup`        |
| Calling virtual methods in C++ Node base ctor                    | Dispatches to base, not derived                                                       | Use a separate `init()` method called after construction                              |
| `print()` in node code                                           | Bypasses logging, no log capture, breaks tooling                                      | `self.get_logger().info(...)` / `RCLCPP_INFO(get_logger(), ...)`                      |
| Logging every iteration of a 1kHz loop                           | Floods `/rosout`, kills disk and bandwidth                                            | Use throttled logs (`throttle_duration_sec`)                                          |
| Hardcoding parameter values in Python launch files               | Can't tune without code change; no `ros2 param` introspection                         | Externalize to YAML config (see `ros2-launch-config`)                                 |

## Related Skills

- **ros2-messaging** — QoS profiles, custom messages, pub/sub patterns
- **ros2-service-action** — when to use service vs action; clients and servers
- **ros2-launch-config** — turning your nodes into a launchable system
- **ros2-lifecycle** — production nodes with managed startup/shutdown
- **ros2-clean-architecture** — full layered structure for larger codebases
- **ros2-testing** — unit and integration tests for your nodes
