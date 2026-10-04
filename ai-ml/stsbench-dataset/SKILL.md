---
name: stsbench-dataset
description: "A skill for understanding and using the STSBench dataset for modeling neuronal activity in the dorsal stream of primate visual cortex. Based on arXiv:2607.15631."
license: Complete terms in LICENSE.txt
metadata:
  arxiv_id: "2607.15631"
  subjects: ["Neurons and Cognition (q-bio.NC)", "Computer Vision and Pattern Recognition (cs.CV)"]
  year: "2026"
---

# STSBench Dataset Skill

This skill provides guidance on understanding and utilizing the STSBench dataset, a large-scale dataset of single neuron recordings from the superior temporal sulcus (STS) in macaque visual cortex, designed for modeling neuronal activity in the dorsal stream.

## Paper Overview

- **Title**: STSBench: A Large-Scale Dataset for Modeling Neuronal Activity in the Dorsal Stream of Primate Visual Cortex
- **Authors**: Ethan B. Trepka, Ruobing Xia, Shude Zhu, Sharif Saleki, Danielle Abreu Lopes, Stephen J. Niño Cital, Konstantin F. Willeke, Mindy Kim, Tirin Moore
- **arXiv**: 2607.15631 [q-bio.NC]
- **Submitted**: July 17, 2026
- **Comments**: 21 pages, 10 figures, Advances in Neural Information Processing Systems 38 (NeurIPS 2025) Datasets and Benchmarks Track
- **Journal Reference**: Advances in Neural Information Processing Systems 38 (2025)

## Key Contributions

1. **Large-scale dataset**: Over 2,000 neurons recorded from the superior temporal sulcus (STS) in Rhesus macaques while viewing thousands of unique natural videos.
2. **Benchmark for encoding models**: The dataset can be used to benchmark and compare encoding models that predict neural responses from visual stimuli.
3. **Stimulus reconstruction**: Enables reconstruction of visual input from recorded neural activity, testing the sufficiency of the dorsal stream encoding.
4. **Dorsal stream focus**: Addresses the lack of large-scale datasets for the dorsal stream, which is critical for spatial processing and motion perception.

## Dataset Description

- **Subjects**: Rhesus macaques
- **Area**: Superior temporal sulcus (STS), part of the dorsal visual stream
- **Recordings**: Single neuron recordings (extracellular)
- **Stimuli**: Thousands of unique, natural videos (complex, dynamic scenes)
- **Scale**: ~50x larger than previous dorsal stream datasets
- **Availability**: The dataset is available upon request from the authors (contact information in the paper).

## How to Use This Skill

### 1. Understanding the Dorsal Stream

The dorsal stream (the "where" pathway) processes spatial relationships, motion, and object location. STS is a higher-order area within the dorsal stream involved in integrating visual information with other sensory inputs and cognitive functions.

### 2. Loading and Exploring the Dataset

If you obtain the dataset, it likely consists of:
- Neural spike times (or firing rates) aligned to video frames
- Video stimulus files (or feature representations)
- Metadata about recording sessions, neurons, and experimental conditions

Typical steps:
- Load neural data (e.g., in MATLAB, Python with Neurodata Without Borders (NWB) format, or custom formats)
- Align neural responses to stimulus onset
- Preprocess neural data (e.g., smoothing, spike sorting validation)
- Extract features from videos (e.g., using deep learning models, hand-crafted features, or raw pixels)

### 3. Building Encoding Models

To model how neurons in STS respond to visual stimuli:

1. **Feature Extraction**: Convert video frames into feature representations (e.g., using CNN features from models pretrained on ImageNet, or optic flow, or human-labeled action labels).
2. **Model Selection**: Choose a mapping from features to neural responses:
   - Linear regression (with regularization)
   - Generalized Linear Models (GLMs) with Poisson or exponential link for spike counts
   - Deep neural networks (CNNs, RNNs) for nonlinear mappings
3. **Training**: Use a subset of data to learn the mapping.
4. **Evaluation**: Predict neural responses on held-out data and compute correlation (Pearson's r) or explained variance.

### 4. Stimulus Reconstruction

To test whether the dorsal stream encoding is sufficient to reconstruct the visual input:

1. Train an encoding model (as above) to predict neural activity from visual features.
2. Invert the model (or use a separate decoder) to estimate the visual features from neural activity.
3. Optimize to find the image or video that maximizes the likelihood of the observed neural responses.
4. Evaluate the similarity between the original and reconstructed stimuli (e.g., using pixel correlation, feature similarity, or human judgments).

### 5. Comparison with Ventral Stream

Compare your models from STS with those from ventral stream areas (e.g., V4, IT) to understand hierarchical processing differences.

## References and Resources

- **Paper**: [arXiv:2607.15631](https://arxiv.org/abs/2607.15631)
- **References**:
  - `references/stsbench-abstract.md`: Full abstract and metadata
  - `references/stsbench-methods.md`: Summary of methods (optional)
- **Scripts**: None currently provided (data acquisition and processing are highly dependent on the specific dataset format)

## Activation Keywords

- STS
- dorsal stream
- superior temporal sulcus
- neural encoding
- stimulus reconstruction
- macaque vision
- large-scale neural dataset
- NeurIPS 2025

## Notes

- The dataset is proprietary and must be obtained directly from the authors.
- Ensure compliance with any data use agreements and ethical guidelines for primate research.
- This skill focuses on the conceptual use of the dataset; specific implementation details will depend on the data format provided.