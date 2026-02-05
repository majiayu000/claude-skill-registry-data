---
name: detector-plugin
description: Create new vision detector plugins following Bob The Skull's detector architecture. Use when adding new detectors like object detection, pose estimation, gesture recognition, or any computer vision detector.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Vision Detector Plugin Creation

Scaffolds new vision detector plugins following the established detector plugin architecture in Bob The Skull.

## When to Use

- Creating new computer vision detectors (object, pose, gesture, etc.)
- Adding detection capabilities to the vision system
- Implementing custom detection algorithms
- Extending the vision processor with new detector types

## Detector Architecture Overview

All detectors in Bob The Skull follow this pattern:

```
vision/detectors/
├── base_detector.py        # Abstract base class
├── face_detector.py         # Example detector
├── motion_detector.py       # Example detector
├── nsfw_detector.py         # Example detector
└── your_new_detector.py     # Your detector here
```

## Base Detector Interface

Every detector must:
1. Extend `BaseDetector` from `base_detector.py`
2. Implement `process_frame(frame, timestamp) -> DetectionResult`
3. Accept `DetectorConfig`, `event_bus`, and detector-specific config in `__init__`
4. Return `DetectionResult` with detection status and data
5. Optionally implement `get_state()` and `update_config()`

## Detector Template

```python
"""
your_detector.py - [Description of detector purpose]

[Brief explanation of what this detector does and when it's useful]
"""

import logging
import time
from typing import Dict, Any, Optional
import numpy as np
import cv2

from vision.detectors.base_detector import BaseDetector, DetectorConfig, DetectionResult
from events import YourDetectionEvent  # Create matching event

logger = logging.getLogger(__name__)


class YourDetector(BaseDetector):
    """
    [Detector name] detection plugin

    [Detailed description of detector behavior]
    """

    def __init__(self, config: DetectorConfig, event_bus, detector_config: Dict[str, Any]):
        """
        Initialize [detector name]

        Args:
            config: Detector configuration
            event_bus: Event bus for publishing detections
            detector_config: Additional detector-specific config
        """
        super().__init__(config, event_bus)

        # Detector-specific config
        self.param1 = detector_config.get('param1', default_value)
        self.param2 = detector_config.get('param2', default_value)

        # Detection state
        self.last_detection = None
        self.detection_active = False

        # Initialize models/algorithms
        # self.model = load_model()

        logger.info(f"YourDetector initialized: param1={self.param1}")

    def process_frame(self, frame, timestamp: float) -> Optional[DetectionResult]:
        """
        Process frame for [detection type]

        Args:
            frame: OpenCV frame (BGR)
            timestamp: Current timestamp

        Returns:
            DetectionResult with detection status
        """
        try:
            # 1. Preprocess frame
            # processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 2. Run detection algorithm
            # detections = self.detect(processed)

            # 3. Calculate confidence/metrics
            confidence = 0.0  # Calculate actual confidence

            # 4. Check if detection exceeds threshold
            detected = confidence >= self.config.min_confidence

            # 5. Handle state changes with stability
            state_changed = False
            activated = False
            deactivated = False

            if detected and not self.detection_active:
                # Detection started
                self.detection_active = True
                state_changed = True
                activated = True

                # Publish detection event
                self.event_bus.publish(YourDetectionEvent(
                    confidence=confidence,
                    detector_id=self.config.detector_id,
                    data={}  # Add detection-specific data
                ))
                logger.info(f"Detection activated: {confidence:.2f}")

            elif not detected and self.detection_active:
                # Detection cleared
                self.detection_active = False
                state_changed = True
                deactivated = True
                logger.info("Detection cleared")

            # 6. Return result
            return DetectionResult(
                detected=self.detection_active,
                confidence=confidence,
                state_changed=state_changed,
                activated=activated,
                deactivated=deactivated,
                data={
                    'confidence': confidence,
                    # Add detector-specific data
                }
            )

        except Exception as e:
            logger.error(f"Error in detection: {e}", exc_info=True)
            return None

    def get_state(self) -> Dict[str, Any]:
        """
        Get current detector state

        Returns:
            Dict with detector state
        """
        return {
            'detector_id': self.config.detector_id,
            'detector_type': self.config.detector_type,
            'detection_active': self.detection_active
        }

    def update_config(self, new_config: Dict[str, Any]):
        """
        Update detector configuration

        Args:
            new_config: New configuration values
        """
        if 'min_confidence' in new_config:
            self.config.min_confidence = new_config['min_confidence']
            logger.info(f"Updated min_confidence to {self.config.min_confidence}")

        if 'param1' in new_config:
            self.param1 = new_config['param1']
            logger.info(f"Updated param1 to {self.param1}")

    def cleanup(self):
        """Cleanup detector resources"""
        logger.info(f"Cleaning up YourDetector {self.config.detector_id}")
        # Release resources (models, connections, etc.)
```

## Registration in vision_processor.py

Add detector creation method:

```python
def _create_your_detector(self, detector_id: str, detector_config: Dict[str, Any]):
    """
    Create a [detector name] from config

    Args:
        detector_id: Unique detector ID
        detector_config: Detector configuration dict
    """
    try:
        from vision.detectors.your_detector import YourDetector

        # Build detector config
        config = DetectorConfig(
            detector_id=detector_id,
            detector_type='your_type',
            name=detector_config.get('name', 'Your Detector'),
            enabled=detector_config.get('enabled', True),
            target_fps=detector_config.get('target_fps', 5.0),
            min_confidence=detector_config.get('min_confidence', 0.5),
            stability_seconds=detector_config.get('stability_seconds', 1.0),
            debounce_seconds=detector_config.get('debounce_seconds', 2.0),
            custom_params=detector_config.get('custom_params', {})
        )

        # Build detector-specific config
        your_config = {
            'param1': detector_config.get('param1',
                                         getattr(self.config, 'YOUR_PARAM1', default)),
            'param2': detector_config.get('param2',
                                         getattr(self.config, 'YOUR_PARAM2', default))
        }

        # Create and register detector
        detector = YourDetector(config, self.event_bus, your_config)
        self.detector_manager.register_detector(detector)

        logger.info(f"Created your detector: {detector_id}")

    except Exception as e:
        logger.error(f"Failed to create detector {detector_id}: {e}", exc_info=True)
```

Add to detector type mapping (around line 113):

```python
detector_creators = {
    'face': self._create_face_detector,
    'motion': self._create_motion_detector,
    'nsfw': self._create_nsfw_detector,
    'your_type': self._create_your_detector,  # Add this
}
```

## Event Definition

Create matching event in `events.py`:

```python
@dataclass
class YourDetectionEvent:
    """Published when [detection type] is detected"""
    confidence: float
    detector_id: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
```

## Configuration in BobConfig.py

Add detector-specific parameters:

```python
# Your Detection (plugin-based)
YOUR_PARAM1: type = default_value  # Description
YOUR_PARAM2: type = default_value  # Description
```

## Example YAML Configuration

```yaml
vision:
  detectors:
    - type: your_type
      detector_id: your_detector_main
      enabled: true
      target_fps: 5.0
      min_confidence: 0.6
      stability_seconds: 1.0
      debounce_seconds: 2.0
      param1: value1
      param2: value2
```

## Common Detector Patterns

### Real-time Detectors (High FPS)
- Motion detection
- Gesture recognition
- Target FPS: 10-15
- Fast algorithms (background subtraction, optical flow)

### Heavy Detectors (Low FPS)
- Face recognition
- Object detection
- Pose estimation
- Target FPS: 2-5
- Deep learning models

### Threshold-based Detectors
- Compare metric against threshold
- Use stability filtering (StableValue pattern)
- Debounce to prevent flapping

### Event-based Detectors
- Publish events on state changes (activated/deactivated)
- Include detection data in events
- State machine can respond to events

## Testing Your Detector

Create test script:

```python
# test_your_detector.py
import cv2
from vision.detectors.your_detector import YourDetector
from vision.detectors.base_detector import DetectorConfig
from local_event_bus import LocalEventBus

event_bus = LocalEventBus()
config = DetectorConfig(
    detector_id='test',
    detector_type='your_type',
    name='Test Detector',
    enabled=True,
    target_fps=5.0,
    min_confidence=0.5,
    stability_seconds=1.0,
    debounce_seconds=2.0
)

detector_config = {
    'param1': value1,
    'param2': value2
}

detector = YourDetector(config, event_bus, detector_config)

# Test with webcam or video
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = detector.process_frame(frame, time.time())
    if result:
        print(f"Detected: {result.detected}, Confidence: {result.confidence:.2f}")

    cv2.imshow('Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Checklist

- [ ] Create detector class extending BaseDetector
- [ ] Implement process_frame() with detection logic
- [ ] Define detector-specific configuration parameters
- [ ] Add detector creation method to vision_processor.py
- [ ] Register detector type in detector_creators mapping
- [ ] Create matching event class in events.py
- [ ] Add config parameters to BobConfig.py (if needed)
- [ ] Test detector independently
- [ ] Test detector integration with vision system
- [ ] Document detector behavior and parameters

## References

**Existing Detectors:**
- `vision/detectors/face_detector.py` - Complex detector with recognition
- `vision/detectors/motion_detector.py` - Simple, fast detector
- `vision/detectors/nsfw_detector.py` - Model-based detector

**Base Classes:**
- `vision/detectors/base_detector.py` - BaseDetector, DetectorConfig, DetectionResult

**Integration:**
- `vision/vision_processor.py` - VisionProcessor class, detector registration
- `vision/detector_manager.py` - DetectorManager class
