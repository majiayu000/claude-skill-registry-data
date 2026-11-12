---
name: architect-4c
description: Use only when explicitly invoked. Core concepts, level definitions, principles, and common mistakes in Simon Brown's C4 model.
metadata:
  language: en
  translation_of: architect-4c-cn
  version: "0.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/architect-4c
---

# C4 software architecture model

## Core concepts and definitions

C4 is Simon Brown's software architecture model. A software system contains containers, containers contain components, and code elements implement components.

| Level | Definition |
|---|---|
| Context | One software system, its direct users, and external collaborators. |
| Container | An application or data store within a system, forming a runtime boundary for code execution or data storage. |
| Component | A unit of functionality with an explicit interface inside one container, typically deployed with that container. |
| Code | The classes, interfaces, functions, or data structures implementing one component. |

A person represents a role interacting with the system. An external system is outside the current system boundary and may belong to the same organization.

A system landscape describes relationships across systems. A dynamic view describes interaction order within a scenario. A deployment view maps container instances to infrastructure in a particular environment. These are supporting views.

## Principles

Based on the [C4 website](https://c4model.com/) and its [diagram definitions](https://c4model.com/diagrams).

- Use hierarchical abstractions and expand through system, container, component, and code containment.
- Choose levels for the audience. There is no requirement to use all four.
- Keep the model independent of notation.
- Keep the model independent of tooling.

## Avoiding mistakes

- A C4 container is distinct from a Docker container, virtual machine, source folder, or library.
- Identify components by responsibility and interface, rather than folder or class names alone.
- Code is level four. Deployment and dynamic diagrams do not replace it.
- Multiple deployed instances of one logical container still map to one container.
- Distinguish runtime calls, source dependencies, and data flows.
- Separate current state, target design, and inference. Leave unsupported structures and relationships unconfirmed.
