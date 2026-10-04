---
name: ros2-clean-architecture
description: >
  Clean Architecture, Hexagonal Architecture, and Ports and Adapters for ROS2 codebases. Use
  when starting or refactoring a ROS2 package larger than a single node, separating domain
  logic from rclpy, rclcpp, or tf2_ros infrastructure, making robot logic testable without
  spinning ROS, applying dependency inversion, creating adapters, or untangling nodes that mix
  CV, math, state machines, and ROS plumbing.
---

# ROS2 + Clean Architecture

## When to Use This Skill

- Starting a new ROS2 package that will grow beyond one or two nodes
- A node has become a 1000-line file mixing CV math, state machines, and rclpy callbacks
- You can't test your planner/controller/perception logic without `rclpy.init()`
- The team wants to swap simulation and hardware backends without rewriting business code
- Large codebase needs a structure rule that survives team turnover

If your package is one small node and a launch file, this is overkill. Reach for it when complexity has crossed the threshold where wiring and logic have started fusing.

## The Dependency Rule

```
+---------------------------------------------------------+
|                  PRESENTATION LAYER                     |
|        (CLI, dashboards, REST APIs, RViz plugins)       |
+----------------------------+----------------------------+
                             |  depends on
+----------------------------v----------------------------+
|                  APPLICATION LAYER                      |
|         (Use Cases, Application Services)               |
+----------------------------+----------------------------+
                             |  depends on
+----------------------------v----------------------------+
|                    DOMAIN LAYER                         |
|        (Entities, Value Objects, Ports/Interfaces)      |
+----------------------------^----------------------------+
                             |  implements
+----------------------------+----------------------------+
|                INFRASTRUCTURE LAYER                     |
|     (ROS2 adapters, hardware drivers, persistence)      |
+---------------------------------------------------------+
```

**One rule, four corollaries:**

1. Domain depends on **nothing** (no `rclpy`, no `tf2`, no DB, no HTTP).
2. Application depends on Domain only.
3. Infrastructure implements Domain interfaces; Domain knows nothing about Infrastructure.
4. Presentation depends on Application only.

Why bother: the domain layer becomes a pure-Python (or pure-C++) library you can unit-test in 20 ms, swap simulation for hardware by changing one DI wiring, and keep stable across ROS distros.

## Directory Layout

```
my_robot_pkg/
├── package.xml
├── setup.py                      # ament_python (or CMakeLists.txt)
├── my_robot_pkg/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/             # Robot, RobotState, ...
│   │   ├── values/               # Position, Velocity, ...
│   │   ├── interfaces/           # IMotionController, ITransformService, IRobotRepository
│   │   └── use_cases/            # MoveRobotUseCase, NavigateToGoalUseCase
│   ├── application/
│   │   ├── services/             # Application services (orchestrators)
│   │   └── ports/                # Application-level ports (rare)
│   └── infrastructure/
│       ├── ros2/
│       │   ├── nodes/            # ROS2 adapter nodes
│       │   ├── publishers/       # Domain entity → ROS msg
│       │   ├── subscribers/      # ROS msg → Domain entity
│       │   ├── services/         # tf_service.py, etc.
│       │   └── adapters/         # ROS2MotionController : IMotionController
│       └── hardware/             # Direct GPIO/CAN/serial implementations
└── launch/, config/, msg/, test/
```

## Domain Layer (No ROS Imports)

### Entity (has identity)

```python
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class Entity:
    id: UUID = None
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id
    def __hash__(self):
        return hash(self.id)


@dataclass
class Robot(Entity):
    name: str = ''
    max_velocity: float = 1.0
    max_acceleration: float = 0.5
```

```cpp
// domain/entities/robot.hpp — no rclcpp.hpp here
#pragma once
#include <string>

namespace domain::entities {

struct Robot {
  std::string id;
  std::string name;
  double max_velocity{1.0};
  double max_acceleration{0.5};

  bool operator==(const Robot& other) const { return id == other.id; }
};

}  // namespace domain::entities
```

### Value Object (immutable, no identity)

```python
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Position:
    x: float
    y: float
    z: float = 0.0
    def distance_to(self, other: 'Position') -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
```

```cpp
namespace domain::values {

struct Position {
  const double x;
  const double y;
  const double z;
  Position(double x, double y, double z = 0.0) : x(x), y(y), z(z) {}
  double distance_to(const Position& o) const {
    return std::sqrt((x - o.x)*(x - o.x) + (y - o.y)*(y - o.y) + (z - o.z)*(z - o.z));
  }
};

}  // namespace domain::values
```

### Port (interface)

```python
from abc import ABC, abstractmethod
from typing import Optional
from .entities.robot import Robot
from uuid import UUID

class IRobotRepository(ABC):
    @abstractmethod
    def get_by_id(self, robot_id: UUID) -> Optional[Robot]: ...
    @abstractmethod
    def save(self, robot: Robot) -> Robot: ...
```

```cpp
// domain/interfaces/robot_repository.hpp
#pragma once
#include "domain/entities/robot.hpp"
#include <optional>

namespace domain::interfaces {

class IRobotRepository {
public:
  virtual ~IRobotRepository() = default;
  virtual std::optional<entities::Robot> get_by_id(const std::string& id) = 0;
  virtual void save(const entities::Robot& robot) = 0;
};

}  // namespace domain::interfaces
```

## Application Layer

A use case orchestrates domain interactions through ports. It contains the business rule, not the wiring.

```python
class MoveRobotUseCase:
    def __init__(self, motion: IMotionController, transforms: ITransformService):
        self._motion = motion
        self._transforms = transforms

    def execute(self, target: Position) -> bool:
        current = self._transforms.get_transform('map', 'base_link')
        if current is None:
            return False
        # Pure domain logic — distance check, cancellation rules, etc.
        return self._motion.move_to(target)
```

```cpp
namespace application::use_cases {

class MoveRobot {
public:
  MoveRobot(std::shared_ptr<domain::interfaces::IMotionController> motion,
            std::shared_ptr<domain::interfaces::ITransformService> transforms)
      : motion_(std::move(motion)), transforms_(std::move(transforms)) {}

  bool execute(const domain::values::Position& target) {
    auto current = transforms_->get_transform("map", "base_link");
    if (!current) return false;
    return motion_->move_to(target);
  }

private:
  std::shared_ptr<domain::interfaces::IMotionController> motion_;
  std::shared_ptr<domain::interfaces::ITransformService> transforms_;
};

}  // namespace application::use_cases
```

## Infrastructure Layer (ROS2 Adapters)

Adapters implement domain ports against ROS2.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from my_robot_pkg.domain.interfaces import IMotionController
from my_robot_pkg.domain.values.position import Position

class ROS2MotionController(IMotionController):
    def __init__(self, node: Node):
        self._pub = node.create_publisher(Twist, 'cmd_vel', 10)
        self._node = node

    def move_to(self, target: Position) -> bool:
        # Translate domain target into a Twist (or send via action — see ros2-service-action)
        msg = Twist()
        msg.linear.x = target.x   # toy example
        self._pub.publish(msg)
        return True
```

```cpp
class ROS2MotionController : public domain::interfaces::IMotionController {
public:
  explicit ROS2MotionController(rclcpp::Node::SharedPtr node) : node_(node) {
    pub_ = node_->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
  }
  bool move_to(const domain::values::Position& target) override {
    geometry_msgs::msg::Twist msg;
    msg.linear.x = target.x;
    pub_->publish(msg);
    return true;
  }
private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
};
```

The node itself wires use cases to ROS comms. See `ros2-node-creation` for the node pattern; this skill complements it by structuring what lives outside the node.

## Composition Root

One small place — typically `main()` — wires everything together.

```python
def main():
    rclpy.init()
    node = Node('robot_app')

    # Adapters
    motion = ROS2MotionController(node)
    transforms = TFService(node)

    # Use cases
    move = MoveRobotUseCase(motion, transforms)

    # ROS2 entry points (subscribers/services that call use cases)
    bind_subscriptions(node, move)

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

For tests, the same wiring works with fake adapters — no `rclpy.init()` needed for the use case under test.

## Anti-Patterns

```python
# WRONG — domain entity importing rclpy
from rclpy.node import Node    # never in domain/
class Robot:
    def __init__(self, node: Node): ...

# WRONG — business rule in infrastructure
class ROS2MotionController:
    def move_to(self, position):
        if self._battery_level < 20:    # business rule belongs in domain/application
            return False
        ...

# WRONG — use case importing ROS message types
from geometry_msgs.msg import Twist
class MoveRobotUseCase:
    def execute(self, twist: Twist) -> bool: ...   # take a domain Position instead
```

```cpp
// WRONG — domain header pulling in rclcpp
#include <rclcpp/rclcpp.hpp>            // never in domain/
namespace domain::entities {
  class Robot {
    rclcpp::Node::SharedPtr node_;      // domain has no idea ROS exists
  };
}
```

## When NOT to Apply This

- **One node, one job.** A driver wrapping a serial device doesn't need three layers.
- **Throwaway demos.** The structure pays off across months and across team members.
- **Hot research code.** Iteration speed beats architecture in early prototyping.

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                     | Fix                                                                                     |
|---------------------------------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Putting the business rule in the ROS adapter                  | Can't reuse logic for sim or new hardware; not unit-testable        | Move the rule to a use case; adapter only translates                                    |
| Domain entity holds a `Node*` or message type                 | Whole layered structure collapses; dependency rule violated         | Domain owns plain types; infrastructure converts at the boundary                        |
| Passing `geometry_msgs/Twist` into a use case                 | Use case now needs `geometry_msgs` to compile                       | Define a domain `Velocity` value object; convert in the adapter                         |
| 1:1 mapping between every ROS message and a domain entity     | Bookkeeping noise with no benefit                                   | Convert only at the use-case boundary; let internal layers use the same type            |
| Three layers for a 50-line driver                             | Overhead exceeds benefit                                            | Skip Clean Architecture for trivial packages                                            |
| Use cases scheduling timers / publishing                      | Use case becomes a quasi-node; loses test isolation                 | Timers and publishers belong in the adapter; use case is called by the adapter           |

## Related Skills

- **ros2-node-creation** — node skeleton that calls into use cases
- **ros2-messaging** — domain↔message conversion belongs in publishers/subscribers
- **ros2-transforms** — `ITransformService` is the canonical domain port example
- **ros2-testing** — unit-test use cases without `rclpy`; integration-test adapters
- **robotics-design-patterns** — broader patterns (BT, FSM, HAL) that fit inside this skeleton
