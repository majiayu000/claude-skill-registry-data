---
name: TCTB
description: Evaluates the throughput and resource allocation efficiency of RIS-aided mobile edge computing systems by measuring the total computation task bits successfully completed under varying network conditions. Use when the user has predictions and gold and needs to compute TCTB.
metadata:
  skill_kind: metric
  source_arxiv: 2102.07384
  bibtex_key: hu2021rismec
  confidence: high
---

# TCTB

> Reconfigurable Intelligent Surface Aided Mobile Edge Computing: From Optimization-Based to Location-Only Learning-Based Solutions — Hu et al. (2021) (arXiv:2102.07384, 2021)

## What this evaluates

Evaluates the throughput and resource allocation efficiency of RIS-aided mobile edge computing systems by measuring the total computation task bits successfully completed under varying network conditions.

## Datasets

- **Simulated RIS-MEC Environment** — total ?; splits: (unstated)

## Metrics

- `TCTB` **(primary)** — range: other
  - Total Completed Task-input Bits. It represents the sum of successfully computed task bits across all user equipments (UEs), maximized by jointly optimizing RIS reflecting coefficients, AP beamforming, and UE energy partition.

## Input / output format

**Input**: System configuration parameters including UE locations, channel state information (CSI) or location-only features, number of AP antennas (M), number of UEs (N), and uniform energy budget (E).

**Output**: Optimized resource allocation vectors: RIS phase-shift coefficients, AP receive beamforming weights, and UE energy allocation ratios for local computing versus offloading.

## Scoring recipe

```python
def evaluate_tctb(scheme, params):
    channels = generate_rician_channels(params)
    alloc = scheme.run(channels, params)
    bits_per_ue = [compute_ue_bits(ue, alloc, channels) for ue in params.ues]
    return sum(bits_per_ue)
```

## Common pitfalls

- TCTB values are highly sensitive to the Rician K-factors and path loss exponents, which are scenario-dependent.
- The metric assumes ideal synchronization and ignores practical hardware impairments beyond the explicitly modeled CSI/location uncertainty.
- Direct comparisons with other MEC literature are invalid as they typically optimize for different objectives like energy efficiency or latency.

## Evidence (verbatim from paper)

> In this section, simulation results are given to verify the effectiveness and performance improvement of the proposed BCD optimization algorithm as well as the CSI-based and location-only deep learning architectures. In addition, the effectiveness and robustness of the two proposed deep learning methods to the corrupted input features of CSI and UEs’ locations with uncertainty is also validated by simulations. ... we first show the TCTB of all the considered schemes w.r.t. the UEs’ uniform energy budget... The performance in terms of TCTB versus the number of the AP’s antennas is presented... we study the effects of the number of UEs, i.e., N, on the system performance of TCTB.

## Citation

```bibtex
@misc{hu2021rismec,
  title={Reconfigurable Intelligent Surface Aided Mobile Edge Computing: From Optimization-Based to Location-Only Learning-Based Solutions},
  author={Hu et al. (2021)},
  year={2021},
  note={arXiv:2102.07384}
}
```

- arXiv: 2102.07384
