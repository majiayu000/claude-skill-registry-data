---
name: spata2-docs-local
description: SPATA2 空间转录组学分析工具包 - 100%覆盖414个核心文件（388个API参考+25个教程+1个主页）
---

# SPATA2 Spatial Transcriptomics Analysis Skill

Comprehensive assistance with SPATA2 spatial transcriptomics analysis, generated from official documentation covering 414 core files including API references, tutorials, and spatial analysis methods.

## When to Use This Skill

This skill should be triggered when:

**Core Spatial Analysis Tasks:**
- Analyzing spatial transcriptomics data from Visium, MERFISH, or other platforms
- Identifying tissue outlines and spatial boundaries
- Computing spatial gradients and expression patterns
- Performing spatial annotation screening (SAS)
- Working with SPATA2 objects and SpatialData classes

**Data Processing & Manipulation:**
- Loading and preprocessing spatial transcriptomics data
- Adding molecular variables and image data to SPATA2 objects
- Platform compatibility checks (Visium, VisiumHD, MERFISH)
- Spatial segmentation and tissue outline identification

**Visualization & Interpretation:**
- Creating surface plots and spatial visualizations
- Setting up SI unit axes for spatial plots
- Visualizing spatial annotations and gradients
- Interpreting spatial expression patterns

**Advanced Analysis:**
- Spatial trajectory analysis
- Differential expression in spatial context
- Gene set enrichment analysis for spatial data
- Copy number variation analysis in spatial data

## Quick Reference

### Core SPATA2 Workflow

**1. Load and Initialize SPATA2 Object**
```r
# Load example data
library(SPATA2)
data("example_data")
object <- loadExampleObject("UKF275T")

# Or create from individual data
object <- spata2_initiation_seurat(seurat_object)
```

**2. Identify Tissue Outline**
```r
# Method 1: Based on observations (recommended for most platforms)
object <- identifyTissueOutline(
  object,
  method = "obs",
  eps = getCCD(object, unit = "px") * 1.25,
  minPts = 3
)

# Method 2: Based on image (requires pixel content identification)
object <- identifyPixelContent(object, img_name = "image1")
object <- identifyTissueOutline(object, method = "image", img_name = "image1")
```

**3. Create Spatial Annotations**
```r
# Create numeric annotations (e.g., hypoxia areas)
object <- createNumericAnnotations(
  object = object,
  variable = "HM_HYPOXIA",
  threshold = "kmeans_high",
  id = "hypoxia_ann",
  inner_borders = FALSE,
  force1 = TRUE
)
```

**4. Spatial Annotation Screening (SAS)**
```r
# Pre-filter genes with SPARKX (recommended)
object <- runSPARKX(object)
sparkx_genes <- getSparkxGenes(object, threshold_pval = 0.05)

# Run SAS analysis
sas_out <- spatialAnnotationScreening(
  object = object,
  ids = "hypoxia_ann",
  variables = sparkx_genes,
  core = FALSE,
  distance = "dte"  # distance to edge
)
```

**5. Visualization**
```r
# Basic surface plot
plotSurface(object, color_by = "METRN")

# Add spatial annotation outline
plotSurface(object, color_by = "bayes_space") +
  ggpLayerSpatAnnOutline(object, ids = "hypoxia_ann")

# Add SI unit axes
plotSurface(object, color_by = "METRN") +
  ggpLayerThemeCoords() +
  ggpLayerAxesSI(object, unit = "mm")
```

### Essential Utility Functions

**Get Center-to-Center Distance**
```r
# Get CCD in different units
ccd_px <- getCCD(object, unit = "px")
ccd_mm <- getCCD(object, unit = "mm")
```

**Compute Capture Area**
```r
# Automatically calculates capture area for the spatial method
object <- computeCaptureArea(object)
```

**Spatial Annotation Barplot**
```r
# Plot changes in grouping proportion vs distance to annotation
plotSasBarplot(
  object,
  grouping = "bayes_space",
  id = "hypoxia_ann",
  distance = distToEdge(object, "hypoxia_ann"),
  unit = getDefaultUnit(object)
)
```

### Platform-Specific Examples

**Visium Data Processing**
```r
# Load Visium data
object <- loadExampleObject("UKF275T", process = TRUE, meta = TRUE)

# Visium-specific tissue outline parameters
object <- identifyTissueOutline(
  object,
  method = "obs",
  eps = getCCD(object, unit = "px") * 1.25,
  minPts = 3
)
```

**MERFISH Data Processing**
```r
# For non-grid platforms (MERFISH, SlideSeq, etc.)
object <- identifyTissueOutline(
  object,
  method = "obs",
  eps = average_min_distance * 10,
  minPts = 25
)
```

## Reference Files

This skill includes comprehensive documentation organized in `references/`:

### **api.md** (385 pages)
Complete API reference covering:
- **Spatial Methods**: `createSpatialMethod()`, `computeCaptureArea()`, `getCCD()`
- **Visualization**: `plotSurface()`, `plotSasBarplot()`, `ggpLayerAxesSI()`
- **Spatial Analysis**: `identifyTissueOutline()`, `spatialAnnotationScreening()`
- **Data Manipulation**: Functions for adding data, platform compatibility
- **Core Classes**: SPATA2, SpatialData, SpatialMethod object methods

### **tutorials.md** (27 pages)
Step-by-step tutorials including:
- **Spatial Annotation Screening**: Complete workflow for SAS analysis
- **Data Processing**: Platform-specific preprocessing guides
- **Visualization Techniques**: Advanced plotting and customization
- **Analysis Workflows**: End-to-end analysis examples

### **spatial_analysis.md** (1 page)
Overview of SPATA2 capabilities:
- **Introduction**: What SPATA2 offers for spatial analysis
- **Platform Support**: Visium, MERFISH, and other technologies
- **Key Features**: Spatial gradients, annotations, trajectories

### **other.md** (2 pages)
Additional information:
- **Installation and setup**
- **Authors and citation information**
- **License details**

## Working with This Skill

### For Beginners

1. **Start with tutorials.md** - Read the spatial annotation screening tutorial for a complete workflow example
2. **Understand the basics** - Learn about SPATA2 objects, tissue identification, and basic visualization
3. **Follow the Core Workflow** - Use the quick reference steps as your foundation
4. **Practice with example data** - Use `loadExampleObject()` to explore SPATA2 functionality

### For Intermediate Users

1. **Explore api.md** - Dive into specific functions for your analysis needs
2. **Platform-specific optimization** - Check platform compatibility and adjust parameters accordingly
3. **Advanced visualization** - Master SI units, custom color palettes, and multi-layer plots
4. **Spatial annotation screening** - Implement SAS for your specific research questions

### For Advanced Users

1. **Custom spatial methods** - Use `createSpatialMethod()` for new platforms
2. **Advanced analysis** - Combine multiple techniques like spatial trajectories with SAS
3. **Performance optimization** - Fine-tune parameters for large datasets
4. **Integration with other tools** - Combine SPATA2 with Seurat, SingleCellExperiment, etc.

### Navigation Tips

- **Search by function name** - Use the API reference to find specific functions
- **Check platform compatibility** - Always verify your platform is supported
- **Follow the tutorials** - The spatial annotation screening tutorial covers most use cases
- **Use examples** - Copy-paste examples from the documentation as starting points

## Key Concepts

### Core Objects

**SPATA2 Object**: The main data structure containing spatial transcriptomics data, coordinates, images, and analysis results.

**SpatialData**: Contains spatial coordinates, image data, and method-specific information.

**SpatialMethod**: Defines the spatial technology platform (Visium, MERFISH, etc.) and its parameters.

### Spatial Analysis Concepts

**Tissue Outline Identification**: Using DBSCAN clustering to identify tissue boundaries and sections. Critical for proper spatial analysis.

**Spatial Annotation Screening (SAS)**: Hypothesis-driven screening for genes showing non-random spatial patterns relative to reference features.

**Center-to-Center Distance (CCD)**: The physical distance between adjacent spots/barcodes, crucial for distance-based analyses.

**Distance Measures**: SPATA2 supports multiple distance units (pixels, mm, μm) with automatic conversion capabilities.

### Platform-Specific Considerations

**Visium**: Fixed grid layout with known CCD. Use `eps = CCD * 1.25` and `minPts = 3`.

**MERFISH/SlideSeq**: Variable spot locations. Use average minimum distance * 10 for `eps` and `minPts = 25`.

**Image-based Analysis**: Requires `identifyPixelContent()` before using image-based tissue outline identification.

## Resources

### references/
Complete documentation extracted from official SPATA2 sources:
- Detailed function documentation with parameters and examples
- Step-by-step tutorials for common analyses
- Platform-specific guidance and best practices
- Code examples with proper R syntax highlighting

### scripts/
Add your custom SPATA2 analysis scripts and automation workflows here.

### assets/
Store reference images, example datasets, and visualization templates.

## Notes

- This skill covers SPATA2 version 3.1.0+ with all modern features
- Documentation includes 414 core files with comprehensive coverage
- All code examples are extracted from official documentation
- Platform-specific guidance is included for major spatial technologies
- Spatial annotation screening (SAS) is a key feature for hypothesis-driven analysis

## Updating

To refresh this skill with updated SPATA2 documentation:
1. Re-run the scraper with updated configuration
2. The skill will be rebuilt with the latest API changes and features
3. Check version-specific notes for compatibility updates