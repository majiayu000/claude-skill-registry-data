---
name: osta-docs-local
description: OSTA 本地文档（OSTA/）
---

# Osta-Docs-Local Skill

Comprehensive assistance with spatial transcriptomics analysis using Bioconductor's OSTA (Orchestrating Spatial Transcriptomics Analysis) framework.

## When to Use This Skill

This skill should be triggered when:
- **Working with spatial omics data analysis** in R/Bioconductor
- **Exploring the Bioconductor spatial ecosystem** and finding relevant packages
- **Learning spatial transcriptomics workflows** including sequencing-based and imaging-based platforms
- **Implementing spatial data analysis** steps like quality control, normalization, clustering
- **Finding Bioconductor packages** for specific spatial analysis tasks (clustering, visualization, etc.)
- **Understanding package ecosystem metrics** and growth trends in spatial omics
- **Debugging spatial analysis code** or troubleshooting Bioconductor package issues
- **Learning best practices** for spatial transcriptomics data analysis

## Quick Reference

### Essential Bioconductor Package Discovery

**Example 1: Find all spatial omics packages**
```r
library(BiocPkgTools)
df <- biocPkgList()
.f <- \(x, y=df) vapply(y$biocViews, \(.) all(x %in% .), logical(1))
spatial_packages <- df$Package[.f("Spatial")]
print(spatial_packages)
```

**Example 2: Find packages for specific spatial analysis tasks**
```r
# Find spatial clustering packages
spatial_clustering <- df$Package[.f(c("Spatial", "Clustering"))]
print(spatial_clustering)
```

**Example 3: Interactive package exploration**
```r
library(BiocPkgTools)
biocExplore()
```

### Key Spatial Analysis Libraries

**Example 4: Core spatial packages to load**
```r
library(ggspavis)          # Spatial visualization
library(OSTA.data)         # OSTA example datasets
library(SpatialExperiment) # Spatial data structures
library(SpatialExperimentIO) # Data import/export
```

**Example 5: Analyze Bioconductor ecosystem growth**
```r
library(dplyr)
library(ggplot2)

# Get package growth metrics over time
ids <- c("SingleCell", "Spatial")
gg <- lapply(ids, \(id) {
  nm <- df$Package[.f(id)]
  ys <- BiocPkgTools:::getPkgYearsInBioc(nm) |>
    mutate(first=first_version_release_date) |>
    mutate(last=last_version_release_date) |>
    filter(!is.na(first))
  # Complete months between first/last dates
  lapply(split(ys, ys$package), \(.) {
    data.frame(package=.$package, date=seq(.$first, .$last))
  }) |> do.call(what=rbind) |> group_by(date) |> count()
}) |> bind_rows(.id="biocViews")
```

**Example 6: Visualize package ecosystem trends**
```r
ggplot(gg, aes(date, n, col=biocViews)) +
  geom_line(linewidth=0.8) +
  geom_smooth(data=filter(gg, n >= 5),
      method="lm", se=FALSE, linewidth=1) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(x=NULL, y="# packages") +
  theme_bw()
```

**Example 7: Find packages by specific analysis categories**
```r
# Common spatial analysis categories
categories <- c("BatchEffect", "Normalization", "QualityControl",
               "Visualization", "Clustering", "DimensionReduction",
               "FeatureExtraction", "DifferentialExpression",
               "GeneSetEnrichment")

# Count packages for each category
package_counts <- lapply(categories, \(cat) {
  n <- sum(.f(c("Spatial", cat)))
  data.frame(category=cat, count=n)
}) |> do.call(what=rbind)
```

## Key Concepts

### Spatial Omics Data Types
- **Sequencing-based platforms**: Visium, Visium HD, Visium DLPFC, Visium CRC
- **Imaging-based platforms**: Xenium, CODEX, MIBI
- **Data structures**: SpatialExperiment, SpatialFeatureExperiment

### Bioconductor Ecosystem
- **biocViews**: Hierarchical categorization system for packages
- **Package discovery**: Using BiocPkgTools for ecosystem exploration
- **Growth metrics**: ~0.48 spatial packages added per year on average
- **Package lifetime**: Average 4 years in Bioconductor

### Analysis Workflow Steps
1. **Data import**: Reading spatial data from various platforms
2. **Quality control**: Filtering and assessment of data quality
3. **Normalization**: Standardizing expression values
4. **Dimensionality reduction**: PCA, UMAP, t-SNE for spatial data
5. **Clustering**: Identifying spatial domains or cell types
6. **Visualization**: ggspavis for spatial plots
7. **Statistical testing**: Differential expression, spatial statistics

## Reference Files

This skill includes comprehensive documentation in `references/`:

### analysis.md
- **Overview**: Introduction to OSTA (Orchestrating Spatial Transcriptomics Analysis)
- **Content**: Complete book structure with 39 pages covering spatial transcriptomics workflows
- **Key sections**: Sequencing-based and imaging-based platforms, platform-independent analyses, cross-platform analyses
- **Target audience**: Users learning spatial transcriptomics with Bioconductor

### pages.md
- **Detailed documentation**: Chapter 4 "Ecosystem" with comprehensive package exploration
- **Interactive examples**: R code for discovering and analyzing Bioconductor spatial packages
- **Statistical analysis**: Package growth trends, lifetime analysis, co-occurrence patterns
- **Practical tools**: Code snippets for package discovery and ecosystem metrics

## Working with This Skill

### For Beginners
1. **Start with core concepts**: Read the analysis.md reference to understand OSTA framework
2. **Explore package ecosystem**: Use Example 1-3 to discover relevant spatial packages
3. **Learn basic workflows**: Focus on sequencing-based or imaging-based platform sections
4. **Practice with examples**: Run the R code examples to get hands-on experience

### For Intermediate Users
1. **Advanced package discovery**: Use Example 7 to find packages for specific analysis tasks
2. **Ecosystem analysis**: Apply Example 5-6 to understand package trends and metrics
3. **Multi-platform workflows**: Explore cross-platform analysis sections
4. **Integration with Python**: Check sections on Python interoperability

### For Advanced Users
1. **Custom analysis pipelines**: Combine multiple packages for specialized workflows
2. **Ecosystem research**: Use the metrics and trend analysis tools for research
3. **Package development**: Understand ecosystem patterns for new package creation
4. **Large-scale analyses**: Apply multi-sample and differential analysis methods

## Navigation Tips

- **Search by platform**: Look for specific platform names (Visium, Xenium) in reference docs
- **Find by analysis type**: Use keywords like "clustering", "normalization", "visualization"
- **Cross-reference examples**: Code examples are linked to specific analysis steps
- **Follow workflows**: Each platform has dedicated workflow sections with complete examples

## Resources

### references/
- **analysis.md**: Complete OSTA book overview and structure
- **pages.md**: Detailed ecosystem chapter with interactive R examples
- Both files contain executable R code with proper language annotations
- Examples are extracted from official documentation and tested

### External Resources
- **Bioconductor BiocViews**: Online package browsing
- **OSTA book**: Complete online resource for spatial transcriptomics
- **Related book**: OSCA (Orchestrating Single-Cell Analysis) for single-cell foundations

## Notes

- This skill focuses on **spatial transcriptomics** using Bioconductor in R
- **BiocPkgTools** is essential for package discovery and ecosystem analysis
- Code examples emphasize **reproducible workflows** with real datasets
- The skill bridges **sequencing-based** and **imaging-based** spatial platforms
- **Python interoperability** is supported for integrated analyses

## Updating

To refresh this skill with updated documentation:
1. Re-run the OSTA documentation scraper
2. Update package lists and examples as Bioconductor evolves
3. Add new platform workflows as they become available
4. Maintain currency with Bioconductor releases (every 6 months)
