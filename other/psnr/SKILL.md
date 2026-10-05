---
name: PSNR
description: Evaluates the trade-off between file size reduction and image fidelity when encoding radio astronomy data using JPEG2000. It benchmarks both lossless and lossy compression modes to determine the compression ratio at which visual artifacts first appear. Use when the user has predictions and gold and needs to compute PSNR.
metadata:
  skill_kind: metric
  source_arxiv: 1403.2801
  bibtex_key: kitaeff2014astronomical
  confidence: high
---

# PSNR

> Astronomical Imagery: Considerations For a Contemporary Approach with JPEG2000 — Kitaeff et al. (2014) (arXiv:1403.2801, 2014)

## What this evaluates

Evaluates the trade-off between file size reduction and image fidelity when encoding radio astronomy data using JPEG2000. It benchmarks both lossless and lossy compression modes to determine the compression ratio at which visual artifacts first appear.

## Datasets

- **Radio Astronomy FITS Test Set** — total 11; splits: test (11)

## Metrics

- `PSNR` **(primary)** — range: dB
  - Peak Signal-to-Noise Ratio in decibels (dB), calculated as 10 * log10(MAX^2 / MSE), where MAX is the maximum pixel intensity (65535 for 16-bit data) and MSE is the mean squared error between the original and compressed images.
- `Compression Ratio` — range: ratio
  - The ratio of the original FITS file size to the resulting JPEG2000 file size.

## Input / output format

**Input**: FITS files containing radio astronomy data cubes or planar images, converted to 16-bit unsigned integer grayscale images.

**Output**: JPEG2000 files and associated quality metrics (PSNR, MAD, etc.) and compression ratios.

## Scoring recipe

```python
def compute_metrics(original_fits, compressed_jp2):
    orig_arr = fits_to_16bit(original_fits)
    comp_arr = jp2_to_16bit(compressed_jp2)
    mse = np.mean((orig_arr - comp_arr) ** 2)
    max_val = 65535.0
    psnr = 10 * np.log10((max_val ** 2) / mse) if mse > 0 else float('inf')
    compression_ratio = original_fits.size_bytes / compressed_jp2.size_bytes
    return psnr, compression_ratio
```

## Common pitfalls

- Floating-point FITS data must be manually scaled to 16-bit integers before encoding, potentially losing precision if the dynamic range is small.
- The f2j converter does not transfer FITS headers to JPEG2000 metadata boxes, losing astronomical metadata.
- Visual degradation occurs over a wide range of compression ratios despite PSNR values clustering in a narrow band, making PSNR alone insufficient to predict perceptual quality.

## Evidence (verbatim from paper)

> We have built-in f2j the options to calculate the mean squared error (MSE), root mean squared error (RMSE), peak signal to noise ratio (PSNR), mean absolute error (MAE), fidelity and maximum absolute distortion (MAD) metrics (as well as intermediate data for these metrics). These metrics are recommended for compression benchmarks (Delcourt et al., [2011]). In practice, we’ve found the fidelity metric to be unhelpful, as in none of the tests conducted did it drop below 0.98, even for badly distorted images. MSE, RMSE and PSNR are all re-expressions of the same information and thus interchangeable. PSNR was found to be the most intuitive to work with and was therefore used in most of our tests.

## Citation

```bibtex
@misc{kitaeff2014astronomical,
  title={Astronomical Imagery: Considerations For a Contemporary Approach with JPEG2000},
  author={Kitaeff et al. (2014)},
  year={2014},
  note={arXiv:1403.2801}
}
```

- arXiv: 1403.2801
