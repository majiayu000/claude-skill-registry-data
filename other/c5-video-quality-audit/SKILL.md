---
name: c5-video-quality-audit
display_name: "Auditoría de Calidad y Compresión de Video (PSNR/SSIM/VMAF)"
description: "Auditoría cuantitativa de compresión y fidelidad de video comparando secuencias cuadro a cuadro mediante PSNR, SSIM y VMAF, con generación de reportes HTML interactivos. Dispara con \"calidad de video\", \"psnr ssim\", \"diferencia de compresion\", \"video quality diff\", \"auditoría de compresion\"."
---

# Skill: C5 Video Quality & Compression Audit

Este protocolo audita cuantitativamente la fidelidad visual y degrados introducidos por códecs de video (H.264, HEVC, AV1, ProRes) comparando un video fuente (Reference) contra un video procesado (Distorted) cuadro a cuadro.

---

## 1. Métricas de Calidad Visual

### 1.1. Peak Signal-to-Noise Ratio (PSNR)

Dada la imagen de referencia $R$ y la distorsionada $D$ de dimensiones $M \times N$:

$$ MSE = \frac{1}{M \cdot N} \sum_{i=0}^{M-1} \sum_{j=0}^{N-1} [R(i,j) - D(i,j)]^2 $$

$$ PSNR = 10 \cdot \log_{10} \left( \frac{MAX_I^2}{MSE} \right) $$

### 1.2. Structural Similarity Index Measure (SSIM)

$$ SSIM(x,y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)} $$

Donde $\mu$, $\sigma^2$ y $\sigma_{xy}$ representan la media, varianza y covarianza local del brillo y contraste.

---

## 2. Pipeline de Auditoría Ffmpeg / Python

```bash
# Cálculo determinista de PSNR y SSIM cuadro a cuadro
ffmpeg -i distorted.mp4 -i reference.mp4 -filter_complex "[0:v][1:v]psnr=stats_file=psnr.log;[0:v][1:v]ssim=stats_file=ssim.log" -f null -
```

---

## 3. Entregable: Reporte HTML Interactivo

El resultado genera un panel interactivamente navegable cuadro a cuadro:
- Gráfico temporal de curva PSNR / SSIM / VMAF por frame.
- Selector de fotograma con visualizador A/B Split-Slider.
- Mapa de calor de residuos $|R(i,j) - D(i,j)|$ resaltando artefactos de compresión y micro-bloques.
