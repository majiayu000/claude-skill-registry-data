---
name: sam3-api
description: Use when working with SAM3 (Segment Anything Model 3) - provides API patterns for text prompts, bounding boxes, point prompts, video tracking, batch inference, and model building
---

# SAM3 API Guidance

Use this skill when working with SAM3 (Segment Anything Model 3) from Facebook Research.

**Reference examples** in `references/`:
- `sam3_image_predictor_example.md` - Basic text/box prompts
- `sam3_image_batched_inference.md` - DataPoint batch API
- `sam3_image_interactive.md` - Interactive refinement widget
- `sam3_for_sam1_task_example.md` - SAM1-style point prompts
- `sam3_video_predictor_example.md` - Video tracking with text/point prompts
- `sam3_for_sam2_video_task_example.md` - SAM2-style video tracking API
- `sam3_agent.md` - Using SAM3 with LLMs for complex queries

## Overview

SAM3 is a unified foundation model for promptable segmentation across images and videos. It supports:
- **Text prompts**: Open-vocabulary segmentation ("person", "red car", etc.)
- **Geometric prompts**: Bounding boxes with positive/negative labels
- **Point prompts**: Click-based segmentation (SAM1-style via `predict_inst`)
- **Video tracking**: Track objects across video frames

Repository: https://github.com/facebookresearch/sam3

## Installation

```bash
conda create -n sam3 python=3.12
conda activate sam3
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
git clone https://github.com/facebookresearch/sam3.git
cd sam3
pip install -e .
huggingface-cli login  # Required for model weight downloads
```

## Model Building

### Image Model

```python
from sam3.model_builder import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor

# Build model (downloads weights automatically from HuggingFace)
model = build_sam3_image_model()

# For SAM1-style point prompts, enable instance interactivity
model = build_sam3_image_model(enable_inst_interactivity=True)

# Create processor with confidence threshold
processor = Sam3Processor(model, confidence_threshold=0.5)
```

### Video Model

```python
from sam3.model_builder import build_sam3_video_predictor, build_sam3_video_model

# Multi-GPU video predictor
predictor = build_sam3_video_predictor(gpus_to_use=range(torch.cuda.device_count()))

# SAM2-style tracker
sam3_model = build_sam3_video_model()
tracker = sam3_model.tracker
tracker.backbone = sam3_model.detector.backbone
```

### GPU Configuration

```python
import torch

# Enable TensorFloat32 for Ampere GPUs
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Use bfloat16 for entire session
torch.autocast("cuda", dtype=torch.bfloat16).__enter__()

# Optional: inference mode for no gradients
torch.inference_mode().__enter__()
```

## Image Segmentation API

### Setting an Image

```python
from PIL import Image

image = Image.open("path/to/image.jpg")
inference_state = processor.set_image(image)

# Get image dimensions from state (singular keys for single image)
width = inference_state["original_width"]
height = inference_state["original_height"]
```

### Batch Image Processing

For efficient multi-image inference:

```python
from PIL import Image

images = [Image.open(f"image_{i}.jpg") for i in range(3)]
inference_state = processor.set_image_batch(images)

# Get dimensions (plural keys for batch)
widths = inference_state["original_widths"]   # List[int]
heights = inference_state["original_heights"]  # List[int]

# Apply prompt to all images
inference_state = processor.set_text_prompt(state=inference_state, prompt="person")

# Results are batched - access per image
for i in range(len(images)):
    masks_i = inference_state["masks"][i]
    boxes_i = inference_state["boxes"][i]
    scores_i = inference_state["scores"][i]
```

**Key difference**: Single image uses `original_width`/`original_height`, batch uses `original_widths`/`original_heights` (plural).

### Text Prompts

Text prompts find ALL instances of a concept in the image:

```python
# Reset prompts first (important when switching prompts)
processor.reset_all_prompts(inference_state)

# Set text prompt - triggers inference automatically
inference_state = processor.set_text_prompt(state=inference_state, prompt="shoe")

# Access results
masks = inference_state["masks"]   # Tensor: (N, H, W) boolean masks where N = detected objects
boxes = inference_state["boxes"]   # Tensor: (N, 4) boxes in xyxy pixel format
scores = inference_state["scores"] # Tensor: (N,) confidence scores

# For batch processing, results are lists of tensors:
# masks[i] = (N_i, H, W) for image i
# boxes[i] = (N_i, 4) for image i
# scores[i] = (N_i,) for image i
```

### Geometric Prompts (Bounding Boxes)

Boxes use **normalized cxcywh format** (center_x, center_y, width, height):

```python
from sam3.model.box_ops import box_xywh_to_cxcywh
from sam3.visualization_utils import normalize_bbox

# Convert from pixel xywh to normalized cxcywh
box_xywh = torch.tensor([480.0, 290.0, 110.0, 360.0]).view(-1, 4)
box_cxcywh = box_xywh_to_cxcywh(box_xywh)
norm_box = normalize_bbox(box_cxcywh, width, height).flatten().tolist()

# Add positive box prompt (label=True)
processor.reset_all_prompts(inference_state)
inference_state = processor.add_geometric_prompt(
    state=inference_state,
    box=norm_box,      # [cx, cy, w, h] normalized 0-1
    label=True         # True=positive, False=negative
)
```

### Multi-Box Prompting (Positive + Negative)

```python
# Multiple boxes with different labels
boxes_xywh = [[480.0, 290.0, 110.0, 360.0], [370.0, 280.0, 115.0, 375.0]]
boxes_cxcywh = box_xywh_to_cxcywh(torch.tensor(boxes_xywh).view(-1, 4))
norm_boxes = normalize_bbox(boxes_cxcywh, width, height).tolist()

box_labels = [True, False]  # First positive, second negative

processor.reset_all_prompts(inference_state)
for box, label in zip(norm_boxes, box_labels):
    inference_state = processor.add_geometric_prompt(
        state=inference_state, box=box, label=label
    )
```

### Coordinate Conversion Helper

```python
def convert_xyxy_to_normalized_cxcywh(x0, y0, x1, y1, img_width, img_height):
    """Convert pixel xyxy coordinates to normalized cxcywh format."""
    center_x = (x0 + x1) / 2.0 / img_width
    center_y = (y0 + y1) / 2.0 / img_height
    width = (x1 - x0) / img_width
    height = (y1 - y0) / img_height
    return [center_x, center_y, width, height]
```

### Confidence Threshold

```python
# Adjust threshold dynamically
inference_state = processor.set_confidence_threshold(0.3, inference_state)
```

## SAM1-Style Point Prompts (predict_inst)

For interactive point-based segmentation, use `predict_inst`:

```python
import numpy as np

# Build model with instance interactivity enabled
model = build_sam3_image_model(enable_inst_interactivity=True)
processor = Sam3Processor(model)

# Set image
inference_state = processor.set_image(image)

# Point coordinates in pixel format (x, y)
input_point = np.array([[520, 375]])
input_label = np.array([1])  # 1=positive, 0=negative

# Predict with multiple mask outputs
masks, scores, logits = model.predict_inst(
    inference_state,
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True,  # Returns 3 masks for ambiguous prompts
)

# Sort by score
sorted_ind = np.argsort(scores)[::-1]
masks = masks[sorted_ind]
scores = scores[sorted_ind]
logits = logits[sorted_ind]
```

### Iterative Refinement with Logits

```python
# Use previous logits to refine
mask_input = logits[np.argmax(scores), :, :]

masks, scores, logits = model.predict_inst(
    inference_state,
    point_coords=np.array([[500, 375], [1125, 625]]),
    point_labels=np.array([1, 1]),  # Two positive clicks
    mask_input=mask_input[None, :, :],
    multimask_output=False,  # Single refined mask
)
```

### Box Prompts with predict_inst

```python
input_box = np.array([425, 600, 700, 875])  # xyxy format

masks, scores, _ = model.predict_inst(
    inference_state,
    point_coords=None,
    point_labels=None,
    box=input_box[None, :],
    multimask_output=False,
)
```

### Combined Points and Boxes

```python
input_box = np.array([425, 600, 700, 875])
input_point = np.array([[575, 750]])
input_label = np.array([0])  # Negative point to exclude region

masks, scores, logits = model.predict_inst(
    inference_state,
    point_coords=input_point,
    point_labels=input_label,
    box=input_box,
    multimask_output=False,
)
```

### Batched predict_inst

```python
# Multiple boxes at once
input_boxes = np.array([
    [75, 275, 1725, 850],
    [425, 600, 700, 875],
    [1375, 550, 1650, 800],
])

masks, scores, _ = model.predict_inst(
    inference_state,
    point_coords=None,
    point_labels=None,
    box=input_boxes,
    multimask_output=False,
)
# masks.shape: (batch_size, num_masks, H, W)
```

### predict_inst Tips

- **Multimask output**: `multimask_output=True` returns 3 candidate masks for ambiguous prompts (single point). Use `False` for specific prompts (multiple points, box, or refined) to get a single mask
- **Logit refinement**: Pass previous `logits` to `mask_input` for iterative refinement

## Batched Inference API (DataPoint)

The batched API provides lower-level control for efficient multi-image/multi-query processing. It uses two core data structures:

### Understanding DataPoint

A **DataPoint** is the fundamental unit for batched inference. It bundles an image with one or more queries:

```python
Datapoint(
    images=[...],        # List of images (typically one)
    find_queries=[...],  # List of queries to run on the image(s)
)
```

**Why use DataPoints?**
- **Batching**: Process multiple images in one forward pass
- **Multiple queries per image**: Run several text/box queries on one image efficiently
- **Shared computation**: Image features computed once, reused across all queries

### Understanding FindQueryLoaded

A **FindQueryLoaded** represents a single segmentation query. Each query can be:
- A text prompt (e.g., "cat", "person in red shirt")
- A visual prompt (bounding boxes with positive/negative labels)
- A combination (text hint + visual exemplars)

```python
FindQueryLoaded(
    query_text="cat",              # Text prompt (use "visual" for box-only queries)
    image_id=0,                    # Which image this query applies to
    input_bbox=tensor,             # Optional: box prompts in XYXY pixel format
    input_bbox_label=tensor,       # Optional: True (positive) / False (negative) per box
    inference_metadata=...,        # Required: metadata for postprocessing results
    object_ids_output=[],          # Unused for inference
    is_exhaustive=True,            # Unused for inference
    query_processing_order=0,      # Processing priority
)
```

**InferenceMetadata** tracks original dimensions for proper mask/box rescaling:
```python
InferenceMetadata(
    coco_image_id=1,               # Unique ID for this query (used to retrieve results)
    original_image_id=1,           # Image identifier
    original_category_id=1,        # Category identifier
    original_size=[width, height], # Original image dimensions
    object_id=0,                   # Object identifier
    frame_index=0,                 # Frame index (for video)
)
```

### Creating DataPoints

```python
from sam3.train.data.sam3_image_dataset import InferenceMetadata, FindQueryLoaded, Image as SAMImage, Datapoint
from sam3.train.data.collator import collate_fn_api as collate
from sam3.model.utils.misc import copy_data_to_device

def create_datapoint_with_text(pil_image, text_query):
    """Create a datapoint for text prompt."""
    w, h = pil_image.size
    datapoint = Datapoint(find_queries=[], images=[])
    datapoint.images = [SAMImage(data=pil_image, objects=[], size=[h, w])]
    datapoint.find_queries.append(
        FindQueryLoaded(
            query_text=text_query,
            image_id=0,
            object_ids_output=[],
            is_exhaustive=True,
            query_processing_order=0,
            inference_metadata=InferenceMetadata(
                coco_image_id=1,
                original_image_id=1,
                original_category_id=1,
                original_size=[w, h],
                object_id=0,
                frame_index=0,
            )
        )
    )
    return datapoint

def create_datapoint_with_boxes(pil_image, boxes_xyxy, labels, text_prompt="visual"):
    """Create a datapoint for visual prompt (boxes in XYXY format)."""
    w, h = pil_image.size
    datapoint = Datapoint(find_queries=[], images=[])
    datapoint.images = [SAMImage(data=pil_image, objects=[], size=[h, w])]
    datapoint.find_queries.append(
        FindQueryLoaded(
            query_text=text_prompt,
            image_id=0,
            object_ids_output=[],
            is_exhaustive=True,
            query_processing_order=0,
            input_bbox=torch.tensor(boxes_xyxy, dtype=torch.float).view(-1, 4),
            input_bbox_label=torch.tensor(labels, dtype=torch.bool).view(-1),
            inference_metadata=InferenceMetadata(
                coco_image_id=1,
                original_image_id=1,
                original_category_id=1,
                original_size=[w, h],
                object_id=0,
                frame_index=0,
            )
        )
    )
    return datapoint
```

### Transforms

Transforms preprocess DataPoints before model inference. Import from `sam3.train.transforms.basic_for_api`.

**Essential inference transforms:**

| Transform | Purpose |
|-----------|---------|
| `ComposeAPI` | Chains transforms sequentially |
| `RandomResizeAPI` | Resizes image to model input size |
| `ToTensorAPI` | Converts PIL image → PyTorch tensor |
| `NormalizeAPI` | Normalizes channels + converts coordinates |

**Important**: `NormalizeAPI` automatically converts `input_bbox` from absolute XYXY pixels to normalized CxCyWH format. This is why you provide boxes in XYXY pixel format when creating DataPoints—the transform handles conversion.

```python
from sam3.train.transforms.basic_for_api import ComposeAPI, RandomResizeAPI, ToTensorAPI, NormalizeAPI

# Standard inference transform pipeline
transform = ComposeAPI(
    transforms=[
        RandomResizeAPI(sizes=1008, max_size=1008, square=True, consistent_transform=False),
        ToTensorAPI(),
        NormalizeAPI(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)
```

**Transform parameters:**
- `RandomResizeAPI(sizes, max_size, square, consistent_transform)`: Resize to target size
  - `sizes=1008`: Target size (or list of sizes for random selection during training)
  - `square=True`: Force square output
  - `consistent_transform=False`: For video, apply same resize to all frames if True
- `NormalizeAPI(mean, std)`: Channel normalization (SAM3 uses [0.5, 0.5, 0.5])

**Training/augmentation transforms** (also available in `basic_for_api`):
- `RandomSizeCropAPI`, `CenterCropAPI` - Cropping with object preservation
- `RandomHorizontalFlip`, `RandomAffine` - Geometric augmentation
- `ColorJitter`, `RandomGrayscale` - Color augmentation
- `RandomResizedCrop`, `RandomPadAPI`, `PadToSizeAPI` - Size adjustments
- `RandomMosaicVideoAPI` - Video-specific mosaic augmentation
- `RandomSelectAPI` - Probabilistic transform selection

### Postprocessing

The postprocessor converts raw model outputs to usable masks/boxes at original image resolution:

```python
from sam3.eval.postprocessors import PostProcessImage

postprocessor = PostProcessImage(
    max_dets_per_img=-1,           # -1 = no limit, or topk detections
    iou_type="segm",               # "segm" for masks, "bbox" for boxes only
    use_original_sizes_box=True,   # Rescale boxes to original image size
    use_original_sizes_mask=True,  # Rescale masks to original image size
    convert_mask_to_rle=False,     # False = binary masks, True = RLE format
    detection_threshold=0.5,       # Confidence threshold
    to_cpu=False,                  # Keep on GPU for further processing
)

# Create and transform datapoints
datapoint1 = create_datapoint_with_text(img1, "cat")
datapoint1 = transform(datapoint1)

datapoint2 = create_datapoint_with_boxes(img2, [[59, 144, 76, 163]], [True])
datapoint2 = transform(datapoint2)

# Collate and forward
batch = collate([datapoint1, datapoint2], dict_key="dummy")["dummy"]
batch = copy_data_to_device(batch, torch.device("cuda"), non_blocking=True)
output = model(batch)
results = postprocessor.process_results(output, batch.find_metadatas)
```

## Video Segmentation API

### Video Predictor (Multi-GPU)

```python
from sam3.model_builder import build_sam3_video_predictor

predictor = build_sam3_video_predictor(gpus_to_use=range(torch.cuda.device_count()))

# Start session
response = predictor.handle_request(
    request=dict(type="start_session", resource_path="video.mp4")
)
session_id = response["session_id"]

# Text prompt on frame
response = predictor.handle_request(
    request=dict(
        type="add_prompt",
        session_id=session_id,
        frame_index=0,
        text="person",
    )
)

# Propagate through video
outputs_per_frame = {}
for response in predictor.handle_stream_request(
    request=dict(type="propagate_in_video", session_id=session_id)
):
    outputs_per_frame[response["frame_index"]] = response["outputs"]

# Remove object
predictor.handle_request(
    request=dict(type="remove_object", session_id=session_id, obj_id=2)
)

# Point prompt (relative coordinates 0-1, plain Python lists)
points = [[0.5, 0.5]]  # List[List[float]]
labels = [1]  # List[int]: 1=positive, 0=negative
response = predictor.handle_request(
    request=dict(
        type="add_prompt",
        session_id=session_id,
        frame_index=0,
        points=points,
        point_labels=labels,
        obj_id=2,
    )
)

# Box prompt (xywh format, normalized 0-1)
boxes = [[0.3, 0.2, 0.4, 0.5]]  # List[List[float]]: [x, y, w, h]
box_labels = [1]  # List[int]: 1=positive, 0=negative
response = predictor.handle_request(
    request=dict(
        type="add_prompt",
        session_id=session_id,
        frame_index=0,
        bounding_boxes=boxes,
        bounding_box_labels=box_labels,
    )
)

# Reset and close
predictor.handle_request(dict(type="reset_session", session_id=session_id))
predictor.handle_request(dict(type="close_session", session_id=session_id))
predictor.shutdown()
```

### SAM2-Style Tracker API

```python
from sam3.model_builder import build_sam3_video_model

sam3_model = build_sam3_video_model()
predictor = sam3_model.tracker
predictor.backbone = sam3_model.detector.backbone

# Initialize state
inference_state = predictor.init_state(video_path="video.mp4")

# Add points (relative coordinates)
rel_points = [[x / width, y / height] for x, y in points]
points_tensor = torch.tensor(rel_points, dtype=torch.float32)
labels_tensor = torch.tensor([1], dtype=torch.int32)

_, obj_ids, low_res_masks, video_res_masks = predictor.add_new_points(
    inference_state=inference_state,
    frame_idx=0,
    obj_id=1,
    points=points_tensor,
    labels=labels_tensor,
    clear_old_points=False,
)

# Add box (relative coordinates)
rel_box = [[xmin/width, ymin/height, xmax/width, ymax/height] for xmin, ymin, xmax, ymax in boxes]
rel_box = np.array(rel_box, dtype=np.float32)

_, obj_ids, low_res_masks, video_res_masks = predictor.add_new_points_or_box(
    inference_state=inference_state,
    frame_idx=0,
    obj_id=1,
    box=rel_box,
)

# Propagate
video_segments = {}
for frame_idx, obj_ids, low_res_masks, video_res_masks, obj_scores in predictor.propagate_in_video(
    inference_state,
    start_frame_idx=0,
    max_frame_num_to_track=300,
    reverse=False,
    propagate_preflight=True
):
    video_segments[frame_idx] = {
        obj_id: (video_res_masks[i] > 0.0).cpu().numpy()
        for i, obj_id in enumerate(obj_ids)
    }

# Clear prompts
predictor.clear_all_points_in_video(inference_state)
```

## Key Coordinate Formats

| Context | Format | Range |
|---------|--------|-------|
| `add_geometric_prompt` box | cxcywh | normalized 0-1 |
| `predict_inst` points | xy | pixels |
| `predict_inst` box | xyxy | pixels |
| Batched API `input_bbox` | xyxy | pixels |
| Video Predictor points | xy | normalized 0-1 |
| Video Predictor bounding_boxes | xywh | normalized 0-1 |
| SAM2-Style Tracker points | xy | normalized 0-1 |
| SAM2-Style Tracker box | xyxy | normalized 0-1 |

**Video API comparison:**
- **Video Predictor** (`build_sam3_video_predictor`): Multi-GPU, session-based `handle_request()` API, supports text prompts
- **SAM2-Style Tracker** (`build_sam3_video_model().tracker`): Single-GPU, `add_new_points_or_box()` API , no text prompts, uses tensors

## Important Notes

1. **Reset prompts**: Call `processor.reset_all_prompts(state)` to clear previous results when reusing the same `inference_state` for a new query. Not needed after `set_image()` which returns a fresh state
2. **Inference triggers**: `add_geometric_prompt()` and `set_text_prompt()` automatically run inference
3. **Video sessions**: Each session is tied to one video; close to free GPU memory
4. **Text + geometric prompts**: The `Sam3Processor` API (`set_text_prompt`, `add_geometric_prompt`) does not support combining text and geometric prompts. Use the batched DataPoint API instead, which allows text hints with box prompts via `FindQueryLoaded(query_text="hint", input_bbox=...)`
5. **Negative-only boxes**: Require text prompt hint (use batched API with `query_text`)

## Visualization

```python
from sam3.visualization_utils import (
    plot_results,
    draw_box_on_image,
    normalize_bbox,
    show_mask,
    show_points,
    show_box,
)

# Plot all results from inference state
plot_results(pil_image, inference_state)

# Draw box on image
image_with_box = draw_box_on_image(pil_image, box_xywh)
```
