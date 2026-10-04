---
name: ros2-transforms
description: >
  ROS2 TF2 transform patterns for static and dynamic broadcasters, listeners, buffers, frame
  trees, and timestamped lookup. Use when designing robot coordinate frames, publishing sensor
  or odometry transforms, using tf2_ros, TransformBroadcaster, StaticTransformBroadcaster,
  TransformListener, lookupTransform, debugging disconnected or stale frames,
  ExtrapolationException, TF_OLD_DATA, /tf, /tf_static, map, odom, base_link, or camera
  frames.
---

# ROS2 Transforms (TF2)

## When to Use This Skill

- Designing the coordinate-frame hierarchy for a new robot
- Publishing static transforms (sensor mountings) and dynamic transforms (odometry, joint poses)
- Looking up transforms in a perception or planning node
- Diagnosing "TF tree disconnected" or "Could not find transform" errors
- Keeping `tf2_ros` out of your domain/business code so it stays unit-testable

## A Clean Frame Tree

A typical mobile robot:

```
map                              # global, fixed frame (set by SLAM/AMCL)
 └── odom                        # drift-prone but smooth, set by odometry source
      └── base_footprint         # robot ground projection (z=0)
           └── base_link         # robot body origin
                ├── lidar_link
                ├── camera_link
                │    └── camera_optical    # REP-103 optical convention (z forward)
                ├── imu_link
                └── left_wheel
                └── right_wheel
```

Rules of thumb:

- `map → odom` is the localization correction; `odom → base_footprint` is the odometry estimate.
- Each frame has exactly one parent. The TF tree is a tree, not a graph.
- Sensor frames use REP-103: x-forward, y-left, z-up; camera optical frames use z-forward.
- Static mountings (camera-on-base) → `/tf_static`. Anything that moves → `/tf`.

## Broadcast: Static vs. Dynamic

### Static (sensor mountings, fixed extrinsics) — Python

```python
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster

class CameraMount(Node):
    def __init__(self):
        super().__init__('camera_mount')
        self._static = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'camera_link'
        t.transform.translation.x = 0.10
        t.transform.translation.y = 0.00
        t.transform.translation.z = 0.20
        t.transform.rotation.w = 1.0    # identity quaternion
        self._static.sendTransform(t)
```

### Dynamic (odometry, joint motion) — Python

```python
from tf2_ros import TransformBroadcaster

class OdometryPublisher(Node):
    def __init__(self):
        super().__init__('odometry_publisher')
        self._tf = TransformBroadcaster(self)
        self.create_timer(0.02, self._tick)   # 50 Hz

    def _tick(self):
        x, y, theta = self._read_encoders()
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = x
        t.transform.translation.y = y
        # convert theta → quaternion
        t.transform.rotation.z = math.sin(theta / 2.0)
        t.transform.rotation.w = math.cos(theta / 2.0)
        self._tf.sendTransform(t)
```

### C++ broadcaster

```cpp
#include <tf2_ros/static_transform_broadcaster.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

class OdometryPublisher : public rclcpp::Node {
public:
  OdometryPublisher() : Node("odometry_publisher"),
      tf_(std::make_unique<tf2_ros::TransformBroadcaster>(this)) {
    timer_ = create_wall_timer(std::chrono::milliseconds(20),
        [this] () { tick(); });
  }
private:
  void tick() {
    geometry_msgs::msg::TransformStamped t;
    t.header.stamp = now();
    t.header.frame_id = "odom";
    t.child_frame_id = "base_footprint";
    // ... fill translation/rotation ...
    tf_->sendTransform(t);
  }
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_;
  rclcpp::TimerBase::SharedPtr timer_;
};
```

## Listen: Look Up Transforms

```python
from tf2_ros import Buffer, TransformListener
from rclpy.duration import Duration
from tf2_ros import LookupException, ExtrapolationException

class GoalProjector(Node):
    def __init__(self):
        super().__init__('goal_projector')
        self._buf = Buffer()
        self._listener = TransformListener(self._buf, self)

    def project(self, target_frame: str, source_frame: str):
        try:
            tf = self._buf.lookup_transform(
                target_frame, source_frame, rclpy.time.Time(),
                timeout=Duration(seconds=0.1))
            return tf
        except (LookupException, ExtrapolationException) as e:
            self.get_logger().warn(
                f'TF {source_frame}->{target_frame} unavailable: {e}')
            return None
```

```cpp
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_listener.h>

class GoalProjector : public rclcpp::Node {
public:
  GoalProjector() : Node("goal_projector"),
      tf_buffer_(get_clock()),
      tf_listener_(tf_buffer_) {}

  std::optional<geometry_msgs::msg::TransformStamped>
  lookup(const std::string& target, const std::string& source) {
    try {
      return tf_buffer_.lookupTransform(
          target, source, tf2::TimePointZero,
          tf2::durationFromSec(0.1));
    } catch (const tf2::TransformException& ex) {
      RCLCPP_WARN(get_logger(), "%s -> %s: %s",
                  source.c_str(), target.c_str(), ex.what());
      return std::nullopt;
    }
  }
private:
  tf2_ros::Buffer tf_buffer_;
  tf2_ros::TransformListener tf_listener_;
};
```

## Keep TF2 Out of Domain Code

For codebases large enough to layer, define a domain `Pose` (plain dataclass with position, orientation, frame_id, timestamp) and an `ITransformService` port. The TF2 buffer/listener live in an infrastructure adapter that implements the port. Tests inject a fake adapter; the use case never imports `tf2_ros`.

See `ros2-clean-architecture` for the full port-and-adapter pattern.

## Use `Time(0)` vs. Specific Timestamps

- `lookup_transform(target, source, Time())` (Python `rclpy.time.Time()` or C++ `tf2::TimePointZero`) returns the **latest** available transform. Convenient, but loses time correlation.
- For data fusion, look up the transform at the **timestamp of the data** so you align correctly:

```python
tf = self._buf.lookup_transform(
    'map', msg.header.frame_id, msg.header.stamp,
    timeout=Duration(seconds=0.1))
```

This will raise `ExtrapolationException` if the transform isn't yet available — handle by waiting or skipping the message.

## Debugging the TF Tree

```bash
# Visualize the tree
ros2 run tf2_tools view_frames     # writes frames.pdf
xdg-open frames.pdf

# Inspect a single transform
ros2 run tf2_ros tf2_echo base_link camera_link

# Live monitor
ros2 topic echo /tf_static --once
ros2 topic hz /tf
```

Common warnings:

- `TF_OLD_DATA` — broadcaster sent a transform with a timestamp older than what's already in the buffer. Usually a clock-mixing bug (sim time vs wall time).
- `Lookup would require extrapolation into the future` — transform isn't published yet at the time you're asking for. Either wait or use `Time(0)`.
- `frame X does not exist` — typo, or a node responsible for publishing X isn't running.

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                          | Fix                                                                                       |
|---------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Publishing static transforms on `/tf` instead of `/tf_static` | TF buffer fills with duplicate identical transforms                      | Use `StaticTransformBroadcaster`; it publishes once with TRANSIENT_LOCAL durability        |
| Two broadcasters publishing the same `child_frame_id`         | TF tree non-deterministic; "lookup would require extrapolation"          | One frame, one broadcaster. Audit with `view_frames`.                                      |
| Mixing wall time and `use_sim_time=true`                      | `TF_OLD_DATA` warnings, lookups fail intermittently                      | Set `use_sim_time` consistently across all nodes (see `ros2-launch-config`)               |
| Domain code imports `tf2_ros`                                 | Can't unit-test without spinning a ROS node                              | Define `ITransformService`; inject a fake in tests                                         |
| Looking up at `Time(0)` then fusing with a timestamped message | Sensor data ends up paired with a transform from the wrong instant      | Look up at the message timestamp; handle `ExtrapolationException`                          |
| No timeout on `lookup_transform`                              | Caller blocks forever on first failure                                   | Always pass a `timeout`; catch the exception                                              |

## Related Skills

- **ros2-messaging** — `/tf` and `/tf_static` are messaging on `tf2_msgs`/`geometry_msgs`
- **ros2-node-creation** — base nodes that own a `Buffer` + `TransformListener`
- **ros2-clean-architecture** — port pattern for keeping TF out of domain code
- **robot-perception** — fusing sensors via TF lookups
