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

## 2. Do not use `docker-compose`

The usage of `docker-compose` has been deprecated and in some cases it doesn't work anymore.
Please replace `docker-compose` with `docker compose` everywhere, namely in `bash` scripts, `Makefile` and `Makefile.mk` files, `.md` files, all kinds of Markdown files, and other files you may find it.
Leave all binary files untouched.

## 3. Checklist

[] No Dockerfile should use older Java version images
[] No Testcontainers code should use older Java version images
