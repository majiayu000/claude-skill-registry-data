---
name: spatialdata-io-docs-local
description: SpatialData-IO 空间数据I/O工具包 - 100%覆盖85个核心文件（20个空间平台+6个API+6个CLI+53个生成器文档）
---

# Spatialdata-Io-Docs-Local Skill

Comprehensive assistance with spatialdata-io-docs-local development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with spatialdata-io-docs-local
- Asking about spatialdata-io-docs-local features or APIs
- Implementing spatialdata-io-docs-local solutions
- Debugging spatialdata-io-docs-local code
- Learning spatialdata-io-docs-local best practices

## Quick Reference

### Common Patterns

**Pattern 1:** spatialdata-io API spatialdata_io.codex spatialdata_io.cosmx spatialdata_io.curio spatialdata_io.dbit spatialdata_io.experimental.iss spatialdata_io.mcmicro spatialdata_io.merscope spatialdata_io.seqfish spatialdata_io.steinbock spatialdata_io.stereoseq spatialdata_io.visium spatialdata_io.visium_hd spatialdata_io.xenium spatialdata_io.generic spatialdata_io.image spatialdata_io.geojson spatialdata_io.experimental.from_legacy_anndata spatialdata_io.experimental.to_legacy_anndata spatialdata_io.xenium_aligned_image spatialdata_io.xenium_explorer_selection CLI Changelog Contributing guide References .md .pdf CLI Contents spatialdata_io codex cosmx curio dbit generic iss macsima mcmicro merscope seqfish steinbock stereoseq visium visium-hd xenium CLI# This section documents the Command Line Interface (CLI) for the spatialdata_io package. spatialdata_io# Convert standard technology data formats to SpatialData object. Usage: python -m spatialdata_io <Command> -i <input> -o <output> For help on how to use a specific command, run: python -m spatialdata_io <Command> –help spatialdata_io [OPTIONS] COMMAND [ARGS]... codex# Codex conversion to SpatialData. spatialdata_io codex [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --fcs <fcs># Whether the .fcs file is provided if False a .csv file is expected. [default: True] cosmx# Cosmic conversion to SpatialData. spatialdata_io cosmx [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --dataset-id <dataset_id># Name of the dataset [default: None] --transcripts <transcripts># Whether to load transcript information. [default: True] curio# Curio conversion to SpatialData. spatialdata_io curio [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. dbit# Conversion of DBit-seq to SpatialData. spatialdata_io dbit [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --anndata-path <anndata_path># Path to the counts and metadata file. [default: None] --barcode-position <barcode_position># Path to the barcode coordinates file. [default: None] --image-path <image_path># Path to the low resolution image file. [default: None] --dataset-id <dataset_id># Dataset ID. [default: None] --border <border># Value pass internally to _xy2edges. [default: True] --border-scale <border_scale># The factor by which the border is scaled. [default: 1] generic# Read generic data to SpatialData. spatialdata_io generic [OPTIONS] Options -i, --input <input># Required Path to the image/shapes input file. Supported extensions: [‘.tif’, ‘.tiff’, ‘.png’, ‘.jpg’, ‘.jpeg’, ‘.geojson’] -o, --output <output># Required Path to zarr store to write to. If it does not exist yet, create new zarr store from input -n, --name <name># name of the element to be stored --data-axes <data_axes># Axes of the data for image files. Valid values are permutations of ‘cyx’ and ‘czyx’. -c, --coordinate-system <coordinate_system># Coordinate system in spatialdata object to which an element should belong iss# ISS conversion to SpatialData. spatialdata_io iss [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --raw-relative-path <raw_relative_path># Required Relative path to raw raster image file. --labels-relative-path <labels_relative_path># Required Relative path to label image file. --h5ad-relative-path <h5ad_relative_path># Required Relative path to counts and metadata file. --instance-key <instance_key># Which column of the AnnData table contains the CellID. [default: None] --dataset-id <dataset_id># Dataset ID [default: region] --multiscale-image <multiscale_image># Whether to process the image into a multiscale image [default: True] --multiscale-labels <multiscale_labels># Whether to process the label image into a multiscale image [default: True] macsima# Read MACSima formatted dataset and convert to SpatialData. spatialdata_io macsima [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --filter-folder-names <filter_folder_names># List of folder names to filter out when parsing multiple folders. [default: None] --subset <subset># Subset the image to the first ‘subset’ pixels in x and y dimensions. [default: None] --c-subset <c_subset># Subset the image to the first ‘c-subset’ channels. [default: None] --max-chunk-size <max_chunk_size># Maximum chunk size for x and y dimensions. [default: 1024] --c-chunks-size <c_chunks_size># Chunk size for c dimension. [default: 1] --multiscale <multiscale># Whether to create a multiscale image. [default: True] --transformations <transformations># Whether to add a transformation from pixels to microns to the image. [default: True] --scale-factors <scale_factors># Scale factors to use for downsampling. If None, scale factors are calculated based on image size. [default: None] --default-scale-factor <default_scale_factor># Default scale factor to use for downsampling. [default: 2] --nuclei-channel-name <nuclei_channel_name># Common string of the nuclei channel to separate nuclei from other channels. [default: ‘DAPI’] --split-threshold-nuclei-channel <split_threshold_nuclei_channel># Threshold for splitting nuclei channels. [default: 2] --skip-rounds <skip_rounds># List of round numbers to skip when parsing the data. [default: None] --include-cycle-in-channel-name <include_cycle_in_channel_name># Whether to include the cycle number in the channel name. [default: False] mcmicro# Conversion of MCMicro to SpatialData. spatialdata_io mcmicro [OPTIONS] Options -i, --input <input># Required Path to the mcmicro project directory. -o, --output <output># Required Path to the output.zarr file. merscope# Merscope conversion to SpatialData. spatialdata_io merscope [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --vpt-outputs <vpt_outputs># Optional argument to specify the path to the Vizgen postprocessing tool. [default: None] --z-layers <z_layers># Indices of the z-layers to consider. [default: 3] --region-name <region_name># Name of the ROI. [default: None] --slide-name <slide_name># Name of the slide/run [default: None] --backend <backend># Either ‘dask_image’ or ‘rioxarray’. [default: None] Options: dask_image | rioxarray --transcripts <transcripts># Whether to read transcripts. [default: True] --cells-boundaries <cells_boundaries># Whether to read cells boundaries. [default: True] --cells-table <cells_table># Whether to read cells table. [default: True] --mosaic-images <mosaic_images># Whether to read the mosaic images. [default: True] seqfish# Seqfish conversion to SpatialData. spatialdata_io seqfish [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --load-images <load_images># Whether to load images. [default: True] --load-labels <load_labels># Whether to load labels. [default: True] --load-points <load_points># Whether to load points. [default: True] --load-shapes <load_shapes># Whether to load shapes. [default: True] --cells-as-circles <cells_as_circles># Whether to read cells as circles. [default: False] --rois <rois># Which sections to load. Provide one or more section indices. [default: All sections are loaded] steinbock# Steinbock conversion to SpatialData. spatialdata_io steinbock [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --labels-kind <labels_kind># What kind of labels to use. [default: ‘deepcell’] Options: deepcell | ilastik stereoseq# Stereoseq conversion to SpatialData. spatialdata_io stereoseq [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --dataset-id <dataset_id># Dataset ID. [default: None] --read-square-bin <read_square_bin># If True, will read the square bin {xx.GEF_FILE!r} file and build corresponding points element. [default: True] --optional-tif <optional_tif># If True, will read {xx.TISSUE_TIF!r} files. [default: False] visium# Visium conversion to SpatialData. spatialdata_io visium [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --dataset-id <dataset_id># Dataset ID. [default: None] --counts-file <counts_file># Name of the counts file, defaults to {vx.FILTERED_COUNTS_FILE!r}. [default: None] --fullres-image-file <fullres_image_file># Path to the full resolution image. [default: None] --tissue-positions-file <tissue_positions_file># Path to the tissue positions file. [default: None] --scalefactors-file <scalefactors_file># Path to the scalefactors file. [default: None] visium-hd# Visium HD conversion to SpatialData. spatialdata_io visium-hd [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --dataset-id <dataset_id># Dataset ID. [default: None] --filtered-counts-file <filtered_counts_file># It sets the value of counts_file to {vx.FILTERED_COUNTS_FILE!r} (when True) or to``{vx.RAW_COUNTS_FILE!r}`` (when False). [default: True] --bin-size <bin_size># When specified, load the data of a specific bin size, or a list of bin sizes. By default, it loads all the available bin sizes. [default: None] --bins-as-squares <bins_as_squares># If true, bins are represented as squares otherwise as circles. [default: True] --fullres-image-file <fullres_image_file># Path to the full resolution image. [default: None] --load-all-images <load_all_images># If False, load only the full resolution, high resolution, and low resolution images. If True, also the following images: {vx.IMAGE_CYTASSIST!r}. [default: False] --annotate-table-by-labels <annotate_table_by_labels># If true, annotates the table by labels. [default: False] xenium# Xenium conversion to SpatialData. spatialdata_io xenium [OPTIONS] Options -o, --output <output># Required Path to the output file. -i, --input <input># Required Path to the input file. --cells-boundaries <cells_boundaries># Whether to read cells boundaries. [default: True] --nucleus-boundaries <nucleus_boundaries># Whether to read Nucleus boundaries. [default: True] --cells-as-circles <cells_as_circles># Whether to read cells as circles. [default: None] --cells-labels <cells_labels># Whether to read cells labels (raster). [default: True] --nucleus-labels <nucleus_labels># Whether to read nucleus labels (raster). [default: True] --transcripts <transcripts># Whether to read transcripts. [default: True] --morphology-mip <morphology_mip># Whether to read morphology mip image. [default: True] --morphology-focus <morphology_focus># Whether to read morphology focus image. [default: True] --aligned-images <aligned_images># Whether to parse additional H&E or IF aligned images. [default: True] --cells-table <cells_table># Whether to read cells annotations in the AnnData table. [default: True] --n-jobs <n_jobs># Number of jobs. [default: 1] previous spatialdata_io.xenium_explorer_selection next Changelog Contents spatialdata_io codex cosmx curio dbit generic iss macsima mcmicro merscope seqfish steinbock stereoseq visium visium-hd xenium By scverse © Copyright 2025, scverse..

```
spatialdata_io
```

**Pattern 2:** Usage:

```
spatialdata_io [OPTIONS] COMMAND [ARGS]...
```

**Pattern 3:** spatialdata-io API spatialdata_io.codex spatialdata_io.cosmx spatialdata_io.curio spatialdata_io.dbit spatialdata_io.experimental.iss spatialdata_io.mcmicro spatialdata_io.merscope spatialdata_io.seqfish spatialdata_io.steinbock spatialdata_io.stereoseq spatialdata_io.visium spatialdata_io.visium_hd spatialdata_io.xenium spatialdata_io.generic spatialdata_io.image spatialdata_io.geojson spatialdata_io.experimental.from_legacy_anndata spatialdata_io.experimental.to_legacy_anndata spatialdata_io.xenium_aligned_image spatialdata_io.xenium_explorer_selection CLI Changelog Contribution guide References .rst .pdf spatialdata_io.xenium_aligned_image Contents xenium_aligned_image() spatialdata_io.xenium_aligned_image# spatialdata_io.xenium_aligned_image(image_path, alignment_file, imread_kwargs=mappingproxy({}), image_models_kwargs=mappingproxy({}), dims=None, rgba=False, c_coords=None)# Read an image aligned to a Xenium dataset, with an optional alignment file. Parameters: image_path (str | Path) – Path to the image. alignment_file (str | Path | None) – Path to the alignment file, if not passed it is assumed that the image is aligned. image_models_kwargs (Mapping[str, Any] (default: mappingproxy({}))) – Keyword arguments to pass to the image models. dims (tuple[str, ...] | None (default: None)) – Dimensions of the image (tuple of axes names); valid strings are “c”, “x” and “y”. If not passed, the function will try to infer the dimensions from the image shape. Please use this argument when the default behavior fails. Example: for an image with shape (1, y, 1, x, 3), use dims=(“anystring”, “y”, “dummy”, “x”, “c”). Values that are not “c”, “x” or “y” are considered dummy dimensions and will be squeezed (the data must have len 1 for those axes). rgba (bool (default: False)) – Interprets the c channel as RGBA, by setting the channel names to r, g, b (a). When c_coords is not None, this argument is ignored. c_coords (list[str] | None (default: None)) – Channel names for the image. By default, the function will try to infer the channel names from the image shape and name (by detecting if the name suggests that the image is a H&E image). Example: for an RGB image with shape (3, y, x), use c_coords=[“r”, “g”, “b”]. Return type: DataTree Returns: : The single-scale or multi-scale aligned image element. previous spatialdata_io.experimental.to_legacy_anndata next spatialdata_io.xenium_explorer_selection Contents xenium_aligned_image() By scverse © Copyright 2025, scverse.

```
xenium_aligned_image()
```

**Pattern 4:** dims (tuple[str, ...] | None (default: None)) – Dimensions of the image (tuple of axes names); valid strings are “c”, “x” and “y”. If not passed, the function will try to infer the dimensions from the image shape. Please use this argument when the default behavior fails. Example: for an image with shape (1, y, 1, x, 3), use dims=(“anystring”, “y”, “dummy”, “x”, “c”). Values that are not “c”, “x” or “y” are considered dummy dimensions and will be squeezed (the data must have len 1 for those axes).

```
tuple
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **cli.md** - Cli documentation
- **core.md** - Core documentation
- **other.md** - Other documentation
- **platforms_10x.md** - Platforms 10X documentation
- **platforms_commercial.md** - Platforms Commercial documentation
- **platforms_experimental.md** - Platforms Experimental documentation
- **platforms_imaging.md** - Platforms Imaging documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
