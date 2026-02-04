---
name: data-model-reporter
description: Standards for generating Model Cards from data analysis notebooks. Aligned with Hugging Face and ISO transparency standards.
---

# Skill: Model Card Reporter

This skill defines the standard for generating **Model Cards** from data analysis notebooks. It aligns with **Hugging Face** and **Google** standards to ensure transparency, reproducibility, and ethical reporting.

---

## 💎 1. Core Principles

1.  **Standard Alignment**:
    - Follows the Hugging Face Model Card structure (YAML Metadata + Markdown Sections).
    - Must include "Ethical Considerations" and "Limitations".
2.  **Evidence-Based**:
    - All metrics (Accuracy, F1, etc.) must be extracted directly from the notebook execution results.
    - No hallucinated metrics.
3.  **Neutral Tone**:
    - Use objective language. Avoid marketing buzzwords like "Superb", "Perfect".
    - Acknowledge biases and limitations honestly.

---

## 🏗️ 2. Report Structure

The output must follow `report-template.md`.

### Metadata (YAML Frontmatter)
Essential for machine readability (Hugging Face Hub compatibility).
- `language`: (e.g., en, ko)
- `library_name`: (e.g., sklearn, pytorch)
- `tags`: (e.g., tabular-classification, finance)
- `metrics`: (e.g., accuracy, f1)

### Section 1: Model Details
- **Architecture**: Algorithm used (e.g., Random Forest, BERT).
- **Framework**: Version info (e.g., Scikit-Learn 1.0.2).
- **Author**: Developer or Team name.

### Section 2: Intended Use
- **Primary Use**: What specific problem does this solve?
- **Out of Scope**: When should this model NOT be used? (Crucial for safety).

### Section 3: Factors & Metrics
- **Factors**: Input features used. Highlight key drivers (SHAP values, feature importance).
- **Metrics**: Quantitative performance on Test/Validation sets.

### Section 4: Ethical Considerations (Critical)
- **Bias**: Are there protected groups (gender, race) that might be unfairly treated?
- **Fairness**: Disparate impact analysis results.

---

## 🏆 3. Quality Standards

1.  **Metric Integrity**:
    - REPORTED metrics MUST MATCH valid execution outputs.
    - If code failed to run, do NOT guess the number. Mark as "N/A".
2.  **Disclosure**:
    - Always disclose the 'Out of Scope' use cases to prevent misuse.
    - Always mention the framework version for reproducibility.

## ✅ 4. Checklist

- [ ] **Extraction**: Did you find the model object and training metrics?
- [ ] **Completeness**: Are all 5 sections of the template filled?
- [ ] **Safety Check**: Is 'Out of Scope' clearly defined?
- [ ] **Verification**: Did you explicitly warn the user to review the 'Ethical Considerations'?

