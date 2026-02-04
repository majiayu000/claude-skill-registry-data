---
name: slide-gen-assembly
description: "Brand-specific PowerPoint building with python-pptx. Supports multiple templates, custom layouts, and programmatic slide generation."
version: "2.0.0"
author: "davistroy"
---

# PowerPoint Assembly Skill

Builds final PowerPoint presentations with brand-specific templates.

## Capabilities

- **Brand Templates**: CFA, Stratfield (extensible)
- **Multiple Content Types**: Text, bullets, tables, images, code blocks
- **Programmatic Control**: Full python-pptx integration
- **Cross-Platform**: Windows, macOS, Linux

## Usage

```bash
python -m plugin.cli build-presentation content.md --template stratfield
```

## Available Templates

| Template   | Description           | Use Case                   |
|------------|-----------------------|----------------------------|
| cfa        | Chick-fil-A branding  | CFA-specific presentations |
| stratfield | Stratfield Consulting | Client deliverables        |

## Adding Custom Templates

1. Create template file: `plugin/templates/mytemplate/template.py`
2. Implement template class extending `TemplateBase`
3. Register in template package `__init__.py`

```python
from plugin.lib.presentation.template_base import TemplateBase
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

class MyTemplate(TemplateBase):
    def __init__(self):
        super().__init__()
        self.primary_color = RGBColor(0x2E, 0x5E, 0xAA)
        self.font_family = "Arial"

    def build_title_slide(self, prs, title, subtitle):
        # Implementation
        pass
```

## Output

Generates `.pptx` file compatible with:

- Microsoft PowerPoint 2016+
- Google Slides (import)
- LibreOffice Impress
- Apple Keynote (import)
