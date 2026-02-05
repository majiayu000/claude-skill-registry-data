---
name: organ-axis-complete
description: Organ Axis tutorial docs - 100%覆盖文档（模型应用+公式+注释采样+教程)
---

# Organ-Axis-Complete Skill

Comprehensive assistance with OrganAxis computational approach for constructing Common Coordinate Frameworks (CCF) from spatial landmarks.

## When to Use This Skill

This skill should be triggered when:

### **Spatial Analysis & CCF Development**
- Building Common Coordinate Frameworks for any organ or tissue
- Mapping specimens to reference spaces using spatial landmarks
- Performing multi-sample spatial integration while preserving continuous information
- Developing spatial axes for specific anatomical structures (e.g., Cortico-Medullary Axis)

### **Tissue Annotation & Sampling**
- Need consistent tissue annotations across different spatial platforms
- Working with spatial sampling resolution harmonization
- Creating hexagonal point grids (HPG) for standardized spatial sampling
- Annotating tissues at different resolutions (pixel-level vs. spot-level)

### **Platform-Specific Tasks**
- Analyzing Visium spatial transcriptomics data with 100µm spot resolution
- Working with imaging technologies like IBEX at pixel resolution
- Using TissueTag for interactive tissue annotation in Jupyter notebooks
- Integrating data from multiple spatial omics platforms

### **Research Applications**
- Studying molecular gradients and intra-compartmental tissue differences
- Modeling linear and non-linear spatial associations
- Analyzing cellular neighborhoods and anatomical structures
- Developing hypothesis-driven spatial frameworks

## Quick Reference

### Core OrganAxis Concepts

```python
# Basic CCF Construction Principles
# OrganAxis enables mapping 2D tissues to Common Coordinate Frameworks
# Derived purely from reference images, universally applicable across platforms
# Reduces double-dipping risk by not using high-dimensional gene space
```

### Spatial Sampling Setup

```python
# Spatial Sampling Frequency Definition
# Define in μm or mm (e.g., spot every 2 μm)
# Independent of imaging resolution (pixel space)
# Must be consistent across all samples and modalities
```

### Tissue Annotation Workflow

```python
# Multi-Platform Annotation Strategy
# Visium: Use 10x Genomics Loupe Browser (100µm resolution)
# Imaging: Use Napari (pixel-level resolution)
# Jupyter: Use TissueTag for interactive annotation
# Cluster: Implement programmatic annotation solutions
```

### Hexagonal Point Grid (HPG) Creation

```python
# HPG for Cross-Platform Harmonization
# Create hexagonal grid with predetermined sampling frequency
# Map pixel-level annotations to grid points
# Balance between structure resolution and noise robustness
# Lower frequency = more robust but less detail
```

### Spatial Resolution Trade-offs

```python
# Resolution Selection Guidelines
# Higher spatial sampling: Discern fine structures, less noise robust
# Lower spatial sampling: Capture broad structures, more noise robust
# Match resolution to research question requirements
# Consider tissue variability and structure complexity
```

### Multi-Sample Integration Strategy

```python
# Diagonal Integration Approach
# Preserve continuous spatial information across samples
# Enable direct inter-sample comparisons
# Use landmark-based orientation with nonlinear transformations
# Account for specimen-to-specimen variability
```

### Hypothesis-Driven Framework Development

```python
# CCF Development Best Practices
# Requires prior knowledge of tissue biology
# Focus on biologically robust and meaningful axes
# Example: Human thymus Cortico-Medullary Axis (CMA)
# Validate framework with domain expertise
```

## Key Concepts

### **Common Coordinate Framework (CCF)**
A set of rules allowing researchers to map specimens to a reference space, enabling direct inter-sample comparisons and integration. Types include:
- **Anatomical coordinate systems**: For stereotypical structures (e.g., embryos)
- **Landmark-based systems**: Using morphological/histological or molecular features
- **Non-linear transformations**: For systems with high variability

### **Spatial Sampling Frequency**
Defined in μm or mm (e.g., spot every 2 μm), independent of imaging resolution. Critical for harmonizing across technologies and maintaining consistency across samples and modalities.

### **Hexagonal Point Grid (HPG)**
A filter-like structure for mapping pixel-level annotations to a standardized spatial sampling frequency, balancing structure resolution with noise robustness.

### **Double-Dipping Prevention**
OrganAxis approach is derived purely from reference images, not from high-dimensional gene space, significantly reducing the risk of circular analysis.

### **Cortico-Medullary Axis (CMA)**
The specific application of OrganAxis to derive the human thymus spatial framework, demonstrating the approach's practical implementation.

## Reference Files

### **getting_started.md**
**Pages: 3**
- **Introduction**: Comprehensive overview of CCF concepts and OrganAxis methodology
- **Common Coordinate Framework**: Detailed explanation of CCF types and applications
- **Welcome**: OrganAxis features and computational approach summary

**Key Topics Covered:**
- Tissue compartment subdivision challenges
- Inter-sample variability handling
- Allen Mouse Brain Atlas example
- Human brain mapping complexities
- Multi-dimensional extension capabilities

### **tutorials.md**
**Pages: 1**
- **Prerequisites for CFF establishment**: Complete guide to tissue annotation and spatial sampling

**Key Topics Covered:**
- Consistent tissue annotation strategies across platforms
- Spatial sampling resolution definition and harmonization
- TissueTag tool for Jupyter notebook annotation
- Platform-specific annotation tools (Loupe Browser, Napari)
- HPG implementation for cross-platform integration

## Working with This Skill

### **For Beginners**
1. **Start with**: `getting_started.md` → Introduction section
2. **Focus on**: Understanding CCF fundamentals and why they matter
3. **Practice**: Basic tissue annotation concepts using familiar examples
4. **Key takeaway**: Learn how spatial frameworks enhance reproducibility

### **For Intermediate Users**
1. **Reference**: `tutorials.md` for practical implementation guidance
2. **Implement**: Hexagonal point grid creation and sampling frequency optimization
3. **Apply**: Multi-platform annotation strategies in your projects
4. **Master**: Balance between spatial resolution and noise robustness

### **For Advanced Users**
1. **Extend**: Apply OrganAxis to 3D and 4D datasets
2. **Customize**: Develop organ-specific CCF models using domain expertise
3. **Integrate**: Multi-modal spatial data with diagonal integration approaches
4. **Innovate**: Create new spatial axes for novel anatomical structures

### **Navigation Tips**
- Use `view` command to read specific reference files when detailed information is needed
- Cross-reference between getting_started concepts and tutorials implementation
- Focus on hypothesis-driven framework development for biologically meaningful results
- Consider platform-specific limitations when designing spatial sampling strategies

## Resources

### **references/**
Organized documentation containing:
- Detailed theoretical explanations with mathematical foundations
- Platform-specific implementation strategies
- Real-world application examples (thymus CMA)
- Links to original documentation and tools
- Structured table of contents for rapid navigation

### **scripts/**
Add helper scripts for:
- HPG generation algorithms
- Spatial sampling frequency calculators
- Cross-platform annotation converters
- CCF transformation utilities

### **assets/**
Add templates and examples for:
- Tissue annotation schemas
- Spatial landmark definition templates
- Multi-sample integration workflows
- Platform-specific configuration files

## Notes

- **Universally Applicable**: OrganAxis works across any spatial platform and resolution
- **Hypothesis-Driven**: Requires prior biological knowledge for meaningful axis development
- **Active Development**: Project under continuous improvement with community feedback
- **Non-Restrictive**: Not limited by dimensionality - applicable to 3D and 4D datasets
- **Memory**: Developed in memory of Daniele Muraro

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the current configuration
2. Update reference files with latest methodology improvements
3. Refresh Quick Reference examples with new use cases
4. Maintain alignment with active development in the OrganAxis repository
