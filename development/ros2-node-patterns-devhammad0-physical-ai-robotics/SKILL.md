---
name: ros2-node-patterns
version: 1.0.0
category: robotics-technical
description: Encodes ROS 2 best practices for node design, topic naming, publisher/subscriber patterns, and message handling. Used when creating ROS 2 code examples or architectural designs for robotics lessons.
activation_trigger: "When creating ROS 2 code examples, designing node architecture, or explaining ROS 2 patterns"
---

# ROS 2 Node Patterns Skill

## Skill Identity

You possess deep knowledge of ROS 2 node design patterns, best practices, and common pitfalls. Use this skill to:

1. **Generate valid ROS 2 code** that follows Python style guidelines
2. **Explain node architecture patterns** to students
3. **Design topic naming conventions** that scale
4. **Debug common node issues** systematically

---

## Core Knowledge: ROS 2 Node Fundamentals

### Node Structure (Python with rclpy)

**Minimal Publisher Node Template**:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # or other message type

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')

        # Create publisher: (message_type, topic_name, queue_size)
        self.publisher_ = self.create_publisher(String, 'topic_name', 10)

        # Create timer: (callback_period_sec, callback_function)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.counter = 0

    def timer_callback(self):
        # Publish message
        msg = String()
        msg.data = 'Hello World: %d' % self.counter
        self.publisher_.publish(msg)

        # Log for debugging
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()

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

**Key Elements**:
- [ ] `rclpy.init()` before creating node
- [ ] Node inherits from `rclpy.node.Node`
- [ ] `super().__init__(node_name)` sets unique node name
- [ ] `create_publisher(MsgType, topic_name, queue_size)` creates publisher
- [ ] `create_timer(period, callback)` for periodic execution
- [ ] `rclpy.spin(node)` runs the node
- [ ] `rclpy.shutdown()` on exit

**Minimal Subscriber Node Template**:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        # Create subscription: (message_type, topic_name, callback, queue_size)
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10
        )
        self.subscription  # Prevent unused variable warning

    def listener_callback(self, msg):
        # Handle incoming message
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()

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

---

## Topic Naming Conventions

**Pattern**: Use hierarchical, descriptive names with namespacing

**Good Examples**:
- `/robot_name/sensor/lidar` - Clear hierarchy
- `/robot_arm/joint1/state` - Robot + subsystem + specific
- `/camera/rgb/image` - Device + type + data
- `/turtle1/cmd_vel` - Entity + command type (follows ROS convention)

**Poor Examples**:
- `/data` - Too vague
- `/sensor_data_topic` - Redundant "topic" suffix
- `/LIDAR` - Inconsistent naming (should be lowercase)
- `/sensor123_output` - No semantic meaning

**Naming Rules**:
1. Use lowercase with underscores (snake_case)
2. Use forward slashes for hierarchy (`/parent/child/data`)
3. Start with `/` (absolute namespace)
4. Prefer descriptive over short names
5. Include data type hint if helpful (`/imu`, `/lidar`, `/camera`)

---

## Message Type Selection

### Standard Message Types (std_msgs)

**String**: Text data
```python
from std_msgs.msg import String
msg = String(data="Hello")
```

**Int32, Float32, etc.**: Numeric data
```python
from std_msgs.msg import Int32, Float32
msg = Int32(data=42)
```

**Bool**: Boolean
```python
from std_msgs.msg import Bool
msg = Bool(data=True)
```

### Geometry Messages (geometry_msgs)

**Twist**: Velocity (linear + angular)
```python
from geometry_msgs.msg import Twist
msg = Twist()
msg.linear.x = 1.0   # m/s forward
msg.angular.z = 0.5  # rad/s rotation
```

**Point, Quaternion, Pose**: Spatial data
```python
from geometry_msgs.msg import Point, Quaternion, Pose
point = Point(x=1.0, y=2.0, z=3.0)
```

### Sensor Messages (sensor_msgs)

**LaserScan**: Lidar data
```python
from sensor_msgs.msg import LaserScan
```

**Image**: Camera data
```python
from sensor_msgs.msg import Image
```

**Imu**: Inertial measurement
```python
from sensor_msgs.msg import Imu
```

---

## Common Patterns & Anti-Patterns

### Pattern 1: Periodic Publishing (Timer-based)

**When to use**: Sensor readings, heartbeat messages, state broadcasts

```python
# In __init__:
self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

# Callback:
def timer_callback(self):
    msg = SensorData()
    msg.value = self.read_sensor()
    self.publisher_.publish(msg)
```

### Pattern 2: Event-Driven Publishing

**When to use**: Changes detected, user input, system events

```python
def event_handler(self, event):
    if event.is_important:
        msg = EventMessage()
        msg.event_type = event.type
        self.publisher_.publish(msg)
```

### Pattern 3: Request-Reply (Services)

**When to use**: Direct questions/answers (not streaming data)

```python
# Server:
self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_callback)

def add_callback(self, request, response):
    response.sum = request.a + request.b
    return response

# Client:
client = node.create_client(AddTwoInts, 'add_two_ints')
request = AddTwoInts.Request(a=5, b=3)
response = client.call(request)
```

### Anti-Pattern 1: Waiting in Callback

❌ **BAD**:
```python
def callback(self, msg):
    time.sleep(2)  # BLOCKS other callbacks!
    # process data
```

✅ **GOOD**:
```python
def callback(self, msg):
    # Quick processing only
    self.process_data_async(msg)  # Offload to background
```

### Anti-Pattern 2: Blocking I/O in Spin Loop

❌ **BAD**:
```python
while True:
    data = socket.recv()  # Blocks node!
    rclpy.spin_once(node)
```

✅ **GOOD**:
```python
# Use executor with multiple nodes
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

---

## Error Diagnosis Patterns

### Error: "rclpy.init() called twice"

**Cause**: Multiple nodes calling init in same process
**Solution**: Call `rclpy.init()` once, before creating nodes

```python
# main():
rclpy.init()  # Once here
node1 = Node1()
node2 = Node2()
executor = MultiThreadedExecutor()
executor.add_node(node1)
executor.add_node(node2)
executor.spin()
```

### Error: "Topic not publishing"

**Diagnosis steps**:
1. Is publisher node running? `ros2 node list` (should show node)
2. Is topic created? `ros2 topic list` (should show topic)
3. Are messages being sent? `ros2 topic echo /topic_name`
4. Is message type correct? `ros2 topic info /topic_name` (check Type)

### Error: "Subscriber callback never fires"

**Diagnosis**:
1. Is publisher running? (producer must exist)
2. Is subscriber node spinning? (need `rclpy.spin()`)
3. Topic name match exactly? (case-sensitive, `/` matters)
4. Message type match? (Subscriber must use same type as publisher)

### Error: "Node crashes with 'module not found'"

**Cause**: Missing import
**Solution**: Install package and import correctly

```bash
sudo apt install ros-humble-geometry-msgs
```

```python
from geometry_msgs.msg import Twist  # Correct import
```

---

## Code Generation Checklist

When generating ROS 2 code, ensure:

- [ ] `rclpy.init()` called before node creation
- [ ] Node has unique name: `Node('unique_name')`
- [ ] Publisher created with correct type: `create_publisher(Type, '/topic', 10)`
- [ ] Subscriber created with correct callback signature
- [ ] Callbacks are quick (offload slow work)
- [ ] `rclpy.spin()` present (or executor.spin())
- [ ] `rclpy.shutdown()` on exit
- [ ] Topic names use `/namespace/topic` format
- [ ] Message types imported correctly
- [ ] Error handling for missing packages
- [ ] Logging for debugging: `self.get_logger().info()`
- [ ] Expected output documented

---

## Templates for Common Tasks

### Template: Robot Command Node

```python
# Sends motion commands to robot
class RobotCommandNode(Node):
    def __init__(self):
        super().__init__('robot_commands')
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_command(self, linear_x, angular_z):
        cmd = Twist()
        cmd.linear.x = linear_x
        cmd.angular.z = angular_z
        self.cmd_publisher.publish(cmd)
        self.get_logger().info(f'Sent: v={linear_x}, w={angular_z}')
```

### Template: Sensor Reader Node

```python
# Reads from sensor, publishes data
class SensorReaderNode(Node):
    def __init__(self):
        super().__init__('sensor_reader')
        self.data_publisher = self.create_publisher(Float32, '/sensor/value', 10)
        self.timer = self.create_timer(0.1, self.read_sensor)

    def read_sensor(self):
        # Read from actual sensor (or simulation)
        value = self.sensor.read()  # Placeholder
        msg = Float32(data=float(value))
        self.data_publisher.publish(msg)
```

### Template: Data Processor Node

```python
# Reads from topic, processes, publishes result
class ProcessorNode(Node):
    def __init__(self):
        super().__init__('processor')
        self.sub = self.create_subscription(Float32, '/raw_data', self.process, 10)
        self.pub = self.create_publisher(Float32, '/processed_data', 10)

    def process(self, msg):
        # Process data
        processed = msg.data * 2.0  # Example
        result = Float32(data=processed)
        self.pub.publish(result)
```

---

## Learning Activation

When using this skill in lessons:

1. **Show working code first** (student gains confidence)
2. **Explain key lines** (why rclpy.init? why spin?)
3. **Show expected output** (proves it works)
4. **Provide diagnostic commands** (ros2 topic echo, ros2 node list)
5. **Offer common errors** (students anticipate issues)
6. **Include AI CoLearning prompt** ("Ask Claude about message types")

---

## Success Criteria

Code generated with this skill must:

- [ ] Follow PEP 8 Python style
- [ ] Be copy-pasteable (students can run directly)
- [ ] Include expected output (verified)
- [ ] Include error handling (try/except, shutdown)
- [ ] Have clear comments on key ROS 2 APIs
- [ ] Work in specified simulator (Turtlesim, Gazebo, Isaac Sim)
- [ ] Be tested before inclusion in lesson

