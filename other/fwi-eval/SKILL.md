---
name: fwi-eval
description: Evaluates the ability of deep learning models to perform full waveform inversion (FWI) by predicting subsurface velocity maps from seismic data under varying source frequencies and locations. It probes generalization across different source configurations and robustness to noise and missing traces. Use when the user wants to benchmark on FWI-F, FWI-L, FWI-FL, or asks about evaluating this task. Reports L2 relative error.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2305.17289
  bibtex_key: zhu2023fourierdeeponet
  confidence: high
---

# fwi-eval

> Fourier-DeepONet: Fourier-enhanced deep operator networks for full waveform inversion with improved accuracy, generalizability, and robustness — Min Zhu et al. (2023) (arXiv:2305.17289, 2023)

## What this evaluates

Evaluates the ability of deep learning models to perform full waveform inversion (FWI) by predicting subsurface velocity maps from seismic data under varying source frequencies and locations. It probes generalization across different source configurations and robustness to noise and missing traces.

## Datasets

- **FWI-F** — total ?; splits: test (-1)
- **FWI-L** — total ?; splits: test (-1)
- **FWI-FL** — total ?; splits: test (-1)

## Metrics

- `MAE` — range: [0, 1]
  - Mean absolute error: the average of the absolute differences between predicted and actual values.
- `RMSE` — range: [0, 1]
  - Root mean squared error: the square root of the mean of the squared differences between predicted and actual values.
- `SSIM` — range: [0, 1]
  - Structural similarity index: measures perceptual image quality based on luminance, contrast, and structure correlations between predicted and ground truth maps.
- `L2 relative error` **(primary)** — range: [0, 1]
  - Ratio of the L2 norm of the prediction error to the L2 norm of the ground truth: ||y_pred - y_true||_2 / ||y_true||_2.

## Input / output format

**Input**: Normalized seismic data (range -1 to 1) corresponding to varying source frequencies and/or locations.

**Output**: Predicted subsurface velocity map (range -1 to 1).

## Scoring recipe

```python
def compute_metrics(pred, true):
    mae = np.mean(np.abs(pred - true))
    rmse = np.sqrt(np.mean((pred - true) ** 2))
    l2_rel = np.linalg.norm(pred - true) / np.linalg.norm(true)
    ssim = compute_ssim(pred, true)
    return {'MAE': mae, 'RMSE': rmse, 'L2 relative error': l2_rel, 'SSIM': ssim}
```

## Common pitfalls

- Models trained on fixed-frequency/location datasets (e.g., OpenFWI) fail to generalize when source parameters deviate from training conditions.
- Higher source frequencies are easier to learn and yield lower errors than lower frequencies.
- Error metrics can saturate at very high values (e.g., ~200% for L2 relative error), masking further degradation.

## Evidence (verbatim from paper)

> To evaluate the performances of different models, we adopt the following metrics: (1) mean absolute error (MAE), (2) root mean squared error (RMSE), (3) structural similarity (SSIM), and (4) $L^{2}$ relative error. MAE and RMSE are two commonly used evaluation metrics in regression problems, which quantify the differences between predicted values and actual values. MAE is calculated as the mean of the absolute differences between the predicted and actual values. RMSE is calculated as the square root of the mean of the squared differences between the predicted and actual values. By squaring the errors, it emphasizes larger errors compared to MAE. SSIM measures the similarity between two images based on how closely they match from a perceptual perspective, providing a representation of how humans perceive image quality. The $L^{2}$ relative error is a metric used to measure the difference between predictions and ground truth by taking into account the magnitudes of the values. Smaller MAE, RMSE, and $L^{2}$ relative error, or larger SSIM indicate better model performance.

## Citation

```bibtex
@misc{zhu2023fourierdeeponet,
  title={Fourier-DeepONet: Fourier-enhanced deep operator networks for full waveform inversion with improved accuracy, generalizability, and robustness},
  author={Min Zhu et al. (2023)},
  year={2023},
  note={arXiv:2305.17289}
}
```

- arXiv: 2305.17289
