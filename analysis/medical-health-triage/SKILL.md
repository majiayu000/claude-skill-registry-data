---
name: medical-health-triage
description: Clinical health triage and biomedical literature synthesizer. Analyzes clinical trial registries, structures differential health insights, cross-checks drug contraindications, and explains complex lab biomarkers for patients and clinicians.
version: 3.0.0
author: AgentBoost Life Sciences & Health
enterprise: true
category: Healthcare & Life Sciences
---

### System Instructions
You are equipped with the `medical-health-triage` autonomous agent. This agent assists healthcare researchers, clinical professionals, and individuals by structuring medical symptoms into differential categories, referencing clinical trial efficacy databases, auditing drug-drug contraindication matrices, and explaining biomarker lab results in clear, structured language.

**CRITICAL RULE:** Always provide an explicit clinical disclaimer. Emphasize that automated analysis is for decision-support and educational synthesis only, and never supersedes formal medical diagnosis or emergency services.

### Execution Protocol
Invoke the clinical triage engine by passing strictly formatted JSON:

```json
{
  "query": "Elevated fasting blood glucose and HbA1c threshold analysis",
  "patient_profile": {
    "age": 48,
    "gender": "male",
    "known_conditions": ["hypertension"],
    "current_medications": ["Lisinopril 10mg"]
  },
  "lab_biomarkers": {
    "fasting_glucose_mg_dl": 118,
    "hba1c_percent": 6.1
  }
}
```

JSON Schema Specification

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Primary clinical question, lab result summary, or symptom complaint.",
      "default": "Elevated fasting blood glucose and HbA1c threshold"
    },
    "patient_profile": {
      "type": "object",
      "properties": {
        "age": { "type": "number" },
        "gender": { "type": "string" },
        "known_conditions": { "type": "array", "items": { "type": "string" } },
        "current_medications": { "type": "array", "items": { "type": "string" } }
      }
    },
    "lab_biomarkers": {
      "type": "object",
      "description": "Key lab values and biomarker results."
    }
  },
  "required": ["query"]
}
```

Outputs

  - Differential Considerations: Categorized medical possibilities ranked by
    clinical literature prevalence.
  - Biomarker Interpretation: Evaluation of lab values against reference
    intervals (e.g., normal, borderline, diagnostic).
  - Drug Interaction Screening: Known interactions or contraindications between
    current medications.
  - Evidence-Based Next Steps: Actionable questions for the patient's primary
    care physician and lifestyle protocol guidance.

Example Tool Call

run_js(data='{"query": "Sudden onset chest tightness and shortness of breath during exertion", "patient_profile": {"age": 55, "gender": "female"}}')

Integration Points

  - Knowledge Hub Curator: Indexes relevant clinical research papers and
    treatment guidelines.
  - Student Learning Mentor: Deconstructs biological pathways (e.g., insulin
    signaling, GLUT-4 transporters) for medical students.
