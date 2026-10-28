---
name: Java Enterprise Edition Frameworks
description: Conventions for using in all JEE frameworks. These are common standards for CDI
---

## 1. Correct annotation usage for use-site targets

Constructor params annotated with `@Claim` should be injected with use-site target `param` as `@param:Claim`
