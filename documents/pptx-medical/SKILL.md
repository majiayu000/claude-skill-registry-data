---
name: pptx-medical
description: Medical PowerPoint presentation generation with clinical data visualization. Creates professional presentations from FHIR resources, lab results, and clinical data. Use when generating patient summaries, care plans, medical reports, or clinical presentations with proper healthcare formatting.
license: MIT
allowed-tools:
  - python
  - javascript
  - bash
metadata:
  version: "1.0.0"
  category: healthcare
  output-format: "pptx"
  fhir-aware: "true"
---

# Medical PowerPoint Generation Skill

## Overview

This skill enables Claude to create professional medical PowerPoint presentations from clinical data, FHIR resources, lab results, and patient information. Designed specifically for healthcare workflows with HIPAA-compliant templates.

## When to Use This Skill

Use this skill when you need to:
- Generate patient summary presentations
- Create clinical care plan slides
- Visualize lab results and trends
- Build medical report presentations
- Design medication management slides
- Create discharge summary presentations

## Core Capabilities

### 1. Medical Presentation Templates

```python
MEDICAL_TEMPLATES = {
    "patient_summary": {
        "title_slide": True,
        "demographics": True,
        "vital_signs": True,
        "medications": True,
        "diagnoses": True,
        "lab_results": True
    },
    "lab_results": {
        "title_slide": True,
        "test_summary": True,
        "trend_charts": True,
        "reference_ranges": True
    },
    "care_plan": {
        "title_slide": True,
        "current_conditions": True,
        "treatment_plan": True,
        "medications": True,
        "follow_up": True
    }
}
```

### 2. Healthcare Color Palettes

```python
HEALTHCARE_PALETTES = {
    "clinical_blue": {
        "primary": "#1E3A8A",      # Deep blue
        "secondary": "#3B82F6",    # Blue
        "accent": "#60A5FA",       # Light blue
        "background": "#F8FAFC",   # Off-white
        "text": "#1E293B"          # Dark gray
    },
    "medical_green": {
        "primary": "#047857",      # Green
        "secondary": "#059669",    # Emerald
        "accent": "#10B981",       # Light green
        "background": "#F0FDF4",   # Light green bg
        "text": "#064E3B"          # Dark green
    },
    "health_purple": {
        "primary": "#6B21A8",      # Purple
        "secondary": "#9333EA",    # Violet
        "accent": "#A78BFA",       # Light purple
        "background": "#FAF5FF",   # Light purple bg
        "text": "#581C87"          # Dark purple
    },
    "professional_gray": {
        "primary": "#374151",      # Gray
        "secondary": "#6B7280",    # Medium gray
        "accent": "#9CA3AF",       # Light gray
        "background": "#F9FAFB",   # Off-white
        "text": "#111827"          # Black
    }
}
```

### 3. Create Title Slide

```python
from pptxgenjs import PptxGenJS

def create_medical_title_slide(prs, title_data, palette="clinical_blue"):
    """Create professional medical presentation title slide"""
    colors = HEALTHCARE_PALETTES[palette]
    
    slide = prs.add_slide()
    
    # Header banner
    slide.add_shape("rect", {
        "x": 0, "y": 0,
        "w": "100%", "h": 1.5,
        "fill": colors["primary"]
    })
    
    # Title
    slide.add_text(title_data.get("title", "Patient Summary"), {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 1,
        "fontSize": 44,
        "bold": True,
        "color": "#FFFFFF",
        "fontFace": "Arial"
    })
    
    # Subtitle
    slide.add_text(title_data.get("subtitle", "Clinical Report"), {
        "x": 0.5, "y": 1.8,
        "w": 9, "h": 0.5,
        "fontSize": 24,
        "color": colors["secondary"],
        "fontFace": "Arial"
    })
    
    # Date and facility
    slide.add_text(
        f"Date: {title_data.get('date', '')}\n" +
        f"Facility: {title_data.get('facility', 'Medical Center')}",
        {
            "x": 0.5, "y": 6.5,
            "w": 4, "h": 0.8,
            "fontSize": 14,
            "color": colors["text"],
            "fontFace": "Arial"
        }
    )
    
    # HIPAA notice
    slide.add_text(
        "CONFIDENTIAL - Protected Health Information",
        {
            "x": 5.5, "y": 6.9,
            "w": 4, "h": 0.4,
            "fontSize": 10,
            "color": "#DC2626",
            "italic": True,
            "fontFace": "Arial"
        }
    )
    
    return slide
```

### 4. Patient Demographics Slide

```python
def create_demographics_slide(prs, patient_data, palette="clinical_blue"):
    """Create patient demographics slide from FHIR Patient resource"""
    colors = HEALTHCARE_PALETTES[palette]
    slide = prs.add_slide()
    
    # Title
    slide.add_text("Patient Demographics", {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 0.7,
        "fontSize": 36,
        "bold": True,
        "color": colors["primary"],
        "fontFace": "Arial"
    })
    
    # Patient info table
    demographics = [
        ["Field", "Value"],
        ["Name", patient_data.get("name", "")],
        ["MRN", patient_data.get("mrn", "")],
        ["Date of Birth", patient_data.get("birth_date", "")],
        ["Age", str(patient_data.get("age", ""))],
        ["Gender", patient_data.get("gender", "")],
        ["Phone", patient_data.get("phone", "")],
        ["Address", patient_data.get("address", "")]
    ]
    
    slide.add_table(demographics, {
        "x": 1.5, "y": 1.5,
        "w": 7, "h": 4,
        "fontSize": 16,
        "fontFace": "Arial",
        "border": {"pt": 1, "color": colors["secondary"]},
        "fill": {
            "color": colors["background"],
            "transparency": 50
        },
        "color": colors["text"]
    })
    
    return slide
```

### 5. Medications List Slide

```python
def create_medications_slide(prs, medications, palette="clinical_blue"):
    """Create medications list from FHIR MedicationRequest resources"""
    colors = HEALTHCARE_PALETTES[palette]
    slide = prs.add_slide()
    
    # Title
    slide.add_text("Current Medications", {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 0.7,
        "fontSize": 36,
        "bold": True,
        "color": colors["primary"],
        "fontFace": "Arial"
    })
    
    # Medications table
    med_data = [["Medication", "Dosage", "Frequency", "Route"]]
    
    for med in medications:
        med_data.append([
            med.get("name", ""),
            med.get("dosage", ""),
            med.get("frequency", ""),
            med.get("route", "PO")
        ])
    
    slide.add_table(med_data, {
        "x": 0.8, "y": 1.5,
        "w": 8.4, "h": 4.5,
        "fontSize": 14,
        "fontFace": "Arial",
        "border": {"pt": 1, "color": colors["secondary"]},
        "fill": {"color": colors["background"]},
        "color": colors["text"],
        "rowH": 0.5,
        "colW": [3, 1.8, 1.8, 1]
    })
    
    # Footer note
    slide.add_text(
        f"Total medications: {len(medications)}",
        {
            "x": 0.8, "y": 6.2,
            "w": 3, "h": 0.4,
            "fontSize": 12,
            "italic": True,
            "color": colors["text"],
            "fontFace": "Arial"
        }
    )
    
    return slide
```

### 6. Lab Results with Charts

```python
def create_lab_results_slide(prs, lab_results, palette="clinical_blue"):
    """Create lab results slide with trend visualization"""
    colors = HEALTHCARE_PALETTES[palette]
    slide = prs.add_slide()
    
    # Title
    slide.add_text("Laboratory Results", {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 0.7,
        "fontSize": 36,
        "bold": True,
        "color": colors["primary"],
        "fontFace": "Arial"
    })
    
    # Results table
    lab_data = [["Test", "Result", "Unit", "Reference Range", "Status"]]
    
    for lab in lab_results:
        status = "Normal"
        if lab.get("value", 0) > lab.get("ref_high", float('inf')):
            status = "High ⬆"
        elif lab.get("value", 0) < lab.get("ref_low", 0):
            status = "Low ⬇"
        
        lab_data.append([
            lab.get("test_name", ""),
            str(lab.get("value", "")),
            lab.get("unit", ""),
            f"{lab.get('ref_low', '')}-{lab.get('ref_high', '')}",
            status
        ])
    
    slide.add_table(lab_data, {
        "x": 0.5, "y": 1.5,
        "w": 9, "h": 4.5,
        "fontSize": 14,
        "fontFace": "Arial",
        "border": {"pt": 1, "color": colors["secondary"]},
        "fill": {"color": colors["background"]},
        "color": colors["text"],
        "colW": [2.5, 1.5, 1, 2, 1.5]
    })
    
    return slide
```

### 7. Vital Signs Trend Chart

```python
def create_vitals_chart_slide(prs, vitals_history, palette="clinical_blue"):
    """Create vital signs trend chart"""
    colors = HEALTHCARE_PALETTES[palette]
    slide = prs.add_slide()
    
    # Title
    slide.add_text("Vital Signs Trends", {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 0.7,
        "fontSize": 36,
        "bold": True,
        "color": colors["primary"],
        "fontFace": "Arial"
    })
    
    # Prepare chart data
    chart_data = {
        "labels": [v["date"] for v in vitals_history],
        "datasets": [
            {
                "name": "Blood Pressure (Systolic)",
                "values": [v.get("bp_systolic", 0) for v in vitals_history],
                "borderColor": colors["primary"],
                "backgroundColor": colors["primary"]
            },
            {
                "name": "Heart Rate",
                "values": [v.get("heart_rate", 0) for v in vitals_history],
                "borderColor": colors["accent"],
                "backgroundColor": colors["accent"]
            }
        ]
    }
    
    slide.add_chart("line", chart_data, {
        "x": 1, "y": 1.5,
        "w": 8, "h": 4.5,
        "title": "Vital Signs Over Time",
        "titleFontSize": 18,
        "titleColor": colors["text"],
        "showLegend": True,
        "legendPos": "r"
    })
    
    return slide
```

### 8. Diagnoses/Problems List

```python
def create_diagnoses_slide(prs, diagnoses, palette="clinical_blue"):
    """Create diagnoses list from FHIR Condition resources"""
    colors = HEALTHCARE_PALETTES[palette]
    slide = prs.add_slide()
    
    # Title
    slide.add_text("Active Diagnoses", {
        "x": 0.5, "y": 0.3,
        "w": 9, "h": 0.7,
        "fontSize": 36,
        "bold": True,
        "color": colors["primary"],
        "fontFace": "Arial"
    })
    
    # Diagnoses table
    dx_data = [["Diagnosis", "ICD-10", "Status", "Onset Date"]]
    
    for dx in diagnoses:
        dx_data.append([
            dx.get("name", ""),
            dx.get("icd10_code", ""),
            dx.get("clinical_status", "Active"),
            dx.get("onset_date", "")
        ])
    
    slide.add_table(dx_data, {
        "x": 0.8, "y": 1.5,
        "w": 8.4, "h": 4.5,
        "fontSize": 14,
        "fontFace": "Arial",
        "border": {"pt": 1, "color": colors["secondary"]},
        "fill": {"color": colors["background"]},
        "color": colors["text"],
        "colW": [4, 1.5, 1.5, 1.4]
    })
    
    return slide
```

## Complete Presentation Workflow

```python
def create_medical_presentation(fhir_data, template="patient_summary"):
    """Generate complete medical presentation from FHIR data"""
    prs = PptxGenJS()
    prs.layout = "LAYOUT_16x9"
    prs.author = "Doctors-Linc AI"
    prs.company = "Healthcare Organization"
    prs.subject = "Patient Medical Summary"
    
    # Choose color palette based on context
    palette = "clinical_blue"
    
    # Title slide
    title_slide = create_medical_title_slide(prs, {
        "title": "Patient Medical Summary",
        "subtitle": "Comprehensive Clinical Overview",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "facility": fhir_data.get("facility", "Medical Center")
    }, palette)
    
    # Demographics slide
    if "patient" in fhir_data:
        demographics_slide = create_demographics_slide(
            prs, fhir_data["patient"], palette
        )
    
    # Medications slide
    if "medications" in fhir_data:
        medications_slide = create_medications_slide(
            prs, fhir_data["medications"], palette
        )
    
    # Lab results slide
    if "lab_results" in fhir_data:
        lab_slide = create_lab_results_slide(
            prs, fhir_data["lab_results"], palette
        )
    
    # Vital signs chart
    if "vitals_history" in fhir_data:
        vitals_slide = create_vitals_chart_slide(
            prs, fhir_data["vitals_history"], palette
        )
    
    # Diagnoses slide
    if "diagnoses" in fhir_data:
        dx_slide = create_diagnoses_slide(
            prs, fhir_data["diagnoses"], palette
        )
    
    # Save presentation
    output_path = f"patient_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
    prs.write_file(output_path)
    
    return {
        "output_path": output_path,
        "slide_count": len(prs.slides),
        "template": template
    }
```

## Medical Chart Types

```python
MEDICAL_CHART_TYPES = {
    "vitals_trend": {
        "type": "line",
        "metrics": ["bp_systolic", "bp_diastolic", "heart_rate", "temperature"],
        "x_axis": "date",
        "title": "Vital Signs Trend"
    },
    "lab_comparison": {
        "type": "bar",
        "metrics": ["glucose", "hba1c", "cholesterol"],
        "x_axis": "test_name",
        "title": "Lab Results Comparison"
    },
    "medication_timeline": {
        "type": "gantt",
        "x_axis": "date",
        "y_axis": "medication_name",
        "title": "Medication Timeline"
    }
}
```

## HIPAA-Compliant Features

```python
def add_hipaa_footer(slide, colors):
    """Add HIPAA confidentiality notice to slide"""
    slide.add_text(
        "CONFIDENTIAL - Contains Protected Health Information (PHI) - " +
        "Unauthorized disclosure is prohibited by HIPAA",
        {
            "x": 0.5, "y": 7,
            "w": 9, "h": 0.4,
            "fontSize": 8,
            "color": "#DC2626",
            "italic": True,
            "align": "center",
            "fontFace": "Arial"
        }
    )

def add_watermark(slide, text="CONFIDENTIAL"):
    """Add watermark to slide"""
    slide.add_text(text, {
        "x": 2, "y": 3,
        "w": 6, "h": 2,
        "fontSize": 72,
        "color": "#E5E7EB",
        "rotate": -45,
        "transparency": 70,
        "align": "center",
        "valign": "middle",
        "fontFace": "Arial",
        "bold": True
    })
```

## Best Practices

1. **Always include HIPAA notices** on confidential slides
2. **Use clear visual hierarchy** - large titles, readable body text
3. **Choose appropriate color palettes** - clinical blue for general, green for wellness
4. **Include reference ranges** for lab results
5. **Show trends** - use charts for temporal data
6. **Limit data per slide** - 5-7 items maximum
7. **Add metadata** - dates, facility, report ID
8. **Use consistent formatting** across all slides

## Integration with Agents

This skill integrates with:
- **FHIR-Generator**: Receives FHIR resources
- **HEALTHCARELINC**: Receives structured medical data
- **Medical-OCR**: Can visualize OCR-extracted data

## Example Use Cases

1. **Patient Discharge Summary**: Demographics + Diagnoses + Medications + Follow-up
2. **Lab Results Report**: Trends + Current values + Reference ranges
3. **Medication Management**: Active meds + Changes + Adherence
4. **Care Team Handoff**: Patient summary + Recent events + Action items

---

**Version**: 1.0.0  
**Last Updated**: 2024-11-22  
**Output Format**: PPTX (PowerPoint)  
**Maintainer**: Doctors-Linc Development Team
