---
name: ros2-diagnostics
description: >
  ROS2 diagnostics, health monitoring, and structured logging patterns. Use when adding
  diagnostic_updater health checks, publishing diagnostic_msgs on /diagnostics, monitoring
  topic frequency, wiring diagnostic_aggregator, reporting hardware status, using OK, WARN,
  ERROR, or STALE states, building health dashboards, checking whether a node or sensor is
  healthy, or fixing log spam with throttled or structured logging.
---

# ROS2 Diagnostics and Health Monitoring

## When to Use This Skill

- Adding health checks to a node so a supervisor or operator dashboard can read its status
- Monitoring topic publication frequency (camera dropping frames, IMU stalled)
- Wiring `diagnostic_aggregator` to roll per-node statuses into a system-wide health view
- Reporting hardware diagnostics from a driver (motor temperature, battery level)
- Tightening up logging — picking levels, throttling high-frequency logs, killing `print()`

## The Standard: `diagnostic_msgs/DiagnosticStatus`

Every diagnostic carries a level (OK/WARN/ERROR/STALE), a name, a message, and key/value pairs:

```
uint8 OK = 0
uint8 WARN = 1
uint8 ERROR = 2
uint8 STALE = 3

uint8 level
string name          # e.g. "left_motor"
string message       # human-readable summary
string hardware_id   # which physical device
KeyValue[] values    # structured details
```

Publish a `DiagnosticArray` of these on `/diagnostics`. Tools like `rqt_robot_monitor` and `diagnostic_aggregator` consume that topic.

## `diagnostic_updater`: The Easy Path

Don't hand-roll the publishing — use `diagnostic_updater`. It owns the publisher, runs your check callbacks on a timer, and sets `STALE` automatically if a check stops being called.

### Python

```python
import rclpy
from rclpy.node import Node
from diagnostic_updater import Updater
from diagnostic_msgs.msg import DiagnosticStatus


class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        self._updater = Updater(self)
        self._updater.setHardwareID('motor_left_v2')
        self._updater.add('Temperature', self._check_temp)
        self._updater.add('Current',     self._check_current)

    def _check_temp(self, stat):
        temp = self._read_temp()
        if temp > 90.0:
            stat.summary(DiagnosticStatus.ERROR, f'overheating: {temp:.1f}C')
        elif temp > 75.0:
            stat.summary(DiagnosticStatus.WARN,  f'warm: {temp:.1f}C')
        else:
            stat.summary(DiagnosticStatus.OK,    f'normal: {temp:.1f}C')
        stat.add('temperature_c', f'{temp:.2f}')
        stat.add('threshold_warn', '75.0')
        stat.add('threshold_error', '90.0')
        return stat

    def _check_current(self, stat):
        amps = self._read_current()
        stat.summary(DiagnosticStatus.OK if amps < 5.0 else DiagnosticStatus.WARN,
                     f'{amps:.2f} A')
        stat.add('current_a', f'{amps:.3f}')
        return stat
```

### C++

```cpp
#include <rclcpp/rclcpp.hpp>
#include <diagnostic_updater/diagnostic_updater.hpp>
#include <diagnostic_msgs/msg/diagnostic_status.hpp>

class MotorNode : public rclcpp::Node {
public:
  MotorNode() : Node("motor_node"), updater_(this) {
    updater_.setHardwareID("motor_left_v2");
    updater_.add("Temperature",
        [this] (diagnostic_updater::DiagnosticStatusWrapper& stat) {
          double t = read_temp();
          if (t > 90.0)      stat.summary(diagnostic_msgs::msg::DiagnosticStatus::ERROR,
                                          "overheating");
          else if (t > 75.0) stat.summary(diagnostic_msgs::msg::DiagnosticStatus::WARN,
                                          "warm");
          else               stat.summary(diagnostic_msgs::msg::DiagnosticStatus::OK,
                                          "normal");
          stat.add("temperature_c", t);
        });
  }
private:
  double read_temp();
  diagnostic_updater::Updater updater_;
};
```

`Updater` publishes on a timer (default 1 Hz). It will mark a check `STALE` if it isn't returning, even if the node itself is alive — invaluable for catching hung threads.

## Topic Frequency Monitoring

If a sensor stops publishing, the consumer often discovers it minutes later. Wrap the publisher in a `TopicDiagnostic` (or `HeaderlessTopicDiagnostic`) so deviation from the expected rate immediately surfaces on `/diagnostics`.

```cpp
#include <diagnostic_updater/publisher.hpp>

class CameraDriver : public rclcpp::Node {
public:
  CameraDriver() : Node("camera"), updater_(this) {
    updater_.setHardwareID("realsense_d435");

    pub_ = create_publisher<sensor_msgs::msg::Image>("image_raw", 10);

    double min_freq = 28.0, max_freq = 32.0;     // expect 30 Hz ± a bit
    diagnostic_updater::FrequencyStatusParam freq_param(
        &min_freq, &max_freq,
        /*tolerance*/ 0.1, /*window_size*/ 10);

    diag_pub_ = std::make_unique<diagnostic_updater::HeaderlessTopicDiagnostic>(
        "image_raw", updater_, freq_param);

    timer_ = create_wall_timer(std::chrono::milliseconds(33),
        [this] () {
          auto msg = sensor_msgs::msg::Image();
          // ... fill ...
          pub_->publish(msg);
          diag_pub_->tick();    // record the publish
        });
  }
private:
  diagnostic_updater::Updater updater_;
  std::unique_ptr<diagnostic_updater::HeaderlessTopicDiagnostic> diag_pub_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};
```

## Aggregation: `diagnostic_aggregator`

For a system view, run `diagnostic_aggregator_node` with an analyzer config that groups statuses by subsystem.

```yaml
# config/diagnostic_aggregator.yaml
diagnostic_aggregator:
  ros__parameters:
    pub_rate: 1.0
    base_path: ""
    analyzers:
      sensors:
        type: diagnostic_aggregator/AnalyzerGroup
        path: Sensors
        analyzers:
          camera:
            type: diagnostic_aggregator/GenericAnalyzer
            path: Camera
            contains: ["camera"]
          lidar:
            type: diagnostic_aggregator/GenericAnalyzer
            path: LiDAR
            contains: ["lidar"]
      motors:
        type: diagnostic_aggregator/GenericAnalyzer
        path: Motors
        contains: ["motor"]
```

`/diagnostics_agg` will publish a tree like `Sensors/Camera/Temperature: OK`. View it with `rqt_robot_monitor`.

## Logging Best Practices

Diagnostics is for structured, supervisor-readable health. Logs are for human-readable narrative. Use both, and keep them disciplined.

### Use the ROS2 logger, never `print` or `std::cout`

```python
self.get_logger().info('node started')
```

```cpp
RCLCPP_INFO(get_logger(), "node started");
```

`print()` and `std::cout` bypass `/rosout`, RViz, log capture, and bag recording. They're invisible to your future self.

### Pick the right level

| Level    | Use for                                                          |
|----------|------------------------------------------------------------------|
| `DEBUG`  | Verbose detail useful only when something is wrong               |
| `INFO`   | Normal operation milestones (start, configured, goal accepted)   |
| `WARN`   | Unexpected but recoverable (sensor drop, retry)                  |
| `ERROR`  | System not operating correctly; needs attention                  |
| `FATAL`  | Unrecoverable; node is shutting down                             |

### Throttle high-frequency logs

A log inside a 1 kHz callback floods `/rosout` and the disk. Use throttling.

```python
self.get_logger().info('still running', throttle_duration_sec=1.0)
self.get_logger().warn(f'sensor jitter: {jitter}s', throttle_duration_sec=5.0)
self.get_logger().info('initialized', once=True)
```

```cpp
RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), /*ms*/ 1000, "still running");
RCLCPP_INFO_ONCE(get_logger(), "initialized");
```

### Set log level dynamically

```bash
ros2 service call /perception/set_logger_levels rcl_interfaces/srv/SetLoggerLevels \
  "{levels: [{name: 'perception', level: 10}]}"   # 10 = DEBUG
```

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                          | Fix                                                                                     |
|---------------------------------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Forgetting `setHardwareID`                                    | `/diagnostics` entries can't be grouped by physical device               | Set a unique hardware ID per `Updater` instance                                          |
| Running `Updater` and never calling `add()`                   | Nothing publishes; silent                                                | Add at least one check; verify with `ros2 topic echo /diagnostics`                       |
| Heavy work inside a check callback                            | `Updater` timer falls behind; STALE warnings cascade                     | Read cached values in checks; do work elsewhere                                          |
| Conflating logs with diagnostics                              | Operators have to parse log streams to know health                       | Use `diagnostic_updater` for health; use `get_logger()` for narrative                    |
| Logging every tick of a high-rate callback                    | Disk fills, log readers can't keep up                                    | Throttle: `throttle_duration_sec=1.0` / `RCLCPP_INFO_THROTTLE`                           |
| `print()` / `std::cout` from a node                           | Bypasses `/rosout`, no capture in bags or remote consoles                | Use `get_logger()` always                                                                |

## Related Skills

- **ros2-messaging** — `/diagnostics` is just a publisher with `DiagnosticArray`
- **ros2-lifecycle** — diagnostics often report which lifecycle state a node is in
- **robot-bringup** — system-level watchdogs that consume `/diagnostics`
- **robotics-testing** — assert on diagnostic outputs during integration tests
