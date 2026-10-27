---
name: mongodb-modeling
description: "MongoDB document modeling, embedding vs referencing, compound indexes, and aggregation pipelines."
---

# MongoDB Data Modeling Protocol

1. Embed data that is queried together and updated atomically; reference data for unbounded growth.
2. Ensure all aggregation queries begin with an indexed $match stage.
3. Prevent unbounded array growth to stay well beneath the 16MB document limit.
