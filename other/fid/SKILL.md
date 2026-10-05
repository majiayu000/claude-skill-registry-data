---
name: fid
description: Measures the distributional similarity between original GAN-generated images and their semantically manipulated counterparts. It evaluates whether a latent space transformation preserves overall image quality and realism while altering specific attributes. Use when the user has predictions and gold and needs to compute FID.
metadata:
  skill_kind: metric
  source_arxiv: 2305.14551
  bibtex_key: palaev2023exploring
  confidence: high
---

# fid

> Exploring Semantic Variations in GAN Latent Spaces via Matrix Factorization — Palaev et al. (2023) (arXiv:2305.14551, 2023)

## What this evaluates

Measures the distributional similarity between original GAN-generated images and their semantically manipulated counterparts. It evaluates whether a latent space transformation preserves overall image quality and realism while altering specific attributes.

## Datasets

- **StyleGAN2 & Liu et al. (2021) GAN generations** — total 1000; splits: test (1000)

## Metrics

- `FID` **(primary)** — range: [0, ∞)
  - Fréchet Inception Distance: computes the Wasserstein-2 distance between the multivariate Gaussian distributions of features extracted by Inception v3 from two sets of images. Lower values indicate higher similarity and better generation/manipulation quality.

## Input / output format

**Input**: Two sets of 1000 images each: (1) original images generated from random latent vectors, and (2) the same images after applying a random GANSpace transformation.

**Output**: A single scalar FID score representing the distance between the two image sets.

## Scoring recipe

```python
def compute_fid(images_orig, images_trans):
    feats_orig = inception_features(images_orig)
    feats_trans = inception_features(images_trans)
    mu1, sigma1 = np.mean(feats_orig, axis=0), np.cov(feats_orig, rowvar=False)
    mu2, sigma2 = np.mean(feats_trans, axis=0), np.cov(feats_trans, rowvar=False)
    diff = mu1 - mu2
    covmean, _ = scipy.linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    fid = np.sum(diff**2) + np.trace(sigma1 + sigma2 - 2.0 * covmean)
    return np.real(fid)
```

## Common pitfalls

- FID is highly sensitive to the specific Inception v3 checkpoint and preprocessing pipeline used; results are not directly comparable across papers without identical feature extractors.
- FID measures global distribution similarity, not semantic correctness; a low FID does not guarantee the intended attribute was successfully manipulated.

## Evidence (verbatim from paper)

> To evaluate the quality of the transformations found by GANSpace, we generated 1000 images for both GANs and applied one random transformation from a set found by GANSpace to each image. We calculated the Fréchet inception distance (FID) (Heusel et al., 2017) between the original generated images and the transformed ones to measure the similarity between the two sets of images. A lower FID score indicates higher similarity.

## Citation

```bibtex
@misc{palaev2023exploring,
  title={Exploring Semantic Variations in GAN Latent Spaces via Matrix Factorization},
  author={Palaev et al. (2023)},
  year={2023},
  note={arXiv:2305.14551}
}
```

- arXiv: 2305.14551
