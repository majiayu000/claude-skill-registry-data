---
name: arch-governance
description: Use ArchUnit for checking the architecture of your Java code.
---

## Introduction

ArchUnit is a free, simple and extensible library for checking the architecture of your Java code. That is, ArchUnit can
check dependencies between packages and classes, layers and slices, check for cyclic dependencies and more. It does so
by analyzing given Java bytecode, importing all classes into a Java code structure. ArchUnit’s main focus is to
automatically test architecture and coding rules, using any plain Java unit testing framework.

## When to Use This Skill

- Use ArchUnit when you want to ensure that your Java code adheres to a specific architecture and coding rules. It is
  particularly useful for large projects with complex dependencies and for enforcing architectural principles across the
  codebase.
- When you need to verify that your codebase follows certain architectural guidelines, such as separation of concerns,
  clean architecture, or domain-driven design principles.
- When you require automated testing of architecture and coding rules to maintain code quality and consistency.
- When you are creating a whole new project or refactoring an existing codebase to enforce architectural principles.

## Installation

### Working with JUnit 4

```xml

<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit4</artifactId>
    <version>1.4.1</version>
    <scope>test</scope>
</dependency>
```

### Working with JUnit 5

```XML

<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.4.1</version>
    <scope>test</scope>
</dependency>
```

### Working with Other Test Frameworks

```XML

<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit</artifactId>
    <version>1.4.1</version>
    <scope>test</scope>
</dependency>
```

### Maven Plugin

There exists a Maven plugin to run ArchUnit rules straight from Maven. For more information see
references/arch-unit-maven-plugin.md

## Resources

> Do not expand the references directory all at once, but rather expand it layer by layer, as needed.

- [Examples](references/archUnit-examples)
- [ArchUnit GitHub Repository](https://github.com/TNG/ArchUnit)
- [ArchUnit Documentation](https://www.archunit.org/userguide)
