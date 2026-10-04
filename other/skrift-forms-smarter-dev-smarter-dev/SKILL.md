---
name: skrift-forms
description: "Skrift form system — Pydantic-backed forms with CSRF protection, template rendering, and hook integration."
---

# Skrift Form System

Skrift forms combine Pydantic validation with CSRF protection, template rendering, and hook integration.

## Architecture

```
FormModel/BaseModel → Form(model, request) → validate() → hooks → data
      │                      │                    │           │
      │                      │                    │           ├─ form_{name}_validated
      │                      │                    │           └─ form_validated
      │                      │                    │
      │                      │                    ├─ CSRF verify (hmac.compare_digest)
      │                      │                    ├─ Token rotation (single-use)
      │                      │                    ├─ Checkbox injection (bool fields)
      │                      │                    └─ Pydantic validation
      │                      │
      │                      ├─ render() → Template("form", name).try_render()
      │                      ├─ csrf_field() → hidden input
      │                      ├─ fields → dict[str, BoundField]
      │                      └─ errors → dict[str, str]
      │
      └─ Registered in _form_registry (by form_name)
```

## Defining Forms

### FormModel (auto-registers)

```python
from skrift.forms import FormModel
from pydantic import Field, EmailStr

class ContactForm(FormModel, form_name="contact"):
    name: str
    email: EmailStr
    message: str = Field(json_schema_extra={"widget": "textarea"})
```

### @form() Decorator (registers a plain BaseModel)

```python
from pydantic import BaseModel
from skrift.forms import form

@form("newsletter", action="/subscribe", method="post")
class NewsletterForm(BaseModel):
    email: str
```

### Field Customization via `json_schema_extra`

| Key | Values | Purpose |
|-----|--------|---------|
| `label` | `str` | Custom label text |
| `widget` | `"textarea"`, `"select"`, `"checkbox"` | Widget type |
| `input_type` | `"email"`, `"password"`, etc. | HTML input type |
| `help_text` | `str` | Help text below field |
| `choices` | `list[tuple[str, str]]` | Options for select widget |
| `attrs` | `dict[str, str]` | Extra HTML attributes |

Full example:

```python
class ContactForm(FormModel, form_name="contact"):
    name: str = Field(json_schema_extra={
        "label": "Your Name",
        "attrs": {"placeholder": "Jane Doe"},
    })
    email: EmailStr = Field(json_schema_extra={
        "label": "Email Address",
        "input_type": "email",
        "help_text": "We'll never share your email.",
    })
    subject: str = Field(json_schema_extra={
        "widget": "select",
        "choices": [
            ("general", "General Inquiry"),
            ("support", "Technical Support"),
        ],
    })
    message: str = Field(json_schema_extra={
        "widget": "textarea",
        "attrs": {"rows": "6"},
    })
    subscribe: bool = Field(default=False, json_schema_extra={
        "label": "Subscribe to newsletter",
    })
```

## Controller GET/POST Pattern

```python
from litestar import Controller, get, post, Request
from litestar.response import Template as TemplateResponse, Redirect
from skrift.forms import Form

class ContactController(Controller):
    path = "/contact"

    @get("/")
    async def show(self, request: Request) -> TemplateResponse:
        form = Form(ContactForm, request)
        return TemplateResponse("contact.html", context={"form": form})

    @post("/")
    async def submit(self, request: Request) -> TemplateResponse | Redirect:
        form = Form(ContactForm, request)
        if await form.validate():
            # form.data is a validated ContactForm instance
            await process_contact(form.data)
            return Redirect("/contact?thanks=1")
        return TemplateResponse("contact.html", context={"form": form})
```

## Template Rendering

### Automatic

```html
{{ form.render() }}
{{ form.render(submit_label="Send") }}
```

### Manual

```html
<form method="{{ form.method }}">
    {{ form.csrf_field() }}
    {% for field in form %}
        {{ field.label_tag() }}
        {{ field.widget() }}
    {% endfor %}
    <button type="submit">Send</button>
</form>
```

### Custom Form Template

Template hierarchy: `form-{name}.html` → `form.html` → programmatic fallback.

```html
{# templates/form-contact.html #}
<form method="{{ form.method }}" class="contact-form">
    {{ form.csrf_field() }}

    {% if form.form_error %}
        <div class="alert">{{ form.form_error }}</div>
    {% endif %}

    <div class="row">
        <div class="col">
            {{ form['name'].label_tag() }}
            {{ form['name'].widget(class_="form-input") }}
        </div>
        <div class="col">
            {{ form['email'].label_tag() }}
            {{ form['email'].widget(class_="form-input") }}
        </div>
    </div>

    {{ form['message'].label_tag() }}
    {{ form['message'].widget(class_="form-input", rows="8") }}

    <button type="submit">{{ submit_label }}</button>
</form>
```

## CSRF Flow

1. `Form.__init__()` — Creates `secrets.token_urlsafe(32)` in session if absent (key: `_csrf_token`)
2. `csrf_field()` — Renders `<input type="hidden" name="_csrf" value="{token}">`
3. `validate()` — Checks submitted `_csrf` against session token via `hmac.compare_digest()`
4. Token rotation — New token generated after successful check (single-use)

## Registration Mechanism

Forms are registered in a global `_form_registry` dict (in `model.py`):
- `FormModel.__init_subclass__()` auto-registers on class creation
- `@form()` decorator registers explicitly
- `get_form_model(name)` retrieves by name, raises `LookupError` if missing

## Hook Integration

Two filter hooks fire after successful validation:

```python
# Form-specific: e.g. "form_contact_validated"
self.data = await hooks.apply_filters(f"form_{self.name}_validated", self.data)

# Global: "form_validated"
self.data = await hooks.apply_filters("form_validated", self.data, self.name)
```

Example hook:

```python
from skrift.lib.hooks import filter

@filter("form_contact_validated")
async def sanitize_contact(data):
    data.message = data.message.strip()
    return data

@filter("form_validated")
async def log_all_forms(data, name):
    print(f"Form '{name}' submitted")
    return data
```

## Jinja2 Global

The `Form` class is registered as a Jinja2 global, making it accessible in templates without passing it through context.

## Key Files

| File | Purpose |
|------|---------|
| `skrift/forms/core.py` | `Form` — CSRF, validation, rendering |
| `skrift/forms/model.py` | `FormModel` base class, `_form_registry`, `get_form_model()` |
| `skrift/forms/fields.py` | `BoundField` — field bound to form instance |
| `skrift/forms/decorators.py` | `@form()` decorator |
| `skrift/templates/form.html` | Default form template |
