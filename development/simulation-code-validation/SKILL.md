---
name: simulation-code-validation
version: 1.0.0
category: robotics-technical
description: Encodes validation patterns for robotics simulation code (ROS 2, Gazebo, Isaac Sim). Ensures code examples are testable, safe, and follow simulation-first pedagogy. Validates Python syntax, ROS 2 patterns, URDF/SDF markup, and troubleshooting completeness.
activation_trigger: "When validating robotics code examples, checking simulation compatibility, or ensuring pedagogical safety in lessons"
---

# Simulation Code Validation Skill

## Skill Identity

You possess deep knowledge of robotics simulation validation, code quality assurance, and pedagogical safety. Use this skill to:

1. **Validate robotics code** against simulation environments (Turtlesim, Gazebo, Isaac Sim, MuJoCo)
2. **Catch common errors** before they reach students (syntax, imports, ROS 2 patterns)
3. **Ensure pedagogical safety** (no forward references, CEFR-appropriate, expected outputs shown)
4. **Validate markup** (URDF/SDF XML for Gazebo, custom message definitions)
5. **Audit troubleshooting completeness** (all common errors documented with solutions)

---

## Core Knowledge: Code Validation Frameworks

### Layer 1: Static Syntax Validation

**Python Validation Checklist**:
- [ ] Valid Python 3.8+ syntax (not Python 2)
- [ ] All imports exist and are correct:
  - `import rclpy` ✅
  - `from rclpy.node import Node` ✅
  - Message imports: `from std_msgs.msg import String` ✅
  - Geometry imports: `from geometry_msgs.msg import Twist` ✅
- [ ] No undefined variables or undefined function references
- [ ] String formatting uses f-strings (modern, readable)
- [ ] Indentation consistent (4 spaces, no tabs)
- [ ] No missing colons or parentheses
- [ ] Main guard: `if __name__ == '__main__':`
- [ ] Type hints present on public methods (optional but recommended)

**PEP 8 Compliance**:
- Line length ≤ 88 characters (Black formatter standard)
- Function names snake_case
- Class names PascalCase
- Constants UPPER_SNAKE_CASE
- 2 blank lines between classes
- 1 blank line between methods

**Example Validation**:
```python
# ❌ BAD - undefined variable
def publisher_callback(self):
    msg = String()
    msg.data = message_text  # 'message_text' not defined

# ✅ GOOD - variable defined
def publisher_callback(self):
    message_text = "Hello"
    msg = String()
    msg.data = message_text
```

---

### Layer 2: ROS 2 Pattern Validation

**Publisher Validation Checklist**:
- [ ] `rclpy.init(args=args)` called exactly ONCE (before node creation)
- [ ] Node has unique, descriptive name: `Node('my_publisher')`
- [ ] Publisher created with 3 params: `create_publisher(MessageType, '/topic/name', queue_size)`
- [ ] Topic name follows convention: starts with `/`, uses lowercase, hyphens or underscores
- [ ] Message type imported correctly: `from X.msg import Y`
- [ ] Timer or callback exists (node must do something)
- [ ] `rclpy.spin(node)` present (without this, callbacks never fire)
- [ ] `rclpy.shutdown()` on exit or in finally block
- [ ] Expected output documented (what should student see?)

**Subscriber Validation Checklist**:
- [ ] `rclpy.init()` called once
- [ ] Subscription created: `create_subscription(MsgType, '/topic', callback, queue_size)`
- [ ] Topic name matches publisher exactly (case-sensitive!)
- [ ] Message type matches publisher exactly
- [ ] Callback function exists with correct signature: `def callback(self, msg):`
- [ ] Message fields accessed correctly (e.g., `msg.data`, `msg.x`)
- [ ] `rclpy.spin()` present
- [ ] Logging present for debugging: `self.get_logger().info()`

**Multi-Node System Validation**:
- [ ] Each node has unique name
- [ ] All topic names consistent across nodes
- [ ] All message types match between pub/sub pairs
- [ ] No circular dependencies (node A waits for B waits for A)
- [ ] Instructions show how to run multiple terminals
- [ ] Expected output shows all nodes running independently
- [ ] `ros2 node list` command shown (proves nodes exist)
- [ ] `ros2 topic list` command shown (proves topics created)

**Common ROS 2 Errors to Catch**:
| Error | Cause | Fix |
|-------|-------|-----|
| `rclpy.init() called twice` | Multiple nodes in same process init twice | Call `rclpy.init()` once, before all nodes |
| Topic not publishing | Publisher not spinning, or topic name wrong | Check topic with `ros2 topic list` |
| Callback never fires | Subscriber not spinning, or message type mismatch | Verify `rclpy.spin()` and types match |
| ModuleNotFoundError: rclpy | ROS 2 not installed | `sudo apt install ros-humble-rclpy` |
| ModuleNotFoundError: geometry_msgs | geometry_msgs not installed | `sudo apt install ros-humble-geometry-msgs` |

---

### Layer 3: Gazebo Simulation Validation

**URDF Syntax Validation**:
- [ ] Valid XML (all tags closed, valid UTF-8)
- [ ] Root element: `<robot name="robot_name">`
- [ ] All links have mass > 0 (or fixed_base in collision)
- [ ] All joints connect valid link pairs (no dangling references)
- [ ] Inertia matrices valid (principal moments satisfy triangle inequality)
- [ ] Visual and collision geometry defined
- [ ] No circular joint chains (unless intentional)

**SDF Syntax Validation (Gazebo 11+)**:
- [ ] Valid XML with `<sdf version="1.9">`
- [ ] Model name specified
- [ ] All links have `<inertial>` blocks
- [ ] Physics engine specified (`<physics type="ode">` or `bullet`)
- [ ] Gravity defined (typically `0 0 -9.81`)

**Gazebo-Specific Errors**:
| Error | Cause | Fix |
|-------|-------|-----|
| Model doesn't appear in Gazebo | Model file not found, or path incorrect | Check path in launch file, verify URDF exists |
| Model falls through ground | Inertia too light or collision undefined | Add mass, define collision geometry |
| Joint doesn't move | Joint limit reached, or controller not connected | Check joint limits, verify Gazebo controller plugin |
| Physics unstable (jittering) | Timestep too large, inertia ratios bad | Reduce step size in physics tag |

---

### Layer 4: Isaac Sim Validation

**Isaac Sim Scene Validation**:
- [ ] USD file format valid (Pixar Universal Scene Description)
- [ ] Physics enabled on rigid bodies
- [ ] Joints have appropriate drive strengths (not too high)
- [ ] Sensors have correct reference frames
- [ ] Cameras have valid intrinsics (focal length, resolution)
- [ ] Lidar scan distance matches expected range

**Common Isaac Sim Issues**:
- Model imports but doesn't appear → Check asset path and load callbacks
- Physics too fast/slow → Adjust substeps and step size in PhysicsScene
- Sensors return wrong data → Verify sensor attachment frames and enable flags
- Synthetic data generation fails → Check camera paths and renderer settings

---

## Pedagogical Safety Validation

### Anti-Forward-Reference Check

**Forward reference** = mentioning a concept not yet taught

**Example Forward Reference** ❌:
> "In Lesson 2, we'll create a publisher node to send motion commands via ROS 2 topics. Next lesson, we'll add machine learning vision processing to detect obstacles."

Problem: Student in Lesson 2 thinks they need to know ML to understand publishers. Breaks confidence.

**Fixed** ✅:
> "In Lesson 2, we'll create a publisher node to send motion commands via ROS 2 topics. Publishers are the foundation for all ROS 2 communication."

Check: Does lesson 2 explain "what is machine learning"? No → Don't mention it.

**Validation Steps**:
1. Extract all concepts mentioned in the code examples
2. Extract all concepts in explanatory text
3. Check against lesson `concepts` in YAML frontmatter
4. Flag any concept not in that lesson or earlier lessons
5. Verify all concept counts stay within CEFR limits

### Expected Output Validation

Every code example MUST have expected output shown.

**Template**:
```python
# Code example
print("Hello, World!")
```

**Expected Output** (REQUIRED):
```
Hello, World!
```

**Validation**:
- [ ] Expected output shown (as code block or screenshot)
- [ ] Output is realistic (not hallucinated)
- [ ] Output was verified (by actually running code)
- [ ] Output shows what student will see (exact terminal output)

---

### Troubleshooting Completeness Audit

**For each code example, audit troubleshooting**:

- [ ] "Command not found" errors documented (if CLI command)
- [ ] Import errors documented (if Python code)
- [ ] Common parameter mistakes documented
- [ ] Timeout/connection issues documented
- [ ] Expected vs actual output comparison provided
- [ ] "Why might this happen?" explained (not just "how to fix")
- [ ] At least 3 common mistakes documented per example

**Example Audit**:
```python
# Lesson code:
ros2 run turtlesim turtlesim_node
```

Troubleshooting audit:
- [ ] "Command not found" → ROS 2 not installed
- [ ] "Could not find executable" → turtlesim package missing
- [ ] Window won't open → Display server issue (SSH without X forwarding)
- [ ] "Connection refused" → ROS_DOMAIN_ID mismatch
```

---

## Code Validation Workflows

### Workflow 1: Validate a Single Code Example

**Input**: Python file or code snippet

**Steps**:
1. **Syntax Check**: Run Python syntax validator
   - `python3 -m py_compile code.py`
   - Catch: missing colons, undefined variables, invalid imports
2. **ROS 2 Pattern Check**: Verify against Layer 2 checklist
   - Node structure valid?
   - Publisher/subscriber patterns correct?
   - Callbacks well-formed?
3. **Runtime Validation**: Mentally trace execution
   - Does `rclpy.init()` happen before node creation?
   - Does `rclpy.spin()` exist?
   - Are message fields accessed correctly?
4. **Output Verification**: Check expected output section exists
   - Is output realistic (tested manually)?
   - Does it match what code would actually produce?
5. **Troubleshooting Audit**: Count error sections
   - Minimum 3 common errors documented?
   - Solutions provided for each?

**Output**: Pass/Fail with list of issues found

---

### Workflow 2: Validate Complete Lesson

**Input**: Lesson markdown file with YAML frontmatter and multiple code examples

**Steps**:
1. **Frontmatter Validation**:
   - [ ] All required YAML fields present
   - [ ] `simulation_required` specified (Turtlesim/Gazebo/Isaac)
   - [ ] `safety_level` appropriate for CEFR level
   - [ ] `cefr_level` specified (A2/B1/C2)
   - [ ] `concepts` list matches content
   - [ ] `learning_objectives` measurable and SMART
2. **Content Structure Validation**:
   - [ ] Only ONE H1 heading (lesson title)
   - [ ] Sections in order: Intro, Prerequisites, Content, Code, Troubleshooting, Self-Assessment, Next
   - [ ] No subsection skipped
3. **Concept Density Check**:
   - Count unique concepts taught
   - A2: should be 5-7 concepts
   - B1: should be 7-10 concepts
   - C2: unlimited
   - Flag if exceeds limit
4. **Forward Reference Check**:
   - [ ] No future lesson concepts mentioned
   - [ ] No advanced topics teased without context
   - [ ] Stays focused on lesson objectives
5. **Code Example Validation**:
   - [ ] Each code example has expected output
   - [ ] Syntax is valid
   - [ ] ROS 2 patterns correct
   - [ ] Copy-pasteable (tested)
6. **Troubleshooting Completeness**:
   - [ ] At least 3 common errors per major code block
   - [ ] Solutions provided
   - [ ] Expected vs actual output comparison
7. **Pedagogical Safety**:
   - [ ] Three Roles framework demonstrated (💬 CoLearning prompts)
   - [ ] No meta-commentary (no "Layer 2" labels visible)
   - [ ] Self-assessment checklist present
   - [ ] Next lesson linked

**Output**: Validation report with pass/fail for each section

---

## Validation Rules by Simulator

### Turtlesim Validation Rules

Turtlesim is **software-only, 2D graphics, no physics simulation**. It runs in a display window.

**Validation**:
- [ ] Code uses only standard ROS 2 messages (std_msgs, geometry_msgs)
- [ ] No physics assumptions (no gravity, friction, inertia)
- [ ] Coordinates are 2D (x, y, theta)
- [ ] Movement commands use `Twist` message type
- [ ] Turtle starting position documented (usually 5.5, 5.5)
- [ ] No collision detection expected
- [ ] Display/graphics required (note for SSH users)

**Common Turtlesim Errors**:
| Error | Cause | Fix |
|-------|-------|-----|
| Turtle doesn't move | Publisher not sending to `/turtle1/cmd_vel` | Check topic name exactly |
| No window appears | Display server not available (SSH) | Use `export DISPLAY=:0` or use X forwarding |
| `ros2 run turtlesim turtlesim_node` fails | turtlesim not installed | `sudo apt install ros-humble-turtlesim` |
| Topic `/turtle1/pose` not available | Turtlesim not running | Launch in separate terminal first |

---

### Gazebo Validation Rules

Gazebo includes **physics simulation, sensors (lidar/camera), complex robot models**.

**Validation**:
- [ ] URDF/SDF file valid XML with correct schema
- [ ] Robot model has defined mass and inertia
- [ ] Collision geometry defined
- [ ] Sensors have correct attachment frames
- [ ] Physics parameters realistic (gravity ~9.81 m/s², timestep 0.001 s)
- [ ] Launch file includes model spawning
- [ ] Joint controllers defined (if joints move)
- [ ] Expected output shows model loading and physics running

**Common Gazebo Errors**:
| Error | Cause | Fix |
|-------|-------|-----|
| Model doesn't appear | URDF parsing error or model file missing | Check `gazebo_ros` plugin, verify file paths |
| Model falls through ground | Collision geometry missing | Add `<collision>` block with valid geometry |
| Joint doesn't move | No controller plugin or joint limits exceeded | Add `gazebo_ros2_control` plugin, check limits |
| Simulation very slow | Timestep too small or physics too complex | Increase `max_step_size` in physics tag |
| Camera/Lidar returns no data | Sensor not attached or plugin missing | Verify sensor frames, add plugin in URDF |

---

### Isaac Sim Validation Rules

Isaac Sim includes **advanced physics, synthetic data generation, ML-ready assets**.

**Validation**:
- [ ] USD asset paths valid (correct directory structure)
- [ ] Physics enabled on rigid bodies
- [ ] Sensor ground truth available (if used for ML)
- [ ] ROS 2 bridge properly configured
- [ ] Synthetic data annotation enabled (if generating datasets)
- [ ] Lighting suitable for vision tasks
- [ ] GPU memory requirements documented

**Common Isaac Sim Errors**:
| Error | Cause | Fix |
|-------|-------|-----|
| Assets don't load | Incorrect USD path or asset not downloaded | Check `NVIDIA_NUCLEUS` path, verify asset exists |
| Physics glitchy | Substeps too low or inertia badly scaled | Increase `number_of_substeps` to 4+ |
| ROS 2 topics not appearing | Isaac ROS 2 bridge not loaded | Load `omni.isaac.ros2_bridge` extension |
| Synthetic data export fails | Annotation layer not set | Enable `omni.syntheticdata` and set annotator labels |

---

## Validation Checklist Template

Use this for auditing any robotics code lesson:

```markdown
## Code Validation Audit

### Python Syntax
- [ ] Valid Python 3.8+ syntax
- [ ] All imports correct and available
- [ ] No undefined variables
- [ ] PEP 8 compliant
- [ ] Main guard present

### ROS 2 Patterns
- [ ] rclpy.init() called exactly once
- [ ] Node has unique name
- [ ] Publishers/subscribers correct
- [ ] Topic names follow conventions
- [ ] Message types match
- [ ] Callbacks well-formed
- [ ] rclpy.spin() present
- [ ] rclpy.shutdown() present

### Simulation Environment
- [ ] Simulator specified (Turtlesim/Gazebo/Isaac)
- [ ] Expected output shown
- [ ] Output verified (not hallucinated)
- [ ] Copy-pasteable code

### Troubleshooting
- [ ] At least 3 common errors documented
- [ ] Solutions provided for each
- [ ] Expected vs actual output comparison
- [ ] Diagnostic commands shown

### Pedagogical Safety
- [ ] No forward references
- [ ] CEFR concept count OK
- [ ] Self-assessment present
- [ ] Three Roles framework shown (💬)
- [ ] Framework stays invisible
- [ ] Next lesson linked
```

---

## Success Criteria

Code validated with this skill must meet:

- [ ] Zero Python syntax errors (verified by linter)
- [ ] Zero ROS 2 pattern violations (all imports, spin(), shutdown() present)
- [ ] All expected outputs documented and realistic
- [ ] Troubleshooting covers 90% of common errors
- [ ] No forward references to future concepts
- [ ] CEFR concept count within limits
- [ ] Copy-pasteable and tested before lesson release
- [ ] Simulator environment explicitly specified
- [ ] Safety checks for autonomous movement
- [ ] Self-assessment checklist included
- [ ] Three Roles framework present but invisible
- [ ] Markdown valid (no broken links, code blocks formatted correctly)

