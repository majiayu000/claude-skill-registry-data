---
name: Model Risk Management
description: Identifying, assessing, and mitigating risks associated with the use of machine learning models in business processes.
---

# Model Risk Management (MRM)

## Overview

Model Risk Management (MRM) is a framework designed to manage the risk of adverse consequences resulting from decisions based on incorrect or misused model outputs. While software engineering focuses on "bugs," MRM focuses on **"Model Errors"**—mathematically correct but contextually wrong predictions.

**Core Principle**: "All models are wrong, but some are dangerous. Manage the danger."

---

## 1. The Three Lines of Defense (Governance)

MRM is traditionally structured to ensure objectivity and accountability.

| Line | Owner | Responsibility |
| :--- | :--- | :--- |
| **First Line** | Data Scientists / ML Engineers | Build, test, and document the model. |
| **Second Line** | Model Validation Team | Independent review and challenge of the model. |
| **Third Line** | Internal Audit | Verify the entire MRM process is being followed. |

---

## 2. Risk Identification (The SR 11-7 Standard)

Based on the **Federal Reserve SR 11-7** guidance, model risk arises from two primary sources:

1.  **Fundamentally Flawed Models**: Errors in theory, data, or math (e.g., using a linear model for a non-linear problem).
2.  **Model Misuse**: Using a model for a purpose it wasn't designed for (e.g., using a high-income spending model to predict low-income credit risk).

---

## 3. Model Inventory Management

You cannot manage risk if you don't know what models you have.

### Mandatory Inventory Fields:
*   **Model ID**: Unique identifier.
*   **Owner**: The business unit responsible.
*   **Tier**: Criticality (High, Medium, Low).
*   **Intended Use**: What problem does it solve?
*   **Dependencies**: What data feeds into it? What systems consume it?
*   **Last Validated**: Date of the last independent audit.

---

## 4. Model Performance Monitoring

Models decay over time. MRM requires monitoring for:

*   **Data Drift**: Input distribution changes (e.g., users get younger).
*   **Concept Drift**: The relationship between input and output changes (e.g., spending habits shift during a recession).
*   **Model Degradation**: Accuracy, Precision, or Recall drops below a predefined threshold.
*   **Stability**: Does the model produce wildly different results for slightly different inputs (Adversarial vulnerability)?

---

## 5. Stress Testing and Scenario Analysis

"Stress testing" the model means testing its performance in extreme, unlikely conditions.

| Scenario | Goal |
| :--- | :--- |
| **Black Swan Event** | How does the model behave during a market crash or pandemic? |
| **Data Corruption** | What happens if a key feature becomes 100% null? |
| **Adversarial Input** | Can a user "jailbreak" the model to get a specific outcome? |
| **Scaling Stress** | Does performance degrade if traffic increases 10x? |

---

## 6. Model Validation Workflow

1.  **Theoretical Review**: Does the math make sense?
2.  **Implementation Review**: Is the code consistent with the math?
3.  **Data Quality Audit**: Is the training data clean and representative?
4.  **Backtesting**: Running the model on historical data to see if it would have predicted the past correctly.
5.  **Benchmarking**: Comparing the model against a simple baseline (e.g., "Always predict the Mean").

---

## 7. Model Retirement and Sunsetting

Models should not live forever.

*   **Triggers for Retirement**: New model version available, performance below threshold, or business use case no longer exists.
*   **Clean Shutdown**: Ensure all downstream systems have migrated to the new model before killing the old API.
*   **Post-Mortem**: Document why the model was retired and what was learned.

---

## 8. Real-World Failure: Zillow Offers
*   **Scenario**: Zillow's "iBuying" model was designed to predict home values and buy houses automatically.
*   **Failure**: The model failed to account for rapid shifts in the housing market and renovation costs. It began "overbidding" on houses that it couldn't sell at a profit.
*   **Outcome**: Zillow shut down the business, laid off 2,000 people, and took a **$500 million write-down**.
*   **MRM Lesson**: Excessive confidence in a model's "black box" output without independent human oversight and market-condition checks is a high-risk activity.

---

## 9. Model Risk Management Checklist

- [ ] **Inventory**: Is the model registered in the central repository?
- [ ] **Tiering**: Have we classified this model's risk (e.g., High-Risk if it impacts credit)?
- [ ] **Validation**: Has someone *other than the builder* reviewed the model?
- [ ] **Documentation**: Do we have a "Model Whitepaper" explaining the theory?
- [ ] **Monitoring**: Are there automated alerts for accuracy drops > 5%?
- [ ] **Retirement**: Is there a 12-month review scheduled to consider model replacement?
- [ ] **Adversarial**: Have we tested for robustness against malicious prompts/inputs?

---

## Related Skills
* `44-ai-governance/model-registry`
* `44-ai-governance/ai-ethics-compliance`
* `40-system-resilience/failure-modes`
