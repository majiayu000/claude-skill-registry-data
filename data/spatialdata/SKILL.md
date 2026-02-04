---
name: spatialdata
description: SpatialData framework for handling spatial multi-modal and multi-scale data. Use this skill for questions about spatial omics data analysis, visualization, and the SpatialData Python ecosystem.
---

# SpatialData Skill

Comprehensive assistance with SpatialData development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

**Data Analysis & Visualization:**
- Working with spatial omics data (images, labels, points, shapes)
- Analyzing multi-modal spatial datasets (transcriptomics, proteomics)
- Visualizing spatial data with napari or spatialdata-plot
- Performing spatial queries and data aggregation

**Framework Implementation:**
- Building spatial data pipelines with SpatialData objects
- Implementing coordinate transformations and spatial indexing
- Working with OME-NGFF/Zarr format storage
- Creating annotation tables with AnnData

**Technical Operations:**
- Loading/saving spatial data in various formats
- Querying spatial elements by regions of interest
- Performing SQL-like joins between spatial elements and tables
- Managing multi-scale image pyramids and chunked storage

**Ecosystem Integration:**
- Using spatialdata-io for technology-specific readers
- Integrating with napari-spatialdata for interactive visualization
- Working with spatialdata-plot for static plotting
- Processing data from technologies like Visium, Stereo-seq, MERFISH

## Key Concepts

### Core SpatialData Elements
- **Images**: Multi-dimensional arrays with channels (c), spatial dimensions (y, x, z), and coordinate transformations
- **Labels**: Segmentation masks as integer arrays where each value represents a spatial region/instance
- **Points**: Coordinate data for transcript locations, point clouds, or single-molecule data
- **Shapes**: Geometric regions (circles, polygons, multipolygons) for areas of interest
- **Tables**: AnnData objects storing annotations that can be linked to spatial elements

### Essential Terminology
- **Coordinate Systems**: Reference frames for spatial alignment and transformations
- **Spatial Elements**: Building blocks (images, labels, points, shapes) with metadata
- **OME-NGFF**: Open Microscopy Environment Next-Generation File Format specification
- **Zarr**: Chunked storage format for large multi-dimensional arrays
- **Regions of Interest (ROIs)**: Specific spatial subsets for analysis
- **Multi-scale**: Pyramidal image representations at different resolutions

### Data Relationships
- Tables can annotate spatial elements but not other tables
- Images cannot be directly annotated by tables (no index)
- Spatial elements require coordinate systems and transformations
- Labels and Shapes are both types of "Regions"

## Quick Reference

### Basic Data Operations

**1. Load and explore sample dataset**
```python
from spatialdata.datasets import blobs
sdata = blobs()
print(sdata)
# Shows all elements: images, labels, points, shapes, tables
```

**2. Access element instances and properties**
```python
# Get unique label instances
from spatialdata import get_element_instances
instances = get_element_instances(sdata["blobs_multiscale_labels"])

# Get image channels
from spatialdata.models import get_channels
channels = get_channels(sdata["blobs_multiscale_image"])
```

**3. Work with coordinate transformations**
```python
# Set image channels
from spatialdata.models import Image2DModel
sdata["blobs_image"] = Image2DModel.parse(
    sdata["blobs_image"],
    c_coords=["r", "g", "b"]
)
```

### Annotation and Table Operations

**4. Retrieve annotation values from elements**
```python
from spatialdata import get_values

# Get values from points element
genes = get_values(value_key="genes", element=sdata["blobs_points"])

# Get values from table annotations
channel_values = get_values(
    value_key="channel_0_sum",
    sdata=sdata,
    element_name="blobs_labels",
    table_name="table"
)
```

**5. Create and manage annotation tables**
```python
from anndata import AnnData
from spatialdata.models import TableModel

# Create table without spatial annotation
codebook_table = AnnData(obs={
    "Gene": ["Gene1", "Gene2", "Gene3"],
    "barcode": ["03210", "23013", "30121"]
})
sdata["codebook"] = TableModel.parse(codebook_table)

# Create table annotating multiple elements
table = TableModel.parse(
    adata,
    region=["blobs_polygons", "blobs_points"],
    region_key="region",
    instance_key="instance_id"
)
```

### Spatial Queries and Operations

**6. Query data by spatial regions**
```python
from spatialdata import bounding_box_query, polygon_query

# Bounding box query
result = sdata.query.bounding_box(
    axes=("y", "x"),
    min_coordinate=[100, 100],
    max_coordinate=[200, 200],
    target_coordinate_system="global"
)

# Polygon query
from shapely.geometry import Polygon
polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
result = sdata.query.polygon(polygon, target_coordinate_system="global")
```

**7. Join spatial elements with tables**
```python
from spatialdata import join_spatialelement_table

# SQL-like join between elements and annotation tables
element_dict, filtered_table = join_spatialelement_table(
    sdata=sdata,
    spatial_element_names="blobs_polygons",
    table_name="annotations",
    how="left",
    match_rows="left"
)
```

### Data Model Validation

**8. Parse and validate different data types**
```python
from spatialdata.models import (
    Image2DModel, Labels2DModel,
    PointsModel, ShapesModel
)

# Parse and validate 2D image
image = Image2DModel.parse(
    data=numpy_array,
    c_coords=["channel1", "channel2"],
    transformations={"global": Identity()}
)

# Parse points from DataFrame
points = PointsModel.parse(
    data=dataframe,
    coordinates={"x": "x_col", "y": "y_col"},
    feature_key="gene_id"
)

# Parse shapes from GeoDataFrame
shapes = ShapesModel.parse(geodataframe)
```

## Reference Files

### **getting_started.md**
**Content:** Installation guide and basic setup
- **Use for:** First-time installation, dependency management
- **Key sections:** PyPI/conda installation, ecosystem packages (spatialdata-io, spatialdata-plot, napari-spatialdata), Docker setup
- **Examples:** Installation commands for different environments

### **api.md** (26 pages)
**Content:** Comprehensive API documentation
- **Use for:** Detailed function and class references
- **Key sections:**
  - **Models**: Image2DModel, Image3DModel, Labels2DModel, Labels3DModel, PointsModel, ShapesModel, TableModel
  - **Operations**: Spatial queries, bounding box operations, polygon queries
  - **Transformations**: Coordinate systems and transformations
  - **Utils**: Helper functions for data manipulation
- **Examples:** Function signatures and usage patterns

### **advanced.md** (4 pages)
**Content:** Design document and advanced concepts
- **Use for:** Understanding framework architecture, design decisions
- **Key sections:** Goals and non-goals, element types, OME-NGFF compliance, coordinate systems
- **Examples:** Technical specifications and implementation details

### **io.md** (1 page)
**Content:** Glossary and terminology
- **Use for:** Understanding spatial data terminology
- **Key sections:** Definitions of NGFF, OME, Zarr, ROI, spatial elements, vector/raster data
- **Examples:** Clear explanations of technical terms

### **other.md** (6 pages)
**Content:** General information and links
- **Use for:** Project overview, citation information, ecosystem links
- **Key sections:** Main project description, related packages, contributing guidelines
- **Examples:** Links to documentation and resources

## Working with This Skill

### For Beginners

1. **Start with getting_started.md** to install SpatialData and dependencies
2. **Use the Quick Reference examples** to understand basic operations
3. **Practice with the blobs dataset** - it contains examples of all element types
4. **Learn the terminology** from io.md glossary

**Beginner workflow:**
```python
# 1. Install and load
pip install spatialdata
from spatialdata.datasets import blobs

# 2. Explore the data structure
sdata = blobs()
print(sdata)

# 3. Access specific elements
points = sdata["blobs_points"]
labels = sdata["blobs_labels"]

# 4. Basic operations
from spatialdata import get_values
values = get_values("genes", element=points)
```

### For Intermediate Users

1. **Study api.md** for detailed function references
2. **Learn spatial queries** - bounding_box_query and polygon_query
3. **Work with annotations** - understand table-element relationships
4. **Explore coordinate transformations** and multi-scale data

**Intermediate workflow:**
```python
# 1. Create your own annotation tables
from spatialdata.models import TableModel
table = TableModel.parse(adata, region="my_labels")

# 2. Perform spatial queries
result = sdata.query.bounding_box(...)

# 3. Join data with annotations
from spatialdata import join_spatialelement_table
elements, table = join_spatialelement_table(...)

# 4. Work with coordinate systems
sdata.transform_to("global", "new_system")
```

### For Advanced Users

1. **Read advanced.md** for architecture understanding
2. **Implement custom data readers** using spatialdata-io patterns
3. **Optimize performance** with chunking and lazy loading
4. **Contribute to the ecosystem** - understanding OME-NGFF compliance

**Advanced workflow:**
```python
# 1. Create custom elements with specific transformations
from spatialdata.models import Image2DModel
image = Image2DModel.parse(
    data,
    transformations={"custom": Translation([100, 100])}
)

# 2. Optimize large datasets
# Use chunking, multi-scale representations
# Implement custom spatial indexes

# 3. Extend the framework
# Create custom models, readers, or visualization tools
```

### Navigation Tips

- **For installation issues:** Check getting_started.md for dependency conflicts
- **For API questions:** Search api.md for specific function names
- **For conceptual understanding:** Start with io.md terminology, then read advanced.md
- **For practical examples:** Use the Quick Reference section with real code patterns
- **For ecosystem integration:** Look for spatialdata-io, spatialdata-plot, napari-spatialdata references

## Resources

### Ecosystem Packages
- **spatialdata-io**: Technology-specific readers and converters
- **spatialdata-plot**: Static plotting and visualization
- **napari-spatialdata**: Interactive napari plugin
- **spatialdata-sandbox**: Example datasets and converters

### Storage Formats
- **Zarr**: Chunked storage for large arrays
- **OME-NGFF**: Standard for bioimaging data
- **Parquet**: Columnar storage for tabular data

### Community
- **scverse project**: Governance and contribution guidelines
- **GitHub repository**: Source code and issue tracking
- **Documentation**: Comprehensive guides and tutorials

## Notes

- SpatialData uses standard scientific Python libraries (xarray, AnnData, geopandas)
- All spatial elements require coordinate systems and transformations
- Tables use AnnData format and can annotate multiple spatial elements
- The framework emphasizes lazy loading and chunked storage for performance
- Compatible with OME-NGFF specification for interoperability

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from the SpatialData documentation
