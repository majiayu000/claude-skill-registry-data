---
name: docker
description: Conventions for docker
---

## 1. Update eclipse temurin image usages to the latest java version.

### Example 1:

If the latest java version is `25`and there is an image being used like:

```dockerfile
FROM eclipse-temurin:21-alpine
```

Then it should be updated to:

```dockerfile
FROM eclipse-temurin:25-alpine
```

### Example 2:

This example is only valid for CircleCI configuration files located in `.circleci/config.yml`.
Replace this:

```yml
    docker:
      - image: eclipse-temurin:21-alpine
```

with:

```yml
    docker:
      - image: eclipse-temurin:25-alpine
```

## 2. Checklist

[] No Dockerfile should use older Java version images
[] No Testcontainers code should use older Java version images
