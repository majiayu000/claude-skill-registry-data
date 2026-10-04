---
name: ros2-bag
description: >
  ROS2 bag recording and replay guidance for rosbag2 CLI and programmatic capture with
  rosbag2_py or rosbag2_cpp. Use when recording robot data, replaying bags for debugging or
  regression tests, choosing SQLite3 versus MCAP, splitting or compressing long recordings,
  using ros2 bag record, play, info, use_sim_time, clock replay, StorageOptions,
  ConverterOptions, BagWriter, BagReader, or application-level data capture.
---

# ROS2 Bag Recording and Replay

## When to Use This Skill

- Capturing data from a robot run for offline analysis or regression testing
- Replaying a recorded bag into your stack to debug perception or planning
- Choosing the storage backend (SQLite3 default vs. MCAP recommended)
- Recording programmatically inside an application (event-triggered captures)
- Splitting long recordings to keep file size manageable

## CLI: 90% of What You Need

```bash
# Record everything (large; usually a bad default)
ros2 bag record -a

# Record specific topics
ros2 bag record /camera/image_raw /tf /tf_static /odom

# MCAP storage (recommended — better tooling, random access, compression)
ros2 bag record -s mcap /camera/image_raw

# Output directory
ros2 bag record -o my_run /camera/image_raw

# Split into multiple files when each reaches 1 GB
ros2 bag record --max-bag-size 1073741824 -a

# Inspect
ros2 bag info my_run/

# Playback
ros2 bag play my_run/

# Playback with simulated clock (so consumers see the bag's timestamps)
ros2 bag play my_run/ --clock --rate 1.0
```

When playing with `--clock`, every consumer must have `use_sim_time:=true`. See `ros2-launch-config` for propagation.

## Storage Backends: SQLite3 vs. MCAP

| Aspect             | SQLite3 (default)              | MCAP (recommended)                     |
|--------------------|---------------------------------|----------------------------------------|
| Tool ecosystem     | ROS2 only                       | Foxglove, Plotjuggler, Python tooling  |
| Random access      | Limited                         | Indexed, fast                          |
| Compression        | Per-message, weak               | Block-based (zstd, lz4)                |
| Large recordings   | File size grows fast            | More compact                           |
| When to pick       | Quick local recordings          | Anything you'll keep or share          |

```bash
ros2 bag record -s mcap --compression-mode file --compression-format zstd ...
```

## Programmatic Recording: Python (`rosbag2_py`)

```python
import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from rosbag2_py import (
    SequentialWriter, StorageOptions, ConverterOptions, TopicMetadata,
)
from sensor_msgs.msg import Image


class EventRecorder(Node):
    """Start recording when an event arrives; stop on shutdown."""

    def __init__(self):
        super().__init__('event_recorder')
        self._writer: SequentialWriter | None = None
        self.create_subscription(Image, 'camera/image_raw',
                                 self._on_image, 10)
        self.create_service_from_callback()  # service to start/stop

    def start(self, uri: str):
        storage = StorageOptions(uri=uri, storage_id='mcap')
        converter = ConverterOptions(
            input_serialization_format='cdr',
            output_serialization_format='cdr')
        self._writer = SequentialWriter()
        self._writer.open(storage, converter)
        self._writer.create_topic(TopicMetadata(
            name='camera/image_raw',
            type='sensor_msgs/msg/Image',
            serialization_format='cdr'))
        self.get_logger().info(f'recording to {uri}')

    def stop(self):
        self._writer = None    # writer flushes & closes on dtor
        self.get_logger().info('recording stopped')

    def _on_image(self, msg: Image):
        if self._writer is None:
            return
        ts = self.get_clock().now().nanoseconds
        self._writer.write('camera/image_raw', serialize_message(msg), ts)
```

## Programmatic Recording: C++ (`rosbag2_cpp`)

```cpp
#include <rclcpp/rclcpp.hpp>
#include <rosbag2_cpp/writer.hpp>
#include <rosbag2_storage/storage_options.hpp>

class EventRecorder : public rclcpp::Node {
public:
  EventRecorder() : Node("event_recorder") {}

  bool start(const std::string& uri) {
    try {
      writer_ = std::make_unique<rosbag2_cpp::Writer>();
      rosbag2_storage::StorageOptions storage{};
      storage.uri = uri;
      storage.storage_id = "mcap";
      rosbag2_cpp::ConverterOptions conv{};
      conv.input_serialization_format = "cdr";
      conv.output_serialization_format = "cdr";
      writer_->open(storage, conv);
      RCLCPP_INFO(get_logger(), "recording to %s", uri.c_str());
      return true;
    } catch (const std::exception& e) {
      RCLCPP_ERROR(get_logger(), "open bag failed: %s", e.what());
      return false;
    }
  }

  void stop() {
    writer_.reset();   // closes
  }

  template <typename T>
  void write(const std::string& topic, const T& msg) {
    if (!writer_) return;
    writer_->write(msg, topic, now());
  }

private:
  std::unique_ptr<rosbag2_cpp::Writer> writer_;
};
```

## Programmatic Reading

```python
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


def replay(uri: str, on_message):
    reader = SequentialReader()
    reader.open(
        StorageOptions(uri=uri, storage_id='mcap'),
        ConverterOptions(
            input_serialization_format='cdr',
            output_serialization_format='cdr'))

    type_by_topic = {t.name: get_message(t.type)
                     for t in reader.get_all_topics_and_types()}

    while reader.has_next():
        topic, raw, ts = reader.read_next()
        msg = deserialize_message(raw, type_by_topic[topic])
        on_message(topic, msg, ts)
```

```cpp
#include <rosbag2_cpp/reader.hpp>

void replay(const std::string& path) {
  rosbag2_cpp::Reader reader;
  reader.open(path);
  while (reader.has_next()) {
    auto msg = reader.read_next();
    // msg->topic_name, msg->time_stamp, msg->serialized_data
  }
}
```

## Patterns

### Event-Triggered Capture

Run a recorder always-on, but only flush a bounded ring buffer to disk when an event fires (collision detected, anomaly logged). This captures the few seconds *before* the trigger — invaluable for postmortems. Consumers: a `ConditionVariable`-protected ring of serialized messages, drained on event.

### Topic Allow-Lists in Production

Recording everything on a robot wastes disk and may capture sensitive data. Maintain an allow-list per recording mode (developer, qa, production) and load it from YAML.

### Bag Hygiene

- Every recording should be paired with the metadata that produced it: ROS distro, package versions, robot serial, calibration files. Write a sidecar JSON next to the bag.
- For long-running fleets, set up rotation (`--max-bag-size`) and an upload pipeline.

## Common Pitfalls

| Pitfall                                                       | What goes wrong                                                          | Fix                                                                                     |
|---------------------------------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Recording with `-a` on a robot                                | 100 GB/hour, fills the disk                                              | Allow-list the topics you actually need                                                  |
| Replaying without `--clock` and `use_sim_time:=true`          | TF lookups extrapolate into the future, then fail                        | Use `ros2 bag play --clock` and propagate `use_sim_time` everywhere                     |
| Writing serialized messages with the wrong `ts`               | `ros2 bag info` shows wrong duration, replay timing is off                | Use the message's own header stamp, not wall clock, when available                      |
| SQLite3 bag from a long run                                   | File grows past tens of GB; tooling slow                                 | Use MCAP; enable splitting (`--max-bag-size`)                                           |
| Forgetting `create_topic` in `rosbag2_py`                     | First `write()` raises                                                   | Register every topic with `TopicMetadata` before writing                                |
| Capturing `/tf` without `/tf_static`                          | Replays have a broken TF tree                                            | Always include both `/tf` and `/tf_static`                                              |

## Related Skills

- **ros2-messaging** — bag is just serialized messages; QoS doesn't apply on read
- **ros2-launch-config** — `use_sim_time` propagation for replay
- **ros2-transforms** — replay needs both `/tf` and `/tf_static`
- **robotics-testing** — bag-driven regression tests
