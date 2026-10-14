---
name: open3d-skill
description: >-
  Open3D 3D data processing — point clouds (filtering, registration, FPFH,
  RANSAC, ICP), mesh operations, TSDF reconstruction, visualization, Open3D-ML,
  RGBD/Kinect/RealSense. Version detection first.
license: Apache-2.0
compatibility: opencode
category: CAD & Hardware Design
---

# Open3D 3D Data Processing

Provenance: extracted from open3d-specialist-subagent. Domain knowledge for point clouds, meshes, visualization, reconstruction, and camera/sensor integration.

## CRITICAL: Version Detection (MANDATORY)

### Version Prompting Rules

You **MUST** determine the user's Open3D version **BEFORE** providing any guidance.

**If the user has NOT specified their Open3D version:**

```
STOP and ask:
"What version of Open3D are you using? You can check with:
  import open3d; print(open3d.__version__)
  # or: pip show open3d

This is required because API availability, function signatures, and module
organization differ significantly between versions. Providing incorrect version
guidance could lead to runtime errors or broken pipelines."
```

**DO NOT proceed with any guidance until the user provides their version.**

### Version Detection Methods

When the user's project files are available, check for version info:
- `import open3d; open3d.__version__`
- `pip show open3d`
- `requirements.txt` or `pyproject.toml` for pinned versions

### Supported Versions

| Version | Release | Key Changes |
|---------|---------|-------------|
| 0.19.0 | 2024-12 | SYCL GPU support, TensorBoard plugin, VoxelBlockGrid |
| 0.18.0 | 2023-11 | Dense SLAM, SLAC optimizer, RGBD video reader |
| 0.17.0 | 2022-08 | Major tensor API overhaul, new rendering pipeline |
| 0.16.0 | 2022-02 | GUI improvements, WebRTC visualizer |
| 0.15.0 | 2021-04 | Open3D-ML TF2 support, new datasets |
| 0.14.0 | 2021-01 | Headless rendering, offscreen renderer |
| 0.13.0 | 2020-06 | New ICP variants, colored ICP |

### Version-Sensitive Areas

These features have significant differences between versions:
- **Tensor API** (`open3d.t` and `open3d.core`) — Major overhaul in 0.17.0+
- **Open3D-ML** (`open3d.ml.torch`, `open3d.ml.tf`) — Dataset/model availability varies by version
- **Rendering** (`open3d.visualization.rendering`) — New pipeline in 0.16.0+
- **Reconstruction System (Tensor)** — New in 0.18.0+
- **SLAM** — Dense SLAM and SLAC optimizer added in 0.18.0+
- **Visualization** — Legacy `draw_geometries` vs. modern `O3DVisualizer` (0.16.0+)

## Core Expertise Areas

### 1. Point Cloud Processing

#### I/O Operations
- Read/write point clouds (PLY, PCD, XYZ, PTS, LAS/LAZ)
- Batch processing of point cloud files
- Point cloud conversion between formats

#### Filtering and Preprocessing
- Statistical outlier removal (`remove_statistical_outlier`)
- Radius outlier removal (`remove_radius_outlier`)
- Voxel downsampling (`voxel_down_sample`)
- Uniform downsampling (`uniform_down_sample`)
- Crop point clouds with bounding boxes or polygons

#### Feature Extraction
- Normal estimation (`estimate_normals`)
- FPFH feature computation (`compute_fpfh_feature`)
- ISS keypoint detection (`detect_keypoints`)
- RANSAC plane/sphere fitting (`segment_plane`)

#### Registration
- Point-to-point ICP (`registration_icp` with `TransformationEstimationPointToPoint`)
- Point-to-plane ICP (`TransformationEstimationPointToPoint`)
- Colored ICP (`colored_icp`)
- Global registration with RANSAC (`registration_ransac_based_on_feature_matching`)
- Multiway registration with pose graph optimization

```python
import open3d as o3d
import numpy as np

source = o3d.io.read_point_cloud("source.ply")
target = o3d.io.read_point_cloud("target.ply")

source.estimate_normals()
target.estimate_normals()

source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    source, o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=100)
)
target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    target, o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=100)
)

result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    source, target, source_fpfh, target_fpfh,
    mutual_filter=True,
    max_correspondence_distance=0.05,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
    ransac_n=3,
    checkers=[
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(0.05),
    ],
    criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999),
)

refined = o3d.pipelines.registration.registration_icp(
    source, target, 0.02, result.transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPlane(),
)
```

### 2. Mesh Operations

#### Mesh I/O and Creation
- Read/write meshes (PLY, OBJ, STL, OFF, glTF)
- Create meshes from point clouds (Poisson, Ball Pivoting, Alpha Shape)
- Primitive mesh creation (box, sphere, cylinder, cone, torus)

#### Mesh Processing
- Mesh simplification (`simplify_quadric_decimation`)
- Mesh subdivision (`subdivide_midpoint`, `subdivide_loop`)
- Mesh smoothing (`smooth_laplacian`)
- Mesh filtering and repair
- Mesh sampling (`sample_points_uniformly`, `sample_points_poisson_disk`)

#### Mesh Analysis
- Compute mesh properties (volume, surface area, bounding box)
- Self-intersection detection
- Mesh watertightness check
- Curvature estimation

```python
import open3d as o3d

mesh = o3d.io.read_triangle_mesh("model.ply")
mesh.compute_vertex_normals()
mesh.compute_triangle_normals()

simplified = mesh.simplify_quadric_decimation(target_number_of_triangles=10000)
smoothed = simplified.smooth_laplacian(number_of_iterations=10)

sampled_points = simplified.sample_points_poisson_disk(number_of_points=5000)
```

#### Surface Reconstruction
- Poisson surface reconstruction (`reconstruct_surface`)
- Ball Pivoting Algorithm (`create_from_point_cloud_ball_pivoting`)
- Alpha Shape reconstruction
- TSDF volume integration

```python
import open3d as o3d

pcd = o3d.io.read_point_cloud("point_cloud.ply")
pcd.estimate_normals()

poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=8, width=0, scale=1.1, linear_fit=False
)

bbox = pcd.get_axis_aligned_bounding_box()
poisson_mesh = poisson_mesh.crop(bbox)
```

### 3. 3D Visualization

#### Interactive Visualization (Legacy)
- `draw_geometries` — Quick visualization of point clouds and meshes
- `draw_geometries_with_custom_animation` — Animated visualization
- `draw_geometries_with_editing` — Interactive editing mode

#### Modern Visualization (0.16.0+)
- `O3DVisualizer` — Modern visualizer with widget support
- `gui` module — Full GUI application framework
- Scene graph with lighting, materials, and post-processing

```python
import open3d as o3d

pcd = o3d.io.read_point_cloud("scene.ply")

vis = o3d.visualization.Visualizer()
vis.create_window(window_name="Point Cloud Viewer", width=1280, height=720)
vis.add_geometry(pcd)
opt = vis.get_render_option()
opt.point_size = 2.0
opt.background_color = np.array([0.1, 0.1, 0.1])
vis.run()
vis.destroy_window()
```

#### Headless Rendering (0.14.0+)
- Offscreen rendering to image buffers
- Batch rendering for automated pipelines

```python
import open3d as o3d

render = o3d.visualization.rendering.OffscreenRenderer(1920, 1080)
render.scene.add_geometry("mesh", mesh, o3d.visualization.rendering.MaterialRecord())
img = render.render_to_image()
img.save("render.png")
```

#### Visualization Best Practices
- Use `O3DVisualizer` for new code (0.16.0+)
- Set appropriate point size for point clouds (2.0+ for sparse, 1.0 for dense)
- Use dark background for better contrast with colored point clouds
- Normalize point clouds before visualization for consistent scale

### 4. Reconstruction

#### TSDF Volume Integration
- Volumetric TSDF integration from RGBD images
- Extract triangle mesh from TSDF volume
- Parameter tuning for volume resolution and truncation distance

```python
import open3d as o3d

volume = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=0.004,
    sdf_trunc=0.04,
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8,
)

for i in range(len(rgbd_images)):
    volume.integrate(rgbd_images[i], extrinsic=poses[i])

mesh = volume.extract_triangle_mesh()
mesh.compute_vertex_normals()
```

#### ICP Registration Pipeline
- Initial coarse alignment with global registration
- Fine alignment with point-to-plane ICP
- Multi-scale ICP for robust convergence

#### Dense SLAM (0.18.0+)
- Tensor-based reconstruction system
- Real-time dense mapping
- Frame-to-model tracking with ICP

### 5. Open3D-ML (Deep Learning)

#### Overview
Open3D-ML provides deep learning models for 3D understanding tasks:
- **Semantic Segmentation** — Point-level and voxel-level classification
- **Object Detection** — 3D bounding box detection from point clouds
- **Frameworks** — PyTorch and TensorFlow support

#### Supported Datasets

| Dataset | Type | Segmentation | Detection |
|---------|------|-------------|-----------|
| KITTI | Outdoor LiDAR | Yes | Yes |
| SemanticKITTI | Outdoor LiDAR | Yes | No |
| NuScenes | Multi-modal | Yes | Yes |
| ScanNet | Indoor RGBD | Yes | Yes |
| S3DIS | Indoor LiDAR | Yes | No |
| Toronto3D | Outdoor LiDAR | Yes | No |
| Waymo | Outdoor LiDAR | Yes | Yes |

#### Training and Inference Pipeline

```python
from open3d.ml import tensors
from open3d.ml.torch.models import PointPillars

model = PointPillars(
    name="PointPillars",
    backbone="resnet",
    num_classes=1,
    voxel_size=0.16,
    point_cloud_range=[0, -39.68, -3, 69.12, 39.68, 1],
)

point_cloud = tensors.PointCloud(points=points, point_features=features)
result = model(point_cloud)
```

#### Open3D-ML Best Practices
- Check framework compatibility (PyTorch vs TensorFlow) per version
- Pre-trained models reduce training time significantly
- Dataset-specific preprocessing is critical for accuracy
- Open3D-ML API stability varies between versions — verify imports

### 6. Camera and Sensors

#### Camera Models
- Pinhole camera parameters (`open3d.camera.PinholeCameraIntrinsic`)
- Fisheye camera model (0.16.0+)
- Camera trajectory processing and visualization

#### RGBD Image Processing
- Create RGBD images from color + depth pairs
- RGBD odometry (`compute_odometry`)
- RGBD to point cloud conversion (`create_point_cloud_from_rgbd_image`)

```python
import open3d as o3d

color_raw = o3d.io.read_image("color.png")
depth_raw = o3d.io.read_image("depth.png")

rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    color_raw, depth_raw,
    depth_scale=1000.0,
    depth_trunc=3.0,
    convert_rgb_to_intensity=False,
)

camera = o3d.camera.PinholeCameraIntrinsic(
    o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
)

pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
    rgbd_image, camera
)
```

#### Sensor Integration
- Azure Kinect (`open3d.io.AzureKinectRecorder`, `AzureKinectSensor`)
- Intel RealSense integration
- LIVOX LiDAR support (0.17.0+)
- TUM RGB-D dataset loader
## Performance Best Practices

### Memory Management
- Use voxel downsampling early to reduce memory usage
- Process large point clouds in tiles or chunks
- Use `numpy` arrays directly when possible for batch operations
- Release geometries with `del` when no longer needed

### GPU Acceleration
- Tensor API (`open3d.t`) leverages CUDA for GPU operations (0.17.0+)
- SYCL support available for Intel GPUs (0.19.0+)
- Open3D-ML training benefits significantly from GPU

### Batch Processing
- Use `open3d.t.geometry.PointCloud` for batch operations on tensors
- Vectorize operations with `open3d.core.Tensor` instead of Python loops
- Pre-allocate buffers for large-scale processing pipelines
## Project Structure Guidance

Recommended structure for Open3D projects:

```
my-open3d-project/
├── data/
│   ├── raw/           # Original point clouds, meshes
│   ├── processed/     # Filtered, downsampled data
│   └── output/        # Results, rendered images
├── src/
│   ├── io.py          # Data loading and saving utilities
│   ├── preprocess.py  # Filtering, downsampling, normalization
│   ├── registration.py # ICP and global registration
│   ├── reconstruction.py # TSDF, Poisson, etc.
│   └── visualization.py  # Rendering and viewer utilities
├── configs/
│   └── params.yaml    # Pipeline parameters
├── notebooks/         # Jupyter notebooks for exploration
├── requirements.txt
└── README.md
```
## Workflow Templates

### Point Cloud Registration Pipeline

```
1. Load source and target point clouds
2. Estimate normals for both clouds
3. Compute FPFH features
4. Run RANSAC-based global registration
5. Refine with point-to-plane ICP
6. Merge point clouds using unified transformation
7. Downsample merged result
8. Optional: run Poisson reconstruction for mesh output
```

### 3D Reconstruction from RGBD

```
1. Load RGBD image sequence and camera intrinsics
2. Create TSDF volume with appropriate voxel size
3. Compute camera poses (odometry or provided)
4. Integrate each RGBD frame into TSDF volume
5. Extract triangle mesh from TSDF
6. Clean up mesh (remove small components, smooth)
7. Export mesh (PLY, OBJ)
8. Visualize and validate result
```

### Open3D-ML Inference Pipeline

```
1. Install Open3D-ML with correct framework (PyTorch or TF)
2. Download pre-trained model weights
3. Load point cloud data in required format
4. Preprocess (normalize, crop, voxelization)
5. Run inference
6. Post-process results (NMS, filtering)
7. Visualize predictions on point cloud
```
## Documentation References

- Open3D Documentation: https://www.open3d.org/docs/release/
- Open3D Python API: https://www.open3d.org/docs/release/python_api/
- Open3D Tutorials: https://www.open3d.org/docs/release/tutorial/
- Open3D GitHub: https://github.com/isl-org/Open3D
- Open3D-ML: https://github.com/isl-org/Open3D-ML
- Open3D Examples: https://www.open3d.org/docs/release/python/examples.html
