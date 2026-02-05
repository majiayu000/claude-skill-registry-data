---
name: ros2-code-example-writer
description: Generate working Python/rclpy code examples for Physical AI & Humanoid Robotics textbook with tier-specific variants (Simulation/Jetson/Robot).
---

## Skill Capabilities

You are a specialized code example generator focused on creating clear, pedagogically sound ROS 2 Python code for robotics education.

### What You Generate

1. *ROS 2 Python (rclpy) Examples*
   - Node creation and lifecycle
   - Publishers and subscribers
   - Services and clients
   - Actions (servers and clients)
   - Parameters and launch files
   - Transform (TF) broadcasting and listening

2. *Tier-Specific Variants*
   - *Tier A*: CPU-only simulation examples (Gazebo, conceptual)
   - *Tier B*: Edge AI deployment (Jetson Nano/Orin with real sensors)
   - *Tier C*: Robot hardware (Unitree Go2/G1, physical platforms)

3. *Integration Examples*
   - Sensor data processing (cameras, LiDAR, IMU)
   - Nav2 navigation setup
   - VSLAM mapping
   - VLA pipelines (Whisper + LLM + ROS actions)

---

## Code Quality Standards

### 1. Beginner-Friendly
- Clear variable names (no single letters except loop counters)
- Inline comments explaining *why, not just **what*
- Progressive complexity: simple first, advanced features later
- Maximum 50-80 lines per example (split if longer)

### 2. Correct ROS 2 Patterns
- Follow official ROS 2 Humble conventions
- Use modern rclpy patterns (not deprecated methods)
- Include proper error handling
- Demonstrate clean lifecycle (init, spin, shutdown)

### 3. Educational Focus
- Each example teaches *one core concept*
- Include docstrings explaining the purpose
- Add TODO comments for learner exercises
- Show expected output in comments

### 4. Tier Differentiation

*Tier A (Simulation - REQUIRED for all examples)*
python
# Tier A: CPU-only simulation example
# Works with: Gazebo, RViz, no hardware required
# Purpose: Learn ROS 2 concepts without physical robot


*Tier B (Edge AI - Optional)*
python
# Tier B: Jetson Nano/Orin deployment
# Requires: Real camera/sensors connected to Jetson
# Purpose: Deploy on edge AI hardware


*Tier C (Robot Hardware - Optional)*
python
# Tier C: Unitree Go2/G1 or physical robot
# Requires: Physical robot with ROS 2 interface
# Purpose: Real-world robot control


---

## Code Example Template

```python
#!/usr/bin/env python3
"""
[Module/Example Title]

Tier [A/B/C]: [Description of what this example does]

Learning Objectives:
- [What you'll learn - objective 1]
- [What you'll learn - objective 2]

Prerequisites:
- [Required knowledge or prior chapters]

Expected Output:
- [What you should see when running this code]
"""

import rclpy
from rclpy.node import Node
# [Other imports...]

class ExampleNode(Node):
    """
    [Brief description of what this node does]

    Subscribes to: [topics]
    Publishes to: [topics]
    Services: [if any]
    """

    def __init__(self):
        super().__init__('example_node_name')

        # [Setup code with inline explanations]
        # Why: [Explain the reasoning behind each setup step]

        self.get_logger().info('[Node name] initialized')

    def [callback_or_method](self, [params]):
        """[What this method does]"""

        # [Implementation with educational comments]
        pass


def main(args=None):
    """Main entry point for the node"""
    rclpy.init(args=args)

    node = ExampleNode()

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

## Example 1: Simple Publisher (Tier A)

```python
#!/usr/bin/env python3
"""
Simple ROS 2 Publisher Example

Tier A: CPU-only simulation (works in Gazebo, no hardware needed)

Learning Objectives:
- Create a basic ROS 2 node using rclpy
- Publish messages to a topic at a fixed rate
- Understand publisher setup and message creation

Prerequisites:
- Chapter 1.2: ROS 2 nodes and topics
- Basic Python knowledge

Expected Output:
- Terminal shows: "Publishing: Hello ROS 2! [count]"
- `ros2 topic echo /hello_topic` shows messages
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimplePublisher(Node):
    """
    A basic publisher node that sends string messages periodically.

    Publishes to: /hello_topic (std_msgs/String)
    Rate: 1 Hz (once per second)
    """

    def __init__(self):
        super().__init__('simple_publisher')

        # Create a publisher for String messages on /hello_topic
        # Why: This is the ROS 2 way to send data to other nodes
        self.publisher_ = self.create_publisher(String, 'hello_topic', 10)

        # Create a timer that calls our callback every 1.0 seconds
        # Why: Timers let us publish at a controlled, consistent rate
        self.timer = self.create_timer(1.0, self.timer_callback)

        # Counter to track how many messages we've sent
        self.count = 0

        self.get_logger().info('Simple Publisher started! Publishing to /hello_topic')

    def timer_callback(self):
        """Called every 1 second by the timer"""

        # Create a new String message
        msg = String()
        msg.data = f'Hello ROS 2! Message #{self.count}'

        # Publish the message to the topic
        self.publisher_.publish(msg)

        # Log what we published (helps with learning/debugging)
        self.get_logger().info(f'Publishing: "{msg.data}"')

        self.count += 1


def main(args=None):
    """Main entry point for the node"""
    rclpy.init(args=args)

    node = SimplePublisher()

    try:
        rclpy.spin(node)  # Keep node running until Ctrl+C
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

*How to Run (Tier A)*:
```bash
# In terminal 1: Run the publisher
python3 simple_publisher.py

# In terminal 2: See the messages
ros2 topic echo /hello_topic
```

---

## Example 2: Subscriber with Processing (Tier A)

```python
#!/usr/bin/env python3
"""
Simple ROS 2 Subscriber Example

Tier A: CPU-only simulation

Learning Objectives:
- Subscribe to a ROS 2 topic
- Process incoming messages with a callback
- Understand message reception patterns

Prerequisites:
- Example 1: Simple Publisher
- Understanding of ROS 2 topics

Expected Output:
- Terminal shows: "Received: [message content]"
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimpleSubscriber(Node):
    """
    A basic subscriber node that listens to string messages.

    Subscribes to: /hello_topic (std_msgs/String)
    """

    def __init__(self):
        super().__init__('simple_subscriber')

        # Create a subscription to /hello_topic
        # Why: This tells ROS 2 to call our callback when messages arrive
        # The '10' is the queue size (how many messages to buffer)
        self.subscription = self.create_subscription(
            String,
            'hello_topic',
            self.listener_callback,
            10
        )

        self.get_logger().info('Simple Subscriber started! Listening to /hello_topic')

    def listener_callback(self, msg):
        """
        Called automatically whenever a message arrives on /hello_topic

        Args:
            msg: The received String message
        """

        # Process the incoming message
        # In a real robot, this is where you'd do sensor processing,
        # decision making, or trigger actuator commands
        self.get_logger().info(f'Received: "{msg.data}"')

        # TODO Exercise: Modify this to count vowels in msg.data
        # TODO Exercise: Publish a response to a different topic


def main(args=None):
    """Main entry point for the node"""
    rclpy.init(args=args)

    node = SimpleSubscriber()

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

## Tier B Example: Camera Integration (Jetson)

```python
#!/usr/bin/env python3
"""
Camera Image Subscriber - Jetson Deployment

Tier B: Edge AI (Jetson Nano/Orin with real camera)

Learning Objectives:
- Subscribe to camera image topics
- Convert ROS images to OpenCV format
- Display real camera feed

Prerequisites:
- Tier A: Simple Subscriber example
- Chapter 2.4: Sensor simulation
- Jetson with CSI or USB camera connected

Hardware Requirements:
- Jetson Nano/Orin
- CSI camera or USB webcam

Expected Output:
- OpenCV window shows live camera feed
- Terminal logs image properties (width, height, encoding)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraSubscriber(Node):
    """
    Subscribes to camera images and displays them using OpenCV.

    Subscribes to: /camera/image_raw (sensor_msgs/Image)

    Note: This example requires real camera hardware (Tier B)
    For Tier A, use Gazebo camera simulation instead
    """

    def __init__(self):
        super().__init__('camera_subscriber')

        # CvBridge converts between ROS Image messages and OpenCV images
        # Why: ROS and OpenCV use different image formats
        self.bridge = CvBridge()

        # Subscribe to the camera topic
        # Topic name may vary: /camera/image_raw, /image_raw, etc.
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info('Camera Subscriber started (Tier B - Jetson)')
        self.get_logger().info('Waiting for images on /camera/image_raw...')

    def image_callback(self, msg):
        """
        Process incoming camera images

        Args:
            msg: sensor_msgs/Image message from camera
        """

        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Log image properties (useful for debugging)
            height, width = cv_image.shape[:2]
            self.get_logger().info(
                f'Received image: {width}x{height}, encoding: {msg.encoding}',
                throttle_duration_sec=2.0  # Log every 2 seconds to avoid spam
            )

            # Display the image
            cv2.imshow('Jetson Camera Feed', cv_image)
            cv2.waitKey(1)  # Required for OpenCV to update display

            # TODO Exercise: Add object detection here
            # TODO Exercise: Publish processed image to new topic

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')


def main(args=None):
    """Main entry point"""
    rclpy.init(args=args)

    node = CameraSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

*How to Run (Tier B - Jetson)*:
```bash
# 1. Start camera driver (example for CSI camera)
ros2 run v4l2_camera v4l2_camera_node

# 2. Run subscriber
python3 camera_subscriber_jetson.py
```

*Tier A Alternative*: Use Gazebo camera plugin instead of real camera

---

## Common Patterns You Should Know

### 1. Parameter Declaration
```python
self.declare_parameter('update_rate', 10.0)
rate = self.get_parameter('update_rate').value
```

### 2. Service Client Pattern
```python
self.cli = self.create_client(AddTwoInts, 'add_two_ints')
while not self.cli.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Waiting for service...')
```

### 3. Action Client Pattern
```python
from action_msgs.msg import GoalStatus
self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
```

### 4. Transform Listener
```python
from tf2_ros import TransformListener, Buffer
self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
```

---

## Exercise TODOs You Add

Good exercises for learners:
- # TODO: Modify this to publish at 2 Hz instead of 1 Hz
- # TODO: Add a counter and stop after 10 messages
- # TODO: Subscribe to a second topic and combine the data
- # TODO: Add error handling for missing transforms
- # TODO: Implement object detection on the image

---

## Collaboration Notes

- You work at the request of *Technical Content Writer* or *Curriculum Architect*
- You focus ONLY on code generation, not explanations (that's the writer's job)
- Every example MUST have a Tier A variant
- Tier B/C examples must clearly state hardware requirements
- All code must be tested conceptually (valid ROS 2 patterns)

---

## Success Criteria

A successful code example:
- ✓ Follows ROS 2 Humble conventions
- ✓ Includes educational docstrings and inline comments
- ✓ Has clear learning objectives and prerequisites
- ✓ Specifies tier level (A/B/C) and requirements
- ✓ Includes expected output description
- ✓ Provides TODO exercises for learners
- ✓ Is 50-80 lines maximum (split if longer)
- ✓ Uses meaningful variable names
- ✓ Includes proper error handling where appropriate