---
description: Imported skill __init__ from anthropic
name: __init__
signature: 83e0f035c5abea238d3f2c3968afbd511ed022b527b7c9cb60a9434cc34ff987
source: /a0/tmp/skills_research/anthropic/skills/pptx/ooxml/scripts/validation/__init__.py
---

"""
Validation modules for Word document processing.
"""

from .base import BaseSchemaValidator
from .docx import DOCXSchemaValidator
from .pptx import PPTXSchemaValidator
from .redlining import RedliningValidator

__all__ = [
    "BaseSchemaValidator",
    "DOCXSchemaValidator",
    "PPTXSchemaValidator",
    "RedliningValidator",
]
