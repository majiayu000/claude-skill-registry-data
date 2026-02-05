---
name: frappe-web-form-builder
description: Generate Frappe Web Forms for public-facing forms. Use when creating customer portals, registration forms, surveys, or public data collection forms.
---

# Frappe Web Form Builder

Generate public-facing web forms with validation, file uploads, and integration with Frappe DocTypes.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to create public forms
- User needs customer-facing forms
- User mentions web forms, surveys, or registration
- User wants portal functionality
- User needs forms without login

## Capabilities

### 1. Web Form JSON

**Customer Registration Form:**
```json
{
  "name": "Customer Registration",
  "route": "customer-registration",
  "title": "Register as Customer",
  "doc_type": "Customer",
  "is_standard": 0,
  "login_required": 0,
  "allow_multiple": 1,
  "show_sidebar": 0,
  "success_url": "/thank-you",
  "success_message": "Registration successful! We'll contact you soon.",
  "introduction_text": "Please fill in your details to register",
  "web_form_fields": [
    {
      "fieldname": "customer_name",
      "label": "Full Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "email_id",
      "label": "Email",
      "fieldtype": "Data",
      "options": "Email",
      "reqd": 1
    },
    {
      "fieldname": "mobile_no",
      "label": "Phone",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "customer_group",
      "label": "Type",
      "fieldtype": "Select",
      "options": "Individual\nCompany",
      "reqd": 1
    },
    {
      "fieldname": "company_name",
      "label": "Company Name",
      "fieldtype": "Data",
      "depends_on": "eval:doc.customer_group=='Company'"
    }
  ]
}
```

### 2. Multi-Step Form

**Multi-Page Web Form:**
```json
{
  "name": "Job Application",
  "is_multi_step": 1,
  "web_form_fields": [
    {
      "fieldname": "step_1",
      "fieldtype": "Section Break",
      "label": "Personal Information"
    },
    {"fieldname": "full_name", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "email", "fieldtype": "Data", "options": "Email", "reqd": 1},

    {
      "fieldname": "step_2",
      "fieldtype": "Section Break",
      "label": "Experience"
    },
    {"fieldname": "years_experience", "fieldtype": "Int"},
    {"fieldname": "current_company", "fieldtype": "Data"},

    {
      "fieldname": "step_3",
      "fieldtype": "Section Break",
      "label": "Documents"
    },
    {"fieldname": "resume", "fieldtype": "Attach", "reqd": 1}
  ]
}
```

## References

**Web Form Implementation:**
- Web Form DocType: https://github.com/frappe/frappe/tree/develop/frappe/website/doctype/web_form
- Web Form Controller: https://github.com/frappe/frappe/blob/develop/frappe/website/doctype/web_form/web_form.py
