---
name: ros2-lifecycle
description: >
  ROS2 managed lifecycle node patterns for deterministic startup, activation, shutdown,
  reconfiguration, and recovery. Use when implementing LifecycleNode behavior, on_configure,
  on_activate, on_deactivate, on_cleanup, on_shutdown, on_error, lifecycle services or
  clients, supervisor orchestration, configure-then-activate flows, deactivate-to-reconfigure
  workflows, or debugging nodes stuck unconfigured or inactive.
---

# ROS2 Lifecycle Nodes

## When to Use This Skill

- Bringing up a production robot where startup order and recovery matter
- A node needs to load resources (models, calibration, hardware connections) before going live
- Reconfiguring a running node without restarting (deactivate → cleanup → configure → activate)
- Implementing a supervisor that orchestrates other nodes via `lifecycle_msgs`
- Debugging "node started but is silently doing nothing" — likely stuck in `unconfigured`

If your node only needs `__init__` and `main`, you don't need a lifecycle node. Reach for it when the **transition** between not-running and fully-operational is itself a thing your system needs to control.

## The State Machine

```
                +-----------+   create()
                |  UNKNOWN  | -----------+
                +-----------+            v
                                 +--------------+
                                 | UNCONFIGURED |<------------+
                                 +--------------+             |
                                       |                      |
                                  configure()             cleanup()
                                       v                      |
                                 +-----------+                |
                                 |  INACTIVE | ---------------+
                                 +-----------+
                                       |
                                  activate()    deactivate()
                                       v             ^
                                 +-----------+       |
                                 |  ACTIVE   |-------+
                                 +-----------+
                                       |
                                   shutdown()
                                       v
                                 +-----------+
                                 |  FINALIZED|
                                 +-----------+
```

| State          | Meaning                                                          |
|----------------|------------------------------------------------------------------|
| `unconfigured` | Just created. No resources held.                                 |
| `inactive`     | Configured (resources allocated), but not yet doing work.        |
| `active`       | Doing its job — publishers publish, subscribers process.          |
| `finalized`    | Shutting down. Terminal.                                          |

## The Discipline: What Happens In Each Transition

| Callback         | Do                                                              | Don't                                                              |
|------------------|-----------------------------------------------------------------|--------------------------------------------------------------------|
| `on_configure`   | Allocate memory, load models, open hardware, create pubs/subs   | Start work, publish, subscribe to topics that will trigger work    |
| `on_activate`    | Activate publishers, start timers, enable subscriptions         | Allocate resources (do that in configure)                          |
| `on_deactivate`  | Stop timers, disable subscriptions, deactivate publishers       | Free resources (you may activate again later)                      |
| `on_cleanup`     | Free everything `on_configure` allocated; back to `unconfigured`| Leave resources held                                               |
| `on_shutdown`    | Final cleanup before destruction                                 | Anything that depends on others — they may already be shutting down|
| `on_error`       | Try to recover; otherwise return FAILURE                        | Hide errors; log + return appropriate state                        |

Returning `FAILURE` from a callback aborts the transition; returning `ERROR` triggers `on_error`.

## Python Implementation

```python
import rclpy
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import TransitionCallbackReturn
from rclpy.lifecycle import LifecyclePublisher
from sensor_msgs.msg import Image
from robot_interfaces.msg import DetectionArray


class ManagedPerception(LifecycleNode):
    def __init__(self):
        super().__init__('managed_perception')
        self.declare_parameter('model_path', '')
        self._model = None
        self._det_pub: LifecyclePublisher = None
        self._image_sub = None

    def on_configure(self, state) -> TransitionCallbackReturn:
        try:
            from my_pkg.detector import load_model
            self._model = load_model(self.get_parameter('model_path').value)
            self._det_pub = self.create_lifecycle_publisher(
                DetectionArray, 'detections', 10)
            self.get_logger().info('configured')
            return TransitionCallbackReturn.SUCCESS
        except Exception as e:
            self.get_logger().error(f'configure failed: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state) -> TransitionCallbackReturn:
        self._image_sub = self.create_subscription(
            Image, 'camera/image_raw', self._on_image, 1)
        # LifecyclePublisher requires explicit activation
        super().on_activate(state)
        self.get_logger().info('active')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state) -> TransitionCallbackReturn:
        self.destroy_subscription(self._image_sub)
        self._image_sub = None
        super().on_deactivate(state)
        self.get_logger().info('inactive')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state) -> TransitionCallbackReturn:
        self.destroy_publisher(self._det_pub)
        self._det_pub = None
        self._model = None
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state) -> TransitionCallbackReturn:
        return TransitionCallbackReturn.SUCCESS

    def on_error(self, state) -> TransitionCallbackReturn:
        self.get_logger().error(f'error in state {state.label}')
        return TransitionCallbackReturn.SUCCESS

    def _on_image(self, msg):
        if self._det_pub is None:
            return
        # Publishers ignore messages while inactive — but explicit guard is clearer
        detections = self._model.detect(msg)
        self._det_pub.publish(detections)


def main():
    rclpy.init()
    node = ManagedPerception()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## C++ Implementation

```cpp
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_lifecycle/lifecycle_node.hpp>
#include <rclcpp_lifecycle/lifecycle_publisher.hpp>
#include <std_msgs/msg/string.hpp>

using CallbackReturn =
    rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

class ManagedNode : public rclcpp_lifecycle::LifecycleNode {
public:
  explicit ManagedNode(const rclcpp::NodeOptions& opts = rclcpp::NodeOptions())
      : LifecycleNode("managed_node", opts) {}

  CallbackReturn on_configure(const rclcpp_lifecycle::State&) override {
    RCLCPP_INFO(get_logger(), "configuring");
    pub_ = create_publisher<std_msgs::msg::String>("topic", 10);
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_activate(const rclcpp_lifecycle::State& state) override {
    LifecycleNode::on_activate(state);   // activates lifecycle publishers
    RCLCPP_INFO(get_logger(), "activating");
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_deactivate(const rclcpp_lifecycle::State& state) override {
    LifecycleNode::on_deactivate(state);
    RCLCPP_INFO(get_logger(), "deactivating");
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_cleanup(const rclcpp_lifecycle::State&) override {
    pub_.reset();
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_shutdown(const rclcpp_lifecycle::State&) override {
    return CallbackReturn::SUCCESS;
  }

private:
  rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::String>::SharedPtr pub_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ManagedNode>();
  rclcpp::spin(node->get_node_base_interface());
  rclcpp::shutdown();
  return 0;
}
```

## Driving Lifecycle Transitions from the CLI

```bash
ros2 lifecycle list /managed_perception              # available transitions
ros2 lifecycle get  /managed_perception              # current state
ros2 lifecycle set  /managed_perception configure
ros2 lifecycle set  /managed_perception activate
ros2 lifecycle set  /managed_perception deactivate
ros2 lifecycle set  /managed_perception shutdown
```

## Lifecycle Client (Programmatic Supervisor)

```cpp
#include <lifecycle_msgs/srv/change_state.hpp>
#include <lifecycle_msgs/msg/transition.hpp>

class LifecycleClient {
public:
  LifecycleClient(rclcpp::Node::SharedPtr node, const std::string& target)
      : node_(node) {
    client_ = node_->create_client<lifecycle_msgs::srv::ChangeState>(
        target + "/change_state");
  }

  bool change(uint8_t transition_id) {
    if (!client_->wait_for_service(std::chrono::seconds(2))) return false;
    auto req = std::make_shared<lifecycle_msgs::srv::ChangeState::Request>();
    req->transition.id = transition_id;
    auto future = client_->async_send_request(req);
    if (rclcpp::spin_until_future_complete(node_, future) !=
        rclcpp::FutureReturnCode::SUCCESS) return false;
    return future.get()->success;
  }

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Client<lifecycle_msgs::srv::ChangeState>::SharedPtr client_;
};

// usage:
client.change(lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE);
client.change(lifecycle_msgs::msg::Transition::TRANSITION_ACTIVATE);
```

## Auto-Configure / Auto-Activate from Launch

See `ros2-launch-config` for the `OnStateTransition` event handler pattern that automatically advances a lifecycle node on startup.

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                          | Fix                                                                                       |
|---------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Allocating in `on_activate`, freeing in `on_deactivate`       | Reactivating after deactivate re-allocates; defeats the configure pattern | Allocate in `on_configure`, free in `on_cleanup`                                          |
| Forgetting `super().on_activate(state)` in Python (or `LifecycleNode::on_activate(state)` in C++) | Lifecycle publishers stay inactive; `publish()` is silently dropped | Always call the base class transition before doing your work                              |
| Returning SUCCESS from a transition that actually failed      | Node ends up in wrong state; downstream supervisors think it's healthy   | Return FAILURE; let the supervisor decide whether to retry or give up                     |
| Doing real work in `on_configure`                             | First reconfigure is slow; resource leaks if configure fails partway     | Configure = setup only; do work after `on_activate`                                       |
| Subscribing in `on_configure`                                 | Subscriptions fire while inactive — undefined behavior                   | Create subs in `on_activate`, destroy in `on_deactivate`                                  |
| No `on_error` handler                                         | One transient failure tears the node down                                 | Implement `on_error` and return SUCCESS to fall back to `unconfigured` for retry          |

## Related Skills

- **ros2-node-creation** — base node patterns; lifecycle adds the state machine
- **ros2-launch-config** — auto-configure/activate via launch event handlers
- **ros2-service-action** — supervisors expose state changes as services
- **robot-bringup** — system-level startup ordering with systemd
