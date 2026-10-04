---
name: ros2-testing
description: >
  ROS2 package testing patterns for rclpy and rclcpp. Use when adding pytest, gtest,
  ament_cmake_pytest, ament_add_gtest, launch_testing, ReadyToTest, node fixtures, spin_once,
  spin_some, integration tests, end-to-end launch tests, service or action tests, CI for ROS2
  workspaces, or debugging flaky tests caused by sleeps, QoS, timing, or executor behavior.
---

# ROS2 Testing

> **This skill** focuses on `pytest`/`gtest` for `rclpy`/`rclcpp` packages.
> See `robotics-testing` for the wider story (hardware mocks, simulation harnesses, CI).

## When to Use This Skill

- Adding tests to a ROS2 package (Python or C++)
- Wiring `BUILD_TESTING` in `CMakeLists.txt` (`ament_cmake_pytest`, `ament_add_gtest`)
- Writing pytest fixtures that handle `rclpy.init`/`rclpy.shutdown` cleanly
- Asserting on what a node publishes given what it receives
- Wrapping a system in a `launch_testing` end-to-end test
- Removing flaky `sleep(N)` calls from existing tests

## The Pyramid

```
        /\
       /  \   E2E (launch_testing) — slow, real config
      /----\
     /      \  Integration — node spun in-process
    /--------\
   /          \  Unit — pure Python / pure C++, no rclpy
  /--------------\
```

Most tests should be unit tests. The architectural rule (see `ros2-clean-architecture`): if your business logic is in plain classes outside the node, you can unit-test it without ROS at all. Reserve integration tests for the node's wiring (subscriptions, timers, service handlers).

## Directory Layout

```
package_name/
├── test/
│   ├── unit/
│   │   ├── test_perception_logic.py
│   │   └── test_state_machine.py
│   ├── integration/
│   │   └── test_perception_node.py
│   └── e2e/
│       └── test_perception.launch.py
└── package.xml
```

## Unit Tests

### Python (pytest)

```python
# test/unit/test_perception_logic.py
import pytest
from my_pkg.perception_logic import PerceptionLogic


def test_threshold_filters_low_confidence():
    logic = PerceptionLogic(threshold=0.7)
    detections = logic.detect_from_array(_fake_image_with_two_objects(0.6, 0.8))
    assert len(detections) == 1
    assert detections[0].confidence == 0.8


def test_invalid_threshold_rejected():
    with pytest.raises(ValueError):
        PerceptionLogic(threshold=1.5)
```

### C++ (GTest)

```cpp
// test/unit/test_robot_controller.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "domain/use_cases/robot_controller.hpp"
#include "domain/interfaces/robot_repository.hpp"

using ::testing::Return;

class MockRepo : public domain::interfaces::IRobotRepository {
public:
  MOCK_METHOD(domain::entities::RobotState, get_state, (), (override));
  MOCK_METHOD(void, set_mode, (domain::entities::RobotMode), (override));
};

TEST(RobotControllerTest, StartFromIdleSucceeds) {
  auto repo = std::make_shared<MockRepo>();
  domain::use_cases::RobotController ctrl(repo);

  EXPECT_CALL(*repo, get_state())
      .WillOnce(Return(domain::entities::RobotState{
          domain::entities::RobotMode::IDLE}));
  EXPECT_CALL(*repo, set_mode(domain::entities::RobotMode::ACTIVE));

  EXPECT_TRUE(ctrl.start().success);
}
```

## Integration Tests (Node Spun In-Process)

### Python — fixture handles `rclpy` lifecycle

```python
# test/integration/test_perception_node.py
import pytest
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray

from my_pkg.perception_node import PerceptionNode


@pytest.fixture(scope='module')
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


@pytest.fixture
def perception(ros_context):
    node = PerceptionNode()
    yield node
    node.destroy_node()


def test_perception_publishes_detections(perception, ros_context):
    helper = Node('test_helper')
    received = []

    helper.create_subscription(
        Detection2DArray, 'detections',
        lambda msg: received.append(msg), 10)

    pub = helper.create_publisher(Image, 'camera/image_raw', 10)
    pub.publish(_fake_image_with_object())

    # Wait for the message — bounded, no arbitrary sleeps
    deadline = helper.get_clock().now() + rclpy.duration.Duration(seconds=1.0)
    while not received and helper.get_clock().now() < deadline:
        rclpy.spin_once(perception, timeout_sec=0.05)
        rclpy.spin_once(helper,     timeout_sec=0.05)

    assert received, 'no detections received within 1s'
    helper.destroy_node()
```

### C++ — `SetUp`/`TearDown` for `rclcpp`

```cpp
// test/integration/test_sensor_node.cpp
#include <gtest/gtest.h>
#include <rclcpp/rclcpp.hpp>
#include "infrastructure/ros2/nodes/sensor_node.hpp"

class SensorNodeTest : public ::testing::Test {
protected:
  void SetUp() override {
    if (!rclcpp::ok()) rclcpp::init(0, nullptr);
    node_ = std::make_shared<infrastructure::ros2::nodes::SensorNode>();
  }
  void TearDown() override {
    node_.reset();
    rclcpp::shutdown();
  }
  std::shared_ptr<infrastructure::ros2::nodes::SensorNode> node_;
};

TEST_F(SensorNodeTest, NameMatches) {
  EXPECT_STREQ(node_->get_name(), "sensor_node");
}
```

### `wait_for_message` Helper Beats `sleep`

```python
def wait_for(predicate, *, nodes, timeout_sec=2.0, tick=0.05):
    """Spin all nodes until predicate() is true or timeout."""
    deadline = nodes[0].get_clock().now() + rclpy.duration.Duration(seconds=timeout_sec)
    while not predicate() and nodes[0].get_clock().now() < deadline:
        for n in nodes:
            rclpy.spin_once(n, timeout_sec=tick)
    return predicate()
```

```python
assert wait_for(lambda: len(received) >= 1, nodes=[perception, helper])
```

## End-to-End: `launch_testing`

Run actual launch files and assert on system-level behavior.

```python
# test/e2e/test_perception.launch.py
import unittest
import launch_testing
import pytest
import rclpy
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_testing.actions import ReadyToTest


@pytest.mark.launch_test
def generate_test_description():
    perception = Node(package='my_pkg', executable='perception_node',
                      name='perception', output='screen')

    return LaunchDescription([
        perception,
        ReadyToTest(),
    ]), {'perception': perception}


class TestPerceptionLaunch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def test_perception_starts_and_publishes(self, perception):
        node = rclpy.create_node('e2e_helper')
        received = []
        node.create_subscription(
            Detection2DArray, 'detections',
            lambda msg: received.append(msg), 10)

        # ... drive inputs, spin, assert ...
        node.destroy_node()
```

## Wiring Tests Into the Build

### `package.xml`

```xml
<test_depend>ament_lint_auto</test_depend>
<test_depend>ament_cmake_pytest</test_depend>     <!-- Python unit/integration -->
<test_depend>ament_cmake_gtest</test_depend>      <!-- C++ unit -->
<test_depend>launch_testing_ament_cmake</test_depend>  <!-- E2E -->
```

### `CMakeLists.txt`

```cmake
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  # Python
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(unit_tests        test/unit)
  ament_add_pytest_test(integration_tests test/integration)

  # C++
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_robot_controller test/unit/test_robot_controller.cpp)
  target_link_libraries(test_robot_controller my_pkg_lib)

  # E2E
  find_package(launch_testing_ament_cmake REQUIRED)
  add_launch_test(test/e2e/test_perception.launch.py)
endif()
```

### Run

```bash
colcon test --packages-select my_pkg
colcon test-result --verbose

# Coverage
pytest --cov=my_pkg --cov-report=html test/unit
```

## No Arbitrary `sleep()` in Tests

`time.sleep(2)` is the leading cause of flaky ROS2 tests: too short under load and the assertion fires before the message arrives; too long and the suite crawls. Always:

1. **Use a bounded wait predicate** (see `wait_for` helper above).
2. **Subscribe before publishing** — otherwise the subscription may not be discovered yet.
3. **Spin both nodes** (publisher and subscriber) inside the wait loop.
4. For services/actions, use `wait_for_service` / `wait_for_server` instead of sleeping.

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                          | Fix                                                                                       |
|---------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Calling `rclpy.init()` in every test                          | Crashes with "context already initialized"                               | One module-scoped fixture: `init` in setup, `shutdown` in teardown                        |
| Subscribing **after** publishing                              | DDS discovery hasn't finished; first message lost                        | Create the subscriber, then spin once, then publish                                       |
| `sleep(2)` to wait for a message                              | Flaky under load                                                         | `wait_for(predicate, timeout=2.0)` with bounded ticks                                     |
| Testing only the node, never the logic                        | Slow tests; coverage of math/algorithms is tied to ROS spin              | Pull logic into plain classes; unit-test those without `rclpy`                            |
| QoS mismatch between test publisher and node subscriber       | Test sees no messages; passes locally if defaults align, fails in CI     | Match QoS exactly (see `ros2-messaging`)                                                  |
| Sharing global state between tests                            | Tests pass alone, fail in suite                                          | Reset state in `setUp`; use function-scoped fixtures for nodes                            |
| Heavy E2E tests for everything                                | Suite takes 10+ minutes; CI flakes constantly                            | Push assertions down to integration tests; keep E2E for true system-level invariants      |

## Coverage Target

Henki's guidance: aim for **90–100%** unit coverage on application logic. Integration tests cover wiring; E2E tests cover the few invariants that only emerge with the full stack running.

## Related Skills

- **ros2-node-creation** — keep logic out of nodes so unit tests don't need `rclpy`
- **ros2-clean-architecture** — port pattern enables mocks for use-case tests
- **ros2-messaging** — match QoS in tests or messages won't arrive
- **ros2-launch-config** — `launch_testing` reuses your launch files
- **robotics-testing** — broader strategies (hardware mocks, simulation, CI)
