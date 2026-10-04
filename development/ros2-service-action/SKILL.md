---
name: ros2-service-action
description: >
  ROS2 services and actions guidance for request-response and long-running cancellable
  operations. Use when choosing between service and action interfaces, defining srv or action
  files, implementing rclpy or rclcpp servers and clients, handling goal acceptance,
  cancellation, feedback, results, structured error codes, lifecycle service calls, service
  deadlocks, or actions stuck executing.
---

# ROS2 Services and Actions

## When to Use This Skill

- Deciding between a service and an action for a new RPC
- Defining a `.srv` or `.action` interface that won't need to change in 6 months
- Implementing a service server / client in Python or C++
- Implementing an action server / client with goal, feedback, result, and cancellation
- Designing structured error codes that clients can act on
- Debugging "service call hangs forever" or "action goal accepted but never executes"

## Service vs. Action: The Decision

| Use a **service** when                                    | Use an **action** when                                                  |
|-----------------------------------------------------------|-------------------------------------------------------------------------|
| The operation completes in well under a second            | The operation takes seconds, minutes, or longer                         |
| There's nothing useful to report mid-flight               | The client wants progress feedback                                      |
| The client never wants to cancel                           | The client may want to cancel (timeout, replan, e-stop)                 |
| Setting/getting state, querying a calibration             | Pick-and-place, navigation, calibration routines, scanning              |

If you're tempted to add a "is_done" service polled in a loop, you wanted an action.

## Defining Interfaces

Put both `.srv` and `.action` files in your `_msgs`/`_interfaces` package (see `ros2-messaging`).

### Service `.srv`

```
# srv/SetMode.srv
uint8 MODE_MANUAL = 0
uint8 MODE_AUTO = 1
uint8 MODE_EMERGENCY = 2
uint8 mode

bool force
---
bool success
string message
uint8 previous_mode
```

The `---` separates request from response. Constants (the `MODE_*` lines) provide enum-like values.

### Action `.action`

```
# action/NavigateToGoal.action
geometry_msgs/PoseStamped target_pose
float32 max_velocity
bool allow_replanning
---
# Result
uint8 ERROR_NONE = 0
uint8 ERROR_OBSTRUCTED = 1
uint8 ERROR_TIMEOUT = 2
uint8 ERROR_INVALID_GOAL = 3
uint8 error_code
string error_message
float32 total_distance
float32 total_time
---
# Feedback
geometry_msgs/PoseStamped current_pose
float32 distance_remaining
float32 estimated_time_remaining
uint8 recovery_count
```

The two `---` separators delimit goal / result / feedback.

### Use enum-style error codes, not raw strings

When an action can fail for multiple reasons, use a numeric `error_code` field with constants. This lets clients branch on failure type, supports localization of error messages, and survives string typos.

```
# Bad — clients have to grep error_message.contains("obstructed")
string error_message
---
# Good — clients can do `if result.error_code == ERROR_OBSTRUCTED: replan()`
uint8 ERROR_NONE = 0
uint8 ERROR_OBSTRUCTED = 1
uint8 error_code
string error_message
```

## Service Server

### Python

```python
import rclpy
from rclpy.node import Node
from robot_interfaces.srv import SetMode

class ModeService(Node):
    def __init__(self):
        super().__init__('mode_service')
        self._mode = SetMode.Request.MODE_MANUAL
        self._srv = self.create_service(
            SetMode, 'robot/set_mode', self._handle)

    def _handle(self, request, response):
        try:
            previous = self._mode
            self._mode = request.mode    # delegate to use case in real code
            response.success = True
            response.message = 'mode set'
            response.previous_mode = previous
        except ValueError as e:
            response.success = False
            response.message = str(e)
        return response
```

### C++

```cpp
#include <rclcpp/rclcpp.hpp>
#include <robot_interfaces/srv/set_mode.hpp>

class ModeService : public rclcpp::Node {
public:
  ModeService() : Node("mode_service") {
    using std::placeholders::_1;
    using std::placeholders::_2;
    srv_ = create_service<robot_interfaces::srv::SetMode>(
        "robot/set_mode",
        std::bind(&ModeService::handle, this, _1, _2));
  }
private:
  void handle(const robot_interfaces::srv::SetMode::Request::SharedPtr req,
              robot_interfaces::srv::SetMode::Response::SharedPtr res) {
    try {
      const auto previous = mode_;
      mode_ = req->mode;
      res->success = true;
      res->message = "mode set";
      res->previous_mode = previous;
    } catch (const std::exception& e) {
      res->success = false;
      res->message = e.what();
    }
  }
  uint8_t mode_ = robot_interfaces::srv::SetMode::Request::MODE_MANUAL;
  rclcpp::Service<robot_interfaces::srv::SetMode>::SharedPtr srv_;
};
```

## Service Client

### Python — call from a separate thread to avoid deadlock

```python
class ModeClient(Node):
    def __init__(self):
        super().__init__('mode_client')
        self._client = self.create_client(SetMode, 'robot/set_mode')
        while not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /robot/set_mode...')

    async def set_mode(self, mode: int) -> bool:
        req = SetMode.Request(); req.mode = mode
        future = self._client.call_async(req)
        result = await future
        return result.success
```

### C++ async client

```cpp
auto client = node->create_client<robot_interfaces::srv::SetMode>("robot/set_mode");
auto request = std::make_shared<robot_interfaces::srv::SetMode::Request>();
request->mode = robot_interfaces::srv::SetMode::Request::MODE_AUTO;

auto future = client->async_send_request(request);
if (rclcpp::spin_until_future_complete(node, future) ==
    rclcpp::FutureReturnCode::SUCCESS) {
  auto response = future.get();
}
```

> **Calling a service from inside a subscription callback?** On `SingleThreadedExecutor` this self-deadlocks: the callback can't return until the service replies, but the executor can't process the reply until the callback returns. Fix: `MultiThreadedExecutor` and put the client in a `ReentrantCallbackGroup`. See `ros2-node-creation`.

## Action Server

### Python — the four callbacks

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from robot_interfaces.action import NavigateToGoal


class NavServer(Node):
    def __init__(self):
        super().__init__('nav_server')
        self._action_server = ActionServer(
            self, NavigateToGoal, 'navigate_to_goal',
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=self._cancel,
            callback_group=ReentrantCallbackGroup(),
        )

    def _goal(self, goal_request):
        if goal_request.max_velocity <= 0.0:
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel(self, goal_handle):
        return CancelResponse.ACCEPT

    async def _execute(self, goal_handle):
        feedback = NavigateToGoal.Feedback()
        result = NavigateToGoal.Result()

        for step in self._plan(goal_handle.request):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.error_code = NavigateToGoal.Result.ERROR_NONE
                result.error_message = 'canceled'
                return result

            self._drive(step)
            feedback.distance_remaining = step.distance_remaining
            feedback.current_pose = step.current_pose
            goal_handle.publish_feedback(feedback)

        goal_handle.succeed()
        result.error_code = NavigateToGoal.Result.ERROR_NONE
        return result
```

### C++

```cpp
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <robot_interfaces/action/navigate_to_goal.hpp>

using NavigateToGoal = robot_interfaces::action::NavigateToGoal;
using GoalHandle = rclcpp_action::ServerGoalHandle<NavigateToGoal>;

class NavServer : public rclcpp::Node {
public:
  NavServer() : Node("nav_server") {
    action_server_ = rclcpp_action::create_server<NavigateToGoal>(
        this, "navigate_to_goal",
        std::bind(&NavServer::handle_goal,    this, std::placeholders::_1, std::placeholders::_2),
        std::bind(&NavServer::handle_cancel,  this, std::placeholders::_1),
        std::bind(&NavServer::handle_accepted,this, std::placeholders::_1));
  }
private:
  rclcpp_action::GoalResponse handle_goal(
      const rclcpp_action::GoalUUID&,
      std::shared_ptr<const NavigateToGoal::Goal> goal) {
    if (goal->max_velocity <= 0.0) return rclcpp_action::GoalResponse::REJECT;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }
  rclcpp_action::CancelResponse handle_cancel(std::shared_ptr<GoalHandle>) {
    return rclcpp_action::CancelResponse::ACCEPT;
  }
  void handle_accepted(std::shared_ptr<GoalHandle> handle) {
    std::thread{std::bind(&NavServer::execute, this, handle)}.detach();
  }
  void execute(std::shared_ptr<GoalHandle> handle) {
    auto feedback = std::make_shared<NavigateToGoal::Feedback>();
    auto result = std::make_shared<NavigateToGoal::Result>();
    // ... step loop with handle->is_canceling() checks ...
    result->error_code = NavigateToGoal::Result::ERROR_NONE;
    handle->succeed(result);
  }
  rclcpp_action::Server<NavigateToGoal>::SharedPtr action_server_;
};
```

## Action Client

```python
from rclpy.action import ActionClient

class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')
        self._client = ActionClient(self, NavigateToGoal, 'navigate_to_goal')

    async def navigate(self, target_pose, on_feedback):
        self._client.wait_for_server()
        goal = NavigateToGoal.Goal()
        goal.target_pose = target_pose
        goal.max_velocity = 0.5
        goal.allow_replanning = True

        send_goal_future = self._client.send_goal_async(
            goal, feedback_callback=lambda fb: on_feedback(fb.feedback))

        goal_handle = await send_goal_future
        if not goal_handle.accepted:
            return None

        result_future = goal_handle.get_result_async()
        wrapped = await result_future
        return wrapped.result
```

```cpp
auto client = rclcpp_action::create_client<NavigateToGoal>(node, "navigate_to_goal");
client->wait_for_action_server();

auto goal_msg = NavigateToGoal::Goal();
goal_msg.target_pose = target;
goal_msg.max_velocity = 0.5;

auto options = rclcpp_action::Client<NavigateToGoal>::SendGoalOptions();
options.feedback_callback =
    [] (rclcpp_action::ClientGoalHandle<NavigateToGoal>::SharedPtr,
       const std::shared_ptr<const NavigateToGoal::Feedback> fb) {
      RCLCPP_INFO(rclcpp::get_logger("nav"), "remaining: %.2f", fb->distance_remaining);
    };
options.result_callback =
    [] (const rclcpp_action::ClientGoalHandle<NavigateToGoal>::WrappedResult& wrapped) {
      // handle wrapped.code (SUCCEEDED, CANCELED, ABORTED) and wrapped.result->error_code
    };
client->async_send_goal(goal_msg, options);
```

## Common Pitfalls

| Pitfall                                                     | What goes wrong                                                                  | Fix                                                                                    |
|-------------------------------------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Using a service for an operation that takes >1s              | Client times out, retries cause duplicate work                                  | Use an action; expose progress + cancel                                                |
| Polling an action's status with a service                   | Race conditions, missed completion                                              | Subscribe to the action's feedback or use `get_result_async`                           |
| Service call from inside a subscription on single-threaded executor | Self-deadlock: callback waits for reply, executor can't deliver it          | MultiThreadedExecutor + `ReentrantCallbackGroup` for the client                        |
| Returning failure as `success=False` only                   | Caller can't distinguish failure types                                          | Add structured `error_code` constants                                                  |
| Action server doing heavy work in `goal_callback`            | New goals reject because previous goal still being validated                    | Validate quickly in `goal_callback`; do work in `execute_callback`                     |
| Forgetting to call `goal_handle.succeed()` / `canceled()` / `abort()` | Action stays in EXECUTING forever; clients hang                            | Every code path through `execute_callback` must terminate the handle                   |
| Spinning the same node from a client and a server          | Deadlock when server replies through the same single-threaded executor          | Put server and client in separate executors or use `ReentrantCallbackGroup`            |

## Related Skills

- **ros2-messaging** — defining the `_msgs` package that holds your `.srv` and `.action` files
- **ros2-node-creation** — executor and callback-group choices for clients and servers
- **ros2-lifecycle** — many lifecycle managers expose state changes as services
- **ros2-testing** — integration-testing servers without spinning a full system
