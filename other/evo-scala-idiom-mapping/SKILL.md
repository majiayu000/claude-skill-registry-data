---
name: evo-scala-idiom-mapping
description: Maps Python constructs to idiomatic Scala 2.13 equivalents.
---
# evo-scala-idiom-mapping
Maps Python→Scala: enum→sealed trait, dataclass→case class, ABC→trait, snake_case→camelCase, Optional→Option, datetime→java.time, Decimal→BigDecimal, Generic variance (+/-), collections.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-scala-idiom-mapping/scripts')
from idiom_mapper import snake_to_camel, map_python_type_to_scala
```
